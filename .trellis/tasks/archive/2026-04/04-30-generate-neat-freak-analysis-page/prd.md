# Generate neat-freak analysis page

## Goal

Generate a new Project Insight analysis page for the `neat-freak` skill under `KKKKhazix/khazix-skills`, publish it into the static site, and register it in the project index.

## What I already know

* User asked: `生成这个的 分析页 https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak`.
* `tools/project_report_manager.py check` returned no existing registered report for `neat-freak`.
* Existing project pages live under `site/projects/<slug>/` with `index.html` and `analysis.md`.
* `site/projects.json` is the project registry and `tools/generate_project_index.py` rebuilds `site/index.html`.
* The `project-insight-analysis` skill requires at least `analysis.md`, `evidence.md`, and a full responsive HTML report; final static-site location is `site/projects/<slug>/index.html` plus `site/projects/<slug>/analysis.md`.

## Assumptions

* Slug: `neat-freak`.
* Report target is the `neat-freak` subdirectory, not the entire `khazix-skills` repository.
* Default analysis mode is static analysis. Do not claim the skill was run.
* Derived resource links should point to:
  * GitHub: `https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak`
  * DeepWiki: `https://deepwiki.com/KKKKhazix/khazix-skills`
  * Zread: `https://zread.ai/KKKKhazix/khazix-skills`

## Open Questions

* None blocking. Use existing site/report conventions.

## Requirements

* Analyze README/docs, skill instruction files, manifests/config, examples, and repository metadata available for `neat-freak`.
* Produce evidence-backed Markdown with a clear adoption stance and no numeric score.
* Produce a full responsive HTML report, not a thin wrapper.
* Preserve Lean framing: `适合谁`, `解决什么问题`, `和别的方案哪里不同`, `为什么现在值得看`, `最小验证方式`.
* Include `Demo 状态：静态推演，未运行`.
* Use diagram choices appropriate for a documentation/skill/rule-pack project.
* Include GitHub, DeepWiki, and Zread resource links in the HTML.
* Register the project in `site/projects.json` and rebuild `site/index.html`.

## Acceptance Criteria

* [x] `site/projects/neat-freak/analysis.md` exists and follows the project insight report structure.
* [x] `site/projects/neat-freak/index.html` exists and is a readable standalone insight page.
* [x] `site/projects/neat-freak/evidence.md` or equivalent task research artifact records evidence and boundaries.
* [x] `site/projects.json` contains a `neat-freak` record.
* [x] `site/index.html` is rebuilt and links to the new page.
* [x] Report validation passes or any limitation is documented.
* [x] Static analysis boundary is explicit; no runtime claim is made.

## Definition of Done

* [x] Quality checks run for generated report artifacts.
* [x] Layout is inspected enough to catch obvious broken HTML, missing links, and page-level overflow risks.
* [x] Trellis check step is completed before final response.

## Verification

* `python .agents/skills/project-insight-analysis/scripts/validate_report.py site/projects/neat-freak/analysis.md site/projects/neat-freak/index.html` -> OK.
* `python3 -m py_compile tools/project_report_manager.py tools/generate_project_index.py tools/generate_final_insight_reports.py` -> OK.
* `python3 -m json.tool site/projects.json >/dev/null` -> OK.
* `node --check tools/verify_reports.js` -> OK.
* Playwright `tools/verify_reports.js` across desktop/poster/mobile -> OK for index and all 5 project pages, including `neat-freak`; no bad images, page-level horizontal overflow, console warnings, or page errors.
* 2026-04-30 layout refinement: updated the index row direction to match the provided table-style reference: three column headers (`工具与简介`, `核心要点`, `资源与链接`), circular project icons, icon-labeled core rows, and vertical resource buttons; regenerated `site/index.html`; reran `node --check`, Python compile, JSON validation, and Playwright verification -> OK.
* Trellis check found stale generated Markdown reports for FinceptTerminal, andrej-karpathy-skills, and free-claude-code after the report generator started emitting `Demo 状态：静态推演，未运行`; regenerated them with `tools/generate_final_insight_reports.py` and reran validation -> OK.

## Spec Update Review

* Updated `.trellis/spec/frontend/component-guidelines.md` and `.trellis/spec/frontend/quality-guidelines.md` with the overview report-list three-column table-style layout contract and verification expectation.
* Existing backend specs already cover project report artifact paths, `site/projects.json` registry contract, derived GitHub resource links, and Playwright verification expectations.

## Out of Scope

* Running the skill inside Claude Code or another agent runtime.
* Analyzing every other skill under `khazix-skills`.
* Changing unrelated existing project reports unless required by the site index rebuild.

## Technical Notes

* Existing comparable report: `site/projects/andrej-karpathy-skills/`.
* Skill instructions: `.agents/skills/project-insight-analysis/SKILL.md`.
* Report template: `.agents/skills/project-insight-analysis/references/report-template.md`.
* Quality rubric: `.agents/skills/project-insight-analysis/references/quality-rubric.md`.
