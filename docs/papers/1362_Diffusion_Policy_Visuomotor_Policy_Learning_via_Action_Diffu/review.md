---
title: "1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu"
authors:
  - "Cheng Chi"
  - "Zhenjia Xu"
  - "Siyuan Feng"
  - "Eric Cousineau"
  - "Yilun Du"
date: "2023.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Robot 조작 작업을 위한 visuomotor policy를 conditional denoising diffusion process로 표현하는 Diffusion Policy를 제안하며, 4개 벤치마크의 15개 작업에서 평균 46.9% 성능 향상을 달성했다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chi et al._2023_Diffusion Policy Visuomotor Policy Learning via Action Diffusion.pdf"
---

# Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

> **저자**: Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, Shuran Song | **날짜**: 2023-03-07 | **URL**: [https://arxiv.org/abs/2303.04137](https://arxiv.org/abs/2303.04137)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Policy Representations. a) Explicit policy with different types of action representations. b) Implicit policy *

Robot 조작 작업을 위한 visuomotor policy를 conditional denoising diffusion process로 표현하는 Diffusion Policy를 제안하며, 4개 벤치마크의 15개 작업에서 평균 46.9% 성능 향상을 달성했다.

## Motivation

- **Known**: 기존 robot policy learning은 multimodal action distribution, high-dimensional action space, training instability 문제를 안고 있으며, 이를 해결하기 위해 mixture of Gaussians나 categorical representation 같은 다양한 action representation이 제안되었다.
- **Gap**: Diffusion model의 강력한 생성 능력이 robot policy learning에 충분히 활용되지 못했으며, visuomotor policy로 적용할 때 필요한 receding horizon control, visual conditioning, time-series 구조 등의 기술적 해결책이 부재했다.
- **Why**: Robot manipulation은 multimodal behavior, 긴 시간적 상관성, 높은 정밀도를 동시에 요구하므로, 이를 안정적으로 모델링할 수 있는 정교한 policy representation이 중요하다.
- **Approach**: Diffusion Policy는 robot action을 DDPM의 denoising process로 모델링하여 noise prediction network가 action-score gradient를 학습하고, stochastic Langevin dynamics를 통해 iterative refinement를 수행한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Diffusion Policy Overview a) General formulation. At time step t, the policy takes the latest To steps of obse*

- **Multimodal action distribution 표현**: Score function의 gradient 학습을 통해 arbitrary normalizable distribution을 정확하게 모델링할 수 있다.
- **High-dimensional action space 확장성**: 단일 action이 아닌 action sequence 예측이 가능하여 temporal consistency를 개선한다.
- **안정적인 학습**: Negative sampling 없이 gradient field를 직접 학습하여 energy-based model의 학습 불안정성을 해결한다.
- **뛰어난 벤치마크 성능**: 15개 작업에서 일관되게 기존 state-of-the-art 방법을 46.9% 초과 달성한다.
- **기술적 기여**: Receding horizon control, visual conditioning (FiLM), transformer-based architecture를 통해 실제 robot 적용을 가능하게 한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Diffusion Policy Overview a) General formulation. At time step t, the policy takes the latest To steps of obse*

- Denoising Diffusion Probabilistic Model (DDPM)을 robot action space에 적용하여 xK ~ N(0,I)에서 시작하는 K iteration의 denoising process로 action sequence를 생성
- Noise schedule (α, γ, σ)을 iteration step k의 함수로 정의하여 gradient descent의 learning rate scheduling으로 해석
- Visual observation Ot를 conditioning variable로 도입하고 FiLM (Feature-wise Linear Modulation)을 사용하여 CNN 기반 architecture에 통합
- Transformer 기반 architecture 제안으로 over-smoothing을 감소시키고 high-frequency action change와 velocity control 성능 향상
- Receding horizon control을 통해 Ta step의 action sequence를 예측하면서 매 time step마다 replanning하는 closed-loop 구조 구현
- Training은 random noise ε_k를 data에 추가한 후 noise prediction network εθ가 이를 예측하도록 MSE loss로 최적화
- 15개 작업의 behavior cloning 평가: simulation과 real-world, 2DoF~6DoF, single/multi-task, rigid/fluid objects 포함

## Originality

- Diffusion model을 robot visuomotor policy에 처음으로 적용한 것으로, generative modeling의 강점을 policy learning에 창의적으로 전이
- Score function gradient learning 관점에서 diffusion process를 gradient descent로 재해석하여 theoretical foundation 제공
- Receding horizon control과 diffusion의 결합으로 long-horizon planning과 responsiveness의 균형을 새롭게 달성
- Vision-conditioned diffusion formulation으로 visual feature를 joint distribution이 아닌 conditioning으로 처리하여 계산 효율성 혁신
- Time-series diffusion transformer라는 새로운 network architecture로 CNN의 over-smoothing 문제를 transformer의 causal attention으로 해결

## Limitation & Further Study

- K iteration의 denoising step이 필요하므로 inference 시간이 single-step policy에 비해 증가하며, real-time 적용 시 latency 고려 필요
- Diffusion model의 학습이 다른 방법보다 더 많은 computational resource를 요구할 가능성
- Behavior cloning으로만 평가되었으므로 reinforcement learning이나 interactive learning paradigm에서의 성능 미검증
- Noise schedule hyperparameter 선택이 성능에 미치는 영향에 대한 심화 분석 부족
- 다양한 robot morphology와 task domain (예: assembly, contact-rich manipulation)에서의 일반화 성능 검증 필요
- 후속 연구로 online adaptation, meta-learning, multi-task transfer learning 연구 가능

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Diffusion model의 강력한 생성 능력을 robot policy learning에 창의적으로 도입하여 multimodality, scalability, training stability 문제를 동시에 해결한 획기적 연구로, 광범위한 실험과 기술적 기여를 통해 robot learning 분야에 새로운 패러다임을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1289_3D_FlowMatch_Actor_Unified_3D_Policy_for_Single-_and_Dual-Ar/review]] — diffusion policy를 flow matching으로 대체하여 동일한 visuomotor 학습을 훨씬 빠르게 수행하는 개선된 접근법
- 🏛 기반 연구: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 3D diffusion policy가 일반적인 diffusion policy를 3D 공간으로 확장한 기반 연구
- 🏛 기반 연구: [[papers/1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey/review]] — 로봇 조작을 위한 diffusion 모델들에 대한 포괄적인 조사와 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion Transformer 정책으로서 diffusion 기반 정책 학습을 확장합니다.
- 🔄 다른 접근: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — 로봇 정책 학습에서 diffusion과 transformer 기반의 서로 다른 행동 모델링 접근법을 비교합니다.
- 🏛 기반 연구: [[papers/1514_Perceiver-Actor_A_Multi-Task_Transformer_for_Robotic_Manipul/review]] — 멀티태스크 transformer 구조가 diffusion policy의 조건부 생성을 위한 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1594_Transferring_Foundation_Models_for_Generalizable_Robotic_Man/review]] — Diffusion Policy를 foundation model로 확장하여 일반화 가능한 로봇 조작으로 발전시킵니다.
- 🏛 기반 연구: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — 연속적 행동 생성을 위한 diffusion 기반 정책 학습의 기초 이론을 제공한다.
- 🏛 기반 연구: [[papers/1395_FlowPolicy_Enabling_Fast_and_Robust_3D_Flow-based_Policy_via/review]] — Diffusion Policy의 기본 아키텍처를 Consistency Flow Matching으로 가속화한 개선 버전이다.
- 🔗 후속 연구: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — Diffusion Policy의 action diffusion 개념을 video generation 프레임워크로 확장하여 정책 학습과 평가를 통합한다.
- 🏛 기반 연구: [[papers/1423_Hierarchical_Diffusion_Policy_manipulation_trajectory_genera/review]] — Diffusion Policy는 계층적 확산 정책이 기반으로 하는 로봇 조작에서의 diffusion model 적용에 대한 기초 연구입니다.
- 🏛 기반 연구: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — Diffusion Policy의 action diffusion과 autoregressive VLM을 단일 모델에서 협력적으로 통합하는 새로운 패러다임을 제시한다.
- 🏛 기반 연구: [[papers/1465_ManiFlow_A_General_Robot_Manipulation_Policy_via_Consistency/review]] — ManiFlow의 flow matching 기반 정책 학습이 기반으로 하는 diffusion policy 방법론
- 🏛 기반 연구: [[papers/1447_Latent_Action_Diffusion_for_Cross-Embodiment_Manipulation/review]] — diffusion policy의 기본 아이디어가 latent action space에서의 cross-embodiment 정책 학습에 적용되었다.
- 🏛 기반 연구: [[papers/1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with/review]] — diffusion policy의 기본 이론과 visuomotor policy learning 방법론을 제공하여 NavDP의 trajectory generation 메커니즘 설계에 핵심적인 기반을 제공한다.
- 🏛 기반 연구: [[papers/1490_NavigateDiff_Visual_Predictors_are_Zero-Shot_Navigation_Assi/review]] — NavigateDiff가 사용하는 action diffusion의 기초가 되는 visuomotor policy learning 방법론을 제시한다.
- 🏛 기반 연구: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — Diffusion Policy의 visuomotor learning 방법론이 RDT-1B의 bimanual diffusion foundation model의 이론적 기반이다.
- 🏛 기반 연구: [[papers/1524_Reactive_Diffusion_Policy_Slow-Fast_Visual-Tactile_Policy_Le/review]] — diffusion policy의 기본 이론과 visuomotor learning 방법론을 제공하여 RDP의 slow-fast hierarchical diffusion policy 설계에 필수적인 기술적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — Diffusion Policy의 핵심 개념을 OneDP가 단일 단계로 압축하여 효율성을 극대화한다.
- 🔄 다른 접근: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — RVT-2와 Diffusion Policy는 모두 정밀한 로봇 조작을 위한 상이한 아키텍처 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1580_Streaming_Flow_Policy_Simplifying_diffusionflow-matching_pol/review]] — Diffusion Policy의 action diffusion 기본 개념이 Streaming Flow Policy의 flow trajectory 기반 단순화된 접근법의 이론적 기초가 된다.
- 🔄 다른 접근: [[papers/1605_VIMA_General_Robot_Manipulation_with_Multimodal_Prompts/review]] — Diffusion Policy가 VIMA와 다른 확산 모델 기반 접근법으로 로봇 조작 정책 학습 문제를 해결한다.
- 🏛 기반 연구: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — Action diffusion의 기본 개념을 제공하여 VITA의 flow matching policy 설계에 핵심적인 이론적 토대를 마련한다.
- 🏛 기반 연구: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — Diffusion Policy의 비주오모터 정책 학습은 Diffusion-VLA의 diffusion 기반 로봇 foundation model에 핵심적인 기술적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1337_Compose_Your_Policies_Improving_Diffusion-based_or_Flow-base/review]] — diffusion 기반 정책 학습의 기초적 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1289_3D_FlowMatch_Actor_Unified_3D_Policy_for_Single-_and_Dual-Ar/review]] — 동일한 로봇 조작 문제를 diffusion 대신 flow matching으로 해결하여 훨씬 빠른 학습과 추론 속도를 제공
- 🔄 다른 접근: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — Multi-modal 행동 학습에서 Transformer 기반 action discretization과 확산 모델 기반 연속 행동이 다른 접근법입니다.
- 🔄 다른 접근: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — 둘 다 궤적 기반 로봇 정책이지만 Diffusion Policy는 순방향 확산 모델을, CoA는 역방향 자동회귀 모델링을 사용합니다.
- 🏛 기반 연구: [[papers/1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi/review]] — Action Diffusion을 통한 visuomotor 정책 학습의 원리적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey/review]] — Diffusion Policy는 로봇 조작에서 diffusion model 적용의 핵심 원리와 방법론을 제시하여 survey의 중요한 기반 연구입니다.
- 🔗 후속 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — 기존 Diffusion Policy의 작은 action head를 큰 transformer로 대체하여 scaling 능력을 향상시킵니다.
- 🏛 기반 연구: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — Diffusion Policy의 기본 visuomotor learning 프레임워크가 MoDE에서 mixture-of-experts로 확장되는 diffusion policy의 기초를 제공한다.
- 🔗 후속 연구: [[papers/1368_DiWA_Diffusion_Policy_Adaptation_with_World_Models/review]] — DiWA의 diffusion 정책 적응과 Diffusion Policy의 비주오모터 학습은 diffusion 기반 로봇 정책의 발전된 활용이다.
- 🏛 기반 연구: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — Diffusion Policy의 action diffusion 개념을 3D 시각 표현과 결합하여 point cloud 기반으로 확장한 방법론입니다.
