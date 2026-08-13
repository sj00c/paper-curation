"""Typed, dependency-free representation of local configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePath
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


@dataclass(frozen=True, slots=True)
class ZoteroConfig:
    collections: Mapping[str, str]
    api_key: str = field(default="", repr=False)
    email: str = ""
    pdf_dir: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class TopicKeywords:
    primary: tuple[str, ...]
    secondary: tuple[str, ...]
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class TopicProfile:
    title: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class PublicationConfig:
    mode: str = "local"
    base_url: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class OperatorConfig:
    name: str = ""
    organization: str = ""
    email: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class NotificationConfig:
    completion_email: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)


@dataclass(frozen=True, slots=True)
class AppConfig:
    zotero: ZoteroConfig
    search_keywords: Mapping[str, TopicKeywords]
    topic_profiles: Mapping[str, TopicProfile]
    publication: PublicationConfig = field(default_factory=PublicationConfig)
    operator: OperatorConfig = field(default_factory=OperatorConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)
    anthropic_api_key: str = field(default="", repr=False)
    google_api_key: str = field(default="", repr=False)
    gemini_api_key: str = field(default="", repr=False)
    openai_api_key: str = field(default="", repr=False)
    paperbanana_dir: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AppConfig":
        data = _mapping(data, "$")
        zotero_data = _mapping(data.get("zotero"), "zotero")
        collections_data = _mapping(zotero_data.get("collections"), "zotero.collections")
        collections = {
            _text(alias, "zotero.collections key", required=True): _text(
                collection, f"zotero.collections.{alias}", required=True
            )
            for alias, collection in collections_data.items()
        }
        if not collections:
            raise ConfigValidationError("zotero.collections", "must configure at least one topic")
        for alias in collections:
            alias_path = PurePath(alias)
            if alias in {".", ".."} or alias_path.is_absolute() or len(alias_path.parts) != 1:
                raise ConfigValidationError(
                    f"zotero.collections.{alias}", "topic aliases must be single directory names"
                )
        zotero = ZoteroConfig(
            collections=MappingProxyType(collections),
            api_key=_text(zotero_data.get("api_key", ""), "zotero.api_key"),
            email=_text(zotero_data.get("email", ""), "zotero.email"),
            pdf_dir=_text(zotero_data.get("pdf_dir", ""), "zotero.pdf_dir"),
            extra=MappingProxyType({key: value for key, value in zotero_data.items() if key not in {"collections", "api_key", "email", "pdf_dir"}}),
        )

        keyword_data = _mapping(data.get("search_keywords", {}), "search_keywords")
        profile_data = _mapping(data.get("topic_profiles", {}), "topic_profiles")
        aliases = set(collections)
        unknown_keywords = set(keyword_data) - aliases
        unknown_profiles = set(profile_data) - aliases
        if unknown_keywords:
            raise ConfigValidationError(
                "search_keywords",
                "contains aliases that are not configured Zotero collections",
            )
        if unknown_profiles:
            raise ConfigValidationError(
                "topic_profiles",
                "contains aliases that are not configured Zotero collections",
            )
        keywords: dict[str, TopicKeywords] = {}
        profiles: dict[str, TopicProfile] = {}
        for alias in collections:
            if alias in keyword_data:
                entry = _mapping(keyword_data[alias], f"search_keywords.{alias}")
                keywords[alias] = TopicKeywords(
                    primary=_string_list(entry.get("primary"), f"search_keywords.{alias}.primary", required=True),
                    secondary=_string_list(entry.get("secondary", []), f"search_keywords.{alias}.secondary"),
                    extra=MappingProxyType({key: value for key, value in entry.items() if key not in {"primary", "secondary"}}),
                )
            if alias in profile_data:
                profile = _mapping(profile_data[alias], f"topic_profiles.{alias}")
                profiles[alias] = TopicProfile(
                    title=_text(profile.get("title", ""), f"topic_profiles.{alias}.title"),
                    extra=MappingProxyType({key: value for key, value in profile.items() if key != "title"}),
                )

        publication_data = _mapping(data.get("publication", {}), "publication")
        mode = _text(publication_data.get("mode", "local"), "publication.mode", required=True).lower()
        if mode not in {"local", "public"}:
            raise ConfigValidationError("publication.mode", "must be 'local' or 'public'")
        base_url = _text(publication_data.get("base_url", ""), "publication.base_url")
        parsed = urlparse(base_url) if base_url else None
        if base_url and (parsed.scheme not in {"http", "https"} or not parsed.netloc):
            raise ConfigValidationError("publication.base_url", "must be an absolute HTTP(S) URL")
        if mode == "public" and not base_url:
            raise ConfigValidationError("publication.base_url", "is required for public publication")
        publication = PublicationConfig(mode, base_url, MappingProxyType({key: value for key, value in publication_data.items() if key not in {"mode", "base_url"}}))

        def optional_block(name: str, fields: tuple[str, ...]) -> tuple[dict[str, str], Mapping[str, Any]]:
            block = _mapping(data.get(name, {}), name)
            return ({field: _text(block.get(field, ""), f"{name}.{field}") for field in fields}, MappingProxyType({key: value for key, value in block.items() if key not in fields}))

        operator_values, operator_extra = optional_block("operator", ("name", "organization", "email"))
        notification_values, notification_extra = optional_block("notifications", ("completion_email",))
        known = {"zotero", "search_keywords", "topic_profiles", "publication", "operator", "notifications", "anthropic_api_key", "google_api_key", "gemini_api_key", "openai_api_key", "paperbanana_dir"}
        return cls(
            zotero=zotero,
            search_keywords=MappingProxyType(keywords),
            topic_profiles=MappingProxyType(profiles),
            publication=publication,
            operator=OperatorConfig(**operator_values, extra=operator_extra),
            notifications=NotificationConfig(**notification_values, extra=notification_extra),
            anthropic_api_key=_text(data.get("anthropic_api_key", ""), "anthropic_api_key"),
            google_api_key=_text(data.get("google_api_key", ""), "google_api_key"),
            gemini_api_key=_text(data.get("gemini_api_key", ""), "gemini_api_key"),
            openai_api_key=_text(data.get("openai_api_key", ""), "openai_api_key"),
            paperbanana_dir=_text(data.get("paperbanana_dir", ""), "paperbanana_dir"),
            extra=MappingProxyType({key: value for key, value in data.items() if key not in known}),
        )
