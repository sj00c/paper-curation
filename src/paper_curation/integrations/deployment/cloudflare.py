"""Cloudflare Workers deployment adapter.

This adapter receives one fully selected target.  It deliberately does not
inspect configuration to find a different account, project, URL, or provider.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
from typing import Callable, Mapping

from paper_curation.application.deploy import DeploymentPlan, DeploymentReceipt


class DeploymentError(RuntimeError):
    """A selected Cloudflare target failed; callers must surface the failure."""

    def __init__(self, receipt: DeploymentReceipt) -> None:
        super().__init__(f"Cloudflare deployment failed with exit status {receipt.returncode}")
        self.receipt = receipt


def _inside(workspace: Path, candidate: Path) -> Path:
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(workspace)
    except ValueError as error:
        raise ValueError("deployment paths must remain inside the workspace") from error
    return resolved


def _sanitize(value: str, credential: str) -> str:
    return value.replace(credential, "[REDACTED]") if credential else value


@dataclass(frozen=True, slots=True)
class CloudflareDeployment:
    """Run one configured ``wrangler deploy`` command for a local site."""

    api_token: str
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run
    environment: Mapping[str, str] | None = None

    def deploy(self, plan: DeploymentPlan) -> DeploymentReceipt:
        """Deploy the selected workspace site, without a fallback target."""

        if not self.api_token.strip():
            raise ValueError("CLOUDFLARE_API_TOKEN is required for Cloudflare deployment")

        workspace = Path(plan.workspace).resolve(strict=False)
        if not workspace.is_absolute():  # Defensive: resolve() is normally absolute.
            raise ValueError("workspace must be an absolute path")
        site = _inside(workspace, Path(plan.site))
        config = _inside(workspace, Path(plan.config))
        if not site.is_dir() or not (site / "index.html").is_file():
            raise ValueError("a built site directory containing index.html is required")
        if not config.is_file():
            raise ValueError("a configured wrangler config file is required")

        command = (
            "npx", "wrangler", "deploy",
            "--config", str(config),
            "--assets", str(site),
        )
        environment = dict(os.environ if self.environment is None else self.environment)
        environment["CLOUDFLARE_API_TOKEN"] = self.api_token
        completed = self.runner(
            command,
            cwd=str(workspace),
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        receipt = DeploymentReceipt(
            command=command,
            returncode=completed.returncode,
            stdout=_sanitize(completed.stdout or "", self.api_token),
            stderr=_sanitize(completed.stderr or "", self.api_token),
            base_url=plan.base_url,
        )
        if completed.returncode != 0:
            raise DeploymentError(receipt)
        return receipt
