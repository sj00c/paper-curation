---
title: "1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys"
authors:
  - "Xue Bin Peng"
  - "Pieter Abbeel"
  - "Sergey Levine"
  - "Michiel van de Panne"
date: "2018.04"
doi: ""
arxiv: ""
score: 4.0
essence: "Motion capture 데이터를 활용한 example-guided reinforcement learning으로 물리 기반 캐릭터 애니메이션을 학습하는 방법을 제안하며, 모션 모방과 task 목표를 결합하여 강건하고 다양한 기술을 수행하는 제어 정책을 학습한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Character_Motion_Policy_Transfer"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Peng et al._2018_DeepMimic Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills.pdf"
---

# DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills

> **저자**: Xue Bin Peng, Pieter Abbeel, Sergey Levine, Michiel van de Panne | **날짜**: 2018-04-08 | **URL**: [https://arxiv.org/abs/1804.02717](https://arxiv.org/abs/1804.02717)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Highly dynamic skills learned by imitating reference motion capture clips using our method, executed by physical*

Motion capture 데이터를 활용한 example-guided reinforcement learning으로 물리 기반 캐릭터 애니메이션을 학습하는 방법을 제안하며, 모션 모방과 task 목표를 결합하여 강건하고 다양한 기술을 수행하는 제어 정책을 학습한다.

## Motivation

- **Known**: Physics 기반 캐릭터 애니메이션은 오래된 연구 분야이며, Deep RL은 복잡한 행동을 학습할 수 있지만 생성된 모션 품질이 낮고 부자연스러운 artifacts를 보이는 것으로 알려져 있다.
- **Gap**: 기존 RL 방법은 모션 품질이 낮고, kinematic animation과 physics 기반 tracking controller를 결합한 방식은 복잡하며 제한된 유연성을 가진다.
- **Why**: Animation 품질과 physics 기반 시뮬레이션의 강건성을 동시에 달성할 수 있다면 사용자가 원하는 스타일을 유지하면서도 환경 변화와 perturbation에 자연스럽게 대응하는 캐릭터 애니메이션이 가능해진다.
- **Approach**: Motion capture 데이터에 기반한 reference state imitation reward와 task objective를 결합한 RL 프레임워크를 구성하며, phase-aware policy를 사용하여 reference motion과 유사한 물리 기반 행동을 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Highly dynamic skills learned by imitating reference motion capture clips using our method, executed by physical*

- **Motion quality와 robustness의 결합**: Reference motion capture 데이터를 활용하여 prior deep RL 방법보다 훨씬 자연스럽고 품질 높은 모션을 생성하면서도 perturbation에 강건한 제어 정책을 달성
- **다양한 동적 기술 학습**: Cartwheel, spinkick 등 매우 동적인 acrobatic 기술부터 locomotion, martial arts까지 광범위한 기술을 단일 프레임워크로 학습
- **다중 클립 통합**: Max-operator 기반 multi-clip reward, multi-task policy 학습, value function 기반 policy sequencing 등 여러 모션 클립을 통합하는 방법 제시
- **다양한 캐릭터 적용**: Humanoid, Atlas robot, bipedal dinosaur, dragon 등 여러 morphology의 캐릭터에 대한 scalability 입증
- **Ablation study**: Reference state initialization과 early termination이 highly dynamic skill 학습에 critical한 요소임을 규명

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Schematic illustration of the visuomotor policy network. The*

- Reference motion capture 데이터로부터 target state trajectory를 추출하고, imitation reward를 통해 학습 정책이 reference motion을 따르도록 유도
- Phase-aware policy network를 사용하여 motion의 cyclic nature를 명시적으로 모델링
- Motion imitation objective와 task objective (e.g., 특정 방향으로 걷기, 목표 던지기)를 weighted combination으로 결합
- Reference state initialization을 통해 학습 초기에 reference trajectory 근처에서 시작하는 trajectory distribution 활용
- Early termination을 통해 reference motion에서 벗어나면 episode를 종료하여 학습 효율 증대
- Multi-clip 통합: (1) max operator 기반 reward로 여러 클립 중 가장 적합한 것 선택, (2) Multi-task policy 학습으로 diverse skills 동시 학습, (3) Value function 기반 feasibility 평가로 single-clip policies 연결

## Originality

- Motion capture와 deep RL의 결합 자체는 새로운 것은 아니지만, 구체적인 reward design (phase-aware imitation reward), reference state initialization, early termination 등의 특정 기법 조합이 physics-based character animation 맥락에서 효과적임을 처음 체계적으로 입증
- 다양한 morphology의 캐릭터와 기술에 대한 광범위한 실증적 검증으로 방법의 일반성 입증
- Multi-clip 통합을 위한 여러 전략 제시 (max-operator, multi-task, policy sequencing)로 실제 애니메이션 제작 워크플로우에 실용적 가치 추가
- Phase-aware representation을 통해 cyclic motion의 특성을 명시적으로 활용하는 설계

## Limitation & Further Study

- Method의 각 component가 individually well-known이므로 기술적 novelty 자체는 제한적 (조합의 효과성이 주요 기여)
- Reference motion capture 데이터에 대한 의존성으로 인해 새로운 기술 개발보다는 기존 모션의 재현과 변형에 주로 활용 가능
- Highly dynamic skill 학습에 있어서도 reference trajectory 근처에서의 학습 bias로 인해 reference와 크게 다른 새로운 동작 생성의 한계
- Multiple characters에 대한 실험이 보여지지만, 각 morphology별 reward function 조정의 필요성에 대한 논의 부족
- 후속 연구: Reinforcement learning과 data-driven 방식의 균형을 자동으로 조정하는 adaptive weighting 메커니즘 개발, hierarchical policy structure를 통한 더 복잡한 skill composition 실현, sim-to-real transfer를 위한 robust domain adaptation 기법 연구

## Evaluation

- Novelty: 3/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 개별 기술의 novel 한 조합보다는 physics-based character animation에서의 효과적 시스템 설계를 통해 실질적 가치를 제시하며, 광범위한 실증 결과로 방법의 실용성과 확장성을 강력히 입증한 매우 영향력 있는 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1801_AMP_Adversarial_Motion_Priors_for_Stylized_Physics-Based_Cha/review]] — motion capture 데이터 활용에서 example-guided learning과 adversarial motion prior라는 서로 다른 학습 패러다임을 제시한다
- 🔗 후속 연구: [[papers/1785_A_Whole-Body_Motion_Imitation_Framework_from_Human_Data_for/review]] — 전신 동작 모방 프레임워크가 DeepMimic의 motion capture 기반 학습을 실제 휴머노이드 로봇에 적용할 수 있는 구체적인 구현 방법을 제공한다
- 🏛 기반 연구: [[papers/2092_MaskedMimic_Unified_Physics-Based_Character_Control_Through/review]] — MaskedMimic의 통합된 물리 기반 캐릭터 제어가 DeepMimic의 예시 기반 학습에 필요한 마스킹과 제어 통합 기술을 제공한다
- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — whole-body motion tracking을 residual learning으로 접근하여 DeepMimic과 다른 관점의 해결책을 제시한다.
- 🔄 다른 접근: [[papers/1615_Physics-Based_Motion_Imitation_with_Adversarial_Differential/review]] — 물리 기반 모션 모방을 위한 다른 적대적 학습 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1643_RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with/review]] — 물리적 피드백을 통한 대형 모션 모델 정렬로 발전됩니다.
- 🏛 기반 연구: [[papers/1952_GENMO_A_GENeralist_Model_for_Human_MOtion/review]] — 인간 모션에 대한 일반적 모델링 접근법의 기초를 제공합니다.
- 🏛 기반 연구: [[papers/1691_Stabilizing_Humanoid_Robot_Trajectory_Generation_via_Physics/review]] — 예시 기반 깊은 강화학습의 물리 기반 캐릭터 제어 기초를 제공한다.
- 🏛 기반 연구: [[papers/1612_PhysHMR_Learning_Humanoid_Control_Policies_from_Vision_for_P/review]] — PhysHMR의 비전-기반 물리적 제어 정책 학습이 DeepMimic의 example-guided 강화학습 방법론을 확장한 것이다
- 🏛 기반 연구: [[papers/1615_Physics-Based_Motion_Imitation_with_Adversarial_Differential/review]] — DeepMimic의 physics-based character control과 adversarial training 방법론이 ADD의 적대적 차별자 설계의 이론적 기초를 제공함
- 🏛 기반 연구: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — DeepMimic의 물리 기반 모방 학습 프레임워크가 VisualMimic의 동작 추적 방법론의 기초가 된다.
- 🏛 기반 연구: [[papers/1758_Whole-body_Humanoid_Robot_Locomotion_with_Human_Reference/review]] — DeepMimic의 예시 기반 강화학습 방법론이 인간 보행 데이터 모방 학습의 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1801_AMP_Adversarial_Motion_Priors_for_Stylized_Physics-Based_Cha/review]] — 둘 다 motion capture 데이터를 활용하지만 adversarial prior와 example-guided learning이라는 서로 다른 학습 패러다임을 제시한다
- 🏛 기반 연구: [[papers/1785_A_Whole-Body_Motion_Imitation_Framework_from_Human_Data_for/review]] — DeepMimic의 motion capture 기반 모방 학습 방법론이 인간 데이터로부터 전신 동작을 학습하는 핵심 기반을 제공한다
- 🏛 기반 연구: [[papers/1975_Hierarchical_visuomotor_control_of_humanoids/review]] — 예제 가이드 깊은 강화학습이 계층적 시각운동 제어의 기반 방법론이다.
- 🏛 기반 연구: [[papers/2026_InterMimic_Towards_Universal_Whole-Body_Control_for_Physics-/review]] — 물리 기반 캐릭터 제어의 기본적인 강화학습 원리와 모방 학습 방법론의 이론적 토대를 제공한다.
- 🏛 기반 연구: [[papers/2037_KungfuBot_Physics-Based_Humanoid_Whole-Body_Control_for_Lear/review]] — 물리 기반 캐릭터 제어를 위한 강화학습의 기본 원리가 쿵푸 동작 모방 학습의 이론적 토대를 제공한다.
- 🏛 기반 연구: [[papers/2067_Learning_to_Control_Physically-simulated_3D_Characters_via_G/review]] — 물리 기반 캐릭터 제어의 기본 방법론을 2D 데이터 기반 3D 제어로 확장한 기반
- 🏛 기반 연구: [[papers/2116_Olaf_Bringing_an_Animated_Character_to_Life_in_the_Physical/review]] — DeepMimic의 physics-based character control 방법론이 애니메이션 캐릭터를 실제 물리 로봇으로 구현하는 Olaf의 핵심 기술적 토대를 제공합니다.
- 🏛 기반 연구: [[papers/2135_Perpetual_Humanoid_Control_for_Real-time_Simulated_Avatars/review]] — DeepMimic의 example-guided deep RL이 PHC의 대규모 motion clips 학습과 physics-based control의 기술적 토대를 제공합니다.
