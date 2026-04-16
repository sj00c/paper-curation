---
title: "943_Citation_Analysis_as_a_Tool_in_Journal_Evaluation"
authors:
  - "Eugene Garfield"
date: "1972"
doi: "10.1126/science.178.4060.471"
arxiv: ""
score: 4.0
essence: "Science Citation Index(SCI) 데이터베이스를 활용하여 저널들의 인용 빈도(citation frequency)와 영향도(impact)를 분석함으로써 과학 정책 수립을 위한 저널 평가 도구로서의 인용 분석(citation analysis)의 가능성을 제시한다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Computational_Bibliometric_Analysis"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Research_Reproducibility_Crisis"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Garfield_1972_Citation Analysis as a Tool in Journal Evaluation.pdf"
---

# Citation Analysis as a Tool in Journal Evaluation

> **저자**: Eugene Garfield | **날짜**: 1972 | **DOI**: [10.1126/science.178.4060.471](https://doi.org/10.1126/science.178.4060.471)

---

## Essence


Science Citation Index(SCI) 데이터베이스를 활용하여 저널들의 인용 빈도(citation frequency)와 영향도(impact)를 분석함으로써 과학 정책 수립을 위한 저널 평가 도구로서의 인용 분석(citation analysis)의 가능성을 제시한다.

## Motivation

- **Known**: 1927년 이후 저널 인용 패턴에 관한 단편적 연구들이 수행되어 왔으나, 저널 네트워크 전체에 대한 체계적 이해는 부재한 상태이다. 수작업 데이터 처리의 한계로 인해 광범위한 분석이 불가능했다.
- **Gap**: 저널 인용 네트워크 전체에 대한 체계적 분석 부재. 다학제적이고 장기간의 인용 데이터를 통합 분석할 수 있는 방법론 및 도구의 부족.
- **Why**: 저널은 과학 정보 교환의 중요한 통신 수단이므로, 저널 네트워크의 구조와 상호관계를 파악하는 것은 과학 정책 수립, 도서관 구성, 정보 유통 최적화에 필수적이다.
- **Approach**: SCI 데이터베이스(1971년 기준 27백만 개 이상의 참고문헌 포함, 2,200개 저널 커버)를 활용하여 1969년 4분기 저널들의 인용 패턴을 대규모로 추출하고 분석한다. 컴퓨터를 통한 기계 가독 형식의 데이터 조작으로 이전에 불가능했던 규모의 분석을 가능하게 한다.

## Achievement


- **SCI 데이터베이스의 활용성 입증**: 27백만 개 이상의 참고문헌과 2,200개 저널을 포함하는 기계 가독 형식의 데이터베이스를 인용 분석에 효과적으로 활용할 수 있음을 보여줌
- **다층적 인용 통계 분석 구조 제시**: 저널별 인용 빈도, 인용의 시간적 분포, 인용 및 피인용 저널 간 관계를 체계적으로 추출하고 시각화하는 방법론 제시
- **저널 평가 지표의 다원화**: 인용 빈도(frequency)와 인용 영향도(impact)를 결합하여 저널의 과학적 중요성을 다각적으로 평가할 수 있는 근거 제공
- **과학 정책 지원 도구로서의 가능성**: 저널 인용 패턴 분석을 통해 과학 분야별 정보 유통 구조를 파악하고 도서관, 정보센터, 정책입안자의 의사결정을 지원할 수 있음을 제시

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Statistics on cited journals. The data on cited journals show the total number*

- SCI 데이터베이스에서 1969년 4분기 동안 2,200개 저널에 발표된 논문들의 인용 정보 추출 (약 100만 건의 저널 인용)
- 각 저널에 대해 인용된 총 횟수(total citations)를 계산
- 인용의 출판 연도별 분포(1960-1969)를 추출하여 인용의 시간적 패턴 분석
- 개별 저널(citing journal)이 다른 저널(cited journal)을 인용한 횟수를 매트릭스 형태로 정렬
- 인용 빈도가 높은 저널과 저널 간 인용 관계를 시각화하여 저널 네트워크 구조 파악

## Originality

- 저널 인용 분석을 위해 처음으로 대규모 기계 가독 형식의 데이터베이스를 체계적으로 활용
- 1927년 이후 단편적으로 수행되어 온 연구들을 통합하여 과학 전체 영역을 포괄하는 통일된 접근법 제시
- 인용 빈도뿐만 아니라 인용의 시간적 분포를 분석하여 저널의 지속적 영향도를 평가하는 다층적 방법론 도입
- 저널 평가를 개별 지표에서 벗어나 인용 네트워크의 구조적 관계로 파악하려는 새로운 관점 제시

## Limitation & Further Study

- 1969년 4분기 데이터만을 분석대상으로 하여 시간적 대표성에 제한. 장기간 추적으로 인용 패턴의 변화 분석 필요
- SCI 커버리지 편향: 영어로 출판된 저널과 주류 과학 분야에 치중될 가능성. 비영어권, 지역 저널, 신흥 분야의 저널 평가에 제한
- 인용의 질(quality)을 반영하지 못함. 부정적 인용, 자명한 인용, 관성적 인용 등을 구분하지 않음
- 저널별 논문 수, 저널 나이, 발행 주기 등의 정규화 부재로 인해 서로 다른 특성의 저널들 간 단순 비교의 한계
- **후속연구**: 시계열 분석(time series analysis)으로 인용 패턴의 동적 변화 추적; 인용 맥락 분석(citation context analysis) 도입; 학제 간 인용 패턴 비교; 저널 특성 변수(impact factor, age, discipline 등)를 고려한 정규화 방법론 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 3/5
- Overall: 4/5

**총평**: 본 논문은 대규모 인용 데이터베이스를 처음으로 체계적으로 활용하여 저널 평가의 새로운 가능성을 제시한 선구적 연구이다. 과학 정보학 분야의 기초를 마련했으며, 현대 journal impact factor 개념의 이론적 토대가 되었다. 다만 분석 대상의 시간적 제약과 인용의 질적 측면 미반영이 한계이다.

## Related Papers

- 🏛 기반 연구: [[papers/1081_Science_Citation_IndexA_New_Dimension_in_Indexing_This_uniqu/review]] — Science Citation Index의 기본 개념을 저널 평가라는 실용적 응용 분야로 구체화
- 🔄 다른 접근: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — 저널 영향도 평가를 전통적 인용 분석과 상대적 인용 비율이라는 다른 지표로 각각 측정
- 🔗 후속 연구: [[papers/933_An_index_to_quantify_an_individuals_scientific_research_outp/review]] — 인용 기반 평가를 저널 수준에서 개별 연구자 수준으로 확장한 h-index 개발의 기초
- 🔗 후속 연구: [[papers/1008_Reinforcing_Prestige_Journal_Citation_Biases_in_Astronomy/review]] — 1972년 저널 평가를 위한 인용 분석이 천문학 분야 저널 인용 편향 분석으로 구체적으로 확장됩니다.
- 🏛 기반 연구: [[papers/1006_Real-World_Evidence_in_the_First_Round_of_the_US_Inflation_R/review]] — 정책 결정에서 인용 분석이 어떻게 활용되는지 보여주는 기본적인 방법론적 배경을 제공합니다.
- 🔗 후속 연구: [[papers/1081_Science_Citation_IndexA_New_Dimension_in_Indexing_This_uniqu/review]] — Science Citation Index의 기본 개념을 저널 평가라는 구체적 응용 분야로 확장한 연구
- 🏛 기반 연구: [[papers/1218_Viewing_Citation_Analysis_Through_the_Lens_of_Citation_Justi/review]] — 저널 평가 도구로서의 인용 분석 기초 이론이 인용 공정성 논의의 출발점을 제공합니다.
- 🏛 기반 연구: [[papers/1151_Citation_Analysis_of_DESIDOC_Journal_of_Information_Technolo/review]] — 저널 평가 도구로서 인용 분석의 기본 개념을 다룬 기초 연구로, DJLIT 인용 분석의 이론적 토대를 제공합니다.
- 🏛 기반 연구: [[papers/1138_Arts_and_Humanities_Citation_Index_for_Research_Evaluation_i/review]] — 저널 평가 도구로서의 인용 분석이 A&HCI를 종교학 연구평가에 사용할 때의 문제점 분석에 기반을 제공하기 때문
