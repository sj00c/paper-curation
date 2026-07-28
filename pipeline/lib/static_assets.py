"""Integrity manifest and serving policy for owned local dashboard assets."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Mapping

ASSET_MANIFEST_VERSION = 1
ASSET_PACKAGE = "paper-curation"
ASSET_VERSION = "0.0.0"
ASSET_SOURCE = "owned-local-dashboard"
ASSET_SPDX = "MIT"


@dataclass(frozen=True)
class StaticAsset:
    """A content-addressed, repository-owned dashboard asset."""

    path: str
    byte_length: int
    sha256: str
    package: str
    version: str
    source: str
    spdx: str
    runtime_role: str


LOCAL_DASHBOARD_ASSETS: Mapping[str, StaticAsset] = {
    "docs/public/paper-curation-local.js": StaticAsset(
        path="docs/public/paper-curation-local.js",
        byte_length=14784,
        sha256="826f8b5444db75169d8b70d756de3135f644d7901a7b1f672d45cfee94c41285",
        package=ASSET_PACKAGE,
        version=ASSET_VERSION,
        source=ASSET_SOURCE,
        spdx=ASSET_SPDX,
        runtime_role="local-dashboard-behavior",
    ),
    "docs/public/paper-curation-local.css": StaticAsset(
        path="docs/public/paper-curation-local.css",
        byte_length=17661,
        sha256="820021c57d5ba6d8208cd4a043fefedb5b4556f788ae905d1fb1b712868854b7",
        package=ASSET_PACKAGE,
        version=ASSET_VERSION,
        source=ASSET_SOURCE,
        spdx=ASSET_SPDX,
        runtime_role="local-dashboard-presentation",
    ),
}



def _relative_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise ValueError("asset path must be a non-traversing repository-relative path")
    return candidate


def _asset_file(repo_root: Path, repo_relative_path: str) -> Path:
    root = Path(repo_root).resolve(strict=True)
    relative = _relative_path(repo_relative_path)
    candidate = root
    for part in relative.parts:
        candidate /= part
        if candidate.is_symlink():
            raise ValueError(f"asset must not contain a symlink: {repo_relative_path}")
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(f"asset escapes repository root: {repo_relative_path}") from error
    return candidate


def manifest_records() -> tuple[dict[str, object], ...]:
    """Return deterministic serializable records for the versioned manifest."""
    return tuple(asdict(LOCAL_DASHBOARD_ASSETS[path]) for path in sorted(LOCAL_DASHBOARD_ASSETS))


def verify_manifest_closure(repo_root: Path | str, observed_paths: Iterable[str] | None = None) -> None:
    """Reject missing, extra, altered, symlinked, or traversing local assets."""
    expected = set(LOCAL_DASHBOARD_ASSETS)
    if observed_paths is None:
        root = Path(repo_root).resolve(strict=True)
        observed = {
            path.relative_to(root).as_posix()
            for path in (root / "docs/public").glob("paper-curation-local.*")
        }
    else:
        observed = {Path(path).as_posix() for path in observed_paths}
    if observed != expected:
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        raise ValueError(f"asset manifest closure mismatch: missing={missing}, extra={extra}")
    for path, asset in LOCAL_DASHBOARD_ASSETS.items():
        file_path = _asset_file(Path(repo_root), path)
        if not file_path.is_file():
            raise ValueError(f"asset is missing or not a regular file: {path}")
        content = file_path.read_bytes()
        if len(content) != asset.byte_length:
            raise ValueError(f"asset byte length mismatch: {path}")
        if sha256(content).hexdigest() != asset.sha256:
            raise ValueError(f"asset SHA-256 mismatch: {path}")


def local_asset_headers(repo_relative_path: str) -> dict[str, str]:
    """Return the fixed safe response policy for an integrity-verified asset."""
    _relative_path(repo_relative_path)
    asset = LOCAL_DASHBOARD_ASSETS.get(repo_relative_path)
    if asset is None:
        raise ValueError("unknown local dashboard asset")
    mime = "text/javascript; charset=utf-8" if asset.path.endswith(".js") else "text/css; charset=utf-8"
    return {
        "Content-Type": mime,
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
    }
