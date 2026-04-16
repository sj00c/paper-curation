---
title: "1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso"
authors:
  - "Takuma Yoneda"
  - "Jiading Fang"
  - "Peng Li"
  - "Huanyu Zhang"
  - "Tianchong Jiang"
date: "2023.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Statler는 로봇 계획 작업에서 LLM이 세계 상태를 명시적으로 유지하고 추적하도록 하는 모델 기반 프레임워크로, 상태 기반 의사결정을 통해 장기 계획 능력을 향상시킨다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robot_Policy_Learning"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yoneda et al._2023_Statler State-Maintaining Language Models for Embodied Reasoning.pdf"
---

# Statler: State-Maintaining Language Models for Embodied Reasoning

> **저자**: Takuma Yoneda, Jiading Fang, Peng Li, Huanyu Zhang, Tianchong Jiang, Shengjie Lin, Ben Picker, David Yunis, Hongyuan Mei, Matthew R. Walter | **날짜**: 2023-06-30 | **URL**: [https://arxiv.org/abs/2306.17840](https://arxiv.org/abs/2306.17840)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our Statler framework enables robots to carry out complex tasks specified in natural language that require reaso*

Statler는 로봇 계획 작업에서 LLM이 세계 상태를 명시적으로 유지하고 추적하도록 하는 모델 기반 프레임워크로, 상태 기반 의사결정을 통해 장기 계획 능력을 향상시킨다.

## Motivation

- **Known**: 기존 LLM 기반 로보틱스 연구는 LLM을 정책 함수로 사용하여 과거 행동과 관찰만을 조건으로 미래 행동을 생성하는 모델 프리 접근법에 초점을 맞추어왔다.
- **Gap**: LLM이 장기 계획 작업에서 암묵적으로 세계 상태를 유지하기 어렵다는 문제와, 관찰 불가능한 잠재 동역학을 다루는 방법이 부족하다.
- **Why**: 명시적 세계 상태 추적은 부분 관찰성 문제 해결, 장기 계획 스케일링, 그리고 더 정보에 기반한 의사결정을 가능하게 하여 로봇의 복잡한 추론 능력을 대폭 향상시킨다.
- **Approach**: Statler는 world-state reader와 world-state writer 두 개의 prompted LLM으로 구성되어, reader가 현재 상태를 읽고 행동을 생성하면 writer가 행동에 따른 상태 전이를 업데이트하는 방식으로 작동한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Model accuracies on the three-cups-and-a-ball shell*

- **세계 상태 유지의 효과성**: 삼개-컵-공 게임에서 LLM+State 방식이 기존 LLM과 Chain-of-Thought 방법보다 현저히 높은 정확도를 달성하며, 스왑 횟수가 증가할수록 성능 격차가 확대됨
- **Code-as-Policies 대비 성능 향상**: 로봇 시뮬레이션 작업에서 Statler가 Code-as-Policies 같은 강력한 기존 방법들을 크게 능가함
- **확장 가능성**: 명시적 상태 유지로 인해 장기 계획 작업으로의 확장 잠재력을 보여줌
- **일반성**: 프롬프트가 도메인 불가지론적(domain-agnostic)으로 설계되어 다양한 분야에 적용 가능

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Our Statler framework enables robots to carry out complex tasks specified in natural language that require reaso*

- 초기 상태를 JSON 형식의 객체 지향 표현으로 정의
- world-state reader가 사용자 쿼리와 현재 상태를 입력받아 실행 가능한 코드(예: 파이썬 스니펫) 생성
- 생성된 코드에 update_wm 함수 호출을 포함시켜 상태 업데이트 필요 신호
- world-state writer가 수행된 행동 정보를 입력받아 새로운 세계 상태로 업데이트
- 각 구성요소에 대해 시연(demonstration) 기반 프롬프팅으로 LLM 유도
- Code-as-Policies의 계층적 코드 생성 능력을 유지하면서 상태 추적 메커니즘 추가

## Originality

- 기존 모델 프리 접근법과 달리 LLM 기반 로보틱스에 모델 기반 패러다임 도입
- 고전적 모델 기반 강화학습의 개념을 LLM의 상식 지식과 결합한 새로운 프레임워크
- LLM을 환경 모델로 활용하여 암묵적 상태 유지 어려움을 명시적 상태 추적으로 해결하는 창의적 설계
- symbolic world state tracking과 LLM의 유연성을 결합한 hybrid 접근

## Limitation & Further Study

- 세계 상태 추정이 완벽하지 않을 수 있으며, 복잡한 환경에서 상태 표현의 정확성 검증 부족
- JSON 기반 상태 표현이 모든 도메인에 적합한지에 대한 명확한 논의 미흡
- 실제 로봇 환경에서의 성능 평가 (현재는 주로 시뮬레이션에 기반)
- 대규모 복잡 도메인에서 프롬프트 설계 및 관리 작업량에 대한 분석 부재
- 후속 연구로 더 표현력 있는 상태 표현 방식 탐색, 부분 관찰성을 명시적으로 다루는 확률적 상태 추정, 실제 로봇 하드웨어에서의 검증이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Statler는 LLM 기반 로봇 계획에 모델 기반 접근을 도입한 참신한 프레임워크로, 간단하면서도 효과적인 설계로 장기 계획 문제에서 강력한 성능 향상을 보여준다. 다만 실제 로봇 환경에서의 검증과 복잡 도메인 적응성에 대한 추가 연구가 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1459_LLM-State_Open_World_State_Representation_for_Long-horizon_T/review]] — 장기 지평 작업을 위한 상태 표현과 추적의 기반이 되는 open-world state representation 연구입니다.
- 🔄 다른 접근: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 상태 유지를 위한 서로 다른 접근법 - 명시적 상태 추적 vs 에피소딕 메모리 시스템입니다.
- 🔗 후속 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — multi-scale 메모리를 명시적 상태 유지와 결합하여 더 효과적인 장기 계획을 수행할 수 있습니다.
- 🔄 다른 접근: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue은 Statler와 유사하게 LLM의 추론을 embodied 환경에서 활용하지만 내부 독백 방식의 다른 접근법이다.
- 🔄 다른 접근: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — LM-Nav는 상태 유지 언어 모델을 네비게이션에 적용하여 Statler의 embodied reasoning을 다른 도메인에서 구현한다.
- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — Reflective Planning은 Statler의 상태 기반 추론을 다단계 계획에 적용하는 유사한 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — 두 논문 모두 LLM 기반 장기 계획을 다루지만 상태 유지와 RL 통합의 다른 접근법이다.
- 🔄 다른 접근: [[papers/1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac/review]] — Statler는 embodied reasoning을 위해 state-maintaining 접근법을 사용하여 Embodied-Reasoner와 다른 추론 전략을 제시합니다.
- 🔄 다른 접근: [[papers/1422_Hi_Robot_Open-Ended_Instruction_Following_with_Hierarchical/review]] — 둘 다 계층적 instruction following을 다루지만 VLM + VLA vs state-maintaining language model이라는 다른 아키텍처를 사용한다.
- 🔄 다른 접근: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Statler는 상태 유지 메커니즘을 통해 embodied 추론을 개선하는 반면, Inner Monologue는 환경 피드백 기반 내적 독백을 사용합니다.
- 🔄 다른 접근: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — Statler는 LLM의 상태 유지를 통해 embodied 추론을 개선하는 반면, GLAM은 온라인 RL을 통한 점진적 개선에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1459_LLM-State_Open_World_State_Representation_for_Long-horizon_T/review]] — 둘 다 장기 작업을 위한 상태 추적을 다루지만 hybrid object-centric representation vs state-maintaining language model이라는 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — embodied reasoning을 위한 state-maintaining 메커니즘을 multi-scale memory로 확장하여 더 복잡한 장기간 작업에서의 상태 추적 능력을 향상시킨다.
- 🔄 다른 접근: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — 두 논문 모두 LLM을 활용한 장기 계획을 다루지만 RL 통합과 상태 유지의 접근법이 다르다.
- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — 두 논문 모두 VLM의 장기 계획 능력을 다루지만 reflection과 상태 유지의 접근법이 다르다.
- 🔗 후속 연구: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — RoboTron-Nav의 통합된 embodied navigation이 Statler의 상태 유지 언어 모델로 확장되어 더 정교한 추론 기반 네비게이션을 실현할 수 있습니다.
- 🔄 다른 접근: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 장기 지평 작업을 위한 서로 다른 접근법 - 에피소딕 메모리 vs 명시적 상태 유지입니다.
- 🏛 기반 연구: [[papers/1379_Embodied-R_Collaborative_Framework_for_Activating_Embodied_S/review]] — Statler의 state-maintaining language model이 Embodied-R의 대규모 VLM과 소규모 LM 협력 구조에서 상태 유지 메커니즘의 기초를 제공한다.
