"""Pure capability facts derived from explicitly supplied inputs."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from .config.models import AppConfig

PathPredicate = Callable[[Path], bool]


@dataclass(frozen=True, slots=True)
class Capabilities:
    """Available integrations, without selecting providers or causing side effects."""

    claude_auth: bool
    zotero: bool
    google_embeddings: bool
    google_audio: bool
    openai: bool
    paperbanana: bool
    public_deploy: bool


def _present(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def detect_capabilities(
    config: AppConfig,
    environment: Mapping[str, str],
    *,
    path_exists: PathPredicate,
    path_is_dir: PathPredicate,
    claude_credentials_path: str | Path = Path(".claude") / ".credentials.json",
) -> Capabilities:
    """Derive integration availability without reading environment or filesystem itself.

    Callers provide an environment snapshot and filesystem predicates so this function is
    deterministic and safe to call during planning or tests.
    """
    google_enabled = not _present(environment.get("PAPER_CURATION_NO_GEMINI"))
    google_key = (
        environment.get("GOOGLE_API_KEY")
        or environment.get("GEMINI_API_KEY")
        or config.google_api_key
        or config.gemini_api_key
    )
    zotero_key = environment.get("ZOTERO_API_KEY") or config.zotero.api_key
    paperbanana_dir = environment.get("PAPERBANANA_DIR") or config.paperbanana_dir
    claude_key = environment.get("ANTHROPIC_API_KEY") or config.anthropic_api_key
    claude_oauth = environment.get("CLAUDE_CODE_OAUTH_TOKEN")
    return Capabilities(
        claude_auth=_present(claude_key) or _present(claude_oauth) or path_exists(Path(claude_credentials_path)),
        zotero=bool(config.zotero.collections) and _present(zotero_key),
        google_embeddings=google_enabled and _present(google_key),
        google_audio=google_enabled and _present(google_key),
        openai=_present(environment.get("OPENAI_API_KEY") or config.openai_api_key),
        paperbanana=_present(paperbanana_dir) and path_is_dir(Path(paperbanana_dir)),
        public_deploy=config.publication.mode == "public" and bool(config.publication.base_url),
    )
