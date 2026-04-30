---
name: project-insight-analysis
description: Analyze GitHub, open-source, internal, or AI Agent projects with a decision-oriented Lean framework plus optional architecture/diagram lenses. Use when the user asks to evaluate a project, judge project value, generate a project insight report, compare project maturity, produce Gold Example demos, inspect architecture/business flow/key assets, or package reusable project analysis reports.
---

# Project Insight Analysis

Use this skill to produce decision-oriented project reports, not generic README summaries. The goal is to judge value, explain how the project works, identify key assets and risks, and produce evidence-backed Markdown plus a readable HTML insight page.

The HTML page is the primary deliverable unless the user explicitly asks for text only. Do not generate a thin two-line HTML wrapper around a Markdown report.

## Workflow

0. **Check existing site reports**
   - When the user gives a GitHub URL, repo path, or project slug in this repository, first run `python tools/project_report_manager.py check <repo-or-slug>` from the repository root.
   - If it already exists in `site/projects.json`, return the existing `site/projects/<slug>/` and `site/projects/<slug>/analysis.md` paths unless the user explicitly asks to regenerate.
   - If it does not exist, continue with the analysis workflow and register the finished report with `tools/project_report_manager.py register`.

1. **Set execution boundary**
   - Default to static analysis unless the user explicitly asks to run the project.
   - If static, never claim the Demo was run. Write `Demo 状态：静态推演，未运行`.

2. **Collect evidence**
   - Read README/docs, manifests, source entrypoints, architecture docs, CI, license, and repo metadata.
   - Classify evidence as `README/docs`, `code`, `config`, `repo-meta`, `license`, or `static-inference`.

3. **Write the report**
   - Follow `references/report-template.md`.
   - Do not produce a user-facing numeric project score. Scores are hard to compare across project types and tend to obscure the actual decision.
   - Produce one responsive HTML page per project. Do not create a separate infographic HTML unless the user explicitly requests a second artifact.
   - Prefer a new-user-first technical-reader structure:
     1. 新用户先看什么：适合谁、解决什么问题、和别的方案哪里不同、为什么现在值得看、最小验证方式
     2. Gold Example / Demo
     3. 项目机制图：可选；按项目实际选择 UML / CLD / SFD / BOT / 混合图
     4. 架构视角：可选；先评估复杂度，再裁剪 C4 / 4+1 / UML 组合
     5. 核心资产与价值
     6. 采用前确认与证据边界
   - Lean Canvas / 精益判断 must be preserved and strengthened. Do not remove `适合谁`、`解决什么问题`、`和别的方案哪里不同`.
   - If the user specifically requires the older five-module framework, map it without adding extra peer modules: Lean Canvas belongs inside `项目价值判断`; flow and assets belong inside `核心业务流程与关键资产`; architecture lenses such as 4+1 belong inside `技术实现与可落地性` only when they add real explanatory value.

4. **Adapt to project type**
   - API/proxy tools: focus on request/response flow, protocol contracts, routing, auth, error handling, provider compatibility.
   - Desktop/large apps: focus on user workflows, UI/service/data layers, install/build, release, testing, license.
   - Documentation/skill projects: focus on instruction flow, distribution formats, consistency, examples, eval gaps.
   - Choose diagrams from actual project behavior:
     - UML Sequence/Interaction for request or task execution.
     - UML Component/Logical for module relations.
     - CLD for feedback loops.
     - SFD for stocks and flows such as context/data/skills/backlog.
     - BOT for conceptual time trends. Mark BOT as conceptual unless measured data exists.
   - UML + system dynamics mixed diagrams are allowed when useful: use a central task/request interaction backbone and add only the CLD/SFD/BOT layer that explains adoption, trust, risk, context, backlog, or other real feedback.
   - UML + CLD mixed diagrams are examples, not a required template.
   - Architecture lens decision:
     - Simple/medium projects: prefer C4 L1 Context + C4 L2 Container + one core Dynamic/Sequence diagram.
     - Complex/heterogeneous projects: use 4+1 as the theory lens, but draw concrete views with C4/UML/Mermaid. Include Scenario, Process, Development/Implementation, and Deployment/Physical only when evidence supports them.
     - Documentation/skill/rule-pack projects: use C4-light, rule execution flow, or distribution structure; do not force Logical/Physical/Process cards.
     - A core interaction diagram has priority regardless of framework. If absent, explain why.

5. **Review**
   - Use `references/quality-rubric.md`.
   - Use a checklist, not a numeric project score.
   - When a report artifact exists, run `python scripts/validate_report.py <analysis.md> <report.html>` from this skill directory, or pass equivalent paths. Treat failures as required fixes and browser/layout checks as an additional layer.
   - Revise if the report overclaims, lacks evidence, misfits the project type, hides the practical usage scenario, buries value/differentiation under delivery details, or uses a fixed diagram shape that does not fit the project.

6. **Produce deliverables**
   - At minimum: `analysis.md`, `evidence.md`, and a full `report.html`.
   - In this repository, the final static-site location is `site/projects/<slug>/index.html` plus `site/projects/<slug>/analysis.md`; project-specific images belong under `site/projects/<slug>/assets/`.
   - After producing or updating a project report, update `site/projects.json` and rebuild `site/index.html` with `python tools/generate_project_index.py`. Prefer `python tools/project_report_manager.py register ...` when adding a new project because it copies artifacts and rebuilds the index.
   - For HTML, use `assets/html-template.html` as a report page template, not a summary wrapper. The default layout is a single responsive insight page: positioning hero, non-scoring fact strip, strengthened Lean section, Gold Example, optional interactive project mechanism diagram, optional architecture lens, core assets, adoption checks, and evidence boundary.
   - For GitHub projects, render hero resource links for `GitHub`, `DeepWiki`, and `Zread`. Derive `DeepWiki` and `Zread` from the GitHub URL as `https://deepwiki.com/<owner>/<repo>` and `https://zread.ai/<owner>/<repo>`; strip a trailing `.git` suffix. If the URL is not a GitHub repository URL, omit derived links instead of rendering broken anchors.
   - Render project diagrams as a coherent canvas, not as unrelated mini cards. Prefer SVG or Mermaid-rendered visuals for the visible diagram, keep structured source in a separate tab, and provide a mobile-readable vertical fallback when the full diagram would become too small.
   - Architecture sections must include a decision note: complexity, selected framework, tailoring reason, and omitted views. Do not output a fake 4+1 made of unrelated text cards.
   - In HTML, render architecture Mermaid or structured source as visible diagrams. Keep the source in a collapsible/source area; do not leave architecture diagrams as raw code blocks only.
   - Do not rely on a generic auto-layout for every architecture diagram. Choose a semantic drawing pattern: behavior constraints and distribution for rule/skill projects, request boundary and adapter chain for API/proxy projects, workflow/data bus/deployment boundaries for desktop or large apps.
   - Keep visual layout readable across desktop, 1080px vertical screenshots, and mobile; avoid page-level horizontal scroll, clipped diagrams, and mid-word title breaks.
   - Apply report-layout rules: 16px+ body text, 1.5-1.75 line-height, controlled text line length, 4/8px spacing scale, consistent max-width, semantic color tokens, visible focus states, 44px touch targets in navigation, no page-level horizontal scroll, and table wrappers or card layouts on mobile.
   - Gold Example priority: real project image/video first; repository example second; constructed scenario only when neither exists.
   - A real image/video is valid only if it directly shows the project's core product surface, core workflow, expected user action, or evaluated output. Do not use a repository image merely because it exists; if the image is a side integration, mascot, unrelated UI, generic branding, or does not help a new reader understand the project value, downgrade to a repository example or structured flow demo.
   - Keep Mermaid or structured diagram source with the HTML. Generated bitmap images are optional display assets and must not replace the source.

## References

- Full framework: `references/framework.md`
- Report template: `references/report-template.md`
- Quality rubric: `references/quality-rubric.md`
- Diagram modeling rules: `references/diagram-modeling.md`
- Report validator: `scripts/validate_report.py`
- Site manager: `tools/project_report_manager.py` in the repository root
- External UI layout reference: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
