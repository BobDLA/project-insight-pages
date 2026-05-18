# OpenViking evidence log

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
