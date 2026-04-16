---
title: "1214_The_Story_is_Not_the_Science_Execution-Grounded_Evaluation_o"
authors:
  - "Xiaoyan Bai"
  - "Alex Baumgartner"
  - "Haojia Sun"
  - "Ari Holtzman"
  - "Chenhao Tan"
date: "2026"
doi: "10.48550/arXiv.2602.18458"
arxiv: ""
score: 4.0
essence: "논문 내러티브만으로는 감지할 수 없는 연구의 문제점을 발견하기 위해, 코드와 데이터를 함께 검증하는 execution-grounded evaluation 프레임워크를 제안하고 MechEvalAgent를 구현했다."
tags:
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Computational_Bibliometric_Analysis"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scientific_Language_Model_Development"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bai et al._2026_The Story is Not the Science Execution-Grounded Evaluation of Mechanistic Interpretability Research.pdf"
---

# The Story is Not the Science: Execution-Grounded Evaluation of Mechanistic Interpretability Research

> **저자**: Xiaoyan Bai, Alex Baumgartner, Haojia Sun, Ari Holtzman, Chenhao Tan | **날짜**: 2026 | **DOI**: [10.48550/arXiv.2602.18458](https://doi.org/10.48550/arXiv.2602.18458)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. (a) Execution-grouned evaluation uncovers failures that narrative-alone review misses. In this example, Failur*

논문 내러티브만으로는 감지할 수 없는 연구의 문제점을 발견하기 위해, 코드와 데이터를 함께 검증하는 execution-grounded evaluation 프레임워크를 제안하고 MechEvalAgent를 구현했다.

## Motivation

- **Known**: 기존 동료 심사 체계는 논문 내러티브에만 집중하며, AI 에이전트의 대량 연구 생산으로 인해 재현성 검증의 어려움이 증가하고 있다.
- **Gap**: 현존하는 AI 기반 논문 평가 시스템들은 내러티브의 일관성만 검사하고 실제 실행 가능성, 코드 정확성, 결과 재현성을 종합적으로 검증하지 못한다.
- **Why**: AI가 생성하는 대량의 연구 결과와 암묵적 할루시네이션으로 인해 과학적 엄밀성이 위협받고 있으며, execution-grounded 평가는 인간 리뷰어가 놓치는 문제를 자동으로 감지할 수 있다.
- **Approach**: mechanistic interpretability를 테스트 대상으로 하여 plan, report, code, data, walkthrough로 구성된 표준화된 연구 산출물을 정의하고, coherence, reproducibility, generalizability의 세 가지 차원에서 평가하는 MechEvalAgent를 개발했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. (a) Execution-grouned evaluation uncovers failures that narrative-alone review misses. In this example, Failur*

- **Execution-grounded evaluation framework**: 내러티브와 실행 자원을 결합하여 plan-implementation 일관성, 코드 실행 가능성, 결과 재현성, 일반화 가능성을 체계적으로 검증하는 첫 프레임워크
- **MechEvalAgent 구현**: 인간 전문가와 80% 이상의 일치도를 달성하며 인간 리뷰어가 놓친 51개의 추가 문제를 식별
- **인간 리뷰 초과 성능**: 87개 중 67개의 인간 식별 실패를 포착하고 동시에 인간이 감지하지 못한 51개의 methodological 문제 발견
- **효율성 증대**: 인간 리뷰어의 평균 2.2시간 대비 더 빠른 평가 속도 달성

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of the MechEvalAgent framework. Re-*

- **표준화된 연구 산출물**: 인간 작성 논문에서 plan과 report를 추출하고, AI 생성 결과물에서는 연구 trace까지 포함하는 unified standard 정의
- **Coherence 평가**: consistency와 instruction following 체크로 내부 일관성 검증 (9개 체크리스트 항목)
- **Reproducibility 평가**: execution quality (코드 실행 가능성, 계산 정확성)와 replication quality (독립적 재현 가능성) 검증 (11개 체크리스트 항목)
- **Generalizability 평가**: 새로운 모델, 새로운 데이터, 관련 작업에 대한 일반화 가능성 테스트 (3개 체크리스트 항목)
- **Multi-agent 아키텍처**: 각 평가 차원별로 전문화된 에이전트가 관련 입력을 처리하도록 설계

## Originality

- 코드와 데이터 실행을 포함한 execution-grounded evaluation을 처음으로 제안하여 기존 narrative-alone 평가의 한계를 극복
- plan-implementation 일관성 검증을 통해 goal drift나 silent methodology replacement 감지 가능
- mechanistic interpretability 분야에 맞춘 특화된 평가 프레임워크를 구현하되, 일반화 가능한 설계로 다른 과학 분야 적용 가능성 제시

## Limitation & Further Study

- mechanistic interpretability 분야의 30개 연구 산출물에만 평가를 수행하여 다른 AI 분야로의 일반화 가능성 미검증
- execution-grounded evaluation을 위해 코드, 데이터, walkthrough 등 추가 산출물이 필수이나, 현실의 논문 제출 과정에 이를 강제하는 메커니즘 부재
- AI 에이전트의 평가 능력이 인간 전문가에 의존적이며, 평가 기준의 주관성이 완전히 제거되지 않음
- 매우 새로운 방법론이나 예외적 경우에 대한 평가 신뢰도가 검증되지 않음
- **후속 연구**: 다양한 scientific domain으로 프레임워크 확장, 학술 출판 시스템과의 통합 방안 모색, execution-grounded evaluation의 false positive/negative 비율 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 재현성 위기 시대에 AI 에이전트를 평가자로 활용하는 혁신적 접근을 제시하며, execution-grounded evaluation으로 인간 리뷰어가 놓치는 51개의 문제를 식별하여 과학적 엄밀성 강화의 실질적 경로를 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1157_Critical_Review_with_Scientometrics_Approach_on_the_Retrofit/review]] — 논문 검증을 LLM 기반 텍스트 분석과 코드/데이터 실행 검증이라는 상호 보완적 방법으로 수행
- 🏛 기반 연구: [[papers/1162_DREAM_Deep_Research_Evaluation_with_Agentic_Metrics/review]] — 실행 기반 평가가 에이전트 기반 연구 평가 시스템의 핵심 검증 메커니즘으로 활용
- 🧪 응용 사례: [[papers/925_1500_scientists_lift_the_lid_on_reproducibility/review]] — 재현성 위기 문제를 해결하기 위해 코드와 데이터 실행 검증이라는 구체적 솔루션 제시
- 🔗 후속 연구: [[papers/1175_Figures_as_Interfaces_Toward_LLM-Native_Artifacts_for_Scient/review]] — 코드와 데이터 검증 기반 평가와 LLM-native figures의 기계 판독성을 결합하면 과학 연구의 투명성과 재현성을 획기적으로 향상시킬 수 있다.
- 🏛 기반 연구: [[papers/958_Estimating_the_Reproducibility_of_Psychological_Science/review]] — 심리학의 재현성 평가 연구가 제공하는 실험 검증 방법론이 execution-grounded evaluation 프레임워크 설계에 핵심적인 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1157_Critical_Review_with_Scientometrics_Approach_on_the_Retrofit/review]] — 논문 품질 검증을 LLM 기반 비판적 검토와 실행 기반 평가라는 서로 다른 접근법으로 수행
- 🔗 후속 연구: [[papers/1162_DREAM_Deep_Research_Evaluation_with_Agentic_Metrics/review]] — 실행 기반 평가의 한계를 에이전트 기반 메트릭으로 보완하여 더 포괄적인 연구 평가 제시
- 🔗 후속 연구: [[papers/1175_Figures_as_Interfaces_Toward_LLM-Native_Artifacts_for_Scient/review]] — LLM-native figures의 기계 판독성과 execution-grounded evaluation의 코드 검증 기능을 결합하여 과학 재현성을 크게 향상시킬 수 있다.
