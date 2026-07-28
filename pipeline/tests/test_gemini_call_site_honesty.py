"""Call sites that only *project* the Gemini key must agree with the resolver too.

pipeline/tests/test_gemini_key_resolver.py pins the resolver seam itself.  This
module pins the three projections that never return the key: the localhost
capability booleans, the insights provider call, and the doctor report.  Each one
regressed independently before the retrofit, and each one is invisible to the
resolver-agreement matrix because none of them returns a key.

No network call is made: the google-genai SDK is replaced by a stub that records
the api_key it was handed.
"""

import contextlib
import io
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
ROOT = PIPELINE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import config_loader  # noqa: E402
import doctor as doctor_module  # noqa: E402
import extract_insights  # noqa: E402
import serve_local  # noqa: E402


# (name, environment, config.json payload, key is usable)
PROJECTION_MATRICES = (
    ("env-only", {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""}, {}, True),
    ("env-alias-only", {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "alias", "PAPER_CURATION_NO_GEMINI": ""}, {}, True),
    ("config-only", {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
     {"gemini_api_key": "config-key"}, True),
    ("config-only-legacy-alias", {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
     {"google_api_key": "legacy-config-key"}, True),
    ("disabled-by-flag", {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": "1"},
     {"gemini_api_key": "config-key"}, False),
    ("nothing-configured", {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""}, {}, False),
)

SECRET = "AIza-call-site-honesty-sentinel"


class _StubModels:
    def __init__(self, client):
        self.client = client

    def generate_content(self, **kwargs):
        raise AssertionError(f"provider was called with api_key={self.client.api_key!r}")


class _StubClient:
    constructed: list = []

    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        self.models = _StubModels(self)
        _StubClient.constructed.append(api_key)


def _stub_sdk():
    genai = types.ModuleType("google.genai")
    genai.Client = _StubClient
    gtypes = types.ModuleType("google.genai.types")

    class _Config:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    gtypes.GenerateContentConfig = _Config
    genai.types = gtypes
    google = types.ModuleType("google")
    google.genai = genai
    return {"google": google, "google.genai": genai, "google.genai.types": gtypes}


def _matrix(env, config):
    return (patch.dict(os.environ, env, clear=False),
            patch.object(config_loader, "load_config", return_value=config))


def _gemini_report(cfg):
    """doctor's real Gemini branch; unrelated Anthropic/TLS probes are stubbed out."""
    reporter = doctor_module.Reporter()
    buffer = io.StringIO()
    status = types.SimpleNamespace(ready=False, mode=None)
    with patch.object(doctor_module, "_check_secret_sources", lambda *a, **k: None), \
            patch.object(doctor_module, "_check_tls_status", lambda *a, **k: None), \
            patch.object(doctor_module, "_check_anthropic_auth", lambda *a, **k: status), \
            contextlib.redirect_stdout(buffer):
        doctor_module.check_api_keys(reporter, cfg)
    text = buffer.getvalue()
    gemini = " | ".join(line.strip() for line in text.splitlines()
                        if "Gemini" in line or "GOOGLE_API_KEY" in line)
    return gemini, reporter, text


class CapabilityProjectionTests(unittest.TestCase):
    def test_capability_booleans_track_the_canonical_resolver(self):
        for name, env, config, usable in PROJECTION_MATRICES:
            with self.subTest(matrix=name):
                env_patch, config_patch = _matrix(env, config)
                with env_patch, config_patch:
                    projections = {
                        "resolve_google_key": serve_local.resolve_google_key() is not None,
                        "gemini_api_key_available": serve_local.gemini_api_key_available(),
                        "audio_capability": serve_local.audio_capability()["state"] == "AVAILABLE",
                    }
                self.assertEqual(set(projections.values()), {usable},
                                 f"capability projections disagree on matrix {name}: {projections}")

    def test_audio_capability_reason_matches_its_state(self):
        for name, env, config, usable in PROJECTION_MATRICES:
            with self.subTest(matrix=name):
                env_patch, config_patch = _matrix(env, config)
                with env_patch, config_patch:
                    capability = serve_local.audio_capability()
                expected = ("AVAILABLE", "READY") if usable else ("UNAVAILABLE", "GEMINI_AUTH_UNAVAILABLE")
                self.assertEqual((capability["state"], capability["reason"]), expected)

    def test_capability_payload_never_carries_the_key(self):
        env_patch, config_patch = _matrix(
            {"GOOGLE_API_KEY": SECRET, "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
            {"gemini_api_key": SECRET},
        )
        with env_patch, config_patch:
            capability = serve_local.audio_capability()
        self.assertEqual(capability["state"], "AVAILABLE")
        self.assertNotIn(SECRET, repr(capability))


class InsightsProviderCallTests(unittest.TestCase):
    def setUp(self):
        _StubClient.constructed = []

    def test_insights_imports_the_canonical_resolver(self):
        self.assertIs(extract_insights.get_google_key, config_loader.get_google_key)

    def test_disable_switch_stops_the_call_before_a_client_exists(self):
        env_patch, config_patch = _matrix(
            {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "alias", "PAPER_CURATION_NO_GEMINI": "1"},
            {"gemini_api_key": "config-key"},
        )
        with env_patch, config_patch, patch.dict(sys.modules, _stub_sdk(), clear=False):
            with self.assertRaises(RuntimeError) as raised:
                extract_insights._cc_gemini_call("prompt", {"name": "x", "input_schema": {}})
        self.assertIn("no Gemini API key", str(raised.exception))
        self.assertEqual(_StubClient.constructed, [])

    def test_config_only_key_still_reaches_the_provider(self):
        env_patch, config_patch = _matrix(
            {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
            {"gemini_api_key": "config-key"},
        )
        with env_patch, config_patch, patch.dict(sys.modules, _stub_sdk(), clear=False):
            with self.assertRaises(AssertionError):  # the stub refuses to talk to a provider
                extract_insights._cc_gemini_call("prompt", {"name": "x", "input_schema": {}})
        self.assertEqual(_StubClient.constructed, ["config-key"])


class DoctorHonestyTests(unittest.TestCase):
    def test_disabled_gemini_is_reported_as_disabled_not_configured(self):
        env_patch, config_patch = _matrix(
            {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": "1"},
            {"gemini_api_key": "config-key"},
        )
        with env_patch, config_patch:
            gemini, reporter, _ = _gemini_report({"gemini_api_key": "config-key"})
        self.assertIn("Gemini optional capability disabled", gemini)
        self.assertNotIn("설정됨", gemini)
        self.assertIn("PAPER_CURATION_NO_GEMINI", gemini)
        self.assertEqual(reporter.fails, 0)

    def test_enabled_gemini_is_still_reported_as_configured(self):
        env_patch, config_patch = _matrix(
            {"GOOGLE_API_KEY": "env-key", "GEMINI_API_KEY": "", "PAPER_CURATION_NO_GEMINI": ""},
            {"gemini_api_key": "config-key"},
        )
        with env_patch, config_patch:
            gemini, reporter, _ = _gemini_report({"gemini_api_key": "config-key"})
        self.assertIn("설정됨", gemini)
        self.assertNotIn("disabled", gemini)
        self.assertEqual(reporter.fails, 0)

    def test_optional_gemini_never_fails_the_diagnosis_or_prints_the_key(self):
        for name, env, config, _usable in PROJECTION_MATRICES:
            with self.subTest(matrix=name):
                secret_env = {key: (SECRET if value and key != "PAPER_CURATION_NO_GEMINI" else value)
                              for key, value in env.items()}
                secret_config = {key: SECRET for key in config}
                env_patch, config_patch = _matrix(secret_env, secret_config)
                with env_patch, config_patch:
                    _, reporter, text = _gemini_report(secret_config)
                self.assertEqual(reporter.fails, 0, f"Gemini is optional; matrix {name} must not fail doctor")
                self.assertNotIn(SECRET, text)


if __name__ == "__main__":
    unittest.main()
