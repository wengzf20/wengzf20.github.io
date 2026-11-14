"""Check generated local links and ensure archived content stays unpublished."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
import os

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site').resolve()
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and key in ('href', 'src', 'poster'):
                self.links.append(value)
errors = []
files = list(root.rglob('*.html'))
# Match Linux/GitHub Pages casing even when checking on a case-insensitive Mac.
output_paths = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
# macOS merges /Blog/ (the index) and /blog/ (post/archive directories).
# On Linux these remain separate; no alias is added there.
if (root / 'BLOG').exists() and (root / 'blog').exists() and (root / 'BLOG').samefile(root / 'blog'):
    output_paths |= {'Blog/' + p[5:] for p in output_paths if p.startswith('blog/')}
    output_paths |= {'blog/' + p[5:] for p in output_paths if p.startswith('Blog/')}
for page in files:
    parser = Links(); parser.feed(page.read_text())
    for link in parser.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path: continue
        path = unquote(url.path)
        target = root / path.lstrip('/') if path.startswith('/') else page.parent / path
        relative = os.path.relpath(os.path.normpath(target), root).replace(os.sep, '/')
        if relative not in output_paths and ('index.html' if relative == '.' else relative.rstrip('/') + '/index.html') not in output_paths:
            errors.append(f'{page.relative_to(root)} -> {link}')
for required in ['index.html', 'Research/index.html', 'Publications/index.html', 'Blog/index.html', 'Gallery/index.html', 'feed.xml', 'sitemap.xml']:
    if not (root / required).is_file(): errors.append(f'Missing {required}')
for forbidden in ['archive', 'assets/jupyter', 'node_modules', 'Gemfile', 'Gemfile.lock', 'scripts']:
    if (root / forbidden).exists(): errors.append(f'Published excluded path: {forbidden}')
for page in [*files, root / 'feed.xml', root / 'sitemap.xml']:
    if page.is_file() and ('Prepare figures for journal articles' in page.read_text() or '/2023/jupyter-notebook/' in page.read_text()):
        errors.append(f'Archived article exposed: {page.relative_to(root)}')
if errors:
    print('\n'.join(sorted(set(errors)))); sys.exit(1)
print(f'Checked {len(files)} HTML pages: local links, required routes, and archive exclusions passed.')
