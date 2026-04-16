---
title: "1801_AMP_Adversarial_Motion_Priors_for_Stylized_Physics-Based_Cha"
authors:
  - "Xue Bin Peng"
  - "Ze Ma"
  - "Pieter Abbeel"
  - "Sergey Levine"
  - "Angjoo Kanazawa"
date: "2021.04"
doi: ""
arxiv: ""
score: 4.0
essence: "물리 기반 캐릭터 애니메이션에서 adversarial motion prior를 학습하여 비구조화된 모션 클립 데이터셋으로부터 자동으로 스타일을 추출하고, 간단한 보상 함수로 정의된 고수준 태스크 목표를 달성하면서도 자연스러운 움직임을 생성하는 방법을 제안한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Character_Motion_Policy_Transfer"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Peng et al._2021_AMP Adversarial Motion Priors for Stylized Physics-Based Character Control.pdf"
---

# AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control

> **저자**: Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, Angjoo Kanazawa | **날짜**: 2021-04-05 | **URL**: [https://arxiv.org/abs/2104.02180](https://arxiv.org/abs/2104.02180)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. Schematic overview of the system. Given a motion dataset defining a*

물리 기반 캐릭터 애니메이션에서 adversarial motion prior를 학습하여 비구조화된 모션 클립 데이터셋으로부터 자동으로 스타일을 추출하고, 간단한 보상 함수로 정의된 고수준 태스크 목표를 달성하면서도 자연스러운 움직임을 생성하는 방법을 제안한다.

## Motivation

- **Known**: 데이터 기반 모션 추적 방법은 실제 배우의 모션 클립으로부터 고품질 애니메이션을 생성할 수 있으나, 대규모 비구조화 데이터셋에 적용할 때 적절한 모션 클립 선택과 시퀀싱을 위한 모션 플래너가 필요하며 이는 수작업 설계와 annotation을 요구한다.
- **Gap**: 기존 추적 기반 방법들은 클립 선택 메커니즘과 명시적 목표 함수 설계에 의존하므로, 비구조화된 대규모 모션 데이터셋을 자동으로 활용하면서 다양한 스타일을 학습하고 조합하는 일반화된 방법이 부재하다.
- **Why**: 자동화된 스타일 학습은 모션 데이터의 활용을 극대화하고 애니메이터의 수작업을 줄이며, 비인간 생물이나 가상 캐릭터에 적용 시 모션 데이터가 부족한 상황에서 현실적 움직임을 생성할 수 있어 게임, VR, 로봇 제어 등 다양한 분야에 가치가 있다.
- **Approach**: Adversarial discriminator를 통해 데이터셋의 모션과 학습된 정책의 모션을 구분하도록 훈련하여 motion prior를 학습하고, 이를 goal-conditioned reinforcement learning 프레임워크에 통합하여 스타일 보상과 태스크 보상을 결합한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. Performance of Target Heading policies trained with different*

- **자동 모션 선택 및 보간**: Adversarial motion prior가 명시적 클립 선택이나 sequencing 메커니즘 없이 동적으로 적절한 모션을 선택하고 일반화할 수 있음을 입증
- **스킬 조합의 자동 출현**: 모션 플래너나 task-specific annotation 없이 이질적인 동작들(예: 달리기, 점프, 구르기)이 자동으로 조합되어 복잡한 태스크 수행 가능
- **기존 추적 기반 방법 대비 성능**: 최첨단 추적 기반 기법과 비슷한 수준의 고품질 모션 생성
- **확장성**: 비구조화된 대규모 모션 데이터셋을 효과적으로 수용 가능한 첫 번째 adversarial learning 기반 전신 모션 생성 시스템

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Schematic overview of the system. Given a motion dataset defining a*

- Discriminator를 adversary로 하여 데이터셋 모션과 정책 생성 모션의 분포 차이를 학습
- Motion prior의 판별 확률을 style reward로 변환하여 RL 학습 신호로 활용
- Goal-conditioned RL에서 task reward와 style reward를 결합
- 물리 시뮬레이션 기반 캐릭터 컨트롤러를 정책으로 학습
- 학습된 정책이 자동으로 다양한 모션 클립에서 관련 행동을 선택하고 목표 태스크 수행
- 추가적인 motion planner나 clip annotation 없이 end-to-end 학습

## Originality

- Adversarial imitation learning을 물리 기반 전신 캐릭터 애니메이션에 처음으로 체계적으로 적용하고 실제 복잡한 동작 학습에 성공
- Motion prior를 일반적인 스타일 유사성 측정 지표로 사용하여 명시적 모션 선택이 불필요한 자동화된 접근법 제시
- 비구조화 모션 클립 데이터셋으로부터 자동 스킬 조합이 가능함을 시연
- 기존 adversarial imitation learning 기법의 설계 결정(예: network architecture, reward formulation 등)을 개선하여 고품질 전신 모션 생성 달성

## Limitation & Further Study

- Adversarial discriminator 학습의 안정성: 적대적 학습의 불안정성이 모션 생성 품질에 영향을 미칠 가능성
- 모션 데이터셋의 품질 의존성: 비구조화된 클립 품질이 최종 결과에 직접 영향
- 복잡한 멀티-모달 행동 조합: 근본적으로 서로 다른 스타일의 모션 혼합 시 부자연스러움 가능성
- 후속 연구: 더 안정적인 adversarial 학습 알고리즘, 다중 스타일의 조건부 제어, 정적 안정성과 동적 응답성의 트레이드-오프 개선, 실제 로봇 시스템으로의 전이 학습

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 adversarial motion prior를 통해 비구조화 모션 데이터의 자동 활용을 실현한 물리 기반 캐릭터 애니메이션 분야의 중요한 기여로, 모션 선택 메커니즘 설계의 부담을 제거하면서도 최첨단 성능을 달성하며 게임, 영상, 로봇 등 다양한 응용 분야에 실질적 가치를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — 둘 다 motion capture 데이터를 활용하지만 adversarial prior와 example-guided learning이라는 서로 다른 학습 패러다임을 제시한다
- 🔗 후속 연구: [[papers/2073_Learning_to_Walk_in_Costume_Adversarial_Motion_Priors_for_Ae/review]] — 의상 착용 캐릭터를 위한 adversarial motion prior 확장이 AMP의 stylized character control 응용 범위를 넓힌다
- 🏛 기반 연구: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — StyleLoco의 generative adversarial distillation 기법이 AMP의 자연스러운 움직임 생성에 필요한 핵심 기술적 기반을 제공한다
- 🔗 후속 연구: [[papers/1758_Whole-body_Humanoid_Robot_Locomotion_with_Human_Reference/review]] — 인간 보행 데이터 모방 학습이 AMP의 adversarial motion prior를 실제 humanoid 로봇에 적용하는 구체적 사례입니다.
- 🏛 기반 연구: [[papers/1800_AMOR_Adaptive_Character_Control_through_Multi-Objective_Rein/review]] — AMP의 adversarial prior 학습에서 AMOR의 multi-objective 보상 조정이 스타일과 태스크 목표의 균형을 맞춥니다.
- 🔗 후속 연구: [[papers/1792_Adversarial_Locomotion_and_Motion_Imitation_for_Humanoid_Pol/review]] — AMP의 adversarial motion prior 학습이 ALMI의 대적적 휴머노이드 정책 학습에 방법론적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1809_ASE_Large-Scale_Reusable_Adversarial_Skill_Embeddings_for_Ph/review]] — 둘 다 adversarial skill learning을 다루지만 AMP는 motion prior에, ASE는 large-scale reusable skill embedding에 중점을 둔다.
- 🧪 응용 사례: [[papers/2027_InterPrior_Scaling_Generative_Control_for_Physics-Based_Huma/review]] — InterPrior의 physics-based humanoid control scaling이 AMP의 adversarial motion prior를 더 복잡한 상호작용 시나리오로 확장하는 데 적용될 수 있다.
- 🏛 기반 연구: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — 스타일화된 물리 기반 캐릭터 제어를 위한 adversarial motion prior의 기초 개념을 제공한다.
- 🏛 기반 연구: [[papers/1635_Reduced-Order_Model-Guided_Reinforcement_Learning_for_Demons/review]] — ROM-GRL의 adversarial discriminator가 AMP의 adversarial motion prior 방법론을 reduced-order model에 적용한 것이다
- 🏛 기반 연구: [[papers/1758_Whole-body_Humanoid_Robot_Locomotion_with_Human_Reference/review]] — AMP의 adversarial motion prior 개념이 인간 보행 데이터를 활용한 자연스러운 움직임 생성에 핵심적입니다.
- 🧪 응용 사례: [[papers/1800_AMOR_Adaptive_Character_Control_through_Multi-Objective_Rein/review]] — AMOR의 MORL 프레임워크가 AMP의 adversarial motion prior 학습에서 보상 균형 문제를 해결합니다.
- 🏛 기반 연구: [[papers/1854_Coordinated_Humanoid_Robot_Locomotion_with_Symmetry_Equivari/review]] — 적대적 모션 사전이 대칭성 기반 정책의 이론적 기초를 제공합니다.
- 🏛 기반 연구: [[papers/1792_Adversarial_Locomotion_and_Motion_Imitation_for_Humanoid_Pol/review]] — AMP의 adversarial motion prior 학습 방법론이 ALMI의 대적적 학습 프레임워크의 이론적 기반이 된다.
- 🔄 다른 접근: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — motion capture 데이터 활용에서 example-guided learning과 adversarial motion prior라는 서로 다른 학습 패러다임을 제시한다
- ⚖️ 반론/비판: [[papers/1928_Feature-Based_vs_GAN-Based_Learning_from_Demonstrations_When/review]] — GAN 기반 접근법과 적대적 모션 프라이어의 차이점을 명확히 하여 방법론 선택 기준을 제시한다.
- 🏛 기반 연구: [[papers/1971_Heracles_Bridging_Precise_Tracking_and_Generative_Synthesis/review]] — AMP의 adversarial motion prior 기법이 Heracles의 자연스러운 복구 동작 생성을 위한 기초 이론을 제공한다.
- 🏛 기반 연구: [[papers/1994_Humanoid_Goalkeeper_Learning_from_Position_Conditioned_Task-/review]] — AMP의 적대적 모션 프라이어가 골키퍼의 자동화되고 인간다운 전신 동작 생성의 핵심 토대가 된다.
- 🏛 기반 연구: [[papers/2072_Learning_to_Walk_and_Fly_with_Adversarial_Motion_Priors/review]] — 스타일화된 물리 기반 캐릭터 제어를 위한 적대적 동작 선험의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2073_Learning_to_Walk_in_Costume_Adversarial_Motion_Priors_for_Ae/review]] — Adversarial Motion Priors의 원리를 제공하며, 제약이 있는 엔터테인먼트 로봇의 자연스러운 보행 학습에 직접 활용된다.
- 🏛 기반 연구: [[papers/2074_Learning_Vision-Driven_Reactive_Soccer_Skills_for_Humanoid_R/review]] — 적대적 동작 선험을 시각 기반 동적 제어 환경으로 확장하는 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/2109_Natural_Humanoid_Robot_Locomotion_with_Generative_Motion_Pri/review]] — AMP의 adversarial motion prior를 frozen generative model 기반의 더 안정적인 fine-grained 감독으로 발전시킨 연구이다.
- 🏛 기반 연구: [[papers/2116_Olaf_Bringing_an_Animated_Character_to_Life_in_the_Physical/review]] — 스타일화된 물리 기반 캐릭터 애니메이션의 핵심 방법론을 제공하여 올라프의 believable한 움직임 구현에 활용된다.
- 🔄 다른 접근: [[papers/2135_Perpetual_Humanoid_Control_for_Real-time_Simulated_Avatars/review]] — AMP의 adversarial motion priors가 PHC의 PMCP와 다른 adversarial 접근법으로 robust physics-based character control을 달성합니다.
- 🔄 다른 접근: [[papers/2137_PhysDiff_Physics-Guided_Human_Motion_Diffusion_Model/review]] — diffusion 기반 물리 제약 대신 adversarial motion prior를 통해 물리적으로 타당한 캐릭터 제어를 달성한다.
