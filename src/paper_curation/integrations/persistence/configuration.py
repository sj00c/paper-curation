"""Filesystem persistence adapter for the setup configuration use case."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from typing import Any

from paper_curation.application.setup import SetupPlan, SetupResult
from paper_curation.config.models import AppConfig


class FilesystemConfigWriter:
    """Create setup directories and atomically persist strict JSON configuration."""

    def write(self, plan: SetupPlan) -> SetupResult:
        encoded = _encode_config(plan.config)
        target_path = plan.target_path
        existing = target_path.exists()
        if existing and not plan.replace:
            raise FileExistsError(f"configuration already exists at {target_path}")

        for directory in plan.workspace_directories:
            directory.mkdir(parents=True, exist_ok=True)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        backup_path: Path | None = None
        if existing:
            backup_path = plan.backup_path
            assert backup_path is not None
            _write_backup(backup_path, target_path.read_bytes())

        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{target_path.name}.", suffix=".tmp", dir=target_path.parent
        )
        temporary_path = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb") as temporary:
                temporary.write(encoded)
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary_path, target_path)
        finally:
            temporary_path.unlink(missing_ok=True)

        return SetupResult(target_path, plan.workspace_directories, backup_path)


def _write_backup(path: Path, contents: bytes) -> None:
    """Create one exact private backup without ever replacing an existing backup."""

    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as backup:
            backup.write(contents)
            backup.flush()
            os.fsync(backup.fileno())
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


def _encode_config(config: AppConfig) -> bytes:
    """Return the complete strict schema without exposing any values in errors."""

    data: dict[str, Any] = {
        "workspace": {"root": config.workspace.root},
        "source": {
            "provider": config.source.provider,
            "transport": config.source.transport,
            "collections": dict(config.source.collections),
            "sqlite_path": config.source.sqlite_path,
        },
        "core": {"review": {
            "provider": config.core.review.provider,
            "model": config.core.review.model,
            "local_endpoint": config.core.review.local_endpoint,
        }},
        "features": {
            name: {"enabled": feature.enabled, "provider": feature.provider}
            for name, feature in config.features.items()
        },
        "credentials": {
            "zotero_api_key": config.credentials.zotero_api_key,
            "anthropic_api_key": config.credentials.anthropic_api_key,
            "google_api_key": config.credentials.google_api_key,
            "gemini_api_key": config.credentials.gemini_api_key,
            "openai_api_key": config.credentials.openai_api_key,
        },
        "search_keywords": {
            alias: {"primary": list(keywords.primary), "secondary": list(keywords.secondary)}
            for alias, keywords in config.search_keywords.items()
        },
        "topic_profiles": {
            alias: {"title": profile.title, **dict(profile.extra)}
            for alias, profile in config.topic_profiles.items()
        },
        "publication": _publication_data(config),
        "operator": {
            "name": config.operator.name,
            "organization": config.operator.organization,
            "email": config.operator.email,
        },
        "notifications": {"completion_email": config.notifications.completion_email},
    }
    try:
        return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ValueError("configuration cannot be encoded as strict JSON") from error


def _publication_data(config: AppConfig) -> dict[str, str]:
    """Encode deployment selection only for explicitly public publication."""

    publication = {
        "mode": config.publication.mode,
        "base_url": config.publication.base_url,
    }
    if config.publication.mode == "public":
        publication.update(
            provider=config.publication.provider,
            config_path=config.publication.config_path,
        )
    return publication
