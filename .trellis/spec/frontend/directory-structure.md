# Directory Structure

> The frontend is a generated static site. There is no `src/` frontend app,
> component directory, routing framework, or bundler.

---

## Directory Layout

```text
site/
  index.html
  projects.json
  projects/
    <slug>/
      index.html
      analysis.md
      assets/
        <asset files>
```

---

## Page Ownership

- `site/index.html` is the overview page and should be generated from
  `tools/generate_project_index.py`.
- `site/projects/<slug>/index.html` is a project report page.
- `site/projects/<slug>/analysis.md` is the Markdown report paired with the HTML
  report.
- `site/projects/<slug>/assets/` contains report-specific images/media.

Supported example:

```python
record = {
    "slug": slug,
    "title": args.title or slug,
    "file": f"projects/{slug}/",
    "markdown": f"projects/{slug}/analysis.md",
    "repo": args.repo,
    "category": args.category,
    "adoption": args.adoption,
    "audience": args.audience,
    "summary": args.summary,
    "problem": args.problem,
    "difference": args.difference,
    "demo": args.demo,
    "architecture": args.architecture,
    "tags": tags,
    "updated": args.updated or date.today().isoformat(),
}
```

---

## Asset Placement

When registering or generating project-specific assets, copy them into the
project's own asset directory.

Supported example:

```python
for asset in args.asset:
    source = Path(asset)
    copy_if_given(asset, project_dir / "assets" / source.name)
```

---

## Naming Conventions

- Project page directories are slug-based: `site/projects/<slug>/`.
- The project HTML entry is always `index.html`.
- The paired Markdown report is always `analysis.md`.
- Asset file names are preserved when copied into `assets/`.

---

## Do Not Introduce Without A Requirement

- A frontend framework directory such as `src/components/`.
- A client-side router.
- A bundler output directory committed to the repo.
- Shared global assets for project-specific images that already belong under a
  project slug.
