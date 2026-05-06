# neat-freak Evidence Notes

## Sampling

- Target: `https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak`
- Analysis date: 2026-04-30
- Mode: static analysis only
- Local source snapshot: `bf39594` (`bf39594646840bc85368bb40771f3f6ec3fc7503`)
- Repo metadata from GitHub API on 2026-04-30: 7,314 stars, 1,115 forks, MIT license, default branch `main`
- Subdirectory files: `neat-freak/SKILL.md`, `neat-freak/references/agent-paths.md`, `neat-freak/references/sync-matrix.md`
- Runtime boundary: the skill was not installed or executed in Claude Code, Codex, OpenCode, or OpenClaw.

## Evidence Map

| Type | Source | Supports |
| --- | --- | --- |
| README/docs | `README.md:21-24` | Repository positions skills as structured instruction sets following Agent Skills and working across Claude Code, Codex, OpenCode, and OpenClaw. |
| README/docs | `README.md:34`, `README.md:65-99` | `neat-freak` reconciles project docs, root AI instructions, and agent memory after a session; triggers include `/neat`, Chinese phrases, and `sync up`. |
| README/docs | `README.md:46-54` | Installation is by asking an agent to install a skill URL; there is no separate package manager flow. |
| README/docs | `README.md:96-97` | External distribution badges exist for ClawHub and Tessl; treat them as distribution signals, not runtime evidence. |
| skill | `neat-freak/SKILL.md:1-13` | Skill metadata and trigger phrases; cross-platform support claim. |
| skill | `neat-freak/SKILL.md:21-27` | Core stance: act as knowledge-base editor, keep documentation and memory clean, accurate, and newcomer-friendly. |
| skill | `neat-freak/SKILL.md:29-41` | Three knowledge layers: agent memory, root `CLAUDE.md` / `AGENTS.md`, and project `docs/` / `README.md`. |
| skill | `neat-freak/SKILL.md:45-60` | First mandatory step is mechanical inventory of memory, root files, docs, README, and agent configs. |
| skill | `neat-freak/SKILL.md:62-101` | Change impact matrix and real-edit requirement; docs first, then AI root files, then memory. |
| skill | `neat-freak/SKILL.md:103-119` | Self-check checklist and relative-time cleanup requirements. |
| skill | `neat-freak/SKILL.md:121-143` | Expected final summary shape. |
| reference | `neat-freak/references/agent-paths.md:17-29` | Codex path model: no separate memory index, project facts go into `AGENTS.md`; also note fallback guide names. |
| reference | `neat-freak/references/agent-paths.md:30-51` | OpenClaw and OpenCode path behavior; cross-platform installation and scanning differences. |
| reference | `neat-freak/references/sync-matrix.md:5-17` | Code-change to documentation-layer mapping. |
| reference | `neat-freak/references/sync-matrix.md:18-27` | Memory cleanup rules, including absolute dates and removing completed todos. |
| reference | `neat-freak/references/sync-matrix.md:40-49` | Standard documentation update pattern: integration guide, architecture, runbook, handoff/change record. |
| license | `LICENSE` | MIT license. |
| repo-meta | GitHub API | Repo created 2026-04-06, updated 2026-04-30, pushed 2026-04-29; stars/forks/open issues sampled above. |
| static-inference | Local file inventory | No scripts, package manifest, tests, CI, or executable entrypoint in `neat-freak`; evaluate as a documentation/skill/rule-pack project. |

## Derived Links

- GitHub page: `https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak`
- DeepWiki page derived from repo URL: `https://deepwiki.com/KKKKhazix/khazix-skills`
- Zread page derived from repo URL: `https://zread.ai/KKKKhazix/khazix-skills`

## Report Stance

- Adoption stance: useful as an end-of-session knowledge hygiene baseline for active AI-assisted repositories; validate in a low-risk repo before making it team policy.
- Gold Example: constructed from the skill instructions, because the repository provides trigger examples and workflow rules but no recorded run output.
- Diagram choice: rule execution flow + C4-light distribution/context; optional BOT for expected drift reduction, labeled conceptual.
- Risk boundary: the skill can edit docs and memory broadly, so teams should review path inventory, deletion policy, and platform-specific memory behavior before delegating it unattended.
