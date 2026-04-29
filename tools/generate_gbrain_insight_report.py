from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tools.generate_final_insight_reports as gen  # noqa: E402


def gbrain_media_html(project: dict) -> str:
    media = project["media"]
    if media.get("kind") != "gbrain_demo":
        return ORIGINAL_MEDIA_HTML(project)
    return f"""
    <div class="example-card">
      <div class="example-row"><b>本地启动</b><p><code>gbrain init</code> 建本地 PGLite brain；<code>gbrain import ~/notes/</code> 导入 Markdown。</p></div>
      <div class="example-row"><b>用户问题</b><p>“Prep me for my meeting with Jordan in 30 minutes”</p></div>
      <div class="example-row good"><b>brain-first</b><p><code>gbrain query</code> 先查个人知识库，再结合 typed links / timeline 组织上下文。</p></div>
      <div class="example-row"><b>写回复利</b><p><code>put_page</code> 写入新事实；auto-link、citation 和维护任务让下一次查询更好。</p></div>
      <div class="media-caption">{gen.inline(media['caption'])}</div>
    </div>
    """


ORIGINAL_MEDIA_HTML = gen.media_html
gen.media_html = gbrain_media_html


def semantic_gbrain_context_svg(title: str) -> str:
    parts = gen.arch_svg_canvas(title, 460)
    gen.arch_box(parts, 60, 190, 155, 70, "Human / Agent", "asks / observes")
    gen.arch_box(parts, 275, 160, 190, 100, "GBrain Surface", "CLI + MCP + skills", fill="#e8f4f2", stroke="#8ac7bd")
    gen.arch_box(parts, 535, 160, 210, 100, "Operations Contract", "single source of truth", fill="#17202b", stroke="#17202b", title_fill="#ffffff")
    gen.arch_box(parts, 835, 95, 210, 72, "PGLite", "local zero-config")
    gen.arch_box(parts, 835, 245, 210, 72, "Postgres + pgvector", "Supabase / self-hosted")
    gen.arch_box(parts, 275, 330, 190, 62, "29 Skills", "resolver + workflows")
    gen.arch_box(parts, 535, 330, 210, 62, "Minions / Cron", "durable jobs")
    gen.arch_arrow(parts, 215, 225, 275, 210, "task")
    gen.arch_arrow(parts, 465, 210, 535, 210, "tool call")
    gen.arch_arrow(parts, 745, 192, 835, 131, "engine")
    gen.arch_arrow(parts, 745, 228, 835, 281, "scale path")
    gen.arch_arrow(parts, 370, 330, 370, 260, "route", color="#0f766e", marker="arrow-teal")
    gen.arch_arrow(parts, 640, 330, 640, 260, "background", color="#0f766e", marker="arrow-teal")
    parts.append("</svg>")
    return gen.diagram_svg_shell("\n".join(parts), "系统全貌图突出 GBrain 的真实边界：agent-facing CLI/MCP/skills 通过统一 operations contract 访问本地或远程 brain engine。")


def semantic_gbrain_static_svg(title: str) -> str:
    parts = gen.arch_svg_canvas(title, 470)
    parts.append('<rect x="55" y="88" width="1070" height="330" rx="14" fill="#fbfcfb" stroke="#cfd8d3"/>')
    gen.arch_box(parts, 95, 155, 175, 66, "src/cli.ts", "trusted local caller")
    gen.arch_box(parts, 95, 275, 175, 66, "src/mcp/server.ts", "remote/untrusted")
    gen.arch_box(parts, 330, 210, 205, 86, "operations.ts", "41+ shared ops", fill="#17202b", stroke="#17202b", title_fill="#ffffff")
    gen.arch_box(parts, 600, 130, 190, 62, "BrainEngine", "interface")
    gen.arch_box(parts, 600, 225, 190, 62, "hybrid search", "keyword + vector + RRF")
    gen.arch_box(parts, 600, 320, 190, 62, "link extraction", "typed edges / timeline")
    gen.arch_box(parts, 860, 130, 190, 62, "PGLiteEngine", "embedded Postgres")
    gen.arch_box(parts, 860, 225, 190, 62, "PostgresEngine", "pgvector / Supabase")
    gen.arch_box(parts, 860, 320, 190, 62, "skills + jobs", "resolver / minions")
    gen.arch_arrow(parts, 270, 188, 330, 237, "local")
    gen.arch_arrow(parts, 270, 308, 330, 263, "remote")
    gen.arch_arrow(parts, 535, 252, 600, 161, "engine")
    gen.arch_arrow(parts, 535, 252, 600, 256, "query")
    gen.arch_arrow(parts, 535, 252, 600, 351, "write hook")
    gen.arch_arrow(parts, 790, 161, 860, 161)
    gen.arch_arrow(parts, 790, 256, 860, 256)
    gen.arch_arrow(parts, 790, 351, 860, 351)
    parts.append("</svg>")
    return gen.diagram_svg_shell("\n".join(parts), "静态组织图把接口、契约、引擎、搜索/图谱能力和 skill/job 层分开，避免把它讲成单一 RAG 脚本。")


def semantic_gbrain_deployment_svg(title: str) -> str:
    parts = gen.arch_svg_canvas(title, 430)
    parts.append('<rect x="65" y="102" width="465" height="245" rx="14" fill="#fbfcfb" stroke="#cfd8d3"/>')
    gen.svg_text("Local-first path", 92, 130, 24, size=14, weight=900, fill="#0f766e", anchor="start")
    gen.arch_box(parts, 105, 165, 170, 62, "Developer machine", "Bun + CLI")
    gen.arch_box(parts, 310, 165, 170, 62, "PGLite file", "~/.gbrain")
    gen.arch_box(parts, 200, 265, 180, 58, "Markdown repo", "source of truth")
    parts.append('<rect x="635" y="102" width="480" height="245" rx="14" fill="#fbfcfb" stroke="#cfd8d3"/>')
    gen.svg_text("Remote MCP path", 662, 130, 24, size=14, weight=900, fill="#0f766e", anchor="start")
    gen.arch_box(parts, 675, 165, 170, 62, "AI Client", "Claude / Cursor")
    gen.arch_box(parts, 875, 165, 185, 62, "gbrain serve", "HTTP wrapper / stdio")
    gen.arch_box(parts, 875, 265, 185, 58, "Supabase Postgres", "pgvector")
    gen.arch_arrow(parts, 275, 196, 310, 196, "local")
    gen.arch_arrow(parts, 295, 265, 295, 227, "import")
    gen.arch_arrow(parts, 845, 196, 875, 196, "MCP")
    gen.arch_arrow(parts, 967, 227, 967, 265, "DB")
    gen.arch_arrow(parts, 745, 227, 875, 296, "trust boundary", color="#a66f12", marker="arrow-amber", dashed=True)
    parts.append("</svg>")
    return gen.diagram_svg_shell("\n".join(parts), "部署视图区分本地 PGLite 试用路径和远程 MCP/Supabase 路径；采用风险主要出现在远程访问、凭据和多设备同步。")


gen.SEMANTIC_ARCH_RENDERERS.update({
    "gbrain_context": semantic_gbrain_context_svg,
    "gbrain_static": semantic_gbrain_static_svg,
    "gbrain_deployment": semantic_gbrain_deployment_svg,
})


PROJECT = {
    "slug": "gbrain",
    "title": "GBrain",
    "url": "https://github.com/garrytan/gbrain",
    "adoption_label": "适合 agent-heavy 团队试点",
    "adoption_detail": "适合已经有 Markdown 知识库、MCP/CLI agent 工作流和长期记忆痛点的个人或小团队；正式托管前要验证隐私、迁移、远程 MCP 权限和数据库运维。",
    "summary": [
        "GBrain 是 **个人知识脑 + agent skillpack + CLI/MCP 工具层**，目标是让 agent 在会话之外持续积累可检索、可链接、可维护的上下文。",
        "它不是普通向量库 wrapper；真正差异在 **operations contract、BrainEngine 抽象、typed links/timeline、29 个 skills 和 Minions job queue** 的组合。",
    ],
    "lean": {
        "适合谁": [
            "已经用 Claude Code、OpenClaw、Hermes、Cursor 或自建 MCP agent 的重度用户。",
            "有 Markdown/Obsidian/Notion/会议/邮件/网页等长期知识资产，希望 agent 能跨任务复用的人。",
            "愿意让 agent 参与安装、导入、维护和定期任务的小团队或个人研究者。",
        ],
        "解决什么问题": [
            "通用 coding/chat agent 会忘记历史上下文，下一次任务仍要重新喂资料。",
            "纯向量搜索很难回答关系型问题，例如谁和谁一起出现、某家公司和某人有什么关系。",
            "知识库会随时间变脏：引用、反链、孤儿页面、迁移和 cron 任务都需要持续维护。",
        ],
        "和别的方案哪里不同": [
            "它把 **CLI/MCP operations、pluggable engine、graph/timeline extraction 和 skill workflows** 合在一起，而不是只做一层 RAG。",
            "默认本地 PGLite 两秒可起步，同时保留 Postgres + pgvector / Supabase 的规模化路径。",
            "仓库把 agent 操作协议写进 `AGENTS.md`、`CLAUDE.md`、`skills/RESOLVER.md`，把“人读文档”改成“agent 按协议执行”。",
        ],
        "为什么现在值得看": [
            "MCP 和 agent skill 正在成为工具接入层，GBrain 正好把个人知识库包装成 agent 可操作的工具表面。",
            "仓库更新很活跃：GitHub API 显示 2026-04-28 仍有 push，版本为 `0.22.6.1`。",
            "README 给出生产使用数据和 BrainBench 结果，但这些是项目方声明，采用前仍需复现实验。",
        ],
        "最小验证方式": [
            "不要先上远程 MCP；本地 `bun install && bun link` 后用 PGLite 跑 `gbrain init`。",
            "导入 20-50 篇自己的 Markdown，跑 `gbrain query`、`gbrain graph-query`、`gbrain stats`，观察是否真的回答出关系型问题。",
            "再打开 MCP，仅暴露低风险目录，验证 `OperationContext.remote` 对 `file_upload` 等敏感操作的约束。",
        ],
    },
    "facts": [
        ("11,973", "GitHub stars；1,458 forks；GitHub API 采样于 2026-04-28。"),
        ("29 skills", "`skills/RESOLVER.md` 调度 brain/query/ingest/enrich/minion 等工作流。"),
        ("190 tests", "`test/` 下约 190 个测试文件；CI 运行 gitleaks 与 `bun run test`。"),
    ],
    "tags": [("agent memory", "green"), ("CLI/MCP", "blue"), ("隐私需验证", "red")],
    "media": {
        "kind": "gbrain_demo",
        "caption": "该 demo 来自 README 的 CLI 查询示例和会议准备场景，是静态推演，未真实运行 GBrain。",
    },
    "demo": {
        "title": "会议前上下文准备：从问题到 brain-first 回答",
        "source_label": "README CLI / meeting 示例 + 静态推演，未运行",
        "points": [
            "用户问：`Prep me for my meeting with Jordan in 30 minutes`。",
            "Agent 先按 `skills/RESOLVER.md` 选择 query / brain-ops，而不是直接上网或凭记忆回答。",
            "`query` 通过 operations contract 调用 hybrid search、typed links 和 timeline，拉出相关人、公司、过往会议和 open threads。",
            "若产生新事实，`put_page` 写回页面并触发 auto-link / citation 维护，让下一次查询更好。",
        ],
    },
    "diagrams": {
        "selected_types": ["UML Sequence", "UML Component", "CLD / SFD"],
        "mixed": True,
        "reason": "GBrain 的关键是 read-enrich-write 循环如何把 agent 请求、skill 路由、operations contract、engine/search/graph 和写回维护串成一个会复利的系统。",
        "scenario": "用户要求 agent 准备一次会议，agent 需要先查 brain，再把新信息写回。",
        "sequence": [
            ("用户 / Agent", "Skill Resolver", "提出会议准备或知识查询", "根据触发词选择 query / brain-ops"),
            ("Skill Resolver", "Brain Ops / Query Skill", "读取对应 skill", "执行 brain-first 流程"),
            ("Brain Ops / Query Skill", "Operations Contract", "调用 query / get_page / put_page", "CLI 与 MCP 共用同一契约"),
            ("Operations Contract", "BrainEngine", "hybrid search + graph/timeline", "抽象 PGLite/Postgres"),
            ("BrainEngine", "PGLite / Postgres", "keyword/vector/link 查询", "返回页面、chunks、typed edges"),
            ("Operations Contract", "Brain Pages", "写回引用、反链、timeline", "下一轮查询获得更多上下文"),
        ],
        "components": [
            ("skills/RESOLVER.md", "把自然语言任务分派到 29 个 skill。"),
            ("src/core/operations.ts", "CLI、MCP 和工具 JSON 的单一契约源。"),
            ("BrainEngine", "统一 PGLite 与 Postgres/pgvector 的存储与搜索能力。"),
            ("hybrid search + graph", "把 keyword、vector、RRF、typed links 和 timeline 合并为查询能力。"),
            ("Minions / Cron", "让批量导入、维护和长任务可持久运行。"),
        ],
        "system": [
            {
                "kind": "R",
                "title": "记忆复利回路",
                "items": ["更多信号进入", "页面/实体增加", "typed links 与 timeline 更密", "查询质量提升", "用户更愿意让 agent 先查 brain"],
            },
            {
                "kind": "B",
                "title": "安全与运维控制回路",
                "items": ["远程 MCP / cron 扩大", "隐私和迁移风险上升", "trust boundary / doctor / tests 介入", "试点范围回到可控"],
            },
        ],
    },
    "architecture": {
        "label": "自适应架构视角",
        "complexity": "复杂 / 异构",
        "framework": "4+1 理论裁剪 + C4/UML 表达",
        "tailoring": "项目横跨 CLI、MCP、skillpack、pluggable database engine、hybrid search、graph/timeline、Minions job queue 和远程 trust boundary。使用 4+1 作为分类，但只保留场景、过程、开发/实现和部署边界。",
        "omitted": "不单独输出抽象 Logical 文字卡；逻辑对象已合并到系统全貌、核心交互和静态组织图中。未画完整 cron/voice/webhook 生态，避免把 README 声明当成已验证部署。",
        "views": [
            {
                "title": "系统全貌",
                "view_type": "场景视图(+1) / C4 L1 Context",
                "visual_kind": "gbrain_context",
                "description": "系统边界是 agent-facing CLI/MCP/skills 到 operations contract，再到本地 PGLite 或远程 Postgres brain engine。",
                "mermaid": """flowchart LR
    User[Human or Agent] --> Surface[GBrain CLI / MCP / Skills]
    Skills[29 Skills + Resolver] --> Surface
    Surface --> Ops[Operations Contract]
    Ops --> Engine[BrainEngine]
    Engine --> PGLite[PGLite Local Brain]
    Engine --> Postgres[Postgres + pgvector]
    Ops --> Jobs[Minions / Cron Jobs]""",
            },
            {
                "title": "核心业务流转",
                "view_type": "Process View / UML Sequence",
                "priority": True,
                "scenario": "用户要求 agent 准备一次会议或回答跨页面知识问题。",
                "description": "重点是一次请求如何先查 brain、合成回答，再通过写回和 auto-link 让后续查询变好。",
                "mermaid": """sequenceDiagram
    autonumber
    actor U as User
    participant A as Agent
    participant R as Skill Resolver
    participant O as Operations Contract
    participant E as BrainEngine
    participant DB as PGLite or Postgres
    participant W as Brain Pages
    U->>A: Prep me for my meeting
    A->>R: choose query / brain-ops skill
    R->>O: call query / get_page
    O->>E: hybrid search + graph traversal
    E->>DB: keyword, vector, links, timeline
    DB-->>E: pages, chunks, typed edges
    E-->>A: cited context
    A->>O: put_page with new facts
    O->>W: write citations, backlinks, timeline""",
            },
            {
                "title": "静态组织结构",
                "view_type": "Development / Implementation View with C4 L2",
                "visual_kind": "gbrain_static",
                "description": "静态结构展示开发边界：CLI/MCP 表面、operations contract、engine/search/link extraction、skills 和 jobs。",
                "mermaid": """flowchart TB
    CLI[src/cli.ts trusted CLI] --> Ops[src/core/operations.ts]
    MCP[src/mcp/server.ts remote MCP] --> Ops
    Ops --> Engine[BrainEngine Interface]
    Engine --> PGLite[PGLiteEngine]
    Engine --> PG[PostgresEngine]
    Ops --> Search[hybrid search / RRF]
    Ops --> Links[link extraction / timeline]
    Resolver[skills/RESOLVER.md] --> CLI
    Resolver --> MCP
    Jobs[Minions / Cron] --> Ops""",
            },
            {
                "title": "部署 / 信任边界",
                "view_type": "C4 Deployment",
                "visual_kind": "gbrain_deployment",
                "description": "最小试点用本地 PGLite；远程 MCP 和 Supabase/Postgres 才需要额外审权限、凭据、RLS、备份和访问边界。",
                "mermaid": """flowchart TB
    subgraph Local[Local-first path]
      Dev[Developer Machine] --> CLI[gbrain CLI]
      CLI --> File[PGLite ~/.gbrain]
      Repo[Markdown Repo] --> CLI
    end
    subgraph Remote[Remote MCP path]
      Client[AI Client] --> Server[gbrain serve / HTTP wrapper]
      Server --> PG[Supabase Postgres + pgvector]
    end
    Server -.remote trust boundary.-> PG""",
            },
        ],
    },
    "key_assets": [
        ("`src/core/operations.ts`", "CLI、MCP、工具定义和 mutating/read 操作共享的契约层，是可维护性的核心。"),
        ("`BrainEngine` + engines", "PGLite 本地零配置和 Postgres/pgvector 规模化路径共用接口，减少后续迁移成本。"),
        ("`hybrid.ts` + graph/timeline", "keyword、vector、RRF、source boost、typed links 和 timeline 共同支撑非纯语义检索问题。"),
        ("`skills/RESOLVER.md` + 29 skills", "把 agent 行为、导入、查询、维护、skillify、minions 等流程显式化。"),
        ("测试与 CI", "`test/` 约 190 个测试文件，CI 跑 gitleaks 与 `bun run test`，比普通个人工具更重视回归。"),
    ],
    "adoption": [
        "先本地 PGLite 试点，不要一开始开放远程 MCP 或接真实隐私数据。",
        "用自己的 20-50 篇 Markdown 做最小集，验证 query、graph-query、stats、links/timeline 是否真实增益。",
        "再验证敏感路径：`file_upload` confinement、remote=true 行为、MCP token/HTTP wrapper、Supabase 备份和 RLS。",
        "对 README 的生产数字和 BrainBench 结论保持关注，但采用前应在自己的 corpus 上复现检索质量。",
    ],
    "deepwiki": ["本轮未使用 DeepWiki 作为主要来源；以 GitHub API、README、AGENTS/CLAUDE、源码、docs、CI 和测试目录为静态证据。"],
    "evidence": [
        "GitHub API：`garrytan/gbrain`，TypeScript，MIT，stars 11,973，forks 1,458，open issues 303，最近 push 2026-04-28。",
        "`README.md` 描述 29 skills、30+ MCP tools、PGLite/Postgres、BrainBench 和生产脑数据；这些生产数字未在本地复现。",
        "`AGENTS.md` 明确安装流程、read order、trust boundary 和 before shipping 流程。",
        "`CLAUDE.md` 与 `docs/ENGINES.md` 支撑 BrainEngine、PGLite/Postgres、operations contract 和测试体系判断。",
        "`src/core/operations.ts`、`src/mcp/server.ts`、`src/core/engine.ts`、`src/core/search/hybrid.ts`、`skills/RESOLVER.md` 支撑架构判断。",
        "未真实运行 `bun install`、`gbrain init`、MCP server、PGLite/Postgres 或 BrainBench；本报告为静态分析，未真实运行目标项目。",
    ],
}


def main() -> None:
    gen.SITE_DIR.mkdir(parents=True, exist_ok=True)
    gen.PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    out = gen.PROJECTS_DIR / "gbrain"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(gen.page(PROJECT), encoding="utf-8")
    (out / "analysis.md").write_text(gen.markdown_report(PROJECT), encoding="utf-8")


if __name__ == "__main__":
    main()
