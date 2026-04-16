---
title: "1710_The_invariant_extended_Kalman_filter_as_a_stable_observer"
authors:
  - "Axel Barrau"
  - "Silvère Bonnabel"
date: "2014.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Invariant Extended Kalman Filter (IEKF)를 Lie group 위의 결정론적 비선형 관찰자로 분석하여, 표준 선형 조건 하에서 임의의 궤적 주변에서의 국소 안정성을 증명한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/Humanoid_Exercise_Learning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Barrau and Bonnabel_2014_The invariant extended Kalman filter as a stable observer.pdf"
---

# The invariant extended Kalman filter as a stable observer

> **저자**: Axel Barrau, Silvère Bonnabel | **날짜**: 2014-10-06 | **URL**: [https://arxiv.org/abs/1410.1465](https://arxiv.org/abs/1410.1465)

---

## Essence


Invariant Extended Kalman Filter (IEKF)를 Lie group 위의 결정론적 비선형 관찰자로 분석하여, 표준 선형 조건 하에서 임의의 궤적 주변에서의 국소 안정성을 증명한다.

## Motivation

- **Known**: EKF는 공학에서 가장 인기 있는 관찰자이지만 최적성 보장이 없으며, 추정 오차가 클 때 선형화 가정이 위반되어 발산할 수 있다는 것이 알려져 있다.
- **Gap**: 비선형 시스템의 관찰자 설계는 linearized error equation이 미지의 참 상태에 의존하기 때문에 어렵고, 대부분의 EKF 안정성 논문들은 Kalman 공분산 행렬의 고유값이 양의 스칼라로 상하한을 갖는다는 강한 가정을 필요로 한다.
- **Why**: Navigation과 robotics 응용에서 신뢰할 수 있는 관찰자 이론이 필수적이며, 특히 IEKF의 우수한 실제 성능에 대한 이론적 근거를 제공하는 것이 중요하다.
- **Approach**: Lie group 위의 곱셈형 시스템 클래스를 특성화하여 error equation의 자율성(autonomy)을 보이고, 이를 바탕으로 IEKF의 수렴성을 증명한다.

## Achievement


- **승법 시스템 클래스 완전 특성화**: left-invariant 시스템보다 훨씬 광범위한 시스템 클래스에서 상태 error equation의 자율성이 성립함을 증명
- **선형 오차 진화 성질**: 적절한 비선형 변환을 통해 비선형 error가 선형 미분방정식을 따르는 성질 발견
- **IEKF의 수렴성 보장**: 표준 선형 조건을 적용하면 IEKF가 임의의 궤적 주변에서 점근 관찰자임을 증명
- **응용 사례 검증**: mobile robotics (unicycle)과 UAV inertial navigation 예제에서 IEKF 수렴성 증명 및 EKF 우월성 실증

## How


- Lie group G에서의 dynamics를 고려하고 두 궤적 χ_t와 ¯χ_t의 left/right invariant error 정의
- 비선형 오차 함수 ξ_t를 구성하여 이것이 선형 자율 미분방정식 dξ_t/dt = A_t ξ_t를 만족함을 보임
- Continuous-time dynamics와 discrete observations를 결합한 IEKF 공식화
- Riccati 방정식의 해의 상하한 조건을 기반으로 오차의 점근 수렴성 증명
- Mobile robotics와 UAV navigation의 구체적 시스템에 대해 framework 적용 가능성 검증

## Originality

- Left-invariant 시스템 이상의 광범위한 승법 시스템 클래스 도입 및 완전한 특성화
- 비선형 시스템에서 선형 error evolution 성질이 존재함을 발견한 기하학적 통찰
- Continuous-time dynamics와 discrete observations 결합에서의 IEKF 수렴성 증명이 선행 연구에 없음
- EKF의 강한 수렴 조건을 제거하고 표준 선형 조건만으로 수렴을 보장하는 첫 결과

## Limitation & Further Study

- 국소(local) 수렴만 증명되었으며, 초기 조건이 충분히 참 상태에 가까워야 함
- Continuous-time model과 discrete observations의 조합에 한정되어 완전 discrete 시스템 미포함
- 측정값에 노이즈가 있을 때의 robust convergence 분석 미흡
- 더 복잡한 비선형 시스템(예: 고도의 비홀로노믹 시스템)에 대한 확장성 검토 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 IEKF의 수렴성을 엄밀히 증명하고 일반적인 시스템 클래스를 특성화함으로써 비선형 관찰자 이론에 중요한 기여를 하며, navigation 응용에서의 우수한 실제 성능을 이론적으로 정당화한다.

## Related Papers

- 🧪 응용 사례: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — IEKF의 안정성 분석에 필요한 Lie group 상의 조건들이 Spectral Normalization의 Lipschitz 제약과 수학적으로 연관되어 상호 보완한다.
- 🏛 기반 연구: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — IEKF의 비선형 관찰자 이론이 도어 통과와 같은 복잡한 행동에서 상태 추정의 안정성을 보장하는 기반을 제공한다.
- 🔗 후속 연구: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — IEKF의 안정적 상태 추정 이론이 PolygMap의 멀티모달 센서 융합 시스템에 수학적으로 견고한 기반을 제공한다
- 🏛 기반 연구: [[papers/1849_Contact-Aided_Invariant_Extended_Kalman_Filtering_for_Robot/review]] — Contact-Aided IEKF가 기본 IEKF 이론을 접촉 상황으로 확장한 발전된 형태이다
- 🔄 다른 접근: [[papers/2023_InEKFormer_A_Hybrid_State_Estimator_for_Humanoid_Robots/review]] — 둘 다 휴머노이드 상태 추정을 다루지만 IEKF는 전통적 필터링에, InEKFormer는 하이브리드 학습 접근을 사용한다
- 🏛 기반 연구: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — Spectral Normalization의 Lipschitz 연속성 보장이 IEKF의 안정성 분석에서 요구되는 수학적 조건과 이론적으로 연관된다.
- 🏛 기반 연구: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — IEKF의 안정적인 상태 추정 이론이 PolygMap의 LiDAR-RGB-D-IMU 센서 융합 시스템의 수학적 기반을 제공한다
- 🔄 다른 접근: [[papers/1834_Chasing_Stability_Humanoid_Running_via_Control_Lyapunov_Func/review]] — 휴머노이드의 안정성을 Control Lyapunov Function과 Invariant Extended Kalman Filter라는 서로 다른 수학적 도구로 보장한다
- 🔄 다른 접근: [[papers/1849_Contact-Aided_Invariant_Extended_Kalman_Filtering_for_Robot/review]] — 둘 다 불변 확장 칼만 필터를 다루지만 접촉 보조 상태 추정과 안정한 관찰자라는 서로 다른 응용 관점을 제시한다
- 🧪 응용 사례: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — 복잡한 도어 통과 행동에서 IEKF의 안정적인 상태 추정이 GPU 가속 인식과 전신 제어의 신뢰성을 보장한다.
- 🏛 기반 연구: [[papers/2023_InEKFormer_A_Hybrid_State_Estimator_for_Humanoid_Robots/review]] — 불변 확장 칼만 필터의 안정적 관찰자 특성이 InEKFormer의 하이브리드 상태 추정 기반을 제공한다.
- 🏛 기반 연구: [[papers/2078_Legged_Robot_State-Estimation_Through_Combined_Forward_Kinem/review]] — The invariant extended Kalman filter가 Legged Robot State-Estimation의 Factor Graph에 통합된 Preintegrated Contact 인수 개발의 이론적 기반을 제공한다.
