# Quality Guidelines

> Frontend quality is verified through regenerated static output plus
> Playwright layout/behavior checks. There is no configured JS linter or unit
> test runner.

---

## Required Patterns

- Keep generated HTML reproducible from the Python generator when the page is
  generator-owned.
- Escape project data before inserting it with `innerHTML`.
- Keep controls and generated rows stable for `tools/verify_reports.js`
  selectors.
- Preserve responsive behavior across desktop, poster, and mobile viewports.
- Preserve no-horizontal-overflow checks.
- Keep the index page reader-facing: no maintenance/generator copy in the main
  page body and no standalone project slug subtitles.

Supported verification selectors from `tools/verify_reports.js`:

```javascript
projectRows: document.querySelectorAll(".project-row").length,
topLineRows: document.querySelectorAll(".topline").length,
controls: document.querySelectorAll(".toolbar input, .toolbar select").length,
tagChips: document.querySelectorAll("#tag-filters [data-tag]").length,
tableHeadColumns: document.querySelectorAll(".project-table-head span").length,
projectSlugSubtitles: document.querySelectorAll(".project-row .project-slug").length,
audienceSubtitles: document.querySelectorAll(".project-row .audience").length,
summarySubtitles: document.querySelectorAll(".project-row .project-summary").length,
summaryContract: (() => {
  const inlineText = value => String(value ?? "")
    .replace(/\*\*(.+?)\*\*/g, "$1")
    .replace(/`([^`]+?)`/g, "$1")
    .trim();
  const projectByTitle = new Map(projects.map(project => [String(project.title || ""), project]));
  return [...document.querySelectorAll(".project-row")].every(row => {
    const title = row.querySelector("h3")?.textContent.trim() || "";
    const summary = row.querySelector(".project-summary")?.textContent.trim() || "";
    const project = projectByTitle.get(title);
    return summary && project && summary === inlineText(project.summary)
      && summary !== inlineText(project.audience);
  });
})(),
emphasisMarks: document.querySelectorAll(".project-summary strong, .summary-text strong").length,
rawInlineMarkers: /\*\*.+?\*\*/.test([...document.querySelectorAll(".project-summary, .summary-text")]
  .map(node => node.textContent || "")
  .join(" ")),
visualHierarchy: (() => {
  const rows = document.querySelectorAll(".project-row").length;
  const primary = document.querySelectorAll(".summary-line.primary").length;
  const difference = document.querySelectorAll(".summary-line.difference").length;
  const mechanism = document.querySelectorAll(".summary-line.mechanism").length;
  const panels = document.querySelectorAll(".project-row .summary-stack").length;
  const accentMarkers = new Set([...document.querySelectorAll(".summary-line")]
    .map(row => getComputedStyle(row).getPropertyValue("--accent").trim()));
  const strongColors = new Set([...document.querySelectorAll(".summary-line .summary-text strong")]
    .map(node => getComputedStyle(node).color));
  return primary === rows && difference === rows && mechanism === rows
    && panels === rows && accentMarkers.size >= 3 && strongColors.size <= 2;
})(),
hasCategoryFilter: Boolean(document.querySelector("#category-filter")),
hasAdoptionFilter: Boolean(document.querySelector("#adoption-filter")),
categoryBadges: document.querySelectorAll(".project-row .badge").length,
adoptionBadges: document.querySelectorAll(".project-row .adoption").length,
hasCategorySort: Boolean(document.querySelector('#sort-by option[value="category"]')),
hasProjectShapeText: document.body.innerText.includes("项目形态"),
hasHeroCopy: document.body.innerText.includes("从问题场景、目标用户、差异机制、架构视角和采用风险等维度理解一个项目。"),
hasListCopy: document.body.innerText.includes("每份报告围绕问题、差异、机制、架构和采用判断展开；可用关键词或标签收窄列表。"),
hasMaintenanceCopy: /新增项目只维护清单数据|扩充：|python3 tools\/generate_project_index\.py/.test(document.body.innerText),
diagramShells: document.querySelectorAll(".diagram-shell").length,
visibleSvgs: document.querySelectorAll(".diagram-panel:not([hidden]) svg").length,
architectureViews: document.querySelectorAll("#views .arch-view").length,
```

---

## Browser Verification

When HTML/CSS/JS changes, use the repo's documented browser flow:

```bash
mkdir -p temp/verification/playwright
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
bash "$PWCLI" open http://localhost:8765/site/
bash "$PWCLI" run-code --filename tools/verify_reports.js --json
```

The verifier checks:

- broken images
- horizontal overflow
- index search behavior
- expected list/control counts
- report page sections
- diagram tabs
- architecture view structure

---

## Forbidden Patterns

- Rendering data-derived strings into HTML without using the current escaping
  helpers.
- Removing IDs/classes used by `tools/verify_reports.js` without updating the
  verifier in the same task.
- Hand-editing generated HTML when the matching generator should own the change.
- Introducing framework or bundler dependencies without a task-level decision.

---

## Review Checklist

- Does the overview search still narrow `gbrain` to one project?
- Does clicking a visible tag chip, such as `MCP`, narrow the index
  predictably?
- Are `#category-filter` and `#adoption-filter` absent unless a task explicitly
  reintroduces them?
- Are category/adoption absent as standalone hero metrics, sort modes, and
  per-row badges?
- Does the hero describe multi-dimensional project analysis for report readers?
- Is maintenance/generator copy absent from the index page body?
- Is the duplicate top `.topline` brand/count/update row absent above the hero?
- Are standalone project slug subtitles absent from report rows?
- Does each report row render `.project-summary` from explicit `summary` data,
  with no `.audience` subtitle under the title?
- Does the desktop report list keep the three-column table header and row
  structure (`工具与简介`, `核心要点`, `资源与链接`) while stacking on mobile?
- Do important report-list phrases render through `<strong>` emphasis without
  exposing raw `**` markers in visible text?
- Do `解决问题`, `差异点`, and `Demo / 机制` render as one cohesive analysis group
  with subtle markers/separators instead of competing full-width color bars?
- Do report diagram tabs still switch panels?
- Do all referenced project assets load?
- Does mobile avoid horizontal overflow?
- Are generator changes reflected in generated `site/` files?
