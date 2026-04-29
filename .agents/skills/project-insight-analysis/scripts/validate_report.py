#!/usr/bin/env python3
"""Validate Project Insight Analysis report artifacts.

This script is intentionally lightweight: it uses only the Python standard
library and checks the report-specific gates that are easy to regress during
iteration. It is not a replacement for browser layout verification.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SCORE_PATTERNS = [
    (re.compile(r"综合评分|项目评分|评分条|score-value|verdict-score|overall score", re.I), "score wording"),
    (re.compile(r"(?<![\w.-])(?:[1-9]\d?|100)\s*/\s*100(?![\w.-])"), "N/100 score"),
]

OLD_TEMPLATE_MARKERS = [
    "GBrain",
    "PGLite/Postgres",
    "Asks questions or sends signals",
]

UNRELATED_DEMO_PATTERNS = [
    re.compile(r"Wintermute", re.I),
    re.compile(r"voice[-\s]?client", re.I),
    re.compile(r"仓库中的\s*voice\s*client", re.I),
]

LEAN_TERMS = [
    "适合谁",
    "解决什么问题",
    "和别的方案哪里不同",
    "为什么现在值得看",
    "最小验证方式",
]

CORE_TERMS = [
    "Gold Example",
    "核心资产",
    "证据",
]

ARCH_DECISION_TERMS = [
    ("项目复杂性评估结果", "项目复杂性评估", "Project complexity"),
    ("选用的架构描述框架", "选用框架", "Selected architecture framework"),
    ("裁剪策略理由", "裁剪策略", "Tailoring reason"),
    ("省略内容", "Omitted views"),
]


@dataclass
class ReportResult:
    path: str
    kind: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def strip_html(source: str) -> str:
    source = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    source = html.unescape(source)
    return re.sub(r"\s+", " ", source).strip()


def has_any(text: str, variants: tuple[str, ...] | list[str]) -> bool:
    return any(item in text for item in variants)


def extract_paragraphs(source: str, is_html: bool) -> list[str]:
    if is_html:
        values = []
        for raw in re.findall(r"<p\b[^>]*>(.*?)</p>", source, flags=re.I | re.S):
            values.append(strip_html(raw))
        return [item for item in values if item]

    paragraphs = []
    for block in re.split(r"\n\s*\n", source):
        block = block.strip()
        if not block or block.startswith(("#", "|", "```", "- ")):
            continue
        paragraphs.append(re.sub(r"\s+", " ", block))
    return paragraphs


def check_common(result: ReportResult, source: str, visible_text: str) -> None:
    if not re.search(r"^\s*#\s+\S+", source, flags=re.M) and "<h1" not in source.lower():
        result.errors.append("missing H1 / main title")

    for pattern, label in SCORE_PATTERNS:
        if pattern.search(visible_text):
            result.errors.append(f"contains forbidden numeric scoring marker: {label}")

    if all(marker in source for marker in OLD_TEMPLATE_MARKERS):
        result.errors.append("contains unrelated old GBrain/PGLite report-template example")

    if "Gold Example" in visible_text or "Demo" in visible_text:
        for pattern in UNRELATED_DEMO_PATTERNS:
            if pattern.search(visible_text) or pattern.search(source):
                result.errors.append(f"contains likely unrelated demo media marker: {pattern.pattern}")
                break

    missing_lean = [term for term in LEAN_TERMS if term not in visible_text]
    if missing_lean:
        result.errors.append("missing Lean/new-user terms: " + ", ".join(missing_lean))

    missing_core = [term for term in CORE_TERMS if term not in visible_text]
    if missing_core:
        result.errors.append("missing core report terms: " + ", ".join(missing_core))

    if "静态分析" in visible_text and not has_any(visible_text, ["未运行", "未真实运行", "静态推演"]):
        result.warnings.append("static analysis is mentioned but runtime boundary is not explicit")

    if "适合观察与场景试用" in visible_text:
        result.errors.append("contains rejected old adoption wording: 适合观察与场景试用")

    long_paragraphs = [p for p in extract_paragraphs(source, result.kind == "html") if len(p) > 280]
    if long_paragraphs:
        result.warnings.append(f"{len(long_paragraphs)} long paragraph(s) over 280 characters")


def check_mechanism(result: ReportResult, source: str, visible_text: str) -> None:
    if "项目机制图" not in visible_text and "diagram-shell" not in source:
        return

    if result.kind == "html":
        if "diagram-shell" not in source:
            result.errors.append("mechanism diagram promised but .diagram-shell is missing")
        if "<svg" not in source and "class=\"mermaid\"" not in source and "class='mermaid'" not in source:
            result.errors.append("mechanism diagram has no visible SVG/Mermaid rendering")
        if "data-diagram-panel=\"source\"" not in source and "图源" not in visible_text:
            result.errors.append("mechanism diagram source panel is missing")
        if "diagram-mobile" not in source:
            result.warnings.append("mechanism diagram has no mobile fallback marker")
        return

    for term in ["图型选择", "选择理由", "场景"]:
        if term not in visible_text:
            result.errors.append(f"mechanism diagram missing field: {term}")


def check_architecture(result: ReportResult, source: str, visible_text: str) -> None:
    has_arch = "架构视角" in visible_text or "arch-lens" in source or "Architecture Decision" in visible_text
    if not has_arch:
        return

    for variants in ARCH_DECISION_TERMS:
        if not has_any(visible_text, variants):
            result.errors.append(f"architecture decision note missing: {variants[0]}")

    if not has_any(visible_text, ["核心业务流转", "Core Process", "Priority Interaction", "Dynamic", "sequenceDiagram"]):
        result.errors.append("architecture lens missing priority core interaction")

    if result.kind == "html":
        if "view-card" in source:
            result.errors.append("old 4+1 text-card layout marker found: view-card")
        if "arch-source" not in source:
            result.errors.append("architecture Mermaid/source block is not preserved")
        if not re.search(r"<article\b[^>]*class=\"[^\"]*arch-view[^\"]*\"[\s\S]*?<svg\b", source):
            result.errors.append("architecture section has no visible SVG inside arch-view")
        if "Mermaid 源码" in visible_text and "<svg" not in source:
            result.errors.append("architecture source appears without visible rendered diagram")
        return

    if "```mermaid" not in source:
        result.errors.append("architecture Markdown missing Mermaid / structured source block")


def check_html_assets(result: ReportResult, path: Path, source: str) -> None:
    if "<meta name=\"viewport\"" not in source and "<meta name='viewport'" not in source:
        result.errors.append("HTML missing responsive viewport meta")

    if "infographic" in path.name.lower():
        result.errors.append("separate infographic HTML artifact is not allowed by default")

    for raw_src in re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", source, flags=re.I):
        if raw_src.startswith(("http://", "https://", "data:", "#")):
            continue
        asset = (path.parent / html.unescape(raw_src)).resolve()
        if not asset.exists():
            result.errors.append(f"missing local image asset: {raw_src}")


def validate(path: Path) -> ReportResult:
    source = path.read_text(encoding="utf-8")
    kind = "html" if path.suffix.lower() in {".html", ".htm"} else "markdown"
    visible_text = strip_html(source) if kind == "html" else source
    result = ReportResult(path=str(path), kind=kind)

    check_common(result, source, visible_text)
    check_mechanism(result, source, visible_text)
    check_architecture(result, source, visible_text)
    if kind == "html":
        check_html_assets(result, path, source)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Project Insight report Markdown/HTML artifacts.")
    parser.add_argument("paths", nargs="+", help="Report files to validate.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    results = []
    for item in args.paths:
        path = Path(item)
        if not path.exists():
            result = ReportResult(path=str(path), kind="missing", errors=["file does not exist"])
        else:
            result = validate(path)
        results.append(result)

    payload = {
        "ok": all(item.ok for item in results),
        "results": [
            {
                "path": item.path,
                "kind": item.kind,
                "ok": item.ok,
                "errors": item.errors,
                "warnings": item.warnings,
            }
            for item in results
        ],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in results:
            status = "OK" if item.ok else "FAIL"
            print(f"{status} {item.path}")
            for error in item.errors:
                print(f"  error: {error}")
            for warning in item.warnings:
                print(f"  warning: {warning}")

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
