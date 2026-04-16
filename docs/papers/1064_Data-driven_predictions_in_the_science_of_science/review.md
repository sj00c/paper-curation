---
title: "1064_Data-driven_predictions_in_the_science_of_science"
authors:
  - "Aaron Clauset"
  - "Daniel B. Larremore"
  - "Roberta Sinatra"
date: "2017.02"
doi: "10.1126/science.aal4217"
arxiv: ""
score: 4.0
essence: "본 논문은 과학의 사회적 프로세스를 데이터 기반으로 분석하는 '과학의 과학(Science of Science)' 분야를 조사하고, 과학적 발견의 예측가능성에 대한 현황과 한계를 논의한다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Science_Policy_Funding"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Clauset et al._2017_Data-driven predictions in the science of science.pdf"
---

# Data-driven predictions in the science of science

> **저자**: Aaron Clauset, Daniel B. Larremore, Roberta Sinatra | **날짜**: 2017-02-03 | **DOI**: [10.1126/science.aal4217](https://doi.org/10.1126/science.aal4217)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. How unexpected is a discovery? Scientific discoveries vary in how unexpected they were relative to existing know*

본 논문은 과학의 사회적 프로세스를 데이터 기반으로 분석하는 '과학의 과학(Science of Science)' 분야를 조사하고, 과학적 발견의 예측가능성에 대한 현황과 한계를 논의한다.

## Motivation

- **Known**: 과학 공동체의 발전과 자원 배분을 위해 미래 발견의 예측이 필요하며, 디지털 기술의 발전으로 인용, 생산성, 경력 궤적 등의 풍부한 데이터가 가용해졌다.
- **Gap**: 발견의 예측가능성에 대한 정량적 이해가 부족하며, 전문가 판단 중심의 예측과 데이터 기반 예측의 정확도 차이가 명확하지 않다.
- **Why**: 과학 자원의 효율적 배분과 연구비 지원 결정, 인사채용 등 다양한 의사결정에서 발견의 예측가능성 이해가 핵심적이기 때문이다.
- **Approach**: 인용 데이터(citations), 연구자 채용 패턴(faculty hiring), 과학적 생산성(productivity), 주요 발견의 시기(timing of discoveries) 등 4가지 영역에서 정량적 패턴을 식별하는 데이터 기반 분석을 수행했다.

## Achievement


1. **선호적 연결(Preferential Attachment) 메커니즘**: 현시성과 우연의 긍정적 피드백이 인용 분포를 설명하며, 개별 논문의 인용 누적 진화를 예측할 수 있음
2. **생산성 피크의 시기성**: 대부분의 연구자들에게 최고 생산성이 경력 초기 8년 내에 집중되는 패턴 발견
3. **발견의 시기적 무작위성**: 150명 물리학자의 발행 이력 분석 결과, 주요 발견이 경력의 어느 시점에서나 발생 가능함을 확인
4. **Sleeping Beauties 현상**: 250만 개의 출판물 분석으로 장시간 미주목 후 갑자기 주목받는 발견들이 모든 학문 분야에 존재함을 입증

## How


- 현대 서지 데이터베이스(Google Scholar, PubMed, Web of Science 등)에서 인용 수, 출판 기록, 경력 궤적 데이터 수집
- 선호적 연결 모델 및 수정 버전(논문의 최근성과 내재적 매력도 제어)을 통한 인용 진화 시뮬레이션
- 대규모 코호트(2,300+ 컴퓨터과학 교수, 10,000명 조사자) 비교 분석
- 100년 규모의 역사적 출판 데이터 메타분석으로 장기 패턴 추출
- 네트워크 분석과 계산적 도구를 이용한 논문 내용 자동 분류 및 과학적 진전 정량화

## Originality

- **학제적 통합**: 과학사, 사회학, 계량경제학, 네트워크 과학을 결합한 체계적 프레임워크 제시
- **규모의 대표성**: 개별 사례 대신 수십만 개의 경력과 수백만 개의 논문을 통계적으로 분석
- **예측의 한계 명시**: 선호적 연결로 설명 불가능한 예외(sleeping beauties)와 근본적 불예측성을 구체적으로 제시
- **새로운 발견-발견자 분리 관점**: 발견 자체의 예측가능성과 발견자의 예측가능성을 구분하는 분석 틀 제안

## Limitation & Further Study

- **데이터 제약**: 측정 가능한 정량적 지표(인용, 생산성)에 편향되어 있으며, 숨겨진 요인(개인의 직관, 운, 학파 효과 등)을 충분히 포착하지 못함
- **배경 효과**: 교수 채용의 예측 성능이 낮으며, 이는 데이터 부족이 아닌 근본적 불예측성일 가능성 존재
- **sleeping beauties의 미해결 과제**: 발견의 각성 시점이 과학 전반의 진전에 의존하므로 사전 예측이 불가능할 수 있음
- **선택 편향**: 과학적 영향의 정의가 인용에 국한되어, 장기 사회적 영향이나 학문 외 가치는 미반영
- **후속 연구 제안**: (1) 정성적 인터뷰나 숨겨진 변수 측정을 통한 데이터 확충 (2) 특정 분야(생의학, 물리학)의 발견 메커니즘 차이 분석 (3) 예측 결과의 과학 공동체 피드백 효과 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 과학적 발견의 예측가능성에 관한 중요한 질문을 체계적으로 접근하되, 어떤 발견은 예측 가능하고 어떤 발견은 근본적으로 불예측적인지를 실증적으로 구분함으로써 과학 정책과 자원 배분에 실질적 통찰을 제공한다.

## Related Papers

- 🧪 응용 사례: [[papers/998_Predicting_Scientific_Breakthroughs_Based_on_Structural_Dyna/review]] — 과학적 발견의 예측 가능성 이론을 구조적 역학 기반으로 실제 구현한다.
- 🔗 후속 연구: [[papers/1020_Scientific_prize_network_predicts_who_pushes_the_boundaries/review]] — 과학상 수상 네트워크 분석을 통해 과학 발전 예측의 새로운 지표를 제시한다.
- 🏛 기반 연구: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 과학의 과학 분야의 데이터와 방법론에 대한 종합적 분석이 과학적 발견의 예측 가능성 연구의 방법론적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1019_Science_of_science/review]] — 과학의 과학 분야를 다루지만, 전반적 개관보다는 데이터 기반 예측이라는 특정 접근법의 현황과 한계에 집중한다.
- 🔗 후속 연구: [[papers/1066_Accelerating_science_with_human-aware_artificial_intelligenc/review]] — 데이터 기반 과학 예측의 한계를 인간 중심 AI로 극복하여, 과학자의 전문성을 통합한 예측 모델의 성능 향상을 보여준다.
- 🔗 후속 연구: [[papers/1019_Science_of_science/review]] — 과학의 과학 분야에서 데이터 기반 예측의 구체적인 방법론과 응용을 보여줍니다.
- 🧪 응용 사례: [[papers/1022_SciSciGPT_advancing_humanAI_collaboration_in_the_science_of/review]] — 과학의 과학에서 예측 가능성 연구를 AI 협력 시스템으로 실제 구현한다.
- 🔗 후속 연구: [[papers/931_AI-Driven_Automation_Can_Become_the_Foundation_of_Next-Era_S/review]] — 데이터 기반 과학 예측을 AI 자동화로 확장하여 과학학 연구의 완전 자동화 실현
- 🔗 후속 연구: [[papers/1066_Accelerating_science_with_human-aware_artificial_intelligenc/review]] — 과학의 과학에서 데이터 기반 예측의 한계를 인간 전문성 통합을 통해 극복하여, 예측 성능을 400% 향상시키는 구체적 방법을 제시한다.
- 🔄 다른 접근: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 과학의 과학 분야를 다루지만, 예측 가능성보다는 데이터, 측정, 실증 방법론의 종합적 분석에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/962_Forecasting_high-impact_research_topics_via_machine_learning/review]] — 과학학에서 데이터 기반 예측을 구체적인 연구 주제 임팩트 예측으로 발전시킨다
- 🏛 기반 연구: [[papers/963_Forecasting_the_future_of_artificial_intelligence_with_machi/review]] — 과학의 과학에서 데이터 기반 예측 연구의 이론적 배경과 방법론적 기반을 제공한다.
