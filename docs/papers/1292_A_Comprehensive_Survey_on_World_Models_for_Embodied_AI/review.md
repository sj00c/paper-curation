---
title: "1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI"
authors:
  - "Xinqing Li"
  - "Xin He"
  - "Le Zhang"
  - "Min Wu"
  - "Xiaoli Li"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Embodied AI를 위한 World Models에 대한 포괄적 조사로, Functionality, Temporal Modeling, Spatial Representation의 세 축 분류체계를 제안하여 환경 동역학을 캡처하고 예측하는 내부 시뮬레이터를 체계적으로 정리한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_A Comprehensive Survey on World Models for Embodied AI.pdf"
---

# A Comprehensive Survey on World Models for Embodied AI

> **저자**: Xinqing Li, Xin He, Le Zhang, Min Wu, Xiaoli Li, Yun Liu | **날짜**: 2025-10-19 | **URL**: [https://arxiv.org/abs/2510.16732](https://arxiv.org/abs/2510.16732)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Structure of this survey. The figure classifies world models along three axes and illustrates representative met*

Embodied AI를 위한 World Models에 대한 포괄적 조사로, Functionality, Temporal Modeling, Spatial Representation의 세 축 분류체계를 제안하여 환경 동역학을 캡처하고 예측하는 내부 시뮬레이터를 체계적으로 정리한다.

## Motivation

- **Known**: World Models는 model-based RL에서 출발하였으며, 최근 대규모 생성 모델 발전으로 고충실도 예측을 가능하게 하는 범용 환경 시뮬레이터로 확장되었다. 기존 조사들은 기능 중심 또는 응용 중심으로 세분화되어 있다.
- **Gap**: World Models에 대한 통일된 분류체계와 평가 지표의 부재로 인해 서로 다른 하위 커뮤니티 간 용어 불일치가 발생하고 있으며, 통합 데이터셋과 물리적 일관성을 평가하는 메트릭이 부족하다.
- **Why**: Embodied AI 에이전트의 성능은 시간적 일관성, 기하학적 정확성, 실시간 제어의 계산 효율성에 크게 의존하며, 이를 위해서는 시간적 모델링과 공간 표현의 설계가 근본적인 영향을 미친다.
- **Approach**: Decision-Coupled vs. General-Purpose, Sequential Simulation & Inference vs. Global Difference Prediction, Global Latent Vector부터 Decomposed Rendering Representation까지 세 축으로 구성된 통합 분류체계를 제안하고, 로보틱스, 자율주행, 일반 비디오 설정에서 데이터셋과 평가 메트릭을 체계화한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Structure of this survey. The figure classifies world models along three axes and illustrates representative met*

- **통합 분류체계**: Functionality, Temporal Modeling, Spatial Representation의 세 축으로 world models를 조직화하여 기존 조사들의 산재된 관점을 통합한 프레임워크 제시
- **수학적 정식화**: POMDP 기반의 dynamics prior, filtered posterior, reconstruction을 명확히 정의하고 ELBO 최적화 목표를 수립하여 이론적 기초 강화
- **포괄적 자원 정리**: 로보틱스, 자율주행, 일반 비디오 도메인에 걸쳐 데이터셋과 평가 메트릭(픽셀 예측 품질, 상태 수준 이해, 태스크 성능)을 체계화
- **정량적 비교분석**: 최신 state-of-the-art 모델들의 성능 비교 및 물리적 일관성 대 픽셀 충실도, 성능 대 계산 효율성 간 트레이드오프 분석
- **미개척 과제 도출**: 장기 시간적 일관성 달성과 오차 축적 완화의 핵심 모델링 어려움을 특정하고 실시간 제어의 계산 복잡성 문제 제기

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Structure of this survey. The figure classifies world models along three axes and illustrates representative met*

- POMDP 프레임워크를 기반으로 latent state zt에 대한 one-step filtering posterior qϕ(zt | zt−1, at−1, ot)로 부분 관측성 처리
- Markovian factorization 가정 하에 ELBO를 reconstruction 목표 log pθ(ot | zt)와 KL 정규화 항으로 분해하여 학습 목표 수립
- Decision-Coupled 모델은 특정 의사결정 태스크에 최적화된 동역학을 학습하고, General-Purpose 모델은 태스크 불가지론적 환경 시뮬레이터로 설계
- Sequential Simulation & Inference는 자기회귀 방식으로 상태를 단계적 전개하고, Global Difference Prediction은 미래 상태 전체를 병렬로 추정
- 공간 표현은 Global Latent Vector, Token Feature Sequence, Spatial Latent Grid, neural fields 등 기하학적 충실도 수준에 따라 다양화
- Recurrent, Transformer, Diffusion 기반 디코더 등 다양한 아키텍처로 인스턴스화하여 모델 유연성 확보
- 로보틱스, 자율주행, 일반 비디오 도메인별 표준화된 데이터셋과 평가 메트릭 수립으로 비교 가능성 확보

## Originality

- 기존 기능 중심 또는 응용 중심 분류에서 벗어나 temporal modeling과 spatial representation을 명시적 축으로 도입한 삼축 분류체계의 혁신적 제안
- Sequential Simulation & Inference vs. Global Difference Prediction의 이분법적 구분으로 시간적 모델링 패러다임의 근본적 차이를 명확히 함
- Global Latent Vector부터 Decomposed Rendering Representation까지 공간 표현의 계층적 분류를 통해 기하학적 충실도와 계산 복잡성의 연속체 구성
- 물리적 일관성 평가 메트릭의 필요성을 명시적으로 제기하여 픽셀 충실도 중심의 평가 패러다임 전환 촉구
- long-horizon error accumulation 문제를 세 가지 핵심 미개척 과제(통합 데이터셋 부재, 평가 메트릭 부족, 시간적 일관성 vs. 계산 효율성 트레이드오프) 중 하나로 체계화

## Limitation & Further Study

- 조사 논문의 특성상 새로운 알고리즘이나 실험 결과를 제시하지 않아 이론적 기여에 국한되며, 제시된 분류체계의 실질적 유용성은 추후 적용 사례에 따라 결정될 필요
- 세 축 분류체계가 현존 모델을 충분히 포괄하는지, 새로운 패러다임(예: 멀티모달 학습, 메모리 증강 아키텍처)의 등장 시 확장 가능성이 명확하지 않음
- POMDP 기반 수학적 정식화는 표준적이나, Global Difference Prediction 모델들이 이 프레임워크에 어떻게 매핑되는지 구체적 설명 부족
- 로보틱스, 자율주행, 일반 비디오 간 도메인 특화성이 크지만, 도메인 간 모델 전이 가능성이나 통합 평가 방안에 대한 논의 미흡
- 후속 연구로는 제시된 분류체계 기반의 벤치마크 구축, 통합 데이터셋 개발, 물리적 일관성 메트릭 정의, 장기 예측 오차 축적 해결 방안 모색이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 조사는 world models 분야의 산재된 문헌을 통합하는 체계적인 분류체계와 수학적 기초를 제시하여, embodied AI 연구의 방향성 제시와 평가 표준화에 기여할 잠재력이 높다. 다만 새로운 실험적 증거나 알고리즘 혁신이 없어 기여도가 구조화와 정리에 한정되며, 제시된 체계가 빠르게 변화하는 생성 모델 환경에서 장기적 유용성을 갖기 위해서는 후속 벤치마킹 및 메트릭 개발이 필수적이다.

## Related Papers

- 🏛 기반 연구: [[papers/1294_A_Generalist_Agent/review]] — Gato의 다중 모달리티 처리 개념이 embodied AI를 위한 world model 설계의 중요한 이론적 기반을 제공
- 🧪 응용 사례: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — Genie의 생성형 환경 모델이 본 서베이에서 제시한 world model 분류체계의 실제 구현 사례
- 🧪 응용 사례: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — World Model을 자율주행이라는 구체적 도메인에 적용한 사례를 제공한다.
- 🔗 후속 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — World Model을 활용한 다양한 도메인 마스터링 방법론을 제시한다.
- 🔄 다른 접근: [[papers/1630_WMNav_Integrating_Vision-Language_Models_into_World_Models_f/review]] — VLM을 World Model에 통합하는 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1631_World_Models/review]] — World Models의 기본 개념과 이론적 토대를 embodied AI 맥락에서 체계적으로 정리한 확장 연구입니다.
- 🔄 다른 접근: [[papers/1355_DreamDojo_A_Generalist_Robot_World_Model_from_Large-Scale_Hu/review]] — 세계 모델 학습에서 인간 동영상과 3D 표현을 각각 활용하는 서로 다른 접근법입니다.
- 🏛 기반 연구: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — embodied AI의 world model과 multimodal foundation model의 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — DreamerV3의 world model 접근법은 embodied AI를 위한 세계 모델 연구의 핵심 기초를 제공한다.
- 🏛 기반 연구: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — World Models for Embodied AI 서베이가 대규모 모델 기반 embodied AI의 의사결정과 학습에 필요한 세계 모델 이론을 제공함
- 🏛 기반 연구: [[papers/1481_Motus_A_Unified_Latent_Action_World_Model/review]] — embodied AI를 위한 world model의 포괄적인 이론적 기반을 제공하여 Motus의 unified latent action world model 설계에 필수적인 배경지식을 제공한다.
- 🏛 기반 연구: [[papers/1492_Neural_Brain_A_Neuroscience-inspired_Framework_for_Embodied/review]] — 신경과학 기반 Neural Brain은 embodied AI를 위한 월드 모델의 생물학적 영감을 제공합니다.
- 🏛 기반 연구: [[papers/1494_NORA-15_A_Vision-Language-Action_Model_Trained_using_World_M/review]] — world model 기반 학습의 이론적 기초와 embodied AI에서의 world model 활용 방법론을 제공한다.
- 🏛 기반 연구: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — World model 기반 embodied AI의 전반적 이해가 reflective planning 연구의 기초가 된다.
- 🏛 기반 연구: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — embodied AI를 위한 world model의 포괄적 이해를 제공하는 기반 서베이 연구입니다.
- 🏛 기반 연구: [[papers/1630_WMNav_Integrating_Vision-Language_Models_into_World_Models_f/review]] — World model 기반 embodied AI에 대한 포괄적인 이론적 배경과 survey를 제공한다.
- 🔗 후속 연구: [[papers/1631_World_Models/review]] — World Models for Embodied AI 서베이가 World Models의 기본 개념을 embodied AI 전반으로 확장하여 최신 발전사항을 종합적으로 다룬다
- 🔗 후속 연구: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — World Model 서베이에서 제시된 개념들을 V-JEPA 2가 비디오 기반으로 실현한다.
- 🏛 기반 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — World Models for Embodied AI의 포괄적 조사가 VLN taxonomy의 이론적 배경과 미래 발전 방향을 제시한다.
- 🏛 기반 연구: [[papers/1313_Aspects_of_entanglement_with_background_electric_and_magneti/review]] — 양자장론적 entanglement 개념이 World Model의 시공간 표현 이론에 기초를 제공한다.
- 🔗 후속 연구: [[papers/1387_EWMBench_Evaluating_Scene_Motion_and_Semantic_Quality_in_Emb/review]] — Embodied AI를 위한 world model 서베이는 EWMBench가 벤치마킹하는 EWM 기술들의 포괄적인 이론적 배경을 제공합니다.
- 🔗 후속 연구: [[papers/1359_Diffusion_for_World_Modeling_Visual_Details_Matter_in_Atari/review]] — Atari에서 검증된 diffusion world model을 더 복잡한 3D 환경으로 확장할 수 있는 방향을 제시합니다.
- 🔗 후속 연구: [[papers/1299_A_Survey_of_Robotic_Navigation_and_Manipulation_with_Physics/review]] — Embodied AI를 위한 World Model 서베이와 물리 시뮬레이터 서베이가 상호 보완적인 관점을 제공합니다.
- 🔗 후속 연구: [[papers/1305_Aligning_Cyber_Space_with_Physical_World_A_Comprehensive_Sur/review]] — Embodied AI를 위한 World Model 포괄 서베이와 사이버-물리 연결 서베이가 상호 보완적 관점을 제공합니다.
- 🧪 응용 사례: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D-VLA는 World Models 서베이에서 제시된 3D spatial representation과 generative modeling 개념을 실제 로봇 시스템에 구현한 사례입니다.
- 🏛 기반 연구: [[papers/1368_DiWA_Diffusion_Policy_Adaptation_with_World_Models/review]] — World model을 활용한 policy adaptation의 기본 개념과 구조를 제공합니다.
