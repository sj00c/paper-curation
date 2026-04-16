---
title: "1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit"
authors:
  - "Hengtao Li"
  - "Pengxiang Ding"
  - "Runze Suo"
  - "Yihao Wang"
  - "Zirui Ge"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "VLA-RFT는 데이터 기반 world model을 시뮬레이터로 활용하여 vision-language-action 모델을 reinforcement learning으로 효율적으로 fine-tuning하는 프레임워크이다. 검증된 reward를 기반으로 GRPO 최적화를 수행하여 400 단계 이하의 fine-tuning으로 strong supervised baseline을 초과하는 성능을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_VLA-RFT Vision-Language-Action Reinforcement Fine-tuning with Verified Rewards in World Simulators.pdf"
---

# VLA-RFT: Vision-Language-Action Reinforcement Fine-tuning with Verified Rewards in World Simulators

> **저자**: Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, Weihua Su | **날짜**: 2025-10-01 | **URL**: [https://arxiv.org/abs/2510.00406](https://arxiv.org/abs/2510.00406)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The Framework of VLA-RFT. A world model functions as a simulator that processes*

VLA-RFT는 데이터 기반 world model을 시뮬레이터로 활용하여 vision-language-action 모델을 reinforcement learning으로 효율적으로 fine-tuning하는 프레임워크이다. 검증된 reward를 기반으로 GRPO 최적화를 수행하여 400 단계 이하의 fine-tuning으로 strong supervised baseline을 초과하는 성능을 달성한다.

## Motivation

- **Known**: VLA 모델은 imitation learning에 의존하여 distribution shift 하에서 error accumulation과 낮은 robustness 문제를 겪는다. Simulation-based RL과 real-world RL은 각각 높은 sample 복잡도와 비용 문제를 가지고 있다.
- **Gap**: 기존 RL 접근법들은 현실적 제약(높은 상호작용 비용, sim-to-real gap, 안전성)을 극복하지 못하고 있다. World model 기반의 효율적이고 실용적인 VLA post-training 패러다임이 부재하다.
- **Why**: VLA의 실제 배포와 확장성을 위해서는 imitation learning의 근본적 한계를 극복하고 generalization과 robustness를 동시에 달성할 수 있는 효율적인 학습 방법이 필수적이다.
- **Approach**: Data-driven world model을 통해 real-world 상호작용 없이 policy rollout을 시뮬레이션하고, goal-achieving reference trajectory와의 비교를 통해 dense, trajectory-level reward를 생성한다. GRPO 프레임워크로 이러한 검증된 reward를 기반으로 VLA를 end-to-end 최적화한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: The Framework of VLA-RFT. A world model functions as a simulator that processes*

- **효율성**: 400 단계 이하의 fine-tuning으로 150K 반복 supervised fine-tuning baseline을 초과하는 성능 달성
- **우수한 성능**: LIBERO 벤치마크에서 base VLA 86.6%에서 91.1%로 성능 향상 (general settings)
- **강화된 Robustness**: 4가지 perturbation 조건(Object Pos, Goal Pos, RoboState, Combined)에서 일관된 성능 유지
- **Compositional Generalization**: supervised baseline 대비 우수한 compositional 일반화 능력 입증
- **실행시간 Robustness**: 예상치 못한 환경 변화에서도 안정적인 task 실행 및 failure recovery 능력

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Training Paradigm of VLA-RFT. In the pre-training stage, both the world model and*

- Stage I: World model과 VLA policy를 offline 데이터셋에서 함께 pretrain하여 안정적인 초기화 제공
- World model: Real interaction data로부터 action 조건부 future visual observation 예측 학습
- Policy rollout: VLA가 생성한 action sequence를 world model에 입력하여 synthetic trajectory 생성
- Verified reward design: Goal-achieving reference trajectory와의 LPIPS 및 MAE 기반 pixel/perception reward 계산
- GRPO optimization: Trajectory-level verified reward를 기반으로 VLA policy를 end-to-end 최적화
- Flow-matching action head: Stable action chunk generation을 위한 dual-system VLA 구조 활용

## Originality

- World model을 단순 dynamics 시뮬레이터가 아닌 verified reward 생성 메커니즘으로 통합하는 혁신적 접근
- Dense, trajectory-level reward 설계로 action-aligned learning signal 제공
- Offline data로부터 학습한 world model 기반 시뮬레이션을 통해 real-world interaction 비용 제거
- GRPO와 world model의 결합으로 VLA post-training을 위한 새로운 패러다임 제시

## Limitation & Further Study

- World model의 예측 오차 누적에 대한 장기적 영향 분석 부재 (long-horizon task에서의 성능 저하 가능성)
- LIBERO 벤치마크 중심의 평가로 다양한 robot morphology와 task 도메인에 대한 generalization 검증 필요
- World model 학습에 필요한 offline 데이터셋의 규모와 다양성에 대한 민감도 분석 부족
- Sim-to-real gap 측면에서 실제 로봇 환경에서의 검증 필요 (시뮬레이션 기반 실험만 수행)
- Reward 설계가 goal trajectory 기반으로 제한되어 있어 exploration과 novelty 추구 가능성 제약

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLA-RFT는 world model 기반 reinforcement fine-tuning을 통해 효율성, 성능, robustness를 동시에 달성하는 실용적이고 창의적인 접근법을 제시한다. 극도로 제한된 fine-tuning 단계로 strong baseline을 초과하고 perturbed 환경에서 일관된 성능을 유지하는 점에서 높은 가치가 있으나, 실제 로봇 환경에서의 검증과 장기 horizon task에 대한 분석이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — VLA 강화학습 fine-tuning에 대한 서로 다른 접근법 - data-driven world model vs direct RL입니다.
- 🔗 후속 연구: [[papers/1411_GR-RL_Going_Dexterous_and_Precise_for_Long-Horizon_Robotic_M/review]] — long-horizon robotic task를 reinforcement fine-tuning으로 해결하는 확장 연구입니다.
- 🏛 기반 연구: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — contrastive reinforced fine-tuning이 VLA-RFT의 기반 방법론을 제공합니다.
- 🔗 후속 연구: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — VLA-RL이 VLA-RFT의 강화 학습 파인튜닝 아이디어를 더 일반적이고 숙련된 로봇 조작으로 확장한다.
- 🏛 기반 연구: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — World model 기반 학습의 이론적 토대를 제공하여 VLA-RFT의 데이터 기반 world model 활용 방법론을 뒷받침한다.
- 🔄 다른 접근: [[papers/1494_NORA-15_A_Vision-Language-Action_Model_Trained_using_World_M/review]] — 두 논문 모두 VLA 모델의 성능 향상을 위해 강화학습 기반 후처리를 활용하지만 구체적 방법론이 다르다.
- 🔗 후속 연구: [[papers/1513_Parallels_Between_VLA_Model_Post-Training_and_Human_Motor_Le/review]] — 인간 운동 학습 관점의 VLA post-training을 reinforcement fine-tuning으로 실제 구현
- 🏛 기반 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — VLA-RFT의 reinforcement fine-tuning 방법론이 RLinf-VLA의 통합 RL 프레임워크 설계의 이론적 기반이다.
- 🔄 다른 접근: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — VLA 모델의 강화학습 기반 fine-tuning에 대한 서로 다른 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — 둘 다 VLA 모델의 강화학습 개선을 다루지만, VLA-RL은 OOD 대응력을, VLA-RFT는 world model 효율성에 집중한다.
- 🔗 후속 연구: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — WHALE의 world model을 VLA fine-tuning의 시뮬레이터로 활용하여 더 효율적인 강화학습 프레임워크를 구축한다.
- 🔗 후속 연구: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — VLA 모델의 강화학습 기반 파인튜닝에 대한 확장된 접근 방식을 제공합니다.
- 🏛 기반 연구: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — VLA-RFT의 vision-language-action reinforcement fine-tuning 방법론이 Embodied-R1의 RFT 기반 훈련 접근법에 기초가 된다.
