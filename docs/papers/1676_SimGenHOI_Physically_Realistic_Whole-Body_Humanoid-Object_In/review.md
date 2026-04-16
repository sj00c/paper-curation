---
title: "1676_SimGenHOI_Physically_Realistic_Whole-Body_Humanoid-Object_In"
authors:
  - "Yuhang Lin"
  - "Yijia Xie"
  - "Jiahong Xie"
  - "Yuehao Huang"
  - "Ruoyu Wang"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "SimGenHOI는 Diffusion Transformers 기반의 생성 모델과 강화학습 기반의 접촉-인식 제어 정책을 결합하여 물리적으로 현실적인 인간형 로봇-객체 상호작용을 생성하는 통합 프레임워크이다. 상호 미세조정 전략을 통해 생성 모델과 제어 정책이 반복적으로 서로를 개선하여 장기 조작 과제의 성공률을 높인다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lin et al._2025_SimGenHOI Physically Realistic Whole-Body Humanoid-Object Interaction via Generative Modeling and R.pdf"
---

# SimGenHOI: Physically Realistic Whole-Body Humanoid-Object Interaction via Generative Modeling and Reinforcement Learning

> **저자**: Yuhang Lin, Yijia Xie, Jiahong Xie, Yuehao Huang, Ruoyu Wang, Jiajun Lv, Yukai Ma, Xingxing Zuo | **날짜**: 2025-08-18 | **URL**: [https://arxiv.org/abs/2508.14120](https://arxiv.org/abs/2508.14120)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Our proposed framework uses a diffusion model for key action generation and reinforcement learning to train*

SimGenHOI는 Diffusion Transformers 기반의 생성 모델과 강화학습 기반의 접촉-인식 제어 정책을 결합하여 물리적으로 현실적인 인간형 로봇-객체 상호작용을 생성하는 통합 프레임워크이다. 상호 미세조정 전략을 통해 생성 모델과 제어 정책이 반복적으로 서로를 개선하여 장기 조작 과제의 성공률을 높인다.

## Motivation

- **Known**: 기존 diffusion 기반 HOI 생성 방법들은 다양한 동작을 생성할 수 있으나 접촉 불가능, 관통, 부자연스러운 동작 같은 물리적 인공물로 고통받는다. 강화학습 기반 물리 제어는 현실성을 보장하지만 단순한 상호작용만 가능하고 장기 과제로 확장하기 어렵다.
- **Gap**: 생성 모델의 다양성과 물리적 현실성 사이의 근본적인 trade-off가 존재하며, 특히 장기 동적 상호작용 과제에서 이 문제가 심화된다.
- **Why**: 물리적으로 현실적인 인간형 로봇 동작 생성은 실제 환경에서의 로봇 작업 실행을 위해 필수적이며, 관통, 발 미끄러짐 같은 인공물을 제거하는 것이 성공적인 조작에 중요하다.
- **Approach**: Key action 예측을 통한 diffusion 기반 생성 모델과 접촉-인식 whole-body 제어 정책을 설계하고, 두 컴포넌트가 서로를 반복적으로 개선하는 상호 미세조정 전략을 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: With the condition of text prompt, object geometry,*

- **물리적 현실성 확보**: DiT 기반 생성 모델과 RL 기반 제어 정책의 결합으로 관통, 발 미끄러짐 등의 물리적 인공물을 효과적으로 제거하고 추적 성공률을 현저히 향상
- **Key action 기반 생성 패러다임**: 밀집된 동작 시퀀스 대신 필수 상호작용 동역학을 포착하는 key action을 생성하여 자연스럽게 장기 HOI 생성을 지원
- **상호 미세조정 전략**: 생성 모델이 성공적으로 추적된 동작으로 학습하고 개선된 생성 모델이 정책 성능을 향상시키는 반복적 개선 메커니즘
- **확장된 과제 범위**: 단순한 객체 이동을 넘어 다양한 조작 과제를 지원하는 contact-aware whole-body 제어 정책 설계

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Our proposed framework uses a diffusion model for key action generation and reinforcement learning to train*

- Diffusion Transformers 모델을 사용하여 텍스트 프롬프트, 객체 기하학, 희소 객체 waypoint, 초기 인간형 포즈를 조건으로 key action 예측
- 예측된 key action을 부드러운 동작 궤적으로 보간하여 HOI 정책이 추적할 수 있는 참조 궤적 생성
- 강화학습으로 훈련된 contact-aware 제어 정책을 통해 생성된 동작을 추적하면서 관통 및 발 미끄러짐 같은 인공물 수정
- 생성 모델: 성공적으로 추적된 동작으로 재학습, 제어 정책: 개선된 현실적 동작으로부터 추적 강건성 향상
- Isaac Gym 물리 시뮬레이터에서 전체 프레임워크 평가 및 검증

## Originality

- 기존 diffusion 모델과 RL 정책의 단순 조합이 아닌, 상호 미세조정을 통한 반복적 개선 메커니즘의 제안 - 생성 모델과 제어 정책의 feedback loop 설계
- Dense trajectory 대신 key action 기반 생성 패러다임으로 long-horizon HOI 자연스럽게 지원하는 새로운 접근
- Contact-aware whole-body 제어 정책: 단순 tracking을 넘어 접촉 상태를 명시적으로 고려하는 설계
- 생성 모델 출력에 contact probability를 포함시켜 제어 정책이 접촉 정보를 활용할 수 있도록 설계

## Limitation & Further Study

- 실제 로봇 하드웨어에서의 검증이 부재하며 sim-to-real gap 해결 방안이 제시되지 않음
- 복잡한 손가락 단위(finger-level) 조작이나 다중 객체 상호작용으로의 확장성 평가 부족
- Key action 개수, interpolation 방식 등의 하이퍼파라미터에 대한 민감도 분석 미흡
- 상호 미세조정 과정의 수렴성 보장 및 최적화 이론적 분석 부재
- 후속 연구: (1) 실제 로봇에서의 검증 및 도메인 적응 기법, (2) 손가락 단위 제어와 다중 객체 시나리오 확장, (3) 상호 미세조정의 이론적 기초 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 생성 모델과 강화학습의 상호 보완적 강점을 효과적으로 결합하여 물리적으로 현실적인 장기 인간형 로봇-객체 상호작용 생성이라는 중요한 문제를 해결하였다. 특히 상호 미세조정 전략과 key action 기반 패러다임은 높은 독창성을 보여주며, 광범위한 실험을 통해 방법의 효과를 입증했으나 sim-to-real 검증이 부족한 점이 아쉽다.

## Related Papers

- 🔄 다른 접근: [[papers/1679_SkillMimic_Learning_Basketball_Interaction_Skills_from_Demon/review]] — 두 논문 모두 휴머노이드-객체 상호작용을 다루지만, 일반적인 상호작용과 농구 특화 기술이라는 다른 특화 정도를 가진다.
- 🏛 기반 연구: [[papers/2026_InterMimic_Towards_Universal_Whole-Body_Control_for_Physics-/review]] — 물리 기반 인간-객체 상호작용의 범용적인 제어 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1947_Generalizable_Humanoid_Manipulation_with_3D_Diffusion_Polici/review]] — 일반화 가능한 휴머노이드 조작을 diffusion transformer와 강화학습으로 결합하여 더 발전시킨다.
- 🔗 후속 연구: [[papers/2148_TokenHSI_Unified_Synthesis_of_Physical_Human-Scene_Interacti/review]] — 인간-장면-객체 상호작용을 다루며, 물리적 현실성과 토큰화된 표현이라는 보완적 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1931_Flow_Matching_Imitation_Learning_for_Multi-Support_Manipulat/review]] — 접촉이 풍부한 조작 작업에서 강화학습 기반 접촉 인식 제어와 플로우 매칭 기반 모방 학습이 상호 보완적이다.
- 🔄 다른 접근: [[papers/1679_SkillMimic_Learning_Basketball_Interaction_Skills_from_Demon/review]] — 두 논문 모두 휴머노이드-객체 상호작용을 다루지만, 농구 특화 기술과 일반적인 상호작용이라는 다른 특화 정도를 가진다.
- 🔗 후속 연구: [[papers/1613_PhysHSI_Towards_a_Real-World_Generalizable_and_Natural_Human/review]] — SimGenHOI의 물리적 human-object interaction을 실제 환경으로 확장한 시스템
- 🏛 기반 연구: [[papers/1908_Embrace_Collisions_Humanoid_Shadowing_for_Deployable_Contact/review]] — SimGenHOI의 물리적으로 현실적인 인간-객체 상호작용이 contact-agnostic 동작에 필요한 환경 상호작용 시뮬레이션 기반을 제공한다
- 🏛 기반 연구: [[papers/1909_Embracing_Bulky_Objects_with_Humanoid_Robots_Whole-Body_Mani/review]] — SimGenHOI의 물리적으로 현실적인 전신 휴머노이드-물체 상호작용 기술이 부피가 큰 물체 포용을 위한 물리 기반 학습의 기반을 제공한다.
- 🔄 다른 접근: [[papers/1969_HDMI_Learning_Interactive_Humanoid_Whole-Body_Control_from_H/review]] — 둘 다 물리적으로 현실적인 인간-물체 상호작용을 다루지만 HDMI는 단일 RGB 비디오를, SimGenHOI는 시뮬레이션 생성을 사용한다.
- 🔄 다른 접근: [[papers/1995_Humanoid_Hanoi_Investigating_Shared_Whole-Body_Control_for_S/review]] — 휴머노이드 물체 조작을 Humanoid Hanoi는 스킬 기반으로, SimGenHOI는 물리적 상호작용으로 접근한다.
- 🧪 응용 사례: [[papers/2026_InterMimic_Towards_Universal_Whole-Body_Control_for_Physics-/review]] — 물리적으로 현실적인 인간-객체 상호작용 생성을 위한 구체적인 시뮬레이션 환경과 검증 방법을 제공한다.
- 🔗 후속 연구: [[papers/2100_Mimicking-Bench_A_Benchmark_for_Generalizable_Humanoid-Scene/review]] — SimGenHOI의 humanoid-object interaction이 Mimicking-Bench의 대규모 3D 장면 상호작용 벤치마크로 확장된 것이다
- 🔗 후속 연구: [[papers/2106_MorphoGuard_A_Morphology-Based_Whole-Body_Interactive_Motion/review]] — MorphoGuard의 Material Point Method를 SimGenHOI의 물리적으로 현실적인 인간-객체 상호작용과 결합하여 더 정확한 접촉 시뮬레이션이 가능하다.
- 🔗 후속 연구: [[papers/2170_Unified_Human-Scene_Interaction_via_Prompted_Chain-of-Contac/review]] — 물리적으로 현실적인 전신 인간-객체 상호작용이 인간-장면 상호작용의 확장된 형태이다.
- 🏛 기반 연구: [[papers/2148_TokenHSI_Unified_Synthesis_of_Physical_Human-Scene_Interacti/review]] — 물리적으로 현실적인 전신 인간-객체 상호작용 생성의 기본 기술이 TokenHSI의 통합 정책 설계에 적용된다.
