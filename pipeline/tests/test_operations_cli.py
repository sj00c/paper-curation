"""Injected CLI contracts for local operational commands."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from paper_curation.application.diagnostics import ProbeResult
from paper_curation.application.workspace_ops import (
    BuildWorkspaceResult,
    ValidateWorkspaceResult,
    WorkspaceIssue,
)
from paper_curation.composition import OperationsDependencies
from paper_curation.cli import main


_SECRET = "never-print-this-secret"


def _config(workspace: Path) -> str:
    return f'''{{
  "workspace": {{"root": "{workspace}"}},
  "source": {{"provider": "zotero", "transport": "local-sqlite", "sqlite_path": "{workspace}/source.sqlite", "collections": {{"demo": "Demo"}}}},
  "core": {{"review": {{"provider": "local-model", "model": "configured-model", "local_endpoint": "http://localhost"}}}},
  "features": {{}},
  "credentials": {{"zotero_api_key": "{_SECRET}", "anthropic_api_key": "", "google_api_key": "", "gemini_api_key": "", "openai_api_key": ""}},
  "search_keywords": {{"demo": {{"primary": ["demo"], "secondary": []}}}}, "topic_profiles": {{"demo": {{"title": "Demo"}}}},
  "publication": {{"mode": "local", "base_url": ""}},
  "operator": {{"name": "", "organization": "", "email": ""}},
  "notifications": {{"completion_email": ""}}
}}'''


class _Writer:
    calls = 0

    def write(self, plan):  # type: ignore[no-untyped-def]
        type(self).calls += 1
        from paper_curation.application.setup import SetupResult
        return SetupResult(plan.target_path, plan.workspace_directories, plan.backup_path)


class _Probes:
    networks: list[bool] = []

    def python_312(self): return ProbeResult(True)
    def workspace_readable(self, location): return ProbeResult(True)
    def workspace_writable(self, location): return ProbeResult(True)
    def source_ready(self, transport, *, network):
        type(self).networks.append(network)
        return ProbeResult(True)
    def core_provider_ready(self, provider, *, network):
        type(self).networks.append(network)
        return ProbeResult(True)
    def required_dependencies(self): return ()
    def enhancement_ready(self, capability, feature, *, network): return ProbeResult(True)


class _Workspace:
    calls: list[object] = []
    invalid = False

    def build(self):
        type(self).calls.append("build")
        return BuildWorkspaceResult(Path("/workspace/site/index.html"), ())

    def validate(self):
        type(self).calls.append("validate")
        issues = (WorkspaceIssue(Path("/workspace/papers/bad"), "invalid"),) if type(self).invalid else ()
        return ValidateWorkspaceResult(issues)

    def repair(self, *, execute):
        type(self).calls.append(("repair", execute))
        from paper_curation.application.workspace_ops import RepairWorkspaceResult
        return RepairWorkspaceResult((), execute)


def _dependencies() -> OperationsDependencies:
    return OperationsDependencies(
        config_writer=_Writer,
        diagnostics_probes=lambda config, *, environment: _Probes(),
        workspace_ops=lambda root: _Workspace(),
    )


class OperationsCliTests(unittest.TestCase):
    def setUp(self) -> None:
        _Writer.calls = 0
        _Probes.networks = []
        _Workspace.calls = []
        _Workspace.invalid = False
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input = self.root / "input.json"
        self.input.write_text(_config(self.root / "workspace"), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *argv: str) -> tuple[int, str]:
        output = StringIO()
        with redirect_stdout(output):
            code = main(argv, operations_dependencies=_dependencies())
        return code, output.getvalue()

    def test_setup_is_preview_first_and_secret_safe(self) -> None:
        target = self.root / "config.json"
        code, output = self.run_cli("setup", "--input", str(self.input), "--config", str(target))
        self.assertEqual(code, 0)
        self.assertEqual(_Writer.calls, 0)
        self.assertFalse(target.exists())
        self.assertNotIn(_SECRET, output)
        self.assertTrue(all(line.startswith("/") for line in output.splitlines()))

        code, _ = self.run_cli("setup", "--input", str(self.input), "--config", str(target), "--execute")
        self.assertEqual(code, 0)
        self.assertEqual(_Writer.calls, 1)

    def test_inspect_and_doctor_are_read_only_with_network_opt_in(self) -> None:
        code, output = self.run_cli("inspect", "--config", str(self.input))
        self.assertEqual(code, 0)
        self.assertNotIn(_SECRET, output)
        self.assertEqual(_Workspace.calls, [])
        self.assertEqual(_Writer.calls, 0)

        code, _ = self.run_cli("doctor", "--config", str(self.input))
        self.assertEqual(code, 0)
        self.assertEqual(_Probes.networks, [False, False])
        code, _ = self.run_cli("doctor", "--config", str(self.input), "--network")
        self.assertEqual(code, 0)
        self.assertEqual(_Probes.networks[-2:], [True, True])

    def test_build_validate_and_repair_use_local_workspace_operations(self) -> None:
        code, _ = self.run_cli("build", "--config", str(self.input))
        self.assertEqual(code, 0)
        self.assertEqual(_Workspace.calls, ["build"])

        _Workspace.calls = []
        _Workspace.invalid = True
        code, _ = self.run_cli("validate", "--config", str(self.input))
        self.assertEqual(code, 1)
        self.assertEqual(_Workspace.calls, ["validate"])

        _Workspace.calls = []
        code, _ = self.run_cli("repair", "--config", str(self.input))
        self.assertEqual(code, 0)
        code, _ = self.run_cli("repair", "--config", str(self.input), "--execute")
        self.assertEqual(code, 0)
        self.assertEqual(_Workspace.calls, [("repair", False), ("repair", True)])

    def test_strict_configuration_errors_are_nonzero_and_secret_safe(self) -> None:
        malformed = self.root / "malformed.json"
        malformed.write_text('{"credentials": {"zotero_api_key": "never-print-this-secret"}}', encoding="utf-8")
        code, output = self.run_cli("validate", "--config", str(malformed))
        self.assertEqual(code, 1)
        self.assertNotIn(_SECRET, output)


if __name__ == "__main__":
    unittest.main()
