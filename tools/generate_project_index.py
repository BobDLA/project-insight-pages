#!/usr/bin/env python3
"""Generate the project report overview page."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "site" / "projects.json"
OUTPUT_PATH = ROOT / "site" / "index.html"

FEATURED_TAGS = [
    "Agent",
    "MCP",
    "CLI",
    "API Proxy",
    "接口代理",
    "Knowledge",
    "知识工具",
    "Desktop",
    "桌面应用",
    "Finance",
    "本地试点",
    "团队基线",
    "研究评估",
    "小范围验证",
    "需审计",
]


def load_projects() -> list[dict[str, object]]:
    projects = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for project in projects:
        summary = project.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            name = project.get("slug") or project.get("title") or "<unknown>"
            raise ValueError(f"{name}: missing required summary field in {DATA_PATH.relative_to(ROOT)}")
    return sorted(
        projects,
        key=lambda item: (
            str(item.get("category", "")),
            str(item.get("title", "")).lower(),
        ),
    )


def discovery_tags(projects: list[dict[str, object]]) -> set[str]:
    tags: set[str] = set()
    for project in projects:
        for tag in project.get("tags", []) if isinstance(project.get("tags"), list) else []:
            if tag:
                tags.add(str(tag))
    return tags


def render() -> str:
    projects = load_projects()
    embedded = json.dumps(projects, ensure_ascii=False, indent=2)
    featured_tags = json.dumps(FEATURED_TAGS, ensure_ascii=False, indent=2)
    total = len(projects)
    tag_count = len(discovery_tags(projects))
    updated_values = [str(project.get("updated", "")) for project in projects if project.get("updated")]
    last_updated = max(updated_values) if updated_values else date.today().isoformat()

    html = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>项目洞察报告</title>
  <style>
:root {
  --bg: #f3f0e8;
  --paper: #fffdf8;
  --sheet: #f8fafb;
  --ink: #151923;
  --muted: #65707d;
  --line: #d8ddd9;
  --line-strong: #bfc8c2;
  --teal: #0f766e;
  --blue: #315c8f;
  --amber: #a66f12;
  --soft-teal: #e8f4f2;
  --radius: 8px;
  --shadow: 0 18px 60px rgba(21, 25, 35, .08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background:
    linear-gradient(90deg, rgba(21,25,35,.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(21,25,35,.03) 1px, transparent 1px),
    var(--bg);
  background-size: 32px 32px;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 16px;
  line-height: 1.58;
  overflow-x: hidden;
}
a { color: #0b5c55; text-decoration: none; }
a:hover { text-decoration: underline; }
strong { color: #071018; font-weight: 820; }
code {
  padding: 1px 5px;
  border: 1px solid #d7dfdc;
  border-radius: 5px;
  background: #f4f7f6;
  color: #183d39;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: .92em;
}
.page { width: 100%; max-width: 1280px; margin: 0 auto; padding: 28px; }
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(300px, .8fr);
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--paper);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.hero-main { min-width: 0; padding: 40px 46px 34px; }
.eyebrow {
  display: block;
  max-width: 100%;
  color: var(--muted);
  font-size: 13px;
  font-weight: 760;
  overflow-wrap: anywhere;
}
h1 {
  margin: 10px 0 16px;
  font-size: clamp(38px, 4.8vw, 68px);
  line-height: 1.02;
  letter-spacing: 0;
}
.hero-main p {
  max-width: 760px;
  margin: 0;
  color: #384451;
  font-size: 18px;
}
.hero-side {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  align-content: start;
  padding: 34px;
  border-left: 1px solid var(--line);
  background: linear-gradient(180deg, #f8fafb, #fffaf0);
}
.metric {
  display: grid;
  gap: 6px;
  min-width: 0;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255,255,255,.72);
}
.metric.wide { grid-column: 1 / -1; }
.metric b { font-size: 30px; line-height: 1; }
.metric b.metric-date { font-size: 20px; line-height: 1.15; }
.metric span { color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
.toolbar {
  position: sticky;
  top: 0;
  z-index: 3;
  display: grid;
  grid-template-columns: minmax(260px, 1fr) minmax(150px, 190px);
  gap: 10px;
  margin: 22px 0;
  padding: 12px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: rgba(255,253,248,.96);
  box-shadow: 0 12px 36px rgba(21,25,35,.08);
  backdrop-filter: blur(8px);
}
.control { display: grid; gap: 5px; }
.control label {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 780;
}
.control label span {
  color: #40505b;
  font-weight: 720;
  overflow-wrap: anywhere;
}
input, select {
  width: 100%;
  min-height: 44px;
  padding: 9px 11px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fff;
  color: var(--ink);
  font: inherit;
}
input:focus,
select:focus,
.tag-filter-button:focus-visible,
.tag:focus-visible,
.clear-tag:focus-visible {
  outline: 3px solid rgba(15,118,110,.18);
  border-color: var(--teal);
}
.tag-filter-panel {
  grid-column: 1 / -1;
  display: grid;
  gap: 8px;
  min-width: 0;
  padding-top: 10px;
  border-top: 1px solid var(--line);
}
.tag-filter-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 820;
}
.tag-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  min-width: 0;
}
.tag-filter-button,
.tag {
  display: inline-flex;
  align-items: center;
  max-width: 100%;
  padding: 4px 8px;
  border: 1px solid #dce4df;
  border-radius: 6px;
  background: #fbfcfb;
  color: #56636e;
  font: inherit;
  font-size: 12px;
  line-height: 1.35;
  overflow-wrap: anywhere;
}
.tag-filter-button {
  padding: 6px 9px;
  background: #fff;
  cursor: pointer;
}
.tag-filter-button[aria-pressed="true"],
.tag[aria-pressed="true"] {
  border-color: #0f766e;
  background: #e8f4f2;
  color: #0b5c55;
}
.tag {
  cursor: pointer;
}
.clear-tag {
  min-height: 28px;
  padding: 3px 8px;
  border: 1px solid var(--line-strong);
  border-radius: 6px;
  background: #fff;
  color: #123d38;
  font: inherit;
  font-size: 12px;
  font-weight: 760;
  cursor: pointer;
}
.section {
  margin-top: 22px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--paper);
  box-shadow: 0 12px 40px rgba(21,25,35,.06);
  overflow: hidden;
}
.section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  padding: 22px 24px;
  border-bottom: 1px solid var(--line);
  background: #f9faf8;
}
.section-head h2 { margin: 0; font-size: 22px; line-height: 1.2; }
.section-head p { margin: 4px 0 0; color: var(--muted); }
.count-pill {
  flex: 0 0 auto;
  padding: 7px 10px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: #fff;
  color: var(--muted);
  font-size: 13px;
  font-weight: 760;
}
.project-list { display: grid; }
.project-row {
  display: grid;
  grid-template-columns: minmax(230px, .34fr) minmax(0, 1fr) minmax(124px, auto);
  gap: 22px;
  align-items: start;
  padding: 22px 24px;
  border-bottom: 1px solid var(--line);
  background: #fff;
}
.project-row:last-child { border-bottom: 0; }
.project-title { min-width: 0; }
.project-title h3 {
  margin: 0 0 6px;
  font-size: 24px;
  line-height: 1.22;
  overflow-wrap: anywhere;
}
.project-summary {
  margin-top: 10px;
  padding-left: 10px;
  border-left: 3px solid #d8e0dc;
  color: #4b5965;
  font-size: 14px;
  line-height: 1.55;
  overflow-wrap: anywhere;
}
.project-summary strong { color: #24313c; font-weight: 830; }
.summary-stack {
  display: grid;
  margin: 0;
  padding: 8px 14px;
  min-width: 0;
  border: 1px solid #e2e8e4;
  border-radius: var(--radius);
  background: #fcfdfc;
}
.summary-line {
  --accent: #a7b3ae;
  display: grid;
  grid-template-columns: 86px minmax(0, 1fr);
  gap: 14px;
  min-width: 0;
  padding: 9px 0;
  border-top: 1px solid #edf1ee;
}
.summary-line:first-child {
  padding-top: 4px;
  border-top: 0;
}
.summary-line:last-child { padding-bottom: 4px; }
.summary-label {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 860;
  white-space: nowrap;
}
.summary-label::before {
  content: "";
  width: 6px;
  height: 6px;
  flex: 0 0 auto;
  border-radius: 999px;
  background: var(--accent);
}
.summary-text {
  margin: 0;
  color: #384451;
  line-height: 1.52;
  overflow-wrap: anywhere;
}
.summary-text strong { font-weight: 840; }
.summary-line.primary {
  --accent: #8fb6ae;
}
.summary-line.difference {
  --accent: #9eacbf;
}
.summary-line.mechanism {
  --accent: #c0ad87;
}
.summary-line.primary .summary-label {
  color: #4f6e68;
}
.summary-line.difference .summary-label {
  color: #53657a;
}
.summary-line.mechanism .summary-label {
  color: #756844;
}
.summary-line .summary-text strong {
  color: #22313d;
}
.summary-line.primary .summary-text {
  color: #17242a;
  font-size: 15.5px;
  font-weight: 700;
}
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}
.actions {
  display: grid;
  gap: 8px;
  min-width: 124px;
  justify-items: stretch;
}
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 8px 12px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fff;
  color: #123d38;
  font-size: 14px;
  font-weight: 780;
  white-space: nowrap;
}
.button.primary {
  border-color: #0f766e;
  background: #0f766e;
  color: #fff;
}
.empty {
  padding: 40px 24px;
  color: var(--muted);
  text-align: center;
}
@media (max-width: 980px) {
  .page { padding: 18px; }
  .hero { grid-template-columns: 1fr; }
  .hero-side { border-left: 0; border-top: 1px solid var(--line); }
  .toolbar { position: static; grid-template-columns: 1fr 1fr; }
  .tag-filter-panel { grid-column: 1 / -1; }
  .project-row { grid-template-columns: 1fr; }
  .actions { display: flex; flex-wrap: wrap; }
}
@media (max-width: 620px) {
  .page { padding: 12px; }
  .hero-main, .hero-side { padding: 24px 20px; }
  .hero-side { grid-template-columns: 1fr; }
  .toolbar { grid-template-columns: 1fr; }
  .section-head { display: block; padding: 18px; }
  .count-pill { display: inline-flex; margin-top: 10px; }
  .project-row { padding: 18px; }
  .summary-line { grid-template-columns: 1fr; gap: 3px; }
  .actions { display: grid; grid-template-columns: 1fr; }
  .button { width: 100%; }
}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero" aria-labelledby="page-title">
      <div class="hero-main">
        <span class="eyebrow">Project Insight Reports</span>
        <h1 id="page-title">项目洞察报告</h1>
        <p>从问题场景、目标用户、差异机制、架构视角和采用风险等维度理解一个项目。</p>
      </div>
      <aside class="hero-side" aria-label="索引概况">
        <div class="metric"><b id="metric-total">__TOTAL__</b><span>已收录项目</span></div>
        <div class="metric"><b>__TAG_COUNT__</b><span>可见标签</span></div>
        <div class="metric wide"><b class="metric-date">__LAST_UPDATED__</b><span>最近更新</span></div>
      </aside>
    </section>

    <section class="toolbar" aria-label="查找项目">
      <div class="control search-control">
        <label for="search">搜索</label>
        <input id="search" type="search" placeholder="项目名、仓库、价值、标签、架构关键词">
      </div>
      <div class="control sort-control">
        <label for="sort-by">排序</label>
        <select id="sort-by">
          <option value="title">按项目名</option>
          <option value="updated">按更新时间</option>
        </select>
      </div>
      <div class="tag-filter-panel">
        <div class="tag-filter-head">
          <span>标签</span>
          <button type="button" class="clear-tag" id="clear-tag" hidden>清除标签</button>
        </div>
        <div class="tag-filter-row" id="tag-filters" aria-label="标签"></div>
      </div>
    </section>

    <section class="section" aria-labelledby="list-title">
      <div class="section-head">
        <div>
          <h2 id="list-title">报告列表</h2>
          <p>每份报告围绕问题、差异、机制、架构和采用判断展开；可用关键词或标签收窄列表。</p>
        </div>
        <span class="count-pill" id="result-count">__TOTAL__ 个项目</span>
      </div>
      <div class="project-list" id="project-list"></div>
      <div class="empty" id="empty-state" hidden>没有匹配的项目。请放宽搜索或标签。</div>
    </section>
  </main>

  <script>
const EMBEDDED_PROJECTS = __EMBEDDED__;
const FEATURED_TAGS = __FEATURED_TAGS__;
let projects = [...EMBEDDED_PROJECTS];
let activeTag = "";

const el = {
  search: document.querySelector("#search"),
  sort: document.querySelector("#sort-by"),
  tagFilters: document.querySelector("#tag-filters"),
  clearTag: document.querySelector("#clear-tag"),
  list: document.querySelector("#project-list"),
  count: document.querySelector("#result-count"),
  empty: document.querySelector("#empty-state"),
  total: document.querySelector("#metric-total")
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}

function renderInline(value) {
  const source = String(value ?? "");
  const pattern = /(\*\*(.+?)\*\*|`([^`]+?)`)/g;
  let html = "";
  let index = 0;
  let match;

  while ((match = pattern.exec(source)) !== null) {
    html += escapeHtml(source.slice(index, match.index));
    if (match[2] !== undefined) {
      html += `<strong>${escapeHtml(match[2])}</strong>`;
    } else {
      html += `<code>${escapeHtml(match[3])}</code>`;
    }
    index = pattern.lastIndex;
  }

  html += escapeHtml(source.slice(index));
  return html;
}

function normalize(value) {
  return String(value ?? "").trim().toLowerCase();
}

function visibleTags(project) {
  return Array.isArray(project.tags) ? project.tags : [];
}

function projectFacets(project) {
  return [project.category, project.adoption, ...visibleTags(project)].filter(Boolean).map(String);
}

function searchable(project) {
  return [
    project.title, project.slug, project.repo, project.summary, project.audience,
    project.problem, project.difference, project.demo, project.architecture,
    ...projectFacets(project)
  ].join(" ").toLowerCase();
}

function tagKey(tag) {
  return normalize(tag);
}

function discoveryTags() {
  const present = new Map();
  projects.forEach(project => {
    visibleTags(project).forEach(tag => {
      const key = tagKey(tag);
      if (key && !present.has(key)) present.set(key, tag);
    });
  });
  const featured = FEATURED_TAGS
    .map(tag => present.get(tagKey(tag)))
    .filter(Boolean);
  const featuredKeys = new Set(featured.map(tagKey));
  const rest = [...present.values()]
    .filter(tag => !featuredKeys.has(tagKey(tag)))
    .sort((a, b) => String(a).localeCompare(String(b), "zh-CN"));
  return [...featured, ...rest];
}

function projectMatchesTag(project, tag) {
  const target = tagKey(tag);
  return projectFacets(project).some(value => tagKey(value) === target);
}

function sortProjects(items) {
  const mode = el.sort.value;
  return [...items].sort((a, b) => {
    if (mode === "updated") return String(b.updated || "").localeCompare(String(a.updated || ""));
    return String(a.title || "").localeCompare(String(b.title || ""), "zh-CN");
  });
}

function filteredProjects() {
  const query = el.search.value.trim().toLowerCase();
  return sortProjects(projects.filter(project => {
    const matchesSearch = !query || searchable(project).includes(query);
    const matchesTag = !activeTag || projectMatchesTag(project, activeTag);
    return matchesSearch && matchesTag;
  }));
}

function renderTagButton(tag, className) {
  const active = activeTag && tagKey(activeTag) === tagKey(tag);
  return `<button type="button" class="${className}" data-tag="${escapeHtml(tag)}" aria-pressed="${active ? "true" : "false"}">${escapeHtml(tag)}</button>`;
}

function renderTagFilters() {
  el.tagFilters.innerHTML = discoveryTags()
    .map(tag => renderTagButton(tag, "tag-filter-button"))
    .join("");
  el.clearTag.hidden = !activeTag;
}

function renderTags(tags) {
  return (Array.isArray(tags) ? tags : [])
    .map(tag => renderTagButton(tag, "tag"))
    .join("");
}

function renderList(items) {
  el.list.innerHTML = items.map(project => `
    <article class="project-row" aria-label="${escapeHtml(project.title)}">
      <div class="project-title">
        <h3>${escapeHtml(project.title)}</h3>
        <div class="project-summary">${renderInline(project.summary)}</div>
        <div class="tag-row">${renderTags(project.tags)}</div>
      </div>
      <dl class="summary-stack">
        <div class="summary-line primary">
          <dt class="summary-label">解决问题</dt>
          <dd class="summary-text">${renderInline(project.problem)}</dd>
        </div>
        <div class="summary-line difference">
          <dt class="summary-label">差异点</dt>
          <dd class="summary-text">${renderInline(project.difference)}</dd>
        </div>
        <div class="summary-line mechanism">
          <dt class="summary-label">Demo / 机制</dt>
          <dd class="summary-text">${renderInline(project.demo)}</dd>
        </div>
      </dl>
      <div class="actions">
        <a class="button primary" href="${escapeHtml(project.file)}" aria-label="打开 ${escapeHtml(project.title)} 报告">报告</a>
        <a class="button" href="${escapeHtml(project.markdown)}" aria-label="打开 ${escapeHtml(project.title)} Markdown">Markdown</a>
        <a class="button" href="${escapeHtml(project.repo)}" target="_blank" rel="noreferrer" aria-label="打开 ${escapeHtml(project.title)} GitHub 仓库">GitHub</a>
      </div>
    </article>
  `).join("");
}

function renderAll() {
  const items = filteredProjects();
  el.count.textContent = `${items.length} / ${projects.length} 个项目`;
  el.total.textContent = projects.length;
  el.empty.hidden = items.length > 0;
  renderTagFilters();
  renderList(items);
}

async function loadRuntimeData() {
  if (location.protocol === "file:") return;
  try {
    const response = await fetch("projects.json", { cache: "no-store" });
    if (!response.ok) return;
    const data = await response.json();
    if (Array.isArray(data) && data.length) projects = data;
  } catch (error) {
    console.warn("Using embedded project index data.", error);
  }
}

function setActiveTag(tag) {
  activeTag = activeTag && tagKey(activeTag) === tagKey(tag) ? "" : tag;
  renderAll();
}

function handleTagClick(event) {
  const button = event.target.closest("[data-tag]");
  if (!button) return;
  setActiveTag(button.dataset.tag);
}

el.search.addEventListener("input", renderAll);
el.sort.addEventListener("change", renderAll);
el.tagFilters.addEventListener("click", handleTagClick);
el.list.addEventListener("click", handleTagClick);
el.clearTag.addEventListener("click", () => {
  activeTag = "";
  renderAll();
});

loadRuntimeData().then(() => {
  renderAll();
});
  </script>
</body>
</html>
"""
    return (
        html.replace("__EMBEDDED__", embedded)
        .replace("__FEATURED_TAGS__", featured_tags)
        .replace("__TOTAL__", str(total))
        .replace("__TAG_COUNT__", str(tag_count))
        .replace("__LAST_UPDATED__", last_updated)
    )


def main() -> None:
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
