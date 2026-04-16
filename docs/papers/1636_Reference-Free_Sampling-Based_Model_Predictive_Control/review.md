---
title: "1636_Reference-Free_Sampling-Based_Model_Predictive_Control"
authors:
  - "Fabian Schramm"
  - "Pierre Fabre"
  - "Nicolas Perrin-Gilbert"
  - "Justin Carpentier"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 사전정의된 보행 패턴이나 접촉 시퀀스 없이 MPPI 기반의 샘플링 기반 MPC 프레임워크를 제안하여 emergent locomotion을 실현한다. Cubic Hermite spline 파라미터화를 통해 위치와 속도 제어점을 동시에 최적화하여 실시간 CPU 기반 제어를 가능하게 한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Exercise_Learning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Schramm et al._2025_Reference-Free Sampling-Based Model Predictive Control.pdf"
---

# Reference-Free Sampling-Based Model Predictive Control

> **저자**: Fabian Schramm, Pierre Fabre, Nicolas Perrin-Gilbert, Justin Carpentier | **날짜**: 2025-11-24 | **URL**: [https://arxiv.org/abs/2511.19204](https://arxiv.org/abs/2511.19204)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our reference-free sampling-based MPC framework*

본 논문은 사전정의된 보행 패턴이나 접촉 시퀀스 없이 MPPI 기반의 샘플링 기반 MPC 프레임워크를 제안하여 emergent locomotion을 실현한다. Cubic Hermite spline 파라미터화를 통해 위치와 속도 제어점을 동시에 최적화하여 실시간 CPU 기반 제어를 가능하게 한다.

## Motivation

- **Known**: MPPI는 비미분 최적화로 접촉이 많은 시나리오에 적합하며, 최근 DIAL-MPC와 같은 diffusion 기반 annealing 전략이 제안되었다. 하지만 기존 샘플링 기반 MPC 방법들은 Raibert heuristics나 사전정의된 보행 참조에 의존한다.
- **Gap**: 기존 방법들은 참조 보행 패턴이나 사전학습 없이 emergent locomotion을 발견하지 못하며, GPU 가속을 필요로 하거나 샘플 효율이 낮다. 또한 위치만 샘플링하는 기존 접근법은 동적 일관성이 부족하다.
- **Why**: 참조 없는 제어는 새로운 환경이나 작업에 대한 적응성과 일반화 가능성을 향상시키며, CPU 기반 실시간 제어는 로봇 하드웨어 접근성을 높이고 실제 적용 가능성을 증대시킨다.
- **Approach**: 본 논문은 cubic Hermite spline을 사용하여 위치와 속도 제어점을 동시에 샘플링하고, diffusion 기반 noise annealing 스케줄을 적용하며, PD 컨트롤러를 통해 추적한다. 고수준 목표에 기반한 참조 없는 비용 함수로 emergent 움직임을 발현시킨다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Sequence illustrating the discovered walking gait on the Go2 quadruped.*

- **실시간 CPU 기반 제어**: 30개 샘플만으로 50 Hz 제어 주기를 달성하여 GPU 가속 제거
- **Emergent locomotion 발현**: 트로팅, 갤로핑, 수직 자세 유지, 점프 등 다양한 보행 패턴을 참조 없이 자동 발견
- **복잡한 행동 생성**: 백플립, 동적 악수(handstand) 밸런싱, 휴머노이드 보행 등 오프라인 사전학습 없이 시뮬레이션에서 구현
- **실제 로봇 검증**: Go2 사족보행 로봇에서 점프 0.55m 높이 달성 및 다양한 보행 패턴 실증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Comparison of spline parameterizations for the same*

- Cubic Hermite spline 파라미터화: 각 노드에서 위치 θ^q_k와 속도 θ^v_k를 제어 변수로 설정하여 동적 일관성 강화
- MPPI 프레임워크: 현재 시퀀스에 Gaussian noise를 가하고 비용 평가 후 importance-weighted 평균으로 업데이트
- Diffusion 기반 annealing: 초기 반복에서 광범위 탐색을 수행하고 후기로 갈수록 세밀한 정제를 진행
- PD 컨트롤러 추적: 샘플링된 위치와 속도 참조를 PD 컨트롤러로 추적하여 토크 명령 생성
- 참조 없는 비용 함수: 위상 시계나 에어타임 페널티 대신 고수준 목표(속도, 높이 등)만을 비용에 반영
- 상태 예측 및 warm-starting: 최적화 단계 간 시간 일관성 유지로 안정성과 수렴성 향상
- Joint limit 제약: 노드 미분을 경계까지의 거리에 따라 제한하여 overshoot 방지

## Originality

- 위치와 속도 제어점을 동시에 샘플링하는 cubic Hermite spline 도입으로 기존 위치 전용 파라미터화 대비 탐색 공간 확장
- 참조 보행이나 사전정의된 접촉 시퀀스 완전 제거로 순수 고수준 목표 기반 emergent 행동 발현
- 30개 샘플로 실시간 CPU 기반 제어 달성하는 극도의 샘플 효율성 (기존 DIAL-MPC: 2048-4096 샘플)
- Contact-making/breaking 전략의 자동 적응으로 hand-crafted 접촉 규칙 제거

## Limitation & Further Study

- 현실 로봇에서는 점프만 검증되고 트로팅/갤로핑 등은 주로 시뮬레이션 결과이므로 sim-to-real 갭 존재
- 고수준 비용 함수 설계 여전히 필요하며, 비용 함수 변경에 따른 민감도 분석 부재
- 모든 실험이 정도 높은 물리 시뮬레이터(MuJoCo)에 의존하므로 실제 접촉 역학 오차의 영향 평가 필요
- 더 복잡한 형태(사족보행 이상의 자유도)에 대한 샘플 수 증가 추세 명확화 필요
- 불규칙한 지형이나 동적 장애물이 있는 환경에 대한 성능 평가 부재
- **후속 연구**: 온라인 모델 학습을 통한 동역학 불확실성 처리, 더 긴 수평선에 대한 계산 복잡도 최적화, 다양한 terrain에서의 강건성 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 참조 없는 emergent locomotion 발현, 극도의 샘플 효율성, 그리고 실시간 CPU 제어라는 세 가지 측면에서 우수한 기여를 제시한다. Cubic Hermite spline 파라미터화와 diffusion annealing의 조합은 창의적이며, Go2 로봇의 실제 검증은 신뢰성을 높인다. 다만 현실 로봇 검증의 범위 확대와 sim-to-real 갭 분석이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1759_Whole-Body_Model-Predictive_Control_of_Legged_Robots_with_Mu/review]] — MPPI 기반 샘플링 MPC와 iLQR 기반 전신 MPC는 모두 사전 정의된 패턴 없이 실시간 최적화 제어를 추구하는 상호 보완적 방법이다.
- 🏛 기반 연구: [[papers/1777_A_Gait_Driven_Reinforcement_Learning_Framework_for_Humanoid/review]] — Reference-free MPC 프레임워크가 gait-driven RL의 실시간 gait planner 구성요소에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1622_Predictive_Sampling_Real-time_Behaviour_Synthesis_with_MuJoC/review]] — Reference-Free MPC는 spline 파라미터화 기반을, Predictive Sampling은 간단한 샘플링 기반 MPC를 통해 실시간 제어를 다르게 구현함
- 🔗 후속 연구: [[papers/1938_Full-Order_Sampling-Based_MPC_for_Torque-Level_Locomotion_Co/review]] — Full-Order Sampling-Based MPC의 토크 수준 전신 제어가 본 논문의 emergent locomotion MPC를 더욱 정밀하게 확장함
- 🧪 응용 사례: [[papers/2149_TOP_Time_Optimization_Policy_for_Stable_and_Accurate_Standin/review]] — TOP의 시간 최적화 정책이 본 논문의 reference-free MPC를 안정적이고 정확한 기립 제어에 적용한 사례임
- 🔄 다른 접근: [[papers/1622_Predictive_Sampling_Real-time_Behaviour_Synthesis_with_MuJoC/review]] — 두 논문 모두 sampling-based MPC를 사용하지만, Predictive Sampling은 간단한 샘플링을, Reference-Free는 spline 파라미터화를 통한 최적화를 제안함
- 🔄 다른 접근: [[papers/1759_Whole-Body_Model-Predictive_Control_of_Legged_Robots_with_Mu/review]] — iLQR 기반 전신 MPC와 MPPI 기반 샘플링 MPC는 모두 실시간 최적화 제어를 추구하는 상호 보완적인 최적화 알고리즘이다.
- 🏛 기반 연구: [[papers/1759_WoCoCo_Learning_Whole-Body_Humanoid_Control_with_Sequential/review]] — Reference-Free MPC 방법론이 MuJoCo 기반 전신 제어의 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1855_Cost-Matching_Model_Predictive_Control_for_Efficient_Reinfor/review]] — reference-free sampling 기반 MPC가 Cost-Matching MPC의 반복적 해결 부담을 제거하는 효율적인 기초 방법론을 제공한다
- 🧪 응용 사례: [[papers/1777_A_Gait_Driven_Reinforcement_Learning_Framework_for_Humanoid/review]] — Gait-driven RL의 실시간 보행 계획이 reference-free MPC 프레임워크에서 emergent locomotion 생성에 직접 활용된다.
- 🔗 후속 연구: [[papers/1897_Ego-Vision_World_Model_for_Humanoid_Contact_Planning/review]] — reference-free sampling-based MPC가 ego-vision world model의 contact planning을 더 자유로운 제어 방식으로 확장한다.
- 🏛 기반 연구: [[papers/1938_Full-Order_Sampling-Based_MPC_for_Torque-Level_Locomotion_Co/review]] — reference-free sampling-based MPC의 이론적 기반이 DIAL-MPC의 training-free 접근법에 도움이 된다.
- 🔄 다른 접근: [[papers/2049_Learning_Differentiable_Reachability_Maps_for_Optimization-b/review]] — 미분 가능한 도달성 맵과 참조 자유 샘플링 기반 모델 예측 제어는 모두 최적화 기반 제어이지만 서로 다른 접근법을 사용한다.
