---
title: "1047_Theory_and_Practice_of_the_g-index"
authors:
  - "Leo Egghe"
date: "2006"
doi: "10.1007/s11192-006-0144-7"
arxiv: ""
score: 4.0
essence: "h-지수의 개선 버전인 g-지수를 제안하고, 상위 g개 논문이 함께 최소 g²개의 인용을 받은 최대 순위 g로 정의하여 상위 논문들의 인용 성과를 더 잘 반영한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Egghe_2006_Theory and Practice of the g-index.pdf"
---

# Theory and Practice of the g-index

> **저자**: Leo Egghe | **날짜**: 2006 | **DOI**: [10.1007/s11192-006-0144-7](https://doi.org/10.1007/s11192-006-0144-7)

---

## Essence


h-지수의 개선 버전인 g-지수를 제안하고, 상위 g개 논문이 함께 최소 g²개의 인용을 받은 최대 순위 g로 정의하여 상위 논문들의 인용 성과를 더 잘 반영한다.

## Motivation

- **Known**: Hirsch의 h-지수는 과학자의 전체 인용 성과를 단일 수치로 측정하는 간단하고 견고한 지표이지만, 최상위 인용 논문들의 지속적인 인용 증가를 반영하지 못하는 한계가 있다.
- **Gap**: h-지수는 상위 h개 논문이 선정된 후 추가 인용 증가를 무시하므로 상위 논문의 영향력을 충분히 반영하지 못한다. 이를 극복하면서 h-지수의 장점을 유지하는 지표의 필요성이 있다.
- **Why**: 인용 성과 측정에서 최상위 논문들의 높은 인용 영향을 적절히 반영하는 것은 과학자의 가시성(visibility)과 전체적인 학문적 기여도를 더 정확하게 평가하기 위해 중요하다.
- **Approach**: 논문 순위 r에서 누적 인용 수 G(r)이 r²보다 크거나 같은 최대 순위 g를 정의하는 g-지수를 도입하고, Lotka 법칙에 기반한 수학적 이론을 개발하여 일반 공식을 유도한다.

## Achievement


- **g-지수의 유일성 정리**: 모든 논문 집합에 대해 g-지수는 항상 유일하게 존재함을 증명 (정리 II.2.1)
- **g ≥ h 성질**: g-지수가 항상 h-지수보다 크거나 같음을 증명하여 상위 논문의 인용을 더 잘 반영함을 보임
- **Lotka 법칙 기반 공식**: 주어진 Lotka 지수 α에 대해 g = T¹/(α-1)[(α-2)/(α-1)]^(α/(α-1))의 명시적 공식 도출
- **Price 메달리스트 실증 분석**: 실제 과학자 데이터(Price 메달리스트)를 이용하여 g-지수가 h-지수보다 과학자들 간의 구분을 더 잘 제공함을 시연

## How


- 연속 변수를 사용한 수학적 정의: 순위-빈도 함수 g(r)과 누적 아이템 함수 G(r) 정의
- 존재 정리 증명: H(r) = G(r)/r이 단조감소함을 보이고 중간값 정리 적용
- Lotka 법칙 f(j) = C/j^α 하에서 역함수 관계식 g(r) = (C(α-1)/r)^(1/(α-1)) 유도
- 적분을 통한 누적 인용 수 계산: G(g) = g²을 만족하는 g 구간 [0,T]에서의 수치 계산
- 실제 논문 데이터(Web of Knowledge)를 이용한 구체적 예시 계산 및 검증

## Originality

- h-지수의 직관적 한계를 명확하게 지적하고 이를 해결하는 간단하면서도 우아한 수정안 제시
- g-지수가 항상 존재하고 유일하다는 수학적 증명을 통한 이론적 기초 확립
- Lotka 법칙에 기반한 명시적 공식 유도로 이론과 실제의 연결
- 기존 h-지수 연구들과 달리 누적 인용 수를 제곱과 비교하는 혁신적 아이디어

## Limitation & Further Study

- Lotka 법칙이 모든 인용 분포에 적용되지 않을 수 있으며, α > 2 조건의 제한성
- Web of Knowledge 데이터베이스의 불완전성(일부 인용 누락, 특정 저널만 포함) 반영 미흡
- g-지수의 시간적 변화 추이와 h-지수와의 차이가 실제 평가에 미치는 영향에 대한 심층 분석 부재
- 다양한 학문 분야별 α 값의 차이와 그에 따른 g-지수 해석의 차이 미탐구
- 후속 연구: g-지수의 동적 특성, 다양한 데이터베이스 적용, 타 지표들과의 비교 분석 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 인용 성과 측정의 중요한 지표인 h-지수의 명확한 한계를 식별하고, 수학적으로 엄밀하게 증명된 g-지수를 제안하여 scientometrics 분야에 실질적인 기여를 한다. 이론과 실제의 균형잡힌 제시가 뛰어나다.

## Related Papers

- 🔄 다른 접근: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — NK 복합 지수가 g-지수의 인용 중심 평가를 넘어 경력 기간과 저자 기여도까지 통합하는 확장된 접근법을 제시한다.
- 🏛 기반 연구: [[papers/933_An_index_to_quantify_an_individuals_scientific_research_outp/review]] — h-지수 개발이 g-지수 설계의 직접적 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — 상대지표 기반 보편적 인용 분포가 g-지수의 절댓값 기반 평가와 다른 정규화된 비교 방법을 제시한다.
- 🔗 후속 연구: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — 상대 인용 비율이라는 새로운 지표가 g-지수와 함께 인용 기반 영향력 측정의 다양한 접근법을 보여준다.
- 🏛 기반 연구: [[papers/1003_Quantifying_Long-term_Scientific_Impact/review]] — 장기적 과학적 영향력 정량화의 필요성을 기반으로, 상위 성과 논문들의 인용을 더 잘 포착하는 지표 개발의 중요성을 보여준다.
- 🔄 다른 접근: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — g-지수가 상위 논문의 인용 성과를 강조하는 반면, NK 지수는 경력 기간과 저자 기여도까지 통합적으로 평가한다.
- 🔗 후속 연구: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — 기존의 g-지수 등 인용 기반 지표를 발전시켜 분야별 정규화를 통한 더 정확한 영향력 측정을 가능하게 한다.
- 🔄 다른 접근: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — g-지수의 절댓값 기반 평가와 달리 상대지표를 통한 학문분야 간 객관적 비교 방법을 제시한다.
- 🔗 후속 연구: [[papers/928_A_General_Theory_of_Bibliometric_and_Other_Cumulative_Advant/review]] — 누적 우위 이론의 베타 함수 모델링이 g-index와 같은 새로운 서지학적 지수 개발의 수학적 토대가 됩니다.
- 🔗 후속 연구: [[papers/933_An_index_to_quantify_an_individuals_scientific_research_outp/review]] — h-index를 보완하기 위해 개발된 g-index는 고인용 논문의 영향을 더 강하게 반영하는 대안적 지표입니다.
- 🔄 다른 접근: [[papers/937_Authorship_titles_and_open_access_as_drivers_of_citation_per/review]] — 인용 성과 측정을 위한 다른 지표인 g-index를 통해 저자십 효과를 평가할 수 있다.
- 🔄 다른 접근: [[papers/1210_Scilit_with_the_Integrated_Impact_Indicator_Assessment/review]] — 학술 영향력 측정에서 기존 g-index와 새로운 I3/I3N 지표의 서로 다른 접근법을 비교할 수 있습니다.
