---
title: "1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables"
authors:
  - "Zhenguo Sun"
  - "Yibo Peng"
  - "Yuan Meng"
  - "Xukun Li"
  - "Bo-Sheng Huang"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "RobotDancing은 잔차 동작(residual action) 강화학습을 통해 인간형 로봇이 장기간 고역동 춤 동작을 추적할 수 있도록 하는 프레임워크로, 모델-실제 간의 동역학 불일치를 명시적으로 보정한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Sun et al._2025_RobotDancing Residual-Action Reinforcement Learning Enables Robust Long-Horizon Humanoid Motion Tra.pdf"
---

# RobotDancing: Residual-Action Reinforcement Learning Enables Robust Long-Horizon Humanoid Motion Tracking

> **저자**: Zhenguo Sun, Yibo Peng, Yuan Meng, Xukun Li, Bo-Sheng Huang, Zhenshan Bing, Xinlong Wang, Alois Knoll | **날짜**: 2025-09-25 | **URL**: [https://arxiv.org/abs/2509.20717](https://arxiv.org/abs/2509.20717)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

RobotDancing은 잔차 동작(residual action) 강화학습을 통해 인간형 로봇이 장기간 고역동 춤 동작을 추적할 수 있도록 하는 프레임워크로, 모델-실제 간의 동역학 불일치를 명시적으로 보정한다.

## Motivation

- **Known**: DeepMimic 이후 물리 기반 인간형 로봇 제어는 상당히 발전했으나, 기존 방법들은 절대 관절 명령(absolute joint commands)을 출력하므로 장기간 고에너지 동작에서 오차가 누적되어 불안정하다.
- **Gap**: 기존 연구들은 참조 궤적과 로봇의 실제 동역학 간의 불일치를 명시적으로 모델링하지 않으며, 장기 추적 안정성을 충분히 다루지 못한다.
- **Why**: 춤, 점프, 회전 등 고역동 인간형 로봇 행동은 산업, 엔터테인먼트, 재활 로봇에 중요하며, 다중 로봇 플랫폼으로의 일반화 가능성이 있다.
- **Approach**: 관절 위치 편차를 학습하는 잔차 동작 정책을 사용하고, 분포 인식 샘플링과 실패 인식 우선순위 적응을 결합하여 장기 추적 오차 누적을 줄인다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **잔차 동작 학습**: 절대 명령 대신 참조 관절의 수정값을 학습하여 동역학 불일치를 명시적으로 보정
- **단일 단계 RL 파이프라인**: 다중 단계 증류나 teacher-student 기법 없이 통합 관찰, 보상, 하이퍼파라미터로 훈련
- **장기 고역동 추적**: Unitree G1에서 분 단위의 춤 동작(점프, 회전, 손짚고 옆으로 구르기)을 추적
- **영점 시뮬레이션-실제 전달**: 특별한 추가 조정 없이 H1, H1-2 등 다중 인간형 로봇으로 전달 가능

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- 분포 인식 샘플링: 드물지만 정보가 많은 자세의 커버리지를 증가시키기 위해 참조 궤적을 다시 샘플링
- 실패 인식 우선순위 적응: 훈련 중 지속적으로 어려운 동작 세그먼트에 학습 자원 할당
- Domain randomization: 지형 마찰, 로봇 특성, 센서 노이즈, 제어 지연 등을 무작위화하여 로버스트성 향상
- 위상 무관 참조 조건화: 시간 인덱스를 직접 사용하지 않고 참조 동작 문맥을 통해 일반화 개선
- 선택적 잔차 동작: 일부 관절에만 잔차를 적용하여 모델 용량을 동역학 보정에 집중
- 커리큘럼 학습: 제어 난이도를 점진적으로 증가시켜 수렴 가속화

## Originality

- 모션 추적에 명시적 잔차 동작 학습 적용: 기존 I-CTRL과 달리 제약 없는 RL로 전체 신체 춤 동작을 처리
- 분포-실패 이원 샘플링 전략: 드문 자세 커버리지와 어려운 세그먼트 모두를 다루는 혁신적 접근
- 다중 전체 크기 로봇 플랫폼으로의 일반화: 단일 하이퍼파라미터 세트로 여러 로봇에 전달 가능한 첫 시연

## Limitation & Further Study

- 평가가 주로 춤 동작에 집중되어 있으며, 다른 고역동 작업(예: 민첩한 이동)에 대한 검증 부족
- 실제 로봇에서의 안정성 메트릭과 실패 사례에 대한 상세한 분석 부족
- 다양한 신체 형태, 구동기 특성, 환경 조건에서의 일반화 범위가 명확하지 않음
- 후속 연구: 조작 작업, 외부 교란 로버스트성, 더 높은 자유도 시스템으로의 확장이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RobotDancing은 잔차 동작 학습과 이원 샘플링 전략을 통해 인간형 로봇의 장기 고역동 모션 추적 문제를 우아하게 해결하며, 실제 로봇으로의 영점 전달 성공은 실무적 가치가 높다.

## Related Papers

- 🔄 다른 접근: [[papers/1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables/review]] — RobotDancing의 잔차 동작 RL과 같은 카테고리의 다른 논문들이 residual learning을 다른 방식으로 활용하여 동역학 불일치를 해결함
- 🔗 후속 연구: [[papers/1924_FARM_Frame-Accelerated_Augmentation_and_Residual_Mixture-of-/review]] — FARM의 residual mixture-of-experts 접근법이 RobotDancing의 잔차 동작 강화학습을 더욱 정교하게 확장할 수 있음
- 🏛 기반 연구: [[papers/1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control/review]] — Taming Diffusion Probabilistic Models의 캐릭터 제어 기법이 RobotDancing의 고역동 춤 동작 추적의 확률적 모델링 기초를 제공함
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — residual action 기반 접근법을 고역동 춤 추적과 자연스러운 보행-달리기 전환에 각각 적용합니다.
- 🏛 기반 연구: [[papers/1679_SkillMimic_Learning_Basketball_Interaction_Skills_from_Demon/review]] — 농구 skill learning의 기초가 되는 동적 동작 추적 및 모델-실제 간 불일치 보정 방법론입니다.
- 🔗 후속 연구: [[papers/1650_Robot_Drummer_Learning_Rhythmic_Skills_for_Humanoid_Drumming/review]] — 리듬감과 접촉 제어가 춤 동작의 beat matching에도 적용될 수 있는 확장 가능성을 보여줍니다.
- 🔄 다른 접근: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — RobotDancing이 음악과 움직임의 연결을 residual-action RL로 접근하여 RoboPerform과 다른 기술적 해결책을 제시한다.
