"""Static contract for rejected personal, lecture, and scheduling tooling."""

import subprocess
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
DELETED_TOOLS = {
    "pipeline/agent_lecture_digest.py",
    "pipeline/agent_lecture_watchdog.py",
    "pipeline/curriculum_map.py",
    "pipeline/lecture_map.py",
}
TOOL_NAMES = {path.name for path in map(Path, DELETED_TOOLS)}
PROVENANCE_PATHS = {"docs/upstream-integration-provenance.md"}
ROOT_DOCUMENTS_AND_CONFIG = {
    ".env.example",
    ".gitignore",
    "CLAUDE.md",
    "README.en.md",
    "README.md",
    "config.example.json",
    "package.json",
}
HOME_PATH_MARKERS = ("/Users/", "/home/")
LECTURE_SCHEDULING_MARKERS = (
    "launchd",
    "lecture schedule",
    "lecture-schedule",
    "lecture_schedule",
    "lecture scheduler",
    "lecture-scheduler",
    "lecture_scheduler",
    "scheduled lecture",
    "scheduled-lecture",
    "scheduled_lecture",
    "lecture watchdog",
    "lecture-watchdog",
    "lecture_watchdog",
)


def tracked_paths():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        Path(line)
        for line in result.stdout.splitlines()
        if (REPOSITORY / line).is_file()
    ]


def is_scanned_production_path(path):
    if path.as_posix() in ROOT_DOCUMENTS_AND_CONFIG:
        return True
    if path.parts[0] == "pipeline":
        return len(path.parts) == 1 or path.parts[1] != "tests"
    return path.parts[0] in {"bin", "docs"}


class NoPersonalToolingTests(unittest.TestCase):
    def test_rejected_tools_are_absent_from_the_worktree(self):
        for tool in DELETED_TOOLS:
            with self.subTest(tool=tool):
                self.assertFalse((REPOSITORY / tool).exists())

    def test_tracked_production_paths_have_no_rejected_tool_references(self):
        offenders = []
        for path in tracked_paths():
            relative = path.as_posix()
            if not is_scanned_production_path(path) or relative in PROVENANCE_PATHS:
                continue
            try:
                text = (REPOSITORY / path).read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for tool_name in TOOL_NAMES:
                if tool_name in text:
                    offenders.append(f"{relative}: {tool_name}")
        self.assertEqual(offenders, [])

    def test_no_personal_home_or_lecture_scheduling_surface_remains(self):
        offenders = []
        for path in tracked_paths():
            relative = path.as_posix()
            if not is_scanned_production_path(path):
                continue
            try:
                text = (REPOSITORY / path).read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for marker in HOME_PATH_MARKERS:
                if marker in text:
                    offenders.append(f"{relative}: {marker}")
            if relative in PROVENANCE_PATHS:
                continue
            lowered = text.lower()
            for marker in LECTURE_SCHEDULING_MARKERS:
                if marker in lowered:
                    offenders.append(f"{relative}: {marker}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
