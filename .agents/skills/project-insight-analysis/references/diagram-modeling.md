# Diagram Modeling Rules

Use diagrams to explain project behavior, not to decorate the report.

## Selection Rules

- Use UML Sequence / Interaction when the reader needs to follow one request, task, or user workflow.
- Use UML Component / Logical when the reader needs module boundaries, adapters, data layers, or distribution files.
- Use CLD when feedback loops matter: adoption, trust, compatibility coverage, risk controls, or learning loops.
- Use SFD when stocks and flows matter: context accumulation, cache growth, backlog reduction, skill registration, data inflow.
- Use BOT when a time trend matters. If no measured data exists, label it as a conceptual trend.

Do not always use UML + CLD. That combination is appropriate only when both micro execution and macro feedback loops are important.

UML, CLD, SFD, and BOT are optional components. If a diagram would restate the text, add vague abstractions, or imply a runtime structure that is not present, omit it.

Architecture views are adaptive. Use C4 for simple/medium projects, use 4+1 only for complex/heterogeneous projects with concrete runtime, development, scenario, and deployment boundaries, and use C4-light or rule execution flow for prompt/skill/rule-pack projects. A promised architecture section must include a complexity/framework/tailoring decision note and at least one core interaction diagram unless the project truly has no meaningful interaction path.

## Mermaid

Prefer Mermaid or another structured source as the editable diagram source. Store the source with the HTML or Markdown report.

For the visible HTML report, do not rely on raw text lists when a diagram is promised. Use one of these presentation patterns:

- SVG flow canvas for request/task/user workflows.
- SVG component canvas for module boundaries and contracts.
- SVG or Mermaid system dynamics canvas for CLD, SFD, or BOT.
- A tabbed diagram shell when multiple views are useful: `主流程`、`组件关系`、`系统动力学`、`图源`.
- A mixed UML + system dynamics canvas when useful: central task/request interaction plus only the feedback, stock/flow, or trend layer that explains the project.
- A vertical mobile fallback for small screens so the reader does not need page-level horizontal scrolling.

If the report also uses generated bitmap images:

- Keep the prompt/source next to the image.
- Treat the image as presentation, not as the only diagram artifact.
- Ensure Chinese labels remain readable.

## Mixed UML + System Dynamics Image Style

When generating a bitmap similar to `docs/reference/image.md`, use:

- Modern technical blueprint / BioRender-like style.
- Central UML interaction or sequence backbone.
- Optional outer CLD/SFD/BOT layer only if the project actually needs it.
- Blue for reinforcing or growth dynamics.
- Orange/gray for balancing or control dynamics.
- Clear Chinese labels and consistent icons.
- A concrete scenario title such as `用户：从 Claude Code 发起一次工具调用任务`.

The OpenClaw example is a style reference, not a fixed template.
