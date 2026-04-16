---
title: "2070_Learning_to_Look_Around_Enhancing_Teleoperation_and_Learning"
authors:
  - "Bipasha Sen"
  - "Michelle Wang"
  - "Nandini Thakur"
  - "Aditya Agarwal"
  - "Pulkit Agrawal"
date: "2024.11"
doi: ""
arxiv: ""
score: 4.0
essence: "인간의 자연스러운 머리 움직임을 모방하는 5-DOF actuated neck을 원격 조종 시스템에 통합하여 작업자의 직관성 향상, 인지 부하 감소, 자율 정책 학습 개선을 달성하는 연구이다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/Portable_Humanoid_Teleoperation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Sen et al._2024_Learning to Look Around Enhancing Teleoperation and Learning with a Human-like Actuated Neck.pdf"
---

# Learning to Look Around: Enhancing Teleoperation and Learning with a Human-like Actuated Neck

> **저자**: Bipasha Sen, Michelle Wang, Nandini Thakur, Aditya Agarwal, Pulkit Agrawal | **날짜**: 2024-11-01 | **URL**: [https://arxiv.org/abs/2411.00704](https://arxiv.org/abs/2411.00704)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: A teleoperation system featuring an actuated neck and dexterous arms, enabling human-like manipu-*

인간의 자연스러운 머리 움직임을 모방하는 5-DOF actuated neck을 원격 조종 시스템에 통합하여 작업자의 직관성 향상, 인지 부하 감소, 자율 정책 학습 개선을 달성하는 연구이다.

## Motivation

- **Known**: 원격 조종 시스템은 직접적인 데이터 수집 방식을 제공하지만 제한된 시야각과 직관성 부족으로 어려움을 겪고 있다. 인간은 머리와 목 움직임을 통해 복잡한 공간을 자연스럽게 인지한다.
- **Gap**: 기존 원격 조종 시스템은 정적인 광각 카메라만 사용하여 폐색 처리와 동적 시점 조정이 제한되며, 이는 모방 학습 데이터의 분포 이동(distribution shift) 문제를 야기한다. 인간의 자연스러운 지각 능력을 시뮬레이션하는 원격 조종 시스템이 부재하다.
- **Why**: 작업자의 인지 부하를 감소시키고 복잡한 전신 조작 능력을 향상시키며, 고품질의 데이터를 수집하여 자율 로봇의 정책 학습 성능을 개선할 수 있다.
- **Approach**: 5-DOF actuated neck을 탑재한 인간형 로봇 시스템을 설계하고, Apple Vision Pro의 머리 추적과 hand tracking 기술을 통해 직관적인 텔레오퍼레이션을 실현한다. 이를 통해 7개의 원격 조종 작업과 3개의 자율 정책 학습 작업에서 효과를 검증한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: A teleoperation system featuring an actuated neck and dexterous arms, enabling human-like manipu-*

- **직관적 원격 조종**: 5-DOF actuated neck으로 인간 같은 머리 움직임(회전, 기울임, 피킹)을 구현하여 작업자의 인지 부하를 감소시킴
- **개선된 데이터 품질**: 표준 RGB 카메라와 동적 카메라 조정으로 왜곡 없는 고품질 이미지 획득 및 인식 오류 최소화
- **향상된 대화형 지각**: 동적 물체 추적과 폐색 관리를 통해 자연스러운 인간 행동 모방 및 다양한 작업 적응성 입증
- **자율 정책 학습 개선**: actuated neck이 공간 인식 향상, 분포 이동 감소, 작업별 적응 조정을 지원함을 3개 작업에서 입증

## How


- Universal Robotics UR5e 듀얼 암(각 5kg 페이로드), Interbotix WidowX-200 5-DOF neck, Husarion Panther 모바일 베이스로 구성된 인간형 로봇 시스템 구축
- Apple Vision Pro를 통한 6-DOF 머리 추적으로 작업자의 머리 포즈를 로봇 neck 카메라 포즈에 직접 매핑
- Ascension trakSTAR와 Manus VR 장갑을 이용한 정밀한 손 추적으로 그리퍼 조작 제어
- Intel Realsense D405 카메라 4개를 neck, torso, wrist에 배치하여 멀티 뷰 감지 정보 수집
- 7개의 원격 조종 작업(coat hanger finding 등)과 3개의 자율 정책 학습 작업에서 성능 비교 평가
- imitation learning을 통해 teleoperation 데이터로부터 다중 작업 정책 학습 및 일반화 능력 검증

## Originality

- 인간의 목 움직임을 시스템적으로 원격 조종 플랫폼에 통합한 최초 시도로, 피킹(peeking)을 통한 폐색 관리 능력 구현
- 동적 카메라 조정이 imitation learning에서 distribution shift를 감소시킬 수 있음을 실증적으로 입증
- 멀티모달 입력(머리 추적 + 손 추적)과 다양한 센서(RGB, proprioception)를 통합한 완전한 원격 조종 시스템 구현
- interactive perception 개념을 actuated neck으로 실현하여 시간 경과에 따른 물체 추적 학습 지원

## Limitation & Further Study

- Apple Vision Pro를 이용한 손 추적이 로봇 신체 근처 작업에서 시야 벗어남 문제 발생, 향후 안정적 손 추적 기술 개선 필요
- 7개 원격 조종 작업과 3개 학습 작업 구성이 제한적이며, 더 다양한 환경과 작업에 대한 일반화 검증 필요
- actuated neck의 2m/s 모바일 베이스 속도가 인간 보행 속도에 미치지 못할 수 있으며, 불균형한 지형에서의 안정성 추가 검증 필요
- 5-DOF neck의 정확한 동작학(kinematics) 모델링과 정밀도 한계에 대한 분석 부재
- haptic feedback 시스템 미통합으로 원격 조종의 몰입감 제한, 향후 촉각 피드백 통합 고려 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 인간의 자연스러운 지각 능력을 원격 조종 시스템에 구현한 혁신적 접근으로, 직관성 향상과 자율 정책 학습 개선에 대한 실증적 증거를 제시한다. 다만 평가 작업의 범위 확대와 기술적 한계 개선을 통해 더욱 강화될 수 있다.

## Related Papers

- 🏛 기반 연구: [[papers/1750_Vision_in_Action_Learning_Active_Perception_from_Human_Demon/review]] — Learning to Look Around의 능동적 머리 움직임이 Vision in Action의 인간 시연에서 배운 능동 인식 원리를 휴머노이드 텔레오퍼레이션에 적용한 것이다.
- 🔗 후속 연구: [[papers/2124_Open-TeleVision_Teleoperation_with_Immersive_Active_Visual_F/review]] — Learning to Look Around의 5-DOF actuated neck을 Open-TeleVision의 VR 기반 몰입형 시각 피드백과 결합하여 더 직관적인 원격 조종이 가능하다.
- 🔄 다른 접근: [[papers/1879_DIJIT_A_Robotic_Head_for_an_Active_Observer/review]] — Learning to Look Around은 텔레오퍼레이션용 능동 목 제어, DIJIT은 일반적인 능동 관찰자용 로봇 헤드로 서로 다른 응용 목적을 가진다.
- 🏛 기반 연구: [[papers/1750_Vision_in_Action_Learning_Active_Perception_from_Human_Demon/review]] — 텔레오퍼레이션과 학습 향상에서 능동적 시각 탐색이 look-around 행동과 유사한 메커니즘을 사용한다.
- 🏛 기반 연구: [[papers/1866_Development_of_an_Intuitive_GUI_for_Non-Expert_Teleoperation/review]] — 텔레조작과 학습을 향상시키는 look-around 기술이 비전문가 GUI의 직관적인 인터페이스 설계에 필요한 시각적 피드백 기반을 제공한다
- 🔄 다른 접근: [[papers/2071_Learning_to_Look_Seeking_Information_for_Decision_Making_via/review]] — 원격 조작과 학습을 위한 시각적 탐색 향상과 능동적 정보 탐색이라는 다른 접근법을 사용한다.
- 🧪 응용 사례: [[papers/2124_Open-TeleVision_Teleoperation_with_Immersive_Active_Visual_F/review]] — Learning to Look Around의 텔레오퍼레이션 향상 기법이 Open-TeleVision의 능동적 카메라 제어와 결합되어 더 효과적인 원격 조종을 가능하게 한다.
