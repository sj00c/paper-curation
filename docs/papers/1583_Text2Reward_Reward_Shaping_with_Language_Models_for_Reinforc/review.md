---
title: "1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc"
authors:
  - "Tianbao Xie"
  - "Siheng Zhao"
  - "Chen Henry Wu"
  - "Yitao Liu"
  - "Qian Luo"
date: "2023.09"
doi: ""
arxiv: ""
score: 4.0
essence: "LLM을 활용하여 자연어로 기술된 목표로부터 자동으로 dense reward function을 생성하고 형성하는 data-free 프레임워크 Text2Reward를 제시한다. 생성된 reward code는 해석 가능하고 실행 가능한 프로그램 형태로, 기존의 inverse RL이나 sparse reward 기반 방법들보다 넓은 범위의 작업을 지원한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/LLM-Based_Reward_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xie et al._2023_Text2Reward Reward Shaping with Language Models for Reinforcement Learning.pdf"
---

# Text2Reward: Reward Shaping with Language Models for Reinforcement Learning

> **저자**: Tianbao Xie, Siheng Zhao, Chen Henry Wu, Yitao Liu, Qian Luo, Victor Zhong, Yanchao Yang, Tao Yu | **날짜**: 2023-09-20 | **URL**: [https://arxiv.org/abs/2309.11489](https://arxiv.org/abs/2309.11489)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: An overview of TEXT2REWARD of three stages: Expert Abstraction provides an abstraction*

LLM을 활용하여 자연어로 기술된 목표로부터 자동으로 dense reward function을 생성하고 형성하는 data-free 프레임워크 Text2Reward를 제시한다. 생성된 reward code는 해석 가능하고 실행 가능한 프로그램 형태로, 기존의 inverse RL이나 sparse reward 기반 방법들보다 넓은 범위의 작업을 지원한다.

## Motivation

- **Known**: Reward shaping은 RL의 오랜 숙제이며, 전통적으로 전문가의 수작업을 요구한다. Inverse RL과 preference learning은 시연 데이터나 인간 피드백에 의존하고 해석성이 낮은 문제가 있다.
- **Gap**: LLM을 사용한 reward code 생성 기존 연구는 sparse reward나 상수 형태의 unshaped dense reward만 생성한다. 해석 가능하면서도 동적으로 변하는 free-form dense reward code를 자동으로 생성하고 human feedback으로 반복 개선하는 방법이 부족하다.
- **Why**: Reward 설계 자동화는 RL 개발 비용을 대폭 낮출 수 있으며, 해석 가능한 코드 형태의 reward는 debugging과 refinement가 용이하다. Human-in-the-loop 방식으로 실무적 적용성을 높일 수 있다.
- **Approach**: LLM에 natural language instruction, 환경의 Pythonic 추상화 표현, background knowledge, few-shot examples을 입력하여 executable reward code를 생성한다. 코드 실행 피드백으로 구문/런타임 오류를 자동 수정하고, 정책 학습 후 human feedback으로 reward code를 반복 개선한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Learning curves on MANISKILL2 under zero-shot and few-shot reward generation settings,*

- **조작 작업 성능**: ManiSkill2와 MetaWorld의 17개 작업 중 13개에서 생성된 reward code가 전문가 작성 코드와 동등하거나 우수한 성공률과 수렴 속도 달성
- **새로운 운동 행동 학습**: MuJoCo 환경에서 6개의 새로운 locomotion behavior를 94% 이상의 성공률로 학습
- **실제 로봇 배포**: 시뮬레이터에서 학습한 정책이 실제 Franka Panda 로봇에 성공적으로 배포됨
- **Human feedback 효율성**: 3회 미만의 human feedback으로 성공률을 0에서 거의 100%로 향상 및 task ambiguity 해결
- **높은 해석성**: 생성된 reward가 코드 형태로 명확히 읽고 이해할 수 있음

## How

![Figure 1](figures/fig1.webp)

*Figure 1: An overview of TEXT2REWARD of three stages: Expert Abstraction provides an abstraction*

- Pythonic 클래스 기반 환경 추상화로 LLM이 객체 상태와 호출 가능 함수를 명확히 이해하도록 표현
- NumPy/SciPy 등 기존 패키지의 함수 정보와 사용 예시를 background knowledge로 제공
- Instruction embedding을 통해 유사한 instruction-code 쌍을 few-shot examples로 동적 선택
- 생성된 코드를 즉시 실행하여 구문 오류, 런타임 오류를 감지하고 LLM으로 반복 수정
- 정책 학습 후 롤아웃 실행 결과를 바탕으로 사용자로부터 실패 모드나 선호도 피드백 수집
- Human feedback을 prompt에 반영하여 reward code를 반복적으로 개선하는 interactive loop 구성

## Originality

- Data-free 방식으로 전문가 시연이나 선호도 데이터 수집 없이 reward code 자동 생성
- Free-form shaped dense reward code 생성으로 기존의 sparse reward나 constant function 방식보다 표현력 확장
- 코드 실행 피드백을 통한 자동 error correction으로 생성 코드의 실행 가능성 보장
- Human-in-the-loop refinement pipeline으로 task ambiguity와 sub-optimal behavior를 실용적으로 해결
- Pythonic 환경 표현으로 여러 로봇 벤치마크(ManiSkill2, MetaWorld, MuJoCo)에 걸친 일반화 가능성 입증

## Limitation & Further Study

- LLM의 능력에 의존하므로 모델 성능이 제한되면 생성 quality도 제한됨 (논문에서 GPT-4/Codex 기반)
- 환경 추상화 설계가 여전히 수동적이며, 새로운 환경마다 적절한 Pythonic 표현을 정의해야 함
- Human feedback의 질과 빈도에 따라 결과가 크게 달라질 수 있으며, feedback 수집 비용의 trade-off 분석 부족
- 복잡한 long-horizon task에 대한 성능 평가와 확장성이 제한적임
- LLM의 hallucination이나 부정확한 코드 생성에 대한 실패 사례 분석이 상세하지 않음
- 후속 연구로 더 자동화된 환경 추상화 방법, 더 복잡한 task 지원, 다양한 LLM 모델 비교 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 LLM 기반 reward code 자동 생성으로 RL의 오랜 challenge인 reward design을 혁신적으로 해결하며, Pythonic 추상화와 code execution feedback을 통해 높은 해석성과 신뢰성을 달성했다. 광범위한 로봇 벤치마크와 실제 로봇 배포로 실용성을 입증하고 human-in-the-loop 파이프라인으로 실무 적용 가능성을 보여주는 ICLR 2024의 우수 논문이다.

## Related Papers

- 🔄 다른 접근: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — SPRINT는 Text2Reward와 유사하게 LLM을 활용하지만 보상 생성 대신 instruction relabeling에 집중하는 다른 접근법이다.
- 🔄 다른 접근: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — Language to Rewards는 Text2Reward와 동일한 언어-보상 변환 문제를 다른 방법론으로 접근한다.
- 🧪 응용 사례: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — ExploRLLM은 Text2Reward가 생성한 언어 기반 보상을 강화학습 탐험에 실제 적용하는 구체적 사례다.
- 🧪 응용 사례: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — Guiding Pretraining with LLM은 Text2Reward의 언어 기반 보상 형성을 사전훈련 과정에 적용하는 응용 사례다.
- 🔗 후속 연구: [[papers/1548_Robotic_Skill_Acquisition_via_Instruction_Augmentation_with/review]] — 언어 기반 보상 형성 개념이 instruction augmentation의 이론적 기초를 제공한다.
- 🔗 후속 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — Plan-Seq-Learn은 Text2Reward의 언어 기반 보상 생성을 장기 계획 학습과 결합한 확장된 접근법입니다.
- 🏛 기반 연구: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — Text2Reward의 언어 기반 보상 설계를 시뮬레이션 작업 자동 생성으로 확장한 응용이다.
- 🏛 기반 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — 언어 모델을 활용한 reward shaping의 기초적 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — 둘 다 LLM을 활용한 RL 보상 설계를 다루지만 탐색 가이드 vs 직접적 보상 생성이라는 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — 언어를 보상으로 변환하는 개념을 reward shaping으로 더 체계화하고 일반화한 접근법이다.
- 🏛 기반 연구: [[papers/1548_Robotic_Skill_Acquisition_via_Instruction_Augmentation_with/review]] — Text2Reward의 언어 기반 보상 설계가 DIAL의 자연어 명령어 생성과 언어 조건부 정책 학습의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — Text2Reward는 SPRINT와 유사하게 LLM을 활용하지만 instruction relabeling 대신 자동 보상 함수 생성에 집중한다.
- 🔄 다른 접근: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — 개인화 학습을 위해 TidyBot은 LLM의 요약 능력을, Text2Reward는 reward shaping을 활용하는 서로 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — Text2Reward의 언어를 통한 reward shaping 개념이 Do As I Can에서 제시된 언어 기반 로봇 행동 grounding의 기초적 아이디어를 제공한다.
- 🔄 다른 접근: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — Text2Reward는 LLM을 활용하되 ExploRLLM과 달리 보상 shaping을 통해 RL 성능을 개선하는 다른 접근법을 사용합니다.
- 🧪 응용 사례: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Text2Reward의 언어 모델 기반 보상 설계는 Code as Policies의 자연어-코드 변환을 강화학습에 구체적으로 적용한다.
- 🏛 기반 연구: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — 언어 모델을 활용한 보상 설계의 기초 방법론을 제공한다.
- 🧪 응용 사례: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — 언어 모델을 사용한 보상 형성의 구체적인 강화학습 적용 사례입니다.
