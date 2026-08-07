# Branch ledger — `work/oauth-on-latest`

Every commit on this branch (`upstream/master..HEAD`), classified by which stated
purpose it serves. The point is that when this is later PR'd upstream, the selection is
obvious without re-reading three dozen commit messages.

This table lists every in-range commit **except the single commit that writes the
current revision of this file** — its own hash cannot exist before it is committed.
Everything already reachable when the file is edited is listed. Regenerate the range with
`git log --oneline upstream/master..HEAD` and confirm only the tip ledger-commit is
absent.

The three stated purposes were:

1. **Pull the latest upstream release**
2. **Apply OAuth** (Claude Code subscription auth instead of a Console API key)
3. **Generalize the ai4s-hardcoded pipeline** so it uses the user's own Zotero
   folder/schema structure

A fourth category, **detour**, covers work that is defensible but was not asked for —
mostly cleanup of mistakes made while doing the above. It is listed honestly rather
than folded into the purposes.

Regenerate the commit list with:

```bash
git log --reverse --format='%h %s' upstream/master..HEAD
```

## Purpose 1 — upstream sync

| Commit | Summary | Why |
|---|---|---|
| `d3da625` | Merge `upstream/master` into `work/oauth-on-latest` | Brings v0.10.0 (`12f6feb`) plus the two commits master had moved past it. One README conflict resolved by keeping this fork's npx CLI form and upstream's new `/api/citedby-answer` route, both verified true in the merged tree. |

Verify: `git rev-list --count HEAD..upstream/master` is `0`, and
`git merge-base --is-ancestor v0.10.0 HEAD` succeeds.

## Purpose 2 — OAuth

| Commit | Summary | Why |
|---|---|---|
| `82f80f6` | Add Claude Code OAuth pipeline support | The `anthropic_auth` module: auth-mode resolution, saved-login/env token detection, and a `claude -p` bridge exposing a small `anthropic.Anthropic`-shaped client. |
| `9166844` | Route upstream's new Claude callsites through the OAuth-aware client | Upstream had added Claude calls that constructed the SDK directly, which bypasses OAuth. |

Verify: `anthropic_auth.auth_status()` returns `mode=oauth ready=True`, and every Claude
callsite goes through `create_anthropic_client()` — no *pipeline* module imports the
Anthropic SDK directly except `anthropic_auth` itself. (Two tests,
`pipeline/tests/test_relevance.py` and `test_verify.py`, construct a real SDK client for
an optional live-API smoke call gated on `ANTHROPIC_API_KEY`; both are skipped without a
key.)

## Purpose 3 — generalize beyond ai4s

Split into two waves. The first removed hardcoding; the second made the pipeline consume
the user's own Zotero structure.

### 3a — remove the ai4s hardcoding

| Commit | Summary | Why |
|---|---|---|
| `e64a56b` | Stop assuming every install is ai4s | `--topic` defaulted to `"ai4s"` in 12 entrypoints, so omitting it silently targeted a topic the install may not have. `resolve_topic()` now uses the single configured topic and refuses when ambiguous. Also fixed `review_to_html` falling back to the ai4s theme, which gave non-ai4s installs red pages and a 404 "back" link. |
| `96a3feb` | Catch the theme fallback I missed in compare_papers | Same bug, second copy. Listed here because it completes 3a, though it exists because the first pass was incomplete. |

### 3b — use the user's Zotero folder tree

| Commit | Summary | Why |
|---|---|---|
| `c4791cf` | Read the user's own Zotero hierarchy as a classification source | `lib/zotero_tree.py`: top-level collection is the topic, its children are the categories, emitted in the same `_new_classification.json` shape the HDBSCAN path writes. |
| `6fcb3b9` | Make the unclassified bin selectable instead of always dropped | Always skipping the bin silently dropped 439 of 3,273 ai4s papers. `--unclassified skip|include`. |
| `164c1ba` | Wire the Zotero source into classify_papers behind an opt-in flag | `--classify-source hdbscan|zotero`, default unchanged, flag threaded through `run_full` → `run_update_force` → `classify_papers`. |
| `7f8c097` | Read the collection tree from zotero.sqlite instead of the Web API | The data is already on disk. One query (0.1s) replaces paging 15,399 items over the network, needs no API key, and excludes trashed items. Web API stays as the fallback. |
| `642179e` | Document the Zotero classification source and ledger the branch | The docs half of Purpose 3 (README/README.en/AGENTS/CLAUDE/operations describe `--classify-source`/`--unclassified`/`zotero.sqlite`/`--topic`) plus this ledger. PR candidate with the 3b code. |
| `a68636c` | Refuse --unclassified at the orchestrators, and correct the docs QA caught | Closes a silent-drop: `run_full`/`run_update_force` ignored `--unclassified` on the hdbscan path instead of refusing it. Fixes six doc claims a review pass found. PR candidate with 3b. |
| `2fb79aa` | Bind the guard test, fix the mode axis, correct the docs | The `a68636c` guard had no behavioral test (a raise→pass mutation stayed green); adds one. Also refuses classify flags on non-classifying modes (deploy/validate/…), the same silent-drop by a different door. PR candidate with 3b. |

Verified end to end on real data (see `.gjc/_session-*/ultragoal/ledger.jsonl`, goal
G001): real writing runs on the 3,273-paper ai4s corpus assigned 2,828 papers across 7
categories with `--unclassified skip` and 3,267 across 8 with `include`; `build_topic_index`
then produced a page containing all 8 Zotero category names and none of the 11 prior
HDBSCAN ones. The corpus was sha256-backed up and restored byte-identically afterward.

## Provider-substitution work (fork policy, predates this session's brief)

This group enforces "a missing optional provider disables its own feature and never
silently substitutes another." It is a deliberate behavior change relative to upstream,
so it is **not** part of purposes 1–3 and should be PR'd separately, if at all.

| Commit | Summary |
|---|---|
| `fce1d89` | No silent provider substitution; honor the Gemini off switch |
| `d53c821` | Drop the cross-provider fallback chain in cross-category insights |
| `b26a228` | Address review on the insights fallback removal |
| `08bab0f` | QA: grow the no-substitution suite to 50 cases |
| `d5c5b30` | Unify the Gemini key path in build_search_index; split the exit codes |
| `707596c` | Make a missing optional API kill only its own feature, not the run |
| `97a809c` | Tell the user why browser Deep Research is off instead of failing cryptically |
| `ba608fc` | Gate the primary Deep Research path too, and fix the test that hid it |
| `cbf251a` | Stop doctor lying about Gemini, and treat its absence as optional |
| `57753ee` | Make Gemini optional at setup instead of blocking onboarding |
| `5064d61` | Remove the three cross-provider fallbacks I missed |
| `42c2878` | Make three optional-dependency failures degrade instead of taking a feature down |
| `0daaf2c` | Make the docs stop promising a fallback the code no longer has |

## Portable fixes (not purpose-specific, safe to PR on their own)

Real bugs found along the way that any install hits, independent of purposes 1–3.

| Commit | Summary | Why it matters |
|---|---|---|
| `4a2433b` | Strip deploy credentials by slot, not by key prefix | Credential-stripping missed keys that did not match the expected prefix. |
| `b6145a1` | Stop setup from installing a skill that stopped being true | The rendered skill hardcoded ai4s, so every non-ai4s install shipped a skill pointing at a topic the user does not have. |
| `6387e1e` | Point the concurrency docs at the knob that actually exists | Docs named a flag that was not the real one. |
| `f40e55f` | Split md_to_html out of agent_lecture_digest | The converter lived in a module that imports `google.genai` at import time, so citedby reports rendered raw markdown on machines without the Gemini SDK. |
| `4d8cc08` | Launch child steps with sys.executable, not literal "python" | `force_py312()` re-execs the entrypoint, then child steps ran whatever `python` PATH resolved to. The commit replaces 35 of them (`git show 4d8cc08 --numstat` → 35/35 in `run_update_force.py`). |
| `61170a7` | Write the index files atomically | A kill mid-write left a truncated `_papers_index.json`, which every later step reads. |
| `ba5b0a1` | Declare PyYAML; document py312 as the only supported interpreter | `lib/metrics/store.py` imports `yaml` at module level but it was not in requirements, so step 1.5 failed silently every cycle. |
| `0f1223c` | Stop hardcoding the original author's home directory | `lecture_map.py` inserted a path that exists on exactly one machine. |
| `9eeae81` | Finish the three I reported and left undone | `prepare_deploy` topic labels and probe paths read from config instead of a four-topic dict; setup renders to an untracked path instead of overwriting the tracked reference. |

`9eeae81` is listed here rather than as a detour because its content is portable
generalization work; only its timing was a detour (it finished items reported but left
undone in an earlier turn).

## Detours — not asked for

| Commit | Summary | Why it exists |
|---|---|---|
| `726fe59` | Fix a SyntaxError I introduced that killed every generated topic page | Repairs damage from an earlier commit in this branch. |
| `012adef` | Verify the generated page as an artifact, not as source text | Follow-up to `726fe59`: the test had asserted against source text, so it could not have caught the break. |
| `83873c1` | Stop line-ending churn from burying real diffs | A batch patch rewrote 8 CRLF files as LF, which staged as 6,138 changed lines for a 359-line change. Those figures are working-tree measurements taken before the commit, so they are not recoverable from git history. Caught before committing, but nothing in the repo would have stopped it — hence `.gitattributes` + `scripts/check-eol.py` + a CI job. |
| `4e5840e` | Purge the last stale LF count and guard against its return | The 179→184 LF correction had missed two extensionless files (`.gitattributes`, `scripts/pre-push`); this finishes it and adds a `git grep` test so a frozen count can't recur. Cleanup of this branch's own artifacts. |
| `6a51012` | Match the frozen-count guard's docstring and rigor to what it does | The `4e5840e` test's docstring overstated its regex coverage and could pass vacuously on a git failure. Cleanup of a defect introduced one commit earlier. |

The repo has 17 CRLF tracked text files and many LF ones **by design** — exact counts
via `git ls-files --eol`. The CRLF ones come from upstream, which still commits from
Windows. Do not normalize: it would rewrite thousands of lines and conflict wholesale on
every upstream merge.

## Upstream PR guidance

| Group | PR candidate? | Note |
|---|---|---|
| Purpose 1 (`d3da625`) | n/a | A merge of upstream into this fork; nothing to send back. |
| Purpose 2 (OAuth) | **Yes** | Self-contained: one new module plus callsite routing. |
| Purpose 3a (de-hardcoding) | **Yes** | Bug fixes; any non-ai4s install is affected. |
| Purpose 3b (Zotero tree) | **Yes** | Purely additive — new module, new flags, default behavior unchanged. Ships as `c4791cf`/`6fcb3b9`/`164c1ba`/`7f8c097` + the docs `642179e` + the hardening `a68636c`/`2fb79aa` (orchestrator guards, behavioral guard test, mode-axis guard). |
| Portable fixes | **Yes**, individually | Each stands alone. |
| Provider substitution | **Separate discussion** | A deliberate behavior change; upstream may consider the fallbacks intentional. |
| Detours | **Fork-local** | `83873c1` is arguably useful upstream (upstream authors from Windows); `726fe59`/`012adef`/`4e5840e`/`6a51012` only repair damage introduced on this branch. |
