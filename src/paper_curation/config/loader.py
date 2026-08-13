"""Explicit configuration loading; importing this module performs no I/O."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from paper_curation.errors import ConfigFileError

from .models import AppConfig


def load_config(path: str | Path) -> AppConfig:
    """Load and validate a JSON configuration file at an explicit path."""
    config_path = Path(path)
    try:
        with config_path.open(encoding="utf-8") as config_file:
            data: Mapping[str, object] = json.load(config_file)
    except FileNotFoundError as error:
        raise ConfigFileError(str(config_path), "file does not exist") from error
    except OSError as error:
        raise ConfigFileError(str(config_path), "file cannot be read") from error
    except json.JSONDecodeError as error:
        raise ConfigFileError(str(config_path), "invalid JSON") from error
    return AppConfig.from_mapping(data)
