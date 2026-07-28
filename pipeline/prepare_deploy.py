"""Fail-closed preview adapter for an exact product-deploy scope.

The local product does not contain a trusted deployment-approval issuer or
deployment executor. It can preview one exact topic scope, but cannot deploy.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


_TOPIC_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")


def _require_topic(topic):
    if not isinstance(topic, str) or not _TOPIC_RE.fullmatch(topic):
        raise ValueError("topic must be an exact, safe topic alias")
    return topic


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inside(child, parent):
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def _relative_file(value, label):
    if not isinstance(value, str) or not value or value.startswith("/"):
        raise ValueError(f"{label} must be a relative file path")
    path = Path(value)
    if any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"{label} must not contain traversal")
    return path


def _load_sealed_scope(topic, staging_value, manifest_value, target_value, pathspec):
    """Validate a manifest whose complete file set seals the deploy input."""
    expected_pathspec = f"docs/{topic}"
    if pathspec != expected_pathspec:
        raise ValueError(f"pathspec must be exactly {expected_pathspec!r}")

    staging = Path(staging_value).resolve(strict=True)
    if not staging.is_dir() or staging.is_symlink():
        raise ValueError("staging must be a real directory")
    manifest = Path(manifest_value).resolve(strict=True)
    target = Path(target_value).resolve(strict=True)
    if not _inside(manifest, staging) or not _inside(target, staging):
        raise ValueError("manifest and target must be inside staging")
    if manifest.is_symlink() or target.is_symlink() or not manifest.is_file() or not target.is_file():
        raise ValueError("manifest and target must be regular files")

    try:
        document = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("manifest must be valid JSON") from exc
    if not isinstance(document, dict):
        raise ValueError("manifest must be an object")
    if document.get("topic") != topic or document.get("pathspec") != pathspec:
        raise ValueError("manifest topic or pathspec does not match the requested scope")

    target_rel = _relative_file(document.get("target"), "manifest target")
    if target != (staging / target_rel).resolve(strict=True):
        raise ValueError("target does not match the sealed manifest")
    files = document.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("manifest files must be a non-empty object")
    seen = set()
    for relative, expected_hash in files.items():
        rel = _relative_file(relative, "manifest file")
        if rel in seen or not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            raise ValueError("manifest contains an invalid file digest")
        if rel != target_rel and rel.parts[: len(Path(pathspec).parts)] != Path(pathspec).parts:
            raise ValueError("manifest file is outside the exact topic pathspec")
        seen.add(rel)
        candidate = (staging / rel).resolve(strict=True)
        if not _inside(candidate, staging) or candidate.is_symlink() or not candidate.is_file():
            raise ValueError("manifest references an unsafe file")
        if _sha256(candidate) != expected_hash:
            raise ValueError("sealed staging manifest has changed")
    actual_files = set()
    for candidate in staging.rglob("*"):
        if candidate.is_symlink():
            raise ValueError("sealed staging contains a symlink")
        if candidate.is_file() and candidate != manifest:
            actual_files.add(candidate.relative_to(staging))
    if actual_files != seen:
        missing = sorted(str(path) for path in seen - actual_files)
        extra = sorted(str(path) for path in actual_files - seen)
        raise ValueError(f"sealed staging file set mismatch: missing={missing}, extra={extra}")
    if target_rel not in seen:
        raise ValueError("manifest must seal the deploy target")
    scoped = (staging / pathspec).resolve(strict=True)
    if not _inside(scoped, staging) or not scoped.is_dir() or scoped.is_symlink():
        raise ValueError("sealed staging does not contain the exact topic scope")
    return staging, manifest, target, document




def main():
    parser = argparse.ArgumentParser(description="Preview one exact product-deploy scope")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--dry-run", action="store_true", help="Preview an exact topic scope only")
    args = parser.parse_args()
    try:
        topic = _require_topic(args.topic)
        if not args.dry_run:
            raise ValueError("only --dry-run is supported; product deploy requires an external trusted approval boundary")
        print(json.dumps({"operation": "deploy-preview", "topic": topic, "pathspec": f"docs/{topic}"}))
    except (ValueError, PermissionError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
