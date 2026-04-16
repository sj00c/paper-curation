---
title: "1820_BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Contr"
authors:
  - "Qiayuan Liao"
  - "Takara E. Truong"
  - "Xiaoyu Huang"
  - "Yuman Gao"
  - "Guy Tevet"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "BeyondMimic은 인간 모션 데이터로부터 학습한 compact motion-tracking 공식과 classifier guidance를 활용한 diffusion model을 결합하여, 휴머노이드 로봇이 학습 중 보지 못한 다양한 작업을 zero-shot으로 수행할 수 있는 통합 제어 프레임워크를 제시한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liao et al._2025_BeyondMimic From Motion Tracking to Versatile Humanoid Control via Guided Diffusion.pdf"
---

# BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion

> **저자**: Qiayuan Liao, Takara E. Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, C. Karen Liu | **날짜**: 2025-08-11 | **URL**: [https://arxiv.org/abs/2508.08241](https://arxiv.org/abs/2508.08241)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of the proposed versatile humanoid control framework. (A) Scalable*

BeyondMimic은 인간 모션 데이터로부터 학습한 compact motion-tracking 공식과 classifier guidance를 활용한 diffusion model을 결합하여, 휴머노이드 로봇이 학습 중 보지 못한 다양한 작업을 zero-shot으로 수행할 수 있는 통합 제어 프레임워크를 제시한다.

## Motivation

- **Known**: DeepMimic 스타일의 motion tracking RL은 자연스러운 움직임을 생성하지만 모션별 튜닝이 필요하고, VAE 기반 생성 모델은 기술적으로는 능숙하지만 명시적 목표 조건이 없는 작업(장애물 회피 등)에서 성능이 저하된다.
- **Gap**: 기존 방법들은 (1) 단일 모션에 대해 state-of-the-art 성능을 내거나 (2) 여러 모션 간 조합이 가능하지만 unseen task에 대한 일반화 능력이 부족하다. 두 특성을 동시에 달성하면서 실제 하드웨어에 zero-shot 전이하는 통합 프레임워크가 없다.
- **Why**: 휴머노이드 로봇이 인간처럼 다양한 민첩한 행동을 수행하면서도 미리 정의되지 않은 새로운 상황에 즉시 적응할 수 있어야 실제 환경에서 실용성을 갖기 때문이다.
- **Approach**: Classical mechanics 기반의 정교한 액추에이션 모델링으로 compact RL 보상 함수(3개 정규화항 + 통합 작업 보상)를 설계하여 diverse motion들에 단일 하이퍼파라미터로 학습하고, 학습된 skills을 state-action co-diffusion model로 캡처한 후 classifier guidance를 통해 테스트 시 새로운 목표로 온라인 최적화한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Diverse motion tracking policies deployed on a real humanoid robot. We demonstrate*

- **Scalable motion tracking**: 회전목마, 스핀킥, 플립킥, 스프린팅 등 radically agile behavior를 단일 setup과 공유된 하이퍼파라미터로 학습하면서 state-of-the-art human-like 성능 달성
- **Versatile task composition**: motion inpainting, joystick teleoperation, obstacle avoidance 등 학습 중 미경험한 다양한 downstream task를 zero-shot으로 해결
- **Real-world deployment**: 제시된 기술들을 실제 휴머노이드 로봇에 성공적으로 전이하여 야외 환경에서 자연스럽고 민첩한 움직임 시연
- **Unified controller**: 작업별 재학습이나 미세조정 없이 단일 diffusion 모델로 diverse skills을 관리하는 최초의 실세계 적용 사례

## How


- Classical mechanics 원리에 기반한 로봇 액추에이션 모델링으로 시뮬레이션-현실 간극 최소화 (지연 시간 등 배포 오차 사전 제거)
- 보상 함수를 3개 물리 일관성 정규화항 + 통합 작업 보상으로 축소하여 motion-agnostic 설계 구현
- Domain randomization을 불확실성이 높은 물리 속성에만 적용하여 견고성과 학습 목표 균형 유지
- State-action co-diffusion model 구축으로 현재 상태와 액션 시퀀스의 결합 분포 학습
- Classifier guidance 기법으로 diffusion 모델의 gradient field를 활용하여 테스트 시 임의의 미분 가능한 목표 함수로 온라인 최적화
- Predictive control 방식으로 future state와 action 모두에 대한 cost 공식화 가능하게 설계

## Originality

- Classical mechanics 기반 액추에이션 모델과 최소화된 보상 함수로 domain randomization의 필요성을 크게 감소시킨 혁신적 접근
- State-action co-diffusion을 predictive control과 결합하여 classifier guidance 기반 온라인 최적화로 unseen task 해결하는 novel 설계
- Motion tracking RL과 diffusion 생성 모델을 계층적 조합이 아닌 통합 프레임워크로 구축하여 기존 VAE 기반 방법의 제약 극복
- Zero-shot sim-to-real 전이로 실제 하드웨어에서 diverse agile skills과 새로운 작업 동시 달성한 첫 사례

## Limitation & Further Study

- 학습 데이터로 사용된 human motion의 다양성과 품질에 따른 성능 의존성이 명시적으로 분석되지 않음
- Diffusion 모델의 샘플링 단계 수와 계산 비용이 실시간 제어에 미치는 영향 논의 부족
- Classifier guidance의 가중치 선택(trade-off parameter)에 대한 원칙적 설정 방법이 명확하지 않음
- Obstacle avoidance 등 일부 downstream task에 대해 정량적 성능 비교(baseline 대비)가 부족
- 후속 연구는 (1) 더 복잡한 환경 조작 작업, (2) 실시간 경로 계획과의 통합, (3) 다중 에이전트 협력 시나리오 확장이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: BeyondMimic은 motion tracking RL의 민첩성과 diffusion 모델의 유연성을 효과적으로 결합하여, 휴머노이드 로봇 제어의 장기적 과제인 자연스러움, 민첩성, versatility를 동시에 달성하는 강력한 프레임워크를 제시한다. 실제 로봇 배포와 zero-shot task 일반화 시연은 로보틱스 커뮤니티에 상당한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1821_BFM-Zero_A_Promptable_Behavioral_Foundation_Model_for_Humano/review]] — 두 논문 모두 zero-shot humanoid control을 다루지만 BeyondMimic은 diffusion 기반, BFM-Zero는 RL 기반 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — CLoSD의 diffusion-physics 폐쇄루프 개념이 BeyondMimic의 motion tracking과 classifier guidance 결합에 이론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/2119_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_G/review]] — BeyondMimic의 compact motion tracking이 OmniControl의 임의 관절 제어로 확장되어 더 세밀한 인간 모션 제어를 달성할 수 있다
- 🔗 후속 연구: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — BeyondMimic의 motion tracking을 넘어선 versatile control이 ResMimic의 GMT 기반 loco-manipulation을 더욱 발전시킬 수 있음
- 🏛 기반 연구: [[papers/1821_BFM-Zero_A_Promptable_Behavioral_Foundation_Model_for_Humano/review]] — BeyondMimic의 compact motion tracking과 BFM-Zero의 shared latent space는 모두 통합된 행동 표현 학습이라는 공통 목표를 가진다.
- 🔄 다른 접근: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — 텍스트 기반 캐릭터 제어에서 CLoSD는 diffusion-physics 루프, BeyondMimic은 motion tracking 기반으로 다른 접근법을 사용한다.
- 🔄 다른 접근: [[papers/1934_From_Experts_to_a_Generalist_Toward_General_Whole-Body_Contr/review]] — 둘 다 motion tracking에서 일반화된 whole-body control로의 전환을 다루지만, BumbleBee는 expert-generalist 프레임워크를, BeyondMimic은 versatile control 접근법을 사용합니다.
- 🔗 후속 연구: [[papers/1944_General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast/review]] — BeyondMimic의 다재다능한 제어 기법이 FAST의 빠른 적응 메커니즘을 보완할 수 있다.
- 🔄 다른 접근: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — 둘 다 motion tracking에서 versatile control로의 발전을 다루지만, GMT는 unified policy 학습에, BeyondMimic은 tracking에서 전체적 제어로의 확장에 집중합니다.
- 🏛 기반 연구: [[papers/1918_ExBody2_Advanced_Expressive_Humanoid_Whole-Body_Control/review]] — BeyondMimic의 모션 추적에서 다양한 휴머노이드 제어로의 전환 기술이 ExBody2의 표현력 있는 전신 동작 구현을 위한 기반 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1985_HOVER_Versatile_Neural_Whole-Body_Controller_for_Humanoid_Ro/review]] — BeyondMimic의 동작 추적을 넘어서는 다목적 제어로 HOVER가 발전시킨 확장된 형태다.
- 🏛 기반 연구: [[papers/2107_MOSAIC_Bridging_the_Sim-to-Real_Gap_in_Generalist_Humanoid_M/review]] — BeyondMimic의 모션 추적 기술이 MOSAIC의 범용 humanoid 동작 추적기 개발에 핵심적인 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2126_Opt2Skill_Imitating_Dynamically-feasible_Whole-Body_Trajecto/review]] — Opt2Skill의 DDP-RL 통합 파이프라인이 BeyondMimic의 모션 추적에서 다목적 휴머노이드 제어로 확장하는 이론적 기반을 제공한다.
