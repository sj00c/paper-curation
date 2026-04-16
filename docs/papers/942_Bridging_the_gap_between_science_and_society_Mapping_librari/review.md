---
title: "942_Bridging_the_gap_between_science_and_society_Mapping_librari"
authors:
  - "Wang Zuorong"
  - "Sun Jiaxuan"
  - "He Shan"
  - "Deng Sanhong"
  - "Wang Hao"
date: "2026.03"
doi: "10.47989/ir31iconf64195"
arxiv: ""
score: 4.0
essence: "본 연구는 영국 Research Excellence Framework (REF)의 465개 사례 분석을 통해 도서관이 과학 연구의 사회적 영향을 중개하는 구체적 전략 5가지를 의미론적 분석(LLM + BERTopic)으로 규명했다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zuorong et al._2026_Bridging the gap between science and society Mapping libraries' strategies for engaging in the rese 1.pdf"
---

# Bridging the gap between science and society: Mapping libraries' strategies for engaging in the research impact process through semantic analysis

> **저자**: Wang Zuorong, Sun Jiaxuan, He Shan, Deng Sanhong, Wang Hao | **날짜**: 2026-03-20 | **DOI**: [10.47989/ir31iconf64195](https://doi.org/10.47989/ir31iconf64195)

---

## Essence

![Figure 4](figures/fig4.webp)

*Figure 4. Research workflow diagram.*

본 연구는 영국 Research Excellence Framework (REF)의 465개 사례 분석을 통해 도서관이 과학 연구의 사회적 영향을 중개하는 구체적 전략 5가지를 의미론적 분석(LLM + BERTopic)으로 규명했다.

## Motivation

- **Known**: 기존 문헌은 대학, 기업, 정부, 일반 대중 등 주요 행위자를 중심으로 연구 영향 과정을 분석했으나, 도서관과 같은 제도적 중개자의 역할은 체계적으로 이해되지 못했다.
- **Gap**: 도서관이 연구와 사회를 잇는 지식 중개자로서 어떤 구체적 전략을 배포하는지, 그리고 이것이 어떤 영향 유형에 집중되어 있는지에 대한 실증적 이해가 부족하다.
- **Why**: 도서관의 연구 영향 중개 역할을 이해하는 것은 디지털 격차 해소, 과학적 소양 증진, 공평한 정보 접근 보장을 위한 제도적 전략 수립에 필수적이다.
- **Approach**: REF 데이터베이스 465개 사례에서 도서관 언급 텍스트를 GPT-4o로 추출한 후, BERTopic을 활용한 의미론적 군집화로 도서관 전략을 분류 및 요약했다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5. Distribution of library involvement cases across research field and impact type.*

- **5가지 도서관 전략 규명**: 미디어 커뮤니케이션 및 공공 참여, 공공 대화 및 문화 제시, 예술 협업 및 라이브 경험, 디지털 콘텐츠 창제 및 배포, 대규모 이벤트 조율
- **학문 분야별 집중도 파악**: 인문학 및 예술(Main Panel D) 76% 집중, 문화적 영향(67%), 사회적 영향(22%) 순으로 분포
- **실증 기반 프레임워크 제시**: 도서관의 연구 생태계 내 역할을 명확히 하는 증거 기반 개념틀 제안
- **지식 중개자 역할 확립**: 도서관을 단순 저장소에서 능동적 중개자로 재개념화하는 이론적 기여

## How

![Figure 4](figures/fig4.webp)

*Figure 4. Research workflow diagram.*

- 465개 REF 사례 데이터셋 구성 (REF2014, REF2021)
- 도서관명 정확 일치(exact matching) 기반 관련 텍스트 추출
- GPT-4o를 활용한 전략 추출 (prompt engineering으로 5개 사례로 정제)
- 추출 결과의 10% (50개 사례)를 독립적 2인 연구자가 수동 검증
- BERTopic 모델링으로 전략(ws) 및 근거(we) 필드에 차등 가중치 부여
- Library Technology 웹사이트에서 웹 스크래핑으로 도서관 메타데이터 수집

## Originality

- 도서관의 연구 영향 중개 역할을 대규모 실제 사례로 처음 체계적으로 분석
- LLM(GPT-4o)과 BERTopic의 하이브리드 접근법으로 맥락 무결성을 유지하면서 자동 분석 수행
- REF 공식 데이터베이스를 활용하여 검증된 영향 사례 기반의 실증적 근거 제시
- 도서관 유형별 차별화된 전략 존재 가능성을 제기하여 추후 이론화 방향 제안

## Limitation & Further Study

- 영국 REF 데이터만 사용으로 지리적 일반화 가능성 제한 (저자도 향후 다른 지역으로의 확대 필요 언급)
- 자동 추출 단계에서 LLM 환각(hallucination) 위험이 완전히 제거되지 않음 (10% 수동 검증으로 부분 완화)
- 도서관 명칭 정확 일치 방식으로 인한 이름 변경, 약칭 등으로 인한 누락 가능성
- **후속연구 방향**: 공개도서관, 대학도서관, 특수도서관 등 도서관 유형별 전략 차이 분석 필요; 다른 국가·지역 데이터 기반 모델 일반화 가능성 검증; 각 전략의 영향 크기(magnitude) 및 지속성 측정 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 연구는 도서관의 연구 영향 중개 역할을 처음으로 대규모 실제 사례 기반으로 규명하여 이론적·실무적 기여가 크며, 하이브리드 텍스트 분석 기법의 적절한 활용으로 신뢰성을 확보했다. 다만 지역 특수성으로 인한 일반화 제한과 추가 이론적 심화가 필요하다.

## Related Papers

- 🧪 응용 사례: [[papers/1016_Sci2Pol_Evaluating_and_Fine-tuning_LLMs_on_Scientific-to-Pol/review]] — 과학-정책 연결에서 도서관의 중개 역할과 유사하게 과학 연구를 정책으로 변환하는 AI 시스템을 제시한다.
- 🏛 기반 연구: [[papers/1043_The_selective_use_of_physics_knowledge_in_policy_how_interdi/review]] — 정책에서 과학 지식의 선택적 활용에 대한 이론적 배경을 제공하여 도서관의 중개 전략 이해를 돕는다.
- 🔄 다른 접근: [[papers/972_Identifying_interdisciplinary_emergence_in_the_science_of_sc/review]] — 학제간 지식 결합을 통한 사회적 영향 창출의 다른 접근법으로 주제 모델링 기반 분석을 제시한다.
- 🔄 다른 접근: [[papers/964_Funding_the_Frontier_Visualizing_the_Broad_Impact_of_Science/review]] — 과학의 사회적 영향을 도서관 중개 전략과 펀딩 시각화라는 다른 관점에서 접근한다
- 🔗 후속 연구: [[papers/974_Information_Pathways_in_Online_Science_Communication_The_Rol/review]] — 과학 소통의 정보 경로 분석을 도서관의 사회적 중개 역할로 확장한 연구이다
- 🧪 응용 사례: [[papers/1016_Sci2Pol_Evaluating_and_Fine-tuning_LLMs_on_Scientific-to-Pol/review]] — 과학과 사회 간 격차 해소를 위한 도서관 역할 매핑은 LLM 기반 과학-정책 브리프가 실제 지식 전달 생태계에서 어떤 역할을 할 수 있는지 보여줍니다.
- 🏛 기반 연구: [[papers/994_Organisational_accounts_engaged_in_scholarly_communication_o/review]] — 과학과 사회 간 격차를 메우는 도서관 매핑 연구가 기관 계정의 학술 커뮤니케이션 역할 이해의 기초를 제공한다.
- 🏛 기반 연구: [[papers/1137_Art_tourism_a_nascent_concept_but_symptomatic_of_a_trend_Ins/review]] — 과학과 사회를 연결하는 도서관 역할 매핑이 예술 관광에서 문화기관과 사회 연결 분석에 이론적 기반을 제공하기 때문
- 🏛 기반 연구: [[papers/1141_Assistive_technology_for_developmental_conditions_A_scientom/review]] — 보조기술 연구가 과학과 사회 간 격차를 메우는 역할을 도서관 과학의 관점에서 분석할 수 있다.
