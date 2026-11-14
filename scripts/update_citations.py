#!/usr/bin/env python3
"""Update BibTeX citation_count fields from pasted Google Scholar text.

Usage: python3 scripts/update_citations.py [citation_number.txt] [--dry-run]
Input: optional TITLE/CITED BY/YEAR header, then three nonempty lines per
record (title, authors, venue followed by TAB count TAB year). Missing counts
are left unchanged, never interpreted as zero. No network or extra packages.
"""
import argparse
import html
from pathlib import Path
import re
import sys
import unicodedata

REPO = Path(__file__).resolve().parents[1]
ENTRY = re.compile(r'^@(?:article|conference|inproceedings|misc|book|incollection)\s*\{([^,]+),', re.M | re.I)
COUNT = re.compile(r'^[ \t]*citation_count\s*=\s*\{(\d+)\}\s*,?[ \t]*\n?', re.M | re.I)


def normalize(title):
    # Scholar appends this author suffix to the Cantera toolbox paper's title.
    title = re.sub(r':\s*Z\.\s*Li\s+et\s+al\.\s*$', '', title, flags=re.I)
    title = unicodedata.normalize('NFKD', html.unescape(title)).lower()
    return ''.join(c for c in title if c.isalnum())


def field(entry, name):
    match = re.search(r'\b' + re.escape(name) + r'\s*=\s*\{', entry, re.I)
    if not match:
        return None
    start = match.end()
    depth = 1
    for i in range(start, len(entry)):
        if entry[i] == '{' and (i == 0 or entry[i-1] != '\\'):
            depth += 1
        elif entry[i] == '}' and (i == 0 or entry[i-1] != '\\'):
            depth -= 1
            if depth == 0:
                return entry[start:i]
    raise ValueError(f'Unclosed {name} field')


def read_records(path):
    lines = [line.strip(' \r\n') for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    if lines and lines[0].strip().upper().startswith('TITLE') and 'YEAR' in lines[0].upper():
        lines.pop(0)
    if not lines or len(lines) % 3:
        raise ValueError('Expected three nonempty lines per record: title, authors, and venue<TAB>count<TAB>year.')
    records = []
    seen = set()
    for i in range(0, len(lines), 3):
        title = lines[i].strip()
        cells = lines[i+2].rsplit('\t', 2)
        if len(cells) != 3 or not re.fullmatch(r'\d{4}', cells[2].strip()):
            raise ValueError(f'Invalid count/year line for {title!r}; retain the tab separators from Scholar.')
        count = cells[1].strip().rstrip('*').strip()
        if count and not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)', count):
            raise ValueError(f'Invalid citation count for {title!r}: {count!r}')
        identity = (normalize(title), cells[2].strip())
        if identity in seen:
            raise ValueError(f'Duplicate source record: {title!r}; resolve it before updating.')
        seen.add(identity)
        records.append((title, int(count.replace(',', '')) if count else None, cells[2].strip()))
    return records


def update(input_path, bib_paths, dry_run=False):
    records = read_records(input_path)
    sources = {p: p.read_text(encoding='utf-8') for p in bib_paths}
    entries = []
    for path, source in sources.items():
        starts = list(ENTRY.finditer(source))
        for i, match in enumerate(starts):
            end = starts[i+1].start() if i+1 < len(starts) else len(source)
            block = source[match.start():end]
            title = field(block, 'title')
            if title:
                entries.append((path, match.start(), end, match[1], title, field(block, 'year'), block))
    edits = {p: [] for p in sources}
    matched = unchanged = skipped = 0
    used = set()
    for title, count, year in records:
        candidates = [e for e in entries if normalize(e[4]) == normalize(title)]
        if len(candidates) > 1:
            candidates = [e for e in candidates if e[5] == year]
        if len(candidates) != 1:
            print(f"SKIP ({'ambiguous' if candidates else 'not found'}): {title}")
            skipped += 1
            continue
        path, start, end, key, _, bib_year, block = candidates[0]
        if (path, key) in used:
            raise ValueError(f'Multiple source records match {key}; no files written.')
        used.add((path, key))
        if count is None:
            print(f'SKIP (blank count): {title}')
            skipped += 1
            continue
        matched += 1
        old = field(block, 'citation_count')
        if old is not None and old != str(count) and not COUNT.search(block):
            raise ValueError(f'Unsupported citation_count formatting in {key}; no files written.')
        if old == str(count):
            unchanged += 1
            continue
        if COUNT.search(block):
            changed = COUNT.sub(f'  citation_count = {{{count}}},\n', block, count=1)
        else:
            changed = block.replace('\n', f'\n  citation_count = {{{count}}},\n', 1)
        edits[path].append((start, end, changed))
        note = f' (Scholar year {year}; bibliography {bib_year} retained)' if bib_year != year else ''
        print(f'{key}: {old if old is not None else "unset"} -> {count}{note}')
    # Parse and validate everything before writing; unrelated fields stay intact.
    if not dry_run:
        for path, replacements in edits.items():
            if replacements:
                result = sources[path]
                for start, end, changed in sorted(replacements, reverse=True):
                    result = result[:start] + changed + result[end:]
                path.write_text(result, encoding='utf-8')
    changes = sum(map(len, edits.values()))
    print(f'{"Dry run" if dry_run else "Complete"}: {matched} matched, {changes} {"would change" if dry_run else "updated"}, {unchanged} unchanged, {skipped} skipped.')
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='?', type=Path, default=REPO.parent / 'citation_number.txt')
    parser.add_argument('--dry-run', action='store_true', help='report matches without changing files')
    args = parser.parse_args()
    try:
        update(args.input, [REPO / '_bibliography/papers.bib', REPO / '_bibliography/conference.bib'], args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
