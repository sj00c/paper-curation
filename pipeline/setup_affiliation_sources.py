#!/usr/bin/env python3
"""Acquire and build the public ROR inputs used for affiliation normalization.

The ROR dump and projected SQLite index live under gitignored ``.cache/``.
This command makes their acquisition reproducible and idempotent.

    python pipeline/setup_affiliation_sources.py            # ensure everything
    python pipeline/setup_affiliation_sources.py --check     # report, change nothing
    python pipeline/setup_affiliation_sources.py --refresh-ror  # pull a new release
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

ROR_DIR = ROOT / ".cache" / "ror"
ZENODO_COMMUNITY = "https://zenodo.org/api/records?communities=ror-data&sort=newest&size=1"


def latest_ror_release() -> dict:
    with urllib.request.urlopen(ZENODO_COMMUNITY, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    hits = payload.get("hits", {}).get("hits") or []
    if not hits:
        raise SystemExit("Zenodo returned no ROR release")
    record = hits[0]
    for entry in record.get("files", []):
        if entry["key"].endswith("-ror-data.zip"):
            return {"key": entry["key"], "size": entry["size"],
                    "url": entry["links"]["self"],
                    "record": str(record.get("id", ""))}
    raise SystemExit("newest ROR release has no -ror-data.zip asset")


def download(url: str, target: Path, expected_size: int) -> None:
    """Download to a temporary file and only then publish it.

    A partial download that keeps the final name is worse than no download: the
    first attempt at this dump stopped at 8 of 35 MB and looked present.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".part")
    request = urllib.request.Request(
        url, headers={"User-Agent": "paper-curation/1.0 (affiliation setup)"})
    with urllib.request.urlopen(request, timeout=300) as response, \
            temporary.open("wb") as handle:
        shutil.copyfileobj(response, handle, length=1 << 20)
    actual = temporary.stat().st_size
    if expected_size and actual != expected_size:
        temporary.unlink(missing_ok=True)
        raise SystemExit(
            f"incomplete download: {actual} of {expected_size} bytes")
    temporary.replace(target)


def ensure_ror_dump(refresh: bool = False) -> dict:
    from lib import ror_index
    existing = ror_index.latest_dump()
    if existing and not refresh:
        return {"status": "present", "dump": existing.name,
                "bytes": existing.stat().st_size}
    release = latest_ror_release()
    archive = ROR_DIR / release["key"]
    if not archive.exists() or archive.stat().st_size != release["size"]:
        download(release["url"], archive, release["size"])
    with zipfile.ZipFile(archive) as bundle:
        members = [n for n in bundle.namelist() if n.endswith(".json")]
        if not members:
            raise SystemExit(f"{archive.name} contains no JSON payload")
        bundle.extract(members[0], ROR_DIR)
    return {"status": "downloaded", "dump": members[0],
            "archive": archive.name, "zenodo_record": release["record"]}


def ensure_ror_index(rebuild: bool = False) -> dict:
    from lib import ror_index
    if ror_index.INDEX_PATH.exists() and not rebuild:
        import sqlite3
        conn = sqlite3.connect(f"file:{ror_index.INDEX_PATH}?mode=ro", uri=True)
        try:
            meta = dict(conn.execute("SELECT key, value FROM meta").fetchall())
        finally:
            conn.close()
        return {"status": "present", **meta}
    return {"status": "built", **ror_index.build_index()}


def report() -> dict:
    from lib import ror_index
    dump = ror_index.latest_dump()
    return {
        "ror_dump": dump.name if dump else None,
        "ror_index": (str(ror_index.INDEX_PATH)
                      if ror_index.INDEX_PATH.exists() else None),
        "ready": bool(ror_index.INDEX_PATH.exists()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report what is present and exit non-zero if not ready")
    ap.add_argument("--refresh-ror", action="store_true",
                    help="download the newest ROR release and rebuild the index")
    args = ap.parse_args()

    if args.check:
        state = report()
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0 if state["ready"] else 2

    result = {"dump": ensure_ror_dump(refresh=args.refresh_ror)}
    result["index"] = ensure_ror_index(rebuild=args.refresh_ror)
    result["state"] = report()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["state"]["ready"] else 2


if __name__ == "__main__":
    from _env_guard import force_py312
    force_py312()
    raise SystemExit(main())
