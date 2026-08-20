"""Resolve selected providers without inferring selections from credentials."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from .config.models import AppConfig
from .errors import ConfigValidationError

PathPredicate = Callable[[Path], bool]


@dataclass(frozen=True, slots=True)
class Capabilities:
    """Readiness of explicitly selected source, Core provider, and features."""

    source_ready: bool
    core_review_ready: bool
    features: Mapping[str, bool]
    public_deploy: bool


def _present(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _credential(config_value: str, environment: Mapping[str, str], *names: str) -> bool:
    return _present(next((environment[name] for name in names if _present(environment.get(name))), config_value))


def _provider_ready(
    provider: str,
    config: AppConfig,
    environment: Mapping[str, str],
    *,
    path_exists: PathPredicate,
    path_is_dir: PathPredicate,
    claude_credentials_path: str | Path,
) -> bool:
    if provider == "claude-code-oauth":
        return _present(environment.get("CLAUDE_CODE_OAUTH_TOKEN")) or path_exists(Path(claude_credentials_path))
    if provider == "anthropic-api":
        return _credential(config.credentials.anthropic_api_key, environment, "ANTHROPIC_API_KEY")
    if provider in {"google", "gemini"}:
        return _credential(
            config.credentials.google_api_key or config.credentials.gemini_api_key,
            environment,
            "GOOGLE_API_KEY",
            "GEMINI_API_KEY",
        )
    if provider == "openai":
        return _credential(config.credentials.openai_api_key, environment, "OPENAI_API_KEY")
    if provider == "local-model":
        return bool(config.core.review.local_endpoint)
    if provider == "paperbanana":
        directory = environment.get("PAPERBANANA_DIR", "")
        return _present(directory) and path_is_dir(Path(directory))
    raise ConfigValidationError("provider", f"'{provider}' is not supported")


def _provider_requirement(provider: str) -> str:
    requirements = {
        "claude-code-oauth": "CLAUDE_CODE_OAUTH_TOKEN or Claude credentials file",
        "anthropic-api": "credentials.anthropic_api_key or ANTHROPIC_API_KEY",
        "google": "credentials.google_api_key, credentials.gemini_api_key, GOOGLE_API_KEY, or GEMINI_API_KEY",
        "gemini": "credentials.google_api_key, credentials.gemini_api_key, GOOGLE_API_KEY, or GEMINI_API_KEY",
        "openai": "credentials.openai_api_key or OPENAI_API_KEY",
        "local-model": "core.review.local_endpoint",
        "paperbanana": "PAPERBANANA_DIR pointing to a directory",
    }
    return requirements[provider]


def detect_capabilities(
    config: AppConfig,
    environment: Mapping[str, str],
    *,
    path_exists: PathPredicate,
    path_is_dir: PathPredicate,
    claude_credentials_path: str | Path = Path.home() / ".claude" / ".credentials.json",
) -> Capabilities:
    """Validate selected providers and return no facts for unselected providers."""
    if config.source.transport == "local-sqlite":
        source_ready = path_exists(Path(config.source.sqlite_path))
        if not source_ready:
            raise ConfigValidationError("source.sqlite_path", "does not exist for local-sqlite transport")
    else:
        source_ready = _credential(config.credentials.zotero_api_key, environment, "ZOTERO_API_KEY")
        if not source_ready:
            raise ConfigValidationError("credentials.zotero_api_key", "is required for zotero-storage transport")

    core_review_ready = _provider_ready(
        config.core.review.provider,
        config,
        environment,
        path_exists=path_exists,
        path_is_dir=path_is_dir,
        claude_credentials_path=claude_credentials_path,
    )
    if not core_review_ready:
        raise ConfigValidationError(
            "core.review.provider",
            f"selected provider '{config.core.review.provider}' requires {_provider_requirement(config.core.review.provider)}",
        )

    features: dict[str, bool] = {}
    for name, feature in config.features.items():
        if not feature.enabled:
            features[name] = False
            continue
        ready = _provider_ready(
            feature.provider,
            config,
            environment,
            path_exists=path_exists,
            path_is_dir=path_is_dir,
            claude_credentials_path=claude_credentials_path,
        )
        if not ready:
            raise ConfigValidationError(
                f"features.{name}.provider",
                f"selected provider '{feature.provider}' requires {_provider_requirement(feature.provider)}",
            )
        features[name] = True
    return Capabilities(
        source_ready=source_ready,
        core_review_ready=core_review_ready,
        features=MappingProxyType(features),
        public_deploy=config.publication.mode == "public",
    )
