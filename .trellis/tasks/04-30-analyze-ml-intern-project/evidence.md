# Evidence Log: huggingface/ml-intern

Analysis date: 2026-04-30
Mode: Static analysis only, project not run
Repository: https://github.com/huggingface/ml-intern
Inspected commit: `5db99fadaf6ef578a02c3692e7845c1c3855b0e5`

## Repo Metadata

- Type: public GitHub repository owned by `huggingface`.
- GitHub description: "ml-intern: an open-source ML engineer that reads papers, trains models, and ships ML models".
- API snapshot on 2026-04-30: created `2025-10-30T13:43:09Z`, updated `2026-04-30T08:58:21Z`, pushed `2026-04-30T08:51:03Z`.
- API snapshot on 2026-04-30: 7,575 stars, 735 forks, 68 open issues, primary language Python.
- API snapshot on 2026-04-30: `license: null`; no `LICENSE` file was found in the cloned tree.
- Releases and tags API returned empty lists.
- Local clone summary: 161 tracked files; 97 Python files, 20 TypeScript files, 19 TSX files; roughly 42,608 lines across selected source, config, docs, and lock files.

## README / Docs Evidence

- README states the core value proposition: an ML intern that autonomously researches, writes, and ships ML-related code with access to Hugging Face docs, papers, datasets, and cloud compute.
  Source: `README.md:5-7`, GitHub view: https://github.com/huggingface/ml-intern/blob/5db99fadaf6ef578a02c3692e7845c1c3855b0e5/README.md#L5-L7
- README installation uses `uv sync` and `uv tool install -e .`, then exposes `ml-intern` globally.
  Source: `README.md:13-24`.
- README requires or prompts for provider and platform credentials: Anthropic, OpenAI, HF token, and GitHub token.
  Source: `README.md:26-34`.
- README supports interactive mode, headless mode, model selection, max iterations, and no-stream mode.
  Source: `README.md:36-57`.
- README documents one-way Slack notification gateways for approvals, errors, and turn completion.
  Source: `README.md:59-107`.
- README architecture diagram describes `submission_loop`, `Handlers.run_agent`, `Session`, `ContextManager`, `ToolRouter`, doom-loop detection, LLM calls, approval checks, tool execution, and repeated tool-call iteration.
  Source: `README.md:109-215`.
- README event list includes processing, streaming, tool call/output, approval, compacted, interrupted, turn complete, and shutdown states.
  Source: `README.md:217-236`.
- README says MCP servers are configured through `configs/cli_agent_config.json` or `configs/frontend_agent_config.json`, with env substitution.
  Source: `README.md:263-283`.

## Runtime / Code Evidence

- Python packaging defines the CLI entrypoint `ml-intern = "agent.main:cli"`, Python `>=3.11`, and dependencies including LiteLLM, Hugging Face Hub, FastMCP, FastAPI, APScheduler, and PyMongo.
  Source: `pyproject.toml:1-31`, `pyproject.toml:54-81`.
- Package data explicitly includes config JSON and prompt YAML to avoid broken installed CLI/headless behavior.
  Source: `pyproject.toml:61-75`.
- CLI and frontend configs both save sessions to `smolagents/ml-intern-sessions`, connect to `https://huggingface.co/mcp?login`, and require confirmation for CPU jobs.
  Source: `configs/cli_agent_config.json:1-19`, `configs/frontend_agent_config.json:1-14`.
- The main system prompt forces a literature-first ML workflow, current API research, dataset/model validation, Trackio monitoring, HF Jobs pre-flight checks, one-job-first batch discipline, sandbox-first development, and non-silent failure handling.
  Source: `agent/prompts/system_prompt_v3.yaml:1-198`.
- `ToolRouter` registers built-in tools for research, HF docs, HF papers, web search, dataset inspection, planning, notification, HF Jobs, HF repo file/git operations, GitHub examples/repos/files, and sandbox/local tools.
  Source: `agent/core/tools.py:17-54`, `agent/core/tools.py:284-390`.
- MCP tool registration skips conflicting/disallowed HF tools including `hf_jobs`, `hf_doc_search`, `hf_doc_fetch`, and `hf_whoami`.
  Source: `agent/core/tools.py:67`, `agent/core/tools.py:155-174`.
- Agent loop handles context compaction, doom-loop detection, malformed tool recovery, streaming and non-streaming LLM calls, JSON tool-argument validation, parallel execution of non-approval tools, approval-required tool batching, and turn-complete/error/interrupted events.
  Source: `agent/core/agent_loop.py:830-1248`.
- Approval is required for sandbox creation, GPU/CPU HF Jobs depending config, repo uploads/deletes, private repo operations, and destructive HF repo git actions.
  Source: `agent/core/agent_loop.py:80-147`.
- Sandbox tools expose `sandbox_create`, `bash`, `read`, `write`, and `edit`; sandbox auto-creation requires an HF token and includes stale sandbox cleanup logic.
  Source: `agent/tools/sandbox_tool.py:1-10`, `agent/tools/sandbox_tool.py:159-260`.
- HF Jobs tool exposes CPU/GPU hardware flavors, default agent-friendly env vars, token propagation, uv command wrapping, and hf-transfer dependency injection.
  Source: `agent/tools/jobs_tool.py:1-220`.
- FastAPI backend starts session manager and KPI scheduler, flushes active sessions on shutdown, mounts routers, and serves static frontend files when present.
  Source: `backend/main.py:29-114`.
- Web agent routes expose session create, restore summary, model switching, notification destinations, quota, jobs access, submit, approval, SSE chat, pro-click telemetry, and reconnectable event streams.
  Source: `backend/routes/agent.py:80-180`, `backend/routes/agent.py:330-760`.
- Premium models are gated to HF org membership and daily quota is charged on message submit, not session creation.
  Source: `backend/routes/agent.py:108-167`, `backend/routes/agent.py:543-640`.
- Session persistence is optional: no-op without MongoDB, Mongo-backed with session/message/event/trace indexes, quota counters, and pro-conversion tracking when configured.
  Source: `agent/core/session_persistence.py:1-170`, `agent/core/session_persistence.py:360-489`.
- Frontend SSE transport parses event IDs/data, maps backend events to Vercel AI SDK UI chunks, handles approvals, quota exhaustion, billing-required states, and stream reconnection through `/api/events/{session_id}`.
  Source: `frontend/src/lib/sse-chat-transport.ts:1-454`.

## Quality / CI Evidence

- Tests found: 26 files under `tests/`, with 259 test definitions or pytest references by rough grep count.
- Test areas include model gating, KPI rollups, config, malformed tool calls, doom-loop detection, heartbeat, HF access, LLM params, messaging, sandbox auth, session persistence, SFT tagging, user quotas, and web search.
- GitHub workflows run Claude PR review on `pull_request_target` with trusted base checkout and Claude-on-mention automation.
  Source: `.github/workflows/claude-review.yml`, `.github/workflows/claude.yml`.
- `REVIEW.md` defines high-rigor review rules, priority labels, P0 investigation requirements, P1 caps, and line-citation expectations for behavior claims.
  Source: `REVIEW.md`.

## Evidence Boundary

- Static analysis did not execute `uv sync`, `ml-intern`, tests, frontend build, FastAPI server, HF OAuth, HF Jobs, HF sandboxes, Slack notifications, MongoDB persistence, or model-provider calls.
- GitHub API metadata may change after 2026-04-30; numbers in this report are a snapshot, not a durable benchmark.
- The repository has no detected license file and GitHub API reported no license. This is an adoption blocker for redistribution or commercial use until clarified.
- Product readiness is inferred from code, docs, tests, and recent commits; no live production SLA, deployed Space URL, or maintainer roadmap was verified.
