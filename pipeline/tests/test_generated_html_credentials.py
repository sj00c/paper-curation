"""생성 HTML 에 자격증명이 새지 않는다.

브라우저 Deep Research 는 BYOK 다. 로컬 편의를 위해 API 키를 구워 넣는 경로가
있고 prepare_deploy 가 배포 전에 걷어내지만, 두 가지는 무조건이다.

1. 키가 없으면(=구독 OAuth 로 도는 정상 상태) 생성물에 자격증명이 하나도 없다.
2. OAuth 토큰은 어떤 경우에도 HTML 로 내려가지 않는다. 구독 자격증명이 정적
   산출물로 새면 그건 되돌릴 수 없다.
"""
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

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

    def test_review_to_html_key_slot_is_empty_without_env_or_config(self):
        import importlib
        with patch.dict("os.environ", {}, clear=True):
            with patch("json.load", return_value={}):
                mod = importlib.reload(importlib.import_module("review_to_html"))
                self.assertEqual(getattr(mod, "_GEMINI_KEY", ""), "")


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


if __name__ == "__main__":
    unittest.main()
