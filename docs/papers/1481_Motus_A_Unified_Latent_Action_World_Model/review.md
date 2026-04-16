---
title: "1481_Motus_A_Unified_Latent_Action_World_Model"
authors:
  - "Hongzhe Bi"
  - "Hengkai Tan"
  - "Shenghao Xie"
  - "Zeyuan Wang"
  - "Shuhe Huang"
date: "2025.12"
doi: ""
arxiv: ""
score: 4.0
essence: "Motus는 vision-language-action 모델, world 모델, inverse dynamics 모델, video generation 모델을 unified latent action world model로 통합하는 embodied agent 프레임워크이며, Mixture-of-Transformer 아키텍처와 optical flow 기반 latent action을 통해 대규모 이질적 데이터 학습을 가능하게 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bi et al._2025_Motus A Unified Latent Action World Model.pdf"
---

# Motus: A Unified Latent Action World Model

> **저자**: Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, Jun Zhu | **날짜**: 2025-12-15 | **URL**: [https://arxiv.org/abs/2512.13030](https://arxiv.org/abs/2512.13030)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Motus Architecture. Here, at . . . at+k are actions, zt . . . zt+k are latent actions, and τv and τa are the r*

Motus는 vision-language-action 모델, world 모델, inverse dynamics 모델, video generation 모델을 unified latent action world model로 통합하는 embodied agent 프레임워크이며, Mixture-of-Transformer 아키텍처와 optical flow 기반 latent action을 통해 대규모 이질적 데이터 학습을 가능하게 한다.

## Motivation

- **Known**: 기존 embodied agent 방법들은 VLA, WM, IDM, VGM을 분리된 모델로 구축하고 있으며, 일부 연구는 이들을 부분적으로 통합하려 시도했으나 완전한 통일을 이루지 못했다.
- **Gap**: 현존 방법들은 5가지 주요 확률분포를 모두 통합하지 못하고 있으며, 이질적 데이터(인터넷 비디오, egocentric 데모, 로봇 궤적)에서 대규모 action 사전학습이 어렵다.
- **Why**: 통일된 embodied agent는 이해, 세계 모델링, 제어를 하나의 시스템으로 통합해야 하며, 이를 통해 일반적 다중모달 priors와 domain-specific priors를 효과적으로 활용할 수 있다.
- **Approach**: Motus는 Tri-model Joint Attention을 통해 vision-language understanding, video generation, action 전문가를 통합하고, UniDiffuser 스타일의 scheduler로 modality 간 flexible switching을 지원하며, optical flow 기반 latent action과 3단계 학습 파이프라인으로 대규모 action 사전학습을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Motus Architecture. Here, at . . . at+k are actions, zt . . . zt+k are latent actions, and τv and τa are the r*

- **통합 아키텍처**: 5가지 embodied intelligence 패러다임(WM, IDM, VLA, VGM, Video-Action Joint Prediction Model)을 하나의 unified model로 통합
- **성능 향상**: 시뮬레이션에서 X-VLA 대비 +15%, π0.5 대비 +45% 개선, 실제 로봇에서 +11~48% 개선
- **확장 가능한 학습 레시피**: 3단계 학습 파이프라인과 6계층 데이터 피라미드를 통한 cross-embodiment 지식 전이
- **Latent action 표현**: optical flow 기반 pixel-level delta action으로 무레이블 비디오에서의 사전학습 가능

## How

![Figure 1](figures/fig1.webp)

*Figure 1. Motus Architecture. Here, at . . . at+k are actions, zt . . . zt+k are latent actions, and τv and τa are the r*

- **Mixture-of-Transformer (MoT) 아키텍처**: understanding expert, video generation model, action expert를 shared multi-head self-attention layer로 연결하는 Tri-model Joint Attention 설계
- **UniDiffuser 스타일 scheduler**: 각 modality에 서로 다른 timestep과 noise scale 할당으로 flexible한 inference mode switching 실현
- **Deep Compression Autoencoder (DC-AE)**: optical flow를 저차원 latent으로 인코딩하되, 소수의 action label로 supervision하여 robotic activity에 초점 맞춤
- **3단계 학습 파이프라인**: video pretraining → latent action pretraining → embodiment-specific action finetuning
- **6계층 데이터 피라미드**: web-scale, egocentric human, simulation, task-agnostic, multi-robotic, target-robotic 데이터 활용

## Originality

- optical flow를 universal motion expression으로 활용하여 cross-embodiment action 표현을 통합한 novel latent action 설계
- Tri-model Joint Attention을 통한 새로운 multimodal fusion 방식으로 specialized functionality 보존과 cross-modal knowledge fusion 동시 달성
- 3단계 학습 파이프라인과 6계층 데이터 피라미드를 통한 체계적인 대규모 multi-domain pretraining 및 finetuning 전략
- UniDiffuser 기반의 flexible scheduler로 5가지 서로 다른 modeling mode의 adaptive switching 구현

## Limitation & Further Study

- optical flow 추출의 계산 비용과 부정확성이 latent action 학습에 미치는 영향에 대한 분석 부족
- 6계층 데이터 피라미드 구성 시 각 계층의 최적 크기 비율과 영향도에 대한 ablation study 제한적
- 서로 다른 로봇 embodiment 간의 action space 불일치 문제를 optical flow로 완전히 해결하는지 검증 필요
- 실제 로봇 실험이 제한된 환경과 task에 한정되어 일반화 가능성 검증 필요
- 후속 연구로 더 다양한 embodiment과 복잡한 조작 task에 대한 확대 실험 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Motus는 분산된 embodied agent 아키텍처를 unified model로 통합하면서 optical flow 기반 latent action과 체계적인 multi-stage 학습으로 대규모 이질적 데이터 활용을 가능하게 한 혁신적 연구이며, 강력한 실험 성과와 함께 embodied AI의 통합 모델링에 대한 새로운 패러다임을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — embodied AI를 위한 world model의 포괄적인 이론적 기반을 제공하여 Motus의 unified latent action world model 설계에 필수적인 배경지식을 제공한다.
- 🔄 다른 접근: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — world model 기반 embodied agent에서 unified latent action vs generative world model for autonomous driving이라는 서로 다른 도메인별 접근법을 보여준다.
- 🔗 후속 연구: [[papers/1598_Unified_Video_Action_Model/review]] — unified video action model의 개념을 latent action world model과 결합하여 더 통합적인 vision-language-action 프레임워크를 구축한다.
- 🔄 다른 접근: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — unified world model에서 latent action vs 3D vision-language-action의 다른 통합 방식
- 🏛 기반 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — Motus의 world model 기반이 되는 video foundation model을 활용한 물리적 AI
- 🔗 후속 연구: [[papers/1394_FLaRe_Achieving_Masterful_and_Adaptive_Robot_Policies_with_L/review]] — latent action world model을 adaptive robot policy로 확장한 실제 적용 사례
- 🔄 다른 접근: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — 둘 다 unified vision-language-action model을 다루지만 latent action world model과 mixture-of-transformers의 접근법 차이를 비교할 수 있다.
- 🏛 기반 연구: [[papers/1631_World_Models/review]] — world model의 기본 개념과 원리를 unified latent action space에서 구현하는 이론적 기반을 제공한다.
