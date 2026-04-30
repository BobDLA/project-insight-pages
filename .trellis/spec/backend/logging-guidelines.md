# Logging Guidelines

> Current state: the repo does not use Python `logging`, structured logs, or log
> level conventions. Tools print concise command results to stdout.

---

## Current Output Patterns

Use `print(...)` for successful script results and generated-file notices.

Supported examples:

```python
print(json.dumps({"registered": slug, "file": record["file"], "markdown": record["markdown"]}, ensure_ascii=False, indent=2))
```

```python
print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")
```

For browser runtime fallback, the generated static page uses `console.warn`
only when `projects.json` cannot be loaded and embedded data is used instead.

Supported example:

```javascript
try {
  const response = await fetch("projects.json", { cache: "no-store" });
  if (!response.ok) return;
  const data = await response.json();
  if (Array.isArray(data) && data.length) projects = data;
} catch (error) {
  console.warn("Using embedded project index data.", error);
}
```

---

## Do Not Add Without A Requirement

- Global logging configuration.
- JSON log schemas.
- Log files.
- Verbose progress logs in generated site scripts.

---

## Sensitive Output

Current scripts handle public report metadata and local file paths. If a future
task adds tokens, credentials, private repository data, or user secrets, do not
print those values. This is a new contract and should be documented in this file
when introduced.
