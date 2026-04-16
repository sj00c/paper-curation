---
title: "1904_EgoVLA_Learning_Vision-Language-Action_Models_from_Egocentri"
authors:
  - "Ruihan Yang"
  - "Qinxi Yu"
  - "Yecheng Wu"
  - "Rui Yan"
  - "Borui Li"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "egocentric human 비디오로부터 Vision-Language-Action (VLA) 모델을 학습하여 로봇 조작 정책을 획득하고, Inverse Kinematics과 retargeting을 통해 인간 행동을 로봇 행동으로 변환한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Egocentric_Manipulation_Imitation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yang et al._2025_EgoVLA Learning Vision-Language-Action Models from Egocentric Human Videos.pdf"
---

# EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos

> **저자**: Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, Hongxu Yin, Sifei Liu, Song Han, Yao Lu, Xiaolong Wang | **날짜**: 2025-07-16 | **URL**: [https://arxiv.org/abs/2507.12440](https://arxiv.org/abs/2507.12440)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: EgoVLA. Our vision-language-action model learns manipulation skills from egocentric human*

egocentric human 비디오로부터 Vision-Language-Action (VLA) 모델을 학습하여 로봇 조작 정책을 획득하고, Inverse Kinematics과 retargeting을 통해 인간 행동을 로봇 행동으로 변환한다.

## Motivation

- **Known**: 대규모 실제 로봇 데이터 수집은 로봇 조작 학습에 효과적이지만 로봇 하드웨어 요구로 인해 데이터 규모가 제한된다. VLA 모델은 다중모드 인식-행동 통합에서 강한 성능을 보인다.
- **Gap**: 현존하는 VLA 모델은 로봇 데이터에 의존하여 확장성이 떨어지며, egocentric human 비디오의 풍부한 장면과 작업 다양성을 활용하지 못한다.
- **Why**: 인간 비디오는 로봇 데이터보다 대규모이고 다양한 환경과 작업을 포함하며, 80억의 인간이 전 세계 환경에서 조작 행동을 수행하므로 이를 활용하면 로봇 정책 학습의 확장성과 견고성을 크게 향상할 수 있다.
- **Approach**: NVILA-2B backbone 기반 VLA를 egocentric human manipulation 데이터셋에서 학습하고, unified action space (MANO hand parameters)를 통해 인간 행동을 로봇 행동으로 변환한 후, 소수의 로봇 시연으로 fine-tuning한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Unified Action Space: MANO hand parameters are used as a shared action space for humans and*

- **대규모 egocentric human 데이터셋 구성**: HOI4D, HOT3D, HoloAssist, TACO로부터 약 500,000개의 image-action pair를 통합하여 다양한 조작 작업 커버
- **Unified action space 설계**: MANO hand parameters를 공유 표현으로 사용하여 인간과 로봇 간 행동 변환 가능하게 구현
- **Ego Humanoid Manipulation Benchmark 제안**: 12개의 다양한 bimanual manipulation 작업을 포함한 시뮬레이션 벤치마크 구축
- **상당한 성능 향상**: baseline 대비 short-horizon 및 long-horizon 작업에서 유의미한 개선을 달성하고 visual observation과 spatial location에 걸친 일반화 능력 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: EgoVLA takes visual history, language instruction, and action query token as input. The latent fea-*

- egocentric RGB observations, wrist poses, hand poses, camera poses를 포함한 인간 비디오 데이터셋 구성
- world-frame camera poses를 사용하여 future wrist positions를 현재 camera frame에 투영하여 일관성 있는 supervision 보장
- 3 FPS 샘플링으로 6개의 RGB frames (1초 history) 및 language instructions, action query tokens, human proprioception state를 입력으로 VLA 학습
- MANO hand parameters로 표현된 인간 행동을 Inverse Kinematics와 retargeting을 통해 로봇 action space로 변환
- 인간 VLA로부터 적은 수의 로봇 시연으로 fine-tuning하여 최종 로봇 정책 EgoVLA 획득
- NVIDIA IsaacSim 기반 Ego Humanoid Manipulation Benchmark에서 다양한 specialist 및 generalist baseline 대비 평가

## Originality

- egocentric human 비디오를 VLA 학습의 primary source로 활용하여 기존의 로봇 데이터 의존성 극복
- unified action space (MANO hand parameters)를 통한 인간-로봇 embodiment gap bridging 방식이 기하학적 변환만으로 행동 변환 가능하게 설계
- 대규모 인간 egocentric 데이터와 소량의 로봇 시연을 결합한 hybrid training 전략
- bimanual dexterous manipulation에 특화된 Ego Humanoid Manipulation Benchmark 제안

## Limitation & Further Study

- MANO hand parameters 기반 action space가 모든 로봇 hand morphology를 충분히 표현하지 못할 가능성
- HoloAssist 데이터의 noisy hand pose annotations를 1/10로 down-sampling하여 데이터 활용도 저하 가능성
- 현재 평가가 NVIDIA IsaacSim 시뮬레이션 환경에 한정되어 실제 로봇에서의 성능 검증 필요
- egocentric human 비디오와 로봇 작업 간의 embodiment gap을 완전히 해소하지 못하여 robot-specific fine-tuning이 여전히 필요
- 후속 연구로 실제 로봇 플랫폼에서의 transfer learning 성능 평가 및 다양한 로봇 morphology에 대한 일반화 능력 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 egocentric human 비디오를 활용한 VLA 학습이라는 혁신적 접근으로 로봇 데이터 수집의 확장성 문제를 효과적으로 해결하며, unified action space 설계와 종합적인 벤치마크 제안을 통해 높은 실용성과 학술적 기여를 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1903_EgoMimic_Scaling_Imitation_Learning_via_Egocentric_Video/review]] — EgoMimic의 egocentric video 프레임워크가 EgoVLA의 Vision-Language-Action 모델 학습에 기본 데이터 처리 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1901_EgoHumanoid_Unlocking_In-the-Wild_Loco-Manipulation_with_Rob/review]] — EgoHumanoid가 같은 egocentric data를 humanoid loco-manipulation으로 접근하여 EgoVLA와 다른 embodiment 관점을 제시한다.
- 🔗 후속 연구: [[papers/1812_Behavior_Foundation_Model_for_Humanoid_Robots/review]] — Behavior Foundation Model이 EgoVLA의 vision-language-action 학습을 humanoid robots에 특화된 foundation model로 확장한다.
- 🏛 기반 연구: [[papers/1915_Endowing_GPT-4_with_a_Humanoid_Body_Building_the_Bridge_Betw/review]] — EgoVLA의 Vision-Language-Action 모델 구조가 GPT-4 기반 BiBo 프레임워크의 embodied instruction compiler 설계에 기반 이론을 제공한다.
- 🧪 응용 사례: [[papers/2166_ULTRA_Unified_Multimodal_Control_for_Autonomous_Humanoid_Who/review]] — EgoVLA의 VLA 모델을 ULTRA의 통합 multimodal 제어 시스템에 적용하면 더 풍부한 언어-행동 매핑이 가능하다.
- 🏛 기반 연구: [[papers/1646_RoboMirror_Understand_Before_You_Imitate_for_Video_to_Humano/review]] — RoboMirror의 비디오-인간 모방 기법이 EgoVLA의 자아중심 비디오 기반 VLA 학습의 핵심 기반입니다.
- 🔗 후속 연구: [[papers/1961_H-RDT_Human_Manipulation_Enhanced_Bimanual_Robotic_Manipulat/review]] — H-RDT의 인간 조작 강화 양손 로봇 조작이 EgoVLA의 VLA 모델을 구체적 조작 태스크로 확장한 형태입니다.
- 🏛 기반 연구: [[papers/1412_GR00T_N1_An_Open_Foundation_Model_for_Generalist_Humanoid_Ro/review]] — EgoVLA의 egocentric vision-language-action 학습 방법론이 GR00T N1의 System 2 비전-언어 모듈 설계에 기초가 됨
- 🔄 다른 접근: [[papers/1888_DreamZero_World_Action_Models_are_Zero-shot_Policies/review]] — Vision-Language-Action 모델에 대한 포괄적 서베이와 구체적인 egocentric VLA 구현이 서로 다른 관점에서 VLA 기술을 다룬다.
- 🔗 후속 연구: [[papers/1901_EgoHumanoid_Unlocking_In-the-Wild_Loco-Manipulation_with_Rob/review]] — EgoVLA가 egocentric human video를 VLA 모델로 확장하여 EgoHumanoid의 embodiment 정렬을 더 포괄적인 언어-비전-행동 모델로 발전시킨다.
- 🔄 다른 접근: [[papers/1903_EgoMimic_Scaling_Imitation_Learning_via_Egocentric_Video/review]] — EgoVLA가 같은 egocentric video 데이터를 VLA 모델로 접근하여 EgoMimic과 다른 학습 패러다임을 제시한다.
- 🔄 다른 접근: [[papers/1915_Endowing_GPT-4_with_a_Humanoid_Body_Building_the_Bridge_Betw/review]] — 둘 다 VLM을 휴머노이드 제어에 활용하지만 BiBo는 GPT-4를, EgoVLA는 egocentric 데이터 기반 VLA를 사용한다.
- 🏛 기반 연구: [[papers/2005_Humanoid_World_Models_Open_World_Foundation_Models_for_Human/review]] — EgoVLA의 vision-language-action learning이 HWM의 egocentric video to control token 변환을 위한 기초 방법론을 제공한다.
- 🏛 기반 연구: [[papers/2012_HumanoidVLM_Vision-Language-Guided_Impedance_Control_for_Con/review]] — EgoVLA의 vision-language-action learning이 HumanoidVLM의 adaptive manipulation framework 기반이 됩니다.
- 🔄 다른 접근: [[papers/2087_LookOut_Real-World_Humanoid_Egocentric_Navigation/review]] — 자아중심적 비전-언어-행동 모델과 실제 자아중심적 네비게이션이라는 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/2099_MimicDroid_In-Context_Learning_for_Humanoid_Robot_Manipulati/review]] — EgoVLA의 vision-language-action learning이 MimicDroid의 in-context learning 기반 humanoid manipulation에 방법론적 토대를 제공했다
- 🏛 기반 연구: [[papers/2166_ULTRA_Unified_Multimodal_Control_for_Autonomous_Humanoid_Who/review]] — 자기중심 비디오에서 비전-언어-행동 모델 학습이 물리 기반 신경 리타겟팅과 통합 멀티모달 제어의 이론적 기반이 됩니다.
