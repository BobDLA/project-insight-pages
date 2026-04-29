# Skill 一致性校准总结

校准对象：`.agents/skills/project-insight-analysis`

## 校准结论

skill 已调整为 v5 可复用状态：默认生成单一响应式 HTML，保留并增强 Lean 判断，按项目实际选择 UML / CLD / SFD / BOT / 混合图；项目机制图和架构视角都是可选组件。架构视角改为自适应生成：简单/中等项目优先 C4，复杂/异构项目才使用 4+1，并且核心交互图优先。HTML 中的架构图按项目语义绘制为可读图形，Mermaid / 结构化图源只作为折叠源码保留。

## 三项目校准结果

| 项目 | 类型 | 采用口径 | 结论 |
| --- | --- | --- | --- |
| free-claude-code | API/proxy | 适合本地试点 | 通过 |
| FinceptTerminal | 桌面大型应用 | 适合学习研究；机构采用前需审计 | 通过 |
| andrej-karpathy-skills | 文档/skill | 适合作为 Agent 行为基线；仍需 eval 验证 | 通过 |

一致性检查项：

- 单一 HTML 输出，无独立信息图版本。
- 无项目分数、总分或评分条。
- Lean 判断包含适合谁、问题、差异、时机和最小验证。
- 每个项目按实际机制选择图型，而不是固定套 UML+CLD。
- 对需要同时解释微观执行和宏观反馈的项目，可使用 UML + 系统动力学混合图。
- 每个项目都有可见架构图和 Mermaid / 结构化图源；源码不会作为唯一图形展示。
- 架构图按项目语义绘制，不使用同一套通用自动布局套所有项目。
- 架构视角先输出复杂度评估、框架选择、裁剪理由和省略内容。
- free-claude-code 使用 C4；FinceptTerminal 使用 4+1 + C4/UML 标注；andrej-karpathy-skills 使用 C4-light。
- 每个架构视角都优先提供核心交互 Mermaid。
- 静态 Demo 均明确标注未运行。

结论：skill 达到可复用状态。
