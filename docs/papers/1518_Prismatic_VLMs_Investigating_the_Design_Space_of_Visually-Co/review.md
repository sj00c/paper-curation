---
title: "1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co"
authors:
  - "Siddharth Karamcheti"
  - "Suraj Nair"
  - "Ashwin Balakrishna"
  - "Percy Liang"
  - "Thomas Kollar"
date: "2024.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Visually-Conditioned Language Models (VLMs)의 설계 공간을 체계적으로 탐색하여 핵심 설계 결정이 모델 성능에 미치는 영향을 분석하고, 표준화된 평가 스위트와 최적화된 학습 코드, 그리고 InstructBLIP과 LLaVa v1.5를 능가하는 Prismatic VLMs를 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Karamcheti et al._2024_Prismatic VLMs Investigating the Design Space of Visually-Conditioned Language Models.pdf"
---

# Prismatic VLMs: Investigating the Design Space of Visually-Conditioned Language Models

> **저자**: Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, Dorsa Sadigh | **날짜**: 2024-02-12 | **URL**: [https://arxiv.org/abs/2402.07865](https://arxiv.org/abs/2402.07865)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Prismatic VLMs.* Through rigorous experiments ex-*

Visually-Conditioned Language Models (VLMs)의 설계 공간을 체계적으로 탐색하여 핵심 설계 결정이 모델 성능에 미치는 영향을 분석하고, 표준화된 평가 스위트와 최적화된 학습 코드, 그리고 InstructBLIP과 LLaVa v1.5를 능가하는 Prismatic VLMs를 제시한다.

## Motivation

- **Known**: LLaVa, InstructBLIP, PaLI-3 등 많은 VLM이 CLIP 같은 사전학습된 시각 백본의 패치 특징을 언어 모델의 입력 공간으로 투영하는 'patch-as-token' 접근법을 채택하고 있다. 그러나 이미지 전처리, 아키텍처, 최적화 등의 핵심 설계 결정에 대한 체계적인 탐색이 부족하다.
- **Gap**: 기존 VLM 연구는 제한된 설계 공간만 탐색하며, 개별 선택이 하위 작업 성능에 미치는 영향을 일관성 있게 평가하지 않는다. 또한 객관적이고 표준화된 평가 벤치마크의 부재로 인해 모델 성능을 이해하기 어렵다.
- **Why**: VLM의 채택이 증가하면서 설계 결정의 영향을 이해하는 것이 모델 개발을 가속화할 수 있다. 표준화된 평가와 체계적인 분석을 통해 더 효율적이고 성능이 높은 모델을 개발할 수 있다.
- **Approach**: 12개 벤치마크로 구성된 표준화된 평가 스위트(VQA, 객체 지역화, 환각 감지 등)를 구축하고, 최적화 절차, 시각 표현, 언어 모델, 학습 스케일 등 4개의 핵심 설계 축을 따라 VLM을 체계적으로 탐색한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Prismatic VLMs.* Through rigorous experiments ex-*

- **표준화된 평가 스위트**: Visual Question Answering 4개, 객체 지역화 4개, 도전 과제 4개로 구성된 12개 벤치마크를 통해 VLM의 세밀한 능력을 평가할 수 있는 체계를 제공
- **최적화된 학습 코드베이스**: PyTorch와 FSDP를 기반으로 한 모듈식 코드베이스로 20% 더 빠른 학습 속도를 달성하며, 시각 및 언어 백본을 쉽게 교체 가능
- **성능 우수성**: Prismatic VLMs (7B/13B)이 InstructBLIP과 LLaVa v1.5를 12개 다양한 작업에서 능가하면서 30% 이상의 학습 계산 비용 절감
- **설계 인사이트**: 다단계 학습 절차 제거 가능(20-25% 계산 비용 감소), CLIP과 DINOv2 같은 다중 시각 백본 융합의 효과 검증

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Exploring VLM Design Axes. We explore four key design axes for developing VLMs: 1) optimization procedure, 2) *

- 시각 표현(ViT, CLIP, DINOv2), 시각-언어 프로젝터, 언어 모델로 구성된 표준 VLM 아키텍처 채택
- LLaVa v1.5 데이터 혼합(558K 캡셔닝 + 665K 명령어 튜닝 샘플)을 사용하여 통제된 실험 수행
- 다음 토큰 예측 손실함수로 최적화하며, FSDP를 활용한 분산 학습으로 효율성 극대화
- 4개 설계 축에 따라 ablation study 수행: 최적화 절차(다단계 vs 단일 단계), 시각 백본(CLIP, DINOv2, 융합), 언어 모델(기본 vs 명령어 튜닝), 데이터 및 시간 스케일
- LLaVa v1.5 재현으로 코드베이스 검증 후 설계축 탐색 진행

## Originality

- VLM 설계 공간의 최초 체계적 탐색으로, 개별 설계 선택이 성능에 미치는 영향을 정량적으로 분석
- 12개 벤치마크 기반의 표준화된 평가 프레임워크로 일관된 VLM 평가 체계 제안
- 다중 백본 융합(CLIP + DINOv2)을 통한 시각 표현 개선 방법 제시
- 효율적이고 모듈식인 공개 학습 코드베이스 제공으로 후속 연구의 접근성 향상

## Limitation & Further Study

- 평가 데이터셋이 주로 영어 중심이므로 다국어 VLM 성능 평가 부재
- 개방형 가중치 데이터만 사용하므로 독점 데이터를 활용한 모델과 비교 제한
- 계산 자원에 따른 대규모 모델(30B+) 탐색 미흡
- 후속 연구에서 로봇 제어, 실시간 애플리케이션 등 구체적 응용 분야에 대한 성능 검증 필요
- 시각-언어 정렬 방식(projector 아키텍처, 토큰 수 등)의 더 깊은 탐색 여지

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 VLM의 설계 공간을 체계적으로 탐색하는 첫 포괄적 연구로, 표준화된 평가 프레임워크와 최적화된 학습 코드, 그리고 우수한 성능의 모델을 제시함으로써 VLM 개발의 기초를 다진다. 공개된 리소스와 명확한 인사이트는 후속 연구를 크게 가속화할 수 있는 중요한 기여이다.

## Related Papers

- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — Prismatic VLMs의 체계적인 설계 공간 분석이 RT-2의 vision-language-action 통합 방법론의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — PaLI-X의 multilingual vision-language 확장이 Prismatic VLMs의 설계 원리를 다국어 환경으로 발전시킨다.
- 🔄 다른 접근: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — DINOv2의 self-supervised visual learning과 Prismatic VLMs의 supervised VLM 설계는 시각적 표현 학습의 다른 패러다임을 보여준다.
- 🏛 기반 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — VLM의 로봇 적용을 위한 설계 최적화의 기초가 되는 foundation model 연구
- 🧪 응용 사례: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — VLM 설계 최적화를 실제 VLA 구현에 적용한 zero-modification 접근법
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — VLA 모델 서베이에서 제시된 설계 원칙들을 Prismatic VLMs가 체계적으로 검증한다.
- 🏛 기반 연구: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — PaLI-X의 multilingual vision-language scaling이 기반으로 하는 VLM 설계 공간 연구
- 🏛 기반 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — Prismatic VLM의 시각-언어 모델 설계 공간 연구가 VLA 모델의 백본 선택과 아키텍처 설계 분석의 기반이 되었다.
- 🏛 기반 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — Prismatic VLMs 연구는 RoboFlamingo가 기반으로 하는 vision-language 모델의 설계 공간에 대한 체계적 분석을 제공한다.
- 🔄 다른 접근: [[papers/1611_Visual_Instruction_Tuning/review]] — Prismatic VLMs는 LLaVA와 유사한 vision-language 모델이지만 다양한 아키텍처 설계를 체계적으로 탐구하는 다른 접근법이다.
- 🔄 다른 접근: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — Prismatic VLMs의 general visually-grounded language와 EmbSpatial-Bench의 embodied spatial understanding은 VLM 평가에서 서로 다른 특화 영역을 다룬다.
- 🏛 기반 연구: [[papers/1571_Sigmoid_Loss_for_Language_Image_Pre-Training/review]] — Sigmoid Loss의 효율적인 vision-language pre-training 기법이 Prismatic VLMs의 설계 공간 탐구에 훈련 효율성 측면의 기반을 제공한다.
