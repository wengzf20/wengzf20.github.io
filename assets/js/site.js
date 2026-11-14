(() => {
  const root = document.documentElement;
  try {
    const saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  } catch (_) {}
  document.getElementById("theme-toggle")?.addEventListener("click", () => {
    const dark = root.dataset.theme
      ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try {
      localStorage.setItem("theme", root.dataset.theme);
    } catch (_) {}
  });
  document.querySelectorAll(".bib-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const panel = document.getElementById(button.getAttribute("aria-controls"));
      if (!panel) return;
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      panel.hidden = expanded;
    });
  });
  const article = document.getElementById("article-body");
  const toc = document.getElementById("article-toc");
  if (article && toc) {
    // Citation titles are headings for accessibility, not article sections.
    const headings = [...article.querySelectorAll("h2, h3")].filter(
      (heading) => !heading.closest(".publication, .publications, .bibliography, .references"),
    );
    headings.forEach((heading, index) => {
      if (!heading.id) {
        const base =
          heading.textContent
            .trim()
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, "-")
            .replace(/^-|-$/g, "") || "section";
        let id = base,
          suffix = index;
        while (document.getElementById(id)) id = `${base}-${++suffix}`;
        heading.id = id;
      }
      const link = document.createElement("a");
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent;
      if (heading.tagName === "H3") link.className = "subheading";
      toc.append(link);
    });
    if (headings.length) {
      document.querySelector(".contents").hidden = false;
      const details = toc.closest("details");
      const narrow = matchMedia("(max-width: 980px)");
      const update = () => {
        details.open = !narrow.matches;
      };
      update();
      narrow.addEventListener("change", update);
    }
  }
  // Stack each research column independently while preserving DOM/mobile order.
  const projectGrid = document.querySelector(".projects .grid");
  if (projectGrid) {
    const cards = [...projectGrid.querySelectorAll(".project-card")];
    const mobile = matchMedia("(max-width: 600px)");
    let frame;
    const arrangeProjects = () => {
      frame = null;
      projectGrid.classList.add("is-masonry");
      const columns = mobile.matches ? 1 : 2;
      const gap = parseFloat(getComputedStyle(projectGrid).columnGap) || 24;
      const width = (projectGrid.clientWidth - gap * (columns - 1)) / columns;
      const heights = Array(columns).fill(0);
      cards.forEach((card, index) => {
        const column = index % columns;
        card.style.width = `${width}px`;
        card.style.transform = `translate(${column * (width + gap)}px, ${heights[column]}px)`;
        heights[column] += card.offsetHeight + gap;
      });
      projectGrid.style.height = `${Math.max(0, ...heights) - (cards.length ? gap : 0)}px`;
    };
    const scheduleProjects = () => {
      if (frame == null) frame = requestAnimationFrame(arrangeProjects);
    };
    arrangeProjects();
    window.addEventListener("resize", scheduleProjects);
    projectGrid.querySelectorAll("img").forEach((img) => {
      img.addEventListener("load", scheduleProjects);
      img.addEventListener("error", scheduleProjects);
    });
    if (typeof ResizeObserver !== "undefined") {
      const observer = new ResizeObserver(scheduleProjects);
      cards.forEach((card) => observer.observe(card));
    }
  }
  const content = document.querySelector("main");
  const dollarMath = Boolean(document.querySelector("[data-inline-dollar-math]"));
  const mathText = content?.textContent || "";
  if (/\\\(|\\\[|\$\$|\\begin\{(?:equation|align|gather|multline)\*?\}/.test(mathText) || (dollarMath && /\$[^$]+\$/.test(mathText))) {
    const inlineMath = [["\\(", "\\)"]];
    if (dollarMath) inlineMath.push(["$", "$"]);
    window.MathJax = {
      tex: {
        inlineMath,
        displayMath: [["\\[", "\\]"], ["$$", "$$"]],
        processEscapes: true,
        tags: "ams",
      },
      options: {
        skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"],
      },
    };
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js";
    script.async = true;
    document.head.append(script);
  }
})();
