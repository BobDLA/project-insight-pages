# Project Insight Pages

这是一个项目洞察报告集合，用来帮助读者快速判断一个开源项目：

- 适合谁
- 解决什么问题
- 和别的方案有什么不同
- 最小验证路径是什么
- 架构和运行机制是否讲得清楚
- 采用前有哪些边界需要确认

报告不是 README 摘要，也不是项目评分榜。它更像一份面向首次接触项目的技术判断卡：先讲使用场景和价值，再补 Demo、机制图、架构视角和证据边界。

## 阅读入口

优先从线上站点进入：

- [项目洞察总览](https://bobdla.github.io/project-insight-pages/)

如果你正在浏览仓库文件，也可以打开本地入口：

- [本地站点首页](site/index.html)

## 已收录项目

| 项目 | 类型 | 报告 |
| --- | --- | --- |
| OpenViking | AI Browser / Trace Data | [HTML](site/projects/OpenViking/) · [Markdown](site/projects/OpenViking/analysis.md) |
| andrej-karpathy-skills | Agent Skill / Rules | [HTML](site/projects/andrej-karpathy-skills/) · [Markdown](site/projects/andrej-karpathy-skills/analysis.md) |
| neat-freak | CLI / AI Cleanup | [HTML](site/projects/neat-freak/) · [Markdown](site/projects/neat-freak/analysis.md) |
| claude-context | Agentic Coding / MCP Code Search | [HTML](site/projects/claude-context/) · [Markdown](site/projects/claude-context/analysis.md) |
| free-claude-code | API / Proxy | [HTML](site/projects/free-claude-code/) · [Markdown](site/projects/free-claude-code/analysis.md) |
| FinceptTerminal | Desktop / FinTech | [HTML](site/projects/FinceptTerminal/) · [Markdown](site/projects/FinceptTerminal/analysis.md) |
| GBrain | Knowledge Tool / MCP | [HTML](site/projects/gbrain/) · [Markdown](site/projects/gbrain/analysis.md) |

## 报告结构

每份报告通常包含：

- **新用户先看什么**：适合谁、解决什么问题、差异点、为什么现在值得看、最小验证方式。
- **Gold Example / Demo**：优先使用能直接解释核心工作流的真实示例；没有合适媒体时使用结构化场景卡片。
- **项目机制图**：按项目实际选择 UML、C4、CLD、SFD、BOT 或轻量流程图，不强行套模板。
- **架构视角**：只在有解释增益时使用，重点看核心交互和边界。
- **核心资产与价值**：说明真正支撑项目价值的代码、规则、数据或示例。
- **采用前确认**：列出试用、集成或生产采用前需要确认的风险。

## 阅读建议

先看总览页的“采用口径”和“差异点”，再打开具体 HTML 报告。需要审计证据、复用文字或比较版本时，再看对应的 Markdown。

维护和生成说明见 [docs/development.md](docs/development.md)。
