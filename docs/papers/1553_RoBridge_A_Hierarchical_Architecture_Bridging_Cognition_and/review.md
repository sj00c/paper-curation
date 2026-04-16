---
title: "1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and"
authors:
  - "Kaidong Zhang"
  - "Rongtao Xu"
  - "Pengzhen Ren"
  - "Junfan Lin"
  - "Hefeng Wu"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "RoBridge는 Vision-Language Model의 선언적 능력과 강화학습의 절차적 능력을 통합하는 계층적 아키텍처로, Invariant Operable Representation(IOR)을 상징적 브릿지로 활용하여 로봇의 인지와 실행 간 격차를 해소한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_RoBridge A Hierarchical Architecture Bridging Cognition and Execution for General Robotic Manipulat.pdf"
---

# RoBridge: A Hierarchical Architecture Bridging Cognition and Execution for General Robotic Manipulation

> **저자**: Kaidong Zhang, Rongtao Xu, Pengzhen Ren, Junfan Lin, Hefeng Wu, Liang Lin, Xiaodan Liang | **날짜**: 2025-05-03 | **URL**: [https://arxiv.org/abs/2505.01709](https://arxiv.org/abs/2505.01709)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Comparison of RoBridge and previous methods. Declarative skill methods (left) directly generate specific contr*

RoBridge는 Vision-Language Model의 선언적 능력과 강화학습의 절차적 능력을 통합하는 계층적 아키텍처로, Invariant Operable Representation(IOR)을 상징적 브릿지로 활용하여 로봇의 인지와 실행 간 격차를 해소한다.

## Motivation

- **Known**: 최근 대규모 언어-멀티모달 모델의 발전으로 로봇의 명령 이해도가 향상되었으나, 기존 방법들은 인지와 실행 중 하나의 능력을 희생하는 트레이드오프를 안고 있다.
- **Gap**: 선언적 기술(VLM 기반)은 물리적 직관이 부족해 부정확한 실행 계획을 생성하고, 절차적 기술(강화학습)은 학습 효율이 낮으며 환경 변화에 취약하다는 문제가 미해결되어 있다.
- **Why**: 개방형 환경에서 다양한 작업을 수행하는 로봇 개발은 중요한 연구 방향이며, 인지와 실행을 효과적으로 통합하면 로봇의 일반화 능력과 실무 적용성이 크게 향상될 수 있기 때문이다.
- **Approach**: High-level Cognitive Planner(HCP)가 자연언어 명령을 물리적 직관을 가진 IOR로 변환하고, Guided Embodied Agent(GEA)가 이를 구체적 실행 동작으로 변환하는 3계층 구조를 제시한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Comparison of RoBridge and previous methods. Declarative skill methods (left) directly generate specific contr*

- **새로운 작업에 대한 높은 성공률**: 미학습 작업에 대해 75% 성공률 달성
- **우수한 Sim-to-Real 일반화**: 작업당 5개의 실제 데이터 샘플만으로 83% 평균 성공률
- **통합 아키텍처의 첫 구현**: 선언적 능력과 절차적 능력을 상호 제약 없이 통합한 최초의 완전한 시스템
- **환경 불변성**: 조명 변화, 카메라 자세 편차 등 다양한 간섭 조건에서 안정적 성능 유지

## How

![Figure 2](figures/fig2.webp)

*Figure 2. RoBridge overview. RoBridge adopts a three-layer architecture, consisting of a high-level cognitive planner (H*

- High-level Cognitive Planner: 대규모 사전학습된 VLM을 기반으로 자연언어 명령을 분석하고 인과 추론을 통해 물리적으로 타당한 IOR 생성
- Invariant Operable Representation: 환경 불변성과 물리적 직관을 가진 기호적 표현으로 Action(place, push 등), Gripper, Object, Target, Constraint 등의 구조화된 정보 포함
- Guided Embodied Agent: DiT block 기반 아키텍처로 IOR을 저수준 실행 동작으로 변환하며, RL 학습을 통해 환경과의 상호작용에서 절차적 기술 획득
- Continual Skill Aggregation: GEA가 다양한 환경과 작업에서 반복적으로 상호작용하여 지속적으로 기술을 집적

## Originality

- Central Pattern Generator(CPG) 이론에서 영감을 받아 고수준 추론과 저수준 제어 사이의 불변 중간 표현 개념 도입
- IOR 설계로 VLM과 구체적 로봇 제어 간의 완전히 새로운 인터페이스 제시
- 선언적 기술과 절차적 기술의 상호 제약을 제거하는 첫 번째 통합 프레임워크
- 기존 방법들의 부분적 요소들(VoxPoser의 코드 생성, ReKep의 키포인트)을 체계적으로 통합한 완전한 시스템

## Limitation & Further Study

- IOR 설계가 특정 도메인(로봇 조작)에 맞춰져 있어 다른 로봇 작업으로의 확장성이 명확하지 않음
- 실험이 주로 시뮬레이션 환경에서 수행되었으며, 현실 세계 테스트가 제한적(작업당 5개 샘플)
- HCP가 의존하는 VLM의 성능에 크게 좌우되므로, VLM의 공간-시간 추론 능력 한계가 시스템 성능에 직접 영향
- 다중 로봇 협력이나 매우 복잡한 긴 주기 작업에 대한 검증이 부족
- 후속 연구: IOR 설계의 일반화, 보다 강력한 공간-시간 VLM 활용, 실제 환경에서의 광범위한 검증, 복잡도가 높은 작업으로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoBridge는 인지와 실행의 근본적 분리 문제를 IOR이라는 새로운 상징적 표현으로 우아하게 해결한 혁신적 아키텍처이며, 높은 성공률과 Sim-to-Real 성능으로 로봇 조작 분야의 중요한 진전을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — vision-language-action model의 web knowledge transfer 이론을 제공하여 RoBridge의 VLM과 강화학습 통합에 필요한 사전학습된 능력 활용 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — 로봇 인지-실행 통합에서 hierarchical architecture with symbolic bridge vs corrective planning이라는 서로 다른 계층적 제어 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — interactive environment에서의 LLM grounding을 IOR 기반 hierarchical architecture로 확장하여 더 체계적인 인지-실행 통합을 달성한다.
- 🔄 다른 접근: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — RoBridge의 hierarchical architecture와 OpenHelix의 dual-system이 인지와 실행 분리라는 동일한 문제를 서로 다른 구조적 접근으로 해결한다.
- 🏛 기반 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue의 embodied reasoning through planning이 RoBridge의 cognition-execution bridging의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — 인지와 실행의 통합에서 RoBridge는 계층적 아키텍처로, ThinkAct는 dual system으로 서로 다른 방식으로 문제를 해결한다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 embodied multimodal 능력이 RoBridge의 Vision-Language Model과 강화학습 통합 설계에 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma/review]] — Fast-in-Slow의 dual-system 구조와 RoBridge의 계층적 아키텍처를 결합하면 더 효과적인 인지-실행 통합이 가능하다.
- 🔄 다른 접근: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — OpenHelix의 dual-system VLA와 RoBridge의 hierarchical architecture는 인지와 실행 분리라는 같은 문제를 다른 구조로 해결한다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — 고수준 추론과 저수준 실행 통합을 ThinkAct는 dual system으로, RoBridge는 계층적 아키텍처로 서로 다르게 해결한다.
- 🔗 후속 연구: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — 인지와 행동을 연결하는 계층적 아키텍처로 constraint-aware programming을 확장한다.
