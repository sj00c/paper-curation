---
title: "1711_The_MIT_Humanoid_Robot_Design_Motion_Planning_and_Control_Fo"
authors:
  - "Matthew Chignoli"
  - "Donghyun Kim"
  - "Elijah Stanger-Jones"
  - "Sangbae Kim"
date: "2021.04"
doi: ""
arxiv: ""
score: 4.0
essence: "MIT 휴머노이드 로봇이 고도의 동역학 운동(백플립, 전플립, 회전 점프)을 수행하기 위해 맞춤형 액추에이터 설계, actuator-aware kino-dynamic 모션 플래닝, 그리고 MPC와 WBIC을 통합한 착지 제어 시스템을 제시한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Exercise_Learning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chignoli et al._2021_The MIT Humanoid Robot Design, Motion Planning, and Control For Acrobatic Behaviors.pdf"
---

# The MIT Humanoid Robot: Design, Motion Planning, and Control For Acrobatic Behaviors

> **저자**: Matthew Chignoli, Donghyun Kim, Elijah Stanger-Jones, Sangbae Kim | **날짜**: 2021-04-19 | **URL**: [https://arxiv.org/abs/2104.09025](https://arxiv.org/abs/2104.09025)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

MIT 휴머노이드 로봇이 고도의 동역학 운동(백플립, 전플립, 회전 점프)을 수행하기 위해 맞춤형 액추에이터 설계, actuator-aware kino-dynamic 모션 플래닝, 그리고 MPC와 WBIC을 통합한 착지 제어 시스템을 제시한다.

## Motivation

- **Known**: 보스턴 다이나믹스의 Atlas 로봇이 백플립을 시연했지만 방법론이 공개되지 않았으며, DARPA Robotics Challenge 이후 현대 휴머노이드 로봇들은 주로 저동역학 작업에 최적화되어 있다.
- **Gap**: 고도의 동역학 운동을 수행하는 휴머노이드 로봇을 위한 통합적인 하드웨어 설계, 모션 플래닝, 제어 프레임워크의 실제 구현 방법이 문서화되지 않았으며, 기존 설계 패러다임(유압식, 콤플라이언트 액추에이터)은 고속 동작에 제약이 있다.
- **Why**: acrobatic 동작 능력은 휴머노이드 로봇의 민첩성과 동역학 제어 능력을 입증하며, MIT Cheetah의 성공적인 설계 원리를 휴머노이드에 적용하여 일반화된 동역학 운동 제어 방법을 확립할 수 있다.
- **Approach**: MIT Cheetah의 torque-dense electric motors, high-bandwidth force control, backdrivability 설계 원리를 휴머노이드 로봇에 적용하고, actuator 제약 조건을 반영한 kino-dynamic 모션 플래닝과 centroidal dynamics 기반의 MPC 및 whole-body impulse control을 계층적으로 통합한다.

## Achievement


- **맞춤형 액추에이터 개발**: U10 및 U12 모듈을 설계하고 custom dynamometer로 torque, velocity, power 특성을 실험적으로 검증하여 정확한 dynamics 모델 구성
- **Actuator-aware 모션 플래닝**: configuration-dependent reaction force limits을 고려한 kino-dynamic planner 개발으로 actuator 제약 조건을 직접 반영
- **고성능 착지 제어**: MPC와 WBIC의 dynamically consistent 통합으로 장시간 최적 제어와 고대역폭 전신 피드백 동시 달성
- **simulation에서의 동적 동작 실증**: back flip, front flip, spinning jump 등의 acrobatic 운동을 realistic dynamics에서 성공적으로 시뮬레이션

## How


- 두 가지 proprioceptive motor module (U10, U12)을 기반으로 설계하여 각 관절의 torque와 속도 요구사항 충족
- Dynamometer를 이용한 실험으로 torque constant, inductance, resistance 측정 및 voltage droop과 back-EMF를 포함한 torque-speed curve 모델링
- Centroidal dynamics와 joint-level kinematics를 동시에 최적화하는 kino-dynamic planner로 full-body dynamics 제약 조건 반영
- MPC로 long-time horizon 최적 궤적 계획 후, WBIC이 MPC의 위치/반력 명령을 받아 high-bandwidth instantaneous 제어 실행
- Battery voltage droop을 반영한 정밀한 actuator 토크 검증으로 시뮬레이션 결과의 실제 구현 가능성 확보

## Originality

- MIT Cheetah의 설계 원리를 최초로 humanoid 플랫폼에 적용하여 high-bandwidth torque control과 backdrivability 달성
- Actuator 성능 제약을 직접 반영하는 새로운 kino-dynamic motion planner 개발
- MPC와 WBIC의 계층적 통합에서 body orientation task의 우선순위 조정으로 향상된 착지 제어 성능 달성
- Custom dynamometer 설계 및 실험 검증으로 simulation의 신뢰성 강화

## Limitation & Further Study

- 현재까지는 realistic dynamics simulation에서만 동작을 검증했으며, 실제 하드웨어에서의 동작 시연이 아직 이루어지지 않음
- 단일 battery pack의 voltage droop 모델만 포함하고 있으며, 장시간 동작에서의 배터리 성능 열화는 고려되지 않음
- Kino-dynamic planner의 computational 복잡도와 solve time에 대한 상세한 분석이 부족함
- 착지 후의 후속 동작이나 연속적인 multiple acrobatic motions에 대한 검토 필요
- External disturbance나 modeling error에 대한 강건성 평가가 simulation 기반이므로 실제 환경에서의 성능 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 humanoid 로봇의 고도의 동역학 운동을 실현하기 위해 하드웨어, 모션 플래닝, 제어를 통합적으로 설계한 체계적인 접근법을 제시하며, 맞춤형 액추에이터 개발과 정밀한 검증을 통해 높은 신뢰성을 확보한 우수한 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1682_SMASH_Mastering_Scalable_Whole-Body_Skills_for_Humanoid_Ping/review]] — MIT 휴머노이드의 고역학 운동 제어 기술이 탁구와 같은 정밀한 스포츠 동작의 MPC 기반 제어에 기반 기술을 제공한다.
- 🔗 후속 연구: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — 백플립과 같은 acrobatic motion planning 기법이 도어 통과의 동적 행동 계획에 확장 적용될 수 있다.
- 🔗 후속 연구: [[papers/2001_Humanoid_Robot_Acrobatics_Utilizing_Complete_Articulated_Rig/review]] — MIT 휴머노이드의 고동역학 운동과 완전 관절 강체 역학 활용 곡예를 결합하면 더 극한의 운동이 가능하다
- 🏛 기반 연구: [[papers/1834_Chasing_Stability_Humanoid_Running_via_Control_Lyapunov_Func/review]] — Control Lyapunov Function 기반 안정성 추적이 MIT 휴머노이드의 MPC-WBIC 통합 착지 제어의 이론적 기반을 제공한다
- 🔗 후속 연구: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — 강건한 이족 점프 제어의 개념을 백플립, 전플립 등 고도의 아크로바틱 동작으로 확장하여 kino-dynamic 계획과 착지 제어를 통합했다.
- 🏛 기반 연구: [[papers/1920_Explosive_Output_to_Enhance_Jumping_Ability_A_Variable_Reduc/review]] — 폭발적 출력을 통한 점프 능력 향상의 개념을 MIT 휴머노이드의 맞춤형 액추에이터 설계와 동역학 계획으로 구체화하여 아크로바틱 동작을 가능하게 했다.
- 🧪 응용 사례: [[papers/1757_Whole-body_Multi-contact_Motion_Control_for_Humanoid_Robots/review]] — 전신 동적 제어 기술을 투구라는 구체적 작업에 적용하여 다리 달린 조작기의 고도 동역학 운동을 실현했다.
- 🔗 후속 연구: [[papers/1682_SMASH_Mastering_Scalable_Whole-Body_Skills_for_Humanoid_Ping/review]] — SMASH의 ego-centric vision 기반 탁구 기술이 MIT 휴머노이드의 동적 운동 제어에 통합되어 더 복잡한 스포츠 동작이 가능하다.
