# Hook Guidelines

> Current state: there are no framework hooks. Do not introduce React hooks or a
> hook abstraction for ordinary changes.

---

## Current Interaction Pattern

Use plain functions and event listeners in embedded JavaScript.

Supported examples:

```javascript
el.search.addEventListener("input", renderAll);
el.sort.addEventListener("change", renderAll);
el.tagFilters.addEventListener("click", handleTagClick);
el.list.addEventListener("click", handleTagClick);
el.clearTag.addEventListener("click", () => {
  activeTag = "";
  renderAll();
});
```

```javascript
document.querySelectorAll('.diagram-shell').forEach((shell) => {
  const buttons = Array.from(shell.querySelectorAll('[data-diagram-tab]'));
  const panels = Array.from(shell.querySelectorAll('[data-diagram-panel]'));
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const target = button.dataset.diagramTab;
      buttons.forEach((item) => item.setAttribute('aria-selected', String(item === button)));
      panels.forEach((panel) => {
        panel.hidden = panel.dataset.diagramPanel !== target;
      });
    });
  });
});
```

---

## Data Loading

The overview page embeds project data at generation time and optionally refreshes
from `projects.json` when served over HTTP.

Supported example:

```javascript
async function loadRuntimeData() {
  if (location.protocol === "file:") return;
  try {
    const response = await fetch("projects.json", { cache: "no-store" });
    if (!response.ok) return;
    const data = await response.json();
    if (Array.isArray(data) && data.length) projects = data;
  } catch (error) {
    console.warn("Using embedded project index data.", error);
  }
}
```

---

## Not Supported

- `use*` custom hooks.
- React Query, SWR, or framework data-fetching hooks.
- Shared hook libraries.
