# Project Insight Static Site

本仓库用于生成、维护和发布项目洞察分析页。最终页面保存在 `site/`，可通过 GitHub Pages 静态托管。

## 目录

- `site/index.html`：项目洞察总览入口。
- `site/projects.json`：项目清单；新增项目时更新这里。
- `site/projects/<slug>/index.html`：单个项目 HTML 报告。
- `site/projects/<slug>/analysis.md`：单个项目 Markdown 审计版。
- `.agents/skills/project-insight-analysis/`：项目级 agent skill。
- `tools/`：报告生成、索引生成、验证和项目注册脚本。
- `docs/methodology/`：分析框架、报告模板和质量清单。
- `docs/reference/`：早期输入材料、建模样例和 UI 参考。
- `docs/archive/`：校准记录等归档材料。

`temp/` 和 `dist/` 是本地工作产物，不进入 Git。

## 本地预览

```bash
python3 -m http.server 8765
```

打开：

```text
http://localhost:8765/site/
```

## 重新生成

```bash
python3 -m py_compile \
  tools/generate_final_insight_reports.py \
  tools/generate_gbrain_insight_report.py \
  tools/generate_project_index.py \
  tools/project_report_manager.py

python3 tools/generate_final_insight_reports.py
python3 tools/generate_gbrain_insight_report.py
python3 tools/generate_project_index.py
```

## 新增项目

先检查是否已经分析过：

```bash
python3 tools/project_report_manager.py check https://github.com/owner/repo
```

未分析时，用 `.agents/skills/project-insight-analysis/` 的流程生成项目 HTML 与 Markdown，然后注册：

```bash
python3 tools/project_report_manager.py register \
  --repo https://github.com/owner/repo \
  --category "API / Tool" \
  --adoption "适合本地试点" \
  --audience "目标用户" \
  --problem "解决的问题" \
  --difference "差异点" \
  --demo "核心 demo 或机制" \
  --architecture "架构表达" \
  --html path/to/report.html \
  --markdown path/to/analysis.md \
  --tags "tag1,tag2"
```

注册会复制报告到 `site/projects/<slug>/`，更新 `site/projects.json`，并重建 `site/index.html`。

## 验证

```bash
python3 .agents/skills/project-insight-analysis/scripts/validate_report.py \
  site/projects/free-claude-code/analysis.md \
  site/projects/FinceptTerminal/analysis.md \
  site/projects/andrej-karpathy-skills/analysis.md \
  site/projects/gbrain/analysis.md \
  site/projects/free-claude-code/index.html \
  site/projects/FinceptTerminal/index.html \
  site/projects/andrej-karpathy-skills/index.html \
  site/projects/gbrain/index.html \
  --json
```

浏览器验证：

```bash
mkdir -p temp/verification/playwright
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
bash "$PWCLI" open http://localhost:8765/site/
bash "$PWCLI" run-code --filename tools/verify_reports.js --json
```

## 发布

仓库包含 `.github/workflows/pages.yml`。推送到 GitHub 后，在仓库设置中启用 GitHub Pages 的 GitHub Actions 发布源即可发布 `site/`。

## 打包

`dist/` 不进入 Git。需要本地 zip 时重新生成：

```bash
rm -f dist/project-insight-analysis-skill.zip dist/project-insight-reports.zip
mkdir -p dist
zip -qr dist/project-insight-analysis-skill.zip .agents/skills/project-insight-analysis
zip -qr dist/project-insight-reports.zip README.md docs site tools .github .gitignore
unzip -t dist/project-insight-analysis-skill.zip
unzip -t dist/project-insight-reports.zip
```
