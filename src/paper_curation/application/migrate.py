"""Safe, local migration of legacy ``config.json`` files."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile
import stat
from typing import Any, Mapping

from paper_curation.config.models import AppConfig
from paper_curation.errors import ConfigFileError


@dataclass(frozen=True, slots=True)
class ConfigMigrationPlan:
    """The complete in-memory result of a configuration migration."""

    config: Mapping[str, Any]
    changed_paths: tuple[str, ...]

    @property
    def has_changes(self) -> bool:
        return bool(self.changed_paths)


def _object(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise ValueError(f"{path} must be an object with string keys")
    return value


def _collections(config: Mapping[str, Any]) -> Mapping[str, str]:
    zotero = _object(config.get("zotero"), "zotero")
    collections = _object(zotero.get("collections"), "zotero.collections")
    if not collections:
        raise ValueError("zotero.collections must configure at least one topic")
    result: dict[str, str] = {}
    for alias, display_name in collections.items():
        if not isinstance(alias, str) or not alias.strip():
            raise ValueError("zotero.collections aliases must be non-empty strings")
        if not isinstance(display_name, str) or not display_name.strip():
            raise ValueError(f"zotero.collections.{alias} must be a non-empty string")
        result[alias] = display_name
    return result


def plan_config_migration(mapping: Mapping[str, Any]) -> ConfigMigrationPlan:
    """Return a deterministic, validated migration without modifying ``mapping``."""

    source = _object(mapping, "$")
    collections = _collections(source)
    migrated = deepcopy(dict(source))
    changes: list[str] = []

    if "search_keywords" not in migrated:
        keywords = {}
        migrated["search_keywords"] = keywords
    else:
        keywords = migrated["search_keywords"]
        _object(keywords, "search_keywords")
    if "topic_profiles" not in migrated:
        profiles = {}
        migrated["topic_profiles"] = profiles
    else:
        profiles = migrated["topic_profiles"]
        _object(profiles, "topic_profiles")

    for alias, display_name in collections.items():
        if alias not in keywords:
            keywords[alias] = {"primary": [display_name], "secondary": []}
            changes.append(f"search_keywords.{alias}")
        if alias not in profiles:
            profiles[alias] = {"title": display_name}
            changes.append(f"topic_profiles.{alias}.title")
            continue
        profile = _object(profiles[alias], f"topic_profiles.{alias}")
        if "title" not in profile:
            profile["title"] = display_name
            changes.append(f"topic_profiles.{alias}.title")

    if "publication" not in migrated:
        publication = {}
        migrated["publication"] = publication
    else:
        publication = migrated["publication"]
        _object(publication, "publication")
    if "mode" not in publication:
        publication["mode"] = "local"
        changes.append("publication.mode")
    if "base_url" not in publication:
        publication["base_url"] = ""
        changes.append("publication.base_url")

    # This checks all existing values too: execute must never replace a file with
    # a configuration the application cannot load.
    AppConfig.from_mapping(migrated)
    return ConfigMigrationPlan(migrated, tuple(changes))


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
        original_mode = stat.S_IMODE(config_path.stat().st_mode)
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
