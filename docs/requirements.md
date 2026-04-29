# 用户要求整理

本文整理本项目在对话中形成的全部关键要求，作为后续维护和复用 `project-insight-analysis` skill 的准绳。

## 1. 分析框架

- 最终方案应结合 `docs/reference/rules.md`、`docs/reference/lean.md`、`docs/reference/demo.md`、`docs/reference/4+1.md` 等早期材料，但不能机械拼接。
- Lean Canvas 和快速决策简报有重叠，应合并为“项目价值判断”或 HTML 中的“新用户先看什么”。
- 4+1 / C4 / UML / 系统动力学都是分析支架，不是固定一级模块。
- 工程化成熟度、架构与运行机制存在交集，应合并到“技术实现与可落地性”，不要重复分区。
- “INTJ 式评价”不应作为独立模块；如果需要尖锐判断，应融入最终建议或采用判断。
- `lightning talk` 不作为正式定义使用，避免让方案显得口径不准。

## 2. 最终报告结构

面向首次接触项目的技术读者，HTML 报告采用：

1. 新用户先看什么
2. Gold Example / Demo
3. 项目机制图
4. 架构视角（可选）
5. 核心资产与价值
6. 采用前确认与证据边界

其中“新用户先看什么”必须强化：

- 适合谁
- 解决什么问题
- 和别的方案哪里不同
- 为什么现在值得看
- 最小验证方式

## 3. 内容取舍

- 去掉打分环节。分数不一致、没有横向对比意义、指向性不强。
- 不再输出项目总分、综合评分、评分条或类似表达。
- 内容重点要从新用户角度说明使用场景、价值、差异点。
- CI/CD、风险、壁垒、最终建议等交付审计内容要精简，只保留影响试用/采用决策的部分。
- 大段文字必须拆成 label/value、bullet 或流程图，避免不便阅读。
- 加粗只用于真正关键的判断、差异点和行动，不做自动关键词加粗。
- DeepWiki 内容可以作为辅助理解，但要标明证据边界，不能替代 README/docs/source 证据。

## 4. Gold Example / Demo

Gold Example 选择优先级：

1. 真实项目图片或视频，但必须直接展示核心产品界面、核心工作流、用户动作或输出结果，不能只是仓库里的旁支图片。
2. 仓库中的 example / README 示例。
3. 基于源码证据构想的使用场景。

静态分析时必须明确标注“静态推演，未运行”，不能伪造运行结果。
若图片只是旁支集成、品牌图、无关客户端 UI 或生态截图，不能作为 Gold Example 主视觉，应降级为 README/example 流程卡片。

## 5. 图表与建模

- 图表是可选组件，只在能增加解释力时使用。
- 按项目实际从 UML Sequence/Interaction、UML Component/Logical、CLD、SFD、BOT、混合图中选择。
- 不管采用 C4、4+1、UML 或系统动力学，都必须优先提供一个核心业务流程的交互图；没有交互图时要说明为什么该项目不适合。
- 不要把示例中的固定流程写进提示词；每个项目应根据实际机制生成图。
- UML + 系统动力学混合图可以使用，但只是可选表达方式。
- `docs/reference/image.md` 和用户截图中的 UML + CLD / 系统动力学混合图是风格参考，不是固定模板。
- Mermaid 和生成图片都可以用；可视图表必须有结构化源。
- 图表不能是未对齐卡片或抽象文字块，必须画成可读的流程、组件、反馈、存量或趋势画布。
- 手机端需要纵向 fallback，避免图表文字太小或页面级横向滚动。

## 6. 自适应架构视角

- 架构视角先做复杂度判断，再选择框架，不再默认输出 4+1。
- 简单/中等项目优先使用 C4：L1 Context + L2 Container + 核心 Dynamic/Sequence。
- 复杂/异构项目才使用 4+1 作为理论分类，并用 C4/UML/Mermaid 表达具体视图。
- 复杂项目的 4+1 输出至少要包含：场景视图、过程视图、开发/实现视图；有真实部署边界时再补物理/部署视图。
- 对规则包、prompt/skill、小工具，不应强行套 Logical/Physical/Process；可用 C4-light 或规则执行链路替代。
- Mermaid 图源必须保留，但 HTML 中不能只展示源码；架构 section 必须把 Mermaid 渲染为可读图形，并在移动端提供纵向 fallback。
- 架构 section 不能只是五张文字卡片。
- 架构图不要依赖通用自动布局；应按语义选择图法，例如规则包使用“规则约束 agent / 核心原则分发”，桌面应用使用“工作流边界 / DataHub 数据流 / 部署边界”。

## 7. 页面排版

- 页面需要彻底重设计，不能只是把 Markdown 包成 HTML。
- UI 设计参考需可追溯，外部参考记录为 `docs/reference/ui-design-references.md`，来源包括 `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`。
- 保留单一响应式 HTML，不再单独维护 infographic HTML。
- section 标题、说明和正文左边界必须统一，不出现左侧空列或右侧内容过小。
- 项目机制图 header 中的选择理由、场景、图型标签应左对齐顺排。
- 卡片内部要 bullet 对齐，文字大小、间距、分区节奏要统一。
- 首屏要明确项目、采用判断和关键事实。
- 页面在桌面、1080px 竖向截图、390px 手机宽度下都不能横向溢出。
- 页面风格参考成熟 UI 排版原则：稳定网格、清晰层级、克制配色、可扫描文本、可访问性底线和响应式验证。

## 8. 项目分析要求

首批三个项目：

- `Alishahryar1/free-claude-code`
  - 类型：API/proxy 工具。
  - 重点：Claude Code 请求、Anthropic Messages/SSE/tool use 兼容、provider routing、本地/外部模型适配。
  - 采用口径：适合本地试点，公网共享前需补鉴权和日志脱敏。

- `Fincept-Corporation/FinceptTerminal`
  - 类型：C++/Qt 桌面金融终端。
  - 重点：用户研究工作流、Qt Screen、DataHub topic、Producer/Data Source、缓存/状态、研究视图。
  - 采用口径：适合学习研究；机构采用前需审计。

- `forrestchang/andrej-karpathy-skills`
  - 类型：文档/skill/规则包。
  - 重点：模糊需求如何通过规则变成澄清、最小修改和验证闭环。
  - 采用口径：适合作为 Agent 行为基线；仍需 eval 验证。
  - 不展示 4+1。

补充项目：

- `garrytan/gbrain`
  - 类型：个人/团队知识操作工具。
  - 重点：README 命令流、知识导入、查询、MCP `put_page` 写回和最小验证闭环。
  - Gold Example 不使用与核心流程无关的 `voice-client` / `Wintermute` 图片；若没有核心界面截图，使用结构化流程卡片。

## 9. 交付要求

- 生成最终可复用 skill。
- 生成最终 HTML 报告和 Markdown 审计版。
- 生成 zip：
  - `dist/project-insight-analysis-skill.zip`
  - `dist/project-insight-reports.zip`
- 提供最终执行报告。
- 生成汇总入口页，链接所有项目概览，并支持后续项目扩充：
  - 入口页为 `site/index.html`。
  - 项目清单为 `site/projects.json`。
  - 项目多时应支持搜索、分类筛选、采用口径筛选、排序和统一列表视图。
- 整理项目目录：
  - 不需要、临时、旧版本材料放入 `temp/`。
  - 用户要求整理成文档。
  - 添加 README 和目录说明。
