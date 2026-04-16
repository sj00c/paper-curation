---
title: "1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A"
authors:
  - "Huy Ha"
  - "Pete Florence"
  - "Shuran Song"
date: "2023.07"
doi: ""
arxiv: ""
score: 4.0
essence: "LLM 기반 고수준 계획과 sampling-based robot planner를 활용하여 언어-레이블 로봇 데이터 생성을 확장하고, 이를 diffusion policy를 통해 다중 작업 언어-조건 visuo-motor 정책으로 증류하는 로봇 스킬 획득 프레임워크를 제시한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Semantic_Task_Generalization"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ha et al._2023_Scaling Up and Distilling Down Language-Guided Robot Skill Acquisition.pdf"
---

# Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition

> **저자**: Huy Ha, Pete Florence, Shuran Song | **날짜**: 2023-07-26 | **URL**: [https://arxiv.org/abs/2307.14535](https://arxiv.org/abs/2307.14535)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Language-guided Skill Acquisition enables scalable robot learning. In the data generation stage, a LLM takes*

LLM 기반 고수준 계획과 sampling-based robot planner를 활용하여 언어-레이블 로봇 데이터 생성을 확장하고, 이를 diffusion policy를 통해 다중 작업 언어-조건 visuo-motor 정책으로 증류하는 로봇 스킬 획득 프레임워크를 제시한다.

## Motivation

- **Known**: 로봇 학습에서 대규모 데이터 생성은 인간 주석에 의존하거나 강화학습의 비효율성에 제약을 받으며, 다중 작업 언어-조건 정책 학습은 전문가 시연이나 수동 보상 설계가 필요하다.
- **Gap**: LLM의 상식 추론 능력과 sampling-based planner의 유연성을 결합하여 전문가 시연 없이 대규모 로봇-완전 데이터를 자동으로 생성하고, 이를 robust closed-loop control policy로 효과적으로 증류하는 통합 프레임워크가 부재하다.
- **Why**: 로봇 조작 기술의 확장 가능한 습득은 실제 배포 환경에서 robust하고 재사용 가능한 스킬을 요구하며, 이는 LLM의 일반화 능력과 robot planner의 정밀성을 결합함으로써 달성할 수 있다.
- **Approach**: LLM을 데이터 수집 정책으로 사용하여 작업을 재귀적으로 분해하고 6DoF 탐색 프리미티브로 grounding한 후, LLM이 추론한 성공 조건으로 자동 라벨링하고, 성공 궤적만을 필터링하여 multi-task diffusion policy로 증류한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Benchmark. We validate our approach on a new multi-task benchmark addressing challenging long-horizon*

- **대규모 자동 데이터 생성**: LLM 기반 계획과 sampling-based planner의 조합으로 전문가 시연 없이 diverse하고 rich한 조작 궤적을 자동으로 생성
- **다중 작업 언어-조건 diffusion policy**: single-task diffusion policy를 multi-task 언어-조건 설정으로 확장하여 robust한 closed-loop 제어 정책 학습
- **실계 전이 및 성능 향상**: 도메인 랜더마이제이션을 통해 실계에 직접 전이되며, 평균적으로 5개 도메인 전반에서 33.2% 절대 성공률 향상 달성
- **종합 벤치마크 구축**: 장기 horizon(~800 제어 사이클), 상식 추론, 도구 사용, 직관적 물리를 요구하는 5개 도메인 18개 작업으로 구성된 새로운 다중 작업 벤치마크 제공

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Language-Driven Robot Data Generation takes as input the task description and simulation state, and outputs*

- **작업 분해**: LLM이 자연어 작업 설명을 계층적 작업 트리로 재귀적으로 분해하여 단순화
- **Grounding**: 분해된 작업을 motion planner, grasp sampler 등 6DoF 탐색 프리미티브의 시퀀스로 grounding
- **성공 함수 추론**: LLM이 각 작업의 성공 조건을 코드 스니펫으로 자동 추론하여 궤적 검증 및 실패 시 재시도 가능
- **성공 필터링**: 성공 궤적만 추출하여 replay buffer 구성
- **Diffusion Policy 확장**: diffusion policy의 noise prediction network를 language embedding과 시각 정보로 조건화하여 multi-task 학습
- **행동 클로닝**: 필터링된 성공 궤적에 대해 behavior cloning으로 visuo-linguo-motor policy 학습

## Originality

- **LLM-기반 자동 데이터 수집**: LLM을 data collection policy로 활용하면서 동시에 success verification 및 자동 라벨링 수행하는 novel 접근법
- **다중 작업 언어-조건 diffusion policy**: 기존 single-task diffusion policy를 다중 작업 언어-조건 설정으로 확장하는 새로운 formulation
- **성공 필터링 기반 증류**: 최적이 아닌 suboptimal policy의 성공 궤적만 필터링하여 downstream policy 성능을 향상시키는 strategy
- **재시도 행동 학습**: 데이터 수집 과정에서 실패 복구 경험을 명시적으로 포함하여 정책이 robust retrying behavior를 학습하도록 유도

## Limitation & Further Study

- **시뮬레이션 의존성**: 데이터 수집이 시뮬레이션에서 수행되므로 sim-to-real transfer의 완전성이 domain randomization의 effectiveness에 의존
- **LLM 성능 제약**: 작업 분해 및 성공 함수 추론이 LLM의 능력에 의존하므로 복잡한 작업의 경우 실패 가능성 존재
- **벤치마크 제한**: 제시된 벤치마크가 특정 5개 도메인과 18개 작업으로 제한되어 더 넓은 범위의 조작 기술에 대한 일반화 검증 필요
- **실시간 성능**: 장기 horizon 작업에 대한 diffusion policy의 추론 시간 비용이 실계 적용 시 challenge가 될 수 있음
- **후속 연구**: (1) 더 복잡한 다중 객체 상호작용 및 동역학 기반 작업으로의 확장, (2) LLM 성공 함수 추론의 신뢰성 향상, (3) 온라인 학습을 통한 real-world 적응 능력 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 LLM 기반 계획과 sampling-based planning을 결합한 자동 로봇 데이터 생성과 multi-task diffusion policy 학습의 novel한 통합 프레임워크를 제시하며, 33.2% 성능 향상과 함께 로봇 스킬 습득의 확장 가능성을 입증한다. 다중 작업 벤치마크와 함께 로봇 학습 분야에 의미 있는 기여를 하고 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — Language to Rewards는 언어 기반 로봇 스킬 합성에서 LLM을 활용하지만 보상 신호 생성에 집중하는 다른 접근법이다.
- 🔄 다른 접근: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — GenSim은 LLM을 활용한 로봇 시뮬레이션 작업 생성으로 스킬 확장과 유사한 목표를 다른 방식으로 달성한다.
- 🔄 다른 접근: [[papers/1548_Robotic_Skill_Acquisition_via_Instruction_Augmentation_with/review]] — Instruction Augmentation은 언어 기반 로봇 스킬 학습에서 데이터 확장을 위한 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — Plan-Seq-Learn은 언어 모델을 활용한 장기 계획 학습으로 스킬 획득과 유사한 목표를 다른 방법론으로 접근한다.
- 🔄 다른 접근: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — SPRINT가 offline RL과 instruction relabeling에 중점을 두는 반면, Scaling Up and Distilling Down은 LLM 기반 계획과 diffusion policy 증류를 결합한다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 언어 모델 프로그램 기반 embodied control 개념이 LLM 기반 고수준 계획의 이론적 기초가 된다.
- 🔗 후속 연구: [[papers/1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A/review]] — Language-Guided Robot Skill Acquisition의 언어 기반 스킬 학습을 sampling-based planner와 diffusion policy를 통해 확장 가능한 프레임워크로 발전시켰다.
- 🔗 후속 연구: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — 로봇공학 스케일링 법칙이 Scaling Up and Distilling Down의 언어 기반 로봇 스킬 학습에서 효율적 스케일링 전략 수립에 활용된다.
- 🔗 후속 연구: [[papers/1534_RoboAgent_Generalization_and_Efficiency_in_Robot_Manipulatio/review]] — RoboAgent의 semantic augmentation을 language-guided skill acquisition과 결합하여 더 효율적인 robot learning을 실현할 수 있다.
- 🏛 기반 연구: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — language-guided robot skill learning의 기초 이론을 제공하여 RT-H의 언어 기반 행동 계층 구조와 skill 간 데이터 공유에 필요한 방법론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — Scaling Up and Distilling Down이 LLM 기반 계획과 diffusion policy에 중점을 두는 반면, SPRINT는 instruction relabeling과 offline RL 기반 접근법을 제시한다.
