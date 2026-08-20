"""AST-enforced dependency boundaries for the installable package.

These tests intentionally inspect imports rather than comments or arbitrary source text.
"""

from __future__ import annotations

import ast
import unittest
from collections.abc import Iterable
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = ROOT / "src" / "paper_curation"

DOMAIN_FORBIDDEN_PREFIXES = (
    "argparse",
    "os",
    "pathlib",
    "shutil",
    "tempfile",
    "glob",
    "fileinput",
    "zipfile",
    "tarfile",
    "sqlite3",
    "subprocess",
    "importlib.resources",
    "http",
    "urllib",
    "socket",
    "ssl",
    "ftplib",
    "smtplib",
    "imaplib",
    "poplib",
    "telnetlib",
    "requests",
    "httpx",
    "aiohttp",
    "websockets",
    "boto3",
    "anthropic",
    "openai",
    "vertexai",
    "cohere",
    "mistralai",
    "ollama",
    "groq",
    "google",
    "litellm",
    "together",
    "replicate",
    "huggingface_hub",
    "transformers",
    "paper_curation.cli",
    "paper_curation.rendering",
    "paper_curation.integrations",
)

APPLICATION_FORBIDDEN_PREFIXES = (
    "pipeline",
    "anthropic",
    "openai",
    "vertexai",
    "cohere",
    "mistralai",
    "ollama",
    "groq",
    "google",
    "litellm",
    "together",
    "replicate",
    "huggingface_hub",
    "transformers",
    "paper_curation.integrations",
    "paper_curation.rendering",
    "paper_curation.bibliography",
    "paper_curation.retrieval",
)

CONCRETE_ADAPTER_PREFIXES = (
    "paper_curation.integrations",
    "paper_curation.rendering",
    "paper_curation.bibliography",
    "paper_curation.retrieval",
)


def package_module(path: Path) -> str:
    relative = path.relative_to(PACKAGE_ROOT).with_suffix("")
    parts = ("paper_curation", *relative.parts)
    return ".".join(parts[:-1] if path.name == "__init__.py" else parts)


def resolve_from_import(path: Path, node: ast.ImportFrom) -> str:
    """Return an absolute target for an ``ImportFrom``, including relative imports."""
    if not node.level:
        return node.module or ""

    package_parts = package_module(path).split(".")
    if path.name != "__init__.py":
        package_parts.pop()
    parent_parts = package_parts[: len(package_parts) - node.level + 1]
    if node.module:
        parent_parts.extend(node.module.split("."))
    return ".".join(parent_parts)


def imports_in(path: Path) -> Iterable[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from ((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            target = resolve_from_import(path, node)
            if target:
                if any(alias.name == "*" for alias in node.names):
                    yield node.lineno, target
                else:
                    yield from (
                        (node.lineno, f"{target}.{alias.name}")
                        for alias in node.names
                    )


def has_prefix(target: str, prefixes: tuple[str, ...]) -> bool:
    return any(target == prefix or target.startswith(f"{prefix}.") for prefix in prefixes)


def is_internal_adapter_import(path: Path, target: str) -> bool:
    importer = package_module(path)
    return any(
        (target == prefix or target.startswith(f"{prefix}."))
        and (importer == prefix or importer.startswith(f"{prefix}."))
        for prefix in CONCRETE_ADAPTER_PREFIXES
    )


def source_files(directory: Path) -> Iterable[Path]:
    return sorted(path for path in directory.rglob("*.py") if "__pycache__" not in path.parts)


class ArchitectureBoundaryTests(unittest.TestCase):
    maxDiff = None

    def assert_no_forbidden_imports(self, directory: Path, prefixes: tuple[str, ...], policy: str) -> None:
        violations = []
        for path in source_files(directory):
            for line, target in imports_in(path):
                if has_prefix(target, prefixes):
                    violations.append(f"{path.relative_to(ROOT)}:{line}: imports {target}")
        self.assertEqual(
            [],
            violations,
            f"{policy}. Move the dependency behind an application-owned port and assemble it in "
            f"paper_curation.composition.\n" + "\n".join(violations),
        )

    def test_domain_has_no_cli_io_rendering_or_provider_imports(self) -> None:
        self.assert_no_forbidden_imports(
            PACKAGE_ROOT / "domain",
            DOMAIN_FORBIDDEN_PREFIXES,
            "Domain must remain pure: no CLI, filesystem, network, rendering, or provider imports",
        )

    def test_application_has_no_pipeline_or_concrete_provider_adapter_imports(self) -> None:
        self.assert_no_forbidden_imports(
            PACKAGE_ROOT / "application",
            APPLICATION_FORBIDDEN_PREFIXES,
            "Application must not import pipeline, provider SDKs, or concrete adapters",
        )

    def test_only_composition_root_may_import_concrete_adapter_packages(self) -> None:
        violations = []
        composition = PACKAGE_ROOT / "composition.py"
        for path in source_files(PACKAGE_ROOT):
            if path == composition:
                continue
            for line, target in imports_in(path):
                if (
                    has_prefix(target, CONCRETE_ADAPTER_PREFIXES)
                    and not is_internal_adapter_import(path, target)
                ):
                    violations.append(f"{path.relative_to(ROOT)}:{line}: imports {target}")
        self.assertEqual(
            [],
            violations,
            "Concrete adapters may be assembled only by paper_curation.composition.\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
