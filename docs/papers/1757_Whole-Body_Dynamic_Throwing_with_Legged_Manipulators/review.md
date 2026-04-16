---
title: "1757_Whole-Body_Dynamic_Throwing_with_Legged_Manipulators"
authors:
  - "Humphrey Munn"
  - "Brendan Tidd"
  - "Peter Böhm"
  - "Marcus Gallagher"
  - "David Howard"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "다리가 있는 로봇의 전신 동역학을 활용하여 강화학습 기반의 3D 목표지점으로의 정확한 투척을 학습하는 방법을 제시하고, 시뮬레이션에서 학습한 정책을 실제 휴머노이드 로봇으로 전이시켰다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Munn et al._2024_Whole-Body Dynamic Throwing with Legged Manipulators.pdf"
---

# Whole-Body Dynamic Throwing with Legged Manipulators

> **저자**: Humphrey Munn, Brendan Tidd, Peter Böhm, Marcus Gallagher, David Howard | **날짜**: 2024-10-08 | **URL**: [https://arxiv.org/abs/2410.05681](https://arxiv.org/abs/2410.05681)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our robot throwing policies demonstrated on real hardware (top) and in simulation (bottom) showing complex full-*

다리가 있는 로봇의 전신 동역학을 활용하여 강화학습 기반의 3D 목표지점으로의 정확한 투척을 학습하는 방법을 제시하고, 시뮬레이션에서 학습한 정책을 실제 휴머노이드 로봇으로 전이시켰다.

## Motivation

- **Known**: 로봇 투척 연구는 주로 고정된 로봇 팔이나 2D 평면 목표에 집중했으며, 최근 일부 연구에서 쿼드러페드의 신체 모멘텀을 활용한 궤적 최적화(trajectory optimization) 기반 접근을 시도했다.
- **Gap**: 기존 연구는 arm-only 설정, 2D 목표 평면 제한, 또는 계산적으로 비효율적인 비학습 방법(trajectory optimization)을 사용하며, 높은 자유도(DoF)의 전신 동역학을 활용하면서 안정성과 투척 성능을 균형있게 최적화하는 방법이 부재하다.
- **Why**: 투척은 긴급 상황에서의 효율적인 물체 운송이나 접근 불가능한 영역으로의 물체 전달 등 실제 응용에서 중요하며, 다리 로봇의 전신 활용은 도달 범위와 투척력을 극대화할 수 있기 때문이다.
- **Approach**: PPO 알고리즘 기반 deep RL을 Isaac Lab에서 학습하며, 투척 정확도와 안정성을 최적화하는 적응형 커리큘럼(adaptive curriculum)을 도입하고, 희소 보상(sparse-reward) 환경에서의 효율적 학습을 위한 맞춤형 RL 환경을 설계했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Throwing error (metres) between robot throw and target for the*

- **3D 투척 일반화**: 2D 평면에 제한되던 기존 연구와 달리 임의의 3D 공간 목표지점으로의 투척을 가능하게 함
- **전신 동역학 활용**: 신체 모멘텀, counter-balancing, 전신 동역학을 활용하여 arm-only 방식 대비 범위, 정확도, 안정성 개선
- **적응형 커리큘럼**: 투척 성능과 안정성 간의 트레이드오프를 동적으로 최적화하는 커리큘럼 임계값 자동 조정 방식 개발
- **다중 로봇 플랫폼 검증**: 휴머노이드(13 DoF)와 쿼드러페드 암(19 DoF) 두 형태에서 우월한 성능 입증
- **Sim2Real 전이**: 시뮬레이션 학습 정책을 실제 휴머노이드 로봇에 성공적으로 전이

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Policy Evaluation and Real-world deployment architecture.*

- Isaac Lab 환경에서 병렬화된 PPO 구현을 활용한 joint-level 제어기 학습
- 극좌표(polar coordinates)로 표현된 3D 투척 목표를 정책 입력으로 제공
- 희소 보상 문제 해결: 투척 거리·정확도와 안정성 보상을 동시에 최적화
- 적응형 커리큘럼: 안정성 보상과 투척 성능 보상의 비중을 학습 진행에 따라 동적 조정
- 고차원 행동 공간(13-19 DoF)에서 비제약 학습으로 복잡한 전신 동작 자동 발견
- Motion capture를 통한 sim2real 전이 검증 및 실제 투척 궤적 측정

## Originality

- **첫 전신 동역학 3D 투척**: arm-only 제약을 벗고 전신 모멘텀과 동역학을 활용한 3D 임의 목표 투척은 선례가 없음
- **맞춤형 적응형 커리큘럼**: loco-manipulation 커리큘럼을 투척 특화로 재설계하여 동적 행동 탐색(jumping 등)을 장려하는 혁신적 접근
- **비제약 전신 학습**: trajectory optimization처럼 움직임을 제약하지 않고 deep RL로 고자유도 전신 조율을 자동으로 학습
- **희소 보상 환경 설계**: 투척의 본질적 희소성(release 시점에만 보상)을 명시적으로 다루는 환경 구성

## Limitation & Further Study

- **실제 로봇 전이 제한**: Sim2Real 전이가 완전하지 않으며 실제 under-actuated 휴머노이드에서 일부 성능 저하 보고
- **안정성-성능 트레이드오프**: 커리큘럼이 균형을 개선하지만 극단적 거리에서 안정성과 정확도 간 근본적 한계 존재 가능
- **도메인 적응 부재**: 실제 환경의 센서 노이즈, 마찰, 공기 저항 등에 대한 강건성 평가 제한적
- **일반화 범위**: 특정 로봇 형태에 대해 학습되었으며 다른 형태(biped, 팔 없는 로봇)로의 일반화 미검증
- **후속 연구 방향**: (1) 현실적 센서 노이즈 및 모델 오차에 대한 강건성 강화, (2) 여러 투척 스타일(underhand, sidearm 등) 학습, (3) 동시 투척과 이동을 연결하는 복합 과제

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 전신 동역학을 활용한 3D 임의 목표 투척이라는 명확한 혁신과 적응형 커리큘럼이라는 기술적 기여로 로봇 조작 연구의 새로운 방향을 제시했으나, 실제 로봇 전이의 완전성 부족과 일반화 범위 제약이 실용적 임팩트를 다소 제한한다.

## Related Papers

- 🔄 다른 접근: [[papers/1759_WoCoCo_Learning_Whole-Body_Humanoid_Control_with_Sequential/review]] — 둘 다 전신 동역학 제어를 다루지만 MPC는 모델 예측 제어, 투척 논문은 강화학습을 사용합니다.
- 🔗 후속 연구: [[papers/2001_Humanoid_Robot_Acrobatics_Utilizing_Complete_Articulated_Rig/review]] — Complete Articulated Rigid Body를 활용한 acrobatics가 동적 투척 기술의 더 복잡한 응용을 보여줍니다.
- 🧪 응용 사례: [[papers/1973_Hierarchical_Planning_and_Control_for_Box_Loco-Manipulation/review]] — 전신 투척 기술이 box loco-manipulation의 물체 던지기 단계에 직접 활용 가능합니다.
- 🔄 다른 접근: [[papers/1759_WoCoCo_Learning_Whole-Body_Humanoid_Control_with_Sequential/review]] — 둘 다 전신 동역학 제어를 다루지만 하나는 MPC, 다른 하나는 RL 기반 투척 제어입니다.
- 🧪 응용 사례: [[papers/2149_TOP_Time_Optimization_Policy_for_Stable_and_Accurate_Standin/review]] — 전신 동적 던지기 제어 기술을 서서하기 조작의 상체 동작 최적화에 실제 적용할 수 있다.
