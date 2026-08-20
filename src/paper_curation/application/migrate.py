"""Safe, local migration of legacy ``config.json`` files."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePath, PureWindowsPath
import tempfile
from typing import Any, Mapping

from paper_curation.config.models import AppConfig
from paper_curation.errors import ConfigFileError


# Migration-only alias: the exact ``WRITE_REVIEW_MODEL`` default used by the
# legacy review runtime. Product runtime always requires ``core.review.model``.
_LEGACY_REVIEW_MODEL_DEFAULT = "claude-sonnet-5"


@dataclass(frozen=True, slots=True)
class ConfigMigrationPlan:
    """The complete in-memory result of a configuration migration."""

    config: Mapping[str, Any]
    changed_paths: tuple[str, ...]
    reported_paths: tuple[str, ...] = ()

    @property
    def has_changes(self) -> bool:
        return bool(self.changed_paths)


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"{path} must be an object with string keys")
    return value


def _collections(value: Any, path: str) -> dict[str, str]:
    collections = _object(value, path)
    if not collections:
        raise ValueError(f"{path} must configure at least one topic")
    result: dict[str, str] = {}
    for alias, display_name in collections.items():
        if not isinstance(alias, str) or not alias.strip():
            raise ValueError("zotero.collections aliases must be non-empty strings")
        if not isinstance(display_name, str) or not display_name.strip():
            raise ValueError(f"{path}.{alias} must be a non-empty string")
        result[alias] = display_name
    return result


def _report(reported: list[str], path: str) -> None:
    if path not in reported:
        reported.append(path)


def _safe_publication_config_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("publication.config_path must be a non-empty string")
    location = PurePath(value)
    windows_location = PureWindowsPath(value)
    if (
        location.is_absolute()
        or windows_location.is_absolute()
        or bool(windows_location.drive)
        or value in {".", ".."}
        or ".." in location.parts
        or ".." in windows_location.parts
    ):
        raise ValueError("publication.config_path must remain a workspace-relative path")
    return value


def _publication_values(
    publication: Mapping[str, Any],
    github: Mapping[str, Any],
    reported: list[str],
) -> dict[str, str]:
    """Migrate only an explicitly selected and safe public deployment."""

    publication_url = publication.get("base_url", "")
    github_url = github.get("pages_base_url", "")
    if not isinstance(publication_url, str):
        raise ValueError("publication.base_url must be a string")
    if not isinstance(github_url, str):
        raise ValueError("github.pages_base_url must be a string")
    legacy_mode = publication.get("mode", "local")
    if not isinstance(legacy_mode, str):
        raise ValueError("publication.mode must be a string")
    base_url = publication_url or github_url
    url_path = "publication.base_url" if publication_url else "github.pages_base_url"

    targets: list[tuple[str, str]] = []
    for key in ("provider", "target"):
        if key not in publication:
            continue
        value = publication[key]
        if not isinstance(value, str):
            raise ValueError(f"publication.{key} must be a string")
        if value.strip():
            targets.append((value, f"publication.{key}"))
    config_path = publication.get("config_path", "")
    if not isinstance(config_path, str):
        raise ValueError("publication.config_path must be a string")

    selected_cloudflare = (
        bool(targets)
        and all(value == "cloudflare" for value, _ in targets)
        and bool(config_path.strip())
    )
    if selected_cloudflare:
        safe_path = _safe_publication_config_path(config_path)
        if not base_url.strip():
            raise ValueError(
                "publication.base_url is required to migrate an explicit Cloudflare publication"
            )
        return {
            "mode": "public",
            "base_url": base_url,
            "provider": "cloudflare",
            "config_path": safe_path,
        }

    # URLs document an existing location, not consent to a new deployment.
    if base_url.strip():
        _report(reported, url_path)
    if legacy_mode.lower() != "local":
        _report(reported, "publication.mode")
    for _, path in targets:
        _report(reported, path)
    if config_path.strip():
        _report(reported, "publication.config_path")
    return {
        "mode": "local",
        "base_url": base_url,
        "provider": "",
        "config_path": "",
    }


def _legacy_provider(source: Mapping[str, Any]) -> tuple[str, str]:
    candidates: list[tuple[str, str]] = []
    auth = source.get("anthropic_auth")
    if isinstance(auth, Mapping) and auth.get("mode") == "oauth":
        candidates.append(("claude-code-oauth", "anthropic_auth.mode"))
    if isinstance(source.get("anthropic_api_key"), str) and source["anthropic_api_key"].strip():
        candidates.append(("anthropic-api", "anthropic_api_key"))
    local_model = source.get("local_model")
    if isinstance(local_model, Mapping) and isinstance(local_model.get("base_url"), str) and local_model["base_url"].strip():
        candidates.append(("local-model", "local_model.base_url"))
    if not candidates:
        raise ValueError(
            "core.review.provider cannot be migrated; configure legacy anthropic_auth.mode "
            "as 'oauth', anthropic_api_key, or local_model.base_url"
        )
    if len(candidates) != 1:
        raise ValueError(
            "core.review.provider cannot be migrated because multiple legacy review providers are configured"
        )
    return candidates[0]


def _legacy_review_model(
    source: Mapping[str, Any],
    provider: str,
) -> str:
    """Select an explicit review model without introducing a runtime fallback."""

    if provider == "local-model":
        local_model = _object(source.get("local_model"), "local_model")
        model = local_model.get("model")
        if not isinstance(model, str) or not model.strip():
            raise ValueError(
                "core.review.model cannot be migrated; set local_model.model to the "
                "model used by the legacy runtime"
            )
        return model

    if "anthropic_model" not in source:
        return _LEGACY_REVIEW_MODEL_DEFAULT
    model = source["anthropic_model"]
    if not isinstance(model, str) or not model.strip():
        raise ValueError(
            "core.review.model cannot be migrated; set anthropic_model to the "
            "model used by the legacy runtime"
        )
    return model


def _topic_values(
    source: Mapping[str, Any],
    collections: Mapping[str, str],
    reported: list[str],
) -> tuple[dict[str, dict[str, list[str]]], dict[str, dict[str, str]]]:
    raw_keywords = source.get("search_keywords", {})
    raw_profiles = source.get("topic_profiles", {})
    keywords = _object(raw_keywords, "search_keywords")
    profiles = _object(raw_profiles, "topic_profiles")
    result_keywords: dict[str, dict[str, list[str]]] = {}
    result_profiles: dict[str, dict[str, str]] = {}
    for alias, title in collections.items():
        raw_keyword = keywords.get(alias)
        if raw_keyword is None:
            result_keywords[alias] = {"primary": [title], "secondary": []}
        else:
            entry = _object(raw_keyword, f"search_keywords.{alias}")
            primary = entry.get("primary")
            secondary = entry.get("secondary", [])
            if not isinstance(primary, list) or not all(isinstance(item, str) and item.strip() for item in primary):
                raise ValueError(f"search_keywords.{alias}.primary must be an array of non-empty strings")
            if not isinstance(secondary, list) or not all(isinstance(item, str) and item.strip() for item in secondary):
                raise ValueError(f"search_keywords.{alias}.secondary must be an array of non-empty strings")
            result_keywords[alias] = {"primary": primary, "secondary": secondary}
            for key in entry:
                if key not in {"primary", "secondary"}:
                    _report(reported, f"search_keywords.{alias}.{key}")
        raw_profile = profiles.get(alias)
        if raw_profile is None:
            result_profiles[alias] = {"title": title}
        else:
            entry = _object(raw_profile, f"topic_profiles.{alias}")
            profile_title = entry.get("title", title)
            if not isinstance(profile_title, str) or not profile_title.strip():
                raise ValueError(f"topic_profiles.{alias}.title must be a non-empty string")
            result_profiles[alias] = {"title": profile_title}
            for key in entry:
                if key != "title":
                    _report(reported, f"topic_profiles.{alias}.{key}")
    for alias in keywords:
        if alias not in collections:
            _report(reported, f"search_keywords.{alias}")
    for alias in profiles:
        if alias not in collections:
            _report(reported, f"topic_profiles.{alias}")
    return result_keywords, result_profiles


def _canonical_strict_config(source: Mapping[str, Any]) -> bool:
    """Return whether ``source`` is already the exact emitted migration schema."""

    try:
        AppConfig.from_mapping(source)
    except (TypeError, ValueError):
        return False
    required = {
        "workspace", "source", "core", "features", "credentials",
        "search_keywords", "topic_profiles", "publication", "operator", "notifications",
    }
    if set(source) != required:
        return False
    features = source.get("features")
    if not isinstance(features, Mapping) or set(features) != {
        "figure_validation", "citation_metrics", "dense_search",
    }:
        return False
    profiles = source.get("topic_profiles")
    return isinstance(profiles, Mapping) and all(
        isinstance(profile, Mapping) and set(profile) == {"title"}
        for profile in profiles.values()
    )


def plan_config_migration(mapping: Mapping[str, Any]) -> ConfigMigrationPlan:
    """Return a deterministic, validated migration without modifying ``mapping``."""

    source = _object(mapping, "$")
    if _canonical_strict_config(source):
        return ConfigMigrationPlan(dict(source), ())

    zotero = _object(source.get("zotero"), "zotero")
    collections = _collections(zotero.get("collections"), "zotero.collections")
    reported: list[str] = []
    provider, provider_path = _legacy_provider(source)
    model = _legacy_review_model(source, provider)
    sqlite_path = zotero.get("sqlite_path", "")
    if not isinstance(sqlite_path, str):
        raise ValueError("zotero.sqlite_path must be a string")
    if sqlite_path and not sqlite_path.strip():
        raise ValueError("zotero.sqlite_path must be a non-empty string")
    transport = "local-sqlite" if sqlite_path else "zotero-storage"
    credentials = {
        "zotero_api_key": zotero.get("api_key", source.get("zotero_api_key", "")),
        "anthropic_api_key": source.get("anthropic_api_key", ""),
        "google_api_key": source.get("google_api_key", ""),
        "gemini_api_key": source.get("gemini_api_key", ""),
        "openai_api_key": source.get("openai_api_key", ""),
    }
    for name, value in credentials.items():
        if not isinstance(value, str):
            raise ValueError(f"credentials.{name} must be a string")
    keywords, profiles = _topic_values(source, collections, reported)
    legacy_publication = _object(source.get("publication", {}), "publication")
    github = _object(source.get("github", {}), "github")
    publication = _publication_values(legacy_publication, github, reported)
    operator = _object(source.get("operator", {}), "operator")
    notifications = _object(source.get("notifications", {}), "notifications")
    for block, allowed in (
        ("zotero", {"collections", "sqlite_path", "api_key"}),
        ("publication", {"mode", "base_url", "provider", "target", "config_path"}),
        ("github", {"pages_base_url"}),
        ("operator", {"name", "organization", "email"}),
        ("notifications", {"completion_email"}),
        ("anthropic_auth", {"mode"}),
        ("local_model", {"base_url", "model"}),
    ):
        value = source.get(block, {})
        if isinstance(value, Mapping):
            for key in value:
                if key not in allowed:
                    _report(reported, f"{block}.{key}")
    known_top_level = {
        "zotero", "zotero_api_key", "anthropic_api_key", "google_api_key",
        "gemini_api_key", "openai_api_key", "anthropic_auth", "anthropic_model", "local_model",
        "search_keywords", "topic_profiles", "publication", "github", "operator",
        "notifications",
    }
    for key in source:
        if key not in known_top_level:
            _report(reported, key)
    migrated = {
        "workspace": {"root": "~/.local/share/paper-curation/default"},
        "source": {
            "provider": "zotero",
            "transport": transport,
            "collections": collections,
            "sqlite_path": sqlite_path if transport == "local-sqlite" else "",
        },
        "core": {"review": {
            "provider": provider,
            "model": model,
            "local_endpoint": source["local_model"]["base_url"] if provider_path == "local_model.base_url" else "",
        }},
        "features": {
            name: {"enabled": False, "provider": ""}
            for name in ("figure_validation", "citation_metrics", "dense_search")
        },
        "credentials": credentials,
        "search_keywords": keywords,
        "topic_profiles": profiles,
        "publication": publication,
        "operator": {name: operator.get(name, "") for name in ("name", "organization", "email")},
        "notifications": {"completion_email": notifications.get("completion_email", "")},
    }
    for block, values in (("operator", migrated["operator"]), ("notifications", migrated["notifications"])):
        for key, value in values.items():
            if not isinstance(value, str):
                raise ValueError(f"{block}.{key} must be a string")

    # This checks every generated value: execution must never replace a file
    # with a configuration the application cannot load.
    AppConfig.from_mapping(migrated)
    changes = [
        "workspace.root", "source.provider", "source.transport", "source.collections",
        "source.sqlite_path", "core.review.provider", "core.review.model", "core.review.local_endpoint",
        "features", "credentials", "search_keywords", "topic_profiles", "publication",
        "operator", "notifications",
    ]
    return ConfigMigrationPlan(migrated, tuple(changes + reported), tuple(reported))


def load_config_migration(path: str | Path) -> ConfigMigrationPlan:
    """Read and plan migration for a local JSON config without exposing its values."""

    config_path = Path(path)
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigFileError(str(config_path), "file does not exist") from error
    except OSError as error:
        raise ConfigFileError(str(config_path), "file cannot be read") from error
    except json.JSONDecodeError as error:
        raise ConfigFileError(str(config_path), "invalid JSON") from error
    return plan_config_migration(data)


def execute_config_migration(path: str | Path, plan: ConfigMigrationPlan) -> Path:
    """Back up ``path`` exactly and atomically replace it with the validated plan."""

    config_path = Path(path)
    backup_path = config_path.with_name(f"{config_path.name}.pre-migration.bak")
    try:
        original = config_path.read_bytes()
    except FileNotFoundError as error:
        raise ConfigFileError(str(config_path), "file does not exist") from error
    except OSError as error:
        raise ConfigFileError(str(config_path), "file cannot be read") from error

    # Defend against a caller supplying a plan not produced by this module.
    AppConfig.from_mapping(plan.config)
    encoded = (json.dumps(plan.config, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if plan.has_changes:
        try:
            backup_fd = os.open(
                backup_path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            with os.fdopen(backup_fd, "wb") as backup:
                backup.write(original)
                backup.flush()
                os.fsync(backup.fileno())
        except FileExistsError:
            raise ConfigFileError(str(backup_path), "backup already exists; refusing to overwrite")
        except OSError as error:
            raise ConfigFileError(str(backup_path), "backup cannot be created") from error
    else:
        return backup_path

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{config_path.name}.", suffix=".tmp", dir=config_path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as temporary:
            temporary.write(encoded)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, config_path)
    except OSError as error:
        raise ConfigFileError(str(config_path), "atomic replacement failed") from error
    finally:
        temporary_path.unlink(missing_ok=True)
    return backup_path
