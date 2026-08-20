"""Contract tests for the local Core filesystem adapters."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import fitz

from paper_curation.domain.papers import (
    ArtifactRef,
    Paper,
    StageEvidence,
    paper_identity_fingerprint,
)
from paper_curation.integrations.persistence import (
    FilesystemEvidenceVerifier,
    FilesystemPage,
    FilesystemReceipt,
    FilesystemSidecar,
)
from paper_curation.integrations.text import PyMuPDFTextExtractor


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stage(
    stage: str,
    *artifacts: ArtifactRef,
    provider_id: str = "",
    input_id: str = "",
    model_id: str = "",
) -> StageEvidence:
    return StageEvidence(
        stage,
        artifacts,
        "|".join(item.fingerprint for item in artifacts) or "identity",
        provider_id,
        input_id,
        model_id,
    )


class CoreFilesystemAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace = (Path(self.temporary.name) / "workspace").resolve()
        self.paper = Paper("zotero", "scope-1", "record-1", "<Unsafe title>", ("A <Author>",), "<abstract>")
        self.sidecars = FilesystemSidecar(self.workspace)
        self.pages = FilesystemPage(self.workspace)
        self.receipts = FilesystemReceipt(self.workspace)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _pdf_source(self, text: str = "Meaningful PDF text") -> ArtifactRef:
        pdf = self.workspace / "input.pdf"
        pdf.parent.mkdir(parents=True, exist_ok=True)
        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), text)
        document.save(pdf)
        document.close()
        return ArtifactRef("source-pdf", str(pdf), _digest(pdf))

    def _staged_source(self, text: str = "Meaningful PDF text") -> ArtifactRef:
        input_source = self._pdf_source(text)
        source_path = self.workspace / ".staging" / Path(
            hashlib.sha256(self.paper.source_id.encode()).hexdigest(),
            hashlib.sha256(self.paper.scope_id.encode()).hexdigest(),
            hashlib.sha256(self.paper.record_id.encode()).hexdigest(),
            "source.pdf",
        )
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_bytes(Path(input_source.path).read_bytes())
        source = ArtifactRef(
            "source-pdf",
            str(self.workspace / "papers" / source_path.relative_to(self.workspace / ".staging")),
            _digest(source_path),
        )
        return source

    def _core_outputs(self, review_markdown: str = "# Review\nA **useful** review") -> tuple[ArtifactRef, ArtifactRef, ArtifactRef, ArtifactRef]:
        source = self._staged_source()
        text = PyMuPDFTextExtractor(self.workspace).extract(self.paper, source)
        review_path = self.workspace / ".staging" / Path(text.path).relative_to(self.workspace / "papers").parent / "review.md"
        review_path.write_text(review_markdown, encoding="utf-8")
        review = ArtifactRef("review.md", str(Path(text.path).with_name("review.md")), _digest(review_path))
        sidecar = self.sidecars.write(
            self.paper, text, review, "selected-provider", "selected-model"
        )
        page = self.pages.render(self.paper, review, sidecar)
        return source, text, sidecar, page

    def _complete_evidence(
        self, source: ArtifactRef, text: ArtifactRef, sidecar: ArtifactRef, page: ArtifactRef
    ) -> tuple[StageEvidence, ...]:
        review_path = self.workspace / ".staging" / Path(text.path).relative_to(
            self.workspace / "papers"
        ).parent / "review.md"
        review = ArtifactRef("review.md", str(Path(text.path).with_name("review.md")), _digest(review_path))
        return (
            StageEvidence(
                "identify",
                fingerprint=paper_identity_fingerprint(
                    self.paper.source_id,
                    self.paper.scope_id,
                    self.paper.record_id,
                ),
            ),
            _stage("materialize_source", source, input_id="ATTACHMENT"),
            _stage("extract_text", text),
            _stage(
                "generate_review",
                review,
                provider_id="selected-provider",
                model_id="selected-model",
            ),
            _stage("write_sidecar", sidecar),
            _stage("render_page", page),
        )

    def test_extracts_selected_pdf_to_utf8_staging_with_sha256(self) -> None:
        text = PyMuPDFTextExtractor(self.workspace).extract(
            self.paper, self._staged_source("PDF extraction works")
        )
        staged = self.workspace / ".staging" / Path(text.path).relative_to(self.workspace / "papers")
        self.assertEqual(staged.read_text(encoding="utf-8").strip(), "PDF extraction works")
        self.assertEqual(text.fingerprint, _digest(staged))
        with self.assertRaisesRegex(ValueError, "meaningful text"):
            PyMuPDFTextExtractor(self.workspace).extract(
                self.paper, self._staged_source("   ")
            )
        external = self._pdf_source("external")
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            PyMuPDFTextExtractor(self.workspace).extract(self.paper, external)

    def test_sidecar_records_only_bibliographic_and_hash_provenance(self) -> None:
        _, text, sidecar, _ = self._core_outputs("review payload must not be copied")
        staged = self.workspace / ".staging" / Path(sidecar.path).relative_to(self.workspace / "papers")
        payload = json.loads(staged.read_text(encoding="utf-8"))
        self.assertEqual(payload["paper"]["source_id"], "zotero")
        self.assertEqual(payload["text_sha256"], text.fingerprint)
        self.assertEqual(payload["review_provider_id"], "selected-provider")
        self.assertEqual(payload["review_model_id"], "selected-model")
        self.assertNotIn("review payload", staged.read_text(encoding="utf-8"))

    def test_page_escapes_untrusted_markdown_and_metadata(self) -> None:
        _, _, _, page = self._core_outputs("# Review\n<script>alert('x')</script>")
        staged = self.workspace / ".staging" / Path(page.path).relative_to(self.workspace / "papers")
        rendered = staged.read_text(encoding="utf-8")
        self.assertTrue(rendered.startswith("<!doctype html>"))
        self.assertIn("&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;", rendered)
        self.assertNotIn("<script>alert", rendered)
        self.assertIn("&lt;Unsafe title&gt;", rendered)

    def test_receipt_validates_fingerprints_promotes_atomically_and_is_secret_free(self) -> None:
        source, text, sidecar, page = self._core_outputs("review with credential=super-secret and provider payload")
        evidence = self._complete_evidence(source, text, sidecar, page)
        receipt = self.receipts.commit(self.paper, evidence)
        self.assertTrue(Path(receipt.path).is_file())
        receipt_text = Path(receipt.path).read_text(encoding="utf-8")
        self.assertNotIn("super-secret", receipt_text)
        self.assertNotIn("provider payload", receipt_text)
        self.assertEqual(json.loads(receipt_text)["stages"][1]["input_id"], "ATTACHMENT")
        self.assertTrue(
            FilesystemEvidenceVerifier(self.workspace).valid(
                self.paper, (_stage("render_page", page),)
            )
        )
        other = Paper("zotero", "scope-1", "other-record", "Other")
        self.assertFalse(
            FilesystemEvidenceVerifier(self.workspace).valid(
                other,
                (
                    StageEvidence(
                        "identify",
                        fingerprint=paper_identity_fingerprint(
                            other.source_id, other.scope_id, other.record_id
                        ),
                    ),
                    *evidence[1:],
                ),
            )
        )

        prior_page = Path(page.path).read_bytes()
        changed_source, changed_text, changed_sidecar, changed_page = self._core_outputs("new review")
        changed_staged = self.workspace / ".staging" / Path(changed_page.path).relative_to(self.workspace / "papers")
        changed_staged.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            self.receipts.commit(
                self.paper,
                self._complete_evidence(changed_source, changed_text, changed_sidecar, changed_page),
            )
        self.assertEqual(Path(page.path).read_bytes(), prior_page)

    def test_receipt_rejects_missing_staged_artifact_even_when_old_canonical_matches(self) -> None:
        source, text, sidecar, page = self._core_outputs()
        evidence = self._complete_evidence(source, text, sidecar, page)
        self.receipts.commit(self.paper, evidence)
        _, new_text, new_sidecar, new_page = self._core_outputs()
        staged_source = self.workspace / ".staging" / Path(source.path).relative_to(
            self.workspace / "papers"
        )
        staged_source.unlink()
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            self.receipts.commit(
                self.paper, self._complete_evidence(source, new_text, new_sidecar, new_page)
            )

    def test_receipt_rejects_wrong_record_artifact_contract(self) -> None:
        source, text, sidecar, page = self._core_outputs()
        evidence = list(self._complete_evidence(source, text, sidecar, page))
        evidence[2] = _stage(
            "extract_text",
            ArtifactRef("text", str(self.receipts.workspace_root / "papers" / "wrong" / "text.txt"), text.fingerprint),
        )
        with self.assertRaisesRegex(ValueError, "contract"):
            self.receipts.commit(self.paper, tuple(evidence))

    def test_receipt_rejects_wrong_stage_and_artifact_name(self) -> None:
        source, text, sidecar, page = self._core_outputs()
        evidence = self._complete_evidence(source, text, sidecar, page)
        wrong_stage = list(evidence)
        wrong_stage[2] = StageEvidence("render_page", wrong_stage[2].artifacts, wrong_stage[2].fingerprint)
        with self.assertRaisesRegex(ValueError, "stage"):
            self.receipts.commit(self.paper, tuple(wrong_stage))
        wrong_name = list(evidence)
        artifact = wrong_name[2].artifacts[0]
        wrong_name[2] = _stage(
            "extract_text", ArtifactRef("page", artifact.path, artifact.fingerprint)
        )
        with self.assertRaisesRegex(ValueError, "contract"):
            self.receipts.commit(self.paper, tuple(wrong_name))

    def test_receipt_seeds_verified_complete_resumed_canonical_artifacts(self) -> None:
        source, text, sidecar, page = self._core_outputs()
        evidence = self._complete_evidence(source, text, sidecar, page)
        self.receipts.commit(self.paper, evidence)
        receipt = self.receipts.commit(self.paper, evidence)
        self.assertTrue(Path(receipt.path).is_file())

    def test_rejects_symlinked_workspace_ancestors(self) -> None:
        target = self.workspace / "target"
        target.mkdir(parents=True)
        for name in ("workspace", "papers", ".staging"):
            root = self.workspace / f"symlink-{name}"
            link = root if name == "workspace" else root / name
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                FilesystemSidecar(link if name == "workspace" else root).write(
                    self.paper,
                    self._pdf_source(),
                    self._pdf_source(),
                    "provider",
                    "model",
                )

    def test_rejects_path_traversal_identifiers(self) -> None:
        unsafe = Paper("../outside", "scope", "record", "Title")
        text = self._pdf_source()
        with self.assertRaisesRegex(ValueError, "source_id"):
            self.sidecars.write(
                unsafe, text, text, "selected-provider", "selected-model"
            )


if __name__ == "__main__":
    unittest.main()
