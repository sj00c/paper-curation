---
title: "1615_Physics-Based_Motion_Imitation_with_Adversarial_Differential"
authors:
  - "Ziyu Zhang"
  - "Sergey Bashkirov"
  - "Dun Yang"
  - "Yi Shi"
  - "Michael Taylor"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Physics-based 캐릭터 애니메이션을 위해 Adversarial Differential Discriminator (ADD)를 통해 수동 보상 함수 설계 없이 다중 목표 최적화를 자동으로 수행하는 방법을 제시한다. 단일 positive sample(영점 벡터)만으로도 효과적으로 여러 목표를 동적으로 균형잡아 고난도 동작을 모방할 수 있다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Physics-Based Motion Imitation with Adversarial Differential Discriminators.pdf"
---

# Physics-Based Motion Imitation with Adversarial Differential Discriminators

> **저자**: Ziyu Zhang, Sergey Bashkirov, Dun Yang, Yi Shi, Michael Taylor, Xue Bin Peng | **날짜**: 2025-05-08 | **URL**: [https://arxiv.org/abs/2505.04961](https://arxiv.org/abs/2505.04961)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. We propose an adversarial multi-objective optimization technique that enables physically simulated characters to*

Physics-based 캐릭터 애니메이션을 위해 Adversarial Differential Discriminator (ADD)를 통해 수동 보상 함수 설계 없이 다중 목표 최적화를 자동으로 수행하는 방법을 제시한다. 단일 positive sample(영점 벡터)만으로도 효과적으로 여러 목표를 동적으로 균형잡아 고난도 동작을 모방할 수 있다.

## Motivation

- **Known**: Physics-based 캐릭터 애니메이션은 RL 기반 방법으로 발전했으나, 수작업 보상 함수 설계가 필수적이었다. 기존 adversarial imitation learning은 분포 매칭을 통해 자연스러운 동작을 생성하지만 정확한 reference motion 복제에는 한계가 있다.
- **Gap**: 다중 목표 최적화에서 가중치 선택이 수동이고 시간소비적이며, 기존 adversarial imitation learning은 정밀한 동작 복제보다 스타일 학습에 초점이 맞춰져 있다.
- **Why**: Physics-based 애니메이션 응용에서 정확한 reference 동작 복제는 필수적이며, 수동 보상 함수 설계 제거는 다양한 기술에 대한 일반화 가능성을 크게 높일 수 있다.
- **Approach**: Discriminator가 objective 값의 차이를 나타내는 differential vector를 입력받아 이상적 해(영점 벡터)와의 분류를 학습하게 함으로써, 학습 과정에서 여러 목표를 자동으로 동적 균형잡는 GAN 기반 프레임워크를 제안한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2. Snapshots of the simulated humanoid characters trained using ADD performing various skills. ADD enables characte*

- **자동 목표 균형**: 수동 가중치 선택 없이 목표들을 동적으로 균형잡으며, 선형 가중합보다 비선형 관계 포착 가능
- **높은 품질의 동작 모방**: Humanoid와 로봇이 곡예 및 민첩한 기술을 포함한 다양한 동작을 정확히 복제하여 최신 방법과 동등한 수준 달성
- **단순한 positive sample**: 영점 벡터 하나만으로도 효과적인 최적화 가능, 실제 demonstration 필요 없음
- **일반성**: Motion tracking 외 다양한 다중 목표 RL 문제에 광범위하게 적용 가능

## How

![Figure 4](figures/fig4.webp)

*Figure 4 compares the learning curves of humanoid characters*

- Differential vector는 각 목표에서 모델 성능과 이상적 성능 간의 차이를 표현
- Discriminator는 differential vector가 이상적 해(영점)인지 아닌지 분류하도록 학습
- Agent는 discriminator의 예측 오류를 최대화하도록 정책을 최적화
- 학습 과정에서 모델 성능 향상에 따라 discriminator는 더 어려운 목표에 동적으로 초점 전환
- GAN 기반 adversarial mini-max 게임 프레임워크로 joint optimization 수행

## Originality

- 기존 weighted sum 방식 대신 adversarial discriminator로 자동 목표 가중치 결정하는 신규 접근
- 단일 positive sample(영점 벡터)로도 discriminator 효과성을 보인 점
- 비선형 목표 관계를 포착할 수 있는 differential vector 개념 도입
- Motion tracking에서 수동 보상 함수 제거를 통한 일반화 가능한 프레임워크 제시

## Limitation & Further Study

- Discriminator 학습의 수렴 안정성과 hyperparameter 선택에 대한 분석 부족
- 복잡한 다중 목표(3개 이상) 환경에서의 scalability 검증 미흡
- ADD와 기존 hand-crafted reward의 계산 비용 및 학습 속도 직접 비교 부재
- 후속 연구: 더 복잡한 목표 공간에서의 성능 검증, transfer learning 적용 가능성 탐색, 실제 로봇 제어로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 다중 목표 최적화의 자동화를 위해 창의적인 adversarial discriminator 설계를 제시하며, physics-based 캐릭터 애니메이션에서 수동 보상 함수 설계 제거를 통해 일반화 가능성을 크게 향상시킨다. 핵심 아이디어의 단순성과 광범위한 적용 가능성이 강점이다.

## Related Papers

- 🏛 기반 연구: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — DeepMimic의 physics-based character control과 adversarial training 방법론이 ADD의 적대적 차별자 설계의 이론적 기초를 제공함
- 🔄 다른 접근: [[papers/1800_AMOR_Adaptive_Character_Control_through_Multi-Objective_Rein/review]] — AMOR은 multi-objective reinforcement learning을, ADD는 adversarial differential discriminator를 사용하여 다중 목표 최적화를 다르게 접근함
- 🔗 후속 연구: [[papers/2092_MaskedMimic_Unified_Physics-Based_Character_Control_Through/review]] — MaskedMimic의 마스킹 기반 physics 제어 기법이 ADD의 자동 목표 균형 조정 능력을 더욱 정교하게 확장할 수 있음
- 🔗 후속 연구: [[papers/1623_Preference-Conditioned_Multi-Objective_RL_for_Integrated_Com/review]] — ADD의 자동 목표 균형 조정을 preference-conditioned MORL로 확장한 연구
- 🏛 기반 연구: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — 물리 기반 모션 모방에서 adversarial differential과 self-supervised adaptation이라는 관련된 학습 패러다임을 사용한다.
- 🔄 다른 접근: [[papers/1691_Stabilizing_Humanoid_Robot_Trajectory_Generation_via_Physics/review]] — 두 논문 모두 물리 기반 모방 학습을 다루지만, 물리 정보 기반 안정화와 adversarial differential privacy라는 다른 접근을 사용한다.
- 🏛 기반 연구: [[papers/1623_Preference-Conditioned_Multi-Objective_RL_for_Integrated_Com/review]] — ADD의 multi-objective optimization을 preference-based framework로 발전시킨 연구
- 🔄 다른 접근: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — 물리 기반 모션 모방을 위한 다른 적대적 학습 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/2126_Opt2Skill_Imitating_Dynamically-feasible_Whole-Body_Trajecto/review]] — Physics-based motion imitation with adversarial differential이 Opt2Skill의 DDP 기반 궤적 생성과 다른 adversarial 접근법으로 물리적으로 실현 가능한 동작을 생성합니다.
