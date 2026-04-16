---
title: "1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo"
authors:
  - "Chen Tang"
  - "Ben Abbatematteo"
  - "Jiaheng Hu"
  - "Rohan Chandra"
  - "Roberto Martín-Martín"
date: "2024.08"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 로봇 공학에서의 실제 성공 사례들을 중심으로 Deep Reinforcement Learning(DRL)의 현황을 종합적으로 조사하며, 로봇 역량, 문제 공식화, 해결 방법, 실세계 성공 수준의 네 가지 축으로 이루어진 새로운 분류 체계를 제시한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robot_Policy_Learning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Tang et al._2024_Deep Reinforcement Learning for Robotics A Survey of Real-World Successes.pdf"
---

# Deep Reinforcement Learning for Robotics: A Survey of Real-World Successes

> **저자**: Chen Tang, Ben Abbatematteo, Jiaheng Hu, Rohan Chandra, Roberto Martín-Martín, Peter Stone | **날짜**: 2024-08-07 | **URL**: [https://arxiv.org/abs/2408.03539](https://arxiv.org/abs/2408.03539)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The four aspects of our taxonomy: (a) Robot competencies learned with DRL;*

본 논문은 로봇 공학에서의 실제 성공 사례들을 중심으로 Deep Reinforcement Learning(DRL)의 현황을 종합적으로 조사하며, 로봇 역량, 문제 공식화, 해결 방법, 실세계 성공 수준의 네 가지 축으로 이루어진 새로운 분류 체계를 제시한다.

## Motivation

- **Known**: RL과 deep neural networks를 결합한 DRL은 board games, video games, healthcare, recommendation systems 등 다양한 분야에서 우수한 성능을 보여주었으나, 대부분의 성과는 시뮬레이션 환경에서만 달성되었고 실제 로봇 시스템에 적용 시에는 샘플 효율성, 안정성, 시뮬레이션과 현실의 괴리 등 근본적인 어려움이 존재한다.
- **Gap**: 기존 RL 관련 로봇 공학 설문은 실세계 성공에 초점을 맞추지 않았으며, DRL이 다양한 로봇 응용 분야에서 어떤 수준의 성숙도를 달성했는지 체계적으로 평가하고 도메인 간 공통 기법과 미개척 영역을 식별하는 종합적인 분석이 부족했다.
- **Why**: 로봇 공학에서 DRL의 실제 배포 사례가 증가하고 있으며, 실세계 환경의 복잡성 속에서 DRL의 적용 가능성과 한계를 명확히 파악하는 것이 향후 로봇 시스템 개발의 방향을 결정하는 데 중요하기 때문이다.
- **Approach**: 로봇 역량(locomotion, navigation, manipulation, mobile manipulation, multi-robot interaction, human-robot interaction)을 분류하고, 문제 공식화와 해결 방법론을 체계적으로 분석하며, 실세계 성공 수준(Level 0-5: 시뮬레이션만→상용화)을 평가하는 종합 분류 체계를 구축하여 현황을 평가한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: The four aspects of our taxonomy: (a) Robot competencies learned with DRL;*

- **DRL의 실세계 성공 사례 문서화**: 드론 챔피언 레이싱, 사족 로봇 보행 제어, 자율 주행 등 주요 응용 분야에서 DRL의 달성 수준을 구체적으로 제시
- **4축 분류 체계 제시**: 로봇 역량, 문제 공식화, 솔루션 접근법, 실세계 성공 수준으로 이루어진 새로운 분류법을 통해 DRL 문헌을 체계적으로 조직화
- **도메인 간 공통 기법 식별**: 서로 다른 로봇 응용 분야 간의 기법 교차 분석을 통해 일반적으로 적용 가능한 방법론과 미개척 영역 파악
- **현장 도전 과제 분석**: 샘플 효율성, 안정성, 시뮬-투-리얼 전이, 장기 수평 작업 통합 등 실세계 배포의 주요 장애물 명시

## How

![Figure 1](figures/fig1.webp)

*Figure 1: The four aspects of our taxonomy: (a) Robot competencies learned with DRL;*

- 로봇 역량을 단일 로봇 역량(mobility, manipulation)과 다중 로봇 상호작용으로 계층화하고, mobility를 locomotion과 navigation으로 세분화
- 문제 공식화 측면에서 RL agent-environment 상호작용, 학습 환경(시뮬레이션/실제), 데이터 소스(experience tuples, offline dataset, expert, learned model) 구분
- 솔루션 접근법으로 policy network와 planning-based 방법론 비교
- 실세계 성공 수준을 6단계(Level 0: 시뮬레이션 검증 ~ Level 5: 상용화 제품 배포)로 정의하여 성숙도 평가
- 각 로봇 역량 영역별로 주요 논문, 기법, 성공 사례, 개방형 문제를 체계적으로 검토

## Originality

- 기존 설문과 달리 **실세계 성공에 명시적으로 초점**을 맞추며, 실제 배포 수준을 6단계로 정량화하는 평가 체계 도입
- **다축 분류 체계(4축)**로 기존의 특정 작업이나 기법 중심 분류를 넘어 전체 경관을 통합적으로 분석
- **최근 5년 문헌 중심**(DRL의 주요 성과 시기)으로 현대적 관점에서 필드를 재평가하며, 도메인 간 교차 분석을 통해 공통 패턴과 미개척 영역 식별
- 로봇 공학자와 RL 전문가를 모두 대상으로 하는 이중 관점의 분석 제시

## Limitation & Further Study

- **샘플 효율성**: 실세계 로봇의 상호작용 비용이 높아 충분한 학습 데이터 수집의 어려움이 여전히 미해결 과제
- **시뮬레이션-현실 갭**: 완벽한 물리 시뮬레이션을 구현할 수 없어 sim-to-real transfer의 신뢰성이 제한적
- **장기 수평 작업**: 복잡한 개방형 환경의 장기 작업 완수를 위해 여러 역량을 통합하는 holistic 접근법이 미개발
- **평가 방법론 표준화 부족**: 로봇 시스템 간 공정한 비교를 위한 벤치마크 및 평가 절차의 표준화 필요
- **후속 연구**: 안정적이고 샘플 효율적인 실세계 RL 패러다임 개발, 다양한 로봇 역량을 발견하고 통합하는 원칙 기반 방법론, 엄격한 개발 및 평가 절차 수립이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 DRL이 로봇 공학에서 달성한 실제 성공과 한계를 명확하고 체계적으로 분석하는 현대적 설문으로, 네 가지 축의 분류 체계는 필드의 현황을 이해하고 향후 연구 방향을 수립하는 데 유용한 프레임워크를 제공한다. 특히 실세계 배포 수준의 정량화는 기존 설문과의 차별성 있는 기여이며, RL 실무자와 로봇 공학자 모두에게 가치 있는 참고 자료가 될 수 있다.

## Related Papers

- 🏛 기반 연구: [[papers/1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat/review]] — AutoRT는 DRL 정책을 실제 로봇에 대규모로 배포하는 orchestration 프레임워크로, 실세계 성공 사례 조사의 핵심 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — Neural Scaling Laws는 DRL 성공 사례 조사에서 제시된 스케일링 원칙을 이론적으로 확장하고 일반화합니다.
- 🔄 다른 접근: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — RLinf-VLA는 DRL 대신 VLA 모델에 RL을 통합하는 새로운 접근법으로 로봇 학습의 대안적 패러다임을 제시합니다.
- 🔗 후속 연구: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — LLM을 활용한 강화학습 사전 훈련 가이드로서 DRL의 실세계 적용을 확장합니다.
- 🧪 응용 사례: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — 언어 모델을 사용한 보상 형성의 구체적인 강화학습 적용 사례입니다.
- 🔄 다른 접근: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — 로보틱스에서 강화학습의 실제 적용사례를 종합적으로 정리한 대표적인 서베이 논문입니다.
- 🔗 후속 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation model 시대의 로봇 공학에서 강화학습의 역할과 발전방향을 제시합니다.
- 🏛 기반 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — World model을 통한 강화학습이 로봇 분야 적용의 중요한 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1328_Deep_Reinforcement_Learning_for_Bipedal_Locomotion_A_Brief_S/review]] — 로봇공학을 위한 DRL의 실제 응용으로 이족 보행을 확장한다.
- 🔗 후속 연구: [[papers/1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf/review]] — real-world robotics의 DRL 응용을 learned dynamics model과 결합하여 안전한 네비게이션으로 발전시켰다.
- 🏛 기반 연구: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — real-world humanoid locomotion을 위한 deep reinforcement learning의 이론적 기초와 실제 적용 사례를 제공한다.
- 🔗 후속 연구: [[papers/1567_SE3-Equivariant_Robot_Learning_and_Control_A_Tutorial_Survey/review]] — Deep RL for Robotics Survey의 강화학습 접근법을 SE(3) 동형성을 명시적으로 고려한 기하학적 관점으로 확장했다.
- 🏛 기반 연구: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — Deep RL for Robotics 서베이는 sim-to-real RL의 이론적 배경과 실제 적용 사례를 포괄적으로 제시합니다.
- 🧪 응용 사례: [[papers/1299_A_Survey_of_Robotic_Navigation_and_Manipulation_with_Physics/review]] — 실제 로봇 응용을 위한 심층 강화학습 서베이와 물리 시뮬레이터 역할 분석이 실용적 관점을 제공합니다.
