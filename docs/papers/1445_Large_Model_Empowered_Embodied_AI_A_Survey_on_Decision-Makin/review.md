---
title: "1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin"
authors:
  - "Wenlong Liang"
  - "Rui Zhou"
  - "Yang Ma"
  - "Bing Zhang"
  - "Songlin Li"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "대규모 모델이 강화된 embodied AI 시스템의 의사결정과 학습 방법을 체계적으로 조사한 종합 서베이로, 계층적/end-to-end 의사결정 패러다임, imitation learning/reinforcement learning 기반 embodied learning, 그리고 world model의 역할을 통합적으로 분석한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Language_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liang et al._2025_Large Model Empowered Embodied AI A Survey on Decision-Making and Embodied Learning.pdf"
---

# Large Model Empowered Embodied AI: A Survey on Decision-Making and Embodied Learning

> **저자**: Wenlong Liang, Rui Zhou, Yang Ma, Bing Zhang, Songlin Li, Yijia Liao, Ping Kuang | **날짜**: 2025-08-14 | **URL**: [https://arxiv.org/abs/2508.10399](https://arxiv.org/abs/2508.10399)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Organization of this survey.*

대규모 모델이 강화된 embodied AI 시스템의 의사결정과 학습 방법을 체계적으로 조사한 종합 서베이로, 계층적/end-to-end 의사결정 패러다임, imitation learning/reinforcement learning 기반 embodied learning, 그리고 world model의 역할을 통합적으로 분석한다.

## Motivation

- **Known**: Embodied AI는 수십 년간 탐색되어 왔으며, 최근 LLM, VLM 등 대규모 모델의 발전이 perception, interaction, planning, learning 능력을 향상시켰다. 기존 서베이는 대규모 모델 자체 또는 planning, learning, simulator 등 개별 컴포넌트에 초점을 맞추었다.
- **Gap**: 기존 서베이들은 대규모 모델과 embodied agent의 시너지에 대한 체계적 분석이 부족하며, 2024년 이후 등장한 Vision-Language-Action (VLA) 모델과 end-to-end 의사결정에 대한 최신 진전을 반영하지 못했다. 또한 world model을 embodied AI 서베이에 통합한 사례가 없었다.
- **Why**: Embodied AI는 AGI로 가는 유망한 경로를 제시하지만, 개방적이고 동적인 환경에서 일반적 목적의 작업을 수행하는 인간 수준의 지능 달성이 여전히 도전적이기 때문에, 대규모 모델이 어떻게 이를 해결하는지 체계적으로 정리할 필요가 있다.
- **Approach**: hierarchical과 end-to-end 의사결정 패러다임을 분류하여 각각이 대규모 모델로부터 어떻게 향상되는지 분석하고, imitation learning과 reinforcement learning에서 policy/reward 설계가 대규모 모델으로 어떻게 개선되는지 검토하며, world model의 설계 방법과 역할을 처음으로 통합적으로 조사한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Organization of this survey.*

- **포괄적 분류 체계**: hierarchical 의사결정(high-level planning, low-level execution, feedback)과 end-to-end 의사결정(VLA 모델 기반)을 체계적으로 분류하고 대규모 모델의 역할을 명확히 함
- **학습 방법론 통합**: imitation learning과 reinforcement learning에서 대규모 모델이 policy network와 reward function 설계를 어떻게 강화하는지 상세히 분석
- **World model 통합**: 처음으로 world model을 embodied AI 서베이에 포함시켜 의사결정과 학습 향상에서의 역할 제시
- **이중 분석 방법론**: 수평적 분석(다양한 접근법 비교)과 수직적 분석(핵심 모델의 진화 추적)을 결합하여 거시적 개요와 심층적 통찰 동시 제공
- **최신 진전 반영**: VLA 모델, end-to-end 의사결정, 최신 대규모 모델 등 2024-2025년의 최신 발전을 포함

## How

![Figure 5](figures/fig5.webp)

*Fig. 5. Hierarchical decision-making paradigm, consisting of perception and interaction, high-level planning,*

- Hierarchical 패러다임에서 LLM/VLM을 이용한 high-level planning, vision-guided low-level execution, feedback-based iterative optimization의 구조 분석
- VLA 모델의 분해 및 perception, action generation, deployment efficiency 측면에서의 대규모 모델 강화 방식 검토
- Imitation learning에서 대규모 모델 기반 behavior cloning, behavior abstraction, in-context learning 등의 policy 구성 방법 분석
- Reinforcement learning에서 LLM 기반 reward function 설계, policy network 구성, exploration 전략 향상 방식 검토
- World model의 설계 원리(representation learning, predictive modeling, contrastive learning 등)와 decision-making/learning 개선 메커니즘 분석
- Hierarchical과 end-to-end 패러다임의 비교 분석(성능, 해석성, 샘플 효율성, 실제 배포 측면)
- Transfer learning, meta-learning 등 추가 embodied learning 방법론의 대규모 모델 활용 방식 검토

## Originality

- 대규모 모델과 embodied AI의 시너지에 초점을 맞춘 최초의 종합 서베이로, 기존 서베이의 단편적 접근을 넘어 통합적 관점 제시
- Hierarchical과 end-to-end 의사결정을 동등하게 상세히 비교 분석하고 각각의 장단점을 명확히 함
- World model을 embodied AI 서베이에 처음으로 통합시켜 perception-action-learning의 완전한 루프 분석
- 이중 분석 방법론(수평적/수직적)을 통해 개별 기술의 진화와 기술 간 상호작용을 동시에 추적
- 2024년 이후의 최신 VLA 모델, end-to-end 패러다임, 최신 대규모 모델 발전을 체계적으로 포함

## Limitation & Further Study

- 실제 로봇 실험 결과 수집 및 비교 분석 부족—주로 시뮬레이션 기반 연구 검토로 실제 배포 격차 미분석
- 계산 비용, 모델 해석성, 안전성 등 실무적 고려사항에 대한 심층 분석 부족
- 대규모 모델의 hallucination, 분포 외(out-of-distribution) 상황 대응 등의 문제점 상세 논의 미흡
- 다중 모달리티(멀티센서, 다양한 환경) 통합 시 발생하는 센싱-의사결정-실행의 대기 시간(latency) 및 동기화 문제 논의 부족
- 후속 연구 방향: 실제 로봇 환경에서의 대규모 모델 적용 검증, 저자원 환경에서의 효율적 활용, 안전성과 신뢰도 보증 메커니즘 개발, 멀티 에이전트 협력 시나리오로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 서베이는 대규모 모델이 embodied AI의 의사결정과 학습을 어떻게 강화하는지를 체계적이고 포괄적으로 분석한 매우 시의적절한 리뷰로, 특히 VLA 모델, end-to-end 패러다임, world model 통합을 통해 기존 서베이를 크게 진전시켰다. 다만 실제 배포 및 실무적 도전 과제에 대한 심화 분석과 실험적 검증이 추가되면 더욱 가치 있는 자료가 될 것이다.

## Related Papers

- 🔗 후속 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — 대규모 모델 기반 embodied AI 서베이가 Foundation Models in Robotics의 기초 연구를 의사결정과 학습 관점에서 심화 발전시킨다.
- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — 둘 다 embodied AI의 포괄적 조사이지만, 대규모 모델 서베이는 의사결정에, General-Purpose Robots 서베이는 foundation model 전반에 초점을 둔다.
- 🏛 기반 연구: [[papers/1294_A_Generalist_Agent/review]] — 대규모 모델 기반 embodied AI 연구가 DeepMind의 Generalist Agent 개념을 이론적 기반으로 삼아 발전된 연구 분야이다.
- 🔗 후속 연구: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Foundation Model Driven Robotics의 전반적 리뷰를 의사결정 패러다임과 embodied learning으로 구체화하여 발전시킨다.
- 🏛 기반 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — Robot Learning in the Era of Foundation Models의 기본 개념을 계층적/end-to-end 의사결정과 학습으로 체계화한다.
- 🏛 기반 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — World Models for Embodied AI 서베이가 대규모 모델 기반 embodied AI의 의사결정과 학습에 필요한 세계 모델 이론을 제공함
- 🔗 후속 연구: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — Exploring Embodied Multimodal Large Models은 대규모 모델 강화 embodied AI를 구체적인 개발과 데이터 관점에서 확장함
- 🔄 다른 접근: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — VLA Models 서베이는 대규모 모델 중심 vs VLA 아키텍처 중심으로 embodied AI를 다른 관점에서 체계화함
- 🔗 후속 연구: [[papers/1405_Generative_Artificial_Intelligence_in_Robotic_Manipulation_A/review]] — 생성형 AI 모델들의 로봇 조작 활용을 구체적으로 다루며, 대규모 모델 기반 embodied AI 서베이와 상호 보완적이다.
- 🏛 기반 연구: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — large model empowered embodied AI가 산업용 로봇의 embodied intelligence 프레임워크 기반
- 🔗 후속 연구: [[papers/1305_Aligning_Cyber_Space_with_Physical_World_A_Comprehensive_Sur/review]] — Large Model Empowered Embodied AI 서베이는 본 논문의 MLM과 WM 중심 관점을 의사결정 관점에서 확장합니다.
