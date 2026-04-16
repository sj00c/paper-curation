---
title: "1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion"
authors:
  - "Qingpeng Li"
  - "Chengrui Zhu"
  - "Yanming Wu"
  - "Xin Yuan"
  - "Zhen Zhang"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "RuN은 Conditional Motion Generator를 통한 운동학적 모션 프라이어와 강화학습 기반 residual policy를 분리하여, 인형로봇의 자연스러운 보행-달리기 전환을 실현하는 decoupled residual learning 프레임워크이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_RuN Residual Policy for Natural Humanoid Locomotion.pdf"
---

# RuN: Residual Policy for Natural Humanoid Locomotion

> **저자**: Qingpeng Li, Chengrui Zhu, Yanming Wu, Xin Yuan, Zhen Zhang, Jian Yang, Yong Liu | **날짜**: 2025-09-25 | **URL**: [https://arxiv.org/abs/2509.20696](https://arxiv.org/abs/2509.20696)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the RuN framework. (a) Motion Retargeting: Raw human motions are converted into a kinematically feas*

RuN은 Conditional Motion Generator를 통한 운동학적 모션 프라이어와 강화학습 기반 residual policy를 분리하여, 인형로봇의 자연스러운 보행-달리기 전환을 실현하는 decoupled residual learning 프레임워크이다.

## Motivation

- **Known**: Deep Reinforcement Learning은 인형로봇 제어에 강력하지만, 단일 정책이 운동 모방, 속도 추적, 안정성을 동시에 학습해야 하는 복잡성이 있다. Generative Motion Prior 방식이 자연스러운 동작을 제공하지만 직접 추적(direct tracking) 전략의 학습 복잡성이 여전히 높다.
- **Gap**: 기존 DRL 기반 방법들은 motion imitation, velocity tracking, stability maintenance의 세 가지 목표가 충돌하여 성능과 학습 효율성에 트레이드오프가 발생한다. 이를 해결하기 위한 decoupled 구조의 체계적 접근이 부족하다.
- **Why**: 인형로봇이 인간 중심 환경에서 다양한 속도에서 자연스럽고 동적인 보행을 수행할 수 있어야 하며, 특히 보행-달리기 간 매끄러운 전환은 실용적 배포에 필수적이다.
- **Approach**: CMG를 통해 kinematically natural motion prior를 생성하고, 경량의 residual policy가 동역학적 상호작용을 보정하는 방식으로 제어 태스크를 분해한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Fig. 5: Performance comparison of different algorithms. This figure shows*

- **Decoupled Residual Learning Framework**: 운동 제어를 motion prior와 residual correction으로 분리하여 학습 공간을 대폭 축소
- **Conditional Motion Generator**: 인간 모션 데이터셋으로 학습된 autoregressive 생성 모델로 보행-달리기 범위의 자연스러운 운동 생성
- **광범위한 속도 범위 커버**: 0-2.5 m/s 범위에서 안정적이고 자연스러운 보행과 매끄러운 전환 달성
- **실제 로봇 검증**: Unitree G1 인형로봇에서 시뮬레이션과 현실 실험을 통해 state-of-the-art 대비 우수한 성능 입증
- **학습 효율성 개선**: 기존 방법 대비 훨씬 빠른 training 수렴

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the RuN framework. (a) Motion Retargeting: Raw human motions are converted into a kinematically feas*

- 대규모 인간 모션 데이터셋을 motion retargeting을 통해 kinematically feasible 참조 데이터로 변환
- 변환된 데이터로 autoregressive CMG를 offline으로 학습하여 frozen motion prior 생성
- PPO 강화학습으로 경량 residual policy 훈련하며, imitation rewards, task rewards, regularization rewards의 조합 사용
- 최종 제어 명령 = CMG 출력 + residual policy 출력의 가산 구조
- 시뮬레이션 환경에서 학습 후 실제 로봇으로 sim-to-real 전이

## Originality

- 기존 direct tracking 기반 GMP 방식과 달리 residual learning으로 구조적 분리를 달성한 novel한 접근
- Autoregressive CMG를 humanoid locomotion 분야에 적용하여 조건부 운동 생성의 새로운 활용
- Multi-objective 충돌을 해결하기 위한 principled decomposition으로 학습 복잡성 대폭 감소
- 보행-달리기의 부드러운 전환을 residual policy 프레임워크로 실현한 최초 사례

## Limitation & Further Study

- CMG가 offline 데이터셋에 의존하므로 데이터셋 품질과 다양성이 최종 성능의 상한을 결정
- Residual policy의 보정 범위가 제한되어 있어 극단적인 외부 섭동이나 예상 밖의 동역학에 대한 적응성 미검증
- 실험이 Unitree G1 단일 플랫폼에서만 수행되어 다른 인형로봇 아키텍처로의 일반화 가능성 불명확
- 후속 연구: (1) 적응형 residual policy를 통한 실시간 CMG 재조정, (2) 시각 정보를 활용한 더 복잡한 환경 네비게이션, (3) 더 많은 로봇 플랫폼에서의 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RuN은 humanoid locomotion 제어의 근본적인 복잡성을 elegant하게 해결한 well-motivated 프레임워크로, decoupled residual learning 접근이 학습 효율성과 최종 성능을 모두 개선하며 실제 로봇에서 검증된 강력한 방법론이다.

## Related Papers

- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 인간 모션을 휴머노이드가 따라하는 문제에서 residual learning과 일반적인 추적 방법이라는 다른 접근을 사용한다.
- 🏛 기반 연구: [[papers/2109_Natural_Humanoid_Robot_Locomotion_with_Generative_Motion_Pri/review]] — 자연스러운 휴머노이드 보행을 위한 generative motion prior의 기초적인 개념을 제공한다.
- 🔗 후속 연구: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — StyleLoco의 자연스러운 보행 생성을 조건부 모션 생성기와 residual policy로 분리하여 더 발전시킨다.
- 🔄 다른 접근: [[papers/1635_Reduced-Order_Model-Guided_Reinforcement_Learning_for_Demons/review]] — RuN과 ROM-GRL 모두 자연스러운 휴머노이드 보행을 위한 decoupled learning을 사용하지만 전자는 motion generator 기반, 후자는 ROM 기반이다
- 🔗 후속 연구: [[papers/1925_FastStair_Learning_to_Run_Up_Stairs_with_Humanoid_Robots/review]] — RuN의 자연스러운 보행-달리기 전환이 FastStair의 계단 달리기 학습과 결합되어 더 다양한 동적 이동 능력을 실현할 수 있다
- 🔄 다른 접근: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — 자연스러운 보행을 위해 residual learning vs motion adaptation이라는 서로 다른 decoupling 방식을 사용합니다.
- 🏛 기반 연구: [[papers/1655_Robust_and_Generalized_Humanoid_Motion_Tracking/review]] — motion prior 기반 자연스러운 보행이 robust motion tracking의 기초 methodology가 됩니다.
- 🔄 다른 접근: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — human motion adaptation vs residual policy라는 서로 다른 방식의 자연스러운 휴머노이드 제어 접근법입니다.
- 🔄 다른 접근: [[papers/1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables/review]] — residual action 기반 접근법을 고역동 춤 추적과 자연스러운 보행-달리기 전환에 각각 적용합니다.
- 🔄 다른 접근: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — 두 논문 모두 자연스러운 휴머노이드 보행을 위한 residual learning을 다루지만, adversarial distillation과 조건부 생성기라는 다른 학습 방법을 사용한다.
- 🔄 다른 접근: [[papers/1635_Reduced-Order_Model-Guided_Reinforcement_Learning_for_Demons/review]] — ROM-GRL과 RuN 모두 자연스러운 휴머노이드 보행을 위한 decoupled learning을 사용하지만 전자는 ROM 기반, 후자는 motion generator 기반이다
- 🔄 다른 접근: [[papers/2105_MoRE_Mixture_of_Residual_Experts_for_Humanoid_Lifelike_Gaits/review]] — 둘 다 natural humanoid locomotion이지만 MoRE는 복잡한 지형 횡단에, RuN은 일반적인 자연스러운 보행에 중점을 둔다
- 🔗 후속 연구: [[papers/2109_Natural_Humanoid_Robot_Locomotion_with_Generative_Motion_Pri/review]] — RuN의 natural locomotion을 generative motion prior를 통해 더욱 정교하게 구현한 연구다
- 🔄 다른 접근: [[papers/2110_No_More_Marching_Learning_Humanoid_Locomotion_for_Short-Rang/review]] — 단거리 목표 도달과 자연스러운 보행을 위한 다른 접근법으로, constellation 기반과 residual policy의 차이를 비교할 수 있다.
