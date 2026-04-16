---
title: "1033_The_Empowerment_of_Science_of_Science_by_Large_Language_Mode"
authors:
  - "Guoqiang Liang"
  - "Jingqian Gong"
  - "Mengxuan Li"
  - "Gege Lin"
  - "Shuo Zhang"
date: "2025.11"
doi: "10.48550/arXiv.2511.15370"
arxiv: ""
score: 3.0
essence: "대규모언어모델(LLM)의 핵심 기술(프롬프트 엔지니어링, RAG, 파인튜닝 등)을 정리하고 과학계량학(SciSci) 분야에의 적용 가능성을 제시하는 종합 리뷰 논문이다."
tags:
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Scientific_Language_Model_Development"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liang et al._2025_The Empowerment of Science of Science by Large Language Models New Tools and Methods.pdf"
---

# The Empowerment of Science of Science by Large Language Models: New Tools and Methods

> **저자**: Guoqiang Liang, Jingqian Gong, Mengxuan Li, Gege Lin, Shuo Zhang | **날짜**: 2025-11-19 | **DOI**: [10.48550/arXiv.2511.15370](https://doi.org/10.48550/arXiv.2511.15370)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Parameters and classification of notable LLMs*

대규모언어모델(LLM)의 핵심 기술(프롬프트 엔지니어링, RAG, 파인튜닝 등)을 정리하고 과학계량학(SciSci) 분야에의 적용 가능성을 제시하는 종합 리뷰 논문이다.

## Motivation

- **Known**: LLM은 자연어 처리, 이미지 인식, 멀티모달 작업에서 우수한 성능을 보이고 있으며, GPT 시리즈의 발전을 통해 Transformer 아키텍처 기반의 모델이 주류를 이루고 있다. 과학계량학은 인용 분석, 토픽 모델링, 그래프 신경망 등 전통적 방법에서 AI 기반 방법으로 진화하고 있다.
- **Gap**: LLM의 핵심 기술 체계(프롬프트, RAG, 파인튜닝, 사전훈련, 도구 학습)가 과학계량학 분야에 어떻게 구체적으로 통합될 수 있는지에 대한 통합적 로드맵이 부재하다. AI 에이전트 기반 과학평가 모델의 실제 구현 방법과 신흥 연구 분야 탐지 및 지식 그래프 구축의 LLM 기반 방법론이 명확하지 않다.
- **Why**: LLM은 현재 AI 분야의 인프라로 작용하며 전 산업에 영향을 미치고 있으므로, 학문 평가와 과학 정책 수립이 이루어지는 과학계량학에 LLM을 효과적으로 도입하는 것은 미래 과학 생태계 구축에 필수적이다.
- **Approach**: LLM의 기술 아키텍처와 개념을 사용자 관점에서 체계적으로 분류하고 설명한 후, 과학계량학의 역사적 발전 과정을 추적하여 LLM의 잠재적 적용 영역을 도출한다. 이를 통해 AI 에이전트 기반 과학평가 모델, 신흥 연구 탐지, 지식 그래프 구축 방법을 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Parameters and classification of notable LLMs*

- **LLM 기술 체계 정리**: Transformer와 MoE 아키텍처 분류, 일반 목적 모델과 수직 모델의 구분, 프롬프트 엔지니어링, RAG, 파인튜닝, 사전훈련, 도구 학습 등 5대 핵심 기술 설명
- **과학계량학 진화 추적**: 인용 분석에서 BERT, GCN, 지식 그래프 등 AI 기반 방법으로의 패러다임 전환 기록
- **LLM의 SciSci 응용 전망 제시**: AI 에이전트 기반 과학평가 모델 구상, 신흥 연구 분야 탐지 및 지식 그래프 구축 방법론 제안
- **용어 체계화**: 토크나이제이션, 임베딩, AI 에이전트 등 개념 간 관계를 도식화하여 LLM 이해도 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2. The common terminology and relation of LLMs*

- LLM 분류 기준의 다층적 분석: 입력 데이터 유형(언어/시각/멀티모달), 아키텍처(Transformer/MoE), 적용 영역(일반/수직)
- GPT 시리즈(GPT-1부터 ChatGPT-4)의 진화 과정을 파라미터, 레이어, 학습 데이터 규모 지표로 정량화
- 과학계량학의 방법론 변화를 시간대별로 정렬: 전통적 방법(인용 분석, 단어 빈도)→기계학습(동적 토픽 모델, Word2Vec)→딥러닝(BERT, GCN, 지식 그래프)
- LLM 기술의 SciSci 영역별 맵핑을 통한 구체적 활용 시나리오 제시

## Originality

- 과학계량학 분야에 대한 LLM의 체계적 적용 가능성을 최초로 종합적으로 검토한 리뷰
- 사용자 관점의 LLM 기술 설명으로 학제간 접근성 강화 (기술 깊이보다 활용성 중심)
- 전통적 과학계량학 방법론에서 AI 기반 방법론으로의 패러다임 전환을 역사적 맥락에서 명확화
- AI 에이전트 기반 과학평가 모델이라는 새로운 개념 도입으로 과학 거버넌스 혁신 가능성 시사

## Limitation & Further Study

- 제시된 LLM 적용 사례들(신흥 연구 탐지, 지식 그래프 구축)이 구체적인 구현 세부사항, 성능 평가 지표, 검증 결과 없이 고수준의 개념 수준에 머물러 있음
- AI 에이전트 기반 과학평가 모델의 윤리적 우려(학자 평가의 자동화로 인한 편향, 투명성 부족)에 대한 논의 부재
- LLM의 환각(hallucination) 문제, 학습 데이터 편향(미국 61개 vs 중국 15개 모델의 격차)이 과학계량학 적용 시 야기할 수 있는 문제에 대한 분석 불충분
- 후속 연구: 실제 SciSci 데이터셋을 사용한 LLM 기반 방법론의 벤치마크 성능 평가 필요. AI 에이전트의 과학평가 활용에 대한 규제 프레임워크 개발. 다국어 과학 문헌 처리를 위한 비영어권 LLM의 역할 확대 연구

## Evaluation

- Novelty: 3/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 3/5

**총평**: 본 논문은 LLM의 핵심 기술을 명확하게 정리하고 과학계량학의 미래 방향을 제시하는 가치 있는 리뷰이나, 제안된 적용 방법론들이 개념 수준에서 구체적 구현 사례와 검증 결과로 뒷받침되지 못하여 실제 임팩트 평가가 어렵다.

## Related Papers

- 🔗 후속 연구: [[papers/1021_Scientific_production_in_the_era_of_large_language_models/review]] — 대규모 언어모델이 과학 생산에 미치는 영향을 실증적으로 분석하여 LLM의 과학계량학 적용 가능성을 구체적으로 입증한다.
- 🧪 응용 사례: [[papers/1077_Quantifying_large_language_model_usage_in_scientific_papers/review]] — 과학 논문에서 LLM 사용량을 정량화하여 LLM이 과학계량학에 미치는 실제 영향을 측정한다.
- 🏛 기반 연구: [[papers/1069_Breaking_the_gatekeepers_how_AI_will_revolutionize_scientifi/review]] — AI가 과학적 발견 과정을 어떻게 혁신할 수 있는지에 대한 이론적 배경을 제공한다.
- ⚖️ 반론/비판: [[papers/1192_Large_language_models_and_responsible_research_evaluation_an/review]] — LLM을 활용한 연구 평가에서 발생할 수 있는 책임과 윤리적 문제들을 제기하여 신중한 접근을 요구한다.
- 🔗 후속 연구: [[papers/1022_SciSciGPT_advancing_humanAI_collaboration_in_the_science_of/review]] — 과학학 분야 인간-AI 협력 연구에서 LLM의 과학학 역량 강화로 구체적 기술 영역이 확장된다.
- ⚖️ 반론/비판: [[papers/953_Do_Large_Language_Models_Reduce_Research_Novelty_Evidence_fr/review]] — LLM이 연구 참신성을 감소시킨다는 우려와 과학학 역량 강화라는 긍정적 관점이 대조된다.
- 🏛 기반 연구: [[papers/1016_Sci2Pol_Evaluating_and_Fine-tuning_LLMs_on_Scientific-to-Pol/review]] — 대규모 언어 모델에 의한 과학의 과학 분야 강화는 과학-정책 브리프 생성에서 LLM 활용의 이론적 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1114_GoAI_Enhancing_AI_Students_Learning_Paths_and_Idea_Generatio/review]] — LLM 기반 과학 발견을 교육 분야에 구체적으로 적용한 실용적 사례다
- 🔗 후속 연구: [[papers/931_AI-Driven_Automation_Can_Become_the_Foundation_of_Next-Era_S/review]] — AI4SoS 자동화 프레임워크가 LLM의 과학 연구 역량 강화라는 더 넓은 맥락에서 구체적 실현 방안을 제시합니다.
- 🏛 기반 연구: [[papers/1072_Embracing_Foundation_Models_for_Advancing_Scientific_Discove/review]] — LLM이 과학의 과학 분야를 어떻게 강화할 수 있는지에 대한 기반적 논의를 과학 발견으로 구체화한다.
- 🔗 후속 연구: [[papers/1073_MOLIERE_Automatic_Biomedical_Hypothesis_Generation_System/review]] — LLM을 활용한 과학 발견 자동화 시스템의 차세대 발전 방향을 제시한다
- 🧪 응용 사례: [[papers/1078_Quantifying_the_use_and_potential_benefits_of_artificial_int/review]] — AI가 과학의 과학 분야에 미치는 구체적인 영향과 활용 사례를 보여준다.
- 🔗 후속 연구: [[papers/963_Forecasting_the_future_of_artificial_intelligence_with_machi/review]] — 대형 언어 모델이 과학의 과학 연구에 미치는 영향을 AI 연구 예측의 구체적 사례로 확장 분석한다.
- 🔗 후속 연구: [[papers/1140_Assessing_the_impact_of_Open_Research_Information_Infrastruc/review]] — NLP 기반 scientometrics를 대규모 언어모델을 활용한 과학학 연구로 확장할 수 있다.
- 🔗 후속 연구: [[papers/1170_Evolution_of_Social_Work_Knowledge_Production_Over_35_Years/review]] — AI가 사회복지 지식 생산에 미치는 영향을 대규모 언어모델의 과학학 혁신과 연계하여 분석할 수 있다.
- 🏛 기반 연구: [[papers/1179_Global_Research_Trends_in_Knowledge_Management_in_Higher_Edu/review]] — 고등교육 지식관리에서 AI와 디지털 변환의 미래 방향을 대규모 언어모델 연구로 뒷받침할 수 있다.
- 🔗 후속 연구: [[papers/1153_Classical_RAG_for_Semantic_Search__Quantum_Modules_for_Resea/review]] — LLM 기반 과학학 연구에서 양자 컴퓨팅 모듈을 통합한 차세대 연구 평가 시스템으로 확장한다.
