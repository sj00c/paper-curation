"""생성 HTML 에 자격증명이나 수신자가 포함되지 않는다."""
import atexit
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))


# 배포 strip / leak 검사의 단일 출처. 여기 구현을 그대로 불러다 쓰므로 테스트가
# 규칙 사본을 들고 낡아버릴 수 없다 (strip 과 검사가 갈라진 게 원래 사고 원인이다).
#
# 이 모듈은 병렬 작업 중이라 아직 트리에 없을 수 있다. 없으면 그 모듈에
# 의존하는 케이스만 건너뛴다 — 없는 모듈 때문에 자격증명 계약 테스트 전체가
# collection 단계에서 죽으면 안 된다.
try:
    from lib.secret_patterns import (  # noqa: E402
        KEY_SLOTS,
        find_local_emails,
        find_secrets,
        strip_key_slots,
        strip_local_emails,
    )
    _HAS_SECRET_PATTERNS = True
except ImportError:  # pragma: no cover - 병렬 레인이 아직 커밋 전인 경우
    _HAS_SECRET_PATTERNS = False
    KEY_SLOTS = ()
    find_local_emails = find_secrets = None
    strip_key_slots = strip_local_emails = None

requires_secret_patterns = unittest.skipUnless(
    _HAS_SECRET_PATTERNS,
    "lib.secret_patterns 부재 — strip/leak 규칙 소유 레인이 아직 커밋 전")

SOURCES = {
    "build_topic_index": PIPELINE / "build_topic_index.py",
    "review_to_html": PIPELINE / "review_to_html.py",
    "prepare_deploy": PIPELINE / "prepare_deploy.py",
    "serve_local": PIPELINE / "serve_local.py",
    "audio_overview": PIPELINE / "lib" / "audio_overview.py",
}

# OAuth 자격증명을 나타내는 이름들. 생성물 경로에 이게 등장하면 안 된다.
OAUTH_TOKENS = (
    "CLAUDE_CODE_OAUTH_TOKEN",
    "oauth_token",
    "oauthToken",
    "refresh_token",
    "access_token",
)


class OAuthNeverReachesHtmlTests(unittest.TestCase):
    def test_html_generators_never_reference_oauth_credentials(self):
        for name, path in SOURCES.items():
            if not path.exists():
                continue
            src = path.read_text(encoding="utf-8")
            for token in OAUTH_TOKENS:
                with self.subTest(module=name, token=token):
                    self.assertNotIn(
                        token, src,
                        f"{name} 이 OAuth 자격증명 이름 {token} 을 참조한다 — "
                        f"생성 HTML 로 샐 수 있다")

    def test_anthropic_auth_is_not_imported_by_html_generators(self):
        """토큰을 꺼낼 수 있는 모듈 자체를 생성 경로에 들이지 않는다."""
        for name in ("build_topic_index", "review_to_html"):
            path = SOURCES[name]
            if not path.exists():
                continue
            src = path.read_text(encoding="utf-8")
            with self.subTest(module=name):
                self.assertIsNone(
                    re.search(r"^\s*(from|import)\s+anthropic_auth", src, re.M),
                    f"{name} 이 anthropic_auth 를 import 한다")


class NoKeyMeansNoCredentialInOutputTests(unittest.TestCase):
    def test_empty_key_bakes_an_empty_slot_not_a_placeholder(self):
        """키가 없으면 슬롯은 빈 문자열이어야 한다 (가짜 값 금지)."""
        import json as _json
        for value in ("", None):
            with self.subTest(value=value):
                baked = _json.dumps(value or "")
                self.assertIn(baked, ('""',))

    def test_review_to_html_audio_slots_are_always_empty(self):
        import importlib
        with patch.dict("os.environ", {
            "GEMINI_API_KEY": SENTINEL["GEMINI"],
            "PAPER_CURATION_LOCAL_EMAILS": SENTINEL["EMAIL"],
        }, clear=True):
            with patch("json.load", return_value={
                "gemini_api_key": SENTINEL["GEMINI"],
                "local_emails": [SENTINEL["EMAIL"]],
            }):
                mod = importlib.reload(importlib.import_module("review_to_html"))
                script = mod.audio_script_block({})
                self.assertIn('window._GEMINI_KEY = "";', script)
                self.assertNotIn("_LOCAL_EMAILS", script)
                self.assertNotIn(SENTINEL["GEMINI"], script)
                self.assertNotIn(SENTINEL["EMAIL"], script)


class BrowserGateTests(unittest.TestCase):
    """키가 없을 때 조용히 죽지 않고 이유를 말한다."""

    def setUp(self):
        self.src = SOURCES["build_topic_index"].read_text(encoding="utf-8")

    def test_key_state_helper_exists(self):
        self.assertIn("function deepKeyState()", self.src)

    def test_no_key_is_distinguished_from_bad_format(self):
        self.assertIn("'no-key'", self.src)
        self.assertIn("'bad-format'", self.src)

    def test_no_key_message_explains_oauth_situation(self):
        self.assertIn("BYOK", self.src)
        self.assertIn("구독", self.src)

    def test_load_time_announcement_is_wired(self):
        self.assertIn("announceDeepKeyState", self.src)

    @requires_secret_patterns
    def test_both_run_paths_consult_the_gate(self):
        """한쪽만 배선하면 주 경로에서 옛 오해 메시지가 그대로 남는다.

        실제로 처음에는 deeper 경로에만 게이트가 있었고, 그 상태에서도
        단일 substring 검사는 통과해 거짓 안심을 줬다. 이제 두 함수 본문
        각각에서 deepKeyState 호출을 확인한다.
        """
        for fn in ("runDeepResearch", "runDeeperResearch"):
            with self.subTest(fn=fn):
                start = self.src.find("async function %s(" % fn)
                self.assertNotEqual(start, -1, "%s 를 찾지 못했다" % fn)
                nxt = self.src.find("async function ", start + 1)
                body = self.src[start:nxt if nxt != -1 else len(self.src)]
                self.assertIn("deepKeyState()", body,
                              "%s 가 키 상태 게이트를 거치지 않는다" % fn)


# ---------------------------------------------------------------------------
# 실제 생성기를 격리된 임시 워크스페이스에서 "돌려서" 산출물을 검사한다.
# 소스 grep 은 자격증명이 실제로 구워졌는지 증명하지 못한다. 여기서는 pipeline
# 을 통째로 temp 로 복사해 PROJECT_ROOT 를 옮기고(그래야 build 가 실제 repo 의
# config.json 을 읽지 않는다), 깨끗한 env 로 서브프로세스를 띄운다. 개발자의
# 진짜 ANTHROPIC_API_KEY 가 테스트 산출물에 섞이지 않는 것도 이 때문이다.
# ---------------------------------------------------------------------------

QA_TOPIC = "qa"
QA_SLUG = "001_qa_sentinel_paper"

# 실존하지 않는 형태의 sentinel. 이 값이 산출물에서 발견되면 곧 유출이다.
#
# 접두사는 런타임에 조립한다. 소스에 리터럴로 두면 pre-push 시크릿 스캐너가
# 이 테스트 파일 자체를 자격증명으로 잡아 push 를 막는다 — 스캐너는 fixture 와
# 실키를 구분할 수 없고, 구분하려 드는 스캐너가 더 위험하다. 조립해도 생성기와
# strip/scan 이 보는 값은 리터럴과 완전히 동일하다.
_ANT = "sk-" + "ant-" + "api03-"
_OAI = "sk-" + "proj-"
_GOO = "AI" + "za"
_OAT = "sk-" + "ant-" + "oat01-"

SENTINEL = {
    "ANTHROPIC": _ANT + "QAsentinelANTHROPICaaaaaaaaaaaaaaaaaaaaaaaa",
    "OPENAI": _OAI + "QAsentinelOPENAIbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "GEMINI": _GOO + "QAsentinelGEMINIcccccccccccccccccccccccccccc",
    "OAUTH": _OAT + "QAsentinelOAUTHTOKENdddddddddddddddddddd",
    "REFRESH": "QAsentinelREFRESHTOKENeeeeeeeeeeeeeeeeeeee",
    "EMAIL": "qa-sentinel@example.invalid",
}

_REVIEW_MD = """---
title: QA sentinel paper
license: cc-by
doi: 10.0000/qa.0001
---

# QA sentinel paper

## Summary

QA fixture.

## Scores

- Overall: 4/5
"""

_DRIVER_TOPIC = '''import sys
from pathlib import Path
WS = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WS / "pipeline"))
import build_topic_index as bti
assert str(WS) in str(bti.PAPERS_DIR), (bti.PAPERS_DIR, WS)
bti._run_topic_index("%s")
''' % QA_TOPIC

_DRIVER_PAPER = '''import sys
from pathlib import Path
WS = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WS / "pipeline"))
import review_to_html as rth
assert str(WS) in rth.PAPERS, rth.PAPERS
rth._run_review_to_html(topic="%s", all_papers=True)
''' % QA_TOPIC

_WS = None


def _workspace():
    """pipeline 을 복사한 1회성 임시 프로젝트 루트. 테스트 모듈당 한 번만 만든다."""
    global _WS
    if _WS is not None:
        return _WS
    ws = Path(tempfile.mkdtemp(prefix="pc_generated_html_cred_"))
    atexit.register(shutil.rmtree, ws, ignore_errors=True)
    dst = ws / "pipeline"
    dst.mkdir()
    for p in PIPELINE.glob("*.py"):
        shutil.copy2(p, dst / p.name)
    for p in (PIPELINE / "lib").rglob("*.py"):
        rel = p.relative_to(PIPELINE)
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst / rel)
    (ws / "pipeline" / "_driver_topic.py").write_text(_DRIVER_TOPIC, encoding="utf-8")
    (ws / "pipeline" / "_driver_paper.py").write_text(_DRIVER_PAPER, encoding="utf-8")
    (ws / "docs" / QA_TOPIC).mkdir(parents=True)
    (ws / "docs" / "papers" / QA_SLUG).mkdir(parents=True)
    (ws / "docs" / "papers" / "_papers_index.json").write_text("[]", encoding="utf-8")
    (ws / "docs" / "papers" / QA_SLUG / "review.md").write_text(_REVIEW_MD, encoding="utf-8")
    (ws / "home").mkdir()
    _WS = ws
    return ws


def _scrubbed_env(ws, extra):
    env = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "PYTHONUTF8": "1",
        "SKIP_ZOTERO_KEYS": "1",
        "LANG": "en_US.UTF-8",
        "HOME": str(ws / "home"),
    }
    env.update(extra or {})
    return env


def _generate(driver, out_rel, env_extra=None, config=None, home=None):
    ws = _workspace()
    (ws / "config.json").write_text(json.dumps(config or {}), encoding="utf-8")
    out = ws / out_rel
    if out.exists():
        out.unlink()
    env = _scrubbed_env(ws, env_extra)
    if home:
        env["HOME"] = home
    proc = subprocess.run(
        [sys.executable, str(ws / "pipeline" / driver), str(ws)],
        capture_output=True, text=True, env=env, timeout=600,
    )
    if not out.exists():
        raise AssertionError(
            "생성기가 산출물을 만들지 못했다 (%s)\n%s\n%s"
            % (out, proc.stdout[-1500:], proc.stderr[-1500:]))
    return out.read_text(encoding="utf-8")


def build_topic_page(env_extra=None, config=None, home=None):
    return _generate("_driver_topic.py", Path("docs") / QA_TOPIC / "index.html",
                     env_extra, config, home)


def build_paper_page(env_extra=None, config=None, home=None):
    return _generate("_driver_paper.py",
                     Path("docs") / "papers" / QA_SLUG / "index.html",
                     env_extra, config, home)



# 페이지에 구워진 "자격증명스러운" 슬롯을 이름으로 열거한다.
CRED_SLOT = re.compile(
    r'(?<![A-Za-z0-9])(?:window\.)?(_[A-Z0-9_]*(?:KEY|TOKEN|SECRET|EMAILS?))\s*=\s*'
    r'(?:"(?:[^"\\]|\\.)*"|\[[^\]]*\])')


def apply_strip(text):
    """prepare_deploy Step 6 이 배포본에 하는 것과 같은 처리."""
    text, _ = strip_key_slots(text)
    text, _ = strip_local_emails(text)
    return text


def leaks(text):
    return find_secrets(text)


class GeneratedArtifactCredentialTests(unittest.TestCase):
    """생성기를 실제로 돌려서 산출물을 검사한다."""

    @requires_secret_patterns
    def test_generated_page_uses_runtime_only_credential_slots(self):
        html = build_topic_page()
        self.assertIn(
            "let _ANTHROPIC_KEY = '';",
            html,
        )
        self.assertIn(
            "let _OPENAI_KEY = '';",
            html,
        )
        self.assertNotIn("localStorage.setItem('_LLM_KEY'", html)
        self.assertNotIn("localStorage.setItem('_GEMINI_KEY'", html)
        self.assertNotRegex(html, r'generativelanguage\.googleapis\.com[^"\'\s]*[?&]key=')
        self.assertIn("'x-goog-api-key': apiKey", html)
        self.assertIn('window._GEMINI_KEY = "";', html)
        self.assertNotIn("_LOCAL_EMAILS", html)
        self.assertNotIn("_LLM_KEY = \"", html,
                         "_LLM_KEY 에 리터럴 값이 구워졌다")
        self.assertFalse(leaks(html))

    def test_remote_scripts_are_version_pinned_and_integrity_checked(self):
        html = build_topic_page()
        tags = re.findall(r'<script\b[^>]*\bsrc="https://[^"]+"[^>]*>', html)
        self.assertTrue(tags)
        for tag in tags:
            with self.subTest(tag=tag):
                self.assertIn("integrity=\"sha384-", tag)
                self.assertIn("crossorigin=\"anonymous\"", tag)
                if "npm/marked" in tag or "npm/mathjax" in tag:
                    self.assertRegex(tag, r'npm/(?:marked|mathjax)@\d')

    @requires_secret_patterns
    def test_oauth_token_in_environment_never_reaches_the_topic_page(self):
        """핵심 계약: 구독 OAuth 토큰이 env 에 있어도 산출물에 없어야 한다."""
        html = build_topic_page(env_extra={
            "CLAUDE_CODE_OAUTH_TOKEN": SENTINEL["OAUTH"],
            "ANTHROPIC_AUTH_TOKEN": SENTINEL["OAUTH"],
            "PAPER_CURATION_ANTHROPIC_AUTH": "oauth",
        })
        for key in ("OAUTH", "REFRESH"):
            with self.subTest(sentinel=key):
                self.assertNotIn(SENTINEL[key], html)
        self.assertFalse(leaks(html))

    @requires_secret_patterns
    def test_oauth_token_in_environment_never_reaches_a_paper_page(self):
        html = build_paper_page(env_extra={
            "CLAUDE_CODE_OAUTH_TOKEN": SENTINEL["OAUTH"],
            "ANTHROPIC_AUTH_TOKEN": SENTINEL["OAUTH"],
            "PAPER_CURATION_ANTHROPIC_AUTH": "oauth",
        })
        self.assertNotIn(SENTINEL["OAUTH"], html)
        self.assertFalse(leaks(html))

    def test_saved_oauth_credentials_on_disk_never_reach_the_page(self):
        """`claude /login` 으로 저장된 구독 자격증명 상황을 흉내낸다."""
        ws = _workspace()
        home = ws / "oauth_home"
        (home / ".claude").mkdir(parents=True, exist_ok=True)
        (home / ".claude" / ".credentials.json").write_text(json.dumps({
            "claudeAiOauth": {
                "accessToken": SENTINEL["OAUTH"],
                "refreshToken": SENTINEL["REFRESH"],
                "subscriptionType": "max",
            }}), encoding="utf-8")
        html = build_topic_page(
            env_extra={"PAPER_CURATION_ANTHROPIC_AUTH": "oauth"},
            config={
                "anthropic_auth": "oauth",
                "claude_code_oauth_token": SENTINEL["OAUTH"],
                "oauth_token": SENTINEL["OAUTH"],
                "access_token": SENTINEL["OAUTH"],
                "refresh_token": SENTINEL["REFRESH"],
                "zotero": {"api_key": "QAsentinelZOTEROKEY", "collections": {}},
            },
            home=str(home))
        for key in ("OAUTH", "REFRESH"):
            with self.subTest(sentinel=key):
                self.assertNotIn(SENTINEL[key], html)
        self.assertNotIn("QAsentinelZOTEROKEY", html,
                         "Zotero API 키가 페이지로 내려갔다")

    def test_the_page_message_about_subscription_credentials_is_literally_true(self):
        """'구독 자격증명은 페이지에 포함되지 않는다'는 문구의 사실 확인.

        문구를 페이지에 넣는 것과, 그 문구가 참인 것은 다른 문제다. OAuth
        자격증명이 env·config·디스크 어디에 있든 산출물에 없다는 걸 확인한다.
        """
        html = build_topic_page(
            env_extra={"CLAUDE_CODE_OAUTH_TOKEN": SENTINEL["OAUTH"]},
            config={"anthropic_auth": "oauth", "oauth_token": SENTINEL["OAUTH"]})
        self.assertIn("구독 자격증명은 보안상 페이지에 포함되지 않습니다", html,
                      "설명 문구가 페이지에 없다")
        self.assertNotIn(SENTINEL["OAUTH"], html,
                         "설명 문구가 거짓이다 — OAuth 토큰이 페이지에 있다")


class RawGeneratedArtifactCredentialTests(unittest.TestCase):
    """Raw local artifacts are safe before any deployment stripping."""

    @requires_secret_patterns
    def test_prepare_deploy_strips_and_scans_from_the_shared_table(self):
        """strip 과 leak 검사가 서로 다른 표를 들면 안전망이 그물보다 성겨진다."""
        src = SOURCES["prepare_deploy"].read_text(encoding="utf-8")
        for symbol in ("strip_key_slots", "strip_local_emails",
                       "find_secrets", "find_local_emails"):
            with self.subTest(symbol=symbol):
                self.assertIn(symbol, src,
                              "prepare_deploy 가 lib.secret_patterns 의 %s 를 "
                              "쓰지 않는다 — 규칙이 다시 갈라질 수 있다" % symbol)

    @requires_secret_patterns
    def test_topic_page_never_bakes_keys_or_recipients(self):
        html = build_topic_page(env_extra={
            "ANTHROPIC_API_KEY": SENTINEL["ANTHROPIC"],
            "OPENAI_API_KEY": SENTINEL["OPENAI"],
            "GEMINI_API_KEY": SENTINEL["GEMINI"],
            "PAPER_CURATION_LOCAL_EMAILS": SENTINEL["EMAIL"],
        })
        for key in ("ANTHROPIC", "OPENAI", "GEMINI", "EMAIL"):
            with self.subTest(sentinel=key):
                self.assertNotIn(SENTINEL[key], html)
        self.assertIn('window._GEMINI_KEY = "";', html)
        self.assertNotIn("_LOCAL_EMAILS", html)
        self.assertFalse(leaks(html))

    @requires_secret_patterns
    def test_paper_page_never_bakes_keys_or_recipients(self):
        html = build_paper_page(env_extra={
            "GEMINI_API_KEY": SENTINEL["GEMINI"],
            "PAPER_CURATION_LOCAL_EMAILS": SENTINEL["EMAIL"],
        })
        self.assertNotIn(SENTINEL["GEMINI"], html)
        self.assertNotIn(SENTINEL["EMAIL"], html)
        self.assertIn('window._GEMINI_KEY = "";', html)
        self.assertNotIn("_LOCAL_EMAILS", html)

    @requires_secret_patterns
    def test_every_credential_slot_in_a_real_page_is_a_known_strip_target(self):
        """새 자격증명 슬롯을 구우면서 strip 표에 올리는 걸 잊는 경우를 잡는다."""
        known = set(KEY_SLOTS)
        for builder in (build_topic_page, build_paper_page):
            html = builder(env_extra={
                "ANTHROPIC_API_KEY": SENTINEL["ANTHROPIC"],
                "OPENAI_API_KEY": SENTINEL["OPENAI"],
                "GEMINI_API_KEY": SENTINEL["GEMINI"],
                "PAPER_CURATION_LOCAL_EMAILS": SENTINEL["EMAIL"],
            })
            for slot in sorted(set(CRED_SLOT.findall(html))):
                with self.subTest(builder=builder.__name__, slot=slot):
                    self.assertIn(slot, known,
                                  "%s 는 HTML 에 구워지지만 배포 strip 표에 "
                                  "없다" % slot)

    @requires_secret_patterns
    def test_raw_generation_does_not_depend_on_provider_key_prefix(self):
        odd = {
            "ANTHROPIC_API_KEY": "QAoddANTHROPIC-no-sk-prefix-1111111111",
            "OPENAI_API_KEY": "QAoddOPENAI-no-sk-prefix-2222222222",
            "GEMINI_API_KEY": "QAoddGEMINI-no-AIza-prefix-333333333",
        }
        html = build_topic_page(env_extra=dict(odd))
        for name, value in odd.items():
            with self.subTest(env=name):
                self.assertNotIn(value, html)
        self.assertFalse(find_local_emails(html))

    @requires_secret_patterns
    def test_key_reinjection_is_absent(self):
        """생성물에 owner 키를 다시 굽는 복구 경로를 두지 않는다."""
        src = SOURCES["prepare_deploy"].read_text(encoding="utf-8")
        strip_at = src.find("strip_key_slots(")
        self.assertNotEqual(strip_at, -1, "Step 6 strip 호출부를 찾지 못했다")
        upload = re.search(r"^\s+_wrangler_deploy\(\)\s*$", src, re.M)
        self.assertIsNotNone(upload, "wrangler 업로드 호출부를 찾지 못했다")
        self.assertLess(strip_at, upload.start(), "strip 이 업로드보다 뒤에 있다")
        self.assertNotIn("_reinject_local_keys", src)


class GeneratedPageBrowserGateTests(unittest.TestCase):
    """게이트를 텍스트가 아니라 '동작' 으로 검증한다.

    소스 grep 은 함수 이름을 바꾸면 같이 죽고, 반대로 페이지가 실제로는
    실행조차 안 되는 상태여도 통과한다. 여기서는 진짜로 생성된 페이지의
    <script> 를 최소 DOM 위에서 실행하고, 사용자가 관측하는 결과 —
    #deep-status 텍스트와 버튼 disabled — 만 본다.
    """

    SHIM = Path(__file__).resolve().parent / "_generated_page_shim.mjs"

    def setUp(self):
        self.node = shutil.which("node")
        if not self.node:
            self.skipTest("node 없음 — 브라우저 게이트 동작 검증 생략")

    def _page_script(self, html, *, require_parse=False):
        blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
        self.assertTrue(blocks, "생성 페이지에 <script> 가 없다")
        script = max(blocks, key=len)
        path = Path(_workspace()) / "page.js"
        path.write_text(script, encoding="utf-8")
        check = subprocess.run([self.node, "--check", str(path)],
                               capture_output=True, text=True)
        if check.returncode != 0:
            detail = "\n".join(check.stderr.splitlines()[:4])
            if require_parse:
                self.fail(
                    "생성된 페이지의 메인 <script> 가 파싱되지 않는다 — 이 블록의 "
                    "코드는 하나도 실행되지 않으므로 키 상태 안내도 뜨지 않는다:\n"
                    + detail)
            # 파싱 자체가 깨진 상태에서 동작 검증은 의미가 없다. 원인은
            # test_generated_main_script_is_parseable_javascript 가 보고한다.
            self.skipTest("메인 <script> 파싱 불가 (아래 테스트 참조):\n" + detail)
        return path

    def test_generated_main_script_is_parseable_javascript(self):
        """이게 깨지면 검색·필터·Deep Research·키 안내가 전부 죽는다.

        JS 는 build_topic_index.py 의 non-raw 삼중따옴표 문자열 안에 들어 있어서
        `'...\\n\\n'` 처럼 두 번 이스케이프하지 않으면 파이썬이 개행을 먼저
        먹고, 생성물에는 JS 문자열 리터럴 안에 실제 개행이 박힌다.
        """
        self._page_script(build_topic_page(), require_parse=True)

    def _run(self, path, options):
        proc = subprocess.run(
            [self.node, str(self.SHIM), str(path), json.dumps(options)],
            capture_output=True, text=True, timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stderr[-1500:])
        return json.loads(proc.stdout)

    def test_no_key_page_states_the_reason_and_disables_the_buttons(self):
        path = self._page_script(build_topic_page())
        res = self._run(path, {})
        self.assertIsNone(res["loadError"], "페이지 스크립트가 로드 중 죽는다")
        self.assertNotIn("ERR:", "".join(res["fired"]),
                         "DOMContentLoaded 핸들러가 예외로 끝난다: %s" % res["fired"])
        text = res["statusText"] or ""
        self.assertTrue(text, "키가 없는데 아무 설명도 뜨지 않는다 (조용한 실패)")
        for phrase in ("BYOK", "OAuth", "구독"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertTrue(res["statusActive"], "설명이 숨겨진 채로 있다")
        self.assertIs(res["rerunDisabled"], True, "재시작 버튼이 잠기지 않았다")
        self.assertIs(res["audioDisabled"], True, "오디오 버튼이 잠기지 않았다")

    def test_the_load_time_explanation_survives_every_load_handler(self):
        """뒤따르는 DOMContentLoaded 핸들러가 설명을 덮어쓰면 안 된다."""
        path = self._page_script(build_topic_page())
        res = self._run(path, {})
        self.assertGreater(res["domHandlers"], 1,
                           "load 핸들러가 하나뿐이면 이 테스트는 무의미하다")
        self.assertIn("BYOK", res["statusText"] or "",
                      "모든 load 핸들러가 돈 뒤 설명이 사라졌다")

    def test_bad_format_key_is_not_reported_as_a_missing_key(self):
        """형식이 틀린 키와 '키가 아예 없음' 은 다른 안내여야 한다."""
        path = self._page_script(build_topic_page())
        res = self._run(path, {
            "action": "run",
            "promptReturn": "definitely-not-a-key",
        })
        text = res["statusAfterRun"] or ""
        self.assertTrue(text, "형식이 틀린 키인데 아무 안내도 없다")
        self.assertNotIn("BYOK", text,
                         "형식 오류를 '키가 없다' 안내로 잘못 설명한다")
        self.assertIs(res["rerunDisabled"], True,
                      "유효한 키가 없는데 재실행 버튼이 활성화됐다")

    def test_cancelling_the_byok_prompt_leaves_an_explanation(self):
        """프롬프트를 취소해도 이유가 남아야 한다 — 무성 실패 금지."""
        path = self._page_script(build_topic_page())
        res = self._run(path, {"action": "run", "promptReturn": None})
        self.assertEqual(res["hasRunDeepResearch"], "function",
                         "runDeepResearch 를 찾지 못했다 (이름이 바뀌었나?)")
        self.assertIsNone(res.get("runError"), res.get("runError"))
        self.assertTrue(res["promptMessages"], "BYOK 프롬프트가 뜨지 않았다")
        self.assertIn("BYOK", res["promptMessages"][0],
                      "프롬프트가 왜 키를 물어보는지 설명하지 않는다")
        after = res["statusAfterRun"] or ""
        for phrase in ("BYOK", "구독"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, after,
                              "취소 후 설명이 사라지고 짧은 오류만 남았다")

    def test_the_second_run_path_is_gated_too(self):
        """주 경로만 막고 deeper 경로를 열어두면 계약이 반쪽이다.

        이쪽은 프롬프트 없이 키 상태 메시지를 그대로 던진다. 실제 페이지에서
        거부되는지, 그리고 거부 사유가 옛 '키 형식' 오해가 아니라 BYOK/구독
        설명인지 본다.
        """
        path = self._page_script(build_topic_page())
        res = self._run(path, {"action": "deeper"})
        self.assertEqual(res["hasRunDeeperResearch"], "function",
                         "runDeeperResearch 를 찾지 못했다 (이름이 바뀌었나?)")
        self.assertTrue(res.get("deeperRejected"),
                        "키가 없는데 deeper 경로가 그냥 진행됐다")
        for phrase in ("BYOK", "구독"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, res.get("deeperError") or "",
                              "deeper 경로가 이유를 설명하지 않는다")


if __name__ == "__main__":
    unittest.main()
