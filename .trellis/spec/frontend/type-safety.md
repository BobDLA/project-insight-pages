# Type Safety

> Current state: frontend JavaScript is plain JavaScript embedded in generated
> HTML. There is no TypeScript, schema validation library, or build step.

---

## Current Runtime Guards

Use small runtime guards where the current code already does so:

```javascript
if (Array.isArray(data) && data.length) projects = data;
```

Use nullish fallback in escaping and rendering helpers:

```javascript
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}
```

Use Python type hints in generator functions where they already exist:

```python
def report_sections(project: dict) -> list[tuple[str, str, str, str, str]]:
    ...
```

---

## Data Contract

The frontend expects project objects to provide the registry fields documented in
`../backend/database-guidelines.md`. The index renderer reads these keys:

- `title`
- `slug`
- `category`
- `adoption`
- `audience`
- `summary`
- `problem`
- `difference`
- `demo`
- `architecture`
- `tags`
- `file`
- `markdown`
- `repo`
- `updated`

The index title area renders `summary` as the one-sentence functional
highlight. `audience` remains searchable metadata and must not be used as the
title-area subtitle.

The index renderer accepts only lightweight inline markers in `summary`,
`problem`, `difference`, and `demo`: `**...**` for emphasis and `` `...` `` for
code spans. Treat those markers as display hints, not as trusted HTML. The
rendered visible text should not expose raw marker characters.

---

## Not Supported

- TypeScript interfaces.
- Zod/Yup/io-ts schemas.
- Generated client types.
- Build-time type checking for frontend code.
