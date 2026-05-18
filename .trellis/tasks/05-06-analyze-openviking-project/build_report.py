from __future__ import annotations

import shutil
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ROOT = TASK_DIR.parents[2]
sys.path.insert(0, str(ROOT))

from tools.generate_final_insight_reports import clean_output, page

REPO_DIR = TASK_DIR / "repo" / "OpenViking"
ASSET_SOURCE = REPO_DIR / "docs" / "images" / "ov-provenance-example.png"


PROJECT = {
    "slug": "OpenViking",
    "title": "OpenViking",
    "url": "https://github.com/volcengine/OpenViking",
    "analysis_mode": "静态分析；仓库源码、README、docs、CI、license 和 GitHub API 元数据采样；未安装或运行服务。",
    "adoption_label": "适合技术试点；生产采用需审计",
    "adoption_detail": (
        "适合先在低风险 Agent 工作流中验证资源导入、记忆提交、分层检索和可观测性；"
        "生产采用前必须确认 AGPL 边界、模型服务成本、数据隔离、密钥/隐私配置和运维复杂度。"
    ),
    "summary": [
        "OpenViking 把 **资源、记忆、技能和会话历史** 统一进 `viking://` 虚拟文件系统，目标是做 AI Agent 的上下文数据库。",
        "它的差异点不是单纯向量召回，而是 **L0/L1/L2 分层 + 目录递归检索 + 会话记忆迭代 + 插件集成** 的组合。",
    ],
    "lean": {
        "适合谁": [
            "正在构建长任务 AI Agent、编码 Agent、研究 Agent 或企业内部助理的团队。",
            "需要把文档、代码仓库、用户偏好、工具经验和 Agent 技能长期管理起来的平台工程团队。",
            "想研究 context engineering、agentic RAG、记忆生命周期和多租户上下文隔离的技术读者。",
        ],
        "解决什么问题": [
            "Agent 上下文常散落在 prompt、向量库、文件、插件和聊天历史里，缺少统一读写与审计边界。",
            "传统 RAG 往往是平铺 chunk 检索，难以解释“为什么命中这里”，也难以让 Agent 逐层读取细节。",
            "长会话会产生大量可沉淀经验，简单截断或压缩会丢失可复用记忆。",
        ],
        "和别的方案哪里不同": [
            "它把上下文映射到 `viking://resources`、`viking://user/memories`、`viking://agent/skills` 等目录，而不是只暴露向量搜索 API。",
            "写入后异步生成 L0 摘要、L1 overview 和 L2 原文，检索时先定位目录再递归下钻，并保留 retrieval provenance。",
            "项目同时提供 Python SDK、HTTP API、Rust CLI、MCP/WebDAV、Claude Code/OpenClaw/OpenCode 插件、VikingBot 和 Docker/Helm 部署资产。",
        ],
        "为什么现在值得看": [
            "Agent 应用从“单次问答”转向长期任务后，上下文治理、记忆复用和检索可观测性会成为工程瓶颈。",
            "仓库在 2026-05-06 仍非常活跃，最近提交涉及 memory isolation，说明多用户/多 Agent 场景正在快速演进。",
            "它已经把概念文档、API、测试、CI、观测面板、插件示例和发布流程都放进仓库，足够做技术试点评估。",
        ],
        "最小验证方式": [
            "本地或 Docker 启动 server，配置 embedding 与 VLM，先导入一个小型代码仓库或文档目录。",
            "用 `ov ls/tree/find/grep` 或 Python `client.find()` 验证 `viking://` 目录、L0/L1/L2 和检索命中是否可解释。",
            "再接入一个 Claude Code/OpenClaw/OpenCode 低风险会话，验证自动 recall、session commit、memory diff 和隐私边界。",
        ],
    },
    "facts": [
        ("23.5k", "GitHub stars at 2026-05-06 API sample；forks 1.7k，open issues 248。"),
        ("v0.3.13", "Latest GitHub release observed: 2026-04-29；default branch latest clone commit 44d3cc4。"),
        ("AGPL-3.0", "Main project license；Rust crates and examples separately include Apache-2.0 license files。"),
    ],
    "tags": [("Context DB", "green"), ("Agent 记忆", "blue"), ("生产需审计", "red")],
    "media": {
        "kind": "image",
        "source": str(ASSET_SOURCE),
        "asset": "ov-provenance-example.png",
        "caption": (
            "仓库 `docs/images/ov-provenance-example.png` 展示 `include_provenance=True` 时的搜索结果、"
            "searched directories、matched contexts 和 thinking trace；它直接对应 OpenViking 的核心卖点：可解释的上下文检索。"
        ),
    },
    "demo": {
        "title": "导入 OpenViking README 后做可解释检索",
        "source_label": "仓库 `examples/quick_start.py` + README CLI quick start + provenance 示例图；Demo 状态：静态推演，未运行",
        "points": [
            "用 Python SDK 或 `ov add-resource` 导入一个 URL、文件或目录，目标落到 `viking://resources/...`。",
            "ResourceProcessor 解析内容，TreeBuilder 写入 AGFS/RAGFS，SemanticQueue 异步生成 `.abstract.md` 与 `.overview.md` 并写入向量索引。",
            "Agent 用 `find` 做简单语义检索，或用 `search` 结合 session context 生成 typed queries。",
            "检索结果返回 URI、层级、摘要、相关上下文和可选 provenance，Agent 再按需读取 L1/L2 细节。",
        ],
    },
    "diagrams": {
        "selected_types": ["UML Sequence", "UML Component", "CLD", "SFD"],
        "mixed": True,
        "reason": (
            "OpenViking 的关键机制横跨资源导入、语义队列、向量索引、会话记忆和插件消费；"
            "用一次检索任务的 UML 主链路解释执行边界，再用 CLD/SFD 表达上下文积累、信任和风险控制。"
        ),
        "scenario": "Agent 导入一个代码仓库/文档资源，随后在长任务中检索相关上下文并把会话经验沉淀为记忆。",
        "sequence": [
            ("Agent / CLI / Plugin", "ResourceService", "add_resource 或 add_skill", "入口可以是 SDK、HTTP、Rust CLI 或插件"),
            ("ResourceService", "Parser + TreeBuilder", "解析文件/URL/目录并写入 `viking://`", "Parser 不直接调用 LLM，先建立目录树"),
            ("Parser + TreeBuilder", "SemanticQueue", "提交 L0/L1 生成任务", "bottom-up 生成摘要和 overview"),
            ("SemanticQueue", "Vector Index", "embedding + metadata records", "索引保存 URI、向量和摘要，不保存完整文件内容"),
            ("Agent / CLI / Plugin", "SearchService + VikingFS", "find/search 查询", "`search` 可结合 session context 做 intent analysis"),
            ("SearchService + VikingFS", "HierarchicalRetriever", "目录定位 + 递归下钻 + rerank", "返回 matched contexts、relations 和可选 provenance"),
            ("SessionService", "Memory Extractor", "commit 后抽取长期记忆", "异步写入 user/agent memory 并记录 memory diff"),
        ],
        "components": [
            ("FastAPI / SDK / Rust CLI", "统一暴露资源、文件系统、检索、会话、隐私和管理 API。"),
            ("Service Layer", "FS/Search/Resource/Session/Pack/Debug 等业务服务复用同一 VikingFS。"),
            ("Parser + TreeBuilder", "把文档、代码、媒体、URL 和目录转成 `viking://` 层级树。"),
            ("SemanticQueue", "异步生成 L0/L1，控制 VLM/embedding 并发并写入索引。"),
            ("VikingFS", "URI 规范、读写、关系、访问控制、加密透明化和向量同步的核心边界。"),
            ("RAGFS + VectorDB", "内容存储和语义索引分离，支持 local/S3/memory 与 local/http/VikingDB。"),
            ("Retriever + IntentAnalyzer", "find/search 的语义召回、typed queries、递归检索和 rerank。"),
            ("Agent Integrations", "Claude Code、OpenClaw、OpenCode、MCP、VikingBot 等消费同一上下文能力。"),
        ],
        "system": [
            {
                "kind": "R",
                "title": "上下文质量增强回路",
                "items": ["统一导入资源/记忆/技能", "L0/L1/L2 可导航", "检索结果更可解释", "Agent 任务成功率提高", "更多上下文被沉淀"],
            },
            {
                "kind": "B",
                "title": "生产采用约束回路",
                "items": ["上下文变敏感", "多租户/密钥/隐私风险上升", "启用鉴权/加密/审计", "部署边界收紧"],
            },
            {
                "kind": "SFD",
                "title": "上下文库存量",
                "items": ["导入文档/会话/技能", "检索与读取", "L0/L1/L2 上下文库存", "过期、删除或再索引"],
            },
        ],
    },
    "architecture": {
        "label": "4+1 裁剪的上下文数据库架构视角",
        "complexity": "高：Python 服务、Rust CLI/RAGFS、C++ 扩展、向量索引、异步队列、插件、Bot、Docker/Helm、多租户/加密/观测同时存在。",
        "framework": "4+1 作为判断框架，具体图用 C4 L1/L2、UML Sequence 和 Deployment flowchart 表达。",
        "tailoring": (
            "完整 4+1 会过重；本报告保留 Scenario、Process、Development/Implementation 和 Deployment/Physical。"
            "Logical view 合并到 C4 容器/组件图中，重点解释上下文写入、检索、记忆和部署边界。"
        ),
        "omitted": "未画数据库 ERD 和每个 API router 细节；静态分析无法确认真实运行性能、模型调用质量和云端商业服务边界。",
        "views": [
            {
                "title": "系统全貌",
                "view_type": "C4 L1 Context / Scenario View",
                "description": "OpenViking 位于 Agent runtime 与模型/存储基础设施之间，向 CLI、SDK、HTTP、MCP、WebDAV 和插件提供同一套上下文数据库能力。",
                "mermaid": """flowchart LR
    Agent[Agent Runtime / Developer] --> SDK[Python SDK / Rust CLI / Plugins]
    SDK --> API[OpenViking HTTP API or Embedded Client]
    API --> Service[OpenViking Service Layer]
    Service --> Model[VLM / Embedding / Rerank Providers]
    Service --> Storage[RAGFS Content Store + Vector Index]
    Service --> Obs[Observer / Metrics / Grafana]
    Service --> Admin[Auth / Multi-tenant / Privacy / Encryption]""",
            },
            {
                "title": "核心业务流转",
                "view_type": "UML Sequence / Process View",
                "priority": True,
                "scenario": "导入资源后，Agent 在一次任务中检索上下文并在 commit 时沉淀长期记忆。",
                "description": "这个视图展示最关键的行为链：资源写入先形成层级目录，再异步生成语义层；检索时先定位目录，再递归下钻；会话 commit 另走记忆抽取链路。",
                "mermaid": """sequenceDiagram
    autonumber
    participant A as Agent or CLI
    participant R as ResourceService
    participant P as Parser and TreeBuilder
    participant Q as SemanticQueue
    participant V as VikingFS and Vector Index
    participant S as SearchService
    participant H as HierarchicalRetriever
    participant M as Session Memory Extractor
    A->>R: add_resource(URL/file/directory)
    R->>P: parse and build viking:// tree
    P->>Q: enqueue L0/L1 generation
    Q->>V: write abstracts, overviews, vectors
    A->>S: find/search query
    S->>H: typed query + target scopes
    H->>V: global search then recursive directory search
    V-->>A: matched contexts + URI + provenance
    A->>M: session.commit()
    M->>V: write user/agent memories and memory_diff""",
            },
            {
                "title": "静态组织结构",
                "view_type": "Development / Implementation View",
                "description": "源码组织显示这是一个多语言系统：Python 负责服务和业务层，Rust 负责 CLI/RAGFS，C++ 扩展承担底层索引/能力探测，Bot 和插件负责上层集成。",
                "mermaid": """flowchart LR
    subgraph Python[Python package]
      Server[openviking/server routers]
      Services[openviking/service]
      Parse[openviking/parse]
      Retrieve[openviking/retrieve]
      Storage[openviking/storage]
      Session[openviking/session]
    end
    subgraph Rust[Rust workspace]
      OvCli[crates/ov_cli]
      Ragfs[crates/ragfs]
      RagfsPy[crates/ragfs-python]
    end
    subgraph Native[Native extensions]
      Cpp[src C++ extensions]
    end
    subgraph Integrations[Integrations]
      Examples[examples plugins]
      Bot[VikingBot]
      Docs[docs and console]
    end
    Server --> Services
    Services --> Parse
    Services --> Retrieve
    Services --> Storage
    Storage --> RagfsPy
    RagfsPy --> Ragfs
    OvCli --> Server
    Bot --> Server
    Examples --> Server
    Cpp --> Storage""",
            },
            {
                "title": "部署与运行边界",
                "view_type": "Deployment / Physical View",
                "description": "仓库同时支持 embedded mode、独立 HTTP server、Docker compose、Docker image、Helm 示例和带 VikingBot 的 server；生产关键在模型服务、持久化、密钥和多租户隔离。",
                "mermaid": """flowchart LR
    Local[Embedded Python Process] --> Workspace[Local ~/.openviking workspace]
    Client[SDK / CLI / Plugin] --> Server[openviking-server :1933]
    Server --> Console[Console UI :8020]
    Server --> Bot[VikingBot optional /chat]
    Server --> FS[LocalFS or S3 AGFS]
    Server --> VDB[Local/http/Volcengine VectorDB]
    Server --> Model[Embedding/VLM/Rerank APIs]
    Server --> KMS[Local key / Vault / Volcengine KMS]
    Docker[Docker Compose / Image] --> Server
    Helm[K8s Helm example] --> Server""",
            },
        ],
    },
    "key_assets": [
        ("`viking://` URI 与目录语义", "Context types、Viking URI、FS API 和 namespace 规则让 Agent 像操作文件一样操作上下文。"),
        ("L0/L1/L2 分层处理链", "Parser、TreeBuilder、SemanticQueue 和 `.abstract.md`/`.overview.md` 机制把检索、导航和细读拆开。"),
        ("HierarchicalRetriever", "全局定位、目录递归、score propagation、rerank fallback 和 relations 是区别于平铺 RAG 的核心算法资产。"),
        ("Session memory lifecycle", "commit、archive、memory extraction、dedup decision 和 memory_diff 让会话经验可审计地沉淀。"),
        ("部署与集成资产", "Rust CLI、HTTP API、MCP/WebDAV、Claude Code/OpenClaw/OpenCode 插件、VikingBot、Docker/Helm 降低试点门槛。"),
        ("安全与治理资产", "multi-tenant identity、API key roles、privacy config、envelope encryption、metrics/observer 支撑生产化讨论。"),
    ],
    "adoption": [
        "先把试点范围限定在非敏感仓库或文档，确认导入、分层摘要、检索结果和 provenance 是否符合团队调试习惯。",
        "确认 AGPL-3.0 对服务化部署和二次修改的合规影响；Rust crates/examples 的 Apache-2.0 不能覆盖主项目许可证。",
        "压测模型调用成本与延迟，尤其是 VLM 摘要、embedding、rerank、长会话 commit 和批量资源导入。",
        "生产部署必须配置 root/user key、account/user/agent 边界、加密 provider、日志脱敏、备份和再索引策略。",
        "把插件接入低风险 Agent 后再逐步扩大，不要直接把个人/客户长期记忆导入未审计的共享实例。",
    ],
    "deepwiki": [
        "外部阅读入口按 GitHub URL 派生：DeepWiki https://deepwiki.com/volcengine/OpenViking，Zread https://zread.ai/volcengine/OpenViking。",
        "本报告的判断主要来自本地克隆源码、README/docs、CI、license 和 GitHub API；未把第三方总结当作事实来源。",
    ],
    "evidence": [
        "README 定位为面向 AI Agents 的 Context Database，列出 filesystem paradigm、tiered loading、directory recursive retrieval、visualized trajectory、automatic session management。",
        "`docs/en/concepts/01-architecture.md` 描述 Client、Service、Retrieve、Session、Parse、Compressor、Storage 与 AGFS + Vector Index。",
        "`openviking/service/core.py` 初始化 RAGFS、QueueManager、VikingDBManager、VikingFS、processors、SessionCompressor、WatchScheduler 和各 service。",
        "`openviking/retrieve/hierarchical_retriever.py` 实现全局向量定位、目录递归、score propagation、rerank fallback 和 relation 读取。",
        "`pyproject.toml` 声明 Python 3.10+、FastAPI、OpenTelemetry、tree-sitter、mcp、model provider 依赖和 `ov` / `openviking-server` / `vikingbot` scripts。",
        "未安装依赖、未启动 server、未运行 `ov`、未调用模型服务；性能、召回质量和部署稳定性均为证据边界之外。",
    ],
}


ANALYSIS_MD = f"""# OpenViking 项目洞察报告

## 0. Metadata

- Project: OpenViking
- URL: https://github.com/volcengine/OpenViking
- Analysis date: 2026-05-06
- Analysis mode: 静态分析
- Sampling boundary: README、docs/en、examples、pyproject/Cargo/Docker/CI、核心 Python/Rust 源码、GitHub API 元数据
- Runtime boundary: Demo 状态：静态推演，未运行
- Observed repo state: latest clone commit `44d3cc4` at 2026-05-06T10:45:06+08:00；latest release `v0.3.13` published 2026-04-29

## 1. 新用户先看什么

### 适合谁

- 正在构建长任务 AI Agent、编码 Agent、研究 Agent 或企业内部助理的团队。
- 需要把文档、代码仓库、用户偏好、工具经验和 Agent 技能长期管理起来的平台工程团队。
- 想研究 context engineering、agentic RAG、记忆生命周期和多租户上下文隔离的技术读者。

### 解决什么问题

- Agent 上下文常散落在 prompt、向量库、文件、插件和聊天历史里，缺少统一读写与审计边界。
- 传统 RAG 往往是平铺 chunk 检索，难以解释“为什么命中这里”，也难以让 Agent 逐层读取细节。
- 长会话会产生大量可沉淀经验，简单截断或压缩会丢失可复用记忆。

### 和别的方案哪里不同

- 它把上下文映射到 `viking://resources`、`viking://user/memories`、`viking://agent/skills` 等目录，而不是只暴露向量搜索 API。
- 写入后异步生成 L0 摘要、L1 overview 和 L2 原文，检索时先定位目录再递归下钻，并保留 retrieval provenance。
- 项目同时提供 Python SDK、HTTP API、Rust CLI、MCP/WebDAV、Claude Code/OpenClaw/OpenCode 插件、VikingBot 和 Docker/Helm 部署资产。

### 为什么现在值得看

- Agent 应用从“单次问答”转向长期任务后，上下文治理、记忆复用和检索可观测性会成为工程瓶颈。
- 仓库在 2026-05-06 仍非常活跃，最近提交涉及 memory isolation，说明多用户/多 Agent 场景正在快速演进。
- 它已经把概念文档、API、测试、CI、观测面板、插件示例和发布流程都放进仓库，足够做技术试点评估。

### 最小验证方式

- 本地或 Docker 启动 server，配置 embedding 与 VLM，先导入一个小型代码仓库或文档目录。
- 用 `ov ls/tree/find/grep` 或 Python `client.find()` 验证 `viking://` 目录、L0/L1/L2 和检索命中是否可解释。
- 再接入一个 Claude Code/OpenClaw/OpenCode 低风险会话，验证自动 recall、session commit、memory diff 和隐私边界。

## 2. Gold Example / Demo

- Demo source: `examples/quick_start.py`、README CLI quick start、`docs/images/ov-provenance-example.png`
- Demo status: Demo 状态：静态推演，未运行
- Demo media relevance: provenance 示例图直接展示 Search Results、searched directories、matched contexts 和 thinking trace，能解释“可观测检索轨迹”这一核心价值。
- Why this example matters: 它把 OpenViking 的完整价值链压缩为一个可验证路径：导入资源、等待语义处理、读取 L0/L1、语义检索、查看命中 URI 和 provenance。

Steps:

- 用 Python SDK 或 `ov add-resource` 导入一个 URL、文件或目录，目标落到 `viking://resources/...`。
- ResourceProcessor 解析内容，TreeBuilder 写入 AGFS/RAGFS，SemanticQueue 异步生成 `.abstract.md` 与 `.overview.md` 并写入向量索引。
- Agent 用 `find` 做简单语义检索，或用 `search` 结合 session context 生成 typed queries。
- 检索结果返回 URI、层级、摘要、相关上下文和可选 provenance，Agent 再按需读取 L1/L2 细节。

Boundary:

- 本轮没有安装依赖、没有启动 `openviking-server`、没有调用模型服务，也没有复现实验表格中的 OpenClaw 效果。

## 3. 项目机制图

- 图型选择: UML Sequence, UML Component, CLD, SFD
- 选择理由: OpenViking 的关键机制横跨资源导入、语义队列、向量索引、会话记忆和插件消费；用一次检索任务的 UML 主链路解释执行边界，再用 CLD/SFD 表达上下文积累、信任和风险控制。
- 场景: Agent 导入一个代码仓库/文档资源，随后在长任务中检索相关上下文并把会话经验沉淀为记忆。

```mermaid
sequenceDiagram
    autonumber
    participant A as Agent / CLI / Plugin
    participant R as ResourceService
    participant P as Parser + TreeBuilder
    participant Q as SemanticQueue
    participant V as Vector Index
    participant S as SearchService + VikingFS
    participant H as HierarchicalRetriever
    participant M as Memory Extractor
    A->>R: add_resource or add_skill
    R->>P: parse file / URL / directory into viking:// tree
    P->>Q: enqueue L0/L1 generation
    Q->>V: embedding + metadata records
    A->>S: find/search query
    S->>H: intent + recursive directory retrieval
    H-->>A: matched contexts + URI + provenance
    A->>M: session.commit()
    M->>V: user/agent memories + memory_diff
```

## 4. 架构视角

- 项目复杂性评估结果: 高，包含 Python 服务、Rust CLI/RAGFS、C++ 扩展、向量索引、异步队列、插件、Bot、Docker/Helm、多租户/加密/观测。
- 选用的架构描述框架: 4+1 作为判断框架，具体图用 C4 L1/L2、UML Sequence 和 Deployment flowchart 表达。
- 裁剪策略理由: 完整 4+1 会过重；本报告保留 Scenario、Process、Development/Implementation 和 Deployment/Physical。Logical view 合并到 C4 容器/组件图中。
- 省略内容: 未画数据库 ERD 和每个 API router 细节；静态分析无法确认真实运行性能、模型调用质量和云端商业服务边界。

### 系统全貌

- View type: C4 L1 Context / Scenario View
- Description: OpenViking 位于 Agent runtime 与模型/存储基础设施之间，向 CLI、SDK、HTTP、MCP、WebDAV 和插件提供同一套上下文数据库能力。

```mermaid
{PROJECT["architecture"]["views"][0]["mermaid"]}
```

### 核心业务流转 -> PRIORITY

- View type: UML Sequence / Process View
- Scenario: 导入资源后，Agent 在一次任务中检索上下文并在 commit 时沉淀长期记忆。
- Interaction notes: 资源写入、语义分层、递归检索、会话记忆是 OpenViking 最核心的四段链路。

```mermaid
{PROJECT["architecture"]["views"][1]["mermaid"]}
```

### 静态组织结构

- View type: Development / Implementation View
- Description: 源码组织显示这是多语言系统：Python 负责服务和业务层，Rust 负责 CLI/RAGFS，C++ 扩展承担底层索引/能力探测，Bot 和插件负责上层集成。

```mermaid
{PROJECT["architecture"]["views"][2]["mermaid"]}
```

### Deployment / Physical View

```mermaid
{PROJECT["architecture"]["views"][3]["mermaid"]}
```

## 5. 核心资产与价值

| Asset | Location | Why it matters |
| --- | --- | --- |
| `viking://` URI 与目录语义 | `docs/en/concepts/02-context-types.md`, `03-context-layers.md`, `04-viking-uri.md`, `openviking/storage/viking_fs.py` | 让 Agent 像操作文件一样管理资源、记忆和技能。 |
| L0/L1/L2 分层处理链 | `openviking/parse/`, `openviking/parse/tree_builder.py`, `openviking/storage/queuefs/`, docs concepts | 把检索、导航和细读分开，降低一次性上下文注入成本。 |
| HierarchicalRetriever | `openviking/retrieve/hierarchical_retriever.py` | 支持全局定位、目录递归、score propagation、rerank fallback 和 relations。 |
| Session memory lifecycle | `docs/en/concepts/08-session.md`, `openviking/service/session_service.py`, `openviking/session/` | 把长会话归档、压缩、抽取记忆和 memory_diff 审计串起来。 |
| 部署与集成资产 | `examples/`, `crates/ov_cli/`, `Dockerfile`, `docker-compose.yml`, `deploy/helm`, `bot/` | 降低从本地试点到插件/服务化部署的迁移成本。 |
| 安全与治理资产 | `docs/en/concepts/10-encryption.md`, `11-multi-tenant.md`, `13-privacy.md`, `openviking/server/auth.py` | 支撑多用户、多 Agent 和敏感上下文的生产化讨论。 |

## 6. 采用前确认与证据边界

### 采用前确认

- 先把试点范围限定在非敏感仓库或文档，确认导入、分层摘要、检索结果和 provenance 是否符合团队调试习惯。
- 确认 AGPL-3.0 对服务化部署和二次修改的合规影响；Rust crates/examples 的 Apache-2.0 不能覆盖主项目许可证。
- 压测模型调用成本与延迟，尤其是 VLM 摘要、embedding、rerank、长会话 commit 和批量资源导入。
- 生产部署必须配置 root/user key、account/user/agent 边界、加密 provider、日志脱敏、备份和再索引策略。
- 把插件接入低风险 Agent 后再逐步扩大，不要直接把个人/客户长期记忆导入未审计的共享实例。

### 证据与边界

| Type | Source | Supports |
| --- | --- | --- |
| README/docs | `README.md`, `docs/en/concepts/*.md`, `docs/en/api/01-overview.md` | 项目定位、五个核心概念、API 面、部署模式、检索和 session 机制。 |
| code | `openviking/service/core.py`, `openviking/storage/viking_fs.py`, `openviking/retrieve/hierarchical_retriever.py`, `openviking/server/app.py` | 服务组合、URI 边界、检索实现、FastAPI router 注册和错误 envelope。 |
| config | `pyproject.toml`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/*.yml` | 语言/依赖、CLI/RAGFS workspace、容器部署、CI/发布/测试边界。 |
| repo-meta | GitHub API sampled 2026-05-06 | stars/forks/issues、default branch、release、license、pushed_at。 |
| license | `LICENSE`, `crates/LICENSE`, `examples/LICENSE` | 主项目 AGPL-3.0；crates/examples Apache-2.0。 |
| static-inference | 源码结构和文档交叉判断 | 采用风险、架构复杂度、最小试点路径；未代表真实运行结果。 |
"""


EVIDENCE_MD = """# OpenViking evidence log

Analysis date: 2026-05-06

## Repo metadata

- GitHub API `volcengine/OpenViking`: description says OpenViking is an open-source context database for AI Agents and unifies memory, resources, and skills through a file-system paradigm.
- Created: 2026-01-05T07:11:17Z.
- Updated: 2026-05-06T02:45:13Z.
- Pushed: 2026-05-06T02:45:07Z.
- Default branch: `main`.
- Stars/forks/open issues at sample time: 23,494 / 1,733 / 248.
- Latest release observed: `v0.3.13`, published 2026-04-29T12:11:14Z.
- Local shallow clone latest commit: `44d3cc41b1c999cca2abadc476023226a41af6ef` (`Feat/memory isolation 支持群聊模式 (#1711)`, 2026-05-06T10:45:06+08:00).

## README/docs evidence

- `README.md`: positions OpenViking as a Context Database for AI Agents, with filesystem management paradigm, tiered context loading, directory recursive retrieval, visualized retrieval trajectory, and automatic session management.
- `docs/en/concepts/01-architecture.md`: describes Client, Service, Retrieve, Session, Parse, Compressor, Storage and AGFS + Vector Index.
- `docs/en/concepts/02-context-types.md`: defines Resource, Memory, Skill and their lifecycle/usage.
- `docs/en/concepts/03-context-layers.md`: defines L0 `.abstract.md`, L1 `.overview.md`, and L2 original detail.
- `docs/en/concepts/05-storage.md`: separates AGFS content storage from Vector Index metadata/vector storage.
- `docs/en/concepts/07-retrieval.md`: documents find/search, intent analysis, hierarchical retrieval, rerank and result types.
- `docs/en/concepts/08-session.md`: documents add_message, used, commit, archive, memory extraction and memory_diff.
- `docs/en/concepts/10-encryption.md`: documents transparent at-rest encryption and root/account/file key hierarchy.
- `docs/en/concepts/11-multi-tenant.md`: documents account/user/agent identity boundaries and ROOT/ADMIN/USER roles.
- `docs/en/concepts/13-privacy.md`: documents skill privacy extraction and placeholder restore.
- `docs/en/api/01-overview.md`: documents Embedded, HTTP, CLI modes; response envelopes; endpoint groups including system, resources, filesystem, search, sessions, privacy, admin, WebDAV and VikingBot.

## Code evidence

- `openviking/server/app.py`: creates FastAPI app, initializes OpenVikingService, APIKeyManager, metrics, tracing/logging, task cleanup, MCP session manager, structured error handlers and routers.
- `openviking/service/core.py`: composes FS/Search/Resource/Session/Pack/Debug services and initializes AGFS, QueueManager, VikingDBManager, VikingFS, encryption, directories, processors, SessionCompressor, LockManager and WatchScheduler.
- `openviking/service/resource_service.py`: validates resource scopes, handles add_resource, wait, watch task creation, public remote target guard, and telemetry.
- `openviking/service/search_service.py`: exposes `find` and `search`; `search` can add session context before calling VikingFS.
- `openviking/storage/viking_fs.py`: owns URI normalization/access checks, encryption/decryption, file operations, L0/L1, relations and semantic search.
- `openviking/retrieve/hierarchical_retriever.py`: implements global vector search, starting point merge, initial L2 candidates, recursive directory search, score propagation, rerank fallback, convergence detection and related context reads.
- `openviking/retrieve/intent_analyzer.py`: builds prompt from session summary/recent messages/current query and parses typed query plans.
- `examples/quick_start.py`: demonstrates embedded client initialize, add_resource, ls, glob/read, wait_processed, abstract/overview and find.
- `examples/openclaw-plugin/README.md` and `examples/claude-code-memory-plugin/README.md`: show concrete Agent integration paths and memory/retrieval workflows.

## Config/build evidence

- `pyproject.toml`: Python 3.10+, project scripts `ov`, `openviking`, `openviking-server`, `vikingbot`; dependencies include FastAPI, OpenTelemetry, tree-sitter, model/provider clients, document parsers, `mcp`.
- `Cargo.toml`: Rust workspace contains `crates/ov_cli`, `crates/ragfs`, `crates/ragfs-python`.
- `Dockerfile`: multi-stage build with Rust toolchain, uv Python builder, ragfs-python maturin build, runtime exposes 1933 and 8020.
- `docker-compose.yml`: runs `ghcr.io/volcengine/openviking:latest`, maps 1933/8020 and mounts `~/.openviking`.
- `.github/workflows`: includes PR checks, main checks, CodeQL, build/release/publish, Docker build, docs, API effect tests and full/lite tests.
- Test file count sampled with `find tests -name 'test_*.py'`: 356.

## License evidence

- `LICENSE`: GNU Affero General Public License v3 for main project.
- `crates/LICENSE`: Apache License 2.0.
- `examples/LICENSE`: Apache License 2.0.
- README states main project AGPLv3, crates/ov_cli Apache 2.0, examples Apache 2.0, third_party respective original licenses. The local file observed is `crates/LICENSE`, not `crates/ov_cli/LICENSE`.

## Runtime boundary

- Static analysis only.
- The project was not installed.
- `openviking-server`, `ov`, Docker, examples, tests and model calls were not run.
- Retrieval quality, latency, cost, memory extraction quality, multi-tenant isolation and production operability remain adoption-validation items.
"""


def main() -> None:
    assets_dir = TASK_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ASSET_SOURCE, assets_dir / "ov-provenance-example.png")

    (TASK_DIR / "report.html").write_text(clean_output(page(PROJECT)), encoding="utf-8")
    (TASK_DIR / "analysis.md").write_text(clean_output(ANALYSIS_MD), encoding="utf-8")
    (TASK_DIR / "evidence.md").write_text(clean_output(EVIDENCE_MD), encoding="utf-8")


if __name__ == "__main__":
    main()
