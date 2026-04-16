---
title: "2043_Learning_Adaptive_Neural_Teleoperation_for_Humanoid_Robots_F"
authors:
  - "Sanjar Atamuradov"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "VR 텔레오퍼레이션에서 전통적인 IK+PD 파이프라인을 RL 기반 신경망 정책으로 대체하여 힘 적응, 궤적 부드러움, 사용자 적응을 동시에 달성하는 학습 기반 프레임워크를 제안한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Atamuradov_2025_Learning Adaptive Neural Teleoperation for Humanoid Robots From Inverse Kinematics to End-to-End Co.pdf"
---

# Learning Adaptive Neural Teleoperation for Humanoid Robots: From Inverse Kinematics to End-to-End Control

> **저자**: Sanjar Atamuradov | **날짜**: 2025-11-15 | **URL**: [https://arxiv.org/abs/2511.12390](https://arxiv.org/abs/2511.12390)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Neural teleoperation policy architecture. The network takes VR controller poses (14-dim), joint states (28-*

VR 텔레오퍼레이션에서 전통적인 IK+PD 파이프라인을 RL 기반 신경망 정책으로 대체하여 힘 적응, 궤적 부드러움, 사용자 적응을 동시에 달성하는 학습 기반 프레임워크를 제안한다.

## Motivation

- **Known**: VR 텔레오퍼레이션은 복잡한 조작 작업에 유망한 접근법이며, RL 기반 로봇 제어는 동역학 처리와 외란 적응에서 성공을 거두었다.
- **Gap**: 기존 IK+PD 파이프라인은 외부 힘 처리 불가, 사용자 적응 불능, 운동 인공물 발생 등의 근본적 한계가 있으며, 실시간 텔레오퍼레이션에 적합한 학습 기반 방법은 부족하다.
- **Why**: 자연스럽고 견고한 휴머노이드 로봇 텔레오퍼레이션은 창고 물류, 재해 대응, 우주 탐사 등 실제 응용에 필수적이며, 학습 기반 접근은 성능과 적응성을 크게 향상시킬 수 있다.
- **Approach**: IK 시연으로부터의 모방 학습 초기화, 부드러움과 힘 강건성을 위한 PPO 기반 RL 미세조정, 그리고 외부 힘 교과학습을 통해 VR 입력에서 로봇 관절 명령으로의 end-to-end 신경망 정책을 학습한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3 provides a detailed breakdown of performance*

- **추적 오차 감소**: IK 기선 대비 34% 더 낮은 추적 오차 달성
- **궤적 부드러움**: 45% 더 부드러운 모션으로 에너지 효율성 및 기계 마모 감소
- **힘 적응**: 외부 힘에 대한 암묵적 보상으로 IK 기선 대비 우월한 힘 적응 성능
- **실시간 성능**: 50Hz 제어 주파수 유지로 배포 가능성 입증
- **다양한 작업**: pick-and-place, door opening, 양팔 조정 등 복잡한 조작 작업 검증

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Neural teleoperation policy architecture. The network takes VR controller poses (14-dim), joint states (28-*

- VR 입력 인코더: 초기 그립 자세 대비 상대 변환으로 VR 좌표계 불변성 확보
- 고유감각 인코더: 로봇 상태(관절 위치, 속도, 이전 액션)를 5 타임스텝 이력과 함께 MLP로 인코딩
- LSTM 정책 헤드: VR 입력과 고유감각을 결합하여 시간적 일관성 및 평활한 궤적 생성
- 단계 1 모방 학습: IK 시연 데이터셋으로 behavioral cloning으로 초기화
- 단계 2 PPO 미세조정: tracking reward, smoothness reward(가속도 및 jerk 페널티), energy regularization 조합
- 단계 3 힘 적응 교과학습: 외부 힘 크기를 점진적으로 증가시키며 고유감각 기반 암묵적 보상 학습
- Sim-to-Real 전이: dynamics randomization(질량 ±10%)으로 시뮬레이션 갭 극복

## Originality

- VR 텔레오퍼레이션 분야에서 IK+PD 파이프라인을 완전히 대체하는 end-to-end 신경망 정책 제시
- 모방 학습과 RL 미세조정의 계층적 결합으로 데이터 효율성과 성능 동시 달성
- 힘 교과학습을 통한 암묵적 힘 적응 메커니즘으로 힘 센서나 haptic 피드백 없이 강건성 확보
- 상대 좌표 인코딩으로 VR 좌표계 프레임 불변성 확보하여 배포 일반화 개선

## Limitation & Further Study

- 시뮬레이션 중심 검증으로 실제 Unitree G1 실험 결과 제시가 제한적임
- 신경망 정책의 해석성 부족으로 긴급 상황 대응이나 safety guarantee 어려움
- LSTM 의존성으로 인한 메모리 상태 누적 오류 가능성 미분석
- VR 사용자의 다양한 조작 스타일에 대한 적응 정도 정량화 부족
- 후속 연구로 safety-critical 작업을 위한 제약 조건부 RL, 다중 사용자 선호도 학습, 정책 설명가능성 개선이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 학습 기반 신경망 정책으로 VR 텔레오퍼레이션의 근본적 한계를 해결하고 명확한 성능 향상을 보여주는 실질적으로 가치 있는 연구이며, 모방 학습과 교과 학습의 조합 설계가 우수하다.

## Related Papers

- 🔄 다른 접근: [[papers/1921_ExtremControl_Low-Latency_Humanoid_Teleoperation_with_Direct/review]] — 휴머노이드 텔레오퍼레이션에서 RL 기반 신경망 정책 대신 저지연 직접 제어 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1707_Teleoperation_of_Humanoid_Robots_A_Survey/review]] — 휴머노이드 로봇 텔레오퍼레이션에 대한 포괄적인 이론적 배경과 기술적 현황을 제공한다.
- 🔗 후속 연구: [[papers/1839_CLONE_Closed-Loop_Whole-Body_Humanoid_Teleoperation_for_Long/review]] — 적응형 신경 텔레오퍼레이션을 폐쇄 루프 전신 제어와 결합하여 장기간 안정적인 원격 조작 시스템을 구현할 수 있다.
- 🔗 후속 연구: [[papers/1756_Whole-Body_Bilateral_Teleoperation_with_Multi-Stage_Object_P/review]] — Learning Adaptive의 적응형 신경 텔레오퍼레이션이 전신 양측 텔레오퍼레이션의 다단계 객체 처리와 결합되어 더 정교한 조작 가능
- 🏛 기반 연구: [[papers/1977_High-Speed_and_Impact_Resilient_Teleoperation_of_Humanoid_Ro/review]] — 고속 충격 내성 텔레오퍼레이션이 Learning Adaptive의 적응형 신경 제어에 동적 환경에서의 견고성 기반 제공
- 🔄 다른 접근: [[papers/1652_Robot_Trains_Robot_Automatic_Real-World_Policy_Adaptation_an/review]] — RTR은 로봇-로봇 협력 학습을, Learning Adaptive Neural Teleoperation은 인간-로봇 원격조작을 통해 휴머노이드 학습을 다르게 지원함
- 🔄 다른 접근: [[papers/1775_A_Closed-Form_Geometric_Retargeting_Solver_for_Upper_Body_Hu/review]] — 둘 다 humanoid teleoperation을 위한 수학적 솔버를 제공하지만 adaptive neural vs closed-form geometric 접근법이 다릅니다.
- 🔗 후속 연구: [[papers/1866_Development_of_an_Intuitive_GUI_for_Non-Expert_Teleoperation/review]] — 비전문가용 GUI가 적응형 신경 텔레오퍼레이션으로 발전하여 사용자 친화성과 지능형 보조 기능을 결합한 더 고도화된 인터페이스를 구현한다.
