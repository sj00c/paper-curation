---
title: "1617_VLA-Cache_Efficient_Vision-Language-Action_Manipulation_via"
authors:
  - "Siyu Xu"
  - "Yunke Wang"
  - "Chenghao Xia"
  - "Dihao Zhu"
  - "Tao Huang"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "VLA-Cache는 로봇 조작 작업에서 인접한 프레임 간의 시간적 중복성을 활용하여 정적 시각 토큰의 KV 표현을 캐싱하고 재사용함으로써 Vision-Language-Action 모델의 추론을 가속화하는 학습 불필요 방법이다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Trajectory-Conditioned_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xu et al._2025_VLA-Cache Efficient Vision-Language-Action Manipulation via Adaptive Token Caching.pdf"
---

# VLA-Cache: Efficient Vision-Language-Action Manipulation via Adaptive Token Caching

> **저자**: Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, Chang Xu | **날짜**: 2025-02-04 | **URL**: [https://arxiv.org/abs/2502.02175](https://arxiv.org/abs/2502.02175)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: During the inference of the VLA model, static*

VLA-Cache는 로봇 조작 작업에서 인접한 프레임 간의 시간적 중복성을 활용하여 정적 시각 토큰의 KV 표현을 캐싱하고 재사용함으로써 Vision-Language-Action 모델의 추론을 가속화하는 학습 불필요 방법이다.

## Motivation

- **Known**: Vision-Language-Action (VLA) 모델은 강력한 멀티모달 추론 능력을 갖춘 end-to-end 로봇 제어 기술이다. 그러나 실시간 로봇 제어에 필요한 높은 계산 비용이 도전 과제로 남아 있다.
- **Gap**: 기존 VLA 가속 기법들은 양자화나 구조 수정 등 범용적 접근을 취하거나 재훈련이 필요하며, VLA의 본질적 특성인 연속적 시각 입력의 시간적 중복성을 직접적으로 활용하지 못한다.
- **Why**: 로봇 조작에서 배경과 정적 물체는 프레임 간 거의 변하지 않으므로 이를 재활용하면 대폭적 계산 절감이 가능하다. 실시간 로봇 제어의 필수 요구사항인 빠른 의사결정을 위해 추론 지연 감소가 중요하다.
- **Approach**: VLA-Cache는 adjacent frames 간 최소 변화를 보이는 토큰을 식별하여 캐싱된 KV 표현을 재사용하되, decoder attention scores 기반 필터링으로 작업 관련 토큰을 선별적으로 재계산한다. 추가로 layer-adaptive token reusing strategy로 decoder layer별 attention entropy에 따라 재사용 비율을 동적 조정한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Visualization of VLA-Cache token reuse across settings. (a) LIBERO simulation with*

- **추론 가속화**: CUDA latency에서 최대 1.7배 속도 향상을 달성하고 제어 주파수를 15% 증가시켰다.
- **무시할 수 있는 성능 손실**: 작업 성공률에 미미한 손실만 발생시키면서 속도 개선을 달성했다.
- **학습 불필요 및 플러그앤플레이**: 모델 재훈련이나 구조 수정 없이 기존 VLA 모델에 직접 적용 가능하다.
- **광범위한 검증**: LIBERO, SIMPLER 두 시뮬레이션 환경 및 Kinova Jaco2 실제 로봇에서 실증했다.
- **다중 모델 호환성**: OpenVLA, CogAct, OpenVLA-OFT 등 여러 최신 VLA 모델에 일관되게 적용된다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: VLA-Cache accelerates the VLA’s language decoding process across timesteps via the*

- **정적 토큰 식별**: adjacent frames 간 visual token의 변화도를 측정하여 최소 변화를 보이는 토큰을 정적으로 분류한다.
- **작업 관련성 필터링**: 시각적으로는 정적이지만 그리퍼나 목표 물체 근처 등 의미적으로 중요한 토큰을 decoder attention scores로 식별하여 재사용 제외 목록에 추가한다.
- **Temporal KV Caching**: 정적이고 작업 관련성이 없는 토큰의 KV 표현을 캐시에서 재사용하여 redundant computation을 우회한다.
- **Layer-adaptive 재사용 전략**: 각 decoder layer의 attention entropy를 계산하여 layer 깊이에 따라 토큰 재사용 비율을 동적으로 조정한다.
- **Cross-frame 연속성 활용**: 폐루프 로봇 조작의 특성상 연속적 프레임 간 강한 시간적 연속성을 직접적으로 활용한다.

## Originality

- VLA 모델의 본질적 특성인 temporal redundancy를 명시적으로 활용한 첫 시도이다.
- Attention score 기반 task-relevance filtering은 단순 정적 토큰 필터링을 넘어 의미적 중요도를 고려하는 정교한 접근이다.
- Layer-adaptive caching strategy는 decoder layer별 상이한 attention pattern을 활용한 창의적 최적화 기법이다.
- 학습 불필요의 완전한 training-free 특성으로 기존 모델에 대한 접근성이 높다.

## Limitation & Further Study

- 정적 토큰 식별 기준이 프레임 간 pixel 변화도 기반으로, 움직임이 큰 환경에서 성능 저하 가능성이 있다.
- Attention score 기반 필터링이 특정 VLA 아키텍처나 decoder 구조에 최적화되어 있을 수 있으며, 다양한 아키텍처에 대한 일반화 검토가 제한적이다.
- 배경 정적 영역이 적은 작업(예: 밀집된 물체 조작) 환경에서 가속 이득이 제한될 수 있다.
- 실시간 성능 평가가 주로 CUDA latency 기반이며, 메모리 사용량이나 에너지 효율성에 대한 분석이 부족하다.
- **후속 연구**: (1) 광학 흐름(optical flow) 기반 더 정교한 정적 토큰 식별, (2) 동적 환경이나 빠른 변화에 대한 강건성 개선, (3) 다양한 robot embodiment에 대한 적응성 연구.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLA-Cache는 로봇 조작의 시간적 특성을 창의적으로 활용하여 학습 불필요한 상태에서 실질적 추론 가속을 달성한 실용적이고 우수한 연구이다. 작업 관련성 필터링과 layer-adaptive 전략의 정교함과 광범위한 실증이 높은 가치를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — VLA 추론 가속화를 위한 서로 다른 최적화 방법 - KV caching vs token pruning입니다.
- 🏛 기반 연구: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — 실시간 action execution이 VLA 모델의 효율적인 추론 최적화 기반입니다.
- 🔗 후속 연구: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — one-step diffusion을 KV 캐싱과 결합하여 더 빠른 visuomotor policy를 구현할 수 있습니다.
- 🔗 후속 연구: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — VITA의 효율적인 flow matching 정책을 KV 캐싱을 통해 더욱 가속화하여 추론 효율성을 극대화합니다.
- 🔄 다른 접근: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — 둘 다 VLA 모델의 실시간 실행을 목표로 하지만 VLA-Cache는 캐싱에, Running VLAs는 전반적인 최적화에 집중합니다.
- 🏛 기반 연구: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — self-adaptive robust attention transformer의 scaling 방법론을 제공하여 VLA-Cache의 효율적인 attention 처리에 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — TinyVLA의 추론 효율성 향상을 KV 캐싱을 통한 추가적인 최적화로 확장하여 더 실용적인 시스템을 구축한다.
- 🔗 후속 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — VLA-Cache의 efficient manipulation via caching이 FAST의 efficient action tokenization과 함께 VLA 모델의 전반적 효율성 향상을 위한 상호 보완적 접근이다.
- 🔄 다른 접근: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — VLA 모델 추론 가속화를 위한 서로 다른 최적화 전략 - token pruning vs KV caching입니다.
- 🏛 기반 연구: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — VLA 모델의 추론 효율성 향상이라는 공통 목표를 가지며, 캐싱과 경량화라는 상호 보완적 접근을 보여준다.
- 🔗 후속 연구: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — VITA의 효율적인 vision-to-action flow를 KV caching을 통해 더욱 가속화하여 실시간 성능을 향상시킵니다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — VLA-Cache의 효율적 추론 개념을 1-bit 양자화로 더 극단적으로 발전시킨 메모리 최적화 연구입니다.
