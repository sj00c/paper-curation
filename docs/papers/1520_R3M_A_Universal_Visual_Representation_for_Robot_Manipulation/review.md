---
title: "1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation"
authors:
  - "Suraj Nair"
  - "Aravind Rajeswaran"
  - "Vikash Kumar"
  - "Chelsea Finn"
  - "Abhinav Gupta"
date: "2022.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Ego4D 인간 비디오 데이터셋에서 pre-train한 R3M 시각 표현을 제안하여, 로봇 조작 작업의 data-efficient 학습을 가능하게 한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Nair et al._2022_R3M A Universal Visual Representation for Robot Manipulation.pdf"
---

# R3M: A Universal Visual Representation for Robot Manipulation

> **저자**: Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, Abhinav Gupta | **날짜**: 2022-03-23 | **URL**: [https://arxiv.org/abs/2203.12601](https://arxiv.org/abs/2203.12601)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Pre-Training Reusable Representations for Robot Manipulation (R3M): We pre-train a visual*

Ego4D 인간 비디오 데이터셋에서 pre-train한 R3M 시각 표현을 제안하여, 로봇 조작 작업의 data-efficient 학습을 가능하게 한다.

## Motivation

- **Known**: 컴퓨터 비전과 NLP 분야에서 대규모 다양한 데이터로 pre-train한 표현(ImageNet, BERT)이 downstream 작업 성능을 크게 향상시킨다는 것이 알려져 있다. 로봇 분야에서도 일반적 표현 학습의 필요성이 인식되고 있으나, 로봇 상호작용 데이터 부족으로 진전이 제한적이다.
- **Gap**: 로봇을 위한 ImageNet/BERT 수준의 universal visual representation이 부재하며, 기존 로봇 데이터셋은 제한된 환경과 작업만 포함하고 있다. 인간 비디오의 embodiment 차이가 로봇 학습에 효과적인지 실증적으로 검증된 바가 부족하다.
- **Why**: 효과적인 universal representation은 새로운 환경과 작업에서의 sample efficiency를 획기적으로 개선할 수 있으며, 이는 실제 로봇 배포의 실현 가능성을 높인다. 인간 비디오라는 풍부한 in-the-wild 데이터 활용은 로봇 학습의 확장성 문제를 해결할 수 있는 경로를 제시한다.
- **Approach**: Ego4D 인간 비디오 데이터셋에서 time-contrastive learning, video-language alignment, L1 sparsity penalty의 세 가지 학습 목표를 결합하여 R3M을 pre-train하고, 이를 frozen perception module로 사용하여 downstream 정책 학습을 수행한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Data Efﬁcient Imitation Learning in Unseen Environments/Tasks. We report the success rates*

- **simulation 성능**: 12개 조작 작업에서 training from scratch 대비 20% 이상, CLIP/MoCo 같은 SOTA 표현 대비 10% 이상의 성공률 향상 달성
- **실제 로봇 성능**: Franka Emika Panda 로봇이 20개 미만의 demonstrations(약 10분)으로 수건 접기, 팬에 상추 넣기 등 복잡한 작업을 50% 이상의 성공률로 학습
- **일반화 능력**: 9개 시점과 3개 서로 다른 simulation 환경에서 일관되게 우수한 성능 입증
- **실용성**: pre-trained model과 코드 공개로 즉시 다운로드 가능한 standard vision model 제공

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Ego4D [16] Video and Language (left). Sample frames and associated language from Grauman*

- Ego4D 데이터셋의 egocentric 비디오에서 diverse human manipulation behavior 수집
- Time-contrastive learning으로 temporal dynamics 및 state transition 정보 포착
- Video-language alignment을 통해 semantic relevance와 task-relevant features(objects, relationships) 학습
- L1/L2 penalties로 background 등 irrelevant features 제거하고 compact representation 유도
- Frozen perception module로 downstream policy learning(imitation learning 등)에 사용
- Adroit, Franka-Kitchen, MetaWorld 등 다양한 simulation 환경에서 광범위한 평가 수행

## Originality

- 인간 비디오의 temporal dynamics와 언어 정보를 동시에 활용하는 multi-modal pre-training 설계가 차별화됨 (concurrent work는 정적 프레임만 사용)
- 로봇 조작을 위해 명시적으로 설계된 세 가지 손실함수(temporal, semantic, sparsity) 조합의 이론적 근거 제시
- 기존 CLIP, ImageNet, MoCo 등과의 직접 비교를 통해 인간 비디오 pre-training의 효과를 체계적으로 실증
- Embodiment gap 극복 가능성을 실제 로봇 실험으로 입증하는 것이 novel contribution

## Limitation & Further Study

- 실제 로봇 실험이 단일 환경(cluttered apartment)과 한정된 작업 수로 제한적 - 다양한 실제 환경에서의 일반화 검증 필요
- Demonstration 수(20개)는 여전히 적지만, dense reward나 task specification의 필요성 미검토
- R3M의 내부 표현이 어떤 semantic features를 학습했는지의 해석가능성 분석 부족
- Ego4D의 인간 손과 로봇 gripper 간 morphological 차이 영향 분석 미흡
- 시간 경과에 따른 표현의 transferability 변화 및 domain shift 정량화 부족
- 후속 연구는 더 많은 실제 로봇 플랫폼/환경, larger-scale real-world evaluation, representation interpretability 향상에 초점

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: R3M은 인간 비디오 pre-training을 통해 로봇 조작의 data-efficient 학습을 달성한 중요한 실증 연구로, 실제로 다운로드 가능한 artifact를 제공함으로써 로봇 학습 커뮤니티의 standard tool 역할 가능성이 높다. 다만 실제 로봇 검증의 확장성과 표현 해석가능성 개선이 향후 과제이다.

## Related Papers

- 🏛 기반 연구: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — R3M의 visual representation learning을 위한 기본적인 self-supervised visual feature learning 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — R3M의 인간 비디오 기반 pre-training과 달리 masked visual pre-training을 통한 motor control representation learning 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — R3M의 visual representation을 MC-JEPA의 joint-embedding predictive architecture로 확장하여 더 효과적인 self-supervised robot learning을 실현할 수 있다.
- 🔗 후속 연구: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — R3M의 universal visual representation을 masked visual pre-training과 결합하여 더 강력한 motor control을 위한 시각적 표현을 학습할 수 있다.
- 🔗 후속 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — CLIP의 visual representation을 로봇 조작을 위한 universal visual representation과 결합하여 더 강력한 시각적 이해를 달성할 수 있다.
- 🏛 기반 연구: [[papers/1515_Phantom_Training_Robots_Without_Robots_Using_Only_Human_Vide/review]] — Phantom이 인간 비디오에서 로봇 정책을 학습하기 위해 활용하는 visual representation learning의 기초 방법론을 제공한다.
- 🏛 기반 연구: [[papers/1302_Adapt3R_Adaptive_3D_Scene_Representation_for_Domain_Transfer/review]] — 범용 시각 표현 R3M이 Adapt3R의 3D 장면 표현 학습에 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1331_CLASS_Contrastive_Learning_via_Action_Sequence_Supervision_f/review]] — 둘 다 universal visual representation을 추구하지만 CLASS는 action sequence supervision에, R3M은 general robot manipulation에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — R3M의 supervised visual representation과 DINOv2의 self-supervised visual feature는 로봇 조작을 위한 시각 표현 학습에서 서로 다른 접근 방식을 제시한다.
