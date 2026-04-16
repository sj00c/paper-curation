---
title: "1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S"
authors:
  - "Adrien Bardes"
  - "Jean Ponce"
  - "Yann LeCun"
date: "2023.07"
doi: ""
arxiv: ""
score: 4.0
essence: "MC-JEPA는 광학 흐름 추정과 콘텐츠 특성 학습을 단일 공유 인코더 내에서 결합하는 자기 지도 학습 방법으로, 두 목표가 서로 상호 이득을 주어 모션 정보를 포함하는 콘텐츠 특성을 학습한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bardes et al._2023_MC-JEPA A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Conten.pdf"
---

# MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features

> **저자**: Adrien Bardes, Jean Ponce, Yann LeCun | **날짜**: 2023-07-24 | **URL**: [https://arxiv.org/abs/2307.12698](https://arxiv.org/abs/2307.12698)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Multi-task self-supervised learning of content and motion features. MC-JEPA com-*

MC-JEPA는 광학 흐름 추정과 콘텐츠 특성 학습을 단일 공유 인코더 내에서 결합하는 자기 지도 학습 방법으로, 두 목표가 서로 상호 이득을 주어 모션 정보를 포함하는 콘텐츠 특성을 학습한다.

## Motivation

- **Known**: 자기 지도 학습은 주로 객체 식별을 위한 콘텐츠 특성 학습에 집중하고, 광학 흐름 추정은 이미지 콘텐츠 이해 없이 픽셀 수준의 모션을 추정하는 별개의 작업이다.
- **Gap**: 기존 방법들은 콘텐츠 또는 모션 중 하나에만 집중하거나, 모션 추정이 의미론적 콘텐츠를 활용하지 못하는 문제가 있다.
- **Why**: 단일 인코더로 모션과 콘텐츠 정보를 모두 학습할 수 있다면, 광학 흐름 추정부터 의미론적 분할에 이르는 다양한 시각 작업에서 더 나은 성능을 얻을 수 있다.
- **Approach**: MC-JEPA는 PWC-Net 기반의 M-JEPA 광학 흐름 추정 모듈과 VICReg 자기 지도 학습 방법을 다중 작업 설정에서 결합하여, 역방향 일관성 손실과 분산-공분산 정규화를 포함한 개선 사항을 적용한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Qualitative visualization: optical flow. We compare our results of our complete model*

- **통합 아키텍처**: PWC-Net 기반 flow estimator와 VICReg 기반 content learning을 공유 인코더로 통합하여 안정적인 다중 작업 학습 달성
- **성능**: KITTI 2015, Sintel 등 unsupervised optical flow 벤치마크에서 기존 방법 수준의 성능 달성
- **전이 학습**: Cityscapes, DAVIS 등 이미지 및 비디오 분할 작업에서 강력한 전이 성능 확인
- **단일 모델**: 하나의 인코더로 모션과 콘텐츠 작업을 동시에 수행 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2: MC-JEPA architecture. Our method learns motion through optical flow estimation on*

- PWC-Net 기반 coarse-to-fine flow estimation 아키텍처 사용으로 pyramidal features에서 반복적으로 flow 정제
- Forward-backward flow consistency를 위한 cycle consistency loss 적용으로 모션 추정 안정성 개선
- Variance-covariance regularization (VC Reg)을 모든 feature layer에 적용하여 다중 작업 학습 불안정성 해결
- Image augmentation을 통한 VICReg content learning과 비디오 쌍에 기반한 optical flow learning 동시 수행
- Reconstruction loss로 warped frame과 target frame 비교, regression loss로 feature-level flow 추정

## Originality

- 자기 지도 광학 흐름 추정과 콘텐츠 특성 학습을 명시적으로 통합하는 첫 번째 접근법
- Variance-covariance regularization을 multi-task optical flow와 content learning 조합의 불안정성 해결 방법으로 도입
- Joint-embedding predictive architecture를 multi-task 설정에서 활용하여 이미지와 비디오 데이터를 동시에 학습

## Limitation & Further Study

- 학습 안정성을 위해 variance-covariance regularization이 필수적인데, 이는 추가 계산 비용을 초래함
- Flow learning의 시작 시점(epoch)에 대한 민감성이 존재하며, 적절한 curriculum learning 전략이 필요할 수 있음
- ImageNet과 비디오 데이터셋 간의 도메인 불일치가 완전히 해결되지 않을 수 있음
- 후속연구: 더 효율적인 multi-task 균형 조정 메커니즘 개발, 더 다양한 비디오 데이터셋에서의 검증, 3D 장면 이해로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MC-JEPA는 자기 지도 학습에서 광학 흐름과 콘텐츠 학습을 통합하는 창의적이고 기술적으로 견고한 방법으로, 다양한 시각 작업에서 단일 인코더로 우수한 성능을 달성하는 의미 있는 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — MC-JEPA가 확장한 self-supervised learning의 joint-embedding 기초 방법론
- 🔗 후속 연구: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — V-JEPA의 비디오 self-supervised learning을 motion과 content 결합으로 발전
- 🔄 다른 접근: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — 로봇 제어를 위한 visual pre-training에서 joint-embedding vs masked 방법의 차이
- 🏛 기반 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — joint-embedding 예측 아키텍처가 JARVIS-1의 multimodal memory 구조 설계에 기반이 된다.
- 🔗 후속 연구: [[papers/1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation/review]] — R3M의 visual representation을 MC-JEPA의 joint-embedding predictive architecture로 확장하여 더 효과적인 self-supervised robot learning을 실현할 수 있다.
- 🔗 후속 연구: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — I-JEPA의 joint-embedding 아키텍처가 MC-JEPA의 self-supervised video understanding으로 확장되어 시간적 정보까지 다룬다.
- 🔗 후속 연구: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — Minecraft 환경에서의 joint-embedding predictive architecture를 실세계 비디오로 확장하여 더 일반적인 응용을 제시합니다.
