---
title: "1624_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_A"
authors:
  - "Yan Zhang"
  - "Yao Feng"
  - "Alpár Cseke"
  - "Nitin Saini"
  - "Nathan Bajandas"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "PRIMAL은 두 단계 학습 패러다임으로 아바타의 모터 시스템을 generative motion model로 구현하여, 물리적으로 반응성 있고 제어 가능하며 실시간 상호작용이 가능한 3D 캐릭터 애니메이션을 실현한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "sub/Egocentric_Manipulation_Imitation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_PRIMAL Physically Reactive and Interactive Motor Model for Avatar Learning.pdf"
---

# PRIMAL: Physically Reactive and Interactive Motor Model for Avatar Learning

> **저자**: Yan Zhang, Yao Feng, Alpár Cseke, Nitin Saini, Nathan Bajandas, Nicolas Heron, Michael J. Black | **날짜**: 2025-03-21 | **URL**: [https://arxiv.org/abs/2503.17544](https://arxiv.org/abs/2503.17544)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. PRIMAL is a novel generative real-time 3D character animation system that works in Unreal Engine. The avatar r*

PRIMAL은 두 단계 학습 패러다임으로 아바타의 모터 시스템을 generative motion model로 구현하여, 물리적으로 반응성 있고 제어 가능하며 실시간 상호작용이 가능한 3D 캐릭터 애니메이션을 실현한다.

## Motivation

- **Known**: Text-to-motion, human-scene interaction 등 다양한 조건부 motion generation 방법들이 발전했으나, 대부분 오프라인 방식이고 실시간 상호작용성과 물리적 반응성이 부족하다. Physics-based 방법들은 물리적 정확성을 제공하지만 시뮬레이션 비용이 크다.
- **Gap**: 기존 방법들은 긴 시간대 motion 생성에 초점을 맞춰 실시간 반응성과 동적 제어가 어렵고, 짧은 시간 척도에서의 물리 역학을 충분히 모델링하지 못한다. 또한 제한된 mocap 데이터로 인해 일반화 성능이 낮다.
- **Why**: Interactive avatar는 게이밍, AR/VR, 비디오 생성 등 다양한 응용분야에서 필수적이며, 자율적으로 움직이면서도 외부 자극에 실시간으로 반응할 수 있는 시스템이 필요하다.
- **Approach**: Autoregressive diffusion model을 이용해 0.5초(15프레임) 단위의 짧은 motion segment를 학습하는 pretrain 단계와, ControlNet 기반 adaptor로 고수준 행동을 학습하는 adaptation 단계의 두 단계 패러다임을 적용한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. PRIMAL is a novel generative real-time 3D character animation system that works in Unreal Engine. The avatar r*

- **물리적 사실성**: Physics simulation 없이도 foot-ground contact 등 물리적으로 그럴듯한 movement를 implicit하게 학습
- **실시간 반응성**: Classifier-based guidance를 통해 impulse, magnet 등 동적 자극에 실시간 반응
- **무제한 생성**: Autoregressive 구조로 시간 제한 없이 연속적인 motion 생성
- **효율적 적응**: ControlNet 기반 adaptor로 적은 계산 비용으로 새로운 task에 신속하게 적응
- **실제 시스템 구현**: Unreal Engine에서 동작하는 완전한 interactive character animation system 실현

## How


- **Pretraining 단계**: 모든 mocap segment를 0.5초 단위로 분할하여 unsupervised diffusion model 학습 - 현재 joint 상태와 속도로부터 다음 0.5초 motion 예측
- **짧은 시간 척도 전략**: 0.5초 범위에서 physics가 지배적이라는 가정으로, 과거 motion 조건을 제거하여 semantic overfitting 방지
- **제어 메커니즘**: Classifier-based guidance로 목표 속도/방향 달성 및 external force 반응 구현
- **Adaptation 단계**: ControlNet 기반 adaptor를 transformer의 individual block에 control embedding 추가하여 spatial target reaching, few-shot action generation 수행
- **Real-time 추론**: Autoregressive 구조로 초기 single-frame state에서 연속적 motion 생성 및 동적 제어 신호 적용

## Originality

- **단기 motion modeling 전략**: Physics dominance의 0.5초 척도 전제로 과거 조건 제거 - 기존 autoregressive 방식과 다른 혁신적 접근
- **Physics 없는 물리성**: Explicit physics simulation이나 contact labeling 없이 diffusion model만으로 물리적 현실성 달성
- **두 단계 분리 학습**: Motor control(physics)과 behavior(semantics)를 분리하여 각각 다른 시간 척도로 모델링
- **Interactive adaptor**: ControlNet을 활용한 효율적 fine-tuning으로 다양한 task-specific adaptation 가능
- **Unbounded motion generation**: Autoregressive 구조로 기존 방법의 고정 길이 제약 극복

## Limitation & Further Study

- 0.5초 척도 가정의 일반화: 매우 느린 움직임이나 1초 이상의 협응적 움직임에서 성능 검증 부족
- Physics simulation 비교 부족: PhysD-diff, CLoSD 등 hybrid 방식과의 상세한 정량적 비교 미흡
- Dataset dependency: Mocap 데이터의 diversity와 품질에 따른 영향도 분석 필요
- Control signal 제약: Classifier-based guidance의 정확도 및 복잡한 multi-task 제어 상황에서의 안정성 검증 필요
- **후속 연구**: 다양한 신체 유형, 의류, 환경 변수에서의 일반화 개선; Contact-explicit model과의 하이브리드 방식 탐색; 더 강력한 physical plausibility 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: PRIMAL은 짧은 시간 척도에서의 physics 지배성이라는 통찰력으로 unsupervised diffusion model을 통해 실시간 반응성과 물리적 사실성을 동시에 달성한 혁신적 접근이며, Unreal Engine 구현으로 실제 응용 가능성을 입증한 탁월한 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — PRIMAL의 generative motion model과 제스처 생성의 LLM+Motion-GPT는 서로 다른 인간형 실시간 애니메이션 접근법
- 🔗 후속 연구: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — EMOTION의 표현적 휴머노이드 동작 생성이 PRIMAL의 반응형 모터 모델을 감정적 표현으로 확장한 형태
- 🏛 기반 연구: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — 자유형 휴머노이드 로코모션이 PRIMAL의 물리적 반응성과 제어 가능한 3D 캐릭터 애니메이션의 기반 기술
- 🔄 다른 접근: [[papers/1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control/review]] — PRIMAL과 Taming Diffusion 모두 물리적으로 반응성 있는 캐릭터 제어를 다루지만 전자는 generative motion model에, 후자는 확산 모델에 기반한다
- 🏛 기반 연구: [[papers/1817_Benchmarking_Potential_Based_Rewards_for_Learning_Humanoid_L/review]] — PRIMAL의 두 단계 학습 패러다임이 Benchmarking Potential Based Rewards의 휴머노이드 학습 평가 방법론을 활용할 수 있다
- 🏛 기반 연구: [[papers/1917_Example-based_Motion_Synthesis_via_Generative_Motion_Matchin/review]] — Generative motion synthesis 방법론을 interactive avatar control에 적용한 기반 연구
- 🔗 후속 연구: [[papers/2135_Perpetual_Humanoid_Control_for_Real-time_Simulated_Avatars/review]] — PRIMAL의 reactive motor model을 real-time avatar control로 확장한 연구
- 🧪 응용 사례: [[papers/1928_Feature-Based_vs_GAN-Based_Learning_from_Demonstrations_When/review]] — Feature-based vs GAN-based 비교 프레임워크가 물리적 반응형 모션 모델 선택에 적용될 수 있다.
