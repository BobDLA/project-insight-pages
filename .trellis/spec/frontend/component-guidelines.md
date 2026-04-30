# Component Guidelines

> Components in this project are HTML sections and Python string render helpers,
> not framework components.

---

## Page Section Pattern

Report pages are composed from Python helpers returning HTML strings. Keep one
semantic section or page fragment per helper.

Supported examples:

```python
def section(idx: str, anchor: str, title: str, note: str, body: str) -> str:
    return f"""
    <section id="{anchor}" class="section">
      <div class="section-head">
        <div class="section-index">{idx}</div>
        <h2>{title}</h2>
        <p class="section-note">{note}</p>
      </div>
      <div class="section-body">{body}</div>
    </section>
    """
```

```python
def report_sections(project: dict) -> list[tuple[str, str, str, str, str]]:
    sections = [
        ("lean", "Lean 判断", "新用户先看什么", "保留精益创业视角：适合谁、问题、差异、时机和最小验证。", lean_html(project)),
        ("demo", "Demo", "Gold Example / Demo", "优先使用真实项目图片或仓库 example；未运行时明确标注静态推演。", demo_html(project)),
    ]
```

### Index Copy Pattern

The overview page is a reader-facing report directory, not a maintenance or
generator page. Keep top-level copy focused on what the reports explain.

Supported copy:

```html
<span class="eyebrow">Project Insight Reports</span>
<h1 id="page-title">项目洞察报告</h1>
<p>从问题场景、目标用户、差异机制、架构视角和采用风险等维度理解一个项目。</p>
```

For the list heading, describe report content and reader actions:

```html
<h2 id="list-title">报告列表</h2>
<p>每份报告围绕问题、差异、机制、架构和采用判断展开；可用关键词或标签收窄列表。</p>
```

Do not put maintenance commands or generator instructions in the main page body.
Maintenance workflow belongs in README or project docs.

Do not show a standalone slug subtitle under each project title; the title and
GitHub action are enough identity for report readers.

Under each project title, render the explicit `project.summary` one-sentence
functional highlight. Do not infer this title-area subtitle from
`project.audience`; audience can remain searchable metadata.

### Index List Summary Pattern

When a generated list item shows labeled facts, render them as a compact
description list instead of generic `div`/`p` pairs. This keeps the report index
scan-friendly while preserving semantic label/value structure for checks and
assistive technology.

Supported example:

```javascript
<dl class="summary-stack">
  <div class="summary-line primary">
    <dt class="summary-label">解决问题</dt>
    <dd class="summary-text">${escapeHtml(project.problem)}</dd>
  </div>
  <div class="summary-line">
    <dt class="summary-label">差异点</dt>
    <dd class="summary-text">${escapeHtml(project.difference)}</dd>
  </div>
</dl>
```

Use a cohesive analysis group for row details so the list does not become a
stack of competing colored bars. `解决问题` is the primary scan target; `差异点`
and `Demo / 机制` should remain distinct but quieter. Prefer a light bordered
panel, thin separators, small accent markers, and neutral dark emphasis text
over broad saturated color blocks or many competing text colors.

---

## Escaping Contract

Escape untrusted or data-derived text before injecting it into HTML. Existing
helpers use Python `html.escape` and a small `inline()` formatter for limited
Markdown-like emphasis/code.

Supported example:

```python
def inline(text: str) -> str:
    placeholders: dict[str, str] = {}
    raw = re.sub(r"\*\*(.+?)\*\*", lambda m: hold(f"<strong>{escape(m.group(1))}</strong>"), text)
    raw = re.sub(r"`([^`]+?)`", lambda m: hold(f"<code>{escape(m.group(1))}</code>"), raw)
    escaped = escape(raw)
    for key, value in placeholders.items():
        escaped = escaped.replace(escape(key), value)
    return escaped
```

The overview page's client-side renderer escapes project data before using
`innerHTML`.

Supported example:

```javascript
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}
```

When the index list needs visual emphasis inside data-derived summary/detail
text, use the local inline renderer and keep the supported syntax narrow:
`**important**` for emphasis and `` `code` `` for code spans. The renderer must
escape all unmatched text and escape marker contents before returning
`<strong>` or `<code>` HTML. Use this only for report-list text such as
`summary`, `problem`, `difference`, and `demo`; tags, labels, links, and control
text should stay plain escaped text.

---

## Styling Patterns

- CSS is embedded in generated HTML.
- Design tokens live in `:root` custom properties.
- Layouts use CSS Grid/Flexbox, `minmax(0, ...)`, fixed border radius variables,
  and responsive media queries.
- The current visual language is quiet report/dashboard UI, not a marketing
  landing page.

Supported example:

```css
:root {
  --bg: #f3f0e8;
  --paper: #fffdf8;
  --ink: #151923;
  --muted: #65707d;
  --line: #d8ddd9;
  --teal: #0f766e;
  --radius: 8px;
}
```

---

## Accessibility Patterns

Use semantic HTML and ARIA labels that already exist in the pages:

- `<main>`, `<article>`, `<header>`, `<section>`, `<nav>`, `<figure>`,
  `<figcaption>`, `<dl>`, `<dt>`, `<dd>`.
- `aria-label` for report articles, diagram type rows, and tablists.
- Real `<button type="button">` controls for diagram tabs.
- `hidden` to hide inactive panels.

Supported example:

```python
buttons = "".join(
    f'<button type="button" data-diagram-tab="{escape(key)}" aria-selected="{str(index == 0).lower()}">{escape(label)}</button>'
    for index, (key, label, _) in enumerate(tabs)
)
```

---

## Not Supported

- React/Vue/Svelte components.
- Props interfaces.
- CSS modules, Tailwind, styled-components, or build-time CSS processing.
