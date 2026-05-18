# OpenHuman Evidence Notes

- Project: `tinyhumansai/openhuman`
- URL: https://github.com/tinyhumansai/openhuman
- Analysis date: 2026-05-18
- Analysis mode: static repository analysis plus Zread clue verification
- Runtime boundary: not run locally; no install, login, OAuth, desktop build, network tracing, or E2E execution was performed.
- Sampled branch: GitHub default branch `main`
- Sampled manifest version: `0.53.49`

## repo-meta

- GitHub API on 2026-05-18: `tinyhumansai/openhuman`, description "Your Personal AI super intelligence. Private, Simple and extremely powerful.", primary language Rust, license GPL-3.0, default branch `main`.
- GitHub API counts at sampling time: 14,011 stars, 1,200 forks, 116 open issues.
- GitHub API timestamps: created `2026-02-18T20:01:27Z`, updated `2026-05-18T04:36:13Z`, pushed `2026-05-18T03:30:59Z`.

## external-guide

- Zread overview surfaced five high-signal leads: `context first, conversation second`, Memory Tree mechanics, Intelligence Layer, Controller System, and CEF webview scanners.
- Zread claim accepted after verification: Memory Tree ingests connected integrations into local SQLite/Obsidian structures; README and memory README support this.
- Zread claim accepted after verification: Controller System is transport-agnostic; `src/core/mod.rs`, `src/core/all.rs`, and `src/core/dispatch.rs` support this.
- Zread claim accepted after verification: CEF scanner direction avoids new JS injection for migrated providers; `CLAUDE.md` supports this.
- Zread claim corrected: it describes a sidecar core and React 18. Current `CLAUDE.md` says sidecar was removed and core is linked in-process; `app/package.json` uses React `^19.1.0`.

## README/docs

- `README.md` positions OpenHuman as an early-beta, open-source personal AI assistant with desktop app, mascot, 118+ integrations, memory tree, Obsidian wiki, native voice, model routing, local AI via Ollama, and TokenJuice compression.
- `README.md` states every active connection is walked every twenty minutes and pulled into the memory tree.
- `README.md` states connected data is canonicalized into `<=3k-token` Markdown chunks, scored, and folded into hierarchical summary trees stored in SQLite and an Obsidian-compatible vault.
- `README.md` frames the thesis as getting context in minutes rather than weeks, with one sync pass giving compressed context of inbox, calendar, repos, docs, and messages.
- `README.md` install path points to hosted downloads and shell installers for macOS/Linux and Windows.
- `README.md` contributor path requires Node.js 24+, pnpm 10.10.0, Rust 1.93.0, CMake, Ninja, ripgrep, and desktop build prerequisites.
- `CLAUDE.md` documents shipped product scope as desktop only and says core runs in-process inside the Tauri host as a tokio task; there is no sidecar binary anymore.
- `CLAUDE.md` says frontend RPC still goes over HTTP through `core_rpc_relay` and `core_rpc` to local `http://127.0.0.1:<port>/rpc`, authenticated with `OPENHUMAN_CORE_TOKEN`.
- `CLAUDE.md` says the QuickJS / `rquickjs` skills runtime was removed; `src/openhuman/skills/` is now metadata-only.
- `CLAUDE.md` says migrated provider webviews must not grow new JavaScript injection; scraping and observability run natively through CDP in provider scanner modules.
- `gitbooks/features/privacy-and-security.md` claims local Memory Tree SQLite and Obsidian vault, backend-brokered LLM/OAuth/search/TTS, OS keychain storage, TLS, short-lived tokens, and no training on user data.
- `gitbooks/features/privacy-and-security.md` states auto-fetch is bound by OAuth scope, provider sync interval, and daily budget; revoked connections stop syncing but existing local chunks remain.
- `gitbooks/features/token-compression.md` documents TokenJuice as a rule overlay that compacts verbose tool output before it enters LLM context, with builtin/user/project rule layers.
- `gitbooks/features/token-compression.md` describes the operational path as classify output, match the applicable compression rule, then reduce the verbose result before LLM context construction.
- `gitbooks/features/mascot/meeting-agents.md` documents a meeting agent that joins Google Meet as a real participant, listens through streaming STT, diarizes and postprocesses transcript, folds meeting content into Memory Tree under people/topics/project, speaks through TTS injected as outbound mic feed, and exposes mascot canvas/lip-sync/listening/thinking poses as outbound camera.
- `gitbooks/features/mascot/meeting-agents.md` names implementation areas including `src/openhuman/meet_agent/brain.rs`, `src/openhuman/voice/`, `app/src/features/meet/MascotFrameProducer.tsx`, `mascot_native_window.rs`, and a Meet child webview with no injected JS.
- Some GitBook architecture pages appear older than `CLAUDE.md`; they mention sidecar and QuickJS runtime. Current-source claims in this report prefer `CLAUDE.md` and code.

## code

- `Cargo.toml` root defines package `openhuman` version `0.53.49`, `openhuman-core` binary, and dependencies for HTTP, async runtime, SQLite, encryption, Sentry, Socket.IO, speech/audio, OS automation, optional channels, and test dependencies.
- `app/package.json` defines `openhuman-app` version `0.53.49`, Node `>=24.0.0`, React `^19.1.0`, Vite, Tauri 2.10, Redux Toolkit, Socket.IO client, Three.js, Remotion, Sentry, Vitest, WDIO/Appium tooling.
- `app/package.json` has `core:stage` as a no-op message saying core is linked in-process and sidecar removed.
- `src/core/mod.rs` defines `ControllerSchema`, `FieldSchema`, and `TypeSchema` as shared transport-agnostic controller contracts.
- `src/core/all.rs` centralizes registry and dispatch logic for controllers, provides `RegisteredController`, `ControllerHandler`, `schema_for_rpc_method`, validation, internal-only controllers, and domain aggregation.
- `src/core/dispatch.rs` routes calls through core methods, registered domain controllers, then legacy domain dispatcher, and validates params against controller schema.
- `src/openhuman/memory/README.md` documents `UnifiedMemory` over SQLite, FTS5, vector tables, graph tables, document ingestion, tree retrieval, canonicalization, chunker/content store, score/retrieval, tree_source/tree_topic/tree_global, and background seals/summaries.
- `src/openhuman/agent/README.md` documents the agent domain as owning LLM tool loop, sub-agent dispatch, conversation transcripts, trigger triage, and prompt assets.
- `src/openhuman/skills/README.md` documents skill discovery, parsing, injection, scope precedence, trust markers, resource bounds, and metadata-only skill behavior.
- `src/openhuman/channels/README.md` documents Slack, Discord, Telegram, WhatsApp, IRC, Matrix, Signal, iMessage, Email, Lark, Mattermost, DingTalk, QQ, Linq, Web, and CLI channels.

## config

- `.github/workflows/test-reusable.yml` runs frontend coverage, `cargo test -p openhuman`, and `cargo test --manifest-path app/src-tauri/Cargo.toml` in a pinned CI image.
- `.github/workflows/test.yml` delegates PR/push tests to `test-reusable.yml`.
- `.github/workflows/pr-quality.yml` contains PR checklist, coverage matrix sync, and markdown link checks.
- `docs/TEST-COVERAGE-MATRIX.md` maps product features to Rust unit/integration, Vitest, WDIO E2E, and manual smoke coverage; it explicitly lists multiple missing/partial areas.
- `CLAUDE.md` documents coverage requirement of at least 80% on changed lines and detailed debug runners.

## license

- `LICENSE` and GitHub API identify GPL-3.0.

## static-inference

- Adoption stance: promising but not low-risk; the repo is large, fast-moving, early beta, and uses nontrivial desktop/runtime dependencies. Best evaluated through a contained desktop trial, not by embedding into critical personal data workflows immediately.
- Differentiation inference: the most distinctive bundle is context-first personal agent + local Memory Tree/Obsidian vault + auto-fetch + ControllerSchema contract + TokenJuice/model routing/background tasks + native desktop/webview integration + mascot/meeting/voice participation in live workflows.
- Risk inference: privacy claims depend on exact backend boundaries, OAuth proxy behavior, telemetry defaults, local retrieval path, and model context sent to providers; these need runtime and network verification beyond static docs.
- Execution risk inference: CEF/Tauri, Rust 1.93, Node 24, OAuth providers, local AI, speech/audio, OS permissions, webview scanners, and optional channels create a high setup/debug surface for contributors and self-hosters.
