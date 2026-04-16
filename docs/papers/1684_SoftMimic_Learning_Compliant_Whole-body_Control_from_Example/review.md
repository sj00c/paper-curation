---
title: "1684_SoftMimic_Learning_Compliant_Whole-body_Control_from_Example"
authors:
  - "Gabriel B. Margolis"
  - "Michelle Wang"
  - "Nolan Fey"
  - "Pulkit Agrawal"
date: "2025.10"
doi: "10.48550/arXiv.2510.17792"
arxiv: ""
score: 4.0
essence: "SoftMimic은 역기구학 솔버를 이용해 순응적 동작 데이터셋을 생성하고 강화학습으로 학습하여, 인간형 로봇이 외부 힘에 순응하면서도 균형을 유지하는 제어 정책을 학습하는 프레임워크이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Margolis et al._2025_SoftMimic Learning Compliant Whole-body Control from Examples.pdf"
---

# SoftMimic: Learning Compliant Whole-body Control from Examples

> **저자**: Gabriel B. Margolis, Michelle Wang, Nolan Fey, Pulkit Agrawal | **날짜**: 2025-10-20 | **DOI**: [10.48550/arXiv.2510.17792](https://doi.org/10.48550/arXiv.2510.17792)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Soft Whole-body Control via Compliant Motion Augmentation. Left: Given an original reference motion (qref) and a*

SoftMimic은 역기구학 솔버를 이용해 순응적 동작 데이터셋을 생성하고 강화학습으로 학습하여, 인간형 로봇이 외부 힘에 순응하면서도 균형을 유지하는 제어 정책을 학습하는 프레임워크이다.

## Motivation

- **Known**: 강화학습을 통한 인간형 로봇의 동작 모방은 빠른 학습을 가능하게 하지만, 기존 방법들은 강체적 제어를 유도하여 예상치 못한 접촉 시 깨지기 쉽고 위험한 거동을 초래한다.
- **Gap**: 고자유도 인간형 로봇에서 전신 균형을 유지하면서 순응적 거동을 학습하는 것은 탐색 문제와 비용 함수의 상충으로 인해 도전적이며, 기존 RL 접근법은 직접적으로 이를 발견하기 어렵다.
- **Why**: 실제 배포 환경에서는 예상치 못한 접촉과 외부 힘이 빈번하게 발생하므로, 순응성 있는 제어는 안전성과 로봇-인간 협업 가능성을 근본적으로 향상시킨다.
- **Approach**: 오프라인 단계에서 IK 솔버를 이용해 다양한 상호작용 시나리오에 대한 운동학적으로 실행 가능한 순응 궤적 데이터셋을 생성하고, RL 정책이 원본 참조 동작을 관찰하면서 증강된 순응 목표를 추적하도록 학습시킨다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Stiffness adherence. The humanoid’s effective translational*

- **자동 데이터 생성**: IK 솔버를 통해 광범위한 상호작용 시나리오에서 운동학적으로 가능하고 스타일이 일관된 순응 궤적을 자동으로 생성
- **순응성 제어 학습**: 정책이 외부 힘을 고유감각으로부터 추론하고 사전계산된 순응 거동으로 반응하도록 암묵적으로 학습
- **강건성 및 일반화**: 단일 동작 클립으로부터 다양한 작업 변동(상자 크기 등)에 적응하고, 예상치 못한 충돌을 안전하게 관리
- **배포 시간 경직도 제어**: 배포 시 사용자가 지정한 경직도 입력으로 원하는 힘-변위 관계를 조절
- **실제 로봇 검증**: Unitree G1 인간형 로봇 실험으로 시뮬레이션과 실제 환경 간 유효성 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Soft Whole-body Control via Compliant Motion Augmentation. Left: Given an original reference motion (qref) and a*

- 참조 동작(q_ref), 외부 wrench(W_ext), 로봇 경직도(K_robot)가 주어졌을 때 IK 솔버를 사용하여 운동학적으로 실행 가능한 순응 동작(q_aug) 생성
- 생성된 순응 궤적 데이터셋으로 강화학습 정책 훈련—정책은 원본 참조를 입력받지만 증강된 순응 목표에 대한 추적 보상 수신
- 이 공식화는 정책이 자신의 고유감각 상태로부터 외부 힘을 암묵적으로 추론하고 적절히 반응하도록 강제
- PD 제어기를 통한 위치 목표 설정점 변조로 다양한 경직도 범위를 신경망 정책으로 표현
- 오프라인 단계에서 불가능한 작업을 필터링하여 RL 훈련 중 불가능한 작업 학습 회피

## Originality

- IK 솔버를 활용한 증강 데이터 생성과 RL 훈련을 결합한 새로운 학습-예제 전략으로, 직접적 RL 탐색의 비효율성 극복
- 순응 거동을 고정된 참조 대신 동적으로 생성된 증강 참조로 정의함으로써, 신경망 정책이 암묵적으로 힘을 추론하고 반응하도록 유도하는 혁신적 접근
- 배포 시간 경직도 조절 매커니즘으로 단일 정책이 광범위한 경직도를 구현할 수 있도록 설계
- 전신 균형 및 자세 유지를 고려한 인간형 로봇 순응 제어의 첫 번째 학습 기반 통합 솔루션

## Limitation & Further Study

- IK 솔버 기반 데이터 생성은 계산 비용이 높을 수 있으며, 참조 동작의 운동학적 실행 불가능 시나리오 처리 방식이 명확하지 않음
- 실험은 주로 Unitree G1 단일 플랫폼에서 검증되었으므로 다른 인간형 로봇으로의 일반화 가능성 미흡
- 외부 힘의 크기와 방향이 명시적으로 주어지지 않고 고유감각으로만 추론되므로, 극단적인 힘 시나리오에서의 성능 한계 미검증
- 후속 연구: 더 정교한 힘 추론 메커니즘, 다양한 로봇 플랫폼에 대한 확장성 검증, 시각 정보 통합을 통한 적응성 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SoftMimic은 역기구학 기반 데이터 증강과 강화학습을 창의적으로 결합하여 인간형 로봇의 순응적 제어라는 중요한 문제를 체계적으로 해결하며, 이론과 실제 로봇 실험으로 그 효과를 입증한 우수한 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1953_GentleHumanoid_Learning_Upper-body_Compliance_for_Contact-ri/review]] — 두 논문 모두 순응적 제어를 다루지만, 전신 순응성과 상체 컴플라이언스라는 다른 적용 범위를 가진다.
- 🏛 기반 연구: [[papers/1836_CHIP_Adaptive_Compliance_for_Humanoid_Control_through_Hindsi/review]] — 힌드사이트를 통한 적응적 컴플라이언스 제어의 기초 개념을 제공한다.
- 🔗 후속 연구: [[papers/2004_Humanoid_Whole-Body_Locomotion_on_Narrow_Terrain_via_Dynamic/review]] — 좁은 지형에서의 휴머노이드 보행을 순응적 전신 제어로 확장하여 더 복잡한 환경에 적용한다.
- 🏛 기반 연구: [[papers/1714_Thor_Towards_Human-Level_Whole-Body_Reactions_for_Intense_Co/review]] — 강한 접촉 상호작용에서 전신 반응을 생성하는 기반 기술을 순응적 제어라는 관점에서 확장하여 외부 힘에 대한 적응을 구현했다.
- 🔄 다른 접근: [[papers/1691_Stabilizing_Humanoid_Robot_Trajectory_Generation_via_Physics/review]] — 휴머노이드의 안정적 제어를 위해 서로 다른 접근(순응적 동작 생성 vs 물리 기반 궤적 보정)을 통해 물리 법칙과 안정성을 보장한다.
- 🔗 후속 연구: [[papers/1694_SteadyTray_Learning_Object_Balancing_Tasks_in_Humanoid_Tray/review]] — 외부 힘에 순응하는 제어 개념을 동적 보행 중 트레이 운반이라는 구체적 작업으로 확장하여 물체 균형 유지를 실현했다.
- 🧪 응용 사례: [[papers/1982_Hold_My_Beer_Learning_Gentle_Humanoid_Locomotion_and_End-Eff/review]] — 순응적 전신 제어 기술을 실제 음료 운반과 같은 섬세한 조작 작업에 적용하여 부드러운 이동과 종단점 제어를 달성했다.
- 🔄 다른 접근: [[papers/1691_Stabilizing_Humanoid_Robot_Trajectory_Generation_via_Physics/review]] — 휴머노이드의 안정적 제어를 위해 서로 다른 접근(물리 기반 궤적 보정 vs 순응적 동작 생성)을 통해 물리 법칙과 안정성을 보장한다.
- 🔗 후속 연구: [[papers/1694_SteadyTray_Learning_Object_Balancing_Tasks_in_Humanoid_Tray/review]] — 순응적 전신 제어의 개념을 동적 보행 중 트레이 운반이라는 구체적 작업으로 확장하여 불안정한 물체의 안정적 운반을 실현했다.
- 🏛 기반 연구: [[papers/1714_Thor_Towards_Human-Level_Whole-Body_Reactions_for_Intense_Co/review]] — 순응적 전신 제어의 기반 기술을 강한 접촉 상호작용 환경으로 확장하여 인간 수준의 전신 반응을 생성하는 프레임워크로 발전시켰다.
- 🏛 기반 연구: [[papers/1836_CHIP_Adaptive_Compliance_for_Humanoid_Control_through_Hindsi/review]] — SoftMimic의 compliant control 학습과 CHIP의 adaptive compliance가 모두 물리적 상호작용에서의 유연성 확보라는 공통 목표를 가진다.
- 🔄 다른 접근: [[papers/1953_GentleHumanoid_Learning_Upper-body_Compliance_for_Contact-ri/review]] — 둘 다 compliant whole-body control을 다루지만, GentleHumanoid는 impedance control 통합에, SoftMimic은 example 기반 compliance learning에 집중합니다.
