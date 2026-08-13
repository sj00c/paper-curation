#!/usr/bin/env python3
"""Atomically publish a local bibliography DB to an explicit target."""
from __future__ import annotations

import argparse
import os
import shutil
import time
from pathlib import Path


def publish(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    shutil.copy2(source, tmp)
    os.replace(tmp, target)
    print(f"published {source} -> {target}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument(
        "--target",
        type=Path,
        help="Destination path (or set PAPER_CURATION_BIBLIO_PUBLISH_TARGET).",
    )
    ap.add_argument("--wait-for-pid", type=int)
    ap.add_argument("--poll", type=int, default=60)
    args = ap.parse_args()
    target = args.target or os.environ.get(
        "PAPER_CURATION_BIBLIO_PUBLISH_TARGET", ""
    ).strip()
    if not target:
        ap.error(
            "an explicit target is required: pass --target or set "
            "PAPER_CURATION_BIBLIO_PUBLISH_TARGET"
        )
    if args.wait_for_pid:
        while True:
            try:
                os.kill(args.wait_for_pid, 0)
            except ProcessLookupError:
                break
            except PermissionError:
                break
            time.sleep(args.poll)
    publish(args.source, Path(target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
