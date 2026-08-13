"""Python entry point for the declarative local orchestrator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .application.migrate import execute_config_migration, load_config_migration
from .orchestration import Planner, StepExecutionError, SubprocessRunner


_COMMANDS = ("setup", "inspect", "doctor", "build", "update", "serve", "query", "validate", "repair", "deploy")
_TOPIC_COMMANDS = {"build", "update", "validate", "repair", "deploy"}
_OPTIONAL_TOPIC_COMMANDS = {"serve", "query"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="paper-curation")
    subparsers = parser.add_subparsers(dest="command", required=True)
    migrate = subparsers.add_parser("migrate", help="preview local config.json migration")
    migrate.add_argument("--config", default="config.json", metavar="PATH")
    migrate.add_argument("--execute", action="store_true",
                         help="back up and apply the displayed local migration")
    for command in _COMMANDS:
        subparser = subparsers.add_parser(command)
        if command in _TOPIC_COMMANDS:
            subparser.add_argument("--topic", required=True)
        elif command in _OPTIONAL_TOPIC_COMMANDS:
            subparser.add_argument("--topic")
        if command == "query":
            subparser.add_argument("--query", required=True)
        if command == "repair":
            subparser.add_argument("--execute", action="store_true",
                                   help="perform the destructive repair after previewing it")
        subparser.add_argument("--dry-run", action="store_true")
        subparser.add_argument("args", nargs=argparse.REMAINDER,
                               help="arguments passed unchanged to the underlying legacy script")
    legacy = subparsers.add_parser("legacy-run-full")
    legacy.add_argument("--topic")
    legacy.add_argument("--dry-run", action="store_true")
    legacy.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
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
    forwarded = tuple(args.args)
    if forwarded[:1] == ("--",):
        forwarded = forwarded[1:]
    plan = Planner().plan(
        args.command,
        topic=getattr(args, "topic", None),
        execute=getattr(args, "execute", False),
        query=getattr(args, "query", None),
        legacy_args=forwarded,
    )
    for index, step in enumerate(plan.topological_steps(), 1):
        print(f"{index}. {' '.join(step.argv)}")
    if args.dry_run:
        return 0
    try:
        SubprocessRunner(capture_output=False).run_plan(plan)
    except StepExecutionError as exc:
        receipt = exc.receipt
        print(f"[paper-curation] {receipt.detail or str(exc)}")
        return receipt.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
