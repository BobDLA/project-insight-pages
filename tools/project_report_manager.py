#!/usr/bin/env python3
"""Manage project insight report registrations for the static site."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
PROJECTS_DIR = SITE_DIR / "projects"
INDEX_DATA = SITE_DIR / "projects.json"
INDEX_SCRIPT = ROOT / "tools" / "generate_project_index.py"


def load_projects() -> list[dict]:
    if not INDEX_DATA.exists():
        return []
    return json.loads(INDEX_DATA.read_text(encoding="utf-8"))


def save_projects(projects: list[dict]) -> None:
    INDEX_DATA.parent.mkdir(parents=True, exist_ok=True)
    INDEX_DATA.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug_from(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.startswith(("http://", "https://", "git@")):
        if value.startswith("git@"):
            value = value.split(":", 1)[-1]
            return Path(value).name.removesuffix(".git")
        parsed = urlparse(value)
        return Path(parsed.path).name.removesuffix(".git")
    return Path(value).name.removesuffix(".git")


def find_project(projects: list[dict], value: str) -> dict | None:
    slug = slug_from(value).lower()
    target = value.strip().rstrip("/").removesuffix(".git").lower()
    for project in projects:
        project_slug = str(project.get("slug", "")).lower()
        project_repo = str(project.get("repo", "")).strip().rstrip("/").removesuffix(".git").lower()
        if slug == project_slug or target == project_repo:
            return project
    return None


def copy_if_given(src: str | None, dst: Path) -> None:
    if not src:
        return
    source = Path(src)
    if not source.is_absolute():
        source = ROOT / source
    if not source.exists():
        raise SystemExit(f"missing source file: {source}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != dst.resolve():
        shutil.copyfile(source, dst)


def rebuild_index() -> None:
    subprocess.run([sys.executable, str(INDEX_SCRIPT)], cwd=ROOT, check=True)


def cmd_list(_: argparse.Namespace) -> int:
    for project in load_projects():
        print(f"{project.get('slug')}\t{project.get('category')}\t{project.get('file')}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    project = find_project(load_projects(), args.target)
    if project:
        print(json.dumps({"exists": True, "project": project}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps({"exists": False, "slug": slug_from(args.target)}, ensure_ascii=False, indent=2))
    return 1 if args.strict else 0


def cmd_register(args: argparse.Namespace) -> int:
    projects = load_projects()
    existing = find_project(projects, args.slug or args.repo)
    if existing and not args.replace:
        raise SystemExit(f"project already registered: {existing.get('slug')} (use --replace to update)")

    slug = args.slug or slug_from(args.repo)
    project_dir = PROJECTS_DIR / slug
    if not args.dry_run:
        project_dir.mkdir(parents=True, exist_ok=True)
        copy_if_given(args.html, project_dir / "index.html")
        copy_if_given(args.markdown, project_dir / "analysis.md")
        for asset in args.asset:
            source = Path(asset)
            copy_if_given(asset, project_dir / "assets" / source.name)

    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    record = {
        "slug": slug,
        "title": args.title or slug,
        "file": f"projects/{slug}/",
        "markdown": f"projects/{slug}/analysis.md",
        "repo": args.repo,
        "category": args.category,
        "adoption": args.adoption,
        "audience": args.audience,
        "summary": args.summary,
        "problem": args.problem,
        "difference": args.difference,
        "demo": args.demo,
        "architecture": args.architecture,
        "tags": tags,
        "updated": args.updated or date.today().isoformat(),
    }

    if args.dry_run:
        print(json.dumps({"dry_run": True, "record": record}, ensure_ascii=False, indent=2))
        return 0

    if existing:
        projects = [record if project is existing else project for project in projects]
    else:
        projects.append(record)
    projects.sort(key=lambda item: (str(item.get("category", "")), str(item.get("title", "")).lower()))
    save_projects(projects)
    rebuild_index()
    print(json.dumps({"registered": slug, "file": record["file"], "markdown": record["markdown"]}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List registered projects")
    list_parser.set_defaults(func=cmd_list)

    check_parser = sub.add_parser("check", help="Check whether a repo URL or slug has been analyzed")
    check_parser.add_argument("target")
    check_parser.add_argument("--strict", action="store_true", help="Exit 1 when the project is missing")
    check_parser.set_defaults(func=cmd_check)

    register = sub.add_parser("register", help="Register a generated report and rebuild the site index")
    register.add_argument("--repo", required=True)
    register.add_argument("--slug")
    register.add_argument("--title")
    register.add_argument("--category", required=True)
    register.add_argument("--adoption", required=True)
    register.add_argument("--audience", required=True)
    register.add_argument("--summary", required=True)
    register.add_argument("--problem", required=True)
    register.add_argument("--difference", required=True)
    register.add_argument("--demo", required=True)
    register.add_argument("--architecture", required=True)
    register.add_argument("--tags", default="")
    register.add_argument("--updated")
    register.add_argument("--html", help="Path to generated HTML; copied to site/projects/<slug>/index.html")
    register.add_argument("--markdown", help="Path to generated Markdown; copied to site/projects/<slug>/analysis.md")
    register.add_argument("--asset", action="append", default=[], help="Asset file copied into the project asset directory")
    register.add_argument("--replace", action="store_true")
    register.add_argument("--dry-run", action="store_true", help="Print the record without copying files or updating the index")
    register.set_defaults(func=cmd_register)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
