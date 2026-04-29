#!/usr/bin/env python3
"""Generate the project report overview page."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "site" / "projects.json"
OUTPUT_PATH = ROOT / "site" / "index.html"


def load_projects() -> list[dict[str, object]]:
    projects = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return sorted(projects, key=lambda item: (str(item.get("category", "")), str(item.get("title", "")).lower()))


def render() -> str:
    projects = load_projects()
    embedded = json.dumps(projects, ensure_ascii=False, indent=2)
    total = len(projects)
    categories = sorted({str(project.get("category", "未分类")) for project in projects})
    updated_values = [str(project.get("updated", "")) for project in projects if project.get("updated")]
    last_updated = max(updated_values) if updated_values else date.today().isoformat()

    html = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>项目洞察总览</title>
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
strong { color: #071018; font-weight: 850; }
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
.topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 14px;
  color: var(--muted);
  font-size: 13px;
}
.brand {
  color: var(--teal);
  font-weight: 900;
  letter-spacing: .08em;
  text-transform: uppercase;
}
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
.metric span { color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
.toolbar {
  position: sticky;
  top: 0;
  z-index: 3;
  display: grid;
  grid-template-columns: minmax(260px, 1.35fr) minmax(150px, .5fr) minmax(150px, .5fr) minmax(150px, .45fr);
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
  color: var(--muted);
  font-size: 12px;
  font-weight: 780;
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
input:focus, select:focus {
  outline: 3px solid rgba(15,118,110,.18);
  border-color: var(--teal);
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
  grid-template-columns: minmax(210px, .45fr) minmax(0, 1fr) auto;
  gap: 18px;
  align-items: start;
  padding: 20px 24px;
  border-bottom: 1px solid var(--line);
  background: #fff;
}
.project-row:last-child { border-bottom: 0; }
.project-title { min-width: 0; }
.project-title h3 {
  margin: 4px 0 8px;
  font-size: 22px;
  line-height: 1.22;
  overflow-wrap: anywhere;
}
.badge {
  display: inline-flex;
  max-width: 100%;
  padding: 4px 8px;
  border: 1px solid #b7d4cf;
  border-radius: 999px;
  background: var(--soft-teal);
  color: #0b5c55;
  font-size: 12px;
  font-weight: 820;
  overflow-wrap: anywhere;
}
.adoption {
  margin-top: 8px;
  color: #21313c;
  font-weight: 820;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 18px;
  margin: 0;
}
.detail-grid dt {
  color: var(--muted);
  font-size: 12px;
  font-weight: 820;
}
.detail-grid dd {
  margin: 3px 0 0;
  color: #2d3742;
}
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}
.tag {
  padding: 3px 7px;
  border: 1px solid #d4dad6;
  border-radius: 6px;
  background: #f6f8f7;
  color: #46515c;
  font-size: 12px;
}
.actions {
  display: grid;
  gap: 8px;
  min-width: 112px;
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
.maintain-note {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  align-items: center;
  padding: 14px 24px;
  border-top: 1px solid var(--line);
  background: #f9faf8;
  color: var(--muted);
  font-size: 13px;
}
@media (max-width: 980px) {
  .page { padding: 18px; }
  .hero { grid-template-columns: 1fr; }
  .hero-side { border-left: 0; border-top: 1px solid var(--line); }
  .toolbar { position: static; grid-template-columns: 1fr 1fr; }
  .project-row { grid-template-columns: 1fr; }
  .actions { display: flex; flex-wrap: wrap; }
}
@media (max-width: 620px) {
  .page { padding: 12px; }
  .topline { display: block; }
  .hero-main, .hero-side { padding: 24px 20px; }
  .hero-side { grid-template-columns: 1fr; }
  .toolbar { grid-template-columns: 1fr; }
  .section-head { display: block; padding: 18px; }
  .count-pill { display: inline-flex; margin-top: 10px; }
  .project-row { padding: 18px; }
  .detail-grid { grid-template-columns: 1fr; gap: 8px; }
  .actions { display: grid; grid-template-columns: 1fr; }
  .button { width: 100%; }
}
  </style>
</head>
<body>
  <main class="page">
    <div class="topline">
      <span class="brand">Project Insight Reports</span>
      <span>__TOTAL__ 个项目 · 更新至 __LAST_UPDATED__ · <code>projects.json</code></span>
    </div>

    <section class="hero" aria-labelledby="page-title">
      <div class="hero-main">
        <span class="eyebrow">项目报告入口</span>
        <h1 id="page-title">项目洞察总览</h1>
        <p>按类型、采用口径和核心差异快速定位报告。新增项目只维护清单数据，再重新生成本页。</p>
      </div>
      <aside class="hero-side" aria-label="索引概况">
        <div class="metric"><b id="metric-total">__TOTAL__</b><span>已收录项目</span></div>
        <div class="metric"><b>__CATEGORY_COUNT__</b><span>项目类型</span></div>
        <div class="metric wide"><b>1</b><span>统一列表视图，面向浏览和管理</span></div>
      </aside>
    </section>

    <section class="toolbar" aria-label="筛选项目">
      <div class="control">
        <label for="search">搜索</label>
        <input id="search" type="search" placeholder="项目名、价值、标签、架构关键词">
      </div>
      <div class="control">
        <label for="category-filter">类型</label>
        <select id="category-filter"><option value="">全部类型</option></select>
      </div>
      <div class="control">
        <label for="adoption-filter">采用口径</label>
        <select id="adoption-filter"><option value="">全部口径</option></select>
      </div>
      <div class="control">
        <label for="sort-by">排序</label>
        <select id="sort-by">
          <option value="category">按类型</option>
          <option value="title">按项目名</option>
          <option value="updated">按更新时间</option>
        </select>
      </div>
    </section>

    <section class="section" aria-labelledby="list-title">
      <div class="section-head">
        <div>
          <h2 id="list-title">报告列表</h2>
          <p>先看采用口径和差异点，再打开完整项目页。</p>
        </div>
        <span class="count-pill" id="result-count">__TOTAL__ 个项目</span>
      </div>
      <div class="project-list" id="project-list"></div>
      <div class="empty" id="empty-state" hidden>没有匹配的项目。请放宽搜索或筛选条件。</div>
      <div class="maintain-note">
        <strong>扩充：</strong>
        <span>新增报告后更新 <code>site/projects.json</code>，运行 <code>python3 tools/generate_project_index.py</code>。</span>
      </div>
    </section>
  </main>

  <script>
const EMBEDDED_PROJECTS = __EMBEDDED__;
let projects = [...EMBEDDED_PROJECTS];

const el = {
  search: document.querySelector("#search"),
  category: document.querySelector("#category-filter"),
  adoption: document.querySelector("#adoption-filter"),
  sort: document.querySelector("#sort-by"),
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

function searchable(project) {
  return [
    project.title, project.slug, project.category, project.adoption, project.audience,
    project.problem, project.difference, project.demo, project.architecture,
    ...(project.tags || [])
  ].join(" ").toLowerCase();
}

function uniqueValues(key) {
  return [...new Set(projects.map(project => project[key]).filter(Boolean))].sort((a, b) => String(a).localeCompare(String(b), "zh-CN"));
}

function fillSelect(select, values) {
  const first = select.options[0];
  select.replaceChildren(first);
  values.forEach(value => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function sortProjects(items) {
  const mode = el.sort.value;
  return [...items].sort((a, b) => {
    if (mode === "updated") return String(b.updated || "").localeCompare(String(a.updated || ""));
    if (mode === "title") return String(a.title || "").localeCompare(String(b.title || ""), "zh-CN");
    return `${a.category || ""} ${a.title || ""}`.localeCompare(`${b.category || ""} ${b.title || ""}`, "zh-CN");
  });
}

function filteredProjects() {
  const query = el.search.value.trim().toLowerCase();
  return sortProjects(projects.filter(project => {
    const matchesSearch = !query || searchable(project).includes(query);
    const matchesCategory = !el.category.value || project.category === el.category.value;
    const matchesAdoption = !el.adoption.value || project.adoption === el.adoption.value;
    return matchesSearch && matchesCategory && matchesAdoption;
  }));
}

function renderTags(tags) {
  return (tags || []).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
}

function renderList(items) {
  el.list.innerHTML = items.map(project => `
    <article class="project-row">
      <div class="project-title">
        <span class="badge">${escapeHtml(project.category)}</span>
        <h3>${escapeHtml(project.title)}</h3>
        <span class="eyebrow">${escapeHtml(project.slug)}</span>
        <div class="adoption">${escapeHtml(project.adoption)}</div>
        <div class="tag-row">${renderTags(project.tags)}</div>
      </div>
      <dl class="detail-grid">
        <div><dt>适合谁</dt><dd>${escapeHtml(project.audience)}</dd></div>
        <div><dt>解决问题</dt><dd>${escapeHtml(project.problem)}</dd></div>
        <div><dt>差异点</dt><dd>${escapeHtml(project.difference)}</dd></div>
        <div><dt>Demo / 机制</dt><dd>${escapeHtml(project.demo)}</dd></div>
      </dl>
      <div class="actions">
        <a class="button primary" href="${escapeHtml(project.file)}">打开报告</a>
        <a class="button" href="${escapeHtml(project.markdown)}">Markdown</a>
        <a class="button" href="${escapeHtml(project.repo)}" target="_blank" rel="noreferrer">GitHub</a>
      </div>
    </article>
  `).join("");
}

function renderAll() {
  const items = filteredProjects();
  el.count.textContent = `${items.length} / ${projects.length} 个项目`;
  el.total.textContent = projects.length;
  el.empty.hidden = items.length > 0;
  renderList(items);
}

function refreshOptions() {
  fillSelect(el.category, uniqueValues("category"));
  fillSelect(el.adoption, uniqueValues("adoption"));
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

["input", "change"].forEach(eventName => {
  el.search.addEventListener(eventName, renderAll);
  el.category.addEventListener(eventName, renderAll);
  el.adoption.addEventListener(eventName, renderAll);
  el.sort.addEventListener(eventName, renderAll);
});

loadRuntimeData().then(() => {
  refreshOptions();
  renderAll();
});
  </script>
</body>
</html>
"""
    return (
        html.replace("__EMBEDDED__", embedded)
        .replace("__TOTAL__", str(total))
        .replace("__CATEGORY_COUNT__", str(len(categories)))
        .replace("__LAST_UPDATED__", last_updated)
    )


def main() -> None:
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
