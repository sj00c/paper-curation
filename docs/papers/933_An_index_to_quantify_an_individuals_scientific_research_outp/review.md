---
title: "933_An_index_to_quantify_an_individuals_scientific_research_outp"
authors:
  - "J. E. Hirsch"
date: "2005"
doi: "10.1073/pnas.0507655102"
arxiv: ""
score: 5.0
essence: "개인의 과학적 연구 성과를 정량화하기 위해 h-index를 제안한다. h-index는 h편 이상의 인용수를 가진 논문의 개수로 정의되며, 연구자의 생산성과 영향력을 동시에 반영하는 단일 지표이다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Computational_Bibliometric_Analysis"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Research_Reproducibility_Crisis"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hirsch_2005_An index to quantify an individual's scientific research output.pdf"
---

# An index to quantify an individual's scientific research output

> **저자**: J. E. Hirsch | **날짜**: 2005 | **DOI**: [10.1073/pnas.0507655102](https://doi.org/10.1073/pnas.0507655102)

---

## Essence


개인의 과학적 연구 성과를 정량화하기 위해 h-index를 제안한다. h-index는 h편 이상의 인용수를 가진 논문의 개수로 정의되며, 연구자의 생산성과 영향력을 동시에 반영하는 단일 지표이다.

## Motivation

- **Known**: 개별 연구자의 학술적 기여도를 평가하기 위해 총 논문수, 총 인용수, 논문당 평균 인용수 등 다양한 지표들이 사용되어 왔으나, 각각의 지표는 생산성, 영향력, 공저자 효과 등에서 편향성을 갖는다.
- **Gap**: 단일하면서도 생산성과 영향력 모두를 공정하게 반영하고, 서로 다른 경력 단계의 연구자들을 비교 가능하게 하는 평가 지표가 부재하다.
- **Why**: 대학 교원 채용, 펀딩 심사, 상 수상 등 학술 평가 상황에서 연구자의 과학적 기여도를 객관적으로 정량화할 필요성이 있으며, 이는 제한된 자원 배분의 정당성을 위해 필수적이다.
- **Approach**: 출판 기록과 인용 기록이라는 객관적 데이터를 활용하여 새로운 지표 h-index를 정의하고, 물리학자들의 데이터를 실증적으로 분석하여 다른 지표와 비교하고 수학적 모델로 검증한다.

## Achievement


- **h-index 정의 및 개념화**: h편 이상의 인용수를 갖춘 논문의 개수로 정의하여 간단하면서도 강력한 지표 제시
- **기존 지표와의 비교 분석**: 총 논문수, 총 인용수, 논문당 인용수, 고인용 논문 개수 등과 비교하여 h-index의 우월성 입증
- **실증적 검증**: E. Witten (h=110), A.J. Heeger (h=107) 등 저명한 물리학자들의 h-index 계산 및 제시
- **수학적 모델링**: 선형 모델 및 stretched exponential 모델을 통해 h와 총 인용수 관계(Nc,tot = ah²) 도출 및 a값 범위(3-5) 규명
- **학제 간 확장성**: 물리학뿐 아니라 생물학 등 다른 과학 분야에도 적용 가능함을 제시

## How


- Thomson ISI Web of Science 데이터베이스에서 '인용 횟수'로 논문 정렬", '인용수가 논문 순위와 같아지는 지점을 찾아 h-index 결정
- 선형 모델(Nc(y) = N₀ - (N₀-h)y)을 적용하여 이론적 분포 도출
- stretched exponential 분포(Nc(y) = N₀e^(-(y/y₀)^β))로 현실적 모델 구성
- 매개변수 a, β, α를 변화시켜 다양한 연구자 분포 모델링
- h와 경력연수(n)의 관계(h ∼ mn)를 선형 회귀로 분석

## Originality

- 단순하면서도 강력한 h-index 개념 창안 - 이전에 없던 새로운 평가 지표의 개발
- 생산성(논문수)과 영향력(인용수)의 균형을 수학적으로 표현한 혁신적 시도
- 단순 선형 모델에서 stretched exponential 모델로 점진적 정교화
- 총 인용수와 h의 관계식(Nc,tot = ah²) 도출을 통한 이론적 기초 제공
- 경력 단계별 비교 가능성을 고려한 설계(h = mn 관계식)

## Limitation & Further Study

- **공저자 효과**: 여러 저자가 참여한 논문의 경우 개별 기여도 반영 부족
- **학문 분야 간 인용 문화 차이**: 학문 분야별로 인용 관습이 다르기 때문에 cross-field 비교 어려움
- **시간 지체 효과**: 최근 논문은 충분한 인용을 받기까지 시간이 필요하므로 신진 연구자에게 불리
- **'Sleeping Beauty' 논문**: 오랜 시간 인용되지 않다가 이후 높은 인용을 받는 논문의 부정확한 평가", '**리뷰 논문의 과도한 가중**: 리뷰 논문은 높은 인용수를 받지만 순 학문적 기여도와 차이 가능
- **후속 연구**: 학문 분야별 정규화 계수 도입, 저자 기여도 가중치 적용, 인용 시간 경과 고려 등이 필요

## Evaluation

- Novelty: 5/5
- Technical Soundness: 4/5
- Significance: 5/5
- Clarity: 5/5
- Overall: 5/5

**총평**: 이 논문은 과학 평가 분야에 혁명적 영향을 미친 h-index를 처음 제안한 기념비적 작업으로, 간결하면서도 강력한 개념 제시와 견고한 수학적 기초, 그리고 실증적 검증을 통해 학술 평가의 새로운 표준을 제시하였다.

## Related Papers

- 🔗 후속 연구: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — h-index의 한계를 극복하기 위해 출판량, 인용 영향력, 경력 기간, 저자 기여도를 통합한 더 포괄적인 성과 지표를 개발했습니다.
- 🔄 다른 접근: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — h-index가 학문 분야별 차이를 반영하지 못하는 문제를 해결하기 위해 공동인용 네트워크 기반의 정규화된 인용 지표를 제안합니다.
- 🔗 후속 연구: [[papers/1047_Theory_and_Practice_of_the_g-index/review]] — h-index를 보완하기 위해 개발된 g-index는 고인용 논문의 영향을 더 강하게 반영하는 대안적 지표입니다.
- 🏛 기반 연구: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — 인용 분포의 보편성을 이해하는 것이 h-index와 같은 개별 연구자 평가 지표의 타당성을 뒷받침하는 이론적 기반이 됩니다.
- 🏛 기반 연구: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — h-지수 개발의 기본 철학이 NK 복합 지수 설계의 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — h-index의 학문 분야별 편향을 해결하기 위해 공동인용 네트워크 기반의 정규화된 대안 지표를 제시합니다.
- 🏛 기반 연구: [[papers/1047_Theory_and_Practice_of_the_g-index/review]] — h-지수 개발이 g-지수 설계의 직접적 이론적 토대를 제공한다.
- 🧪 응용 사례: [[papers/1052_Updated_science-wide_author_databases_of_standardized_citati/review]] — h-지수와 관련 지표들이 표준화된 인용 지표 데이터베이스의 핵심 측정 도구로 활용된다.
- 🔗 후속 연구: [[papers/1056_Where_Do_Your_Citations_Come_From_Citation-Constellation_A_F/review]] — h-지수 등 기존 인용 지표를 넘어서, 인용 네트워크의 사회구조적 경로를 분석하여 연구자의 인용 프로필을 더 세밀하게 분해한다.
- 🔗 후속 연구: [[papers/943_Citation_Analysis_as_a_Tool_in_Journal_Evaluation/review]] — 인용 기반 평가를 저널 수준에서 개별 연구자 수준으로 확장한 h-index 개발의 기초
- 🏛 기반 연구: [[papers/966_Global_citation_inequality_is_on_the_rise/review]] — 개별 연구자의 연구 성과 정량화가 인용 불평등 분석의 방법론적 기초를 제공한다
