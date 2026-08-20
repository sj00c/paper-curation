# Operations

## Official CLI and state boundary

The installable `paper-curation` CLI is the operational interface. The configured workspace owns `papers/`, `.cache/`, `.staging/`, and `site/`; these paths, local databases, caches, credentials, corpus data, and generated output are untracked installation state.

Use only a strict configuration. Unsupported fields and invalid cross-field combinations are rejected. Create it from an explicit input with preview first:

```bash
paper-curation setup --input strict-input-config.json --config config.json
paper-curation setup --input strict-input-config.json --config config.json --execute
```

Use `--replace` only when intentionally overwriting the target configuration. For legacy local configuration, preview then execute migration:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

## Source, provider, and capability policy

`source.transport` is explicit: `local-sqlite` requires `source.sqlite_path` for a local Zotero SQLite library, while `zotero-storage` uses Zotero Storage with no SQLite path. `--topic` is a configured `source.collections` alias.

Core runs with one mandatory, explicitly selected review provider and model. Their failure fails Core; no provider or model fallback is attempted. An enabled enhancement must have an installed selected adapter. Credentials do not select a provider or automatically enable any enhancement.

## Build and serve local output

Inspect and diagnose before normal local publication, then build, validate, and serve:

```bash
paper-curation inspect --config config.json
paper-curation doctor --config config.json
paper-curation build --config config.json
paper-curation validate --config config.json
paper-curation serve --config config.json
```

`inspect` and default `doctor` are read-only. `paper-curation doctor --config config.json --network` checks configured external services. `serve` accepts `--host`, `--port`, `--public-bind`, and `--dry-run`; it does not publish externally.

## Update, query, and repair

Review an update plan before Core writes. Omit `--paper` to select the configured collection; repeat it to select records. Each `--attachment RECORD_ID=ATTACHMENT` must name a selected record and overrides automatic attachment selection.

```bash
paper-curation update --config config.json --topic <topic-alias> --dry-run
paper-curation update --config config.json --topic <topic-alias> --paper <record-id> --attachment <record-id>=<attachment-id>
paper-curation query --config config.json --topic <topic-alias> --query "research question" --limit 10
paper-curation repair --config config.json
paper-curation repair --config config.json --execute
```

`query` is provider-free lexical search over completed, verified Core artifacts. A successful Core record includes its complete review, rendered page, and receipt; partial output is not successful. `repair` previews actions by default and writes only with `--execute`.

## Explicit public Cloudflare deployment

Build and update never deploy. Configure public publication for Cloudflare, inspect the local site and validation result, then preview and explicitly execute deployment:

```bash
paper-curation deploy --config config.json
paper-curation deploy --config config.json --execute
```

Deployment requires configured public Cloudflare publication and required local authentication; do not put credentials, deployment destinations, or generated corpus data in repository material.

## Compatibility troubleshooting

`pipeline/run_full.py` is a filename-compatibility wrapper only. It accepts official CLI arguments, owns no business logic, and is not a primary operational path.
