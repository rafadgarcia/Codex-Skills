#!/usr/bin/env python3
"""Validate the installed skill catalog, manifest, and local Markdown links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)]+?)(?:#[^)]*)?\)")
FRONTMATTER_NAME = re.compile(r"(?m)^name:\s*[\"']?([^\s\"']+)")
IGNORED_DIRS = {".git", ".system", "__pycache__", "scripts"}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "skills-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest["skills"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return [f"invalid skills-manifest.json: {exc}"]

    names: set[str] = set()
    for entry in entries:
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            errors.append("manifest entry has no skill name")
            continue
        if name in names:
            errors.append(f"duplicate manifest entry: {name}")
        names.add(name)
        mode = entry.get("mode")
        if mode not in {"local", "overlay", "pinned"}:
            errors.append(f"{name}: unsupported mode {mode!r}")
        if mode == "overlay" and (
            not entry.get("repo") or not entry.get("branch") or "subPath" not in entry
        ):
            errors.append(f"{name}: overlay requires repo, branch, and subPath")

    skill_dirs = {
        path.name for path in root.iterdir()
        if path.is_dir() and path.name not in IGNORED_DIRS and not path.name.startswith(".")
    }
    for name in sorted(names - skill_dirs):
        errors.append(f"manifest skill folder is missing: {name}")
    for name in sorted(skill_dirs - names):
        errors.append(f"skill folder is absent from manifest: {name}")

    for name in sorted(skill_dirs):
        skill_file = root / name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{name}: SKILL.md is missing")
            continue
        text = skill_file.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)
        if len(frontmatter) < 3 or not frontmatter[0].strip() == "":
            errors.append(f"{name}: missing YAML frontmatter")
        elif not FRONTMATTER_NAME.search(frontmatter[1]):
            errors.append(f"{name}: frontmatter has no name")
        elif FRONTMATTER_NAME.search(frontmatter[1]).group(1) != name:
            errors.append(f"{name}: frontmatter name does not match folder")

    markdown_files = [root / "README.md", *(root / name / "SKILL.md" for name in skill_dirs)]
    for markdown in markdown_files:
        if not markdown.is_file():
            continue
        try:
            content = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{markdown.relative_to(root)}: cannot read Markdown: {exc}")
            continue
        for match in LINK.finditer(content):
            target = match.group(1)
            if target.startswith("#"):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            target_path = (markdown.parent / target).resolve()
            if not target_path.is_file():
                errors.append(f"{markdown.relative_to(root)}: broken local link {target}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    errors = validate(root)
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = sum(
        1 for path in root.iterdir()
        if path.is_dir() and path.name not in IGNORED_DIRS and not path.name.startswith(".")
    )
    print(f"Skill validation passed: {count} skills, manifest and local Markdown links are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
