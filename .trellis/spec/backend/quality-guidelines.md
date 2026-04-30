# Quality Guidelines

> Quality checks are script-based. There is no configured Python linter, JS
> linter, test runner, or package manager manifest in the current repo.

---

## Required Checks For Tool Changes

Run Python compilation for changed Python tools:

```bash
python3 -m py_compile tools/<changed-file>.py
```

When a task changes generated reports or the index generator, regenerate the
affected output:

```bash
python3 tools/generate_project_index.py
```

When a task changes core report generation:

```bash
python3 tools/generate_final_insight_reports.py
python3 tools/generate_gbrain_insight_report.py
python3 tools/generate_project_index.py
```

When a task changes rendered HTML structure, run the existing report validator
if available in the checkout:

```bash
python3 .agents/skills/project-insight-analysis/scripts/validate_report.py \
  site/projects/free-claude-code/analysis.md \
  site/projects/FinceptTerminal/analysis.md \
  site/projects/andrej-karpathy-skills/analysis.md \
  site/projects/gbrain/analysis.md \
  site/projects/free-claude-code/index.html \
  site/projects/FinceptTerminal/index.html \
  site/projects/andrej-karpathy-skills/index.html \
  site/projects/gbrain/index.html \
  --json
```

For browser layout changes, use the existing Playwright verification script
through the repo-documented flow:

```bash
python3 -m http.server 8765
bash "$PWCLI" open http://localhost:8765/site/
bash "$PWCLI" run-code --filename tools/verify_reports.js --json
```

---

## Required Patterns

- Preserve UTF-8 reads/writes for JSON, Markdown, and HTML.
- Preserve deterministic JSON formatting: `ensure_ascii=False`, `indent=2`, and
  trailing newline for `site/projects.json`.
- Preserve deterministic registry sorting by category and title.
- Resolve paths from `ROOT`, not from the caller's current directory.
- Rebuild `site/index.html` after changing `site/projects.json`.

Supported examples:

```python
INDEX_DATA.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
```

```python
subprocess.run([sys.executable, str(INDEX_SCRIPT)], cwd=ROOT, check=True)
```

---

## Forbidden Patterns

- Editing generated `site/index.html` without also updating
  `tools/generate_project_index.py` when the change should be reproducible.
- Changing `site/projects.json` by hand without regenerating `site/index.html`.
- Adding a dependency that requires `package.json`, `requirements.txt`, or a
  virtual environment unless the feature task explicitly introduces that
  tooling.
- Introducing database, API, or framework patterns not present in the repo.

---

## Review Checklist

- Does the change keep source data, generator code, and generated artifacts in
  sync?
- Did Python files compile?
- If HTML/CSS/JS changed, did the verification script still find expected
  selectors and no horizontal overflow?
- Did new project records include all current registry fields?
