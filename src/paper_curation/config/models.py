"""Typed, dependency-free representation of installation configuration."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from pathlib import PurePath, PureWindowsPath
from types import MappingProxyType
from typing import Any, Mapping
from urllib.parse import urlparse

from paper_curation.errors import ConfigTypeError, ConfigValidationError


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigTypeError(path, "must be an object")
    if not all(isinstance(key, str) for key in value):
        raise ConfigTypeError(path, "keys must be strings")
    return value


def _text(value: Any, path: str, *, required: bool = False) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise ConfigTypeError(path, "must be a string")
    value = value.strip()
    if required and not value:
        raise ConfigValidationError(path, "must not be empty")
    return value


def _string_list(value: Any, path: str, *, required: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ConfigTypeError(path, "must be an array of strings")
    items = tuple(_text(item, f"{path}[{index}]", required=True) for index, item in enumerate(value))
    if required and not items:
        raise ConfigValidationError(path, "must contain at least one keyword")
    return items


def _only_keys(value: Mapping[str, Any], path: str, allowed: set[str]) -> None:
    unknown = set(value) - allowed
    if unknown:
        raise ConfigValidationError(path, "contains unsupported keys")


@dataclass(frozen=True, slots=True)
class WorkspaceConfig:
    root: str


@dataclass(frozen=True, slots=True)
class SourceConfig:
    provider: str
    transport: str
    collections: Mapping[str, str]
    sqlite_path: str = ""


@dataclass(frozen=True, slots=True)
class ReviewConfig:
    provider: str
    model: str
    local_endpoint: str = ""


@dataclass(frozen=True, slots=True)
class CoreConfig:
    review: ReviewConfig


@dataclass(frozen=True, slots=True)
class FeatureConfig:
    enabled: bool
    provider: str = ""


@dataclass(frozen=True, slots=True)
class CredentialsConfig:
    zotero_api_key: str = field(default="", repr=False)
    anthropic_api_key: str = field(default="", repr=False)
    google_api_key: str = field(default="", repr=False)
    gemini_api_key: str = field(default="", repr=False)
    openai_api_key: str = field(default="", repr=False)


@dataclass(frozen=True, slots=True)
class TopicKeywords:
    primary: tuple[str, ...]
    secondary: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TopicProfile:
    title: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class PublicationConfig:
    mode: str = "local"
    base_url: str = ""
    provider: str = ""
    config_path: str = ""


@dataclass(frozen=True, slots=True)
class OperatorConfig:
    name: str = ""
    organization: str = ""
    email: str = ""


@dataclass(frozen=True, slots=True)
class NotificationConfig:
    completion_email: str = ""


@dataclass(frozen=True, slots=True)
class AppConfig:
    workspace: WorkspaceConfig
    source: SourceConfig
    core: CoreConfig
    features: Mapping[str, FeatureConfig]
    search_keywords: Mapping[str, TopicKeywords]
    topic_profiles: Mapping[str, TopicProfile]
    credentials: CredentialsConfig = field(default_factory=CredentialsConfig, repr=False)
    publication: PublicationConfig = field(default_factory=PublicationConfig)
    operator: OperatorConfig = field(default_factory=OperatorConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AppConfig":
        data = _mapping(data, "$")
        _only_keys(
            data,
            "$",
            {
                "workspace", "source", "core", "features", "credentials",
                "search_keywords", "topic_profiles", "publication", "operator", "notifications",
            },
        )
        workspace_data = _mapping(data.get("workspace"), "workspace")
        _only_keys(workspace_data, "workspace", {"root"})
        workspace = WorkspaceConfig(root=_text(workspace_data.get("root"), "workspace.root", required=True))

        source_data = _mapping(data.get("source"), "source")
        _only_keys(source_data, "source", {"provider", "transport", "collections", "sqlite_path"})
        provider = _text(source_data.get("provider"), "source.provider", required=True)
        if provider != "zotero":
            raise ConfigValidationError("source.provider", "must be 'zotero'")
        transport = _text(source_data.get("transport"), "source.transport", required=True)
        if transport not in {"local-sqlite", "zotero-storage"}:
            raise ConfigValidationError("source.transport", "must be 'local-sqlite' or 'zotero-storage'")
        collections_data = _mapping(source_data.get("collections"), "source.collections")
        collections = {
            _text(alias, "source.collections key", required=True): _text(
                collection, f"source.collections.{alias}", required=True
            )
            for alias, collection in collections_data.items()
        }
        if not collections:
            raise ConfigValidationError("source.collections", "must configure at least one topic")
        for alias in collections:
            alias_path = PurePath(alias)
            if alias in {".", ".."} or alias_path.is_absolute() or len(alias_path.parts) != 1:
                raise ConfigValidationError(
                    f"source.collections.{alias}", "topic aliases must be single directory names"
                )
        sqlite_path = _text(source_data.get("sqlite_path", ""), "source.sqlite_path")
        if transport == "local-sqlite" and not sqlite_path:
            raise ConfigValidationError("source.sqlite_path", "is required for local-sqlite transport")
        if transport == "zotero-storage" and sqlite_path:
            raise ConfigValidationError("source.sqlite_path", "must be empty for zotero-storage transport")
        source = SourceConfig(provider, transport, MappingProxyType(collections), sqlite_path)

        core_data = _mapping(data.get("core"), "core")
        _only_keys(core_data, "core", {"review"})
        review_data = _mapping(core_data.get("review"), "core.review")
        _only_keys(review_data, "core.review", {"provider", "model", "local_endpoint"})
        review_provider = _text(review_data.get("provider"), "core.review.provider", required=True)
        if review_provider not in {"claude-code-oauth", "anthropic-api", "local-model"}:
            raise ConfigValidationError(
                "core.review.provider",
                "must be 'claude-code-oauth', 'anthropic-api', or 'local-model'",
            )
        review_model = _text(review_data.get("model"), "core.review.model", required=True)
        local_endpoint = _text(review_data.get("local_endpoint", ""), "core.review.local_endpoint")
        if review_provider == "local-model" and not local_endpoint:
            raise ConfigValidationError("core.review.local_endpoint", "is required for local-model")
        if review_provider == "local-model":
            endpoint = urlparse(local_endpoint)
            host = endpoint.hostname or ""
            try:
                loopback = ipaddress.ip_address(host).is_loopback
            except ValueError:
                loopback = host.casefold() == "localhost"
            if (
                endpoint.scheme not in {"http", "https"}
                or not loopback
                or endpoint.username is not None
                or endpoint.password is not None
                or bool(endpoint.params)
                or bool(endpoint.query)
                or bool(endpoint.fragment)
            ):
                raise ConfigValidationError(
                    "core.review.local_endpoint",
                    "must be an HTTP(S) loopback endpoint without credentials",
                )
        if review_provider != "local-model" and local_endpoint:
            raise ConfigValidationError("core.review.local_endpoint", "must be empty unless local-model is selected")
        core = CoreConfig(ReviewConfig(review_provider, review_model, local_endpoint))

        features_data = _mapping(data.get("features", {}), "features")
        features: dict[str, FeatureConfig] = {}
        for name, raw_feature in features_data.items():
            name = _text(name, "features key", required=True)
            feature = _mapping(raw_feature, f"features.{name}")
            _only_keys(feature, f"features.{name}", {"enabled", "provider"})
            enabled = feature.get("enabled")
            if not isinstance(enabled, bool):
                raise ConfigTypeError(f"features.{name}.enabled", "must be a boolean")
            selected_provider = _text(feature.get("provider", ""), f"features.{name}.provider")
            if enabled and not selected_provider:
                raise ConfigValidationError(f"features.{name}.provider", "is required when enabled")
            if not enabled and selected_provider:
                raise ConfigValidationError(f"features.{name}.provider", "must be empty when disabled")
            features[name] = FeatureConfig(enabled, selected_provider)

        credentials_data = _mapping(data.get("credentials", {}), "credentials")
        credential_fields = (
            "zotero_api_key",
            "anthropic_api_key",
            "google_api_key",
            "gemini_api_key",
            "openai_api_key",
        )
        _only_keys(credentials_data, "credentials", set(credential_fields))
        credentials = CredentialsConfig(**{
            field: _text(credentials_data.get(field, ""), f"credentials.{field}")
            for field in credential_fields
        })

        keyword_data = _mapping(data.get("search_keywords", {}), "search_keywords")
        profile_data = _mapping(data.get("topic_profiles", {}), "topic_profiles")
        aliases = set(collections)
        if set(keyword_data) - aliases:
            raise ConfigValidationError("search_keywords", "contains aliases that are not configured source collections")
        if set(profile_data) - aliases:
            raise ConfigValidationError("topic_profiles", "contains aliases that are not configured source collections")
        keywords: dict[str, TopicKeywords] = {}
        profiles: dict[str, TopicProfile] = {}
        for alias in collections:
            if alias in keyword_data:
                entry = _mapping(keyword_data[alias], f"search_keywords.{alias}")
                _only_keys(entry, f"search_keywords.{alias}", {"primary", "secondary"})
                keywords[alias] = TopicKeywords(
                    primary=_string_list(entry.get("primary"), f"search_keywords.{alias}.primary", required=True),
                    secondary=_string_list(entry.get("secondary", []), f"search_keywords.{alias}.secondary"),
                )
            if alias in profile_data:
                profile = _mapping(profile_data[alias], f"topic_profiles.{alias}")
                profiles[alias] = TopicProfile(
                    title=_text(profile.get("title", ""), f"topic_profiles.{alias}.title"),
                    extra=MappingProxyType({key: value for key, value in profile.items() if key != "title"}),
                )

        publication_data = _mapping(data.get("publication", {}), "publication")
        _only_keys(publication_data, "publication", {"mode", "base_url", "provider", "config_path"})
        mode = _text(publication_data.get("mode", "local"), "publication.mode", required=True).lower()
        if mode not in {"local", "public"}:
            raise ConfigValidationError("publication.mode", "must be 'local' or 'public'")
        base_url = _text(publication_data.get("base_url", ""), "publication.base_url")
        parsed = urlparse(base_url) if base_url else None
        if base_url and (parsed.scheme not in {"http", "https"} or not parsed.netloc):
            raise ConfigValidationError("publication.base_url", "must be an absolute HTTP(S) URL")
        provider = _text(publication_data.get("provider", ""), "publication.provider")
        config_path = _text(publication_data.get("config_path", ""), "publication.config_path")
        if mode == "public" and not base_url:
            raise ConfigValidationError("publication.base_url", "is required for public publication")
        if mode == "public" and provider != "cloudflare":
            raise ConfigValidationError("publication.provider", "must be 'cloudflare' for public publication")
        if mode == "public" and not config_path:
            raise ConfigValidationError("publication.config_path", "is required for public publication")
        if mode == "local" and provider:
            raise ConfigValidationError("publication.provider", "must be empty for local publication")
        if mode == "local" and config_path:
            raise ConfigValidationError("publication.config_path", "must be empty for local publication")
        if config_path:
            config_location = PurePath(config_path)
            windows_config_location = PureWindowsPath(config_path)
            if (
                config_location.is_absolute()
                or windows_config_location.is_absolute()
                or bool(windows_config_location.drive)
                or config_path in {".", ".."}
                or ".." in config_location.parts
                or ".." in windows_config_location.parts
            ):
                raise ConfigValidationError(
                    "publication.config_path", "must remain a workspace-relative path"
                )

        def optional_block(name: str, fields: tuple[str, ...]) -> dict[str, str]:
            block = _mapping(data.get(name, {}), name)
            _only_keys(block, name, set(fields))
            return {field: _text(block.get(field, ""), f"{name}.{field}") for field in fields}

        operator_values = optional_block("operator", ("name", "organization", "email"))
        notification_values = optional_block("notifications", ("completion_email",))
        return cls(
            workspace=workspace,
            source=source,
            core=core,
            features=MappingProxyType(features),
            search_keywords=MappingProxyType(keywords),
            topic_profiles=MappingProxyType(profiles),
            credentials=credentials,
            publication=PublicationConfig(mode, base_url, provider, config_path),
            operator=OperatorConfig(**operator_values),
            notifications=NotificationConfig(**notification_values),
        )
