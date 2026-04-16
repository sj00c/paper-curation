---
title: "1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro"
authors:
  - "Zhe Li"
  - "Cheng Chi"
  - "Yangyang Wei"
  - "Boan Zhu"
  - "Yibo Peng"
date: "2025.10"
doi: "10.48550/arXiv.2510.14952"
arxiv: ""
score: 4.0
essence: "RoboGhost는 언어 지시를 humanoid 로봇의 실행 가능한 동작으로 직접 변환하는 retargeting-free 프레임워크로, motion latent을 조건으로 하는 diffusion-based policy를 통해 기존의 다단계 파이프라인의 누적 오류와 지연을 제거한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_From Language to Locomotion Retargeting-free Humanoid Control via Motion Latent Guidance.pdf"
---

# From Language to Locomotion: Retargeting-free Humanoid Control via Motion Latent Guidance

> **저자**: Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, Chang Xu | **날짜**: 2025-10-17 | **DOI**: [10.48550/arXiv.2510.14952](https://doi.org/10.48550/arXiv.2510.14952)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of RoboGhost. We propose a two-stage approach: a motion latent is first generated, then a*

RoboGhost는 언어 지시를 humanoid 로봇의 실행 가능한 동작으로 직접 변환하는 retargeting-free 프레임워크로, motion latent을 조건으로 하는 diffusion-based policy를 통해 기존의 다단계 파이프라인의 누적 오류와 지연을 제거한다.

## Motivation

- **Known**: 기존 language-guided humanoid 제어는 text-to-motion 생성, 로봇 형태로의 motion retargeting, physics-based controller를 이용한 추적의 3단계 파이프라인을 사용하며, 이는 누적 오류, 높은 지연, 약한 의미-제어 coupling을 야기한다.
- **Gap**: 기존 파이프라인은 명시적 human motion 디코딩과 retargeting에 의존하여 fragile하고 비효율적이며, 각 단계가 독립적으로 최적화되어 end-to-end 성능이 제한된다.
- **Why**: Real-time interactive humanoid 제어는 低延遲와 높은 신뢰성이 필수이며, language-guided 제어의 실제 배포를 위해서는 의미적 의도를 유지하면서 직접적인 action 생성 경로가 필요하다.
- **Approach**: Language-grounded motion latent을 semantic anchor로 활용하여 diffusion policy가 noise로부터 직접 executable action을 denoise하도록 하고, causal transformer-diffusion hybrid 구조로 장기적 coherence와 안정성을 동시에 확보한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1:*

- **배포 지연 단축**: 기존 17.85초에서 5.84초로 단축하여 3배 이상의 속도 개선
- **성공률 및 추적 정확도 향상**: retargeting 손실 회피로 5% 높은 성공률과 감소된 추적 오류 달성
- **실제 humanoid 검증**: Unitree G1 등 실제 로봇에서 smooth하고 의미에 부합하는 locomotion 실증
- **멀티모달 확장성**: text 외 image, audio, music 등 다양한 input modality 지원 가능한 범용 프레임워크

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of RoboGhost. We propose a two-stage approach: a motion latent is first generated, then a*

- Motion generator: Continuous autoregressive 모델과 causal autoencoder를 결합하여 text로부터 compact motion latent lref 생성
- Teacher policy: MoE(Mixture of Experts) 기반 oracle policy를 RL로 학습하여 diverse하고 physically plausible한 action 생성
- Student policy: Motion latent을 조건으로 하는 diffusion-based policy를 학습하여 deployment cost 감소
- Causal transformer-diffusion architecture: Transformer backbone으로 long-horizon dependency 캡처, diffusion component로 stochastic stability 제공
- DDIM-accelerated sampling: 빠른 inference를 위해 DDIM 사용으로 실시간 배포 가능

## Originality

- 처음으로 motion latent 조건의 diffusion-based humanoid policy 제안 - 기존 discrete token이나 explicit motion tracking과 대비되는 새로운 패러다임
- Retargeting-free 접근법 - motion decoding과 kinematic retargeting 단계를 완전히 제거하는 근본적인 파이프라인 재설계
- Causal transformer-diffusion hybrid 아키텍처 - long-horizon coherence와 stochastic stability를 unified하는 새로운 motion generator 설계
- End-to-end latent-driven RL framework - MoE teacher와 diffusion student를 활용한 새로운 policy distillation 방식

## Limitation & Further Study

- Motion latent의 해석성 부족 - latent space의 의미적 구조나 제어 가능성에 대한 분석 부재
- Scale 제한 - 실험이 주로 locomotion task에 집중되어 whole-body manipulation이나 복잡한 상호작용 동작의 검증 부족
- Generalization 평가 미흡 - 보이지 않은 instruction이나 robot morphology 변화에 대한 일반화 성능 분석 제한적
- 멀티모달 확장의 구체적 구현 부재 - audio/music input의 실제 구현 및 평가는 제시되지 않음
- 후속 연구 방향: (1) Motion latent 해석성 향상, (2) 복잡한 manipulation task 확장, (3) 다양한 humanoid 형태로의 일반화, (4) Sim-to-real gap 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboGhost는 language-guided humanoid 제어의 근본적인 파이프라인 재설계를 통해 기존의 다단계 접근의 한계를 효과적으로 해결하며, 실제 로봇 배포에서 우수한 성능을 입증한 매우 영향력 있는 연구이다. 다만 해석성 강화와 복잡한 task로의 확장이 후속 과제로 남아있다.

## Related Papers

- 🔄 다른 접근: [[papers/1996_Humanoid_Locomotion_as_Next_Token_Prediction/review]] — 언어에서 로코모션으로의 직접 변환과 다음 토큰 예측 방식의 휴머노이드 보행은 서로 다른 언어 처리 패러다임을 사용한다.
- 🔗 후속 연구: [[papers/1893_ECHO_Edge-Cloud_Humanoid_Orchestration_for_Language-to-Motio/review]] — 엣지-클라우드 협업이 retargeting-free 제어의 실시간 배포 확장이다.
- 🏛 기반 연구: [[papers/2088_Make_Tracking_Easy_Neural_Motion_Retargeting_for_Humanoid_Wh/review]] — 신경망 모션 리타겟팅이 retargeting-free 접근법의 대조되는 기반 기술이다.
- 🔄 다른 접근: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — 둘 다 언어를 휴머노이드 동작으로 변환하지만 RoboGhost는 retargeting-free를, EMOTION은 표현적 비언어 의사소통을 중심으로 한다.
- 🔗 후속 연구: [[papers/1936_From_Motion_to_Behavior_Hierarchical_Modeling_of_Humanoid_Ge/review]] — RoboGhost의 motion latent 기반 diffusion policy를 계층적 행동 계획과 결합하면 더 장기적이고 복잡한 휴머노이드 행동 생성이 가능하다.
- 🔄 다른 접근: [[papers/1937_FRoM-W1_Towards_General_Humanoid_Whole-Body_Control_with_Lan/review]] — 둘 다 언어 지시를 humanoid 동작으로 변환하지만, RoboGhost는 retargeting-free diffusion 접근법을, FRoM-W1은 2단계 언어 이해와 실행 구조를 사용합니다.
- 🏛 기반 연구: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — SENTINEL의 end-to-end language-action model이 RoboGhost의 직접적인 언어-동작 변환 프레임워크의 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — 언어에서 운동으로의 retargeting 기술이 SignBot의 수화 동작 생성에 필요한 기반 방법론이다
- 🔗 후속 연구: [[papers/1642_RGMP_Recurrent_Geometric-prior_Multimodal_Policy_for_General/review]] — 언어 기반 휴머노이드 제어가 RGMP의 기하학적 추론을 자연언어 명령으로 확장하는 발전 방향
- 🧪 응용 사례: [[papers/1643_RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with/review]] — From Language to Locomotion의 retargeting-free 제어가 RLPF의 텍스트-모션 변환을 실제 휴머노이드 제어에 적용한 사례임
- 🔗 후속 연구: [[papers/1646_RoboMirror_Understand_Before_You_Imitate_for_Video_to_Humano/review]] — RoboMirror의 retargeting-free 접근법이 From Language to Locomotion의 언어-보행 직접 변환과 결합되어 더 자연스러운 multimodal 제어를 실현할 수 있다
- 🔄 다른 접근: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — Large Language Action Model과 retargeting-free 언어 제어는 자연언어 기반 휴머노이드 제어의 서로 다른 구현 방식
- 🔗 후속 연구: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — RoboPerform의 오디오 제어 프레임워크가 언어 기반 locomotion과 결합되어 더 풍부한 multimodal humanoid control을 실현할 수 있다.
- 🔗 후속 연구: [[papers/1936_From_Motion_to_Behavior_Hierarchical_Modeling_of_Humanoid_Ge/review]] — PHYLOMAN의 계층적 행동 계획을 RoboGhost의 retargeting-free policy와 결합하면 더 효율적인 장기 행동 실행이 가능하다.
- 🔄 다른 접근: [[papers/1937_FRoM-W1_Towards_General_Humanoid_Whole-Body_Control_with_Lan/review]] — 둘 다 언어에서 locomotion으로의 변환을 다루지만, FRoM-W1은 2단계 구조를, RoboGhost는 retargeting-free 단일 단계 접근법을 사용합니다.
- 🔄 다른 접근: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — 둘 다 언어를 휴머노이드 동작으로 변환하지만 EMOTION은 비언어적 의사소통을, RoboGhost는 retargeting-free 제어를 중심으로 한다.
- 🧪 응용 사례: [[papers/1930_Flexible_Motion_In-betweening_with_Diffusion_Models/review]] — 언어 기반 동작 제어에 diffusion 기반 모션 인-비트위닝 기법을 적용할 수 있다.
- 🔗 후속 연구: [[papers/1968_Harmon_Whole-Body_Motion_Generation_of_Humanoid_Robots_from/review]] — Language to locomotion retargeting이 Harmon의 전신 모션 생성을 보행 제어로 확장합니다.
- 🔗 후속 연구: [[papers/2018_HYPERmotion_Learning_Hybrid_Behavior_Planning_for_Autonomous/review]] — HYPERmotion의 LLM 기반 의미론적 지시 변환을 From Language to Locomotion의 retargeting-free 접근법으로 확장하여 더 직접적인 언어-동작 매핑이 가능하다.
- 🔄 다른 접근: [[papers/2039_LangWBC_Language-directed_Humanoid_Whole-Body_Control_via_En/review]] — 언어 명령을 휴머노이드 제어로 변환하는데 있어 end-to-end 학습 대신 retargeting-free 접근법을 제시한다.
- 🧪 응용 사례: [[papers/2066_Learning_to_Ball_Composing_Policies_for_Long-Horizon_Basketb/review]] — 언어 기반 제어를 통해 농구 동작의 고수준 명령을 자연어로 지시할 수 있는 실용적 응용이다.
- 🏛 기반 연구: [[papers/2168_UniAct_Unified_Motion_Generation_and_Action_Streaming_for_Hu/review]] — language to locomotion의 retargeting-free 접근법이 UniAct의 MLLM 기반 multimodal 명령 처리의 이론적 기반을 제공함
