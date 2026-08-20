# Paper Curation

Paper Curation is an installable local tool that reviews papers in Zotero collections, renders static pages, and searches them. Its official interface is the `paper-curation` CLI supplied by the Python package. After a one-time upstream intake, this fork is the current product source of truth; it does not continuously synchronize with upstream.

## Installation and strict configuration

```bash
git clone <fork-url>
cd paper-curation
conda env create -f environment.yml
conda activate py312
```

`environment.yml` defines a local Conda environment, not Docker. Zotero, authentication state, PDFs, configuration, caches, and generated output stay on the workstation.

The configuration input must satisfy a strict JSON schema. Unsupported keys, wrong types, and contradictory transport or provider settings are rejected. Start from `config.example.json`, but keep installation-specific values in a separate untracked input file. Preview the result and review it before creating configuration and the workspace:

```bash
paper-curation setup --input strict-input-config.json --config config.json
paper-curation setup --input strict-input-config.json --config config.json --execute
```

Add `--replace` to the execute command only when replacing an existing target configuration. For an existing legacy configuration, preview migration before applying it:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

Migration preserves recognized legacy local-data paths and public URLs, and reports values it cannot represent.

## Local workflow

The workspace-root paths `papers/`, `.cache/`, `.staging/`, and `site/` are installation-local state. Neither a corpus nor generated output is tracked in the repository.

Set `source.transport` explicitly. `local-sqlite` requires a local Zotero SQLite library path; `zotero-storage` uses Zotero Storage and has no SQLite path. Pass an alias from `source.collections` to `--topic`.

Core review requires exactly one explicit `core.review.provider` and `core.review.model`. If that pair fails, Core fails; it never falls back to another provider or model. An enabled enhancement is accepted only when an installed adapter exists. Credential presence alone never enables an enhancement or selects a provider.

The normal sequence is:

```bash
paper-curation inspect --config config.json
paper-curation doctor --config config.json
paper-curation build --config config.json
paper-curation validate --config config.json
paper-curation serve --config config.json
```

`inspect` and default `doctor` are read-only; only `doctor --config config.json --network` checks configured external connections. After `build`, pass `validate` before serving the local site. `serve --config config.json --dry-run`, `--host`, `--port`, and `--public-bind` explicitly control its plan and binding.

## Review, search, repair, and public deployment

`update` runs Core for the configured collection. A successful Core result includes a complete review, page, and receipt; a partial result is not successful. Review selection and cost first. Repeat `--paper` to select records; `--attachment RECORD_ID=ATTACHMENT` overrides automatic PDF selection for a selected paper.

```bash
paper-curation update --config config.json --topic <topic-alias> --dry-run
paper-curation update --config config.json --topic <topic-alias> --paper <record-id> --attachment <record-id>=<attachment-id>
paper-curation query --config config.json --topic <topic-alias> --query "research question" --limit 10
paper-curation repair --config config.json
paper-curation repair --config config.json --execute
```

`query` is provider-free local lexical search over completed, verified Core output. `repair` previews recovery actions by default and writes only with `--execute`.

Public deployment is a separate Cloudflare action only when configured explicitly. `build` and `update` never deploy:

```bash
paper-curation deploy --config config.json
paper-curation deploy --config config.json --execute
```

The first command previews deployment. Execution requires public Cloudflare configuration and required local authentication. Keep authentication and deployment destinations out of documentation, static output, and the repository.

## Compatibility

`pipeline/run_full.py` is only a thin filename-compatibility wrapper and accepts the same arguments as the official CLI. It owns no business logic or historical modes/flags.

See the [PRD](docs/PRD.md) for product requirements, [SPEC](docs/SPEC.md) for the normative engineering contract, and [HANDOFF](docs/HANDOFF.md) for current session state. Operational detail remains in [operations](docs/operations.md), explanatory structure in [architecture](docs/architecture.md), and onboarding in the [setup guide](docs/setup-guide.md).
