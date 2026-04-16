---
title: "1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro"
authors:
  - "Jacky Liang"
  - "Wenlong Huang"
  - "Fei Xia"
  - "Peng Xu"
  - "Karol Hausman"
date: "2022.09"
doi: ""
arxiv: ""
score: 4.0
essence: "Large Language Model(LLM)을 활용하여 자연어 명령을 로봇 정책 코드로 직접 변환하는 \"Code as Policies\" 방식을 제안하며, few-shot prompting과 hierarchical code-gen을 통해 복잡한 로봇 행동을 실시간으로 생성한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Robot_Foundation_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liang et al._2022_Code as Policies Language Model Programs for Embodied Control.pdf"
---

# Code as Policies: Language Model Programs for Embodied Control

> **저자**: Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, Andy Zeng | **날짜**: 2022-09-16 | **URL**: [https://arxiv.org/abs/2209.07753](https://arxiv.org/abs/2209.07753)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Given examples (via few-shot prompting), robots can use code-writing*

Large Language Model(LLM)을 활용하여 자연어 명령을 로봇 정책 코드로 직접 변환하는 "Code as Policies" 방식을 제안하며, few-shot prompting과 hierarchical code-gen을 통해 복잡한 로봇 행동을 실시간으로 생성한다.

## Motivation

- **Known**: LLM은 docstring으로부터 Python 프로그램을 합성할 수 있으며, 로봇 제어에 대해 기존에는 고정된 스킬 세트를 조합하거나 대규모 데이터로 end-to-end 학습하는 방식이 사용되어 왔다.
- **Gap**: 기존 LLM 기반 로봇 제어 방식은 인식-행동 피드백 루프에 직접 영향을 미치지 못하여, 새로운 스킬 추가 시 추가 학습 데이터가 필요하고 공간 관계 이해 및 모호한 명령("더 빠르게")의 정량화가 어렵다.
- **Why**: 로봇이 자연어로 표현된 복잡한 작업을 데이터 수집 없이 실시간으로 학습·수행할 수 있다면, 로봇의 범용성과 사용 편의성이 크게 향상되며 인간-로봇 상호작용의 새로운 가능성이 열린다.
- **Approach**: Code-writing LLM에 few-shot prompt로 예제 명령과 대응하는 정책 코드를 제공하여, 새로운 명령에 대해 perception API(객체 감지)와 control primitive API를 조합한 Python 코드를 자동으로 생성하게 한다. Hierarchical code-gen을 통해 미정의 함수를 재귀적으로 정의하여 복잡도를 증가시킨다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Code as Policies can follow natural language instructions across diverse domains and robots: table-top manipulat*

- **Code as Policies 방식론**: LMP(Language Model Programs)를 로봇 정책 표현으로 사용하여 reactive policy(impedance controller)와 waypoint-based policy(vision-based pick and place, trajectory control) 모두 표현 가능
- **Hierarchical code-gen**: 재귀적 함수 정의를 통해 더 복잡한 코드 생성이 가능하며, HumanEval 벤치마크에서 39.8% P@1 달성으로 기존 최고 성능 개선
- **다중 로봇 플랫폼 검증**: 테이블탑 조작, 2D 도형 그리기, 이동형 조작 등 다양한 도메인과 로봇 시스템에서 실제 동작 입증
- **로봇 특화 벤치마크**: 로봇 코드 생성 문제 평가를 위한 새로운 벤치마크 제시

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Given examples (via few-shot prompting), robots can use code-writing*

- Few-shot prompting: 자연어 명령을 주석 형태로, 대응하는 정책 코드를 예제로 제공하여 in-context learning 활성화
- Perception-Action 연결: detect_objects(), is_empty() 등 perception API와 robot.set_velocity(), pick_place() 등 control primitive API를 Python 코드에서 조합
- Hierarchical code-gen: 미정의 함수에 대해 LLM을 재귀적으로 호출하여 함수 정의를 자동으로 생성
- Third-party library 활용: NumPy(점 보간), Shapely(도형 생성/분석) 등 기존 라이브러리를 통한 공간-기하 추론
- Control parameter 추론: 모호한 표현("faster", "to the left")을 코드 문맥에 기반하여 구체적인 수치값(속도, 위치)으로 변환
- 대화형 인터페이스: say() API를 통해 로봇이 자신의 행동을 언어로 설명하는 human-robot dialogue 구현

## Originality

- 기존의 LLM 기반 로봇 제어가 고수준 planning만 담당하던 것에서 벗어나, policy code 생성을 통해 저수준 control까지 통합한 end-to-end 접근법이 창신
- Hierarchical code-gen이 단순 코드 완성을 넘어 자동으로 복잡도를 증가시키는 재귀적 구조는 로봇 정책 합성에 맞춤화된 기술
- 공간 관계, 객체 관계, 행동의 세기 등을 단일 Python 코드로 표현하여 모호성 제거와 일반화를 동시에 달성하는 통합 표현 방식

## Limitation & Further Study

- LLM의 hallucination 및 구문 오류 가능성: 생성된 코드의 안정성과 신뢰성에 대한 검증 메커니즘이 부재할 수 있음
- Perception API의 정확도 의존성: 객체 감지 오류가 정책 실행을 크게 방해할 수 있으나, 논문에서 perception robustness 분석이 제한적
- 실시간 성능: LLM 추론 시간이 로봇의 빠른 반응을 요구하는 고속 제어에 적합한지 미확인
- Scalability 문제: 매우 복잡한 다단계 작업이나 high-frequency control에서의 성능 한계 가능성
- 후속 연구: 생성 코드의 정확성 검증 및 자동 수정 메커니즘, 실시간 성능 최적화, 실패 복구 능력 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 LLM을 로봇 정책 생성에 직접 적용하는 창의적인 방식을 제시하며, hierarchical code-gen을 통한 성능 개선과 다양한 실제 로봇 플랫폼에서의 검증으로 강한 임팩트를 가진다. 다만 생성 코드의 안정성 검증과 실시간 성능 평가가 보완되면 더욱 완성도 높은 연구가 될 것이다.

## Related Papers

- 🔗 후속 연구: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — LLM의 코드 생성을 로봇 정책에서 시뮬레이션 태스크 생성으로 확장하여 더 넓은 활용 범위 제공
- 🏛 기반 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — interactive environment에서의 LLM 기반 학습이 code as policies의 실시간 정책 생성 개념의 기반
- 🔗 후속 연구: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — Code as Policies의 LLM 코드 생성과 Do As I Can의 언어-로봇 스킬 결합은 자연어 명령을 로봇 행동으로 변환하는 상호 보완적 접근법이다.
- 🧪 응용 사례: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — Text2Reward의 언어 모델 기반 보상 설계는 Code as Policies의 자연어-코드 변환을 강화학습에 구체적으로 적용한다.
- 🔗 후속 연구: [[papers/1370_DoReMi_Grounding_Language_Model_by_Detecting_and_Recovering/review]] — DoReMi의 계획-실행 불일치 탐지가 Code as Policies의 실시간 코드 생성을 보완합니다.
- 🔄 다른 접근: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — LLM 기반 로봇 제어에서 코드 생성 방식과 계층적 계획-재계획 방식이 다른 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — 제약 인식 시각 프로그래밍이 Code as Policies의 코드 생성에 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Code as Policies와 유사하게 LLM을 활용하지만 환경 피드백 루프를 통한 내적 독백으로 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — LLM의 코드 생성 능력을 로봇 제어에 활용하는 기본 아이디어가 GenSim의 시뮬레이션 작업 생성에 적용되었다.
- 🔄 다른 접근: [[papers/1460_LLM3Large_Language_Model-based_Task_and_Motion_Planning_with/review]] — 동일한 LLM 기반 작업 계획 문제에 대해 코드 생성 vs 모션 계획 실패 추론이라는 서로 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — LM-Nav의 사전학습 모델 조합 접근법이 Code as Policies의 언어 모델 프로그램으로 더 복잡한 embodied 제어로 확장됩니다.
- 🏛 기반 연구: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — LLM 코드 생성을 로봇 제어에 활용하는 기본 아이디어가 Instruct2Act의 Python 프로그램 생성에 적용되었다.
- 🏛 기반 연구: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — Language to Rewards가 Code as Policies의 언어-코드 변환 철학을 보상 함수 설계 영역으로 확장한 접근법이다.
- 🔄 다른 접근: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — PSL의 LLM 기반 high-level planning과 달리 Code as Policies는 언어 모델을 직접 executable code로 변환하여 embodied control을 수행한다.
- 🔗 후속 연구: [[papers/1505_Open-vocabulary_Queryable_Scene_Representations_for_Real_Wor/review]] — code as policies의 개념을 open-vocabulary scene representation과 결합하여 더 유연하고 쿼리 가능한 로봇 계획 시스템을 구축한다.
- 🔗 후속 연구: [[papers/1506_Open-World_Object_Manipulation_using_Pre-trained_Vision-Lang/review]] — Code as Policies의 언어 기반 제어 개념을 pre-trained VLM과 결합하여 발전시킨다.
- 🏛 기반 연구: [[papers/1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A/review]] — Code as Policies의 언어 모델 프로그램 기반 embodied control 개념이 LLM 기반 고수준 계획의 이론적 기초가 된다.
- 🏛 기반 연구: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — Code as Policies의 언어 기반 로봇 제어 개념이 RT-H의 언어 모션 예측과 행동 계층 구조 설계에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — Code as Policies의 언어 모델 기반 계획 패러다임을 3D Scene Graph 환경으로 확장한 접근법입니다.
- 🔗 후속 연구: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — Code as Policies의 언어 모델 기반 제어를 개인화된 물건 정리라는 구체적 도메인에 적용하여 실용성을 높인다.
- 🔗 후속 연구: [[papers/1594_Transferring_Foundation_Models_for_Generalizable_Robotic_Man/review]] — 언어 모델을 로봇 제어에 활용하는 Code as Policies의 개념을 foundation model 전이 학습으로 확장한 연구입니다.
- 🏛 기반 연구: [[papers/1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-/review]] — Code as Policies의 언어 모델 프로그래밍 패러다임이 TRAVEL의 LLM/VLM 기반 모듈식 접근법의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — Code as Policies와 함께 LLM의 코드 생성 능력을 로봇 제어에 활용하지만, VoxPoser는 3D value map에 특화되어 있다
- 🔄 다른 접근: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — LLM 기반 로봇 제어에서 계층적 계획-재계획과 직접 코드 생성이 다른 오류 처리 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — Do As I Can의 언어-로봇 스킬 grounding과 Code as Policies의 LLM 코드 생성은 자연어 명령을 로봇 행동으로 변환하는 상호 보완적 접근법이다.
- 🏛 기반 연구: [[papers/1370_DoReMi_Grounding_Language_Model_by_Detecting_and_Recovering/review]] — Code as Policies의 실시간 코드 생성이 DoReMi의 계획-실행 불일치 탐지에 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1321_Bootstrap_Your_Own_Skills_Learning_to_Solve_New_Tasks_with_L/review]] — 언어 모델을 구체화 제어에 활용하는 기초적인 접근 방식을 제시합니다.
- 🔗 후속 연구: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — Code as Policies는 ExploRLLM의 LLM 정책 코드 생성 아이디어를 실제 로봇 제어에 적용합니다.
- 🔗 후속 연구: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — Code as Policies의 정책 생성을 제약 조건 모니터링으로 확장하여 더 안전한 로봇 실행 보장
