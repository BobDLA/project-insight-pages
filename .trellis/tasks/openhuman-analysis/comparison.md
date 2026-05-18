# OpenHuman Report Comparison

- Compared: original `site/projects/openhuman/analysis.md` draft before skill update vs regenerated report after adding core innovation extraction.
- Date: 2026-05-18
- Basis: local report artifacts, Zread overview, README/CLAUDE.md/source verification.

## Summary

新版报告明显提升了内容质量：旧版的优点是采用判断、风险边界和 Gold Example 完整；新版保留这些部分，同时把 Zread 抓到的高信号机制转成经过源码核验的报告主体。

2026-05-18 二次修订后，报告又补齐了三个弱项：Mascot/Meeting/Voice 从“提到功能”提升为“实时会议参与机制”；机制图把后台 auto-fetch 与前台 agent turn 视觉拆分；核心资产里的 TokenJuice 从 WHAT 补到 rule overlay 的 HOW。

## Comparison by Dimension

| Dimension | Original report | Regenerated report |
| --- | --- | --- |
| 范式判断 | 泛化为“AI 助手缺少持久个人上下文”。 | 明确写成 `context first, conversation second`：先同步/压缩个人数字生活，再让对话使用已有上下文。 |
| 机制深度 | 知道有 Memory Tree、auto-fetch、tool registry，但解释较浅。 | 补充 20 分钟 auto-fetch、`<=3k-token` chunks、canonicalize/chunk/score、hierarchical summary trees、SQLite/FTS/vector/graph、Obsidian vault。 |
| Intelligence Layer | 只在 evidence 中提到 TokenJuice，正文几乎没解释。 | 正文纳入 Model Routing + TokenJuice + Subconscious/cron，并解释它们分别解决模型选择、上下文成本和后台任务问题。 |
| 架构 contract 理解 | 写到 `src/core/all.rs` 注册大量控制器。 | 提升为 Controller System：`ControllerSchema` 是 transport-agnostic domain contract，`all.rs`/`dispatch.rs` 是 registry + validation + routing。 |
| 技术路径独特性 | 未提 CEF webview scanner。 | 补充 CEF/CDP/IndexedDB scanner 与“migrated providers 不新增 JS injection”的安全边界。 |
| Mascot / Meeting / Voice | 只把 mascot/voice 当产品表面提到。 | 补充 meeting agent 作为 Google Meet 真实参会者的机制：streaming STT、diarization、transcript -> Memory Tree、会中工具调用、TTS outbound mic、lip-sync camera。 |
| 机制图表达 | 单条请求链，容易把后台同步和前台对话混在一起。 | SVG 与 Mermaid 图源拆成两条 lane：后台 auto-fetch -> Memory Tree；前台 UI -> Core -> ControllerSchema/tools -> TokenJuice/model routing，并用 recall 箭头连接。 |
| 核心资产 HOW | TokenJuice 写成“入 LLM 前压缩”。 | 补充 builtin/user/project rule overlay 与 classify -> match rule -> reduce 工作链。 |
| 采用风险与验证路径 | 已覆盖隐私、OAuth、构建、测试、GPL。 | 进一步加入 Memory Tree 质量、TokenJuice 信息损失、CEF scanner 权限/ToS、Zread 纠偏等验证项。 |
| 外部资料核验质量 | 没有利用 Zread 机制洞察。 | 把 Zread 作为线索池：采纳 5 个机制点，同时修正 sidecar process 与 React 18 等过期/错误说法。 |

## Zread Leads Handling

| Zread lead | Handling | Verification |
| --- | --- | --- |
| `context first, conversation second` | Adopted as core thesis. | Supported by README “Context in minutes, not weeks” and one-sync-pass context claims. |
| Memory Tree mechanics | Adopted and deepened. | Supported by README, memory README, privacy docs. |
| Intelligence Layer | Adopted. | Supported by README, TokenJuice docs, source tree modules `routing`, `tokenjuice`, `subconscious`. |
| Controller System | Adopted and reframed. | Supported by `src/core/mod.rs`, `src/core/all.rs`, `src/core/dispatch.rs`. |
| CEF webview scanner | Adopted. | Supported by `CLAUDE.md` scanner/no-new-JS-injection guidance. |
| Sidecar process | Corrected. | `CLAUDE.md` says sidecar was removed and core is linked in-process. |
| React 18 | Corrected. | `app/package.json` says React `^19.1.0`. |

## Residual Limits

- The report is still static analysis. It does not prove OAuth scope handling, backend broker behavior, telemetry defaults, TokenJuice quality, or Memory Tree recall quality.
- Meeting Agent claims are still static documentation/source inference. They need runtime checks for consent, platform policy, audio/video routing, latency, interruption behavior, transcript storage, and deletion.
- GitBook architecture pages conflict with current `CLAUDE.md` in places, so runtime/source truth should be preferred for future updates.
- A stronger next step would be a controlled desktop trial with a test Gmail account and network tracing.
