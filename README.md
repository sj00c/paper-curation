# Paper Curation

**Zotero에 논문 PDF만 모아두었다면, 나머지는 자동입니다.**

논문 수백 편을 한국어 구조화 리뷰로 변환하고, AI가 자동 분류하고, 자연어로 질문하면 논문을 근거로 답변하는 **개인 연구 지식 시스템**을 만듭니다. 로컬에서 동작하며 배포는 선택입니다.

<a href="#english">English</a>

---

## 이런 걸 할 수 있습니다

| 기능 | 설명 |
|------|------|
| **구조화 리뷰** | PDF에서 텍스트/Figure를 추출하고, Claude가 Essence-Motivation-Achievement-How-Originality-Evaluation 6개 섹션의 한국어 리뷰를 자동 작성 |
| **자동 분류** | Bottom-up 토픽 모델링(HDBSCAN + UMAP)으로 카테고리를 자동 생성하고 논문을 분류 |
| **Deep Research** | 자연어 질의 + 임베딩 검색 + Claude 답변. 논문 원문까지 참조하여 정량적 디테일 포함 |
| **타임라인 시각화** | 카테고리별 연구 동향 내러티브 + 다이어그램 자동 생성 (PaperBanana) |
| **네트워크 시각화** | UMAP 2D/3D 인터랙티브 네트워크. 카테고리 필터, Ego Network, Hub/Bridge 하이라이트 |
| **지식 축적** | Obsidian 연동으로 메모가 다음 질의에 반영되는 compounding knowledge |
| **논문 검색/등록** | arXiv, Semantic Scholar, OpenAlex 병렬 검색 + Zotero 자동 등록 (선택) |

**필요한 것**: Zotero 컬렉션 + PDF + API 키 (Anthropic, Google, OpenAI)

---

## 설치: 명령어 한 줄

[Claude Code](https://claude.ai/code)에서 아래 한 줄이면 클론, 의존성 설치, Zotero 연결, 첫 파이프라인 실행까지 자동으로 완료됩니다:

> *"여기에 paper-curation을 설치해줘: https://github.com/jehyunlee/paper-curation"*

<details>
<summary><b>수동 설치</b></summary>

```bash
git clone https://github.com/jehyunlee/paper-curation.git
cd paper-curation
pip install anthropic google-genai openai numpy pymupdf Pillow requests opendataloader-pdf
python pipeline/setup.py
```

`setup.py`가 대화형으로 config.json 생성, Zotero 연결 테스트, API 키 확인, 첫 파이프라인 실행을 안내합니다.

</details>

### 사전 준비

- **Zotero**: [API Key 발급](https://www.zotero.org/settings/keys) + 큐레이션할 컬렉션에 논문 PDF 준비
- **환경변수**: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`
- **Python 3.12+**

---

## 워크플로우

![워크플로우](workflow.png)

```mermaid
flowchart TB
    ZT[Zotero 컬렉션 PDF] --> S1
    subgraph Pipeline[run_full.py 오케스트레이터]
      S1[1 · 데이터 수집<br/>text.md + figures/]
      S2[2 · 구조화 리뷰<br/>review.md 6섹션]
      S3[3 · 토픽 모델링 + 분류<br/>_new_classification.json]
      S4[4 · 인사이트 + 타임라인<br/>narrative + timeline.png]
      S5[5 · Deep Research 인덱스<br/>_search_index.json]
      S6[6 · 인덱스 + 네트워크<br/>index.html + network.html]
    end
    S1 --> S2 --> S3 --> S4 --> S6
    S2 --> S5 --> S6
    S6 --> OUT{로컬 열람 또는 배포}
    OUT -->|로컬| LOCAL[python -m http.server]
    OUT -->|배포| DEPLOY[Cloudflare + gh-pages 스텁]
```

### 1. 데이터 수집

- **입력**: Zotero 컬렉션의 PDF. 선택적으로 arXiv/Semantic Scholar/OpenAlex 병렬 검색 + Zotero 자동 등록
- **처리**: PyMuPDF로 텍스트 추출 + Figure 렌더링(3× zoom, 최대 5장). Gemini가 Figure 품질 검증
- **출력**: `papers/{slug}/text.md`, `papers/{slug}/figures/*.webp`

### 2. 구조화 리뷰

- **입력**: 추출된 텍스트 + Figure
- **처리**: Claude Haiku가 6개 섹션(Essence · Motivation · Achievement · How · Originality · Evaluation) 한국어 리뷰 작성. 기술 용어는 원문 그대로 유지. 병렬 4건 동시 처리
- **출력**: `papers/{slug}/review.md` + `papers/{slug}/index.html`
- **활용**: 브라우저에서 리뷰 열람, Figure 인라인 표시, Related Papers 자동 연결

### 3. 토픽 모델링 + 분류

- **입력**: 전체 리뷰의 Essence + Title
- **처리** (LLM 호출 최소화, bottom-up):
  1. SPECTER2 임베딩 → HDBSCAN fine-grained 클러스터링
  2. TF-IDF 키워드 추출 → Claude Sonnet이 클러스터 작명
  3. Ward linkage로 카테고리 그룹핑
  4. 논문당 1~3개 카테고리 복수 분류 (Node-based Hybrid C: KNN-vote primary + qualified-vote multi)
- **출력**: `_new_classification.json`, `_papers_index.json`

### 4. 인사이트 + 타임라인

- **입력**: 카테고리별 논문 목록 + 리뷰
- **처리**:
  1. Claude Sonnet이 카테고리 요약·세부 주제·카테고리 간 논문 연결 관계 추출
  2. Claude Opus가 카테고리별 연구 동향 내러티브 작성
  3. PaperBanana가 타임라인 다이어그램 자동 생성
- **출력**: `_category_summaries.json`, `_timeline_narrative.json`, `category_timeline_*.png`

### 5. Deep Research 인덱스

- **입력**: 전체 리뷰 + 개인 메모(`notes/`)
- **처리**: Section-aware chunking → OpenAI `text-embedding-3-small` 임베딩 (int8 L2 양자화). 개인 메모도 인덱싱되어 다음 질의에 반영
- **출력**: `_search_index.json`
- **활용**: 토픽 페이지에서 자연어 질의 → 임베딩 유사도 검색 → Claude(Extended Thinking)가 논문 근거 답변 생성

### 6. 인덱스 + 네트워크

- **입력**: 전체 분류 + 리뷰 + 타임라인 + UMAP 좌표
- **처리**: 카테고리 카드·검색·타임라인 내러티브·Deep Research UI를 하나의 HTML로 조립. UMAP 2D/3D 좌표로 D3.js + Three.js 인터랙티브 네트워크 생성
- **출력**: `{topic}/index.html`, `{topic}/network.html`
- **활용**: `cd docs && python -m http.server 8000` → 브라우저에서 바로 사용

### 배포 (선택)

로컬 사용이 기본입니다. 외부 공유가 필요하면 **3-계층 split-host** 구조로 자동 배포됩니다:

| 계층 | 역할 | 내용 |
|------|------|------|
| **Cloudflare Workers (Static Assets)** | 사용자 콘텐츠 서빙 | `docs/` 전체 업로드 (`docs/.assetsignore`로 로컬 전용 토픽 제외) |
| **GitHub `gh-pages` 브랜치** | 진입 URL → Cloudflare 리다이렉트 | 토픽별 리다이렉트 스텁 (1KB 미만), `jehyunlee.github.io/paper-curation/{topic}/` → `workers.dev/{topic}/` |
| **GitHub `master` 브랜치** | 코드·설정·README | 대용량 `docs/papers/`, `docs/{topic}/` 콘텐츠는 `.gitignore`로 제외 |

```bash
# 배포 (환경변수 필요: CF_API_TOKEN + CLOUDFLARE_ACCOUNT_ID)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode deploy
```

자동 처리:
- PNG → WebP 변환 (용량 ~60% 절감)
- 배포용 HTML에서 API 키 제거 후 로컬 working tree 자동 복원
- `npx wrangler deploy` → Cloudflare 업로드 (해시 기반 증분 업로드)
- gh-pages 리다이렉트 스텁 idempotent 동기화 (새 토픽 자동 감지, 변경 없으면 푸시 스킵)
- Cloudflare 200 OK 검증 (최대 5분 폴링)
- master에는 **코드·설정 변경만** commit + push (대용량 콘텐츠는 `.gitignore`)

환경변수 발급: Cloudflare Dashboard → My Profile → API Tokens → "Edit Cloudflare Workers" 템플릿.
```cmd
setx CF_API_TOKEN "..."
setx CLOUDFLARE_ACCOUNT_ID "..."
```

---

## 사용 모드 — 단일 오케스트레이터 `run_full.py`

3축(`--mode` / `--source` / `--images`)으로 SKILL.md의 구 Recipe A~H를 한 줄로 통합. `--source web`이면 검색·등록·sync까지 자동 체인.

```bash
# 주간 운영 — 검색 → Zotero 등록 → sync → 신규만 리뷰
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode curate --source web --days 7

# 로컬 업데이트 — 검색 스킵, sync만 후 신규 리뷰
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode curate --source zotero

# 특정 슬러그만 재리뷰 (감사·복구 시)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode rebuild --slugs 088,1093 --strict-pdf

# 분류만 재실행 (Phase 3 node-based Hybrid C, LLM 호출 없음)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode reclassify

# 타임라인 narrative + 이미지 재생성
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode retime --images all

# 배포만
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode deploy

# 실행 계획 미리보기
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode curate --source web --dry-run

# 로컬 서버
cd docs && python -m http.server 8000
```

`--mode` 의미:
- **curate** — 신규 논문만 리뷰, 기존 유지 (가장 자주 사용)
- **rebuild** — 전체 review.md 재생성. `--yes` 또는 `--slugs`와 조합해서만 실행
- **reclassify** — review.md 유지, 카테고리만 재배정 (node-based)
- **retime** — narrative + 타임라인 이미지 재생성
- **deploy** — `prepare_deploy.py`만 실행

`--source` 매핑:
- **web** → `search_papers + register_zotero + sync_zotero + run_update_force`
- **zotero** → `sync_zotero + run_update_force`

명시 override: `--with-search` / `--no-search` / `--with-register` / `--no-register` / `--with-sync` / `--no-sync`

주요 안전 플래그:
- `--strict-pdf`: fuzzy PDF 매칭 차단 — ID(Zotero/DOI/arXiv) 매칭 안 되면 skip
- `--slugs A,B,C`: 특정 슬러그만 처리
- `--dry-run`: 실행 계획만 출력
- `--skip-dedup`: Zotero dedup preflight 스킵
- `--dedup-execute`: preflight가 실제 삭제까지 수행 (기본은 dry-run 리포트)
- `--yes`: rebuild 모드 확인 게이트 우회

`run_update_force.py`는 `run_full.py`의 review + post-processing 단계로 호출됩니다 — legacy 진입점으로 직접 호출도 가능.

---

## Reliability (v2+)

최근 리팩터링으로 추가된 안전장치:

| 장치 | 설명 |
|------|------|
| `run_full.py` 오케스트레이터 | 3축(`--mode/--source/--images`) 단일 진입점. 검색·등록·sync·리뷰·후처리·배포 자동 체인. dry-run plan 출력 |
| `find_pdf()` ID-first | Zotero attachment → DOI → arXiv → fuzzy(강화) 순서. 과거 fuzzy 오매칭 근본 원인 제거 |
| `--strict-pdf` | fuzzy 완전 차단 모드. 신규/복구 리뷰에 권장 |
| `classify_papers.py` (Phase 3) | node-based Hybrid C — SPECTER2 + KNN-vote primary + qualified-vote multi (LLM 호출 없음, HDBSCAN density 의도에 충실) |
| `audit_matching.py` | 동일 text.md 해시 공유 슬러그 탐지 (duplicate PDF) + 4축 cross-check |
| `fix_matching.py` | 감사 결과 기반 리뷰 삭제 + 재리뷰 명령 자동 출력 (기본 dry-run) |
| `dedup_zotero.py` | Zotero 컬렉션 중복 탐지/삭제 (제목 60자 + DOI + arXiv + PDF 공유). `run_update_force` preflight 자동 통합 |
| `validate_papers.py --strict` | 카테고리↔timeline 이미지 매치, duplicate text.md 탐지. 배포 게이트 |
| `cleanup.py` | stale 카테고리 timeline/캐시 삭제 + narrative JSON 내 stale 엔트리 pruning. 후처리 단계에 자동 통합 |
| `prepare_deploy.py` | split-host 배포 자동화: `wrangler deploy` → Cloudflare, gh-pages 리다이렉트 스텁 idempotent 동기화, Cloudflare 200 OK 폴링, master에 코드 변경만 push. API 키 메모리 제거 후 로컬 원복 |
| 21600s timeout | `generate_timelines` 후처리 호출 타임아웃 1h → 6h (PaperBanana 다중 카테고리 완주) |

**오매칭 감사·복구 워크플로우**:
```bash
PYTHONUTF8=1 python pipeline/audit_matching.py --topic my_topic          # 1. 탐지
PYTHONUTF8=1 python pipeline/fix_matching.py --topic my_topic            # 2. dry-run
PYTHONUTF8=1 python pipeline/fix_matching.py --topic my_topic --execute  # 3. 삭제
# 4. fix_matching이 출력한 run_update_force --slugs ... --strict-pdf 실행
PYTHONUTF8=1 python pipeline/audit_matching.py --topic my_topic          # 5. 검증
```

---

## Karpathy LLM Wiki와의 비교

[Karpathy의 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)는 "LLM이 정리하고 사람이 큐레이션하는 persistent knowledge base"라는 강력한 개념을 제안했습니다. Paper Curation은 이 철학을 공유하면서, 학술 논문에 특화된 자동화 파이프라인을 결합합니다.

| | Karpathy LLM Wiki | Paper Curation |
|---|---|---|
| **핵심 개념** | LLM이 정보를 정리하고 사람이 큐레이션 | 동일 + 자동 파이프라인 |
| **입력** | 자유 형식 텍스트, 웹 페이지 등 | Zotero PDF (학술 논문 특화) |
| **구조화** | 사용자가 직접 마크다운 작성 | 6개 섹션 자동 생성 (Essence~Evaluation) |
| **분류** | 수동 태깅/폴더 | Bottom-up 자동 분류 (HDBSCAN + UMAP) |
| **검색** | 키워드/전문 검색 | 임베딩 RAG + 자연어 질의 + Claude 답변 |
| **Figure** | 지원하지 않음 | PDF에서 자동 추출 + 인라인 표시 |
| **시각화** | 없음 | 타임라인 다이어그램 + UMAP 2D/3D 네트워크 |
| **지식 축적** | wiki-link 기반 | Obsidian wiki-link + 메모 -> 인덱스 재반영 |
| **배포** | 로컬 파일 | 로컬 + 정적 호스팅 (선택) |
| **설치** | 직접 구성 | Claude Code 한 줄 설치 |
| **장점** | 범용, 가벼움, 어떤 주제든 적용 가능 | 논문 특화 자동화, Figure/분류/시각화 내장 |
| **단점** | 논문 메타데이터/Figure 수동 처리 | 학술 논문 외 콘텐츠에는 과도할 수 있음 |

Paper Curation의 Obsidian 연동은 LLM Wiki의 compounding 개념을 그대로 구현합니다:

```
Deep Research 질의 -> Obsidian 메모 작성 -> 인덱스 재빌드 -> 다음 질의에 내 메모가 인용됨
```

---

## 요구사항

| 구분 | 항목 |
|------|------|
| **필수** | Python 3.12+, Zotero (API Key + 컬렉션 + PDF) |
| **API** | Anthropic (Claude Haiku/Sonnet/Opus), Google (Gemini), OpenAI (text-embedding-3-small), Zotero Web API |
| **Python** | anthropic, google-genai, openai, numpy, PyMuPDF, Pillow, requests, scikit-learn, umap-learn |
| **선택** | Obsidian (메모/Graph View), PaperBanana (타임라인 이미지), Zotero Desktop (PDF 원클릭) |

---

<details>
<summary><h2 id="english">English</h2></summary>

# Paper Curation

**If you have PDFs in a Zotero collection, the rest is automatic.**

Turn hundreds of papers into structured Korean reviews, auto-classify them with AI, and ask natural-language questions grounded in the actual papers. A **personal research knowledge system** that runs locally. Deployment is optional.

---

## What It Does

| Feature | Description |
|---------|-------------|
| **Structured Review** | Extracts text/figures from PDF. Claude generates 6-section Korean reviews (Essence-Motivation-Achievement-How-Originality-Evaluation) |
| **Auto-Classification** | Bottom-up topic modeling (HDBSCAN + UMAP) creates categories and assigns papers automatically |
| **Deep Research** | Natural-language Q&A with embedding search + Claude answers grounded in paper text. Includes quantitative details |
| **Timeline Visualization** | Per-category research trend narratives + auto-generated diagrams (PaperBanana) |
| **Network Visualization** | Interactive UMAP 2D/3D network with category filters, ego network, hub/bridge highlighting |
| **Knowledge Compounding** | Obsidian integration: your notes feed back into future queries |
| **Paper Discovery** | Parallel search across arXiv, Semantic Scholar, OpenAlex + auto-registration to Zotero (optional) |

**What you need**: A Zotero collection with PDFs + API keys (Anthropic, Google, OpenAI)

---

## Install: One Line

In [Claude Code](https://claude.ai/code), just say:

> *"Install paper-curation here: https://github.com/jehyunlee/paper-curation"*

Clone, dependencies, Zotero setup, and the first pipeline run — all handled automatically.

<details>
<summary><b>Manual Installation</b></summary>

```bash
git clone https://github.com/jehyunlee/paper-curation.git
cd paper-curation
pip install anthropic google-genai openai numpy pymupdf Pillow requests opendataloader-pdf
python pipeline/setup.py
```

`setup.py` interactively creates config.json, tests Zotero connectivity, checks API keys, and kicks off the first pipeline run.

</details>

### Prerequisites

- **Zotero**: [API Key](https://www.zotero.org/settings/keys) + a collection with paper PDFs
- **Environment variables**: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`
- **Python 3.12+**

---

## Workflow

![Workflow](workflow.png)

```mermaid
flowchart TB
    ZT[Zotero collection PDFs] --> S1
    subgraph Pipeline[run_full.py orchestrator]
      S1[1 · Data Collection<br/>text.md + figures/]
      S2[2 · Structured Review<br/>review.md 6-section]
      S3[3 · Topic Modeling + Classification<br/>_new_classification.json]
      S4[4 · Insights + Timelines<br/>narrative + timeline.png]
      S5[5 · Deep Research Index<br/>_search_index.json]
      S6[6 · Index + Network<br/>index.html + network.html]
    end
    S1 --> S2 --> S3 --> S4 --> S6
    S2 --> S5 --> S6
    S6 --> OUT{Local browse or deploy}
    OUT -->|local| LOCAL[python -m http.server]
    OUT -->|deploy| DEPLOY[Cloudflare + gh-pages stubs]
```

### 1. Data Collection

- **Input**: PDFs from Zotero collection. Optional parallel search (arXiv / Semantic Scholar / OpenAlex) + auto-registration to Zotero
- **Processing**: PyMuPDF extracts text + renders figures (3× zoom, up to 5). Gemini validates figure quality
- **Output**: `papers/{slug}/text.md`, `papers/{slug}/figures/*.webp`

### 2. Structured Review

- **Input**: Extracted text + figures
- **Processing**: Claude Haiku writes 6-section Korean reviews (Essence · Motivation · Achievement · How · Originality · Evaluation). Technical jargon kept verbatim. 4 concurrent workers
- **Output**: `papers/{slug}/review.md` + `papers/{slug}/index.html`
- **Usage**: Browse reviews in browser with inline figures and auto-linked related papers

### 3. Topic Modeling + Classification

- **Input**: Essence + title from all reviews
- **Processing** (bottom-up, minimal LLM calls):
  1. SPECTER2 embeddings → HDBSCAN fine-grained clustering
  2. TF-IDF keywords → Claude Sonnet names each cluster
  3. Ward linkage groups clusters into categories
  4. 1–3 categories per paper (Node-based Hybrid C: KNN-vote primary + qualified-vote multi)
- **Output**: `_new_classification.json`, `_papers_index.json`

### 4. Insights + Timelines

- **Input**: Per-category paper lists + reviews
- **Processing**:
  1. Claude Sonnet extracts category summaries, sub-themes, cross-category connections
  2. Claude Opus writes research-trend narratives per category
  3. PaperBanana auto-generates timeline diagrams
- **Output**: `_category_summaries.json`, `_timeline_narrative.json`, `category_timeline_*.png`

### 5. Deep Research Index

- **Input**: All reviews + personal notes (`notes/`)
- **Processing**: Section-aware chunking → OpenAI `text-embedding-3-small` embeddings (int8 L2 quantized). Personal notes are indexed and reflected in future queries
- **Output**: `_search_index.json`
- **Usage**: Natural-language query on topic page → embedding similarity search → Claude (Extended Thinking) generates grounded answer

### 6. Index + Network

- **Input**: All classifications + reviews + timelines + UMAP coordinates
- **Processing**: Assembles category cards, search, timeline narratives, and Deep Research UI into a single HTML. D3.js + Three.js interactive network from UMAP 2D/3D coordinates
- **Output**: `{topic}/index.html`, `{topic}/network.html`
- **Usage**: `cd docs && python -m http.server 8000` — browse locally

### Deployment (Optional)

Local use is the default. For sharing, a **3-tier split-host** architecture deploys automatically:

| Tier | Role | Contents |
|------|------|----------|
| **Cloudflare Workers (Static Assets)** | Serves user-facing content | Full `docs/` uploaded (local-only topics excluded via `docs/.assetsignore`) |
| **GitHub `gh-pages` branch** | Entry-URL → Cloudflare redirect | Per-topic redirect stubs (<1KB), `jehyunlee.github.io/paper-curation/{topic}/` → `workers.dev/{topic}/` |
| **GitHub `master` branch** | Code / config / README only | Large `docs/papers/`, `docs/{topic}/` content is `.gitignore`'d |

```bash
# Deploy (requires env: CF_API_TOKEN + CLOUDFLARE_ACCOUNT_ID)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode deploy
```

Automatic:
- PNG → WebP conversion (~60% size reduction)
- API keys stripped from deployed HTML, local working tree restored after push
- `npx wrangler deploy` → Cloudflare (hash-based incremental upload)
- gh-pages redirect stub idempotent sync (auto-discovers new topics; no-op when unchanged)
- Cloudflare 200 OK verification (polls up to 5 min)
- Only code/config changes pushed to master (content is gitignored)

Token setup: Cloudflare Dashboard → My Profile → API Tokens → "Edit Cloudflare Workers" template.
```cmd
setx CF_API_TOKEN "..."
setx CLOUDFLARE_ACCOUNT_ID "..."
```

---

## Usage Modes — Single Orchestrator `run_full.py`

Three axes (`--mode` / `--source` / `--images`) replace the legacy Recipe A–H. `--source web` auto-chains search → register → sync.

```bash
# Weekly — search → register to Zotero → sync → review new papers
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode curate --source web --days 7

# Local update — skip search, sync only, then review new papers
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode curate --source zotero

# Re-review specific slugs (audit/recovery)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode rebuild --slugs 088,1093 --strict-pdf

# Reclassify only (Phase 3 node-based Hybrid C, no LLM calls)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode reclassify

# Regenerate timelines (narratives + images)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode retime --images all

# Deploy only (requires CF_API_TOKEN + CLOUDFLARE_ACCOUNT_ID)
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode deploy

# Dry run — show execution plan
PYTHONUTF8=1 python pipeline/run_full.py --topic my_topic --mode curate --source web --dry-run

# Local server
cd docs && python -m http.server 8000
```

`--mode` meanings:
- **curate** — review new papers only, preserve existing (most common)
- **rebuild** — regenerate all review.md. Requires `--yes` or `--slugs`
- **reclassify** — keep reviews, reassign categories (node-based)
- **retime** — regenerate narratives + timeline images
- **deploy** — run `prepare_deploy.py` only (split-host: Cloudflare + gh-pages stubs + master code push)

Safety flags: `--strict-pdf` (block fuzzy PDF match), `--slugs A,B,C`, `--dry-run`, `--skip-dedup`, `--dedup-execute`, `--yes`.

---

## Comparison with Karpathy's LLM Wiki

[Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) proposes a powerful concept: "LLM organizes, human curates — persistent knowledge base." Paper Curation shares this philosophy while adding an automated pipeline specialized for academic papers.

| | Karpathy LLM Wiki | Paper Curation |
|---|---|---|
| **Core concept** | LLM organizes, human curates | Same + automated pipeline |
| **Input** | Free-form text, web pages, etc. | Zotero PDFs (academic paper-focused) |
| **Structuring** | User writes markdown manually | 6-section auto-generation (Essence~Evaluation) |
| **Classification** | Manual tagging/folders | Bottom-up auto-classification (HDBSCAN + UMAP) |
| **Search** | Keyword/full-text search | Embedding RAG + natural-language Q&A + Claude answers |
| **Figures** | Not supported | Auto-extracted from PDF + inline display |
| **Visualization** | None | Timeline diagrams + UMAP 2D/3D network |
| **Knowledge compounding** | Wiki-link based | Obsidian wiki-links + notes re-indexed into answers |
| **Deployment** | Local files | Local + static hosting (optional) |
| **Installation** | Manual setup | One-line Claude Code install |
| **Strength** | General-purpose, lightweight, any topic | Paper-specific automation, figures/classification/visualization built-in |
| **Weakness** | Paper metadata/figures need manual handling | May be overkill for non-academic content |

Paper Curation's Obsidian integration implements the LLM Wiki compounding concept directly:

```
Deep Research query -> Obsidian note -> re-index -> your notes cited in next query
```

---

## Requirements

| Category | Items |
|----------|-------|
| **Required** | Python 3.12+, Zotero (API Key + collection + PDFs) |
| **APIs** | Anthropic (Claude Haiku/Sonnet/Opus), Google (Gemini), OpenAI (text-embedding-3-small), Zotero Web API |
| **Python** | anthropic, google-genai, openai, numpy, PyMuPDF, Pillow, requests, scikit-learn, umap-learn |
| **Optional** | Obsidian (notes/Graph View), PaperBanana (timeline images), Zotero Desktop (one-click PDF) |

</details>

---

*Built with Claude Code*
