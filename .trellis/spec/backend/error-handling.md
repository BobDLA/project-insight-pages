# Error Handling

> Current project error handling is script/CLI oriented. There are no API error
> responses or custom exception classes.

---

## CLI Exit Behavior

Use integer return codes for normal CLI command outcomes:

- `0` for success.
- `1` for a negative check result only when the command has a strict mode.

Supported example:

```python
def cmd_check(args: argparse.Namespace) -> int:
    project = find_project(load_projects(), args.target)
    if project:
        print(json.dumps({"exists": True, "project": project}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps({"exists": False, "slug": slug_from(args.target)}, ensure_ascii=False, indent=2))
    return 1 if args.strict else 0
```

Use `raise SystemExit(...)` for hard validation failures that should stop a CLI
command with a readable message.

Supported examples:

```python
if not source.exists():
    raise SystemExit(f"missing source file: {source}")
```

```python
if existing and not args.replace:
    raise SystemExit(f"project already registered: {existing.get('slug')} (use --replace to update)")
```

---

## Subprocess Errors

When a command depends on another local script, call it with `check=True` so
failures propagate instead of silently producing stale output.

Supported example:

```python
subprocess.run([sys.executable, str(INDEX_SCRIPT)], cwd=ROOT, check=True)
```

---

## Browser Verification Errors

`tools/verify_reports.js` collects browser console warnings/errors and
page-level errors into the returned JSON object. It also records layout and
selector-level assertions for the caller to inspect.

Supported example:

```javascript
const messages = [];
const errors = [];
page.on("console", msg => {
  if (["warning", "error"].includes(msg.type())) {
    messages.push({ type: msg.type(), text: msg.text() });
  }
});
page.on("pageerror", err => errors.push(err.message));
```

---

## Not Supported

- Custom exception hierarchies.
- API response envelopes.
- Retry frameworks.
- Centralized error middleware.
