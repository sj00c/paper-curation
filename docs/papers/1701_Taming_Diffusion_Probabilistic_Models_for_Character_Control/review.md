---
title: "1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control"
authors:
  - "Rui Chen"
  - "Mingyi Shi"
  - "Shaoli Huang"
  - "Ping Tan"
  - "Taku Komura"
date: "2024.04"
doi: ""
arxiv: ""
score: 4.0
essence: "Transformer 기반 Conditional Autoregressive Motion Diffusion Model (CAMDM)을 제안하여 사용자의 동적 제어 신호에 실시간으로 반응하면서 고품질의 다양한 캐릭터 애니메이션을 생성한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Character_Motion_Policy_Transfer"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2024_Taming Diffusion Probabilistic Models for Character Control.pdf"
---

# Taming Diffusion Probabilistic Models for Character Control

> **저자**: Rui Chen, Mingyi Shi, Shaoli Huang, Ping Tan, Taku Komura, Xuelin Chen | **날짜**: 2024-04-23 | **URL**: [https://arxiv.org/abs/2404.15121](https://arxiv.org/abs/2404.15121)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Conditional Autoregressive Motion Diffusion Model*

Transformer 기반 Conditional Autoregressive Motion Diffusion Model (CAMDM)을 제안하여 사용자의 동적 제어 신호에 실시간으로 반응하면서 고품질의 다양한 캐릭터 애니메이션을 생성한다.

## Motivation

- **Known**: 기존 deterministic 캐릭터 컨트롤러는 회귀 대평균(regression to the mean)으로 인한 발 미끄러짐 등의 아티팩트와 반복적인 모션으로 시각적 단조로움을 보이며, 최근 diffusion probabilistic model이 고품질 다양한 샘플 생성에 효과적임이 알려졌다.
- **Gap**: 기존 diffusion model 기반 접근은 실시간 처리의 계산 효율성 부족, 단일 모델로 다중 스타일 지원 불가, 그리고 복잡한 조건 제어 메커니즘이 없다는 문제점이 있다.
- **Why**: 실시간 캐릭터 컨트롤은 게임, VR 등 인터랙티브 애플리케이션의 핵심 요소이며, 고품질의 다양하고 제어 가능한 모션을 단일 통합 모델로 생성할 수 있다면 창작의 유연성과 시스템 효율성을 크게 향상시킨다.
- **Approach**: Autoregressive 프레임워크에 transformer 기반 diffusion model을 적용하되, 별도 조건 토큰화(separate condition tokenization), 과거 모션에 대한 classifier-free guidance, 휴리스틱 미래 궤적 확장(heuristic future trajectory extension) 등의 설계를 통해 실시간 성능과 제어 안정성을 확보한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Visual comparisons of single-style control. From*

- **실시간 생성**: 기존 1000단계 대비 8단계 denoising만으로 실시간 캐릭터 제어 달성
- **다양성 지원**: 동일한 제어 신호에서도 여러 모션을 생성하는 intra-style 다양성 및 단일 모델로 다중 스타일 간 seamless transition 지원
- **제어 안정성**: 별도 조건 토큰화와 attention mechanism을 통해 기존의 불안정한 벡터 기반 조건보다 안정적인 제어 달성
- **실용성**: 공개 mocap 데이터셋에서 다양한 locomotion 스킬에 대해 기존 캐릭터 컨트롤러 대비 우수한 성능 입증

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Illustration of heuristic future trajectory extension.*

- Transformer 기반 encoder-decoder 구조로 과거 모션 히스토리를 입력받아 미래 모션을 조건부로 생성
- Style, speed, facing direction, ground trajectory 등 각 조건을 독립적인 토큰으로 표현하여 attention mechanism을 통해 효과적으로 통합
- Classifier-free guidance를 style 레이블이 아닌 과거 모션 조건 토큰에 적용하여 스타일 전환 시 자연스러운 중간 모션 생성
- 이전 모션의 마지막 프레임 세그먼트를 재활용하여 다음 예측 프레임과의 불연속성을 완화하는 heuristic future trajectory extension 적용
- 모션 예측 길이를 길게 설정하고 사용자 입력 미변화 시 최대한 많은 프레임을 적용하여 intra-style 다양성 향상

## Originality

- 조건 토큰을 분리하여 각 조건의 영향을 명확히 하는 설계는 기존의 단일 벡터 기반 조건화와 차별화
- Classifier-free guidance를 스타일이 아닌 과거 모션에 적용한 것은 intuitive하지 않으면서도 실제로 더 효과적인 novel한 선택
- Heuristic trajectory extension은 간단하지만 diffusion model의 실시간화를 위한 창의적인 문제 해결책
- 단일 unified model로 다중 스타일과 intra/inter-style 다양성을 동시에 지원하는 첫 실시간 시스템

## Limitation & Further Study

- Locomotion 스킬에만 평가되었으며 jumping, attacking 등 다른 형태의 동작에 대한 일반화 가능성 미검증
- Mocap 데이터의 스타일 분포 편향이 있을 경우 특정 스타일의 전환 품질 저하 가능성
- 사용자 조건 입력이 'high-level, coarse'로 제한되어 세밀한 joint 레벨 제어 불가", '8단계 denoising으로 계산 효율성을 얻은 대신 더 많은 단계와의 품질 비교 분석 부재
- 후속 연구: 상체 동작, 감정 표현 등 다양한 모션 타입으로 확장; 더 세밀한 제어 조건 설계; 사용자 연구를 통한 사용성 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Diffusion model을 실시간 캐릭터 컨트롤에 적용하기 위한 체계적이고 실용적인 해결책을 제시한 우수한 논문으로, 별도 조건 토큰화와 classifier-free guidance의 novel한 조합이 다양성과 제어 안정성을 동시에 달성하며, 단일 모델의 다중 스타일 지원은 산업 응용 가치가 높다.

## Related Papers

- 🔄 다른 접근: [[papers/1650_Robot_Drummer_Learning_Rhythmic_Skills_for_Humanoid_Drumming/review]] — CAMDM의 실시간 동적 제어와 드럼 연주의 temporal decomposition은 모두 시간적 조건부 모션 생성을 다루는 상호 보완적 접근법이다.
- 🧪 응용 사례: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — Transformer 기반 diffusion model이 도어 통과와 같은 복잡한 행동 시퀀스의 실시간 애니메이션 생성에 직접 적용될 수 있다.
- 🔄 다른 접근: [[papers/1960_Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthe/review]] — 사용자 제어 신호에 반응하는 캐릭터 모션 생성에서 autoregressive diffusion과 guided diffusion이라는 서로 다른 확산 모델 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1930_Flexible_Motion_In-betweening_with_Diffusion_Models/review]] — 모션 생성에서 실시간 사용자 제어와 유연한 in-betweening이라는 보완적 기능을 제공하는 확산 모델 접근법을 다룬다.
- 🔄 다른 접근: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 사용자 제어 신호에 반응하는 캐릭터 애니메이션을 위해 서로 다른 접근(Conditional Autoregressive vs streaming 자연어)을 통해 실시간 제어를 구현한다.
- 🏛 기반 연구: [[papers/1712_The_Role_of_Domain_Randomization_in_Training_Diffusion_Polic/review]] — 전신 제어를 위한 Diffusion Policies의 역할을 캐릭터 제어라는 특정 도메인으로 확장하여 Transformer 기반 조건부 모델을 개발했다.
- 🔗 후속 연구: [[papers/2119_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_G/review]] — 조건부 모션 생성의 개념을 관절별 세밀한 제어로 확장하여 사용자가 원하는 시점에 특정 관절을 제어할 수 있는 시스템을 구현했다.
- 🏛 기반 연구: [[papers/1650_Robot_Drummer_Learning_Rhythmic_Skills_for_Humanoid_Drumming/review]] — Rhythmic Contact Chain과 temporal decomposition 기법이 실시간 캐릭터 제어를 위한 CAMDM의 조건부 생성 메커니즘에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables/review]] — Taming Diffusion Probabilistic Models의 캐릭터 제어 기법이 RobotDancing의 고역동 춤 동작 추적의 확률적 모델링 기초를 제공함
- 🏛 기반 연구: [[papers/1662_SafeFlow_Real-Time_Text-Driven_Humanoid_Whole-Body_Control_v/review]] — 캐릭터 제어를 위한 diffusion model 기법의 기초를 제공한다.
- 🔄 다른 접근: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 실시간 모션 제어를 위해 서로 다른 접근(streaming 자연어 vs Conditional Autoregressive diffusion)을 통해 동적 명령 수정을 지원한다.
- 🏛 기반 연구: [[papers/1712_The_Role_of_Domain_Randomization_in_Training_Diffusion_Polic/review]] — Diffusion Policies를 캐릭터 제어에 적용한 기반 연구를 휴머노이드 전신 제어로 확장하여 Domain Randomization의 중요성을 체계적으로 분석했다.
- 🔄 다른 접근: [[papers/1624_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_A/review]] — PRIMAL과 Taming Diffusion 모두 물리적으로 반응성 있는 캐릭터 제어를 다루지만 전자는 generative motion model에, 후자는 확산 모델에 기반한다
- 🔄 다른 접근: [[papers/1836_CHIP_Adaptive_Compliance_for_Humanoid_Control_through_Hindsi/review]] — CHIP의 perturbation 기반 적응과 확률적 확산 모델 기반 캐릭터 제어는 동적 환경에서의 적응성을 달성하는 서로 다른 방법론이다.
- 🏛 기반 연구: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — diffusion 모델을 캐릭터 제어에 적용하는 기본 개념이 CLoSD의 physics-diffusion 폐쇄루프 설계에 이론적 토대를 제공한다.
- 🏛 기반 연구: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — Behavior Tree 기반 행동 조정 시스템이 실시간 캐릭터 제어를 위한 diffusion model의 조건부 생성 구조에 기반을 제공한다.
- 🧪 응용 사례: [[papers/1883_DoublyAware_Dual_Planning_and_Policy_Awareness_for_Temporal/review]] — 캐릭터 제어를 위한 확산 확률 모델 길들이기의 실제 적용을 보여줍니다.
- 🔄 다른 접근: [[papers/1886_DreamControl_Human-Inspired_Whole-Body_Humanoid_Control_for/review]] — diffusion model을 character control에 적용하는 다른 접근법을 제시하여 DreamControl과 상호 보완적인 관점을 제공한다.
- 🔄 다른 접근: [[papers/1960_Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthe/review]] — Guided Motion Diffusion과 Taming Diffusion은 모두 diffusion model을 캐릭터 제어에 적용하되 서로 다른 조건부 생성 전략을 사용합니다.
- 🔗 후속 연구: [[papers/1930_Flexible_Motion_In-betweening_with_Diffusion_Models/review]] — CondMDI의 keyframe 제약 기반 모션 인-비트위닝을 diffusion 확률 모델 제어와 결합하면 더 정밀한 캐릭터 제어가 가능하다.
- 🔄 다른 접근: [[papers/2067_Learning_to_Control_Physically-simulated_3D_Characters_via_G/review]] — 확률적 모델을 이용한 캐릭터 제어에서 diffusion과 재투영 기반의 다른 접근법
- 🏛 기반 연구: [[papers/2092_MaskedMimic_Unified_Physics-Based_Character_Control_Through/review]] — 확산 모델을 캐릭터 제어에 적용하는 기본 방법론을 제공하여 마스킹된 모션 생성의 토대가 된다.
- 🔄 다른 접근: [[papers/2111_NoMaD_Goal_Masked_Diffusion_Policies_for_Navigation_and_Expl/review]] — 둘 다 diffusion 기반 제어를 다루지만, NoMaD는 goal masking을 통한 내비게이션에, Taming Diffusion은 캐릭터 제어에 특화된다.
- 🔗 후속 연구: [[papers/2119_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_G/review]] — 캐릭터 제어를 위한 확산 모델이 임의 관절 제어의 확장된 응용이다.
- 🔄 다른 접근: [[papers/2146_TEDi_Temporally-Entangled_Diffusion_for_Long-Term_Motion_Syn/review]] — temporally-entangled diffusion 대신 캐릭터 제어에 특화된 diffusion 확률 모델을 통해 모션 생성을 다룬다.
