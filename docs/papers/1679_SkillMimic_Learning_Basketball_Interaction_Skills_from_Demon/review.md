---
title: "1679_SkillMimic_Learning_Basketball_Interaction_Skills_from_Demon"
authors:
  - "Yinhuai Wang"
  - "Qihan Zhao"
  - "Runyi Yu"
  - "Hok Wai Tsui"
  - "Ailing Zeng"
date: "2024.08"
doi: ""
arxiv: ""
score: 4.0
essence: "SkillMimic은 skill-specific reward 설계 없이 통합된 HOI imitation reward를 사용하여 단일 policy로 다양한 농구 상호작용 기술을 학습하고 합성할 수 있는 data-driven 프레임워크다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2024_SkillMimic Learning Basketball Interaction Skills from Demonstrations.pdf"
---

# SkillMimic: Learning Basketball Interaction Skills from Demonstrations

> **저자**: Yinhuai Wang, Qihan Zhao, Runyi Yu, Hok Wai Tsui, Ailing Zeng, Jing Lin, Zhengyi Luo, Jiwen Yu, Xiu Li, Qifeng Chen, Jian Zhang, Lei Zhang, Ping Tan | **날짜**: 2024-08-12 | **URL**: [https://arxiv.org/abs/2408.15270](https://arxiv.org/abs/2408.15270)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Concept of SkillMimic. We define an interaction skill as*

SkillMimic은 skill-specific reward 설계 없이 통합된 HOI imitation reward를 사용하여 단일 policy로 다양한 농구 상호작용 기술을 학습하고 합성할 수 있는 data-driven 프레임워크다.

## Motivation

- **Known**: 기존 RL 기반 인간-물체 상호작용 학습은 각 skill마다 수작업으로 설계된 reward를 필요로 하며, locomotion 모방 학습은 주로 이동 기술에만 집중되어 있다.
- **Gap**: 다양한 상호작용 기술을 통합된 프레임워크로 학습하고 장기 복합 작업(예: 연속 득점)을 수행할 수 있는 방법이 부재하다.
- **Why**: skill-specific reward 설계의 제거는 확장성과 일반화를 크게 향상시키며, 농구와 같은 복잡한 상호작용 학습에서 실용적인 해결책을 제공한다.
- **Approach**: Contact graph를 통해 정밀한 접촉 모방을 가능하게 하고, 통합된 HOI imitation reward로 다양한 기술을 학습한 후, high-level controller를 통해 기술을 재조합하여 복합 작업을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. We propose a novel approach that for the first time enables physically simulated humanoids to learn a variety *

- **SkillMimic 프레임워크**: 동일한 hyperparameter로 dribbling, layup, shooting 등 다양한 농구 기술을 학습하고 smooth skill switching을 실현
- **Contact graph**: 다양한 상호작용 skill에 적용 가능한 일반적인 접촉 모델링 방법으로 precise contact imitation 달성
- **통합 HOI imitation reward**: skill-specific reward 없이 diverse interaction pattern을 효과적으로 capture하는 통합 reward 설계
- **계층적 기술 합성**: 학습된 interaction skill을 고수준 controller로 재사용하여 연속 득점 같은 장기 복합 작업 달성
- **BallPlay 데이터셋**: RGB 비디오 기반 BallPlay-V(8개 기술)와 optical motion capture 기반 BallPlay-M(35분)의 두 농구 HOI 데이터셋 공개

## How

![Figure 3](figures/fig3.webp)

*Fig. 3 (b) shows the training pipeline of SkillMimic. Given*

- HOI state transition으로 interaction skill을 정의하여 reference motion과의 상태 전이 일치도 기반 학습
- Contact graph를 사용하여 humanoid와 object 간의 physical contact를 explicitly 모델링 및 reward 설계
- Kinematic motion matching, contact reward, object state reward로 구성된 통합 HOI imitation reward 구성
- Single IS policy로 다중 기술 학습 및 smooth transition 지원
- High-level policy를 별도 학습하여 IS policy의 기술 조합으로 복합 작업 수행
- Motion capture 데이터 처리 및 humanoid controller integration을 통한 실제 구현

## Originality

- **첫 통합 HOI imitation 프레임워크**: 기존 locomotion 모방 방법을 interaction skill로 확장하되, contact 및 relative motion의 unbalanced reward 문제를 구체적으로 해결
- **Contact graph 제안**: 기존 interaction graph의 kinematic 한계를 극복하고 physical contact를 explicitly 우선시하는 새로운 모델링 방식
- **Skill 합성을 통한 장기 작업**: 개별 interaction skill 학습과 고수준 제어의 조합으로 처음 연속 농구 득점 달성
- **Data-driven scalability 입증**: dataset 규모 증가에 따른 skill 다양성 및 일반화 개선을 체계적으로 분석

## Limitation & Further Study

- 농구 domain에 특화되어 있으며 다른 복잡한 상호작용(예: 악기 연주, 세밀한 수공예)으로의 일반화 검증 부재
- High-level task 합성을 위한 reward 설계 및 hierarchical policy 학습 과정이 여전히 수작업 개입 필요
- Contact graph가 모든 유형의 상호작용에 동등하게 효과적인지에 대한 분석 부족
- Real robot 실무 적용 전 sim-to-real transfer 검증 필요
- **후속 연구**: (1) 다양한 domain의 HOI 데이터셋 수집 및 cross-domain generalization 연구, (2) high-level policy 학습의 자동화, (3) sim-to-real transfer 기법 개발, (4) 더 복잡한 multi-agent 상호작용 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SkillMimic은 skill-specific reward 제거를 통해 상호작용 기술 학습의 실용성을 혁신적으로 개선했으며, contact graph와 통합 HOI reward 설계는 기술적으로 견고하고 농구 데이터셋 기여와 함께 이 분야의 significant advance를 이룬다.

## Related Papers

- 🔄 다른 접근: [[papers/1676_SimGenHOI_Physically_Realistic_Whole-Body_Humanoid-Object_In/review]] — 두 논문 모두 휴머노이드-객체 상호작용을 다루지만, 농구 특화 기술과 일반적인 상호작용이라는 다른 특화 정도를 가진다.
- 🔗 후속 연구: [[papers/2066_Learning_to_Ball_Composing_Policies_for_Long-Horizon_Basketb/review]] — 농구 스킬 학습의 기초 연구를 장기간 농구 정책 구성으로 확장한다.
- 🔗 후속 연구: [[papers/2074_Learning_Vision-Driven_Reactive_Soccer_Skills_for_Humanoid_R/review]] — 스포츠 기술 학습에서 농구와 축구라는 서로 다른 종목에 대한 휴머노이드 제어 접근법을 다룬다.
- 🔄 다른 접근: [[papers/1650_Robot_Drummer_Learning_Rhythmic_Skills_for_Humanoid_Drumming/review]] — 농구 상호작용과 드럼 연주 모두 rhythmic skill이지만 대상 객체와의 접촉 방식이 다릅니다.
- 🔄 다른 접근: [[papers/1676_SimGenHOI_Physically_Realistic_Whole-Body_Humanoid-Object_In/review]] — 두 논문 모두 휴머노이드-객체 상호작용을 다루지만, 일반적인 상호작용과 농구 특화 기술이라는 다른 특화 정도를 가진다.
- 🏛 기반 연구: [[papers/1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables/review]] — 농구 skill learning의 기초가 되는 동적 동작 추적 및 모델-실제 간 불일치 보정 방법론입니다.
- 🏛 기반 연구: [[papers/2047_Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Huma/review]] — 불완전한 시연 데이터로부터 스포츠 기술을 학습하는 기본 방법론 제공
- 🏛 기반 연구: [[papers/2063_Learning_Soccer_Skills_for_Humanoid_Robots_A_Progressive_Per/review]] — 시연 기반 농구 상호작용 스킬 학습의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/2066_Learning_to_Ball_Composing_Policies_for_Long-Horizon_Basketb/review]] — 농구 동작 학습을 위한 데모 기반 스킬 모방 방법론을 확장하여 장기 시퀀스 합성에 적용할 수 있다.
