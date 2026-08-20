"""Focused contract tests for the official Core composition and CLI route."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from paper_curation.capabilities import Capabilities
from paper_curation.application.curate import CurationFailure, CurationRequest, CurationStage
from paper_curation.application.update import CoreUpdateRecord, CoreUpdateResult
from paper_curation.cli import main
from paper_curation.composition import CompositionDependencies, compose_core_update
from paper_curation.config.models import AppConfig
from paper_curation.domain.papers import ArtifactRef, Paper, StageEvidence
from paper_curation.integrations.persistence.filesystem import FilesystemReceipt, FilesystemStagedReview


def _config(tmp_path: Path, provider: str = "local-model") -> AppConfig:
    source = tmp_path / "zotero.sqlite"
    source.touch()
    review = {"provider": provider, "model": "configured-model"}
    if provider == "local-model":
        review["local_endpoint"] = "http://127.0.0.1:8080"
    return AppConfig.from_mapping({
        "workspace": {"root": str(tmp_path / "workspace")},
        "source": {"provider": "zotero", "transport": "local-sqlite", "sqlite_path": str(source), "collections": {"topic": "COLLECTION"}},
        "core": {"review": review},
        "features": {},
    })


@dataclass
class _Source:
    papers: tuple[Paper, ...]

    def list_records(self, source_id: str, scope_id: str) -> tuple[Paper, ...]:
        assert (source_id, scope_id) == ("zotero", "COLLECTION")
        return self.papers

    def list_attachments(self, paper: Paper) -> tuple[object, ...]:
        return ()


def _dependencies(source: _Source, calls: list[str]) -> CompositionDependencies:
    capabilities = Capabilities(True, True, {}, False)
    return CompositionDependencies(
        detect_capabilities=lambda *args, **kwargs: capabilities,
        zotero_source=lambda path: source,
        zotero_attachments=lambda *args: object(),
        zotero_storage_source=lambda key: calls.append("storage-source") or source,
        zotero_storage_attachments=lambda *args: calls.append("storage-attachments") or object(),
        text_extractor=lambda path: object(),
        claude_review=lambda *args, **kwargs: calls.append("claude") or object(),
        anthropic_review=lambda *args, **kwargs: calls.append("anthropic") or object(),
        local_review=lambda *args, **kwargs: calls.append("local") or object(),
        anthropic_client=lambda key: calls.append("client") or object(),
        sidecar=lambda path: object(),
        page=lambda path: object(),
        receipt=lambda path: object(),
        verifier=lambda path: object(),
        staged_review=lambda path, provider: provider,
    )


def test_composition_constructs_only_the_selected_provider(tmp_path: Path) -> None:
    calls: list[str] = []
    source = _Source(())

    composition = compose_core_update(
        _config(tmp_path, "anthropic-api"),
        environment={"ANTHROPIC_API_KEY": "environment-secret"},
        dependencies=_dependencies(source, calls),
    )

    assert composition.review_provider_id == "anthropic-api"
    assert calls == ["client", "anthropic"]


def test_composition_uses_only_selected_storage_transport(tmp_path: Path) -> None:
    calls: list[str] = []
    source = _Source(())
    config = AppConfig.from_mapping({
        "workspace": {"root": str(tmp_path / "workspace")},
        "source": {
            "provider": "zotero",
            "transport": "zotero-storage",
            "collections": {"topic": "COLLECTION"},
        },
        "core": {
            "review": {
                "provider": "local-model",
                "model": "configured-model",
                "local_endpoint": "http://127.0.0.1:8080",
            }
        },
        "features": {},
        "credentials": {"zotero_api_key": "configured-secret"},
    })

    composition = compose_core_update(
        config,
        dependencies=_dependencies(source, calls),
    )

    assert composition.source is source
    assert calls == ["storage-source", "storage-attachments", "local"]


def test_composition_rejects_enabled_uninstalled_enhancement(tmp_path: Path) -> None:
    config = AppConfig.from_mapping({
        "workspace": {"root": str(tmp_path / "workspace")},
        "source": {
            "provider": "zotero",
            "transport": "local-sqlite",
            "sqlite_path": str((tmp_path / "zotero.sqlite")),
            "collections": {"topic": "COLLECTION"},
        },
        "core": {
            "review": {
                "provider": "local-model",
                "model": "configured-model",
                "local_endpoint": "http://127.0.0.1:8080",
            }
        },
        "features": {"timeline": {"enabled": True, "provider": "google"}},
        "credentials": {"google_api_key": "configured"},
    })
    Path(config.source.sqlite_path).touch()

    with __import__("pytest").raises(ValueError, match="not installed"):
        compose_core_update(
            config,
            dependencies=_dependencies(_Source(()), []),
        )


def test_composition_closes_acquired_resources_when_construction_fails(
    tmp_path: Path,
) -> None:
    calls: list[str] = []

    class Source(_Source):
        closed = False

        def close(self) -> None:
            self.closed = True
            raise RuntimeError("source close failed")

    class Attachments:
        closed = False

        def close(self) -> None:
            self.closed = True
            raise RuntimeError("attachment close failed")

    source = Source(())
    attachments = Attachments()
    dependencies = replace(
        _dependencies(source, calls),
        zotero_attachments=lambda *args: attachments,
        local_review=lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("provider construction failed")
        ),
    )
    with __import__("pytest").raises(RuntimeError, match="construction failed"):
        compose_core_update(_config(tmp_path), dependencies=dependencies)
    assert source.closed
    assert attachments.closed


def test_anthropic_client_is_closed_when_adapter_construction_fails(
    tmp_path: Path,
) -> None:
    class Client:
        closed = False

        def close(self) -> None:
            self.closed = True
            raise RuntimeError("client close failed")

    client = Client()
    dependencies = replace(
        _dependencies(_Source(()), []),
        anthropic_client=lambda key: client,
        anthropic_review=lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("adapter construction failed")
        ),
    )
    with __import__("pytest").raises(
        RuntimeError, match="adapter construction failed"
    ):
        compose_core_update(
            _config(tmp_path, "anthropic-api"),
            environment={"ANTHROPIC_API_KEY": "configured"},
            dependencies=dependencies,
        )
    assert client.closed


def test_cli_dry_run_selects_configured_scope_without_provider_call(tmp_path: Path, capsys) -> None:
    calls: list[str] = []
    papers = (
        Paper("zotero", "COLLECTION", "FIRST", "First"),
        Paper("zotero", "COLLECTION", "SECOND", "Second"),
    )
    config_path = tmp_path / "config.json"
    config_path.write_text(__import__("json").dumps({
        "workspace": {"root": str(tmp_path / "workspace")},
        "source": {"provider": "zotero", "transport": "local-sqlite", "sqlite_path": str(tmp_path / "zotero.sqlite"), "collections": {"topic": "COLLECTION"}},
        "core": {"review": {"provider": "local-model", "model": "configured-model", "local_endpoint": "http://127.0.0.1:8080"}},
        "features": {},
    }), encoding="utf-8")
    (tmp_path / "zotero.sqlite").touch()

    assert main(["update", "--config", str(config_path), "--topic", "topic", "--dry-run"], composition_dependencies=_dependencies(_Source(papers), calls)) == 0

    output = capsys.readouterr().out
    assert "record=FIRST" in output and "record=SECOND" in output
    assert "provider=local-model" in output
    assert "model=configured-model" in output
    assert "secret" not in output
    assert calls == []


def test_cli_dry_run_rejects_record_outside_selected_scope(tmp_path: Path, capsys) -> None:
    calls: list[str] = []
    config = _config(tmp_path)
    config_path = tmp_path / "config.json"
    config_path.write_text(
        __import__("json").dumps({
            "workspace": {"root": config.workspace.root},
            "source": {
                "provider": "zotero",
                "transport": "local-sqlite",
                "sqlite_path": config.source.sqlite_path,
                "collections": {"topic": "COLLECTION"},
            },
            "core": {
                "review": {
                    "provider": "local-model",
                    "model": "configured-model",
                    "local_endpoint": "http://127.0.0.1:8080",
                }
            },
            "features": {},
        }),
        encoding="utf-8",
    )
    code = main(
        [
            "update",
            "--config",
            str(config_path),
            "--topic",
            "topic",
            "--paper",
            "MISSING",
            "--dry-run",
        ],
        composition_dependencies=_dependencies(
            _Source((Paper("zotero", "COLLECTION", "FIRST", "First"),)),
            calls,
        ),
    )
    assert code == 1
    assert "failed" in capsys.readouterr().out
    assert calls == []


def test_cli_applies_attachment_mapping_to_selected_record(tmp_path: Path, capsys) -> None:
    calls: list[str] = []
    config = _config(tmp_path)
    config_path = tmp_path / "config.json"
    config_path.write_text(__import__("json").dumps({
        "workspace": {"root": config.workspace.root},
        "source": {"provider": "zotero", "transport": "local-sqlite", "sqlite_path": config.source.sqlite_path, "collections": {"topic": "COLLECTION"}},
        "core": {"review": {"provider": "local-model", "model": "configured-model", "local_endpoint": "http://127.0.0.1:8080"}},
        "features": {},
    }), encoding="utf-8")

    assert main(["update", "--config", str(config_path), "--topic", "topic", "--paper", "FIRST", "--attachment", "FIRST=PDF", "--dry-run"], composition_dependencies=_dependencies(_Source((Paper("zotero", "COLLECTION", "FIRST", "First"),)), calls)) == 0

    assert "record=FIRST attachment=PDF" in capsys.readouterr().out


def test_staged_review_is_verified_and_never_removes_provider_output(tmp_path: Path) -> None:
    paper = Paper("zotero", "COLLECTION", "RECORD", "Title")
    import hashlib
    workspace = tmp_path / "workspace"
    relative = Path(
        hashlib.sha256(paper.source_id.encode()).hexdigest(),
        hashlib.sha256(paper.scope_id.encode()).hexdigest(),
        hashlib.sha256(paper.record_id.encode()).hexdigest(),
    )
    text_path = workspace / ".staging" / relative / "text.txt"
    text_path.parent.mkdir(parents=True)
    text_path.write_text("text", encoding="utf-8")
    logical_text = workspace / "papers" / relative / "text.txt"
    generated = workspace / ".review-provider" / "provider.md"
    generated.parent.mkdir(parents=True)
    generated.write_text("# Review\n", encoding="utf-8")
    review = ArtifactRef("review.md", str(generated), hashlib.sha256(generated.read_bytes()).hexdigest())

    class Provider:
        def write(self, received_paper, received_text):
            return review

    staged = FilesystemStagedReview(workspace, Provider()).write(
        paper,
        ArtifactRef(
            "text",
            str(logical_text),
            hashlib.sha256(text_path.read_bytes()).hexdigest(),
        ),
    )

    assert staged.path.endswith("/review.md")
    assert generated.exists()
    assert (
        workspace / ".staging" / Path(staged.path).relative_to(workspace / "papers")
    ).is_file()
    with __import__("pytest").raises(ValueError, match="complete Core evidence"):
        FilesystemReceipt(tmp_path / "workspace").commit(
            paper, (StageEvidence("generate_review", (staged,), staged.fingerprint, "local-model"),)
        )


def test_partial_core_result_has_a_nonzero_aggregate_exit_code() -> None:
    request = CurationRequest("zotero", "COLLECTION", "RECORD")
    result = CoreUpdateResult((
        CoreUpdateRecord(request, CurationFailure(CurationStage.GENERATE_REVIEW, "provider_failed")),
    ))

    assert result.exit_code == 1
