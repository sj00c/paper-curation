---
title: "1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp"
authors:
  - "Moritz Reuss"
  - "Jyothish Pari"
  - "Pulkit Agrawal"
  - "Rudolf Lioutikov"
date: "2024.12"
doi: ""
arxiv: ""
score: 4.0
essence: "MoDE는 Mixture-of-Experts 아키텍처를 Diffusion Policy에 적용하여 noise-conditioned routing과 noise-conditioned self-attention을 통해 매개변수는 40% 감소시키면서 90% 적은 FLOPs로 더 높은 성능을 달성하는 효율적인 Imitation Learning 정책이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Reuss et al._2024_Efficient Diffusion Transformer Policies with Mixture of Expert Denoisers for Multitask Learning.pdf"
---

# Efficient Diffusion Transformer Policies with Mixture of Expert Denoisers for Multitask Learning

> **저자**: Moritz Reuss, Jyothish Pari, Pulkit Agrawal, Rudolf Lioutikov | **날짜**: 2024-12-17 | **URL**: [https://arxiv.org/abs/2412.12953](https://arxiv.org/abs/2412.12953)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The proposed MoDE architecture (left) uses a transformer with causal masking, where each*

MoDE는 Mixture-of-Experts 아키텍처를 Diffusion Policy에 적용하여 noise-conditioned routing과 noise-conditioned self-attention을 통해 매개변수는 40% 감소시키면서 90% 적은 FLOPs로 더 높은 성능을 달성하는 효율적인 Imitation Learning 정책이다.

## Motivation

- **Known**: Diffusion Policies는 Imitation Learning에서 multimodal 행동 생성 등 강력한 특성을 제공하지만, 모델 규모 증가에 따라 계산 비용이 급격히 증가한다. Mixture-of-Experts는 sparse activation을 통해 매개변수 효율성을 제공한다.
- **Gap**: 기존 Diffusion Policy 아키텍처는 높은 계산 비용으로 인해 실시간 로봇공학 애플리케이션에서 확장성이 제한되며, denoising 과정의 다단계 특성을 활용한 효율적인 설계가 부족하다.
- **Why**: 로봇 정책의 계산 효율성은 온보드 컴퓨팅 리소스가 제한된 모바일 로봇 등 실제 로봇공학 애플리케이션에서 매우 중요하며, 더 나은 성능과 효율성의 균형을 달성할 필요가 있다.
- **Approach**: MoDE는 noise 레벨에 따라 expert를 동적으로 할당하는 noise-conditioned routing과 noise-conditional self-attention 메커니즘을 결합하여, denoising 과정의 다단계 특성을 효율적으로 활용한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: After training MoDE, the router is noise-conditioned, allowing pre-computation of the*

- **성능 우수성**: CALVIN ABC에서 4.01, LIBERO-90에서 0.95를 달성하며 4개 벤치마크에서 CNN 기반 및 Transformer Diffusion Policies보다 평균 57% 성능 향상
- **계산 효율성**: Dense Transformer 아키텍처 대비 90% 적은 FLOPs와 40% 감소된 활성 매개변수를 사용하면서도 expert caching을 통해 추론 비용 90% 절감
- **광범위한 평가**: CALVIN과 LIBERO 벤치마크의 134개 태스크에서 state-of-the-art 성능 달성
- **상세한 분석**: routing 전략, noise-injection 기법, expert 분포 등 MoDE 구성 요소에 대한 포괄적인 ablation study 제공

## How

![Figure 1](figures/fig1.webp)

*Figure 1: The proposed MoDE architecture (left) uses a transformer with causal masking, where each*

- **Noise-conditioned Routing**: Router가 현재 noise 레벨을 기반으로 토큰을 expert에 할당하여 denoising 과정의 다단계 특성 활용
- **Noise-conditional Self-Attention**: Self-attention 메커니즘에 noise 정보를 직접 주입하여 다양한 noise 레벨에서의 효과적인 denoising 지원
- **Expert Caching**: 학습 후 router의 noise-conditioned 특성을 이용하여 expert 할당을 사전 계산하고 캐싱하여 추론 가속화
- **Sparse MoE Design**: 각 forward pass에서 전체 매개변수의 부분집합만 활성화하여 FLOPs 감소
- **Load Balancing**: Expert collapse와 router collapse 방지를 위해 load balancing loss 적용
- **다양한 데이터로 사전학습**: 대규모 로봇공학 데이터셋에서 MoDE를 사전학습하여 일반화 성능 향상

## Originality

- **Noise-conditioned Routing의 혁신성**: 기존 MoE 연구는 입력 특성 기반 routing을 사용했으나, diffusion 과정의 noise 레벨을 routing 신호로 활용하는 것은 새로운 접근
- **Diffusion 과정의 다단계 특성 활용**: denoising 단계별로 다른 expert를 할당하는 아이디어는 diffusion 모델의 내재적 특성을 효율적으로 활용
- **Expert Caching 메커니즘**: noise-conditioned routing의 예측 가능성을 활용한 expert 할당 캐싱으로 추론 가속화는 실용적이고 창의적
- **Diffusion Policy에 특화된 MoE**: 기존 Sparse-DP는 task 특화 expert를 사용하지만, MoDE는 denoising 프로세스에 특화된 noise-conditioned expert 설계로 차별화

## Limitation & Further Study

- **모든 데이터셋에서 일관된 개선 검증 부족**: CALVIN과 LIBERO에서만 평가되었으며, 다른 imitation learning 벤치마크나 downstream robot tasks에서의 성능 미확인
- **Expert collapse 위험**: load balancing loss를 적용했으나, expert specialization의 정도나 collapse 방지의 견고성에 대한 깊이 있는 분석 부족
- **Router 설계 복잡성**: noise-conditioned routing의 최적 설계 원리에 대한 이론적 설명이 제한적이며, router 아키텍처 선택의 정당성 미흡
- **메모리 트레이드오프**: expert caching으로 추론 비용은 감소하지만, 다양한 noise 레벨의 expert 조합을 메모리에 캐싱하는 메모리 오버헤드에 대한 분석 부족
- **후속 연구 방향**: 다중 모달 관찰(비전, 언어) 처리에서의 MoE 효과 분석, 온디바이스 로봇 배포 시 메모리 제약 하에서의 성능, offline RL에서의 적용 가능성 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MoDE는 noise-conditioned routing이라는 창의적인 아이디어로 Diffusion Policy의 계산 효율성을 획기적으로 개선하면서도 성능을 향상시킨 강력한 기여이다. 광범위한 실험과 ablation study를 통해 검증되었으나, 이론적 기초 강화와 더 다양한 도메인에서의 평가가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1424_HiMoE-VLA_Hierarchical_Mixture-of-Experts_for_Generalist_Vis/review]] — HiMoE-VLA의 hierarchical mixture-of-experts와 MoDE의 noise-conditioned MoE는 VLA 모델에서 전문가 혼합을 서로 다른 방식으로 적용한다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy의 기본 visuomotor learning 프레임워크가 MoDE에서 mixture-of-experts로 확장되는 diffusion policy의 기초를 제공한다.
- 🔗 후속 연구: [[papers/1419_H3DP_Triply-Hierarchical_Diffusion_Policy_for_Visuomotor_Lea/review]] — H³DP의 triply-hierarchical diffusion과 MoDE의 efficient expert routing은 모두 diffusion policy의 복잡성과 효율성을 개선하려는 방향이다.
- 🏛 기반 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion Transformer Policy의 기본 아키텍처를 MoE로 확장하여 효율성을 개선한 연구입니다.
- 🏛 기반 연구: [[papers/1424_HiMoE-VLA_Hierarchical_Mixture-of-Experts_for_Generalist_Vis/review]] — Mixture of Experts의 기본 개념을 로봇 데이터의 이질성 문제에 특화하여 계층적으로 확장한다.
- 🔄 다른 접근: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — 둘 다 Mixture-of-Experts 아키텍처를 사용하지만 video generation과 diffusion policy의 접근법 차이를 분석할 수 있다.
- 🔄 다른 접근: [[papers/1479_MoLe-VLA_Dynamic_Layer-skipping_Vision_Language_Action_Model/review]] — VLA 모델의 효율성 향상에서 dynamic layer-skipping vs mixture of experts라는 서로 다른 계산 최적화 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — Efficient Diffusion Transformer가 모델 아키텍처 최적화에 중점을 두는 반면, Running VLAs는 추론 파이프라인 최적화를 통한 실시간 성능 달성에 초점을 맞춘다.
- 🔄 다른 접근: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — Efficient Diffusion Transformer가 diffusion 모델의 효율화에 중점을 두는 반면, SARA-RT는 transformer의 attention mechanism 최적화에 초점을 맞춘다.
- 🔄 다른 접근: [[papers/1337_Compose_Your_Policies_Improving_Diffusion-based_or_Flow-base/review]] — 전문가 혼합을 통한 효율적인 diffusion transformer 정책의 다른 조합 방식입니다.
- 🏛 기반 연구: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — Efficient Diffusion Transformer의 혼합 전문가 모델은 DexVLA의 diffusion expert 통합에 효율적인 구조적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion transformer의 효율성을 위한 MoE와 단일 large transformer의 서로 다른 접근법입니다.
