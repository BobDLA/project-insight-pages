# Claude Context Evidence

## Metadata

| Field | Evidence |
| --- | --- |
| Repository | `https://github.com/zilliztech/claude-context` |
| Local clone | `/tmp/claude-context-analysis` |
| Default branch | `master` |
| HEAD | `367546904b5bcd1d7138a6ae5ca253c8cb0680a1` |
| HEAD message | `feat: deduplicate overlapping search results (#333)` |
| Latest tag / npm package version checked | `v0.1.11`; `@zilliz/claude-context-core` and `@zilliz/claude-context-mcp` latest are `0.1.11` |
| Analysis date | 2026-04-30 |
| Runtime boundary | Static analysis only; no MCP server or indexing run |

## Repository Metadata

- `gh repo view zilliztech/claude-context` returned TypeScript as primary language, MIT License, default branch `master`, about 10,349 stars, 766 forks, 68 open issues, created 2025-06-06, updated 2026-04-30, pushed 2026-04-29.
- Topics include `mcp`, `semantic-search`, `vector-database`, `claude-code`, `cursor`, `vscode-extension`, `agentic-rag`, `merkle-tree`, `gemini-cli`.
- The latest commit adds overlap deduplication for search results and inclusive line-range handling.

## README / Docs Evidence

- `README.md` positions the project as an MCP plugin that adds semantic code search to Claude Code and other AI coding agents.
- `README.md` states the target value: codebase context without loading whole directories into the LLM every request.
- Quick start flow: configure MCP with `npx @zilliz/claude-context-mcp@latest`, set embedding/vector DB credentials, ask the agent to index, check status, then ask natural-language code questions.
- The README lists MCP tools: `index_codebase`, `search_code`, `clear_index`, `get_indexing_status`.
- `docs/getting-started/environment-variables.md` documents process env > `~/.context/.env` > defaults, plus `HYBRID_MODE`, `EMBEDDING_BATCH_SIZE`, custom extensions and ignore patterns.
- `docs/dive-deep/asynchronous-indexing-workflow.md` states indexing starts immediately, runs in the background, progress is persisted under `~/.context/mcp-codebase-snapshot.json`, and search can return partial results while indexing.
- `docs/dive-deep/file-inclusion-rules.md` describes file selection as supported extensions minus ignore patterns, combining defaults, tool parameters, environment variables, root ignore files, and global `.contextignore`.
- `evaluation/README.md` reports a controlled evaluation on 30 SWE-bench Verified instances: comparable F1 with about 39.4% fewer tokens and 36.3% fewer tool calls. The report treats this as project-supplied evidence, not independently reproduced evidence.

## Code Evidence

- `packages/mcp/src/index.ts`
  - Redirects `console.log` and `console.warn` to stderr before MCP startup to avoid corrupting stdio JSON.
  - Uses `@modelcontextprotocol/sdk` with `StdioServerTransport`.
  - Exposes four MCP tools and their schemas.
  - Initializes embedding provider, `MilvusVectorDatabase`, `Context`, `SnapshotManager`, `SyncManager`, and `ToolHandlers`.
  - Runs `validateLegacyZeroEntries()` before accepting requests.
- `packages/mcp/src/handlers.ts`
  - Validates absolute paths and directories.
  - Starts background indexing and returns immediately.
  - Saves status transitions into snapshot state.
  - Allows search during indexing with an incomplete-results warning.
  - Guards collection limit errors and snapshot/cloud divergence.
- `packages/mcp/src/snapshot.ts`
  - Stores v2 snapshot state with `indexed`, `indexing`, and `indexfailed`.
  - Converts interrupted indexing to `indexfailed`.
  - Refuses to persist the known-bad `0 files / 0 chunks / completed` state.
  - Uses a file lock and read-merge behavior for snapshot writes.
- `packages/mcp/src/sync.ts`
  - Runs periodic background sync every five minutes.
  - Supports a trigger file watcher at `~/.context/.sync-trigger`.
  - Uses a global cross-process lock at `~/.context/mcp-sync.lock`.
- `packages/core/src/context.ts`
  - Defaults to AST splitter with 2500 chunk size and 300 overlap.
  - Defaults `HYBRID_MODE` to true.
  - Builds collection names from absolute path hash, with optional sanitized readable prefix.
  - Indexes supported file extensions, applies ignore patterns, chunks files, embeds in batches, and writes to vector DB.
  - Caps indexing at 450,000 chunks with `limit_reached`.
  - Runs hybrid search using dense vector + sparse text request and RRF reranking, or dense-only search when hybrid mode is disabled.
  - Deduplicates same-file overlapping line ranges before returning search results.
- `packages/core/src/splitter/ast-splitter.ts`
  - Uses Tree-sitter parsers for JavaScript, TypeScript, Python, Java, C/C++, Go, Rust, C#, Scala.
  - Falls back to LangChain splitter when AST parsing fails or a language is unsupported.
- `packages/core/src/sync/synchronizer.ts` and `packages/core/src/sync/merkle.ts`
  - Hash files with SHA-256.
  - Persist Merkle snapshots under `~/.context/merkle/`.
  - Detect added, removed, and modified files for incremental re-indexing.
- `packages/core/src/vectordb/milvus-vectordb.ts`
  - Creates regular or hybrid Milvus collections.
  - Hybrid mode uses dense `vector`, sparse `sparse_vector`, BM25 function over `content`, and RRF reranking.
  - Loads collections and waits for indexes before querying.
- `packages/mcp/src/embedding.ts` and `packages/core/src/embedding/*`
  - Support OpenAI, VoyageAI, Gemini, Ollama, and OpenRouter-compatible embeddings in MCP config.

## Config / CI / Release Evidence

- Root `package.json`: monorepo version `0.1.11`, Node `>=20.0.0`, pnpm `>=10.0.0`, scripts for build, dev, lint, typecheck, release, and benchmark.
- `pnpm-workspace.yaml`: packages under `packages/*` and `examples/*`.
- `packages/core/package.json`: npm package `@zilliz/claude-context-core`, Jest test script, Milvus SDK, LangChain, Tree-sitter parsers, embedding SDK dependencies.
- `packages/mcp/package.json`: npm package `@zilliz/claude-context-mcp`, ESM, binary entry, node test runner for `src/**/*.test.ts`.
- `packages/vscode-extension/package.json`: VS Code extension `semanticcodesearch`, commands for search, index, clear, webview, auto-sync settings.
- `packages/chrome-extension/package.json` and README: private Chrome extension package; Chrome Web Store marked “Coming Soon”.
- `.github/workflows/ci.yml`: build matrix for Ubuntu and Windows across Node 20, 22, 24; lint step is commented out; build outputs are verified.
- `.github/workflows/release.yml`: tag-triggered release publishes core, MCP, and VS Code extension.
- Test files observed: `packages/core/src/context.ignore-patterns.test.ts` and `packages/mcp/src/snapshot.request-options.test.ts`.

## License Evidence

- `LICENSE`: MIT License, copyright Zilliz 2025.

## Static Inferences

- Adoption fit is strongest for teams already using Claude Code/Cursor/Gemini CLI-style agent workflows and willing to operate Milvus/Zilliz plus embedding credentials.
- It is not a zero-dependency local search tool by default; external embedding and vector DB setup are part of the product surface, though Ollama/local embedding is supported.
- The implementation includes meaningful production hardening around MCP stdio, background indexing, snapshot poisoning, and cross-process sync, but the automated quality gate is still mostly build-oriented and does not run lint by default.
- The project-supplied evaluation is useful for a first hypothesis, but an adopting team should reproduce it on its own codebase because exact results depend on embedding model, vector DB latency, chunking, and task distribution.
