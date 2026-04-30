from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
PROJECTS_DIR = SITE_DIR / "projects"
REPORT_DIR = PROJECTS_DIR


PROJECTS = [
    {
        "slug": "free-claude-code",
        "title": "free-claude-code",
        "url": "https://github.com/Alishahryar1/free-claude-code",
        "adoption_label": "适合本地试点",
        "adoption_detail": "适合在本机或内网低风险仓库验证；公网共享前必须补鉴权、日志脱敏和 provider 兼容边界。",
        "summary": [
            "把 **Claude Code 的 Anthropic API 请求** 转接到 NVIDIA NIM、OpenRouter、DeepSeek、LM Studio、llama.cpp、Ollama 等 provider。",
            "它的价值不是“免费”，而是让 **Claude Code 工作流** 和 **模型供应商** 解耦。",
        ],
        "lean": {
            "适合谁": [
                "已经在用 Claude Code，但想比较本地模型或多 provider 的个人开发者。",
                "需要在低风险仓库中验证替代 provider 成本、可用性和工具调用效果的小团队。",
            ],
            "解决什么问题": [
                "Claude Code 的默认 provider 可能受成本、配额、区域访问和可用性影响。",
                "直接换客户端会破坏工作流；该项目保持 Claude Code 入口不变，只替换后端模型路径。",
            ],
            "和别的方案哪里不同": [
                "核心不是普通 API wrapper，而是 **Anthropic Messages / SSE / tool use 兼容层**。",
                "它需要持续处理 Claude Code 行为、provider schema 和流式响应差异。",
            ],
            "为什么现在值得看": [
                "本地模型和 OpenAI-compatible provider 增多，Claude Code 用户自然会需要可切换后端。",
                "项目已沉淀 provider registry、fast-path 处理和测试资产，不只是一次性配置脚本。",
            ],
            "最小验证方式": [
                "本机启动代理，设置 `ANTHROPIC_BASE_URL` 指向本地服务。",
                "选一个低风险仓库，验证长任务、工具调用、SSE 流式输出和错误恢复。",
            ],
        },
        "facts": [
            ("14.6k", "GitHub stars；另有 2.0k+ forks，2026-04-27 采样。"),
            ("6 provider 家族", "NIM、OpenRouter、DeepSeek、LM Studio、llama.cpp、Ollama。"),
            ("API Proxy", "FastAPI + Anthropic-style SSE；Claude Code 客户端基本不变。"),
        ],
        "tags": [("本地试点", "green"), ("协议适配", "blue"), ("公网需鉴权", "red")],
        "media": {
            "kind": "image",
            "source": "site/projects/free-claude-code/assets/free-claude-code-demo.png",
            "asset": "free-claude-code-demo.png",
            "caption": "README 中的运行示例图。它说明项目面向 Claude Code 使用链路，而不是展示模型能力本身。",
        },
        "demo": {
            "title": "把 Claude Code 指向本地代理",
            "source_label": "仓库 README 示例图 + 静态推演",
            "points": [
                "启动本地代理服务，例如 `localhost:8082`。",
                "把 `ANTHROPIC_BASE_URL` 指向本地代理。",
                "用 `MODEL_*` 把 Claude 模型名映射到 provider/model。",
                "Claude Code 继续按 Anthropic API 说话，代理负责转发、转换和兜底。",
            ],
        },
        "diagrams": {
            "selected_types": ["UML Sequence", "UML Component", "CLD"],
            "mixed": True,
            "reason": "该项目的关键不是 UI，而是一次 Claude Code 请求如何穿过兼容代理，以及兼容覆盖如何带来更多试点反馈。",
            "scenario": "用户在 Claude Code 中发起一次需要工具调用的 coding 任务。",
            "sequence": [
                ("Claude Code", "Local Proxy", "/v1/messages + tools + stream", "客户端入口保持不变"),
                ("Local Proxy", "ModelRouter", "读取 MODEL_* 映射", "决定目标 provider/model"),
                ("ModelRouter", "Provider Adapter", "构造 provider 请求", "处理 schema、tools、thinking"),
                ("Provider Adapter", "外部/本地模型", "发送兼容请求", "获得 token/工具调用片段"),
                ("Provider Adapter", "Claude Code", "Anthropic-style SSE 返回", "客户端继续按原工作流执行"),
            ],
            "components": [
                ("FastAPI Routes", "接住 Anthropic API 形态请求。"),
                ("ModelRouter", "把 Claude 模型名映射到 provider/model。"),
                ("Provider Registry", "管理 provider catalog、凭据、base URL 和 factory。"),
                ("Anthropic Core", "转换 messages、tools、thinking、SSE 和错误形态。"),
            ],
            "system": [
                {
                    "kind": "R",
                    "title": "兼容性增强回路",
                    "items": ["provider 覆盖增加", "试点成功率提高", "用户信任上升", "更多仓库试用", "暴露更多兼容问题并修复"],
                },
                {
                    "kind": "B",
                    "title": "安全控制回路",
                    "items": ["共享部署扩大", "鉴权/日志风险上升", "补安全边界", "试点范围回到可控状态"],
                },
            ],
        },
        "architecture": {
            "label": "自适应架构视角",
            "complexity": "中等",
            "framework": "C4 模型",
            "tailoring": "这是单入口 API proxy / provider adapter 项目，核心风险在请求转换和 provider 兼容，不需要完整 4+1。保留 C4 L1/L2 和一个核心 Dynamic 交互图。",
            "omitted": "省略独立 Physical View；部署边界只保留为本地/内网/公网安全约束。",
            "views": [
                {
                    "title": "系统全貌",
                    "view_type": "C4 L1 Context",
                    "visual_kind": "proxy_context",
                    "description": "系统边界是 Claude Code 与模型 provider 之间的本地/自托管兼容代理。",
                    "mermaid": """flowchart LR
    Dev[Developer] --> Claude[Claude Code]
    Claude --> Proxy[free-claude-code Local Proxy]
    Proxy --> Config[MODEL_* / Provider Config]
    Proxy --> Providers[External or Local Model Providers]
    Providers --> Proxy
    Proxy --> Claude""",
                },
                {
                    "title": "核心业务流转",
                    "view_type": "C4 Dynamic / UML Sequence",
                    "priority": True,
                    "scenario": "Claude Code 发起一次包含 tools 和 stream 的 coding 请求。",
                    "description": "重点不是静态模块名，而是 Anthropic 请求如何经过路由、适配和 SSE 回传。",
                    "mermaid": """sequenceDiagram
    autonumber
    participant C as Claude Code
    participant P as Local Proxy
    participant R as ModelRouter
    participant A as Provider Adapter
    participant M as External or Local Model
    C->>P: /v1/messages + tools + stream
    P->>R: read MODEL_* mapping
    R->>A: build provider request
    A->>M: compatible provider call
    M-->>A: tokens / tool-call fragments
    A-->>C: Anthropic-style SSE""",
                },
                {
                    "title": "静态组织结构",
                    "view_type": "C4 L2 Container",
                    "visual_kind": "proxy_static",
                    "description": "静态结构只展示真正影响扩 provider 和维护兼容层的容器/模块边界。",
                    "mermaid": """flowchart LR
    Routes[FastAPI Routes] --> Router[ModelRouter]
    Router --> Registry[Provider Registry]
    Registry --> Adapter[Provider Adapters]
    Adapter --> Anthropic[Anthropic Core Conversion]
    Anthropic --> SSE[SSE Response]
    Tests[Smoke and Provider Tests] -.guard.-> Anthropic""",
                },
            ],
        },
        "key_assets": [
            ("Provider Registry", "provider catalog、凭据检查、base URL、factory 和 cache 的统一生命周期。"),
            ("Anthropic Core", "SSE、conversion、thinking、tools、tokens 处理，是兼容 Claude Code 的核心。"),
            ("Fast-path 识别", "quota、title、prefix、suggestion、filepath 小请求可本地响应，降低延迟和消耗。"),
            ("测试资产", "provider、API、SSE、CLI 和 smoke 测试让兼容层更可维护。"),
        ],
        "adoption": [
            "先在单机或内网试点，不要直接开放公网。",
            "重点验证工具调用质量、长上下文稳定性和 provider 错误恢复。",
            "团队共享前补全鉴权、日志脱敏、web_fetch 限制和 provider 兼容矩阵。",
        ],
        "deepwiki": ["未检索到稳定 DeepWiki 首页；本轮以 README、源码结构和本地报告为主。"],
        "evidence": [
            "README 引用本地 `pic.png` 示例图。",
            "`api/routes.py`、`api/services.py`、`providers/registry.py`、`core/anthropic/` 支撑兼容代理判断。",
            "未真实启动服务、未调用 provider、未运行 Claude Code。",
        ],
    },
    {
        "slug": "FinceptTerminal",
        "title": "FinceptTerminal",
        "url": "https://github.com/Fincept-Corporation/FinceptTerminal",
        "adoption_label": "适合学习研究；机构采用前需审计",
        "adoption_detail": "适合先用产品图对应的研究场景理解价值；机构接入前必须审许可证、构建复现、数据源授权和交易安全。",
        "summary": [
            "一个 C++20 / Qt6 原生金融终端，试图把 **行情、研究、组合、新闻、Python 金融分析、AI agents 和 DataHub** 放进桌面工作台。",
            "它更像开源金融工作站，而不是单一金融库。",
        ],
        "lean": {
            "适合谁": [
                "个人投资者、金融工程学习者、开源量化开发者。",
                "想低成本探索行情、研究、组合与 Python 分析整合的小团队。",
                "希望理解金融终端架构、DataHub 数据分发和桌面工作台组织方式的技术人员。",
            ],
            "解决什么问题": [
                "Bloomberg/Eikon 昂贵；开源金融工具往往散落在行情、分析、新闻、交易等不同工具里。",
                "用户真正需要的是一个能串起研究流程的工作台，而不只是 API 列表。",
            ],
            "和别的方案哪里不同": [
                "核心差异是 **Qt 原生桌面 UI + DataHub topic contract + Python 金融脚本生态** 的组合。",
                "如果 DataHub 治理得住复杂数据源，它有机会从功能集合变成可扩展终端平台。",
            ],
            "为什么现在值得看": [
                "开源金融数据、Python 分析和本地 AI agent 都在成熟，桌面集成工作台有现实试用价值。",
                "仓库已有多张产品截图、DataHub 架构文档和大量 C++/Python 资产，足以做场景级静态评估。",
            ],
            "最小验证方式": [
                "先围绕 Equity Research 页面验证一个标的研究路径，例如 AAPL。",
                "确认 installer/构建、行情数据、Python analytics、DataHub topic 更新和缓存行为。",
                "真实账户、交易、机构数据源必须延后到许可证和安全审计之后。",
            ],
        },
        "facts": [
            ("15.8k", "GitHub stars；2.1k+ forks，2026-04-27 采样。"),
            ("DataHub", "in-process pub/sub topic contract 是核心治理资产。"),
            ("2,566+", "约 1,143 个 C++ 源/头文件与 1,423 个 Python 脚本。"),
        ],
        "tags": [("金融工作台", "green"), ("原生桌面", "blue"), ("采用需审计", "red")],
        "media": {
            "kind": "image",
            "source": "site/projects/FinceptTerminal/assets/fincept-equity-research.png",
            "asset": "fincept-equity-research.png",
            "caption": "README 展示的 Equity Research 页面。它最能说明用户入口：从标的研究串起行情、新闻、财务和组合上下文。",
        },
        "demo": {
            "title": "AAPL 研究工作流",
            "source_label": "仓库 README 产品图 + 静态推演",
            "points": [
                "打开 Equity Research 或 Markets 页面，输入 AAPL。",
                "Qt Screen 发出标的请求，DataHub 订阅 `market:quote:AAPL` 等 topic。",
                "Producer 拉取行情、新闻或财务数据，缓存后发布给页面。",
                "研究员在同一工作台查看行情、新闻、财务、组合影响。",
            ],
        },
        "diagrams": {
            "selected_types": ["UML Component", "UML Sequence", "SFD"],
            "mixed": True,
            "reason": "这是桌面金融工作台，核心要解释 UI、DataHub、Producer、缓存和研究视图如何协作；数据/研究上下文积累更适合用 SFD 表达。",
            "scenario": "研究员在 Equity Research 中查看 AAPL，并希望把行情、新闻、财务和组合影响放到同一上下文。",
            "sequence": [
                ("研究员", "Qt Screen", "选择 AAPL / 打开研究页", "形成研究任务"),
                ("Qt Screen", "DataHub Topic", "订阅 quote/news/financials", "页面不直接管理所有数据源"),
                ("DataHub Topic", "Producer/Data Source", "请求行情、新闻、财务数据", "多来源数据进入统一 topic"),
                ("Producer/Data Source", "Cache/State", "写入缓存和状态", "减少重复请求并保留上下文"),
                ("Cache/State", "研究视图", "发布更新", "图表、表格、新闻和组合影响同步刷新"),
            ],
            "components": [
                ("Qt Screens", "承载用户交互和金融场景页面。"),
                ("DataHub", "用 topic 统一 quote、news、economics、broker 等状态。"),
                ("Producers", "HTTP、WebSocket、Broker、PythonRunner 等生产数据。"),
                ("Cache / SQLite", "承接历史数据、状态和本地上下文。"),
                ("Python Scripts", "提供分析、数据获取、agent 和量化能力。"),
            ],
            "system": [
                {
                    "kind": "SFD",
                    "title": "研究上下文存量",
                    "items": ["行情/新闻/财务流入", "DataHub topic 聚合", "缓存与本地状态增加", "研究页可复用上下文变多"],
                },
                {
                    "kind": "B",
                    "title": "机构采用控制回路",
                    "items": ["功能覆盖扩大", "许可证/数据源/交易风险上升", "审计和权限边界补齐", "可采用范围恢复可控"],
                },
            ],
        },
        "architecture": {
            "label": "自适应架构视角",
            "complexity": "复杂 / 异构",
            "framework": "4+1 视图模型 + C4/UML 标注",
            "tailoring": "该项目横跨 Qt 桌面 UI、DataHub、Producer、缓存、Python runtime、外部数据源和潜在 broker。保留场景视图、过程视图、开发/实现视图和部署视图；不再输出五张孤立文字卡。",
            "omitted": "省略单独 Logical 文字卡；逻辑对象已经合并进 C4 L1/L2 和核心过程图，避免重复解释。",
            "views": [
                {
                    "title": "系统全貌",
                    "view_type": "场景视图(+1) / C4 L1 Context",
                    "visual_kind": "fincept_context",
                    "description": "以 AAPL Equity Research 作为 Scenario，先界定研究员、桌面终端和外部数据源的系统边界。",
                    "mermaid": """flowchart LR
    Researcher[Researcher] --> Qt[FinceptTerminal Qt Desktop]
    Qt --> DataHub[DataHub Topic Bus]
    DataHub --> Producers[Market News Financial Producers]
    Producers --> Sources[External Data Sources]
    DataHub --> Python[Python Analytics Runtime]
    DataHub --> Cache[Local Cache and State]
    Qt --> Views[Research Views]""",
                },
                {
                    "title": "核心业务流转",
                    "view_type": "Process View / UML Sequence",
                    "priority": True,
                    "scenario": "研究员在 Equity Research 中查看 AAPL，并希望把行情、新闻、财务和组合影响放到同一上下文。",
                    "description": "这是必须优先理解的交互图：Screen 不直接管理所有来源，而是通过 DataHub topic 组织数据流和状态刷新。",
                    "mermaid": """sequenceDiagram
    autonumber
    actor U as Researcher
    participant S as Qt Screen
    participant H as DataHub Topic
    participant P as Producer / Data Source
    participant C as Cache / State
    participant V as Research View
    U->>S: Open Equity Research and choose AAPL
    S->>H: subscribe quote/news/financials topics
    H->>P: request market, news, financial data
    P->>C: write fetched data and status
    C-->>H: publish state update
    H-->>V: refresh charts, tables, news and portfolio impact""",
                },
                {
                    "title": "静态组织结构",
                    "view_type": "Development / Implementation View with C4 L2/L3",
                    "visual_kind": "fincept_static",
                    "description": "静态组织结构只展示开发边界：UI 场景、应用装配、DataHub、Producer、缓存和 Python 脚本生态。",
                    "mermaid": """flowchart TB
    subgraph Desktop[Qt Desktop Application]
      Screens[src/screens UI Scenes]
      App[src/app main startup]
      Services[Services and Producers]
      DataHub[DataHub Topic Contract]
      Cache[SQLite / Local Cache]
    end
    Scripts[fincept-qt/scripts Python Analytics]
    Screens --> DataHub
    App --> Services
    Services --> DataHub
    DataHub --> Cache
    DataHub --> Scripts""",
                },
                {
                    "title": "物理 / 部署视图",
                    "view_type": "C4 Deployment",
                    "visual_kind": "fincept_deployment",
                    "description": "机构采用前真正要确认的是运行节点、外部依赖、数据授权和真实账户边界，而不是把 README 截图当作可部署证明。",
                    "mermaid": """flowchart TB
    subgraph Workstation[User Workstation]
      App[FinceptTerminal Qt App]
      LocalStore[Local Cache / Profile]
      Py[Python Runtime]
    end
    App --> LocalStore
    App --> Py
    App --> Market[Market Data APIs]
    App --> News[News / Financial APIs]
    App -.optional.-> Broker[Broker Connection]
    Broker --> Account[Real Account Boundary]""",
                },
            ],
        },
        "key_assets": [
            ("DataHub topic contract", "把 markets、news、economics、broker、agents 的数据状态统一到可订阅层。"),
            ("原生终端框架", "`src/app/main.cpp` 初始化 profile、crash、metatypes、DataHub producers 和服务。"),
            ("Python 金融脚本", "`fincept-qt/scripts/` 覆盖分析、agents、数据获取和量化模块。"),
            ("桌面 UI 资产", "`src/screens/` 下的金融场景页面形成 Bloomberg-like 工作台体验。"),
        ],
        "adoption": [
            "学习和研究用途可先试用产品图对应的核心场景。",
            "机构采用前必须确认 AGPL/商业许可、构建复现、数据源授权和交易安全。",
            "不要先接真实账户；先验证 installer、market data、Python analytics 和 DataHub 行为。",
        ],
        "deepwiki": [
            "DeepWiki 将其拆到 data connectors 等专题，说明复杂度主要集中在数据源与终端集成。",
            "本轮 DeepWiki 只作辅助理解；关键判断仍以 README、架构文档、DataHub 文档和源码入口为准。",
        ],
        "evidence": [
            "README 本地图片包含 EquityResearch、Portfolio、News、NodeEditor 等产品截图。",
            "`docs/ARCHITECTURE.md` 与 `fincept-qt/DATAHUB_ARCHITECTURE.md` 支撑 Screen/Service/DataHub 判断。",
            "未构建 Qt、未运行 installer、未连接真实数据源或 broker。",
        ],
    },
    {
        "slug": "andrej-karpathy-skills",
        "title": "andrej-karpathy-skills",
        "url": "https://github.com/forrestchang/andrej-karpathy-skills",
        "adoption_label": "适合作为 Agent 行为基线；仍需 eval 验证",
        "adoption_detail": "适合先作为团队 agent 指令基线；要证明长期价值，需要用真实 PR 或任务集评估返工率和无关 diff 是否下降。",
        "summary": [
            "极轻量 coding agent 行为规则包，把 Karpathy 对 LLM 编码失败模式的观察压缩成 **CLAUDE.md、Claude plugin skill 和 Cursor rule**。",
            "它不是开发框架，而是减少 agent 误判、过度设计和无关改动的行为约束。",
        ],
        "lean": {
            "适合谁": [
                "Claude Code / Cursor 用户。",
                "维护团队级 agent 指令、想减少返工和无关 diff 的工程团队。",
                "正在整理 AI coding 规范、但不想维护长篇流程文档的团队。",
            ],
            "解决什么问题": [
                "Coding agent 容易隐藏假设、过度抽象、顺手改无关代码、没有明确验收目标。",
                "团队需要短、硬、可复制的行为规则，而不是长篇抽象建议。",
            ],
            "和别的方案哪里不同": [
                "四条原则足够短：**先澄清、简单优先、外科式修改、目标驱动执行**。",
                "同一规则被分发为 CLAUDE.md、Skill、Cursor rule 和 plugin manifest，降低采用成本。",
            ],
            "为什么现在值得看": [
                "Agent coding 已经成为日常开发入口，团队开始需要稳定行为基线。",
                "项目传播势能强，说明这类“短规则 + 多分发格式”的需求真实存在。",
            ],
            "最小验证方式": [
                "把规则加入一个真实 repo，选择 5-10 个历史小任务做前后对照。",
                "观察 agent 是否减少无关 diff、是否更早澄清目标、是否更少过度设计。",
            ],
        },
        "facts": [
            ("91.9k", "GitHub stars；8.8k+ forks，传播势能极强。"),
            ("4 principles", "Think Before Coding、Simplicity First、Surgical Changes、Goal-Driven Execution。"),
            ("3 formats", "CLAUDE.md、Skill、Cursor rule 三种主要分发形态。"),
        ],
        "tags": [("行为基线", "green"), ("低接入成本", "blue"), ("仍需 eval", "amber")],
        "media": {
            "kind": "example",
            "caption": "来自 `EXAMPLES.md` 的 “Make the search faster” 示例。它比抽象描述更能说明该项目如何改变 agent 行为。",
        },
        "demo": {
            "title": "Make the search faster",
            "source_label": "仓库 EXAMPLES.md 示例",
            "points": [
                "用户只说“让搜索更快”，但“快”可能指响应时间、吞吐量或感知速度。",
                "错误做法：agent 静默选择缓存、索引、异步等方案并开始大改。",
                "正确做法：先列出三种解释、成本和影响，再让用户确认目标。",
                "价值：减少错误方向、过度实现和返工。",
            ],
        },
        "diagrams": {
            "selected_types": ["行为流程", "BOT"],
            "reason": "这是规则/skill 项目，核心不是系统调用链，而是模糊需求如何被规则转成可验证行动；长期效果适合用概念 BOT 展示。",
            "scenario": "用户给 agent 一个模糊请求：Make the search faster。",
            "sequence": [
                ("用户", "Agent", "提出模糊目标", "Make the search faster"),
                ("Agent", "规则基线", "触发先澄清原则", "列出 latency / throughput / UX"),
                ("用户", "Agent", "确认优化目标", "锁定成功标准"),
                ("Agent", "代码修改", "执行最小路径修改", "避免顺手重构"),
                ("Agent", "验证", "运行测试或基准", "确认目标达成"),
            ],
            "components": [
                ("CLAUDE.md", "项目根目录规则入口。"),
                ("SKILL.md", "Claude plugin 兼容分发。"),
                ("Cursor Rule", "Cursor 项目级 alwaysApply 规则。"),
                ("EXAMPLES.md", "用 before/after 降低误用概率。"),
            ],
            "system": [
                {
                    "kind": "BOT",
                    "title": "概念趋势：返工率下降",
                    "items": ["澄清目标增加", "无关 diff 减少", "返工率预期下降", "需要真实 eval 验证"],
                }
            ],
        },
        "architecture": {
            "label": "自适应架构视角",
            "complexity": "简单",
            "framework": "C4 模型（轻量裁剪）",
            "tailoring": "这是文档/规则包，不是运行时系统。只保留 Context、核心规则交互和分发结构；不使用 4+1、部署图或物理视图。",
            "omitted": "省略 4+1、C4 Deployment 和系统动力部署视角；这些视角会把规则包讲成不存在的运行系统。",
            "views": [
                {
                    "title": "系统全貌",
                    "view_type": "C4 L1 Context",
                    "visual_kind": "skill_context",
                    "description": "系统边界是开发者、coding agent 和规则包之间的行为约束关系。",
                    "mermaid": """flowchart LR
    Developer[Developer] --> Agent[Coding Agent]
    Rules[andrej-karpathy-skills Rule Pack] --> Agent
    Agent --> Repo[Target Repository]
    Examples[EXAMPLES.md] --> Developer""",
                },
                {
                    "title": "核心业务流转",
                    "view_type": "C4 Dynamic / Behavior Sequence",
                    "priority": True,
                    "scenario": "用户提出 Make the search faster 这类模糊请求。",
                    "description": "规则包的价值体现在 agent 如何先暴露假设、确认目标，再最小修改并验证结果。",
                    "mermaid": """sequenceDiagram
    autonumber
    actor U as User
    participant A as Agent
    participant R as Rule Pack
    participant C as Codebase
    participant V as Validation
    U->>A: Make the search faster
    A->>R: apply clarify-first rule
    R-->>A: expose latency / throughput / UX assumptions
    A-->>U: ask for target and success criteria
    U-->>A: confirm objective
    A->>C: make smallest relevant change
    A->>V: run test or benchmark""",
                },
                {
                    "title": "静态组织结构",
                    "view_type": "C4 L2 Container（分发结构）",
                    "visual_kind": "skill_distribution",
                    "description": "静态结构是多分发格式，而不是服务容器。",
                    "mermaid": """flowchart LR
    Core[Four Principles] --> Claude[CLAUDE.md]
    Core --> Skill[Claude Skill SKILL.md]
    Core --> Cursor[Cursor Rule]
    Core --> Examples[EXAMPLES.md]
    Examples -.calibrate.-> Core""",
                },
            ],
        },
        "key_assets": [
            ("CLAUDE.md", "适合直接复制到项目根的核心单文件指令。"),
            ("SKILL.md", "Claude plugin 兼容版本，便于作为 skill 分发。"),
            ("Cursor Rule", "`alwaysApply: true`，适合 Cursor 项目级规则。"),
            ("EXAMPLES.md", "用真实反例和正确行为解释四原则，降低误用概率。"),
        ],
        "adoption": [
            "适合作为团队 agent 行为基线，但不要替代项目自己的工程规则。",
            "简单小改可以快速执行；复杂任务启用澄清、目标定义和验证闭环。",
            "建议补 eval 或 PR 对照，用真实 diff 噪声下降来验证价值。",
        ],
        "deepwiki": [
            "DeepWiki 将项目解释为解决 silent assumptions、over-abstraction、collateral damage 的四原则系统。",
            "DeepWiki 还强调双路径集成：全局 plugin 与项目级 CLAUDE.md；这与本地 README/EXAMPLES.md 一致。",
        ],
        "evidence": [
            "`README.md` 描述四原则与安装方式。",
            "`EXAMPLES.md` 提供 “Make the search faster” 等 before/after 案例。",
            "DeepWiki 页面补充了问题分类、原则映射和分发模型；未真实运行目标项目，也未做真实 AB eval。",
        ],
    },
    {
        "slug": "neat-freak",
        "title": "neat-freak（洁癖）",
        "url": "https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak",
        "adoption_label": "适合作为会话收尾基线；团队推广前需试运行",
        "adoption_detail": "适合已经依赖 coding agent 的个人或小团队，把文档、AGENTS/CLAUDE 和记忆同步变成固定收尾动作；团队强制前需要确认路径、删除策略和人工复核边界。",
        "analysis_mode": "静态分析，DeepWiki/Zread 仅作为派生资源链接，未作为证据来源",
        "summary": [
            "一个端到端的 **知识卫生 skill**：在开发会话结束时盘点项目文档、根级 AI 指令和 agent 记忆，修正过期信息并输出变更摘要。",
            "它的价值不是自动写更多文档，而是用强制盘点、影响矩阵和自检清单减少 stale docs / stale memory 对下一次 agent 协作的污染。",
        ],
        "lean": {
            "适合谁": [
                "已经把 Claude Code、Codex、OpenCode 或 OpenClaw 用在真实仓库里的个人开发者。",
                "经常遇到 README、docs、AGENTS.md / CLAUDE.md 和 agent 记忆互相矛盾的小团队。",
                "需要把阶段性交付变成可交接上下文，而不想每次手工梳理知识库的人。",
            ],
            "解决什么问题": [
                "AI 协作中的文档和记忆会慢慢腐化：代码已改，README 还是旧版，agent 下次会基于错误前提继续工作。",
                "普通收尾总结只会追加记录；neat-freak 把旧信息合并、修正、删除，并要求按受众同步到不同知识层。",
            ],
            "和别的方案哪里不同": [
                "它明确区分三层受众：**agent 记忆**、项目根 `CLAUDE.md / AGENTS.md`、面向人的 `docs/ / README`。",
                "它不是只更新 memory 的工具，而是先机械式枚举文件，再用 `sync-matrix.md` 判断每类代码变化要波及哪些文档。",
            ],
            "为什么现在值得看": [
                "AI coding 已经进入多轮、多 agent、跨会话协作阶段，错误上下文会直接放大返工和误改风险。",
                "项目用 3 个文件把触发词、执行流程、跨平台路径和变更影响矩阵压成可安装 skill，试用成本低。",
            ],
            "最小验证方式": [
                "选一个低风险仓库，完成一次真实小任务后运行 `/neat` 或 `整理一下`。",
                "重点观察它是否发现 README/docs/AGENTS/记忆里的过期内容，以及是否只改应该改的知识层。",
                "第一次试运行后人工 review diff，再决定是否把它加入团队收尾流程。",
            ],
        },
        "facts": [
            ("3 files", "`SKILL.md` + `agent-paths.md` + `sync-matrix.md`，无运行时代码。"),
            ("277 lines", "目标目录核心文本总行数；更像规则包而不是应用。"),
            ("7.3k", "GitHub repo stars；1.1k forks，2026-04-30 采样。"),
        ],
        "tags": [("知识清理", "green"), ("跨平台 Skill", "blue"), ("需人工复核", "amber")],
        "media": {
            "kind": "example",
            "caption": "示例来自 `neat-freak/SKILL.md` 的触发词和执行流程；本轮未安装或实际运行该 skill。",
            "rows": [
                {
                    "label": "触发",
                    "body": "`/neat`、`整理一下`、`同步一下`、`sync up` 等会话收尾短语。",
                    "tone": "",
                },
                {
                    "label": "核心动作",
                    "body": "先枚举 agent 记忆、根级 markdown、README/docs，再判断每个文件该改还是不改。",
                    "tone": "good",
                },
                {
                    "label": "采用风险",
                    "body": "它会真实编辑和清理知识文件；首次接入必须 review diff 和删除策略。",
                    "tone": "bad",
                },
            ],
        },
        "demo": {
            "title": "一次开发会话结束后的知识同步",
            "source_label": "仓库 SKILL.md 流程 + 静态推演",
            "points": [
                "开发任务完成后，用户输入 `/neat` 或自然语言“整理一下”。",
                "Agent 按 skill 要求列出 memory、项目根 markdown、README 和 docs，并标记评估过/要改/不用改。",
                "Agent 用变更影响矩阵判断本次代码或流程变化该同步到哪些知识层。",
                "Agent 真实修改 docs、AGENTS/CLAUDE 或记忆文件，删除过期项，最后输出变更摘要。",
            ],
        },
        "diagrams": {
            "selected_types": ["行为流程", "UML Component", "BOT"],
            "mixed": True,
            "reason": "这是文档/skill/rule-pack 项目，关键不是服务调用链，而是一次会话收尾如何从触发词走到文件盘点、影响矩阵、实际编辑和自检；长期价值只适合用概念 BOT 表达。",
            "scenario": "用户完成一个开发阶段后，希望把代码变化同步到文档、根级 AI 指令和 agent 记忆。",
            "sequence": [
                ("用户", "Agent", "输入 `/neat` 或“整理一下”", "触发会话收尾同步"),
                ("Agent", "盘点清单", "枚举 memory / 根 markdown / docs", "先 ls 再判断"),
                ("盘点清单", "影响矩阵", "映射本次变更类型", "决定波及哪些知识层"),
                ("影响矩阵", "知识文件", "编辑 docs / AGENTS / memory", "合并、修正、删除过期信息"),
                ("知识文件", "变更摘要", "输出已改和未处理项", "给用户可审查结果"),
            ],
            "components": [
                ("规则入口 SKILL.md", "触发词、角色定位、执行流程和自检清单。"),
                ("agent-paths.md", "Claude Code、Codex、OpenCode、OpenClaw 的记忆/配置路径。"),
                ("sync-matrix.md", "把代码层变化映射到 docs、root markdown 和 memory。"),
                ("文件盘点流程", "强制枚举 README、docs、CLAUDE/AGENTS 和散落 markdown。"),
                ("实际编辑要求", "要求真的修改、创建或删除知识文件，而不只是描述计划。"),
                ("收尾摘要", "按记忆变更、文档变更和未处理项回报。"),
            ],
            "system": [
                {
                    "kind": "BOT",
                    "title": "概念趋势：过期上下文下降",
                    "items": ["收尾同步频率增加", "过期文档/记忆减少", "新会话误判风险下降", "需要真实任务验证"],
                },
                {
                    "kind": "B",
                    "title": "编辑风险控制回路",
                    "items": ["可编辑知识层扩大", "误删/误同步风险上升", "人工 review 和路径约束", "团队试点范围回到可控"],
                },
            ],
        },
        "architecture": {
            "label": "自适应架构视角",
            "complexity": "简单",
            "framework": "C4-light + 行为序列",
            "tailoring": "这是 agent skill 和规则包，不是运行时系统。保留 Context、核心行为序列和静态组织/分发视图；用图解释职责边界和知识层，不画不存在的服务部署。",
            "omitted": "省略 4+1、Deployment/Physical View、数据库和 API 视图；目标目录没有运行时代码、测试入口或部署单元。",
            "views": [
                {
                    "title": "系统全貌",
                    "view_type": "C4-light Context",
                    "visual_kind": "neat_context",
                    "description": "系统边界是开发者、coding agent、neat-freak skill 和被同步的三类知识文件。",
                    "mermaid": """flowchart LR
    Developer[Developer] --> Agent[Coding Agent]
    Skill[neat-freak Skill] --> Agent
    Agent --> Root[CLAUDE.md / AGENTS.md]
    Agent --> Docs[README / docs]
    Agent --> Memory[Agent memory]
    Agent --> Summary[Change Summary]""",
                },
                {
                    "title": "核心业务流转",
                    "view_type": "C4 Dynamic / Behavior Sequence",
                    "priority": True,
                    "scenario": "开发任务结束后，用户运行 `/neat`。",
                    "description": "重点是 skill 如何把一个收尾触发转成文件盘点、影响分析、真实编辑和可审查摘要。",
                    "mermaid": """sequenceDiagram
    autonumber
    actor U as User
    participant A as Agent
    participant S as neat-freak Skill
    participant I as Inventory
    participant M as Sync Matrix
    participant F as Knowledge Files
    U->>A: /neat or tidy up docs
    A->>S: load triggers and workflow
    S->>I: enumerate memory, root markdown, docs
    I->>M: classify changed knowledge impact
    M->>F: update docs / root AI files / memory
    F-->>A: diff and unresolved items
    A-->>U: change summary""",
                },
                {
                    "title": "静态组织结构",
                    "view_type": "C4 L2 Container（规则分发结构）",
                    "visual_kind": "neat_distribution",
                    "description": "静态结构展示 `SKILL.md` 如何依赖两份 reference 文件，把触发、盘点、影响矩阵和平台路径连接起来。",
                    "mermaid": """flowchart LR
    Skill[neat-freak/SKILL.md] --> Triggers[Trigger phrases]
    Skill --> Workflow[Inventory and edit workflow]
    Skill --> Checklist[Self-check checklist]
    Skill --> Paths[references/agent-paths.md]
    Skill --> Matrix[references/sync-matrix.md]
    Paths --> Platforms[Claude Code / Codex / OpenCode / OpenClaw]
    Matrix --> Docs[Docs / root AI files / memory]""",
                },
            ],
        },
        "key_assets": [
            ("neat-freak/SKILL.md", "核心资产：触发词、角色定位、强制盘点、实际编辑和最终摘要格式都在这里。"),
            ("references/agent-paths.md", "跨平台路径速查，尤其明确 Codex 没有独立记忆索引，项目事实应进入 AGENTS.md。"),
            ("references/sync-matrix.md", "把 API、环境变量、数据库、用户流程等变化映射到应同步的文档层。"),
            ("README 集成说明", "仓库根 README 给出安装入口、触发方式、三层知识边界和 ClawHub/Tessl 分发信号。"),
        ],
        "adoption": [
            "先在低风险仓库跑一次，并人工 review 所有 diff。",
            "团队使用前要明确哪些 memory / docs / root markdown 可以由 agent 自动编辑，哪些必须人工确认。",
            "不要把它当成架构审查或测试替代品；它解决的是知识同步，不保证代码正确。",
            "对跨项目仓库尤其要检查 sync-matrix 的下游文档同步规则，避免只更新上游说明。",
        ],
        "deepwiki": [
            "本轮未把 DeepWiki 或 Zread 作为事实依据；报告页面仅提供从 GitHub 仓库 URL 派生的外部阅读链接。",
            "事实判断来自 GitHub README、`neat-freak/SKILL.md`、两份 references、MIT license 和 GitHub API 元数据。",
        ],
        "evidence": [
            "`README.md` 说明 skills 遵循 Agent Skills 开放标准，支持 Claude Code、Codex、OpenCode、OpenClaw。",
            "`README.md` 的 neat-freak 小节描述三层同步对象：项目根 AI 指令、docs/README、agent 记忆。",
            "`neat-freak/SKILL.md` 要求先枚举再判断，并要求实际修改文件而不是只描述计划。",
            "`references/agent-paths.md` 记录不同平台的记忆与配置路径差异。",
            "`references/sync-matrix.md` 记录代码变化到文档层的映射和记忆清理规则。",
            "未安装、未触发 `/neat`，未验证它在真实仓库中的自动编辑质量。",
        ],
    },
]


STYLE = """
:root {
  --bg: #f3f0e8;
  --paper: #fffdf8;
  --sheet: #f8fafb;
  --ink: #151923;
  --muted: #65707d;
  --line: #d8ddd9;
  --line-strong: #bfc8c2;
  --teal: #0f766e;
  --blue: #315c8f;
  --amber: #a66f12;
  --red: #a13a32;
  --green: #147a47;
  --dark: #17202b;
  --soft-teal: #e8f4f2;
  --soft-blue: #edf3fb;
  --soft-amber: #fff5dd;
  --soft-red: #fff0ee;
  --radius: 8px;
  --shadow: 0 18px 60px rgba(21, 25, 35, .08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background:
    linear-gradient(90deg, rgba(21,25,35,.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(21,25,35,.03) 1px, transparent 1px),
    var(--bg);
  background-size: 32px 32px;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 16px;
  line-height: 1.58;
  text-rendering: optimizeLegibility;
  overflow-x: hidden;
}
a { color: #0b5c55; text-decoration: none; }
strong { color: #071018; font-weight: 850; }
code {
  padding: 1px 5px;
  border: 1px solid #d7dfdc;
  border-radius: 5px;
  background: #f4f7f6;
  color: #183d39;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: .92em;
}
.page { width: 100%; max-width: 1280px; margin: 0 auto; padding: 28px; }
.topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 14px;
  color: var(--muted);
  font-size: 13px;
}
.brand {
  color: var(--teal);
  font-weight: 900;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.22fr) minmax(330px, .78fr);
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--paper);
  box-shadow: var(--shadow);
  overflow: hidden;
}
.hero-main { min-width: 0; padding: 42px 46px 36px; }
.eyebrow {
  display: block;
  max-width: 100%;
  color: var(--muted);
  font-size: 13px;
  font-weight: 750;
  overflow-wrap: anywhere;
}
.title {
  margin: 14px 0 18px;
  font-size: clamp(36px, 5vw, 60px);
  line-height: 1.02;
  letter-spacing: 0;
  overflow-wrap: anywhere;
}
.summary, .bullets {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.summary { max-width: 78ch; font-size: 17px; }
.summary li, .bullets li {
  position: relative;
  padding-left: 18px;
  overflow-wrap: anywhere;
}
.summary li::before, .bullets li::before {
  content: "";
  position: absolute;
  left: 0;
  top: .72em;
  width: 5px;
  height: 5px;
  border-radius: 999px;
  background: var(--teal);
}
.bullets.compact { gap: 6px; font-size: 14px; }
.resource-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 20px;
}
.resource-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 36px;
  padding: 7px 11px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fff;
  color: #123d38;
  font-size: 13px;
  font-weight: 820;
}
.adoption {
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 26px;
  padding: 34px;
  color: #fff;
  background:
    linear-gradient(180deg, rgba(255,255,255,.08), transparent 42%),
    var(--dark);
}
.adoption-label {
  color: #b9c6d6;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .1em;
  text-transform: uppercase;
}
.adoption-title {
  margin-top: 10px;
  font-size: 28px;
  font-weight: 900;
  line-height: 1.16;
}
.adoption-detail { margin: 13px 0 0; color: #e2ebf3; font-size: 14px; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; }
.tag {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 3px 8px;
  border: 1px solid #aab6c4;
  border-radius: 5px;
  background: #f8fafb;
  color: #394557;
  font-size: 12px;
  font-weight: 850;
}
.tag.green { color: var(--green); border-color: #b8dfc9; background: #eef8f2; }
.tag.blue { color: #254466; border-color: #b9cde5; background: var(--soft-blue); }
.tag.amber { color: var(--amber); border-color: #e6cf9f; background: var(--soft-amber); }
.tag.red { color: var(--red); border-color: #e3b9b4; background: var(--soft-red); }
.adoption .tag { color: #e9f1fb; border-color: #3d4e61; background: #202c3a; }
.facts {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border: 1px solid var(--line-strong);
  border-top: 0;
  background: #fbfcfb;
}
.fact {
  min-width: 0;
  min-height: 102px;
  padding: 18px 22px;
  border-right: 1px solid var(--line);
}
.fact:last-child { border-right: 0; }
.fact b {
  display: block;
  margin-bottom: 7px;
  font-size: 28px;
  font-weight: 900;
  line-height: 1;
  overflow-wrap: anywhere;
}
.fact span { display: block; color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
.nav {
  position: sticky;
  top: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1px;
  margin: 18px 0 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--line);
  overflow: hidden;
}
.nav a {
  display: flex;
  min-height: 46px;
  align-items: center;
  justify-content: center;
  padding: 8px 10px;
  background: var(--paper);
  color: #26313e;
  font-size: 13px;
  font-weight: 800;
  text-align: center;
}
.section {
  display: block;
  margin-top: 28px;
  padding: 30px 0 0;
  border-top: 1px solid var(--line-strong);
}
.section-head {
  min-width: 0;
  display: block;
  margin-bottom: 18px;
}
.section-index {
  display: block;
  margin-bottom: 6px;
  color: var(--teal);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .09em;
  text-transform: uppercase;
}
.section h2 { margin: 0; font-size: 27px; line-height: 1.18; }
.section-note { margin: 8px 0 0; max-width: 860px; color: var(--muted); font-size: 14px; }
.section-body { min-width: 0; display: grid; gap: 18px; }
.lean-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 18px;
}
.kv, .asset, .check-card, .evidence-card {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  padding: 16px;
}
.kv h3, .asset h3, .check-card h3, .evidence-card h3 {
  margin: 0 0 10px;
  font-size: 16px;
  line-height: 1.25;
}
.kv p, .asset p { margin: 0; color: #364150; overflow-wrap: anywhere; }
.demo-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.12fr) minmax(320px, .88fr);
  gap: 18px;
  align-items: start;
}
.media-card {
  min-width: 0;
  margin: 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fbfcfd;
  overflow: hidden;
}
.media-card img {
  display: block;
  width: 100%;
  height: auto;
  max-height: 430px;
  object-fit: contain;
  background: #f7fafc;
}
.media-caption {
  padding: 12px 14px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 13px;
  overflow-wrap: anywhere;
}
.example-card {
  display: grid;
  gap: 10px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: #fbfcfd;
  padding: 14px;
}
.example-row {
  padding: 12px 14px;
  border-left: 4px solid var(--blue);
  background: #fff;
}
.example-row.bad { border-left-color: var(--red); background: var(--soft-red); }
.example-row.good { border-left-color: var(--teal); background: var(--soft-teal); }
.example-row b { display: block; margin-bottom: 4px; }
.example-row p { margin: 0; color: #35414f; }
.diagram-shell {
  min-width: 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--paper);
  box-shadow: 0 12px 34px rgba(21,25,35,.055);
  overflow: hidden;
}
.diagram-header {
  display: block;
  padding: 18px 20px 15px;
  border-bottom: 1px solid var(--line);
  background: #fbfcfb;
}
.type-row { display: flex; flex-wrap: wrap; gap: 8px; }
.type-chip {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 3px 8px;
  border: 1px solid #b9cde5;
  border-radius: 5px;
  background: var(--soft-blue);
  color: #254466;
  font-size: 12px;
  font-weight: 850;
}
.scenario {
  margin: 0 0 6px;
  color: #394656;
  font-size: 14px;
  overflow-wrap: anywhere;
}
.diagram-header .type-row { margin-top: 12px; }
.diagram-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 12px 20px;
  border-bottom: 1px solid var(--line);
  background: #fff;
}
.diagram-tabs button {
  min-height: 34px;
  border: 1px solid var(--line-strong);
  border-radius: 6px;
  background: #f8fafb;
  color: #2f3b48;
  padding: 5px 10px;
  font: inherit;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
}
.diagram-tabs button[aria-selected="true"] {
  color: #fff;
  border-color: var(--teal);
  background: var(--teal);
}
.diagram-panel { padding: 18px 20px 20px; }
.diagram-panel[hidden] { display: none; }
.svg-frame {
  width: 100%;
  overflow: auto;
  border: 1px solid #dce2df;
  border-radius: var(--radius);
  background:
    linear-gradient(90deg, rgba(21,25,35,.035) 1px, transparent 1px),
    linear-gradient(180deg, rgba(21,25,35,.035) 1px, transparent 1px),
    #fff;
  background-size: 28px 28px;
}
.svg-frame svg {
  display: block;
  width: 100%;
  height: auto;
  min-width: 960px;
}
.diagram-caption { margin: 10px 0 0; color: var(--muted); font-size: 13px; }
.diagram-mobile {
  display: none;
  gap: 10px;
}
.mobile-step, .mobile-loop {
  position: relative;
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  padding: 12px 13px 12px 42px;
}
.mobile-step::before {
  content: attr(data-step);
  position: absolute;
  left: 12px;
  top: 13px;
  display: flex;
  width: 22px;
  height: 22px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--dark);
  color: #fff;
  font-size: 11px;
  font-weight: 900;
}
.mobile-step b, .mobile-loop b { display: block; margin-bottom: 4px; line-height: 1.3; }
.mobile-step p, .mobile-step small, .mobile-loop p {
  display: block;
  margin: 0;
  color: var(--muted);
  overflow-wrap: anywhere;
}
.mobile-step p, .mobile-loop p { color: #35414f; }
.mermaid-block {
  margin: 0;
  padding: 14px;
  border: 1px solid #dce2df;
  border-radius: var(--radius);
  background: #f8fafb;
  color: #26313e;
  font-size: 12px;
  line-height: 1.48;
  overflow: auto;
  white-space: pre-wrap;
}
.asset-grid, .view-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.arch-lens {
  min-width: 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--paper);
  overflow: hidden;
  box-shadow: 0 12px 34px rgba(21,25,35,.045);
}
.arch-head {
  display: block;
  padding: 18px 20px;
  border-bottom: 1px solid var(--line);
  background: #fbfcfb;
}
.arch-kicker {
  display: block;
  margin-bottom: 6px;
  color: var(--teal);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.arch-head h3 { margin: 0; font-size: 20px; line-height: 1.25; }
.arch-reason {
  display: block;
  max-width: 100%;
  margin-top: 12px;
  border-left: 3px solid var(--teal);
  background: var(--soft-teal);
  padding: 12px 14px;
  color: #24433f;
  font-size: 13px;
}
.arch-decision {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid var(--line);
  background: #fffdf8;
}
.arch-kv {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: #fbfcfb;
  padding: 13px 14px;
}
.arch-kv b {
  display: block;
  margin-bottom: 4px;
  color: var(--teal);
  font-size: 12px;
  font-weight: 900;
}
.arch-kv span {
  display: block;
  color: #354252;
  font-size: 14px;
  overflow-wrap: anywhere;
}
.arch-views {
  display: grid;
  gap: 14px;
  padding: 20px;
  background:
    linear-gradient(90deg, rgba(21,25,35,.026) 1px, transparent 1px),
    linear-gradient(180deg, rgba(21,25,35,.022) 1px, transparent 1px),
    #fffdf8;
  background-size: 24px 24px;
}
.arch-view {
  min-width: 0;
  border: 1px solid #ccd7d2;
  border-radius: var(--radius);
  background: var(--paper);
  overflow: hidden;
}
.arch-view-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 12px;
  align-items: start;
  padding: 15px 16px;
  border-bottom: 1px solid var(--line);
  background: #fbfcfb;
}
.arch-view h4 {
  margin: 0 0 6px;
  font-size: 17px;
  line-height: 1.25;
}
.arch-view-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--muted);
  font-size: 13px;
}
.priority-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 3px 8px;
  border: 1px solid #e6cf9f;
  border-radius: 5px;
  background: var(--soft-amber);
  color: var(--amber);
  font-size: 12px;
  font-weight: 900;
}
.arch-view-body {
  display: grid;
  gap: 12px;
  padding: 14px 16px 16px;
}
.arch-view-body p {
  margin: 0;
  color: #354252;
}
.arch-source {
  border: 1px solid #dce2df;
  border-radius: var(--radius);
  background: #fbfcfb;
  overflow: hidden;
}
.arch-source summary {
  min-height: 38px;
  padding: 9px 12px;
  color: #26313e;
  cursor: pointer;
  font-size: 13px;
  font-weight: 850;
}
.arch-source .mermaid-block {
  border: 0;
  border-top: 1px solid #dce2df;
  border-radius: 0;
}
.two-col { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.footer {
  margin-top: 28px;
  padding: 18px 0 4px;
  border-top: 1px solid var(--line-strong);
  color: var(--muted);
  font-size: 13px;
}
@media (max-width: 980px) {
  .page { padding: 16px; }
  .hero, .demo-layout, .two-col { grid-template-columns: 1fr; }
  .nav { position: static; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .lean-grid, .asset-grid, .view-grid, .facts, .arch-decision { grid-template-columns: 1fr; }
  .fact { border-right: 0; border-bottom: 1px solid var(--line); }
  .fact:last-child { border-bottom: 0; }
  .media-card img { max-height: none; }
}
@media (max-width: 1180px) and (min-width: 561px) {
  .svg-frame svg { min-width: 0; }
}
@media (max-width: 560px) {
  body { font-size: 15px; }
  .page { padding: 12px; }
  .topline { align-items: flex-start; }
  .hero-main, .adoption { padding: 24px 20px; }
  .title {
    font-size: 32px;
    overflow-wrap: break-word;
  }
  .nav { grid-template-columns: 1fr; }
  .section h2 { font-size: 24px; }
  .diagram-tabs { padding: 10px 12px; }
  .diagram-panel { padding: 12px; }
  .svg-frame { display: none; }
  .diagram-mobile { display: grid; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
"""

INTERACTION_SCRIPT = """
document.querySelectorAll('.diagram-shell').forEach((shell) => {
  const buttons = Array.from(shell.querySelectorAll('[data-diagram-tab]'));
  const panels = Array.from(shell.querySelectorAll('[data-diagram-panel]'));
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const target = button.getAttribute('data-diagram-tab');
      buttons.forEach((item) => item.setAttribute('aria-selected', String(item === button)));
      panels.forEach((panel) => {
        panel.hidden = panel.getAttribute('data-diagram-panel') !== target;
      });
    });
  });
});
"""


def inline(text: str) -> str:
    placeholders: dict[str, str] = {}

    def hold(value: str) -> str:
        key = f"@@{len(placeholders)}@@"
        placeholders[key] = value
        return key

    raw = re.sub(r"\*\*(.+?)\*\*", lambda m: hold(f"<strong>{escape(m.group(1))}</strong>"), text)
    raw = re.sub(r"`([^`]+?)`", lambda m: hold(f"<code>{escape(m.group(1))}</code>"), raw)
    escaped = escape(raw)
    for key, value in placeholders.items():
        escaped = escaped.replace(escape(key), value)
    return escaped


def bullets(items: list[str], compact: bool = False) -> str:
    klass = "bullets compact" if compact else "bullets"
    return f'<ul class="{klass}">' + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>"


def tags(project: dict) -> str:
    return "".join(f'<span class="tag {klass}">{escape(label)}</span>' for label, klass in project["tags"])


def facts(project: dict) -> str:
    return "".join(f'<div class="fact"><b>{escape(k)}</b><span>{inline(v)}</span></div>' for k, v in project["facts"])


def github_repo_parts(url: object) -> tuple[str, str] | None:
    match = re.match(r"^https://(?:www\.)?github\.com/([^/\s]+)/([^/\s?#]+)(?:[/?#].*)?$", str(url or "").strip())
    if not match:
        return None
    owner = match.group(1)
    repo = match.group(2).removesuffix(".git")
    if not owner or not repo:
        return None
    return owner, repo


def resource_links(project: dict) -> str:
    links = [("GitHub", project["url"])]
    repo = github_repo_parts(project.get("url"))
    if repo:
        owner, name = repo
        links.extend([
            ("DeepWiki", f"https://deepwiki.com/{owner}/{name}"),
            ("Zread", f"https://zread.ai/{owner}/{name}"),
        ])
    items = "".join(
        f'<a class="resource-link" href="{escape(url)}" target="_blank" rel="noreferrer" '
        f'aria-label="打开 {escape(project["title"])} {escape(label)} 页面">{escape(label)}</a>'
        for label, url in links
    )
    return f'<div class="resource-links" aria-label="外部资源">{items}</div>'


def lean_html(project: dict) -> str:
    return '<div class="lean-grid">' + "".join(
        f'<div class="kv"><h3>{escape(label)}</h3>{bullets(items)}</div>'
        for label, items in project["lean"].items()
    ) + "</div>"


def media_asset_path(project: dict) -> str | None:
    media = project["media"]
    return f"assets/{media['asset']}" if media.get("kind") == "image" else None


def media_html(project: dict) -> str:
    media = project["media"]
    if media.get("kind") == "image":
        return f"""
        <figure class="media-card">
          <img src="{escape(media_asset_path(project) or '')}" alt="{escape(project['title'])} demo image">
          <figcaption class="media-caption">{inline(media['caption'])}</figcaption>
        </figure>
        """
    if media.get("rows"):
        rows = "".join(
            f'<div class="example-row {escape(row.get("tone", ""))}"><b>{inline(row["label"])}</b><p>{inline(row["body"])}</p></div>'
            for row in media["rows"]
        )
        return f"""
        <div class="example-card">
          {rows}
          <div class="media-caption">{inline(media['caption'])}</div>
        </div>
        """
    return f"""
    <div class="example-card">
      <div class="example-row"><b>User</b><p>“Make the search faster”</p></div>
      <div class="example-row bad"><b>错误做法</b><p>静默选择缓存、索引、异步处理，然后开始大范围修改。</p></div>
      <div class="example-row good"><b>正确做法</b><p>先澄清：响应时间、吞吐量、还是感知速度？再选最小修改路径。</p></div>
      <div class="media-caption">{inline(media['caption'])}</div>
    </div>
    """


def demo_html(project: dict) -> str:
    demo = project["demo"]
    return f"""
    <div class="demo-layout">
      {media_html(project)}
      <div class="kv">
        <h3>{inline(demo['title'])}</h3>
        <p class="section-note">{escape(demo['source_label'])}</p>
        {bullets(demo['points'])}
      </div>
    </div>
    """


def clean_label(text: str) -> str:
    return strip_md(text).replace("`", "")


def label_lines(text: str, max_chars: int, max_lines: int = 3) -> list[str]:
    cleaned = clean_label(text)
    if not cleaned:
        return [""]
    words = cleaned.split()
    lines: list[str] = []
    if len(words) > 1:
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and len(candidate) > max_chars:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
    else:
        lines = [cleaned[i : i + max_chars] for i in range(0, len(cleaned), max_chars)]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(0, max_chars - 3)].rstrip() + "..."
    return lines


def svg_text(
    text: str,
    x: float,
    y: float,
    max_chars: int,
    *,
    max_lines: int = 3,
    size: int = 14,
    weight: int = 600,
    fill: str = "#1f2937",
    anchor: str = "middle",
    line_height: int | None = None,
) -> str:
    line_height = line_height or int(size * 1.32)
    lines = label_lines(text, max_chars, max_lines)
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">'
        + "".join(tspans)
        + "</text>"
    )


def svg_defs() -> str:
    return """
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#315c8f"/>
      </marker>
      <marker id="arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f766e"/>
      </marker>
      <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#a66f12"/>
      </marker>
      <filter id="soft-shadow" x="-20%" y="-20%" width="140%" height="150%">
        <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#111827" flood-opacity=".10"/>
      </filter>
    </defs>
    """


def diagram_svg_shell(svg: str, caption: str) -> str:
    return f"""
    <div class="svg-frame">{svg}</div>
    <p class="diagram-caption">{inline(caption)}</p>
    """


def mobile_flow_html(project: dict) -> str:
    rows = []
    for index, (frm, to, msg, note) in enumerate(project["diagrams"]["sequence"], start=1):
        rows.append(
            f"""
            <div class="mobile-step" data-step="{index}">
              <b>{escape(frm)} -> {escape(to)}</b>
              <p>{inline(msg)}</p>
              <small>{inline(note)}</small>
            </div>
            """
        )
    return '<div class="diagram-mobile">' + "".join(rows) + "</div>"


def mobile_component_html(project: dict) -> str:
    rows = [
        f"""
        <div class="mobile-step" data-step="{index}">
          <b>{escape(name)}</b>
          <p>{inline(role)}</p>
        </div>
        """
        for index, (name, role) in enumerate(project["diagrams"]["components"], start=1)
    ]
    return '<div class="diagram-mobile">' + "".join(rows) + "</div>"


def mobile_system_html(project: dict) -> str:
    rows = []
    for loop in project["diagrams"].get("system", []):
        rows.append(
            f"""
            <div class="mobile-loop">
              <b>{escape(loop["kind"])} · {inline(loop["title"])}</b>
              <p>{inline(" -> ".join(loop["items"]))}</p>
            </div>
            """
        )
    return '<div class="diagram-mobile">' + "".join(rows) + "</div>"


def flow_svg(project: dict) -> str:
    sequence = project["diagrams"]["sequence"]
    nodes = [sequence[0][0]] + [step[1] for step in sequence]
    width, height = 1180, 470
    margin, node_w, node_h = 62, 148, 66
    gap = (width - margin * 2) / (len(nodes) - 1)
    y = 82
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(project["title"])} runtime flow">',
        svg_defs(),
        '<rect x="1" y="1" width="1178" height="468" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text("运行主链路", 42, 38, 12, size=15, weight=850, fill="#0f766e", anchor="start"),
        svg_text(project["diagrams"]["scenario"], 185, 38, 58, size=13, weight=500, fill="#65707d", anchor="start", max_lines=2),
    ]
    xs = [margin + index * gap for index in range(len(nodes))]
    for index, name in enumerate(nodes):
        x = xs[index] - node_w / 2
        fill = "#e8f4f2" if index == 0 else "#f8fafb"
        stroke = "#0f766e" if index == 0 else "#cfd8d3"
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{node_w}" height="{node_h}" rx="8" fill="{fill}" stroke="{stroke}" filter="url(#soft-shadow)"/>')
        parts.append(f'<circle cx="{x + 22:.1f}" cy="{y + 22}" r="12" fill="#17202b"/>')
        parts.append(svg_text(str(index + 1), x + 22, y + 27, 3, size=12, weight=850, fill="#ffffff"))
        parts.append(svg_text(name, xs[index], y + 42, 14, size=14, weight=850, fill="#17202b", max_lines=2))
    for index, (frm, to, msg, note) in enumerate(sequence):
        x1 = xs[index] + node_w / 2 + 8
        x2 = xs[index + 1] - node_w / 2 - 8
        mid = (x1 + x2) / 2
        parts.append(f'<path d="M{x1:.1f},{y + 33} L{x2:.1f},{y + 33}" stroke="#315c8f" stroke-width="2.5" fill="none" marker-end="url(#arrow-blue)"/>')
        card_w = max(128, min(190, x2 - x1 + 46))
        card_x = mid - card_w / 2
        card_y = 190 + (index % 2) * 92
        parts.append(f'<path d="M{mid:.1f},{y + 43} V{card_y - 10}" stroke="#9fb3c7" stroke-width="1.4" stroke-dasharray="4 5"/>')
        parts.append(f'<rect x="{card_x:.1f}" y="{card_y}" width="{card_w:.1f}" height="76" rx="8" fill="#edf3fb" stroke="#b9cde5"/>')
        parts.append(svg_text(msg, mid, card_y + 27, 15, size=12, weight=800, fill="#1f3f65", max_lines=2))
        parts.append(svg_text(note, mid, card_y + 55, 16, size=11, weight=500, fill="#586879", max_lines=2))
    parts.append('<rect x="62" y="408" width="1056" height="28" rx="14" fill="#f4f7f6" stroke="#d8ddd9"/>')
    parts.append(svg_text("读图方式：从左到右看一次真实任务如何通过项目核心机制完成；下方蓝色框是每一步的关键协议、数据或行为转换。", 590, 427, 76, size=12, weight=550, fill="#4b5563", max_lines=1))
    parts.append("</svg>")
    return "\n".join(parts)


def center_component_label(project: dict) -> str:
    component_names = [name for name, _ in project["diagrams"]["components"]]
    for needle in ["DataHub", "Anthropic", "ModelRouter", "CLAUDE", "规则"]:
        for name in component_names:
            if needle.lower() in name.lower():
                return name
    return "核心机制契约"


def component_svg(project: dict) -> str:
    components = project["diagrams"]["components"]
    width, height = 1180, 500
    bus_y = 226
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(project["title"])} component map">',
        svg_defs(),
        '<rect x="1" y="1" width="1178" height="498" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text("组件关系", 42, 38, 12, size=15, weight=850, fill="#0f766e", anchor="start"),
        '<rect x="210" y="218" width="760" height="78" rx="12" fill="#17202b" stroke="#17202b"/>',
        svg_text(center_component_label(project), 590, 251, 30, size=19, weight=900, fill="#ffffff", max_lines=1),
        svg_text("让模块、数据和外部系统形成可复用的协作边界", 590, 276, 34, size=12, weight=500, fill="#dbe7ef", max_lines=1),
    ]
    top_slots = (len(components) + 1) // 2
    bottom_slots = len(components) // 2
    top_xs = [220 + i * (740 / max(1, top_slots - 1)) for i in range(top_slots)]
    bottom_xs = [220 + i * (740 / max(1, bottom_slots - 1)) for i in range(bottom_slots)] if bottom_slots else []
    top_index = bottom_index = 0
    for index, (name, role) in enumerate(components):
        is_top = index % 2 == 0
        x_center = top_xs[top_index] if is_top else bottom_xs[bottom_index]
        top_index += 1 if is_top else 0
        bottom_index += 0 if is_top else 1
        box_w, box_h = 250, 94
        y = 82 if is_top else 352
        x = x_center - box_w / 2
        color = "#edf3fb" if is_top else "#e8f4f2"
        stroke = "#b9cde5" if is_top else "#b8d8d3"
        connector_start_y = y + box_h if is_top else y
        connector_end_y = bus_y if is_top else bus_y + 78
        marker = "arrow-blue" if is_top else "arrow-teal"
        parts.append(f'<path d="M{x_center:.1f},{connector_start_y:.1f} L{x_center:.1f},{connector_end_y:.1f}" stroke="{("#315c8f" if is_top else "#0f766e")}" stroke-width="2" fill="none" marker-end="url(#{marker})"/>')
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="{color}" stroke="{stroke}"/>')
        parts.append(svg_text(name, x + 16, y + 30, 23, size=14, weight=900, fill="#17202b", anchor="start", max_lines=1))
        parts.append(svg_text(role, x + 16, y + 55, 27, size=12, weight=500, fill="#53606d", anchor="start", max_lines=2))
    parts.append('<path d="M120,257 H206" stroke="#a66f12" stroke-width="2.4" fill="none" marker-end="url(#arrow-amber)"/>')
    parts.append('<path d="M974,257 H1060" stroke="#a66f12" stroke-width="2.4" fill="none" marker-end="url(#arrow-amber)"/>')
    parts.append(svg_text("输入", 96, 263, 8, size=13, weight=800, fill="#a66f12"))
    parts.append(svg_text("输出", 1084, 263, 8, size=13, weight=800, fill="#a66f12"))
    parts.append("</svg>")
    return "\n".join(parts)


def system_loop_color(kind: str) -> tuple[str, str, str]:
    normalized = kind.upper()
    if normalized == "R":
        return "#315c8f", "#edf3fb", "arrow-blue"
    if normalized == "B":
        return "#a66f12", "#fff5dd", "arrow-amber"
    return "#0f766e", "#e8f4f2", "arrow-teal"


def cld_loop_svg(parts: list[str], loop: dict, y0: int, width: int) -> None:
    color, fill, marker = system_loop_color(loop["kind"])
    items = loop["items"]
    parts.append(f'<rect x="32" y="{y0}" width="{width - 64}" height="206" rx="10" fill="{fill}" stroke="{color}" stroke-opacity=".32"/>')
    parts.append(f'<circle cx="86" cy="{y0 + 58}" r="26" fill="#fff" stroke="{color}" stroke-width="2"/>')
    parts.append(svg_text(loop["kind"], 86, y0 + 66, 4, size=22, weight=900, fill=color))
    parts.append(svg_text(loop["title"], 126, y0 + 46, 28, size=16, weight=900, fill="#17202b", anchor="start", max_lines=1))
    parts.append(svg_text("CLD 回路", 126, y0 + 70, 18, size=12, weight=700, fill="#65707d", anchor="start", max_lines=1))
    start_x, available = 230, width - 420
    step = available / max(1, len(items) - 1)
    xs = [start_x + i * step for i in range(len(items))]
    box_w, box_h = min(155, step - 22 if len(items) > 1 else 170), 58
    y = y0 + 88
    for index, item in enumerate(items):
        x = xs[index] - box_w / 2
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{box_w:.1f}" height="{box_h}" rx="8" fill="#fff" stroke="{color}" stroke-opacity=".38"/>')
        parts.append(svg_text(item, xs[index], y + 24, 13, size=12, weight=700, fill="#29313c", max_lines=2))
        if index < len(items) - 1:
            x1 = xs[index] + box_w / 2 + 8
            x2 = xs[index + 1] - box_w / 2 - 8
            parts.append(f'<path d="M{x1:.1f},{y + 29} L{x2:.1f},{y + 29}" stroke="{color}" stroke-width="2" fill="none" marker-end="url(#{marker})"/>')
            parts.append(svg_text("+" if loop["kind"].upper() == "R" else "-", (x1 + x2) / 2, y + 20, 2, size=12, weight=900, fill=color))
    if len(items) > 2:
        parts.append(
            f'<path d="M{xs[-1]:.1f},{y + box_h + 12} C{xs[-1]:.1f},{y0 + 196} {xs[0]:.1f},{y0 + 196} {xs[0]:.1f},{y + box_h + 12}" '
            f'stroke="{color}" stroke-width="2.2" fill="none" marker-end="url(#{marker})"/>'
        )


def sfd_svg(parts: list[str], loop: dict, y0: int, width: int) -> None:
    color, fill, marker = system_loop_color(loop["kind"])
    items = loop["items"]
    labels = (items + ["", "", "", ""])[:4]
    parts.append(f'<rect x="32" y="{y0}" width="{width - 64}" height="206" rx="10" fill="{fill}" stroke="{color}" stroke-opacity=".32"/>')
    parts.append(svg_text(loop["title"], 56, y0 + 42, 34, size=16, weight=900, fill="#17202b", anchor="start", max_lines=1))
    parts.append(svg_text("SFD：存量与流量", 56, y0 + 66, 20, size=12, weight=700, fill="#65707d", anchor="start", max_lines=1))
    cy = y0 + 122
    parts.append(f'<path d="M190,{cy} H380" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#{marker})"/>')
    parts.append(svg_text(labels[0], 285, cy - 15, 18, size=12, weight=700, fill=color, max_lines=1))
    parts.append(f'<rect x="390" y="{cy - 48}" width="210" height="96" rx="8" fill="#fff" stroke="{color}" stroke-width="2"/>')
    parts.append(f'<ellipse cx="495" cy="{cy - 48}" rx="105" ry="16" fill="#fff" stroke="{color}" stroke-width="2"/>')
    parts.append(f'<ellipse cx="495" cy="{cy + 48}" rx="105" ry="16" fill="none" stroke="{color}" stroke-width="2"/>')
    parts.append(svg_text(labels[2] or labels[1], 495, cy + 5, 18, size=14, weight=850, fill="#17202b", max_lines=2))
    parts.append(f'<path d="M610,{cy} H850" stroke="{color}" stroke-width="3" fill="none" marker-end="url(#{marker})"/>')
    parts.append(svg_text(labels[3], 730, cy - 15, 20, size=12, weight=700, fill=color, max_lines=1))
    parts.append(f'<rect x="870" y="{cy - 36}" width="190" height="72" rx="8" fill="#fff" stroke="{color}" stroke-opacity=".42"/>')
    parts.append(svg_text(labels[1], 965, cy - 2, 18, size=13, weight=850, fill="#29313c", max_lines=2))


def bot_svg(parts: list[str], loop: dict, y0: int, width: int) -> None:
    color, fill, marker = system_loop_color(loop["kind"])
    items = loop["items"]
    parts.append(f'<rect x="32" y="{y0}" width="{width - 64}" height="226" rx="10" fill="{fill}" stroke="{color}" stroke-opacity=".32"/>')
    parts.append(svg_text(loop["title"], 56, y0 + 42, 36, size=16, weight=900, fill="#17202b", anchor="start", max_lines=1))
    parts.append(svg_text("BOT：行为随时间变化", 56, y0 + 66, 24, size=12, weight=700, fill="#65707d", anchor="start", max_lines=1))
    x0, y_axis = 290, y0 + 168
    parts.append(f'<path d="M{x0},{y0 + 80} V{y_axis} H850" stroke="#64748b" stroke-width="1.8" fill="none"/>')
    parts.append(f'<path d="M{x0 + 20},{y_axis - 16} C{x0 + 165},{y_axis - 72} {x0 + 340},{y_axis - 88} 830,{y_axis - 114}" stroke="{color}" stroke-width="4" fill="none" marker-end="url(#{marker})"/>')
    parts.append(svg_text(items[0] if items else "干预增加", 360, y_axis - 48, 18, size=12, weight=800, fill=color, max_lines=1))
    parts.append(svg_text(items[2] if len(items) > 2 else "结果变化", 760, y_axis - 120, 18, size=12, weight=800, fill=color, max_lines=1))
    chip_x = 890
    for index, item in enumerate(items[:4]):
        yy = y0 + 82 + index * 32
        parts.append(f'<rect x="{chip_x}" y="{yy}" width="210" height="24" rx="12" fill="#fff" stroke="{color}" stroke-opacity=".32"/>')
        parts.append(svg_text(item, chip_x + 105, yy + 16, 20, size=11, weight=700, fill="#29313c", max_lines=1))


def system_svg(project: dict) -> str:
    loops = project["diagrams"].get("system", [])
    width = 1180
    row_heights = [246 if loop["kind"].upper() == "BOT" else 226 for loop in loops]
    height = max(280, 64 + sum(row_heights))
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(project["title"])} system dynamics">',
        svg_defs(),
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text("系统动力学视角", 42, 38, 18, size=15, weight=850, fill="#0f766e", anchor="start"),
    ]
    y0 = 58
    for loop, row_height in zip(loops, row_heights):
        kind = loop["kind"].upper()
        if kind == "SFD":
            sfd_svg(parts, loop, y0, width)
        elif kind == "BOT":
            bot_svg(parts, loop, y0, width)
        else:
            cld_loop_svg(parts, loop, y0, width)
        y0 += row_height
    parts.append("</svg>")
    return "\n".join(parts)


def mixed_svg(project: dict) -> str:
    sequence = project["diagrams"].get("sequence", [])
    loops = project["diagrams"].get("system", [])
    nodes = [sequence[0][0]] + [step[1] for step in sequence] if sequence else []
    width, height = 1180, 620
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(project["title"])} mixed behavior and dynamics">',
        svg_defs(),
        '<rect x="1" y="1" width="1178" height="618" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text("UML + 系统动力学混合视角", 42, 38, 26, size=15, weight=850, fill="#0f766e", anchor="start"),
        svg_text(project["diagrams"]["scenario"], 292, 38, 64, size=13, weight=500, fill="#65707d", anchor="start", max_lines=2),
    ]
    if nodes:
        margin, node_w, node_h = 78, 132, 62
        gap = (width - margin * 2) / max(1, len(nodes) - 1)
        y = 258
        xs = [margin + index * gap for index in range(len(nodes))]
        parts.append('<rect x="52" y="212" width="1076" height="156" rx="12" fill="#f8fafb" stroke="#d8ddd9"/>')
        parts.append(svg_text("微观执行骨架", 78, 238, 16, size=13, weight=850, fill="#17202b", anchor="start"))
        for index, name in enumerate(nodes):
            x = xs[index] - node_w / 2
            fill = "#e8f4f2" if index == 0 else "#fff"
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{node_w}" height="{node_h}" rx="8" fill="{fill}" stroke="#cfd8d3"/>')
            parts.append(svg_text(str(index + 1), x + 16, y + 24, 3, size=11, weight=900, fill="#0f766e"))
            parts.append(svg_text(name, xs[index], y + 42, 13, size=12, weight=850, fill="#17202b", max_lines=2))
            if index < len(nodes) - 1:
                parts.append(f'<path d="M{xs[index] + node_w / 2 + 8:.1f},{y + 31} L{xs[index + 1] - node_w / 2 - 8:.1f},{y + 31}" stroke="#315c8f" stroke-width="2.2" fill="none" marker-end="url(#arrow-blue)"/>')
    if loops:
        top = loops[0]
        color, fill, marker = system_loop_color(top["kind"])
        parts.append(f'<rect x="72" y="82" width="1036" height="94" rx="12" fill="{fill}" stroke="{color}" stroke-opacity=".36"/>')
        parts.append(svg_text(f'{top["kind"]} · {top["title"]}', 96, 114, 28, size=15, weight=900, fill=color, anchor="start"))
        top_items = top["items"][:5]
        x_start, x_gap = 310, 150
        for index, item in enumerate(top_items):
            x = x_start + index * x_gap
            parts.append(f'<rect x="{x - 58}" y="112" width="116" height="34" rx="17" fill="#fff" stroke="{color}" stroke-opacity=".34"/>')
            parts.append(svg_text(item, x, 134, 12, size=10, weight=700, fill="#29313c", max_lines=1))
            if index < len(top_items) - 1:
                parts.append(f'<path d="M{x + 62},129 H{x + x_gap - 64}" stroke="{color}" stroke-width="1.8" fill="none" marker-end="url(#{marker})"/>')
        parts.append(f'<path d="M980,154 C930,206 820,222 700,232" stroke="{color}" stroke-width="2.2" fill="none" stroke-dasharray="5 5" marker-end="url(#{marker})"/>')
    if len(loops) > 1:
        bottom = loops[1]
        color, fill, marker = system_loop_color(bottom["kind"])
        parts.append(f'<rect x="72" y="430" width="1036" height="124" rx="12" fill="{fill}" stroke="{color}" stroke-opacity=".36"/>')
        parts.append(svg_text(f'{bottom["kind"]} · {bottom["title"]}', 96, 464, 30, size=15, weight=900, fill=color, anchor="start"))
        bottom_items = bottom["items"][:4]
        x_start, x_gap = 330, 185
        for index, item in enumerate(bottom_items):
            x = x_start + index * x_gap
            parts.append(f'<rect x="{x - 72}" y="480" width="144" height="42" rx="8" fill="#fff" stroke="{color}" stroke-opacity=".34"/>')
            parts.append(svg_text(item, x, 505, 13, size=11, weight=750, fill="#29313c", max_lines=2))
            if index < len(bottom_items) - 1:
                parts.append(f'<path d="M{x + 78},501 H{x + x_gap - 80}" stroke="{color}" stroke-width="1.8" fill="none" marker-end="url(#{marker})"/>')
        parts.append(f'<path d="M270,480 C240,416 288,382 382,356" stroke="{color}" stroke-width="2.2" fill="none" stroke-dasharray="5 5" marker-end="url(#{marker})"/>')
    parts.append(svg_text("读图方式：中心看一次任务如何完成；外圈只保留对采用、信任、风险或存量变化有解释增益的反馈回路。", 590, 594, 78, size=12, weight=550, fill="#4b5563", max_lines=1))
    parts.append("</svg>")
    return "\n".join(parts)


def mobile_mixed_html(project: dict) -> str:
    wrapper = '<div class="diagram-mobile">'
    flow_inner = mobile_flow_html(project)
    system_inner = mobile_system_html(project)
    if flow_inner.startswith(wrapper):
        flow_inner = flow_inner[len(wrapper) : -6]
    if system_inner.startswith(wrapper):
        system_inner = system_inner[len(wrapper) : -6]
    rows = [
        """
        <div class="mobile-loop">
          <b>混合图读法</b>
          <p>先看任务执行步骤，再看哪些反馈回路会改变长期采用、风险或上下文存量。</p>
        </div>
        """
    ]
    return wrapper + "".join(rows) + flow_inner + system_inner + "</div>"


def mermaid_sequence(project: dict) -> str:
    lines = ["sequenceDiagram", "    autonumber"]
    aliases: dict[str, str] = {}

    def alias(name: str) -> str:
        if name not in aliases:
            aliases[name] = f"P{len(aliases) + 1}"
        return aliases[name]

    for frm, to, msg, note in project["diagrams"]["sequence"]:
        alias(frm)
        alias(to)
    for name, ref in aliases.items():
        lines.append(f"    participant {ref} as {name}")
    for frm, to, msg, note in project["diagrams"]["sequence"]:
        from_ref = alias(frm)
        to_ref = alias(to)
        lines.append(f"    {from_ref}->>{to_ref}: {msg}")
        lines.append(f"    Note over {to_ref}: {note}")
    return "\n".join(lines)


def mermaid_components(project: dict) -> str:
    lines = ["flowchart LR"]
    for idx, (name, role) in enumerate(project["diagrams"]["components"], start=1):
        safe = f"N{idx}"
        lines.append(f"    {safe}[{name}<br/>{role}]")
        if idx > 1:
            lines.append(f"    N{idx-1} --> {safe}")
    return "\n".join(lines)


def diagram_source(project: dict) -> str:
    diagrams = project["diagrams"]
    sources = []
    if diagrams.get("sequence"):
        sources.append("%% 主流程 / sequence\n" + mermaid_sequence(project))
    if diagrams.get("components"):
        sources.append("%% 组件关系 / component\n" + mermaid_components(project))
    if diagrams.get("system"):
        system_lines = ["%% 系统动力学 / CLD-SFD-BOT"]
        for loop in diagrams["system"]:
            system_lines.append(f'{loop["kind"]} {loop["title"]}: ' + " -> ".join(loop["items"]))
        sources.append("\n".join(system_lines))
    if diagrams.get("mixed"):
        sources.append("%% 混合图说明\n中心使用一次任务/请求执行骨架；外圈只叠加有解释增益的 CLD/SFD/BOT 回路。")
    return "\n\n---\n\n".join(sources)


def diagram_html(project: dict) -> str:
    diagrams = project.get("diagrams")
    if not diagrams:
        return ""
    type_chips = "".join(f'<span class="type-chip">{escape(t)}</span>' for t in diagrams["selected_types"])
    tabs: list[tuple[str, str, str]] = []
    if diagrams.get("mixed") and diagrams.get("sequence") and diagrams.get("system"):
        tabs.append((
            "mixed",
            "混合图",
            diagram_svg_shell(mixed_svg(project), "参考 docs/reference/image.md 的思路：中心是一次任务执行，外圈只保留有解释增益的动力回路。") + mobile_mixed_html(project),
        ))
    if diagrams.get("sequence"):
        tabs.append((
            "flow",
            "主流程",
            diagram_svg_shell(flow_svg(project), "主流程图把一次典型任务拆成角色、协议/数据转换和关键交接点。") + mobile_flow_html(project),
        ))
    if diagrams.get("components"):
        tabs.append((
            "component",
            "组件关系",
            diagram_svg_shell(component_svg(project), "组件图强调核心契约：哪个模块承接输入，哪些模块围绕它提供数据、适配或规则。") + mobile_component_html(project),
        ))
    if diagrams.get("system"):
        tabs.append((
            "system",
            "系统动力学",
            diagram_svg_shell(system_svg(project), "系统动力学图只在反馈、存量或趋势能解释项目机制时使用。") + mobile_system_html(project),
        ))
    source = diagram_source(project)
    tabs.append(("source", "图源", f'<pre class="mermaid-block">{escape(source)}</pre>'))
    buttons = "".join(
        f'<button type="button" data-diagram-tab="{escape(key)}" aria-selected="{str(index == 0).lower()}">{escape(label)}</button>'
        for index, (key, label, _) in enumerate(tabs)
    )
    panels = "".join(
        f'<div class="diagram-panel" data-diagram-panel="{escape(key)}" {"hidden" if index else ""}>{body}</div>'
        for index, (key, _, body) in enumerate(tabs)
    )
    return f"""
    <div class="diagram-shell">
      <div class="diagram-header">
        <div>
          <p class="scenario"><strong>选择理由：</strong>{inline(diagrams['reason'])}</p>
          <p class="scenario"><strong>场景：</strong>{inline(diagrams['scenario'])}</p>
        </div>
        <div class="type-row" aria-label="diagram model types">{type_chips}</div>
      </div>
      <div class="diagram-tabs" role="tablist" aria-label="diagram views">
        {buttons}
      </div>
      {panels}
    </div>
    """


def parse_mermaid_node_token(token: str) -> tuple[str, str]:
    cleaned = token.strip().rstrip(";")
    match = re.match(r"^([A-Za-z0-9_]+)\[(.+)\]$", cleaned)
    if match:
        return match.group(1), match.group(2).strip()
    match = re.match(r"^([A-Za-z0-9_]+)\((.+)\)$", cleaned)
    if match:
        return match.group(1), match.group(2).strip()
    return cleaned, cleaned


def split_mermaid_edge(line: str) -> tuple[str, str, str, bool] | None:
    if "-." in line and ".->" in line:
        left, rest = line.split("-.", 1)
        label, right = rest.split(".->", 1)
        return left.strip(), right.strip(), label.strip(), True
    if "-->" in line:
        left, right = line.split("-->", 1)
        return left.strip(), right.strip(), "", False
    return None


def parse_arch_flowchart(mermaid: str) -> tuple[str, dict[str, str], list[tuple[str, str, str, bool]], dict[str, str], list[str]]:
    orientation = "LR"
    nodes: dict[str, str] = {}
    edges: list[tuple[str, str, str, bool]] = []
    groups: dict[str, str] = {}
    order: list[str] = []
    current_group = ""
    for raw in mermaid.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("flowchart"):
            parts = line.split()
            if len(parts) > 1:
                orientation = parts[1].strip()
            continue
        if line.startswith("subgraph"):
            match = re.match(r"subgraph\s+([A-Za-z0-9_]+)\[(.+)\]", line)
            current_group = match.group(2).strip() if match else line.replace("subgraph", "", 1).strip()
            continue
        if line == "end":
            current_group = ""
            continue
        edge = split_mermaid_edge(line)
        if edge:
            left_token, right_token, edge_label, dotted = edge
            left_id, left_label = parse_mermaid_node_token(left_token)
            right_id, right_label = parse_mermaid_node_token(right_token)
            for node_id, label in [(left_id, left_label), (right_id, right_label)]:
                if node_id not in nodes:
                    order.append(node_id)
                nodes[node_id] = label
                if current_group:
                    groups.setdefault(node_id, current_group)
            edges.append((left_id, right_id, edge_label, dotted))
            continue
        node_id, label = parse_mermaid_node_token(line)
        if re.match(r"^[A-Za-z0-9_]+$", node_id):
            if node_id not in nodes:
                order.append(node_id)
            nodes[node_id] = label
            if current_group:
                groups[node_id] = current_group
    return orientation, nodes, edges, groups, order


def assign_arch_levels(nodes: dict[str, str], edges: list[tuple[str, str, str, bool]], order: list[str]) -> dict[str, int]:
    levels = {node_id: 0 for node_id in order}
    for frm, to, _, _ in edges:
        levels.setdefault(frm, 0)
        levels.setdefault(to, 0)
        if to not in order:
            order.append(to)
        if frm not in order:
            order.append(frm)
        if levels[to] <= levels[frm]:
            levels[to] = levels[frm] + 1
    max_level = max(levels.values(), default=0)
    if max_level > max(6, len(nodes)):
        return {node_id: index for index, node_id in enumerate(order)}
    return levels


def arch_flow_svg(mermaid: str, title: str) -> str:
    orientation, nodes, edges, groups, order = parse_arch_flowchart(mermaid)
    if not nodes:
        return f'<pre class="mermaid-block"><code>{escape(mermaid)}</code></pre>'
    levels = assign_arch_levels(nodes, edges, order[:])
    layer_map: dict[int, list[str]] = {}
    for node_id in order:
        layer_map.setdefault(levels.get(node_id, 0), []).append(node_id)
    layer_count = max(layer_map.keys(), default=0) + 1
    max_rows = max((len(v) for v in layer_map.values()), default=1)
    width = 1180
    height = max(310, 110 + max_rows * 112)
    node_w = 190 if layer_count <= 5 else 160
    node_h = 74
    x_margin = 82
    y_margin = 92
    positions: dict[str, tuple[float, float]] = {}
    if orientation.upper() == "TB":
        height = max(360, 118 + layer_count * 112)
        max_cols = max((len(v) for v in layer_map.values()), default=1)
        for level in range(layer_count):
            layer_nodes = layer_map.get(level, [])
            y = y_margin + level * 112
            available = width - x_margin * 2
            step = available / max(1, len(layer_nodes) - 1)
            for idx, node_id in enumerate(layer_nodes):
                x = width / 2 if len(layer_nodes) == 1 else x_margin + idx * step
                positions[node_id] = (x, y)
    else:
        available = width - x_margin * 2
        step_x = available / max(1, layer_count - 1)
        for level in range(layer_count):
            layer_nodes = layer_map.get(level, [])
            x = x_margin + level * step_x
            step_y = max(92, (height - y_margin - 46) / max(1, len(layer_nodes)))
            start_y = y_margin + (height - y_margin - step_y * (len(layer_nodes) - 1)) / 2 - 28 if layer_nodes else y_margin
            for idx, node_id in enumerate(layer_nodes):
                positions[node_id] = (x, start_y + idx * step_y)
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)} architecture flow">',
        svg_defs(),
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text(title, 42, 38, 28, size=15, weight=850, fill="#0f766e", anchor="start"),
        svg_text("Mermaid flowchart 渲染图", 42, 62, 30, size=12, weight=650, fill="#65707d", anchor="start"),
    ]
    for frm, to, edge_label, dotted in edges:
        if frm not in positions or to not in positions:
            continue
        x1, y1 = positions[frm]
        x2, y2 = positions[to]
        if orientation.upper() == "TB":
            start = (x1, y1 + node_h / 2)
            end = (x2, y2 - node_h / 2 - 8)
            path = f"M{start[0]:.1f},{start[1]:.1f} L{end[0]:.1f},{end[1]:.1f}"
        else:
            start = (x1 + node_w / 2, y1)
            end = (x2 - node_w / 2 - 8, y2)
            mid_x = (start[0] + end[0]) / 2
            path = f"M{start[0]:.1f},{start[1]:.1f} C{mid_x:.1f},{start[1]:.1f} {mid_x:.1f},{end[1]:.1f} {end[0]:.1f},{end[1]:.1f}"
        dash = ' stroke-dasharray="5 5"' if dotted else ""
        parts.append(f'<path d="{path}" stroke="#315c8f" stroke-width="2.2" fill="none"{dash} marker-end="url(#arrow-blue)"/>')
        if edge_label:
            label_x = (start[0] + end[0]) / 2
            label_y = (start[1] + end[1]) / 2 - 8
            parts.append(f'<rect x="{label_x - 46:.1f}" y="{label_y - 15:.1f}" width="92" height="22" rx="11" fill="#edf3fb" stroke="#b9cde5"/>')
            parts.append(svg_text(edge_label, label_x, label_y, 12, size=10, weight=800, fill="#254466", max_lines=1))
    for node_id in order:
        x, y = positions[node_id]
        label = nodes[node_id]
        group = groups.get(node_id, "")
        fill = "#e8f4f2" if group else "#ffffff"
        stroke = "#8ac7bd" if group else "#cfd8d3"
        parts.append(f'<rect x="{x - node_w / 2:.1f}" y="{y - node_h / 2:.1f}" width="{node_w}" height="{node_h}" rx="8" fill="{fill}" stroke="{stroke}" filter="url(#soft-shadow)"/>')
        parts.append(svg_text(label, x, y - 4, 19, size=13, weight=850, fill="#17202b", max_lines=2))
        if group:
            parts.append(svg_text(group, x, y + 26, 22, size=10, weight=650, fill="#65707d", max_lines=1))
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "上图由架构视角的 Mermaid flowchart 源码静态渲染，源码保留在下方。")


def arch_box(parts: list[str], x: float, y: float, w: float, h: float, title: str, subtitle: str = "", *, fill: str = "#ffffff", stroke: str = "#cfd8d3", title_fill: str = "#17202b") -> None:
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="{fill}" stroke="{stroke}" filter="url(#soft-shadow)"/>')
    parts.append(svg_text(title, x + w / 2, y + h / 2 - (8 if subtitle else -4), 20, size=14, weight=900, fill=title_fill, max_lines=2))
    if subtitle:
        parts.append(svg_text(subtitle, x + w / 2, y + h / 2 + 22, 24, size=11, weight=600, fill="#65707d", max_lines=1))


def arch_arrow(parts: list[str], x1: float, y1: float, x2: float, y2: float, label: str = "", *, color: str = "#315c8f", dashed: bool = False, marker: str = "arrow-blue") -> None:
    dash = ' stroke-dasharray="5 5"' if dashed else ""
    parts.append(f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" stroke="{color}" stroke-width="2.3" fill="none"{dash} marker-end="url(#{marker})"/>')
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        parts.append(f'<rect x="{mx - 54:.1f}" y="{my - 17:.1f}" width="108" height="24" rx="12" fill="#fff" stroke="#d8ddd9"/>')
        parts.append(svg_text(label, mx, my, 14, size=10, weight=800, fill="#254466", max_lines=1))


def arch_svg_canvas(title: str, height: int) -> list[str]:
    width = 1180
    return [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)} architecture diagram">',
        svg_defs(),
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text(title, 42, 38, 28, size=15, weight=850, fill="#0f766e", anchor="start"),
        svg_text("语义架构图", 42, 62, 18, size=12, weight=650, fill="#65707d", anchor="start"),
    ]


def semantic_proxy_context_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 360)
    y = 155
    nodes = [
        (70, y, 170, 76, "Developer", "uses"),
        (280, y, 190, 76, "Claude Code", "Anthropic API shape"),
        (520, y, 220, 86, "free-claude-code", "local/self-hosted proxy"),
        (790, 100, 160, 66, "MODEL_*", "routing config"),
        (790, 205, 230, 76, "External / Local Models", "provider families"),
    ]
    for node in nodes:
        fill = "#e8f4f2" if node[4] == "free-claude-code" else "#ffffff"
        stroke = "#8ac7bd" if node[4] == "free-claude-code" else "#cfd8d3"
        arch_box(parts, *node, fill=fill, stroke=stroke)
    arch_arrow(parts, 240, y + 38, 280, y + 38, "task")
    arch_arrow(parts, 470, y + 38, 520, y + 38, "/v1/messages")
    arch_arrow(parts, 740, y + 25, 790, 133, "model map")
    arch_arrow(parts, 740, y + 58, 790, 243, "provider call")
    arch_arrow(parts, 790, 263, 740, y + 68, "SSE", color="#0f766e", marker="arrow-teal")
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "上下文图突出系统边界：Claude Code 不变，代理承接路由和 provider 适配。")


def semantic_proxy_static_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 360)
    y = 155
    xs = [90, 295, 500, 705, 910]
    labels = [
        ("FastAPI Routes", "Anthropic endpoint"),
        ("ModelRouter", "model mapping"),
        ("Provider Registry", "catalog / factory"),
        ("Provider Adapters", "schema conversion"),
        ("Anthropic Core", "SSE / tools / errors"),
    ]
    for x, (name, role) in zip(xs, labels):
        arch_box(parts, x, y, 160, 76, name, role, fill="#ffffff")
    for index in range(len(xs) - 1):
        arch_arrow(parts, xs[index] + 160, y + 38, xs[index + 1], y + 38)
    arch_box(parts, 500, 275, 180, 50, "Smoke / Provider Tests", "guard compatibility", fill="#edf3fb", stroke="#b9cde5")
    arch_arrow(parts, 590, 275, 990, y + 76, "guard", dashed=True)
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "静态组织图只保留扩展 provider 和维护兼容层需要看的边界。")


def semantic_fincept_context_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 460)
    arch_box(parts, 60, 190, 150, 70, "Researcher", "AAPL workflow")
    arch_box(parts, 265, 170, 190, 100, "Qt Desktop", "Equity Research UI", fill="#e8f4f2", stroke="#8ac7bd")
    arch_box(parts, 520, 160, 210, 120, "DataHub Topic Bus", "quote / news / financials", fill="#17202b", stroke="#17202b", title_fill="#ffffff")
    right_nodes = [
        (820, 90, 210, 62, "Market / News / Financial APIs", "external sources"),
        (820, 190, 180, 62, "Python Analytics", "local runtime"),
        (820, 290, 180, 62, "Cache / State", "local context"),
    ]
    for node in right_nodes:
        arch_box(parts, *node)
    arch_box(parts, 265, 315, 190, 62, "Research Views", "charts / tables / news")
    arch_arrow(parts, 210, 225, 265, 220, "opens")
    arch_arrow(parts, 455, 220, 520, 220, "subscribe")
    arch_arrow(parts, 730, 195, 820, 121, "producers")
    arch_arrow(parts, 730, 220, 820, 221)
    arch_arrow(parts, 730, 245, 820, 321)
    arch_arrow(parts, 520, 255, 455, 346, "publish", color="#0f766e", marker="arrow-teal")
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "系统全貌图突出研究场景边界：UI 通过 DataHub 组织外部数据、Python 分析和本地状态。")


def semantic_fincept_static_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 470)
    parts.append('<rect x="52" y="88" width="710" height="312" rx="14" fill="#fbfcfb" stroke="#cfd8d3"/>')
    parts.append(svg_text("Qt Desktop Application", 80, 118, 26, size=14, weight=900, fill="#0f766e", anchor="start"))
    arch_box(parts, 95, 160, 180, 62, "src/screens", "UI scenes")
    arch_box(parts, 95, 285, 180, 62, "src/app/main.cpp", "startup / wiring")
    arch_box(parts, 335, 160, 190, 62, "Services / Producers", "HTTP / WS / broker")
    arch_box(parts, 335, 285, 190, 62, "DataHub", "topic contract", fill="#17202b", stroke="#17202b", title_fill="#ffffff")
    arch_box(parts, 585, 225, 130, 62, "SQLite / Cache", "state")
    arch_box(parts, 845, 190, 220, 74, "fincept-qt/scripts", "Python analytics / agents")
    arch_arrow(parts, 275, 191, 335, 191, "events")
    arch_arrow(parts, 275, 316, 335, 316, "init")
    arch_arrow(parts, 525, 191, 585, 248, "state")
    arch_arrow(parts, 525, 316, 585, 265, "cache")
    arch_arrow(parts, 715, 256, 845, 227, "runtime")
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "静态组织图用分层边界表达 C++/Qt、DataHub、缓存和 Python 运行时的职责。")


def semantic_fincept_deployment_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 430)
    parts.append('<rect x="70" y="100" width="500" height="255" rx="14" fill="#fbfcfb" stroke="#cfd8d3"/>')
    parts.append(svg_text("User Workstation", 96, 130, 24, size=14, weight=900, fill="#0f766e", anchor="start"))
    arch_box(parts, 115, 165, 170, 62, "Qt App", "desktop runtime")
    arch_box(parts, 345, 145, 170, 62, "Python Runtime", "local scripts")
    arch_box(parts, 345, 250, 170, 62, "Local Cache", "profile / state")
    arch_box(parts, 690, 105, 210, 62, "Market Data APIs", "licensed data")
    arch_box(parts, 690, 210, 210, 62, "News / Financial APIs", "external data")
    arch_box(parts, 690, 315, 210, 62, "Broker Connection", "optional / sensitive")
    arch_box(parts, 950, 315, 150, 62, "Real Account", "safety boundary", fill="#fff5dd", stroke="#e6cf9f")
    arch_arrow(parts, 285, 196, 345, 176)
    arch_arrow(parts, 285, 196, 345, 281)
    arch_arrow(parts, 570, 196, 690, 136, "fetch")
    arch_arrow(parts, 570, 196, 690, 241, "fetch")
    arch_arrow(parts, 570, 196, 690, 346, "optional", dashed=True)
    arch_arrow(parts, 900, 346, 950, 346, "risk", color="#a66f12", marker="arrow-amber")
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "部署视图强调机构采用前必须确认的本地运行、外部数据、broker 和真实账户边界。")


def semantic_skill_context_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 390)
    arch_box(parts, 80, 170, 170, 70, "Developer", "asks task")
    arch_box(parts, 500, 145, 200, 110, "Coding Agent", "acts in repo", fill="#e8f4f2", stroke="#8ac7bd")
    arch_box(parts, 900, 170, 190, 70, "Target Repository", "code changes")
    arch_box(parts, 500, 60, 220, 62, "Rule Pack", "clarify / simple / surgical")
    arch_box(parts, 120, 285, 180, 56, "EXAMPLES.md", "calibrates behavior", fill="#edf3fb", stroke="#b9cde5")
    arch_arrow(parts, 250, 205, 500, 200, "request")
    arch_arrow(parts, 600, 122, 600, 145, "constraints", color="#0f766e", marker="arrow-teal")
    arch_arrow(parts, 700, 200, 900, 205, "minimal change")
    arch_arrow(parts, 300, 313, 500, 236, "examples", dashed=True)
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "上下文图表达规则包的真实作用：它约束 agent 行为，而不是作为运行服务参与调用链。")


def semantic_skill_distribution_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 430)
    arch_box(parts, 90, 178, 210, 86, "Four Principles", "core behavior contract", fill="#17202b", stroke="#17202b", title_fill="#ffffff")
    outputs = [
        (470, 90, "CLAUDE.md", "repo/global instruction"),
        (470, 170, "Claude Skill SKILL.md", "skill distribution"),
        (470, 250, "Cursor Rule", "alwaysApply rule"),
        (470, 330, "EXAMPLES.md", "behavior calibration"),
    ]
    for x, y, name, note in outputs:
        arch_box(parts, x, y, 220, 56, name, note)
        arch_arrow(parts, 300, 221, x, y + 28)
    arch_box(parts, 835, 170, 220, 86, "Team Agent Baseline", "shared behavior")
    arch_arrow(parts, 690, 118, 835, 196)
    arch_arrow(parts, 690, 198, 835, 208)
    arch_arrow(parts, 690, 278, 835, 220)
    arch_arrow(parts, 690, 358, 835, 232, "calibrate", dashed=True)
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "分发结构图把核心原则和多种落地格式分开，避免画成不存在的系统组件网络。")


def semantic_neat_context_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 430)
    arch_box(parts, 75, 175, 170, 70, "Developer", "end-of-session")
    arch_box(parts, 340, 150, 205, 118, "Coding Agent", "loads neat-freak", fill="#e8f4f2", stroke="#8ac7bd")
    arch_box(parts, 650, 60, 230, 62, "Root AI Files", "CLAUDE.md / AGENTS.md")
    arch_box(parts, 650, 180, 230, 62, "Project Docs", "README / docs")
    arch_box(parts, 650, 300, 230, 62, "Agent Memory", "platform-specific")
    arch_box(parts, 940, 176, 170, 74, "Change Summary", "what changed / skipped")
    arch_arrow(parts, 245, 210, 340, 208, "/neat")
    arch_arrow(parts, 545, 198, 650, 91, "sync")
    arch_arrow(parts, 545, 205, 650, 211, "sync")
    arch_arrow(parts, 545, 212, 650, 331, "sync")
    arch_arrow(parts, 880, 211, 940, 213, "report", color="#0f766e", marker="arrow-teal")
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "上下文图强调 neat-freak 的边界：它不是运行服务，而是会话收尾时同步文档、根级 AI 指令和平台记忆的规则包。")


def semantic_neat_distribution_svg(title: str) -> str:
    parts = arch_svg_canvas(title, 430)
    arch_box(parts, 90, 172, 210, 92, "neat-freak/SKILL.md", "triggers + workflow", fill="#17202b", stroke="#17202b", title_fill="#ffffff")
    outputs = [
        (460, 80, "Trigger Phrases", "/neat / sync up / 整理一下"),
        (460, 165, "Inventory Workflow", "ls + read + classify"),
        (460, 250, "sync-matrix.md", "change impact mapping"),
        (460, 335, "agent-paths.md", "platform memory paths"),
    ]
    for x, y, name, note in outputs:
        arch_box(parts, x, y, 235, 58, name, note)
        arch_arrow(parts, 300, 218, x, y + 29)
    arch_box(parts, 835, 95, 230, 72, "Docs First", "README / docs")
    arch_box(parts, 835, 215, 230, 72, "AI Context Next", "AGENTS / CLAUDE / memory")
    arch_box(parts, 835, 335, 230, 58, "Self-check", "paths / dates / contradictions")
    arch_arrow(parts, 695, 194, 835, 131)
    arch_arrow(parts, 695, 279, 835, 251)
    arch_arrow(parts, 695, 364, 835, 364)
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "静态组织图把触发词、盘点流程、影响矩阵和平台路径分开，说明它如何把一次收尾动作拆成可审查步骤。")


SEMANTIC_ARCH_RENDERERS = {
    "proxy_context": semantic_proxy_context_svg,
    "proxy_static": semantic_proxy_static_svg,
    "fincept_context": semantic_fincept_context_svg,
    "fincept_static": semantic_fincept_static_svg,
    "fincept_deployment": semantic_fincept_deployment_svg,
    "skill_context": semantic_skill_context_svg,
    "skill_distribution": semantic_skill_distribution_svg,
    "neat_context": semantic_neat_context_svg,
    "neat_distribution": semantic_neat_distribution_svg,
}


def parse_arch_sequence(mermaid: str) -> tuple[dict[str, str], list[tuple[str, str, str]], list[str]]:
    participants: dict[str, str] = {}
    order: list[str] = []
    messages: list[tuple[str, str, str]] = []
    for raw in mermaid.splitlines():
        line = raw.strip()
        if not line or line in {"sequenceDiagram", "autonumber"}:
            continue
        part_match = re.match(r"^(participant|actor)\s+([A-Za-z0-9_]+)\s+as\s+(.+)$", line)
        if part_match:
            alias, label = part_match.group(2), part_match.group(3).strip()
            participants[alias] = label
            if alias not in order:
                order.append(alias)
            continue
        msg_match = re.match(r"^([A-Za-z0-9_]+)\s*[-.]+>>\s*([A-Za-z0-9_]+)\s*:\s*(.+)$", line)
        if msg_match:
            frm, to, msg = msg_match.group(1), msg_match.group(2), msg_match.group(3).strip()
            for alias in [frm, to]:
                participants.setdefault(alias, alias)
                if alias not in order:
                    order.append(alias)
            messages.append((frm, to, msg))
    return participants, messages, order


def arch_sequence_svg(mermaid: str, title: str) -> str:
    participants, messages, order = parse_arch_sequence(mermaid)
    if not order:
        return f'<pre class="mermaid-block"><code>{escape(mermaid)}</code></pre>'
    width = 1180
    height = max(360, 150 + len(messages) * 58)
    margin_x = 72
    available = width - margin_x * 2
    step = available / max(1, len(order) - 1)
    xs = {alias: (width / 2 if len(order) == 1 else margin_x + idx * step) for idx, alias in enumerate(order)}
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)} sequence">',
        svg_defs(),
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="8" fill="#fffdf8" stroke="#d8ddd9"/>',
        svg_text(title, 42, 38, 28, size=15, weight=850, fill="#0f766e", anchor="start"),
        svg_text("Mermaid sequenceDiagram 渲染图", 42, 62, 34, size=12, weight=650, fill="#65707d", anchor="start"),
    ]
    top_y = 92
    for idx, alias in enumerate(order, start=1):
        x = xs[alias]
        parts.append(f'<rect x="{x - 72:.1f}" y="{top_y - 34}" width="144" height="58" rx="8" fill="#edf3fb" stroke="#b9cde5"/>')
        parts.append(f'<circle cx="{x - 54:.1f}" cy="{top_y - 13}" r="11" fill="#17202b"/>')
        parts.append(svg_text(str(idx), x - 54, top_y - 9, 3, size=10, weight=900, fill="#ffffff"))
        parts.append(svg_text(participants[alias], x + 10, top_y - 11, 14, size=12, weight=850, fill="#17202b", max_lines=2))
        parts.append(f'<path d="M{x:.1f},{top_y + 24} V{height - 34}" stroke="#b9c6d2" stroke-width="1.4" stroke-dasharray="5 6"/>')
    for idx, (frm, to, msg) in enumerate(messages, start=1):
        y = top_y + 62 + (idx - 1) * 58
        x1, x2 = xs[frm], xs[to]
        direction = 1 if x2 >= x1 else -1
        start_x = x1 + 34 * direction
        end_x = x2 - 42 * direction
        marker = "arrow-blue" if direction > 0 else "arrow-teal"
        parts.append(f'<path d="M{start_x:.1f},{y} H{end_x:.1f}" stroke="#315c8f" stroke-width="2.2" fill="none" marker-end="url(#{marker})"/>')
        label_x = (start_x + end_x) / 2
        label_w = min(260, max(150, abs(end_x - start_x) - 18))
        parts.append(f'<rect x="{label_x - label_w / 2:.1f}" y="{y - 28}" width="{label_w:.1f}" height="24" rx="12" fill="#fff" stroke="#d8ddd9"/>')
        parts.append(svg_text(msg, label_x, y - 11, 28, size=11, weight=750, fill="#29313c", max_lines=1))
    parts.append("</svg>")
    return diagram_svg_shell("\n".join(parts), "上图由架构视角的 Mermaid sequenceDiagram 源码静态渲染，源码保留在下方。")


def architecture_mermaid_visual(view: dict) -> str:
    semantic_renderer = SEMANTIC_ARCH_RENDERERS.get(view.get("visual_kind", ""))
    if semantic_renderer:
        return semantic_renderer(view["title"])
    mermaid = view["mermaid"]
    title = view["title"]
    first_line = next((line.strip() for line in mermaid.splitlines() if line.strip()), "")
    if first_line.startswith("sequenceDiagram"):
        return arch_sequence_svg(mermaid, title)
    if first_line.startswith("flowchart"):
        return arch_flow_svg(mermaid, title)
    return f'<pre class="mermaid-block"><code>{escape(mermaid)}</code></pre>'


def architecture_mermaid_mobile(mermaid: str) -> str:
    first_line = next((line.strip() for line in mermaid.splitlines() if line.strip()), "")
    rows: list[str] = []
    if first_line.startswith("sequenceDiagram"):
        participants, messages, _ = parse_arch_sequence(mermaid)
        for index, (frm, to, msg) in enumerate(messages, start=1):
            rows.append(
                f"""
                <div class="mobile-step" data-step="{index}">
                  <b>{escape(participants.get(frm, frm))} -> {escape(participants.get(to, to))}</b>
                  <p>{inline(msg)}</p>
                </div>
                """
            )
    elif first_line.startswith("flowchart"):
        _, nodes, edges, _, _ = parse_arch_flowchart(mermaid)
        for index, (frm, to, label, _) in enumerate(edges, start=1):
            note = f" / {label}" if label else ""
            rows.append(
                f"""
                <div class="mobile-step" data-step="{index}">
                  <b>{escape(nodes.get(frm, frm))} -> {escape(nodes.get(to, to))}</b>
                  <p>{inline(note.strip(" /") or "结构依赖 / 数据流向")}</p>
                </div>
                """
            )
    if not rows:
        rows.append(
            """
            <div class="mobile-loop">
              <b>架构图</b>
              <p>该视图保留 Mermaid 源码，可在桌面宽度查看完整图形。</p>
            </div>
            """
        )
    return '<div class="diagram-mobile">' + "".join(rows) + "</div>"


def architecture_html(project: dict) -> str:
    architecture = project.get("architecture")
    if not architecture:
        return ""
    decision_items = [
        ("项目复杂性评估", architecture["complexity"]),
        ("选用框架", architecture["framework"]),
        ("裁剪策略", architecture["tailoring"]),
        ("省略内容", architecture["omitted"]),
    ]
    decision = "".join(
        f'<div class="arch-kv"><b>{escape(label)}</b><span>{inline(value)}</span></div>'
        for label, value in decision_items
    )
    blocks = []
    for index, view in enumerate(architecture["views"], start=1):
        scenario = view.get("scenario")
        scenario_html = f'<p><strong>场景描述：</strong>{inline(scenario)}</p>' if scenario else ""
        priority = '<span class="priority-badge">Priority Interaction</span>' if view.get("priority") else ""
        visual = architecture_mermaid_visual(view)
        mobile_visual = architecture_mermaid_mobile(view["mermaid"])
        source = (
            '<details class="arch-source"><summary>Mermaid 源码</summary>'
            f'<pre class="mermaid-block"><code>{escape(view["mermaid"])}</code></pre></details>'
        )
        blocks.append(
            f"""
            <article class="arch-view">
              <div class="arch-view-head">
                <div>
                  <h4>{index}. {escape(view['title'])}</h4>
                  <div class="arch-view-meta">
                    <span><strong>视图类型：</strong>{inline(view['view_type'])}</span>
                  </div>
                </div>
                {priority}
              </div>
              <div class="arch-view-body">
                {scenario_html}
                <p>{inline(view['description'])}</p>
                {visual}
                {mobile_visual}
                {source}
              </div>
            </article>
            """
        )
    return f"""
    <div class="arch-lens">
      <div class="arch-head">
        <span class="arch-kicker">Adaptive Architecture Lens</span>
        <h3>{escape(architecture.get('label', '自适应架构视角'))}</h3>
        <div class="arch-reason">先做复杂度评估，再选择 C4 或 4+1；无论框架如何，核心业务交互图优先。</div>
      </div>
      <div class="arch-decision">{decision}</div>
      <div class="arch-views">{''.join(blocks)}</div>
    </div>
    """


def assets_html(project: dict) -> str:
    return '<div class="asset-grid">' + "".join(
        f'<div class="asset"><h3>{escape(title)}</h3><p>{inline(body)}</p></div>'
        for title, body in project["key_assets"]
    ) + "</div>"


def adoption_html(project: dict) -> str:
    return f"""
    <div class="two-col">
      <div class="check-card"><h3>采用前确认</h3>{bullets(project['adoption'])}</div>
      <div class="evidence-card"><h3>DeepWiki / 证据边界</h3>{bullets(project['deepwiki'] + project['evidence'], compact=True)}</div>
    </div>
    """


def section(idx: str, anchor: str, title: str, note: str, body: str) -> str:
    return f"""
    <section id="{anchor}" class="section">
      <div class="section-head">
        <div class="section-index">{idx}</div>
        <h2>{title}</h2>
        <p class="section-note">{note}</p>
      </div>
      <div class="section-body">{body}</div>
    </section>
    """


def report_sections(project: dict) -> list[tuple[str, str, str, str, str]]:
    sections = [
        ("lean", "Lean 判断", "新用户先看什么", "保留精益创业视角：适合谁、问题、差异、时机和最小验证。", lean_html(project)),
        ("demo", "Demo", "Gold Example / Demo", "优先使用真实项目图片或仓库 example；未运行时明确标注静态推演。", demo_html(project)),
    ]
    diagram = diagram_html(project)
    if diagram:
        sections.append((
            "diagram",
            "机制图",
            "项目机制图",
            "图表是可选组件；只在 UML / 系统动力学等表达方式能带来解释增益时使用。",
            diagram,
        ))
    architecture = architecture_html(project)
    if architecture:
        sections.append((
            "views",
            "架构视角",
            project.get("architecture", {}).get("label", "自适应架构视角"),
            "先判断复杂度，再裁剪 C4 / 4+1 / UML 组合；核心业务交互图必须优先。",
            architecture,
        ))
    sections.extend([
        ("assets", "资产", "核心资产与价值", "只保留新用户和技术评估者需要理解的关键资产。", assets_html(project)),
        ("adopt", "采用确认", "采用前确认与证据边界", "风险和工程化信息只保留会影响试用/采用决策的部分。", adoption_html(project)),
    ])
    return sections


def page(project: dict) -> str:
    sections = report_sections(project)
    nav = "".join(f'<a href="#{escape(anchor)}">{escape(nav_label)}</a>' for anchor, nav_label, _, _, _ in sections)
    section_html = "".join(
        section(f"{index:02d}", anchor, title, note, body)
        for index, (anchor, _, title, note, body) in enumerate(sections, start=1)
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <title>{escape(project['title'])} 项目洞察</title>
  <style>{STYLE}</style>
</head>
<body>
<main class="page">
  <div class="topline"><span class="brand">Project Insight</span><span>Lean · 自适应架构视角 · 图型按需选择 · 静态分析</span></div>
  <article aria-label="{escape(project['title'])} 项目洞察">
    <header class="hero">
      <div class="hero-main">
        <div class="eyebrow">{escape(project['url'])}</div>
        <h1 class="title">{escape(project['title'])}</h1>
        {bullets(project['summary']).replace('class="bullets"', 'class="summary"')}
        {resource_links(project)}
      </div>
      <aside class="adoption">
        <div>
          <div class="adoption-label">Adoption Read</div>
          <div class="adoption-title">{escape(project['adoption_label'])}</div>
          <p class="adoption-detail">{inline(project['adoption_detail'])}</p>
        </div>
        <div class="tags">{tags(project)}</div>
      </aside>
    </header>
    <section class="facts">{facts(project)}</section>
    <nav class="nav">
      {nav}
    </nav>
    {section_html}
    <footer class="footer">
      <div><strong>生成文件：</strong>site/projects/{escape(project['slug'])}/index.html</div>
      <div><strong>边界：</strong>静态分析，未真实运行目标项目。</div>
    </footer>
  </article>
</main>
<script>{INTERACTION_SCRIPT}</script>
</body>
</html>"""


def strip_md(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text).replace("`", "")


def markdown_report(project: dict) -> str:
    lines = [
        f"# {project['title']} 项目洞察报告",
        "",
        f"- URL：{project['url']}",
        f"- 采用判断：{project['adoption_label']}",
        f"- 判断说明：{strip_md(project['adoption_detail'])}",
        f"- 分析方式：{project.get('analysis_mode', '静态分析，DeepWiki 仅作辅助理解')}",
        "",
        "## 1. 新用户先看什么",
        "",
    ]
    for label, items in project["lean"].items():
        lines += [f"### {label}", *[f"- {strip_md(x)}" for x in items], ""]
    lines += [
        "## 2. Gold Example / Demo",
        "",
        f"- 示例：{project['demo']['title']}",
        f"- 来源：{project['demo']['source_label']}",
        "- Demo 状态：静态推演，未运行",
        *[f"- {strip_md(x)}" for x in project["demo"]["points"]],
        "",
        "## 3. 项目机制图",
        "",
        f"- 图型选择：{', '.join(project['diagrams']['selected_types'])}",
        f"- 选择理由：{project['diagrams']['reason']}",
        f"- 场景：{project['diagrams']['scenario']}",
    ]
    lines += [f"- {a} -> {b}：{strip_md(c)}；{strip_md(d)}" for a, b, c, d in project["diagrams"]["sequence"]]
    if project.get("architecture"):
        architecture = project["architecture"]
        lines += [
            "",
            f"## 4. {architecture.get('label', '自适应架构视角')}",
            "",
            f"- 项目复杂性评估结果：{architecture['complexity']}",
            f"- 选用的架构描述框架：{architecture['framework']}",
            f"- 裁剪策略理由：{strip_md(architecture['tailoring'])}",
            f"- 省略内容：{strip_md(architecture['omitted'])}",
            "",
        ]
        for view in architecture["views"]:
            marker = " -> PRIORITY" if view.get("priority") else ""
            lines += [
                f"### {view['title']}{marker}",
                "",
                f"- 视图类型：{view['view_type']}",
            ]
            if view.get("scenario"):
                lines.append(f"- 场景描述：{strip_md(view['scenario'])}")
            lines += [
                f"- 说明：{strip_md(view['description'])}",
                "",
                "```mermaid",
                view["mermaid"],
                "```",
                "",
            ]
        next_index = 5
    else:
        lines += ["", "## 4. 架构视角取舍", "", "- 未使用架构视角：该项目更适合用行为流程、分发格式和示例来解释；强行套 C4/4+1 会偏空。"]
        next_index = 5
    lines += ["", f"## {next_index}. 核心资产与价值", ""]
    lines += [f"- {a}：{strip_md(b)}" for a, b in project["key_assets"]]
    lines += ["", f"## {next_index + 1}. 采用前确认", ""]
    lines += [f"- {strip_md(x)}" for x in project["adoption"]]
    lines += ["", "## 证据与边界", ""]
    lines += [f"- {strip_md(x)}" for x in project["deepwiki"] + project["evidence"]]
    lines.append("")
    return "\n".join(lines)


def copy_assets() -> None:
    for project in PROJECTS:
        media = project["media"]
        if media.get("kind") != "image":
            continue
        src = ROOT / media["source"]
        dst = PROJECTS_DIR / project["slug"] / "assets" / media["asset"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists() and src.resolve() != dst.resolve():
            shutil.copyfile(src, dst)


def cleanup_old_secondary_pages() -> None:
    if not SITE_DIR.exists():
        return
    old_pattern = "*-" + "info" + "graphic.html"
    for old in SITE_DIR.glob(old_pattern):
        old.unlink()


def clean_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def main() -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    cleanup_old_secondary_pages()
    copy_assets()
    for project in PROJECTS:
        out = PROJECTS_DIR / project["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(clean_output(page(project)), encoding="utf-8")
        (out / "analysis.md").write_text(clean_output(markdown_report(project)), encoding="utf-8")


if __name__ == "__main__":
    main()
