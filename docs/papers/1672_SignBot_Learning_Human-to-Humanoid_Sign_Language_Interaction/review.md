---
title: "1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction"
authors:
  - "Guanren Qiao"
  - "Sixu Lin"
  - "Ronglai Zuo"
  - "Zhizheng Wu"
  - "Kui Jia"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "SignBot은 수화 언어를 인식하고 생성할 수 있는 인간형 로봇을 위한 프레임워크로, motion retargeting, policy training, 그리고 generative interaction을 통합하여 청각장애인과의 자연스러운 상호작용을 실현한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Qiao et al._2025_SignBot Learning Human-to-Humanoid Sign Language Interaction.pdf"
---

# SignBot: Learning Human-to-Humanoid Sign Language Interaction

> **저자**: Guanren Qiao, Sixu Lin, Ronglai Zuo, Zhizheng Wu, Kui Jia, Guiliang Liu | **날짜**: 2025-05-30 | **URL**: [https://arxiv.org/abs/2505.24266](https://arxiv.org/abs/2505.24266)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of SignBot: The framework consists of three stages: (1) Motion Retargeting aligns human sign language*

SignBot은 수화 언어를 인식하고 생성할 수 있는 인간형 로봇을 위한 프레임워크로, motion retargeting, policy training, 그리고 generative interaction을 통합하여 청각장애인과의 자연스러운 상호작용을 실현한다.

## Motivation

- **Known**: 최근 computer vision과 LLM의 발전으로 수화 생성, 번역, 인식이 향상되었으나, 이러한 시스템들은 실제 물리적 상호작용을 제공하지 못한다. 인간형 로봇의 발전으로 embodied AI를 통한 실제 상호작용이 가능해졌다.
- **Gap**: 기존 teleoperation 방식은 자동성이 부족하고, learning-based control은 손가락의 복잡한 움직임을 다루지 못하며, 대부분의 dexterous hand는 DoF와 손목 유연성이 제한적이다.
- **Why**: 청각장애인(DHH) 커뮤니티의 의사소통 접근성 향상과 소수 언어 사용자와의 상호작용 촉진이 중요하며, embodied AI를 통한 물리적 상호작용이 실제 사회 영향을 미칠 수 있다.
- **Approach**: SignBot은 세 가지 주요 컴포넌트로 구성된다: (1) 인간 수화를 로봇 kinematics로 변환하는 motion retargeting, (2) decoupled upper/lower body policies로 simulation에서 학습하는 policy training, (3) translator, responder, generator를 통합한 generative interaction 모듈.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: An example of real-world interaction between the robot and the human customer.*

- **인간-로봇 상호작용 프레임워크**: 청각장애인 커뮤니티와 로봇 간 seamless한 수화 의사소통을 가능하게 하는 통합 시스템 개발
- **정확한 수화 실행**: 다양한 인간 수화 동작에 강건하게 적응하는 로봇 제어 정책으로 안정적이고 정확한 수화 표현 달성
- **도메인 적응성**: Sim-to-Real 전이를 통해 다양한 로봇과 데이터셋에 대한 적응 및 일반화 능력 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of SignBot: The framework consists of three stages: (1) Motion Retargeting aligns human sign language*

- Human sign language video mesh에서 motion 추출 후, body와 hand를 분리하여 retargeting 수행
- Dual T-Pose를 spatial alignment reference로 사용하여 human skeleton과 robot skeleton 간 mapping
- Upper body는 imitation learning으로 target sign language pose를 추적, lower body는 RL policy로 안정성 유지
- POMDP 기반 robot learning 환경 정의로 proprioception과 goal imitation으로 구성된 observation space 활용
- Sign language translation function (fT), responding function (fR), generation function (fG)를 통한 closed-loop interaction pipeline 구성
- Conditional sequence generation으로 text 입력으로부터 SMPL-X 기반 sign language 시퀀스 생성

## Originality

- 처음으로 embodied humanoid robot에서 autonomous sign language interaction을 구현한 연구로, 기존 teleoperation 방식의 자동성 부족 문제 해결
- Decoupled policy 접근으로 upper body의 복잡한 hand gesture와 lower body의 안정성을 분리하여 처리하는 신규 방식
- Sign language processing의 translation, response, generation 세 가지 모듈을 통합하여 closed-loop interaction 구현
- Motion retargeting에서 추가 DoF를 도입하여 로봇의 자연스러운 수화 표현 향상

## Limitation & Further Study

- 대부분의 dexterous hand가 제한된 DoF를 가지고 있어 수화의 세부 표현에 제약 가능성
- Hand retargeting 방법에 대한 상세 설명이 부족하여 손가락의 복잡한 움직임 처리 방식이 명확하지 않음
- 다양한 sign language dialect와 지역별 변이에 대한 적응성 검증 필요
- Real-world interaction 실험의 규모와 정량적 평가 지표가 제한적일 수 있음
- 후속 연구는 더 많은 DoF를 가진 dexterous hand 개발, 다국어 수화 처리, 대규모 사용자 연구를 통한 사회적 영향 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SignBot은 embodied humanoid robot에서 처음으로 자동화된 sign language interaction을 구현한 혁신적 연구로, 청각장애인 커뮤니티의 의사소통 접근성 향상에 실질적 기여를 한다. 다만 hand retargeting 기술의 상세 설명과 더 광범위한 실세계 평가가 보완되면 영향력이 더욱 증대될 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — 음성-제스처 생성의 다중 모달 프레임워크가 SignBot의 수화 인식/생성을 위한 기본 상호작용 구조
- 🔗 후속 연구: [[papers/1634_Realistic_Lip_Motion_Generation_Based_on_3D_Dynamic_Viseme_a/review]] — 입술 운동 생성을 포함한 SignBot의 수화 시스템이 전체적인 인간-휴머노이드 소통으로 확장
- 🔄 다른 접근: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — 계층적 의도 인식 표현과 수화 언어 상호작용은 휴머노이드 소통의 서로 다른 표현 방식
- 🔄 다른 접근: [[papers/1750_Vision_in_Action_Learning_Active_Perception_from_Human_Demon/review]] — 인간-로봇 상호작용에서 수화 언어와 능동적 지각이라는 서로 다른 소통 방식을 다루지만 모두 텔레오퍼레이션 기술을 활용한다.
- 🔗 후속 연구: [[papers/1756_Whole-Body_Bilateral_Teleoperation_with_Multi-Stage_Object_P/review]] — 휴머노이드의 인간과의 상호작용에서 의사소통(수화)과 물리적 협력(물체 조작)이라는 보완적 기능을 다룬다.
- 🏛 기반 연구: [[papers/1873_Dexterous_Teleoperation_of_20-DoF_ByteDexter_Hand_via_Human/review]] — 인간의 손 동작을 로봇이 모방하는 과제에서 수화와 손가락 조작이라는 관련 영역을 다룬다.
- 🏛 기반 연구: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — 언어에서 운동으로의 retargeting 기술이 SignBot의 수화 동작 생성에 필요한 기반 방법론이다
- 🔗 후속 연구: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — SignBot의 수화 상호작용이 음성-제스처 생성을 시각적 언어로 확장한 포괄적 소통 시스템
- 🔗 후속 연구: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — SENTINEL의 언어-행동 모델과 SignBot의 수화 상호작용을 결합하면 다중 모달 의사소통이 가능한 휴머노이드를 구현할 수 있다
- 🔗 후속 연구: [[papers/1634_Realistic_Lip_Motion_Generation_Based_on_3D_Dynamic_Viseme_a/review]] — SignBot의 수화 인식/생성이 입술 운동 생성을 포함한 다중 모달 소통 시스템으로 확장된 형태
- 🔄 다른 접근: [[papers/1750_Vision_in_Action_Learning_Active_Perception_from_Human_Demon/review]] — 인간-로봇 상호작용에서 능동적 지각과 수화 언어라는 서로 다른 소통 방식을 VR 텔레오퍼레이션을 통해 학습한다.
- 🔄 다른 접근: [[papers/1756_Whole-Body_Bilateral_Teleoperation_with_Multi-Stage_Object_P/review]] — 휴머노이드의 인간과의 상호작용에서 물리적 협력(물체 조작)과 의사소통(수화)이라는 서로 다른 상호작용 방식을 다룬다.
