---
title: "1322_BOSS_Benchmark_for_Observation_Space_Shift_in_Long-Horizon_T"
authors:
  - "Yue Yang"
  - "Linfeng Zhao"
  - "Mingyu Ding"
  - "Gedas Bertasius"
  - "Daniel Szafir"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇의 시각 기반 장기 작업 수행 시, 선행 스킬의 실행으로 인한 관찰 공간 변화(Observation Space Shift, OSS)가 후속 스킬의 성능을 심각하게 저하시키는 문제를 식별하고, 이를 평가하기 위한 BOSS 벤치마크를 제안한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Robotic_Policy_Scaling"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yang et al._2025_BOSS Benchmark for Observation Space Shift in Long-Horizon Task.pdf"
---

# BOSS: Benchmark for Observation Space Shift in Long-Horizon Task

> **저자**: Yue Yang, Linfeng Zhao, Mingyu Ding, Gedas Bertasius, Daniel Szafir | **날짜**: 2025-02-21 | **URL**: [https://arxiv.org/abs/2502.15679](https://arxiv.org/abs/2502.15679)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. The example illustrates how Observation Space Shift (OSS) occurs*

로봇의 시각 기반 장기 작업 수행 시, 선행 스킬의 실행으로 인한 관찰 공간 변화(Observation Space Shift, OSS)가 후속 스킬의 성능을 심각하게 저하시키는 문제를 식별하고, 이를 평가하기 위한 BOSS 벤치마크를 제안한다.

## Motivation

- **Known**: Hierarchical Imitation Learning(HIL)은 task planner가 pre-trained 스킬들을 조합하여 장기 작업을 수행하는 방식으로 널리 알려져 있다. Skill chaining 문제의 해결을 위해 transition policy 학습이나 상태 분포 정렬 등의 방법들이 제시되었으나, 이들은 시각 입력 기반 정책에는 부적절한 가정을 포함한다.
- **Gap**: 시각 기반 visuomotor 정책에서 발생하는 OSS 문제를 체계적으로 정의하고 평가할 수 있는 벤치마크가 부재하다. 기존 방법들은 비시각적 관찰 공간을 기반으로 설계되어 실제 시각적 장기 작업에는 적용이 제한된다.
- **Why**: 로봇이 복잡한 일상적 작업을 자동으로 수행하기 위해서는 다양한 스킬을 순차적으로 조합할 수 있어야 하는데, OSS는 이러한 스킬 체이닝의 실패를 야기하는 근본적인 문제이다. 이 문제를 명확히 이해하고 해결하는 것이 시각 기반 로봇 제어의 실용화에 필수적이다.
- **Approach**: LIBERO 시뮬레이터 기반으로 세 가지 난이도의 도전 과제(Single Predicate Shift, Accumulated Predicate Shift, Skill Chaining)를 포함하는 BOSS 벤치마크를 개발하고, Behavioral Cloning과 OpenVLA 등 최신 IL 알고리즘들을 평가한다. Rule-based Automatic Modification Generator(RAMG)를 통해 대규모 시각적으로 다양한 데이터셋을 생성하여 데이터 증강 효과를 검증한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2. This figure illustrates the three challenges of BOSS, each examining a distinct aspect of OSS, using concrete ex*

- **OSS 문제의 형식화**: 시각 기반 skill chaining에서 발생하는 관찰 공간 변화를 처음으로 명확하게 정의하고 분류
- **BOSS 벤치마크 개발**: 3단계 난이도(C1, C2, C3)로 구성된 체계적인 평가 프레임워크로, Behavioral Cloning(3가지) 및 OpenVLA에서 최소 34~67%의 성능 저하 실증
- **데이터셋 생성 및 한계 규명**: RAMG를 통해 생성한 대규모 다양한 데이터셋으로도 OSS 문제를 해결할 수 없음을 증명하여 알고리즘적 솔루션의 필요성 강조
- **커뮤니티 자원 제공**: 증강된 대규모 데이터셋 공개로 향후 연구의 기초 제공

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. This figure illustrates the three challenges of BOSS, each examining a distinct aspect of OSS, using concrete ex*

- LIBERO 시뮬레이터에서 단순한 관찰 공간 변경(potato in bowl 등)부터 누적된 여러 수정사항까지 체계적으로 생성
- BOSS-C1: 단일 선행 스킬의 관찰 수정에 따른 정책 견고성 평가
- BOSS-C2: 여러 선행 스킬의 누적 효과 평가 (e.g., 열린 서랍 + 그릇 안의 감자)
- BOSS-C3: 3개 스킬 체인 (OpenDrawer → PlaceObject → MoveContainer)의 end-to-end 평가
- Rule-based Automatic Modification Generator(RAMG)로 기존 LIBERO 데이터셋을 자동으로 확장하여 시각적 다양성 증대
- Behavioral Cloning (3가지 변형)과 Visual Language Action 모델(OpenVLA) 등 4가지 IL 알고리즘 벤치마킹

## Originality

- **문제 정의의 참신성**: 시각 기반 skill chaining에서 OSS를 독립적인 문제로 처음 식별하고 형식화
- **벤치마크 설계**: 기존 벤치마크(Meta-World, RLBench, Calvin 등)와 달리 스킬 전환 문제에 특화된 구조화된 평가 프레임워크
- **자동 데이터 생성**: RAMG를 통한 규칙 기반 자동 수정으로 대규모 시각적으로 다양한 테스트 사례 효율적 생성
- **부정적 결과의 가치**: 데이터 증강이 OSS 문제의 근본 해결책이 아님을 엄밀히 증명함으로써 알고리즘 수준의 해결책 필요성 제시

## Limitation & Further Study

- **시뮬레이션 기반 평가**: 실제 로봇 환경에서의 OSS 영향이 시뮬레이션과 다를 수 있으며, sim-to-real 전이 성능 미검증
- **제한된 도메인**: LIBERO 기반이므로 가정된 객체 타입과 환경이 특정 도메인에 편향될 가능성
- **데이터 증강의 한계만 증명**: OSS 해결을 위한 구체적인 알고리즘 솔루션을 제시하지 않고 문제만 규명
- **평가 대상의 한계**: Behavioral Cloning과 OpenVLA만 평가되어 다른 최신 IL 방법(e.g., diffusion-based models)과의 비교 부재
- **후속 연구 방향**: 시각적 attention 메커니즘, 도메인 적응, state correction 모듈 등 해결책 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 시각 기반 로봇 학습에서 간과되어온 OSS 문제를 명확히 정의하고 체계적인 벤치마크를 제공함으로써 장기 작업 수행의 근본적 과제를 드러낸다. 데이터 증강의 한계를 증명하고 알고리즘적 솔루션의 필요성을 강조하여 향후 연구의 명확한 방향을 제시하는 가치 있는 기여이다.

## Related Papers

- 🔗 후속 연구: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — 메모리와 추론 능력을 강화한 VLA로 장기 작업의 OSS 문제를 해결한다.
- 🏛 기반 연구: [[papers/1459_LLM-State_Open_World_State_Representation_for_Long-horizon_T/review]] — 장기 작업을 위한 오픈 월드 상태 표현의 기초 이론을 제공한다.
- 🔄 다른 접근: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — 멀티스케일 메모리를 활용한 다른 장기 작업 해결 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1591_Towards_Diverse_Behaviors_A_Benchmark_for_Imitation_Learning/review]] — 모방학습에서 다양한 행동을 위한 벤치마크의 기초적인 평가 기준을 제공합니다.
- 🔗 후속 연구: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — 평생 로봇 학습에서 지식 전이 벤치마크로서 관찰 공간 변화 문제를 확장합니다.
