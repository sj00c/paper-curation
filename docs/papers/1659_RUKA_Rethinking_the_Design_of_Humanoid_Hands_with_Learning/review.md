---
title: "1659_RUKA_Rethinking_the_Design_of_Humanoid_Hands_with_Learning"
authors:
  - "Anya Zorin"
  - "Irmak Guzey"
  - "Billy Yan"
  - "Aadhithya Iyer"
  - "Lisa Kondrich"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "RUKA는 3D 프린팅과 저가 부품으로 제작한 tendon-driven humanoid hand로, learning-based control을 통해 정밀성, 컴팩트성, 강도, 저비용을 동시에 달성한다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/Exoskeleton_Hand_Teleoperation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zorin et al._2025_RUKA Rethinking the Design of Humanoid Hands with Learning.pdf"
---

# RUKA: Rethinking the Design of Humanoid Hands with Learning

> **저자**: Anya Zorin, Irmak Guzey, Billy Yan, Aadhithya Iyer, Lisa Kondrich, Nikhil X. Bhattasali, Lerrel Pinto | **날짜**: 2025-04-17 | **URL**: [https://arxiv.org/abs/2504.13165](https://arxiv.org/abs/2504.13165)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: RUKA is a tendon-driven humanoid hand that is simple,*

RUKA는 3D 프린팅과 저가 부품으로 제작한 tendon-driven humanoid hand로, learning-based control을 통해 정밀성, 컴팩트성, 강도, 저비용을 동시에 달성한다.

## Motivation

- **Known**: 로봇 손의 기존 설계들은 정밀성, 컴팩트성, 강도, 저비용 중 일부만 만족하며 trade-off를 요구한다. Tendon-driven 설계는 컴팩트하고 강력하지만 비선형성과 불확실성으로 인해 제어가 어렵다.
- **Gap**: 기존의 tendon-driven 손들은 joint encoder를 통해 closed-loop control을 구현하려 하지만 비용이 높고 유지보수가 어렵다. Learning-based 접근으로 encoder 없이 tendon-driven 손을 효과적으로 제어할 수 있는 방법이 부족하다.
- **Why**: 저비용의 anthropomorphic robotic hand는 로봇 연구의 접근성을 높이고, human demonstration 기반 학습을 용이하게 하며, 실제 환경에서의 응용을 확대할 수 있다.
- **Approach**: MANUS motion-capture glove를 로봇 손에 장착하여 joint와 fingertip position 데이터를 수집하고, 이를 통해 joint-to-actuator 및 fingertip-to-actuator models를 학습한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: (A) A Venn diagram of a variety of robotic hands [1, 44, 43, 13, 24, 11] demonstrates RUKA’s unique combination *

- **오픈소스 하드웨어 설계**: $1,300 이하의 비용으로 제작 가능하며 7시간 내에 조립 가능한 완전 open-source tendon-driven hand 제공
- **Data-driven control approach**: MANUS glove를 활용한 자동화된 데이터 수집으로 복잡한 tendon 비선형성을 학습 모델로 해결
- **우수한 성능 비교**: LEAP, Allegro 등 기존 손들 대비 reachability, durability, strength에서 우수함을 실증
- **실제 응용 검증**: Teleoperation 작업에서 dexterous movement 수행 능력 입증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: (A) Joints enable 15 degrees of freedom of RUKA labeled with their corresponding joint names. (B) The splay of t*

- MANUS motion-capture glove를 RUKA 손에 장착하여 encoder 없이도 정확한 joint 및 fingertip position 데이터 획득
- procedurally sampling을 통해 motor limits 내에서 actuation command를 자동으로 변화시켜 (actuator command, joint/fingertip position) 쌍 데이터 대규모 수집
- 수집된 데이터로부터 joint-to-actuator model과 fingertip-to-actuator model 학습
- 학습된 모델을 통한 inverse control: 목표 position이 주어질 때 필요한 actuator command 예측
- Tendon-driven 메커니즘의 복잡한 kinematics를 완전히 모델링하지 않고 data-driven 방식으로 근사

## Originality

- Motion-capture glove를 로봇 손에 직접 장착하는 혁신적 데이터 수집 방식: 기존 Vicon, IR sensor, AR tag 기반 방법보다 간편하고 확장성 높음
- Morphological accuracy를 활용한 human demonstration 직접 활용 전략으로 retargeting 복잡성 제거
- 저비용 tendon-driven 설계와 learning-based control의 결합으로 hardware trade-off 재고찰
- 완전 open-source로 재현성과 접근성 강조한 연구 문화 기여

## Limitation & Further Study

- 학습된 모델의 generalization 성능과 distribution shift에 대한 robustness 평가 부족
- Tendon 탄성, 마찰, 히스테리시스 등 비모델링 요인이 실제 제어에 미치는 영향 분석 제한적
- Dexterous manipulation 작업(복잡한 in-hand manipulation 등)에서의 autonomous learning 성능 미제시
- 15 DOF 대비 11 actuator의 underactuation이 특정 grasp 형태에 미치는 제약 조건 심화 분석 필요
- 후속연구: reinforcement learning으로 closed-loop autonomous control policy 학습, soft finger design으로 compliance 추가 연구, 다양한 object manipulation 벤치마크 확대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RUKA는 learning-based control과 실용적 hardware 설계를 결합하여 저비용 대 성능 비율에서 로봇 손 영역의 새로운 기준을 제시하며, open-source 공개로 접근성을 극대화한 의미 있는 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1631_RAPID_Hand_A_Robust_Affordable_Perception-Integrated_Dextero/review]] — 둘 다 저비용 휴머노이드 손을 제안하지만 RUKA는 tendon-driven 메커니즘에, RAPID Hand는 인지 통합에 중점을 둔다
- 🔗 후속 연구: [[papers/1700_TACT_Humanoid_Whole-body_Contact_Manipulation_through_Deep_I/review]] — RUKA의 learning-based control과 TACT의 촉각 모방 학습을 결합하면 더 정교한 접촉 조작이 가능하다
- 🏛 기반 연구: [[papers/2169_UniDex_A_Robot_Foundation_Suite_for_Universal_Dexterous_Hand/review]] — UniDex의 범용 민첩한 조작 기술이 RUKA hand의 학습 기반 제어 시스템에 적용될 수 있다
- 🔄 다른 접근: [[papers/1700_TACT_Humanoid_Whole-body_Contact_Manipulation_through_Deep_I/review]] — 둘 다 손 기반 조작을 다루지만 촉각 센서 활용 vs tendon-driven 메커니즘으로 접근이 다르다
- 🔄 다른 접근: [[papers/1630_Quasi-Direct_Drive_for_Low-Cost_Compliant_Robotic_Manipulati/review]] — 둘 다 저비용 로봇 하드웨어를 제안하지만 Blue는 7-DOF 팔에, RUKA는 tendon-driven hand에 초점을 맞춘다
- 🔗 후속 연구: [[papers/1803_Antagonistic_Bowden-Cable_Actuation_of_a_Lightweight_Robotic/review]] — 학습 기반 휴머노이드 손 설계 재고찰이 Bowden 케이블 구동 방식의 20 DOF 극경량 구현을 더욱 최적화할 수 있다.
- 🏛 기반 연구: [[papers/1773_A_21-DOF_Humanoid_Dexterous_Hand_with_Hybrid_SMA-Motor_Actua/review]] — 학습 기반 휴머노이드 손 설계의 이론적 기반을 RUKA의 재설계 철학에서 찾을 수 있습니다.
- 🏛 기반 연구: [[papers/1870_DexterCap_An_Affordable_and_Automated_System_for_Capturing_D/review]] — RUKA의 학습 기반 휴머노이드 손 설계가 DexterCap으로 수집된 인간 손 동작 데이터를 효과적으로 재현할 수 있는 로봇 손 하드웨어 기반을 제공한다.
- 🔄 다른 접근: [[papers/1873_Dexterous_Teleoperation_of_20-DoF_ByteDexter_Hand_via_Human/review]] — ByteDexter의 링크구동 20-DoF 손과 RUKA의 학습 기반 휴머노이드 손 설계는 정교한 로봇 손에서 기계적 설계 vs 학습적 접근의 서로 다른 철학을 보여준다.
- 🔄 다른 접근: [[papers/1876_DIAL_Distilling_Intent-Aware_Latents_for_Vision-Language-Act/review]] — 휴머노이드 손 설계에서 SoftHand Model-W와 RUKA라는 서로 다른 설계 철학과 학습 기반 접근법을 제시한다
- 🔄 다른 접근: [[papers/2129_ORCA_An_Open-Source_Reliable_Cost-Effective_Anthropomorphic/review]] — ORCA는 tendon-driven 저비용 설계, RUKA는 학습 기반 손 설계로 서로 다른 접근법의 휴머노이드 손 개발을 제시한다.
