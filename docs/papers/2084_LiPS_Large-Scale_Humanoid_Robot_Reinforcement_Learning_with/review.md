---
title: "2084_LiPS_Large-Scale_Humanoid_Robot_Reinforcement_Learning_with"
authors:
  - "Qiang Zhang"
  - "Gang Han"
  - "Jingkai Sun"
  - "Wen Zhao"
  - "Jiahang Cao"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "LiPS는 GPU 기반 병렬 훈련 환경에서 URDF 형식의 휴머노이드 로봇을 위한 강화학습 방법으로, 멀티-리지드바디 폐루프 동역학 모델링을 통해 시뮬레이션-현실 간 격차를 줄인다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Parallel_Robot_Training"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_LiPS Large-Scale Humanoid Robot Reinforcement Learning with Parallel-Series Structures.pdf"
---

# LiPS: Large-Scale Humanoid Robot Reinforcement Learning with Parallel-Series Structures

> **저자**: Qiang Zhang, Gang Han, Jingkai Sun, Wen Zhao, Jiahang Cao, Jiaxu Wang, Hao Cheng, Lingfeng Zhang, Yijie Guo, Renjing Xu | **날짜**: 2025-03-11 | **URL**: [https://arxiv.org/abs/2503.08349](https://arxiv.org/abs/2503.08349)

---

## Essence

![Figure 4](figures/fig4.webp)

*Fig. 4: Illustration of LiPS Simulation Training and Real-World Deployment Process.*

LiPS는 GPU 기반 병렬 훈련 환경에서 URDF 형식의 휴머노이드 로봇을 위한 강화학습 방법으로, 멀티-리지드바디 폐루프 동역학 모델링을 통해 시뮬레이션-현실 간 격차를 줄인다.

## Motivation

- **Known**: IsaacGym 등 GPU 기반 시뮬레이터가 대규모 병렬 강화학습 훈련을 가능하게 하며, 휴머노이드 로봇은 복잡한 직렬-병렬 메커니즘을 포함한다. 현재 대부분의 방법은 훈련 중 개루프 토폴로지를 사용하고 sim2real 단계에서 직렬-병렬 구조로 변환한다.
- **Gap**: 현재 GPU 기반 물리 엔진들은 폐루프 토폴로지나 복잡한 멀티-리지드바디 구조 시뮬레이션 능력이 제한되어 있으며, URDF 형식은 병렬 구조의 동적 특성을 정확히 표현하지 못한다.
- **Why**: 휴머노이드 로봇의 복잡한 동역학을 훈련 단계에서 정확히 시뮬레이션할 수 있으면 훈련 효율을 높이고 sim2real 격차를 줄여 실제 배포 시 성능을 향상시킬 수 있다.
- **Approach**: LiPS는 URDF 기반 시뮬레이션 환경에서 멀티-리지드바디 폐루프 동역학 모델링을 최적화하여 훈련 중부터 병렬 구조를 정확히 표현하고, 이를 통해 sim2real 변환 난이도를 감소시킨다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Illustration of LiPS Simulation Training and Real-World Deployment Process.*

- **대규모 병렬 훈련 지원**: URDF 기반 복잡한 로봇의 GPU 병렬 강화학습 훈련을 효과적으로 지원하는 도구 제공
- **sim2real 격차 감소**: 훈련 단계에서 동역학을 정확히 모델링하여 현실 배포 시 성능 저하 최소화
- **훈련 및 추론 효율 향상**: 복잡한 동적 거동을 시뮬레이션하여 실제 로봇 배포 시 계산 부하와 오류 감소
- **일반화 가능성**: URDF 기반 다양한 로봇에 쉽게 적용 가능한 범용 방법론 제시

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Schematic Diagram of Ankle Dynamics Modeling*

- URDF 모델 파일 형식의 기하학적 특성에 동적 특성을 추가로 모델링
- 멀티-리지드바디 폐루프 동역학을 GPU 기반 IsaacGym 환경에 통합
- 훈련 중 병렬-직렬 구조를 직접 시뮬레이션하여 개루프 토폴로지 대신 사용
- 발목 메커니즘 등 복잡한 병렬 구조의 동역학을 정확히 모델링 (Fig. 3 참조)
- 시뮬레이션 훈련 정책을 실제 로봇에 직접 배포 가능하도록 설계

## Originality

- GPU 기반 대규모 병렬 훈련 환경에서 폐루프 멀티-리지드바디 동역학을 처음으로 효과적으로 모델링
- 기존 개루프 훈련 패러다임의 한계를 극복하고 훈련 단계에서 실제 로봇 구조를 반영하는 새로운 접근
- URDF 형식의 제약을 유지하면서 동적 특성을 추가하는 창의적인 솔루션
- sim2real 변환의 난이도를 근본적으로 해결하는 혁신적 방법론

## Limitation & Further Study

- 현재까지 IsaacGym 기반 구현만 제시되었으며, 다른 GPU 물리 엔진(PyBullet 등)으로의 확장 검증 부족
- URDF 형식 자체의 표현 능력 한계로 인한 극도로 복잡한 병렬 구조에서의 정확도 미검증
- IsaacLab 등 신규 시뮬레이션 플랫폼으로의 적용 가능성 미제시
- 다양한 휴머노이드 로봇 설계(Tesla Optimus, Boston Dynamics 등)에 대한 광범위한 실증 데이터 부족
- **후속 연구**: 실제 하드웨어 배포 시 성능 검증, 다양한 병렬 메커니즘 설계에 대한 일반화 연구, 계산 비용 최적화 방안 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LiPS는 휴머노이드 로봇의 GPU 병렬 강화학습에서 sim2real 격차를 크게 줄이는 실질적이고 실용적인 방법으로, URDF 기반 복잡한 로봇 제어 연구에 중요한 기여를 한다. 다만 광범위한 실제 로봇 검증과 다양한 시뮬레이션 플랫폼으로의 확장 연구가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/2006_Humanoid-Gym_Reinforcement_Learning_for_Humanoid_Robot_with/review]] — 강화학습 기반 휴머노이드 훈련이라는 같은 목표를 다른 시뮬레이션 환경과 병렬화 방식으로 구현한 대안이다.
- 🏛 기반 연구: [[papers/1846_ComFree-Sim_A_GPU-Parallelized_Analytical_Contact_Physics_En/review]] — GPU 기반 병렬 물리 시뮬레이션의 핵심 기술적 기반을 제공하여 LiPS의 대규모 훈련을 가능하게 한다.
- 🔗 후속 연구: [[papers/1942_GaussGym_An_open-source_real-to-sim_framework_for_learning_l/review]] — 실제-시뮬레이션 프레임워크를 GPU 병렬 환경으로 확장하여 더 효율적인 휴머노이드 학습을 실현한다.
- 🧪 응용 사례: [[papers/2151_Toward_Reliable_Sim-to-Real_Predictability_for_MoE-based_Rob/review]] — MoE 기반 로봇 제어의 시뮬레이션-현실 예측 가능성을 대규모 병렬 훈련으로 개선할 수 있다.
- 🔄 다른 접근: [[papers/2061_Learning_Sim-to-Real_Humanoid_Locomotion_in_15_Minutes/review]] — 15분 내 시뮬레이션-현실 학습과 GPU 기반 병렬 훈련이라는 다른 접근법으로 빠른 휴머노이드 학습을 제시한다.
- 🏛 기반 연구: [[papers/1828_Booster_Gym_An_End-to-End_Reinforcement_Learning_Framework_f/review]] — 종단간 강화학습 프레임워크의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2108_Multi-task_Deep_Reinforcement_Learning_with_PopArt/review]] — PopArt의 multi-task 강화학습 정규화 기법이 LiPS의 병렬 훈련에서 다양한 휴머노이드 모델 간 학습 안정성을 향상시킨다.
- 🔄 다른 접근: [[papers/2061_Learning_Sim-to-Real_Humanoid_Locomotion_in_15_Minutes/review]] — GPU 기반 병렬 훈련을 통한 대규모 휴머노이드 강화학습의 다른 접근법을 제시한다.
