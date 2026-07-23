# Paper Curation

**Zotero 컬렉션에 PDF만 있으면, 나머지는 자동입니다.**

논문 PDF → 한국어 구조화 리뷰 → 자동 분류 → 연구 동향 타임라인 → 검색 가능한 사이트 + **Deep Research**(논문 근거 RAG Q&A)까지 — Claude Code가 오케스트레이션하는 개인 논문 큐레이션 파이프라인.

**라이브 데모 — 설치 없이 바로 보기:**

- **Humanoid** — https://paper-curation.jehyunlee.dev/humanoid/
- **Physical AI** — https://paper-curation.jehyunlee.dev/physical-ai/

**핵심 기능 5줄 요약:**

- **리뷰 자동화** — PDF에서 텍스트·Figure를 추출해 Claude가 6개 섹션 한국어 리뷰를 자동 작성
- **분류·네트워크** — SPECTER2 + HDBSCAN + UMAP로 카테고리를 자동 생성·배정하고, `--insights` 사용 시 D3.js 인터랙티브 네트워크까지 생성
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

Zotero 컬렉션 + PDF + Zotero API key와 Google API key가 필요합니다. Claude 호출은 준비된 Claude Code OAuth 또는 Anthropic Console API key 중 하나를 `auto`로 감지하며, 필요하면 setup에서 선택합니다. 특정 인증이나 토픽을 기본값으로 강제하지 않습니다.

현재 체크아웃의 `bin/paper-curation.mjs`가 내부/팀 milestone의 단일 하네스입니다. Node.js 내장 모듈만 사용하며 스킬 설치는 Python/conda 패키지보다 먼저 동작합니다. 공개 GitHub/npm release, 공개 scanner/license 정리, canonical upstream embedding merge는 아직 완료·공개 준비 상태가 아니며, 버전 metadata seam을 통한 audit/migration으로 연기되어 있습니다.

```bash
cd paper-curation

# 1) Python 의존성 없이 현재 체크아웃용 managed skill bundle 설치
node ./bin/paper-curation.mjs skill install

# 2) 키를 shell history에 남기지 않고 입력
cp .env.example .env
open -e .env                    # Linux: ${EDITOR:-vi} .env
```

```dotenv
ZOTERO_API_KEY=발급받은_Zotero_키
GEMINI_API_KEY=발급받은_Google_키
```

```bash
# 3) 현재 사용자 기준으로 새 설정 생성
# 기존 ignored config.json은 fork/worktree 잔재일 수 있으므로 자동 재사용하지 않습니다.
node ./bin/paper-curation.mjs setup --fresh-config

# 4) 의존성/네트워크와 선택된 Anthropic 인증 진단
node ./bin/paper-curation.mjs doctor --network --anthropic-smoke

# 5) setup이 출력한 alias 중 하나로 scratch-only smoke
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy

# 6) 첫 로컬 curate
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy
```

setup은 Zotero 컬렉션을 조회해 하나 이상을 선택받고 각각의 topic alias를 생성합니다. alias는 임의의 Zotero 주제 프로필일 수 있으며 문서 예제나 저장소 기본값으로 고정하지 않습니다. 새 `config.json`은 secret-free로 생성하고, Zotero/Google/Anthropic credential은 `.env` 또는 process environment에서만 공급합니다. 기존 설정이 현재 사용자 것임을 확인한 경우에만 `setup --reuse-config`를 사용합니다. Zotero Storage PDF는 필요할 때 `pdf_cache/`로 다운로드합니다. 로컬 linked attachment는 `.env`의 `ZOTERO_DIR`로 지정할 수 있습니다.

> **프로덕션 경고:** smoke·검증·로컬 실행은 `PAPER_CURATION_NO_DEPLOY=1`과 `--no-deploy`를 함께 사용합니다. 보호를 제거한 production curate는 Cloudflare 설정이 있으면 자동 publish할 수 있습니다. 배포는 명시적인 요청에서만 실행하세요.
>
> ```bash
> node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode deploy
> ```

Console API key를 강제하려면 `.env` 또는 process env에 `ANTHROPIC_API_KEY`를 넣고 `setup --fresh-config --auth api-key`를 사용합니다. OAuth를 강제하려는 경우에만 `--auth oauth`를 사용합니다. `auto`는 준비된 OAuth/API key를 감지하되 OAuth 토큰이나 API key를 config에 저장하지 않습니다.

**Immutable release 이후 GitHub NPX:**

현재 첫 실행 문서는 체크아웃 로컬 Node 하네스만 실행하도록 제공합니다. immutable tag/SHA가 붙은 내부 릴리스가 공지된 뒤에만 해당 릴리스 노트의 고정 ref를 사용하세요. 공개 GitHub/npm 배포와 public-readiness 주장은 연기되어 있으며, `npx --yes github:jehyunlee/paper-curation`처럼 ref 없는 GitHub 실행은 첫 설치 경로로 사용하지 않습니다.

**수동 conda py312 fallback:**

```bash
# 이미 받은 maintainer/fork/PR checkout 루트에서 실행합니다.
cd paper-curation
conda create -n py312 -c conda-forge python=3.12 pip -y
conda activate py312
pip install -r requirements.txt

# 실제 키는 명령행에 쓰지 말고 편집기로 .env에 저장합니다.
cp .env.example .env
open -e .env
claude auth login
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth oauth --no-run

# Anthropic Console API 키 과금 대안:
# 편집기로 .env에 ANTHROPIC_API_KEY를 추가한 뒤 실행합니다.
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
5. **카테고리 요약 + 타임라인 내러티브/main·category 다이어그램** & **Deep Research 검색 인덱스**(BM25 + Gemini 임베딩, `pipeline/lib/search_index_metadata.py` metadata contract)
6. **토픽 인덱스** `index.html`(Deep Research·Audio Overview 내장) → **로컬 열람**(`serve_local.py`) 또는 **명시적 배포**

**브라우저 안에서**: Deep Research(키 자동 감지)와 Audio Overview(Gemini TTS → MP3)가 동작합니다. 기존 검색 인덱스/임베딩 cache metadata가 현재 `search_index_metadata.py` 계약과 맞지 않으면 혼합 사용하거나 자동 rebuild하지 않습니다(never auto-rebuilt). 명시적인 rebuild/audit 지시가 필요합니다.
**Option 분기**: `--insights`(크로스카테고리 인사이트 + 네트워크) · `--mode deploy`(Cloudflare + gh-pages) · `--local-fallback`(망 전멸 시 로컬 LLM).

단계별 입력·처리·출력 상세 → **[Architecture & Internals](docs/architecture.md)**

새 체크아웃에는 originality 평가 기본값이 내장되어 있어 별도 trigger JSON 없이 구조화 리뷰의 Originality 섹션이 생성됩니다. 선택 dependency(Java, PaperBanana, 로컬 LLM 등)는 없으면 안전하게 fallback 또는 기능 생략으로 degrade합니다. TLS 검증은 기본으로 켜져 있으며, 기업 프록시 등에서 필요한 경우 신뢰 CA를 설치하거나 `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`를 사용하세요. 임시 비보안 우회는 명명된 opt-out `PAPER_CURATION_INSECURE_TLS=1` 또는 `network.allow_insecure_tls`+`network.insecure_tls_reason`이 있을 때만 허용됩니다.

## 사용 모드

단일 진입점은 현재 체크아웃의 Node 하네스입니다. `--` 뒤 인자는 `pipeline/run_full.py`로 전달됩니다.

```bash
# 로컬 업데이트 — 검색 스킵, 신규/누락 narrative·timeline 기본 보강
# 배포 억제를 강제하므로 Cloudflare 자격증명이 있어도 publish하지 않습니다.
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy

# 주간 운영 — 검색 → Zotero 등록 → sync → 신규 리뷰 + timeline 보강
# --max-papers는 web 검색/등록 후보 수만 제한하며, Zotero review/post-processing cap이 아닙니다.
# 이 프로덕션 명령은 Cloudflare 자격증명/설정이 있으면 성공 후 자동 publish될 수 있습니다.
node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source web --days 7 --max-papers 20

# timeline 보강까지 끄고 리뷰/분류만 로컬에서 돌리려면
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --images skip --no-deploy

# 특정 슬러그 repair-only/rebuild는 배포 억제를 함께 사용
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode rebuild --slugs 088,1093 --strict-pdf --no-deploy --yes

# 분류만 / 타임라인만 (로컬 실행은 배포 억제)
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode reclassify --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode retime --images all --no-deploy
node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode deploy

# 실행 계획 미리보기 / 로컬 서버 (검증은 배포 억제)
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --dry-run --no-deploy
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
