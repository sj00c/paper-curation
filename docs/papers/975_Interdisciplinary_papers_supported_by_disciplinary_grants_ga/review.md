---
title: "975_Interdisciplinary_papers_supported_by_disciplinary_grants_ga"
authors:
  - "Minsu Park"
  - "Suman Maity"
  - "Stefan Wuchty"
  - "Dashun Wang"
date: "2026.02"
doi: "10.1093/pnasnexus/pgag057"
arxiv: ""
score: 4.0
essence: "350,000개 그랜트와 1.3백만 논문을 분석한 결과, 학제간 그랜트보다 학문 분야별(disciplinary) 그랜트가 지원한 학제간 논문이 더 높은 인용도를 보인다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Park et al._2026_Interdisciplinary papers supported by disciplinary grants garner deep and broad scientific impact.pdf"
---

# Interdisciplinary papers supported by disciplinary grants garner deep and broad scientific impact

> **저자**: Minsu Park, Suman Maity, Stefan Wuchty, Dashun Wang | **날짜**: 2026-02-27 | **DOI**: [10.1093/pnasnexus/pgag057](https://doi.org/10.1093/pnasnexus/pgag057)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3. Impact of interdisciplinary papers as a function of grant interdisciplinarity. a) Interdisciplinary papers from *

350,000개 그랜트와 1.3백만 논문을 분석한 결과, 학제간 그랜트보다 학문 분야별(disciplinary) 그랜트가 지원한 학제간 논문이 더 높은 인용도를 보인다.

## Motivation

- **Known**: 학제간 연구는 혁신과 복잡한 사회문제 해결의 핵심이며, 펀딩 에이전시들이 학제간 연구 지원을 점진적으로 증가시키고 있다.
- **Gap**: 학제간 그랜트가 실제로 높은 영향력의 학제간 연구를 생산하는지에 대한 대규모 실증 분석이 부족하며, 그랜트와 논문의 학제성(interdisciplinarity)을 동시에 측정할 통일된 방법론이 없다.
- **Why**: 그랜트는 과학 발전을 주도하는 핵심 메커니즘이므로, 학제간 그랜트의 효과성을 이해하는 것은 과학 정책과 펀딩 의사결정의 최적화에 필수적이다.
- **Approach**: Dimensions와 Microsoft Academic Graph (MAG)의 통합 데이터베이스를 활용하고, labeled-LDA (labeled-latent Dirichlet allocation) 기반 텍스트 분석으로 그랜트와 논문 모두의 학제성을 Rao-Stirling (RS) diversity로 통일 측정한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3. Impact of interdisciplinary papers as a function of grant interdisciplinarity. a) Interdisciplinary papers from *

- **패러독스 발견**: 학제간 그랜트는 의도대로 학제간 논문을 생산하지만, 평균적으로 더 적은 수의 논문을 산출한다.
- **임팩트 역전**: 학제간 그랜트 지원 학제간 논문이 학문분야별 그랜트 지원 학제간 논문보다 현저히 낮은 인용도를 기록한다.
- **핵심 발견**: 깊은 학문분야별 전문성을 갖춘 그랜트가 지원한 고도로 학제적 논문이 핵심 학문분야 내 및 광범위한 분야로부터 불균형적으로 많은 인용을 받는다.
- **메커니즘 규명**: 이 임팩트 우위는 펀딩 규모, 학문분야 경계 내 아이디어 수용, 협업 형식의 단순한 결과가 아니다.

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Quantifying the level of interdisciplinarity of individual publications and grants. Major publication databases *

- 1985-2009년 26개 국가 164개 기관의 350,000개 그랜트 및 관련 1.3백만 논문 수집
- MAG의 논문 필드 분류와 초록을 이용한 지도학습 기반 labeled-LDA로 각 학문분야의 단어 표현 학습
- 그랜트 초록의 필드별 확률 추정으로 그랜트의 학제성 계산
- 논문의 참고문헌(inspiration) 또는 인용(appeal)의 필드 분포로 논문의 학제성 계산
- Rao-Stirling (RS) diversity 지표를 통해 학제성을 0-1 범위로 정량화
- 인간 평가(human ratings) 및 샘플 외 예측(out-of-sample predictions)을 통한 모델 검증

## Originality

- 그랜트와 논문의 학제성을 동일한 필드 분류 체계 하에서 통일 측정하는 새로운 방법론 개발
- 지도학습 기반 labeled-LDA를 사용하여 그랜트 초록에서 필드별 확률 추정—기존 방법의 한계 극복
- 대규모 다국가·다기관 그랜트-논문 쌍 연결 데이터셋 구축으로 거시적 인과 관계 분석 가능
- 학제성의 다차원 구조(volume, balance, disparity)를 동시에 고려한 정교한 정량화

## Limitation & Further Study

- 분석 기간이 1985-2009년으로 제한되어 최근 펀딩 트렌드 반영 미흡
- 인용도(citation count)만을 영향력 지표로 사용하여 다른 형태의 과학적 영향력(사회적 영향, 특허 응용 등) 미측정
- 그랜트-논문 연결이 acknowledgement 기반으로 제한되어 실제 인과 관계 완전히 파악 어려움
- 후속 연구: (1) 2010년 이후 데이터로 시간 경향 추적, (2) 다양한 영향력 지표 통합, (3) 학제간 그랜트가 낮은 임팩트를 보이는 메커니즘에 대한 심층 질적 분석, (4) 학문분야별·국가별 맥락 차이 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 대규모 다국가 데이터와 혁신적인 측정 방법론을 통해 학제간 연구 펀딩의 역설적 효과를 실증적으로 규명한 중요한 연구이다. 과학 정책과 펀딩 전략 수립에 직접적인 함의를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1111_A_Strategic_Guide_to_White_Space_Analysis_for_Pharmaceutical/review]] — 제약 분야 백색공간 분석과 그랜트-논문 학제간성 분석은 연구 기회 식별의 서로 다른 접근법이다.
- 🔗 후속 연구: [[papers/983_Mapping_Research_Funding_and_Outputs_at_the_Topic_Level_in_t/review]] — 북유럽 연구 자금-성과 매핑에서 학제간 그랜트의 효과성이라는 더 구체적 주제로 확장된다.
- 🏛 기반 연구: [[papers/1002_Public_use_and_public_funding_of_science/review]] — 과학의 공공 이용과 공공 자금 지원 관계 연구가 그랜트 유형별 효과 분석의 이론적 토대를 제공한다.
- 🧪 응용 사례: [[papers/964_Funding_the_Frontier_Visualizing_the_Broad_Impact_of_Science/review]] — 펀딩 영향 시각화 시스템에서 학제간 연구의 학문별 그랜트 지원 효과가 중요한 분석 사례로 활용된다.
- 🏛 기반 연구: [[papers/1043_The_selective_use_of_physics_knowledge_in_policy_how_interdi/review]] — 학제간 연구가 받는 펀딩 지원의 한계를 보여주어, 학제간 물리학이 정책 영향력으로 이어지지 않는 구조적 배경을 설명한다.
- 🧪 응용 사례: [[papers/1110_A_cross-disciplinary_research_framework_at_institution_level/review]] — 학제간 논문이 분야별 지원금으로도 높은 성과를 낸다는 증거가 IFISC 모델의 실효성을 뒷받침하기 때문
- 🧪 응용 사례: [[papers/1120_SciEvo_A_2_Million_30-Year_Cross-disciplinary_Dataset_for_Te/review]] — 학제간 논문의 지원 메커니즘 분석이 30년간 학제간 지식 교류 패턴 이해에 실증적 기초를 제공한다.
- 🧪 응용 사례: [[papers/964_Funding_the_Frontier_Visualizing_the_Broad_Impact_of_Science/review]] — 학제간 논문의 학문별 그랜트 지원 효과 분석이 펀딩 영향 시각화에서 학제성의 구체적 메커니즘을 보여준다.
- 🔗 후속 연구: [[papers/972_Identifying_interdisciplinary_emergence_in_the_science_of_sc/review]] — 학제간 논문이 받는 지원에 대한 분석을 학제간 지식 결합의 출현 식별로 확장한다.
- 🔄 다른 접근: [[papers/983_Mapping_Research_Funding_and_Outputs_at_the_Topic_Level_in_t/review]] — 지역별 자금-성과 관계와 그랜트 유형별 학제간 논문 효과는 서로 다른 펀딩 분석 관점이다.
