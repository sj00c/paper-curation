---
title: "1023_SciSciNet_A_large-scale_open_data_lake_for_the_science_of_sc"
authors:
  - "Zihang Lin"
  - "Yian Yin"
  - "Lu Liu"
  - "Dashun Wang"
date: "2023.06"
doi: "10.1038/s41597-023-02198-9"
arxiv: ""
score: 4.0
essence: "SciSciNet은 134M개 이상의 과학 출판물과 자금 조달, 특허, 임상시험 등 외부 연계를 포괄하는 대규모 개방형 데이터 레이크(data lake)로서 과학의 과학(science of science) 연구의 진입 장벽을 낮추고 재현성을 향상시킨다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Science_Policy_Funding"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lin et al._2023_SciSciNet A large-scale open data lake for the science of science research.pdf"
---

# SciSciNet: A large-scale open data lake for the science of science research

> **저자**: Zihang Lin, Yian Yin, Lu Liu, Dashun Wang | **날짜**: 2023-06-01 | **DOI**: [10.1038/s41597-023-02198-9](https://doi.org/10.1038/s41597-023-02198-9)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1  The entity relationship diagram of SciSciNet. SciSciNet includes “SciSciNet_Papers” as the main data*

SciSciNet은 134M개 이상의 과학 출판물과 자금 조달, 특허, 임상시험 등 외부 연계를 포괄하는 대규모 개방형 데이터 레이크(data lake)로서 과학의 과학(science of science) 연구의 진입 장벽을 낮추고 재현성을 향상시킨다.

## Motivation

- **Known**: 과학의 과학 분야는 CiteSeerX, AMiner, OpenAlex, Crossref 등 여러 대규모 데이터셋의 가용성으로 성장해왔으나, 데이터셋 간 연계 추적과 전처리 과정의 중복이 문제가 되어왔다.
- **Gap**: 데이터가 증가함에 따라 이용 가능한 데이터 소스와 상호 연계를 추적하기 어려워지고 있으며, 데이터 전처리 및 측정 단계에서 중복 노력과 표준화 부족이 발생하고 있다.
- **Why**: 통합된 데이터 레이크는 연구 강건성과 재현성을 향상시키고, 데이터 처리의 중복을 줄이며, 진입 장벽을 낮춤으로써 과학의 과학 분야의 다양성과 포용성을 확대할 수 있다.
- **Approach**: Microsoft Academic Graph(MAG)를 중심으로 Crossref, OpenAlex, PatentsView, NIH/NSF 자금 데이터, 임상시험 정보 등 다양한 출처의 데이터를 통합하고 링크하며, 표준화된 전처리와 공통 측정값(disruption, team composition 등)을 계산 제공한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3  Summary statistics of scientific publications in SciSciNet. (a) The number of publications in 19 top-level*

- **포괄적 데이터 통합**: 134M개 이상의 과학 출판물과 저자, 소속기관, 자금 출처(NIH, NSF), 산출물(특허, 임상시험, 뉴스)을 연계한 통합 데이터 레이크 구축
- **투명한 전처리 문서화**: 데이터 수집, 정제, 링킹의 상세한 전처리 단계와 분석 선택사항을 명확히 문서화하여 재현성 확보
- **표준화된 메트릭 제공**: Disruption score, team size, citation impact(C10) 등 과학의 과학 문헌에서 빈번히 사용되는 측정값을 사전 계산 제공
- **다중 검증 방법**: 내부 데이터 검증, 크로스 데이터베이스 검증, 문헌의 표준 결과 재현을 통한 데이터 품질 보증
- **공개 접근성**: Figshare를 통한 자유로운 데이터 접근으로 다양한 연구자의 참여와 데이터 레이크 협력적 확충 가능

## How

![Figure 2](figures/fig2.webp)

*Fig. 2  Matching NSF reference string to MAG records. (a) Distribution of Z-scores for papers matched in*

- Microsoft Academic Graph(MAG)를 핵심 데이터 소스로 활용하되 MAG 종료 이후에도 지속성 확보
- Crossref DOI 메타데이터와 OpenAlex의 논문-저자-기관-개념 연결 통합
- NIH RePORTER와 NSF Awards 데이터를 매칭하여 자금 조달과 출판물 연계
- PatentsView 및 Patent Citation to Science 데이터를 통해 특허-논문 인용 관계 구축
- Clinical Trials, Altmetric, 뉴스 피드 데이터와의 외부 연계를 통한 과학의 사회적 영향 추적
- Z-score 기반 매칭 알고리즘을 사용하여 참고문헌 문자열을 MAG 레코드로 변환
- 행 중복 제거, 개체 해석 명확화 등 전처리 단계 상세 기록

## Originality

- **통합 범위의 광대함**: 134M개 논문과 함께 자금(NIH, NSF), 특허, 임상시험, 언론/소셜미디어 등 상류와 하류 연계를 동시에 포괄한 업계 최초 수준의 통합 데이터 레이크
- **협력적 데이터 레이크 개념**: 연구 커뮤니티가 공동으로 데이터와 측정값을 기여하고 확충할 수 있는 생태계 설계
- **투명한 전처리 문서화 강조**: 게시된 논문에서 생략되는 상세한 데이터 처리 선택사항을 명시적으로 기록 및 공개하는 관행 수립
- **표준화된 벤치마크 메트릭**: 분야에서 자주 사용되는 측정값(disruption, team composition 등)을 미리 계산하여 제공함으로써 일관성 확보

## Limitation & Further Study

- **MAG 종료 의존성**: 핵심 데이터 소스인 MAG가 2021년 종료되었으므로, 향후 최신 데이터 유지 및 업데이트 메커니즘 필요
- **국가/언어 편향**: NIH, NSF 등 미국 기관 중심 자금 데이터로 인한 지역 및 학제 간 대표성 차이 가능성
- **시간적 커버리지 제약**: 특정 데이터(특허-과학 인용)의 경우 역사적 데이터 수집 및 매칭의 완전성 문제 가능
- **명확성 한계**: 저자 이름 변동, 소속기관 변경, 중복 개체 등 개인 및 기관 식별 관련 오류의 완전한 해결 어려움
- **후속 연구**: (1) 실시간 데이터 업데이트 및 증분 방식의 데이터 갱신 시스템 구축, (2) 국제적 자금 데이터 확대를 통한 글로벌 대표성 개선, (3) 분산 기여 플랫폼 개발로 커뮤니티 참여 활성화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SciSciNet은 과학의 과학 분야의 커뮤니티 기반 인프라로서 데이터 통합, 투명한 문서화, 표준화된 메트릭 제공을 통해 연구의 강건성과 접근성을 획기적으로 향상시키는 고가치의 공공재이다. 특히 상류(자금)에서 하류(사회적 영향)까지의 전체 연구 혁신 생태계를 포괄한 점과 협력적 데이터 레이크 모델 제안이 분야의 표준으로 자리잡을 잠재력을 보유하고 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — 과학의 과학 연구를 위한 서로 다른 범위와 구조를 가진 대규모 오픈 데이터 플랫폼들입니다.
- 🔗 후속 연구: [[papers/993_OpenAlex_A_fully-open_index_of_scholarly_works_authors_venue/review]] — 학술 색인의 완전 개방화가 과학의 과학 연구를 위한 포괄적 데이터 레이크로 확장됩니다.
- 🏛 기반 연구: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 과학의 과학 분야에서 데이터, 측정, 실증적 방법론의 중요성을 보여주는 이론적 배경을 제공합니다.
- 🧪 응용 사례: [[papers/991_Open_Datasets_in_Learning_Analytics_Trends_Challenges_and_Be/review]] — 학습 분석의 오픈 데이터셋 동향 분석은 SciSciNet과 같은 오픈 데이터 레이크가 특정 연구 분야에서 어떻게 활용될 수 있는지 보여주는 구체적 응용 사례입니다.
- 🔄 다른 접근: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — 대규모 학술 데이터 구축에서 서로 다른 접근법과 범위를 가진 경쟁적인 오픈 데이터 플랫폼들입니다.
- 🧪 응용 사례: [[papers/1019_Science_of_science/review]] — 과학의 과학이라는 새로운 학문 분야의 연구를 위한 대규모 데이터 인프라를 제공합니다.
- 🏛 기반 연구: [[papers/1022_SciSciGPT_advancing_humanAI_collaboration_in_the_science_of/review]] — SciSciNet 대규모 과학 데이터 레이크는 SciSciGPT가 효과적으로 작동하기 위해 필요한 포괄적 데이터 인프라를 제공합니다.
- 🔗 후속 연구: [[papers/1052_Updated_science-wide_author_databases_of_standardized_citati/review]] — 과학의 과학 연구를 위한 대규모 오픈 데이터 구축의 연장선에서, 인용 지표에 특화된 표준화된 데이터베이스를 제공한다.
- 🏛 기반 연구: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 과학의 과학 연구를 위한 대규모 오픈 데이터 구축이 실증적 연구 방법론 발전의 핵심 인프라임을 보여준다.
- 🏛 기반 연구: [[papers/991_Open_Datasets_in_Learning_Analytics_Trends_Challenges_and_Be/review]] — 과학의 과학을 위한 대규모 오픈 데이터 레이크로, 학습분석 공개 데이터셋 연구에 필요한 데이터 인프라 토대를 제공합니다.
- 🧪 응용 사례: [[papers/992_OpenAlex_in_focus_Metadata_quality_of_publication_type_and_l/review]] — 대규모 과학학 데이터 레이크에서 메타데이터 품질 문제가 연구 결과에 미치는 영향을 정량화할 수 있다.
- 🔗 후속 연구: [[papers/993_OpenAlex_A_fully-open_index_of_scholarly_works_authors_venue/review]] — OpenAlex 데이터를 활용하여 과학계량학 연구를 위한 더 포괄적인 오픈 데이터 레이크를 구축한다.
- 🔗 후속 연구: [[papers/939_BibFusion_A_Python_package_to_integrate_deduplicate_and_harm/review]] — 서지 데이터 통합을 넘어 과학의 과학을 위한 대규모 오픈 데이터 레이크로 확장된 플랫폼을 제공한다.
- 🔗 후속 연구: [[papers/978_Introducing_the_open_biomedical_map_of_science/review]] — SciSciNet 오픈 데이터 레이크에서 생의학 분야 특화 과학 지도로 연구 범위가 구체화된다.
