---
title: "1021_Scientific_production_in_the_era_of_large_language_models"
authors:
  - "Keigo Kusumegi"
  - "Xinyu Yang"
  - "Paul Ginsparg"
  - "Mathijs de Vaan"
  - "Toby Stuart"
date: "2025"
doi: "10.1126/science.adw3000"
arxiv: ""
score: 4.0
essence: "대규모 LLM(Large Language Models) 도입이 과학 논문 생산성을 36-60% 증가시키고, 특히 비영어권 연구자의 진입장벽을 낮추지만, 글쓰기 복잡도가 더 이상 연구 품질의 신뢰할 수 있는 지표가 되지 않게 변화시킨다."
tags:
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scientific_Language_Model_Development"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kusumegi et al._2025_Scientific production in the era of large language models 2.pdf"
---

# Scientific production in the era of large language models

> **저자**: Keigo Kusumegi, Xinyu Yang, Paul Ginsparg, Mathijs de Vaan, Toby Stuart, Yian Yin | **날짜**: 2025 | **DOI**: [10.1126/science.adw3000](https://doi.org/10.1126/science.adw3000)

---

## Essence


대규모 LLM(Large Language Models) 도입이 과학 논문 생산성을 36-60% 증가시키고, 특히 비영어권 연구자의 진입장벽을 낮추지만, 글쓰기 복잡도가 더 이상 연구 품질의 신뢰할 수 있는 지표가 되지 않게 변화시킨다.

## Motivation

- **Known**: AI 기술이 단백질 구조 예측과 신소재 발견 같은 특정 과학 분야에서 가치를 입증했으나, LLM의 거시적 과학 생산성 영향에 대한 체계적 이해는 부족했다.
- **Gap**: LLM 도입 후 과학 출판 패턴, 저자 생산성, 글쓰기 품질과 출판 성과의 관계 변화에 대한 대규모 실증 데이터가 없었다.
- **Why**: LLM이 급속히 확산되는 상황에서 과학 생산 과정의 근본적 변화를 이해하고, 과학 정책입안자들이 제도를 조정하기 위해 필수적이다.
- **Approach**: 2018년 1월-2024년 6월 arXiv, bioRxiv, SSRN 등 3개 프리프린트 저장소에서 199만 개 논문을 수집하고, AI 탐지 알고리즘(AI detection algorithm)을 적용하여 LLM 사용 여부를 판별한 후, 저자 고정효과 사건 분석(author-level fixed-effects event models)으로 LLM 채택의 인과효과를 추정했다.

## Achievement


- **생산성 증가**: LLM 채택 후 논문 제출 빈도가 arXiv 36.2%, bioRxiv 52.9%, SSRN 59.8% 증가
- **비대칭적 이점**: 아시아계 저자와 아시아 소재 기관 소속 연구자가 23.7-89.3% 생산성 향상으로 영어권 저자(23.7-46.2%)보다 더 큰 이득
- **글쓰기 복잡도 역전**: LLM 비사용 논문은 글쓰기 복잡도가 높을수록 출판 확률 증가하지만, LLM 사용 논문은 복잡도가 높을수록 출판 확률 감소(역의 관계)
- **신뢰성 약화**: LLM이 쉽게 복잡한 과학 문장을 생성하므로, 글쓰기 복잡도가 더 이상 연구 품질의 신뢰할 수 있는 신호가 아님을 입증

## How


- AI 탐지 알고리즘: 2023년 이전 인간 저술 추상을 기준으로 토큰(단어) 분포 학습, ChatGPT 이후 논문과 비교하여 LLM 사용 여부 식별
- 인과추론: LLM 미채택 저자를 대조군으로 설정하고 저자 고정효과 이벤트 스터디 모형으로 채택 전후 생산성 변화 측정
- 네이티브 언어 추정: 저자 이름과 소속 기관 정보를 바탕으로 영어 모국어 여부 분류하여 이질성 분석
- 글쓰기 복잡도 측정: Flesch Reading Ease 점수의 역수를 사용하여 평균 문장 길이와 음절 수 종합
- 출판 결과 추적: 2023년 이후 프리프린트의 동료심사 학술지·학술대회 게재 여부를 2024년 6월까지 추적

## Originality

- LLM 시대의 첫 대규모 거시적 실증 연구: 199만 개 논문 데이터로 LLM 도입의 과학 생산성 영향을 정량화
- 혁신적 인과성 식별 전략: 저자의 '첫 LLM 사용' 시점을 기준으로 한 이벤트 스터디로 순수 인과효과 추정", '글쓰기 품질-출판 성과 관계의 역전 발견: LLM 사용으로 인해 전통적 품질 신호(글쓰기 복잡도)의 예측력이 반전되는 새로운 현상 발견
- 국제 형평성 효과 규명: 비영어권 연구자의 불균형적 이익을 정량적으로 입증하여 과학 민주화의 양면성 분석

## Limitation & Further Study

- **AI 탐지 신뢰도**: 텍스트 기반 AI 탐지 알고리즘의 위양성/위음성 오류 가능성, 특히 정교한 저자의 혼합 사용(hybrid writing) 포착 미흡
- **인과성의 한계**: LLM 채택자와 미채택자 간 관찰되지 않은 이질성(unobserved heterogeneity) 존재 가능, 관찰된 공변량만으로 완전한 인과효과 추정 불가능
- **언어권 추정 오류**: 저자 이름과 소속 기관만으로 네이티브 영어 사용자 분류하므로 개인차 미반영
- **출판 시간 지연**: 프리프린트 제출 후 동료심사 및 게재까지 시간이 소요되므로, 2023년 이후 논문의 출판 결과는 아직 불완전할 수 있음
- **장기 품질 영향 미상**: 글쓰기 복잡도 역전이 실제 과학적 신뢰도 하락을 의미하는지, 아니면 단순 지표 왜곡인지는 추가 검증 필요
- **후속연구**: (1) 생성된 텍스트의 실제 과학적 정확성과 창의성을 직접 평가하는 연구, (2) 5년 이상 장기 인용 영향도(citation impact) 추적, (3) LLM 기능 고도화에 따른 동적 효과 분석, (4) 다양한 학문 분야별 차등 영향 심층 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 과학 출판의 LLM 영향을 최초로 대규모 정량화한 중요한 실증 연구로, 비영어권 연구자 역량강화의 긍정적 효과와 함께 전통적 품질 평가 지표의 신뢰도 약화라는 심각한 제도적 과제를 제시한다. 과학 정책과 동료심사 체계의 근본적 개선이 시급하다.

## Related Papers

- 🏛 기반 연구: [[papers/1077_Quantifying_large_language_model_usage_in_scientific_papers/review]] — LLM 사용 정량화 방법론이 생산성 변화 분석의 측정 기반을 제공한다.
- ⚖️ 반론/비판: [[papers/953_Do_Large_Language_Models_Reduce_Research_Novelty_Evidence_fr/review]] — LLM이 연구 생산성을 높인다는 주장과 연구 참신성을 감소시킨다는 반대 관점을 제시한다.
- 🔗 후속 연구: [[papers/1072_Embracing_Foundation_Models_for_Advancing_Scientific_Discove/review]] — LLM이 과학 논문 생산에 미치는 영향을 기초로 과학 발견 자체를 위한 LLM 활용으로 확장한다.
- ⚖️ 반론/비판: [[papers/1119_Publish_and_Perish_How_AI-Accelerated_Writing_Without_Propor/review]] — 적절한 검토 없는 AI 가속 글쓰기의 폐해는 LLM 시대 과학 생산성 증가의 잠재적 부작용과 질적 우려를 제기합니다.
- 🧪 응용 사례: [[papers/1057_Which_stylistic_features_fool_ChatGPT_research_evaluations/review]] — ChatGPT 연구 평가를 속이는 문체적 특징 분석은 LLM 사용이 과학 논문 품질 평가에 미치는 구체적 영향을 보여줍니다.
- ⚖️ 반론/비판: [[papers/1001_Public_Profile_Matters_A_Scalable_Integrated_Approach_to_Rec/review]] — AI 기반 인용 추천 시스템이 LLM 시대의 과학 논문 생산성 증가에 어떤 영향을 미치는지 비교 분석한다.
- 🔗 후속 연구: [[papers/1033_The_Empowerment_of_Science_of_Science_by_Large_Language_Mode/review]] — 대규모 언어모델이 과학 생산에 미치는 영향을 실증적으로 분석하여 LLM의 과학계량학 적용 가능성을 구체적으로 입증한다.
- 🏛 기반 연구: [[papers/1041_The_Rise_of_Large_Language_Models_and_the_Direction_and_Impa/review]] — 대규모 언어 모델 시대의 과학적 생산성 변화가 연방 펀딩 영향 분석의 이론적 배경을 제공한다.
- 🔄 다른 접근: [[papers/1068_Artificial_intelligence_and_illusions_of_understanding_in_sc/review]] — LLM이 과학 생산에 미치는 영향을 다루지만, 생산성 변화보다는 과학적 이해의 질적 저하에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1072_Embracing_Foundation_Models_for_Advancing_Scientific_Discove/review]] — LLM이 과학 논문 작성에 미치는 영향을 넘어서 과학 발견 자체를 위한 기초 모델 활용으로 확장한다.
- ⚖️ 반론/비판: [[papers/1074_OLMo_Accelerating_the_Science_of_Language_Models/review]] — 언어모델이 과학 생산성에 미치는 영향에 대한 상반된 관점을 제시한다.
- 🧪 응용 사례: [[papers/994_Organisational_accounts_engaged_in_scholarly_communication_o/review]] — 대규모 언어 모델 시대의 과학 생산 연구에서 소셜 미디어 학술 커뮤니케이션이 실제 적용 사례가 된다.
- 🔗 후속 연구: [[papers/953_Do_Large_Language_Models_Reduce_Research_Novelty_Evidence_fr/review]] — 대형 언어모델 시대의 과학 생산 연구가 LLM이 연구 새로움에 미치는 영향을 더 광범위한 맥락에서 분석한다.
- 🔗 후속 연구: [[papers/1140_Assessing_the_impact_of_Open_Research_Information_Infrastruc/review]] — 대형언어모델 시대의 과학적 생산성 연구가 오픈 연구 인프라의 영향 평가 방법론으로 확장될 수 있기 때문
