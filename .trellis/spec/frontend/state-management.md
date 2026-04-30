# State Management

> State is page-local vanilla JavaScript. There is no global store, URL state
> router, or server-state cache.

---

## Overview Page State

The overview page keeps a local `projects` array, initialized from embedded data
and optionally replaced by `projects.json` at runtime.

Supported example:

```javascript
const EMBEDDED_PROJECTS = __EMBEDDED__;
let projects = [...EMBEDDED_PROJECTS];
```

DOM references are grouped in a plain object:

```javascript
const el = {
  search: document.querySelector("#search"),
  sort: document.querySelector("#sort-by"),
  tagFilters: document.querySelector("#tag-filters"),
  clearTag: document.querySelector("#clear-tag"),
  list: document.querySelector("#project-list"),
  count: document.querySelector("#result-count"),
  empty: document.querySelector("#empty-state"),
  total: document.querySelector("#metric-total")
};
```

Derived state is recomputed from DOM control values and the `projects` array:

```javascript
let activeTag = "";

function visibleTags(project) {
  return Array.isArray(project.tags) ? project.tags : [];
}

function projectFacets(project) {
  return [project.category, project.adoption, ...visibleTags(project)].filter(Boolean).map(String);
}

function searchable(project) {
  return [
    project.title, project.slug, project.repo, project.summary, project.audience,
    project.problem, project.difference, project.demo, project.architecture,
    ...projectFacets(project)
  ].join(" ").toLowerCase();
}

function filteredProjects() {
  const query = el.search.value.trim().toLowerCase();
  return sortProjects(projects.filter(project => {
    const matchesSearch = !query || searchable(project).includes(query);
    const matchesTag = !activeTag || projectFacets(project)
      .some(value => value.trim().toLowerCase() === activeTag.trim().toLowerCase());
    return matchesSearch && matchesTag;
  }));
}
```

Do not use `category` / `adoption` select dropdowns as the primary overview
discovery model. Keep them searchable by including them in project facets, but
derive visible chips from `tags`. Do not render category/adoption hero metrics,
sort modes, or per-row badges; duplicate useful category/adoption concepts into
`tags` when they should appear as chips.

---

## Diagram Tab State

Report pages store active diagram state in DOM attributes:

- active tab: `aria-selected="true"`
- active panel: panel without `hidden`
- tab/panel linkage: matching `data-diagram-tab` and `data-diagram-panel`

Supported example:

```javascript
panels.forEach((panel) => {
  panel.hidden = panel.dataset.diagramPanel !== target;
});
```

---

## Not Supported

- Redux, Zustand, MobX, Pinia, Vuex, or context stores.
- URL-synchronized filter state.
- Client-side persistence in localStorage/sessionStorage.
- Server-state caching.
