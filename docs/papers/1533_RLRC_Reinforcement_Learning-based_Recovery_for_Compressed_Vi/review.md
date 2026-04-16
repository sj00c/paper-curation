---
title: "1533_RLRC_Reinforcement_Learning-based_Recovery_for_Compressed_Vi"
authors:
  - "Yuxuan Chen"
  - "Xiao Li"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action 모델의 실제 배포를 위해 structured pruning, SFT/RL 기반 성능 복구, 그리고 양자화를 결합한 RLRC 압축 방법을 제안하여 8배의 메모리 감소와 2.3배의 처리량 향상을 달성한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Model_Scaling_Performance"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen and Li_2025_RLRC Reinforcement Learning-based Recovery for Compressed Vision-Language-Action Models.pdf"
---

# RLRC: Reinforcement Learning-based Recovery for Compressed Vision-Language-Action Models

> **저자**: Yuxuan Chen, Xiao Li | **날짜**: 2025-06-21 | **URL**: [https://arxiv.org/abs/2506.17639](https://arxiv.org/abs/2506.17639)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1 : RLRC substantially compresses the VLA, leading to*

Vision-Language-Action 모델의 실제 배포를 위해 structured pruning, SFT/RL 기반 성능 복구, 그리고 양자화를 결합한 RLRC 압축 방법을 제안하여 8배의 메모리 감소와 2.3배의 처리량 향상을 달성한다.

## Motivation

- **Known**: VLA 모델은 로봇 조작 작업에서 뛰어난 성능을 보이지만 매우 큰 파라미터 크기와 높은 추론 지연으로 인해 자원 제약이 있는 로봇 플랫폼에 배포하기 어렵다. 기존 압축 기법들(quantization, pruning, knowledge distillation)은 LLM에서 성공을 거두었다.
- **Gap**: VLA에 대한 체계적인 압축 기법 적용 연구가 부족하며, 기존의 VLA 가속화 방법들(VLA-Cache, FlashVLA)도 메모리 소비와 추론 속도 면에서 충분한 개선을 제공하지 못한다.
- **Why**: 자원 제약이 있는 로봇 플랫폼에서 VLA의 실시간 배포는 로보틱스의 실용화에 필수적이며, 구조화된 압축 파이프라인의 개발은 일반 목적 로봇 능력의 광범위한 보급을 가능하게 한다.
- **Approach**: 먼저 VLA에 대한 quantization, pruning, knowledge distillation의 효과를 실증적으로 연구한 후, structured pruning으로 LLM 컴포넌트를 압축하고 SFT와 RL의 조합으로 성능을 복구하며 최종적으로 post-training quantization을 적용하는 3단계 파이프라인을 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1 : RLRC substantially compresses the VLA, leading to*

- **종합적인 압축 분석**: quantization, 비구조화 pruning, 구조화 pruning(LLM-Pruner, FLAP) 등 다양한 기법의 VLA 적용 효과를 체계적으로 비교 분석
- **효율적인 압축 성과**: 최대 8배의 메모리 감소와 2.3배의 처리량(throughput) 향상을 원본 VLA의 작업 성공률 유지 또는 초과하면서 달성
- **성능 복구 방법론**: SFT와 RL을 결합하여 pruning으로 인한 성능 저하를 효과적으로 복구하는 방법 제시
- **실무 적용 가능성**: LIBERO 벤치마크에서 기존 압축 기법들을 능가하며 자원 제약 환경에서의 실제 배포 가능성 입증

## How

![Figure 5](figures/fig5.webp)

*Fig. 5 : Overview of RLRC. RLRC contains three components: (1) structured pruning of VLA: structured pruning is employed*

- **단계 1 - Structured Pruning**: LLM-Pruner 또는 FLAP을 사용하여 VLA 내 LLM 컴포넌트의 채널, 헤드 등을 구조적으로 제거 (20% pruning ratio에서 실험)
- **단계 2 - Performance Recovery**: Supervised Fine-Tuning(SFT)로 기본 성능 복구 후, Reinforcement Learning을 통해 로봇 환경과의 상호작용으로부터 추가 학습
- **단계 3 - Post-training Quantization**: 4-bit 또는 8-bit 양자화를 통해 메모리 및 계산 비용을 추가로 감소
- **경험적 비교**: 기본 quantization, unstructured pruning(Magnitude, Wanda), structured pruning(LLM-Pruner, FLAP), 그리고 이들의 조합에 대한 상세 비교 실험

## Originality

- VLA에 특화된 압축 파이프라인을 체계적으로 설계한 첫 번째 연구로, 일반 LLM 압축 기법을 VLA의 특수성(로봇 제어 작업)을 고려하여 적응
- RL 기반 성능 복구라는 novel approach로 pruning으로 인한 성능 저하를 단순 SFT를 넘어 환경 상호작용을 통해 극복
- 구조화 pruning과 양자화의 결합으로 메모리와 추론 속도 양측면에서 동시에 최적화하는 종합적 접근

## Limitation & Further Study

- **RL 안정성**: RLRC에서 RL 단계의 훈련 안정성이 명시적으로 다루어지지 않았으며, 보상 신호 설계 및 샘플 효율성에 대한 상세 분석 부재
- **일반화 평가**: LIBERO 벤치마크만 사용되었으며, 실제 로봇 하드웨어(embedded device)에서의 배포 검증과 다양한 로봇 플랫폼에서의 성능 평가 필요
- **압축 비율 분석**: 특정 pruning ratio(20%)에 대한 선택 근거 부족, 다양한 sparsity 수준에서의 세밀한 트레이드오프 분석 미흡
- **후속 연구**: adaptive pruning, 하드웨어 특화 양자화 스킴, 그리고 온디바이스 RL 적응의 더 효율적인 방법 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RLRC는 VLA 압축을 위한 실용적이고 포괄적인 파이프라인을 제시하며, RL 기반 성능 복구라는 창의적 접근으로 기존 압축 방법을 능가한다. 자원 제약 로봇 환경에서의 VLA 배포 가능성을 크게 향상시킨다.

## Related Papers

- 🔄 다른 접근: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — RLRC의 압축과 SpecPrune-VLA의 pruning 가속화는 VLA 모델 효율성 향상을 위한 서로 다른 최적화 전략이다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — BitVLA의 1-bit quantization이 RLRC의 structured pruning과 quantization을 더 극단적인 압축으로 발전시킨다.
- 🧪 응용 사례: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — RLRC의 압축 기술이 Running VLAs at Real-time Speed의 실시간 실행 요구사항을 만족하는 실제적 해결책을 제공한다.
- 🔄 다른 접근: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — 두 논문 모두 VLA 모델의 효율화를 다루지만 압축과 어텐션 최적화의 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — OneDP의 추론 속도 개선과 RLRC의 모델 압축이 상호 보완적인 효율화 방법이다.
- 🏛 기반 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — RLRC의 RL-based recovery를 위한 효율적인 VLA reinforcement learning training framework를 제공한다.
- 🔗 후속 연구: [[papers/1494_NORA-15_A_Vision-Language-Action_Model_Trained_using_World_M/review]] — NORA-1.5의 성능을 실제 배포에 활용하기 위해 model compression과 RL 기반 성능 복구 방법을 적용할 수 있다.
- 🔗 후속 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — RLinf-VLA의 효율적인 RL 훈련 프레임워크가 RLRC의 압축된 VLA 모델 성능 복구와 결합되어 전체 배포 파이프라인을 완성한다.
- ⚖️ 반론/비판: [[papers/1542_RoboMonkey_Scaling_Test-Time_Sampling_and_Verification_for_V/review]] — RLRC의 모델 압축과 RoboMonkey의 샘플링 확장이 효율성과 성능의 상반된 접근법이다.
- 🔄 다른 접근: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — 두 논문 모두 로봇 transformer의 효율화를 다루지만 어텐션 최적화와 모델 압축의 다른 접근법이다.
