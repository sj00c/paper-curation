---
title: "1833_Characteristics_Management_and_Utilization_of_Muscles_in_Mus"
authors:
  - "Kento Kawaharazuka"
  - "Kei Okada"
  - "Masayuki Inaba"
date: "2026.02"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Kengoro와 Musashi 근골격 휴머노이드 로봇의 근육 특성을 5가지 속성(Redundancy, Independency, Anisotropy, Variable Moment Arm, Nonlinear Elasticity)으로 분류하고, 이를 효과적으로 관리·활용하는 방법론을 제시한다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Laparoscopic_Teleoperation_Systems"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kawaharazuka et al._2026_Characteristics, Management, and Utilization of Muscles in Musculoskeletal Humanoids Empirical Stud.pdf"
---

# Characteristics, Management, and Utilization of Muscles in Musculoskeletal Humanoids: Empirical Study on Kengoro and Musashi

> **저자**: Kento Kawaharazuka, Kei Okada, Masayuki Inaba | **날짜**: 2026-02-09 | **URL**: [https://arxiv.org/abs/2602.08518](https://arxiv.org/abs/2602.08518)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. The basic musculoskeletal structure: the components include bones,*

본 논문은 Kengoro와 Musashi 근골격 휴머노이드 로봇의 근육 특성을 5가지 속성(Redundancy, Independency, Anisotropy, Variable Moment Arm, Nonlinear Elasticity)으로 분류하고, 이를 효과적으로 관리·활용하는 방법론을 제시한다.

## Motivation

- **Known**: 근골격 휴머노이드는 다양하게 개발되어 왔으며, 근육의 중복성과 비선형 탄성은 가변 강성 제어 등의 장점을 제공하지만 동시에 모델링과 제어를 복잡하게 만든다.
- **Gap**: 기존 연구는 대부분 시뮬레이션이나 2D 단순화 모델에 집중되어 있으며, 실제 전신 근골격 로봇의 근육 특성에 대한 통합적이고 체계적인 논의가 부족하다.
- **Why**: 근육 특성의 장단점을 명확히 이해하고 체계적으로 관리·활용할 수 있다면, 근골격 휴머노이드의 제어 성능을 향상시키고 생체모방 로봇의 이점을 더욱 효과적으로 활용할 수 있다.
- **Approach**: 실제 구현된 Kengoro와 Musashi 로봇을 대상으로 다양한 연구 결과를 바탕으로 근육 특성을 5가지 속성으로 분류하고, body schema learning, reflex control, muscle grouping, body schema adaptation 등의 소프트웨어 기법을 통해 관리·활용 방법을 제시한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. The overview of the system which manages and utilizes advantages/disadvantages of the musculoskeletal structure.*

- **근육 특성의 체계적 분류**: Redundancy, Independency, Anisotropy, Variable Moment Arm, Nonlinear Elasticity의 5가지 속성으로 근골격 구조를 분류하여 복잡한 특성을 단순화
- **장단점 통합 분석**: 각 속성의 조합으로부터 발생하는 장단점을 체계적으로 분석하고 정리
- **실제 로봇 기반 검증**: 실제 구현된 Kengoro와 Musashi 로봇에서 다양한 연구 결과를 바탕으로 이론 검증
- **통합 제어 시스템**: body schema learning, reflex control, muscle grouping, body schema adaptation을 통합한 소프트웨어 시스템 구현
- **관절각 추정 방법론**: 복잡한 관절 구조에서 근육 길이 변화만으로 EKF와 비전 기반 AR marker를 이용한 관절각 추정 기법 제시

## How

![Figure 4](figures/fig4.webp)

*Fig. 4. The overview of the system which manages and utilizes advantages/disadvantages of the musculoskeletal structure.*

- Extended Kalman Filter(EKF)를 이용한 근육 길이 변화로부터의 관절각 추정 (식 7-15)
- Vision 기반 AR marker 인식을 통한 관절각 추정값 보정 (식 16)
- Quadratic programming을 이용한 목표 관절 토크 실현 근육 장력 계산 (식 17)
- Body schema learning: 근육-관절 복합 관계의 학습을 통한 제어 모델 구축
- Reflex control: 근육 이완 제어 등의 반사 제어 시스템 구현
- Muscle grouping: 근육 그룹화를 통한 제어 차원 축소
- Body schema adaptation: 환경 변화 대응을 위한 신체 스키마 적응

## Originality

- 실제 전신 근골격 휴머노이드 로봇의 다양한 연구 사례를 바탕으로 근육 특성을 체계적으로 분류한 첫 시도
- 근육 특성의 장단점을 통합적으로 논의하고 관리·활용 방법론을 제시한 통일된 프레임워크 구축
- 복잡한 관절 구조를 갖춘 근골격 로봇에서 joint encoder 없이 근육 길이와 비전 정보만으로 관절각을 추정하는 실용적 방법론 제시
- 여러 소프트웨어 기법(body schema learning, reflex control, muscle grouping 등)을 통합한 실제 동작 구현 사례 제공

## Limitation & Further Study

- 소프트웨어 중심의 논의로, 하드웨어 설계 및 최적화에 대한 논의 부재
- Pulley를 사용하는 wire-driven robot과 pneumatic artificial muscle 기반 로봇은 직접 대상으로 하지 않음
- Joint angle estimation에서 모델링되지 않은 요인(근육 신축, 마찰 등)의 영향으로 인한 오류 존재
- 모션 실험 결과에 대한 정량적 성능 평가 지표 및 비교 분석 부재 (본문 발췌 범위 내)
- 후속 연구로 각 특성의 장단점을 최적화하는 제어 알고리즘 개발 필요
- 다양한 작업 환경과 동작에서의 일반화 성능 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 근골격 휴머노이드의 근육 특성을 처음으로 체계적으로 분류하고 관리·활용 방법을 제시한 중요한 기여이며, 실제 로봇 구현 사례를 바탕으로 높은 실용성을 갖추고 있다. 다만 정량적 성능 평가 및 일반화 가능성에 대한 보완이 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1618_PIMBS_Efficient_Body_Schema_Learning_for_Musculoskeletal_Hum/review]] — PIMBS의 근골격 신체 스키마 학습이 Kengoro와 Musashi의 복잡한 근육 특성을 효과적으로 관리하는 기초 방법론을 제공한다
- 🔗 후속 연구: [[papers/1990_Human-Level_Actuation_for_Humanoids/review]] — 인간 수준의 액추에이션이 근골격 휴머노이드의 5가지 근육 특성을 더욱 효과적으로 활용할 수 있는 하드웨어적 기반을 제공한다
- 🔄 다른 접근: [[papers/1920_Explosive_Output_to_Enhance_Jumping_Ability_A_Variable_Reduc/review]] — 근육의 비선형 탄성 특성을 variable reduction과 근육 특성 관리라는 서로 다른 관점에서 활용한다
- 🏛 기반 연구: [[papers/1851_Control_of_Humanoid_Robots_with_Parallel_Mechanisms_using_Di/review]] — 병렬 구동 메커니즘의 미분가능한 해석 모델이 근골격 휴머노이드의 복잡한 근육 특성을 효율적으로 계산하고 관리하는 데 필요한 수학적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1859_DecARt_Leg_Design_and_Evaluation_of_a_Novel_Humanoid_Robot_L/review]] — 근골격 로봇의 복잡한 근육 시스템과 DecARt Leg의 decoupled actuation은 휴머노이드 구동에 대한 서로 다른 설계 철학을 보여준다.
- 🧪 응용 사례: [[papers/2130_OSMO_Open-Source_Tactile_Glove_for_Human-to-Robot_Skill_Tran/review]] — 근골격 근육 특성의 관리 방법론이 OSMO 촉각 장갑의 인간-로봇 스킬 전이에서 근력 및 촉각 피드백 매핑에 실용적으로 적용될 수 있다
- 🏛 기반 연구: [[papers/1618_PIMBS_Efficient_Body_Schema_Learning_for_Musculoskeletal_Hum/review]] — 근골격 시스템의 특성 분석을 바탕으로 PIMBS의 physics-informed learning 설계
- 🧪 응용 사례: [[papers/1851_Control_of_Humanoid_Robots_with_Parallel_Mechanisms_using_Di/review]] — 병렬 구동 메커니즘의 미분가능한 해석이 근골격 휴머노이드의 복잡한 근육-텐던 시스템의 정확한 동역학 모델링에 실질적으로 응용된다.
- 🏛 기반 연구: [[papers/1919_Exceeding_the_Maximum_Speed_Limit_of_the_Joint_Angle_for_the/review]] — 근골격 휴머노이드의 근육 특성 관리 방법론이 중복 힘줄 구동에서 관절 각속도 한계를 초과하는 방법의 이론적 기반을 제공한다
- 🔗 후속 연구: [[papers/1990_Human-Level_Actuation_for_Humanoids/review]] — 근육 특성 관리가 Human-Level Actuation Score 계산에 필수적인 생체역학적 요소를 확장한다.
- 🏛 기반 연구: [[papers/2054_Learning_Humanoid_Arm_Motion_via_Centroidal_Momentum_Regular/review]] — 인간의 팔 스윙에서 영감을 받은 제어가 근골격 시스템에서의 근육 특성 및 활용에 대한 이해를 기반으로 한다.
