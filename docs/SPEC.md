# Paper Curation 공학 명세(SPEC)

- 기준일: 2026-08-20
- 규범 상태: 구현과 검증이 따라야 할 계약

## 문서 경계

| 문서 | 소유 질문 | 링크 |
|---|---|---|
| PRD | 왜 만들며 사용자가 무엇을 얻는가 | [PRD.md](PRD.md) |
| SPEC | 구현이 만족해야 할 정확한 공학 계약은 무엇인가 | 이 문서 |
| HANDOFF | 지금 무엇이 사실이며 다음 세션은 무엇을 하는가 | [HANDOFF.md](HANDOFF.md) |

충돌은 소유권으로 해결한다. **PRD=why/what, SPEC=how/contract, HANDOFF=current state**. ‘구현됨’ 표시는 2026-08-20 현재 코드 상태일 뿐, 이 명세의 완료 선언이 아니다.

## 1. 규범 범위와 기준

현재 fork가 유일한 향후 제품 기준이다. 과거의 one-time upstream intake는 역사적 입력일 뿐이며, 지속적인 upstream fetch, merge, rebase, 동기화 또는 호환성은 계약이 아니다.

설치 가능한 `src/paper_curation` 패키지와 `paper-curation` CLI가 공식 인터페이스다. `pipeline/run_full.py`는 공식 CLI로 직접 위임하는 얇은 **공식-CLI 파일명 wrapper**만 허용한다. `pipeline/run_update_force.py` 및 관련 operator script는 레거시/operator 확장으로 남아 있으며 제품 업무 로직의 source of truth가 아니다.

## 2. 계층과 의존성

의존성은 안쪽으로만 향한다: CLI·composition·orchestration → application → domain. Domain은 CLI, 네트워크, 파일시스템, 렌더러와 provider SDK를 알지 못한다. Application은 port와 use case를 소유하며 `pipeline`, concrete adapter, provider SDK를 import하지 않는다. Integration, retrieval, rendering, config, deployment는 domain/application 계약을 구현한다. concrete adapter 조립은 하나의 composition root만 수행한다. side effect는 application/orchestration의 명시적 계획에 의해 adapter에서만 발생한다.

각 책임은 다음과 같다.

- `domain`: 논문·서지·identity·분류의 순수 모델, 규칙, 오류.
- `application`: Core, setup, update, diagnostics, enhancement, serve/deploy, workspace 및 bibliography use case와 port 계약.
- `config`: 제품 manifest, 설치 설정, 실행 선택의 parse·검증·migration.
- `integrations`: Zotero, PDF/텍스트, review provider, persistence, server, deployment 등의 외부 adapter.
- `rendering`: 패키지 static resource로 로컬 정적 결과를 렌더링.
- `retrieval`: lexical/dense retrieval 계약과 adapter.
- `orchestration`: 선언적 실행 모델·runner.
- `pipeline`: 호환 wrapper 또는 명시적 operator 확장만.

**구현됨:** 위 패키지 경계와 composition root가 존재하며, import 경계 테스트가 있다. **남은 계약:** 레거시 operator 확장이 제품 업무 로직을 완전히 벗어나도록 축소·제거하는 일이다.

## 3. Core 계약

Core는 반드시 다음 순서를 유지한다.

1. `IDENTIFY`: `(source_id, scope_id, record_id)`로 정확히 한 record를 확인한다.
2. `MATERIALIZE_SOURCE`: 명시 attachment 또는 유일한 PDF attachment만 물질화한다.
3. `EXTRACT_TEXT`: 선택 extractor로 검증 가능한 비어 있지 않은 텍스트를 만든다.
4. `GENERATE_REVIEW`: 정확히 선택된 Core provider와 model로 필수 review를 만든다.
5. `WRITE_SIDECAR`: 서지, 텍스트·리뷰의 provenance와 선택 provider/model을 기록한다.
6. `RENDER_PAGE`: review와 sidecar에서 로컬 페이지를 만든다.
7. `COMMIT_RECEIPT`: 검증된 산출물 및 evidence를 원자적으로 canonical 위치에 승격한다.

각 stage evidence에는 stage, 입력 식별 또는 fingerprint, artifact reference/fingerprint, 비밀이 아닌 provider/model ID 및 정제된 진단만 남긴다. credential, raw provider response, 논문 전문은 일반 receipt에 넣지 않는다. 모든 필수 artifact와 evidence가 검증된 경우에만 Core가 성공이다.

실패 상태는 stage별 안정 코드로 구분한다. 미선택 독립 기능은 `SKIPPED`, 필수 선행 실패 때문에 실행할 수 없는 기능은 `BLOCKED`이며 서로 대체하지 않는다. batch는 record별 결과를 독립 보존하고 Core 실패가 하나라도 있으면 non-zero 종료한다.

### 재개와 원자성

현재 입력과 adapter/provider/model fingerprint에 일치하는 **연속된 Core prefix**만 재사용한다. 누락·비연속 evidence, 검증 실패 evidence 또는 다른 review provider/model의 evidence는 거부한다. 영향을 주는 extractor/provider/model 변경은 해당 stage부터 재실행한다. receipt 없는 기존 결과는 자동 신뢰하지 않는다.

산출물은 논문별 staging 위치에 작성하고, Core 전체 검증 뒤 page·sidecar·receipt를 함께 atomic replace/commit한다. 실패는 이전 완료 결과를 삭제하거나 부분 결과로 덮어쓰지 않는다.

**구현됨:** Core stage 순서, 고유 record/PDF 선택, provider/model resume 불일치 거부, prefix evidence 검증, record별 batch 결과 및 receipt commit port가 구현되어 있다. **필수 검증:** 실제 adapter 조합에서도 atomic publish와 resume fingerprint 계약을 계속 보장해야 한다.

## 4. 자료원, Zotero 및 workspace

Core identity는 source-neutral하게 `source_id`, `scope_id`, `record_id`, `attachment_id`를 사용한다. v1 composition은 Zotero를 제공한다. PDF 결정은 explicit attachment ID 또는 정확히 하나의 PDF attachment뿐이다. 다중 PDF의 임의 선택, 기본 fuzzy title matching, 선택되지 않은 OA/provider 전환, 검증되지 않은 PDF의 성공 처리는 금지한다.

Zotero transport는 `local-sqlite` 또는 `zotero-storage`를 명시 선택한다. local-sqlite는 로컬 SQLite 경로와 로컬/linked PDF를 사용하며 Zotero API credential을 요구하지 않는다. zotero-storage는 API/Storage 인증을 요구한다. Zotero 변경은 별도 선택 capability이며 읽기 전용 source와 혼동하지 않는다.

workspace는 설치별 로컬 경로로 설정, cache, PDF, DB, staging, receipt, 생성물을 소유한다. 이들은 repository에 추적하지 않는다. package static resource는 package data로 제공하며 caller 작업 디렉터리의 임의 resource에 의존하지 않는다.

## 5. provider, 비용 및 enhancement

Core review provider는 `claude-code-oauth`, `anthropic-api`, `local-model` 중 정확히 하나이며 model도 비어 있지 않아야 한다. `local-model` endpoint는 credential 없는 HTTP(S) loopback endpoint여야 한다. 선택 provider의 인증·실행 조건은 실행 전 확인하며 비용 분류(`LOCAL`, `REMOTE_UNMETERED`, `METERED`)를 노출한다. 실패 시 다른 provider 또는 model을 instantiate하거나 호출하지 않는다.

각 enhancement는 `enabled=true`와 정확한 `selected_provider`가 모두 필요하다. credential 존재만으로 활성화하거나, 선택되지 않은 provider를 생성·호출해서는 안 된다. enhancement 실패는 Core를 보존하고 의존 단계는 `BLOCKED`가 된다.

**현재 구현 상태:** composition은 enabled enhancement가 하나라도 있으면 “selected enhancements are not installed” 설정 오류로 거부한다. production enhancement adapter는 설치·배선되지 않았으므로, enhancement를 구현됨으로 광고해서는 안 된다. Core와 로컬 운영 경로만 현재 composition 대상이다.

## 6. 설정 계약

설정은 엄격한 allow-list schema로 세 층을 분리한다.

1. **제품 manifest(추적 가능):** schema version, 지원 capability, adapter/provider ID, 비밀 없는 기본 동작, 최소 runtime.
2. **설치 설정(untracked):** workspace, source/transport, scope mapping, Core provider/model, topic profile, publication, 선택 capability/provider와 credential 참조 또는 로컬 값.
3. **실행 선택(일회성):** record, attachment, 이번 enhancement, rebuild/repair 범위.

알 수 없는 key, 잘못된 type, 빈 필수값, 허용되지 않은 provider/transport, 비활성 feature의 provider, local-sqlite의 누락 SQLite 경로를 거부한다. collection alias는 단일 상대 directory name이어야 한다. source는 현재 `zotero`만, transport는 `local-sqlite` 또는 `zotero-storage`만 허용한다.

주제·기관·사용자명·홈 경로·collection ID·모델 순서·prompt 스타일·배포 계정·수신자·코퍼스 DB·생성 페이지를 제품 코드 기본값으로 넣지 않는다. topic profile 또는 설치 설정/로컬 workspace가 소유한다.

## 7. 공식 CLI와 side effect

공식 명령은 `setup`, `migrate`, `inspect`, `doctor`, `build`, `update`, `serve`, `query`, `validate`, `repair`, `deploy`다.

- `setup`: workspace, Zotero source/transport/scope, Core provider/model, 선택 기능, publication을 선택·검증하고 설정 및 Core smoke를 준비한다.
- `migrate`: 기본 preview이며 `--execute`일 때만 설치 설정을 변경한다.
- `inspect`: read-only로 선택, 비용, 예상 외부 호출, workspace와 누락 조건을 표시한다.
- `doctor`: 기본 read-only·비네트워크다. Core 결함은 오류, 비활성 optional은 오류가 아니며 활성 optional 결함은 해당 기능 오류다.
- `update`: 선택 record에 Core를 실행하고, 성공 record에만 선택 enhancement를 시도한다.
- `build`: 설치 로컬 산출물만 만든다.
- `serve`, `query`, `validate`: 로컬 결과의 제공·조회·검증을 수행한다.
- `repair`: 기본 preview, `--execute`일 때만 쓰며 대상·영향을 먼저 보고한다.
- `deploy`: public publication 설정과 명시 명령이 모두 있을 때만 외부 공개를 수행한다.

`build`와 `update`는 절대로 deploy하지 않는다.

## 8. 서지 identity, 보안 및 개인정보

서지 identity는 source record identity와 독립적으로 DOI 및 정규화된 저자·제목·연도 근거를 사용하며, 불확실하거나 충돌하는 candidate를 임의 병합하지 않는다. affiliation 및 cited-by intake도 provenance와 ambiguity를 보존하고 source identity를 덮어쓰지 않는다.

credential은 repository, static output, URL, log, receipt에 기록하지 않는다. 설치 secret/config은 로컬·최소 권한으로 둔다. browser BYOK는 page memory에만 존재하며 Web Storage, URL, static output에 쓰지 않는다. 로그는 allow-list 구조화 필드와 정제 오류만 남긴다. public deploy 전 secret, 로컬 경로, email 및 credential slot 누출을 검사한다.

## 9. 비기능 계약

- **신뢰성:** record별 독립 실행, 가능한 atomic write, 재실행 시 중복·충돌 없는 결과.
- **관찰성:** stage 시작·완료·실패·시간, 비밀 없는 adapter/provider ID, 재실행 범위.
- **성능:** record 병렬화 가능성, provider별 concurrency 제한, Core를 지연시키지 않는 corpus-wide optional, fingerprint 재사용.
- **이식성:** 공식 workstation은 Conda `py312`; macOS arm64 우선 검증; machine path 비포함.
- **유지보수성:** source/extraction/provider/persistence/rendering을 단일 모듈에 혼합하지 않고, use case는 fake port로 검증 가능해야 한다.

## 10. migration·레거시 경계

과거 pipeline의 범용 알고리즘(저자 identity, affiliation 정규화, evidence/provenance, DOI 오탐 방지, synthetic 계약)은 현재 fork에서 유지·검증할 수 있다. 특정 운영자 corpus, 기관 registry, 작업 노트, 생성 이미지, person/topic/machine 기본값, 공식 CLI 우회 script는 제품 기준에 포함하지 않는다.

레거시 기능은 adapter 또는 공식 CLI 동작으로 완전히 대체된 뒤 삭제해야 하며, 신구 구현을 병렬 source of truth로 유지하지 않는다. `run_update_force.py`는 아직 남은 operator extension이므로 이를 공식 흐름으로 문서화하거나 새 제품 동작의 근거로 삼지 않는다.

## 11. 검증 매트릭스와 release gate

필수 검증 범위는 다음과 같다.

| 범주 | 반드시 증명할 계약 |
|---|---|
| Core/use case | 순서, 산출물, 고유 provider/model, substitution 0회, stale/non-prefix resume 거부, BLOCKED, atomic commit |
| Zotero/PDF/text/provider adapter | local SQLite와 Storage, explicit/multiple/missing PDF, 유효/손상 PDF, extraction·auth·timeout·schema 실패, receipt 비밀/전문 미포함 |
| CLI | setup, inspect read-only, doctor Core/optional 구분, update 단일·다중·부분 실패, migration/repair preview 대 execute, build/update no-deploy |
| 분야 중립 | 서로 다른 두 synthetic topic·workspace·taxonomy·locale에서 코드 수정 없이 실행하고 topic/person/machine 누출 없음 |
| browser/security | 로컬 페이지 및 asset, 필수 review·서지 표시, secret·로컬 경로·email 비노출 |

출시에는 clean local setup의 setup/doctor, 한 논문의 전체 Core, provider 미선택 사전 실패, 미선택·fallback 호출 0회, record별 결과 보존, enhancement 실패 후 Core 보존, import boundary, synthetic topic, untracked local data, 얇은 `run_full.py`, legacy source-of-truth 제거, 전체 Python/CLI/security/browser gate, build/update-deploy 분리가 모두 필요하다.

현재 gate 결과와 미완료 작업은 [HANDOFF.md](HANDOFF.md)가 소유한다.
