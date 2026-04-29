# 目录整理记录

整理时间：2026-04-28

## 稳定资产抽取

| 来源 | 目标 | 原因 |
| --- | --- | --- |
| `sources/free-claude-code/pic.png` | `site/projects/free-claude-code/assets/free-claude-code-demo.png` | 让生成器不依赖源码快照目录。 |
| `sources/FinceptTerminal/images/EquityResearch.png` | `site/projects/FinceptTerminal/assets/fincept-equity-research.png` | 让生成器不依赖源码快照目录。 |

## 移入 `docs/reference/`

| 原路径 | 新路径 | 原因 |
| --- | --- | --- |
| `rules.md` | `docs/reference/rules.md` | 早期规则草稿，保留为设计来源。 |
| `lean.md` | `docs/reference/lean.md` | 早期 Lean 材料，保留为设计来源。 |
| `demo.md` | `docs/reference/demo.md` | 早期 Demo 材料，保留为设计来源。 |
| `4+1.md` | `docs/reference/4+1.md` | 早期架构视角材料，保留为设计来源。 |
| `image.md` | `docs/reference/image.md` | 混合建模风格参考，保留为设计来源。 |
| `项目洞察分析方案.md` | `docs/reference/项目洞察分析方案.md` | 初始方案文档，保留为设计来源。 |

## 移入 `temp/`

| 原路径 | 新路径 | 原因 |
| --- | --- | --- |
| `sources/` | `temp/source-repos/` | 目标项目源码快照较大，归档后根目录更清晰。 |
| `analysis_html/` | `temp/old-iterations/analysis_html/` | 旧版 HTML 输出。 |
| `reports/v1/` | `temp/old-iterations/reports/v1/` | 旧版迭代报告。 |
| `reports/v2/` | `temp/old-iterations/reports/v2/` | 旧版迭代报告。 |
| `.playwright-cli/` | `temp/browser-artifacts/playwright-cli/` | 浏览器调试快照和截图。 |
| `output/` | `temp/browser-artifacts/output/` | 历史验证截图和旧脚本。 |
| `tools/__pycache__/` | `temp/cache/tools__pycache__/` | Python 缓存，可再生成。 |
| `download.png` | `temp/misc/download.png` | 零散图片，不属于最终交付。 |
| `REPORT_QUALITY_FIX.md` | `temp/old-iterations/docs/REPORT_QUALITY_FIX.md` | 迭代质量修正记录，内容已被最终方法文档、要求整理和执行报告吸收。 |
| `skill(1).zip` 解包副本 | `temp/skill-audit/` | 用于审计外部 skill 版本，吸收可执行校验脚本思路后归档。原 zip 保持不动。 |

## 当前稳定结构

- `site/`：GitHub Pages 发布目录，包含总览、项目页、Markdown 报告和项目资产。
- `.agents/skills/project-insight-analysis/`：项目级可复用 skill。
- `tools/`：生成、注册和验证脚本。
- `docs/`：需求、执行报告、目录说明、方法论、参考材料和归档。
- `README.md`：根目录唯一说明入口。

## 忽略的本地产物

- `temp/`：源码快照、旧版本、截图、缓存和零散材料。
- `dist/`：可再生成 zip 包。
