"""Cross-category insights 는 provider 를 조용히 갈아타지 않는다.

설정된 backend 가 실패했을 때 사용자가 고르지도 않은 다른 회사 모델이 대신
답하면 (a) 결과의 출처를 신뢰할 수 없고 (b) 그 API 에 과금된다. 미설정
backend 를 건너뛰는 것(부재)은 허용하되, 설정된 backend 의 실패를 다른
provider 로 넘기는 것(대체)은 금지다.
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import extract_insights as ei  # noqa: E402


def _identity_cached_call(_cache_dir, _prompt, _tag, make_call, **_kw):
    """cached_call 을 우회해 실제 backend 선택 경로만 본다."""
    return make_call()


class BackendAvailabilityTests(unittest.TestCase):
    def test_anthropic_availability_follows_auth_not_env(self):
        """OAuth 구독 모드에서는 ANTHROPIC_API_KEY 가 없는 것이 정상이다."""
        class _Ready:
            ready = True

        class _NotReady:
            ready = False

        with patch("anthropic_auth.auth_status", return_value=_Ready()):
            self.assertTrue(ei._cc_backend_available("anthropic"))
        with patch("anthropic_auth.auth_status", return_value=_NotReady()):
            self.assertFalse(ei._cc_backend_available("anthropic"))

    def test_gemini_availability_honors_the_off_switch(self):
        with patch("config_loader.get_google_key", return_value="AIza-x"):
            self.assertTrue(ei._cc_backend_available("gemini"))
        with patch("config_loader.get_google_key", return_value=""):
            self.assertFalse(ei._cc_backend_available("gemini"))

    def test_unknown_backend_is_never_available(self):
        self.assertFalse(ei._cc_backend_available("bogus"))


class NoSilentSubstitutionTests(unittest.TestCase):
    """핵심 계약: 첫 backend 가 죽어도 두 번째가 호출되지 않는다."""

    def _run(self, available, anthropic=None, openai=None, gemini=None):
        called = []

        def _anth(client, prompt, schema):
            called.append("anthropic")
            if isinstance(anthropic, Exception):
                raise anthropic
            return anthropic

        def _oai(prompt, schema):
            called.append("openai")
            if isinstance(openai, Exception):
                raise openai
            return openai

        def _gem(prompt, schema):
            called.append("gemini")
            if isinstance(gemini, Exception):
                raise gemini
            return gemini

        with patch.object(ei, "_CC_BACKENDS", ["anthropic", "openai", "gemini"]), \
             patch.object(ei, "_cc_backend_available", lambda b: b in available), \
             patch.object(ei, "_cc_anthropic_call", _anth), \
             patch.object(ei, "_cc_openai_call", _oai), \
             patch.object(ei, "_cc_gemini_call", _gem), \
             patch("api._llm.cached_call", _identity_cached_call), \
             patch("api._llm.topic_cache_dir", return_value="/tmp/does-not-matter"):
            out = ei.extract_cross_category_insights(
                "topic",
                {"cat": [{"slug": "001_paper", "title": "P", "essence": "e"}]},
                {"cat": "s"}, client=object())
        return out, called

    def test_first_backend_failure_does_not_call_the_next(self):
        out, called = self._run(
            available={"anthropic", "openai", "gemini"},
            anthropic=RuntimeError("429 overloaded"),
            openai={"cross_category": [{"title": "should never be used"}],
                    "per_category": {}},
        )
        self.assertEqual(called, ["anthropic"],
                         "설정된 backend 가 실패했는데 다른 provider 가 호출됐다")
        # 실패는 상위에서 흡수되어 빈 결과가 된다 — 다른 회사 답이 아니라.
        self.assertEqual(out.get("cross_category"), [])

    def test_unconfigured_backend_is_skipped_without_being_called(self):
        """부재는 대체가 아니다: 미설정 backend 는 건너뛰고 다음을 쓴다."""
        out, called = self._run(
            available={"gemini"},
            gemini={"cross_category": [{"title": "gemini result"}],
                    "per_category": {}},
        )
        self.assertEqual(called, ["gemini"])
        self.assertEqual(out["cross_category"][0]["title"], "gemini result")

    def test_no_configured_backend_yields_empty_not_a_substitute(self):
        out, called = self._run(available=set())
        self.assertEqual(called, [])
        self.assertEqual(out.get("cross_category"), [])

    def test_success_path_uses_only_the_first_available_backend(self):
        out, called = self._run(
            available={"anthropic", "openai"},
            anthropic={"cross_category": [{"title": "claude result"}],
                       "per_category": {}},
            openai={"cross_category": [{"title": "should never be used"}],
                    "per_category": {}},
        )
        self.assertEqual(called, ["anthropic"])
        self.assertEqual(out["cross_category"][0]["title"], "claude result")


class SourceContractTests(unittest.TestCase):
    def test_no_next_backend_loop_survives_in_source(self):
        """`→ next backend` 로 넘어가던 루프가 되살아나면 잡는다."""
        import inspect
        src = inspect.getsource(ei.extract_cross_category_insights)
        self.assertNotIn("next backend", src)
        self.assertNotIn("all cross-category backends failed", src)


if __name__ == "__main__":
    unittest.main()
