"""Offline regression tests for persist-skill.sh (no Cloudflare credentials)."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import re


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "persist-skill.sh"


def bash_executable():
    """Prefer Git for Windows Bash over the Windows WSL `bash` app alias."""
    configured = os.environ.get("SKILL_TEST_BASH")
    candidates = [configured, shutil.which("bash")]
    if os.name == "nt":
        candidates.extend((
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
        ))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            if os.name != "nt" or "\\Git\\" in candidate:
                return candidate
    raise unittest.SkipTest("Bash is required (Git Bash on Windows)")


def bash_path(path):
    """Convert a Windows absolute path to the drive syntax understood by Git Bash."""
    value = str(path)
    if os.name == "nt":
        match = re.match(r"^([A-Za-z]):[\\/](.*)$", value)
        if match:
            return "/" + match.group(1).lower() + "/" + match.group(2).replace("\\", "/")
    return value


class PersistSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        # Supply a minimal cloned bundle without contacting GitHub.
        git = self.bin / "git"
        git.write_text('''#!/usr/bin/env bash
set -eu
if [[ "$*" == *sparse-checkout* ]]; then
  exit 0
fi
for destination; do :; done
mkdir -p "$destination/skills/turnstile-spin/scripts"
printf 'fixture skill\\n' > "$destination/skills/turnstile-spin/SKILL.md"
printf '#!/usr/bin/env bash\\n' > "$destination/skills/turnstile-spin/scripts/helper.sh"
''')
        git.chmod(0o755)
        python_command = self.bin / "python3"
        python_executable = bash_path(Path(sys.executable))
        python_command.write_text(
            '#!/usr/bin/env bash\n'
            'args=()\n'
            'for arg in "$@"; do\n'
            '  if [[ "$arg" =~ ^/([A-Za-z])/(.*)$ ]]; then arg="${BASH_REMATCH[1]^}:/${BASH_REMATCH[2]}"; fi\n'
            '  args+=("$arg")\n'
            'done\n'
            f'exec "{python_executable}" "${{args[@]}}"\n', encoding="utf-8"
        )
        python_command.chmod(0o755)
        self.env = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ.get("PATH", "")}
        self.env["TMPDIR"] = bash_path(self.root)
        self.bash = bash_executable()
        self.runner = self.root / "run-with-test-path.sh"
        self.runner.write_text(
            f'#!/usr/bin/env bash\nexport PATH="{bash_path(self.bin)}:$PATH"\nexec "$@"\n',
            encoding="utf-8",
        )
        self.runner.chmod(0o755)

    def run_script(self, target):
        result = subprocess.run(
            [self.bash, bash_path(self.runner), bash_path(SCRIPT), "--path", bash_path(target / "SKILL.md")],
            cwd=self.project,
            env=self.env,
            capture_output=True,
            text=True,
        )
        return result, json.loads(result.stdout)

    def test_copy_failure_is_reported(self):
        # A file where the parent directory should be prevents installation.
        parent = self.project / ".claude"
        parent.write_text("keep this file\n")
        result, output = self.run_script(parent / "skills" / "turnstile-spin")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(output, {"status": "error", "reason": "copy_failed"}, result.stderr)
        self.assertEqual(parent.read_text(), "keep this file\n")

    def test_copy_to_new_or_empty_directory(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                target = self.project / str(existing) / "turnstile-spin"
                if existing:
                    target.mkdir(parents=True)
                result, output = self.run_script(target)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output["status"], "ok")
                self.assertEqual((target / "SKILL.md").read_text(), "fixture skill\n")
                self.assertTrue(os.access(target / "scripts" / "helper.sh", os.X_OK))

    def test_nonempty_destination_is_preserved(self):
        target = self.project / "turnstile-spin"
        target.mkdir()
        existing = target / "SKILL.md"
        existing.write_text("existing skill\n")
        result, output = self.run_script(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output["reason"], "target_not_empty")
        self.assertEqual(existing.read_text(), "existing skill\n")


if __name__ == "__main__":
    unittest.main()
