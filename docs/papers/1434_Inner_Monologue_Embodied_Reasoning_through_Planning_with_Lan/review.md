---
title: "1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan"
authors:
  - "Wenlong Huang"
  - "Fei Xia"
  - "Ted Xiao"
  - "Harris Chan"
  - "Jacky Liang"
date: "2022.07"
doi: ""
arxiv: ""
score: 4.0
essence: "LLM을 로봇 제어에 활용할 때, 환경 피드백을 자연어로 주입하여 LLM이 '내적 독백(inner monologue)'을 형성하게 함으로써 폐루프 계획 및 추론을 가능하게 한다. 추가 학습 없이 프롬프팅만으로 복잡한 장기 조작 작업을 수행할 수 있음을 보여준다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robot_Policy_Learning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2022_Inner Monologue Embodied Reasoning through Planning with Language Models.pdf"
---

# Inner Monologue: Embodied Reasoning through Planning with Language Models

> **저자**: Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, Brian Ichter | **날짜**: 2022-07-12 | **URL**: [https://arxiv.org/abs/2207.05608](https://arxiv.org/abs/2207.05608)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Inner Monologue enables grounded closed-loop feedback for robot planning with large language models*

LLM을 로봇 제어에 활용할 때, 환경 피드백을 자연어로 주입하여 LLM이 '내적 독백(inner monologue)'을 형성하게 함으로써 폐루프 계획 및 추론을 가능하게 한다. 추가 학습 없이 프롬프팅만으로 복잡한 장기 조작 작업을 수행할 수 있음을 보여준다.

## Motivation

- **Known**: 최근 LLM의 추론 능력을 로봇 계획에 활용하는 연구들이 진행되었으며, 자연어가 다양한 기초 모델 간의 통합 인터페이스로 기능할 수 있음이 알려져 있다.
- **Gap**: 기존 LLM 기반 로봇 계획 연구들(예: SayCan)은 각 행동이 성공적으로 실행된다고 가정하여, 동적 환경에서의 중간 실패나 재계획을 제대로 처리하지 못한다. 환경 피드백을 자연어로 통합하여 폐루프 계획을 수행하는 연구가 부족하다.
- **Why**: 로봇이 복잡하고 장기적인 작업을 수행하려면 단순한 계획 생성뿐 아니라 실시간 환경 변화에 대응하고 실패로부터 회복할 수 있어야 하며, 이는 로봇 자동화의 실용성과 강건성 향상에 필수적이다.
- **Approach**: LLM의 프롬프트에 성공 감지, 장면 설명, 인간 상호작용 등 다양한 자연어 피드백을 동적으로 주입하여, LLM이 이전 행동의 결과를 반영해 다음 행동을 선택하도록 유도한다. 사전학습된 LLM과 로봇 스킬 라이브러리를 few-shot prompting으로 조합한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Different instantiations of Inner Monologue in three distinct domains – simulated tabletop rearrangement (top)*

- **폐루프 피드백의 효과 입증**: 세 가지 도메인(시뮬레이션 탁상 정리, 실제 탁상 정리, 실제 주방 이동 조작)에서 자연어 피드백이 고수준 지시 완료율을 유의미하게 향상시킴
- **확장된 창발 능력**: 추가 학습 없이 새로운 지시 적응, 자기 제안 목표 설정, 상호작용적 장면 이해, 다국어 상호작용 등 예상 밖의 능력이 나타남
- **강건성 향상**: 확률적 실패에 대한 효율적 재시도, 체계적 불가능성 하에서의 재계획, 모호한 쿼리에 대한 인간 피드백 요청이 동적 환경에서 성능 개선
- **적응형 계획**: 실패 원인 분석(그림 4)에 따라 다양한 대응 전략(재시도, 재계획, 질문)을 자동으로 선택

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Various types of textual feedback. Success Detection gives task-specific task completion information, Passive*

- **다중 피드백 소스 통합**: Success Detector(작업 특정 성공 감지), Scene Descriptor(객체/상태 인식), Human Feedback(명확화 및 지도)을 자연어로 변환하여 프롬프트에 추가
- **Inner Monologue 프롬프트 구조**: 고수준 지시, 현재까지의 행동 이력, 최신 환경 피드백을 순차적으로 LLM 프롬프트에 포함시켜 다음 행동 예측
- **사전학습 요소 활용**: frozen LLM(GPT-3 등), 사전학습된 vision-language 모델(CLIP 등), 미리 학습된 로봇 조작 스킬 라이브러리를 조합
- **Few-shot prompting**: 추가 미세조정 없이 몇 가지 예제로 작업 형식을 지정하여 LLM이 새로운 환경과 작업에 일반화
- **피드백 기반 액션 선택**: LLM이 가능한 다음 행동들을 생성하고, 현재 상태 피드백을 고려해 실행 가능한 액션 선택

## Originality

- **피드백-인식 폐루프 계획**: 기존의 open-loop LLM 계획에서 벗어나 환경 피드백을 자연어로 인코딩하여 폐루프 계획을 구현한 점이 새로움
- **'내적 독백' 은유의 구체화**: 인간의 사고 과정을 로봇 계획에 적용하는 개념적 틀을 제시하고, 이를 LLM 프롬프팅으로 실현", '**다양한 피드백 소스의 통합**: 성공 감지, 시각적 장면 이해, 인간 상호작용을 단일 자연어 인터페이스로 통합
- **추가 학습 불필요**: 기존 기초 모델을 그대로 사용하여 새로운 환경과 작업에 즉시 적용 가능한 실용성

## Limitation & Further Study

- **피드백 제공의 의존성**: 환경 피드백(scene description, success detection)의 품질에 크게 의존하며, 부정확한 피드백이 계획을 악화시킬 수 있음
- **확장성 문제**: 복잡한 환경에서 정확한 scene description이나 success detection을 생성하기 어려울 수 있으며, 이를 위해 많은 perception 모델이 필요
- **LLM의 일반화 한계**: 학습 데이터에 없는 극단적 상황이나 창의적 해결책이 필요한 작업에서는 LLM의 성능 한계 존재
- **비용과 응답 속도**: LLM 호출의 지연과 비용이 실시간 로봇 제어에 제약이 될 수 있음
- **후속 연구 방향**: (1) 더 경량의 언어 모델로 확장 가능성 탐색, (2) 피드백 품질 향상을 위한 자동 perception 모델 개선, (3) 계획-실행 루프의 지연 감소 기술 개발, (4) 로봇 실패로부터의 학습 메커니즘 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 LLM 기반 로봇 계획에 폐루프 피드백을 자연어로 통합하는 창의적이고 실용적인 접근을 제시하며, 추가 학습 없이도 복잡한 실제 작업을 수행 가능함을 다수의 실험으로 입증했다. 다만 perception 피드백의 품질 의존성과 LLM의 고비용·지연 문제가 추후 개선 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — 둘 다 LLM을 로봇 제어에 활용하지만 Inner Monologue는 환경 피드백에, Instruct2Act는 API 기반 실행에 집중한다.
- 🔗 후속 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — 내적 독백을 통한 추론을 embodied chain-of-thought로 더 체계화하고 발전시킨 접근법이다.
- 🏛 기반 연구: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — 사고 연쇄(thought chain)를 통한 embodied reasoning의 기본 개념이 Inner Monologue에서 시작되었다.
- 🔄 다른 접근: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies와 유사하게 LLM을 활용하지만 환경 피드백 루프를 통한 내적 독백으로 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 멀티모달 LLM을 환경 피드백을 통한 폐루프 계획에 특화하여 활용한다.
- 🔗 후속 연구: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — Language to Rewards의 언어 기반 제어를 환경 피드백이 포함된 내적 독백으로 발전시킨다.
- 🔗 후속 연구: [[papers/1460_LLM3Large_Language_Model-based_Task_and_Motion_Planning_with/review]] — LLM3는 Inner Monologue의 언어 기반 추론을 Task and Motion Planning으로 확장하여 더 복잡한 계획 문제를 해결합니다.
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — Statler는 상태 유지 메커니즘을 통해 embodied 추론을 개선하는 반면, Inner Monologue는 환경 피드백 기반 내적 독백을 사용합니다.
- 🏛 기반 연구: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — CoPAL의 LLM 기반 계획 수정은 Inner Monologue가 제시한 언어 모델의 로봇 제어 적용을 발전시킨 것입니다.
- 🔗 후속 연구: [[papers/1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac/review]] — Inner Monologue의 언어 기반 추론을 embodied 환경에서 시각-행동과 통합한 발전된 형태이다.
- 🔗 후속 연구: [[papers/1422_Hi_Robot_Open-Ended_Instruction_Following_with_Hierarchical/review]] — Inner Monologue의 LLM 기반 추론을 계층적 VLM 구조로 발전시켜 더 체계적인 개방형 과제 수행을 가능하게 한다.
- 🏛 기반 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — Inner Monologue는 GLAM이 구현하는 LLM 기반 embodied agent의 환경 피드백 처리에 대한 기초 연구입니다.
- 🏛 기반 연구: [[papers/1460_LLM3Large_Language_Model-based_Task_and_Motion_Planning_with/review]] — Inner Monologue의 언어 기반 계획 및 추론은 LLM3가 구현하는 Task and Motion Planning의 기본적인 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — 둘 다 LLM 기반 로봇 제어이지만 Instruct2Act는 API 활용에, Inner Monologue는 환경 피드백에 집중한다.
- 🏛 기반 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — 장기간 작업을 위한 메모리 시스템의 기초가 되는 planning with language 개념
- 🔗 후속 연구: [[papers/1492_Neural_Brain_A_Neuroscience-inspired_Framework_for_Embodied/review]] — 신경과학적 framework는 Inner Monologue의 계획 기능을 생물학적으로 구현하는 방법을 제시합니다.
- 🏛 기반 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — Inner Monologue의 언어 모델 기반 계획 개념을 motion planning과 RL로 확장한다.
- 🔗 후속 연구: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — Inner Monologue의 언어 기반 계획이 reflection 메커니즘과 결합되어 더욱 정교한 다단계 장기 계획을 수립할 수 있다.
- 🏛 기반 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — Inner Monologue의 언어 기반 추론 메커니즘이 embodied chain-of-thought의 다단계 추론 파이프라인 설계에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and/review]] — Inner Monologue의 embodied reasoning through planning이 RoBridge의 cognition-execution bridging의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — Inner Monologue은 Statler와 유사하게 LLM의 추론을 embodied 환경에서 활용하지만 내부 독백 방식의 다른 접근법이다.
- 🏛 기반 연구: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — embodied reasoning에서 내적 독백과 사고 체인을 활용한 계획의 기반 연구입니다.
- 🔄 다른 접근: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — Inner Monologue은 TidyBot과 같은 개인화된 로봇 지원을 내부 추론 과정을 통해 달성하는 다른 방법론이다.
- 🧪 응용 사례: [[papers/1605_VIMA_General_Robot_Manipulation_with_Multimodal_Prompts/review]] — Inner Monologue가 VIMA의 멀티모달 프롬프트를 실제 대화형 로봇 추론 시나리오에 적용한 사례다.
- 🔄 다른 접근: [[papers/1370_DoReMi_Grounding_Language_Model_by_Detecting_and_Recovering/review]] — 계획-실행 불일치 감지 대신 inner monologue를 통한 다른 embodied reasoning 접근법
- 🔗 후속 연구: [[papers/1379_Embodied-R_Collaborative_Framework_for_Activating_Embodied_S/review]] — Inner Monologue의 embodied reasoning through planning이 Embodied-R에서 VLM과 LM의 협력을 통한 spatial reasoning으로 더욱 발전했다.
