"""Synthetic Git tests for the owned pre-push security boundary."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
SCANNER = SCRIPTS / "scan-secrets.py"
PRE_PUSH = SCRIPTS / "pre-push"
INSTALL_HOOKS = SCRIPTS / "install-hooks.sh"


class SecurityGuardrailTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "guardrail@example.test")
        self.git("config", "user.name", "Guardrail Test")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=self.repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check
        )

    def commit(self, filename: str, content: str, message: str = "test commit") -> str:
        (self.repo / filename).write_text(content, encoding="utf-8")
        self.git("add", filename)
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def zero_oid(self) -> str:
        return "0" * len(self.git("rev-parse", "HEAD").stdout.strip())

    def scan(self, *update: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCANNER), "--update", *update],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def install_owned_scripts(self) -> Path:
        destination = self.repo / "scripts"
        destination.mkdir()
        for source in (SCANNER, PRE_PUSH, INSTALL_HOOKS):
            shutil.copy2(source, destination / source.name)
        return destination

    def test_normal_commit_range_is_scanned(self) -> None:
        base = self.commit("readme.txt", "base\n")
        head = self.commit("readme.txt", "safe update\n")

        result = self.scan("refs/heads/main", head, "refs/heads/main", base)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_new_branch_and_annotated_tag_are_scanned(self) -> None:
        head = self.commit("safe.txt", "safe\n")
        zero = self.zero_oid()
        self.git("tag", "-a", "v1", "-m", "safe release")
        tag_oid = self.git("rev-parse", "refs/tags/v1").stdout.strip()

        branch = self.scan("refs/heads/new", head, "refs/heads/new", zero)
        tag = self.scan("refs/tags/v1", tag_oid, "refs/tags/v1", zero)

        self.assertEqual(branch.returncode, 0, branch.stderr)
        self.assertEqual(tag.returncode, 0, tag.stderr)

    def test_raw_object_secret_is_rejected_without_echoing_it(self) -> None:
        secret = "sk-proj-" + "a" * 30
        head = self.commit("credential.txt", f"token={secret}\n")

        result = self.scan("refs/heads/main", head, "refs/heads/main", self.zero_oid())

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout)
        self.assertNotIn(secret, result.stderr)

    def test_pre_push_fails_when_scanner_cannot_run(self) -> None:
        scripts = self.install_owned_scripts()
        head = self.commit("safe.txt", "safe\n")
        (scripts / "scan-secrets.py").write_text("#!/usr/bin/env python3\nraise SystemExit(9)\n", encoding="utf-8")
        update = f"refs/heads/main {head} refs/heads/main {self.zero_oid()}\n"

        result = subprocess.run(
            ["sh", str(scripts / "pre-push")], cwd=self.repo, input=update, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        self.assertNotEqual(result.returncode, 0)

    def test_pre_push_rejects_malformed_update_input(self) -> None:
        scripts = self.install_owned_scripts()

        result = subprocess.run(
            ["sh", str(scripts / "pre-push")], cwd=self.repo, input="not-a-ref-update\n", text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        self.assertNotEqual(result.returncode, 0)

    def test_existing_hook_is_preserved(self) -> None:
        self.install_owned_scripts()
        hook = self.repo / ".git" / "hooks" / "pre-push"
        hook.write_text("#!/bin/sh\necho unmanaged\n", encoding="utf-8")

        result = subprocess.run(
            ["sh", str(self.repo / "scripts" / "install-hooks.sh")], cwd=self.repo, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(hook.read_text(encoding="utf-8"), "#!/bin/sh\necho unmanaged\n")

    def test_environment_cannot_bypass_secret_scan(self) -> None:
        scripts = self.install_owned_scripts()
        secret = "sk-ant-" + "b" * 30
        head = self.commit("credential.txt", secret + "\n")
        update = f"refs/heads/main {head} refs/heads/main {self.zero_oid()}\n"
        environment = {**os.environ, "PAPER_CURATION_SKIP_SECRET_SCAN": "1"}

        result = subprocess.run(
            ["sh", str(scripts / "pre-push")], cwd=self.repo, input=update, text=True, env=environment,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout)
        self.assertNotIn(secret, result.stderr)


if __name__ == "__main__":
    unittest.main()
