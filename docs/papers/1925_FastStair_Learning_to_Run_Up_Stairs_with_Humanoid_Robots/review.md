---
title: "1925_FastStair_Learning_to_Run_Up_Stairs_with_Humanoid_Robots"
authors:
  - "Yan Liu"
  - "Tao Yu"
  - "Haolin Song"
  - "Hongbo Zhu"
  - "Nianzong Hu"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "FastStair는 model-based foothold planner와 model-free RL을 통합하여 humanoid robot의 고속 계단 등반을 실현하는 다단계 학습 프레임워크이다. DCM 기반 planner로 탐색을 안내하고 speed-specialized experts와 LoRA를 통해 보수성을 완화한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2026_FastStair Learning to Run Up Stairs with Humanoid Robots.pdf"
---

# FastStair: Learning to Run Up Stairs with Humanoid Robots

> **저자**: Yan Liu, Tao Yu, Haolin Song, Hongbo Zhu, Nianzong Hu, Yuzhi Hao, Xiuyong Yao, Xizhe Zang, Hua Chen, Jie Zhao | **날짜**: 2026-01-15 | **URL**: [https://arxiv.org/abs/2601.10365](https://arxiv.org/abs/2601.10365)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2.*

FastStair는 model-based foothold planner와 model-free RL을 통합하여 humanoid robot의 고속 계단 등반을 실현하는 다단계 학습 프레임워크이다. DCM 기반 planner로 탐색을 안내하고 speed-specialized experts와 LoRA를 통해 보수성을 완화한다.

## Motivation

- **Known**: RL은 동적 이동을 생성할 수 있으나 암묵적 안정성 보상으로 인해 계단에서 불안정한 행동을 유발한다. Model-based planner는 명시적 안정성을 보장하지만 보수적 동작으로 속도를 제한한다.
- **Gap**: 고속과 안정성의 상충 관계를 동시에 해결할 수 있는 프레임워크가 부재하다. Planner 기반 가이던스는 보수성을 전이하여 고속성을 제약한다.
- **Why**: 계단 등반은 humanoid robot의 실제 배포에 필수적이며, 인간 수준의 민첩성과 안정성을 동시에 달성하는 것은 로봇 제어의 핵심 과제이다.
- **Approach**: Parallel DCM 기반 foothold planner를 RL 루프에 통합하여 안전 영역으로 탐색을 편향시키고, 속도별 experts 학습과 LoRA 기반 통합으로 보수성을 완화한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **고속 계단 등반 달성**: 명령된 속도 1.65 m/s까지 안정적인 계단 등반 실현 및 33단계 나선형 계단(계단 높이 17 cm)을 12초에 완주
- **병렬 최적화 고속화**: Discrete search 기반 reformulation으로 RL 훈련 속도를 약 25배 가속화
- **다단계 학습 프레임워크**: Safety-focused base policy에서 출발하여 speed-specialized experts로 fine-tuning 후 LoRA로 통합하는 체계적 접근
- **실제 로봇 배포**: Oli humanoid robot에 배포하여 Canton Tower Robot Run Up Competition 우승

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- DCM(Divergent Component of Motion) 기반 foothold planner를 병렬 discrete search로 reformulate하여 GPU 병렬 계산에 최적화
- Pre-training 단계에서 planner가 생성한 feasible footholds를 foothold-tracking reward로 사용하여 안전한 기본 정책 학습
- Post-training 단계에서 저속[-0.3, 0.8 m/s]과 고속[0.8, 1.6 m/s] 명령을 통해 기본 정책을 두 개의 속도 전문가로 fine-tune
- LoRA (Low-Rank Adaptation) 레이어로 두 experts의 파라미터를 하나의 네트워크에 통합하여 전체 속도 범위에서 부드러운 전환 실현
- Rule-based switcher를 사용하여 commanded speed에 따라 experts 간 전환 제어

## Originality

- Model-based planner를 RL 탐색 가이더로 통합하되, 최적화-탐색 reformulation으로 계산 오버헤드를 최소화한 novel 접근
- 속도별 action distribution의 차이를 인식하고 이를 해결하기 위해 속도 전문가 분해와 LoRA 기반 통합이라는 새로운 해결책 제시
- DCM 기반 planner의 명시적 안정성 보장과 RL의 동적 민첩성을 체계적으로 조화시키는 다단계 프레임워크

## Limitation & Further Study

- 현재 방법은 계단 특화 설계로, 일반적인 지형(바위, 경사) 적응성이 검증되지 않음
- LoRA fine-tuning이 전문가 간 평활 전환을 보장하나, 극단적 속도 변화에서의 안정성 분석 부재
- Planner 계산 비용 감소에도 여전히 병렬 환경 필요로, 단일 에피소드 실시간 성능 분석 필요
- 후속 연구: (1) 다양한 지형에 대한 adaptive foothold planning, (2) 더 가벼운 LoRA 구조 탐색, (3) 학습 없이 새로운 계단 형태에 대한 generalization 메커니즘

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: FastStair는 model-based 안정성과 learning-based 민첩성의 근본적 상충을 다단계 학습과 LoRA 기반 통합으로 우아하게 해결한 혁신적 프레임워크이다. 실제 로봇 배포와 경쟁 우승으로 실용성이 입증되었다.

## Related Papers

- 🔄 다른 접근: [[papers/1980_HiWET_Hierarchical_World-Frame_End-Effector_Tracking_for_Lon/review]] — 둘 다 복잡한 지형에서의 보행을 다루지만 FastStair는 계단에, HiWET는 일반적인 지형 추적에 특화되어 있다.
- 🔗 후속 연구: [[papers/1978_Hiking_in_the_Wild_A_Scalable_Perceptive_Parkour_Framework_f/review]] — FastStair의 고속 계단 등반 기법이 복잡한 야외 환경에서의 파쿠어에 응용될 수 있다.
- 🔄 다른 접근: [[papers/1811_BeamDojo_Learning_Agile_Humanoid_Locomotion_on_Sparse_Footho/review]] — 둘 다 humanoid 로봇의 제한된 발판 공간에서의 민첩한 이동을 다루지만, BeamDojo는 sparse foothold에서의 일반적인 locomotion에 집중하는 반면 FastStair는 계단이라는 특수 지형에 특화되었습니다.
- 🏛 기반 연구: [[papers/1944_General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast/review]] — FAST의 대규모 사전학습과 빠른 적응 프레임워크가 FastStair의 다단계 학습 접근법의 이론적 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1637_Reinforcement_Learning_for_Versatile_Dynamic_and_Robust_Bipe/review]] — FastStair의 계단 오르기 기술이 본 논문의 versatile dynamic locomotion 프레임워크를 실제 계단 환경에 적용한 사례임
- 🔗 후속 연구: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — 계단 오르기에 특화된 FastStair의 방법론을 다양한 점프 동작으로 확장한 연구이다.
- 🔗 후속 연구: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — RuN의 자연스러운 보행-달리기 전환이 FastStair의 계단 달리기 학습과 결합되어 더 다양한 동적 이동 능력을 실현할 수 있다
- 🧪 응용 사례: [[papers/1804_APEX_Learning_Adaptive_High-Platform_Traversal_for_Humanoid/review]] — FastStair의 계단 오르기 학습 기법이 APEX의 climb-up과 climb-down 기술을 실제 계단 환경에서 더욱 빠르고 효율적으로 만드는 데 활용될 수 있다.
- 🔗 후속 연구: [[papers/1834_Chasing_Stability_Humanoid_Running_via_Control_Lyapunov_Func/review]] — FastStair의 계단 달리기와 함께 CLF 기반 안정성 제어가 다양한 동적 locomotion 과제에 적용될 수 있음을 보여준다.
- 🧪 응용 사례: [[papers/1859_DecARt_Leg_Design_and_Evaluation_of_a_Novel_Humanoid_Robot_L/review]] — DecARt Leg의 agile locomotion 능력과 FAST 메트릭이 휴머노이드 로봇의 계단 오르기 학습에 실질적으로 적용되어 동적 성능을 평가할 수 있다.
- 🔗 후속 연구: [[papers/1944_General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast/review]] — FAST의 일반적인 사전학습 프레임워크를 계단 등반이라는 특수한 도전적 과제에 적용하여 구체화한 사례입니다.
- 🧪 응용 사례: [[papers/1920_Explosive_Output_to_Enhance_Jumping_Ability_A_Variable_Reduc/review]] — 계단 오르기에서 무릎 관절의 폭발적 출력이 동적 감속비 조절과 함께 활용될 수 있다.
- 🔄 다른 접근: [[papers/2045_Learning_agile_and_dynamic_motor_skills_for_legged_robots/review]] — 동적 운동 기술 학습에서 범용적 접근법 대신 계단 오르기에 특화된 휴머노이드 학습 방법을 제시한다.
- 🔗 후속 연구: [[papers/2127_Optimizing_Bipedal_Locomotion_for_The_100m_Dash_With_Compari/review]] — 휴머노이드의 빠른 계단 오르기 학습을 평지 고속 주행으로 확장한 발전된 응용이다.
