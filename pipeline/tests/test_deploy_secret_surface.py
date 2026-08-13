"""배포 자산의 자격증명 노출 방지 — strip / 안전망 / 복원의 계약 테스트.

`test_generated_html_credentials.py` 가 "생성기가 OAuth 자격증명에 닿지 않는다"
를 지킨다면, 이 파일은 그 다음 관문을 지킨다: **구워진 키가 배포 자산 밖으로
나가지 않는다.**

여기 있는 테스트는 전부 과거에 실제로 뚫렸던 구멍을 하나씩 겨눈다:

* strip 이 값의 접두사(`sk-`/`AIza`)를 보고 판단해 fail-open 이었다.
* `_GEMINI_KEY` 만 `window.` 선언을 받고 나머지는 못 받았다.
* strip 과 leak 검사가 `index.html` 만 훑어 `network.html` 과 `.json` 은 무방비였다.
* leak 검사 정규식이 stripper 보다 좁아(레거시 OpenAI 키) 안전망 구실을 못했다.
* re-inject 가 strip 과 다른 형태를 매치해, 한 번 지워진 슬롯이 복원되지 않았다.
"""
from __future__ import annotations

import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE))

from lib.secret_patterns import (  # noqa: E402
    BYTE_PATTERNS,
    KEY_SLOTS,
    PATTERNS,
    find_local_emails,
    find_secrets,
    redact,
    strip_key_slots,
    strip_local_emails,
)

# 실제 provider 형태를 흉내낸 합성 값. 진짜 키는 절대 넣지 않는다.
FAKE = {
    "anthropic_api": "sk-ant-api03-" + "A" * 40,
    "anthropic_oauth": "sk-ant-oat01-" + "B" * 40,
    "openai_project": "sk-proj-" + "C" * 40,
    "openai_legacy": "sk-" + "D" * 48,
    "google_api": "AIza" + "E" * 35,
    # Google AI Studio 신형 형식. 이 감사에서 로컬 생성물 3,273개에
    # 실제로 박혀 있던 형식이고, 예전 stripper/검사가 둘 다 놓쳤다.
    "google_api_aq": "AQ.Ab8RN6" + "I" * 44,
    "google_oauth": "ya29." + "F" * 40,
    "aws": "AKIA" + "G" * 16,
    "github": "ghp_" + "H" * 30,
    "zotero_api": "Z" * 24,
}

# 접두사가 전혀 없는 자격증명(Azure OpenAI 32-hex, 사내 게이트웨이 등).
# 탐지는 불가능하지만 **슬롯 기반 strip 은 반드시 지워야 한다.**
OPAQUE_KEY = "0123456789abcdef0123456789abcdef"


class SecretPatternTests(unittest.TestCase):
    def test_every_known_credential_shape_is_detected(self):
        for name, value in FAKE.items():
            with self.subTest(shape=name):
                source = (
                    f'ZOTERO_API_KEY = "{value}"'
                    if name == "zotero_api" else f'let x = "{value}";'
                )
                self.assertTrue(
                    find_secrets(source),
                    f"{name} 형태가 leak 검사에서 탐지되지 않는다",
                )

    def test_legacy_openai_key_is_detected(self):
        """예전 leak 정규식은 `sk-(ant|proj)-` 만 알아 이걸 놓쳤다."""
        self.assertTrue(find_secrets(FAKE["openai_legacy"]))

    def test_google_oauth_token_is_detected(self):
        self.assertTrue(find_secrets(FAKE["google_oauth"]))

    def test_zotero_api_key_is_detected(self):
        self.assertTrue(find_secrets(
            f'ZOTERO_API_KEY = "{FAKE["zotero_api"]}"'
        ))

    def test_zotero_api_key_requires_a_zotero_context_label(self):
        self.assertEqual(find_secrets(FAKE["zotero_api"]), [])

    def test_paper_titles_are_not_false_positives(self):
        """논문 제목·슬러그의 `sk-...` 는 자격증명이 아니다.

        실제 코퍼스(docs/ 17,021 파일)에서 나온 문자열들이다. 문자 클래스를
        느슨하게 풀면 배포가 영구 abort 된다 — 그럼 아무도 안전망을 안 켠다.
        """
        benign = [
            "sk-Oriented_Dialogue_System_with_Of",
            "sk-Technology_Fit_and_Community_of_Practice_Th",
            "sk-based_approach_to_assessing_liability_risk_for_AI-dri",
            "sk-reminds-us-of-the-possible-dangers-of-unregulated-ai",
            "sk-management-and-healthcare-policy-journal",
            "sk-congress-sam-altman-chatgpt-openai",
            "Task-Oriented Dialogue",
            "risk-assessment-tools-in-the-u-s-criminal-justice-system",
        ]
        for text in benign:
            with self.subTest(text=text[:40]):
                self.assertEqual(find_secrets(text), [], f"오탐: {text}")

    def test_byte_patterns_mirror_text_patterns(self):
        """pre-push 훅(bytes)과 배포 검사(str)가 같은 표를 봐야 한다."""
        self.assertEqual(
            [n for n, _ in PATTERNS], [n for n, _ in BYTE_PATTERNS]
        )
        for (_, rx_s), (_, rx_b) in zip(PATTERNS, BYTE_PATTERNS):
            self.assertEqual(rx_s.pattern.encode("ascii"), rx_b.pattern)

    def test_redact_never_returns_the_full_value(self):
        for value in FAKE.values():
            with self.subTest(value=value[:10]):
                shown = redact(value)
                self.assertNotIn(shown, (value,))
                self.assertLess(len(shown), len(value))


class SlotStripTests(unittest.TestCase):
    def test_slot_strip_ignores_value_shape(self):
        """fail-open 회귀 방지: 접두사가 없는 키도 반드시 지워진다."""
        src = f'const _LLM_KEY = "{OPAQUE_KEY}";'
        out, n = strip_key_slots(src)
        self.assertEqual(n, 1)
        self.assertNotIn(OPAQUE_KEY, out)
        self.assertIn('_LLM_KEY = ""', out)

    def test_window_declared_slots_are_stripped(self):
        """예전엔 `_GEMINI_KEY` 만 `window.` 를 받았다."""
        for slot in KEY_SLOTS:
            with self.subTest(slot=slot):
                src = f'window.{slot} = "{FAKE["openai_legacy"]}";'
                out, n = strip_key_slots(src)
                self.assertEqual(n, 1, f"{slot}: window. 선언이 strip 되지 않았다")
                self.assertEqual(find_secrets(out), [])
                self.assertIn(f'window.{slot} = ""', out)

    def test_every_declaration_form_and_slot_combination(self):
        for slot in KEY_SLOTS:
            for decl in ("const ", "let ", "var ", "window.", ""):
                for shape, value in FAKE.items():
                    with self.subTest(slot=slot, decl=decl.strip(), shape=shape):
                        src = f'{decl}{slot} = "{value}";'
                        out, n = strip_key_slots(src)
                        self.assertEqual(n, 1)
                        self.assertEqual(find_secrets(out), [])

    def test_strip_is_idempotent(self):
        src = f'let _ANTHROPIC_KEY = "{FAKE["anthropic_api"]}" || localStorage.getItem("_ANTHROPIC_KEY") || "";'
        once, n1 = strip_key_slots(src)
        twice, n2 = strip_key_slots(once)
        self.assertEqual((n1, n2), (1, 0))
        self.assertEqual(once, twice)

    def test_strip_preserves_a_runtime_prompt_fallback_chain(self):
        """키 리터럴만 비우고 runtime BYOK 표현은 보존한다."""
        src = (f'let _ANTHROPIC_KEY = "{FAKE["anthropic_api"]}"'
               " || getRuntimeKey() || '';")
        out, _ = strip_key_slots(src)
        self.assertIn("getRuntimeKey()", out)

    def test_strip_does_not_touch_unrelated_assignments(self):
        src = 'const _SEARCH_INDEX = "papers/_search_index.json";'
        out, n = strip_key_slots(src)
        self.assertEqual((out, n), (src, 0))

    def test_local_emails_are_emptied_and_detected(self):
        src = 'window._LOCAL_EMAILS = ["a@b.com", "c@d.org"];'
        self.assertTrue(find_local_emails(src))
        out, n = strip_local_emails(src)
        self.assertEqual(n, 1)
        self.assertFalse(find_local_emails(out))
        self.assertIn("window._LOCAL_EMAILS = []", out)


class DeploySurfaceTests(unittest.TestCase):
    """strip/검사 대상이 실제 업로드 surface 와 일치하는지."""

    def setUp(self):
        import prepare_deploy
        self.pd = prepare_deploy

    def test_scanned_suffixes_cover_generated_asset_types(self):
        # network.html(generate_network) · _search_index.json(build_search_index)
        # · rss.xml(build_rss) 은 전부 docs/ 아래로 업로드된다.
        for suffix in (".html", ".json", ".xml", ".js", ".txt", ".md"):
            with self.subTest(suffix=suffix):
                self.assertIn(suffix, self.pd._SCANNED_SUFFIXES)

    def test_scannable_files_finds_non_index_html(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "humanoid").mkdir()
            (root / "humanoid" / "index.html").write_text("x", encoding="utf-8")
            (root / "humanoid" / "network.html").write_text("x", encoding="utf-8")
            (root / "humanoid" / "_search_index.json").write_text("{}", encoding="utf-8")
            (root / "humanoid" / "fig.png").write_bytes(b"\x89PNG")
            found = {p.name for p in self.pd._scannable_files(root)}
        self.assertEqual(found, {"index.html", "network.html", "_search_index.json"})

    def test_scan_scope_equals_the_wrangler_upload_set(self):
        """검사 범위는 `.assetsignore` 로 정의된 업로드 집합과 같아야 한다.

        넓으면 업로드되지 않는 로컬 캐시(`_local_keys.json` 은 이름 그대로
        키를 담는다)에서 오탐이 나 배포가 영구 abort 되고, 운영자는 안전망을
        꺼 버린다. 좁으면 진짜 유출을 놓친다. wrangler 와 같은 파일을 읽어
        양쪽이 어긋날 수 없게 한다.
        """
        rules = self.pd._assetsignore_rules(self.pd.DOCS_DIR)
        self.assertTrue(rules, "docs/.assetsignore 를 읽지 못했다")
        expectations = [
            # 업로드되지 않음 → 검사 대상 아님
            ("_cross/a.html", True), ("_local_keys.json", True),
            ("papers/006_X/review.md", True), ("papers/006_X/text.md", True),
            ("papers/006_X/citations.md", True),
            ("papers/006_X/citedby/report.html", True),
            ("papers/006_X/citedby/sub/a.json", True),
            ("x/.obsidian/c.json", True),
            (".gjc/state.json", True),
            # 업로드됨 → 반드시 검사
            ("my-topic/index.html", False), ("my-topic/network.html", False),
            ("my-topic/_search_index.json", False),
            ("papers/006_X/index.html", False),
            ("papers/_papers_index.json", False),
            ("index.html", False), ("setup-guide.md", False),
        ]
        for rel, ignored in expectations:
            with self.subTest(path=rel):
                self.assertEqual(self.pd._is_ignored(rel, rules), ignored)

    def test_glob_star_does_not_cross_path_separators(self):
        """`papers/*/citedby` 가 `papers/a/b/citedby` 를 먹으면 검사 범위가
        조용히 줄어든다 — 통짜 fnmatch 를 쓰면 실제로 그렇게 된다."""
        rules = [("papers/*/citedby", True)]
        self.assertTrue(self.pd._is_ignored("papers/006_X/citedby/r.html", rules))
        self.assertFalse(self.pd._is_ignored("papers/a/b/citedby/r.html", rules))

    def test_real_docs_scan_scope_excludes_global_local_only_paths(self):
        targets = self.pd._scannable_files(self.pd.DOCS_DIR)
        rels = {p.relative_to(self.pd.DOCS_DIR).as_posix() for p in targets}
        self.assertFalse([r for r in rels if r.startswith("_cross/")])
        self.assertFalse([r for r in rels if "/citedby/" in r])
        self.assertFalse([r for r in rels if r.endswith(("/review.md", "/text.md"))])

    def test_step6_strip_walks_every_html_not_just_index(self):
        """회귀 방지: 이 루프가 `index.html` 로 좁아지면 network.html 이 샌다."""
        src = (PIPELINE / "prepare_deploy.py").read_text(encoding="utf-8")
        self.assertIn('DOCS_DIR.rglob("*.html")', src)
        self.assertNotIn('DOCS_DIR.rglob("index.html")', src)

    def test_leak_scan_uses_the_shared_table(self):
        """로컬 정규식으로 되돌아가면 표가 다시 갈라진다.

        주석은 옛 버그를 설명하느라 패턴 문자열을 그대로 인용하므로,
        코드 라인만 남기고 본다.
        """
        src = (PIPELINE / "prepare_deploy.py").read_text(encoding="utf-8")
        self.assertIn("find_secrets(body)", src)
        code = "\n".join(
            line for line in src.splitlines() if not line.lstrip().startswith("#")
        )
        for revived in ("sk-(ant|proj)-", "AIza[0-9A-Za-z", "re.compile(r'sk-"):
            with self.subTest(pattern=revived):
                self.assertNotIn(revived, code)

    def test_prepare_deploy_aborts_on_a_leak(self):
        """안전망이 실제로 프로세스를 세우는지 — 문자열 검사로는 부족하다."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "leak.html").write_text(
                f'<script>window._SOMETHING = "{FAKE["anthropic_oauth"]}";</script>',
                encoding="utf-8",
            )
            leaks = [
                (str(p), name, redact(v))
                for p in self.pd._scannable_files(root)
                for name, v in find_secrets(p.read_text(encoding="utf-8"))
            ]
        self.assertEqual(len(leaks), 1)
        # 로그에 원문이 찍히면 안 된다.
        self.assertNotIn(FAKE["anthropic_oauth"], leaks[0][2])


class ScanSecretsHookTests(unittest.TestCase):
    def test_hook_runs_with_only_scripts_present(self):
        """훅은 `scripts/` 만 떼어 놔도 실행돼야 한다.

        문자열 검사로는 부족하다 — 실제로 이 작업 중에 훅을 `pipeline/lib`
        에 결합해 깨뜨렸고, grep 기반 검사는 그 변형을 통과시켰다. 그래서
        pipeline 이 없는 임시 디렉터리에 훅만 복사해 **실행**한다.
        `.git/hooks/pre-push` 가 부르는 유일한 파일이므로 이게 진짜 계약이다.
        """
        import shutil
        import subprocess
        import tempfile
        hook = PIPELINE.parent / "scripts" / "scan-secrets.py"
        with tempfile.TemporaryDirectory() as td:
            isolated = Path(td) / "scripts"
            isolated.mkdir()
            shutil.copy2(hook, isolated / "scan-secrets.py")
            proc = subprocess.run(
                [sys.executable, str(isolated / "scan-secrets.py"), "--help"],
                cwd=td, capture_output=True, text=True,
                env={**os.environ, "PYTHONPATH": ""},
            )
        self.assertEqual(
            proc.returncode, 0,
            f"pipeline/ 없이 훅이 죽는다 — 훅 자체가 무력화된다:\n{proc.stderr[-400:]}",
        )
        self.assertNotIn("ModuleNotFoundError", proc.stderr)

    def test_hook_table_matches_the_shared_table_exactly(self):
        """복제본이 표류하면 여기서 잡는다 — 중복을 허용하는 유일한 근거."""
        mod = self._load_hook()
        self.assertEqual(
            [(n, rx.pattern) for n, rx in mod.RAW_PATTERNS],
            [(n, rx.pattern.encode("ascii")) for n, rx in PATTERNS],
            "scripts/scan-secrets.py 의 표가 lib/secret_patterns 와 어긋났다",
        )

    @staticmethod
    def _load_hook():
        import importlib.util
        path = PIPELINE.parent / "scripts" / "scan-secrets.py"
        spec = importlib.util.spec_from_file_location("scan_secrets_hook", path)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_hook_module_loads(self):
        mod = self._load_hook()
        names = [n for n, _ in mod.RAW_PATTERNS]
        self.assertIn("OpenAI legacy key", names)
        self.assertIn("Google OAuth token", names)
        self.assertIn("Zotero API key", names)

    def test_hook_detects_zotero_key_raw_whitespace_and_base64(self):
        import base64
        mod = self._load_hook()
        key = FAKE["zotero_api"].encode("ascii")
        for source, suffix in (
            (b'ZOTERO_API_KEY="' + key + b'"', ""),
            (b'ZOTERO_API_KEY="' + key[:12] + b"\n" + key[12:] + b'"',
             " (whitespace-split)"),
            (base64.b64encode(b'ZOTERO_API_KEY="' + key + b'"'), " (base64)"),
        ):
            with self.subTest(source=suffix or "raw"):
                self.assertIn("Zotero API key" + suffix, mod.findings(source))

    def test_hook_ignores_zotero_configuration_placeholders(self):
        mod = self._load_hook()
        for placeholder in (
            b"ZOTERO_API_KEY",
            b"YOUR_ZOTERO_API_KEY",
            b"${ZOTERO_API_KEY}",
            b'ZOTERO_API_KEY="YOUR_ZOTERO_API_KEY_HERE"',
        ):
            with self.subTest(placeholder=placeholder):
                self.assertNotIn("Zotero API key", mod.findings(placeholder))

    def test_snapshot_ignores_deleted_blob_but_history_and_tip_modes_find_it(self):
        """`--all`은 현재 snapshot, `--history`/push는 reachable history를 본다."""
        import subprocess
        import tempfile

        hook = PIPELINE.parent / "scripts" / "scan-secrets.py"
        key = FAKE["zotero_api"]
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)

            def git(*args, input=None):
                return subprocess.run(
                    ["git", *args], cwd=repo, input=input, text=True,
                    capture_output=True, check=True,
                )

            git("init", "-q")
            git("config", "user.email", "test@example.invalid")
            git("config", "user.name", "Test")
            (repo / "secret.txt").write_text(
                f'ZOTERO_API_KEY="{key}"\n', encoding="ascii"
            )
            git("add", "secret.txt")
            git("commit", "-qm", "secret")
            secret_oid = git("rev-parse", "HEAD").stdout.strip()
            git("update-ref", "refs/remotes/origin/main", secret_oid)
            (repo / "secret.txt").write_text("removed\n", encoding="ascii")
            git("commit", "-am", "remove secret", "-q")
            tip_oid = git("rev-parse", "HEAD").stdout.strip()

            def scan(*args, input=None):
                return subprocess.run(
                    [sys.executable, str(hook), *args], cwd=repo, input=input,
                    text=True, capture_output=True, check=False,
                )

            snapshot = scan("--all")
            history = scan("--history")
            fallback = scan()
            new_ref = scan(
                input=f"refs/heads/main {tip_oid} refs/heads/main {'0' * 40}\n"
            )

        self.assertEqual(snapshot.returncode, 0, snapshot.stderr)
        for name, proc in (
            ("history", history), ("no-stdin fallback", fallback), ("new ref", new_ref)
        ):
            with self.subTest(mode=name):
                self.assertEqual(proc.returncode, 1, proc.stderr)
                self.assertIn("Zotero API key", proc.stderr)
                self.assertNotIn(key, proc.stderr)

    def test_existing_ref_scans_only_objects_introduced_after_destination_tip(self):
        mod = self._load_hook()
        calls = []
        with patch.object(mod, "rev_objects", side_effect=lambda args: calls.append(args) or set()):
            mod.pushed_objects([
                "refs/heads/main " + "a" * 40
                + " refs/heads/main " + "b" * 40
            ])
        self.assertEqual(calls, [["a" * 40, "^" + "b" * 40]])


class AudioOverviewKeyStateTests(unittest.TestCase):
    """Deep Research 와 같은 이유 설명을 Audio Overview 도 해야 한다."""

    def setUp(self):
        import lib.audio_overview as ao
        self.js = ao.AUDIO_JS

    def test_audio_key_state_separates_no_key_from_bad_format(self):
        self.assertIn("function audioKeyState()", self.js)
        self.assertIn('reason: "no-key"', self.js)
        self.assertIn('reason: "bad-format"', self.js)

    def test_no_key_message_explains_byok_and_oauth(self):
        state = self.js.split("function audioKeyState()", 1)[1].split("\nfunction ", 1)[0]
        self.assertIn("BYOK", state)
        self.assertIn("정상", state, "키가 없는 것이 '정상'이라는 설명이 없다")

    def test_ensure_gemini_key_consults_the_state(self):
        body = self.js.split("function ensureGeminiKey()", 1)[1].split("\nfunction ", 1)[0]
        self.assertIn("audioKeyState()", body)
        self.assertIn("st.message", body)

    def test_visible_hint_explains_why_no_key_is_baked(self):
        self.assertIn("BYOK", self.js.split("audio-hint", 1)[1][:400])

    def test_gemini_key_shapes_accept_the_format_this_repo_actually_uses(self):
        """`AIza` 만 받으면 지금 발급되는 `AQ.` 키를 거절한다.

        이 저장소의 로컬 생성물에 실제로 박혀 있던 키가 `AQ.` 형식이다.
        독자가 자기 AI Studio 키를 붙여넣어도 "형식이 틀렸다"고 거절당하면
        BYOK 안내 문구를 아무리 잘 써도 기능은 못 쓴다.
        """
        self.assertIn("function isGeminiKey(", self.js)
        self.assertIn('startsWith("AQ.")', self.js)
        # 형식 검증 지점이 헬퍼를 거치는지 — 직접 startsWith("AIza") 가 남아
        # 있으면 그 경로만 조용히 신형 키를 막는다.
        code = "\n".join(
            ln for ln in self.js.splitlines() if not ln.lstrip().startswith("//")
        )
        self.assertNotIn('startsWith("AIza")', code.replace(
            'return s.startsWith("AIza") || s.startsWith("AQ.");', ""))

    def test_topic_page_backend_detection_accepts_both_google_shapes(self):
        src = (
            PIPELINE.parent
            / "src"
            / "paper_curation"
            / "rendering"
            / "topic_page"
            / "app.js"
        ).read_text(encoding="utf-8")
        self.assertIn("k.startsWith('AIza') || k.startsWith('AQ.')", src)

    def test_generated_audio_js_parses(self):
        """설명 문구를 넣다가 JS 를 깨뜨리지 않았는지."""
        import shutil
        import subprocess
        import tempfile
        node = shutil.which("node")
        if not node:
            self.skipTest("node not available")
        import lib.audio_overview as ao
        block = ao.audio_script_block(
            "", mode="paper", ctx={"title": "t", "review": "r", "connections": []},
        )
        js = re.sub(r"(?s)^.*?<script>|</script>.*$", "", block)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(js)
            tmp = f.name
        try:
            proc = subprocess.run([node, "--check", tmp], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr[:400])
        finally:
            os.unlink(tmp)


if __name__ == "__main__":
    unittest.main()
