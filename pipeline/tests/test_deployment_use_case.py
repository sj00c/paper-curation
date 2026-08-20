"""Contracts for explicit public Cloudflare deployment."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.application.deploy import (
    DeployRequest,
    DeploySite,
    DeployStatus,
    DeploymentPlan,
    DeploymentReceipt,
)
from paper_curation.integrations.deployment.cloudflare import CloudflareDeployment, DeploymentError


@dataclass
class RecordingPort:
    calls: list[DeploymentPlan] = field(default_factory=list)

    def deploy(self, plan: DeploymentPlan) -> DeploymentReceipt:
        self.calls.append(plan)
        return DeploymentReceipt(("fake",), 0, "", "", plan.base_url)


class RecordingRunner:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        self.calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, self.returncode, self.stdout, self.stderr)


def request(root: Path, **changes: object) -> DeployRequest:
    values: dict[str, object] = {
        "workspace": root,
        "site": root / "site",
        "config": root / "wrangler.toml",
        "publication_mode": "public",
        "base_url": "https://papers.example.test/catalog/",
        "built": True,
        "validated": True,
        "execute": False,
    }
    values.update(changes)
    return DeployRequest(**values)  # type: ignore[arg-type]


class DeploySiteTests(unittest.TestCase):
    def test_local_mode_is_refused_without_adapter_call(self) -> None:
        port = RecordingPort()
        result = DeploySite(port).run(request(Path("/workspace"), publication_mode="local", execute=True))
        self.assertEqual(result.status, DeployStatus.REFUSED)
        self.assertEqual(port.calls, [])

    def test_preview_never_calls_adapter(self) -> None:
        port = RecordingPort()
        result = DeploySite(port).run(request(Path("/workspace")))
        self.assertEqual(result.status, DeployStatus.PREVIEW)
        self.assertEqual(port.calls, [])
        self.assertEqual(result.plan.base_url, "https://papers.example.test/catalog")  # type: ignore[union-attr]

    def test_missing_or_unvalidated_build_is_refused(self) -> None:
        port = RecordingPort()
        deploy = DeploySite(port)
        self.assertEqual(deploy.run(request(Path("/workspace"), built=False, execute=True)).status, DeployStatus.REFUSED)
        self.assertEqual(deploy.run(request(Path("/workspace"), validated=False, execute=True)).status, DeployStatus.REFUSED)
        self.assertEqual(port.calls, [])


class CloudflareDeploymentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "site").mkdir()
        (self.root / "site" / "index.html").write_text("site", encoding="utf-8")
        (self.root / "wrangler.toml").write_text("name = 'configured-target'", encoding="utf-8")
        self.plan = DeploymentPlan(
            self.root,
            self.root / "site",
            self.root / "wrangler.toml",
            "https://papers.example.test/catalog",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_execute_uses_one_exact_configured_command(self) -> None:
        runner = RecordingRunner(stdout="uploaded")
        receipt = CloudflareDeployment("token-value", runner, {}).deploy(self.plan)
        command, kwargs = runner.calls[0]
        workspace = self.root.resolve()
        self.assertEqual(runner.calls[0][0], (
            "npx", "wrangler", "deploy", "--config", str(workspace / "wrangler.toml"),
            "--assets", str(workspace / "site"),
        ))
        self.assertEqual(len(runner.calls), 1)
        self.assertEqual(kwargs["cwd"], str(workspace))
        self.assertEqual(kwargs["env"], {"CLOUDFLARE_API_TOKEN": "token-value"})
        self.assertEqual(receipt.command, command)
        self.assertEqual(receipt.base_url, self.plan.base_url)

    def test_selected_target_failure_has_no_fallback(self) -> None:
        runner = RecordingRunner(returncode=1, stderr="configured target failed")
        adapter = CloudflareDeployment("token-value", runner, {})
        with self.assertRaises(DeploymentError) as raised:
            adapter.deploy(self.plan)
        self.assertEqual(len(runner.calls), 1)
        self.assertEqual(raised.exception.receipt.returncode, 1)
        self.assertEqual(raised.exception.receipt.stderr, "configured target failed")

    def test_missing_local_build_never_invokes_wrangler(self) -> None:
        (self.root / "site" / "index.html").unlink()
        runner = RecordingRunner()
        with self.assertRaisesRegex(ValueError, "built site"):
            CloudflareDeployment("token-value", runner, {}).deploy(self.plan)
        self.assertEqual(runner.calls, [])

    def test_receipt_redacts_credential_and_reports_success(self) -> None:
        runner = RecordingRunner(stdout="deployed token-value", stderr="token-value")
        receipt = CloudflareDeployment("token-value", runner, {}).deploy(self.plan)
        self.assertEqual(receipt.returncode, 0)
        self.assertEqual(receipt.stdout, "deployed [REDACTED]")
        self.assertEqual(receipt.stderr, "[REDACTED]")
        self.assertNotIn("token-value", repr(receipt))


if __name__ == "__main__":
    unittest.main()
