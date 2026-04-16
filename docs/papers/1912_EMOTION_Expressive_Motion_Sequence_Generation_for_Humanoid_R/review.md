---
title: "1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R"
authors:
  - "Peide Huang"
  - "Yuhan Hu"
  - "Nataliya Nechyporenko"
  - "Daehwa Kim"
  - "Walter Talbott"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "EMOTION은 대규모 언어 모델(LLM)의 문맥 학습 능력을 활용하여 인간형 로봇이 표정, 제스처, 신체 움직임 등 자연스러운 비언어적 의사소통을 수행할 수 있도록 하는 프레임워크이다. 온라인 사용자 연구를 통해 생성된 모션이 인간 수행자와 동등하거나 우수함을 입증했다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2024_EMOTION Expressive Motion Sequence Generation for Humanoid Robots with In-Context Learning.pdf"
---

# EMOTION: Expressive Motion Sequence Generation for Humanoid Robots with In-Context Learning

> **저자**: Peide Huang, Yuhan Hu, Nataliya Nechyporenko, Daehwa Kim, Walter Talbott, Jian Zhang | **날짜**: 2024-10-30 | **URL**: [https://arxiv.org/abs/2410.23234](https://arxiv.org/abs/2410.23234)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of the EMOTION framework.*

EMOTION은 대규모 언어 모델(LLM)의 문맥 학습 능력을 활용하여 인간형 로봇이 표정, 제스처, 신체 움직임 등 자연스러운 비언어적 의사소통을 수행할 수 있도록 하는 프레임워크이다. 온라인 사용자 연구를 통해 생성된 모션이 인간 수행자와 동등하거나 우수함을 입증했다.

## Motivation

- **Known**: 로봇의 표현적 행동이 인간-로봇 상호작용을 개선할 수 있으며, 전통적으로 수작업으로 제작된 모션 시퀀스나 사전 녹음된 궤적에 의존하는 방법이 사용되어 왔다.
- **Gap**: 기존 방법들은 인간 비언어 의사소통의 다양성과 미묘함을 충분히 모방하지 못하며, 무한한 수의 다양한 제스처를 위해 인간이 직접 엔지니어링한 모션 프리미티브가 필요하다.
- **Why**: 인간형 로봇의 자연스러운 제스처 생성은 사용자의 만족도와 몰입도를 증대시키고, 로봇의 사회적 수용성을 높이는 데 중요하다.
- **Approach**: LLM과 vision-language model의 in-context learning 능력을 활용하여 사회적 맥락에서 표현적 모션 시퀀스를 동적으로 생성하며, 인간 피드백을 통해 반복적으로 개선하는 EMOTION++ 버전도 제시한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of the EMOTION framework.*

- **제스처 생성 능력**: 10개의 서로 다른 표현적 제스처(thumbs-up, wave, stop 등)를 자동으로 생성할 수 있으며, 일부 제스처에서는 인간 수행자보다 우수한 자연스러움과 이해도를 달성했다.
- **인간 피드백 통합**: EMOTION++가 EMOTION보다 자연스러움과 이해도 측면에서 유의미하게 우수함을 보여주었다.
- **설계 시사점**: 손 위치, 움직임 패턴, 팔과 어깨 관절, 손가락 자세, 속도 등 로봇 제스처의 인간 지각에 영향을 미치는 주요 변수들을 식별했다.

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of the EMOTION framework.*

- 사용자 언어 지시, 로봇 이미지 관찰을 입력으로 받아 LLM이 연속값 모션 시퀀스(cartesian position, euler angle, finger state)를 텍스트로 생성
- 생성된 모션 시퀀스에 inverse kinematics를 적용하여 로봇의 관절 명령으로 변환
- trajectory interpolation과 trajectory tracking을 통해 로봇에서 실행
- 인간 피드백이 제공되면 LLM에 해당 피드백을 문맥으로 추가하여 모션 시퀀스를 반복 개선
- skeleton detection, motion retargeting, down-sampling을 통해 인간 데모로부터 모션 학습 지원

## Originality

- 기존의 GenEM과 달리, 사전 정의된 고수준 스킬 라이브러리 없이 LLM이 직접 복잡한 손과 손가락 궤적을 최소한의 예제로 생성하는 점이 혁신적이다.
- 조작(manipulation) 또는 이동(locomotion) 정책이 아닌 인간-로봇 상호작용 영역에 LLM 기반 시퀀스 생성을 적용한 점이 차별화된다.
- 자연언어 인간 피드백을 직접적으로 모션 시퀀스 개선에 통합하는 반복적 개선 방식이 새롭다.

## Limitation & Further Study

- 평가된 제스처가 10개로 제한적이며, 일부 제스처(listening, jazz-hands)는 3점 미만의 낮은 평가를 받아 모든 제스처에서 성능이 일정하지 않다.
- 온라인 사용자 연구만 수행되었으며, 실제 로봇-인간 상호작용 시나리오에서의 성능 검증이 부족하다.
- LLM의 출력이 항상 유효한 모션 시퀀스를 생성하는지, 또는 에러 처리 메커니즘이 어떻게 작동하는지 명확하지 않다.
- **후속 연구**: 더 광범위한 제스처 집합에 대한 평가, 실제 인간-로봇 상호작용 환경에서의 장시간 평가, LLM의 신뢰성 및 안정성 개선, 다양한 로봇 플랫폼으로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: EMOTION은 LLM의 in-context learning을 창의적으로 활용하여 인간형 로봇의 표현적 모션 생성을 자동화한 실질적 솔루션을 제시한다. 사용자 연구를 통한 검증과 인간 피드백 통합 방식은 실용성을 높이나, 다양한 제스처에 대한 성능 편차와 실제 상호작용 환경 테스트의 필요성이 향후 과제로 남아 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — LLM 기반 표현적 모션 생성과 의미적 공동 발화 제스처 합성은 모두 자연스러운 인간형 표현을 목표로 한다.
- 🔗 후속 연구: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 실시간 텍스트 기반 휴머노이드 모션 제어가 표현적 모션 시퀀스 생성의 실시간 적용이다.
- 🏛 기반 연구: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — 표현적 휴머노이드 보행이 감정적 모션 생성의 기반이 되는 기술이다.
- 🔄 다른 접근: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — 둘 다 언어를 휴머노이드 동작으로 변환하지만 EMOTION은 비언어적 의사소통을, RoboGhost는 retargeting-free 제어를 중심으로 한다.
- 🏛 기반 연구: [[papers/1915_Endowing_GPT-4_with_a_Humanoid_Body_Building_the_Bridge_Betw/review]] — EMOTION의 LLM 기반 모션 생성이 GPT-4를 휴머노이드 제어에 활용하는 BiBo 프레임워크의 기반 기술을 제공한다.
- 🔗 후속 연구: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — EMOTION의 표현적 모션 생성을 Hierarchical Intention-Aware 프레임워크와 결합하면 더 복잡한 의도 기반 휴머노이드 행동이 가능하다.
- 🔗 후속 연구: [[papers/1624_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_A/review]] — EMOTION의 표현적 휴머노이드 동작 생성이 PRIMAL의 반응형 모터 모델을 감정적 표현으로 확장한 형태
- 🏛 기반 연구: [[papers/1634_Realistic_Lip_Motion_Generation_Based_on_3D_Dynamic_Viseme_a/review]] — EMOTION의 표현적 모션 생성 기술이 입술 운동의 감정적 표현력을 향상시키는 기반이 된다
- 🔄 다른 접근: [[papers/1865_Design_and_Control_of_a_Bipedal_Robotic_Character/review]] — Design and Control of Bipedal Robotic Character와 EMOTION 모두 휴머노이드의 표현적 동작을 다루지만 연극적 성능 vs 감정적 동작 시퀀스로 서로 다른 예술적 목표를 추구한다.
- 🔗 후속 연구: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — 표현적 모션 시퀀스 생성으로 오디오 기반 제어가 발전됩니다.
- 🔗 후속 연구: [[papers/1893_ECHO_Edge-Cloud_Humanoid_Orchestration_for_Language-to-Motio/review]] — EMOTION의 언어 기반 표현적 동작 생성이 ECHO의 diffusion 기반 text-to-motion 생성기를 더욱 풍부하고 자연스럽게 확장할 수 있다.
- 🔄 다른 접근: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — 둘 다 언어를 휴머노이드 동작으로 변환하지만 RoboGhost는 retargeting-free를, EMOTION은 표현적 비언어 의사소통을 중심으로 한다.
- 🔄 다른 접근: [[papers/1936_From_Motion_to_Behavior_Hierarchical_Modeling_of_Humanoid_Ge/review]] — 둘 다 표현력 있는 humanoid motion 생성을 다루지만, PHYLOMAN은 계층적 행동 계획에, EMOTION은 expressive sequence generation에 집중합니다.
- 🔗 후속 연구: [[papers/1915_Endowing_GPT-4_with_a_Humanoid_Body_Building_the_Bridge_Betw/review]] — BiBo 프레임워크가 EMOTION의 LLM 기반 모션 생성을 확장하여 더 복잡한 개방형 환경 상호작용을 가능하게 한다.
- 🔗 후속 연구: [[papers/1968_Harmon_Whole-Body_Motion_Generation_of_Humanoid_Robots_from/review]] — Harmon의 언어 기반 동작 생성을 감정적 표현까지 확장한 EMOTION의 발전된 형태다.
- 🔄 다른 접근: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — EMOTION의 expressive motion generation이 HIAER과 다른 방식으로 감정적 휴머노이드 동작을 생성합니다.
- 🔄 다른 접근: [[papers/2039_LangWBC_Language-directed_Humanoid_Whole-Body_Control_via_En/review]] — 둘 다 언어 기반 휴머노이드 제어이지만 LangWBC는 end-to-end 전신 제어, EMOTION은 감정 표현 모션 생성 중심
- 🔗 후속 연구: [[papers/2168_UniAct_Unified_Motion_Generation_and_Action_Streaming_for_Hu/review]] — UniAct의 multimodal 명령 처리를 EMOTION의 expressive motion sequence generation과 결합하면 더 감정적이고 표현적인 실시간 휴머노이드 제어가 가능합니다.
