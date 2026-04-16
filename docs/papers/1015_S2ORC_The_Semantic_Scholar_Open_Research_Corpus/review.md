---
title: "1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus"
authors:
  - "Kyle Lo"
  - "Lucy Lu Wang"
  - "Mark Neumann"
  - "Rodney Kinney"
  - "Daniel Weld"
date: "2020"
doi: "10.18653/v1/2020.acl-main.447"
arxiv: ""
score: 4.0
essence: "81.1M 학술 논문의 메타데이터, 초록, 인용 정보와 8.1M 오픈 액세스 논문의 구조화된 전체 텍스트를 포함하는 대규모 공개 학술 코퍼스(S2ORC)를 소개한다."
tags:
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Computational_Bibliometric_Analysis"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Polymer_Science_Publication_Analytics"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lo et al._2020_S2ORC The Semantic Scholar Open Research Corpus.pdf"
---

# S2ORC: The Semantic Scholar Open Research Corpus

> **저자**: Kyle Lo, Lucy Lu Wang, Mark Neumann, Rodney Kinney, Daniel Weld | **날짜**: 2020 | **DOI**: [10.18653/v1/2020.acl-main.447](https://doi.org/10.18653/v1/2020.acl-main.447)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Inline citations and references to ﬁgures and*

81.1M 학술 논문의 메타데이터, 초록, 인용 정보와 8.1M 오픈 액세스 논문의 구조화된 전체 텍스트를 포함하는 대규모 공개 학술 코퍼스(S2ORC)를 소개한다.

## Motivation

- **Known**: 학술 논문은 NLP 연구에서 중요한 텍스트 도메인이며, 인용 그래프(AMiner, MAG, Semantic Scholar)와 디지털 아카이브(arXiv, PubMed)가 연구에 활용되어왔다. 기존 AAN, PubMed Central, RefSeer 등의 코퍼스는 규모가 작거나 도메인 특화적이며 기계 가독성 있는 전체 텍스트를 제공하지 않는다.
- **Gap**: 기존 코퍼스는 충분한 규모의 구조화된 전체 텍스트와 학제 간(multi-disciplinary) 커버리지를 동시에 제공하지 못한다. 인용 맥락, 표/그림 참조, 해결된 인용 링크를 포함하는 통합 리소스가 부족하다.
- **Why**: 학술 텍스트에 대한 대규모 구조화된 코퍼스는 요약, 언어 모델링, 개체 추출, 텍스트 분류, 파싱, 담론 분석 등 다양한 NLP 작업과 문헌 분석 연구를 가능하게 한다.
- **Approach**: Semantic Scholar 문헌 코퍼스를 기반으로 SCIENCEPARSE와 GROBID를 사용하여 PDF에서 구조화된 데이터를 추출하고, arXiv LaTeX 소스에서 추가 구조 정보를 파싱한다. 메타데이터 통합, 오픈 액세스 식별, 논문 클러스터링, 참고문헌 링크 해결의 4단계 파이프라인을 적용한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Inline citations and references to ﬁgures and*

- **규모와 포괄성**: 81.1M 논문(메타데이터 및 초록 포함), 8.1M 오픈 액세스 전체 텍스트(PDF 파싱), 1.5M LaTeX 파싱본으로 기존 PubMed Central의 3배 이상 규모
- **구조화된 정보**: 인라인 인용 언급(inline citations), 표/그림/수식 참조, 해결된 참고문헌 링크, 섹션 헤더, 단락 구조 등 기계 가독성 있는 주석
- **학제 간 커버리지**: 다양한 학문 분야를 포괄(컴퓨터 과학, 물리, 수학, 생의학 등)하여 기존 도메인 특화 코퍼스의 한계 극복
- **공개 가용성**: GitHub을 통해 공개되어 학술 커뮤니티에 기여하는 대규모 공개 자원

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Inline citations and references to ﬁgures and*

- SCIENCEPARSE v3.0.0과 GROBID v0.5.5를 사용한 PDF 처리 파이프라인: 메타데이터(제목, 저자, 초록) 추출, 섹션별 본문 단락 추출, 표/그림 캡션과 방정식 추출, 인라인 인용과 참고문헌 추출
- 인라인 인용 후처리: 정규표현식을 사용하여 인용 스타일(BRACKET, NAME-YEAR, OTHER) 분류, 오류(false positive/negative) 수정, 괄호 인용 범위 확장([3]-[5] → [3], [4], [5])
- LaTeX 소스 처리: XML 변환을 통해 본문, 섹션 헤더, 캡션, 표 표현, 방정식, 인용 및 참조 추출 (거의 완벽한 정확도)
- 4단계 파이프라인: (1) PDF/LaTeX 처리 → (2) 논문 클러스터당 최적 메타데이터/전체 텍스트 선택 → (3) 불충분한 메타데이터/내용 논문 필터링 → (4) 코퍼스 내 논문 클러스터 간 참고문헌 링크 해결
- Semantic Scholar 기반 메타데이터 통합: 출판사, MAG, arXiv, PubMed 등 다양한 소스에서 논문 수집 및 제목 유사도/DOI 기반 클러스터링

## Originality

- 기존 코퍼스 대비 3배 규모의 구조화된 전체 텍스트 제공으로 새로운 수준의 리소스 구축
- PDF 파싱과 LaTeX 소스 파싱의 이중 처리로 상호 보완적 구조 정보 제공 (PDF는 메타데이터, LaTeX는 수식/표 구조)
- 인라인 인용 언급과 참고문헌 항목의 명시적 링크, 표/그림 참조의 캡션 연결로 교차 논문 담론 분석 활성화
- 오픈 액세스 상태 자동 식별과 다중 소스 메타데이터 통합의 자동화된 파이프라인

## Limitation & Further Study

- **언어 제한**: 영어 논문만 포함(다국어 학술 출판물 미포함)
- **PDF 파싱 의존성**: GROBID의 인식 오류(인용 오검출/미검출)에 의존하며, 복잡한 레이아웃의 논문에서 추출 정확도 저하 가능
- **LaTeX 메타데이터 품질**: LaTeX 소스의 메타데이터 추출 정확도가 PDF 기반보다 낮아 메타데이터 선택에 미사용
- **클러스터링 오류**: 제목 유사도/DOI 기반 클러스터링의 한계로 같은 논문의 중복 클러스터 또는 다른 논문의 오병합 가능성
- **후속 연구**: (1) 다국어 논문 포함으로 확대, (2) PDF 파싱 정확도 개선 알고리즘 개발, (3) 시간에 따른 코퍼스 동적 갱신 메커니즘, (4) LaTeX 메타데이터 추출 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: S2ORC는 학술 텍스트에 대한 기존 코퍼스의 규모, 구조화, 학제 간 포괄성의 한계를 획기적으로 극복하는 대규모 공개 자원으로, NLP 및 문헌 분석 연구에 지대한 기여를 할 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 대규모 학술 코퍼스가 과학의 과학 연구에서 데이터 기반 실증 분석의 핵심 인프라를 제공한다.
- 🔄 다른 접근: [[papers/993_OpenAlex_A_fully-open_index_of_scholarly_works_authors_venue/review]] — OpenAlex와 S2ORC가 서로 다른 접근으로 대규모 학술 데이터베이스를 구축하여 상호 보완적 역할을 한다.
- 🧪 응용 사례: [[papers/1054_Whats_In_Your_Field_Mapping_Scientific_Research_with_Knowled/review]] — 대규모 학술 코퍼스를 활용하여 LLM과 지식 그래프를 결합한 과학 연구 매핑 시스템 구축이 가능하다.
- 🔄 다른 접근: [[papers/1023_SciSciNet_A_large-scale_open_data_lake_for_the_science_of_sc/review]] — 대규모 학술 데이터 구축에서 서로 다른 접근법과 범위를 가진 경쟁적인 오픈 데이터 플랫폼들입니다.
- 🔄 다른 접근: [[papers/1023_SciSciNet_A_large-scale_open_data_lake_for_the_science_of_sc/review]] — 과학의 과학 연구를 위한 서로 다른 범위와 구조를 가진 대규모 오픈 데이터 플랫폼들입니다.
- 🏛 기반 연구: [[papers/1112_CS-KG_20_A_Large-scale_Knowledge_Graph_of_Computer_Science/review]] — 대규모 학술 코퍼스 구축과 처리 방법론의 기반을 제공한다
- 🏛 기반 연구: [[papers/1120_SciEvo_A_2_Million_30-Year_Cross-disciplinary_Dataset_for_Te/review]] — S2ORC 오픈 연구 코퍼스가 대규모 scientometric 데이터셋 구축의 방법론적 선례를 제공한다.
- 🧪 응용 사례: [[papers/1054_Whats_In_Your_Field_Mapping_Scientific_Research_with_Knowled/review]] — S2ORC와 같은 대규모 학술 코퍼스를 기반으로 LLM과 지식 그래프를 결합한 연구 매핑 시스템을 구축한다.
- 🧪 응용 사례: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — S2ORC와 같은 대규모 학술 데이터셋이 과학의 과학 연구에서 실증적 분석의 핵심 데이터 인프라를 제공한다.
- 🔄 다른 접근: [[papers/1074_OLMo_Accelerating_the_Science_of_Language_Models/review]] — 언어 모델 연구와 의미론적 학술 코퍼스라는 서로 다른 오픈 사이언스 접근법을 제시한다.
- 🧪 응용 사례: [[papers/990_Networks_of_Scientific_Papers/review]] — Semantic Scholar 오픈 연구 코퍼스가 인용 네트워크 패턴 분석을 대규모로 실현할 수 있는 데이터 인프라를 제공한다.
- 🏛 기반 연구: [[papers/991_Open_Datasets_in_Learning_Analytics_Trends_Challenges_and_Be/review]] — S2ORC 의미론적 연구 코퍼스가 학습분석 분야 공개 데이터셋 발굴과 분석의 데이터 기반을 제공한다.
- 🔄 다른 접근: [[papers/993_OpenAlex_A_fully-open_index_of_scholarly_works_authors_venue/review]] — 학술 메타데이터 제공을 위한 또 다른 대규모 오픈 연구 코퍼스로서 OpenAlex와 상호 보완적인 역할을 한다.
- 🏛 기반 연구: [[papers/978_Introducing_the_open_biomedical_map_of_science/review]] — S2ORC 의미론적 연구 코퍼스가 개방형 생의학 과학 지도 개발의 데이터 기반을 제공한다.
- 🏛 기반 연구: [[papers/1196_Media_and_Digital_Marketing_Bibliomatrix_Analysis_using_R_Fu/review]] — 대규모 학술 연구 코퍼스가 소셜미디어 마케팅 연구 분석의 데이터 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1206_Review_of_E-Commerce_Literature_Inferences_Trends_and_Recomm/review]] — S2ORC 대규모 학술 코퍼스가 제공하는 포괄적인 과학 문헌 데이터베이스 구조와 메타데이터 표준이 e-commerce 문헌 분석의 방법론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1209_Scientometric_Analysis_of_Data_Privacy_and_Cloud_Security_Re/review]] — 대규모 학술 데이터셋 구축에서 서로 다른 접근법(arXiv 중심 vs 의미론적 스콜라 코퍼스)을 제시합니다.
- 🔄 다른 접근: [[papers/1228_OpenRad_a_Curated_Repository_of_Open-access_AI_models_for_Ra/review]] — OpenRad와 S2ORC 모두 대규모 과학 데이터를 체계적으로 수집하고 표준화하여 연구 커뮤니티에 제공하는 오픈 사이언스 인프라 구축 프로젝트다.
- 🏛 기반 연구: [[papers/1150_Characterization_of_a_Workload_Generator_for_Content-based_P/review]] — 대규모 오픈 연구 코퍼스의 데이터 특성화 방법이 CBPS 시스템 워크로드 분석의 기초 방법론 제공
