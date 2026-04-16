---
title: "1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud"
authors:
  - "Zhe Li"
  - "Cheng Chi"
  - "Yangyang Wei"
  - "Boan Zhu"
  - "Tao Huang"
date: "2025.12"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboPerform은 오디오를 직접 제어 신호로 사용하여 음악에 맞춰 춤을 추거나 음성에 맞춰 제스처를 생성하는 휴머노이드 로봇 제어 프레임워크로, 명시적 모션 재구성을 제거하여 저지연 및 고충실도를 달성한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_Do You Have Freestyle Expressive Humanoid Locomotion via Audio Control.pdf"
---

# Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control

> **저자**: Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Tao Huang, Zhenguo Sun, Yibo Peng, Pengwei Wang, Zhongyuan Wang, Fangzhou Liu, Chang Xu, Shanghang Zhang | **날짜**: 2025-12-29 | **URL**: [https://arxiv.org/abs/2512.23650](https://arxiv.org/abs/2512.23650)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1.*

RoboPerform은 오디오를 직접 제어 신호로 사용하여 음악에 맞춰 춤을 추거나 음성에 맞춰 제스처를 생성하는 휴머노이드 로봇 제어 프레임워크로, 명시적 모션 재구성을 제거하여 저지연 및 고충실도를 달성한다.

## Motivation

- **Known**: 기존 휴머노이드 로봇은 사전 정의된 모션이나 희소한 텍스트 명령으로만 제어되며, 오디오-모션 생성 후 retargeting 파이프라인은 cascaded error, 높은 지연시간, 느슨한 음향-구동 매핑을 야기한다.
- **Gap**: 오디오를 implicit style 신호로 직접 활용하여 통합된 모션 생성을 하는 unified framework이 없으며, retargeting 없이 실시간 오디오-모션 정렬을 달성하는 방법이 부족하다.
- **Why**: 휴머노이드 로봇이 음악 및 음성과 같은 리치한 오디오 신호에 반응하는 표현력 있는 성능을 수행할 수 있다면 인간-로봇 상호작용의 자연스러움과 몰입감이 크게 향상될 수 있다.
- **Approach**: motion = content + style 원칙으로 오디오를 implicit style signal로 인코딩하고, ΔMoE teacher policy와 diffusion-based student policy를 통해 content latent와 audio-driven style latent를 분리하여 직접 모션을 생성한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of RoboPerform. We propose a two-stage approach: train an adaptor to inject kinematic information int*

- **First unified audio-to-locomotion framework**: 오디오를 암시적 제어 신호로 활용하는 첫 번째 통합 프레임워크로, 음악-춤과 음성-제스처 양쪽 작업을 지원한다.
- **ΔMoE 교사 정책**: Residual mixture-of-experts 아키텍처로 다양한 모션 패턴을 특화된 전문가들이 처리하며, 동적 가중치 조정을 통해 견고한 모션 추적을 실현한다.
- **Retargeting-free 설계**: 명시적 모션 재구성을 제거하여 cascaded error를 제거하고, 지연시간을 크게 감소시키며, 실시간 성능을 달성한다.
- **물리적 타당성과 오디오 정렬**: 광범위한 실험을 통해 물리적으로 그럴듯한 모션과 높은 오디오 시간 정렬을 동시에 달성함을 입증한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of RoboPerform. We propose a two-stage approach: train an adaptor to inject kinematic information int*

- Audio-motion alignment: InfoNCE loss를 사용하여 temporal attention augmented adaptor로 raw audio latents를 motion latents와 정렬
- ΔMoE teacher policy: 3D conditional inputs를 4개의 nested subspaces로 분할하고 gating network로 residual fusion을 통해 동적 가중치 조정
- Content-style decomposition: Text-to-motion model에서 추출한 high-level content latent와 audio-driven style latent를 분리
- Diffusion-based student policy: Content latent와 temporally-aligned style latent로 guided denoising을 통해 executable actions 생성
- Knowledge distillation: Teacher policy의 지식을 student policy에 증류하여 효율성과 성능 균형

## Originality

- 오디오를 첫 번째 implicit control modality로 활용하는 novel perspective로, 기존 language-guided나 motion-replay 패러다임에서 벗어남
- Motion decomposition (content + style)을 통한 새로운 latent-driven framework로, retargeting-free 설계를 처음으로 audio-driven locomotion에 적용
- ΔMoE의 residual fusion 구조로 기존 orthogonal MoE와 차별화되는 전문가 혼합 방식 제안
- InfoNCE-optimized audio-motion alignment module을 통해 kinematic priors를 audio에 직접 임베딩

## Limitation & Further Study

- 실제 로봇 배포 실험이 논문에 명확히 제시되지 않아 sim-to-real 갭에 대한 검증 필요
- Content와 style의 분리 정도에 따른 성능 변화에 대한 상세 분석 부족
- 복잡한 다중 오디오 신호(음악 + 음성 동시) 처리에 대한 확장성 미검증
- 후속연구: 실제 로봇 플랫폼에서의 제어 안정성 및 일반화 성능 평가, 더 다양한 장르/언어의 오디오에 대한 적응성 강화, visual feedback을 포함한 closed-loop 제어 시스템 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboPerform은 오디오 제어 신호를 휴머노이드 로봇 모션에 직접 통합하는 novel한 접근으로, retargeting-free 설계와 content-style decomposition을 통해 저지연 고충실도 실시간 성능을 달성한 의미 있는 기여이다. 다만 실제 로봇 배포 및 sim-to-real 검증이 추가되면 실용성이 더욱 강화될 것이다.

## Related Papers

- 🏛 기반 연구: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — semantic co-speech gesture synthesis가 audio-controlled humanoid locomotion의 음성-동작 매핑에 대한 기본 원리를 제공한다.
- 🔄 다른 접근: [[papers/1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables/review]] — RobotDancing이 음악과 움직임의 연결을 residual-action RL로 접근하여 RoboPerform과 다른 기술적 해결책을 제시한다.
- 🔗 후속 연구: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — real-time text-driven motion control이 RoboPerform의 audio control을 텍스트 모달리티로 확장하여 더 다양한 입력 방식을 지원한다.
- 🔗 후속 연구: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — RoboPerform의 오디오 제어 프레임워크가 언어 기반 locomotion과 결합되어 더 풍부한 multimodal humanoid control을 실현할 수 있다.
- 🔄 다른 접근: [[papers/1865_Design_and_Control_of_a_Bipedal_Robotic_Character/review]] — 표현적 인간형 운동을 위한 다른 실시간 제어 방식을 제시합니다.
- 🔗 후속 연구: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — 표현적 모션 시퀀스 생성으로 오디오 기반 제어가 발전됩니다.
- 🏛 기반 연구: [[papers/1624_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_A/review]] — 자유형 휴머노이드 로코모션이 PRIMAL의 물리적 반응성과 제어 가능한 3D 캐릭터 애니메이션의 기반 기술
- 🔗 후속 연구: [[papers/1865_Design_and_Control_of_a_Bipedal_Robotic_Character/review]] — 이족 로봇 캐릭터의 표현적 동작이 Do You Have Freestyle의 자율적 표현형 휴머노이드 로코모션으로 확장되어 더 자유로운 동작 표현을 가능하게 한다.
- 🏛 기반 연구: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — 표현적 휴머노이드 보행이 감정적 모션 생성의 기반이 되는 기술이다.
- 🔗 후속 연구: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — Do You Have Freestyle의 표현적 보행이 HIAER의 감정 맥락 기반 동작 생성을 확장합니다.
- 🔄 다른 접근: [[papers/2073_Learning_to_Walk_in_Costume_Adversarial_Motion_Priors_for_Ae/review]] — 자율 휴머노이드 보행을 통한 표현적 보행과 미적 제약 하 자연스러운 보행이라는 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/2156_Towards_Motion_Turing_Test_Evaluating_Human-Likeness_in_Huma/review]] — expressive locomotion 연구에 Motion Turing Test를 적용하면 인간다운 표현력의 정량적 평가가 가능해짐
