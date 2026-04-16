---
title: "1680_SLAC_Simulation-Pretrained_Latent_Action_Space_for_Whole-Bod"
authors:
  - "Jiaheng Hu"
  - "Peter Stone"
  - "Roberto Martín-Martín"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "SLAC는 저충실도 시뮬레이터에서 학습한 task-agnostic 잠재 행동 공간을 사용하여 고자유도 모바일 매니퓨레이터가 실제 환경에서 효율적이고 안전하게 강화학습으로 접촉이 풍부한 전신 조작 작업을 학습할 수 있게 한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hu et al._2025_SLAC Simulation-Pretrained Latent Action Space for Whole-Body Real-World RL.pdf"
---

# SLAC: Simulation-Pretrained Latent Action Space for Whole-Body Real-World RL

> **저자**: Jiaheng Hu, Peter Stone, Roberto Martín-Martín | **날짜**: 2025-06-04 | **URL**: [https://arxiv.org/abs/2506.04147](https://arxiv.org/abs/2506.04147)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: SLAC uses a task-agnostic action space trained in low-fidelity simulation (left) to learn*

SLAC는 저충실도 시뮬레이터에서 학습한 task-agnostic 잠재 행동 공간을 사용하여 고자유도 모바일 매니퓨레이터가 실제 환경에서 효율적이고 안전하게 강화학습으로 접촉이 풍부한 전신 조작 작업을 학습할 수 있게 한다.

## Motivation

- **Known**: 시뮬레이션 기반 강화학습은 현실 격차로 인해 취약하고, 실제 환경 강화학습은 안전 탐색과 표본 효율성 문제로 고자유도 로봇에 적용하기 어렵다.
- **Gap**: 고자유도 모바일 매니퓨레이터가 데모나 사전 정의된 행동 우선순위 없이 실제 환경에서 학습하면서도 안전하고 효율적인 강화학습을 수행할 수 있는 방법이 부재했다.
- **Why**: 가정용 및 산업용 로봇이 복잡한 고자유도 시스템을 제어해야 하는데, 기존 방법들은 표본 효율성, 안전성, 현실 격차 중 하나 이상에서 한계를 보여 실제 배포가 어렵다.
- **Approach**: SLAC는 두 단계 절차를 통해 문제를 해결한다: (1) 저충실도 시뮬레이터에서 unsupervised skill discovery를 통해 시간적 추상화, 분리성(disentanglement), 안전성을 갖춘 latent action space를 학습하고, (2) 이를 action interface로 사용하는 novel off-policy RL 알고리즘으로 실제 환경에서 downstream task를 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: SLAC uses a task-agnostic action space trained in low-fidelity simulation (left) to learn*

- **1시간 미만의 실제 상호작용으로 학습**: bimanual mobile manipulator가 데모나 hand-crafted behavior priors 없이 접촉이 풍부한 전신 조작 작업(청소, 장애물 회피, 집기 등)을 1시간 이내에 학습
- **높은 표본 효율성**: latent action space를 통해 고차원 native action space에서의 직접 강화학습 대비 현저히 향상된 표본 효율성 달성
- **안전한 탐색**: unsupervised skill discovery 목적함수가 위험한 행동을 피하도록 설계되어 로봇과 환경 손상 위험 감소
- **현실 격차 강건성**: 저충실도 시뮬레이터 사용으로 high-fidelity simulation의 필요성 제거하고, latent action 수준에서의 약간의 불일치는 실제 환경 보상 신호로 보정 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2: The two-step SLAC procedure to enable real-world policy learning. (Left) In the first*

- **Unsupervised Skill Discovery (USD)**: 저충실도 시뮬레이터에서 task-agnostic latent action space를 학습하기 위해 customized USD 목적함수 설계
- **Temporal Abstraction**: latent actions를 여러 환경 스텝에 걸쳐 실행되도록 하여 decision frequency 감소 및 탐색 효율성 향상
- **Disentanglement**: 각 latent action 차원이 독립적으로 상태에 영향을 미치도록 학습하여 여러 제어 목표의 동시 최적화 용이
- **Safety Objective**: USD 목적함수에 안전성 제약을 통합하여 위험한 행동 패턴 억제
- **Multi-discrete Latent Action Space**: 연속 행동 공간 대신 N-dimensional multi-discrete latent action space Z = Z₁ × · · · × Zₙ 사용
- **Latent Action Decoder**: πdec(a|odec, z)를 학습하여 latent action z를 low-level action a로 변환
- **Perception-to-Latent Task Policy**: πtask(z|o)를 실제 환경에서 novel off-policy RL 알고리즘으로 학습, 고차원 관측 o(카메라 이미지)에서 latent action 선택
- **Shared Decoder Observation**: odec(고유 상태, 가구 자세 등)를 시뮬레이션과 실제 환경 간 공유하여 도메인 갭 감소

## Originality

- **저충실도 시뮬레이션 활용**: 기존 sim-to-real 방법들과 달리 high-fidelity simulation에 의존하지 않고 행동 공간 학습만을 목적으로 저충실도 시뮬레이터 활용
- **Task-agnostic Pretraining**: task-specific이 아닌 generic latent action space를 시뮬레이션에서 학습하여 다양한 downstream task에 재사용 가능
- **통합된 USD 목적함수**: 시간적 추상화, 분리성, 안전성을 동시에 촉진하는 customized unsupervised skill discovery 목적함수 제안
- **데모 및 우선순위 제거**: 기존 고자유도 로봇 실제 학습 방법들과 달리 demonstrations나 hand-crafted behavior priors 없이 순수 자율 학습 실현

## Limitation & Further Study

- **저충실도 시뮬레이터 필요성**: 여전히 시뮬레이터에 대한 접근성이 필요하며, latent action space의 품질이 시뮬레이션의 정확도에 의존
- **Decoder Observation의존성**: shared decoder observation odec(고유 상태 등)의 정확한 측정이 필요하며, 이는 로봇 플랫폼마다 설정 필요
- **다중 과제 평가 제한**: 논문에서는 bimanual mobile manipulator의 특정 조작 작업들만 평가, 다른 고자유도 로봇(휴머노이드 등)이나 작업 도메인에의 일반화 검증 필요
- **실제 환경 보상 설계**: downstream task learning을 위해 여전히 각 작업별 reward function Rtask 설계 필요
- **후속 연구 방향**: (1) 더 복잡한 시뮬레이션-현실 갭에서의 latent action robustness 향상, (2) 연속 latent action space로의 확장 및 비교, (3) 보상 설계 부담 감소를 위한 reward learning 통합, (4) 다양한 고자유도 로봇 플랫폼과 도메인으로의 일반화 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SLAC는 저충실도 시뮬레이션 기반 latent action space pretraining과 실제 환경 강화학습을 결합하여 고자유도 모바일 매니퓨레이터의 복잡한 접촉 조작 작업을 안전하고 효율적으로 학습할 수 있게 하는 혁신적인 접근법을 제시하며, 1시간 미만의 실제 상호작용만으로 의미 있는 성과를 달성함으로써 실제 로봇 학습의 실용성을 크게 향상시킨다.

## Related Papers

- 🔄 다른 접근: [[papers/2089_ManiSkill-HAB_A_Benchmark_for_Low-Level_Manipulation_in_Home/review]] — 두 논문 모두 전신 조작 작업을 다루지만, 잠재 행동 공간과 홈 환경 벤치마크라는 다른 접근을 사용한다.
- 🏛 기반 연구: [[papers/1614_Physically_Consistent_Humanoid_Loco-Manipulation_using_Laten/review]] — 물리적으로 일관된 휴머노이드 조작을 위한 잠재 공간 사용의 기초 개념을 제공한다.
- 🔗 후속 연구: [[papers/2159_TrajBooster_Boosting_Humanoid_Whole-Body_Manipulation_via_Tr/review]] — 전신 조작을 위한 궤적 향상 방법을 잠재 행동 공간에서 더 효율적으로 구현한다.
- 🔄 다른 접근: [[papers/1751_Visual_Imitation_Enables_Contextual_Humanoid_Control/review]] — 전신 조작 학습에서 잠재 행동 공간과 4D 기하학 재구성이라는 서로 다른 표현 학습 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1794_AGILE_A_Comprehensive_Workflow_for_Humanoid_Loco-Manipulatio/review]] — 휴머노이드 loco-manipulation에서 SLAC의 잠재 행동 공간이 AGILE의 포괄적 워크플로우에 통합될 수 있다.
- 🏛 기반 연구: [[papers/2126_Opt2Skill_Imitating_Dynamically-feasible_Whole-Body_Trajecto/review]] — 동적으로 실행 가능한 궤적 모방에서 잠재 행동 공간과 최적화 기반 접근법이 상호 보완적이다.
- 🔄 다른 접근: [[papers/1652_Robot_Trains_Robot_Automatic_Real-World_Policy_Adaptation_an/review]] — task-agnostic latent space vs robot-guided learning이라는 다른 방식의 실제 환경 적응 접근법입니다.
- 🔗 후속 연구: [[papers/1674_Sim-to-Real_Learning_for_Humanoid_Box_Loco-Manipulation/review]] — 저충실도 시뮬레이션 기반 잠재 공간이 복잡한 접촉 기반 조작 작업으로 확장됩니다.
- 🏛 기반 연구: [[papers/1674_Sim-to-Real_Learning_for_Humanoid_Box_Loco-Manipulation/review]] — 분리된 정책 학습이 전신 조작에서 task-agnostic 잠재 공간 학습의 기초가 됩니다.
- 🔄 다른 접근: [[papers/1652_Robot_Trains_Robot_Automatic_Real-World_Policy_Adaptation_an/review]] — teacher-student 프레임워크를 로봇 팔과 휴머노이드 vs 시뮬레이션과 실제 환경에서 다르게 구현합니다.
- 🔄 다른 접근: [[papers/1751_Visual_Imitation_Enables_Contextual_Humanoid_Control/review]] — real-to-sim-to-real과 simulation-pretrained latent space라는 서로 다른 시뮬레이션-실제 연결 접근법을 사용한다.
- 🔄 다른 접근: [[papers/2016_HUSKY_Humanoid_Skateboarding_System_via_Physics-Aware_Whole-/review]] — 스케이트보드 제어와 전신 잠재 액션 스페이스로 physics-aware 제어의 다른 적용 분야를 보여준다.
