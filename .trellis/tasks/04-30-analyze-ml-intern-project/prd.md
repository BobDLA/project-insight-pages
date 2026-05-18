# PRD: Analyze Hugging Face ml-intern

## Goal

Use the project-insight-analysis skill to produce a decision-oriented static analysis report for https://github.com/huggingface/ml-intern.

## Deliverables

- Evidence-backed Markdown report.
- Evidence log with source categories and boundaries.
- Full responsive HTML insight page.
- Registered static-site entry under `site/projects/ml-intern/` with GitHub, DeepWiki, and Zread links.

## Analysis Scope

- Static analysis only. Do not run `ml-intern`, start its backend/frontend, create HF sandboxes, or launch HF Jobs.
- Inspect README/docs, source entrypoints, architecture and runtime code, manifests, CI/review workflow, tests, license state, and GitHub metadata.
- Preserve Lean decision content: audience, problem, differentiation, why now, and minimum validation path.
- Use diagrams that fit the project: core user/task interaction, tool/module boundaries, and adoption feedback loops where they add signal.

## Acceptance Criteria

- The report states an adoption stance without a numeric project score.
- Demo status is explicitly labeled as static projection.
- Key claims cite evidence from README/docs, code, config, repo metadata, tests, or static inference.
- HTML has no raw-only diagram presentation; visible SVG diagrams and source details are included.
- Skill validator passes for Markdown and HTML.
- Project is registered in `site/projects.json` and `site/index.html` is rebuilt.
