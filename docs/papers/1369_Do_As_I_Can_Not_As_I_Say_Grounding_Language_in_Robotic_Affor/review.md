---
title: "1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor"
authors:
  - "Michael Ahn"
  - "Anthony Brohan"
  - "Noah Brown"
  - "Yevgen Chebotar"
  - "Omar Cortes"
date: "2022.04"
doi: ""
arxiv: ""
score: 4.0
essence: "Large Language Models(LLM)의 의미론적 지식과 로봇의 실행 가능한 스킬을 결합하여, LLM을 affordance function으로 grounding함으로써 자연어 명령을 실제 로봇 행동으로 변환한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ahn et al._2022_Do As I Can, Not As I Say Grounding Language in Robotic Affordances.pdf"
---

# Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

> **저자**: Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, Andy Zeng | **날짜**: 2022-04-04 | **URL**: [https://arxiv.org/abs/2204.01691](https://arxiv.org/abs/2204.01691)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: LLMs have not interacted with their environment and observed the outcome of their responses, and*

Large Language Models(LLM)의 의미론적 지식과 로봇의 실행 가능한 스킬을 결합하여, LLM을 affordance function으로 grounding함으로써 자연어 명령을 실제 로봇 행동으로 변환한다.

## Motivation

- **Known**: LLM은 방대한 텍스트 데이터로부터 의미론적 지식을 인코딩할 수 있으나, 실제 물리적 세계와의 상호작용 경험이 부족하여 구체적인 로봇 실행에 부적절한 제안을 생성하는 경향이 있다.
- **Gap**: LLM의 고수준 의미론적 지식과 로봇이 실제로 실행 가능한 저수준 스킬 간의 gap을 해소하여, 추상적이고 장기간에 걸친 자연어 명령을 로봇이 실제로 수행할 수 있도록 해야 한다.
- **Why**: 자연어로 표현된 복잡한 로봇 작업 명령을 실행하려면 LLM의 지식과 로봇의 실행 능력을 통합해야 하며, 이는 일상적 로봇 어시스턴트의 실현에 필수적이다.
- **Approach**: SayCan 방법으로, LLM이 p(ℓπ|i)(task-grounding)를 제공하고 pretrained skills의 value function이 p(cπ|s, ℓπ)(world-grounding)를 제공하여, 두 확률을 곱함으로써 각 스킬의 성공 가능성을 판단한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: The experiments were performed in an ofﬁce kitchen and a mock kitchen mirroring this setup, with 5*

- **실세계 grounding의 필요성 입증**: affordance function으로 LLM을 grounding하지 않은 baseline 대비 거의 2배 성능 향상
- **장기간 추상 명령 실행**: 모바일 매니퓨레이터가 장기간(long-horizon), 추상적 자연어 명령을 zero-shot으로 실행 가능
- **확장성 검증**: 다양한 LLM 모델 사용 시 기본 언어모델 개선만으로도 로봇 성능 향상 확인
- **101개 실세계 작업 평가**: 실제 주방 환경에서 다양한 로봇 작업을 통해 방법론 검증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: A value function module (a) is queried to form a value function space of action primitives based on*

- LLM을 사용하여 각 available skill의 description ℓπ에 대해 p(ℓπ|i) 확률 계산 (task-grounding)
- 각 skill π에 대해 RL로 학습된 language-conditioned value function으로 p(cπ|s, ℓπ) affordance function 획득 (world-grounding)
- 두 확률의 곱 p(ci|i, s, ℓπ) ∝ p(cπ|s, ℓπ)p(ℓπ|i)로 현재 상태에서 가장 실행 가능한 스킬 선택
- 선택된 스킬들을 순차적으로 실행하여 최종 목표 달성
- Temporal-difference RL 방식으로 sparse reward(성공 1.0, 실패 0.0)를 통해 value function 학습

## Originality

- LLM의 task-grounding과 affordance function의 world-grounding을 명시적으로 분리하고 곱셈으로 결합하는 새로운 framework 제안
- LLM을 단순히 명령 해석 도구가 아닌 스킬 선택 점수 생성기로 활용하는 novel한 접근
- 로봇 affordance와 언어모델을 직접 연결하는 방식으로, 기존의 별도 semantics-to-action mapping 모듈의 필요성 제거
- 실세계 로봇 플랫폼에서 검증된 최초의 대규모 LLM-로봇 통합 시스템 중 하나

## Limitation & Further Study

- **skill 집합의 사전 정의 필요**: 새로운 작업 영역에서는 available skills와 그 description을 미리 정의해야 하므로, 확장성에 제약
- **affordance function 학습 비용**: 각 skill마다 RL 학습이 필요하며, 이는 상당한 데이터와 계산 자원 소요
- **LLM의 hallucination**: LLM이 존재하지 않는 스킬이나 불합리한 skill sequence를 제안할 수 있으나, affordance function이 이를 완전히 필터링하지 못할 가능성
- **후속 연구 방향**: (1) 자동 skill 발견 및 설명 생성 메커니즘 개발, (2) 새로운 환경/로봇으로의 빠른 adaptation 방법, (3) 부분 실패 상황에서의 error recovery 메커니즘 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LLM과 로봇의 embodied skills을 결합하는 원칙적이고 효과적인 방법을 제시하며, 실세계 검증을 통해 자연어 기반 로봇 제어의 실용성을 입증한 영향력 높은 연구이다.

## Related Papers

- 🔗 후속 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Do As I Can의 언어-로봇 스킬 grounding과 Code as Policies의 LLM 코드 생성은 자연어 명령을 로봇 행동으로 변환하는 상호 보완적 접근법이다.
- 🧪 응용 사례: [[papers/1546_Robot_Utility_Models_General_Policies_for_Zero-Shot_Deployme/review]] — Robot Utility Models의 제로샷 배포는 Do As I Can의 LLM affordance function grounding을 실제 로봇 정책으로 구현한다.
- 🏛 기반 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — 대형 언어 모델의 인터랙티브 환경 grounding은 Do As I Can의 affordance function 설계에 핵심적인 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — Plan-Seq-Learn의 language model guided RL과 Do As I Can의 affordance function 접근은 언어와 로봇 행동 연결에서 서로 다른 학습 패러다임을 사용한다.
- 🏛 기반 연구: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — Text2Reward의 언어를 통한 reward shaping 개념이 Do As I Can에서 제시된 언어 기반 로봇 행동 grounding의 기초적 아이디어를 제공한다.
- 🔄 다른 접근: [[papers/1404_Gemini_Robotics_Bringing_AI_into_the_Physical_World/review]] — SayCan과 Gemini Robotics 모두 LLM을 로봇 제어에 활용하지만 affordance grounding vs 직접 제어의 차이가 있음
- 🔄 다른 접근: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — SayCan과 Instruct2Act 모두 언어 지시를 로봇 행동으로 변환하지만 affordance 기반 vs API 호출 방식의 차이가 있음
- 🔄 다른 접근: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — 둘 다 언어 기반 로봇 제어이지만 Language to Rewards는 보상 함수에, Do As I Can은 직접적인 행동 생성에 집중한다.
- 🏛 기반 연구: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — 언어 기반 affordance 추론의 기본 개념을 제공하여 UniAff의 통일된 affordance 표현에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — 언어 기반 affordance 추론의 기본 개념을 제공하여 VoxPoser의 LLM affordance reasoning에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1301_A3VLM_Actionable_Articulation-Aware_Vision_Language_Model/review]] — 로봇 어포던스 기반 언어 학습의 이론적 기반을 관절 인식 VLM으로 확장합니다.
- 🔗 후속 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 LLM 코드 생성과 Do As I Can의 언어-로봇 스킬 결합은 자연어 명령을 로봇 행동으로 변환하는 상호 보완적 접근법이다.
