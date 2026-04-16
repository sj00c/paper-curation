---
title: "1444_Language_to_Rewards_for_Robotic_Skill_Synthesis"
authors:
  - "Wenhao Yu"
  - "Nimrod Gileadi"
  - "Chuyuan Fu"
  - "Sean Kirmani"
  - "Kuang-Huei Lee"
date: "2023.06"
doi: ""
arxiv: ""
score: 4.0
essence: "LLM을 이용하여 자연어 명령을 보상 함수로 변환하고, 실시간 최적화기(MuJoCo MPC)로 로봇 행동을 합성하는 새로운 패러다임을 제시한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robot_Policy_Learning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Deep_Reinforcement_Learning_Applications"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yu et al._2023_Language to Rewards for Robotic Skill Synthesis.pdf"
---

# Language to Rewards for Robotic Skill Synthesis

> **저자**: Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, Brian Ichter, Ted Xiao, Peng Xu, Andy Zeng, Tingnan Zhang, Nicolas Heess, Dorsa Sadigh, Jie Tan, Yuval Tassa, Fei Xia | **날짜**: 2023-06-14 | **URL**: [https://arxiv.org/abs/2306.08647](https://arxiv.org/abs/2306.08647)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: LLMs have some internal knowledge about robot motions, but cannot directly translate them into actions*

LLM을 이용하여 자연어 명령을 보상 함수로 변환하고, 실시간 최적화기(MuJoCo MPC)로 로봇 행동을 합성하는 새로운 패러다임을 제시한다.

## Motivation

- **Known**: LLM은 논리 추론, 코드 생성 등에서 우수하나 저수준 로봇 동작은 훈련 데이터 부족으로 직접 생성하기 어렵다. 기존 방법들은 LLM을 의미론적 계획기로만 사용하거나 수동으로 설계된 제어 원시(primitives)에 의존한다.
- **Gap**: 자연어 명령과 저수준 로봇 동작 사이의 추상화 수준 간극이 크다. 보상 함수의 의미적 풍부성과 모듈성이 LLM과 로봇 제어 사이의 중간 인터페이스로 활용될 수 있다는 점이 미충분하게 탐구되었다.
- **Why**: LLM 기반 로봇 제어는 사용자가 저수준 엔지니어링 지식 없이도 대화형으로 복잡한 로봇 행동을 생성할 수 있게 하며, 확장 가능하고 유연한 로봇 스킬 합성을 가능케 한다.
- **Approach**: LLM의 코드 작성 능력을 활용하여 자연어 명령을 보상 함수 코드로 변환한 후, MuJoCo MPC 최적화기로 실시간 로봇 행동을 합성하고 사용자 피드백을 통해 반복적으로 개선한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Comparison of our method and alternative methods in terms of pass rate: if we generate N pieces of code*

- **방법론의 효과성**: 시뮬레이션된 사족 로봇과 손재주 있는 조작 로봇에서 설계한 17개 작업의 90%를 성공적으로 해결하며, 코드 기반 원시 스킬 기준선(50%)보다 40% 더 높은 성능 달성
- **실제 로봇 검증**: 실제 로봇 팔에서 비파지형 밀기(non-prehensile pushing)와 같은 복잡한 조작 스킬이 대화형 시스템을 통해 자발적으로 나타남
- **대화형 사용자 경험**: 사용자가 즉시 결과를 관찰하고 피드백을 제공할 수 있는 대화형 행동 생성 시스템 구현

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Detailed dataflow of the Reward Translator. A Motion Descriptor LLM takes the user input and describe*

- Motion Descriptor LLM이 사용자 자연어 입력을 분석하여 로봇 상태와 행동의 특성을 추출
- Reward Translator가 추출된 특성을 파라미터화된 보상 함수 코드로 변환 (Python 코드 생성)
- Motion Controller가 생성된 보상을 MuJoCo MPC를 통해 최적화하여 저수준 동작 명령 생성
- 사용자가 결과를 관찰하고 언어 수정사항을 제공하면 시스템이 반복적으로 보상 함수를 개선
- 보상 함수의 모듈성을 활용하여 토크, 발 위치, 몸통 상태 등 다양한 목표를 독립적으로 명시

## Originality

- 자연언어를 직접 저수준 동작으로 변환하는 대신 보상 함수를 중간 인터페이스로 사용하는 새로운 패러다임
- LLM의 코드 생성 능력을 보상 함수 작성에 처음 적용하여 데이터 효율적인 접근법 제시
- 실시간 최적화(MuJoCo MPC)와 LLM을 결합하여 대화형 피드백 루프를 가능하게 함
- 기존 언어-보상 연구와 달리 학습 데이터 없이 LLM만으로 보상 생성 가능하게 함

## Limitation & Further Study

- 17개 작업은 상대적으로 제한된 범위이며, 더 복잡하고 다양한 현실 세계 작업에서의 일반화 가능성 불명확
- LLM이 생성한 보상 함수의 품질이 LLM의 능력과 프롬프트 설계에 크게 의존하여 재현성과 안정성 문제 가능성
- 실제 로봇 실험이 단일 로봇 팔에 제한되어 있으며, 다양한 로봇 플랫폼에서의 성능 검증 필요
- MuJoCo MPC의 계산 비용과 하드웨어 요구사항이 배포 가능성을 제한할 수 있음
- 후속 연구: 다중 모달리티 입력(이미지, 비디오) 활용, 강화학습과의 결합, 부안전한 행동에 대한 제약 조건 명시 방법 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 LLM을 보상 함수 생성기로 활용하여 자연언어와 저수준 로봇 동작 사이의 간극을 효과적으로 해소하는 혁신적인 접근법을 제시한다. 강력한 실험 결과와 실제 로봇 검증을 통해 방법론의 타당성을 입증하며, 로봇 제어에서 LLM 활용의 새로운 방향을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — 언어를 보상으로 변환하는 기본 개념이 ELLM의 LLM 기반 RL 가이던스에 적용되었다.
- 🔗 후속 연구: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — 언어를 보상으로 변환하는 개념을 reward shaping으로 더 체계화하고 일반화한 접근법이다.
- 🔄 다른 접근: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — 둘 다 언어 기반 로봇 제어이지만 Language to Rewards는 보상 함수에, Do As I Can은 직접적인 행동 생성에 집중한다.
- 🔗 후속 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — Language to Rewards의 자연어-보상 변환이 Plan-Seq-Learn의 언어 기반 계획 수립과 결합되어 더 복잡한 로봇 스킬 합성을 가능하게 한다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Language to Rewards가 Code as Policies의 언어-코드 변환 철학을 보상 함수 설계 영역으로 확장한 접근법이다.
- 🔗 후속 연구: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — ExploRLLM은 Language to Rewards의 LLM 기반 보상 생성을 탐색 가이드로 활용하여 실제 RL 학습에 적용합니다.
- 🔗 후속 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Language to Rewards의 언어 기반 제어를 환경 피드백이 포함된 내적 독백으로 발전시킨다.
- 🔗 후속 연구: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — Language to Rewards의 개념을 RL 사전학습에서 LLM 가이드 탐색으로 발전시켰다.
- 🏛 기반 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — PSL의 language model guided RL을 위한 language to rewards mapping과 skill synthesis의 이론적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A/review]] — Language to Rewards는 언어 기반 로봇 스킬 합성에서 LLM을 활용하지만 보상 신호 생성에 집중하는 다른 접근법이다.
- 🔄 다른 접근: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — Language to Rewards는 Text2Reward와 동일한 언어-보상 변환 문제를 다른 방법론으로 접근한다.
- 🏛 기반 연구: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — 자연어로부터 로봇 행동을 학습하기 위한 language-to-reward 기본 패러다임을 제시합니다.
- 🏛 기반 연구: [[papers/1321_Bootstrap_Your_Own_Skills_Learning_to_Solve_New_Tasks_with_L/review]] — Language to Rewards의 언어 기반 보상 설계는 BOSS의 LLM 가이드 스킬 학습에 핵심적인 기반 메커니즘을 제공한다.
- 🔗 후속 연구: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — Language to Rewards가 ExploRLLM의 LLM 가이드 탐색을 보상 설계를 통한 스킬 합성으로 확장합니다.
- 🔗 후속 연구: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — 언어를 보상으로 변환하는 로봇 스킬 합성으로 language-conditioned manipulation을 확장한다.
