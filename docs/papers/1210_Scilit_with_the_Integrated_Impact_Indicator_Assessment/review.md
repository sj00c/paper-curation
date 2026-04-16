---
title: "1210_Scilit_with_the_Integrated_Impact_Indicator_Assessment"
authors:
  - "Haochen Dong"
  - "Sun Qiao"
  - "Yanping Mu"
  - "Lu Liao"
  - "Diogo Rodrigues"
date: "2026"
doi: "10.48550/arXiv.2601.01716"
arxiv: ""
score: 4.0
essence: "Scilit 데이터베이스의 I3와 I3/N이라는 새로운 영향력 지표를 제시하고, 기존의 Journal Impact Factor와 CiteScore와 비교하여 학제 간 저널 평가에서 우월성을 입증한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Dong et al._2026_Scilit with the Integrated Impact Indicator Assessment.pdf"
---

# Scilit with the Integrated Impact Indicator Assessment

> **저자**: Haochen Dong, Sun Qiao, Yanping Mu, Lu Liao, Diogo Rodrigues, F. Sauerburger, Yi Bu, R. Haunschild | **날짜**: 2026 | **DOI**: [10.48550/arXiv.2601.01716](https://doi.org/10.48550/arXiv.2601.01716)

---

## Essence


Scilit 데이터베이스의 I3와 I3/N이라는 새로운 영향력 지표를 제시하고, 기존의 Journal Impact Factor와 CiteScore와 비교하여 학제 간 저널 평가에서 우월성을 입증한다.

## Motivation

- **Known**: Web of Science의 JIF와 Scopus의 CiteScore가 저널 평가의 주요 지표로 널리 사용되고 있으며, 이들은 평균 기반의 인용 지표로서 학문 분야별 인용 밀도 차이, 왜곡된 인용 분포, 그리고 전략적 행동으로 인한 문제점들이 지적되어 왔다.
- **Gap**: 기존 주요 데이터베이스(WoS, Scopus)는 선택적 색인 정책으로 인한 편향, 제한된 메타데이터 품질, 유료 접근 제한 등의 문제를 가지고 있으며, 더욱 포괄적이고 과학적으로 근거 있는 인용 지표가 필요하다.
- **Why**: 저널 평가 지표는 연구자의 투고 선택, 출판사의 시장 전략, 도서관의 저널 선택, 그리고 대학의 채용·승진 평가에 광범위하게 영향을 미치므로, 더욱 공정하고 신뢰성 높은 평가 방법이 중요하다.
- **Approach**: Scilit 데이터베이스의 multi-source 수집 체계(Crossref, DataCite, PubMed, DOAJ 등)를 활용하여 17,816개의 매칭된 저널 데이터셋을 구성하고, 2023-2024년에 대해 I3/N, JIF, CiteScore를 학문 분야 및 출판사 관점에서 비교 분석한다.

## Achievement


- **포괄적 데이터베이스 구축**: DOI 등록 기관, PubMed, 출판사 API, 오픈액세스 디렉토리, 프리프린트 서버 등 다중 소스로부터 181백만 이상의 항목을 집계하여 WoS·Scopus보다 광범위한 커버리지 제공
- **향상된 메타데이터 품질**: 고급 저자 동일인물 식별 기술 적용 및 14개 세분화된 출판물 유형 분류로 Google Scholar나 OpenAlex 대비 더욱 정확한 참고문헌 매칭 달성
- **I3와 I3/N 지표의 우월성 입증**: 기존 평균 기반 지표 대비 방법론적 견고성, 학제 간 공정성, 진단 가능성에서 현저히 우수함을 통계 분석으로 입증
- **개방 접근 플랫폼**: MDPI에 의한 지속적 재정 지원으로 완전 무료 접근 보장하여 학계 접근성 극대화

## How

![Figure 5](figures/fig5.webp)

*Figure 5. ER diagram of the Source Entity*

- Scilit의 데이터 수집 파이프라인: Crossref, DataCite 등 DOI 등록 기관에서 메타데이터 수확, PubMed/Medline 통합, 출판사 피드 및 API 직접 수신, DOAJ 및 프리프린트 서버 색인
- 저자 동일인물 식별: 고급 저자 disambiguiation 기법 적용으로 중복 및 모호한 저자 정보 해결 (Fig 3 참조)
- 출판물 분류: Research Article, Review Article, Conference Paper, Clinical Trial, Case Report 등 14개 세분화된 유형으로 분류
- 비교 분석 방법: 17,816개 저널의 매칭 데이터셋 기반으로 기술 통계량, 분포 특성을 학문 분야 및 출판사 관점에서 다층적 분석
- 참고문헌 완성도 평가: OpenAlex 대비 Scilit의 논문당 인용 수 및 인용 논문 수를 비교하여 참고문헌 매칭 완성도 우월성 입증

## Originality

- 기존 WoS·Scopus 중심의 학술 평가 체계에서 벗어나 multi-source 수집을 통한 더욱 포괄적인 대안 플랫폼 제시
- I3와 I3/N이라는 새로운 통합 영향력 지표 프레임워크를 제안하고 대규모 실증 분석으로 검증
- 학제 간 저널 평가에서 필드 정규화 문제를 해결하는 방법론적 기여
- 완전 개방 접근을 보장하면서 학술 데이터베이스 지속성을 확보하는 비즈니스 모델

## Limitation & Further Study

- OpenAlex 대비 총 작업 수(works) 면에서 72.2백만 대 100.1백만으로 여전히 뒤처져 있으며, 저자 및 기관 정보가 있는 작업의 비중(43.6% vs 90.1%)도 낮음
- I3/N의 신뢰성 검증을 위해 더 장기간의 데이터(2023-2024년만 분석)와 다양한 학문 분야에서의 추가 파일럿 및 검증 필요
- 저자 disambiguation의 완전성 수준이 명확히 제시되지 않았으며, 프리프린트와 정식 출판물 간의 중복 제거 메커니즘이 상세히 설명되지 않음
- 후속 연구: (1) I3/N의 예측 타당성 검증, (2) 더 다양한 학문 분야의 사례 분석, (3) 기관 및 개인 수준 지표로의 확장 가능성 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 기존의 배타적이고 편향된 학술 데이터베이스의 대안으로서 Scilit의 포괄적 접근과 새로운 I3/I3/N 지표를 체계적으로 제시하며, 대규모 실증 분석으로 그 우월성을 입증함으로써 학술 평가 방법론에 의미 있는 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1047_Theory_and_Practice_of_the_g-index/review]] — 학술 영향력 측정에서 기존 g-index와 새로운 I3/I3N 지표의 서로 다른 접근법을 비교할 수 있습니다.
- 🔗 후속 연구: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — 상대인용비율(RCR) 개념을 확장하여 학제간 저널 평가에 특화된 지표로 발전시켰습니다.
- 🏛 기반 연구: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — 인용 분포의 보편성 연구가 제공하는 객관적 측정 이론이 I3 지표의 타당성과 신뢰성 검증에 핵심적인 이론적 근거를 제공한다.
