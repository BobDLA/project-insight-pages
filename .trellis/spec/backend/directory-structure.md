# Directory Structure

> Backend-like code in this repo is file-based static-site automation under
> `tools/`. There is no `src/` backend package, web route layer, service layer,
> database layer, or package manager manifest.

---

## Directory Layout

```text
tools/
  generate_final_insight_reports.py   # Generates core project report pages.
  generate_gbrain_insight_report.py   # Extends/reuses the core generator for one report.
  generate_project_index.py           # Rebuilds site/index.html from site/projects.json.
  project_report_manager.py           # CLI to list/check/register reports.
  verify_reports.js                   # Playwright page verification script.

site/
  index.html                          # Generated static overview page.
  projects.json                       # Project registry data source.
  projects/<slug>/index.html          # Generated or registered report page.
  projects/<slug>/analysis.md         # Markdown report.
  projects/<slug>/assets/             # Per-project copied assets.
```

---

## Module Organization

- Put repository automation in `tools/`.
- Keep generated public artifacts in `site/`.
- Use `ROOT = Path(__file__).resolve().parents[1]` in Python tools so commands
  work from any current directory.
- Keep small, script-local helpers near the top-level command they support.
- When a tool produces site output, write with `Path.write_text(...,
  encoding="utf-8")`.

Supported examples:

```python
ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
PROJECTS_DIR = SITE_DIR / "projects"
INDEX_DATA = SITE_DIR / "projects.json"
```

```python
def main() -> None:
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")
```

---

## CLI Organization

`project_report_manager.py` is the only argparse-based CLI in the repo. Follow
its existing shape for new CLI subcommands:

- `build_parser()` creates subcommands.
- Each command is implemented as `cmd_<name>(args: argparse.Namespace) -> int`.
- `main()` returns the selected command's integer status.
- The module exits through `raise SystemExit(main())`.

Supported example:

```python
def cmd_check(args: argparse.Namespace) -> int:
    project = find_project(load_projects(), args.target)
    if project:
        print(json.dumps({"exists": True, "project": project}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps({"exists": False, "slug": slug_from(args.target)}, ensure_ascii=False, indent=2))
    return 1 if args.strict else 0
```

---

## Naming Conventions

- Python tool files use snake_case.
- Generated project slugs are directory names under `site/projects/<slug>/`.
- Registry fields are lower-case JSON keys matching `site/projects.json`
  (`slug`, `title`, `file`, `markdown`, `repo`, `category`, `adoption`,
  `audience`, `summary`, `problem`, `difference`, `demo`, `architecture`, `tags`,
  `updated`).
- JavaScript verification code uses camelCase local variables.

---

## Do Not Introduce Without A Feature Requirement

- A web backend framework.
- A new package layout such as `src/` or `app/`.
- A database or migration folder.
- A build system beyond the existing direct Python/Node script execution.
