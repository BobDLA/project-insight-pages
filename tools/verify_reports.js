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
          controls: document.querySelectorAll(".toolbar input, .toolbar select").length,
          links: [...document.querySelectorAll('a[href^="projects/"]')].map(link => link.getAttribute("href")),
        };
      });
      await page.fill("#search", "gbrain");
      const searchWorks = await page.evaluate(() => ({
        rows: document.querySelectorAll(".project-row").length,
        text: document.body.innerText,
      }));
      layout.searchWorks = searchWorks.rows === 1 && /GBrain/.test(searchWorks.text);
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
