---
title: "1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro"
authors:
  - "Shiduo Zhang"
  - "Zhe Xu"
  - "Peiju Liu"
  - "Xiaopeng Yu"
  - "Yuan Li"
date: "2024.12"
doi: ""
arxiv: ""
score: 4.0
essence: "VLABench는 Vision-Language-Action 모델의 능력을 평가하기 위해 설계된 대규모 로봇 조작 벤치마크로, 자연어 지시, 상식 이전, 장기 추론이 필요한 100개의 과제를 제공한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robot_Policy_Learning"
  - "sub/Multi-Task_Language_Benchmarks"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2024_VLABench A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon R.pdf"
---

# VLABench: A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks

> **저자**: Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, Xipeng Qiu | **날짜**: 2024-12-24 | **URL**: [https://arxiv.org/abs/2412.18194](https://arxiv.org/abs/2412.18194)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of VLABench. VLABench is a large-scale language-conditioned manipulation benchmark to evaluate the co*

VLABench는 Vision-Language-Action 모델의 능력을 평가하기 위해 설계된 대규모 로봇 조작 벤치마크로, 자연어 지시, 상식 이전, 장기 추론이 필요한 100개의 과제를 제공한다.

## Motivation

- **Known**: RLBench, LIBERO, CALVIN 등의 기존 벤치마크들이 존재하지만, 대부분 템플릿 기반 지시와 단기 스킬 학습에 초점을 맞추고 있다. 최근 RT-2, PaLM-E 같은 VLA 모델들이 언어-조작 과제에서 좋은 성능을 보이고 있다.
- **Gap**: 기존 벤치마크들은 자연어의 암묵적 의도, 상식 및 세계 지식 이전, 다단계 추론이 필요한 장기 과제, 그리고 VLA와 VLM의 종합적 역량 평가를 충분히 다루지 못하고 있다.
- **Why**: foundation model 기반의 VLA와 VLM이 로봇 조작 분야에서 큰 잠재력을 보이고 있으나, 이를 공정하고 포괄적으로 평가할 표준화된 벤치마크가 필요하며, 이는 구체화된 AI 연구 발전에 필수적이다.
- **Approach**: 2000개 이상의 3D 객체와 163개 카테고리를 포함한 100개의 신중히 설계된 과제를 제공하며, 자동화된 데이터 수집 프레임워크를 통해 고품질 훈련 데이터를 구성한다. VLA, VLM 기반 워크플로우, 순수 VLM 등 세 가지 접근법을 비교 평가한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of VLABench. VLABench is a large-scale language-conditioned manipulation benchmark to evaluate the co*

- **포괄적 능력 평가**: mesh&texture 이해, 공간 관계, 의미론적 지시 이해, 물리법칙 이해, 지식 이전, 추론 능력 등 여러 차원에서 VLA를 평가하는 첫 번째 벤치마크
- **자연언어 기반 과제**: 템플릿이 아닌 자연스러운 인간-로봇 상호작용 형식의 지시문과 암묵적 의도를 포함한 100개의 LCM 과제
- **자동화 데이터 수집**: heuristic skill과 사전 정보를 활용한 효율적이고 확장 가능한 시뮬레이션 데이터 생성 프레임워크
- **현황 분석**: 기존의 SOTA VLA 모델들과 VLM 기반 워크플로우가 상식 이전, 장기 추론, 의미론적 이해가 필요한 과제에서 상당한 어려움을 겪고 있음을 입증

## How

![Figure 3](figures/fig3.webp)

*Figure 3. Task examples in each dimension. The first row showcases examples of primitive tasks from Section 3.1, while t*

- 100개의 LCM 과제를 6가지 평가 차원(상식&세계지식, mesh&texture, 의미론적 이해, 공간 관계, 물리법칙, 추론)으로 체계적으로 설계
- 2000개 이상의 다양한 3D 객체와 163개의 객체 카테고리를 이용한 강한 domain randomization 적용
- 자동화된 데이터 수집 프레임워크로 각 과제에 대한 표준화된 훈련 데이터셋 구성
- RT-2, PaLM-E 등의 VLA 모델, VoxPoser/CoPA 등의 VLM 기반 워크플로우, 다양한 VLM들에 대한 체계적인 성능 평가
- cross-embodiment 지원, point cloud 데이터 지원, 다중 카메라 관점 제공으로 평가의 다양성 확보

## Originality

- 자연언어 기반 암묵적 의도 표현: 기존 템플릿 기반 지시문과 달리, 실제 인간의 상호작용 방식을 모방한 자연스러운 언어 지시 도입
- 장기 추론(long-horizon reasoning) 강조: multi-step 의사결정과 task decomposition이 필요한 복합 과제를 벤치마크의 핵심 요소로 체계화
- 상식 및 지식 이전 평가: '물체를 특정 인물에게 이동'과 같은 상식 추론이 필수적인 과제를 체계적으로 설계", 'VLA와 VLM 모두를 대상으로 한 통합 평가 프레임워크: 단일 정책 모델과 모듈화된 워크플로우 접근의 장단점을 동시에 평가

## Limitation & Further Study

- 시뮬레이션 환경의 한계: 실제 로봇의 물리적 특성, 불확실성, 실시간 제약 조건들이 완벽히 반영되지 않을 수 있음
- 객체 및 장면 다양성: 2000개 이상의 객체로 광범위하지만, 실제 현실 환경의 무한한 다양성을 완전히 포괄하기는 어려움
- VLA 모델 성숙도: 현재 사용 가능한 VLA 모델들이 상식 이전과 장기 추론에 제대로 최적화되지 않았을 가능성으로, 벤치마크의 어려움이 모델 설계의 한계인지 과제 설계의 타당성인지 구분이 필요
- 후속 연구 방향: VLA 모델의 대규모 사전학습 데이터 확보, 자연언어 의도 이해 능력 강화, 상식 기반 추론 메커니즘 개발, 시뮬-투-리얼 전이 학습 기법 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLABench는 foundation model 기반의 로봇 조작 연구를 평가하기 위한 첫 번째 포괄적 벤치마크로서, 자연언어 지시, 상식 이전, 장기 추론 등 기존 벤치마크가 간과했던 중요한 차원들을 체계적으로 도입했다. 현 SOTA 모델들의 한계를 명확히 드러냄으로써 향후 VLA 및 embodied AI 연구 방향 설정에 중요한 역할을 할 것으로 예상된다.

## Related Papers

- 🔄 다른 접근: [[papers/1325_CALVIN_A_Benchmark_for_Language-Conditioned_Policy_Learning/review]] — CALVIN과 같이 언어 조건부 정책 학습을 위한 벤치마크이지만, VLABench는 더 대규모이고 다양한 태스크를 제공한다
- 🔄 다른 접근: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — LIBERO와 함께 로봇 학습의 지식 전이를 평가하는 벤치마크로, 두 벤치마크를 비교 분석하면 평가 방법론의 차이점을 이해할 수 있다
- 🔗 후속 연구: [[papers/1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level/review]] — ManipBench의 vision-language 모델 평가 접근법을 VLA 모델로 확장하여 더 포괄적인 능력 평가가 가능하다
- 🏛 기반 연구: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — BEHAVIOR-1K의 인간 중심적 벤치마크 설계 철학이 VLABench의 자연어 지시와 상식 추론 평가 설계에 기반이 된다
- 🔄 다른 접근: [[papers/1387_EWMBench_Evaluating_Scene_Motion_and_Semantic_Quality_in_Emb/review]] — 둘 다 embodied AI 벤치마크이지만 EWMBench는 scene/motion quality에, VLABench는 language-conditioned tasks에 집중합니다.
- 🏛 기반 연구: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — embodied AI의 spatial understanding 벤치마킹 방법론을 제공하여 VLABench의 로봇 조작 평가에 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1314_AutoEval_Autonomous_Evaluation_of_Generalist_Robot_Manipulat/review]] — AutoEval이 VLABench의 언어 조건부 로봇 조작 평가를 자율적 평가 시스템으로 확장한다.
- 🏛 기반 연구: [[papers/1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R/review]] — robosuite 시뮬레이션 프레임워크가 VLABench의 대규모 로봇 조작 벤치마크 구축의 기술적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1591_Towards_Diverse_Behaviors_A_Benchmark_for_Imitation_Learning/review]] — Towards Diverse Behaviors 벤치마크가 VLABench와 다른 모방 학습 관점에서 로봇 행동의 다양성을 평가한다.
- 🔄 다른 접근: [[papers/1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level/review]] — VLABench와 함께 VLM의 로봇 조작 능력 평가에 집중하지만 ManipBench는 저수준 추론에 특화된 벤치마크를 제공한다.
- 🧪 응용 사례: [[papers/1446_Large_VLM-based_Vision-Language-Action_Models_for_Robotic_Ma/review]] — Large VLM-based VLA 모델들의 이론적 분류가 VLABench의 언어 조건부 로봇 제어 벤치마크 설계에 실용적 기준을 제공한다.
- 🔗 후속 연구: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — VLABench는 LIBERO의 생애 주기 학습 평가를 VLA 모델로 확장하여 더 포괄적인 벤치마킹을 제공합니다.
- 🏛 기반 연구: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — OpenBench의 벤치마킹 방법론이 VLABench의 대규모 언어 조건부 로봇 벤치마크 설계의 기초적인 평가 프레임워크를 제시합니다.
- 🧪 응용 사례: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 성능을 VLABench의 포괄적인 language-conditioned robotics benchmark에서 평가하고 비교할 수 있다.
- 🏛 기반 연구: [[papers/1535_RoboArena_Distributed_Real-World_Evaluation_of_Generalist_Ro/review]] — VLABench의 language-conditioned robotics 벤치마크 설계가 RoboArena의 실제 환경 평가 프레임워크의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — language-conditioned robotic manipulation benchmark를 대규모 장기 지평선 작업으로 확장하여 더 복잡하고 실용적인 로봇 능력 평가를 다룬다.
- 🧪 응용 사례: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — VLABench가 제공하는 large-scale 벤치마크가 TidyBot의 개인화 정리 작업 성능을 체계적으로 평가하는 데 활용될 수 있다.
- 🔄 다른 접근: [[papers/1591_Towards_Diverse_Behaviors_A_Benchmark_for_Imitation_Learning/review]] — VLABench는 D3IL의 다양성 평가와 유사한 목적으로 언어 조건부 로봇 작업을 위한 대규모 벤치마크를 제공한다.
- 🏛 기반 연구: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — VLABench의 대규모 언어 조건부 로봇 벤치마크는 ALFRED의 언어 기반 작업 학습 개념을 확장한 기초를 제공한다.
- 🧪 응용 사례: [[papers/1345_CoWs_on_Pasture_Baselines_and_Benchmarks_for_Language-Driven/review]] — CoW의 언어 기반 zero-shot 네비게이션 방법론이 VLABench의 대규모 언어 조건부 로봇 벤치마크에서 평가될 수 있습니다.
- 🏛 기반 연구: [[papers/1314_AutoEval_Autonomous_Evaluation_of_Generalist_Robot_Manipulat/review]] — 언어 조건부 로봇 정책 평가를 위한 대규모 벤치마크 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1386_Evaluating_Real-World_Robot_Manipulation_Policies_in_Simulat/review]] — VLABench는 SIMPLER의 시뮬레이션 평가 방법론을 언어 조건부 로봇 학습으로 확장한 연구임
- 🏛 기반 연구: [[papers/1373_DualVLA_Building_a_Generalizable_Embodied_Agent_via_Partial/review]] — VLABench의 language-conditioned robotics 벤치마크가 DualVLA의 추론-행동 분리 효과를 평가하기 위한 기준점을 제공한다.
