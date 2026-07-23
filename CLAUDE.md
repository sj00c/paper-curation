# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic paper curation pipeline. Papers are fetched from Zotero, reviewed via Claude/Gemini APIs, classified into categories, and published as a searchable HTML index with per-paper review pages. Topic pages also expose a **Deep Research UI** that performs client-side RAG against a pre-built embedding index (Google `gemini-embedding-001`, 768d int8, task-typed) and streams Claude answers with `[ref:N]` citations and inline figures. Retrieval is hybrid BM25+dense fused with RRF and LLM re-ranked; query embeddings are computed for the reader by the worker `/api/embed` route (deployed) or `pipeline/serve_local.py` (local), so readers need no API key for retrieval — keys (BYOK) are only for answer generation.

- **Topics**: Configured per-user in secret-free `config.json` using aliases created from the user's Zotero collections (e.g., `bioml`, `robotics-reading`). Per-topic Core-1 search keywords are configurable via the `search_keywords` block (`{topic: {primary: [...], secondary: [...]}}`). Do not infer a current-user topic from repository sample names.
- **Deploy architecture** (split hosting):
  - **Cloudflare Workers (Static Assets + Functions)** is an internal/team deployment path only. `pipeline/prepare_deploy.py` runs `npx wrangler deploy` when explicitly requested (token via `CLOUDFLARE_API_TOKEN`/`CF_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`). `worker/index.js` exposes two routes that need wrangler secrets (`wrangler secret put`): `/api/embed` (Deep Research query embeddings — `GOOGLE_API_KEY`) and `/api/audio-email` (Audio Overview email — `RESEND_API_KEY`).
  - **GitHub `gh-pages` branch** holds tiny redirect stubs only — one `{topic}/index.html` per deployable topic that `meta refresh` + `window.location.replace()` to the Cloudflare URL. Synced idempotently by `prepare_deploy.py`.
  - **GitHub `master` branch** holds only code, `config.example.json`, `wrangler.toml`, and `docs/.assetsignore`. `docs/papers/`, `docs/humanoid/`, `docs/physical-ai/`, etc. are `.gitignore`'d to keep the repo small (full content lives only on Cloudflare + local).
  - Public GitHub/npm release, public scanner/license readiness, and canonical upstream embedding merge are deferred. Upstream embedding work proceeds only as an audit/migration through the versioned `pipeline/lib/search_index_metadata.py` seam; no public-readiness claim.
- **Language**: All reviews are written in Korean with technical terms in English

## Installation Flow (Claude Code)

사용자가 "paper-curation 설치/실행해줘"라고 요청하면 설명만 반환하지 말고 현재 체크아웃의 dependency-free Node 하네스를 직접 실행한다. 기존 ignored `config.json`은 fork/worktree 잔재일 수 있으므로 자동 재사용하지 않는다. 인증과 topic을 예제 값으로 고정하지 않는다.

### Auth and configuration semantics

- setup 기본값은 `--auth auto`다. 준비된 Claude Code OAuth 또는 Anthropic Console API key를 감지하고, 필요할 때만 선택을 받는다.
- OAuth를 강제할 때만 `--auth oauth`, metered Console API key를 강제할 때만 `--auth api-key`를 사용한다.
- Zotero와 Google key는 필수이며 `.env` 또는 process env에서만 공급한다. OpenAI, Resend, Java, PaperBanana는 선택 기능이고 없으면 fallback 또는 기능 생략으로 degrade한다.
- setup은 하나 이상의 Zotero collection을 선택받아 alias를 생성한다. 저장소 예제를 현재 사용자 topic으로 추정하지 않는다.
- `config.json`이 있으면 `--fresh-config` 또는 검증 후 `--reuse-config`를 명시한다. fresh config는 secret-free이며 API key/OAuth token을 저장하지 않는다.

### Current checkout-local onboarding

```bash
cd paper-curation
node ./bin/paper-curation.mjs skill install
cp .env.example .env
open -e .env                    # Linux: ${EDITOR:-vi} .env
node ./bin/paper-curation.mjs setup --fresh-config
node ./bin/paper-curation.mjs doctor --network --anthropic-smoke
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy
```

Support rules:
- `skill install`은 Python/conda 패키지 없이 동작하며 외부 skill에 의존하지 않는 managed skill bundle과 self-contained `SKILL.md`를 설치한다.
- Verification, onboarding, smoke, repair, local curate는 deploy suppression을 유지한다.
- 배포는 사용자가 명시적으로 publish/deploy를 요청한 경우에만 `--mode deploy`로 실행한다.
- `doctor --network --anthropic-smoke`는 선택된 auth, Zotero, Google, structured Claude call을 secret redaction과 함께 검증한다.
- `--max-papers`는 web search/register 후보 제한이며 Zotero review cap이 아니다.
- setup은 PaperBanana 또는 다른 선택 저장소를 자동 clone하지 않는다. TLS 검증은 기본 secure이며 비보안 우회는 `PAPER_CURATION_INSECURE_TLS=1` 또는 `network.allow_insecure_tls`+사유가 있는 경우로 한정한다.
- unqualified GitHub NPX를 첫 실행 경로로 제시하지 않는다.

### Step 2: Manual conda py312 fallback

NPX가 불가능할 때만 수동 경로를 사용한다. hand-picked dependency subset을 설치하지 말고 반드시 전체 `requirements.txt`를 사용한다.

```bash
# 이미 받은 maintainer/fork/PR checkout 루트에서 실행한다.
cd paper-curation
conda create -n py312 -c conda-forge python=3.12 pip -y
conda activate py312
pip install -r requirements.txt

# 실제 키는 shell history 대신 .env에 저장한다.
cp .env.example .env
open -e .env
claude auth login
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth oauth --no-run

# Anthropic Console API 키 과금 대안:
# 편집기로 .env에 ANTHROPIC_API_KEY를 추가한 뒤 실행한다.
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth api-key --no-run
```

`setup.py`는 config.json 생성, Zotero 연결 테스트, PaperBanana 확인, SKILL.md 설치 안내를 수행한다. 직접 실행할 때는 `--no-run`으로 첫 파이프라인을 건너뛴다. NPX에서 첫 실행까지 이어서 돌릴 때만 `--run-first`를 명시한다.

## Architecture

### Central Data Store

`docs/papers/` is the single source of truth for all paper content:
- `docs/papers/_papers_index.json` — master index (965 entries) with metadata, categories, scores
- `docs/papers/{NNN_Slug}/review.md` — Korean review in structured markdown
- `docs/papers/{NNN_Slug}/index.html` — generated from review.md by `review_to_html.py`
- `docs/papers/{NNN_Slug}/figures/*.webp` — extracted figures (PNG→WebP for deploy)

### Topic Views

`docs/{configured-topic}/` contains:
- `index.html` — category-grouped card view (generated by `build_topic_index.py`)
- `network.html` — D3.js force-directed network visualization (generated by `generate_network.py`)
- `_new_classification.json` — category definitions + paper→category assignments
- `_category_summaries.json` — per-category descriptions, sub-themes
- `_timeline_narrative.json` — executive summary + category analyses (Korean)
- `_category_narratives.json` — per-category narrative cache for timeline generation
- `_method_text_*.txt` — methodology narrative per category
- `category_timeline_*.png` — per-category timeline images (PaperBanana)

### Shared Modules

`pipeline/lib/` contains shared utilities:
- `categories.py` — `CATEGORIES_BY_TOPIC` (canonical category lists) + `category_slug()` (name→filesystem slug)
- `paperbanana.py` — PaperBanana wrapper (path management, agent init, diagram generation)
- `dateutil.py` — Date parsing and formatting utilities

### Pipeline Scripts (execution order)

| Step | Script | Purpose |
|------|--------|---------|
| Entry | `pipeline/run_full.py` | 3-axis orchestrator (`--mode/--source/--images`). Chains all steps below in the right order; also exposes `--mode audit/fix-matching/dedup/validate` as standalone tool entrypoints |
| 0 | `pipeline/search_papers.py` | arXiv/S2/OpenAlex search + dedup + relevance filter |
| 0 | `pipeline/register_zotero.py` | Zotero registration + PDF download |
| 0 | `pipeline/sync_zotero.py` | Sync deletions/renames from Zotero |
| 0.5 | `pipeline/dedup_zotero.py` | Zotero collection dedup (title60 + DOI + arXiv + PDF). Preflight (dry-run) auto-integrated into `run_update_force` |
| 1 | `pipeline/run_update_force.py` | Full batch: Zotero fetch → PDF parse → figure extract → **Zotero↔text sanity gate** → review → HTML. ID-first `find_pdf()` with `--strict-pdf` blocking fuzzy |
| 2 | `pipeline/build_papers_index.py` | Rebuild `_papers_index.json` with integrity fields (`text_md_sha256`, `doi_verified`, `zotero_item_key`) via atomic write |
| 3 | `pipeline/classify_papers.py` | **HDBSCAN approximate_predict (원 설계)** — `topic_modeling` 이 저장한 `_hdbscan_model.joblib` 번들(hdbscan_model + UMAP transformer + centroids + tid→cat) 로드 → UMAP 5D 투영 → `hdbscan.approximate_predict` 로 primary sub-cluster 결정. Outlier(-1)는 768D centroid 코사인 최단점으로 강제 배정. `all_categories` 는 centroid 거리 오름차순 top-N parent. SPECTER2 임베딩은 proximity adapter + CLS pooling (업그레이드 후 새 임베딩을 반영하려면 `topic_modeling.py` 를 한 번 재실행해 `_hdbscan_model.joblib` 번들을 재생성해야 함). LLM 호출 없음. **UMAP/hdbscan/sentence-transformers env 필수** (py312 단독 — py314 금지, `_env_guard` 가 py312 로 자동 재실행) |
| 4 | `pipeline/build_category_summaries.py` | Per-category 한글 description + sub-themes via Haiku |
| 4.5 | `pipeline/extract_insights.py` | Paper connections via Sonnet (Core 기본). Cross-category Research Insights 생성은 **opt-in** — `run_full --insights` 일 때만. Auto Haiku-summarization fallback when prompt >988k tokens (compress toward 900k). cross-category 호출은 Anthropic → OpenAI → Gemini fallback |
| 5 | `pipeline/generate_timelines.py` | Bottom-up timeline narrative (Opus) + PaperBanana images. Gemini retry schedule 3×60s → 2×1800s |
| 5.5 | `pipeline/generate_network.py` | **Option O-2 (`--insights` only)** — D3.js force-directed network visualization |
| 5.5 | `pipeline/generate_workflow.py` | Pipeline workflow diagram (PaperBanana, `--style cat/fairy/academic`) |
| 6 | `pipeline/validate_papers.py` | Strict validation gate: figure refs, classification schema, category whitelist, DOI cross-validation, duplicate text.md, timeline↔category match. `--strict` exits 1 |
| 7 | `pipeline/review_to_html.py` | Convert review.md → index.html (canonical template) |
| 8 | `pipeline/build_topic_index.py` | Generate `{topic}/index.html` with cards, search, timelines, Deep Research UI |
| 8.5 | `pipeline/build_search_index.py` | Build Deep Research RAG index — section-aware chunks + Google `gemini-embedding-001` (`output_dimensionality=768`, `task_type=RETRIEVAL_DOCUMENT`; non-3072 차원은 비정규화로 돌아오므로 **반드시 L2-normalize 후 int8 양자화**) + BM25 sparse terms → `{topic}/_search_index.json`. `pipeline/lib/search_index_metadata.py` is authoritative; incompatible index/cache metadata is never mixed and never auto-rebuilt. Recovery requires explicit audit/migration/rebuild through the harness. 쿼리 임베딩은 worker `/api/embed` / `pipeline/serve_local.py` 가 `RETRIEVAL_QUERY` 로 처리 |
| 9 | `pipeline/cleanup.py` | Remove stale files (old timelines, graphify temp, caches) + prune stale category entries from narrative JSONs |
| 10 | `pipeline/prepare_deploy.py` | PNG→WebP, static asset secret-safety checks, `wrangler deploy` → Cloudflare, idempotent gh-pages stub sync, Cloudflare 200 OK polling, then master commit (code/config only — docs/* gitignored) |
| Recover | `pipeline/audit_matching.py` | PDF↔review mismatch audit (duplicate text.md + 4-axis cross-check). Output `{topic}/_audit_report.json` |
| Recover | `pipeline/fix_matching.py` | Recovery tool: delete review/figure artifacts for audit-flagged slugs + print re-review command. Default dry-run, `--execute` for real |

Step 0 scripts are for full/update modes only (skipped in --local). Step 1 is the heavy batch (default `--concurrency 16`, Tier 4 — see README "Concurrency 가이드"). Wall-clock is ~20~30분 for ~80 papers at concurrency 16; ~1.5h at 4 (Tier 1 보수값).

### Optional Step 0 boost: scholar-megasearch

`pipeline/search_papers.py` 는 arXiv + Semantic Scholar + OpenAlex 3개 소스만 본다. **신규 토픽 첫 build** 나 **분야가 넓어 단일 인덱스 누락이 우려되는 주간 사이클** 에는 [scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) 스킬을 Step 0 대안으로 쓸 수 있다 — 20+ DB (Crossref / PubMed / bioRxiv / medRxiv / DOAJ / CORE / BASE / OpenAIRE / Zenodo / Unpaywall / HAL / DBLP / IACR / SSRN / Europe PMC + arXiv / S2 / OpenAlex) fan-out → DOI/arXiv/title30 dedup with provenance → corroboration ranking → OA PDF 다운로드까지 한 번에. 한국 망 arXiv 429 도 자동 fallback.

| Step | Script | Purpose |
|------|--------|---------|
| 0-mega | scholar-megasearch (skill) | 20+ DB fan-out → `literature_search/<topic>_<date>/corpus.json` + `pdfs/manifest.json` |
| 0-mega | `pipeline/megasearch_to_zotero.py` | corpus → `_search_results.json` 변환 + `_papers_index.json` cross-dedup (이미 리뷰한 논문 자동 제외) + 받아둔 PDF 를 Zotero PDF 디렉토리로 pre-stage |

연결 패턴:

```bash
# 1) Claude Code 안에서 스킬 실행 (예: bioml 토픽 첫 build)
#    "search every database for biology + ML for the last year, L4 with PDFs"
#    → literature_search/bioml-ml_2026-06-08/{corpus.json, pdfs/}

# 2) corpus → _search_results.json 변환 (cross-dedup + PDF pre-stage)
PYTHONUTF8=1 python pipeline/megasearch_to_zotero.py \
  --topic bioml \
  --corpus literature_search/bioml-ml_2026-06-08/corpus.json \
  --pdfs-dir literature_search/bioml-ml_2026-06-08/pdfs \
  --min-sources 2          # 2개 이상 DB 가 surface 한 corroborated 만

# 3) 기존 파이프라인 진입 — register_zotero 가 Zotero 등록 + PDF 첨부
PYTHONUTF8=1 python pipeline/register_zotero.py --topic bioml

# 4) 첫 build는 deploy suppression 유지 — publish 의도 확인 전에는 no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy
```

`megasearch_to_zotero.py` 가 자동으로 처리하는 것:
- **min-sources 필터** — `--min-sources 2` 이상이면 corroboration 노이즈 컷
- **`_papers_index.json` cross-dedup** — DOI / arXiv-id / title30 매치 시 skip, `_megasearch_skipped_known.json` 에 로그
- **PDF pre-stage** — scholar-megasearch 가 받은 OA PDF 를 `safe_filename(title) + ".pdf"` 형식으로 Zotero PDF 디렉토리에 복사 → `register_zotero.download_pdf()` 가 존재 체크에서 단축되어 재다운로드 안 함
- **paper dict 매핑** — `year` → `date`, `sources` → `_megasearch_sources` (traceability 유지)

`--register` 한 줄로 변환 + Zotero 등록까지 한 번에:

```bash
PYTHONUTF8=1 python pipeline/megasearch_to_zotero.py \
  --topic bioml --corpus run/corpus.json --pdfs-dir run/pdfs --register
```

**언제 쓰나**:
- 신규 토픽 첫 build — 광범위 sweep + L3+ citation snowball 로 seed corpus 확보
- bioml/chem/medical 처럼 `search_papers.py` 가 잡지 못하는 PubMed/bioRxiv/medRxiv 가 중요한 토픽
- 한국 망에서 arXiv 429 가 chronic 한 시기

**언제 안 쓰나**:
- 주간 운영 (`run_full --mode curate --source web --days 7`) — 기존 `search_papers.py` 가 빠르고 충분
- `--source zotero` (로컬 Zotero 만) — Step 0 자체가 skip

**MCP 의존성**: `~/.claude.json` 의 `mcpServers` 에 `arxiv-mcp-server` / `asta` / `paper-search-mcp` 가 등록돼 있어야 함 (`scholar-megasearch/setup/install.sh` 가 자동 등록). `uv` 가 없으면 arxiv-mcp-server 만 비활성 (paper-search-mcp 가 arXiv 도 커버하므로 운영에는 영향 없음).

### run_update_force.py flags

| Flag | Effect |
|------|--------|
| `--resume` | Update mode: skip existing review.md, preserve categories |
| `--timeline` | Regenerate timeline images (with --resume: changed cats only) |
| `--category` | Re-run topic_modeling, auto-enables --timeline for changed cats |
| `--resume --timeline` | Update + changed category timeline images |
| `--resume --category` | Update + full reclassification + changed cat timelines |

## Python Environment

**표준 환경: 단일 conda env `py312` (Python 3.12, macOS / Linux)** — 오케스트레이터·LLM·웹·PDF·HTML·클러스터링 단계 모두 여기서 돌린다. `requirements.txt` 가 umap-learn / hdbscan / sentence-transformers 를 포함하므로, 현재 인터프리터로 클러스터링 라이브러리 import 가 성공하면 `topic_modeling.py` / `classify_papers.py` 가 **별도 서브프로세스 없이 in-process** 로 실행된다. Python 3.12 는 numba 의 `CALL_KW` 비호환 문제가 없어 단일 env 로 충분하다.

**⚠️ py314 사용 금지 (운영자 지시 2026-06-18)**: paper-curation 은 **py312 단독**으로만 돌린다. Python 3.14 는 numba 의 bytecode interpreter 가 3.14 의 `CALL_KW` opcode 를 처리하지 못해 `umap_cluster.transform()` → `sklearn.pairwise_distances(metric=callable)` 경로에서 죽는다 (`op_CALL_KW: pop from empty list`). 이를 피하려고 과거엔 py314 메인 + py312 보조 듀얼을 썼으나, 지금은 **py312 단일 표준**으로 통일했다. 모든 실행 진입점(`__main__`)이 `_env_guard.force_py312()` 를 호출해, py312 가 아닌 인터프리터(예: py314)로 실행되면 **py312 로 자동 재실행**한다. py312 를 못 찾으면 명확히 실패하며 절대 py314 로 진행하지 않는다 (탐색 우선순위: `PAPER_CURATION_PY312` → 형제 env `../py312/bin/python` → `which python3.12`).

### macOS / Linux (권장)

```bash
# 1) miniconda 가 이미 깔려 있다고 가정. 최초 1회 단일 env 생성:
conda create -n py312 -c conda-forge python=3.12 pip -y
conda activate py312

# 2) 핵심 의존성 설치 (umap-learn / hdbscan / sentence-transformers 포함)
pip install -r requirements.txt

# 3) Java Runtime — opendataloader-pdf 는 Java CLI 래퍼. 없으면 PyMuPDF 로
#    조용히 fallback 되어 표/구조 추출 품질이 떨어짐.
brew install --cask temurin   # macOS Eclipse Temurin (OpenJDK)

# 4) 새 셸이 열릴 때 py312 자동 활성화
echo 'conda activate py312' >> ~/.zshrc

# 5) 평소 로컬 사용 — 클러스터링 라이브러리가 import 되므로 classify/topic_modeling 도 in-process 로 실행
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source web --days 7 --no-deploy
```

> py312 단독 환경만 지원한다. py314 등 다른 인터프리터로 실행해도 `_env_guard.force_py312()` 가 py312 로 자동 재실행하므로, 별도 듀얼 env 구성은 필요 없다 (위 "⚠️ py314 사용 금지" 참조).

### Windows fallback (Smart App Control 환경)

Windows Smart App Control(WDAC) 이 Python 3.14 의 numba/llvmlite DLL 을 차단하는 경우도 위와 동일한 `py312` env 로 분리되어 자동 라우팅된다. 콘다 env 가 형제 위치 (`<base>/envs/py312`) 에 없으면 `PAPER_CURATION_PY312` 환경변수로 절대 경로를 지정:

```cmd
set PAPER_CURATION_PY312=C:\Users\<you>\miniconda3\envs\py312\python.exe
PAPER_CURATION_NO_DEPLOY=1 node .\bin\paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy
```

### 한국 망 환경 우회 (SPECTER2 / arXiv)

한국 ISP 에서 `huggingface.co` LFS 가 막혀 SPECTER2 (`allenai/specter2_base`) 다운로드 실패하는 경우, AWS S3 미러로 한 번 받으면 `topic_modeling.py` 의 `SPECTER2_MODEL` 상수가 `.cache/base/` 를 자동 인식한다:

```bash
mkdir -p .cache && cd .cache
curl -L -o specter2_0.tar.gz "https://ai2-s2-research-public.s3.amazonaws.com/specter2_0/specter2_0.tar.gz"
tar -xzf specter2_0.tar.gz   # base/ + adapters/
```

arXiv 가 chronic 429/timeout 인 경우 `search_papers.py --skip-arxiv` 로 우회 (OpenAlex + S2 만 사용, 윈도우당 ~8분 단축). README "한국 망 환경 우회" 섹션 참고.

## Common Commands

Standard entrypoint is the checkout-local Node harness; `--` forwards to `pipeline/run_full.py` (3축: `--mode/--source/--images`). Direct Python script calls are fallback/debug/recovery only. Python commands require `PYTHONUTF8=1` on Windows to avoid cp949 encoding issues.

```bash
# 진단 / verification
node ./bin/paper-curation.mjs doctor --network --anthropic-smoke

# 로컬 업데이트 — 검색 스킵, sync만 (배포 억제)
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy

# 주간 운영 — 검색 + Zotero 등록 + sync + 신규 리뷰
# --max-papers는 web 검색/등록 후보 수만 제한한다.
# 이 프로덕션 명령은 Cloudflare 자격증명/설정이 있으면 성공 후 자동 publish될 수 있다.
node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source web --days 7 --max-papers 20

# 특정 슬러그만 force-rebuild (감사·복구 시, forced no-deploy)
#   주의: --mode rebuild 는 토픽 전체의 categorization/insights/timelines 까지 재생성한다 (수 시간, API 비용 ↑).
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode rebuild --slugs 088,1093 --strict-pdf --no-deploy --yes

# 분류만 다시 (Phase 3 node-based, LLM 호출 없음; forced no-deploy)
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode reclassify --no-deploy

# 타임라인 narrative + 이미지 재생성 (forced no-deploy)
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode retime --images all --no-deploy

# 배포만: wrangler deploy → Cloudflare + gh-pages 스텁 동기화 + master 코드 push
# internal/team deployment only; deployable topics are explicit operator choices, not sample-topic defaults
# 요구 env: CF_API_TOKEN (or CLOUDFLARE_API_TOKEN) + CLOUDFLARE_ACCOUNT_ID
# Worker secrets (1회): wrangler secret put GOOGLE_API_KEY (/api/embed) + RESEND_API_KEY (/api/audio-email)
node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode deploy

# 실행 계획 미리보기 (변경 0, deploy suppression explicit)
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --dry-run --no-deploy
```

### 감사·복구 (forced no-deploy)

```bash
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode audit --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode fix-matching --no-deploy --yes
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode rebuild --slugs <list> --strict-pdf --no-deploy --yes
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode validate --no-deploy --yes

# 개별 스크립트는 소스 수준 디버깅 전용. Zotero write/delete는 별도 실행 동의가 필요합니다.
PAPER_CURATION_NO_DEPLOY=1 PYTHONUTF8=1 python pipeline/dedup_zotero.py --topic <configured-topic>

# 개별 검증 스크립트 (배포 없음)
PAPER_CURATION_NO_DEPLOY=1 PYTHONUTF8=1 python pipeline/validate_papers.py --topic <configured-topic> --strict

# 분류만 단독 (UMAP transform + hdbscan.approximate_predict)
# 사전 조건: topic_modeling 이 `_hdbscan_model.joblib` 번들을 미리 저장해 두었어야 함
PYTHONUTF8=1 python pipeline/classify_papers.py --topic <configured-topic>
PYTHONUTF8=1 python pipeline/classify_papers.py --topic <configured-topic> --slugs 088,1093 --dry-run

# Topic modeling (UMAP/hdbscan/sentence-transformers 의존 — 단일 py312 env 활성 상태)
PYTHONUTF8=1 python pipeline/topic_modeling.py --topic <configured-topic>

# Cleanup stale files (dry-run / execute)
PYTHONUTF8=1 python pipeline/cleanup.py
PYTHONUTF8=1 python pipeline/cleanup.py --execute
```

### 안전 플래그 (run_full / run_update_force 공통)

- `--strict-pdf` — fuzzy 매칭 차단, ID(Zotero/DOI/arXiv)로만
- `--slugs A,B,C` — 특정 슬러그만 처리
- `--dry-run` — 실행 계획만 출력
- `--skip-dedup` / `--dedup-execute` — Zotero dedup preflight 제어
- `--insights` — 크로스카테고리 Research Insights 생성 opt-in (기본 Core 는 paper-connections 만)
- `--yes` — `--mode rebuild` 확인 게이트 우회

## Key Design Decisions

- **Bottom-up topic modeling**: `topic_modeling.py`는 BERTopic 대신 sklearn HDBSCAN + UMAP을 직접 사용. HDBSCAN fine-grained clustering → c-TF-IDF 키워드 추출 (Grootendorst 2022, 클러스터=1문서 tf × 클래스 idf) → Sonnet 배치 작명 → Sonnet 카테고리 그룹핑. `min_cluster_size`를 자동 조정하여 sub-topic 40~100개를 목표로 한다.
- **Multi-class classification**: Papers get 1 `primary_category` + 1-3 `all_categories`. The topic index shows cards under every matching category.
- **Deployable assets never contain operator secrets**: OAuth tokens, Cloudflare tokens, and deploy credentials must never enter HTML/static assets. Localhost builds may temporarily seed local BYOK keys for convenience, but `prepare_deploy.py` must strip them before Cloudflare/gh-pages output; browser answer generation remains reader BYOK and deployed worker secrets stay in wrangler secrets.
- **Whitelist .gitignore**: Everything is excluded by default (`*`), then only code + configs are whitelisted. Under `docs/` only `index.html` (landing redirect), `setup-guide.md`, and `.assetsignore` are tracked on master. All topic content (`docs/papers/`, `docs/humanoid/`, `docs/physical-ai/`, etc.) is gitignored — it lives locally and on Cloudflare, never on master. `wrangler deploy` uses `docs/` directly; `docs/.assetsignore` excludes ai4s/scisci and local caches from the Cloudflare upload.
- **Two themes**: `ai4s` uses red accent (#D63423), `scisci` uses blue (#2374D6). Theme selection flows through `review_to_html.py` and `build_topic_index.py`.
- **Figure extraction**: PyMuPDF renders pages containing "Figure N" / "Fig. N" at 3x zoom. Up to 5 figures per paper from pages 0-14.
- **Slug format**: `{NNN}_{Title_first_40_chars}` where NNN is zero-padded sequence number.
- **PDF-change auto-detect**: `run_update_force.py` 가 매 실행 시작 시 `_papers_index.json` 의 `pdf_path` 캐시와 디스크 mtime을 비교해 PDF가 review.md 보다 새 것이면 자동으로 `forced_slugs` 에 추가한다 (Zotero API 호출 0, 순수 stat). 캐시는 `find_pdf()` 성공 시 자동 적재되므로 처음 한 사이클을 돈 뒤부터 작동.
- **Subprocess timeouts (LLM steps)**: `run_step()` 에 박힌 wall-clock cap — `topic_modeling=3600s`, `extract_insights=14400s (4h)`, `generate_timelines=21600s (6h)`. 실제 토픽 크기(논문 수)에 맞춰 한 번 늘려 둠 — 한국망↔Anthropic 응답 변동성 + paper_connections 의 카테고리×배치 곱셈 비용을 흡수.
- **Claude auth backend**: `anthropic_auth.create_anthropic_client()` selects either the Anthropic SDK for Console API-key mode or the isolated `claude -p` bridge for subscription OAuth. OAuth structured/tool output requires Claude Code >=2.1.205. OAuth child calls remove API credentials, and auto mode prefers an OAuth token/login over API keys.
- **Zotero `attachments:` URI 핸들링**: `find_pdf()` priority 1 (Zotero children API) 에서 `attachments:<filename>` 접두사를 `ZOTERO_DIR/<filename>` 으로 해석. Zotero 의 "Linked Attachment Base Directory" 설정을 따른다.
- **Zotero PDF cache fallback**: setup/config_loader create project-local `pdf_cache/` when `ZOTERO_DIR` is absent. `find_pdf()` downloads Zotero Storage attachments through the authenticated `/items/{attachmentKey}/file` endpoint into that cache. `ZOTERO_DIR` remains an override for linked-only local attachments.

## External Dependencies

- **Zotero Web API**: Collection names and Zotero API key are configured in `config.json` or env.
- **Claude authentication**: Reviews, connections, summaries, timelines, and insights use either Claude Code OAuth subscription mode (`--auth oauth`, Claude Code >=2.1.205, `claude auth login` or env-only `CLAUDE_CODE_OAUTH_TOKEN`) or Anthropic Console API-key mode (`--auth api-key`, `ANTHROPIC_API_KEY`). OAuth tokens are never saved by setup; `config.json` may store only `anthropic_auth.mode = "oauth"`. OAuth child calls strip API credentials, and auto mode selects an available OAuth token/login before any API key.
- **Google Gemini API**: Required for Figure validation in `pipeline/run_update_force.py`, TTS for Audio Overview, and **Deep Research embeddings** — `gemini-embedding-001` (`output_dimensionality=768`, `task_type=RETRIEVAL_DOCUMENT` for the index in `pipeline/build_search_index.py`, `RETRIEVAL_QUERY` for queries). Query embeddings are served to readers by the worker `/api/embed` route (deployed) or `pipeline/serve_local.py` (local), so readers need no key for retrieval. Key from `GOOGLE_API_KEY` env var or `config.json`. **Gotcha**: non-3072 dims come back non-normalized — L2-normalize before int8 quantization.
- **OpenAI API (optional)**: Optional fallback/BYOK-compatible provider where supported. No longer required for the search index.
- **Resend API (optional)**: Only for deployed Audio Overview email via wrangler secret `RESEND_API_KEY`; not required for local curation.
- **PyMuPDF (fitz)**: PDF text extraction and figure rendering
- **Pillow**: PNG→WebP conversion in `pipeline/prepare_deploy.py`
- **Zotero PDF storage**: Path configured in `config.json` (`zotero.pdf_dir`)
