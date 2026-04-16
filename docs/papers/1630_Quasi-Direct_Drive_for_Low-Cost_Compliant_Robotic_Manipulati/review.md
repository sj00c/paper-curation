---
title: "1630_Quasi-Direct_Drive_for_Low-Cost_Compliant_Robotic_Manipulati"
authors:
  - "David V. Gealy"
  - "Stephen McKinley"
  - "Brent Yi"
  - "Philipp Wu"
  - "Phillip R. Downey"
date: "2019.04"
doi: ""
arxiv: ""
score: 4.0
essence: "Quasi-Direct Drive 구동방식을 기반으로 한 저비용 7-DOF 로봇 팔 Blue를 제안하여 인간 환경에서 안전하고 힘 제어 가능한 조작을 가능하게 함."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Humanoid_Locomotion_and_Control"
  - "sub/Portable_Humanoid_Teleoperation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gealy et al._2019_Quasi-Direct Drive for Low-Cost Compliant Robotic Manipulation.pdf"
---

# Quasi-Direct Drive for Low-Cost Compliant Robotic Manipulation

> **저자**: David V. Gealy, Stephen McKinley, Brent Yi, Philipp Wu, Phillip R. Downey, Greg Balke, Allan Zhao, Menglong Guo, Rachel Thomasson, Anthony Sinclair, Peter Cuellar, Zoe McCarthy, Pieter Abbeel | **날짜**: 2019-04-08 | **URL**: [https://arxiv.org/abs/1904.03815](https://arxiv.org/abs/1904.03815)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

Quasi-Direct Drive 구동방식을 기반으로 한 저비용 7-DOF 로봇 팔 Blue를 제안하여 인간 환경에서 안전하고 힘 제어 가능한 조작을 가능하게 함.

## Motivation

- **Known**: 기존 compliant 로봇들(KUKA LBR, Franka Emika, Barrett WAM)은 우수한 성능을 제공하지만 매우 높은 비용($25,000~$135,000)이 필요하며, 저비용 조작 로봇들은 대부분 DOF 감소나 성능 저하의 트레이드오프를 가짐.
- **Gap**: 현재까지 인간 환경에서의 안전한 배포를 위해 필요한 낮은 비용($5,000 이하)과 힘 제어 능력, 충분한 성능(7-DOF, 인간 규모)을 동시에 만족하는 로봇 팔이 없음.
- **Why**: 로봇의 대규모 배포와 Learning from Demonstration, Reinforcement Learning 같은 AI 기반 제어 방법의 적용을 위해 저비용 compliant 조작 로봇이 필수적이며, 인간 환경에서의 안전한 운영을 위해 힘 제어 능력이 중요함.
- **Approach**: Quasi-Direct Drive 구동방식을 채택하여 가격과 성능의 최적 균형을 달성하였으며, 인간 중심의 설계 지표(인간 대역폭 이상, 10mm 이하 반복도)를 기반으로 Blue 시스템을 설계 및 제조함.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **저비용 달성**: 1500대 이상 생산 시 $5,000 이하의 가격으로 공급 가능
- **적절한 동적 특성**: 위치 제어 대역폭 7.5Hz, 반복도 4mm으로 인간 조작자의 요구를 만족
- **인간 규모 설계**: 3-1-3 DOF 구성으로 인간 동작을 모방하여 직관적 조작 가능
- **완전 실현된 시스템**: 제조가능성, 확장성, 사용 사례 검증 포함한 완전한 패러다임 제시
- **다중 응용**: VR 기반 원격 조종, Learning from Demonstration, 실제 작업(주방 청소, 테이블 정리, 기계 관리) 시연

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- Quasi-Direct Drive 구동방식을 통해 역구동 가능하고 수동적으로 compliant한 시스템 구현
- 인간의 생체 특성(이두박근 대역폭 2.3Hz) 분석을 통해 필요 대역폭 기준 설정
- 열 제약 패러다임을 고려하여 최대 부하를 단기 피크로 정의하고 지속 운영 능력 확보
- Virtual Reality 인터페이스를 이용한 원격 조종 시스템 구축
- 설계-제조-비용 분석을 통한 실제 생산성 검증

## Originality

- 기존 high-precision, high-bandwidth 로봇 설계에서 벗어나 human-centric 성능 메트릭 재정의
- Quasi-Direct Drive 구동방식의 체계적 활용으로 저비용과 compliant 특성의 동시 달성
- 인간 생체학 데이터 활용한 과학적 설계 기준 수립
- AI 기반 제어 방법(LfD, RL)의 대규모 병렬 학습을 가능하게 하는 저비용 플랫폼 제공

## Limitation & Further Study

- 2kg 페이로드로 제한되어 무거운 객체 조작 불가능
- 4mm 반복도는 정밀한 산업 작업에는 미흡할 수 있음
- VR 인터페이스의 사용성과 원격 조종의 지연 시간 영향 분석 부재
- 대규모 생산 시 실제 단가 달성 가능성에 대한 상세한 경제성 분석 필요
- 다양한 실제 환경(습도, 온도, 먼지)에서의 장기 성능 안정성 검증 필요
- 후속 연구: 다양한 작업에 대한 자동화 능력 평가, AI 기반 정책 학습 효율성 실증, 확장성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 인간 환경에서 필요한 저비용 compliant 로봇의 설계 패러다임을 재정의하고 Quasi-Direct Drive 방식을 통해 이를 실현한 획기적 연구로, AI 기반 로봇 학습의 대규모 보급을 가능하게 하는 중요한 플랫폼을 제시함.

## Related Papers

- 🔄 다른 접근: [[papers/1773_A_21-DOF_Humanoid_Dexterous_Hand_with_Hybrid_SMA-Motor_Actua/review]] — Quasi-Direct Drive와 SMA-Motor 하이브리드 구동은 모두 저비용으로 컴플라이언트한 로봇 조작을 실현하는 서로 다른 구동 방식이다.
- 🔗 후속 연구: [[papers/1715_ToddlerBot_Open-Source_ML-Compatible_Humanoid_Platform_for_L/review]] — 저비용 컴플라이언트 조작 기술이 ToddlerBot과 같은 ML 호환 플랫폼에 적용되어 더 안전한 학습 환경을 제공할 수 있다.
- 🔗 후속 연구: [[papers/1631_RAPID_Hand_A_Robust_Affordable_Perception-Integrated_Dextero/review]] — Quasi-Direct Drive의 저비용 힘 제어와 RAPID Hand의 멀티모달 인지를 결합하면 완전한 저비용 조작 시스템을 구축할 수 있다
- 🔄 다른 접근: [[papers/1659_RUKA_Rethinking_the_Design_of_Humanoid_Hands_with_Learning/review]] — 둘 다 저비용 로봇 하드웨어를 제안하지만 Blue는 7-DOF 팔에, RUKA는 tendon-driven hand에 초점을 맞춘다
- 🏛 기반 연구: [[papers/1927_Fauna_Sprout_A_lightweight_approachable_developer-ready_huma/review]] — Fauna Sprout의 경량 휴머노이드 플랫폼이 Quasi-Direct Drive 구동방식의 실제 적용 대상이 될 수 있다
- 🏛 기반 연구: [[papers/1715_ToddlerBot_Open-Source_ML-Compatible_Humanoid_Platform_for_L/review]] — ToddlerBot의 저비용 ML 플랫폼 설계가 Quasi-Direct Drive와 같은 저비용 구동 방식의 실제 적용과 검증에 기반을 제공한다.
- 🏛 기반 연구: [[papers/1851_Control_of_Humanoid_Robots_with_Parallel_Mechanisms_using_Di/review]] — 저비용 컴플라이언트 로봇 조작을 위한 quasi-direct drive가 Cassie 영감 병렬 구동 메커니즘의 효율적인 제어에 필요한 기초 기술을 제공한다
- 🔄 다른 접근: [[papers/1773_A_21-DOF_Humanoid_Dexterous_Hand_with_Hybrid_SMA-Motor_Actua/review]] — SMA-DC모터 하이브리드와 Quasi-Direct Drive는 모두 컴플라이언트하고 저비용인 로봇 구동을 위한 서로 다른 혁신적 접근법이다.
- 🔄 다른 접근: [[papers/2048_Learning_Bipedal_Locomotion_on_Gear-Driven_Humanoid_Robot_Us/review]] — Learning Bipedal Locomotion은 고기어비 액추에이터 사용, Quasi-Direct Drive는 저비용 컴플라이언트 구동으로 서로 다른 액추에이션 방식을 채택한다.
