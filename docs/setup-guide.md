# Paper Curation Setup Guide

## Install the official CLI

Install Miniforge or another Conda distribution, then create the repository's
local workstation environment:

```bash
git clone https://github.com/sj00c/paper-curation.git
cd paper-curation
conda env create -f environment.yml
conda activate py312
paper-curation setup
paper-curation inspect
paper-curation doctor --network
```

The environment file is a Conda YAML file, not Docker Compose. It installs
Python 3.12, Java 17, native clustering dependencies, remaining pip
dependencies, and this checkout in editable mode. Each user continues to use
their host Zotero installation, Claude Code login, local PDFs, and browser.

To update:

```bash
git pull --ff-only origin master
conda env update -f environment.yml --prune
conda activate py312
```

`setup` creates or updates untracked local configuration. It is configuration-only: it does not build, publish, notify, or alter a remote corpus. `inspect` is read-only; use `doctor --network` only when checking configured external services.

## Local configuration and security

Keep `config.json`, `.env`, credential files, PDF caches, databases, and generated corpus data local and untracked. Add only the integrations required by this installation. Missing optional credentials disable their feature rather than selecting another provider. Do not place credentials in documentation, static output, browser storage, or URLs.

Existing installations can evolve configuration safely:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

Review the preview before execution. The migration preserves recognized old local data paths and public URL values, and reports values it cannot migrate.

## First operation

```bash
paper-curation update --topic <topic>
paper-curation validate --topic <topic>
paper-curation serve --topic <topic>
```

Use `build --topic <topic>` for a full rebuild. `query --topic <topic> --query "…"` reads the existing index. `repair --topic <topic>` previews recovery; add `--execute` only after review. `deploy --topic <topic>` is an explicit public operation and never runs automatically after build or update.

## Legacy troubleshooting

`pipeline/run_full.py` remains a compatibility wrapper for existing automation, so it has not been removed. New workflows must use `paper-curation`; invoke the wrapper only to reproduce an advanced legacy command:

```bash
python pipeline/run_full.py --topic <topic> --mode curate --source zotero
```
