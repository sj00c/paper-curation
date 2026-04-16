---
title: "1078_Quantifying_the_use_and_potential_benefits_of_artificial_int"
authors:
  - "Jian Gao"
  - "Dashun Wang"
date: "2024.10"
doi: "10.1038/s41562-024-02020-5"
arxiv: ""
score: 4.0
essence: "AI가 과학 연구에 직접 사용되는 정도와 잠재적 이점을 정량적으로 측정하는 프레임워크를 개발하여, AI 사용이 2015년 이후 급증하고 있으나 교육과 실제 적용 간 괴리가 존재함을 밝혔다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gao and Wang_2024_Quantifying the use and potential benefits of artificial intelligence in scientific research.pdf"
---

# Quantifying the use and potential benefits of artificial intelligence in scientific research

> **저자**: Jian Gao, Dashun Wang | **날짜**: 2024-10-11 | **DOI**: [10.1038/s41562-024-02020-5](https://doi.org/10.1038/s41562-024-02020-5)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1 | Measuring the direct use of AI in scientific research. a, The ‘AI n-gram*

AI가 과학 연구에 직접 사용되는 정도와 잠재적 이점을 정량적으로 측정하는 프레임워크를 개발하여, AI 사용이 2015년 이후 급증하고 있으나 교육과 실제 적용 간 괴리가 존재함을 밝혔다.

## Motivation

- **Known**: AI가 단백질 구조 예측, 신약 설계, 물리 법칙 발견 등 다양한 분야에서 전문가 수준의 성능을 보이고 있다. 경제 및 노동 시장에 미치는 영향에 대한 연구는 진행되어 왔으나 과학 연구에 미치는 영향은 명확하지 않다.
- **Gap**: AI의 광범위한 응용에도 불구하고, 실제로 어느 정도의 AI가 과학 전 분야에서 사용되는지, 그것이 과학 발전에 어떤 이점을 가져오는지에 대한 체계적 이해가 부족하다.
- **Why**: AI 개발을 더 효과적으로 안내하고, 과학 정책 수립에 근거를 제공하며, AI 활용의 형평성과 지속가능성 문제를 규명하는 것이 중요하다.
- **Approach**: 74.6백만 개의 학술 논문과 710만 개의 특허를 분석하여, AI n-gram 프레임워크로 AI의 직접 사용을 측정하고, AI 능력(capability)-분야 작업(task) 프레임워크로 잠재적 이점을 정량화했다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4 | Gender and racial disparities in the use and benefits of AI across*

- **광범위한 AI 사용 현황**: 19개 학문 분야 전반에서 AI 사용이 확산되고 있으며, 2000년 컴퓨터과학 0.5%에서 2019년 1.3%로 증가했고, 2015년 이후 특히 급격한 상승세를 보임
- **AI 사용의 이점**: AI를 언급한 논문이 그렇지 않은 논문 대비 평균 1.816배 더 많은 인용을 받으며(평균 1.069배의 학제 간 인용), AI 사용이 적은 분야에서 더 큰 효과를 보임
- **교육-적용 괴리**: AI 교육 공급과 실제 연구에서의 수요 사이에 상당한 불일치가 존재함을 발견
- **인구통계학적 불평등**: 여성 과학자 또는 흑인 과학자의 비율이 높은 분야에서 AI의 이점을 더 적게 얻고 있으며, 이는 과학 분야의 기존 불평등을 심화시킬 가능성이 있음

## How

![Figure 2](figures/fig2.webp)

*Fig. 2 | Measuring the potential benefits of AI and discipline heterogeneity.*

- Microsoft Academic Graph(MAG) 데이터셋에서 1960-2019년 74.6백만 개 논문 추출
- US Patent and Trademark Office(USPTO)에서 1976-2019년 710만 개 특허 추출
- 키워드 기반 접근법으로 AI 논문 및 특허 식별
- AI 논문에서 bigram/trigram(예: 'deep learning') 추출하여 AI n-gram 생성", '각 분야 및 연도별 논문에서 AI n-gram의 가중 빈도 계산으로 직접 AI 사용도 측정
- AI 논문/특허 제목에서 동사-명사 쌍(예: 'learn representation') 추출로 AI 능력 추론", '각 분야 논문 제목에서 동사-명사 쌍 추출로 분야별 작업 추정
- AI 능력과 분야 작업 간의 중첩도 계산으로 잠재적 이점 측정
- 시간 경과에 따른 변화 분석 및 2015년 기준 AI 능력 고정 실험 수행
- 학문 분야별, 성별, 인종별 분석으로 이질성 및 불평등 규명

## Originality

- 학술 논문과 특허의 빅데이터 통합을 통해 과학 연구에서의 AI 사용을 최초로 체계적으로 정량화
- AI n-gram 프레임워크와 AI 능력-분야 작업 프레임워크라는 이중 측정 방식으로 직접 사용과 잠재적 이점을 동시에 분석
- 미래 노동(future of work) 문헌의 방법론을 과학 정책 영역에 창의적으로 적용
- AI 사용의 인구통계학적 불평등을 과학 분야에서 처음으로 규명
- 2015년 기준 고정 AI 능력 실험으로 시간 경과에 따른 변화가 기술 진보 vs. 분야별 방향 전환 중 어느 것에서 비롯했는지 구분

## Limitation & Further Study

- 키워드 기반 AI 식별 방식의 한계로, AI를 명시하지 않으면서 사용하는 논문들을 포착하지 못할 수 있음
- AI n-gram이 AI의 모든 활용을 완벽히 반영하지 못하며, 특히 narrow AI에 초점이 맞춰져 있음
- 2019년까지의 데이터만 포함되어 최근 ChatGPT 등의 생성형 AI 영향을 반영하지 못함
- 인용 빈도가 질적 영향의 완벽한 지표가 아닐 수 있으며, 다른 이점(연구 속도 향상, 비용 절감 등)의 정량화 부재
- 동사-명사 쌍 추출의 정확도 및 문맥 해석의 한계
- 후속 연구는 (1) 실시간 또는 준실시간 데이터 수집, (2) 질적 인터뷰를 통한 검증, (3) 분야별 AI 적용의 실질적 제약요인 분석이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 과학 연구에서의 AI 활용을 대규모 데이터와 창의적 정량화 방법론으로 체계적으로 분석한 획기적인 연구로, 정책 입안과 형평성 논의에 중요한 근거를 제공한다.

## Related Papers

- 🔗 후속 연구: [[papers/1041_The_Rise_of_Large_Language_Models_and_the_Direction_and_Impa/review]] — LLM이 과학에 미치는 영향을 AI 기술 전반의 연구 방향성 변화로 확장하여 분석한다.
- 🏛 기반 연구: [[papers/962_Forecasting_high-impact_research_topics_via_machine_learning/review]] — 머신러닝을 이용한 연구 주제 예측 방법론이 AI 활용도 측정의 기술적 기반이 된다.
- 🔗 후속 연구: [[papers/1134_A_scientometrics_survey_of_machine_learning_and_neural_netwo/review]] — 기계학습 응용의 과학계량학적 조사와 AI 사용의 정량적 측정은 모두 AI의 과학 연구 영향을 체계적으로 분석한다.
- 🏛 기반 연구: [[papers/1077_Quantifying_large_language_model_usage_in_scientific_papers/review]] — 과학 논문에서의 대형 언어 모델 사용량 정량화가 AI의 과학 연구 활용도를 측정하는 구체적 방법론을 제공한다.
- 🏛 기반 연구: [[papers/1066_Accelerating_science_with_human-aware_artificial_intelligenc/review]] — 인간-인식형 AI 시스템 개발을 위한 현재 AI 활용 현황의 기초 데이터를 제공한다.
- 🧪 응용 사례: [[papers/1033_The_Empowerment_of_Science_of_Science_by_Large_Language_Mode/review]] — AI가 과학의 과학 분야에 미치는 구체적인 영향과 활용 사례를 보여준다.
- 🔗 후속 연구: [[papers/1082_The_Open_Catalyst_2022_OC22_Dataset_and_Challenges_for_Oxide/review]] — 과학 연구에서 AI 활용 효과를 정량화하는 연구에 촉매 연구용 대규모 데이터셋 개발이 중요한 사례가 되기 때문
- 🔗 후속 연구: [[papers/1077_Quantifying_large_language_model_usage_in_scientific_papers/review]] — LLM 사용 정량화를 AI 전반의 과학 연구 활용도와 잠재적 이익 측정으로 확장한다.
- 🏛 기반 연구: [[papers/1134_A_scientometrics_survey_of_machine_learning_and_neural_netwo/review]] — 인공지능의 사용량과 잠재적 이익 정량화가 심혈관질환 연구에서 기계학습 응용 동향 분석의 배경을 제공한다.
