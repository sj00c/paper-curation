---
title: "1196_Media_and_Digital_Marketing_Bibliomatrix_Analysis_using_R_Fu"
authors:
  - "Minawati Wening"
  - "Tinik Sugiati"
  - "Erick Karunia"
  - "S. Shalahuddin"
date: "2026"
doi: "10.57178/paradoks.v9i2.2375"
arxiv: ""
score: 4.0
essence: "본 연구는 2020-2025년 Scopus 데이터베이스의 544개 학술논문을 대상으로 bibliometric analysis를 활용하여 소셜미디어와 디지털마케팅 연구의 발전 추세, 저자 생산성, 국가별 기여도, 인용분석, 연구주제 매핑을 체계적으로 분석한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wening et al._2026_Media and Digital Marketing Bibliomatrix Analysis using R (Future Research Directions).pdf"
---

# Media and Digital Marketing: Bibliomatrix Analysis using R (Future Research Directions)

> **저자**: Minawati Wening, Tinik Sugiati, Erick Karunia, S. Shalahuddin | **날짜**: 2026 | **DOI**: [10.57178/paradoks.v9i2.2375](https://doi.org/10.57178/paradoks.v9i2.2375)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. PRISMA Method Flowchart*

본 연구는 2020-2025년 Scopus 데이터베이스의 544개 학술논문을 대상으로 bibliometric analysis를 활용하여 소셜미디어와 디지털마케팅 연구의 발전 추세, 저자 생산성, 국가별 기여도, 인용분석, 연구주제 매핑을 체계적으로 분석한다.

## Motivation

- **Known**: 선행연구들은 Technology Acceptance Model(TAM)을 기반으로 특정 맥락에서 디지털마케팅 기술 채택을 검증했으나, 대부분 개별 변수 관계 테스트에 국한되었다. 소셜미디어는 브랜드 인식과 소비자 참여를 높이는 전략적 마케팅 플랫폼으로 확립되었다.
- **Gap**: 사회미디어 및 디지털마케팅 분야의 지식 구조, 연구주제 트렌드, 글로벌 과학적 협업 패턴에 대한 포괄적 개요가 부족하며, 최근 시기의 이 분야 발전을 체계적으로 매핑하는 bibliometric 연구가 제한적이다.
- **Why**: 디지털 변환 시대에 학자, 실무자, 정책입안자들이 효과적인 디지털마케팅 전략을 수립하기 위해서는 연구 발전 방향에 대한 포괄적 이해가 필수적이다. 2020-2025년의 최신 연구 동향 매핑을 통해 실증 기반의 근거를 제공할 수 있다.
- **Approach**: 본 연구는 PRISMA 프레임워크를 따라 Scopus 데이터베이스에서 포괄적 샘플링을 수행하고, RStudio의 Bibliometrix 패키지와 BiblioShiny 인터페이스를 이용하여 연간 발행 추세, 저자 생산성, 국가 기여도, 인용 분석, 연구주제 매핑을 정량적으로 분석한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4. Author Productivity Through Lotka’s Law*

1. **출판 증가 추이**: 분석 기간 동안 소셜미디어 마케팅 관련 출판물이 매년 유의미하게 증가했음을 확인
2. **국가별 기여도**: 여러 국가가 출판에 주도적으로 기여했으며 지역별 편차가 존재
3. **국제 협업 증대**: 디지털마케팅 연구에서 국제 협업이 증가하는 추세 발견
4. **핵심 주제 도출**: 소셜미디어 마케팅, 소비자 참여, 디지털 전략이 주요 연구 초점으로 확인
5. **TAM 프레임워크 유효성**: Technology Acceptance Model이 현대 디지털마케팅 연구의 이론적 토대로 지속적 중요성 확인

## How

![Figure 1](figures/fig1.webp)

*Figure 1. PRISMA Method Flowchart*

- Scopus 데이터베이스에서 'social media' 및 'digital marketing' 키워드로 초기 6,187개 문서 검색
- PRISMA 프레임워크를 따라 발행 기간(2020-2025), 주제 영역(Business, Management and Accounting), 문서 유형(Article), 출판 단계(Final), 주요 키워드 적합성, 저널 출처 유형, 언어(영어)를 기준으로 단계적 필터링
- 최종 544개 샘플 확보
- RStudio의 Bibliometrix 패키지로 연간 출판 추세, 저자 생산성(Lotka's Law 적용), 국가별 기여도, 상위 인용 문헌 분석
- BiblioShiny 인터페이스를 통한 시각적 매핑 및 주제 분석
- Purposive sampling 기법으로 연구 목표에 부합하는 대표성 있는 표본 구성

## Originality

- 2020-2025 최신 기간에 대한 포괄적 bibliometric 분석으로 시의성 있는 과학적 근거 제공
- Bibliometrix/BiblioShiny 기반의 자동화된 분석으로 기존 수작업 분석보다 체계성과 객관성 강화
- Technology Acceptance Model을 분석 틀로 적용하여 이론적 깊이 추가
- 출판 트렌드, 저자 생산성, 국가별 기여, 인용분석, 주제 매핑을 통합적으로 제시
- 학계, 실무, 정책 부문의 다층적 이해관계자를 위한 실용적 시사점 도출

## Limitation & Further Study

- Scopus 데이터베이스에만 의존하여 다른 데이터베이스(WoS, Google Scholar 등)의 출판물 누락 가능
- 2020-2025 시간 범위로 제한되어 장기 추세 분석의 깊이 부족
- 영어 출판물만 분석 대상으로 비영어권 연구 간과
- 정성적 분석(문헌의 질, 방법론적 엄밀성)이 부재하여 양적 지표만으로 평가
- Purposive sampling으로 인한 잠재적 선택편향
- 후속연구: 다국가 데이터베이스 통합분석, 시간 범위 확대, 비영어 논문 포함, 메타분석을 통한 효과크기 검증, 연구 주제별 방법론적 질 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 연구는 Bibliometrix 패키지를 활용한 체계적인 bibliometric 분석으로 2020-2025년 소셜미디어 및 디지털마케팅 연구의 현황을 포괄적으로 매핑하며, TAM 이론을 토대로 디지털 변환 시대의 마케팅 패러다임 전환을 설명한다. 다만 단일 데이터베이스 의존과 정성적 분석 부재가 한계이며, 후속 연구에서 다중 데이터베이스 통합과 방법론적 질 평가가 필요하다.

## Related Papers

- 🧪 응용 사례: [[papers/1006_Real-World_Evidence_in_the_First_Round_of_the_US_Inflation_R/review]] — 실제 비즈니스 환경에서 디지털 마케팅 연구 성과의 증거 기반 평가 사례를 제시합니다.
- 🔄 다른 접근: [[papers/1166_Emerging_Trends_in_Cybersecurity_Machine_Learning_as_a_Game-/review]] — 디지털 기술 동향을 서로 다른 관점(마케팅 vs 사이버보안)에서 bibliometric 분석으로 접근합니다.
- 🔄 다른 접근: [[papers/1177_From_Clicks_to_Cradles_Mapping_the_Digital_Landscape_of_Mate/review]] — 디지털 마케팅과 온라인 양육 자원 모두 디지털 플랫폼에서의 사용자 참여와 상호작용 패턴을 bibliometric으로 분석하는 공통된 연구 접근법을 사용한다.
- 🔗 후속 연구: [[papers/954_Do_novel_papers_attract_more_social_attention/review]] — 소셜미디어 마케팅의 사회적 관심도 분석에 novel papers의 사회적 주목도 측정 방법론을 적용하여 더 정확한 영향력 평가가 가능하다.
- 🔄 다른 접근: [[papers/1206_Review_of_E-Commerce_Literature_Inferences_Trends_and_Recomm/review]] — 디지털마케팅과 e-commerce의 bibliometric 분석을 서로 다른 R 패키지로 수행한 연구입니다.
- 🏛 기반 연구: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — 대규모 학술 연구 코퍼스가 소셜미디어 마케팅 연구 분석의 데이터 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1144_Bibliometric_analysis_of_publications_titled_culinary_arts_s/review]] — 미디어와 디지털 마케팅 분야와 요리 예술 분야 모두 실용적 응용 분야의 bibliometric 분석을 수행했기 때문
- 🔗 후속 연구: [[papers/1177_From_Clicks_to_Cradles_Mapping_the_Digital_Landscape_of_Mate/review]] — 어머니의 온라인 양육 자원과 디지털 마케팅을 연계하여 모성과 디지털 미디어의 종합적 분석을 제공한다.
- 🔄 다른 접근: [[papers/1206_Review_of_E-Commerce_Literature_Inferences_Trends_and_Recomm/review]] — e-commerce 문헌 분석과 디지털마케팅 연구가 상호 보완적인 bibliometric 접근을 보여줍니다.
- 🔄 다른 접근: [[papers/1215_Total_Fertility_Rate_Studies_Bibliometric_Analysis_with_R_Pr/review]] — 출산율 연구와 디지털마케팅 연구 모두 R Bibliometrix 패키지를 활용한 분석 방법론을 공유합니다.
- 🔗 후속 연구: [[papers/1135_AI-Augmented_Mobile_and_Data-Driven_Decision_Making_in_Busin/review]] — 디지털 마케팅에서 모바일 AI 의사결정 시스템으로 연구 범위를 확장한다
