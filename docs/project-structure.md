# 项目结构说明

## 根目录

- `README.md`：项目入口、复现、验证、发布和打包命令。
- `.gitignore`：忽略本地缓存、打包产物、临时材料和密钥文件。
- `.github/workflows/pages.yml`：GitHub Pages 发布 workflow。

## 静态站点

- `site/index.html`：项目洞察总览。
- `site/projects.json`：项目清单和索引数据源。
- `site/projects/<slug>/index.html`：项目 HTML 报告。
- `site/projects/<slug>/analysis.md`：项目 Markdown 审计版。
- `site/projects/<slug>/assets/`：项目自己的图片或媒体资产。
- `site/.nojekyll`：禁用 Jekyll 处理，保持静态文件原样发布。

## 可复现材料

- `tools/generate_final_insight_reports.py`：生成前三个项目报告。
- `tools/generate_gbrain_insight_report.py`：生成 GBrain 报告。
- `tools/generate_project_index.py`：根据 `site/projects.json` 生成站点入口。
- `tools/project_report_manager.py`：检查、注册项目并同步更新索引。
- `tools/verify_reports.js`：Playwright 页面验证脚本。
- `.agents/skills/project-insight-analysis/`：可复用项目分析 skill。

## 文档

- `docs/requirements.md`：用户要求整理。
- `docs/final-execution-report.md`：执行记录。
- `docs/methodology/`：方法框架、报告模板、质量检查清单。
- `docs/reference/`：早期输入草稿、建模风格和 UI 参考。
- `docs/archive/skill-calibration/`：skill 一致性校准材料。
- `docs/cleanup-log.md`：目录整理和归档记录。

## 本地归档与产物

- `temp/`：源码快照、旧版本、浏览器产物、缓存和零散材料，仅本地保留。
- `dist/`：本地 zip 包，可再生成，不进入 Git。

## 根目录不应再出现

- `analysis_html_final/`
- `assets/`
- `method/`
- `reports/`
- `skills/`
- `.playwright-cli/`
- `tools/__pycache__/`
