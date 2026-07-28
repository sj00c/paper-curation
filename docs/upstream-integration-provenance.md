# Upstream integration provenance gate

**Status: BLOCKED — no repository-visible upstream comparison evidence is retained.**

## Audit result

This repository contains neither a retained compare response nor retained per-commit API
responses for an upstream comparison. It also contains no independently verifiable record
of an upstream base, head, changed-file inventory, patch, source blob, license, or data
grant.

Accordingly, the prior compare URL, commit inventory, file/contract matrix, response
coverage statements, patch-hash rows, and all associated counts have been removed. They
were assertions in this document, not evidence available elsewhere in the repository.
They must not be used to establish upstream provenance, file scope, source equivalence,
or permission to copy.

The local `.gitignore` whitelist permits this audit record and
`docs/audio-codec-provenance.md`; it does not establish anything about an upstream
`.gitignore` or any upstream file inventory.

## Classification

| Scope | classification | consequence |
|---|---|---|
| Any proposed upstream source, patch, or file list | `unverified` | Reject source adoption. |
| Source license, data provenance, and legal permission | `unverified` | Reject copying, corpus/data adoption, and derived-source claims. |
| Locally specified behavior | `independent-reimplementation-only` | A separately authored local implementation may be reviewed on its own merits; it is not evidence of upstream equivalence or derived from upstream source. |
| Missing, truncated, binary, malformed, or unavailable patch evidence | `unavailable` | Reject adoption; do not substitute an empty patch or a digest. |

This classification is fail-closed. It does not authorize fetching, merging, rebasing,
cherry-picking, copying upstream source, or treating a local path as a corresponding
upstream path.

## Patch-hunk digest procedure

A future evidence review may record a hunk digest only after retaining an auditable
repository-visible evidence record that identifies the immutable commit, file path, and
the exact API patch value used. The raw patch itself is not to be copied into this
repository merely to create a digest.

For an exact UTF-8 `files[].patch` value:

1. Parse hunk boundaries only at a line that is an actual unified-diff hunk header:
   `^@@ -<old-range> \+<new-range> @@(?: .*)?$`, where each range is a non-negative
   line number optionally followed by `,<count>`. The match must begin at the first byte
   of a line; `@@ ` found elsewhere is not a boundary.
2. Each hunk byte sequence starts with its matched header line and ends immediately
   before the next matched header line, or at the end of the patch. Do not create a
   digest for preamble bytes before the first header.
3. Hash each complete hunk byte sequence exactly as received, with SHA-256. Record the
   immutable commit identifier, path, literal matched header, positive byte length, and
   a lowercase, unpadded, 64-hex-character digest.
4. Reject the record as `patch-unparseable` when a present patch has no valid hunk
   header. Reject it as `patch-absent` when the API omits `patch`. In either case, record
   the state and reason, not `N/A`, an empty hash, a header hash, a padded hash, or a
   made-up hunk count.
5. Validate every recorded digest against the same exact patch value before treating it
   as evidence. Any retrieval failure, changed response, malformed header, zero-byte
   scope, digest-format failure, or mismatch is `unavailable` and blocks adoption.

There are no hunk digest records in this repository at present.

## Remaining evidence limitations

* No retained repository-visible artifact supports an upstream compare range or changed
  file inventory.
* No retained artifact supports attribution of a local file or contract to upstream.
* No source-license, data-provenance, or legal-review evidence is available.
* No patch digest can currently be verified because no qualifying evidence record exists.

Until those limitations are resolved through a separately authorized, auditable review,
upstream adoption remains blocked.
