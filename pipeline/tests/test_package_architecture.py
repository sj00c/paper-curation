"""Dependency-direction contracts for the installable package."""

import ast
import sys
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


class PackageArchitectureTests(unittest.TestCase):
    def _imports(self, relative):
        path = SRC / "paper_curation" / relative
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                found.append(node.module)
        return found

    def test_domain_depends_only_on_domain_and_standard_library(self):
        forbidden = ("paper_curation.application", "paper_curation.integrations",
                     "paper_curation.rendering", "paper_curation.orchestration",
                     "paper_curation.retrieval", "paper_curation.bibliography")
        offenders = []
        for path in (SRC / "paper_curation" / "domain").glob("*.py"):
            for imported in self._imports(path.relative_to(SRC / "paper_curation")):
                if imported.startswith(forbidden):
                    offenders.append(f"{path.name}: {imported}")
        self.assertEqual(offenders, [])

    def test_application_does_not_import_outward_adapters(self):
        forbidden = ("paper_curation.integrations", "paper_curation.rendering",
                     "paper_curation.retrieval", "paper_curation.bibliography")
        offenders = []
        for path in (SRC / "paper_curation" / "application").glob("*.py"):
            for imported in self._imports(path.relative_to(SRC / "paper_curation")):
                if imported.startswith(forbidden):
                    offenders.append(f"{path.name}: {imported}")
        self.assertEqual(offenders, [])

    def test_package_imports_do_not_load_legacy_pipeline(self):
        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                f"import sys;sys.path.insert(0,{str(SRC)!r});import paper_curation; "
                "print(paper_curation.__version__); "
                "raise SystemExit(any(n.startswith('pipeline.') for n in sys.modules))",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        self.assertTrue(probe.stdout.strip())


if __name__ == "__main__":
    unittest.main()
