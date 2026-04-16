---
title: "1757_Whole-body_Multi-contact_Motion_Control_for_Humanoid_Robots"
authors:
  - "Masaki Murooka"
  - "Kensuke Fukumitsu"
  - "Marwan Hamze"
  - "Mitsuharu Morisawa"
  - "Hiroshi Kaminaga"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "휴머노이드 로봇이 분산 촉각 센서를 장착하여 팔꿈치, 무릎 등 중간 영역의 접촉을 포함한 전신 다중 접촉 모션을 제어하는 방법을 개발했다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Tactile_Contact_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Murooka et al._2025_Whole-body Multi-contact Motion Control for Humanoid Robots Based on Distributed Tactile Sensors.pdf"
---

# Whole-body Multi-contact Motion Control for Humanoid Robots Based on Distributed Tactile Sensors

> **저자**: Masaki Murooka, Kensuke Fukumitsu, Marwan Hamze, Mitsuharu Morisawa, Hiroshi Kaminaga, Fumio Kanehiro, Eiichi Yoshida | **날짜**: 2025-05-26 | **URL**: [https://arxiv.org/abs/2505.19580](https://arxiv.org/abs/2505.19580)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Control system for whole-body multi-contact motion in a humanoid robot.*

휴머노이드 로봇이 분산 촉각 센서를 장착하여 팔꿈치, 무릎 등 중간 영역의 접촉을 포함한 전신 다중 접촉 모션을 제어하는 방법을 개발했다.

## Motivation

- **Known**: 기존 연구는 손과 발 등 extremities에서의 다중 접촉 모션 제어를 다루었으며, 촉각 센서는 주로 human interaction이나 object manipulation 작업에 활용되었다.
- **Gap**: position-controlled 휴머노이드 로봇이 실시간 촉각 피드백을 통해 중간 영역(forearm 등)에서의 동적 접촉 모션을 실현한 사례가 부재했다.
- **Why**: 휴머노이드 로봇이 좁은 환경에서 안정적으로 작업하려면 전신 영역의 접촉을 활용한 robust 모션이 필수적이며, 이를 통해 disturbance와 environmental error에 대한 안정성을 높일 수 있다.
- **Approach**: 기존 다중 접촉 제어 프레임워크를 확장하여 distributed tactile sensor로부터 측정한 contact polygon과 contact wrench를 이용해 centroidal motion control과 limb motion control을 강화했다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. RHP Kaleido with distributed tactile sensors mounted on one forearm*

- **분산 촉각 센서 기반 접촉 다각형 온라인 업데이트**: 실측 contact polygon과 predefined polygon의 차이를 감지하여 real-time으로 접촉 영역을 보정하여 balance control 안정성을 향상
- **MPC 기반 향상된 centroidal 계획**: Newton-Euler equation 기반의 nonlinear discrete system을 MPC로 제어하며 tactile feedback을 통해 wrench distribution 최적화
- **실시간 dampening 제어**: 촉각 센서의 contact wrench 측정을 피드백으로 활용하여 disturbance와 environmental error에 대한 robustness 증가
- **실제 휴머노이드 로봇 검증**: RHP Kaleido를 통해 forearm contact로 전진 stepping, thigh contact로 앉은 자세 balancing 등 다양한 전신 다중 접촉 모션 실현

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Control system for whole-body multi-contact motion in a humanoid robot.*

- Deformable sheet-shaped distributed tactile sensor를 로봇 limb 표면에 장착하여 robot body shape 변형 최소화
- Contact wrench를 friction pyramid의 ridge vector와 scale factor λ로 표현하여 centroidal 상태 제어 입력으로 활용
- MPC를 통해 centroidal motion을 제어하되, contact polygon 정보로부터 moment 생성 가능 범위를 동적으로 결정
- Limb motion control에서 inverse kinematics와 함께 tactile feedback 기반의 compliance control 적용
- Simulation으로 제어법의 안정성을 검증한 후 real-world 실험 수행

## Originality

- Position-controlled 휴머노이드 로봇에서 실시간 촉각 센서 피드백을 통한 동적 중간 영역 접촉의 첫 실현
- Distributed tactile sensor로부터 contact polygon을 온라인으로 측정하고 이를 centroidal control에 반영하는 새로운 통합 제어 방식
- 기존 extremity-only 다중 접촉 제어 프레임워크를 whole-body contact로 일반화한 확장

## Limitation & Further Study

- Contact sequence의 시간, 위치, 영역이 사전에 결정되어야 하므로 fully autonomous planning은 미실현
- Distributed tactile sensor의 calibration과 spatial map construction 과정이 필요하며 센서 마모에 따른 성능 저하 가능성
- Real-world 실험이 RHP Kaleido 단일 로봇으로만 검증되어 다른 휴머노이드 플랫폼으로의 일반화 가능성 미확인
- 고속 동적 모션에서의 센서 응답 지연과 friction coefficient 변화에 대한 robustness 분석 부족
- 후속 연구로 tactile sensor 기반의 global motion planner 개발과 다양한 로봇 플랫폼 적용 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 distributed tactile sensor를 활용하여 휴머노이드 로봇의 전신 다중 접촉 모션을 처음으로 실현한 의미 있는 연구로, 방법론과 검증이 체계적이나 autonomous planning 미흡이 제한적이다.

## Related Papers

- 🔄 다른 접근: [[papers/2003_Humanoid_Whole-Body_Badminton_via_Multi-Stage_Reinforcement/review]] — 두 연구 모두 전신 동역학을 활용하지만 하나는 투척에, 다른 하나는 배드민턴이라는 서로 다른 동적 작업에 적용합니다.
- 🔗 후속 연구: [[papers/1979_HITTER_A_HumanoId_Table_TEnnis_Robot_via_Hierarchical_Planni/review]] — 탁구 로봇의 계층적 계획과 제어 방식을 전신 동적 투척 작업에 적용할 수 있는 확장된 접근법입니다.
- 🧪 응용 사례: [[papers/2066_Learning_to_Ball_Composing_Policies_for_Long-Horizon_Basketb/review]] — 농구공 다루기와 같은 복합적 볼 조작 작업에 동적 투척 기술을 적용할 수 있습니다.
- 🔄 다른 접근: [[papers/1757_Whole-body_Multi-contact_Motion_Control_for_Humanoid_Robots/review]] — 전신 동역학 투척과 촉각 기반 다중 접촉 제어는 모두 whole-body coordination을 다루지만 접근 방식이 다르다.
- 🔗 후속 연구: [[papers/1779_A_Humanoid_Visual-Tactile-Action_Dataset_for_Contact-Rich_Ma/review]] — 시각-촉각-행동 데이터셋의 접촉이 풍부한 조작 경험이 투척 동작의 정밀한 목표 달성에 활용될 수 있다.
- 🧪 응용 사례: [[papers/1923_FAME_Force-Adaptive_RL_for_Expanding_the_Manipulation_Envelo/review]] — FAME의 force-adaptive RL 기법이 투척 시 물체와의 접촉력 제어 및 조작 영역 확장에 적용될 수 있다.
- 🧪 응용 사례: [[papers/1711_The_MIT_Humanoid_Robot_Design_Motion_Planning_and_Control_Fo/review]] — 전신 동적 제어 기술을 투구라는 구체적 작업에 적용하여 다리 달린 조작기의 고도 동역학 운동을 실현했다.
- 🏛 기반 연구: [[papers/1908_Embrace_Collisions_Humanoid_Shadowing_for_Deployable_Contact/review]] — 전신 다중접촉 동작 제어 기술이 접촉-무관 동작 수행의 핵심 이론적 토대를 제공합니다.
- 🏛 기반 연구: [[papers/1931_Flow_Matching_Imitation_Learning_for_Multi-Support_Manipulat/review]] — 전신 다중접촉 동작 제어의 이론적 기반이 Flow Matching 모방학습의 다중 지지 조작에 필수적입니다.
- 🏛 기반 연구: [[papers/1970_Heavy_lifting_tasks_via_haptic_teleoperation_of_a_wheeled_hu/review]] — Whole-body dynamic throwing 기술이 무거운 물체 들어올리기의 동역학적 기반이 됩니다.
