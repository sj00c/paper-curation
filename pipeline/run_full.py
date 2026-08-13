#!/usr/bin/env python3
"""Compatibility wrapper for the installed orchestration entrypoint."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_curation.orchestration.legacy_run_full import *  # noqa: F401,F403,E402
from paper_curation.orchestration.legacy_run_full import main  # noqa: E402


if __name__ == "__main__":
    main()
