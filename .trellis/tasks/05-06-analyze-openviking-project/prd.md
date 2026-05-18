# Analyze Volcengine OpenViking project

## Goal

Produce a decision-oriented Project Insight Analysis report for `https://github.com/volcengine/OpenViking`, following the local `project-insight-analysis` skill. The report should help a technical reader quickly judge what OpenViking is, who it fits, how it works, which assets matter, and what to verify before adoption.

## What I already know

* User explicitly requested the local skill `.agents/skills/project-insight-analysis`.
* The repository URL is `https://github.com/volcengine/OpenViking`.
* `tools/project_report_manager.py check` reports no existing site report for this repository and suggests slug `OpenViking`.
* The skill requires static evidence collection from README/docs, manifests, source entrypoints, architecture docs, CI, license, and repo metadata.

## Assumptions

* Default analysis boundary is static analysis; the project will not be installed or run unless later requested.
* Final site report should be registered into the local static report index.
* The HTML page is the primary deliverable, with Markdown evidence preserved for future updates.

## Requirements

* Collect evidence from the upstream GitHub repository and classify it as README/docs, code, config, repo-meta, license, or static-inference.
* Produce at minimum:
  * `.trellis/tasks/05-06-analyze-openviking-project/analysis.md`
  * `.trellis/tasks/05-06-analyze-openviking-project/evidence.md`
  * `.trellis/tasks/05-06-analyze-openviking-project/report.html`
* Register final static-site artifacts under `site/projects/OpenViking/` using the project report manager when possible.
* Include derived resource links for GitHub, DeepWiki, and Zread.
* State runtime boundary honestly: `Demo 状态：静态推演，未运行`.
* Do not include a user-facing numeric project score.
* Preserve Lean judgment sections: `适合谁`, `解决什么问题`, `和别的方案哪里不同`, `为什么现在值得看`, `最小验证方式`.
* Use diagrams that fit the actual project behavior and preserve diagram source in the report.

## Acceptance Criteria

* [ ] `analysis.md`, `evidence.md`, and full `report.html` exist for OpenViking.
* [ ] `site/projects/OpenViking/index.html` and `site/projects/OpenViking/analysis.md` are registered.
* [ ] `site/projects.json` and `site/index.html` are updated through existing tools.
* [ ] The skill validator passes on the generated Markdown and HTML artifacts.
* [ ] The final answer lists generated paths, validation status, and static-analysis boundary.

## Out of Scope

* Running OpenViking server, CLI, containers, or examples.
* Benchmarking retrieval quality or performance.
* Comparing OpenViking quantitatively against other context databases.
* Adding a separate infographic HTML page.

## Technical Notes

* Skill file read: `.agents/skills/project-insight-analysis/SKILL.md`.
* Template read: `.agents/skills/project-insight-analysis/references/report-template.md`.
* Quality rubric read: `.agents/skills/project-insight-analysis/references/quality-rubric.md`.
