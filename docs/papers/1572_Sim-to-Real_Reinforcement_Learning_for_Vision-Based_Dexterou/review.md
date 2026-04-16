---
title: "1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou"
authors:
  - "Toru Lin"
  - "Kartik Sachdev"
  - "Linxi Fan"
  - "Jitendra Malik"
  - "Yuke Zhu"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 휴머노이드 로봇의 다중 손가락 손을 이용한 시각 기반 정교한 조작을 위해 sim-to-real RL을 적용하는 실용적인 레시피를 제시하며, 자동화된 실-시뮬레이션 튜닝, 일반화된 보상 설계, 분할-정복 정책 증류, 하이브리드 객체 표현을 통합한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multi-Task_Language_Benchmarks"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lin et al._2025_Sim-to-Real Reinforcement Learning for Vision-Based Dexterous Manipulation on Humanoids.pdf"
---

# Sim-to-Real Reinforcement Learning for Vision-Based Dexterous Manipulation on Humanoids

> **저자**: Toru Lin, Kartik Sachdev, Linxi Fan, Jitendra Malik, Yuke Zhu | **날짜**: 2025-02-27 | **URL**: [https://arxiv.org/abs/2502.20396](https://arxiv.org/abs/2502.20396)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: A sim-to-real RL recipe for vision-based dexterous manipulation. We close the environment*

본 논문은 휴머노이드 로봇의 다중 손가락 손을 이용한 시각 기반 정교한 조작을 위해 sim-to-real RL을 적용하는 실용적인 레시피를 제시하며, 자동화된 실-시뮬레이션 튜닝, 일반화된 보상 설계, 분할-정복 정책 증류, 하이브리드 객체 표현을 통합한다.

## Motivation

- **Known**: Sim-to-real RL은 네비게이션, 로코모션 등에서 성공했으나, 기존 연구는 주로 단일 손이나 상태 기반 설정에 제한되어 있다. 시각 기반 이중 손 조작 학습은 주로 모방 학습에 의존하며 비용이 크다.
- **Gap**: 시각 기반, 접촉이 풍부한 이중 손 조작 작업으로 RL을 효과적으로 확장하는 방법이 명확하지 않으며, 저비용 조작 시스템에서 정확한 실-시뮬레이션 모델링이 부족하다.
- **Why**: 휴머노이드 로봇의 정교한 조작 능력은 제조, 돌봄, 위험 작업 등 현실적 응용에 필수적이며, 확장 가능한 학습 방법은 대규모 로봇 배포를 가능하게 한다.
- **Approach**: 본 논문은 네 가지 핵심 모듈을 통합한다: (1) 4분 미만의 실제 데이터로 파라미터를 자동 조정하는 real-to-sim 모듈, (2) 접촉 및 객체 목표 기반 일반화 보상, (3) 작업 인식 초기화와 divide-and-conquer 정책 증류를 통한 탐색 가속화, (4) sparse/dense 객체 표현과 modality-specific augmentation을 통한 도메인 이동 해결.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview. We train a humanoid robot with two multi-fingered hands to perform a range of contact-*

- **높은 성공률**: 보이지 않은 실제 객체에 대해 본 객체 90%, 미본 객체 60~80% 성공률 달성
- **다양한 작업 학습**: grasp-and-reach, bimanual lift, bimanual handover 세 가지 정교한 조작 작업 성공
- **하드웨어 적응성**: Fourier Hand와 Inspire Hand 두 종류의 다중 손가락 손에서 성능 검증
- **객체 일반화**: 형태, 크기, 색상, 재질, 질량이 다양한 미본 객체에 대한 zero-shot 전이 달성
- **강건성**: 외력 교란에 대한 견고하고 적응적인 정책 행동 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: A sim-to-real RL recipe for vision-based dexterous manipulation. We close the environment*

- **Real-to-Sim 자동 튜닝**: 200 스텝의 joint target 추적 오차 MSE를 최소화하는 파라미터 그리드 서치로 물리 파라미터 및 URDF 파라미터 조정
- **보상 설계**: 접촉 마커 기반 접촉 목표와 3D 객체 중심 위치 기반 객체 목표를 결합하여 이중 손 협력 수행
- **작업 인식 초기화**: 각 작업별 손의 초기 포즈를 설정하여 탐색 효율 향상
- **Divide-and-Conquer 증류**: 단일 작업 specialists 학습 후 generalist 정책으로 증류하여 다중 객체 학습 효율화
- **하이브리드 객체 표현**: Segment Anything 2로 분할된 RGB와 깊이 기반 sparse 표현(객체 중심 위치)과 high-dimensional 특성 결합
- **Modality-specific 증강**: RGB masked augmentation과 깊이 segmentation을 통한 도메인 랜더마이제이션

## Originality

- 저비용 휴머노이드 플랫폼을 위한 자동화된 real-to-sim 시스템 식별 방법으로 4분 미만의 데이터로 충분한 결과 도출
- 접촉-객체 목표 이중 구조를 통한 이중 손 협력 보상 설계의 새로운 접근
- Divide-and-Conquer 정책 증류 프레임워크로 다중 객체 학습 시 탐색 병목 해결
- Sparse/Dense 하이브리드 객체 표현과 modality-specific augmentation 조합으로 80~100% 성공률 개선
- 다중 손가락 손 하드웨어 변형에 대한 최초의 robustness 검증

## Limitation & Further Study

- Real-to-Sim 튜닝이 4분 데이터 필요하므로 완전히 zero-shot이 아니며, 새로운 로봇 플랫폼마다 재튜닝 필요
- 미본 객체에서 60~80% 성공률은 본 객체 대비 상당한 하락을 보이며, 더 복잡한 형태의 객체 일반화 성능이 미흡할 수 있음
- 방법론이 여러 모듈의 조합으로 구성되어 각 컴포넌트의 독립적 기여도 분석이 제한적
- **후속 연구**: (1) 메타 러닝 또는 few-shot adaptation으로 더 빠른 새 플랫폼 적응, (2) 더 강력한 객체 표현 학습으로 일반화 성능 개선, (3) 추상적 스킬 학습으로 다양한 작업 간 지식 전이

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 sim-to-real RL을 실제 휴머노이드 다중 손가락 조작으로 처음 확장하는 실용적이고 포괄적인 솔루션을 제시하며, 자동화된 시스템 식별과 정책 증류 등 여러 혁신을 통해 높은 성공률과 일반화 능력을 입증한다. 다만 미본 객체 성능과 방법의 복잡성 개선에는 여지가 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — Real-World Humanoid Locomotion은 sim-to-real 접근법을 보행에 적용하여 조작과 다른 embodiment에서의 RL 적용 사례를 제시한다.
- 🏛 기반 연구: [[papers/1451_Learning_Human-to-Humanoid_Real-Time_Whole-Body_Teleoperatio/review]] — Human-to-Humanoid Teleoperation 연구는 정교한 조작을 위한 sim-to-real의 기반이 되는 인간-로봇 인터페이스를 제공한다.
- 🏛 기반 연구: [[papers/1431_Impact_of_Static_Friction_on_Sim2Real_in_Robotic_Reinforceme/review]] — 정적 마찰이 Sim2Real에 미치는 영향 연구는 정교한 조작에서 sim-to-real 성공의 핵심 요소를 분석한다.
- 🔄 다른 접근: [[papers/1523_Re3Sim_Generating_High-Fidelity_Simulation_Data_via_3D-Photo/review]] — Re3Sim은 고충실도 시뮬레이션 데이터 생성으로 sim-to-real 문제를 다른 각도에서 해결하는 접근법이다.
- 🔄 다른 접근: [[papers/1625_VR-Robo_A_Real-to-Sim-to-Real_Framework_for_Visual_Robot_Nav/review]] — 두 논문 모두 sim-to-real 전이를 다루지만 손가락 조작 vs 시각 네비게이션으로 응용 영역이 다릅니다.
- 🏛 기반 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — Deep RL for Robotics 서베이는 sim-to-real RL의 이론적 배경과 실제 적용 사례를 포괄적으로 제시합니다.
- 🔄 다른 접근: [[papers/1354_Dex1B_Learning_with_1B_Demonstrations_for_Dexterous_Manipula/review]] — Dex1B가 대규모 시연 데이터에 중점을 두는 반면, Sim-to-Real RL은 시뮬레이션에서 실제로의 전이 문제를 중점적으로 다룬다.
- 🔗 후속 연구: [[papers/1431_Impact_of_Static_Friction_on_Sim2Real_in_Robotic_Reinforceme/review]] — 정적 마찰을 고려한 도메인 랜덤화가 Sim-to-Real 강화학습에서 데스크테라스 조작의 현실 적응성을 크게 개선한다.
- 🔗 후속 연구: [[papers/1484_MuJoCo_Playground/review]] — MuJoCo Playground의 제로샷 sim-to-real 능력은 시각 기반 손재주 조작의 sim-to-real 연구를 더욱 효율적으로 만듭니다.
- 🔗 후속 연구: [[papers/1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with/review]] — sim-to-real transfer의 기본 개념을 navigation diffusion policy와 privileged information을 활용한 zero-shot transfer로 확장한다.
- 🔄 다른 접근: [[papers/1524_Reactive_Diffusion_Policy_Slow-Fast_Visual-Tactile_Policy_Le/review]] — RDP의 visual-tactile policy와 달리 vision-based dexterous manipulation을 위한 sim-to-real 강화학습 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1625_VR-Robo_A_Real-to-Sim-to-Real_Framework_for_Visual_Robot_Nav/review]] — 두 논문 모두 sim-to-real 전이를 다루지만 시각 네비게이션 vs 정교한 손가락 조작으로 응용 도메인이 다릅니다.
- 🔗 후속 연구: [[papers/1355_DexGarmentLab_Dexterous_Garment_Manipulation_Environment_wit/review]] — 시각 기반 손재주 조작의 sim-to-real 강화학습을 의류 조작으로 확장할 수 있습니다.
- 🧪 응용 사례: [[papers/1386_Evaluating_Real-World_Robot_Manipulation_Policies_in_Simulat/review]] — Sim-to-Real RL 방법론이 SIMPLER 환경에서 훈련된 정책을 실제 로봇으로 전이하는 구체적인 적용 방법을 제공합니다.
- 🏛 기반 연구: [[papers/1309_An_Real-Sim-Real_RSR_Loop_Framework_for_Generalizable_Roboti/review]] — 시각 기반 정교한 조작을 위한 Sim-to-Real 강화학습의 기초 이론을 제공한다.
