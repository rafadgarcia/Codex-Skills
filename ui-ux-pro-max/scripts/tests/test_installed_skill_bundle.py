"""Contracts for the files shipped in the installed UI/UX Pro Max skill."""

import re
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[2]
SKILL_MD = SKILL_DIR / "SKILL.md"


class InstalledSkillBundleTests(unittest.TestCase):
    def test_search_script_is_bundled_and_examples_use_skill_dir(self):
        self.assertTrue((SKILL_DIR / "scripts" / "search.py").is_file())
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertGreaterEqual(skill.count('${SKILL_DIR}/scripts/search.py'), 5)
        self.assertNotIn("CLAUDE_PLUGIN_ROOT", skill)

    def test_all_skill_relative_markdown_links_resolve(self):
        broken = []
        for markdown in SKILL_DIR.rglob("*.md"):
            content = markdown.read_text(encoding="utf-8")
            for match in re.finditer(r"\]\(([^)]+\.md)(?:#[^)]+)?\)", content):
                target = match.group(1)
                if target.startswith(("https://", "http://")):
                    continue
                if not (markdown.parent / target).resolve().is_file():
                    broken.append(f"{markdown.relative_to(SKILL_DIR)}: {target}")
        self.assertEqual([], broken)


if __name__ == "__main__":
    unittest.main()
