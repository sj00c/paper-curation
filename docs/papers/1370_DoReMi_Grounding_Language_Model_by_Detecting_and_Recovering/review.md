---
title: "1370_DoReMi_Grounding_Language_Model_by_Detecting_and_Recovering"
authors:
  - "Yanjiang Guo"
  - "Yen-Jen Wang"
  - "Lihan Zha"
  - "Jianyu Chen"
date: "2023.07"
doi: ""
arxiv: ""
score: 4.0
essence: "DoReMi는 LLM으로 고수준 계획과 실행 제약조건을 동시에 생성하고, VLM으로 실행 중 제약 위반을 지속적으로 감지하여 계획-실행 불일치를 즉시 탐지하고 복구하는 로봇 작업 프레임워크이다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Guo et al._2023_DoReMi Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment.pdf"
---

# DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment

> **저자**: Yanjiang Guo, Yen-Jen Wang, Lihan Zha, Jianyu Chen | **날짜**: 2023-07-01 | **URL**: [https://arxiv.org/abs/2307.00329](https://arxiv.org/abs/2307.00329)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Illustration of our motivation. Previous works use LLM to generate only high-level textual plans. Therefore, Low*

DoReMi는 LLM으로 고수준 계획과 실행 제약조건을 동시에 생성하고, VLM으로 실행 중 제약 위반을 지속적으로 감지하여 계획-실행 불일치를 즉시 탐지하고 복구하는 로봇 작업 프레임워크이다.

## Motivation

- **Known**: 기존 연구들은 LLM을 이용해 고수준 텍스트 계획을 생성하고 저수준 제어기가 실행하는 계층적 접근법을 사용했다. 하지만 실제 환경에서 저수준 실행이 고수준 계획에서 벗어날 수 있다.
- **Gap**: 기존 방법들은 각 계획 단계가 완료된 후에만 피드백을 통합하여 재계획하므로, 실행 중 발생하는 불일치에 즉시 대응하지 못한다. 이로 인해 작업 완료 시간이 증가하고 효율성이 떨어진다.
- **Why**: 로봇이 계획-실행 불일치를 즉시 감지하고 복구할 수 있다면 작업 성공률을 높이고 작업 완료 시간을 단축할 수 있으며, 복잡한 실세계 로봇 작업의 실용성을 크게 향상시킬 수 있다.
- **Approach**: DoReMi는 LLM의 이중 역할(계획 생성과 제약조건 생성)과 VLM의 제약 감시를 결합한다. 실행 중 VLM이 제약 위반을 감지하면 LLM이 즉시 재계획을 수행하여 복구한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Previous methods perform open-loop planning or only re-plan when the previous skill is finished. Our DoReMi*

- **이중 역할 활용**: LLM을 단순 계획 생성기가 아닌 제약조건 생성기로도 활용하여 저수준 실행 감시를 가능하게 함
- **자동화된 고주파 피드백**: VLM을 제약 감지기로 활용하여 수동 설계 없이 자동으로 정확하고 빈번한 피드백을 제공
- **즉시 복구 메커니즘**: 계획 단계 완료 후가 아닌 실행 중 불일치 감지 시 즉시 재계획을 통해 회복
- **성능 향상**: 로봇 팔과 휴머노이드 로봇 작업에서 기존 방법 대비 더 높은 작업 성공률과 단축된 작업 완료 시간 달성

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Open-ended scene descriptions of VLMs are ambiguous. DoReMi leverages the LLM to reason specific constraints*

- LLM에 few-shot in-context 프롬핑을 통해 현재 상태와 기본 기술 집합을 바탕으로 다음 기술과 해당 제약조건을 함께 생성
- VLM을 주기적으로 호출하여 LLM이 생성한 특정 제약조건(constraint)에 대해 현재 이미지가 만족하는지 여부를 이진 질문(binary query)으로 검증
- VLM이 제약 위반을 탐지하면 피드백을 LLM 프롬프트에 포함시켜 즉시 재계획 수행
- 재계획 결과로 새로운 기술과 제약조건을 생성하여 실행 단계로 돌아감

## Originality

- LLM을 계획 생성과 제약조건 생성의 이중 역할로 활용하는 새로운 패러다임 제시
- VLM의 개방형 장면 설명(open-ended scene description)의 모호성 문제를 LLM 기반 제약조건으로 명확하고 정밀한 질의(precise query)로 변환
- 실행 단계 중 즉각적인 재계획을 가능하게 하는 execution-level feedback 메커니즘 도입으로 기존의 plan-level feedback 접근법과 차별화

## Limitation & Further Study

- 제약조건 생성의 정확성이 LLM의 성능에 크게 의존하므로, LLM의 제약조건 생성 실패 또는 부정확성이 시스템 전체 성능을 저해할 수 있음
- VLM 호출의 빈도와 latency가 실시간 제어가 필요한 고주파 로봇 작업(예: 동적 다리 로봇)에서 병목이 될 수 있음
- 기본 기술 집합(primitive skills)이 사전에 주어져야 하며, 제약조건이 VLM으로 검증 가능한 시각적 특성으로 표현 가능해야 함
- 후속 연구: VLM 호출 최소화 전략, 더 강력한 제약조건 생성 방법, 고주파 제어 작업으로의 확장, 인간 피드백 통합 방안

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DoReMi는 LLM과 VLM을 창의적으로 결합하여 로봇 작업의 계획-실행 불일치 문제를 즉시 감지하고 복구하는 실용적인 프레임워크를 제시했으며, 명확한 동기, 체계적인 방법론, 견실한 실험을 통해 높은 학술적 가치와 로봇 제어 분야의 실질적 기여를 입증했다.

## Related Papers

- 🏛 기반 연구: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — DoReMi의 제약 조건 기반 실행 감지가 CoPAL의 오류 처리 메커니즘 설계에 기반을 제공
- 🔄 다른 접근: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — 계획-실행 불일치 감지 대신 inner monologue를 통한 다른 embodied reasoning 접근법
- 🧪 응용 사례: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — SayPlan의 3D scene graph 기반 계획 수립이 DoReMi의 고수준 계획 생성과 실행 제약조건 설정에 활용될 수 있습니다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 실시간 코드 생성이 DoReMi의 계획-실행 불일치 탐지에 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — LLM 기반 계획 오류 탐지와 VLM 기반 제약 모니터링이 로봇 실행 감시에서 다른 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — 계층적 플래닝을 제약 조건 위반 감지와 결합하여 더 강건한 plan-execution 시스템으로 발전
- 🔗 후속 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — DoReMi의 계획-실행 불일치 탐지가 Code as Policies의 실시간 코드 생성을 보완합니다.
- 🔄 다른 접근: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — VLM 기반 제약 모니터링과 LLM 기반 계획 오류 탐지가 로봇 실패 처리에서 다른 접근법을 제시합니다.
