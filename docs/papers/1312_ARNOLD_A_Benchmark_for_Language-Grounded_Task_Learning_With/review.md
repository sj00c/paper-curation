---
title: "1312_ARNOLD_A_Benchmark_for_Language-Grounded_Task_Learning_With"
authors:
  - "Ran Gong"
  - "Jiangyong Huang"
  - "Yizhou Zhao"
  - "Haoran Geng"
  - "Xiaofeng Gao"
date: "2023.04"
doi: ""
arxiv: ""
score: 4.0
essence: "ARNOLD은 현실적인 3D 장면에서 연속적 객체 상태를 이해하고 언어 기반 조작 작업을 학습하는 로봇을 평가하기 위한 벤치마크이다. 8개의 언어 조건부 작업과 세밀한 물리 시뮬레이션, 다양한 장면과 객체로 구성되어 있다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gong et al._2023_ARNOLD A Benchmark for Language-Grounded Task Learning With Continuous States in Realistic 3D Scene.pdf"
---

# ARNOLD: A Benchmark for Language-Grounded Task Learning With Continuous States in Realistic 3D Scenes

> **저자**: Ran Gong, Jiangyong Huang, Yizhou Zhao, Haoran Geng, Xiaofeng Gao, Qingyang Wu, Wensi Ai, Ziheng Zhou, Demetri Terzopoulos, Song-Chun Zhu, Baoxiong Jia, Siyuan Huang | **날짜**: 2023-04-09 | **URL**: [https://arxiv.org/abs/2304.04321](https://arxiv.org/abs/2304.04321)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. The ARNOLD benchmark for language-grounded task learning with continuous states in realistic 3D scenes. ARNOLD*

ARNOLD은 현실적인 3D 장면에서 연속적 객체 상태를 이해하고 언어 기반 조작 작업을 학습하는 로봇을 평가하기 위한 벤치마크이다. 8개의 언어 조건부 작업과 세밀한 물리 시뮬레이션, 다양한 장면과 객체로 구성되어 있다.

## Motivation

- **Known**: 기존 로봇 조작 벤치마크는 대부분 이진 상태와 같은 이산화된 객체 상태를 가정하며, 언어 조건부 정책 학습에 관한 연구가 진행되었다. 그러나 이러한 접근법은 복잡한 작업 학습과 실제 환경으로의 정책 이전을 어렵게 만든다.
- **Gap**: 기존 벤치마크는 (1) 복잡한 현실적 장면이 아닌 단순한 환경을 가정하고, (2) 연속적 객체 상태 대신 이산화된 상태를 사용하며, (3) 언어를 정확한 객체 상태에 그라운딩하지 않는다. 또한 신규 목표 상태, 신규 장면, 신규 객체에 대한 일반화 능력 평가가 체계적이지 않다.
- **Why**: 로봇이 인간의 자연스러운 지시를 이해하고 실행하기 위해서는 연속적 객체 상태 공간에서 언어를 정확한 물리적 상태로 매핑할 수 있어야 한다. 이는 실제 환경에서의 효과적인 조작과 작업 학습에 필수적이다.
- **Approach**: ARNOLD은 PhysX 5.0 기반의 고정확 물리 시뮬레이션을 활용하여 8개의 연속적 로봇 조작 작업을 설계하고, 40개의 객체와 20개의 장면으로 다양한 시나리오를 구성했다. 전문가 시연과 템플릿 기반 언어 설명을 제공하며, 신규 상태, 신규 객체, 신규 장면에 대한 체계적인 일반화 평가를 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. The ARNOLD benchmark for language-grounded task learning with continuous states in realistic 3D scenes. ARNOLD*

1. **포괄적 벤치마크**: 현실적인 3D 상호작용 환경에서 연속적 객체 상태, 마찰 기반 그래핑, 다양한 장면 배경을 지원하는 첫 벤치마크 제시
2. **체계적 평가 프레임워크**: 신규 목표 상태(Novel State), 신규 객체(Novel Object), 신규 장면(Novel Scene)에 대한 일반화 능력을 구분하여 평가
3. **기존 방법의 한계 규명**: 최신 언어 조건부 조작 모델(language-conditioned policy learning models)이 여전히 신규 상태와 장면 일반화에서 현저한 어려움을 겪음을 입증
4. **실증적 분석**: 상태 모델링의 중요성을 포함한 광범위한 실험 분석과 제거 연구(ablation studies)를 통해 향후 연구 방향 제시

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Multi-view robot observation in ARNOLD. The top row*

- PhysX 5.0을 활용한 고정확 물리 엔진으로 연속적 동작, 마찰 기반 그래핑, 유체 시뮬레이션 구현
- 8개 작업(예: 서랍 반쯤 열기, 병 180° 회전, 캐비닛 75% 열기, 컵에 물 붓기)에 대한 연속적 목표 상태 정의
- 템플릿 기반 플래너를 통해 풍부한 전문가 시연 궤적과 자동 생성 언어 설명 제공
- 40개 객체, 20개 장면으로 구성된 데이터셋 구축 및 일반화 평가를 위한 데이터 분할 설계
- 최신 language-conditioned policy learning 모델(여러 언어 인코더 및 상태 표현 포함)에 대한 종합적 성능 평가

## Originality

- **연속적 상태 그라운딩**: 기존 벤치마크와 달리 이산화된 상태가 아닌 연속적 객체 상태 범위에서 언어를 정확한 물리적 상태로 매핑하는 문제를 처음 체계적으로 제시
- **다층 일반화 평가**: 신규 목표 상태, 신규 객체, 신규 장면을 구분하는 세분화된 일반화 평가 프레임워크 도입
- **현실적 물리 시뮬레이션**: 기존 RLBench 기반 벤치마크의 단순화된 그래핑과 달리 PhysX 5.0 기반의 사실적 마찰과 동역학 시뮬레이션 제공
- **포괄적 비교**: Table 1에서 기존 주요 벤치마크(ALFRED, ManiSkill, Calvin, BEHAVIOR, RLBench, SoftGym 등)와의 체계적 비교로 ARNOLD의 고유한 특징(연속 상태, 유체 시뮬레이션, 현실적 렌더링, 체계적 일반화 평가) 명확화

## Limitation & Further Study

- **시뮬레이션 기반 한계**: PhysX 기반 물리 시뮬레이션으로도 실제 환경과의 sim-to-real 갭이 존재하며, 본 논문에서도 제한된 실제 환경 실험만 제시
- **작업 수와 다양성**: 8개의 조작 작업으로 제한되어 있으며, 다양한 도메인(예: 매니퓰레이션 외 네비게이션, 그래스핑)으로의 확장 필요
- **현재 모델의 저조한 성능**: 최신 모델들도 20-80% 범위의 성공률을 보이므로, 벤치마크 자체의 난이도가 상당하지만 개선 방향에 대한 이론적 통찰 부족
- **후속 연구 방향**: (1) 언어와 연속 상태의 더 정교한 그라운딩 메커니즘 개발, (2) 신규 객체 및 장면에 대한 강화된 일반화 능력을 갖춘 새로운 알고리즘 필요, (3) sim-to-real 정확도 개선을 위한 추가 연구 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ARNOLD은 언어 기반 로봇 작업 학습에서 연속적 객체 상태 이해와 일반화 능력 평가라는 중요한 공백을 채우는 포괄적이고 잘 설계된 벤치마크이다. 현실적 물리 시뮬레이션과 체계적인 평가 프레임워크를 통해 기존 방법의 한계를 명확히 드러내고, 향후 연구에 실질적인 기여를 할 수 있는 가치 있는 자원이다.

## Related Papers

- 🔗 후속 연구: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — ARNOLD의 연속적 객체 상태 이해와 BEHAVIOR-1K의 1,000개 일상 활동은 복잡한 물리 시뮬레이션 기반 언어 조건부 작업의 진화이다.
- 🔄 다른 접근: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — ARNOLD의 연속적 객체 상태와 ALFRED의 비가역적 상태 변화는 언어 기반 조작 학습에서 상태 모델링의 서로 다른 접근법이다.
- 🧪 응용 사례: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — LIBERO의 지식 전이 벤치마크는 ARNOLD의 언어 기반 조작 작업 평가를 실제 로봇 학습 시나리오로 확장한다.
- 🔄 다른 접근: [[papers/1325_CALVIN_A_Benchmark_for_Language-Conditioned_Policy_Learning/review]] — 언어 조건부 정책 학습을 위한 다른 벤치마크 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1605_VIMA_General_Robot_Manipulation_with_Multimodal_Prompts/review]] — 멀티모달 프롬프트를 활용한 범용 로봇 조작의 기초 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — BEHAVIOR-1K의 1,000개 일상 활동과 ARNOLD의 언어 기반 조작 작업은 현실적 물리 시뮬레이션 기반 벤치마크의 확장이다.
- 🔄 다른 접근: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — ALFRED의 가정용 작업과 ARNOLD의 연속적 객체 상태 이해는 언어 기반 조작 학습의 서로 다른 복잡도와 현실성을 다룬다.
