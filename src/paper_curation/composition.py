"""Composition roots for the mandatory local Core paths."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_curation.application.curate import CuratePaper
from paper_curation.application.deploy import DeploySite
from paper_curation.application.diagnostics import DoctorInstallation, InspectInstallation
from paper_curation.application.serve import ServeSite
from paper_curation.application.setup import SetupUseCase
from paper_curation.application.update import UpdateCore
from paper_curation.application.workspace_ops import BuildWorkspace, RepairWorkspace, ValidateWorkspace
from paper_curation.capabilities import Capabilities, detect_capabilities
from paper_curation.config.models import AppConfig
from paper_curation.errors import ConfigValidationError
from paper_curation.integrations.diagnostics import SystemDiagnosticsProbes
from paper_curation.integrations.deployment.cloudflare import CloudflareDeployment
from paper_curation.integrations.persistence import (
    FilesystemEvidenceVerifier,
    FilesystemPage,
    FilesystemReceipt,
    FilesystemSidecar,
    FilesystemStagedAttachment,
    FilesystemStagedReview,
)
from paper_curation.integrations.persistence.configuration import FilesystemConfigWriter
from paper_curation.integrations.persistence.workspace_ops import FilesystemWorkspaceOps
from paper_curation.integrations.providers.review import (
    AnthropicAPIReviewAdapter,
    ClaudeCodeOAuthReviewAdapter,
    LocalModelReviewAdapter,
)
from paper_curation.integrations.text.pymupdf import PyMuPDFTextExtractor
from paper_curation.integrations.server import LocalStaticServer
from paper_curation.integrations.zotero.api import (
    ZoteroStorageAttachmentPort,
    ZoteroStorageSource,
)
from paper_curation.integrations.zotero.local import ZoteroLocalAttachmentPort, ZoteroLocalSource
from paper_curation.retrieval.local import local_lexical_retrieval_use_case


def _anthropic_client(api_key: str) -> Any:
    try:
        from anthropic import Anthropic
    except ImportError as exc:  # pragma: no cover - installation failure
        raise RuntimeError("Anthropic API support requires the anthropic package") from exc
    return Anthropic(api_key=api_key)


def _environment_credential(environment: Mapping[str, str], configured: str, name: str) -> str:
    value = environment.get(name, "").strip()
    return value or configured


def _close_resource(resource: Any) -> None:
    close = getattr(resource, "close", None)
    if callable(close):
        close()


def _close_resources(resources: tuple[Any, ...], *, raise_errors: bool) -> None:
    first_error: Exception | None = None
    for resource in reversed(resources):
        try:
            _close_resource(resource)
        except Exception as error:
            if first_error is None:
                first_error = error
    if raise_errors and first_error is not None:
        raise first_error


def require_installed_features(config: AppConfig) -> None:
    """Reject selected enhancements until their production adapter is installed."""
    enabled = sorted(name for name, feature in config.features.items() if feature.enabled)
    if enabled:
        raise ConfigValidationError(
            "features",
            "selected enhancements are not installed: " + ", ".join(enabled),
        )


@dataclass(frozen=True, slots=True)
class CoreComposition:
    """The assembled Core use case and its read-only source for selection."""

    update: UpdateCore
    source: Any
    review_provider_id: str
    capabilities: Capabilities
    resources: tuple[Any, ...] = ()

    def close(self) -> None:
        _close_resources(self.resources, raise_errors=True)


@dataclass(frozen=True, slots=True)
class CoreSelectionComposition:
    """Side-effect-free provider/source selection used by update previews."""

    source: Any
    review_provider_id: str
    review_model: str
    capabilities: Capabilities
    resources: tuple[Any, ...] = ()

    def close(self) -> None:
        _close_resources(self.resources, raise_errors=True)


@dataclass(frozen=True, slots=True)
class CompositionDependencies:
    """Injectable concrete constructors for focused CLI and composition tests."""

    detect_capabilities: Callable[..., Capabilities] = detect_capabilities
    zotero_source: Callable[[str | Path], Any] = ZoteroLocalSource
    zotero_attachments: Callable[[str | Path, str | Path], Any] = ZoteroLocalAttachmentPort
    zotero_storage_source: Callable[..., Any] = ZoteroStorageSource
    zotero_storage_attachments: Callable[..., Any] = ZoteroStorageAttachmentPort
    text_extractor: Callable[[Path], Any] = PyMuPDFTextExtractor
    claude_review: Callable[..., Any] = ClaudeCodeOAuthReviewAdapter
    anthropic_review: Callable[..., Any] = AnthropicAPIReviewAdapter
    local_review: Callable[..., Any] = LocalModelReviewAdapter
    anthropic_client: Callable[[str], Any] = _anthropic_client
    sidecar: Callable[[Path], Any] = FilesystemSidecar
    page: Callable[[Path], Any] = FilesystemPage
    receipt: Callable[[Path], Any] = FilesystemReceipt
    verifier: Callable[[Path], Any] = FilesystemEvidenceVerifier
    staged_review: Callable[[Path, Any], Any] = FilesystemStagedReview
    staged_attachment: Callable[[Path, Any], Any] = FilesystemStagedAttachment


@dataclass(frozen=True, slots=True)
class OperationsComposition:
    """The assembled local operational use cases and their outer adapters."""

    setup: SetupUseCase
    inspect: InspectInstallation
    doctor: DoctorInstallation
    build: BuildWorkspace
    validate: ValidateWorkspace
    repair: RepairWorkspace


@dataclass(frozen=True, slots=True)
class OperationsDependencies:
    """Injectable concrete constructors for local operational CLI tests."""

    config_writer: Callable[[], Any] = FilesystemConfigWriter
    diagnostics_probes: Callable[..., Any] = SystemDiagnosticsProbes
    workspace_ops: Callable[[Path], Any] = FilesystemWorkspaceOps


@dataclass(frozen=True, slots=True)
class RuntimeComposition:
    """The assembled read-only query, local serve, and explicit deploy paths."""

    query: Any | None
    serve: ServeSite
    server: Any
    deploy: DeploySite | None
    validate: ValidateWorkspace | None
    workspace: Path
    site: Path
    publication_config: Path
    cloudflare_api_token: str


@dataclass(frozen=True, slots=True)
class RuntimeDependencies:
    """Injectable outer adapters for official runtime CLI commands."""

    local_retrieval: Callable[[Path, str, str, str], Any] = local_lexical_retrieval_use_case
    server: Callable[[], Any] = LocalStaticServer
    workspace_ops: Callable[[Path], Any] = FilesystemWorkspaceOps
    cloudflare_deployment: Callable[..., Any] = CloudflareDeployment


def compose_operations(
    config: AppConfig,
    *,
    environment: Mapping[str, str] | None = None,
    dependencies: OperationsDependencies | None = None,
) -> OperationsComposition:
    """Assemble only local setup, diagnostics, and workspace operations."""
    environment = dict(os.environ if environment is None else environment)
    dependencies = dependencies or OperationsDependencies()
    workspace = Path(config.workspace.root).expanduser()
    operations = dependencies.workspace_ops(workspace)
    return OperationsComposition(
        setup=SetupUseCase(dependencies.config_writer()),
        inspect=InspectInstallation(config),
        doctor=DoctorInstallation(
            config, dependencies.diagnostics_probes(config, environment=environment)
        ),
        build=BuildWorkspace(operations),
        validate=ValidateWorkspace(operations),
        repair=RepairWorkspace(operations),
    )


def compose_runtime(
    config: AppConfig,
    topic: str | None = None,
    *,
    command: str | None = None,
    environment: Mapping[str, str] | None = None,
    dependencies: RuntimeDependencies | None = None,
) -> RuntimeComposition:
    """Assemble runtime commands without the legacy planner or provider fallback."""
    require_installed_features(config)
    command = command or ("query" if topic is not None else "serve")
    if command not in {"query", "serve", "deploy"}:
        raise ValueError("runtime command is not supported")
    if command == "query" and topic is None:
        raise ValueError("query requires a configured topic")
    if topic is not None and topic not in config.source.collections:
        raise ValueError("--topic must name a configured source.collections alias")
    environment = dict(os.environ if environment is None else environment)
    dependencies = dependencies or RuntimeDependencies()
    workspace = Path(config.workspace.root).expanduser().resolve()
    site = workspace / "site"
    publication_config = workspace / config.publication.config_path
    deployment = (
        DeploySite(
            dependencies.cloudflare_deployment(
                environment.get("CLOUDFLARE_API_TOKEN", ""),
                environment=environment,
            )
        )
        if command == "deploy" and config.publication.mode == "public"
        else None
    )
    operations = dependencies.workspace_ops(workspace) if command == "deploy" else None
    return RuntimeComposition(
        query=(
            dependencies.local_retrieval(
                workspace, topic, config.source.provider, config.source.collections[topic]
            )
            if topic is not None
            else None
        ),
        serve=ServeSite(),
        server=dependencies.server() if command == "serve" else None,
        deploy=deployment,
        validate=ValidateWorkspace(operations) if operations is not None else None,
        workspace=workspace,
        site=site,
        publication_config=publication_config,
        cloudflare_api_token=environment.get("CLOUDFLARE_API_TOKEN", ""),
    )


def compose_core_update(
    config: AppConfig,
    *,
    environment: Mapping[str, str] | None = None,
    dependencies: CompositionDependencies | None = None,
) -> CoreComposition:
    """Assemble exactly the selected local Core path without fallback adapters."""
    environment = dict(os.environ if environment is None else environment)
    dependencies = dependencies or CompositionDependencies()
    selection = compose_core_selection(
        config, environment=environment, dependencies=dependencies
    )
    workspace = Path(config.workspace.root).expanduser()
    source_attachments: Any | None = None
    provider: Any | None = None
    try:
        if config.source.transport == "local-sqlite":
            sqlite_path = Path(config.source.sqlite_path).expanduser()
            source_attachments = dependencies.zotero_attachments(
                sqlite_path, sqlite_path.parent / "storage"
            )
        elif config.source.transport == "zotero-storage":
            api_key = _environment_credential(
                environment, config.credentials.zotero_api_key, "ZOTERO_API_KEY"
            )
            source_attachments = dependencies.zotero_storage_attachments(
                api_key, workspace / ".cache" / "zotero"
            )
        else:  # AppConfig validates this, retained as a closed composition boundary.
            raise ConfigValidationError(
                "source.transport", f"'{config.source.transport}' is not supported"
            )
        provider = _selected_review_provider(
            config, workspace, environment, dependencies
        )
        curate = CuratePaper(
            source=selection.source,
            attachments=dependencies.staged_attachment(
                workspace, source_attachments
            ),
            text=dependencies.text_extractor(workspace),
            reviews=dependencies.staged_review(workspace, provider),
            sidecars=dependencies.sidecar(workspace),
            pages=dependencies.page(workspace),
            receipts=dependencies.receipt(workspace),
            review_provider_id=config.core.review.provider,
            review_model_id=config.core.review.model,
            evidence_verifier=dependencies.verifier(workspace),
        )
        return CoreComposition(
            update=UpdateCore(curate),
            source=selection.source,
            review_provider_id=config.core.review.provider,
            capabilities=selection.capabilities,
            resources=(selection.source, source_attachments, provider),
        )
    except Exception:
        acquired = (
            selection.source,
            *((source_attachments,) if source_attachments is not None else ()),
            *((provider,) if provider is not None else ()),
        )
        _close_resources(acquired, raise_errors=False)
        raise


def compose_core_selection(
    config: AppConfig,
    *,
    environment: Mapping[str, str] | None = None,
    dependencies: CompositionDependencies | None = None,
) -> CoreSelectionComposition:
    """Select the exact Core source/provider without constructing a model client."""
    environment = dict(os.environ if environment is None else environment)
    dependencies = dependencies or CompositionDependencies()
    capabilities = dependencies.detect_capabilities(
        config,
        environment,
        path_exists=Path.exists,
        path_is_dir=Path.is_dir,
    )
    require_installed_features(config)
    if config.source.transport == "local-sqlite":
        source = dependencies.zotero_source(Path(config.source.sqlite_path).expanduser())
    elif config.source.transport == "zotero-storage":
        api_key = _environment_credential(
            environment, config.credentials.zotero_api_key, "ZOTERO_API_KEY"
        )
        source = dependencies.zotero_storage_source(api_key)
    else:
        raise ConfigValidationError(
            "source.transport", f"'{config.source.transport}' is not supported"
        )
    return CoreSelectionComposition(
        source,
        config.core.review.provider,
        config.core.review.model,
        capabilities,
        (source,),
    )


def _selected_review_provider(
    config: AppConfig,
    workspace: Path,
    environment: Mapping[str, str],
    dependencies: CompositionDependencies,
) -> Any:
    output_dir = workspace / ".review-provider"
    provider = config.core.review.provider
    if provider == "claude-code-oauth":
        return dependencies.claude_review(
            output_dir, model=config.core.review.model, environment=environment
        )
    if provider == "anthropic-api":
        api_key = _environment_credential(
            environment, config.credentials.anthropic_api_key, "ANTHROPIC_API_KEY"
        )
        client = dependencies.anthropic_client(api_key)
        try:
            return dependencies.anthropic_review(
                output_dir, client, model=config.core.review.model
            )
        except Exception:
            try:
                _close_resource(client)
            except Exception:
                pass
            raise
    if provider == "local-model":
        return dependencies.local_review(
            output_dir,
            config.core.review.local_endpoint,
            model=config.core.review.model,
            api_key="",
        )
    raise ConfigValidationError("core.review.provider", f"'{provider}' is not supported")
