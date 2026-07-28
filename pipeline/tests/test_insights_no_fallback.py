"""Cross-category insights 는 provider 를 조용히 갈아타지 않는다.

설정된 backend 가 실패했을 때 사용자가 고르지도 않은 다른 회사 모델이 대신
답하면 (a) 결과의 출처를 신뢰할 수 없고 (b) 그 API 에 과금된다. 미설정
backend 를 건너뛰는 것(부재)은 허용하되, 설정된 backend 의 실패를 다른
provider 로 넘기는 것(대체)은 금지다.

아래는 그 계약을 적대적으로 두드리는 케이스들이다. 각 클래스가 하나의 공격
벡터를 담당한다:

* ``FailureModeNeverReachesASecondVendorTests`` — 예외/타임아웃/None/깨진
  payload/빈 dict 등 실패 형태를 바꿔 두 번째 vendor 호출을 유도한다.
* ``AvailabilityCheckCannotBeDefeatedTests`` — 공백 키, off 스위치, auth 조회
  실패로 "설정 안 한 vendor 가 선택되는" 상태를 만들려 한다.
* ``CacheTagProvenanceTests`` — 한 backend 로 만든 캐시가 다른 backend 의
  답으로 재활용되는지 본다.
* ``MetaContractTests`` — 부재(unavailable)와 실패(failed)가 구분되는지.
* ``BackendOrderTests`` — 우선순위를 바꿨을 때 뒤 backend 가 몰래 승격되는지.
* ``ImportTimeConfigTests`` — 오타는 시끄럽게 죽고, 정상 설정은 절대 안 죽는지.
"""
import contextlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import extract_insights as ei  # noqa: E402
from api import _llm  # noqa: E402


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
        # 각 vendor helper 의 호출 지점은 정확히 하나여야 한다. 두 번째 호출
        # 지점이 생기면 그게 곧 조용한 대체의 입구다.
        import re
        mod_src = inspect.getsource(ei)
        for helper in ("_cc_anthropic_call", "_cc_openai_call", "_cc_gemini_call"):
            sites = re.findall(rf"(?<!def ){re.escape(helper)}\(", mod_src)
            self.assertEqual(
                len(sites), 1,
                f"{helper} 의 호출 지점이 {len(sites)}곳이다 — 대체 경로 의심")


# ═══════════════════════════════════════════════════════════════════════════
# 적대적 QA 하네스
# ═══════════════════════════════════════════════════════════════════════════

_ALL = ("anthropic", "openai", "gemini")
_DEFAULT_ORDER = list(_ALL)

# 프롬프트 조립(_fit_cat_blocks)이 결정적이도록 작은 고정 입력을 쓴다.
# client=object() 이면 count_tokens 가 실패해 _est_tokens 로 떨어지고, 그 값은
# MAX_PROMPT_TOKENS 아래이므로 Haiku 압축 루프는 돌지 않는다.
_TINY_CATS = {
    "Cat A": [
        {"slug": "001_a", "title": "Paper A", "essence": "aaa", "score": 3,
         "date": "2025-01-01"},
        {"slug": "002_b", "title": "Paper B", "essence": "bbb", "score": 2,
         "date": "2025-02-01"},
        {"slug": "003_c", "title": "Paper C", "essence": "ccc", "score": 1,
         "date": "2025-03-01"},
    ],
    "Cat B": [
        {"slug": "004_d", "title": "Paper D", "essence": "ddd", "score": 5,
         "date": "2024-06-01"},
    ],
}
_TINY_SUMS = [{"category": "Cat A", "summary": "s"}]

_UNSET = object()


class APITimeoutError(Exception):
    """SDK 타임아웃을 흉내내는 예외 (이름이 meta.error 에 그대로 실린다)."""


def _payload(vendor, marker="answer"):
    """vendor 태그가 박힌 응답. 출력에 섞여 나오면 출처를 즉시 알 수 있다."""
    return {"cross_category": [{"title": f"{vendor} {marker}"}],
            "per_category": {vendor: {"trend": "STABLE"}},
            "_vendor": vendor}


class _Spy:
    """세 helper (_cc_anthropic_call/_cc_openai_call/_cc_gemini_call) 호출 감시.

    호출 순서를 그대로 기록한다. 무장하지 않은 vendor 가 호출되면 예외를 던지지
    *않고* 태그 붙은 payload 를 돌려준다 — 프로덕션의 ``except Exception`` 이
    스파이의 항의를 삼켜 "실패" 로 위장하는 것을 막기 위해서다.
    """

    def __init__(self, **behaviour):
        self.calls = []
        self.prompts = {}
        self._behaviour = {b: behaviour.get(b, _UNSET) for b in _ALL}

    def _fire(self, backend, prompt):
        self.calls.append(backend)
        self.prompts[backend] = prompt
        out = self._behaviour[backend]
        if out is _UNSET:
            return _payload(backend, "UNARMED-must-never-be-billed")
        if isinstance(out, BaseException):
            raise out
        if callable(out):
            return out()
        return out

    def anthropic(self, client, prompt, schema):
        return self._fire("anthropic", prompt)

    def openai(self, prompt, schema):
        return self._fire("openai", prompt)

    def gemini(self, prompt, schema):
        return self._fire("gemini", prompt)


def _run_cc(spy, *, available=_UNSET, order=_DEFAULT_ORDER,
            cached_call=_identity_cached_call, cache_dir=None, client=_UNSET,
            topic="qa-topic", cats=None):
    """``extract_cross_category_insights`` 를 스파이와 함께 1회 실행.

    ``available`` 를 주지 않으면 실제 ``_cc_backend_available`` 이 쓰인다.
    ``cached_call=None`` 이면 실제 ``api._llm.cached_call`` (디스크 캐시) 이 쓰인다.
    """
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(ei, "_CC_BACKENDS", list(order)))
        if available is not _UNSET:
            stack.enter_context(patch.object(
                ei, "_cc_backend_available", lambda b: b in available))
        stack.enter_context(patch.object(ei, "_cc_anthropic_call", spy.anthropic))
        stack.enter_context(patch.object(ei, "_cc_openai_call", spy.openai))
        stack.enter_context(patch.object(ei, "_cc_gemini_call", spy.gemini))
        if cached_call is not None:
            stack.enter_context(patch("api._llm.cached_call", cached_call))
        stack.enter_context(patch(
            "api._llm.topic_cache_dir",
            return_value=cache_dir or "/tmp/pc-qa-cache-unused"))
        return ei.extract_cross_category_insights(
            topic, cats or _TINY_CATS, _TINY_SUMS,
            object() if client is _UNSET else client)


@contextlib.contextmanager
def _env(**kw):
    """env 를 임시로 설정/삭제(None). 종료 시 원복."""
    saved = {k: os.environ.get(k) for k in kw}
    try:
        for k, v in kw.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


class _NoSubstitutionAssertions(unittest.TestCase):
    """공통 단정: 고른 backend 하나만 호출되고, 남의 답이 새어나오지 않는다."""

    def assertOnlyVendorCalled(self, spy, backend, msg=""):
        self.assertEqual(
            spy.calls, [backend],
            f"두 번째 vendor 가 호출됐다 (billing/출처 위반): {spy.calls}. {msg}")

    def assertNoForeignContent(self, out, backend):
        """결과 payload 에 다른 vendor 의 흔적이 없다."""
        blob = json.dumps(out, ensure_ascii=False, default=str)
        for other in _ALL:
            if other == backend:
                continue
            self.assertNotIn(
                f'"{other} answer"', blob,
                f"{other} 의 답이 결과에 섞였다 (backend={backend})")
            self.assertNotIn("UNARMED-must-never-be-billed", blob)
        if isinstance(out, dict) and "_vendor" in out:
            self.assertEqual(out["_vendor"], backend)


class FailureModeNeverReachesASecondVendorTests(_NoSubstitutionAssertions):
    """공격 1: 실패 형태를 바꿔 두 번째 vendor 호출을 유도한다."""

    def _armed_rivals(self):
        """openai/gemini 를 '먹음직한' 성공 응답으로 무장해 둔다."""
        return {"openai": _payload("openai"), "gemini": _payload("gemini")}

    def test_raised_exception_does_not_promote_a_rival(self):
        spy = _Spy(anthropic=RuntimeError("429 overloaded"), **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertNoForeignContent(out, "anthropic")
        self.assertEqual(out["meta"]["status"], "failed")
        self.assertEqual(out["meta"]["backend"], "anthropic")

    def test_timeout_like_error_does_not_promote_a_rival(self):
        spy = _Spy(anthropic=APITimeoutError("Request timed out."),
                   **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertNoForeignContent(out, "anthropic")
        self.assertTrue(out["meta"]["error"].startswith("APITimeoutError:"),
                        out["meta"]["error"])

    def test_returned_none_does_not_promote_a_rival(self):
        """helper 가 None 을 돌려줘도 다른 vendor 를 부르지 않는다."""
        spy = _Spy(anthropic=lambda: None, **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertIsNone(out, "None 이 다른 vendor 의 답으로 대체됐다")

    def test_unparseable_payload_error_does_not_promote_a_rival(self):
        """실제 openai/gemini helper 가 던지는 JSONDecodeError 모양."""
        spy = _Spy(anthropic=json.JSONDecodeError("Expecting value", "not json", 0),
                   **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertNoForeignContent(out, "anthropic")
        self.assertEqual(out["meta"]["status"], "failed")
        self.assertTrue(out["meta"]["error"].startswith("JSONDecodeError:"),
                        out["meta"]["error"])

    def test_malformed_non_dict_payload_does_not_promote_a_rival(self):
        """schema 를 어긴 문자열이 그대로 돌아와도 대체는 없다."""
        spy = _Spy(anthropic=lambda: "<<not a dict>>", **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertEqual(out, "<<not a dict>>")

    def test_empty_dict_payload_does_not_promote_a_rival(self):
        spy = _Spy(anthropic=lambda: {}, **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertEqual(out, {})

    def test_schema_shaped_but_empty_result_does_not_promote_a_rival(self):
        spy = _Spy(anthropic=lambda: {"cross_category": [], "per_category": {}},
                   **self._armed_rivals())
        out = _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")
        self.assertEqual(out, {"cross_category": [], "per_category": {}})

    def test_base_exception_propagates_without_touching_a_rival(self):
        """Ctrl-C 는 '실패' 로 뭉개지지도, 대체를 트리거하지도 않는다."""
        spy = _Spy(anthropic=KeyboardInterrupt(), **self._armed_rivals())
        with self.assertRaises(KeyboardInterrupt):
            _run_cc(spy, available=set(_ALL))
        self.assertOnlyVendorCalled(spy, "anthropic")

    def test_missing_anthropic_client_is_a_failure_not_a_handoff(self):
        """client=None → 실제 helper 는 RuntimeError. 그래도 openai 로 안 넘긴다."""
        with patch.object(ei, "_CC_BACKENDS", list(_ALL)), \
             patch.object(ei, "_cc_backend_available", lambda b: b in _ALL), \
             patch.object(ei, "_cc_openai_call",
                          lambda *a, **k: self.fail("openai 가 호출됐다")), \
             patch.object(ei, "_cc_gemini_call",
                          lambda *a, **k: self.fail("gemini 가 호출됐다")), \
             patch("api._llm.cached_call", _identity_cached_call), \
             patch("api._llm.topic_cache_dir", return_value="/tmp/pc-qa-unused"):
            out = ei.extract_cross_category_insights(
                "qa-topic", _TINY_CATS, _TINY_SUMS, None)
        self.assertEqual(out["meta"]["status"], "failed")
        self.assertEqual(out["meta"]["backend"], "anthropic")
        self.assertIn("Anthropic client unavailable", out["meta"]["error"])

    def test_every_chosen_backend_fails_in_isolation(self):
        """어느 backend 가 골라져도 실패는 그 자리에서 끝난다."""
        for backend in _ALL:
            with self.subTest(backend=backend):
                spy = _Spy(**{b: (RuntimeError("boom") if b == backend
                                  else _payload(b)) for b in _ALL})
                out = _run_cc(spy, available={backend})
                self.assertOnlyVendorCalled(spy, backend)
                self.assertNoForeignContent(out, backend)
                self.assertEqual(out["meta"]["backend"], backend)

    def test_unknown_selected_backend_fails_closed(self):
        """가용성 판정이 오염돼 모르는 backend 가 골라져도 실제 vendor 는 안 부른다."""
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        out = _run_cc(spy, available={"cohere"}, order=["cohere", "anthropic"])
        self.assertEqual(spy.calls, [],
                         f"모르는 backend 인데 실제 vendor 가 호출됐다: {spy.calls}")
        self.assertEqual(out["meta"]["status"], "failed")
        self.assertEqual(out["meta"]["backend"], "cohere")
        self.assertIn("unknown insights backend", out["meta"]["error"])
        self.assertNoForeignContent(out, "cohere")


class AvailabilityCheckCannotBeDefeatedTests(_NoSubstitutionAssertions):
    """공격 2: 가용성 판정을 속여 미설정 vendor 를 선택하게 만든다."""

    # ── openai: 공백 키 ────────────────────────────────────────────────────
    def _openai_available(self, env_key, cfg):
        with _env(OPENAI_API_KEY=env_key), patch.object(ei, "load_config", lambda: cfg):
            return ei._cc_backend_available("openai")

    def test_whitespace_openai_key_is_not_configured(self):
        for label, env_key, cfg in [
            ("spaces only, no config key", "   ", {}),
            ("tabs/newlines only, no config key", "\t\n ", {}),
            ("whitespace env masks a real config key", "\t ",
             {"openai_api_key": "sk-real-config"}),
            ("whitespace config key, no env", None, {"openai_api_key": "   "}),
        ]:
            with self.subTest(label):
                self.assertFalse(self._openai_available(env_key, cfg),
                                 f"공백 키가 '설정됨' 으로 통과했다: {label}")

    def test_real_openai_key_is_configured(self):
        self.assertTrue(self._openai_available("sk-env", {}))
        self.assertTrue(self._openai_available(None, {"openai_api_key": "sk-cfg"}))

    def test_whitespace_openai_key_never_bills_openai(self):
        """공백 키면 openai 는 후보에서 빠지고, 실제로 호출되지도 않는다."""
        class _NotReady:
            ready = False

        spy = _Spy(**{b: _payload(b) for b in _ALL})
        with _env(OPENAI_API_KEY="   ", PAPER_CURATION_NO_GEMINI=None), \
             patch.object(ei, "load_config", lambda: {}), \
             patch("anthropic_auth.auth_status", return_value=_NotReady()), \
             patch("config_loader.get_google_key", return_value="AIza-real"):
            out = _run_cc(spy)  # 실제 _cc_backend_available 사용
        # gemini 만 설정돼 있으므로 gemini 가 선택된다 (사용자가 설정한 vendor).
        self.assertOnlyVendorCalled(spy, "gemini")
        self.assertNoForeignContent(out, "gemini")

    def test_whitespace_openai_key_with_nothing_else_yields_unavailable(self):
        class _NotReady:
            ready = False

        spy = _Spy(**{b: _payload(b) for b in _ALL})
        with _env(OPENAI_API_KEY="   "), \
             patch.object(ei, "load_config", lambda: {}), \
             patch("anthropic_auth.auth_status", return_value=_NotReady()), \
             patch("config_loader.get_google_key", return_value=""):
            out = _run_cc(spy)
        self.assertEqual(spy.calls, [], f"미설정 상태에서 vendor 가 호출됐다: {spy.calls}")
        self.assertEqual(out["meta"]["status"], "unavailable")

    # ── gemini: off 스위치 ────────────────────────────────────────────────
    def test_no_gemini_switch_wins_over_a_present_google_key(self):
        """PAPER_CURATION_NO_GEMINI 는 env/config 키가 있어도 gemini 를 끈다."""
        with _env(PAPER_CURATION_NO_GEMINI="1", GOOGLE_API_KEY="AIza-env",
                  GEMINI_API_KEY="AIza-env2"), \
             patch("config_loader.load_config",
                   lambda: {"gemini_api_key": "AIza-cfg"}):
            self.assertFalse(ei._cc_backend_available("gemini"))
        with _env(PAPER_CURATION_NO_GEMINI=None, GOOGLE_API_KEY="AIza-env",
                  GEMINI_API_KEY=None), \
             patch("config_loader.load_config", lambda: {}):
            self.assertTrue(ei._cc_backend_available("gemini"))

    def test_no_gemini_switch_never_bills_google(self):
        class _NotReady:
            ready = False

        spy = _Spy(**{b: _payload(b) for b in _ALL})
        with _env(PAPER_CURATION_NO_GEMINI="1", GOOGLE_API_KEY="AIza-env",
                  OPENAI_API_KEY=None), \
             patch.object(ei, "load_config", lambda: {}), \
             patch("config_loader.load_config",
                   lambda: {"gemini_api_key": "AIza-cfg"}), \
             patch("anthropic_auth.auth_status", return_value=_NotReady()):
            out = _run_cc(spy)
        self.assertEqual(spy.calls, [],
                         f"off 스위치가 걸린 gemini 가 호출됐다: {spy.calls}")
        self.assertEqual(out["meta"]["status"], "unavailable")

    # ── anthropic: auth 조회 ──────────────────────────────────────────────
    def test_auth_status_raising_means_unconfigured_not_a_handoff(self):
        with _env(ANTHROPIC_API_KEY="sk-ant-present"), \
             patch("anthropic_auth.auth_status",
                   side_effect=RuntimeError("keychain locked")):
            self.assertFalse(ei._cc_backend_available("anthropic"))

    def test_auth_status_not_ready_ignores_a_present_env_key(self):
        class _NotReady:
            ready = False

        with _env(ANTHROPIC_API_KEY="sk-ant-present"), \
             patch("anthropic_auth.auth_status", return_value=_NotReady()):
            self.assertFalse(ei._cc_backend_available("anthropic"))

    def test_auth_status_without_ready_attribute_is_unconfigured(self):
        class _Weird:
            pass

        with patch("anthropic_auth.auth_status", return_value=_Weird()):
            self.assertFalse(ei._cc_backend_available("anthropic"))
        with patch("anthropic_auth.auth_status", return_value=None):
            self.assertFalse(ei._cc_backend_available("anthropic"))

    def test_oauth_ready_without_env_key_is_configured(self):
        class _Ready:
            ready = True

        with _env(ANTHROPIC_API_KEY=None), \
             patch("anthropic_auth.auth_status", return_value=_Ready()):
            self.assertTrue(ei._cc_backend_available("anthropic"))

    def test_broken_anthropic_auth_falls_through_to_a_configured_vendor_only(self):
        """auth 조회가 깨지면 anthropic 은 '부재'. 다음은 *설정된* vendor 뿐."""
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        with _env(ANTHROPIC_API_KEY="sk-ant-present", OPENAI_API_KEY="sk-oai"), \
             patch.object(ei, "load_config", lambda: {}), \
             patch("anthropic_auth.auth_status",
                   side_effect=RuntimeError("keychain locked")), \
             patch("config_loader.get_google_key", return_value=""):
            out = _run_cc(spy)
        self.assertOnlyVendorCalled(spy, "openai")
        self.assertNoForeignContent(out, "openai")

    def test_broken_anthropic_auth_alone_is_unavailable_not_substituted(self):
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        with _env(ANTHROPIC_API_KEY="sk-ant-present"), \
             patch("anthropic_auth.auth_status",
                   side_effect=RuntimeError("keychain locked")):
            out = _run_cc(spy, order=["anthropic"])
        self.assertEqual(spy.calls, [])
        self.assertEqual(out["meta"]["status"], "unavailable")
        self.assertEqual(out["meta"]["candidates"], ["anthropic"])

    def test_selected_backend_is_always_inside_the_configured_set(self):
        """가용성 조합을 전수로 돌려 '설정 안 한 vendor 선택' 이 없음을 확인."""
        import itertools
        for r in range(len(_ALL) + 1):
            for combo in itertools.combinations(_ALL, r):
                with self.subTest(configured=combo):
                    spy = _Spy(**{b: _payload(b) for b in _ALL})
                    out = _run_cc(spy, available=set(combo))
                    if not combo:
                        self.assertEqual(spy.calls, [])
                        self.assertEqual(out["meta"]["status"], "unavailable")
                        continue
                    self.assertEqual(len(spy.calls), 1)
                    self.assertIn(spy.calls[0], combo,
                                  "설정하지 않은 vendor 가 호출됐다")
                    self.assertEqual(spy.calls[0], combo[0],
                                     "우선순위 첫 번째가 아닌 vendor 가 골라졌다")
                    self.assertNoForeignContent(out, spy.calls[0])


class CacheTagProvenanceTests(_NoSubstitutionAssertions):
    """공격 3: 한 backend 로 만든 캐시를 다른 backend 의 답으로 재활용시킨다."""

    def test_cache_is_not_shared_across_backends(self):
        with tempfile.TemporaryDirectory() as tmp:
            # 1) anthropic 으로 캐시를 채운다.
            spy1 = _Spy(anthropic=_payload("anthropic"))
            out1 = _run_cc(spy1, available={"anthropic"}, cached_call=None,
                           cache_dir=tmp)
            self.assertOnlyVendorCalled(spy1, "anthropic")
            self.assertEqual(out1["_vendor"], "anthropic")
            prompt = spy1.prompts["anthropic"]

            # 2) 같은 backend 재실행 → 캐시 히트 (호출 0회).
            spy2 = _Spy(anthropic=_payload("anthropic", "SECOND-CALL"))
            out2 = _run_cc(spy2, available={"anthropic"}, cached_call=None,
                           cache_dir=tmp)
            self.assertEqual(spy2.calls, [], "같은 backend 인데 캐시가 안 먹었다")
            self.assertEqual(out2["cross_category"][0]["title"], "anthropic answer")

            # 3) 가용성을 openai 로 뒤집으면 anthropic 캐시는 서빙되지 않는다.
            spy3 = _Spy(openai=_payload("openai"))
            out3 = _run_cc(spy3, available={"openai"}, cached_call=None,
                           cache_dir=tmp)
            self.assertOnlyVendorCalled(spy3, "openai")
            self.assertEqual(out3["_vendor"], "openai",
                             "backend 를 바꿨는데 예전 provider 의 캐시가 서빙됐다")
            self.assertNoForeignContent(out3, "openai")

            # 캐시 태그(=model) 가 backend 별로 분리되어 저장된다.
            tags = sorted(json.loads(p.read_text(encoding="utf-8"))["model"]
                          for p in Path(tmp).glob("*.json"))
            self.assertEqual(tags, ["anthropic", "openai"])
            self.assertNotEqual(_llm.cache_key(prompt, "anthropic"),
                                _llm.cache_key(prompt, "openai"))

    def test_cached_rival_payload_is_not_served_when_chosen_backend_fails(self):
        """가장 날카로운 케이스: anthropic 캐시가 디스크에 있고 openai 가 실패."""
        with tempfile.TemporaryDirectory() as tmp:
            spy1 = _Spy(anthropic=_payload("anthropic"))
            _run_cc(spy1, available={"anthropic"}, cached_call=None, cache_dir=tmp)
            self.assertTrue(list(Path(tmp).glob("*.json")))

            spy2 = _Spy(openai=RuntimeError("openai 500"))
            out = _run_cc(spy2, available={"openai"}, cached_call=None,
                          cache_dir=tmp)
            self.assertOnlyVendorCalled(spy2, "openai")
            self.assertEqual(out["meta"]["status"], "failed")
            self.assertEqual(out["meta"]["backend"], "openai")
            self.assertNoForeignContent(out, "openai")
            self.assertEqual(out["cross_category"], [])

    def test_legacy_joined_tag_cache_is_never_served(self):
        """옛 캐시 태그(``anthropic+openai+gemini``) 항목은 되살아나지 않는다."""
        with tempfile.TemporaryDirectory() as tmp:
            # 프롬프트를 알아내기 위해 1회 실행 (identity cache — 디스크 미사용).
            probe = _Spy(anthropic=_payload("anthropic"))
            _run_cc(probe, available={"anthropic"})
            prompt = probe.prompts["anthropic"]

            legacy_tag = "+".join(_ALL)
            legacy_key = _llm.cache_key(prompt, legacy_tag)
            (Path(tmp) / f"{legacy_key}.json").write_text(json.dumps(
                {"result": _payload("gemini", "LEGACY-JOINED-TAG"),
                 "model": legacy_tag, "schema_version": "v1"}), encoding="utf-8")

            spy = _Spy(anthropic=_payload("anthropic"))
            out = _run_cc(spy, available={"anthropic"}, cached_call=None,
                          cache_dir=tmp)
            self.assertOnlyVendorCalled(spy, "anthropic")
            self.assertNotIn("LEGACY-JOINED-TAG",
                             json.dumps(out, ensure_ascii=False))
            self.assertEqual(out["_vendor"], "anthropic")

    def test_failures_are_not_cached_and_do_not_leak_a_rival(self):
        with tempfile.TemporaryDirectory() as tmp:
            spy1 = _Spy(openai=RuntimeError("openai 429"))
            out1 = _run_cc(spy1, available={"openai"}, cached_call=None,
                           cache_dir=tmp)
            self.assertEqual(out1["meta"]["status"], "failed")
            self.assertEqual(list(Path(tmp).glob("*.json")), [],
                             "실패가 캐시에 남았다")

            spy2 = _Spy(openai=_payload("openai"))
            out2 = _run_cc(spy2, available={"openai"}, cached_call=None,
                           cache_dir=tmp)
            self.assertOnlyVendorCalled(spy2, "openai")
            self.assertEqual(out2["_vendor"], "openai")

    def test_cache_tag_is_the_single_chosen_backend(self):
        """cached_call 에 넘어가는 태그가 후보 목록이 아니라 고른 backend 하나다."""
        seen = {}

        def _capture(cache_dir, prompt, tag, make_call, **kw):
            seen["tag"] = tag
            seen["schema_version"] = kw.get("schema_version")
            return make_call()

        spy = _Spy(**{b: _payload(b) for b in _ALL})
        _run_cc(spy, available=set(_ALL), cached_call=_capture)
        self.assertEqual(seen["tag"], "anthropic")
        self.assertEqual(seen["schema_version"], "v1")

        seen.clear()
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        _run_cc(spy, available={"gemini"}, cached_call=_capture)
        self.assertEqual(seen["tag"], "gemini")


class MetaContractTests(_NoSubstitutionAssertions):
    """공격 4: 부재/실패 구분과 meta 필드."""

    def test_unavailable_meta_shape(self):
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        out = _run_cc(spy, available=set())
        self.assertEqual(spy.calls, [])
        meta = out["meta"]
        self.assertEqual(meta["status"], "unavailable")
        self.assertEqual(meta["reason"], "no configured backend")
        self.assertEqual(meta["candidates"], list(_ALL))
        self.assertNotIn("backend", meta)
        self.assertNotIn("error", meta)
        self.assertEqual(out["cross_category"], [])
        self.assertEqual(out["per_category"], {})
        self.assertNoForeignContent(out, "none")

    def test_unavailable_candidates_reflect_the_configured_order(self):
        spy = _Spy()
        out = _run_cc(spy, available=set(), order=["gemini", "anthropic"])
        self.assertEqual(out["meta"]["candidates"], ["gemini", "anthropic"])
        spy = _Spy()
        out = _run_cc(spy, available=set(), order=[])
        self.assertEqual(out["meta"]["candidates"], [])
        self.assertEqual(out["meta"]["status"], "unavailable")

    def test_failed_meta_carries_backend_and_error(self):
        for backend in _ALL:
            with self.subTest(backend=backend):
                spy = _Spy(**{b: (ValueError("upstream exploded")
                                  if b == backend else _payload(b))
                              for b in _ALL})
                out = _run_cc(spy, available={backend})
                meta = out["meta"]
                self.assertEqual(meta["status"], "failed")
                self.assertEqual(meta["backend"], backend)
                self.assertEqual(meta["error"], "ValueError: upstream exploded")
                self.assertNotIn("candidates", meta)
                self.assertNotIn("reason", meta)
                self.assertEqual(out["cross_category"], [])
                self.assertEqual(out["per_category"], {})
                self.assertNoForeignContent(out, backend)

    def test_failed_and_unavailable_are_distinguishable(self):
        spy = _Spy(anthropic=RuntimeError("x"))
        failed = _run_cc(spy, available={"anthropic"})
        spy2 = _Spy()
        unavailable = _run_cc(spy2, available=set())
        self.assertNotEqual(failed["meta"]["status"],
                            unavailable["meta"]["status"])
        # 두 경로 모두 '빈 결과' 지만 이유가 남는다 — 조용한 대체가 아니다.
        self.assertEqual(failed["cross_category"], [])
        self.assertEqual(unavailable["cross_category"], [])

    def test_failed_error_is_truncated_and_typed(self):
        spy = _Spy(anthropic=RuntimeError("z" * 500))
        out = _run_cc(spy, available={"anthropic"})
        err = out["meta"]["error"]
        self.assertTrue(err.startswith("RuntimeError: "))
        self.assertEqual(len(err) - len("RuntimeError: "), 200)

    def test_meta_is_json_serialisable_for_both_diagnostic_paths(self):
        spy = _Spy(anthropic=RuntimeError("x"))
        json.dumps(_run_cc(spy, available={"anthropic"}), ensure_ascii=False)
        json.dumps(_run_cc(_Spy(), available=set()), ensure_ascii=False)


class BackendOrderTests(_NoSubstitutionAssertions):
    """공격 5: 우선순위를 바꿨을 때 뒤 backend 가 몰래 승격되는지."""

    def test_reordered_first_choice_wins_when_configured(self):
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        out = _run_cc(spy, available=set(_ALL), order=["gemini", "anthropic"])
        self.assertOnlyVendorCalled(spy, "gemini")
        self.assertNoForeignContent(out, "gemini")

    def test_reordered_first_choice_failure_does_not_promote_the_second(self):
        spy = _Spy(gemini=RuntimeError("gemini RESOURCE_EXHAUSTED"),
                   anthropic=_payload("anthropic"),
                   openai=_payload("openai"))
        out = _run_cc(spy, available=set(_ALL), order=["gemini", "anthropic"])
        self.assertOnlyVendorCalled(
            spy, "gemini", "gemini 실패 후 anthropic 이 몰래 승격됐다")
        self.assertEqual(out["meta"]["status"], "failed")
        self.assertEqual(out["meta"]["backend"], "gemini")
        self.assertNoForeignContent(out, "gemini")

    def test_backend_dropped_from_the_order_is_never_called(self):
        """목록에서 빠진 vendor 는 설정돼 있어도 호출되지 않는다."""
        spy = _Spy(**{b: _payload(b) for b in _ALL})
        out = _run_cc(spy, available=set(_ALL), order=["gemini"])
        self.assertOnlyVendorCalled(spy, "gemini")
        spy2 = _Spy(gemini=RuntimeError("boom"), **{"anthropic": _payload("anthropic"),
                                                    "openai": _payload("openai")})
        out2 = _run_cc(spy2, available=set(_ALL), order=["gemini"])
        self.assertOnlyVendorCalled(spy2, "gemini")
        self.assertEqual(out2["meta"]["backend"], "gemini")
        del out

    def test_all_permutations_pick_the_first_configured_entry_only(self):
        import itertools
        for order in itertools.permutations(_ALL):
            for chosen in _ALL:
                configured = {chosen}
                with self.subTest(order=order, configured=chosen):
                    spy = _Spy(**{b: RuntimeError(f"{b} down") for b in _ALL})
                    out = _run_cc(spy, available=configured, order=list(order))
                    self.assertOnlyVendorCalled(spy, chosen)
                    self.assertEqual(out["meta"]["backend"], chosen)


_IMPORT_PROBE = r'''
import importlib, json, os, sys
sys.path.insert(0, sys.argv[1])

CASES = [
    ("default-unset", None),
    ("empty-string", ""),
    ("commas-only", " , , "),
    ("uppercase-and-dupes", " ANTHROPIC , anthropic ,Gemini "),
    ("reordered", "gemini,anthropic"),
    ("single-openai", "openai"),
    ("typo", "anthropi"),
    ("typo-among-valid", "anthropic,openai,claude"),
    ("unsupported-vendor", "cohere"),
    ("empty-plus-typo", " ,bogus, "),
]

# "provider 키가 하나도 없어도 import 는 절대 죽지 않는다" 를 확인하기 위해
# 모든 provider 키를 지운 상태에서 돌린다.
for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "OPENAI_API_KEY",
          "GOOGLE_API_KEY", "GEMINI_API_KEY"):
    os.environ.pop(k, None)

out = []
for name, value in CASES:
    os.environ.pop("EXTRACT_INSIGHTS_CC_BACKENDS", None)
    if value is not None:
        os.environ["EXTRACT_INSIGHTS_CC_BACKENDS"] = value
    sys.modules.pop("extract_insights", None)
    rec = {"case": name}
    try:
        mod = importlib.import_module("extract_insights")
        rec["ok"] = True
        rec["backends"] = list(mod._CC_BACKENDS)
        rec["known"] = list(mod._KNOWN_CC_BACKENDS)
    except SystemExit as e:
        rec["ok"] = False
        rec["kind"] = "SystemExit"
        rec["message"] = str(e)
    except BaseException as e:
        rec["ok"] = False
        rec["kind"] = type(e).__name__
        rec["message"] = str(e)
    out.append(rec)
sys.stdout.write("@@PROBE@@" + json.dumps(out, ensure_ascii=False) + "\n")
'''


class ImportTimeConfigTests(unittest.TestCase):
    """공격 6: import 시 SystemExit 가 발판(footgun)인지 확인."""

    @classmethod
    def setUpClass(cls):
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env.pop("EXTRACT_INSIGHTS_CC_BACKENDS", None)
        proc = subprocess.run(
            [sys.executable, "-c", _IMPORT_PROBE, str(PIPELINE)],
            capture_output=True, text=True, env=env,
            cwd=str(PIPELINE.parent), timeout=300)
        marker = "@@PROBE@@"
        assert marker in proc.stdout, (
            f"probe 실패 rc={proc.returncode}: {proc.stdout[-400:]} "
            f"{proc.stderr[-400:]}")
        payload = proc.stdout.split(marker, 1)[1].splitlines()[0]
        cls.results = {r["case"]: r for r in json.loads(payload)}

    def _case(self, name):
        self.assertIn(name, self.results)
        return self.results[name]

    def test_valid_configurations_import_without_raising(self):
        expected = {
            "default-unset": list(_ALL),
            "empty-string": [],
            "commas-only": [],
            "uppercase-and-dupes": ["anthropic", "gemini"],
            "reordered": ["gemini", "anthropic"],
            "single-openai": ["openai"],
        }
        for name, backends in expected.items():
            with self.subTest(name):
                rec = self._case(name)
                self.assertTrue(
                    rec["ok"],
                    f"정상 설정인데 import 가 죽었다: {rec.get('kind')} "
                    f"{rec.get('message', '')[:160]}")
                self.assertEqual(rec["backends"], backends)

    def test_typoed_backend_fails_loudly_at_import(self):
        for name, typo in [("typo", "anthropi"),
                           ("typo-among-valid", "claude"),
                           ("unsupported-vendor", "cohere"),
                           ("empty-plus-typo", "bogus")]:
            with self.subTest(name):
                rec = self._case(name)
                self.assertFalse(rec["ok"], "오타가 조용히 통과했다")
                self.assertEqual(rec["kind"], "SystemExit")
                self.assertIn(typo, rec["message"])
                # 무엇이 유효한지 알려준다.
                for known in _ALL:
                    self.assertIn(known, rec["message"])

    def test_known_backend_tuple_is_the_validation_source(self):
        rec = self._case("default-unset")
        self.assertEqual(rec["known"], list(_ALL))
        self.assertEqual(rec["backends"], rec["known"])


if __name__ == "__main__":
    unittest.main()
