---
title: "1479_MoLe-VLA_Dynamic_Layer-skipping_Vision_Language_Action_Model"
authors:
  - "Rongyu Zhang"
  - "Menghang Dong"
  - "Yuan Zhang"
  - "Liang Heng"
  - "Xiaowei Chi"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "MoLe-VLA는 Mixture-of-Layers 아키텍처와 Spatial-Temporal Aware Router(STAR)를 통해 LLM의 불필요한 레이어를 동적으로 스킵하여 로봇 조작 작업의 계산 효율을 5.6배 향상시키면서 8% 성능 개선을 달성한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_MoLe-VLA Dynamic Layer-skipping Vision Language Action Model via Mixture-of-Layers for Efficient Ro.pdf"
---

# MoLe-VLA: Dynamic Layer-skipping Vision Language Action Model via Mixture-of-Layers for Efficient Robot Manipulation

> **저자**: Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, Shanghang Zhang | **날짜**: 2025-03-26 | **URL**: [https://arxiv.org/abs/2503.20384](https://arxiv.org/abs/2503.20384)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of our proposed MoLe-VLA: Our proposed framework integrates dynamic layer activation, a novel Spatial*

MoLe-VLA는 Mixture-of-Layers 아키텍처와 Spatial-Temporal Aware Router(STAR)를 통해 LLM의 불필요한 레이어를 동적으로 스킵하여 로봇 조작 작업의 계산 효율을 5.6배 향상시키면서 8% 성능 개선을 달성한다.

## Motivation

- **Known**: Vision Language Action(VLA) 모델은 복잡한 언어-시각 정보 처리가 가능하나 높은 계산 비용으로 실시간 로봇 제어에 부적합하다. 기존 sparsification 기법(early exit, token pruning)은 의미 정보가 풍부한 최종 레이어의 역할을 간과한다.
- **Gap**: 기존 early-exit 전략은 깊은 레이어를 제거하면서 작업에 중요한 의미 정보를 손실하고, Mixture-of-Depth(MoD)는 토큰별 불일치 문제를 야기한다. 로봇 작업의 공간-시간 특성을 고려한 동적 레이어 선택 메커니즘이 부재한다.
- **Why**: 로봇 제어는 50-1000 Hz의 고속 응답이 필요한데 현재 VLA 모델은 5-12 Hz 성능만 제공하므로, 계산 효율을 획기적으로 개선하면서 성능을 유지하는 것이 실제 로봇 배포의 핵심이다.
- **Approach**: Shallow Brain Hypothesis에서 영감을 받아 각 LLM 레이어를 독립적 전문가로 취급하는 Mixture-of-Layers 프레임워크를 제안하고, 공간-시간 정보를 활용하는 STAR 라우터로 동적 레이어 활성화를 수행한다. 추가로 Cognition Self-Knowledge Distillation(CogKD)으로 레이어 스킵으로 인한 인지 능력 손실을 보상한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4. Efficiency analysis compared with state-of-the-art baselines with FLOPs and inference time. (Left) Success rat*

- **계산 비용 감소**: LLM 부분에서 최대 5.6배 계산 비용 감소 달성
- **성능 향상**: 10개 작업에서 평균 8% 성공률 개선
- **효율성과 성능의 균형**: RLBench 시뮬레이션과 실제 로봇 환경 모두에서 우월성 입증
- **생물학적 영감의 구체화**: Shallow Brain Hypothesis 원리를 VLA 모델에 성공적으로 적용

## How

![Figure 2](figures/fig2.webp)

*Figure 2. The overall framework of MoLe-VLA. Our proposed Mixture of Layers (MoLe) architecture consists of a Spatial-Te*

- **Spatial-Temporal Aware Router(STAR)**: 시각 특성에서 공간 정보, 텍스트 입력에서 시간 의존성을 독립적으로 처리한 후 통합하여 각 레이어의 softmax 확률 생성 및 top-k 레이어 선택
- **동적 레이어 스킵**: 라우터의 확률 기반으로 현재 로봇 상태에 따라 필요한 레이어만 활성화하여 불필요한 계산 제거
- **Cognition Self-Knowledge Distillation(CogKD)**: 전체 레이어 모델(교사)과 스킵 모델(학생) 사이의 학습가능한 cognition token을 도입하고, Tokens of Interest(ToIs)를 식별하여 적응적 가중치 조정
- **혼합 전문가 개념의 수직 확장**: 기존 MoE의 수평 적용(layer 내 expert)을 수직 방향으로 확장하여 layer-wise 활성화 달성

## Originality

- **신경과학-기반 설계**: Shallow Brain Hypothesis를 직접 로봇 제어 모델에 적용한 최초 사례
- **공간-시간 인식 라우팅**: 시각과 언어 입력의 서로 다른 특성을 고려한 차별화된 라우터 설계로 기존 단순 선형 라우터 대비 우월함
- **인지 토큰 기반 지식 증류**: 작업 관련 인지 특징을 명시적으로 식별하고 재가중치하는 새로운 자체 증류 패러다임
- **레이어 단위 희소화**: MoD의 토큰별 불일치 문제를 해결하기 위해 전체 입력에 대해 일관된 레이어 조합을 선택하는 방식

## Limitation & Further Study

- **라우터 오버헤드**: STAR 라우터의 계산 비용 자체가 전체 효율 이득에 미치는 영향에 대한 명확한 분석 부재
- **제한된 벤치마크**: RLBench 10개 작업에서만 평가하여 더 복잡하고 다양한 실제 조작 작업에서의 성능 검증 필요
- **하이퍼파라미터 민감성**: top-k 선택, CogKD의 가중치 비율 등 다양한 하이퍼파라미터 조정의 민감도 분석 부족
- **일반화 가능성**: 다양한 VLA 아키텍처(RT-2, OpenVLA 외 다른 모델)에 대한 광범위한 적용 검증 부재
- **후속 연구**: (1) 네트워크 내 레이어 중요도 분석을 통한 더 정교한 라우팅 정책 개발, (2) 적응적 top-k 결정 메커니즘, (3) 다중 모달리티 작업에서의 확장성 연구 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MoLe-VLA는 신경과학 이론과 효율적인 AI 기술을 혁신적으로 결합하여 로봇 제어의 계산-성능 트레이드오프 문제를 크게 개선한 우수한 연구이다. 공간-시간 인식 라우팅과 인지 기반 지식 증류의 설계가 독창적이며, 시뮬레이션과 실제 환경에서의 실증 결과가 설득력 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — VLA 모델의 효율성 향상에서 dynamic layer-skipping vs mixture of experts라는 서로 다른 계산 최적화 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — VLA 모델 가속화 기법을 pruning과 layer-skipping을 결합하여 더 포괄적인 효율성 최적화 솔루션을 제공한다.
- 🧪 응용 사례: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — real-time VLA 실행의 실제 요구사항을 MoLe-VLA의 동적 레이어 스킵핑 기법으로 해결하여 실시간 로봇 제어에 적용한다.
- 🔗 후속 연구: [[papers/1424_HiMoE-VLA_Hierarchical_Mixture-of-Experts_for_Generalist_Vis/review]] — 계층적 구조를 VLA 모델의 dynamic layer-skipping으로 확장한 연구입니다.
- 🔄 다른 접근: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — 둘 다 VLA 모델의 계산 효율성 향상에 중점을 두지만, HybridVLA는 생성 패러다임 통합을, MoLe-VLA는 동적 레이어 스킵에 집중한다.
- 🔄 다른 접근: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — MoLe-VLA는 동적 layer-skipping을 통해 VLA 모델의 추론 속도를 향상시키는 다른 최적화 전략을 제공한다.
- 🔄 다른 접근: [[papers/1351_DeeR-VLA_Dynamic_Inference_of_Multimodal_Large_Language_Mode/review]] — DeeR-VLA의 동적 추론과 MoLe-VLA의 동적 레이어 스킵핑은 VLA 모델 효율성 향상의 서로 다른 구조적 접근법이다.
