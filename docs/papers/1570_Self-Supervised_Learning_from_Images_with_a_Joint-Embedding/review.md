---
title: "1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding"
authors:
  - "Mahmoud Assran"
  - "Quentin Duval"
  - "Ishan Misra"
  - "Piotr Bojanowski"
  - "Pascal Vincent"
date: "2023.01"
doi: ""
arxiv: ""
score: 4.0
essence: "I-JEPA는 손으로 만든 데이터 증강 없이 이미지의 문맥 블록으로부터 대상 블록의 표현을 예측하여 의미론적 이미지 표현을 학습하는 Joint-Embedding Predictive Architecture 기반의 자기 지도 학습 방법이다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Visual_Language_Navigation"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Assran et al._2023_Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture.pdf"
---

# Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture

> **저자**: Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, Nicolas Ballas | **날짜**: 2023-01-19 | **URL**: [https://arxiv.org/abs/2301.08243](https://arxiv.org/abs/2301.08243)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3. I-JEPA. The Image-based Joint-Embedding Predictive*

I-JEPA는 손으로 만든 데이터 증강 없이 이미지의 문맥 블록으로부터 대상 블록의 표현을 예측하여 의미론적 이미지 표현을 학습하는 Joint-Embedding Predictive Architecture 기반의 자기 지도 학습 방법이다.

## Motivation

- **Known**: Invariance 기반 방법들은 손으로 만든 증강을 통해 높은 의미론적 표현을 학습하지만 강한 편향을 도입하고, 생성 방법들은 픽셀/토큰 수준에서 예측하여 의미론적 수준이 낮은 경향을 보인다.
- **Gap**: 기존 자기 지도 학습 방법들은 손으로 만든 증강에 의존하거나 낮은 의미론적 수준의 표현을 생성하는 문제가 있으며, 이를 해결하면서도 계산 효율성을 유지하는 접근법이 부족하다.
- **Why**: 의미론적이면서도 일반화 가능한 표현 학습은 다양한 다운스트림 작업에서 성능을 결정하는 핵심이며, 특히 저수준 시각 작업에서의 성능 향상과 계산 효율성은 실제 응용에서 중요하다.
- **Approach**: 이미지를 컨텍스트 블록과 대상 블록으로 분할하고, context encoder로부터의 표현으로 target encoder가 생성한 대상 블록의 표현을 predictor 네트워크로 예측하는 방식이다. 의미론적 표현을 유도하기 위해 충분히 큰 크기의 대상 블록과 공간적으로 분산된 컨텍스트 블록을 사용하는 마스킹 전략을 핵심으로 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. ImageNet Linear Evaluation. The I-JEPA method*

- **손 제작 증강 제거**: 데이터 증강 없이도 ImageNet-1K 선형 평가에서 MAE 등 픽셀 재구성 방법들을 능가하는 의미론적 표현을 학습한다.
- **우수한 확장성**: ViT-Huge/14를 16개 A100 GPU로 72시간 내에 학습 가능하며, 기존 방법 대비 2.5배~10배 이상 계산 효율적이다.
- **다양한 작업에서의 우수성**: 의미 분류 작업에서는 view-invariant 방법과 경쟁력이 있으며, 객체 카운팅과 깊이 예측 같은 저수준 시각 작업에서 더 우수한 성능을 보인다.
- **강한 오프-더-셀프 성능**: 반지도 1% ImageNet-1K와 의미 전이 작업에서 강력한 성능을 달성한다.

## How

![Figure 3](figures/fig3.webp)

*Figure 3. I-JEPA. The Image-based Joint-Embedding Predictive*

- 이미지를 겹치지 않는 패치로 분할하고, 컨텍스트 블록(공간적으로 분산된 가시 패치 모음)과 대상 블록(마스킹된 영역)을 샘플링한다.
- Context encoder (Vision Transformer)는 컨텍스트 패치만 처리하여 표현을 생성한다.
- Predictor 네트워크(좁은 ViT)는 컨텍스트 표현과 위치 토큰을 입력받아 특정 위치의 대상 블록 표현을 예측한다.
- Target encoder (context encoder의 정지된 가중치)는 전체 이미지에서 대상 블록 표현을 계산한다.
- L2 손실을 통해 예측된 표현과 대상 표현 간의 차이를 최소화하여 학습한다.
- Asymmetric architecture (context encoder와 target encoder의 비대칭 설계)로 표현 붕괴를 방지한다.
- 다양한 크기와 위치의 대상 블록들에 대해 동시에 예측하여 컨텍스트로부터 풍부한 의미 정보를 학습하도록 유도한다.

## Originality

- **표현 공간에서의 예측**: 기존 생성 방법과 달리 픽셀/토큰 수준이 아닌 추상적 표현 공간에서 예측하여 불필요한 저수준 세부사항을 제거하고 의미론적 학습을 유도한다.
- **증강 제거**: 손으로 만든 데이터 증강 없이도 높은 의미론적 표현을 학습할 수 있음을 보여주며, 이는 다른 모달리티로의 일반화 가능성을 높인다.
- **신중한 마스킹 전략**: 대상 블록 크기와 컨텍스트 블록의 공간 분산을 체계적으로 분석하여 의미론적 표현 학습의 핵심 요소를 규명한다.
- **계산 효율성**: 표현 공간에서의 예측으로 인한 낮은 계산 복잡도로 기존 방법 대비 현저히 빠른 pretraining을 실현한다.

## Limitation & Further Study

- **Target encoder 정지**: Target encoder의 가중치를 고정시키는 설계로 인한 이론적 정당성의 부족과 최적성 보장 문제가 있다.
- **저수준 작업의 성능 분석 부족**: 깊이 예측과 객체 카운팅에서 우수성을 보이지만 이러한 성능 향상의 메커니즘에 대한 심층 분석이 제한적이다.
- **다른 Vision Transformer 아키텍처 검증 부족**: 주로 ViT-Huge/14 기반으로 검증되어 다른 아키텍처나 더 작은 모델에서의 효과 검증이 제한적이다.
- **다중 모달리티 확장성**: 이미지 중심의 방법이므로 텍스트, 오디오 등 다른 모달리티로의 직접 확장 가능성에 대한 실증적 검증이 부족하다.
- **후속 연구 방향**: 마스킹 전략의 자동 최적화, target encoder 업데이트 메커니즘 개선, 더 강력한 이론적 분석, 멀티모달 학습으로의 확장 등이 필요하다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: I-JEPA는 표현 공간에서의 예측이라는 창의적 아이디어로 손으로 만든 증강을 제거하면서도 높은 의미론적 표현을 학습하고, 뛰어난 계산 효율성으로 자기 지도 학습의 실용성을 크게 향상시킨 중요한 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — 자기 지도 학습에서 I-JEPA는 joint-embedding predictive로, DINOv2는 supervision 없는 robust feature로 서로 다른 방식을 사용한다.
- 🔗 후속 연구: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — I-JEPA의 joint-embedding 아키텍처가 MC-JEPA의 self-supervised video understanding으로 확장되어 시간적 정보까지 다룬다.
- 🏛 기반 연구: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — I-JEPA의 자기 지도 학습 방법론이 로봇 제어를 위한 masked visual pre-training 기법 개발에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — Learning Transferable Visual Models의 자연어 감독 기반 시각 모델 학습이 I-JEPA의 self-supervised 표현 학습 방법론의 기초가 된다.
- 🏛 기반 연구: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — self-supervised learning의 기본 원리인 joint-embedding을 motor control을 위한 visual representation learning에 적용하는 토대를 제공한다.
- 🏛 기반 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — Self-Supervised Learning의 joint-embedding 개념을 자연언어 감독 학습으로 확장하여 전이 가능한 모델을 구현한다.
- 🏛 기반 연구: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — MC-JEPA가 확장한 self-supervised learning의 joint-embedding 기초 방법론
- 🏛 기반 연구: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — 이미지에서의 joint-embedding 자기지도학습 방법론을 제공하여 V-JEPA 2의 비디오 자기지도학습에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1331_CLASS_Contrastive_Learning_via_Action_Sequence_Supervision_f/review]] — Self-Supervised Learning from Images의 joint-embedding 개념을 action sequence 유사성 기반의 supervised contrastive learning으로 로봇 조작에 적용한 연구입니다.
- 🔗 후속 연구: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — JEPA의 joint-embedding predictive architecture는 DINOv2의 self-supervised learning을 더 발전시킨 representation learning 방법론이다.
