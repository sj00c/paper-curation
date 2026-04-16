---
title: "1859_DecARt_Leg_Design_and_Evaluation_of_a_Novel_Humanoid_Robot_L"
authors:
  - "Egor Davydenko"
  - "Andrei Volchenkov"
  - "Vladimir Gerasimov"
  - "Roman Gorbachev"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 decoupled actuation을 활용하면서도 인간형 다리의 외형을 유지하는 DecARt Leg을 제안하며, FAST(Fastest Achievable Swing Time) 메트릭을 통해 agile locomotion 능력을 평가한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Exercise_Learning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Davydenko et al._2025_DecARt Leg Design and Evaluation of a Novel Humanoid Robot Leg with Decoupled Actuation for Agile L.pdf"
---

# DecARt Leg: Design and Evaluation of a Novel Humanoid Robot Leg with Decoupled Actuation for Agile Locomotion

> **저자**: Egor Davydenko, Andrei Volchenkov, Vladimir Gerasimov, Roman Gorbachev | **날짜**: 2025-11-13 | **URL**: [https://arxiv.org/abs/2511.10021](https://arxiv.org/abs/2511.10021)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. The concept of DecARt Leg design: decoupled actuation, all motors*

본 논문은 decoupled actuation을 활용하면서도 인간형 다리의 외형을 유지하는 DecARt Leg을 제안하며, FAST(Fastest Achievable Swing Time) 메트릭을 통해 agile locomotion 능력을 평가한다.

## Motivation

- **Known**: 기존 humanoid robot은 serial/coupled kinematic structure를 사용하며 제어 단순성과 인간형 외형을 추구한다. Cassie/Digit 로봇은 decoupled design으로 우수한 locomotion 성능을 보이지만 조류 같은 외형을 가진다.
- **Gap**: Decoupled actuation의 효율성과 human-like morphology를 동시에 달성하는 설계가 부재한 상태이다.
- **Why**: Agile locomotion 능력을 갖춘 일반목적형 humanoid robot 개발을 위해 decoupled design의 장점을 활용하면서도 인간형 외형을 유지하는 것이 필요하다.
- **Approach**: Quasi-telescopic kinematic structure를 통해 leg pitch motor와 leg length motor를 분리하고, novel multi-bar ankle actuation system으로 모든 모터를 무릎 위에 배치하여 decoupled actuation과 human-like appearance를 동시에 달성한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- **DecARt Leg 설계**: Decoupled actuation을 실현하면서도 forward-facing knee의 인간형 외형을 유지하는 quasi-telescopic leg design 제시
- **FAST 메트릭**: Agile locomotion capability를 정량적으로 평가하기 위한 새로운 descriptive metric 제안
- **설계 비교**: 기존 leg designs와의 정량적 비교를 통해 DecARt Leg의 우수성 검증
- **시뮬레이션 및 하드웨어 평가**: Extensive simulation과 preliminary hardware experiments로 성능 검증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3. DecARt Leg multi-bar ankle torque transmission structure: different*

- Passive gears와 4-bar parallel structure를 결합하여 leg length motor의 회전을 foot의 직선 운동으로 변환
- Multi-bar linkage system으로 ankle actuation을 실현하고 모든 모터를 leg root 근처에 배치하여 swing inertia 최소화
- Analytical inverse kinematics 도출로 제어 단순성 확보
- Full compact/stretch 가능성과 fully compacted knee 상태에서 ankle 위치 조절 가능성 구현

## Originality

- Decoupled actuation과 human-like morphology의 결합이 기존 연구와 차별화되며, Cassie의 장점을 유지하면서 bird-like appearance 극복
- Rotational actuator만 사용하면서 decoupled design 실현하여 modeling/control 단순성 유지
- FAST 메트릭의 신규 제안으로 agile locomotion capability 정량화
- Multi-bar ankle torque transmission의 novel design으로 motor placement 최적화

## Limitation & Further Study

- Preliminary hardware experiments에 그쳐 full-scale locomotion performance 검증 부족
- FAST 메트릭의 실제 locomotion 성능과의 상관성에 대한 충분한 검증 필요
- Decoupled vs coupled design의 energy efficiency 비교 분석 미흡
- 제어 알고리즘 및 안정성 분석에 대한 상세 기술 부재
- 후속 연구로 full-scale robot 구현, 실제 동적 locomotion 실험, 다양한 terrain에서의 성능 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 humanoid robotics의 오랜 설계 갈등(efficiency vs. human-like appearance)을 새로운 kinematic approach로 해결하려는 의미 있는 시도이며, FAST 메트릭 제안과 함께 충분한 설계 혁신성을 보여준다. 다만 preliminary hardware 수준의 검증에 그쳐 실제 성능 우위를 완전히 입증하지는 못한 한계가 있다.

## Related Papers

- 🔗 후속 연구: [[papers/1990_Human-Level_Actuation_for_Humanoids/review]] — 인간 수준의 액추에이션 기술이 DecARt Leg의 decoupled actuation을 더욱 효과적이고 인간과 유사한 성능으로 구현할 수 있다
- 🔄 다른 접근: [[papers/1851_Control_of_Humanoid_Robots_with_Parallel_Mechanisms_using_Di/review]] — 휴머노이드 다리의 agile locomotion을 decoupled actuation과 병렬 구동 메커니즘이라는 서로 다른 설계 철학으로 달성한다
- 🧪 응용 사례: [[papers/2127_Optimizing_Bipedal_Locomotion_for_The_100m_Dash_With_Compari/review]] — 100m 달리기 최적화가 DecARt Leg의 FAST 메트릭과 agile locomotion 능력을 실제 경쟁적 운동 성능에서 검증할 수 있다
- 🔄 다른 접근: [[papers/1864_Demonstrating_Berkeley_Humanoid_Lite_An_Open-source_Accessib/review]] — DecARt Leg의 고성능 decoupled actuation과 Berkeley Humanoid Lite의 저비용 설계는 휴머노이드 다리 설계에서 성능 vs 접근성의 서로 다른 우선순위를 보여준다.
- 🔗 후속 연구: [[papers/1776_A_Framework_for_Optimal_Ankle_Design_of_Humanoid_Robots/review]] — DecARt Leg의 설계가 휴머노이드 로봇의 최적 발목 설계 프레임워크로 확장되어 전체 다리 시스템의 통합 최적화를 가능하게 한다.
- 🧪 응용 사례: [[papers/1925_FastStair_Learning_to_Run_Up_Stairs_with_Humanoid_Robots/review]] — DecARt Leg의 agile locomotion 능력과 FAST 메트릭이 휴머노이드 로봇의 계단 오르기 학습에 실질적으로 적용되어 동적 성능을 평가할 수 있다.
- 🔗 후속 연구: [[papers/1920_Explosive_Output_to_Enhance_Jumping_Ability_A_Variable_Reduc/review]] — 점프 능력 향상을 위한 가변 감속 출력 시스템으로 확장됩니다.
- 🔄 다른 접근: [[papers/1796_AGILOped_Agile_Open-Source_Humanoid_Robot_for_Research/review]] — 오픈소스 인간형 로봇 연구를 위한 다른 하드웨어 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1833_Characteristics_Management_and_Utilization_of_Muscles_in_Mus/review]] — 근골격 로봇의 복잡한 근육 시스템과 DecARt Leg의 decoupled actuation은 휴머노이드 구동에 대한 서로 다른 설계 철학을 보여준다.
- 🔄 다른 접근: [[papers/1851_Control_of_Humanoid_Robots_with_Parallel_Mechanisms_using_Di/review]] — 휴머노이드 다리의 agile locomotion을 병렬 구동 메커니즘 모델링과 decoupled actuation이라는 서로 다른 접근법으로 달성한다
- 🔄 다른 접근: [[papers/1864_Demonstrating_Berkeley_Humanoid_Lite_An_Open-source_Accessib/review]] — Berkeley Humanoid Lite의 저비용 접근성과 DecARt Leg의 고성능 설계는 휴머노이드 개발에서 민주화 vs 성능 최적화의 서로 다른 목표를 보여준다.
- 🏛 기반 연구: [[papers/1975_Hierarchical_visuomotor_control_of_humanoids/review]] — 휴머노이드 설계와 제어의 기초 원리가 DecARt Leg의 새로운 휴머노이드 로봇 개발의 이론적 토대가 된다.
