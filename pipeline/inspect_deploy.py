#!/usr/bin/env python3
"""Read-only, fail-closed preflight for explicit public deployment."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def inspect_deploy(topic: str) -> tuple[str, ...]:
    failures: list[str] = []
    try:
        config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        config = {}
        failures.append("config.json is missing or invalid")
    publication = config.get("publication") if isinstance(config, dict) else {}
    publication = publication if isinstance(publication, dict) else {}
    if str(publication.get("mode", "")).lower() != "public":
        failures.append("publication.mode must be public")
    base_url = str(
        os.environ.get("PAPER_CURATION_PUBLIC_BASE_URL")
        or publication.get("base_url")
        or ""
    ).strip()
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        failures.append("an absolute public base URL is required")
    if not (os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CF_API_TOKEN")):
        failures.append("Cloudflare API token is required")
    if not os.environ.get("CLOUDFLARE_ACCOUNT_ID"):
        failures.append("CLOUDFLARE_ACCOUNT_ID is required")
    if shutil.which("npx") is None:
        failures.append("npx is required")
    for required in (
        ROOT / "wrangler.toml",
        ROOT / "docs" / "papers" / "_papers_index.json",
        ROOT / "docs" / topic / "index.html",
    ):
        if not required.is_file():
            failures.append(f"required deploy asset missing: {required.relative_to(ROOT)}")
    papers_index = ROOT / "docs" / "papers" / "_papers_index.json"
    if papers_index.is_file():
        try:
            papers = json.loads(papers_index.read_text(encoding="utf-8"))
            if not isinstance(papers, list) or not papers:
                failures.append("papers index must be a non-empty JSON array")
        except (OSError, ValueError):
            failures.append("papers index is invalid JSON")

    docs = ROOT / "docs"
    deploy_topics = sorted(
        directory
        for directory in docs.iterdir()
        if directory.is_dir()
        and directory.name != "papers"
        and not directory.name.startswith((".", "_"))
        and (directory / "index.html").is_file()
    ) if docs.is_dir() else []
    for directory in deploy_topics:
        classification = directory / "_new_classification.json"
        search_index = directory / "_search_index.json"
        for required in (classification, search_index):
            if not required.is_file():
                failures.append(
                    f"required deploy asset missing: {required.relative_to(ROOT)}"
                )
                continue
            try:
                payload = json.loads(required.read_text(encoding="utf-8"))
                if not isinstance(payload, (dict, list)):
                    raise ValueError
            except (OSError, ValueError):
                failures.append(
                    f"deploy asset is invalid JSON: {required.relative_to(ROOT)}"
                )
        if classification.is_file() and (
            directory / "index.html"
        ).stat().st_mtime < classification.stat().st_mtime:
            failures.append(f"topic page is stale: {directory.name}/index.html")
    return tuple(failures)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    args = parser.parse_args(argv)
    failures = inspect_deploy(args.topic)
    if failures:
        for failure in failures:
            print(f"[deploy-preflight] {failure}", file=sys.stderr)
        return 1
    print("[deploy-preflight] ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
