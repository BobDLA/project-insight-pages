# Quality Checklist

Use this as a revision checklist, not a numeric scoring sheet.

## Must Pass

- UI design requirements are traceable to the project docs or an external reference, such as `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`, while the final page still follows the report's technical-reader purpose.
- The report has one responsive HTML page per project unless a second artifact was explicitly requested.
- The report has a clear verbal adoption stance and no user-facing numeric project score.
- `新用户先看什么` preserves Lean content: audience, problem, differentiation, why now, and minimum validation path.
- A new technical reader can understand the usage scenario, core value, differentiation, demo, and mechanism.
- Gold Example uses the best relevant source: real media first only when it directly shows the core product/workflow/action/output; repo example second; constructed scenario last.
- Static analysis is labeled honestly; no runtime success is claimed without execution evidence.
- The mechanism diagram type is selected from actual project behavior, not copied from a fixed template.
- The visible mechanism diagram is drawn as a coherent flow/component/system canvas, with an interaction or source tab when useful.
- Architecture lenses start with complexity, selected framework, tailoring reason, and omitted views. Simple/medium projects default to C4; complex/heterogeneous projects may use 4+1 with C4/UML notation.
- A core interaction diagram is prioritized regardless of framework; if absent, the report explains why.
- Section titles, notes, diagram headers, and body content share a consistent left edge; no large left rail should squeeze the content.
- Desktop, 1080px vertical, and mobile layouts have no page-level horizontal overflow, clipped diagrams, or unreadably dense text blocks.
- Mermaid or structured diagram source is preserved with the report.
- Optional architecture lenses are used only when they add concrete signal. They must not be unrelated text cards labeled Logical/Process/Physical, and HTML must not show Mermaid source as the only representation; render a visible diagram and keep source separately.
- Key assets are tied to concrete files, docs, examples, or static evidence.
- Adoption checks are specific and limited to items that change a trial/use decision.
- If available, `scripts/validate_report.py` passes on the Markdown and HTML artifacts; browser/layout verification is still needed for visual quality.

## Fail If

- The report contains a second duplicated infographic HTML without explicit user request.
- The report contains concrete numeric ratings, `总分`, `综合评分`, or similar scoring language.
- Lean content is removed or reduced to a generic project summary.
- Gold Example uses media that is only adjacent to the project, such as a side integration, generic branding, unrelated client UI, mascot, or ecosystem screenshot that does not explain the core value.
- UML+CLD is always used even when another diagram type fits better.
- 4+1 is forced onto a rule pack, small utility, or prompt/skill repo where Logical/Physical/Process views add no real signal.
- The architecture section skips complexity/framework/tailoring decisions or omits the core interaction diagram without explanation.
- A BOT chart implies measured trends when it is only conceptual.
- The same structure is forced onto API/proxy, desktop app, and documentation/skill projects without adapting diagram choice and emphasis.
- Large paragraphs are left unstructured when bullets, label/value rows, or diagrams would be easier to scan.
- Diagram content appears as disconnected cards, unaligned arrows, clipped SVG/canvas, or tiny text with no mobile fallback.
