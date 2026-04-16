---
title: "1032_The_Diversity-Innovation_Paradox_in_Science"
authors:
  - "Bas Hofstra"
  - "Vivek V. Kulkarni"
  - "Sebastian Munoz-Najar Galvez"
  - "Bryan He"
  - "Dan Jurafsky"
date: "2020"
doi: "10.1073/pnas.1915378117"
arxiv: ""
score: 4.0
essence: "과학계에서 소수집단이 다수집단보다 더 높은 혁신율을 보이지만, 그들의 혁신적 기여가 과소평가되고 학업 경력 성공으로 이어지지 않는 다양성-혁신 역설을 규명한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hofstra et al._2020_The Diversity-Innovation Paradox in Science.pdf"
---

# The Diversity-Innovation Paradox in Science

> **저자**: Bas Hofstra, Vivek V. Kulkarni, Sebastian Munoz-Najar Galvez, Bryan He, Dan Jurafsky, Daniel A. McFarland | **날짜**: 2020 | **DOI**: [10.1073/pnas.1915378117](https://doi.org/10.1073/pnas.1915378117)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

과학계에서 소수집단이 다수집단보다 더 높은 혁신율을 보이지만, 그들의 혁신적 기여가 과소평가되고 학업 경력 성공으로 이어지지 않는 다양성-혁신 역설을 규명한다.

## Motivation

- **Known**: 다양성이 혁신을 유도하고 혁신이 학업 경력 성공을 가져온다는 것이 알려져 있다. 그러나 저대표 집단의 학자들이 학계에서 지속적으로 저대표되는 현상이 존재한다.
- **Gap**: 다양성-혁신 관계와 혁신-경력 성공 관계가 동시에 성립한다면, 소수집단 학자들의 경력이 왜 지속적으로 불평등한지에 대한 설명이 부족하다.
- **Why**: 학계의 구조적 불평등을 이해하고, 소수집단의 혁신이 왜 보상받지 못하는지 규명함으로써 학계의 포용성 증진을 위한 근거를 제공한다.
- **Approach**: 약 120만 명의 미국 박사학위 취득자(1977-2015)의 학위논문과 경력 데이터를 연결하여, 자연어처리(NLP)와 기계학습을 이용해 과학적 혁신을 측정하고 인구통계학적 집단별 혁신율과 그 채택률을 분석한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- **혁신의 정량적 측정**: 개념 쌍의 새로운 조합(# new links)과 그 채택률(uptake per new link)을 통해 과학적 혁신과 임팩트를 객관적으로 측정
- **소수집단의 높은 혁신율**: 과소대표 성별(p<0.001) 및 인종(p<0.05)의 학생들이 통념적 개념 연결을 더 많이 도입
- **혁신의 과소평가**: 소수집단의 혁신적 기여가 다른 학자들에게 더 낮은 채택률을 보이며, 동일한 임팩트의 기여도 소수집단이 학업 성공으로 이어질 가능성이 낮음
- **구조적 불평등의 증거**: 학계가 다양성의 역할을 과소평가함으로써 소수집단의 저대표 현상을 지속적으로 재생산

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- ProQuest 학위논문 데이터베이스(약 120만 건)에서 학위논문의 제목, 초록, 메타데이터 추출
- 미국 인구조사(2000, 2010)와 사회보장청 데이터(1900-2016)를 연결하여 성별과 인종 추론
- 자연어처리 기법(구문 추출, 구조적 토픽 모델링)으로 각 논문에서 과학적 개념 식별
- 개념 쌍의 동시 출현을 추적하여 새로운 개념 연결(novel conceptual co-occurrence) 감지
- Web of Science 데이터베이스와 연결하여 학자들의 향후 출판 및 학문 경력 추적
- institution, academic discipline, graduation year를 통제하여 회귀분석(regression analysis) 수행

## Originality

- 근-완전 모집단(near-complete population) 데이터로 120만 명의 박사학위 취득자 추적 - 표본 편향 최소화
- 개념적 재조합(conceptual recombination)을 혁신의 정의로 사용하여 인용지표(citation metrics)의 학문분야별 편향 극복
- 거시적(macroscopic) 과학 생태계 관점에서 개인 수준의 혁신과 사회 구조적 불평등의 연관성을 동시에 분석
- 30년 데이터, 모든 학문분야, 모든 박사학위 수여기관을 포괄하는 장기간 종단(longitudinal) 분석
- 성별과 인종 추론에 이름 신호(name signals) 활용 - 기존 설문조사 방식보다 대규모 적용 가능

## Limitation & Further Study

- 이름 기반 성별/인종 추론의 오분류 가능성 - 특히 교차성(intersectionality)과 시간변화 반영 부족
- 박사학위 취득자 중심 분석으로 학부 및 대학원 수료 후 진로 미포함
- 혁신의 채택이 순수 학문적 메커니즘만 반영하지 않을 수 있음 - 네트워크 효과, 기관 권력 등 미측정 요인 존재
- 미국 박사학위 취득자 중심으로 국제 학자 미포함 - 결과의 일반화 제한
- **후속연구**: 저채택의 명시적 메커니즘(peer review bias, citation patterns) 규명; 시간경과에 따른 혁신 가치 재평가 추적; 학문분야별 상세 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 연구는 대규모 종단 데이터와 자연어처리 기술을 결합하여 학계의 구조적 불평등을 과학적으로 규명했으며, 다양성-혁신 역설이라는 중요한 사회과학 문제에 새로운 통찰을 제공한다. 방법론의 견고성과 정책적 함의로 인해 높은 가치를 지닌 연구이다.

## Related Papers

- 🔗 후속 연구: [[papers/1031_The_Chaperone_Effect_in_Scientific_Publishing/review]] — 출판에서의 샤페론 효과와 함께 소수집단의 혁신 기여 과소평가가 과학계 불평등의 다면적 양상을 보여준다.
- 🏛 기반 연구: [[papers/976_Intersectional_inequalities_in_science/review]] — 교차적 불평등 관점에서 소수집단이 겪는 다양성-혁신 역설을 더 포괄적으로 이해할 수 있다.
- ⚖️ 반론/비판: [[papers/965_Gender-diverse_teams_produce_more_novel_and_higher-impact_sc/review]] — 성별 다양팀의 혁신 효과와 소수집단의 혁신 과소평가가 다양성의 복합적 영향을 대조적으로 제시한다.
- 🔗 후속 연구: [[papers/1035_The_Innovation_Recognition_Paradox_How_Science_Undervalues_t/review]] — 여성 과학자의 혁신 과소평가 문제와 소수집단의 다양성-혁신 역설은 과학계의 체계적 편향을 보여주는 연결된 현상이다.
- 🔗 후속 연구: [[papers/1121_Superstar_Extinctionsupsup/review]] — 슈퍼스타 소멸 현상은 다양성-혁신 역설과 함께 과학계에서 기존 엘리트 구조가 변화하면서 소수집단의 기여가 재평가되는 양상을 보여줍니다.
- 🧪 응용 사례: [[papers/1217_Tracing_the_Evolution_of_Sleep-Related_Behavioural_Outcomes/review]] — 수면 관련 행동 결과의 진화 추적은 다양성-혁신 역설이 특정 연구 분야에서 어떻게 나타나는지 보여주는 구체적 사례입니다.
- 🔗 후속 연구: [[papers/1020_Scientific_prize_network_predicts_who_pushes_the_boundaries/review]] — 과학계 다양성-혁신 역설은 과학상 수상자 예측에서 소수집단의 혁신적 기여가 어떻게 과소평가되는지 보완적 관점을 제공합니다.
- 🔗 후속 연구: [[papers/1031_The_Chaperone_Effect_in_Scientific_Publishing/review]] — 출판 성공에서의 샤페론 효과와 소수집단의 혁신 과소평가가 모두 과학계의 구조적 불평등을 드러낸다.
- 🔄 다른 접근: [[papers/1035_The_Innovation_Recognition_Paradox_How_Science_Undervalues_t/review]] — 여성 과학자와 소수집단 모두 혁신적 기여를 과소평가받는다는 공통된 패턴을 보여준다.
- ⚖️ 반론/비판: [[papers/1110_A_cross-disciplinary_research_framework_at_institution_level/review]] — 다양성-혁신 역설에 대한 제도적 해결책을 제시한다.
- 🔄 다른 접근: [[papers/953_Do_Large_Language_Models_Reduce_Research_Novelty_Evidence_fr/review]] — 과학의 다양성 감소를 LLM 사용과 다양성-혁신 역설이라는 다른 메커니즘으로 각각 설명
- ⚖️ 반론/비판: [[papers/965_Gender-diverse_teams_produce_more_novel_and_higher-impact_sc/review]] — 과학에서 다양성의 긍정적 효과에 대해 다양성-혁신 역설이라는 복잡한 관점을 제시한다
- 🔗 후속 연구: [[papers/972_Identifying_interdisciplinary_emergence_in_the_science_of_sc/review]] — 과학에서 다양성-혁신 역설을 다룬 연구로, 학제간 신흥 분야 출현의 복잡성을 확장 분석할 수 있습니다.
- 🏛 기반 연구: [[papers/976_Intersectional_inequalities_in_science/review]] — 과학에서 다양성-혁신 역설에 대한 이론적 배경을 제공하여 교차적 불평등의 복잡성을 이해할 수 있다.
