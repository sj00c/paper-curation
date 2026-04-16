---
title: "1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un"
authors:
  - "Jiaming Liu"
  - "Hao Chen"
  - "Pengju An"
  - "Zhuoyang Liu"
  - "Renrui Zhang"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "HybridVLA는 diffusion 기반 action 예측의 연속성과 autoregressive VLM의 추론 능력을 단일 LLM 내에서 통합하는 unified vision-language-action 모델이다. Collaborative training recipe와 adaptive action ensemble mechanism을 통해 두 생성 패러다임의 상호 강화를 실현한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2025_HybridVLA Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model.pdf"
---

# HybridVLA: Collaborative Diffusion and Autoregression in a Unified Vision-Language-Action Model

> **저자**: Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, Chengkai Hou, Mengdi Zhao, KC alex Zhou, Pheng-Ann Heng, Shanghang Zhang | **날짜**: 2025-03-13 | **URL**: [https://arxiv.org/abs/2503.10631](https://arxiv.org/abs/2503.10631)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: (a) Unlike recent diffusion-based VLA methods [12, 13, 14] that attach a separate diffusion*

HybridVLA는 diffusion 기반 action 예측의 연속성과 autoregressive VLM의 추론 능력을 단일 LLM 내에서 통합하는 unified vision-language-action 모델이다. Collaborative training recipe와 adaptive action ensemble mechanism을 통해 두 생성 패러다임의 상호 강화를 실현한다.

## Motivation

- **Known**: Autoregressive VLA 방법은 VLM의 common-sense reasoning을 활용하지만 action 연속성을 손상시키고, diffusion 기반 VLA는 연속적 action을 예측하나 VLM의 token-level reasoning을 완전히 활용하지 못한다.
- **Gap**: 기존 diffusion 기반 VLA는 VLM 이후에 독립적인 diffusion head를 추가하여 두 패러다임의 강점을 진정으로 통합하지 못하고 있다.
- **Why**: 로봇 조작은 정밀한 연속 제어와 복잡한 환경에 대한 고-수준 추론을 모두 필요로 하므로, 두 생성 방식의 장점을 통합된 방식으로 결합하는 것이 중요하다.
- **Approach**: 단일 LLM backbone 내에서 diffusion denoising을 next-token prediction 과정에 seamlessly 통합하는 collaborative training recipe를 제안하고, autoregressive action token confidence 기반으로 두 예측을 adaptive하게 fusion하는 collaborative action ensemble mechanism을 설계한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: (a) Unlike recent diffusion-based VLA methods [12, 13, 14] that attach a separate diffusion*

- **통합 아키텍처**: Diffusion과 autoregressive action generation을 단일 LLM 내에서 구현하여 두 패러다임이 상호 강화되도록 설계
- **Collaborative Training Recipe**: Token sequence formulation과 specialized marker tokens를 통해 discrete autoregressive tokens와 continuous diffusion latents를 효과적으로 연결
- **Adaptive Ensemble Mechanism**: Autoregressive confidence 기반 weighting으로 task별 최적의 action 선택
- **성능 개선**: 시뮬레이션 14%, 실제 로봇 환경 19% mean success rate 향상 달성
- **강화된 일반화**: 대규모 robot data pretraining (760K trajectories)으로 unseen objects, backgrounds, spatial positions, lighting conditions에 대한 robust 성능 시연
- **추론 최적화**: HybridVLA-dif (7B) variant로 9.4 Hz inference speed 달성

## How

![Figure 2](figures/fig2.webp)

*Figure 2: HybridVLA Framework. All multimodal inputs are encoded into tokens and subsequently*

- Internet-scale pretrained VLM (예: LLaVA)을 초기화 백본으로 사용
- Token sequence formulation으로 multimodal inputs, diffusion tokens, autoregressive tokens를 marker tokens로 연결
- Open X-Embodiment, DROID, ROBOMIND 등 대규모 cross-embodiment robot datasets에서 pretraining 수행
- Self-collected simulation 및 실제 로봇 데이터로 fine-tuning
- Diffusion path (noise-to-action denoising)와 autoregressive path (token-by-token prediction)를 공유 LLM 내에서 simultaneously 학습
- Collaborative action ensemble: argmax(confidence scores)에 따라 diffusion 또는 autoregressive action 선택 또는 weighted fusion
- 두 가지 model variant 제공: full HybridVLA (ensemble 기반) 및 HybridVLA-dif (diffusion-only inference)

## Originality

- Diffusion과 autoregressive를 독립적 head가 아닌 shared LLM backbone 내에서 통합하는 새로운 설계 패러다임 제시
- Token representation 간 불일치 문제를 체계적인 token sequence formulation과 marker tokens로 해결
- Task의 특성에 따라 두 방식의 상대적 강점을 인식하고 이를 adaptive ensemble로 활용하는 통찰력
- Collaborative training recipe를 통해 두 생성 패러다임이 단순 concatenation이 아닌 진정한 상호 강화를 달성하도록 설계

## Limitation & Further Study

- 모델 규모 (7B LLM)에서의 성능만 보고되었으며, 더 큰 규모의 VLM에 대한 확장성 검증 필요
- Collaborative training의 computational overhead가 상세히 분석되지 않았음
- Adaptive ensemble mechanism의 confidence threshold 선택 기준이 명확하지 않음
- Real-world 실험이 제한된 수의 task와 환경에서만 수행되었으며, 더 다양한 조작 시나리오에 대한 검증 필요
- Diffusion step 수 (t)에 따른 성능 변화 분석이 preliminary level에 머물러 있음
- 후속 연구: 더 큰 모델 규모에서의 확장성 검증, real-time constraint 환경에서의 적용, 다중 로봇 embodiment 간 transfer learning 효율성 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: HybridVLA는 diffusion과 autoregressive 기반 action 생성의 근본적 한계를 unified architecture와 collaborative training을 통해 우아하게 해결하며, 광범위한 실험과 state-of-the-art 성과를 통해 로봇 조작 분야에 실질적인 진전을 제시하는 견고한 논문이다.

## Related Papers

- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 둘 다 unified VLA 모델이지만 diffusion + autoregressive hybrid vs pure open-source 접근이라는 다른 전략을 사용한다.
- 🏛 기반 연구: [[papers/1624_VQ-VLA_Improving_Vision-Language-Action_Models_via_Scaling_V/review]] — VQ-VLA의 다중 생성 패러다임 개념을 diffusion과 autoregressive의 collaborative training으로 구현했다.
- 🔗 후속 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — FAST의 action tokenization을 diffusion과 autoregressive를 결합한 hybrid 방식으로 확장했다.
- 🔄 다른 접근: [[papers/1479_MoLe-VLA_Dynamic_Layer-skipping_Vision_Language_Action_Model/review]] — 둘 다 VLA 모델의 계산 효율성 향상에 중점을 두지만, HybridVLA는 생성 패러다임 통합을, MoLe-VLA는 동적 레이어 스킵에 집중한다.
- 🔗 후속 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — HybridVLA의 diffusion 기반 action 예측이 Diffusion Transformer Policy의 방법론을 VLM과 통합하여 확장한 형태이다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy의 action diffusion과 autoregressive VLM을 단일 모델에서 협력적으로 통합하는 새로운 패러다임을 제시한다.
- 🔗 후속 연구: [[papers/1366_Discrete_Diffusion_VLA_Bringing_Discrete_Diffusion_to_Action/review]] — Discrete Diffusion VLA의 discrete 접근법을 autoregressive와 결합하여 더 유연한 action generation을 구현한다.
- 🔄 다른 접근: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — 둘 다 VLA 모델의 추론 능력 향상에 초점을 맞추지만, Hume은 dual-system 접근법을, HybridVLA는 diffusion과 autoregressive 통합에 집중한다.
- 🔗 후속 연구: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — HybridVLA의 collaborative diffusion과 autoregression이 OpenHelix가 분석한 dual-system 설계를 실제 구현으로 확장한다.
