# Paper Curation 세션 인계(HANDOFF)

- 기록 시점: 2026-08-20
- 상태: 변경 가능한 실행 인계; 제품 요구사항이나 공학 계약의 소유 문서가 아님

## 문서 경계

| 문서 | 소유 질문 | 링크 |
|---|---|---|
| PRD | 왜 만들며 사용자가 무엇을 얻는가 | [PRD.md](PRD.md) |
| SPEC | 구현이 만족해야 할 정확한 공학 계약은 무엇인가 | [SPEC.md](SPEC.md) |
| HANDOFF | 지금 무엇이 사실이며 다음 세션은 무엇을 하는가 | 이 문서 |

충돌은 소유권으로 해결한다. **PRD=why/what, SPEC=how/contract, HANDOFF=current state**. 현재 fork가 유일한 향후 source of truth이며, one-time upstream intake는 과거 이력이다.

## 1. 목적

현재 fork를 범용 로컬 Paper Curation 하네스로 정리한다. 공식 package/CLI가 Core를 소유하고, 설치별 Zotero·PDF·workspace·credential·생성물은 저장소 밖에 둔다. Core는 선택한 provider/model만 사용하며, 비용 발생 가능 enhancement와 공개 배포는 명시 선택 없이 실행하지 않는다.

## 2. 저장소·브랜치·작업 트리

- branch: `master` (`origin/master` 추적).
- 작업 트리: **대규모 미커밋 변경 집합**. 기존 변경은 사용자 작업으로 취급한다.
- 이 인계 시점에는 documentation split을 포함해 package, pipeline, test, config, 기존 문서에 걸친 변경과 신규 파일이 있다.
- **금지:** 요청 없이는 commit, reset, stash, revert를 하지 않는다.
- corpus, local configuration, credential, local path, generated output은 추가·추적·공개하지 않는다.
- 2026-08-20 정리: `pipeline/tests/fixtures/ultragoal_final_qa.json`(소비자 없는 세션 QA 산출물)을 삭제해 status에 `D`로 남아 있다. untracked 로컬 잔재인 `pipeline/_smoke/`(구 smoke 출력)와 `artifacts/g00*`(구 세션 QA 로그)도 삭제했다. `pipeline/_cache/`, `pipeline/_state/env_probe.json`, `pipeline/_update_force_checkpoint.json`, `config.json`, `docs/_zotero_*.json`은 살아 있는 설치 로컬 데이터라 유지한다.
- 2026-08-20 정리: provider 비용 분류 맵 중복을 제거했다. `cli.py`의 `_review_cost` 사본을 삭제하고 `application/diagnostics.py`의 `review_cost_class`를 단일 소스로 쓴다.

## 3. 구현된 상태

- `paper-curation` CLI와 package가 공식 인터페이스이며, setup/migrate/inspect/doctor/build/update/serve/query/validate/repair/deploy 경로가 있다.
- source-neutral Core use case가 `IDENTIFY → MATERIALIZE_SOURCE → EXTRACT_TEXT → GENERATE_REVIEW → WRITE_SIDECAR → RENDER_PAGE → COMMIT_RECEIPT`를 수행한다.
- Core는 고유 record/PDF, 선택 provider/model, stage evidence, resume prefix 검증, record별 batch 결과 및 receipt commit을 다룬다.
- Zotero local SQLite 및 Zotero Storage adapter, local PDF/text/review/persistence, local serve와 explicit Cloudflare deploy 경로가 있다.
- strict configuration model과 migration/setup/diagnostics/workspace operation 경로가 있다.
- `pipeline/run_full.py`는 package CLI에 직접 위임하는 얇은 공식-CLI 파일명 wrapper다.
- `pipeline/run_update_force.py`는 남아 있는 legacy/operator extension이며 제품 source of truth가 아니다.

## 4. 확정된 핵심 결정

1. 현재 fork만 향후 기준이다. upstream은 재동기화 대상이 아니다.
2. Core review는 정확히 하나의 명시된 provider/model만 사용한다. provider/model fallback은 금지다.
3. credential 존재는 feature 선택이 아니다. build/update는 deploy하지 않는다.
4. source identity는 Zotero에 종속되지 않으며 `(source_id, scope_id, record_id, attachment_id)`를 사용한다.
5. PDF는 explicit attachment 또는 유일한 PDF만 허용한다. 모호성은 실패다.
6. receipt는 provenance와 fingerprint를 남기지만 credential, raw provider response, 논문 전문을 남기지 않는다.
7. workspace 및 사용자 데이터는 install-local·untracked다.
8. enabled enhancement는 현재 production adapter가 없으므로 composition에서 거부한다. 구현됨으로 광고하지 않는다.

## 5. 주요 파일 지도

| 경로 | 현재 역할 |
|---|---|
| `docs/PRD.md` | 제품 intent와 사용자 수용 기준 |
| `docs/SPEC.md` | 규범 engineering contract와 구현/미구현 경계 |
| `docs/HANDOFF.md` | 이 세션의 사실, 검증 결과, 다음 작업 |
| `src/paper_curation/cli.py` | 공식 CLI 명령 진입점 |
| `src/paper_curation/composition.py` | Core·운영·runtime concrete adapter 조립 및 enhancement 거부 |
| `src/paper_curation/application/curate.py` | 단일 논문의 Core stage/port/use case |
| `src/paper_curation/application/update.py` | record별 독립 Core batch 결과 |
| `src/paper_curation/config/models.py` | 엄격한 설치 설정 schema |
| `src/paper_curation/integrations/zotero/` | local SQLite 및 Storage adapter |
| `src/paper_curation/integrations/providers/` | 선택 Core review provider adapter |
| `src/paper_curation/integrations/persistence/` | workspace, artifact, receipt, configuration adapter |
| `src/paper_curation/integrations/deployment/` | 명시적 공개 deployment adapter |
| `pipeline/run_full.py` | thin official-CLI filename wrapper |
| `pipeline/run_update_force.py` | legacy/operator extension; 제품 기준 아님 |
| `pipeline/tests/` | architecture, Core, adapter, CLI, runtime 계약 검증 |

## 6. 검증된 게이트: 최신 관측 결과

다음은 이 인계에 제공된 최신 성공 관측이며, 남은 작업의 완료 선언이 아니다.

| 게이트 | 최신 결과 |
|---|---|
| Python test suite | `1186 passed, 5 warnings, 632 subtests` |
| NPX CLI suite | `14 passed` |
| 정적/배포 hygiene | `compileall`, diff check, wheel build 통과 |
| end-to-end | local E2E 통과 |

경고와 외부 의존 제한:

- 위 결과는 credential 없는 검증 환경의 결과다.
- live Anthropic/Claude, Zotero Storage, Cloudflare smoke는 credential 없이 실행하지 않았다.
- 외부 네트워크 provider의 실제 인증·요금·서비스 가용성은 위 로컬 gate가 대신 증명하지 않는다.
- documentation split 이후에는 호출자가 문서 테스트와 diff hygiene를 검증한다. 이 작업에서 project-wide gate나 formatter는 실행하지 않았다.

## 7. 남은 작업

1. **Enhancement:** enabled enhancement는 production adapter가 설치·배선되지 않아 거부된다. adapter를 실제로 구현·배선·검증하기 전까지 활성 기능으로 취급하지 않는다.
2. **레거시 경계:** `pipeline/run_update_force.py`와 관련 operator script가 아직 남아 있다. 공식 Core와 중복되는 업무 로직을 제거하거나 명시적인 operator-only 경계로 더 축소해야 한다. 테스트 인벤토리: `pipeline/tests`의 85개 테스트 중 31개가 package(`paper_curation`) 계약 테스트, 54개가 레거시 pipeline script 테스트다(`grep -LE "paper_curation" pipeline/tests/test_*.py`로 재현; `test_architecture_boundaries.py`·`test_docs_contract.py`는 package를 import하지 않지만 제품 측 가드다). 레거시 테스트는 폴더 이동 없이 해당 script 제거와 함께 삭제한다.
3. **기준선 정리:** final commit 및 baseline cleanup은 아직 하지 않았다. 요청 없는 commit/reset/stash는 금지다.
4. **실서비스 smoke:** credential이 제공되고 명시적으로 요청될 때에만 live Anthropic/Claude, Zotero Storage, Cloudflare smoke를 수행한다.
5. **출시 조건:** passing current gates와 PRD/SPEC의 모든 release gate 충족은 다르다. 특히 enhancement production adapter와 legacy cleanup이 남아 있으므로 재구축 완료를 선언하지 않는다.

## 8. 다음 세션의 첫 명령과 금지 사항

첫 순서:

```bash
git status --short
```

그 다음 [PRD.md](PRD.md), [SPEC.md](SPEC.md), 이 HANDOFF를 읽고, 변경 범위에 맞는 focused test를 먼저 실행한다. 범위가 충분히 안정된 뒤에만 full test를 실행한다.

명시적 금지:

- secret, local path, corpus, generated output을 repository 또는 문서에 넣지 않는다.
- provider/model fallback을 추가하지 않는다.
- upstream sync, fetch, merge, rebase를 제품 작업으로 수행하지 않는다.
- 요청 없이는 commit, reset, stash를 하지 않는다.

## 9. 새 세션 시작 프롬프트

다음 문장을 새 세션에 그대로 전달할 수 있다.

> `docs/PRD.md`, `docs/SPEC.md`, `docs/HANDOFF.md`를 순서대로 읽고, HANDOFF의 현재 작업 트리를 보존한 채 남은 SPEC 작업을 계속 진행하라. 먼저 `git status --short`와 실제 파일 상태를 확인하고, passing gate를 완료 선언으로 오해하지 말라. 우선순위는 production enhancement adapter 배선, legacy/operator 경계 축소, focused/full 검증이다. provider/model fallback, upstream 동기화, secret·로컬 경로·corpus 추가, 요청 없는 commit/reset/stash는 금지한다.
