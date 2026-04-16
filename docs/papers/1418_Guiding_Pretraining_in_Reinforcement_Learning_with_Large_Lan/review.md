---
title: "1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan"
authors:
  - "Yuqing Du"
  - "Olivia Watkins"
  - "Zihan Wang"
  - "Cédric Colas"
  - "Trevor Darrell"
date: "2023.02"
doi: ""
arxiv: ""
score: 4.0
essence: "ELLM은 대규모 언어모델(LLM)을 활용하여 RL 에이전트의 탐색을 인간의 상식적 지식으로 안내하는 방법을 제안한다. 현재 상태에 기반해 LLM이 제시하는 목표 달성을 보상함으로써 의미 있는 행동 학습을 유도한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/LLM-Based_Reward_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Du et al._2023_Guiding Pretraining in Reinforcement Learning with Large Language Models.pdf"
---

# Guiding Pretraining in Reinforcement Learning with Large Language Models

> **저자**: Yuqing Du, Olivia Watkins, Zihan Wang, Cédric Colas, Trevor Darrell, Pieter Abbeel, Abhishek Gupta, Jacob Andreas | **날짜**: 2023-02-13 | **URL**: [https://arxiv.org/abs/2302.06692](https://arxiv.org/abs/2302.06692)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: ELLM uses a pretrained large language model*

ELLM은 대규모 언어모델(LLM)을 활용하여 RL 에이전트의 탐색을 인간의 상식적 지식으로 안내하는 방법을 제안한다. 현재 상태에 기반해 LLM이 제시하는 목표 달성을 보상함으로써 의미 있는 행동 학습을 유도한다.

## Motivation

- **Known**: RL은 조밀한 보상함수 부재 시 성능이 저하되며, 내재적 동기 탐색(intrinsically motivated exploration)은 신규성 기반 탐색으로 이를 완화하나, 대규모 환경에서는 작업과 무관한 신규성에 빠질 수 있다.
- **Gap**: 기존 내재적 동기 방법들은 신규성만을 최적화하므로 인간에게 의미 있는 행동과 실제 업무에 유용한 행동 간 정렬이 부족하다. 텍스트 기반 사전 지식을 활용한 체계적인 탐색 유도 방법이 필요하다.
- **Why**: RL의 사전학습(pretraining) 단계에서 의미 있는 행동을 효율적으로 학습할 수 있다면 다운스트림 작업 성능이 크게 향상될 수 있으며, 이는 실제 로봇 제어 등 고비용 환경에서 특히 중요하다.
- **Approach**: ELLM은 GPT-3을 통해 에이전트의 현재 상태를 기술한 프롬프트로부터 실행 가능한 목표들을 제시받고, SentenceBERT 임베딩을 사용하여 에이전트의 실제 행동과 제시된 목표 간의 유사도를 내재적 보상으로 활용한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Ground truth achievements unlocked per episode*

- **상식적 행동 커버리지**: ELLM으로 학습한 에이전트는 사전학습 단계에서 일반적인 상식 행동에 대해 더 높은 커버리지를 달성한다
- **다운스트림 성능**: Crafter 게임 환경과 Housekeep 로봇 시뮬레이터에서 다양한 다운스트림 작업에 대해 기존 baseline과 동등하거나 우수한 성능을 보인다
- **인간 의미성**: 탐색되는 행동들이 무작위 신규성 탐색과 달리 인간에게 의미 있고 문맥에 적절한 특징을 보인다
- **재현성**: 코드를 공개하여 결과 재현을 지원한다

## How

![Figure 2](figures/fig2.webp)

*Figure 2: ELLM uses GPT-3 to suggest adequate exploratory goals and SentenceBERT embeddings to compute the similarity*

- LLM 프롬프팅: 현재 관찰을 자연어로 변환한 텍스트 설명을 GPT-3에 입력하여 추천 목표 리스트를 생성
- 캡션 생성: 에이전트의 상태-행동-다음상태 전이(transition)를 자연어로 설명하는 캡션 생성 (예: 'Chop tree')", '유사도 기반 보상: SentenceBERT를 통해 생성된 캡션과 LLM 제시 목표들의 임베딩을 계산하고 코사인 유사도를 내재적 보상으로 사용
- 목표 조건 정책: π(a|o, g) 형태의 목표 조건 정책을 학습하여 현재 관찰과 샘플된 목표 g에 기반해 행동 선택
- 다양한 목표 샘플링: 매 에피소드마다 LLM으로부터 k개의 다양한 목표를 샘플링하여 탐색 다양성 유지

## Originality

- **LLM 기반 탐색 구조화**: 기존 내재적 동기 방법의 신규성 최적화 문제를 LLM 사전학습 지식으로 해결하는 novel한 접근
- **사전학습-다운스트림 파이프라인**: RL 사전학습 단계에서 LLM을 직접 활용하여 효율적인 행동 커버리지를 달성하는 방법론
- **임베딩 기반 보상 함수**: 텍스트 캡션과 LLM 제시 목표 간의 의미적 유사도를 보상으로 사용하는 설계
- **task-agnostic 접근**: 특정 작업 정보 없이 일반적인 상식 지식만으로 탐색을 유도하는 범용성

## Limitation & Further Study

- **LLM 의존성**: GPT-3와 SentenceBERT의 성능에 의존하므로 LLM의 오류나 편향이 직접 전파될 수 있음
- **계산 비용**: 매 상태마다 LLM 쿼리가 필요하여 계산 비용이 증가
- **평가 환경 한정**: Crafter와 Housekeep 두 환경에서만 평가되어 다양한 도메인에서의 일반화 가능성이 미확인
- **문자 기반 상태 표현**: 텍스트 캡션 생성에 의존하므로 고차원적 시각 정보 처리 환경에서는 적용이 어려울 수 있음
- **후속 연구**: 더 효율적인 LLM 쿼리 방법, 다양한 도메인 및 모달리티(시각, 로봇)에서의 확장, LLM 편향 완화 방안 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ELLM은 내재적 동기 탐색의 근본적 문제인 '무관한 신규성 추구'를 대규모 언어모델의 상식 지식으로 창의적으로 해결한 연구이다. 실험 결과가 제한적이고 계산 비용 이슈가 있지만, LLM을 RL 탐색에 통합하는 novel한 접근과 실질적 성능 향상은 이 분야에 중요한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — 둘 다 LLM을 활용한 RL 보상 설계를 다루지만 탐색 가이드 vs 직접적 보상 생성이라는 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — ExploRLLM의 LLM 기반 탐색 가이드 개념을 사전학습 단계에 적용한 확장 연구이다.
- 🔗 후속 연구: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — Language to Rewards의 개념을 RL 사전학습에서 LLM 가이드 탐색으로 발전시켰다.
- 🔄 다른 접근: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — 둘 다 LLM을 RL에 활용하지만 ELLM은 탐색 가이던스에, GLAM은 online 업데이트에 중점을 둔다.
- 🔗 후속 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — Plan-Seq-Learn은 ELLM의 LLM 기반 탐색 가이드를 장기 계획 수립으로 발전시킨 연구입니다.
- 🏛 기반 연구: [[papers/1328_Deep_Reinforcement_Learning_for_Bipedal_Locomotion_A_Brief_S/review]] — 강화학습에서 언어 모델을 활용한 사전학습 가이드의 기초를 제공한다.
- 🔄 다른 접근: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — 둘 다 LLM 기반 RL이지만 GLAM은 online learning에, ELLM은 탐색 가이던스에 집중한다.
- 🏛 기반 연구: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — 언어를 보상으로 변환하는 기본 개념이 ELLM의 LLM 기반 RL 가이던스에 적용되었다.
- 🧪 응용 사례: [[papers/1583_Text2Reward_Reward_Shaping_with_Language_Models_for_Reinforc/review]] — Guiding Pretraining with LLM은 Text2Reward의 언어 기반 보상 형성을 사전훈련 과정에 적용하는 응용 사례다.
- 🏛 기반 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — 대규모 언어모델을 활용한 강화학습 가이드 방법론이 Voyager의 GPT-4 기반 학습 메커니즘의 이론적 기반을 제공한다
- 🏛 기반 연구: [[papers/1353_Describe_Explain_Plan_and_Select_Interactive_Planning_with_L/review]] — 대규모 언어 모델의 상호작용적 환경 가이드 개념이 DEPS의 LLM 기반 대화형 계획의 기초가 됩니다.
- 🏛 기반 연구: [[papers/1389_ExploRLLM_Guiding_Exploration_in_Reinforcement_Learning_with/review]] — LLM 기반 RL 사전 훈련 가이드의 방법론이 ExploRLLM의 LLM 정책 코드 생성 및 탐색 유도 설계의 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — LLM을 활용한 강화학습 사전 훈련 가이드로서 DRL의 실세계 적용을 확장합니다.
