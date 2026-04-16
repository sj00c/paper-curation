---
title: "1227_Exploring_Open_Access_Research_Trends_in_the_Indian_Council"
authors:
  - "Abhijit Roy"
  - "Akhandanand Shukla"
  - "Aditya Tripathi"
date: "2026"
doi: "10.14429/djlit.21105"
arxiv: ""
score: 4.0
essence: "본 연구는 OpenAlex 데이터베이스를 활용하여 2014-2023년 인도 농업연구회의소(ICAR) 기관의 Open Access 출판 패턴을 분석한 scientometric 연구이다. ICAR의 52% 이상의 학술 산출물이 개방 접근성을 갖추고 있으며, Green OA 부족과 저임팩트 저널 게시 문제를 식별했다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Exploring Open Access Research Trends in the Indian Council of Agricultural Rese.pdf"
---

# Exploring Open Access Research Trends in the Indian Council of Agricultural Research

> **저자**: Abhijit Roy, Akhandanand Shukla, Aditya Tripathi | **날짜**: 2026 | **DOI**: [10.14429/djlit.21105](https://doi.org/10.14429/djlit.21105)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Growth of OA routes with citation impact.*

본 연구는 OpenAlex 데이터베이스를 활용하여 2014-2023년 인도 농업연구회의소(ICAR) 기관의 Open Access 출판 패턴을 분석한 scientometric 연구이다. ICAR의 52% 이상의 학술 산출물이 개방 접근성을 갖추고 있으며, Green OA 부족과 저임팩트 저널 게시 문제를 식별했다.

## Motivation

- **Known**: 전 세계적으로 Open Access 출판이 증가하고 있으며, 농업 분야에서는 46%의 논문이 OA를 통해 이용 가능하다. 인도 학술기관의 평균 OA 성과는 23% 수준이다.
- **Gap**: 농업 부문의 기관 수준 OA 출판 추세에 대한 연구가 부족하며, 특히 ICAR 기관들의 OA 전략과 영향력에 대한 종합적 분석이 필요하다.
- **Why**: 공공 자금으로 지원되는 농업 연구가 농민과 정책 입안자에게 효과적으로 전달되어야 하며, ICAR의 OA 정책(2013년 채택) 이행 현황과 개선 방안 파악이 중요하다.
- **Approach**: OpenAlex 데이터베이스에서 ROR ID를 사용하여 ICAR 기관의 60,256개 학술 산출물을 검색하고, OpenRefine으로 데이터를 정제하여 5가지 OA 유형(Green, Gold, Hybrid, Bronze, Diamond)으로 분류했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Growth of OA routes with citation impact.*

- **OA 성과 우수성**: ICAR의 52.22% OA 비율이 농업 분야 글로벌 평균(46%)과 인도 기관 평균(23%)을 모두 상회
- **OA 경로별 분포**: Gold OA가 45.53%(14,328건)로 압도적이며, Bronze OA(17.04%), Diamond OA(15.42%) 순으로 분포
- **인용 영향력**: 31,466건의 OA 문헌이 총 296,180건의 인용을 획득
- **주제 분포**: 식물과학과 농업정책이 주요 연구 영역이며 농업·생물과학에 집중
- **도전 과제 식별**: Green OA 저활용(12.23%), 저임팩트 저널 게시 현황 파악

## How


- OpenAlex REST API를 활용한 데이터 수집 및 검색(ROR ID: 04fw54a43)
- OpenRefine 3.8.4를 사용한 Boolean facet 기반 데이터 정제 및 분류
- 5가지 OA 경로 분류(Green, Gold, Hybrid, Bronze, Diamond OA)
- MS Excel을 통한 출판 추세 및 인용 영향력 분석
- VOSviewer를 활용한 저자 공저자 네트워크, 기관 협력, 국가 간 협력 시각화
- 2014-2023년 10년 기간의 연도별 필터링 적용

## Originality

- ICAR 기관 전체를 대상으로 한 최초의 포괄적 OA scientometric 분석
- OpenAlex의 5가지 OA 유형 분류 체계를 농업 연구 맥락에서 적용
- data carpentry 접근법(OpenRefine)을 통한 대규모 데이터 정제 및 분석 방법론 제시
- OA 성과와 인용 영향력의 역설(높은 접근성 대비 낮은 임팩트) 발견

## Limitation & Further Study

- OpenAlex 메타데이터의 완전성과 정확성에 대한 검증 부족
- Bronze OA의 불명확한 라이선스 상태가 진정한 OA 영향력 평가를 어렵게 함
- 저임팩트 저널 게시의 원인(자금 제약, 정책 격차 등)에 대한 심층 분석 부재
- Green OA 저활용의 근본적 이유(제도적 장애, 인식 부족 등)에 대한 정성적 조사 필요
- 인용 영향력이 제한적일 수 있으므로 Altmetrics 등 다양한 영향력 지표 통합 필요
- **후속 연구**: ICAR 기관의 자기 아카이빙 정책 강화, 펀딩 메커니즘 확대, 고임팩트 저널과의 제휴 전략 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 연구는 인도 농업 연구의 OA 현황을 체계적으로 분석하고, ICAR의 우수한 OA 성과와 함께 Green OA 미활용 및 저임팩트 저널 편중 문제를 명확히 드러냈다. 향후 제도 개선과 정책 강화를 위한 실질적 근거를 제공하는 의미 있는 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/993_OpenAlex_A_fully-open_index_of_scholarly_works_authors_venue/review]] — OpenAlex 색인의 전반적 구조와 기능이 인도 농업연구회의소 개방접근 분석의 데이터 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1140_Assessing_the_impact_of_Open_Research_Information_Infrastruc/review]] — 개방연구정보 인프라의 영향 평가를 인도 농업 연구기관의 구체적 사례로 확장합니다.
- 🔗 후속 연구: [[papers/937_Authorship_titles_and_open_access_as_drivers_of_citation_per/review]] — 개방접근 출판 패턴 분석을 저자 속성과 인용 성과 측면에서 확장한 연구이다
- 🏛 기반 연구: [[papers/1044_The_State_of_OA_A_Large-Scale_Analysis_of_the_Prevalence_and/review]] — 개방접근 출판의 전반적 현황을 제시하여 특정 기관 분석의 기초를 제공한다
- 🔄 다른 접근: [[papers/992_OpenAlex_in_focus_Metadata_quality_of_publication_type_and_l/review]] — OpenAlex 메타데이터 품질을 다른 관점에서 평가하여 보완적 시각을 제공한다
- 🔗 후속 연구: [[papers/997_Polymer_Science_Research_in_India_A_Scientometrics_Study/review]] — 인도 과학기술연구위원회의 오픈 액세스 연구 동향 탐구는 인도 고분자 과학 연구의 과학계량학적 분석을 오픈 액세스 관점으로 확장한다.
