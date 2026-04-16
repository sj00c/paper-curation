---
title: "1631_World_Models"
authors:
  - "David Ha"
  - "Jürgen Schmidhuber"
date: "2018.03"
doi: ""
arxiv: ""
score: 4.0
essence: "환경의 생성형 신경망 world model을 비지도학습으로 학습한 후, 추출된 특징으로 간단한 policy를 훈련하여 강화학습 문제를 해결하는 방법을 제시한다. 심지어 world model이 생성한 상상의 환경에서 훈련한 policy를 실제 환경에 전이 가능함을 보인다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_AI_Architectures"
  - "sub/Generative_Video-Language_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ha and Schmidhuber_2018_World Models.pdf"
---

# World Models

> **저자**: David Ha, Jürgen Schmidhuber | **날짜**: 2018-03-27 | **URL**: [https://arxiv.org/abs/1803.10122](https://arxiv.org/abs/1803.10122)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3. In this work, we build probabilistic generative models of*

환경의 생성형 신경망 world model을 비지도학습으로 학습한 후, 추출된 특징으로 간단한 policy를 훈련하여 강화학습 문제를 해결하는 방법을 제시한다. 심지어 world model이 생성한 상상의 환경에서 훈련한 policy를 실제 환경에 전이 가능함을 보인다.

## Motivation

- **Known**: 강화학습에서 좋은 상태 표현과 미래 예측 모델이 도움이 된다는 것은 알려져 있으며, RNN 기반 world model과 controller의 조합도 이전 연구들(1990-2015)에서 다루어졌다.
- **Gap**: 기존 model-free RL은 작은 네트워크만 사용했는데, 큰 RNN을 효율적으로 훈련하면서도 credit assignment 문제를 해결하는 방법이 부족했다. 또한 이러한 개념들을 실제 RL 환경에서 단순하고 체계적으로 실증하는 연구가 필요했다.
- **Why**: 인간의 뇌는 제한된 감각 정보로부터 내부 모델을 구축하여 빠른 의사결정을 수행하는데, 인공 에이전트도 이를 모방하면 더 효율적이고 해석 가능한 정책을 학습할 수 있기 때문이다.
- **Approach**: 에이전트를 VAE 기반 비전 모듈(V), MDN-RNN 기반 메모리 모듈(M), 선형 컨트롤러(C) 세 부분으로 분해하여, V와 M은 비지도학습으로 world model을 학습하고 C는 이 표현을 이용해 간단하게 훈련한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4. Our agent consists of three components that work closely*

- **모듈화된 아키텍처**: VAE로 공간 정보를, MDN-RNN으로 시간 정보를 각각 압축하여 효율적인 표현 학습
- **확장 가능한 모델**: 전체 1천만 개 파라미터 규모로 확장하면서도 credit assignment 문제를 선형 컨트롤러로 단순화
- **꿈 훈련**: learned world model 내에서 완전히 훈련한 policy를 실제 환경에 성공적으로 전이 가능
- **간단한 policy**: 비지도 학습된 world model 특징만으로도 복잡한 task를 해결하는 최소한의 linear controller로 충분

## How

![Figure 5](figures/fig5.webp)

*Figure 5. Flow diagram of a Variational Autoencoder (VAE).*

- VAE encoder로 각 프레임을 잠재 벡터 z로 압축
- MDN-RNN으로 P(z_{t+1} | a_t, z_t, h_t) 형태로 다음 상태의 확률 분포 모델링
- Temperature 파라미터 τ로 모델의 불확실성 제어
- 선형 모델 a_t = W_c [z_t h_t] + b_c로 컨트롤러 구성
- 비지도학습으로 V, M을 먼저 훈련한 후, 선형 컨트롤러 C만 별도로 훈련
- Learned world model 상에서 직접 policy 최적화 가능

## Originality

- 세 가지 컴포넌트(V, M, C)의 명확한 분리와 단계적 훈련 전략이 실용적이고 체계적
- MDN-RNN을 통한 확률적 world model 학습으로 stochastic 환경 처리
- World model 내 할루시네이션 환경에서 훈련한 정책을 실제 환경으로 전이하는 개념 실증
- 비지도학습 world model로 model-free RL의 credit assignment 문제 우회

## Limitation & Further Study

- 선형 컨트롤러는 simple하지만 복잡한 제어 문제에는 제한적일 수 있음
- World model의 오차가 누적되면 long-horizon 훈련에서 성능 저하 가능
- 현재 실험이 OpenAI Gym의 특정 환경에만 한정되어 일반화 가능성 검증 필요
- VAE의 reconstruction loss와 MDN-RNN의 예측 오차가 최종 policy 성능에 미치는 영향 분석 부족
- 후속 연구에서 더 큰 규모(10^8-10^9 파라미터)의 world model 적용 가능성 탐색 제안

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 reinforcement learning과 생성 모델을 우아하게 결합하여 효율적인 policy 학습을 달성했으며, world model 기반 접근법의 실용성을 명확히 입증한 영향력 있는 작업이다. 모듈화된 설계와 dream training 개념은 이후 연구에 큰 영감을 주었다.

## Related Papers

- 🔗 후속 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — World Models for Embodied AI 서베이가 World Models의 기본 개념을 embodied AI 전반으로 확장하여 최신 발전사항을 종합적으로 다룬다
- 🔗 후속 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — Mastering Diverse Domains through World Models가 원래 World Models를 다양한 도메인으로 확장하여 더 일반화된 접근법을 제시한다
- 🧪 응용 사례: [[papers/1359_Diffusion_for_World_Modeling_Visual_Details_Matter_in_Atari/review]] — Diffusion for World Modeling이 World Models의 생성형 모델링 아이디어를 diffusion 기법으로 구현하여 실제 Atari 환경에서 검증한다
- 🔗 후속 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — Structured World Models from Human Videos가 인간 비디오 데이터를 활용하여 World Models의 학습 데이터 범위를 크게 확장한다
- 🏛 기반 연구: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — WHALE의 확장 가능한 world model 연구가 환경의 생성형 신경망 world model을 비지도학습으로 구축하는 기본 개념의 기반이 되었다.
- 🏛 기반 연구: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — World Models의 생성형 world model 개념이 TriVLA의 에피소딕 월드 모델과 미래 동역학 예측의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — 기본적인 생성형 world model 개념을 비디오 foundation model과 물리적 AI 액션을 위한 현대적 프레임워크로 발전시켰다.
- 🏛 기반 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — World Models의 기본 개념과 이론적 토대를 embodied AI 맥락에서 체계적으로 정리한 확장 연구입니다.
- 🏛 기반 연구: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — World Models의 기본 개념을 자율주행 도메인에 video-text-action으로 확장한 구체적 구현이다.
- 🔗 후속 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — 초기 World Models 연구를 확장하여 150개 이상 도메인에서 안정적으로 작동하는 범용 RL 알고리즘으로 발전시켰다.
- 🏛 기반 연구: [[papers/1439_IPR-1_Interactive_Physical_Reasoner/review]] — World Models의 기본 개념을 VLM 정책과 결합하여 상호작용 기반 물리 추론을 구현한다.
- 🏛 기반 연구: [[papers/1452_Learning_Interactive_Real-World_Simulators/review]] — world model의 기본 개념과 원리를 interactive real-world simulation에 적용하는 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1481_Motus_A_Unified_Latent_Action_World_Model/review]] — world model의 기본 개념과 원리를 unified latent action space에서 구현하는 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — World Models의 기본 개념을 인간 비디오 데이터로 확장하여 로봇 조작 작업에 특화된 structured world model로 발전시켰다.
- 🔗 후속 연구: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 기본적인 생성형 world model을 에피소딕 메모리와 삼중 시스템 아키텍처로 확장하여 장기 조작 작업에 특화했다.
- 🔗 후속 연구: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — 기본적인 생성형 world model을 행동 조건화와 확장 가능성을 갖춘 embodied 환경 특화 모델로 발전시켰다.
- 🏛 기반 연구: [[papers/1630_WMNav_Integrating_Vision-Language_Models_into_World_Models_f/review]] — world model의 기본 개념이 VLM 기반 world model navigation의 이론적 기반입니다.
- 🔄 다른 접근: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — World Models와 V-JEPA 2 모두 환경 모델링을 다루지만 비디오와 일반적 접근법이 다르다.
- 🔄 다른 접근: [[papers/1387_EWMBench_Evaluating_Scene_Motion_and_Semantic_Quality_in_Emb/review]] — World Models의 일반적인 세계 모델 평가와 EWMBench의 embodied world model 특화 평가는 서로 다른 범위와 초점을 가진 벤치마킹 접근이다.
- 🏛 기반 연구: [[papers/1359_Diffusion_for_World_Modeling_Visual_Details_Matter_in_Atari/review]] — 월드 모델링의 기초적인 개념과 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D-VLA의 생성형 월드 모델링 접근법은 World Models의 기본 개념에서 출발하여 3D 공간 추론을 추가한 확장입니다.
- 🏛 기반 연구: [[papers/1360_Diffusion_Models_Are_Real-Time_Game_Engines/review]] — 게임 환경에서의 world model 구현을 위한 기본 이론적 배경을 제공합니다.
- 🏛 기반 연구: [[papers/1368_DiWA_Diffusion_Policy_Adaptation_with_World_Models/review]] — World Models의 세계 모델 개념은 DiWA의 학습된 world model을 활용한 diffusion 정책 적응에 근본적인 이론적 기반을 제공한다.
