# Paper Curation

An installable local tool for reviewing, rendering, and searching a Zotero corpus. The official entry point is the `paper-curation` CLI provided by the Python package. Configuration migration preserves existing local data paths and public URLs.

## Installation and daily use

```bash
git clone https://github.com/sj00c/paper-curation.git
cd paper-curation
conda env create -f environment.yml
conda activate py312
paper-curation setup
paper-curation inspect
paper-curation doctor --network
paper-curation update --topic <topic>
paper-curation serve --topic <topic>
```

`environment.yml` is not a Docker configuration. It creates a local Conda
environment containing Python 3.12, Java 17, native scientific packages, and
the `paper-curation` CLI. Zotero Desktop, Claude Code authentication, PDFs,
and generated output remain on the user's computer.

Update an existing checkout and its environment with:

```bash
git pull --ff-only origin master
conda env update -f environment.yml --prune
conda activate py312
```

`setup` creates or updates only local `config.json`. `inspect` and default `doctor` are read-only; only `doctor --network` checks external connections. Use `build --topic <topic>` for a full rebuild and `update --topic <topic>` for incremental collection and generation. Search, validation, repair, and public deployment are explicit:

```bash
paper-curation query --topic <topic> --query "research question"
paper-curation validate --topic <topic>
paper-curation repair --topic <topic>          # preview
paper-curation repair --topic <topic> --execute # writes changes
paper-curation deploy --topic <topic>
```

Deployment is a separate public operation, never part of `build` or `update`. Local generation does not publish or notify by default.

## Configuration and security

Cross-category insights read provider order from
`EXTRACT_INSIGHTS_CC_BACKENDS`. The first configured provider is selected; the
list is **not a fallback chain**, and a failure never substitutes another
provider.

`config.json`, `.env`, PDF caches, databases, and generated corpus data are installer-local state and are untracked. Missing optional integration credentials disable only their dependent feature. Browser BYOK keys live only in memory for one page load, never in Web Storage or URLs. Owner keys are never embedded in static output.

Preview a schema change before applying it:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

Migration preserves known legacy local-data paths and public URL values, and reports values that cannot be represented in the new schema.

## Compatibility

`pipeline/run_full.py` remains a compatibility wrapper for existing automation. New documentation and automation use the official CLI. Use the legacy call only for troubleshooting or advanced legacy flags:

```bash
python pipeline/run_full.py --topic <topic> --mode curate --source zotero
```

See [operations](docs/operations.md), [architecture](docs/architecture.md), and [CONTRIBUTING.md](CONTRIBUTING.md).
