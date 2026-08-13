#!/usr/bin/env python3
"""Read-only local installation summary for paper-curation."""

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path


DEFAULT_ZOTERO_DB = Path.home() / "Zotero" / "zotero.sqlite"
PLACEHOLDER_ZOTERO_KEY = "YOUR_ZOTERO_API_KEY_HERE"


def run_command(args, cwd):
    """Return a local command's result without emitting its untrusted output."""
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except FileNotFoundError:
        return None, "not installed"
    except subprocess.TimeoutExpired:
        return None, "timed out"
    except OSError as exc:
        return None, type(exc).__name__
    return result, ""


def redact_remote(value):
    """Avoid showing credentials embedded in a Git remote URL."""
    def redact_userinfo(match):
        return match.group("prefix") + ("git@" if match.group("user") == "git" else "***@")

    value = re.sub(
        r"(?P<prefix>://|\s)(?P<user>[^/@\s]+)@",
        redact_userinfo,
        value,
    )
    value = re.sub(r"(://)[^/@\s]+@", r"\1***@", value)
    value = re.sub(r"([?&](?:access_)?token=)[^&#\s]+", r"\1***", value, flags=re.I)
    return value


def load_config(path):
    if not path.exists():
        return None, None
    try:
        with path.open(encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return None, type(exc).__name__
    if not isinstance(config, dict):
        return None, "top-level value is not an object"
    return config, None


def configured_zotero_key(config):
    zotero = config.get("zotero", {}) if isinstance(config, dict) else {}
    value = zotero.get("api_key", "") if isinstance(zotero, dict) else ""
    return bool(str(value).strip() and value != PLACEHOLDER_ZOTERO_KEY) or bool(
        os.environ.get("ZOTERO_API_KEY", "").strip()
    )


def configured_collections(config):
    zotero = config.get("zotero", {}) if isinstance(config, dict) else {}
    collections = zotero.get("collections", {}) if isinstance(zotero, dict) else {}
    if not isinstance(collections, dict):
        return []
    return [(str(alias), str(name)) for alias, name in collections.items() if str(alias).strip()]


def publication_summary(config):
    publication = config.get("publication", {}) if isinstance(config, dict) else {}
    publication = publication if isinstance(publication, dict) else {}
    mode = str(publication.get("mode", "local")).strip().lower() or "local"
    configured_base_url = str(publication.get("base_url", "")).strip()
    environment_base_url = os.environ.get("PAPER_CURATION_PUBLIC_BASE_URL", "").strip()
    base_url = environment_base_url or configured_base_url
    if mode == "public":
        return f"public (explicit; base URL {'configured' if base_url else 'missing'})"
    return "local (default)"


def inspect_repository(repo):
    print("Repository")
    git_dir = repo / ".git"
    if not git_dir.exists():
        print("  checkout: not a Git checkout")
        return
    print("  checkout: Git repository")
    remotes, error = run_command(["git", "remote", "-v"], repo)
    if remotes is None:
        print(f"  remotes: unavailable ({error})")
        return
    lines = []
    seen = set()
    for line in remotes.stdout.splitlines():
        safe = redact_remote(line.strip())
        if safe and safe not in seen:
            seen.add(safe)
            lines.append(safe)
    if lines:
        for line in lines:
            print(f"  remote: {line}")
    else:
        print("  remotes: none configured")


def inspect_python():
    print("Runtime")
    print(f"  Python: {sys.version.split()[0]} ({sys.executable})")
    if sys.version_info[:2] == (3, 12):
        print("  Python requirement: ready (3.12)")
    else:
        print("  Python requirement: needs 3.12 (use conda run -n py312)")


def inspect_claude(repo):
    version, version_error = run_command(["claude", "--version"], repo)
    if version is None:
        print(f"  Claude Code: unavailable ({version_error})")
    elif version.returncode:
        print(f"  Claude Code: unavailable (exit {version.returncode})")
    else:
        match = re.search(r"\d+\.\d+\.\d+", version.stdout + version.stderr)
        print(f"  Claude Code: {match.group(0) if match else 'version not recognized'}")

    auth, auth_error = run_command(["claude", "auth", "status"], repo)
    if auth is None:
        print(f"  Claude auth: unavailable ({auth_error})")
    elif auth.returncode == 0:
        print("  Claude auth: ready (OAuth status command succeeded)")
    else:
        print("  Claude auth: not ready (run claude auth login, or configure ANTHROPIC_API_KEY)")


def inspect_config(repo):
    print("Configuration")
    config, error = load_config(repo / "config.json")
    if error:
        print(f"  config.json: unreadable ({error})")
        return [], None
    if config is None:
        print("  config.json: absent (local configuration has not been created)")
        print("  publication: local (default)")
        return [], None

    print("  config.json: present")
    print(f"  Zotero API key: {'configured' if configured_zotero_key(config) else 'missing'}")
    print(f"  publication: {publication_summary(config)}")
    collections = configured_collections(config)
    if collections:
        print("  topics:")
        keywords = config.get("search_keywords", {})
        profiles = config.get("topic_profiles", {})
        for alias, collection in collections:
            print(f"    {alias}: {collection}")
            if not isinstance(keywords, dict) or alias not in keywords:
                print("      search keywords: missing")
            if not isinstance(profiles, dict) or alias not in profiles:
                print("      presentation profile: using neutral defaults")
    else:
        print("  topics: none configured")
    return collections, config


def inspect_zotero_db():
    configured = os.environ.get("ZOTERO_SQLITE", "").strip()
    database = Path(configured).expanduser() if configured else DEFAULT_ZOTERO_DB
    source = "ZOTERO_SQLITE" if configured else "default path"
    state = "present" if database.is_file() else "missing"
    print(f"  Zotero local SQLite: {state} ({source}: {database})")
    if not database.is_file():
        return
    try:
        # Zotero commonly holds an exclusive lock while running. Immutable
        # read-only mode inspects the last durable snapshot without creating a
        # copy, journal, or other file.
        uri = database.resolve().as_uri() + "?mode=ro&immutable=1"
        connection = sqlite3.connect(uri, uri=True, timeout=2)
        try:
            rows = connection.execute(
                "SELECT c.collectionName, COUNT(DISTINCT ci.itemID) "
                "FROM collections c "
                "LEFT JOIN collectionItems ci ON ci.collectionID=c.collectionID "
                "LEFT JOIN deletedItems d ON d.itemID=ci.itemID "
                "WHERE c.parentCollectionID IS NULL AND d.itemID IS NULL "
                "GROUP BY c.collectionID, c.collectionName "
                "ORDER BY c.collectionName"
            ).fetchall()
        finally:
            connection.close()
    except (OSError, sqlite3.Error) as exc:
        print(f"  Zotero collections: unavailable ({type(exc).__name__})")
        return
    print("  Zotero top-level collections:")
    for name, count in rows:
        print(f"    {name}: {count:,}")


def print_next_steps(collections):
    print("Next steps")
    if len(collections) != 1:
        print("  Build and serve commands are withheld until exactly one topic alias is configured.")
        return
    topic, _ = collections[0]
    print(f"  Build: PYTHONUTF8=1 conda run -n py312 python pipeline/run_full.py --topic {topic}")
    print(f"  Serve: PYTHONUTF8=1 conda run -n py312 python pipeline/serve_local.py --topic {topic}")


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Read-only paper-curation installation summary")
    parser.add_argument("--dir", default=".", help="paper-curation checkout (default: current directory)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    repo = Path(args.dir).expanduser().resolve()
    print("paper-curation inspect (read-only; no network operations)")
    inspect_repository(repo)
    inspect_python()
    inspect_claude(repo)
    collections, _ = inspect_config(repo)
    inspect_zotero_db()
    print_next_steps(collections)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
