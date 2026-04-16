---
title: "1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source"
authors:
  - "Can Cui"
  - "Pengxiang Ding"
  - "Wenxuan Song"
  - "Shuanghao Bai"
  - "Xinyang Tong"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Dual-System VLA 아키텍처의 구조를 비교 분석하고 핵심 설계 요소를 경험적으로 평가하여 로봇 조작을 위한 오픈소스 dual-system VLA 모델을 제공한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cui et al._2025_OpenHelix A Short Survey, Empirical Analysis, and Open-Source Dual-System VLA Model for Robotic Man.pdf"
---

# OpenHelix: A Short Survey, Empirical Analysis, and Open-Source Dual-System VLA Model for Robotic Manipulation

> **저자**: Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, Han Zhao, Siteng Huang, Donglin Wang | **날짜**: 2025-05-06 | **URL**: [https://arxiv.org/abs/2505.03912](https://arxiv.org/abs/2505.03912)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Key Design of Dual-System VLAs. It mainly includes: MMLM Selection, Policy Selection, Latent Feature Represent*

Dual-System VLA 아키텍처의 구조를 비교 분석하고 핵심 설계 요소를 경험적으로 평가하여 로봇 조작을 위한 오픈소스 dual-system VLA 모델을 제공한다.

## Motivation

- **Known**: RT-2 이후 Vision-Language-Action 모델이 로봇 정책 학습에 유망한 접근법으로 주목받고 있으며, 최근 LCB와 DP-VLA 등 dual-system 아키텍처가 제안되고 있다.
- **Gap**: 기존 VLA는 모델 크기가 크고 추론 속도가 느리며 domain shift와 catastrophic forgetting 문제가 있고, dual-system 아키텍처의 설계 요소에 대한 충분한 오픈소스 구현과 체계적 평가가 부족하다.
- **Why**: 로봇의 실시간 제어를 위해서는 효율적이고 빠른 추론이 필수적이면서도 멀티모달 추론 능력은 유지해야 하므로 dual-system 구조의 최적화가 중요하다.
- **Approach**: Dual-process 이론에 기반하여 System 1(빠른 경량 모델)과 System 2(느린 대규모 모델)를 결합하는 아키텍처를 설계하고, 기존 dual-system VLA들의 구조적 차이를 분석하며 핵심 설계 요소에 대해 체계적으로 평가한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Key Design of Dual-System VLAs. It mainly includes: MMLM Selection, Policy Selection, Latent Feature Represent*

- **Dual-System VLA 아키텍처 분류**: MLLM 선택, Policy 선택, Latent 특성 표현, 학습 전략, 통합 전략 등 7가지 핵심 설계 요소를 체계화하고 LCB, DP-VLA, HiRT, Robodual 등 기존 방법들을 비교 분석하는 종합 설문 제공
- **경험적 평가 프레임워크**: 세 가지 평가 환경에서 MLLM 학습 전략, 계층적 추론, 기존 dual-system의 단점 등을 실증적으로 평가하는 방법론 제시
- **오픈소스 OpenHelix 모델**: 저비용 구현이 가능한 실용적인 dual-system VLA 모델 공개 및 향후 성능 개선 계획 제시

## How

![Figure 1](figures/fig1.webp)

*Figure 1. Key Design of Dual-System VLAs. It mainly includes: MMLM Selection, Policy Selection, Latent Feature Represent*

- Dual-process 이론을 로봇 제어에 적용하여 System 1과 System 2를 구분하고 서로 다른 주기로 업데이트되는 비동기 구조 설계
- MLLM(OpenVLA, LLaVA, InstructBLIP, Qwen2-VL 등)에서 추출한 latent representation이 경량 policy 모델(Transformer, DiT 등)을 가이드하는 정보 흐름 구성
- RGB, proprioception, depth, tactile 등 다양한 센서 모달리티 조합에 대한 ablation study 수행
- LoRA fine-tuning, frozen encoder, scratch training 등 다양한 학습 전략 비교 평가
- 고빈도(System 1) 및 저빈도(System 2) 인지 입력의 통합 전략 분석

## Originality

- Dual-process 이론을 로봇 VLA 아키텍처의 이론적 근거로 제시하여 기존 engineering 관점의 접근을 인지과학적으로 정당화
- MLLM이 반드시 robotic pretrain을 거쳐야 하는지, 어떤 크기의 MLLM이 충분한지 등 설계 가정에 대한 실증적 검증
- 7가지 핵심 설계 요소를 체계적으로 분해하고 비교할 수 있는 분류 체계 개발
- 기존 dual-system 설계의 부족한 점(e.g., temporal delay, asynchronous update)을 명확히 지적하고 개선 방향 제시

## Limitation & Further Study

- 논문의 발췌본이므로 실제 실험 결과와 정량적 비교 데이터가 제시되지 않음
- OpenHelix 모델의 구체적인 아키텍처와 성능 지표가 본 발췌에서 명확하지 않음
- 평가 환경이 제한적일 가능성(Fig 2 언급하지만 상세 설명 부재)
- 후속 연구에서는 실제 로봇 하드웨어에서의 성능 평가, 더 다양한 manipulation task에서의 generalization 검증 필요
- MLLM과 policy 모델 간 최적의 latent dimension, temporal synchronization 방식 등에 대한 더 깊은 분석 요구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Dual-System VLA에 대한 최초의 포괄적 설문과 체계적 경험적 분석을 제공하며, 오픈소스 구현으로 커뮤니티 기여도 가능하나, 발표된 발췌에서는 구체적 실험 결과 부재로 평가 강도를 완전히 판단하기 어렵다.

## Related Papers

- 🏛 기반 연구: [[papers/1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to/review]] — VLA 모델의 모듈 분석 연구가 OpenHelix의 dual-system VLA 아키텍처 설계 요소 분석에 이론적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma/review]] — Fast-in-Slow dual-system과 동일한 이중 시스템 접근이지만 OpenHelix는 VLA에 특화된 분석과 구현을 제공한다.
- 🔄 다른 접근: [[papers/1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and/review]] — OpenHelix의 dual-system VLA와 RoBridge의 hierarchical architecture는 인지와 실행 분리라는 같은 문제를 다른 구조로 해결한다.
- 🔗 후속 연구: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — HybridVLA의 collaborative diffusion과 autoregression이 OpenHelix가 분석한 dual-system 설계를 실제 구현으로 확장한다.
- 🏛 기반 연구: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — OpenHelix가 분석한 dual-system VLA의 기초가 되는 triple-system 아키텍처 연구
- 🔗 후속 연구: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — dual-system foundation model 개념을 오픈소스 VLA로 확장한 구현 연구
- 🔄 다른 접근: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — Dual-system VLA 아키텍처에서 OpenHelix는 구조 분석에, RationalVLA는 합리적 판단 능력에 초점을 맞춘 서로 다른 접근이다.
- 🔄 다른 접근: [[papers/1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti/review]] — OneTwoVLA의 adaptive reasoning 접근법과 OpenHelix의 dual-system 아키텍처는 reasoning과 acting을 분리하는 다른 전략을 제시한다.
- 🔄 다른 접근: [[papers/1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and/review]] — RoBridge의 hierarchical architecture와 OpenHelix의 dual-system이 인지와 실행 분리라는 동일한 문제를 서로 다른 구조적 접근으로 해결한다.
