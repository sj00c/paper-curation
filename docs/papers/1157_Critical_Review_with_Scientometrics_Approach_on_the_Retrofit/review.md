---
title: "1157_Critical_Review_with_Scientometrics_Approach_on_the_Retrofit"
authors:
  - "Bonisha Borah"
  - "Hirak Jyoti Hazarika"
date: "2026"
doi: "10.1177/01678329261415740"
arxiv: ""
score: 4.0
essence: "LLM을 과학 논문의 품질 검사기로 활용하여 전체 리뷰 생성 대신 비판적 오류와 부실성 문제를 자동으로 식별하는 기준선 접근법과 평가 프레임워크를 제시한다."
tags:
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Computational_Bibliometric_Analysis"
  - "sub/Scientific_Language_Model_Development"
  - "topic/scisci"
---

# Critical Review with Scientometrics Approach on the Retrofitting Strategies for Reinforced Concrete Structures

> **저자**: Bonisha Borah, Hirak Jyoti Hazarika | **날짜**: 2026 | **DOI**: [10.1177/01678329261415740](https://doi.org/10.1177/01678329261415740)

---

## Essence


LLM을 과학 논문의 품질 검사기로 활용하여 전체 리뷰 생성 대신 비판적 오류와 부실성 문제를 자동으로 식별하는 기준선 접근법과 평가 프레임워크를 제시한다.

## Motivation

- **Known**: 최근 LLM이 peer review 프로세스를 지원할 수 있다는 관심이 증가하고 있으며, 기존 연구들은 LLM 생성 리뷰의 품질을 인간 리뷰와 비교 평가해왔다. 하지만 LLM이 인간 리뷰어를 모방하는 방식은 책임감 없는 사용을 악화시킬 위험이 있다.
- **Gap**: 기존 연구는 LLM이 인간과 같은 방식으로 전체 리뷰를 생성하는 시나리오에만 집중했으며, LLM을 보조 도구로서 특정 하위 작업(critical error 검출)에 활용하는 대안적 접근이 부족하다. 또한 도메인 전문가 모집의 어려움으로 인한 체계적 평가 방법이 미흡하다.
- **Why**: peer review crisis로 인한 검토 부담 증가 속에서 LLM을 책임감 있게 활용하여 리뷰어의 시간을 절감하고 도메인 전문성에 집중하게 할 수 있으며, 이는 논문의 신뢰성을 보장하는 데 중요하다.
- **Approach**: WITHDRAWNARXIV 데이터셋(1,225개 사례)을 활용하여 PDF, OCR, LaTeX 기반의 세 가지 기준선 방식을 제안하고, LLM-as-a-judge 패러다임을 적용한 자동 평가 파이프라인으로 도메인 전문가 모집 비용을 우회한다.

## Achievement


- **WITHDRAWNARXIV-CHECK 데이터셋 구축**: 1,225개의 검증된 critical error 사례를 포함하는 새로운 벤치마크 데이터셋 개발
- **자동 평가 프레임워크**: LLM judge들을 활용한 확장 가능한 Hit Rate@k, Mean Hit Rate@k, Average Precision@k, Mean Average Precision@k 메트릭 제시
- **모델 성능 평가**: o3 등 주요 reasoning LLM들의 critical error 검출 성능과 API 비용 비교 분석
- **공개 자료**: 데이터셋, 코드, 모델 출력물의 공개로 향후 연구 기반 제공

## How


- WITHDRAWNARXIV에서 '치명적 오류' 범주의 6,018개 논문 선별", 'Gemini 2.5 Flash를 사용한 자동 스크리닝으로 2,190개로 필터링
- 수작업 검증으로 비영문, 템플릿 오류, 검출 불가능한 문제 제거하여 최종 1,225개 확정
- 20% 테스트 셋(245개), 80% 훈련/검증 셋(980개)으로 분할
- PDF 첨부, OCR 결과, LaTeX 스크립트 기반 세 가지 입력 방식 구현
- 각 LLM checker가 논문당 최대 5개의 critical problem 도출하도록 지시
- m=2개의 LLM judge가 독립적으로 생성 문제의 정확성 검증
- majority voting으로 hit 여부 결정 및 hit rate, precision 계산

## Originality

- **LLM-as-checker 패러다임**: 기존의 LLM-as-reviewer에서 벗어나 질문 검사 도구로서의 새로운 역할 정의
- **LLM-as-judge 자동 평가**: 도메인 전문가 부재 상황에서 reasoning LLM들을 평가자로 활용한 창의적 솔루션
- **WITHDRAWNARXIV-CHECK 데이터셋**: 저자 retraction comments를 기반으로 구성된 새로운 벤치마크 자료
- **다중 입력 방식 비교**: PDF, OCR, LaTeX 세 가지 접근법의 체계적 비교로 실제 활용 시나리오 반영

## Limitation & Further Study

- **도메인 특성 미반영**: 일반적인 task instruction 사용으로 수학·물리 중심 데이터셋의 특성을 충분히 활용하지 못함
- **LaTeX 의존성**: 88%의 논문만 LaTeX 가용하며, 이미지 처리 미지원으로 정보 손실 발생
- **평가 방법의 한계**: LLM judge 간 일관성 부족 가능성과 'exact match' 기준의 엄격성이 실제 오류 검출 능력을 과소평가할 수 있음", '**데이터셋 편향**: arXiv withdrawn paper 중심으로 다른 학문 분야(생물학, 사회과학 등)의 대표성 부족
- **후속 연구**: (1) 도메인 특화 prompt engineering 적용, (2) OCR 기반 접근법 검증, (3) 인간 평가자와의 hybrid 평가, (4) 다양한 retraction reason 카테고리에 대한 세분화된 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 peer review process에 LLM을 책임감 있게 통합하기 위한 실질적이고 혁신적인 접근을 제시하며, 자동 평가 파이프라임과 새로운 벤치마크 데이터셋으로 향후 연구의 토대를 마련했다. 다만 도메인 특화 최적화와 평가 방법론의 견고성 강화가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1214_The_Story_is_Not_the_Science_Execution-Grounded_Evaluation_o/review]] — 논문 품질 검증을 LLM 기반 비판적 검토와 실행 기반 평가라는 서로 다른 접근법으로 수행
- 🧪 응용 사례: [[papers/1166_Emerging_Trends_in_Cybersecurity_Machine_Learning_as_a_Game-/review]] — 과학계량학적 접근법을 사이버보안 분야 문헌의 품질 검사에 구체적으로 적용하는 사례
- 🔗 후속 연구: [[papers/987_Meta-assessment_of_Bias_in_Science/review]] — 과학 연구의 편향성 메타 평가를 LLM을 활용한 자동화된 품질 검사로 확장
- 🔄 다른 접근: [[papers/1192_Large_language_models_and_responsible_research_evaluation_an/review]] — LLM을 활용한 연구 평가에서 전체 리뷰와 비판적 오류 검출이라는 다른 접근법을 비교한다
- 🏛 기반 연구: [[papers/1162_DREAM_Deep_Research_Evaluation_with_Agentic_Metrics/review]] — 연구 평가 프레임워크의 기본적인 방법론적 토대를 제공한다
- 🔗 후속 연구: [[papers/1057_Which_stylistic_features_fool_ChatGPT_research_evaluations/review]] — ChatGPT 연구 평가의 한계를 극복하는 구체적 해결책을 제시한다
- 🏛 기반 연구: [[papers/1166_Emerging_Trends_in_Cybersecurity_Machine_Learning_as_a_Game-/review]] — 과학계량학적 분석 방법이 LLM 기반 비판적 검토 시스템의 평가 기준 설정에 기초 제공
- 🔄 다른 접근: [[papers/1134_A_scientometrics_survey_of_machine_learning_and_neural_netwo/review]] — 심혈관질환과 건물 개보수 분야는 기계학습 응용에 대한 서로 다른 도메인의 과학계량학적 접근이다.
- 🏛 기반 연구: [[papers/1162_DREAM_Deep_Research_Evaluation_with_Agentic_Metrics/review]] — LLM 기반 과학 논문 품질 평가의 기초 개념을 에이전트 기반 평가로 발전시킨 연구
- 🔄 다른 접근: [[papers/1214_The_Story_is_Not_the_Science_Execution-Grounded_Evaluation_o/review]] — 논문 검증을 LLM 기반 텍스트 분석과 코드/데이터 실행 검증이라는 상호 보완적 방법으로 수행
- 🧪 응용 사례: [[papers/1150_Characterization_of_a_Workload_Generator_for_Content-based_P/review]] — 시스템 성능 특성화 방법론을 논문 품질 평가 시스템에 적용한다
