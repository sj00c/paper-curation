---
title: "1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision"
authors:
  - "Maxime Oquab"
  - "Timothée Darcet"
  - "Théo Moutakanni"
  - "Huy Vo"
  - "Marc Szafraniec"
date: "2023.04"
doi: ""
arxiv: ""
score: 4.0
essence: "자기지도학습(self-supervised learning)을 대규모 큐레이션 데이터와 1B 파라미터 ViT 모델로 학습하여 텍스트 감독 없이도 다양한 비전 작업에서 통용되는 고급 시각 특성을 생성하는 DINOv2 모델을 제안한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Visual_Language_Navigation"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Oquab et al._2023_DINOv2 Learning Robust Visual Features without Supervision.pdf"
---

# DINOv2: Learning Robust Visual Features without Supervision

> **저자**: Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Hervé Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, Piotr Bojanowski | **날짜**: 2023-04-14 | **URL**: [https://arxiv.org/abs/2304.07193](https://arxiv.org/abs/2304.07193)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Evolution of performance when scaling in parameters. We show performance on eight*

자기지도학습(self-supervised learning)을 대규모 큐레이션 데이터와 1B 파라미터 ViT 모델로 학습하여 텍스트 감독 없이도 다양한 비전 작업에서 통용되는 고급 시각 특성을 생성하는 DINOv2 모델을 제안한다.

## Motivation

- **Known**: 자기지도학습은 ImageNet-1k 같은 소규모 큐레이션 데이터셋에서는 우수한 성능을 보이지만, 비큐레이션 데이터로 확장 시 특성 품질이 저하된다. NLP에서는 대규모 비감독 데이터로 foundation 모델이 성공을 거두었다.
- **Gap**: 자기지도학습이 대규모 큐레이션 데이터로 학습될 경우 foundation 모델 수준의 범용 시각 특성을 생성할 수 있는지 미검증된 상태이며, 이를 위한 데이터 처리 파이프라인과 확장 가능한 학습 기법이 부족하다.
- **Why**: Foundation 모델은 다양한 비전 작업에서 미세조정 없이도 즉시 활용 가능하여 이미지 기반 시스템의 구축을 크게 단순화하고, 텍스트 감독 없는 순수 자기지도학습 접근은 이미지의 풍부한 정보를 더 완전하게 포착할 수 있다.
- **Approach**: 자동화된 데이터 처리 파이프라인으로 142M 이미지의 큐레이션 데이터셋을 구축하고, 판별적 자기지도학습(discriminative self-supervised learning) 기반의 iBOT를 개선하여 모델 및 데이터 크기 확장 시 안정성과 속도를 향상시킨 후, 1B 파라미터 ViT를 학습하고 이를 소규모 모델로 증류한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Evolution of performance when scaling in parameters. We show performance on eight*

- **데이터 처리 파이프라인**: 비큐레이션 이미지와 큐레이션 이미지를 embedding 기반 deduplication과 retrieval로 통합하여 다양하고 균형잡힌 대규모 데이터셋 구성
- **확장성 개선**: 기존 방법 대비 약 2배 빠른 학습 속도와 3배 적은 메모리 사용으로 대규모 배치와 장시간 학습 가능
- **성능 초과**: 이미지 수준(분류, 검색) 및 픽셀 수준(분할, 깊이 추정) 벤치마크 8가지에서 OpenCLIP 포함 기존 자기지도학습 방법들을 초과하고 약한감독(weakly-supervised) 모델과 경쟁 수준의 성능 달성
- **범용 특성**: 미세조정 없이 다양한 하위 작업(분류, 인스턴스 검색, 비디오 이해, 깊이 추정 등)에서 강력한 전이 가능성 입증

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Overview of our data processing pipeline. Images from curated and uncurated data sources*

- 데이터: 비큐레이션 소스를 자기지도 retrieval로 큐레이션 데이터와 정렬하고 naive clustering으로 개념 균형 조정
- 모델: iBOT 기반 판별적 자기지도학습에 gradient checkpointing, selective gradient computation, efficient attention 등 메모리-효율 기법 적용
- 학습: Vision Transformer(ViT) 아키텍처로 1B 파라미터 모델 학습 후 knowledge distillation으로 더 작은 모델 계열 생성
- 평가: 이미지 분류, 분할, 깊이, 인스턴스 검색, 세분류, 변형 강건성, 비디오 이해 등 광범위한 벤치마크에서 frozen feature 평가

## Originality

- 자기지도학습 확장에서 **데이터 큐레이션의 중요성** 강조: NLP의 데이터 정제 파이프라인을 비전에 적용한 자동화 approach
- **판별적 자기지도학습의 재검토**: 기존 iBOT를 대규모 데이터와 모델에 맞게 최적화하는 체계적인 기술 개선(메모리, 속도)
- **Foundation 모델 검증**: 순수 자기지도학습만으로 텍스트-이미지 정렬 없이도 foundation 모델 수준의 성능 달성 가능함을 실증적으로 입증

## Limitation & Further Study

- 142M 이미지 데이터셋 규모는 여전히 대규모 비감독 데이터셋(수십억)에 비해 작으며, 큐레이션 과정의 비용과 복잡도에 대한 분석 부재
- 데이터 파이프라인의 자동화 수준 및 다른 도메인(의료, 위성 이미지 등)으로의 일반화 가능성 미검증
- Knowledge distillation의 효과 및 최적 구성에 대한 심층 분석 부족
- 후속 연구: 더 큰 데이터셋에서의 확장성, 다중 모달 학습 통합, 자동 큐레이션 파이프라인 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DINOv2는 자기지도학습으로 foundation 모델 수준의 범용 시각 특성을 생성 가능함을 체계적인 데이터 큐레이션과 확장 최적화로 입증한 획기적 연구이며, 광범위한 벤치마크 검증과 모델 공개로 실용적 영향력이 매우 높다.

## Related Papers

- 🔄 다른 접근: [[papers/1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation/review]] — R3M의 supervised visual representation과 DINOv2의 self-supervised visual feature는 로봇 조작을 위한 시각 표현 학습에서 서로 다른 접근 방식을 제시한다.
- 🔗 후속 연구: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — JEPA의 joint-embedding predictive architecture는 DINOv2의 self-supervised learning을 더 발전시킨 representation learning 방법론이다.
- ⚖️ 반론/비판: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — CLIP의 language supervision과 DINOv2의 purely visual self-supervision은 multimodal vs. unimodal feature learning의 대조적 접근을 보여준다.
- 🏛 기반 연구: [[papers/1345_CoWs_on_Pasture_Baselines_and_Benchmarks_for_Language-Driven/review]] — CLIP 기반 언어-비전 매칭의 기반이 되는 자기지도학습 시각 특성 추출 방법을 제공합니다.
- 🔄 다른 접근: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — 둘 다 self-supervised visual representation learning을 다루지만 masked pre-training과 DINOv2의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — 둘 다 self-supervised visual representation learning을 다루지만 natural language supervision과 비지도 학습의 접근법 차이를 분석할 수 있다.
- 🔄 다른 접근: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — 둘 다 로봇 비전을 위한 시각적 특징 학습에 초점을 맞추지만, 멀티모달 융합은 VLM 통합을, DINOv2는 자기지도 학습에 집중한다.
- 🔄 다른 접근: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — DINOv2의 self-supervised visual learning과 Prismatic VLMs의 supervised VLM 설계는 시각적 표현 학습의 다른 패러다임을 보여준다.
- 🏛 기반 연구: [[papers/1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation/review]] — R3M의 visual representation learning을 위한 기본적인 self-supervised visual feature learning 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1569_Segment_Anything/review]] — 자기 지도 학습 기반 시각 모델에서 SAM은 분할에, DINOv2는 robust visual feature 학습에 특화된 서로 다른 접근법이다.
- 🔄 다른 접근: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — 자기 지도 학습에서 I-JEPA는 joint-embedding predictive로, DINOv2는 supervision 없는 robust feature로 서로 다른 방식을 사용한다.
- 🏛 기반 연구: [[papers/1345_CoWs_on_Pasture_Baselines_and_Benchmarks_for_Language-Driven/review]] — CLIP 기반의 시각적 특성 추출이 언어 기반 zero-shot 네비게이션의 핵심 기반입니다.
