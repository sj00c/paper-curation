---
title: "1337_Compose_Your_Policies_Improving_Diffusion-based_or_Flow-base"
authors:
  - "Jiahang Cao"
  - "Yize Huang"
  - "Hanzhong Guo"
  - "Rui Zhang"
  - "Mu Nan"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 General Policy Composition (GPC)를 제안하여 사전학습된 diffusion 또는 flow 기반 로봇 정책들의 분포 수준 점수를 convex 조합으로 결합함으로써, 추가 학습 없이 개별 정책보다 우수한 성능을 달성한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Robotic_Policy_Scaling"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cao et al._2025_Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribu.pdf"
---

# Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribution-level Composition

> **저자**: Jiahang Cao, Yize Huang, Hanzhong Guo, Rui Zhang, Mu Nan, Weijian Mai, Jiaxu Wang, Hao Cheng, Jingkai Sun, Gang Han, Wen Zhao, Qiang Zhang, Yijie Guo, Qihao Zheng, Chunfeng Song, Xiao Li, Ping Luo, Andrew F. Luo | **날짜**: 2025-10-01 | **URL**: [https://arxiv.org/abs/2510.01068](https://arxiv.org/abs/2510.01068)

---

## Essence


본 논문은 General Policy Composition (GPC)를 제안하여 사전학습된 diffusion 또는 flow 기반 로봇 정책들의 분포 수준 점수를 convex 조합으로 결합함으로써, 추가 학습 없이 개별 정책보다 우수한 성능을 달성한다.

## Motivation

- **Known**: Diffusion-based 모델은 robotic control에서 복잡한 다중모드 행동 분포를 표현할 수 있으나, 대규모 상호작용 데이터셋 획득의 높은 비용으로 성능 향상이 제한된다.
- **Gap**: 기존 정책 합성 연구는 고정된 가중치를 사용하거나 제한된 검증만 수행했으며, 과제별 최적 가중치가 다르다는 점과 이질적인 정책(VA, VLA, 다양한 시각 모드)을 통합하는 방법에 대한 심층적 분석이 부족하다.
- **Why**: 새로운 데이터 수집이나 모델 재학습 없이 기존 정책들을 활용하여 성능을 향상시킬 수 있다면 실용적인 가치가 크며, 이는 로봇 학습의 데이터 효율성 문제를 해결하는 대안이 될 수 있다.
- **Approach**: Distributional score들의 convex 조합이 단일 단계에서 우수한 목적함수를 생성함을 이론적으로 증명하고, Grönwall-type bound를 통해 이 개선이 전체 생성 궤적으로 전파됨을 보인 후, 이를 바탕으로 test-time 가중치 탐색을 통한 GPC 방법을 제안한다.

## Achievement


- **이론적 기초 확립**: Convex 조합된 distributional score가 개별 score보다 우수한 목적함수를 제공함을 증명하고, 이러한 단일 단계 개선이 전체 생성 과정으로 전파되어 시스템 수준의 성능 향상을 가져옴을 보임
- **GPC 방법론**: Diffusion 및 flow 기반 정책, VA 및 VLA 모달리티, 다양한 시각 입력을 포함한 이질적 정책들을 훈련 없이 test-time에 조합할 수 있는 유연한 프레임워크 제안
- **광범위한 검증**: Robomimic, PushT, RoboTwin 벤치마크 및 실제 로봇 실험에서 +8~15% 성능 향상 달성, 다양한 조합 연산자와 가중치 전략의 효과 분석

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of our proposed General Policy Composition. Combining distributional*

- 분자 가중치(w₁, w₂, ..., wₙ)에 대한 convex 조합을 통해 여러 정책의 score 함수 조합: s_composed = Σ wᵢ · s_θᵢ
- Test-time에 validation 데이터 또는 작은 샘플 집합에서 다양한 가중치 조합을 탐색하여 최적 w* 선택
- Langevin dynamics 기반 denoising 과정에서 조합된 score를 사용하여 action 생성
- Diffusion Policy, DP3, MDT, RDT, Flow Policy 등 다양한 정책 아키텍처 및 시각 모드(Florence, 포인트 클라우드 등)에 호환 가능하도록 설계

## Originality

- Score function의 convex 조합이 우수한 목적함수를 생성함을 theoretically 증명하고 Grönwall-type bound로 전파성을 보인 점
- 과제별 최적 가중치가 다르다는 발견으로 test-time weight searching의 필요성을 처음 제시
- VA와 VLA, diffusion과 flow 기반, 다양한 시각 모달리티를 포함한 폭넓은 이질적 정책 조합의 일반화
- 개별 정책 각각보다 우수한 성능 달성 (ensemble이 아닌 score 수준 조합으로)

## Limitation & Further Study

- Test-time weight searching에 소량의 검증 데이터 또는 샘플이 필요하므로 완전한 훈련-프리가 아님
- 최적 가중치 탐색 시 과제별로 다양하게 나타나는 현상의 근본 원인에 대한 깊이 있는 이론적 분석 부족
- 두 개 이상의 정책 조합 시 계산 복잡도 증가로 인한 scalability 한계 미논의
- **후속 연구**: (1) 과제 특성으로부터 최적 가중치를 직접 예측하는 메타러닝 접근법, (2) 더 많은 수의 정책 조합 시 효율적 가중치 탐색 전략, (3) 정책 간 다양성과 조합 성능 간의 관계에 대한 이론적 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 기존 정책 활용을 통한 성능 향상이라는 실용적 문제를 이론적 기초와 함께 해결하며, GPC는 간단하면서도 효과적인 방법으로 로봇 학습의 데이터 효율성 문제에 대한 새로운 관점을 제시한다. 광범위한 실험 검증과 우수한 성능 향상은 로봇 제어 분야에 상당한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — diffusion 기반 정책 학습의 기초적 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — 실시간 액션 청킹 flow 정책으로 정책 composition을 확장한다.
- 🔄 다른 접근: [[papers/1580_Streaming_Flow_Policy_Simplifying_diffusionflow-matching_pol/review]] — 스트리밍 flow 정책이라는 다른 diffusion/flow 기반 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — 전문가 혼합을 통한 효율적인 diffusion transformer 정책의 다른 조합 방식입니다.
- 🏛 기반 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion Transformer Policy의 기본 구조를 여러 정책의 조합으로 확장한 접근방식을 제시합니다.
- 🔄 다른 접근: [[papers/1465_ManiFlow_A_General_Robot_Manipulation_Policy_via_Consistency/review]] — Flow-based 정책을 단일 모델로 학습하는 것과 달리 사전학습된 정책들의 조합으로 접근합니다.
