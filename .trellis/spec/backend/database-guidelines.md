# Database Guidelines

> Current state: this project does not use a database, ORM, migrations, or query
> layer.

---

## Source Of Truth

The persistent project registry is `site/projects.json`. Treat it as a static
JSON data file, not as a database.

Supported examples:

```python
def load_projects() -> list[dict]:
    if not INDEX_DATA.exists():
        return []
    return json.loads(INDEX_DATA.read_text(encoding="utf-8"))
```

```python
def save_projects(projects: list[dict]) -> None:
    INDEX_DATA.parent.mkdir(parents=True, exist_ok=True)
    INDEX_DATA.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
```

---

## Registry Contract

Project records currently use these fields:

```json
{
  "slug": "gbrain",
  "title": "GBrain",
  "file": "projects/gbrain/",
  "markdown": "projects/gbrain/analysis.md",
  "repo": "https://github.com/garrytan/gbrain",
  "category": "知识工具",
  "adoption": "小范围验证",
  "audience": "希望把个人或团队知识沉淀为可查询、可写回工作流的开发者。",
  "summary": "提供 CLI 与 MCP 写回能力，把知识导入、查询和页面更新连成可验证闭环。",
  "problem": "把导入、查询和 MCP 写回串成最小可验证知识操作闭环。",
  "difference": "重点不是展示一个聊天 UI，而是验证知识库命令流和 `put_page` 写回能力。",
  "demo": "gbrain init -> gbrain import -> gbrain query -> MCP put_page 写回。",
  "architecture": "C4-light + 知识写入/查询交互图",
  "tags": ["MCP", "Knowledge Base", "CLI", "Writeback"],
  "updated": "2026-04-28"
}
```

New feature work that reads or writes registry data must preserve this contract
unless the task explicitly changes it.

## Scenario: Project Registration And Index Registry Contract

### 1. Scope / Trigger

- Trigger: adding or changing fields in `site/projects.json`, the registration
  CLI, or the index renderer.
- Current required registry addition: `summary` is a required title-area
  functional highlight for every project.

### 2. Signatures

Project registration must include `--summary`:

```bash
python3 tools/project_report_manager.py register \
  --slug "<slug>" \
  --title "<title>" \
  --source "<report-html-or-dir>" \
  --repo "<github-url>" \
  --category "<compat-search-category>" \
  --adoption "<compat-search-adoption>" \
  --audience "<target-audience>" \
  --summary "<one-sentence-functional-highlight>" \
  --problem "<problem-solved>" \
  --difference "<key-difference>" \
  --demo "<demo-or-mechanism>" \
  --architecture "<architecture-note>" \
  --tag "<tag>" \
  --updated "YYYY-MM-DD"
```

### 3. Contracts

- `summary` is explicit source data; do not infer it from `audience`.
- `category` and `adoption` remain compatibility/search metadata, not visible
  standalone index dimensions.
- `tags` are the visible discovery surface and should duplicate useful
  category/adoption concepts when those concepts should be clickable.
- `summary`, `problem`, `difference`, and `demo` may contain only lightweight
  display markers: `**...**` and `` `...` ``. They are not trusted HTML.
- After any registry change, regenerate `site/index.html`.

### 4. Validation & Error Matrix

| Condition | Expected behavior |
|---|---|
| Missing `--summary` in `register` | `argparse` rejects the command |
| Existing project without `summary` | `tools/generate_project_index.py` raises `ValueError` |
| Duplicate project without `--replace` | registration stops with `SystemExit` |
| Raw `**...**` markers visible in index text | Playwright verifier fails `rawInlineMarkers` |
| Category/adoption rendered as dropdowns or badges | Playwright verifier fails discovery checks |

### 5. Good/Base/Bad Cases

- Good: project has explicit `summary`, useful tags, compatibility metadata,
  and generated index renders summary under the title.
- Base: category/adoption remain in JSON and searchable, but do not appear as
  standalone UI controls.
- Bad: using `audience` as the title subtitle, omitting `summary`, or rendering
  category/adoption as primary filters.

### 6. Tests Required

- `python3 -m py_compile tools/project_report_manager.py tools/generate_project_index.py`
- `python3 -m json.tool site/projects.json >/dev/null`
- `python3 tools/generate_project_index.py`
- Playwright verifier checks summary contract, tag discovery, no raw inline
  markers, and absence of category/adoption standalone UI.

### 7. Wrong vs Correct

#### Wrong

```json
{
  "audience": "想把模糊需求转成可执行 agent 行为约束的团队。",
  "tags": ["Skill", "Agent Rules"]
}
```

#### Correct

```json
{
  "audience": "想把模糊需求转成可执行 agent 行为约束的团队。",
  "summary": "将模糊协作规则沉淀为可执行的 **agent 工作流约束**与**验证基线**。",
  "tags": ["Agent", "Agent 规则", "Skill", "Agent Rules", "团队基线"]
}
```

### Index Discovery Convention

- `tags` are the primary index-page discovery surface. Use short,
  multi-dimensional terms such as `Agent`, `MCP`, `CLI`, `API Proxy`,
  `Knowledge`, `Desktop`, `Finance`, `本地试点`, `团队基线`, and `需审计`.
- `category` and `adoption` are compatibility/search metadata, not standalone
  index-page display dimensions. Do not render them as hero metrics, dropdowns,
  sort modes, or per-row badges unless a task explicitly reverses this
  decision.
- If a category/adoption concept should be visible for discovery, duplicate the
  useful short term into `tags` and regenerate `site/index.html`.
- `summary` is the title-area functional highlight on the index page. It must
  be explicit registry data and must not be inferred from `audience`.
- Keep long explanatory text in `audience`, `problem`, `difference`, and
  `demo`.
- `summary`, `problem`, `difference`, and `demo` may include lightweight
  display markers for the index renderer: `**...**` for important phrases and
  `` `...` `` for code spans. These are not HTML and must still be safely
  rendered by the frontend.
- When tags are expanded in `site/projects.json`, regenerate
  `site/index.html` with `python3 tools/generate_project_index.py`.

---

## Query Patterns

- Load all records with `json.loads(...)`.
- Filter/sort in memory.
- Match existing projects by normalized slug or normalized repo URL.
- Sort saved records by `(category, title.lower())`.

Supported example:

```python
projects.sort(key=lambda item: (str(item.get("category", "")), str(item.get("title", "")).lower()))
```

---

## Migrations

There is no migration system. If a task changes `site/projects.json` shape, the
task must also update:

- `tools/project_report_manager.py`
- `tools/generate_project_index.py`
- existing records in `site/projects.json`
- generated `site/index.html`
- Playwright assertions in `tools/verify_reports.js` when rendered structure
  changes

---

## Not Supported

- ORM models.
- SQL migrations.
- Runtime database connections.
- Transaction handling.
