"""Contract tests for local committed-Core workspace operations."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from paper_curation.integrations.persistence.workspace_ops import FilesystemWorkspaceOps
from paper_curation.domain.papers import paper_identity_fingerprint


class WorkspaceOperationsTests(unittest.TestCase):
    def _record(self, root: Path, *, title: str = "Record", tamper: bool = False) -> Path:
        paper = {"source_id": "source<unsafe>", "scope_id": "scope", "record_id": title}
        record = root / "papers"
        for key in ("source_id", "scope_id", "record_id"):
            record /= hashlib.sha256(paper[key].encode()).hexdigest()
        record.mkdir(parents=True)
        page = record / "index.html"
        page.write_text("<!doctype html><title>page</title>", encoding="utf-8")
        source = record / "source.pdf"
        source.write_bytes(b"source")
        text = record / "text.txt"
        review = record / "review.md"
        sidecar = record / "sidecar.json"
        for path in (text, review, sidecar):
            path.write_text(path.name, encoding="utf-8")
        def artifact(name: str, path: Path) -> dict[str, str]:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            return {"name": name, "path": str(path.resolve()), "fingerprint": digest}
        source_artifact = artifact("source-pdf", source)
        text_artifact = artifact("text", text)
        review_artifact = artifact("review.md", review)
        sidecar_artifact = artifact("sidecar", sidecar)
        page_artifact = artifact("page", page)
        receipt = {
            "schema_version": 1,
            "paper": paper,
            "stages": [
                {"stage": "identify", "fingerprint": paper_identity_fingerprint(paper["source_id"], paper["scope_id"], paper["record_id"]), "artifacts": []},
                {"stage": "materialize_source", "input_id": "attachment-id", "fingerprint": source_artifact["fingerprint"], "artifacts": [source_artifact]},
                {"stage": "extract_text", "fingerprint": text_artifact["fingerprint"], "artifacts": [text_artifact]},
                {"stage": "generate_review", "provider_id": "provider", "model_id": "model", "fingerprint": review_artifact["fingerprint"], "artifacts": [review_artifact]},
                {"stage": "write_sidecar", "fingerprint": sidecar_artifact["fingerprint"], "artifacts": [sidecar_artifact]},
                {"stage": "render_page", "fingerprint": page_artifact["fingerprint"], "artifacts": [page_artifact]},
            ],
        }
        (record / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
        if tamper:
            page.write_text("tampered", encoding="utf-8")
        return record

    def test_build_is_safe_loadable_and_uses_only_committed_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self._record(root, title='title<unsafe>')
            result = FilesystemWorkspaceOps(root).build()
            index = result.index_path.read_text(encoding="utf-8")
            self.assertTrue(index.startswith("<!doctype html>"))
            self.assertIn("source&lt;unsafe&gt;", index)
            self.assertIn("papers/", index)
            copied_page = root / "site" / result.entries[0].page_path.relative_to(root.resolve())
            self.assertTrue(copied_page.is_file())
            self.assertNotIn("provider", index.lower())
            self.assertFalse((root / "site" / "source.pdf").exists())

    def test_validate_detects_complete_malformed_tampered_and_traversal_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            valid = FilesystemWorkspaceOps(root)
            self._record(root)
            self.assertTrue(valid.validate().valid)
            malformed = self._record(root, title="malformed")
            (malformed / "receipt.json").write_text("{", encoding="utf-8")
            tampered = self._record(root, title="tampered", tamper=True)
            traversal = self._record(root, title="traversal")
            receipt = json.loads((traversal / "receipt.json").read_text(encoding="utf-8"))
            receipt["stages"][-1]["artifacts"][0]["path"] = "../config.json"
            (traversal / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            issues = valid.validate().issues
            self.assertGreaterEqual(len(issues), 3)
            messages = "\n".join(issue.message for issue in issues)
            self.assertIn("malformed", messages)
            self.assertIn("fingerprint", messages)
            self.assertIn("exact record-local", messages)
            with self.assertRaises(ValueError):
                valid.build()

    def test_repair_previews_then_quarantines_generated_records_and_preserves_protected_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            record = self._record(root, tamper=True)
            staging = root / ".staging" / "abandoned"
            staging.mkdir(parents=True)
            source_pdf = root / "source.pdf"
            config = root / "config.json"
            credentials = root / "credentials.json"
            for protected in (source_pdf, config, credentials):
                protected.write_text("protected", encoding="utf-8")
            workspace = FilesystemWorkspaceOps(root)
            preview = workspace.repair(execute=False)
            self.assertFalse(preview.executed)
            self.assertTrue(record.exists())
            self.assertTrue(staging.exists())
            result = workspace.repair(execute=True)
            self.assertTrue(result.executed)
            self.assertFalse(record.exists())
            self.assertFalse(staging.exists())
            self.assertEqual(len(list((root / ".quarantine").rglob("receipt.json"))), 1)
            for protected in (source_pdf, config, credentials):
                self.assertEqual(protected.read_text(encoding="utf-8"), "protected")

    def test_failed_build_preserves_prior_site(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            site = root / "site"
            site.mkdir()
            prior = site / "index.html"
            prior.write_text("prior site", encoding="utf-8")
            self._record(root, tamper=True)
            with self.assertRaises(ValueError):
                FilesystemWorkspaceOps(root).build()
            self.assertEqual(prior.read_text(encoding="utf-8"), "prior site")

    def test_rejects_symlinked_workspace_roots_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            outside = root / "outside"
            outside.mkdir()
            linked_workspace = root / "linked-workspace"
            linked_workspace.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                FilesystemWorkspaceOps(linked_workspace).build()
            (root / "papers").symlink_to(outside, target_is_directory=True)
            workspace = FilesystemWorkspaceOps(root)
            self.assertFalse(workspace.validate().valid)
            with self.assertRaises(ValueError):
                workspace.build()
            with self.assertRaises(ValueError):
                workspace.repair(execute=True)
            (root / "papers").unlink()
            self._record(root)
            for name in (".staging", ".quarantine", "site"):
                (root / name).symlink_to(outside, target_is_directory=True)
                with self.assertRaises(ValueError):
                    FilesystemWorkspaceOps(root).repair(execute=True)
                (root / name).unlink()
            unsafe_staging = root / ".staging" / "unsafe"
            unsafe_staging.parent.mkdir()
            unsafe_staging.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "unsafe|symlink"):
                FilesystemWorkspaceOps(root).repair(execute=False)
            unsafe_staging.unlink()
            record = self._record(root, title="partial")
            for child in record.iterdir():
                if child.name != "source.pdf":
                    child.unlink()
            self.assertFalse(FilesystemWorkspaceOps(root).validate().valid)
            self.assertTrue(
                FilesystemWorkspaceOps(root).repair(execute=False).actions
            )

    def test_rejects_cross_record_wrong_duplicate_and_incomplete_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            first = self._record(root, title="first")
            second = self._record(root, title="second")
            receipt = json.loads((first / "receipt.json").read_text(encoding="utf-8"))
            receipt["stages"][1]["artifacts"][0]["path"] = str(second / "source.pdf")
            receipt["stages"][2]["artifacts"].append(receipt["stages"][2]["artifacts"][0])
            receipt["stages"][3]["artifacts"][0]["name"] = "page"
            (first / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            incomplete = self._record(root, title="incomplete")
            incomplete_receipt = json.loads((incomplete / "receipt.json").read_text(encoding="utf-8"))
            incomplete_receipt["stages"].pop()
            (incomplete / "receipt.json").write_text(json.dumps(incomplete_receipt), encoding="utf-8")
            messages = "\n".join(issue.message for issue in FilesystemWorkspaceOps(root).validate().issues)
            self.assertIn("exact record-local", messages)
            self.assertIn("duplicate", messages)
            self.assertIn("incomplete", messages)

    def test_fingerprints_stream_source_and_repair_refuses_external_action(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            record = self._record(root)
            source = record / "source.pdf"
            source.write_bytes(b"x" * (2 * 1024 * 1024 + 1))
            receipt = json.loads((record / "receipt.json").read_text(encoding="utf-8"))
            receipt["stages"][1]["artifacts"][0]["fingerprint"] = hashlib.sha256(source.read_bytes()).hexdigest()
            receipt["stages"][1]["fingerprint"] = receipt["stages"][1]["artifacts"][0]["fingerprint"]
            (record / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            with patch.object(Path, "read_bytes", side_effect=AssertionError("must stream")):
                self.assertTrue(FilesystemWorkspaceOps(root).validate().valid)
            external = root.parent / "not-generated"
            external.mkdir(exist_ok=True)
            with self.assertRaisesRegex(ValueError, "target"):
                FilesystemWorkspaceOps(root)._execute(
                    type(
                        "Action",
                        (),
                        {"action": "quarantine-record", "path": external},
                    )()
                )
            self.assertTrue(external.exists())


if __name__ == "__main__":
    unittest.main()
