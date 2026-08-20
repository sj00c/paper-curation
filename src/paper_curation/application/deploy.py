"""Explicit public-site deployment use case.

The application decides whether deployment is allowed.  It never selects a
provider, reads credentials, or performs a deployment itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Protocol
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class DeploymentPlan:
    """The fully selected deployment target passed to an outer adapter."""

    workspace: Path
    site: Path
    config: Path
    base_url: str


@dataclass(frozen=True, slots=True)
class DeploymentReceipt:
    """Sanitized result returned by a deployment adapter."""

    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    base_url: str


class DeploymentPort(Protocol):
    """Outer boundary for one selected deployment target."""

    def deploy(self, plan: DeploymentPlan) -> DeploymentReceipt:
        """Deploy exactly ``plan`` or raise an adapter-specific error."""


@dataclass(frozen=True, slots=True)
class DeployRequest:
    """Evidence and explicit intent required to publish a built local site."""

    workspace: Path
    site: Path
    config: Path
    publication_mode: str
    base_url: str
    built: bool
    validated: bool
    execute: bool = False


class DeployStatus(StrEnum):
    REFUSED = "refused"
    PREVIEW = "preview"
    DEPLOYED = "deployed"


@dataclass(frozen=True, slots=True)
class DeployResult:
    """A refusal/preview has no receipt because no adapter was called."""

    status: DeployStatus
    reason: str
    plan: DeploymentPlan | None = None
    receipt: DeploymentReceipt | None = None


def _absolute_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return (
        bool(value.strip())
        and parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
        and not parsed.username
        and not parsed.password
    )


def _contained(workspace: Path, path: Path) -> bool:
    try:
        path.relative_to(workspace)
    except ValueError:
        return False
    return True


@dataclass(frozen=True, slots=True)
class DeploySite:
    """Authorize an explicit public deployment and invoke the injected port."""

    deployment: DeploymentPort

    def run(self, request: DeployRequest) -> DeployResult:
        """Deploy only an explicitly built and validated public site."""

        if request.publication_mode.strip().lower() != "public":
            return DeployResult(DeployStatus.REFUSED, "publication.mode must be public")
        if not _absolute_http_url(request.base_url):
            return DeployResult(DeployStatus.REFUSED, "publication.base_url must be an absolute HTTP(S) URL")
        if not request.built:
            return DeployResult(DeployStatus.REFUSED, "a local site build is required")
        if not request.validated:
            return DeployResult(DeployStatus.REFUSED, "a validated local site build is required")

        workspace = Path(request.workspace)
        site = Path(request.site)
        config = Path(request.config)
        if not workspace.is_absolute() or not site.is_absolute() or not config.is_absolute():
            return DeployResult(DeployStatus.REFUSED, "workspace, site, and config must be absolute paths")
        if not _contained(workspace, site) or not _contained(workspace, config):
            return DeployResult(DeployStatus.REFUSED, "site and config must remain inside the workspace")

        plan = DeploymentPlan(workspace, site, config, request.base_url.rstrip("/"))
        if not request.execute:
            return DeployResult(DeployStatus.PREVIEW, "deployment requires explicit execute", plan)

        receipt = self.deployment.deploy(plan)
        return DeployResult(DeployStatus.DEPLOYED, "deployment completed", plan, receipt)

    __call__ = run
