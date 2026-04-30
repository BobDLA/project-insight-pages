async page => {
  const pages = [
    "free-claude-code",
    "FinceptTerminal",
    "andrej-karpathy-skills",
    "gbrain",
  ];
  const indexPages = ["index.html"];
  const viewports = [
    { name: "desktop", width: 1440, height: 1200, fullPage: true },
    { name: "poster", width: 1080, height: 1920, fullPage: true },
    { name: "mobile", width: 390, height: 1200, fullPage: false },
  ];
  const messages = [];
  const errors = [];
  page.on("console", msg => {
    if (["warning", "error"].includes(msg.type())) {
      messages.push({ type: msg.type(), text: msg.text() });
    }
  });
  page.on("pageerror", err => errors.push(err.message));

  const results = [];
  const indexResults = [];
  for (const file of indexPages) {
    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(`http://localhost:8765/site/${file}`, { waitUntil: "networkidle" });
      await page.screenshot({
        path: `temp/verification/playwright/${file.replace(".html", "")}-${viewport.name}.png`,
        fullPage: viewport.fullPage,
      });
      const layout = await page.evaluate(() => {
        const doc = document.documentElement;
        const body = document.body;
        const badImages = [...document.images]
          .filter(img => !img.complete || img.naturalWidth === 0)
          .map(img => img.getAttribute("src"));
        const viewportWidth = doc.clientWidth;
        const overflowElements = [...document.body.querySelectorAll("*")]
          .filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.right > viewportWidth + 1;
          })
          .slice(0, 8)
          .map(el => ({
            tag: el.tagName.toLowerCase(),
            className: String(el.className),
            text: (el.textContent || "").trim().slice(0, 80),
            right: Math.round(el.getBoundingClientRect().right),
          }));
        return {
          title: document.title,
          scrollOverflow: doc.scrollWidth - doc.clientWidth,
          badImages,
          overflowElements,
          projectRows: document.querySelectorAll(".project-row").length,
          cardViews: document.querySelectorAll(".project-card").length,
          tableRows: document.querySelectorAll("#project-table tr").length,
          topLineRows: document.querySelectorAll(".topline").length,
          controls: document.querySelectorAll(".toolbar input, .toolbar select").length,
          tagChips: document.querySelectorAll("#tag-filters [data-tag]").length,
          hasCategoryFilter: Boolean(document.querySelector("#category-filter")),
          hasAdoptionFilter: Boolean(document.querySelector("#adoption-filter")),
          categoryBadges: document.querySelectorAll(".project-row .badge").length,
          adoptionBadges: document.querySelectorAll(".project-row .adoption").length,
          projectSlugSubtitles: document.querySelectorAll(".project-row .project-slug").length,
          audienceSubtitles: document.querySelectorAll(".project-row .audience").length,
          summarySubtitles: document.querySelectorAll(".project-row .project-summary").length,
          summaryContract: (() => {
            const inlineText = value => String(value ?? "")
              .replace(/\*\*(.+?)\*\*/g, "$1")
              .replace(/`([^`]+?)`/g, "$1")
              .trim();
            const projectByTitle = new Map(projects.map(project => [String(project.title || ""), project]));
            return [...document.querySelectorAll(".project-row")].every(row => {
              const title = row.querySelector("h3")?.textContent.trim() || "";
              const summary = row.querySelector(".project-summary")?.textContent.trim() || "";
              const project = projectByTitle.get(title);
              return summary && project && summary === inlineText(project.summary) && summary !== inlineText(project.audience);
            });
          })(),
          emphasisMarks: document.querySelectorAll(".project-summary strong, .summary-text strong").length,
          rawInlineMarkers: /\*\*.+?\*\*/.test([...document.querySelectorAll(".project-summary, .summary-text")]
            .map(node => node.textContent || "")
            .join(" ")),
          visualHierarchy: (() => {
            const rows = document.querySelectorAll(".project-row").length;
            const primary = document.querySelectorAll(".summary-line.primary").length;
            const difference = document.querySelectorAll(".summary-line.difference").length;
            const mechanism = document.querySelectorAll(".summary-line.mechanism").length;
            const panels = [...document.querySelectorAll(".project-row .summary-stack")]
              .filter(panel => getComputedStyle(panel).borderTopWidth !== "0px").length;
            const accentMarkers = new Set([...document.querySelectorAll(".summary-line")]
              .map(row => getComputedStyle(row).getPropertyValue("--accent").trim()));
            const strongColors = new Set([...document.querySelectorAll(".summary-line .summary-text strong")]
              .map(node => getComputedStyle(node).color));
            return {
              primary,
              difference,
              mechanism,
              panels,
              accentColorCount: accentMarkers.size,
              strongColorCount: strongColors.size,
              works: primary === rows && difference === rows && mechanism === rows
                && panels === rows
                && accentMarkers.size >= 3
                && strongColors.size <= 2,
            };
          })(),
          hasCategorySort: Boolean(document.querySelector('#sort-by option[value="category"]')),
          hasProjectShapeText: body.innerText.includes("项目形态"),
          copyChecks: {
            hasHeroEyebrow: document.querySelector(".hero .eyebrow")?.textContent.trim() === "Project Insight Reports",
            hasHeroTitle: document.querySelector("#page-title")?.textContent.trim() === "项目洞察报告",
            hasHeroCopy: body.innerText.includes("从问题场景、目标用户、差异机制、架构视角和采用风险等维度理解一个项目。"),
            hasListCopy: body.innerText.includes("每份报告围绕问题、差异、机制、架构和采用判断展开；可用关键词或标签收窄列表。"),
            hasMaintenanceCopy: /新增项目只维护清单数据|扩充：|python3 tools\/generate_project_index\.py/.test(body.innerText),
          },
          searchableFields: (() => {
            const probe = {
              title: "",
              slug: "",
              repo: "RepoProbe",
              summary: "SummaryProbe",
              audience: "AudienceProbe",
              problem: "",
              difference: "",
              demo: "",
              architecture: "",
              category: "CategoryProbe",
              adoption: "AdoptionProbe",
              tags: ["TagProbe"],
            };
            const text = searchable(probe);
            return {
              repo: text.includes("repoprobe"),
              summary: text.includes("summaryprobe"),
              audience: text.includes("audienceprobe"),
              category: text.includes("categoryprobe"),
              adoption: text.includes("adoptionprobe"),
              tags: text.includes("tagprobe"),
            };
          })(),
          links: [...document.querySelectorAll('a[href^="projects/"]')].map(link => link.getAttribute("href")),
        };
      });
      layout.discoveryModelWorks = !layout.hasCategoryFilter
        && !layout.hasAdoptionFilter
        && layout.categoryBadges === 0
        && layout.adoptionBadges === 0
        && layout.projectSlugSubtitles === 0
        && layout.audienceSubtitles === 0
        && layout.summarySubtitles === layout.projectRows
        && layout.summaryContract
        && layout.topLineRows === 0
        && layout.emphasisMarks >= layout.projectRows
        && !layout.rawInlineMarkers
        && layout.visualHierarchy.works
        && !layout.hasCategorySort
        && !layout.hasProjectShapeText
        && layout.controls === 2
        && layout.tagChips >= 10
        && Object.values(layout.searchableFields).every(Boolean)
        && layout.copyChecks.hasHeroEyebrow
        && layout.copyChecks.hasHeroTitle
        && layout.copyChecks.hasHeroCopy
        && layout.copyChecks.hasListCopy
        && !layout.copyChecks.hasMaintenanceCopy;
      const mcpChip = page.locator('#tag-filters [data-tag="MCP"]').first();
      layout.tagFilterWorks = false;
      if (await mcpChip.count()) {
        await mcpChip.click();
        const tagFilterWorks = await page.evaluate(() => ({
          rows: document.querySelectorAll(".project-row").length,
          text: document.body.innerText,
          activeTag: document.querySelector('#tag-filters [aria-pressed="true"]')?.textContent.trim() || "",
        }));
        layout.tagFilterWorks = tagFilterWorks.rows === 1 && tagFilterWorks.activeTag === "MCP" && /GBrain/.test(tagFilterWorks.text);
      }
      if (await page.locator("#clear-tag").isVisible()) {
        await page.locator("#clear-tag").click();
      }
      const checkSearch = async (term, expectedText) => {
        await page.fill("#search", term);
        const result = await page.evaluate(() => ({
          rows: document.querySelectorAll(".project-row").length,
          text: document.body.innerText,
        }));
        return result.rows === 1 && result.text.includes(expectedText);
      };
      layout.searchWorks = await checkSearch("gbrain", "GBrain");
      layout.repoSearchWorks = await checkSearch("garrytan/gbrain", "GBrain");
      layout.categorySearchWorks = await checkSearch("接口代理", "free-claude-code");
      layout.adoptionSearchWorks = await checkSearch("团队基线", "andrej-karpathy-skills");
      layout.summarySearchWorks = await checkSearch("provider 适配链路", "free-claude-code");
      layout.tagSearchWorks = await checkSearch("Knowledge", "GBrain");
      layout.indexDiscoveryWorks = layout.discoveryModelWorks
        && layout.tagFilterWorks
        && layout.searchWorks
        && layout.repoSearchWorks
        && layout.categorySearchWorks
        && layout.adoptionSearchWorks
        && layout.summarySearchWorks
        && layout.tagSearchWorks;
      indexResults.push({ file, viewport, layout });
    }
  }

  for (const file of pages) {
    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(`http://localhost:8765/site/projects/${file}/`, { waitUntil: "networkidle" });
      await page.screenshot({
        path: `temp/verification/playwright/${file}-${viewport.name}.png`,
        fullPage: viewport.fullPage,
      });
      const layout = await page.evaluate(() => {
        const doc = document.documentElement;
        const body = document.body;
        const badImages = [...document.images]
          .filter(img => !img.complete || img.naturalWidth === 0)
          .map(img => img.getAttribute("src"));
        const viewportWidth = doc.clientWidth;
        const overflowElements = [...document.body.querySelectorAll("*")]
          .filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && rect.right > viewportWidth + 1;
          })
          .slice(0, 8)
          .map(el => ({
            tag: el.tagName.toLowerCase(),
            className: String(el.className),
            text: (el.textContent || "").trim().slice(0, 80),
            right: Math.round(el.getBoundingClientRect().right),
          }));
        return {
          title: document.title,
          scrollOverflow: doc.scrollWidth - doc.clientWidth,
          bodyHeight: Math.round(body.getBoundingClientRect().height),
          badImages,
          overflowElements,
          sectionCount: document.querySelectorAll(".section").length,
          leanItems: document.querySelectorAll("#lean .kv").length,
          diagramTypes: [...document.querySelectorAll(".type-chip")].map(el => el.textContent.trim()),
          diagramShells: document.querySelectorAll(".diagram-shell").length,
          visibleSvgs: document.querySelectorAll(".diagram-panel:not([hidden]) svg").length,
          mermaidBlocks: document.querySelectorAll(".mermaid-block").length,
          architectureViews: document.querySelectorAll("#views .arch-view").length,
          architectureDecisionItems: document.querySelectorAll("#views .arch-kv").length,
          architectureSvgs: document.querySelectorAll("#views .arch-view .svg-frame svg").length,
          architectureSourceBlocks: document.querySelectorAll("#views .arch-source .mermaid-block").length,
          hasOld4p1CardLayout: document.querySelectorAll("#views .view-card").length > 0,
          hasOldStatus: body.innerText.includes("适合观察与场景试用"),
          hasScoreText: /85\/100|78\/100|82\/100|综合评分|综合判断分|score-value|verdict-score/i.test(body.innerText),
        };
      });
      await page.locator('[data-diagram-tab="component"]').first().click();
      const componentVisible = await page.evaluate(() => {
        const panel = document.querySelector('[data-diagram-panel="component"]');
        return Boolean(panel && !panel.hidden && panel.querySelector("svg"));
      });
      layout.componentTabWorks = componentVisible;
      results.push({ file, viewport, layout });
    }
  }
  return { indexResults, results, consoleMessages: messages, pageErrors: errors };
}
