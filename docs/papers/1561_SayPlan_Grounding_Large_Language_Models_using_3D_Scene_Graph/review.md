---
title: "1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph"
authors:
  - "Krishan Rana"
  - "Jesse Haviland"
  - "Sourav Garg"
  - "Jad Abou-Chakra"
  - "Ian Reid"
date: "2023.07"
doi: ""
arxiv: ""
score: 4.0
essence: "SayPlan은 3D Scene Graph (3DSG) 표현을 활용하여 LLM 기반 대규모 로봇 태스크 계획을 확장 가능하게 만드는 접근법이다. 의미론적 검색, 고전적 경로 계획 통합, 반복 재계획 파이프라인을 통해 멀티룸, 멀티플로어 환경에서 실행 가능한 계획을 생성한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Rana et al._2023_SayPlan Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning.pdf"
---

# SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning

> **저자**: Krishan Rana, Jesse Haviland, Sourav Garg, Jad Abou-Chakra, Ian Reid, Niko Suenderhauf | **날짜**: 2023-07-12 | **URL**: [https://arxiv.org/abs/2307.06135](https://arxiv.org/abs/2307.06135)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: SayPlan Overview (top). SayPlan operates across two stages to ensure scalability: (left)*

SayPlan은 3D Scene Graph (3DSG) 표현을 활용하여 LLM 기반 대규모 로봇 태스크 계획을 확장 가능하게 만드는 접근법이다. 의미론적 검색, 고전적 경로 계획 통합, 반복 재계획 파이프라인을 통해 멀티룸, 멀티플로어 환경에서 실행 가능한 계획을 생성한다.

## Motivation

- **Known**: LLM은 다양한 태스크에 대한 계획 생성에서 인상적인 결과를 보여주었다. 그러나 광대한 멀티룸, 멀티플로어 환경에서의 계획 그라운딩은 로보틱스에서 중요한 과제이다.
- **Gap**: 기존 LLM 기반 로봇 계획 방식은 주로 단일 룸 환경에 국한되어 있으며 환경 복잡도 증가에 따라 확장성이 떨어진다. 환경이 확장될수록 모든 자산과 객체 정보를 LLM 컨텍스트에 인코딩하기 어려워진다.
- **Why**: 로봇이 자연어 명령으로부터 멀티플로어 건물 전체에서 복잡한 조작 태스크를 계획하고 실행할 수 있다면 실제 생활 보조 로봇 응용이 가능해진다. 대규모 환경에서의 확장 가능한 LLM 기반 계획 시스템은 실용적 로보틱스 배포의 핵심이다.
- **Approach**: 3DSG의 계층적 구조를 활용하여 LLM이 축약된 그래프 표현에서 의미론적 검색으로 관련 서브그래프를 찾도록 하고, 고전적 경로 계획자(Dijkstra)를 통합하며, 장면 그래프 시뮬레이터 피드백을 통한 반복 재계획으로 실행 불가능한 액션을 수정한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: SayPlan Overview (top). SayPlan operates across two stages to ensure scalability: (left)*

- **확장 가능한 3DSG 처리**: 의미론적 검색 파이프라인으로 전체 대규모 장면 표현을 최대 82.1% 축소하여 LLM이 파싱하도록 함
- **토큰 효율성**: 계층적 3DSG 구조 활용으로 LLM 토큰 한계를 초과하지 않으면서 대규모 환경 계획 지원
- **높은 실행 가능성**: 반복 재계획 파이프라인으로 거의 완벽한 실행 가능률(near-perfect executability) 달성
- **대규모 환경 평가**: 3층 규모, 28-37개 룸, 112-150개 상호작용 가능 객체가 있는 두 개의 광대한 환경에서 검증
- **다양한 태스크 평가**: 의미론적 검색부터 다중룸 장기 목표까지 4개 난이도 수준의 90개 태스크에서 성능 입증
- **실제 로봇 시연**: 모바일 매니퓨레이터 로봇에서의 실제 실행 비디오 데모 제공

## How

![Figure 1](figures/fig1.webp)

*Figure 1: SayPlan Overview (top). SayPlan operates across two stages to ensure scalability: (left)*

- 3D Scene Graph를 JSON 표현으로 LLM에 입력
- 축약된(collapsed) 3DSG를 시작점으로 사용하여 LLM의 초기 컨텍스트 크기 최소화
- LLM이 expand/contract API 함수 호출을 통해 관련 서브그래프 노드 탐색 (의미론적 검색)
- LLM으로부터 고수준 액션 시퀀스 생성 (네비게이션 관련 상세 계획 제외)
- 고전적 경로 계획자(Dijkstra)를 통합하여 LLM이 생성한 고수준 노드 간 최적 경로 완성
- Scene Graph Simulator를 사용하여 생성된 계획 검증 및 실행 불가능성 확인
- 피드백('Cannot release coffee mug here' 등)을 바탕으로 LLM에 재프롬프트하여 반복 재계획", '실행 가능한 계획이 도출될 때까지 검증-재계획 루프 반복

## Originality

- 3DSG의 계층적 구조를 LLM 의미론적 검색에 활용하는 novel 메커니즘 도입
- 고전적 경로 계획자와 LLM 기반 고수준 계획 생성의 효과적 통합으로 LLM 할루시네이션 감소
- 장면 그래프 시뮬레이터 피드백을 통한 반복 재계획 파이프라인으로 계획 실행 가능성 보장
- 기존 PDDL 또는 객체 감지기 기반 접근법과 달리 대규모 다중 룸, 다중 층 환경에서의 실제 확장성 달성
- 자연어 명령으로부터 멀티 플로어 건물에서의 복잡한 조작 태스크 계획의 첫 실증

## Limitation & Further Study

- 3DSG 구성이 사전에 필요하며, 동적 환경 변화에 대한 처리 방식이 제시되지 않음
- 피드백 루프에 의존하므로 계획 수렴 시간이 증가할 수 있음
- Scene Graph Simulator의 정확도가 실제 환경과의 괴리가 있을 경우 계획의 질이 저하될 수 있음
- 평가가 시뮬레이션 환경 중심이며 실제 로봇 실행의 정량적 성공률 상세 데이터 부족
- LLM의 성능이 모델 선택에 따라 달라지는데, 다양한 LLM에 대한 비교 분석 미흡
- 후속 연구: 온라인 장면 그래프 업데이트 메커니즘, 더 큰 규모 환경(예: 다중 건물)으로의 확장, 실시간 동적 환경 대응 방식 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SayPlan은 3DSG의 계층적 구조를 영리하게 활용하여 멀티룸, 멀티플로어 대규모 환경에서 LLM 기반 로봇 계획의 확장성 문제를 실질적으로 해결한 강력한 연구이다. 의미론적 검색, 경로 계획 통합, 반복 재계획 조합으로 실행 가능하고 신뢰성 있는 계획을 보장하여 실제 로보틱스 응용 가능성을 입증한다.

## Related Papers

- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 언어 모델 기반 계획 패러다임을 3D Scene Graph 환경으로 확장한 접근법입니다.
- 🔄 다른 접근: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — 시각-언어 지도 대신 3D Scene Graph를 활용한 다른 접근법으로 로봇 공간 이해를 개선합니다.
- 🔗 후속 연구: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — LLM 기반 계획의 오류 수정 메커니즘을 3DSG 환경에서 확장 가능하게 적용할 수 있습니다.
- 🔄 다른 접근: [[papers/1604_Video_Language_Planning/review]] — SayPlan과 Video Language Planning은 모두 장기 계획 생성에서 서로 다른 표현 방식(3DSG vs 비디오)을 사용합니다.
- 🔄 다른 접근: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser와 SayPlan은 모두 LLM을 활용한 3D 로봇 조작 계획이지만 voxel vs scene graph 표현으로 차별화됩니다.
- 🔗 후속 연구: [[papers/1460_LLM3Large_Language_Model-based_Task_and_Motion_Planning_with/review]] — LLM3는 SayPlan의 3D 장면 이해를 바탕으로 작업-동작 계획을 더욱 정교하게 통합한 발전된 형태입니다.
- 🔗 후속 연구: [[papers/1402_GC-VLN_Instruction_as_Graph_Constraints_for_Training-free_Vi/review]] — SayPlan의 3D scene graph를 연속 환경의 그래프 제약으로 일반화하여 zero-shot 적응을 실현했다.
- 🏛 기반 연구: [[papers/1382_EmbodiedVSR_Dynamic_Scene_Graph-Guided_Chain-of-Thought_Reas/review]] — SayPlan의 3D scene graph 활용이 EmbodiedVSR의 dynamic scene graph 기반 공간 추론 프레임워크 개발에 기초가 된다.
- 🏛 기반 연구: [[papers/1460_LLM3Large_Language_Model-based_Task_and_Motion_Planning_with/review]] — 3D 장면 그래프를 활용한 LLM 기반 계획의 기초 연구로서, LLM3의 모션 계획 실패 추론에 필요한 공간 이해 능력을 제공한다.
- 🏛 기반 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — SayPlan의 LLM 기반 3D 장면 그래프 활용 기법이 PSL의 언어 모델 가이드 계획 수립의 핵심 기반 기술이 된다.
- 🔄 다른 접근: [[papers/1505_Open-vocabulary_Queryable_Scene_Representations_for_Real_Wor/review]] — 둘 다 LLM과 3D 장면 표현을 결합하지만 NLMap은 쿼리 가능한 표현에, SayPlan은 scene graph 기반 계획에 초점을 맞춘 다른 접근법입니다.
- 🧪 응용 사례: [[papers/1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-/review]] — SayPlan의 3D scene graph grounding이 TRAVEL의 landmark 추출과 topological map 구축을 더욱 정밀하게 만들 수 있다.
- 🔄 다른 접근: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser와 SayPlan은 모두 LLM 기반 3D 로봇 조작이지만 voxel 기반 vs scene graph 표현으로 접근이 다릅니다.
- 🔄 다른 접근: [[papers/1604_Video_Language_Planning/review]] — Video Language Planning과 SayPlan은 장기 계획에서 비디오 vs 3D 장면 그래프라는 서로 다른 표현 방식을 사용합니다.
- 🔄 다른 접근: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — 로봇 공간 이해를 위한 서로 다른 접근법 - visual language map vs 3D scene graph입니다.
- 🔄 다른 접근: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — 둘 다 3D scene graph를 활용하지만 OVSG는 open-vocabulary entity grounding에, SayPlan은 LLM 기반 계획에 초점을 맞춘 다른 접근법입니다.
- 🧪 응용 사례: [[papers/1370_DoReMi_Grounding_Language_Model_by_Detecting_and_Recovering/review]] — SayPlan의 3D scene graph 기반 계획 수립이 DoReMi의 고수준 계획 생성과 실행 제약조건 설정에 활용될 수 있습니다.
- 🏛 기반 연구: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — 3D 장면 그래프를 활용한 LLM 기반 계획의 기초 방법론을 제공한다.
