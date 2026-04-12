# Paper Curation

학술 논문 자동 큐레이션 파이프라인: Zotero 연동 → 구조화 리뷰 → 토픽 분류 → 시각화 → Deep Research → Obsidian 지식 축적.

Zotero 컬렉션에서 논문을 가져와 Claude/Gemini API로 한국어 구조화 리뷰를 작성하고, Bottom-up 토픽 모델링(HDBSCAN + UMAP)으로 자동 분류합니다. 로컬에서 검색 가능한 HTML 인덱스, Deep Research(자연어 질의 + Claude 답변 + 인용), Obsidian 연동(메모 축적 + wiki-link)을 통해 **개인 연구 지식이 계속 쌓이는 시스템**을 만듭니다.

<a href="#english">English</a>

![파이프라인 워크플로우](workflow.png)

---

## 핵심 기능

### 🔬 Zotero → 자동 구조화 리뷰

Zotero 컬렉션의 논문 PDF를 자동으로 가져와 Claude Haiku가 **6개 섹션으로 구조화된 한국어 리뷰**를 작성합니다. Jargon(기술 용어·모델명·데이터셋·알고리즘)은 원문 그대로 유지합니다.

- **Essence** — 핵심 요약 (1-2문장)
- **Motivation** — Known / Gap / Why / Approach
- **Achievement** — 주요 성과
- **How** — 방법론
- **Originality** — 독창성
- **Evaluation** — 5축 평가 (Novelty, Technical, Significance, Clarity, Overall)

각 리뷰에는 PDF에서 추출한 Figure(최대 5장)가 인라인으로 삽입되며, 관련 논문(Related Papers)이 자동으로 연결됩니다.

### 🧠 Deep Research — 자연어 질의 + Claude 답변

토픽 페이지의 검색창에서 **🧠 Deep** 모드로 전환하면, 자연어 질의에 대해 `review.md` + `text.md`(원문 발췌)를 근거로 Claude가 **카테고리 요약 스타일의 답변**을 생성합니다.

- **클라이언트-사이드 RAG**: `_search_index.json` (section-aware chunk + OpenAI embedding) → cosine similarity + 논문 다양성 캡
- **원문 발췌 (로컬)**: 상위 10개 논문의 `text.md`를 fetch해 시약 이름·분량·온도·실험 조건 같은 **정량적 디테일**까지 답변에 포함
- **시간 필터**: `"2023년 이후"`, `"최근 1년"`, `"since 2024"` 등 한/영 자연어 인식
- **답변 분량**: Short / Medium (2x) / Long (5x)
- **모델**: Claude Haiku 4.5 (빠름) / Sonnet 4.5 (품질)
- **Extended Thinking**: 답변 전 내부 계획 수립 — 화면에는 진행 상태만 표시
- **내보내기**: 📋 Copy / ⬇ Download `.md` / 🔗 Open in new tab
- **📄 Zotero PDF 원클릭**: References 옆 `📄 PDF` 버튼 클릭 → Zotero 데스크탑이 해당 논문 PDF를 바로 열기 (`zotero://open-pdf` deep link)

### 📝 Obsidian 연동 — 지식 축적 (Compounding Knowledge)

> [Karpathy의 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 개념을 반영했습니다 — LLM이 정리하고 사람이 큐레이션하는 persistent knowledge base. Paper Curation은 여기에 자동 파이프라인(Zotero → 리뷰 → 분류)과 embedding RAG(Deep Research)를 결합합니다.

Deep Research 답변 아래 **📝 Obsidian** 버튼을 클릭하면 Obsidian이 열리면서 새 노트 파일이 자동 생성됩니다:

- **`## My Notes`** 섹션이 맨 위에 — 바로 자기 생각을 적을 수 있음
- **`[[papers/slug/review|제목]]`** wiki-link로 논문 리뷰에 직접 연결
- 파일명은 `PCDR_{날짜}-{질의요약}.md` 형식으로 자동 생성
- **`docs/` 폴더를 Obsidian vault로** 열면 논문 리뷰 + 내 메모를 하나의 workspace에서 탐색
- Obsidian **Graph View**로 질의 ↔ 논문 관계 시각화 — 여러 질의에 걸치는 허브 논문이 한눈에

**지식 축적 흐름**:
```
Deep Research 질의 → 📝 Obsidian 버튼 → 메모 작성/저장
       ↓
docs/notes/ai4s/PCDR_*.md 생성 (git-ignored, 로컬 전용)
       ↓
build_search_index.py 재실행 → 내 메모가 인덱스에 포함
       ↓
다음 Deep Research 질의 → 내 메모가 답변에 인용됨 (compounding ✨)
```

각 논문에도 개별 메모를 추가할 수 있습니다 — `docs/papers/{slug}/notes.md` 파일을 만들면 해당 논문의 "My Notes" 청크로 자동 인덱싱됩니다.

### 🕸 네트워크 시각화

모든 논문을 UMAP 2D/3D 좌표로 배치한 인터랙티브 네트워크:

- D3.js (2D Force-directed, viewport 독립 레이아웃) + Three.js (3D UMAP, OrbitControls)
- 카테고리·관계 필터, 시간 필터, Hub/Bridge 하이라이트
- **Ego Network**: 특정 논문 클릭 → 이웃 논문만 표시 (2D ↔ 3D 전환에도 유지)
- **Reset View** 버튼으로 zoom/pan/카메라 원위치 복원

---

## 작동 방식

1. **검색** — 다중 소스 병렬 검색 (arXiv, Semantic Scholar, OpenAlex) + 중복 제거 + 관련성 필터링
2. **등록** — Zotero에 PDF와 함께 자동 등록
3. **리뷰** — PDF에서 텍스트/Figure 추출, 구조화된 한국어 리뷰 생성 (Claude Haiku). Jargon은 원문 유지 (예: `diffusion model을 사용한다`)
4. **토픽 모델링** — SPECTER2 임베딩 → HDBSCAN 클러스터링 → TF-IDF 키워드 추출 → Sonnet 작명 → Ward linkage 카테고리 그룹핑
5. **인사이트** — 카테고리 요약, 카테고리 간 논문 연결 관계 추출 (cross-category connections)
6. **시각화** — 연구 타임라인 (Opus 내러티브 + PaperBanana 이미지) + UMAP 2D/3D 네트워크 (D3.js + Three.js)
7. **검증** — 깨진 그림 참조, 링크, 포맷 문제 자동 수정
8. **인덱스 빌드** — 토픽 인덱스 HTML (카드, 검색, 타임라인, Deep Research UI) + Deep Research RAG 인덱스 (section-aware chunking + OpenAI embedding)

### 핵심 기술

| 구성 요소 | 기술 |
|-----------|------|
| 클러스터링 | sklearn HDBSCAN (min_cluster_size 자동 조정, target 40~100 sub-topics) |
| 차원 축소 | UMAP (2D + 3D 좌표 동시 생성) |
| 키워드 추출 | sklearn TF-IDF (c-TF-IDF 대체) |
| 카테고리 그룹핑 | Centroid cosine distance + Ward linkage (공간 기반, LLM 작명만) |
| Outlier 처리 | 가장 가까운 centroid 카테고리에 자동 배정 (Other 0편) |
| 네트워크 시각화 | D3.js (2D/Force, viewport 독립 레이아웃 + Reset View) + Three.js (3D UMAP, OrbitControls) |
| 논문 연결 | 카테고리 내 + 카테고리 간 cross-category connections |
| Deep Research | OpenAI text-embedding-3-small (int8 L2 quantised) + Anthropic Claude (Extended Thinking) |

## 파이프라인 단계

| 단계 | 스크립트 | 설명 | 출력 |
|------|---------|------|------|
| 0a | `search_papers.py` | arXiv/S2/OpenAlex 병렬 검색 + 중복 제거 + 관련성 필터 | `_search_results.json` |
| 0b | `register_zotero.py` | Zotero 등록 + PDF 다운로드 | Zotero items + PDFs |
| 1 | `run_update_force.py` | 전체 배치: Zotero 가져오기 → PDF 파싱 → Figure 추출 → 리뷰 | `papers/{slug}/review.md` |
| 2 | `build_papers_index.py` | 모든 review.md에서 마스터 인덱스 재구축 | `_papers_index.json` |
| 3 | `topic_modeling.py` | Bottom-up 토픽 모델링: HDBSCAN → TF-IDF → Sonnet 작명 → Ward 카테고리 | `_new_classification.json` |
| 4 | `build_category_summaries.py` | 카테고리 설명 + 세부 주제 생성 | `_category_summaries.json` |
| 4.5 | `extract_insights.py` | 크로스 카테고리 인사이트 + 논문 연결 관계 | `_paper_connections.json` |
| 5 | `generate_timelines.py` | 타임라인 내러티브 + PaperBanana 이미지 | `category_timeline_*.png` |
| 5.5 | `generate_network.py` | UMAP 2D/3D + D3/Three.js 네트워크 시각화 | `network.html` |
| 6 | `validate_papers.py` | 빌드 후 검증 + 자동 수정 | 수정된 review.md/figures |
| 7 | `review_to_html.py` | review.md → index.html 변환 (정규 템플릿) | `papers/{slug}/index.html` |
| 8 | `build_topic_index.py` | 토픽 인덱스 (카드, 검색, 타임라인, Deep Research UI) | `{topic}/index.html` |
| 8.5 | `build_search_index.py` | Deep Research RAG 인덱스 (section-aware chunking + OpenAI embedding) | `{topic}/_search_index.json` |

## 사용법

### 로컬 서버 실행

```bash
cd docs
python -m http.server 8000
```

브라우저에서 `http://localhost:8000/{topic}/` 으로 접속. Deep Research의 API 키 모달은 **자동 스킵** (`_local_keys.json`이 빌드 시 자동 생성).

### 실행 모드

```bash
# 전체 파이프라인 (검색 + 등록 + 리뷰 + 인덱스 빌드)
PYTHONUTF8=1 python pipeline/run_update_force.py --topic my_topic

# 업데이트 (신규 논문만, 기존 카테고리/리뷰 유지)
PYTHONUTF8=1 python pipeline/run_update_force.py --topic my_topic --resume

# 전체 카테고리 재분류
PYTHONUTF8=1 python pipeline/run_update_force.py --topic my_topic --category
```

### Obsidian vault 설정

`docs/` 폴더를 Obsidian vault로 열면 논문 리뷰 + 내 메모를 하나의 workspace에서 탐색/편집/연결할 수 있습니다:

1. Obsidian 실행 → "Open folder as vault" → `docs/` 선택
2. `papers/` — 자동 생성된 리뷰 (읽기용)
3. `notes/` — 내 메모 (자유 편집)
4. Deep Research → 📝 Obsidian → 자동으로 `notes/{topic}/PCDR_*.md` 생성
5. Graph View (`Ctrl+G`)에서 질의 ↔ 논문 관계 시각화
   - 필터: `path:notes/{topic} file:PCDR` (Deep Research 결과만)
   - Local Graph (Depth 2): 특정 질의 → 인용 논문 → 다른 질의 연결

## 프로젝트 구조

```
paper-curation/
├── pipeline/                ← 파이프라인 스크립트
│   ├── lib/                 ← 공유 모듈 (categories, paperbanana, dateutil)
│   ├── run_update_force.py  ← 전체 파이프라인 실행
│   ├── build_search_index.py ← Deep Research RAG 인덱스 빌드
│   ├── build_topic_index.py ← 토픽 인덱스 + Deep Research UI
│   ├── generate_network.py  ← D3.js/Three.js 네트워크 시각화
│   └── ...                  ← 기타 파이프라인 스크립트
├── docs/                    ← Obsidian vault로도 사용 가능
│   ├── papers/              ← 중앙 저장소 (review.md, figures, notes.md)
│   ├── notes/               ← Personal Notes (git-ignored, 로컬 전용)
│   │   ├── ai4s/            ← PCDR_*.md (Deep Research → Obsidian)
│   │   └── scisci/
│   ├── ai4s/                ← 토픽 뷰 (index.html, 네트워크, 타임라인)
│   └── scisci/              ← 토픽 뷰
├── config.example.json      ← 설정 템플릿
└── CLAUDE.md                ← Claude Code 설정
```

## 설치

**Claude Code 사용 (권장):**

> *"여기에 paper-curation을 설치해줘: https://github.com/jehyunlee/paper-curation"*

Claude Code가 클론, 의존성 설치, Zotero 설정, 스킬 등록, 첫 파이프라인 실행을 자동으로 수행합니다.

<details>
<summary><b>수동 설치</b></summary>

```bash
git clone https://github.com/jehyunlee/paper-curation.git
cd paper-curation
pip install anthropic google-genai openai numpy pymupdf Pillow requests opendataloader-pdf

# ML 스크립트용 Python 3.12 가상환경 (Windows WDAC 대응)
python -m uv venv .venv312 --python 3.12
python -m uv pip install --python .venv312/Scripts/python.exe \
  umap-learn numpy anthropic google-genai openai requests Pillow scikit-learn matplotlib

python pipeline/setup.py
```

`setup.py`가 인터랙티브 설정 마법사를 실행합니다 (config.json 생성, Zotero 연결 테스트, API 키 확인, 스킬 설치, 첫 파이프라인 자동 실행). `OPENAI_API_KEY`는 Deep Research 검색 인덱스 빌드에 필수이며, 환경변수에 없으면 setup이 직접 입력받아 `config.json`에 저장합니다.

</details>

### 사전 준비

- **Zotero**: [API Key 발급](https://www.zotero.org/settings/keys) + 큐레이션할 컬렉션 + Zotero 데스크탑 설치 (PDF 원클릭용)
- **Obsidian**: [다운로드](https://obsidian.md) (메모 편집 + Graph View용)
- **환경변수**: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` 설정 (`OPENAI_API_KEY`는 setup.py가 안내)
- **Python 3.12+**

### 요구사항

- **Python 3.12+**: anthropic, google-genai, openai, numpy, PyMuPDF, Pillow, requests, scikit-learn, umap-learn
- **APIs**: Anthropic (Claude Sonnet/Haiku — 리뷰·분류·인사이트·Deep Research), Google (Gemini — Figure 검증), OpenAI (text-embedding-3-small — Deep Research 인덱스), Zotero Web API
- **Zotero 데스크탑**: PDF 원클릭 열기 (`zotero://open-pdf` deep link)
- **Obsidian** (권장): 메모 편집, wiki-link, Graph View
- **PaperBanana**: [dwzhu-pku/PaperBanana](https://github.com/dwzhu-pku/PaperBanana) (타임라인 이미지용, 선택)

---

<details>
<summary><h2 id="english">English</h2></summary>

Automated academic paper curation pipeline: Zotero → structured review → topic classification → visualization → Deep Research → Obsidian knowledge compounding.

Papers are fetched from a Zotero collection, reviewed via Claude/Gemini APIs, classified using bottom-up topic modeling (HDBSCAN + UMAP), and served locally as a searchable HTML index with Deep Research (natural-language Q&A grounded in paper reviews) and Obsidian integration for persistent personal knowledge.

### Key Features

**🔬 Zotero → Structured Review**: Claude Haiku generates 6-section Korean reviews from PDF text and figures. Technical jargon is kept verbatim in English (e.g. `diffusion model을 사용한다`).

**🧠 Deep Research**: Flip the search box to 🧠 Deep mode to ask free-form questions. Claude answers grounded in `review.md` excerpts + `text.md` raw paper text (local only — for quantitative detail like reagent names, amounts, conditions). Features client-side RAG with OpenAI embeddings, time filters, length presets, Extended Thinking, and export (Copy / Download .md / Open in new tab). Each reference includes a **📄 PDF** button that opens the paper directly in Zotero Desktop via `zotero://open-pdf`.

**📝 Obsidian Integration** (inspired by [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)): Click **📝 Obsidian** on any Deep Research answer to create a new note file (`PCDR_{date}-{query}.md`) in Obsidian with the answer pre-filled and `[[papers/slug/review]]` wiki-links to cited papers. A `## My Notes` section at the top invites you to add your own thinking. Notes are automatically indexed on the next pipeline run, so your ideas compound into future Deep Research answers.

**🕸 Network Visualization**: Interactive UMAP 2D/3D network with category/relation filters, ego network (works across 2D ↔ 3D transitions), and Reset View.

### How It Works

1. **Search** — Multi-source parallel search (arXiv, Semantic Scholar, OpenAlex) + deduplication + relevance filtering
2. **Register** — Auto-register to Zotero with PDF download
3. **Review** — Extract text & figures from PDF, generate a structured Korean review (Claude Haiku)
4. **Topic Modeling** — SPECTER2 embeddings → HDBSCAN clustering → TF-IDF keywords → Sonnet naming → Ward linkage
5. **Insights** — Category summaries, cross-category paper connections
6. **Visualize** — Research timelines + UMAP 2D/3D network (D3.js + Three.js)
7. **Validate** — Auto-fix broken figure refs, links, and formatting issues
8. **Build** — Topic index HTML (cards, search, Deep Research UI) + RAG search index (OpenAI embeddings)

### Usage

```bash
# Run the full pipeline
PYTHONUTF8=1 python pipeline/run_update_force.py --topic my_topic

# Serve locally
cd docs && python -m http.server 8000
# Open http://localhost:8000/{topic}/
```

Open `docs/` as an Obsidian vault to browse reviews, edit notes, and visualize connections in Graph View.

### Installation

```bash
git clone https://github.com/jehyunlee/paper-curation.git
cd paper-curation
pip install anthropic google-genai openai numpy pymupdf Pillow requests opendataloader-pdf
python pipeline/setup.py
```

`setup.py` walks you through config generation, Zotero connectivity, API-key checks (including `OPENAI_API_KEY` for Deep Research), skill installation, and kicks off the first pipeline run.

### Requirements

- **Python 3.12+**: anthropic, google-genai, openai, numpy, PyMuPDF, Pillow, requests, scikit-learn, umap-learn
- **APIs**: Anthropic (Claude), Google (Gemini), OpenAI (embeddings), Zotero Web API
- **Zotero Desktop**: for one-click PDF opening via `zotero://open-pdf`
- **Obsidian** (recommended): note editing, wiki-links, Graph View
- **PaperBanana**: [dwzhu-pku/PaperBanana](https://github.com/dwzhu-pku/PaperBanana) (optional, for timeline images)

</details>

---

*Built with Claude Code*
