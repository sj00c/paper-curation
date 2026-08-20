"""Injected runtime CLI contracts for query, serve, and deploy."""

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

from paper_curation.application.deploy import DeploymentReceipt
from paper_curation.application.workspace_ops import ValidateWorkspaceResult, WorkspaceIssue
from paper_curation.cli import main
from paper_curation.composition import RuntimeDependencies
from paper_curation.domain.retrieval import Hit

_SECRET = "never-print-this-secret"


def _config(workspace: Path, *, public: bool = False) -> str:
    publication = (
        '{"mode": "public", "base_url": "https://example.test", '
        '"provider": "cloudflare", "config_path": "wrangler.toml"}'
        if public else '{"mode": "local", "base_url": ""}'
    )
    return f'''{{
  "workspace": {{"root": "{workspace}"}},
  "source": {{"provider": "zotero", "transport": "local-sqlite", "sqlite_path": "{workspace}/source.sqlite", "collections": {{"demo": "Demo"}}}},
  "core": {{"review": {{"provider": "local-model", "model": "configured-model", "local_endpoint": "http://localhost"}}}},
  "features": {{}},
  "credentials": {{"zotero_api_key": "{_SECRET}", "anthropic_api_key": "", "google_api_key": "", "gemini_api_key": "", "openai_api_key": ""}},
  "search_keywords": {{}}, "topic_profiles": {{}},
  "publication": {publication},
  "operator": {{"name": "", "organization": "", "email": ""}},
  "notifications": {{"completion_email": ""}}
}}'''


class _Query:
    calls: list[tuple[str, object]] = []

    def search(self, topic, query):  # type: ignore[no-untyped-def]
        type(self).calls.append((topic, query))
        return (Hit("chunk-1", "record-1", "Abstract", 1.0, 1, ("lexical",)),)


class _Handle:
    closed = 0
    waited = 0
    url = "http://127.0.0.1:8123"

    def wait(self) -> None:
        type(self).waited += 1

    def close(self) -> None:
        type(self).closed += 1


class _Server:
    calls: list[object] = []

    def start(self, plan):  # type: ignore[no-untyped-def]
        type(self).calls.append(plan)
        return _Handle()


class _Workspace:
    invalid = False

    def validate(self):  # type: ignore[no-untyped-def]
        if type(self).invalid:
            return ValidateWorkspaceResult((WorkspaceIssue(Path("bad"), "invalid"),))
        return ValidateWorkspaceResult(())


class _Deployment:
    calls: list[object] = []
    token = ""

    def __init__(self, token, *, environment):  # type: ignore[no-untyped-def]
        type(self).token = token

    def deploy(self, plan):  # type: ignore[no-untyped-def]
        type(self).calls.append(plan)
        return DeploymentReceipt(("deploy",), 0, "", "", plan.base_url)


def _dependencies() -> RuntimeDependencies:
    return RuntimeDependencies(
        local_retrieval=lambda workspace, topic, source, scope: _Query(),
        server=_Server,
        workspace_ops=lambda workspace: _Workspace(),
        cloudflare_deployment=_Deployment,
    )


class RuntimeCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.workspace = self.root / "workspace"
        (self.workspace / "site").mkdir(parents=True)
        (self.workspace / "site" / "index.html").write_text("ok", encoding="utf-8")
        (self.workspace / "wrangler.toml").write_text("name = 'demo'", encoding="utf-8")
        self.local = self.root / "local.json"
        self.public = self.root / "public.json"
        self.local.write_text(_config(self.workspace), encoding="utf-8")
        self.public.write_text(_config(self.workspace, public=True), encoding="utf-8")
        _Query.calls = []
        _Server.calls = []
        _Handle.closed = 0
        _Handle.waited = 0
        _Workspace.invalid = False
        _Deployment.calls = []
        _Deployment.token = ""

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(self, *argv: str, environment: dict[str, str] | None = None) -> tuple[int, str]:
        output = StringIO()
        with redirect_stdout(output):
            code = main(argv, runtime_dependencies=_dependencies(), environment=environment)
        return code, output.getvalue()

    def test_query_is_lexical_only_and_prints_citeable_identity(self) -> None:
        code, output = self.run_cli(
            "query", "--config", str(self.local), "--topic", "demo", "--query", "terms", "--limit", "3"
        )
        self.assertEqual(code, 0)
        self.assertEqual(len(_Query.calls), 1)
        self.assertEqual(_Query.calls[0][1].limit, 3)
        self.assertIn("rank=1 record=record-1 section=Abstract chunk=chunk-1", output)

    def test_query_rejects_unknown_topic_without_retrieval(self) -> None:
        code, output = self.run_cli(
            "query", "--config", str(self.local), "--topic", "unknown", "--query", "terms"
        )
        self.assertEqual(code, 1)
        self.assertEqual(_Query.calls, [])
        self.assertNotIn(_SECRET, output)

    def test_serve_preview_never_binds_and_start_waits_then_closes(self) -> None:
        code, _ = self.run_cli("serve", "--config", str(self.local), "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(_Server.calls, [])
        code, output = self.run_cli("serve", "--config", str(self.local), "--port", "0")
        self.assertEqual(code, 0)
        self.assertIn(_Handle.url, output)
        self.assertEqual(len(_Server.calls), 1)
        self.assertEqual(_Handle.waited, 1)
        self.assertEqual(_Handle.closed, 1)

    def test_serve_requires_explicit_public_bind(self) -> None:
        code, _ = self.run_cli("serve", "--config", str(self.local), "--host", "0.0.0.0", "--dry-run")
        self.assertEqual(code, 1)
        code, _ = self.run_cli(
            "serve", "--config", str(self.local), "--host", "0.0.0.0", "--public-bind", "--dry-run"
        )
        self.assertEqual(code, 0)

    def test_deploy_refuses_local_and_previews_public_without_adapter_call(self) -> None:
        code, _ = self.run_cli("deploy", "--config", str(self.local))
        self.assertEqual(code, 1)
        self.assertEqual(_Deployment.calls, [])
        self.assertEqual(_Deployment.token, "")
        code, output = self.run_cli("deploy", "--config", str(self.public))
        self.assertEqual(code, 0)
        self.assertIn("preview", output)
        self.assertEqual(_Deployment.calls, [])

    def test_deploy_executes_exact_public_target_only_after_validation(self) -> None:
        code, output = self.run_cli(
            "deploy", "--config", str(self.public), "--execute", environment={"CLOUDFLARE_API_TOKEN": _SECRET}
        )
        self.assertEqual(code, 0)
        self.assertEqual(len(_Deployment.calls), 1)
        plan = _Deployment.calls[0]
        self.assertEqual(plan.config, self.workspace.resolve() / "wrangler.toml")
        self.assertEqual(_Deployment.token, _SECRET)
        self.assertNotIn(_SECRET, output)

    def test_deploy_validation_failure_and_missing_token_do_not_leak_or_deploy(self) -> None:
        _Workspace.invalid = True
        code, output = self.run_cli("deploy", "--config", str(self.public), "--execute")
        self.assertEqual(code, 1)
        self.assertEqual(_Deployment.calls, [])
        self.assertNotIn(_SECRET, output)
        _Workspace.invalid = False
        code, output = self.run_cli("deploy", "--config", str(self.public), "--execute")
        self.assertEqual(code, 1)
        self.assertEqual(_Deployment.calls, [])
        self.assertNotIn(_SECRET, output)


if __name__ == "__main__":
    unittest.main()
