---
title: "1316_Behavior_Transformers_Cloning_k_modes_with_one_stone"
authors:
  - "Nur Muhammad Mahi Shafiullah"
  - "Zichen Jeff Cui"
  - "Ariuntuya Altanzaya"
  - "Lerrel Pinto"
date: "2022.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Behavior Transformer (BeT)는 transformer 아키텍처에 action discretization과 multi-task action correction을 결합하여 unlabeled demonstration data에서 multi-modal continuous actions를 학습하는 기법이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shafiullah et al._2022_Behavior Transformers Cloning $k$ modes with one stone.pdf"
---

# Behavior Transformers: Cloning $k$ modes with one stone

> **저자**: Nur Muhammad Mahi Shafiullah, Zichen Jeff Cui, Ariuntuya Altanzaya, Lerrel Pinto | **날짜**: 2022-06-22 | **URL**: [https://arxiv.org/abs/2206.11251](https://arxiv.org/abs/2206.11251)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3: Architecture of Behavior Transformer. (A) The continuous action binning using k-means algorithm*

Behavior Transformer (BeT)는 transformer 아키텍처에 action discretization과 multi-task action correction을 결합하여 unlabeled demonstration data에서 multi-modal continuous actions를 학습하는 기법이다.

## Motivation

- **Known**: Behavior cloning과 offline RL은 reward 라벨 없이 큰 데이터셋에서 행동을 학습할 수 있지만, 기존 방법들은 unimodal expert 데이터를 가정하므로 multi-modal 행동 분포를 다루지 못한다.
- **Gap**: 자연스러운 human demonstration은 wide variance와 multiple modes를 가지지만, 현재 방법들은 이를 효과적으로 모델링하지 못하며 주로 goal-conditioned policies로 제한된다.
- **Why**: Vision과 NLP는 대규모 사전학습 데이터로부터 학습되지만 behavior learning은 그렇지 못하므로, multi-modal behavior data를 효과적으로 활용할 수 있는 방법이 필요하다.
- **Approach**: Continuous actions를 k-means로 discrete bins로 clustering한 후, transformer가 각 bin의 확률과 residual offset을 동시에 예측하는 방식으로 multi-modal continuous action distribution을 모델링한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Unconditional rollouts from BeT models trained from multi-modal demonstartions on the CARLA,*

- **Multi-modal 성능**: 다양한 robotic manipulation과 self-driving 데이터셋에서 기존 behavior modeling 방법들을 크게 능가한다.
- **Mode coverage**: 하나의 모드로 붕괴되지 않고 pre-collected dataset의 주요 modes를 포착한다.
- **Architecture simplicity**: 복잡한 generative model이나 complicated training scheme 없이 standard transformer를 활용한다.

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Architecture of Behavior Transformer. (A) The continuous action binning using k-means algorithm*

- k-means clustering을 통해 continuous actions를 discrete action bins ⌊a⌋와 continuous residual ⟨a⟩로 분해
- MinGPT transformer backbone을 사용하여 observation sequence로부터 action bin probabilities를 예측
- Multi-task learning으로 action bin 분류와 per-bin residual offset 예측을 동시에 수행
- Test time에 sampled bin에 해당하는 offset을 더하여 continuous action 재구성
- History-aware modeling으로 P(at | ot, ot-1, ..., ot-h+1) 형태로 non-Markovian 정책 학습

## Originality

- Transformer의 discrete token 생성 능력과 action discretization을 결합한 새로운 접근
- Object detection의 offset prediction 개념을 behavior cloning에 적용하는 창의적인 아이디어
- MDN처럼 명시적으로 mode centers를 예측하지 않으면서도 multi-modal 분포를 모델링하는 방식
- K-means 기반 action factorization으로 continuous와 discrete 예측을 분리하는 설계

## Limitation & Further Study

- K-means binning의 선택 (k값)이 성능에 미치는 영향에 대한 자세한 분석 부족
- 고차원 action space에서 k개 bin이 exponential하게 증가할 수 있는 scalability 문제
- Online RL과의 통합이나 reward signal과의 결합 방안에 대한 탐구 미흡
- Residual offset 학습의 정확성이 action reconstruction quality에 미치는 영향 분석 필요
- 후속 연구: multi-task learning과의 더 깊은 통합, 적응적 binning 전략 개발, 다른 discretization 방법 비교

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: BeT는 transformer의 강점과 action discretization을 창의적으로 결합하여 multi-modal behavior learning의 중요한 문제를 우아하게 해결한다. 광범위한 실험과 ablation study로 방법의 효과성을 충분히 입증했으며, behavior cloning 분야에 의미 있는 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Multi-modal 행동 학습에서 Transformer 기반 action discretization과 확산 모델 기반 연속 행동이 다른 접근법입니다.
- 🔗 후속 연구: [[papers/1433_In-Context_Imitation_Learning_via_Next-Token_Prediction/review]] — 다음 토큰 예측을 통한 맥락 내 모방 학습과 Behavior Transformer의 multi-modal 행동 학습을 결합할 수 있습니다.
- 🏛 기반 연구: [[papers/1330_CLAM_Continuous_Latent_Action_Models_for_Robot_Learning_from/review]] — 연속 잠재 행동 모델 CLAM이 BeT의 action discretization에 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1598_Unified_Video_Action_Model/review]] — Unified Video Action Model의 action modeling 개념을 transformer 기반 multi-task action correction과 action discretization으로 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1514_Perceiver-Actor_A_Multi-Task_Transformer_for_Robotic_Manipul/review]] — 둘 다 transformer 아키텍처를 로봇 학습에 활용하지만 BeT는 action discretization에, Perceiver-Actor는 multi-task learning에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1433_In-Context_Imitation_Learning_via_Next-Token_Prediction/review]] — 멀티모달 행동 생성을 위한 Transformer 기반 접근법으로 in-context learning과 behavior cloning의 차이점을 비교할 수 있다.
- 🏛 기반 연구: [[papers/1537_RoboCat_A_Self-Improving_Generalist_Agent_for_Robotic_Manipu/review]] — RoboCat의 self-improving agent를 위한 기본적인 behavior cloning과 multi-modal learning 방법론을 제공한다.
- 🏛 기반 연구: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — Behavior Transformers의 multi-modal transformer 아키텍처가 SARA-RT의 robotics transformer 설계의 기초가 된다.
- 🔄 다른 접근: [[papers/1591_Towards_Diverse_Behaviors_A_Benchmark_for_Imitation_Learning/review]] — Behavior Transformers가 k개 모드를 클로닝하는 방법을 제안한 반면, D3IL은 인간 행동 다양성을 평가하는 벤치마크를 제공한다.
- 🔗 후속 연구: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — Behavior Transformers의 trajectory autoregressive modeling을 목표 상태부터 역순으로 생성하는 혁신적 접근법으로 발전시켜 누적 오차를 완화한 연구입니다.
- 🔄 다른 접근: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — 로봇 정책 학습에서 diffusion과 transformer 기반의 서로 다른 행동 모델링 접근법을 비교합니다.
