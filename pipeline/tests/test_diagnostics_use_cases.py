"""Contracts for the read-only installation diagnostics use cases."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.application.diagnostics import (
    DoctorInstallation,
    DoctorRequest,
    InspectInstallation,
    ProbeResult,
)
from paper_curation.config.models import AppConfig, FeatureConfig


def config_for(*, feature_enabled: bool = False) -> AppConfig:
    return AppConfig.from_mapping({
        "workspace": {"root": "/workspace"},
        "source": {
            "provider": "zotero",
            "transport": "local-sqlite",
            "sqlite_path": "/workspace/source.sqlite",
            "collections": {"unfamiliar-scope": "Anything"},
        },
        "core": {"review": {"provider": "anthropic-api", "model": "configured-model"}},
        "features": {
            "optional-search": {
                "enabled": feature_enabled,
                "provider": "openai" if feature_enabled else "",
            },
            "disabled-provider": {"enabled": False, "provider": ""},
        },
        "credentials": {"anthropic_api_key": "core-secret", "openai_api_key": "optional-secret"},
        "search_keywords": {},
        "topic_profiles": {},
        "publication": {"mode": "local", "base_url": ""},
    })


class RecordingProbes:
    def __init__(self, *, core_ready: bool = True, optional_ready: bool = True) -> None:
        self.core_ready = core_ready
        self.optional_ready = optional_ready
        self.calls: list[object] = []

    def python_312(self) -> ProbeResult:
        self.calls.append("python")
        return ProbeResult(True)

    def workspace_readable(self, location: str) -> ProbeResult:
        self.calls.append(("read", location))
        return ProbeResult(True)

    def workspace_writable(self, location: str) -> ProbeResult:
        self.calls.append(("write-check", location))
        return ProbeResult(True)

    def source_ready(self, transport: str, *, network: bool) -> ProbeResult:
        self.calls.append(("source", transport, network))
        return ProbeResult(True)

    def core_provider_ready(self, provider: str, *, network: bool) -> ProbeResult:
        self.calls.append(("core", provider, network))
        return ProbeResult(self.core_ready, "Core unavailable" if not self.core_ready else "ready")

    def required_dependencies(self):
        self.calls.append("dependencies")
        return (("package.example", ProbeResult(True)),)

    def enhancement_ready(self, capability: str, feature: FeatureConfig, *, network: bool) -> ProbeResult:
        self.calls.append(("enhancement", capability, feature.provider, network))
        return ProbeResult(self.optional_ready, "optional unavailable" if not self.optional_ready else "ready")


class DiagnosticsUseCaseTests(unittest.TestCase):
    def test_inspect_reports_domain_neutral_scopes_without_secrets(self) -> None:
        result = InspectInstallation(config_for()).execute()
        self.assertEqual(result.configured_scopes, ("unfamiliar-scope",))
        self.assertEqual(result.core_review_cost_class, "metered")
        rendered = repr(result)
        self.assertNotIn("core-secret", rendered)
        self.assertNotIn("optional-secret", rendered)

    def test_doctor_is_read_only_and_skips_disabled_enhancements(self) -> None:
        probes = RecordingProbes()
        result = DoctorInstallation(config_for(), probes).execute()
        self.assertTrue(result.core_healthy)
        self.assertNotIn("write", probes.calls)
        self.assertFalse(any(isinstance(call, tuple) and call[0] == "enhancement" for call in probes.calls))
        self.assertNotIn("disabled-provider", repr(probes.calls))

    def test_optional_failure_is_scoped_warning_not_core_failure(self) -> None:
        result = DoctorInstallation(config_for(feature_enabled=True), RecordingProbes(optional_ready=False)).execute()
        optional = next(item for item in result.diagnostics if item.code == "enhancement.optional-search")
        self.assertEqual(optional.severity, "warning")
        self.assertEqual(optional.capability, "optional-search")
        self.assertTrue(result.core_healthy)
        self.assertEqual(result.exit_code, 0)

    def test_core_failure_is_an_error(self) -> None:
        result = DoctorInstallation(config_for(), RecordingProbes(core_ready=False)).execute()
        core = next(item for item in result.diagnostics if item.code == "core.review_provider")
        self.assertEqual(core.severity, "error")
        self.assertFalse(result.core_healthy)
        self.assertEqual(result.exit_code, 1)

    def test_network_is_opt_in(self) -> None:
        probes = RecordingProbes()
        DoctorInstallation(config_for(feature_enabled=True), probes).execute()
        self.assertFalse(any(isinstance(call, tuple) and call[-1] is True for call in probes.calls))
        probes = RecordingProbes()
        DoctorInstallation(config_for(feature_enabled=True), probes).execute(DoctorRequest(network=True))
        self.assertTrue(any(isinstance(call, tuple) and call[-1] is True for call in probes.calls))


if __name__ == "__main__":
    unittest.main()
