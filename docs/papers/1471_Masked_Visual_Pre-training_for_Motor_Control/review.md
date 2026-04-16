---
title: "1471_Masked_Visual_Pre-training_for_Motor_Control"
authors:
  - "Tete Xiao"
  - "Ilija Radosavovic"
  - "Trevor Darrell"
  - "Jitendra Malik"
date: "2022.03"
doi: ""
arxiv: ""
score: 4.0
essence: "실제 이미지에서 자기감독학습(self-supervised learning)으로 시각 표현을 사전학습한 후, 동결된 인코더 위에서 강화학습으로 모터 제어 정책을 학습하는 방법을 제시하며, 지도학습 기반 인코더를 크게 능가한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xiao et al._2022_Masked Visual Pre-training for Motor Control.pdf"
---

# Masked Visual Pre-training for Motor Control

> **저자**: Tete Xiao, Ilija Radosavovic, Trevor Darrell, Jitendra Malik | **날짜**: 2022-03-11 | **URL**: [https://arxiv.org/abs/2203.06173](https://arxiv.org/abs/2203.06173)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Masked visual pre-training for motor control. Left: We ﬁrst pre-train visual representations using self-superv*

실제 이미지에서 자기감독학습(self-supervised learning)으로 시각 표현을 사전학습한 후, 동결된 인코더 위에서 강화학습으로 모터 제어 정책을 학습하는 방법을 제시하며, 지도학습 기반 인코더를 크게 능가한다.

## Motivation

- **Known**: 비전-기반 강화학습은 높은 샘플 복잡도와 낮은 일반화 능력이 문제이며, 보조 목표(auxiliary objectives)를 통해 개선 시도가 있었다. 최근 자기감독학습이 다양한 시각 작업에서 성공했으나 모터 제어 분야에는 적용이 제한적이었다.
- **Gap**: 대규모 실제 이미지를 활용한 자기감독학습이 모터 제어 작업에 효과적인지, 그리고 ImageNet 같은 객체 중심 데이터셋 대비 일상 상호작용 이미지가 더 나은 표현을 학습하는지는 미지의 영역이었다.
- **Why**: 자기감독학습 기반 시각 표현은 라벨 없이 대규모 데이터를 활용하여 샘플 효율성을 높이고 실제 환경으로의 전이 가능성을 제공하며, 다양한 로봇과 작업에 일반화될 수 있어 모터 제어의 실용성을 크게 향상시킨다.
- **Approach**: MAE(Masked Autoencoder)를 사용하여 HOI(Human-Object Interaction) 데이터셋의 이미지에서 시각 표현을 자기감독으로 사전학습한 후, 인코더를 고정하고 PPO 알고리즘으로 작업별 제어 정책을 학습한다. 새로운 벤치마크 PixMC를 제공하여 평가한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3. Example reconstructions. For each triplet from left to right: the masked image, the reconstructed image, the g*

- **자기감독 우월성**: 라벨, 상태 추정, 전문가 시연 없이 지도학습 인코더를 최대 80% 절대 성공률로 초과하며 때로는 오라클 상태 성능과 맞먹는다.
- **일반화 가능성**: 단일 시각 인코더로 다양한 형태의 움직임, 장면, 로봇을 포함하는 모터 제어 작업을 작업별 미세조정 없이 해결한다.
- **데이터셋 발견**: YouTube, Epic Kitchens 등의 자연스러운 인간-물체 상호작용 이미지가 ImageNet 사전학습보다 조작 작업에 더 효과적임을 입증한다.
- **벤치마크 기여**: GPU 시뮬레이터 기반 PixMC 벤치마크를 제공하여 후속 연구를 촉진한다.
- **표현 품질**: 학습된 표현이 색상, 형태, 물체 어포던스를 분리(disentangle)하여 다양한 객체 기하학과 구성을 처리한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Masked visual pre-training for motor control. Left: We ﬁrst pre-train visual representations using self-superv*

- MAE를 사용하여 75% 패치 마스킹 비율로 HOI 데이터셋(~700K 이미지)의 자기감독 사전학습 수행
- Vision Transformer(ViT) 기반 인코더-디코더 아키텍처로 마스크된 패치 재구성
- 사전학습된 인코더를 동결하고 이미지 특성 벡터와 관절 위치/속도 고유감각 정보를 연결
- 작은 MLP 네트워크 정책과 비평자를 PPO 알고리즘으로 각 작업에 대해 학습
- PixMC 벤치마크에서 다양한 비교 기준(오라클, ImageNet 지도학습)에 대해 평가

## Originality

- 실제 이미지에서 대규모로 자기감독학습된 시각 표현을 모터 제어에 처음 적용하는 선도적 시도
- 인코더를 동결하고 다양한 작업에 재사용하는 단순하면서도 효과적인 설계 패러다임 제시
- 자연스러운 일상 상호작용 이미지(Human-Object Interaction)가 객체 분류용 ImageNet보다 제어 작업에 더 적합함을 발견
- 모터 제어 평가용 전문 벤치마크(PixMC)를 구성하고 공개하여 커뮤니티 기여

## Limitation & Further Study

- 평가가 주로 시뮬레이터(GPU 기반)에 한정되어 실제 로봇 하드웨어 검증이 제한적
- HOI 데이터셋 구성이 특정 도메인(주방, 손 중심)에 치우칠 수 있으며 더 다양한 인간 활동 포함 필요
- 인코더 동결 설계가 매우 새로운 시각적 맥락(크게 다른 로봇, 환경)에 대한 적응성 제약
- 마스킹 비율, 데이터셋 크기, 사전학습 기간 등 하이퍼파라미터 영향에 대한 상세 분석 부족
- 후속 연구는 실제 로봇 플랫폼에서의 전이 학습, 더 다양한 작업 도메인 포함, 적응형 인코더 미세조정 전략 탐색이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 자기감독학습 기반 시각 표현이 모터 제어에 매우 효과적임을 처음 체계적으로 보여주는 중요한 기여이며, 실제 이미지의 활용, 인코더 동결 패러다임, 벤치마크 제공을 통해 시각-기반 제어 연구를 크게 진전시킨다.

## Related Papers

- 🔄 다른 접근: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — 둘 다 self-supervised visual representation learning을 다루지만 masked pre-training과 DINOv2의 접근법 차이를 비교할 수 있다.
- 🔗 후속 연구: [[papers/1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation/review]] — R3M의 universal visual representation을 masked visual pre-training과 결합하여 더 강력한 motor control을 위한 시각적 표현을 학습할 수 있다.
- 🏛 기반 연구: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — self-supervised learning의 기본 원리인 joint-embedding을 motor control을 위한 visual representation learning에 적용하는 토대를 제공한다.
- 🔄 다른 접근: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — 로봇 제어를 위한 visual pre-training에서 joint-embedding vs masked 방법의 차이
- 🔄 다른 접근: [[papers/1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation/review]] — R3M의 인간 비디오 기반 pre-training과 달리 masked visual pre-training을 통한 motor control representation learning 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — I-JEPA의 자기 지도 학습 방법론이 로봇 제어를 위한 masked visual pre-training 기법 개발에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1629_Whom_to_Trust_Elective_Learning_for_Distributed_Gaussian_Pro/review]] — 모터 제어를 위한 masked visual pre-training이 분산 Gaussian process regression의 시각적 특징 학습 기반을 제공한다.
