# Security Policy

## Supported branch

Security fixes target the current default branch. Generated corpus data and local configuration are not part of the public source distribution.

## Reporting

Report suspected credential exposure or a vulnerability privately through the repository host's security-advisory channel. Do not open a public issue containing keys, tokens, private paper text, or personal data.

## Credential handling

- `config.json`, `.env`, local key caches, SQLite databases, generated papers, and topic output are gitignored.
- Generated HTML must never contain owner API keys or notification recipients.
- Public deployment requires an explicit publication destination and scans the actual upload surface before invoking Wrangler.
- `scripts/scan-secrets.py` scans Git objects rather than only textual diffs, including binary blobs, merge results, tag messages, whitespace-split values, and supported base64 encodings.
- Zotero, Anthropic, OpenAI, Google, GitHub, AWS, and OAuth credential patterns are blocked by the scanner.

Install the optional pre-push hook with:

```bash
bash scripts/install-hooks.sh
```

Run checks manually with:

```bash
python scripts/scan-secrets.py --all       # current snapshot
python scripts/scan-secrets.py --history   # all reachable history
```

A clean current snapshot does not prove old Git history is clean. Revoke and rotate any credential that was ever committed; deleting the current file is insufficient.

## Runtime boundaries

- TLS certificate and hostname verification remain enabled. Private CAs use `PAPER_CURATION_CA_BUNDLE`.
- Setup is configuration-only unless `--run-first` is explicit.
- Local curation never deploys, sends completion email, or synchronizes a remote bibliography database implicitly.
- Public deploy, email notification, destructive Zotero repair, and remote DB synchronization require separate positive choices.
- Browser answer generation uses reader-provided keys or same-origin server routes; build-time owner credentials are not embedded in pages.
- Browser BYOK credentials remain in memory for one page load; they are not persisted in Web Storage or placed in Google API URLs.
- The public embedding proxy accepts same-origin requests only and is protected by a Cloudflare rate-limit binding.
- Audio Overview is download-only; the public Worker does not expose an anonymous email relay.

## Verification

```bash
python -m unittest discover -s pipeline/tests -p 'test_*.py'
npm run test:npx-cli
python scripts/check-eol.py
python scripts/scan-secrets.py --all
```
