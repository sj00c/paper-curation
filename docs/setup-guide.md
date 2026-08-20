# Paper Curation Setup Guide

## Install the official CLI

Install a Conda distribution, then create the local workstation environment:

```bash
git clone <fork-url>
cd paper-curation
conda env create -f environment.yml
conda activate py312
```

This is a host installation, not Docker. Zotero Desktop, authentication state, local PDFs, and all generated state remain local.

## Create configuration from a strict input

Use `config.example.json` as a schema-shaped reference, then create an untracked strict input configuration for this installation. Its keys, values, and cross-field requirements are validated; unknown keys and invalid provider, transport, or publication combinations are rejected.

Preview setup first:

```bash
paper-curation setup --input strict-input-config.json --config config.json
paper-curation setup --input strict-input-config.json --config config.json --execute
```

The preview does not write. The execute command writes the target configuration and its workspace directories. Add `--replace` only when deliberately replacing an existing target configuration.

For a prior `config.json`, preview migration before applying it:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

Migration preserves recognized old local-data paths and public URLs and reports unsupported values.

## Select local Zotero access and Core review

Set `source.provider` to Zotero and choose one explicit transport:

- `local-sqlite` reads the local Zotero SQLite library and requires `source.sqlite_path`.
- `zotero-storage` uses Zotero Storage and requires an empty `source.sqlite_path`.

Map each local topic alias in `source.collections`; commands use that alias as `--topic`. The configured workspace owns `papers/`, `.cache/`, `.staging/`, and `site/`. They are local, untracked state; do not add corpus data or generated output to the repository.

Core requires exactly one selected `core.review.provider` and an explicit `core.review.model`. A failure is reported for that pair and never causes a fallback. An enhancement with `enabled: true` is rejected unless its selected adapter is installed. Credentials merely permit a selected provider to run; they never enable or select one.

## First local run

Check local configuration, then build, validate, and serve:

```bash
paper-curation inspect --config config.json
paper-curation doctor --config config.json
paper-curation build --config config.json
paper-curation validate --config config.json
paper-curation serve --config config.json
```

`inspect` and default `doctor` are read-only. Use `paper-curation doctor --config config.json --network` only to check configured external services. `serve` is local by default; use its `--dry-run`, `--host`, `--port`, or `--public-bind` options only when those explicit behaviors are needed.

Use update selection and preview before writing Core output. A successful Core run has a complete review, rendered page, and receipt; partial output does not count as success:

```bash
paper-curation update --config config.json --topic <topic-alias> --dry-run
paper-curation update --config config.json --topic <topic-alias> --paper <record-id> --attachment <record-id>=<attachment-id>
```

`query` is local lexical search over completed, verified Core output:

```bash
paper-curation query --config config.json --topic <topic-alias> --query "research question" --limit 10
```

Repair also previews before it writes:

```bash
paper-curation repair --config config.json
paper-curation repair --config config.json --execute
```

## Public deployment and compatibility

Cloudflare publication is explicit and separate from building or updating:

```bash
paper-curation deploy --config config.json
paper-curation deploy --config config.json --execute
```

The preview verifies the configured public action; execution requires explicit public Cloudflare configuration and local authentication. No build-time deployment occurs.

`pipeline/run_full.py` is only a filename-compatibility wrapper for `paper-curation`; it accepts official CLI arguments and owns no historical modes.
