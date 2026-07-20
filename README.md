# Paper Curation

**Zotero 컬렉션에 PDF만 있으면, 나머지는 자동입니다.**

논문 PDF → 한국어 구조화 리뷰 → 자동 분류 → 연구 동향 타임라인 → 검색 가능한 사이트 + **Deep Research**(논문 근거 RAG Q&A)까지 — Claude Code가 오케스트레이션하는 개인 논문 큐레이션 파이프라인.

**라이브 데모 — 설치 없이 바로 보기:**

- **Humanoid** — https://paper-curation.jehyunlee.dev/humanoid/
- **Physical AI** — https://paper-curation.jehyunlee.dev/physical-ai/

**핵심 기능 5줄 요약:**

- **리뷰 자동화** — PDF에서 텍스트·Figure를 추출해 Claude가 6개 섹션 한국어 리뷰를 자동 작성
- **분류·네트워크** — SPECTER2 + HDBSCAN + UMAP로 카테고리를 자동 생성·배정하고 D3.js 인터랙티브 네트워크로 시각화
- **Deep Research RAG** — 자연어 질의 → hybrid 검색(BM25+dense) → LLM 답변 + `[N]` 인용, 필요하면 **웹 검색 토글**로 코퍼스 밖 근거까지
- **Audio Overview** — 리뷰·답변을 팟캐스트형 한국어 오디오로(Gemini TTS → 브라우저 MP3, 배포 시 이메일)
- **[paper-curio](https://github.com/jehyunlee/paper-curio)** — Zotero 플러그인에서 PDF AI Chat, 2~6편 비교 리포트, 컬렉션 우클릭 전체 처리(리뷰·분류·내러티브·main/category 타임라인, 배포 제외)

🇬🇧 [English README](README.en.md)

![Paper Curation 파이프라인](workflow.png)

> 🐱 **한 장으로 보는 전체 파이프라인** — 수집부터 배포까지, 고양이들이 대신합니다.

## 목차

- [📖 독자로 둘러보기](#-독자로-둘러보기)
- [🔧 운영자로 설치하기](#-운영자로-설치하기)
- [💰 비용 가이드](#-비용-가이드)
- [기능](#기능)
- [파이프라인](#파이프라인)
- [사용 모드](#사용-모드)
- [문서](#문서) — Setup / Operations(megasearch · 한국 망 우회 · Concurrency) / Architecture
- [발표/참고자료](#발표참고자료)

## 📖 독자로 둘러보기

설치도, API 키도 필요 없습니다. 위 라이브 데모 링크를 열면 바로 열람할 수 있습니다.

- **웹에서 보기** — [Humanoid](https://paper-curation.jehyunlee.dev/humanoid/) · [Physical AI](https://paper-curation.jehyunlee.dev/physical-ai/). 카테고리별 카드, 검색, 타임라인, 논문별 한국어 리뷰 페이지가 모두 정적으로 제공됩니다.
- **Deep Research 사용법** — 토픽 페이지 상단의 검색창에 자연어로 질문하면 됩니다. **검색(retrieval)은 키가 전혀 필요 없습니다** — 질의 임베딩은 서버(worker `/api/embed`)가 대신 계산합니다. 답변 생성만 본인 API 키(BYOK)를 입력하면 되고, Anthropic·OpenAI·Google 키 prefix를 자동 감지해 그중 하나로 근거 답변을 스트리밍합니다. 코퍼스 밖 최신 정보가 필요하면 **웹 검색 토글**을 켜 인라인 링크 인용으로 보강할 수 있습니다.
- **RSS 구독** — 각 토픽은 Atom 피드를 제공합니다: [Humanoid feed](https://paper-curation.jehyunlee.dev/humanoid/feed.xml) · [Physical AI feed](https://paper-curation.jehyunlee.dev/physical-ai/feed.xml). 리더로 구독하면 새로 추가되는 리뷰를 받아볼 수 있습니다.

## 🔧 운영자로 설치하기

Zotero 컬렉션 + PDF + Zotero API key는 필수입니다. Google API 키도 검색 임베딩·Figure 검증·TTS에 필요합니다. Claude 호출은 두 방식 중 하나를 고릅니다.

- **구독 OAuth (권장)** — Claude Pro/Max/Team/Enterprise 구독을 Claude Code OAuth로 사용합니다. Claude Code **>= 2.1.205** 필요. `claude auth login`으로 저장된 로그인 또는 `claude setup-token`으로 받은 env-only `CLAUDE_CODE_OAUTH_TOKEN`을 사용합니다.
- **Console API 키** — `ANTHROPIC_API_KEY`를 쓰며 Anthropic Console의 metered API 과금입니다. NPX 명령에서는 `--auth api-key`를 명시합니다.

> OAuth 토큰은 setup이 저장하지 않습니다. `config.json`에는 `anthropic_auth.mode = "oauth"`만 저장할 수 있습니다. Claude CLI 자체는 API 키를 OAuth보다 우선할 수 있으므로 OAuth 운영 셸에서 `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`을 unset하는 편이 안전합니다. 이 저장소는 OAuth로 선택된 Claude child 호출에서 두 API 자격증명을 제거하고, `auto` 모드에서는 OAuth token/login을 API 키보다 우선합니다.
`npx` 경로에는 Git, Node.js 18+, `conda` 명령(Miniconda/Miniforge)이 필요합니다. NPX가 `py312` 환경 생성과 Python 의존성 설치를 맡습니다.

**권장 설치 — NPX:**

```bash
# 새 클론 + 온보딩
npx --yes github:jehyunlee/paper-curation init --auth oauth --dir paper-curation

# 이미 체크아웃한 저장소에서 설정
npx . setup --auth oauth

# Anthropic Console API 키 과금으로 운영할 때
npx . setup --auth api-key

# 진단
npx . doctor --network

# 실행
npx . run -- --topic my_topic --mode curate --source zotero
```
**`config.json` 생성 규칙:**

- `config.json`은 비밀값이 들어가는 로컬 파일이라 Git에 포함되지 않습니다. 따라서 `clone`/`pull`만으로는 생기지 않습니다.
- **가장 쉬운 방법은 export 없이 `npx . setup --auth oauth`를 실행하고 프롬프트에 Zotero API key를 붙여 넣는 것입니다.**
- `export`는 선택적인 사전 입력입니다. 현재 셸의 환경변수만 설정하며 파일을 만들지 않습니다. 사용할 경우 같은 터미널에서 setup까지 실행해야 합니다.

```bash
cd ~/dev/paper-curation
npx . setup --auth oauth

# 선택: 파일 대신 환경변수를 쓸 때
export ZOTERO_API_KEY=...
export GEMINI_API_KEY=...
npx . setup --auth oauth
```

파일을 열어 한 번에 채우는 방식은 `.env.example`을 사용합니다:

```bash
cp .env.example .env
open -e .env                    # 또는 원하는 편집기로 .env 열기
npx . setup --auth oauth
```

`.env`에는 필수값인 `ZOTERO_API_KEY=`와 `GEMINI_API_KEY=` 두 줄만 있습니다. setup이 Zotero API로 컬렉션을 조회해 번호 선택을 받고, topic alias를 만들고, `pdf_cache/`를 자동 생성합니다. Zotero Storage에 동기화된 PDF는 필요할 때 API key로 cache에 내려받습니다. 로컬 linked attachment만 사용하고 Zotero Storage에 파일이 없다면 고급 설정으로 `ZOTERO_DIR`을 추가할 수 있습니다. `.env`는 Git에서 제외됩니다.

기본 NPX setup은 비용이 드는 파이프라인을 자동 실행하지 않습니다. 첫 실행까지 setup에서 이어서 돌릴 때만 `--run-first`를 명시합니다.
`npx . doctor --network`는 OAuth(`claude auth login`/`CLAUDE_CODE_OAUTH_TOKEN`) 또는 API 키(`ANTHROPIC_API_KEY`) 중 현재 선택한 Claude 인증과 Zotero/Google 연결을 진단합니다.

**수동 conda py312 fallback:**

```bash
git clone https://github.com/jehyunlee/paper-curation.git && cd paper-curation
conda create -n py312 -c conda-forge python=3.12 pip -y
conda activate py312
pip install -r requirements.txt

# OAuth: 저장된 로그인
claude auth login
# 또는 장기 토큰: 먼저 발급한 뒤 출력된 토큰을 env에 설정
claude setup-token
export CLAUDE_CODE_OAUTH_TOKEN='발급된_토큰'

export GOOGLE_API_KEY=...
export ZOTERO_API_KEY=...
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth oauth --no-run

# API 키 대안
export ANTHROPIC_API_KEY=...
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth api-key --no-run
```

OpenAI는 선택입니다. Resend는 배포된 Audio Overview 이메일에만 필요합니다.

사전 준비 체크리스트, config.json 스키마, 설치 확인, 문제 해결 → **[Setup Guide](docs/setup-guide.md)**

## 💰 비용 가이드

> 정확한 실측이 아니라 **오더 오브 매그니튜드(order-of-magnitude) 가이드**입니다. 실제 비용은 논문 편수·본문 길이·타임라인 재생성 빈도·Insights opt-in 여부에 따라 크게 달라집니다.

Claude 비용은 인증 방식에 따라 다릅니다.

- **OAuth (`--auth oauth`)** — Claude Code 구독(Pro/Max/Team/Enterprise)의 사용량 정책을 따릅니다. Anthropic Console API 사용량으로 과금되지 않습니다.
- **API 키 (`--auth api-key`)** — `ANTHROPIC_API_KEY`로 Anthropic Console metered API 과금이 발생합니다. 아래 표는 이 경우의 대략치입니다.

단계별로 쓰이는 모델과 단가(입력/출력, 100만 토큰당):

| 단계 | 모델 | 단가 (입력 / 출력) |
|------|------|------|
| 리뷰 · 연결 · 인사이트 | `claude-sonnet-5` | $2 / $10 (인트로, ~2026-08-31) → $3 / $15 |
| Figure 검증 (vision judge) | `claude-haiku-4-5` | $1 / $5 |
| 타임라인 내러티브 | `claude-opus` (4.8) | $5 / $25 |
| 분류 | — (HDBSCAN + UMAP) | **LLM 호출 0회 → $0** |
| 검색 임베딩 | Google `gemini-embedding-001` | Google 임베딩 요금(소액) |

**편당 리뷰 대략치** — API 키 과금 기준, 리뷰 1편은 논문 본문 발췌 + 프롬프트를 입력, 6섹션 한국어 리뷰를 출력합니다. 대략 입력 ~15k · 출력 ~4k 토큰으로 잡으면:
- 인트로 단가($2/$10): `15k × $2/1M + 4k × $10/1M ≈ $0.03 + $0.04 = ~$0.07`
- 9/1 이후($3/$15): `15k × $3/1M + 4k × $15/1M ≈ $0.045 + $0.06 = ~$0.11`
- 여기에 연결 생성(증분) + Figure 검증(Haiku)까지 얹으면 **편당 대략 $0.05–0.15** 수준입니다.

**월간 운영 대략치** — API 키 과금으로 주간 ~20편(월 ~80편) 사이클 기준:

- 리뷰: 80편 × ~$0.10 ≈ **$8**
- 연결(증분, dirty 논문만) + 카테고리 요약(Haiku) ≈ **$1–3**
- 타임라인(변경된 카테고리만, Opus, 비정기) ≈ **$1–3**
- **합계 ≈ 월 $10–20** 수준 (Insights opt-in `--insights` 또는 전체 타임라인 재생성 시 증가)

> **각주**: Sonnet 5 인트로 단가는 2026-08-31까지이며 **9/1 인트로 종료 후 재평가 예정**입니다. 분류 단계는 LLM을 전혀 호출하지 않으므로(HDBSCAN) 비용이 없습니다. Deep Research 답변 생성은 독자 BYOK라 운영자 비용에 포함되지 않습니다.

## 기능

**Core** — `run_full --mode curate` 한 줄이면 전부 생성됩니다:

| 기능 | 설명 |
|------|------|
| **구조화 리뷰** | PDF에서 텍스트/Figure 추출 → Claude가 6개 섹션(Essence·Motivation·Achievement·How·Originality·Evaluation) 한국어 리뷰 자동 작성 |
| **자동 분류** | Bottom-up 토픽 모델링(SPECTER2 + HDBSCAN + UMAP)으로 카테고리 자동 생성·배정 |
| **같이 보면 좋은 논문** | 임베딩 후보를 Claude가 선별 — 관계 유형 + 한국어 이유 1문장. 망 장애에 강건(multi-round 재시도 + 연결 0개 논문 우선) |
| **Deep Research** | 자연어 질의 → hybrid 검색(BM25+dense) → LLM 답변 + `[N]` 인용. Anthropic·OpenAI·Google 키 자동 감지 |
| **Audio Overview** | 리뷰/답변을 팟캐스트형 한국어 오디오로(Gemini TTS, 브라우저 MP3 인코딩 → 다운로드 + 배포 시 이메일) |
| **타임라인** | 카테고리별 연구 동향 내러티브 + 다이어그램(PaperBanana) + main research timeline. `curate`에서도 누락 산출물은 기본 보강 |
| **지식 축적** | Obsidian 연동 — 메모가 다음 질의에 반영되는 compounding knowledge |
| **논문 검색/등록** | arXiv·Semantic Scholar·OpenAlex 병렬 검색 + Zotero 자동 등록(선택) |

**Option** — 플래그/모드로 켤 때만:

| 기능 | 켜는 법 | 설명 |
|------|---------|------|
| **콘텐츠 배포 (O-1)** | `--mode deploy` | Cloudflare Workers + gh-pages 스텁. 배포 시 Audio 이메일 발송 활성화 — [운영 매뉴얼](docs/operations.md#deploy-option-o-1) |
| **Insights + 네트워크 (O-2)** | `--insights` | 크로스카테고리 인사이트 + UMAP 2D/3D 인터랙티브 네트워크 재생성 |
| **로컬 LLM fallback** | `--local-fallback` | 망 전멸 시 로컬 모델(Ollama 등)로 연결 생성 완결 — [운영 매뉴얼](docs/operations.md#korean-network-workarounds) |
| **워크플로 다이어그램** | `generate_workflow.py` | 상단 고양이 다이어그램 생성(PaperBanana, `--style cat/fairy/academic`) |

**필요한 것**: Zotero 컬렉션 + PDF + Zotero API key + Google API 키 + Claude 인증(OAuth 구독 또는 Anthropic API 키). OpenAI는 선택, Resend는 배포 이메일에만 필요.

## 파이프라인

`run_full.py` 한 줄이 아래 Core 단계를 순서대로 실행합니다 (위 그림이 전체 흐름):

1. **데이터 수집** — Zotero PDF → `text.md` + `figures/` (선택: arXiv·S2·OpenAlex 검색 후 Zotero 등록)
2. **구조화 리뷰** — Claude가 6섹션 한국어 `review.md`
3. **토픽 모델링 + 분류** — SPECTER2 + HDBSCAN + UMAP로 카테고리 자동 생성·배정
4. **같이 보면 좋은 논문** — 임베딩 후보를 Claude가 선별(multi-round 재시도)
5. **카테고리 요약 + 타임라인 내러티브/main·category 다이어그램** & **Deep Research 검색 인덱스**(BM25 + Gemini 임베딩)
6. **토픽 인덱스** `index.html`(Deep Research·Audio Overview 내장) → **로컬 열람**(`serve_local.py`) 또는 **배포**

**브라우저 안에서**: Deep Research(키 자동 감지)와 Audio Overview(Gemini TTS → MP3)가 동작합니다.
**Option 분기**: `--insights`(크로스카테고리 인사이트 + 네트워크) · `--mode deploy`(Cloudflare + gh-pages) · `--local-fallback`(망 전멸 시 로컬 LLM).

단계별 입력·처리·출력 상세 → **[Architecture & Internals](docs/architecture.md)**

## 사용 모드

단일 진입점은 NPX CLI입니다. `--` 뒤 인자는 `pipeline/run_full.py`로 전달됩니다.

```bash
# 로컬 업데이트 — 검색 스킵, 신규/누락 narrative·timeline 기본 보강
npx . run -- --topic ai4s --mode curate --source zotero

# 주간 운영 — 검색 → Zotero 등록 → sync → 신규 리뷰 + timeline 보강
npx . run -- --topic ai4s --mode curate --source web --days 7

# timeline 보강까지 끄고 리뷰/분류만 돌리려면
npx . run -- --topic ai4s --mode curate --source zotero --images skip

# 분류만 / 타임라인만 / 배포만
npx . run -- --topic ai4s --mode reclassify
npx . run -- --topic ai4s --mode retime --images all
npx . run -- --topic humanoid --mode deploy

# 실행 계획 미리보기 / 로컬 서버
npx . run -- --topic ai4s --mode curate --source zotero --dry-run
PYTHONUTF8=1 python pipeline/serve_local.py     # http://localhost:8000 + /api/embed
```

전체 모드 표, 안전 플래그, Concurrency 튜닝, 복구 절차 → **[Operations Manual](docs/operations.md)**

## 문서

| 문서 | 내용 |
|------|------|
| **[Setup Guide](docs/setup-guide.md)** | 사전 준비 · Claude Code/수동 설치 · config.json · 설치 확인 · 문제 해결 |
| **[Operations Manual](docs/operations.md)** | 모드/안전 플래그 · Concurrency · 한국 망 우회(SPECTER2/arXiv/로컬 fallback) · 배포(O-1) · 복구 |
| **[Architecture & Internals](docs/architecture.md)** | 파이프라인 단계 상세 · 신뢰성 설계 · 내부 구조 · Karpathy LLM Wiki 비교 · 요구사항 |
| **[English README](README.en.md)** | Full English documentation |

## 발표/참고자료

이 프로젝트는 **AAiCON 2026** (국립중앙과학관, 2026.06.25–26)에서 발표되었습니다.

| 형식 | 자료 |
|------|------|
| **구두 발표** | [260625_이제현_AAiCon.pdf](docs/public/260625_이제현_AAiCon.pdf) |
| **포스터** | [260625_이제현_AAiCon_poster.pdf](docs/public/260625_이제현_AAiCon_poster.pdf) |
| **AIX 클리닉 1회** | [AIX 클리닉 1회 (KIST 존슨강당, 2026.07.16.)](docs/public/260715_AIX_clinic_paper_curation.pdf) |

---

*Built with Claude Code.* 🐱
