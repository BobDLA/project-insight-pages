# Backend Development Guidelines

> Current project reality: there is no long-running backend service. The
> backend layer means repository automation under `tools/`: Python generators,
> a Python report-registration CLI, and a Playwright verification script.

---

## Scope

Use these specs when a task changes:

- `tools/*.py`
- `tools/verify_reports.js`
- generated artifacts under `site/`
- report data copied into `site/projects/<slug>/`

Do not use these specs as permission to introduce an API server, database, ORM,
or background service. Those patterns are not present in the current codebase.

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | Static-site generation and CLI script layout | Current |
| [Database Guidelines](./database-guidelines.md) | Documents the absence of DB/ORM patterns | Current |
| [Error Handling](./error-handling.md) | Current CLI and generation error behavior | Current |
| [Quality Guidelines](./quality-guidelines.md) | Regeneration and verification expectations | Current |
| [Logging Guidelines](./logging-guidelines.md) | Current stdout/stderr conventions | Current |

---

## Evidence Baseline

- `tools/project_report_manager.py` owns project registration, copying report
  files/assets, updating `site/projects.json`, and rebuilding `site/index.html`.
- `tools/generate_project_index.py` reads `site/projects.json` and writes
  `site/index.html`.
- `tools/generate_final_insight_reports.py` and
  `tools/generate_gbrain_insight_report.py` generate project report pages and
  Markdown reports.
- `tools/verify_reports.js` is executed by the Playwright CLI and validates the
  rendered static pages.
