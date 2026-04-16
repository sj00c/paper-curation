---
title: "1715_ToddlerBot_Open-Source_ML-Compatible_Humanoid_Platform_for_L"
authors:
  - "Haochen Shi"
  - "Weizhuo Wang"
  - "Shuran Song"
  - "C. Karen Liu"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "ToddlerBot은 머신러닝 기반 로봇 정책 학습을 위해 설계된 저비용, 오픈소스 미니어처 인형로봇으로, 시뮬레이션과 실제 환경 모두에서 고품질 데이터 수집을 가능하게 하며 zero-shot sim-to-real 정책 전이를 지원한다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Portable_Humanoid_Teleoperation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shi et al._2025_ToddlerBot Open-Source ML-Compatible Humanoid Platform for Loco-Manipulation.pdf"
---

# ToddlerBot: Open-Source ML-Compatible Humanoid Platform for Loco-Manipulation

> **저자**: Haochen Shi, Weizhuo Wang, Shuran Song, C. Karen Liu | **날짜**: 2025-02-02 | **URL**: [https://arxiv.org/abs/2502.00893](https://arxiv.org/abs/2502.00893)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: ToddlerBot is an open-source humanoid platform for large-scale, high-quality data collec-*

ToddlerBot은 머신러닝 기반 로봇 정책 학습을 위해 설계된 저비용, 오픈소스 미니어처 인형로봇으로, 시뮬레이션과 실제 환경 모두에서 고품질 데이터 수집을 가능하게 하며 zero-shot sim-to-real 정책 전이를 지원한다.

## Motivation

- **Known**: 기존 휴머노이드 로봇들은 높은 비용과 복잡한 유지보수로 인해 연구 접근성이 낮으며, 시뮬레이션-실제 환경 간 정책 전이가 어렵다는 것이 알려져 있다.
- **Gap**: 기존 미니어처 휴머노이드들은 자유도가 제한적이어서 조작과 이동을 모두 수행하기 어렵고, ML 기반 정책 학습에 필요한 양질의 시뮬레이션-실제 데이터 수집 기능이 부족하다.
- **Why**: 스케일 가능한 머신러닝 기반 로봇 정책 학습을 위해서는 비용 효율적이면서도 높은 정확도의 digital twin을 갖춘 플랫폼이 필수이며, 이는 로봇공학 연구의 민주화와 재현성 향상에 중요하다.
- **Approach**: plug-and-play zero-point calibration과 transferable motor system identification을 통해 high-fidelity digital twin을 구축하고, 직관적인 teleoperation 인터페이스로 whole-body 제어 및 데이터 수집을 가능하게 했으며, 3D-printed와 상용 부품만으로 6,000 USD 이하의 저비용 설계를 실현했다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Experiment Results. We present four different tasks: push-up, pull-up, bimanual, and*

- **30 DoF 미니어처 휴머노이드**: 기존 미니어처 휴머노이드 중 가장 많은 자유도를 갖추어 loco-manipulation 연구에 최적화
- **Zero-shot Sim-to-Real 정책 전이**: 정확한 system identification과 digital twin을 통해 시뮬레이션에서 학습한 정책을 실제 환경에 직접 적용 가능
- **양질의 데이터 수집 플랫폼**: 시뮬레이션 데이터와 human demonstration 기반 실제 데이터를 모두 효율적으로 수집 가능
- **완전한 재현성**: 3D-printed 설계와 상용 부품으로 구성되어 기본 기술 지식만으로 독립적 구축 가능 (CS 학생의 독립 복제 성공 및 5개 팀의 글로벌 복제 보고)
- **강력한 계산 능력**: CUDA accelerator를 탑재하여 시각과 이동 정책의 동시 추론 지원
- **다양한 loco-manipulation 작업 시연**: push-up, pull-up, wagon pushing, bimanual manipulation 등의 작업과 두 로봇의 협력 작업(toy tidying) 성공적 수행

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Mechatronic Design. Orange markers highlights ToddlerBot’s 30 active DoFs: 7 per arm,*

- **System Identification Pipeline**: 모터의 정확한 특성을 파악하여 시뮬레이션 모델의 충실도 향상
- **Zero-point Calibration**: plug-and-play 방식의 캘리브레이션으로 신속한 시스템 설정 가능
- **Whole-body Teleoperation Interface**: 상하체를 동시에 제어할 수 있는 직관적 인터페이스로 human demonstration 데이터 수집
- **Keyframe-interpolated Motion & RL Policy**: 키프레임 보간 운동과 reinforcement learning 정책으로 다양한 행동 학습
- **Anthropomorphic Design**: 인간과 유사한 신체 구조(30 DoF)로 human demonstration 활용 극대화
- **Compact & Safe Design**: 0.56m, 3.4kg의 소형 경량 설계로 일반 환경에서 안전 운용

## Originality

- **첫 30 DoF 미니어처 휴머노이드**: 기존 미니어처 로봇들의 자유도 제약을 극복하여 superhuman range of motion 달성
- **ML-centric 설계 철학**: 정책 학습과 데이터 수집을 핵심 목표로 하는 새로운 로봇 설계 패러다임 제시
- **통합적 재현성 검증**: 독립적 복제와 글로벌 커뮤니티의 복제를 통한 체계적 재현성 입증
- **전이 가능한 System Identification**: 여러 로봇 인스턴스 간 정책의 zero-shot 전이 성공
- **포괄적 오픈소스 공개**: hardware design, digital twin, learning algorithms, tutorials을 모두 공개하여 접근성 극대화

## Limitation & Further Study

- **탑재 용량 제한**: 미니어처 크기로 인해 full-size 휴머노이드 대비 낮은 payload 용량 (인간 규모 객체 조작 불가)
- **확장성 검증 부족**: 대규모 데이터셋에서의 정책 학습 성공 사례가 제시되지 않음
- **동역학적 복잡성**: push-up, pull-up 같은 고난도 동역학 작업에서 더 정교한 제어 알고리즘 필요성 미해결
- **실시간 계산 성능**: onboard compute (2.50 TFLOPS)의 한계로 복잡한 vision-based policy의 온보드 실행 제약
- **후속 연구 제안**: (1) 대규모 reinforcement learning으로 long-horizon loco-manipulation skill 학습, (2) 다양한 embodiment 간의 정책 일반화 연구, (3) 인간 demonstration으로부터 효율적인 학습 방법론 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ToddlerBot은 ML-compatible 설계, 높은 자유도, 완벽한 재현성, 그리고 저비용이라는 독특한 조합으로 로봇공학 연구를 민주화하는 중요한 플랫폼이며, 시뮬레이션-실제 데이터 수집과 정책 학습을 위한 실질적인 도구를 제공한다.

## Related Papers

- 🏛 기반 연구: [[papers/1630_Quasi-Direct_Drive_for_Low-Cost_Compliant_Robotic_Manipulati/review]] — ToddlerBot의 저비용 ML 플랫폼 설계가 Quasi-Direct Drive와 같은 저비용 구동 방식의 실제 적용과 검증에 기반을 제공한다.
- 🧪 응용 사례: [[papers/1707_Teleoperation_of_Humanoid_Robots_A_Survey/review]] — 오픈소스 ML 플랫폼이 텔레오퍼레이션 기술의 접근성 향상과 연구 민주화에 직접적으로 기여한다.
- 🔄 다른 접근: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — Duke Humanoid와 같이 오픈소스 humanoid 플랫폼이지만 ToddlerBot은 미니어처 크기와 ML 호환성에 특화되었습니다.
- 🔄 다른 접근: [[papers/1796_AGILOped_Agile_Open-Source_Humanoid_Robot_for_Research/review]] — 둘 다 저비용 오픈소스 humanoid를 제공하지만 AGILOped는 더 고성능 동적 움직임에 초점을 맞춥니다.
- 🔗 후속 연구: [[papers/2164_TWIST2_Scalable_Portable_and_Holistic_Humanoid_Data_Collecti/review]] — TWIST2의 데이터 수집 시스템이 ToddlerBot의 ML 학습을 위한 고품질 데이터 생성을 지원합니다.
- ⚖️ 반론/비판: [[papers/1778_A_Hierarchical_Model-Based_System_for_High-Performance_Human/review]] — ToddlerBot의 미니어처 설계와 달리 성인용 휴머노이드의 고성능 시스템 통합을 보여줍니다.
- 🏛 기반 연구: [[papers/2006_Humanoid-Gym_Reinforcement_Learning_for_Humanoid_Robot_with/review]] — 시뮬레이션 기반 강화학습 환경을 제공하여 ToddlerBot의 ML 호환성을 지원하는 기반 환경입니다.
- 🔗 후속 연구: [[papers/1707_Teleoperation_of_Humanoid_Robots_A_Survey/review]] — 텔레오퍼레이션 기술 동향이 ToddlerBot과 같은 ML 호환 플랫폼에서 인간-로봇 상호작용 방식의 설계 지침을 제공한다.
- 🔄 다른 접근: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — ToddlerBot과 같이 저비용 오픈소스 humanoid 플랫폼이지만 다른 크기와 용도로 설계되었습니다.
- 🔗 후속 연구: [[papers/1630_Quasi-Direct_Drive_for_Low-Cost_Compliant_Robotic_Manipulati/review]] — 저비용 컴플라이언트 조작 기술이 ToddlerBot과 같은 ML 호환 플랫폼에 적용되어 더 안전한 학습 환경을 제공할 수 있다.
- 🧪 응용 사례: [[papers/1773_A_21-DOF_Humanoid_Dexterous_Hand_with_Hybrid_SMA-Motor_Actua/review]] — 21-DOF 정밀 손 제어 기술이 ToddlerBot과 같은 학습 플랫폼에서 복잡한 조작 스킬 습득에 직접 활용될 수 있다.
- ⚖️ 반론/비판: [[papers/1778_A_Hierarchical_Model-Based_System_for_High-Performance_Human/review]] — 성인용 고성능 휴머노이드 축구 시스템과 미니어처 연구용 플랫폼 ToddlerBot의 설계 철학과 성능 차이를 보여줍니다.
- 🏛 기반 연구: [[papers/1796_AGILOped_Agile_Open-Source_Humanoid_Robot_for_Research/review]] — ToddlerBot의 ML 호환 플랫폼 설계 경험이 AGILOped의 동적 운동 능력 구현에 필요한 기초 지식을 제공한다
- 🏛 기반 연구: [[papers/1927_Fauna_Sprout_A_lightweight_approachable_developer-ready_huma/review]] — ToddlerBot의 오픈소스 ML 호환 설계가 Sprout의 개발자 친화적 접근 방식의 기반이 된다.
- 🏛 기반 연구: [[papers/2077_Learning_with_pyCub_A_Simulation_and_Exercise_Framework_for/review]] — 오픈소스 휴머노이드 플랫폼이 교육용 프레임워크의 하드웨어 기반을 제공한다.
