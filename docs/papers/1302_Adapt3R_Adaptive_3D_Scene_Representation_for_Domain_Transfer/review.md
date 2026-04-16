---
title: "1302_Adapt3R_Adaptive_3D_Scene_Representation_for_Domain_Transfer"
authors:
  - "Albert Wilcox"
  - "Mohamed Ghanem"
  - "Masoud Moghani"
  - "Pierre Barroso"
  - "Benjamin Joffe"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Adapt3R는 calibrated RGBD 카메라로부터 3D 장면 표현을 추출하여 모방 학습(IL) 알고리즘의 조건으로 사용하는 관찰 인코더이며, pretrained 2D backbone으로 의미론적 정보를 추출하고 3D 정보는 end-effector에 상대적인 localization에만 사용하여 novel embodiment과 camera viewpoint으로의 zero-shot transfer를 실현한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wilcox et al._2025_Adapt3R Adaptive 3D Scene Representation for Domain Transfer in Imitation Learning.pdf"
---

# Adapt3R: Adaptive 3D Scene Representation for Domain Transfer in Imitation Learning

> **저자**: Albert Wilcox, Mohamed Ghanem, Masoud Moghani, Pierre Barroso, Benjamin Joffe, Animesh Garg | **날짜**: 2025-03-06 | **URL**: [https://arxiv.org/abs/2503.04877](https://arxiv.org/abs/2503.04877)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Adapt3R extracts scene representations from RGBD inputs for use with a variety of imitation learning*

Adapt3R는 calibrated RGBD 카메라로부터 3D 장면 표현을 추출하여 모방 학습(IL) 알고리즘의 조건으로 사용하는 관찰 인코더이며, pretrained 2D backbone으로 의미론적 정보를 추출하고 3D 정보는 end-effector에 상대적인 localization에만 사용하여 novel embodiment과 camera viewpoint으로의 zero-shot transfer를 실현한다.

## Motivation

- **Known**: Imitation learning은 로봇 조작 작업 학습에 효과적이지만, 훈련 분포 외의 관찰에서는 취약하다. 3D 장면 표현을 사용한 기존 방법들은 unseen embodiment과 camera viewpoint에서 제한적 성능 개선만 제공한다.
- **Gap**: 기존 3D 기반 방법들은 point cloud에서 의미론적 정보를 추론해야 하여 저데이터 체제에서 overfitting에 취약하고, camera pose 변화에 대한 일반화가 부족하거나 task별 튜닝을 필요로 한다.
- **Why**: 다양한 embodiment과 camera viewpoint에서 작동하는 범용 로봇 정책 학습은 실제 배포에 필수적이며, 전체 배포 분포를 커버하는 충분한 데이터 수집은 현실적으로 불가능하므로 아키텍처 차원의 일반화가 필요하다.
- **Approach**: Pretrained CLIP ResNet 2D backbone으로 semantic feature를 추출하여 point cloud에 lift한 후, 신중한 post-processing과 learned attention pooling으로 단일 conditioning vector로 압축하는 방식으로 3D 정보는 localization 역할에만 제한한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: (a) Adapt3R facilitates zero-shot transfer to novel embodiments and viewpoints. (b) Adapt3R can*

- **광범위한 실험**: 93개 시뮬레이션 작업과 6개 실제 작업에서 검증하여 multitask 성능 유지
- **Zero-shot transfer**: novel embodiment과 camera pose에 대해 추가 학습 없이 전이 가능
- **다양한 IL 알고리즘 호환성**: diffusion policy, transformer 등 arbitrary action decoder와 end-to-end 학습 가능
- **실제 성과**: 실제 환경 실험에서 차선 baseline 대비 43.8% 성능 개선

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Adapt3R extracts scene representations from RGBD inputs for use with a variety of imitation learning*

- RGBD 입력으로부터 pretrained CLIP ResNet을 사용하여 feature volume 추출
- Camera calibration 데이터를 활용하여 multiple viewpoint의 features를 단일 point cloud로 통합
- Point cloud에 positional encoding과 language embedding 추가
- Attention pooling 레이어로 point cloud를 단일 conditioning vector z로 압축
- Arbitrary action decoder π_ϕ(a|z)와 end-to-end로 학습
- Point cloud post-processing 단계에서 기하학적 노이즈 제거 및 semantic 정보 보존

## Originality

- **Semantic-3D 역할 분리**: 기존 방법과 달리 semantic 추론은 2D backbone에 완전히 위임하고 3D는 localization만 담당하는 철학적 혁신
- **Foundation model 활용**: Frozen pretrained 2D backbone을 활용하여 데이터 효율성 증대
- **Attention pooling 기반 압축**: 손수작업이 필요한 feature selection 대신 학습 가능한 attention mechanism 도입
- **일반적 아키텍처**: 특정 IL 알고리즘에 종속되지 않고 다양한 action decoder와 호환 가능한 설계

## Limitation & Further Study

- **Calibrated camera 의존성**: Camera intrinsic/extrinsic 파라미터가 필수이며, uncalibrated 설정에서의 성능 미평가
- **실제 실험 수량**: 6개 실제 작업만으로 검증되어 시뮬레이션-현실 간극(sim-to-real) 일반화 정도 불명확
- **Pretrained backbone 선택**: CLIP ResNet 특화 설계로 다른 2D foundation model(e.g., Vision Transformer)의 영향 미분석
- **고주파 제어 한계**: Point cloud 기반 접근의 근본적 한계로 고속 반복 제어가 필요한 작업의 성능 미보고
- **후속 연구**: (1) Uncalibrated/monocular 설정에서의 확장, (2) 더 많은 실제 로봇 embodiment에서의 검증, (3) Long-horizon task에 대한 temporal modeling 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Adapt3R은 semantic 정보와 3D localization을 명확히 분리하는 설계 철학으로 기존 3D 기반 방법의 한계를 체계적으로 해결하며, 광범위한 실험과 실제 성과로 multitask imitation learning에서 embodiment과 viewpoint generalization의 중요한 진전을 이루었다.

## Related Papers

- 🔗 후속 연구: [[papers/1594_Transferring_Foundation_Models_for_Generalizable_Robotic_Man/review]] — 일반화 가능한 로봇 조작을 위한 foundation model 전이와 3D 장면 표현 적응이 상호 보완적입니다.
- 🔄 다른 접근: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — 이종 사전 훈련 데이터 스케일링과 3D 장면 표현 도메인 전이가 다른 일반화 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1520_R3M_A_Universal_Visual_Representation_for_Robot_Manipulation/review]] — 범용 시각 표현 R3M이 Adapt3R의 3D 장면 표현 학습에 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1559_RVT_Robotic_View_Transformer_for_3D_Object_Manipulation/review]] — RVT의 3D object manipulation을 위한 view transformer 개념을 domain transfer를 위한 adaptive 3D scene representation으로 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — 둘 다 cross-embodiment learning을 다루지만 Adapt3R는 3D scene representation에, Scaling Cross-Embodied는 unified policy에 중점을 둡니다.
