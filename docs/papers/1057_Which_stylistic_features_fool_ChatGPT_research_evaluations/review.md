---
title: "1057_Which_stylistic_features_fool_ChatGPT_research_evaluations"
authors:
  - "Kayvan Kousha"
  - "Mike Thelwall"
date: "2026.03"
doi: ""
arxiv: ""
score: 4.0
essence: "ChatGPT는 추상(abstract)의 언어적 복잡성과 길이에 과도하게 반응하여 연구 품질을 평가하는데, 이는 인간 전문가의 평가와 달리 스타일 편향(stylistic bias)을 보인다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kousha and Thelwall_2026_Which stylistic features fool ChatGPT research evaluations.pdf"
---

# Which stylistic features fool ChatGPT research evaluations?

> **저자**: Kayvan Kousha, Mike Thelwall | **날짜**: 2026-03-16 | **URL**: [https://arxiv.org/abs/2603.14919](https://arxiv.org/abs/2603.14919)

---

## Essence


ChatGPT는 추상(abstract)의 언어적 복잡성과 길이에 과도하게 반응하여 연구 품질을 평가하는데, 이는 인간 전문가의 평가와 달리 스타일 편향(stylistic bias)을 보인다.

## Motivation

- **Known**: LLM은 논문 제목과 초록만으로도 연구 품질을 적당한 수준으로 추정할 수 있으며, 전체 텍스트보다 이 짧은 정보로 더 나은 성과를 보인다.
- **Gap**: LLM 기반 연구 평가가 왜 인간 전문가 점수와 적당히 일치하는지 메커니즘이 불명확하며, 연구 품질과 무관한 언어적 특성이 LLM 점수에 미치는 영향을 체계적으로 분석한 연구가 부재하다.
- **Why**: LLM이 점점 더 연구 평가 지원에 활용되고 있으므로, 스타일 편향을 파악하여 저자의 조작 가능성을 평가하고 LLM 기반 평가 시스템의 신뢰성을 확보할 필요가 있다.
- **Approach**: UK REF 2021에 제출된 99,277개 논문 데이터셋에서 초록의 가독성, 언어적 복잡성, 길이 등의 지표를 계산하여 ChatGPT 점수 및 전문가 점수와의 상관관계를 비교 분석한다.

## Achievement


- **언어적 복잡성에 대한 편향 발견**: ChatGPT는 많은 학문 분야에서 언어적 복잡성과 길이를 인간 전문가보다 훨씬 강하게 고려하여 점수를 부여한다.
- **분야별 차이 규명**: 주제 영역(UoA)에 따라 스타일 특성과 점수 간 상관관계의 강도와 패턴이 상이하게 나타난다.
- **실무적 위험성 제시**: 긴 초록과 낮은 가독성이 실제 연구 품질과 무관하게 ChatGPT 점수를 높일 수 있어 평가 조작 가능성을 시사한다.

## How


- REF 2021 데이터셋(99,277개 논문)에서 학문 분야별로 층화 샘플링 수행
- 초록의 가독성 지표 계산(Flesch Reading Ease, Gunning Fog Index 등)
- 초록 길이, 단어 수, 문장 수 등의 언어적 특성 추출
- ChatGPT에 제목과 초록을 입력하여 연구 품질 점수 획득
- Pearson/Spearman 상관분석으로 스타일 특성과 LLM 점수의 관계 분석
- 동일 자료에 대해 REF 전문가 점수와의 상관관계도 병렬 분석
- 학문 분야별 부분군 분석으로 차이점 검증

## Originality

- 초록의 객관적 스타일 특성(가독성, 복잡성, 길이)과 LLM 점수의 관계를 체계적으로 규명한 첫 연구
- LLM 편향을 인간 전문가와 직접 비교하는 설계로 '속임수(cheating)' 가설을 실증적으로 검증", 'REF 같은 실제 정책 평가 데이터셋(99,277개)을 사용하여 높은 현실 타당성 제공
- 학문 분야별 차이를 규명하여 분야 특성에 따른 편향의 이질성 입증

## Limitation & Further Study

- **인과관계 미규명**: 상관관계만 분석했으므로 스타일이 점수를 직접 결정하는지 간접요인인지 확실하지 않음
- **프록시 점수 사용**: 개별 논문 점수가 아닌 부서 평균 점수를 대리변수로 사용하여 측정오차 존재
- **ChatGPT 버전 특정성**: 특정 모델 버전만 분석했으므로 다른 LLM이나 최신 버전으로의 일반화 제한
- **인과성 실험 필요**: 향후 A/B 테스트(예: 동일 내용의 고/저 복잡성 초록 제시)로 인과관계 검증
- **개선 방안 연구**: LLM 프롬프트 엔지니어링이나 파인튜닝으로 스타일 편향 완화 방안 모색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LLM의 스타일 편향을 대규모 실증 데이터로 처음 규명한 중요한 연구로, 연구 평가 시스템의 신뢰성 문제를 제기하고 향후 LLM 개선 방향을 제시한다.

## Related Papers

- 🔗 후속 연구: [[papers/1192_Large_language_models_and_responsible_research_evaluation_an/review]] — 대규모 언어 모델의 책임감 있는 연구 평가에서 스타일 편향 문제가 핵심적 고려사항으로 다뤄진다.
- 🧪 응용 사례: [[papers/987_Meta-assessment_of_Bias_in_Science/review]] — 과학에서 편향의 메타 평가가 ChatGPT의 연구 평가 편향을 이해하는 이론적 틀을 제공한다.
- 🏛 기반 연구: [[papers/1077_Quantifying_large_language_model_usage_in_scientific_papers/review]] — 과학 논문에서 LLM 사용 정량화가 ChatGPT 연구 평가의 스타일 편향 분석에 방법론적 기초를 제공한다.
- ⚖️ 반론/비판: [[papers/953_Do_Large_Language_Models_Reduce_Research_Novelty_Evidence_fr/review]] — LLM이 연구 참신성을 감소시킨다는 연구와 ChatGPT가 스타일에 편향된다는 발견은 AI의 연구 평가 능력에 대한 상반된 우려를 보여준다.
- 🔗 후속 연구: [[papers/1068_Artificial_intelligence_and_illusions_of_understanding_in_sc/review]] — AI가 과학 연구 평가에 야기하는 이해의 환상 문제를 ChatGPT의 스타일 편향이라는 구체적 사례로 실증적으로 보여준다.
- 🔄 다른 접근: [[papers/1162_DREAM_Deep_Research_Evaluation_with_Agentic_Metrics/review]] — AI를 활용한 연구 평가 방법을 다루지만, 에이전트 기반 지표보다는 기존 LLM의 편향성 문제를 규명하는 데 집중한다.
- 🧪 응용 사례: [[papers/1021_Scientific_production_in_the_era_of_large_language_models/review]] — ChatGPT 연구 평가를 속이는 문체적 특징 분석은 LLM 사용이 과학 논문 품질 평가에 미치는 구체적 영향을 보여줍니다.
- 🏛 기반 연구: [[papers/1068_Artificial_intelligence_and_illusions_of_understanding_in_sc/review]] — AI 도구의 이해의 환상 문제를 ChatGPT의 스타일 편향이라는 구체적 사례로 실증적으로 입증하는 연구의 이론적 배경을 제공한다.
- 🔗 후속 연구: [[papers/1157_Critical_Review_with_Scientometrics_Approach_on_the_Retrofit/review]] — ChatGPT 연구 평가의 한계를 극복하는 구체적 해결책을 제시한다
- 🔗 후속 연구: [[papers/1162_DREAM_Deep_Research_Evaluation_with_Agentic_Metrics/review]] — ChatGPT 평가 한계를 극복하는 고도화된 AI 평가 시스템으로 발전시킨다
