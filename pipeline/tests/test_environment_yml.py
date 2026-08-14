"""Contracts for the supported local Conda workstation environment."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class CondaEnvironmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.environment = yaml.safe_load(
            (ROOT / "environment.yml").read_text(encoding="utf-8")
        )

    def test_environment_uses_the_runtime_guard_name_and_python(self) -> None:
        self.assertEqual(self.environment["name"], "py312")
        dependencies = self.environment["dependencies"]
        self.assertIn("python=3.12", dependencies)
        self.assertIn("openjdk=17", dependencies)

    def test_native_clustering_stack_comes_from_conda_forge(self) -> None:
        self.assertEqual(self.environment["channels"], ["conda-forge"])
        dependencies = self.environment["dependencies"]
        for package in (
            "numpy",
            "scikit-learn",
            "joblib",
            "umap-learn",
            "hdbscan",
            "sentence-transformers",
        ):
            self.assertIn(package, dependencies)

    def test_pip_installs_remaining_dependencies_and_checkout(self) -> None:
        pip_blocks = [
            dependency["pip"]
            for dependency in self.environment["dependencies"]
            if isinstance(dependency, dict) and "pip" in dependency
        ]
        self.assertEqual(pip_blocks, [["-r requirements.txt", "-e ."]])

    def test_primary_docs_use_the_conda_environment(self) -> None:
        for relative in ("README.md", "README.en.md", "docs/setup-guide.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("conda env create -f environment.yml", text)
            self.assertIn("conda activate py312", text)


if __name__ == "__main__":
    unittest.main()
