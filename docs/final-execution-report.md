# 最终执行报告

## 当前状态

本项目已整理为可提交 Git、可通过 GitHub Pages 发布的静态项目洞察站点。

- 静态页面根目录为 `site/`。
- 每个项目独立目录：`site/projects/<slug>/`。
- Markdown 审计版与 HTML 报告同目录保存。
- 项目级 skill 位于 `.agents/skills/project-insight-analysis/`。
- `temp/` 和 `dist/` 作为本地产物忽略，不进入 Git。

## 已完成的结构调整

1. `analysis_html_final/` 已改为 `site/`。
2. 旧的根级页面已迁移为：
   - `site/projects/free-claude-code/index.html`
   - `site/projects/FinceptTerminal/index.html`
   - `site/projects/andrej-karpathy-skills/index.html`
   - `site/projects/gbrain/index.html`
3. 项目 Markdown 报告已迁移到对应项目目录的 `analysis.md`。
4. 项目图片资产已迁入对应项目目录的 `assets/`。
5. `method/` 已改为 `docs/methodology/`。
6. `reports/skill-calibration/` 已归档到 `docs/archive/skill-calibration/`。
7. 根目录说明文档已收敛到 `docs/`，根目录只保留 `README.md`。
8. `skills/project-insight-analysis/` 已改为 `.agents/skills/project-insight-analysis/`。
9. 新增 `tools/project_report_manager.py`，支持检查已分析项目、注册新项目并重建索引。
10. 新增 `.github/workflows/pages.yml`，用于发布 `site/`。

## 保留的分析口径

- 不输出项目评分、总分或评分条。
- Gold Example 只有在直接展示核心产品界面、核心工作流、用户动作或输出结果时才可作为主视觉。
- UML、4+1、C4、CLD、SFD、BOT 都是可选表达工具，不强制套用。
- 架构视角先判断复杂度，再选择 C4、4+1、UML 或轻量替代视角。
- HTML 报告优先服务首次接触项目的技术读者：适合谁、解决什么问题、差异点、Demo、机制、采用边界。

## 验证命令

```bash
python3 -m py_compile \
  tools/generate_final_insight_reports.py \
  tools/generate_gbrain_insight_report.py \
  tools/generate_project_index.py \
  tools/project_report_manager.py

python3 tools/generate_final_insight_reports.py
python3 tools/generate_gbrain_insight_report.py
python3 tools/generate_project_index.py

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

浏览器验证使用 `tools/verify_reports.js`，覆盖 `site/index.html` 和四个项目页的桌面、1080px 竖向、390px 手机视口。

## 执行边界

- 所有目标项目报告仍为静态分析。
- 未真实运行目标项目、provider、Qt 构建、broker、数据库或 MCP server。
- `temp/` 中的源码快照和截图只用于本地追溯，不作为 Git 交付内容。
