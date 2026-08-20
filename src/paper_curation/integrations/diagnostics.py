"""Read-only system probes for installation diagnostics."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
import importlib.util
import os
from pathlib import Path
import shutil
import sys

from paper_curation.application.diagnostics import ProbeResult
from paper_curation.config.models import AppConfig, FeatureConfig


NetworkProbe = Callable[[str], bool]
PathAccess = Callable[[str | Path, int], bool]
PathExists = Callable[[str | Path], bool]
CommandLookup = Callable[[str], str | None]
PackageLookup = Callable[[str], object | None]


def _path_exists(location: str | Path) -> bool:
    return Path(location).exists()


@dataclass(frozen=True, slots=True)
class SystemDiagnosticsProbes:
    """Local checks for the configured installation; none create or modify files."""

    config: AppConfig
    environment: Mapping[str, str] = field(default_factory=lambda: dict(os.environ), repr=False)
    path_access: PathAccess = os.access
    path_exists: PathExists = _path_exists
    command_lookup: CommandLookup = shutil.which
    package_lookup: PackageLookup = importlib.util.find_spec
    network_probe: NetworkProbe | None = None

    def _network_ready(self, target: str, *, network: bool) -> ProbeResult:
        if not network:
            return ProbeResult(True, "network probe not requested")
        if self.network_probe is None:
            return ProbeResult(False, "network probe is not configured")
        try:
            ready = bool(self.network_probe(target))
        except Exception:
            ready = False
        return ProbeResult(ready, "network reachable" if ready else "network probe failed")

    def python_312(self) -> ProbeResult:
        ready = sys.version_info[:2] == (3, 12)
        return ProbeResult(ready, "Python 3.12 available" if ready else "Python 3.12 is required")

    def workspace_readable(self, location: str) -> ProbeResult:
        ready = self.path_exists(location) and self.path_access(location, os.R_OK)
        return ProbeResult(ready, "workspace is readable" if ready else "workspace is not readable")

    def workspace_writable(self, location: str) -> ProbeResult:
        ready = self.path_exists(location) and self.path_access(location, os.W_OK)
        return ProbeResult(ready, "workspace is writable" if ready else "workspace is not writable")

    def source_ready(self, transport: str, *, network: bool) -> ProbeResult:
        if transport == "local-sqlite":
            ready = self.path_exists(self.config.source.sqlite_path)
            return ProbeResult(ready, "local source is available" if ready else "local source is unavailable")
        credential = self.config.credentials.zotero_api_key or self.environment.get("ZOTERO_API_KEY", "")
        if not credential.strip():
            return ProbeResult(False, "source credential is unavailable")
        return self._network_ready("source:zotero-storage", network=network)

    def core_provider_ready(self, provider: str, *, network: bool) -> ProbeResult:
        if provider == "claude-code-oauth":
            credential_path = Path.home() / ".claude" / ".credentials.json"
            authenticated = bool(self.environment.get("CLAUDE_CODE_OAUTH_TOKEN", "").strip()) or self.path_exists(credential_path)
            ready = authenticated and self.command_lookup("claude") is not None
            if not ready:
                return ProbeResult(False, "selected Core provider is unavailable")
        elif provider == "anthropic-api":
            ready = bool((self.config.credentials.anthropic_api_key or self.environment.get("ANTHROPIC_API_KEY", "")).strip())
            if not ready:
                return ProbeResult(False, "selected Core provider is unavailable")
        elif provider == "local-model":
            if not self.config.core.review.local_endpoint.strip():
                return ProbeResult(False, "selected Core provider is unavailable")
        else:
            return ProbeResult(False, "selected Core provider is unsupported")
        return self._network_ready(f"core:{provider}", network=network)

    def required_dependencies(self) -> Iterable[tuple[str, ProbeResult]]:
        packages = ["fitz"]
        if self.config.core.review.provider == "anthropic-api":
            packages.append("anthropic")
        for package in packages:
            ready = self.package_lookup(package) is not None
            yield (
                f"package.{package}",
                ProbeResult(ready, f"required package {package} is available" if ready else f"required package {package} is unavailable"),
            )

    def enhancement_ready(self, capability: str, feature: FeatureConfig, *, network: bool) -> ProbeResult:
        provider = feature.provider
        if provider in {"google", "gemini"}:
            ready = bool((
                self.config.credentials.google_api_key
                or self.config.credentials.gemini_api_key
                or self.environment.get("GOOGLE_API_KEY", "")
                or self.environment.get("GEMINI_API_KEY", "")
            ).strip())
        elif provider == "openai":
            ready = bool((self.config.credentials.openai_api_key or self.environment.get("OPENAI_API_KEY", "")).strip())
        elif provider == "paperbanana":
            directory = self.environment.get("PAPERBANANA_DIR", "")
            ready = bool(directory) and Path(directory).is_dir()
        elif provider == "local-model":
            ready = bool(self.config.core.review.local_endpoint.strip())
        else:
            return ProbeResult(False, "enabled enhancement provider is unsupported")
        if not ready:
            return ProbeResult(False, "enabled enhancement provider is unavailable")
        return self._network_ready(f"enhancement:{capability}:{provider}", network=network)
