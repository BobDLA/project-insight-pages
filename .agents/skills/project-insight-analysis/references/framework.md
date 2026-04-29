# Project Insight Framework

## Preferred Report Shape

Generate one responsive HTML page per project by default. The page should work as both a readable report and a vertical screenshot surface.

Use this structure for first-time technical readers:

1. 新用户先看什么
2. Gold Example / Demo
3. 项目机制图（可选）
4. 架构视角（可选；自适应选择 C4 / 4+1 / UML）
5. 核心资产与价值
6. 采用前确认与证据边界

`新用户先看什么` must preserve and strengthen the Lean/精益判断 content:

- 适合谁
- 解决什么问题
- 和别的方案哪里不同
- 为什么现在值得看
- 最小验证方式

Do not force a fixed number of bullets. Use as many as needed, but keep each bullet scan-friendly and avoid paragraph blocks.

## Diagram Selection

Choose diagrams from actual project behavior. Do not hard-code project-specific flows in the skill prompt.

| Diagram | Use When |
| --- | --- |
| UML Sequence / Interaction | Explaining one task/request from input to output |
| UML Component / Logical | Explaining module or adapter relationships |
| CLD | Explaining feedback loops, trust loops, adoption loops, or control loops |
| SFD | Explaining stocks/flows such as context, cache, backlog, data, skills |
| BOT | Explaining behavior over time; mark as conceptual unless measured |

Mixed UML + system dynamics diagrams are allowed when useful, but UML+CLD is only an example, not the default.

Keep Mermaid or another structured source with the report. Generated bitmap images may be used for presentation, but they must not replace the editable source.

## Adaptive Architecture Views

Start with complexity assessment, then choose the lowest-cost useful architecture lens.

Decision rules:

- Simple/medium projects: use C4 L1 Context + C4 L2 Container + a core Dynamic/Sequence diagram.
- Complex/heterogeneous projects: use 4+1 as theory classification, but draw concrete views with C4/UML/Mermaid.
- Rule packs, prompt libraries, skills, and small utilities: use C4-light, rule execution flow, or distribution structure. Do not force Logical/Physical/Process views.

Architecture Decision Note must include:

- Project complexity assessment
- Selected framework
- Tailoring reason
- Omitted views and why

Core interaction diagram priority: every architecture lens should include at least one core process interaction diagram unless the project genuinely has no meaningful interaction path.

Fail if the architecture section is only a set of unrelated text cards labeled Logical/Process/Physical, or if HTML shows Mermaid source as the only representation. Render the diagram visibly and keep Mermaid or equivalent structured source with the report.

Prefer semantic drawing patterns over generic graph auto-layout:

- Rule/skill projects: behavior constraint map and core-principle distribution map.
- API/proxy projects: request boundary, adapter chain, provider routing, and compatibility guard.
- Desktop/large apps: user workflow boundary, data bus/data source flow, local runtime, cache/state, and deployment boundary.

## HTML-first Report Shape

- Hero: project name, one-line positioning, adoption stance, and short explanation.
- Fact strip: non-scoring facts such as stars, formats, provider families, core contract, or source count.
- Main body prioritizes usage scenario, value, differentiation, demo, and mechanism.
- No numeric project score.
- Evidence and boundaries may be a final section or appendix.

## Gold Example Priority

Choose one demo surface in this order:

1. Real project image or video from README/docs/examples.
2. Repository example that demonstrates the intended behavior.
3. Constructed scenario based on source evidence.

Before selecting real media, apply a relevance gate:

- It must directly show the core product surface, core workflow, expected user action, or evaluated output.
- The caption must state what project behavior or value the media proves.
- If the media is a side integration, mascot, generic branding, unrelated client UI, or adjacent ecosystem artifact, do not use it as the Gold Example visual.
- When no relevant media exists, use a README/example command flow, before/after example, or structured scenario card instead.

If the demo is static, say so. Do not imply the project was installed, run, or connected to external providers.

## HTML Layout Principles

- External UI reference: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`. Use it as a source for design-system, responsive, accessibility, and verification discipline; do not copy landing-page or marketing-heavy patterns into technical project insight reports.
- First viewport must make the product/project unmistakable.
- Use a restrained technical report style: stable grid, clear hierarchy, readable body text, and a single visual anchor.
- Body text should be 16px or larger with 1.5-1.75 line-height.
- Use label/value rows, bullets, and diagrams instead of long paragraph blocks.
- Keep section headings, notes, diagram headers, and body content on a consistent left edge; avoid large left rails that squeeze the actual report.
- Navigation links must be at least 44px high.
- Mobile pages must not have page-level horizontal scroll.
- Avoid automatic keyword bolding; bold only key judgments, differences, and actions.

## Evidence Protocol

Evidence types:

- `README/docs`
- `code`
- `config`
- `repo-meta`
- `license`
- `static-inference`

Rules:

- Bind important claims to evidence.
- Mark inferred conclusions as `static-inference`.
- Static analysis must not claim runtime success.
