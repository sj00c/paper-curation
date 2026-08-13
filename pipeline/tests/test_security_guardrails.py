#!/usr/bin/env python3
"""Executable regression matrix for git-object scanning and agent guardrails."""
from __future__ import annotations

import base64
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANTHROPIC = "sk-" + "ant-api03-" + "A" * 32
AWS = "AK" + "IA" + "A" * 16
GITHUB = "gh" + "p_" + "A" * 30
GOOGLE = "AI" + "za" + "A" * 35



def run(args, cwd, *, check=True, env=None):
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True, env=env)
    if check and proc.returncode:
        raise AssertionError(f"{args} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


class PushRepo:
    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pc-security-"))
        self.remote = self.tmp / "remote.git"
        self.work = self.tmp / "work"
        run(["git", "init", "-q", "--bare", str(self.remote)], self.tmp)
        run(["git", "clone", "-q", str(self.remote), str(self.work)], self.tmp)
        run(["git", "config", "user.email", "security-test@example.invalid"], self.work)
        run(["git", "config", "user.name", "Security Test"], self.work)
        hooks = self.work / ".git/hooks"
        shutil.copy2(ROOT / "scripts/pre-push", hooks / "pre-push")
        # 훅이 쓰는 스크립트를 이름으로 나열하면, 훅에 단계가 하나 추가될 때마다
        # 여기가 조용히 뒤처진다. 실제로 줄바꿈 가드를 넣었을 때 훅이 그 단계에서
        # 죽어 시크릿과 무관한 테스트 12개가 함께 무너졌다. 디렉토리째 복사해서
        # 훅이 무엇을 부르든 따라오게 한다.
        shutil.copytree(ROOT / "scripts", self.work / "scripts")
        os.chmod(hooks / "pre-push", 0o755)
        self.commit("base.txt", "base\n", "base")
        self.push("HEAD:refs/heads/main", expect=0)
        run(["git", "branch", "--set-upstream-to=origin/main"], self.work)

    def close(self):
        shutil.rmtree(self.tmp)

    def commit(self, name: str, content: str | bytes, message: str):
        path = self.work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        run(["git", "add", name], self.work)
        run(["git", "commit", "-qm", message], self.work)

    def push(self, refspec: str | None = None, *, expect: int):
        args = ["git", "push", "origin"]
        if refspec:
            args.append(refspec)
        proc = run(args, self.work, check=False)
        self.assert_exit(proc, expect)
        return proc

    @staticmethod
    def assert_exit(proc, expect):
        if proc.returncode != expect:
            raise AssertionError(
                f"push exit={proc.returncode}, expected={expect}\n{proc.stdout}\n{proc.stderr}")


class SecretScannerIntegrationTests(unittest.TestCase):
    def scenario(self):
        repo = PushRepo()
        self.addCleanup(repo.close)
        return repo

    def test_clean_commit_and_worktree_only_secret_pass(self):
        r = self.scenario()
        (r.work / "untracked-secret.txt").write_text(ANTHROPIC, encoding="utf-8")
        r.commit("clean.txt", "clean\n", "clean")
        r.push(expect=0)

    def test_existing_branch_plaintext_is_blocked(self):
        r = self.scenario()
        r.commit("secret.txt", ANTHROPIC, "secret")
        r.push(expect=1)

    def test_new_branch_first_push_is_blocked(self):
        r = self.scenario()
        run(["git", "checkout", "-qb", "feature"], r.work)
        r.commit("secret.txt", ANTHROPIC, "secret")
        r.push("HEAD:refs/heads/feature", expect=1)

    def test_diff_disabled_blob_is_blocked(self):
        r = self.scenario()
        r.commit(".gitattributes", "hidden.bin -diff\n", "attrs")
        r.commit("hidden.bin", ANTHROPIC, "hidden")
        r.push(expect=1)

    def test_nul_binary_blob_is_blocked(self):
        r = self.scenario()
        r.commit("binary.dat", b"\x00prefix\x00" + ANTHROPIC.encode(), "binary")
        r.push(expect=1)

    def test_merge_resolution_blob_is_blocked(self):
        r = self.scenario()
        run(["git", "checkout", "-qb", "feature"], r.work)
        r.commit("conflict.txt", "feature\n", "feature")
        run(["git", "checkout", "main"], r.work)
        r.commit("conflict.txt", "main\n", "main")
        run(["git", "merge", "feature"], r.work, check=False)
        (r.work / "conflict.txt").write_text(ANTHROPIC, encoding="utf-8")
        run(["git", "add", "conflict.txt"], r.work)
        run(["git", "commit", "-qm", "resolve"], r.work)
        r.push(expect=1)

    def test_annotated_tag_message_is_blocked(self):
        r = self.scenario()
        run(["git", "tag", "-a", "v-secret", "-m", ANTHROPIC], r.work)
        r.push("refs/tags/v-secret:refs/tags/v-secret", expect=1)

    def test_whitespace_split_and_base64_are_blocked(self):
        for name, content in (
            ("split", "sk-ant-api03-\n" + "A" * 32),
            ("base64", base64.b64encode(ANTHROPIC.encode()).decode()),
        ):
            with self.subTest(name=name):
                r = self.scenario()
                r.commit(f"{name}.txt", content, name)
                r.push(expect=1)

    def test_additional_provider_patterns_are_blocked(self):
        for name, value in (("aws", AWS), ("github", GITHUB), ("google", GOOGLE)):
            with self.subTest(name=name):
                r = self.scenario()
                r.commit(f"{name}.txt", value, name)
                r.push(expect=1)


class RuntimeAttackSurfaceTests(unittest.TestCase):
    def test_public_worker_has_no_unauthenticated_mail_relay(self):
        source = (ROOT / "worker" / "index.js").read_text(encoding="utf-8")
        self.assertNotIn("/api/audio-email", source)
        self.assertNotIn("RESEND_API_KEY", source)

    def test_embedding_proxy_is_same_origin_and_rate_limited(self):
        source = (ROOT / "worker" / "index.js").read_text(encoding="utf-8")
        self.assertIn("EMBED_RATE_LIMITER", source)
        self.assertIn("Cross-origin requests are not allowed", source)
        self.assertNotIn('"Access-Control-Allow-Origin", "*"', source)
        self.assertIn("frame-ancestors 'none'", source)

    def test_local_server_defaults_to_loopback_and_caps_requests(self):
        source = (ROOT / "pipeline" / "serve_local.py").read_text(encoding="utf-8")
        self.assertIn('default="127.0.0.1"', source)
        self.assertIn("MAX_REQUEST_BYTES", source)
        self.assertIn("cross-origin request rejected", source)

    def test_browser_keys_are_not_persisted_or_put_in_google_urls(self):
        sources = [
            (ROOT / "pipeline" / "build_topic_index.py").read_text(encoding="utf-8"),
            (ROOT / "pipeline" / "lib" / "audio_overview.py").read_text(encoding="utf-8"),
        ]
        joined = "\n".join(sources)
        for slot in ("_LLM_KEY", "_ANTHROPIC_KEY", "_OPENAI_KEY", "_GEMINI_KEY"):
            self.assertNotIn(f"localStorage.setItem('{slot}'", joined)
            self.assertNotIn(f'localStorage.setItem("{slot}"', joined)
        self.assertNotRegex(joined, r'googleapis\.com[^"\'\s]*[?&]key=')

    def test_local_only_model_caches_are_excluded_from_deploy(self):
        ignored = (ROOT / "docs" / ".assetsignore").read_text(encoding="utf-8")
        for pattern in ("**/_embeddings_cache.json", "**/_hdbscan_model.joblib"):
            self.assertIn(pattern, ignored)
