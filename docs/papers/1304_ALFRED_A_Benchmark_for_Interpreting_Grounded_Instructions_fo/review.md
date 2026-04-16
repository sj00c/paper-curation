---
title: "1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo"
authors:
  - "Mohit Shridhar"
  - "Jesse Thomason"
  - "Daniel Gordon"
  - "Yonatan Bisk"
  - "Winson Han"
date: "2019.12"
doi: ""
arxiv: ""
score: 4.0
essence: "ALFRED는 자연어 지시사항과 egocentric vision에서 가정용 작업을 위한 action sequence로의 매핑을 학습하기 위한 벤치마크로, 25k개의 자연어 지시문과 비가역적 상태 변화를 포함하여 실제 로봇 응용과의 간극을 줄인다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shridhar et al._2019_ALFRED A Benchmark for Interpreting Grounded Instructions for Everyday Tasks.pdf"
---

# ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks

> **저자**: Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, Dieter Fox | **날짜**: 2019-12-03 | **URL**: [https://arxiv.org/abs/1912.01734](https://arxiv.org/abs/1912.01734)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: ALFRED consists of 25k language directives*

ALFRED는 자연어 지시사항과 egocentric vision에서 가정용 작업을 위한 action sequence로의 매핑을 학습하기 위한 벤치마크로, 25k개의 자연어 지시문과 비가역적 상태 변화를 포함하여 실제 로봇 응용과의 간극을 줄인다.

## Motivation

- **Known**: Vision-and-language navigation과 embodied question answering 같은 기존 벤치마크들은 Matterport 3D, AI2-THOR, AI Habitat 등의 환경에서 발전했으나, 객체와의 상호작용과 작업 지향적 행동을 체계적으로 다루지 못한다.
- **Gap**: 기존 데이터셋들은 정적 환경 또는 단순한 이산적 상호작용만 다루고, 장기 horizon, 자연언어의 비특정성, 비가역적 action, 부분 관찰성 등 실제 작업의 복잡성을 반영하지 못한다.
- **Why**: 로봇이 인간 공간에서 작동하려면 자연언어를 실제 행동 sequence로 변환해야 하며, 객체 상호작용과 상태 변화가 포함된 현실적인 작업 학습이 필수적이다.
- **Approach**: AI2-THOR 2.0 환경에서 planner 기반 expert demonstration을 수집하고, 각 demonstration에 고수준 목표와 저수준 step-by-step instruction을 포함한 자연언어 주석을 붙인다. 객체 상호작용을 pixelwise interaction mask로 표현하여 현실적인 localization을 요구한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: ALFRED annotations. We introduce 7 different task types parameterized by 84 object classes in 120 scenes.*

- **규모와 다양성**: 120개 실내 장면에서 25,743개 영어 지시문과 8,055개 expert demonstration (총 428,322개 image-action pair) 구성
- **언어 다양성**: 각 task에 대해 고수준 목표와 저수준 단계별 지시사항을 모두 포함
- **작업 복잡성**: 7가지 작업 타입, 84개 객체 클래스, 비가역적 상태 변화, 부분 관찰성, 장기 action horizon 포함
- **상호작용 현실성**: 이산적 객체 선택이 아닌 class-agnostic pixelwise interaction mask를 통한 spatial localization 요구
- **벤치마크 설정**: Baseline seq-to-seq 모델이 5% 미만의 success rate를 보여 significant improvement 여지 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: ALFRED annotations. We introduce 7 different task types parameterized by 84 object classes in 120 scenes.*

- AI2-THOR 2.0의 interactive visual environment에서 planner 기반으로 expert demonstration 생성
- 각 demonstration에 대해 crowdsourced annotation으로 고수준 목표와 저수준 step-by-step instruction 작성
- 7가지 task type (Pick & Place, Stack & Place, Pick Two & Place, Examine in Light, Heat & Place, Cool & Place, Clean & Place) 정의
- Agent의 egocentric visual observation, action, ground-truth interaction mask를 기록하여 deterministically 재현 가능하도록 구성
- Sequence-to-sequence baseline model을 이용한 성능 평가 및 subgoal 단위 분석

## Originality

- 처음으로 interactive visual environment에서 고수준 목표와 저수준 자연언어 지시사항을 모두 제공하는 대규모 데이터셋 구축
- Pixelwise interaction mask를 통해 기존의 discrete object class selection보다 현실적인 spatial localization 요구
- 비가역적 상태 변화, 부분 관찰성, 장기 horizon 등 실제 로봇 작업의 도전 과제들을 종합적으로 반영
- TACoS와 달리 실제 작업 실행을 가능하게 하고, VirtualHome과 달리 egocentric visual feedback과 partial observability 포함

## Limitation & Further Study

- Simulation 환경에 국한되어 있어 sim-to-real transfer의 도전 과제는 다루지 않음
- 120개 장면은 실제 가정용 환경의 다양성을 완벽히 반영하지 못할 수 있음
- Baseline model의 낮은 성능(5% 미만)은 데이터셋의 어려움을 보여주지만, 동시에 더 강력한 모델 개발이 필수적임을 시사
- 후속 연구에서는 hierarchical planning, long-horizon reasoning, compositional task understanding을 다루는 모델 개발이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ALFRED는 자연언어에서 행동으로의 grounding 연구에 현실적인 도전 과제들을 종합적으로 제시하는 중요한 벤치마크이다. 고수준/저수준 언어 주석, 비가역적 상태 변화, pixelwise interaction mask 등의 혁신적 설계가 기존 데이터셋보다 실제 로봇 응용에 더 가깝다.

## Related Papers

- 🔗 후속 연구: [[papers/1325_CALVIN_A_Benchmark_for_Language-Conditioned_Policy_Learning/review]] — ALFRED의 자연어 지시 매핑과 CALVIN의 장기간 언어 조건부 조작은 모두 언어 기반 로봇 작업 학습 벤치마크의 발전이다.
- 🔄 다른 접근: [[papers/1312_ARNOLD_A_Benchmark_for_Language-Grounded_Task_Learning_With/review]] — ALFRED의 가정용 작업과 ARNOLD의 연속적 객체 상태 이해는 언어 기반 조작 학습의 서로 다른 복잡도와 현실성을 다룬다.
- 🏛 기반 연구: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — VLABench의 대규모 언어 조건부 로봇 벤치마크는 ALFRED의 언어 기반 작업 학습 개념을 확장한 기초를 제공한다.
- 🔗 후속 연구: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — LIBERO는 ALFRED의 언어 기반 instruction following을 lifelong learning 맥락으로 확장한 벤치마크입니다.
- 🧪 응용 사례: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — Instruct2Act은 ALFRED와 같은 벤치마크에서 평가될 수 있는 multi-modal instruction mapping의 구체적 구현입니다.
- 🏛 기반 연구: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — Habitat 2.0의 home assistant training 환경을 egocentric vision과 자연어 지시사항 매핑 학습을 위한 구체적인 벤치마크로 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — 둘 다 로봇 학습 벤치마크이지만 ALFRED는 자연어 지시사항과 egocentric vision에, RLBench는 일반적인 로봇 학습 환경에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1312_ARNOLD_A_Benchmark_for_Language-Grounded_Task_Learning_With/review]] — ARNOLD의 연속적 객체 상태와 ALFRED의 비가역적 상태 변화는 언어 기반 조작 학습에서 상태 모델링의 서로 다른 접근법이다.
- 🔗 후속 연구: [[papers/1325_CALVIN_A_Benchmark_for_Language-Conditioned_Policy_Learning/review]] — CALVIN의 장기간 언어 조건부 조작과 ALFRED의 자연어 지시 매핑은 언어 기반 로봇 작업 학습 벤치마크의 발전 과정이다.
