---
title: "1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic"
authors:
  - "Siyuan Huang"
  - "Zhengkai Jiang"
  - "Hao Dong"
  - "Yu Qiao"
  - "Peng Gao"
date: "2023.05"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Large Language Model(LLM)을 활용하여 자연언어 및 시각적 지시사항을 로봇 조작 작업의 순차적 행동으로 매핑하는 Instruct2Act 프레임워크를 제안한다. SAM과 CLIP 같은 기초 모델들을 API로 활용하여 인식, 계획, 행동 루프를 구현하는 Python 프로그램을 생성한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Robot_Foundation_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2023_Instruct2Act Mapping Multi-modality Instructions to Robotic Actions with Large Language Model.pdf"
---

# Instruct2Act: Mapping Multi-modality Instructions to Robotic Actions with Large Language Model

> **저자**: Siyuan Huang, Zhengkai Jiang, Hao Dong, Yu Qiao, Peng Gao, Hongsheng Li | **날짜**: 2023-05-18 | **URL**: [https://arxiv.org/abs/2305.11176](https://arxiv.org/abs/2305.11176)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1:*

본 논문은 Large Language Model(LLM)을 활용하여 자연언어 및 시각적 지시사항을 로봇 조작 작업의 순차적 행동으로 매핑하는 Instruct2Act 프레임워크를 제안한다. SAM과 CLIP 같은 기초 모델들을 API로 활용하여 인식, 계획, 행동 루프를 구현하는 Python 프로그램을 생성한다.

## Motivation

- **Known**: LLM(GPT-3, ChatGPT, LLaMA 등)은 뛰어난 자연언어 이해 및 제로샷 일반화 능력을 보유하고 있다. Visual ChatGPT, VISPROG 등의 선행 연구들은 LLM과 시각 기초 모델을 결합하여 복잡한 시각 작업을 해결해왔다.
- **Gap**: 기존 CaP와 같은 방식들은 직접 정책 코드를 생성하여 높은 정밀도 요구로 인해 복잡한 지시사항 해석에 어려움을 겪는다. 다양한 양식의 지시사항을 통합적으로 처리하면서 높은 정확도를 유지할 수 있는 로봇 시스템이 부족하다.
- **Why**: 일반적 목적의 로봇 시스템은 지각, 계획, 제어를 통합해야 하며, 이를 위해 기초 모델의 강력한 능력과 로봇의 정밀한 제어 능력을 결합하는 것이 중요하다. 다양한 입력 양식을 지원하는 유연한 시스템은 로봇의 실용성과 적용 범위를 크게 확대할 수 있다.
- **Approach**: LLM의 인컨텍스트 학습 능력을 활용하여 멀티모달 지시사항으로부터 중간 수준의 의사결정 행동을 생성한다. SAM으로 객체 위치를 파악하고 CLIP으로 분류한 후, 이 정보를 로봇 스킬과 결합하여 LLM이 결정-행동 코드를 생성하도록 한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Evaluation task suite. We select six tabletop manipulation meta tasks to evaluate the pro-*

- **일반적 목적의 로봇 시스템**: LLM과 멀티모달 기초 모델을 활용한 유연한 로봇 시스템 구축으로 자연언어 및 시각적 지시사항을 모두 처리 가능
- **제로샷 성능 우수성**: 학습 기반의 최신 정책들을 능가하는 성능을 달성하면서도 미세 조정(fine-tuning) 없이 동작
- **낮은 적응 오버헤드**: 기초 모델 적응 비용이 미미하여 처음부터 학습하는 방식 대비 효율성 우수
- **다양한 작업 영역 검증**: 단순 객체 조작, 시각적 목표 도달, 시각적 추론 등 여러 도메인과 시나리오에서 VIMABench의 6개 메타-작업으로 검증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: The paradigm of our proposed Instruct2Act framework. Starting with the task instruc-*

- 인식 단계: SAM API를 통해 이미지 분할로 후보 객체 탐지, CLIP을 이용한 객체 분류
- 계획 단계: LLM이 인식 결과와 로봇 스킬(GetObsImage, PickPlace, RearrangeActions 등)을 활용한 Python 프로그램 생성
- 행동 단계: 생성된 프로그램의 실행으로 로봇 조작(RobotExecution, SpeedSet 등) 수행
- 멀티모달 지시사항 처리: 단일 모달 및 멀티 모달 지시사항 검색 아키텍처를 통해 다양한 입력 유형 처리
- 모듈식 계층 구조: 핵심 모듈, 로봇 API, 지각/행동 모듈을 계층적으로 정의하여 확장성 제공

## Originality

- LLM의 프로그램 생성 능력과 기초 모델들(SAM, CLIP)을 API 기반으로 결합하는 새로운 아키텍처 제안
- 직접 정책 코드 생성이 아닌 중간 수준의 의사결정 행동 생성으로 오류율 감소 달성
- 자연언어, 이미지, 심볼 등 다양한 양식의 멀티모달 지시사항을 통일된 프레임워크로 처리
- 기초 모델들을 미세 조정 없이 읽기 전용(frozen) 방식으로 활용하여 비용 효율성 확보

## Limitation & Further Study

- 테이블탑 조작 도메인에 제한되어 있으며, 더 복잡한 3D 환경이나 다른 로봇 플랫폼에의 일반화 검증 필요
- LLM의 성능이 모델 선택에 의존하며, 프롬프트 설계 및 API 정의가 성공 여부에 큰 영향을 미침
- 시각적 혼동이나 기초 모델의 오류가 누적될 수 있는 구조로, 오류 전파(error cascading) 메커니즘 분석 부족
- 실시간 피드백 루프와 실패 복구 메커니즘에 대한 상세한 논의 필요
- 정량적 성능 비교에서 기존 학습 기반 방법들과의 더 광범위한 비교 실험 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 LLM과 시각 기초 모델을 효과적으로 결합하여 멀티모달 지시사항을 로봇 행동으로 매핑하는 실용적인 프레임워크를 제시하며, 학습 없는 제로샷 방식으로 우수한 성능을 달성했다는 점에서 의의가 있다. 다만 평가 범위가 제한적이고 오류 전파 메커니즘에 대한 분석이 보완되어야 할 것으로 판단된다.

## Related Papers

- 🔄 다른 접근: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — 둘 다 LLM 기반 로봇 제어이지만 Instruct2Act는 API 활용에, Inner Monologue는 환경 피드백에 집중한다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — LLM 코드 생성을 로봇 제어에 활용하는 기본 아이디어가 Instruct2Act의 Python 프로그램 생성에 적용되었다.
- 🔗 후속 연구: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — LLM을 통한 로봇 행동 계획을 corrective planning으로 더 발전시켜 오류 수정 능력을 추가했다.
- 🏛 기반 연구: [[papers/1506_Open-World_Object_Manipulation_using_Pre-trained_Vision-Lang/review]] — Open-World Object Manipulation의 기본 개념을 LLM과 foundation model API로 구현하는 구체적 프레임워크를 제시한다.
- 🧪 응용 사례: [[papers/1569_Segment_Anything/review]] — Segment Anything을 로봇 조작의 객체 인식 API로 활용하여 multimodal instruction을 action으로 매핑한다.
- 🔄 다른 접근: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — SayCan과 Instruct2Act 모두 언어 지시를 로봇 행동으로 변환하지만 affordance 기반 vs API 호출 방식의 차이가 있음
- 🏛 기반 연구: [[papers/1422_Hi_Robot_Open-Ended_Instruction_Following_with_Hierarchical/review]] — Instruct2Act의 multi-modal instruction mapping을 계층적 VLM 구조로 발전시킨 확장 연구이다.
- 🔄 다른 접근: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — 둘 다 LLM을 로봇 제어에 활용하지만 Inner Monologue는 환경 피드백에, Instruct2Act는 API 기반 실행에 집중한다.
- 🔄 다른 접근: [[papers/1605_VIMA_General_Robot_Manipulation_with_Multimodal_Prompts/review]] — Instruct2Act는 VIMA와 같은 다중모달 명령을 로봇 행동으로 매핑하지만 다른 아키텍처를 사용한다.
- 🔄 다른 접근: [[papers/1297_A_Real-to-Sim-to-Real_Approach_to_Robotic_Manipulation_with/review]] — 둘 다 multimodal instruction을 로봇 행동으로 매핑하지만 IKER는 keypoint 기반 reward에, Instruct2Act는 직접적인 action mapping에 중점을 둡니다.
- 🧪 응용 사례: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — Instruct2Act은 ALFRED와 같은 벤치마크에서 평가될 수 있는 multi-modal instruction mapping의 구체적 구현입니다.
