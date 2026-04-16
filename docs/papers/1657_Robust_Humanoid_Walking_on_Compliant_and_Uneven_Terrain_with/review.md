---
title: "1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with"
authors:
  - "Rohan P. Singh"
  - "Mitsuharu Morisawa"
  - "Mehdi Benallegue"
  - "Zhaoming Xie"
  - "Fumio Kanehiro"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "Deep RL을 이용하여 humanoid robot HRP-5P가 시뮬레이션에서 terrain randomization으로 학습한 정책을 실제 환경의 compliant하고 uneven한 terrain에서도 robust하게 보행하도록 하는 연구이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Terrain-Adaptive_Humanoid_Locomotion"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Singh et al._2025_Robust Humanoid Walking on Compliant and Uneven Terrain with Deep Reinforcement Learning.pdf"
---

# Robust Humanoid Walking on Compliant and Uneven Terrain with Deep Reinforcement Learning

> **저자**: Rohan P. Singh, Mitsuharu Morisawa, Mehdi Benallegue, Zhaoming Xie, Fumio Kanehiro | **날짜**: 2025-04-18 | **URL**: [https://arxiv.org/abs/2504.13619](https://arxiv.org/abs/2504.13619)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: HRP-5P humanoid bipedal locomotion (clockwise) on flat rigid*

Deep RL을 이용하여 humanoid robot HRP-5P가 시뮬레이션에서 terrain randomization으로 학습한 정책을 실제 환경의 compliant하고 uneven한 terrain에서도 robust하게 보행하도록 하는 연구이다.

## Motivation

- **Known**: Quadrupedal 로봇에서는 deep RL이 model-based 방식을 능가하는 성과를 보였지만, life-sized humanoid의 challenging terrain 보행은 주로 flat surface에 한정되어 있다. 기존 model-based 접근법은 gait parameter tuning과 terrain classification이 필요했다.
- **Gap**: Large mass와 bulky legs를 가진 life-sized humanoid인 HRP-5P에서 compliant surface와 uneven terrain에 대한 robust end-to-end RL 정책의 실제 구현 사례가 부족하다. 또한 blind locomotion 상황에서 proprioceptive feedback만으로 terrain adaptation을 달성하는 연구가 제한적이다.
- **Why**: Real-world deployment를 위해서는 parameter tuning 없이 다양한 terrain type에 자동으로 적응하는 unified controller가 필수적이며, 특히 compliant surface에서의 robust control은 humanoid의 large inertia로 인해 기술적으로 도전적이다.
- **Approach**: Sim-to-real deep RL 접근법으로 simulation에서 randomized terrain으로 training curriculum을 구성하여 정책을 학습하고, adaptive gait frequency를 위한 clock signal modulation을 제안하여 aperiodic gait를 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: HRP-5P humanoid bipedal locomotion (clockwise) on flat rigid*

- **Sim-to-real transfer 성공**: Training curriculum 기반 terrain randomization으로 simulation에서 학습한 single policy가 실제 HRP-5P robot에서 parameter tuning 없이 다양한 terrain (soft cushion, uneven blocks, grass, paved street)에서 robust walking을 달성
- **Proprioceptive feedback 기반 제어**: Vision이나 terrain classification 없이 joint encoders, IMU, motor current sensors로부터의 정보만으로 terrain 적응
- **Adaptive gait frequency**: Clock signal modulation을 통해 swing과 stance duration을 동적으로 조절하여 challenging terrain에서 보행 robustness 향상
- **다중 보행 모드**: Standing, stepping in-place, forward walking 등 다양한 보행 모드를 단일 정책으로 구현
- **재현성 보장**: Code와 demo video 공개로 연구 재현성 확보

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of our training framework. (L) We propose to train a feedforward RL agent while exposing it to randomiz*

- Model-free deep RL을 이용한 end-to-end policy 학습
- Simulation 환경에서 compliant/uneven terrain randomization curriculum으로 training
- Observation space: proprioceptive measurements (joint positions/velocities, IMU, motor currents), walking mode (one-hot 3D), speed reference (1D scalar), clock signal (sin/cos 기반 cyclic phase variable)
- Action space: 12D joint position commands (6 legs × 2 joints), fixed motor offsets와 low-gain PD controller로 tracking
- Reward function: Bipedal gait terms + mode command tracking + realistic motion terms (Table III 참조)
- Clock control policy: Phase variable φ의 modulation을 학습하여 cycle period L을 동적으로 조절
- 40Hz policy execution + 1000Hz PD control loop
- Early termination: Root height 60cm 미만 또는 self-collision 시 episode 종료

## Originality

- Life-sized humanoid HRP-5P에서 compliant surface와 irregular terrain에 대한 end-to-end RL 정책의 실제 성공 구현 (기존은 flat surface나 simulation에 주로 한정)
- Clock signal modulation을 통한 adaptive gait frequency 개념 도입으로 aperiodic motion 실현 (기존 fixed cycle 기반 접근과 차별화)
- Blind locomotion (exteroceptive sensor 없음) 환경에서 proprioceptive feedback만으로 terrain adaptation 달성
- Terrain randomization curriculum의 효과적인 설계로 sim-to-real transfer의 robustness 입증

## Limitation & Further Study

- Simulation과 real robot 간의 physics mismatch로 인한 sim-to-real gap에 대한 상세한 분석 부족
- Clock control policy의 개선 정도를 quantitative하게 비교한 결과 제시 부족 (simulation에서의 systematic evaluation만 제시)
- 극도로 soft한 surface나 매우 높은 step obstacle에 대한 failure case 분석 미흡
- Computational cost와 training time에 대한 보고 부족
- 다른 humanoid platform (TOCABI 등)으로의 generalization 가능성에 대한 논의 부족
- Real robot에서 adaptive clock control policy의 실제 효과 검증 부재 (simulation에서만 검증)

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Life-sized humanoid의 challenging terrain 보행을 위한 deep RL 기반 접근법의 실제 구현을 성공적으로 입증했으며, sim-to-real transfer와 adaptive gait control의 효과를 명확히 보여준 의미 있는 연구이다. 다만 clock control 정책의 실제 적용 효과 검증과 failure case 분석이 보강되면 더욱 완성도 높은 작업이 될 수 있다.

## Related Papers

- 🔗 후속 연구: [[papers/1677_SKATER_Synthesized_Kinematics_for_Advanced_Traversing_Effici/review]] — Terrain randomization 기반 robust walking이 롤러스케이팅과 같은 특수한 지형 적응 기법으로 확장되어 더 다양한 환경 대응이 가능하다.
- 🔄 다른 접근: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — Deep RL terrain adaptation과 passive dynamics 활용은 모두 에너지 효율적인 이족 보행을 위한 서로 다른 접근 방식이다.
- 🔄 다른 접근: [[papers/1620_PolySim_Bridging_the_Sim-to-Real_Gap_for_Humanoid_Control_vi/review]] — 두 논문 모두 시뮬레이션 학습을 실제 환경에 적용하는 문제를 다루지만, 다른 도메인 랜덤화 전략을 사용한다.
- 🔗 후속 연구: [[papers/2061_Learning_Sim-to-Real_Humanoid_Locomotion_in_15_Minutes/review]] — 15분만에 학습하는 빠른 sim-to-real 방법을 compliant terrain에서의 강건한 보행으로 확장한다.
- 🧪 응용 사례: [[papers/1978_Hiking_in_the_Wild_A_Scalable_Perceptive_Parkour_Framework_f/review]] — 야생 환경에서의 parkour 프레임워크를 compliant하고 불규칙한 지형에서의 보행에 적용한다.
- 🔗 후속 연구: [[papers/1658_RPL_Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challe/review]] — compliant terrain 보행 연구가 payload 추가와 복잡한 지형으로 더욱 도전적인 환경으로 확장됩니다.
- 🏛 기반 연구: [[papers/1675_Sim-to-Real_of_Humanoid_Locomotion_Policies_via_Joint_Torque/review]] — domain randomization의 한계를 극복한 sim-to-real 방법이 복잡 지형 보행에 필수적입니다.
- 🔗 후속 연구: [[papers/1675_Sim-to-Real_of_Humanoid_Locomotion_Policies_via_Joint_Torque/review]] — 개선된 sim-to-real 전이가 복잡한 지형에서의 robust walking으로 적용됩니다.
- 🔄 다른 접근: [[papers/1677_SKATER_Synthesized_Kinematics_for_Advanced_Traversing_Effici/review]] — 수동 바퀴를 활용한 스위즐 보행과 전통적인 terrain adaptation은 모두 충격과 에너지를 줄이는 서로 다른 보행 전략이다.
- 🏛 기반 연구: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — 이족 보행의 기본이 되는 강건한 점프 제어가 복잡한 지형 보행의 토대가 됩니다.
- 🔄 다른 접근: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — 패시브 다이내믹스 기반 에너지 효율성과 terrain randomization 기반 robust성은 이족 보행의 서로 다른 최적화 목표이다.
- 🔗 후속 연구: [[papers/1982_Hold_My_Beer_Learning_Gentle_Humanoid_Locomotion_and_End-Eff/review]] — compliant하고 불균등한 지형에서의 강건한 보행을 부드러운 물체 운반 상황으로 확장한 형태다.
