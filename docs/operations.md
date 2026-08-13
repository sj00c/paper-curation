# Operations

## Official CLI

Operate an installed checkout with an explicit topic where required:

```bash
paper-curation setup
paper-curation inspect
paper-curation doctor --network
paper-curation build --topic <topic>
paper-curation update --topic <topic>
paper-curation serve --topic <topic>
paper-curation query --topic <topic> --query "research question"
paper-curation validate --topic <topic>
paper-curation repair --topic <topic>
paper-curation repair --topic <topic> --execute
paper-curation deploy --topic <topic>
```

`setup` configures locally and does not build, publish, or notify. `inspect` and default `doctor` do not write; `doctor --network` checks configured services. `build` is the full rebuild; `update` is the incremental workflow. `query` reads existing retrieval data. Always review the repair preview before `--execute`. `deploy` is the sole publication command and requires an explicitly configured public destination.

## Local-first state and migration

Keep credentials and installation-specific data in untracked local configuration. Do not copy a local cache, database, corpus, URL, or deployment destination into shared documentation. Preview configuration migration, then apply it only after review:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

The migration preserves recognized legacy local paths and public URLs, and reports unsupported values. It never publishes content.

## Compatibility and troubleshooting

The following is intentionally legacy-only. `pipeline/run_full.py` remains a compatibility wrapper for existing integrations and advanced flags; it is not the recommended entry point:

```bash
python pipeline/run_full.py --topic <topic> --mode curate --source zotero --dry-run
```

Use it only to reproduce or diagnose an existing legacy invocation. Convert new automation to the official CLI.

## Publication boundary

Inspect generated output and target configuration before `paper-curation deploy`. Local builds and updates never implicitly deploy, send notifications, repair remote data, or synchronize a remote bibliography database. Browser keys are ephemeral page-memory values; operator keys must not enter generated pages.
