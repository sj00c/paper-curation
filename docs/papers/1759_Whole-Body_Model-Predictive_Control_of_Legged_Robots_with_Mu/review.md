---
title: "1759_Whole-Body_Model-Predictive_Control_of_Legged_Robots_with_Mu"
authors:
  - "John Z. Zhang"
  - "Taylor A. Howell"
  - "Zeji Yi"
  - "Chaoyi Pan"
  - "Guanya Shi"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "MuJoCo 물리엔진과 iterative LQR (iLQR) 알고리즘을 결합하여 사족 및 인형로봇의 전신 모델예측제어(MPC)를 실시간으로 수행하고, 간단한 방법으로도 현실 세계에 효과적으로 적용 가능함을 입증하는 연구이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Humanoid_Locomotion_and_Control"
  - "sub/Terrain-Adaptive_Humanoid_Locomotion"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Whole-Body Model-Predictive Control of Legged Robots with MuJoCo.pdf"
---

# Whole-Body Model-Predictive Control of Legged Robots with MuJoCo

> **저자**: John Z. Zhang, Taylor A. Howell, Zeji Yi, Chaoyi Pan, Guanya Shi, Guannan Qu, Tom Erez, Yuval Tassa, Zachary Manchester | **날짜**: 2025-03-06 | **URL**: [https://arxiv.org/abs/2503.04613](https://arxiv.org/abs/2503.04613)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

MuJoCo 물리엔진과 iterative LQR (iLQR) 알고리즘을 결합하여 사족 및 인형로봇의 전신 모델예측제어(MPC)를 실시간으로 수행하고, 간단한 방법으로도 현실 세계에 효과적으로 적용 가능함을 입증하는 연구이다.

## Motivation

- **Known**: MPC는 강력한 제어 패러다임이지만 실시간 성능이 요구되는 고자유도 다리로봇 제어에는 복잡한 커스텀 구현이 필요했다. 최근 시뮬레이션 기술과 RL의 발전으로 sim-to-real 성능이 개선되었으나, 모델기반 제어는 여전히 재현성이 낮고 커뮤니티 채택이 느렸다.
- **Gap**: 기존 전신 MPC 방법들은 접촉 역학의 비매끄러운 특성 처리, 해석적 미분 계산, 커스텀 최적화 솔버 개발의 복잡성으로 인해 재현성이 낮고 연구 진입 장벽이 높았다. 표준 시뮬레이터와 간단한 알고리즘으로도 실제 로봇 제어가 가능한지 증명되지 않았다.
- **Why**: 모델기반 제어의 진입 장벽을 낮추고 재현 가능한 오픈소스 baseline을 제공함으로써 커뮤니티 연구 속도를 가속화할 수 있으며, 복잡한 다리로봇 제어 태스크의 실시간 수행 가능성을 입증하는 것이 중요하다.
- **Approach**: MuJoCo 물리엔진의 soft contact 모델과 유한차분 미분 근사를 활용하여 iLQR 알고리즘을 구현하고, time-varying LQR 피드백 정책으로 300-500 Hz 실시간 제어를 달성한다. interactive GUI를 통해 실시간 파라미터 튜닝을 가능하게 하였다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **간단한 baseline 알고리즘 제시**: MuJoCo iLQR을 사용한 단순하면서도 효과적인 전신 MPC 방법으로, 복잡한 커스텀 구현 없이도 real-time 제어 달성
- **다양한 하드웨어 실증**: 사족 동적 보행, 사족 이족보행(handstand), 전신 인형로봇 이족보행 등 여러 과제에서 성공적 적용 입증
- **오픈소스 구현 및 도구 제공**: 코드, 실험 영상, interactive GUI 공개로 재현성 극대화 및 연구 커뮤니티 접근성 향상
- **sim-to-real 유효성 증명**: 모델 불일치(soft contact 모델 vs. 실제 로봇)가 있음에도 불구하고 효과적인 현실 세계 적용 가능성 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- iLQR 알고리즘으로 비선형 궤적 최적화 문제 반복 해결 (식 1)
- MuJoCo의 효율적인 C 구현을 활용한 forward dynamics 및 유한차분 미분 계산
- soft contact 모델로 비매끄러운 접촉 역학 처리
- time-varying LQR 피드백 정책: u_t = ū_t + K_t(x_t - x̄_t) 형태로 50 Hz 계획, 300 Hz 피드백 업데이트
- motion capture와 관성측정장치(IMU), 엔코더 융합을 통한 상태 추정
- joint-level PD 컨트롤러와의 계층적 제어 구조
- Interactive GUI를 통한 실시간 cost weight, goal location, hyperparameter 조정

## Originality

- 유한차분 미분 근사와 표준 물리엔진(MuJoCo)만으로 전신 다리로봇 MPC를 실시간 수행하는 단순성과 효과성의 조화
- 접촉 모드를 명시적으로 지정하지 않으면서도 soft contact 모델로 복잡한 접촉 역학 처리
- interactive GUI를 통한 실시간 파라미터 튜닝으로 사용자 친화적 제어 시스템 구현
- 이족보행처럼 본질적으로 open-loop unstable한 태스크에 derivative-based MPC(iLQR) 적용 성공

## Limitation & Further Study

- Soft contact 모델과 실제 로봇 접촉의 model mismatch가 존재하나 경험적으로 작동 (근본적 원인 분석 부족)
- 유한차분 미분 근사의 수치 안정성 및 정확도 한계에 대한 상세 분석 부재
- MPC 계산 복잡도로 인한 계획 지평(planning horizon) 제약 및 long-horizon 태스크 적용 한계
- 현재 구현이 특정 로봇 플랫폼(Unitree)에 최적화되어 있어 다른 플랫폼으로의 일반화 용이성 불명확
- **후속 연구**: contact mode 자동 선택 메커니즘, 더 정교한 미분 근사 방법 탐색, 동적 모델 불일치 대응 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 복잡한 최적화 이론 대신 표준 도구들의 조합으로 현실 세계 다리로봇 제어를 성공시킨 우수한 실증 연구이며, 공개된 코드와 상세한 구현 정보로 커뮤니티 연구 가속화에 큰 기여할 것으로 기대된다.

## Related Papers

- 🔄 다른 접근: [[papers/1636_Reference-Free_Sampling-Based_Model_Predictive_Control/review]] — iLQR 기반 전신 MPC와 MPPI 기반 샘플링 MPC는 모두 실시간 최적화 제어를 추구하는 상호 보완적인 최적화 알고리즘이다.
- 🏛 기반 연구: [[papers/1628_PyRoki_A_Modular_Toolkit_for_Robot_Kinematic_Optimization/review]] — MuJoCo 기반 실시간 MPC 구현이 PyRoki의 GPU 가속 최적화와 결합되어 더 효율적인 전신 제어가 가능하다.
- 🔄 다른 접근: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — SN 기반 메모리 효율적 학습과 MuJoCo 기반 실시간 MPC는 모두 계산 효율성을 추구하는 상호 보완적 제어 접근법이다.
- 🔄 다른 접근: [[papers/1628_PyRoki_A_Modular_Toolkit_for_Robot_Kinematic_Optimization/review]] — MuJoCo 기반 실시간 전신 MPC와 GPU 가속 역기구학 최적화는 모두 효율적인 휴머노이드 제어를 위한 상호 보완적 접근법이다.
- 🔄 다른 접근: [[papers/1636_Reference-Free_Sampling-Based_Model_Predictive_Control/review]] — MPPI 기반 샘플링 MPC와 iLQR 기반 전신 MPC는 모두 사전 정의된 패턴 없이 실시간 최적화 제어를 추구하는 상호 보완적 방법이다.
- 🏛 기반 연구: [[papers/1784_A_Unified_and_General_Humanoid_Whole-Body_Controller_for_Ver/review]] — 다중 접촉 상황에서의 MPC 기반 전신 제어가 HugWBC의 versatile locomotion 구현에 필요한 기초 이론을 제공한다
