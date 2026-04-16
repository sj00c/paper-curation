---
title: "1664_Sampling-Based_System_Identification_with_Active_Exploration"
authors:
  - "Nikhil Sobanbabu"
  - "Guanqi He"
  - "Tairan He"
  - "Yuxiang Yang"
  - "Guanya Shi"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "SPI-Active는 legged robot의 물리 파라미터를 샘플링 기반으로 식별하고 Fisher Information 최대화를 통한 active exploration으로 sim-to-real 갭을 최소화하는 two-stage 프레임워크이다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Sobanbabu et al._2025_Sampling-Based System Identification with Active Exploration for Legged Robot Sim2Real Learning.pdf"
---

# Sampling-Based System Identification with Active Exploration for Legged Robot Sim2Real Learning

> **저자**: Nikhil Sobanbabu, Guanqi He, Tairan He, Yuxiang Yang, Guanya Shi | **날짜**: 2025-05-20 | **URL**: [https://arxiv.org/abs/2505.14266](https://arxiv.org/abs/2505.14266)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of SPI-Active. Data Collection: Collect real-world trajectories using RL policies or*

SPI-Active는 legged robot의 물리 파라미터를 샘플링 기반으로 식별하고 Fisher Information 최대화를 통한 active exploration으로 sim-to-real 갭을 최소화하는 two-stage 프레임워크이다.

## Motivation

- **Known**: Domain Randomization은 sim-to-real 갭 해결에 광범위하게 사용되지만 휴리스틱에 의존하며, System Identification은 물리 파라미터의 원리적 추정을 제공한다.
- **Gap**: 기존 System Identification 기법들은 differentiable dynamics나 직접 torque measurement를 가정하는데, contact-rich legged robot에서는 이러한 조건이 성립하지 않는다. 또한 충분히 정보성 높은 데이터 수집이 어렵다.
- **Why**: 정확한 물리 파라미터 식별은 고정밀 legged locomotion 작업의 zero-shot sim-to-real transfer를 가능하게 하며, 보수적인 정책 대신 성능 최적화된 제어기 학습을 지원한다.
- **Approach**: SPI-Active는 Stage 1에서 병렬 샘플링을 통해 state prediction error를 최소화하는 물리 파라미터를 식별하고, Stage 2에서 optimal experiment design 원리를 적용하여 Fisher Information을 최대화하는 exploration policy의 command sequence를 최적화한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: SPI-Active enables high-fidelity Sim-to-Real transfer across diverse locomotion tasks. To highlight*

- **Specialized sensor-free identification**: Differentiable simulator나 ground-truth torque 측정 없이 contact-rich legged system의 구조화된 물리 파라미터를 식별 가능
- **Hierarchical active exploration strategy**: Pre-trained multi-behavioral RL policy의 command space 최적화를 통해 안정성을 보장하면서 정보성 높은 데이터 수집
- **Significant sim-to-real performance gains**: Quadruped과 humanoid 모두에서 baseline 대비 42-63% 향상된 diverse locomotion task 성능 달성
- **Generalizable framework**: 개별 task-specific tuning 없이 다양한 고정밀 locomotion 작업(jumping, pole weaving, velocity tracking)으로 일반화

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of SPI-Active. Data Collection: Collect real-world trajectories using RL policies or*

- GPU 기반 병렬 샘플링으로 대규모 파라미터 공간 탐색 수행
- RL 정책으로부터 수집한 real-world trajectory와 simulation rollout 간의 state mismatch 최소화 via zeroth-order 최적화
- Fisher Information Matrix 계산으로 각 파라미터의 uncertainty 정량화
- Multi-behavioral RL policy의 command input을 FIM 기반으로 최적화하여 informative trajectory 생성
- 식별된 파라미터를 simulator에 적용하여 downstream task의 RL 정책 학습

## Originality

- Contact-rich legged system을 위한 최초의 complete white-box system identification 프레임워크로, inertial parameter와 actuator dynamics를 joint하게 식별
- Legged robot의 erratic behavior 문제를 해결하기 위해 hierarchical command optimization 도입 (기존 ASID 등과 차별화)
- Pre-trained policy의 command space 최적화로 active exploration의 안정성과 정보성을 동시에 확보하는 novel approach

## Limitation & Further Study

- 식별 정확도는 초기 데이터 수집 정책(RL policy)의 quality에 의존하며, 부실한 초기 정책은 poor identification으로 이어질 수 있음
- Stage 2의 active exploration은 추가적인 계산 비용(Fisher Information 계산 및 optimization)을 요구함
- 현재는 Unitree Go2와 G1 humanoid에만 검증되었으며, 다른 morphology의 robot으로의 generalization 미검증
- 식별된 파라미터의 물리적 interpretability 검증이 부분적으로만 제공됨 (예: 식별된 질량, 관성의 절대값 정확성 평가 미흡)
- 후속연구: (1) 다양한 robot platform에서의 확장, (2) online refinement 메커니즘 추가, (3) 식별 불확실성의 명시적 propagation

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 legged robot의 sim-to-real 갭 해결을 위한 원리적이고 실용적인 system identification 프레임워크를 제시하며, Fisher Information 기반 active exploration 전략의 창의적 적용으로 고정밀 locomotion 작업에서 현저한 성능 향상을 달성했다.

## Related Papers

- 🔄 다른 접근: [[papers/1620_PolySim_Bridging_the_Sim-to-Real_Gap_for_Humanoid_Control_vi/review]] — 두 논문 모두 sim-to-real 갭 해결을 다루지만, 물리 파라미터 식별과 도메인 랜덤화라는 다른 방법을 사용한다.
- 🔗 후속 연구: [[papers/2151_Toward_Reliable_Sim-to-Real_Predictability_for_MoE-based_Rob/review]] — MoE 기반 로봇 제어의 sim-to-real 예측가능성을 샘플링 기반 시스템 식별로 더 정확하게 만든다.
- 🏛 기반 연구: [[papers/1851_Control_of_Humanoid_Robots_with_Parallel_Mechanisms_using_Di/review]] — 로봇 상태 추정을 위한 접촉 기반 필터링의 기초 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1618_PIMBS_Efficient_Body_Schema_Learning_for_Musculoskeletal_Hum/review]] — SPI-Active와 PIMBS 모두 휴머노이드의 물리 파라미터 식별을 다루지만 전자는 sim-to-real 갭 최소화에, 후자는 신체 스키마 학습에 집중한다
- 🔗 후속 연구: [[papers/1850_Contrastive_Representation_Learning_for_Robust_Sim-to-Real_T/review]] — SPI-Active의 Fisher Information 기반 exploration이 Contrastive Representation Learning의 robust sim-to-real 전이와 결합되어 더 효율적인 domain adaptation을 달성할 수 있다
- 🔄 다른 접근: [[papers/1675_Sim-to-Real_of_Humanoid_Locomotion_Policies_via_Joint_Torque/review]] — sim-to-real gap을 physics parameter identification vs joint torque perturbation으로 다르게 해결합니다.
- 🏛 기반 연구: [[papers/1652_Robot_Trains_Robot_Automatic_Real-World_Policy_Adaptation_an/review]] — 물리 파라미터 식별이 로봇 간 knowledge transfer의 기초적인 system identification입니다.
- 🔄 다른 접근: [[papers/1675_Sim-to-Real_of_Humanoid_Locomotion_Policies_via_Joint_Torque/review]] — sim-to-real을 joint torque perturbation vs sampling-based parameter identification으로 다르게 접근합니다.
- 🔗 후속 연구: [[papers/1652_Robot_Trains_Robot_Automatic_Real-World_Policy_Adaptation_an/review]] — sim-to-real 전이에서 dynamics 파라미터 식별과 최적화가 RTR 프레임워크를 더욱 강화할 수 있습니다.
- 🏛 기반 연구: [[papers/1618_PIMBS_Efficient_Body_Schema_Learning_for_Musculoskeletal_Hum/review]] — Sampling-Based System Identification의 능동적 탐색 기반 시스템 식별 방법이 PIMBS의 효율적 신체 스키마 학습의 기초가 됨
- 🔗 후속 연구: [[papers/2048_Learning_Bipedal_Locomotion_on_Gear-Driven_Humanoid_Robot_Us/review]] — Learning Bipedal Locomotion의 random network distillation을 Sampling-Based System Identification의 능동 탐색과 결합하여 더 효과적인 지형 적응 학습이 가능하다.
