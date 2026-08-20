"""Python entry point for the declarative local orchestrator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .application.curate import CurationFailure, CurationRequest, CurationSuccess
from .application.deploy import DeployRequest, DeployStatus
from .application.diagnostics import DoctorRequest, review_cost_class
from .application.serve import ServeSiteRequest
from .application.update import CoreUpdateRequest
from .application.migrate import execute_config_migration, load_config_migration
from .composition import (
    CompositionDependencies,
    OperationsDependencies,
    RuntimeComposition,
    RuntimeDependencies,
    compose_core_selection,
    compose_core_update,
    compose_operations,
    compose_runtime,
    require_installed_features,
)
from .config.loader import load_config
from .config.models import AppConfig
from .domain.retrieval import Query


_COMMANDS = ("setup", "inspect", "doctor", "build", "update", "serve", "query", "validate", "repair", "deploy")
_OPERATIONS_COMMANDS = {"setup", "inspect", "doctor", "build", "validate", "repair"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="paper-curation")
    subparsers = parser.add_subparsers(dest="command", required=True)
    migrate = subparsers.add_parser("migrate", help="preview local config.json migration")
    migrate.add_argument("--config", default="config.json", metavar="PATH")
    migrate.add_argument("--execute", action="store_true",
                         help="back up and apply the displayed local migration")
    for command in _COMMANDS:
        subparser = subparsers.add_parser(command)
        if command == "setup":
            subparser.add_argument("--input", required=True, metavar="PATH")
            subparser.add_argument("--config", default="config.json", metavar="PATH")
            subparser.add_argument("--execute", action="store_true")
            subparser.add_argument("--replace", action="store_true")
            continue
        if command in _OPERATIONS_COMMANDS:
            subparser.add_argument("--config", default="config.json", metavar="PATH")
            if command == "doctor":
                subparser.add_argument("--network", action="store_true")
            if command == "repair":
                subparser.add_argument("--execute", action="store_true")
            continue
        if command == "update":
            subparser.add_argument("--config", default="config.json", metavar="PATH")
            subparser.add_argument("--topic", required=True)
            subparser.add_argument("--paper", action="append", default=[], metavar="RECORD_ID")
            subparser.add_argument(
                "--attachment", action="append", default=[], metavar="RECORD_ID=ATTACHMENT"
            )
            subparser.add_argument("--dry-run", action="store_true")
        elif command == "query":
            subparser.add_argument("--config", required=True, metavar="PATH")
            subparser.add_argument("--topic", required=True)
            subparser.add_argument("--query", required=True)
            subparser.add_argument("--limit", type=int, default=10)
        elif command == "serve":
            subparser.add_argument("--config", required=True, metavar="PATH")
            subparser.add_argument("--host", default="127.0.0.1")
            subparser.add_argument("--port", type=int, default=8000)
            subparser.add_argument("--public-bind", action="store_true")
            subparser.add_argument("--dry-run", action="store_true")
        elif command == "deploy":
            subparser.add_argument("--config", required=True, metavar="PATH")
            subparser.add_argument("--execute", action="store_true")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    composition_dependencies: CompositionDependencies | None = None,
    operations_dependencies: OperationsDependencies | None = None,
    runtime_dependencies: RuntimeDependencies | None = None,
    environment: dict[str, str] | None = None,
) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "migrate":
        try:
            migration = load_config_migration(args.config)
            for path in migration.changed_paths:
                print(path)
            if args.execute and migration.has_changes:
                execute_config_migration(args.config, migration)
        except (OSError, ValueError) as exc:
            print(f"[paper-curation] migration failed: {exc}")
            return 1
        return 0
    if args.command == "update":
        return _core_update(args, composition_dependencies, environment)
    if args.command in _OPERATIONS_COMMANDS:
        return _operations(args, operations_dependencies, environment)
    if args.command in {"query", "serve", "deploy"}:
        return _runtime(args, runtime_dependencies, environment)
    raise AssertionError(f"unhandled command: {args.command}")


def _runtime(
    args: argparse.Namespace,
    dependencies: RuntimeDependencies | None,
    environment: dict[str, str] | None,
) -> int:
    try:
        config = load_config(args.config)
        topic = args.topic if args.command == "query" else None
        composition = compose_runtime(
            config,
            topic,
            command=args.command,
            environment=environment,
            dependencies=dependencies,
        )
        if args.command == "query":
            assert composition.query is not None
            hits = composition.query.search(args.topic, Query(args.query, limit=args.limit))
            for hit in hits:
                print(
                    f"rank={hit.rank} record={hit.slug} section={hit.section} "
                    f"chunk={hit.chunk_id}"
                )
            return 0
        if args.command == "serve":
            plan = composition.serve.plan(
                ServeSiteRequest(
                    site_root=composition.site,
                    host=args.host,
                    port=args.port,
                    allow_public_bind=args.public_bind,
                )
            )
            if args.dry_run:
                print(f"http://{plan.host}:{plan.port}")
                return 0
            assert composition.server is not None
            handle = composition.server.start(plan)
            print(handle.url)
            try:
                handle.wait()
            except KeyboardInterrupt:
                pass
            finally:
                handle.close()
            return 0
        return _deploy_runtime(args, config, composition)
    except (OSError, ValueError, TypeError, RuntimeError):
        print(f"[paper-curation] {args.command} failed")
        return 1


def _deploy_runtime(
    args: argparse.Namespace, config: AppConfig, composition: RuntimeComposition
) -> int:
    """Validate local deployment evidence before an explicit adapter invocation."""
    request = DeployRequest(
        workspace=composition.workspace,
        site=composition.site,
        config=composition.publication_config,
        publication_mode=config.publication.mode,
        base_url=config.publication.base_url,
        built=composition.site.is_dir() and (composition.site / "index.html").is_file(),
        validated=composition.validate().valid if composition.validate is not None else False,
        execute=args.execute,
    )
    if composition.deploy is None:
        print(DeployStatus.REFUSED)
        return 1
    if args.execute and not composition.cloudflare_api_token.strip():
        raise ValueError("CLOUDFLARE_API_TOKEN is required")
    result = composition.deploy.run(request)
    print(result.status)
    if result.status is DeployStatus.DEPLOYED and result.receipt is not None:
        print(result.receipt.base_url)
    return 0 if result.status in {DeployStatus.PREVIEW, DeployStatus.DEPLOYED} else 1


def _operations(
    args: argparse.Namespace,
    dependencies: OperationsDependencies | None,
    environment: dict[str, str] | None,
) -> int:
    try:
        input_path = args.input if args.command == "setup" else args.config
        config = load_config(input_path)
        if args.command not in {"inspect", "doctor"}:
            require_installed_features(config)
        operations = compose_operations(
            config, environment=environment, dependencies=dependencies
        )
        if args.command == "setup":
            plan = operations.setup.preview(config, args.config, replace=args.replace)
            if not args.execute:
                _print_setup_paths(plan.target_path, plan.workspace_directories, plan.backup_path)
                return 0
            result = operations.setup.execute(plan)
            _print_setup_paths(
                result.target_path, result.workspace_directories, result.backup_path
            )
            return 0
        if args.command == "inspect":
            result = operations.inspect.execute()
            _print_diagnostics(result.diagnostics)
            return 0
        if args.command == "doctor":
            result = operations.doctor.execute(DoctorRequest(network=args.network))
            _print_diagnostics(result.diagnostics)
            return result.exit_code
        if args.command == "build":
            result = operations.build()
            print(result.index_path)
            return 0
        if args.command == "validate":
            result = operations.validate()
            for issue in result.issues:
                print(f"{issue.path}: {issue.message}")
            return 0 if result.valid else 1
        result = operations.repair(execute=args.execute)
        for action in result.actions:
            print(f"{action.action}: {action.path}: {action.reason}")
        return 0
    except (OSError, ValueError, TypeError):
        print(f"[paper-curation] {args.command} failed")
        return 1


def _print_setup_paths(
    target_path: object, workspace_directories: Sequence[object], backup_path: object
) -> None:
    print(target_path)
    for directory in workspace_directories:
        print(directory)
    if backup_path is not None:
        print(backup_path)


def _print_diagnostics(diagnostics: Sequence[object]) -> None:
    for diagnostic in diagnostics:
        print(f"{diagnostic.code}: {diagnostic.message}")  # type: ignore[attr-defined]


def _core_update(
    args: argparse.Namespace,
    dependencies: CompositionDependencies | None,
    environment: dict[str, str] | None,
) -> int:
    try:
        config = load_config(args.config)
        if args.topic not in config.source.collections:
            raise ValueError("--topic must name a configured source.collections alias")
        selection_composition = compose_core_selection(
            config, environment=environment, dependencies=dependencies
        )
        scope_id = config.source.collections[args.topic]
        try:
            records = selection_composition.source.list_records("zotero", scope_id)
        except Exception:
            try:
                selection_composition.close()
            except Exception:
                pass
            raise
        else:
            selection_composition.close()
        available_ids = {record.record_id for record in records}
        selected_ids = tuple(args.paper) or tuple(record.record_id for record in records)
        if not selected_ids:
            raise ValueError("the selected collection contains no records")
        if len(selected_ids) != len(set(selected_ids)):
            raise ValueError("--paper values must be unique")
        unknown_ids = set(selected_ids) - available_ids
        if unknown_ids:
            raise ValueError("--paper must name records in the selected collection")
        attachments = _attachment_mapping(args.attachment, selected_ids)
        selections = tuple(
            CurationRequest(
                source_id="zotero",
                scope_id=scope_id,
                record_id=record_id,
                attachment_id=attachments.get(record_id, ""),
            )
            for record_id in selected_ids
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"[paper-curation] Core update configuration failed: {exc}")
        return 1

    if args.dry_run:
        print(f"provider={selection_composition.review_provider_id}")
        print(f"model={selection_composition.review_model}")
        print(f"cost={review_cost_class(selection_composition.review_provider_id)}")
        for selection in selections:
            print(
                f"selected source={selection.source_id} scope={selection.scope_id} "
                f"record={selection.record_id} attachment={selection.attachment_id or 'auto'}"
            )
        return 0

    try:
        composition = compose_core_update(
            config, environment=environment, dependencies=dependencies
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"[paper-curation] Core update configuration failed: {exc}")
        return 1
    try:
        result = composition.update.execute(CoreUpdateRequest(selections))
    except Exception:
        try:
            composition.close()
        except Exception:
            pass
        raise
    else:
        composition.close()
    for record in result.records:
        if isinstance(record.result, CurationSuccess):
            print(
                f"record={record.request.record_id} result=succeeded "
                f"page={record.result.page.path} receipt={record.result.receipt.path}"
            )
        else:
            failure = record.result
            assert isinstance(failure, CurationFailure)
            print(
                f"record={record.request.record_id} result=failed "
                f"stage={failure.stage} code={failure.code}"
            )
    return result.exit_code


def _attachment_mapping(values: Sequence[str], selected_ids: Sequence[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for value in values:
        record_id, separator, attachment_id = value.partition("=")
        if not separator or not record_id or not attachment_id:
            raise ValueError("--attachment must use RECORD_ID=ATTACHMENT")
        if record_id in mapping:
            raise ValueError("--attachment record IDs must be unique")
        mapping[record_id] = attachment_id
    unknown = set(mapping) - set(selected_ids)
    if unknown:
        raise ValueError("--attachment may only name selected --paper records")
    return mapping


if __name__ == "__main__":
    raise SystemExit(main())
