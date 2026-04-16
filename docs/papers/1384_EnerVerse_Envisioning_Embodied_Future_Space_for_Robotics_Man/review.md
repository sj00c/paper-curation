---
title: "1384_EnerVerse_Envisioning_Embodied_Future_Space_for_Robotics_Man"
authors:
  - "Siyuan Huang"
  - "Liliang Chen"
  - "Pengfei Zhou"
  - "Shengcong Chen"
  - "Zhengkai Jiang"
date: "2025.01"
doi: ""
arxiv: ""
score: 4.0
essence: "EnerVerse는 chunk-wise autoregressive video diffusion과 sparse memory를 활용하여 instruction으로부터 embodied future space를 예측하고, multi-view video generation과 4D Gaussian Splatting 기반 data flywheel을 통해 로봇 조작을 위한 generative foundation model을 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2025_EnerVerse Envisioning Embodied Future Space for Robotics Manipulation.pdf"
---

# EnerVerse: Envisioning Embodied Future Space for Robotics Manipulation

> **저자**: Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Yue Liao, Peng Gao, Hongsheng Li, Maoqing Yao, Guanghui Ren | **날짜**: 2025-01-03 | **URL**: [https://arxiv.org/abs/2501.01895](https://arxiv.org/abs/2501.01895)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: An overview of ENERVERSE. With camera ob-*

EnerVerse는 chunk-wise autoregressive video diffusion과 sparse memory를 활용하여 instruction으로부터 embodied future space를 예측하고, multi-view video generation과 4D Gaussian Splatting 기반 data flywheel을 통해 로봇 조작을 위한 generative foundation model을 제시한다.

## Motivation

- **Known**: Video generation 모델들은 high-quality spatiotemporal prediction이 가능하며, 최근 연구들은 video generation 모델을 로봇 조작 예측에 적용하려는 시도를 하고 있다.
- **Gap**: 기존 방법들은 일반 목적의 video generation 모델을 단순히 adapting하여 2D pixel-level 품질을 추구하지만, 3D 로봇 환경과의 substantial gap을 무시하고 action-conditioned 3D dynamics를 제대로 인코딩하지 못한다.
- **Why**: 정확한 3D 미래 공간 예측과 action planning은 로봇의 물리 세계 상호작용 성능을 결정하는 핵심이며, sim-to-real gap 해결은 실제 배포의 필수 조건이다.
- **Approach**: Multi-view diffusion generator로 3D spatial prior를 학습하고, sparse context memory로 long-term reasoning을 가능하게 하며, 4DGS 기반 data flywheel로 geometry-consistent training data를 확보하여 4D world representation을 physical action으로 변환한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: An overview of ENERVERSE. With camera ob-*

- **Chunk-wise Autoregressive Architecture**: Sparse memory를 활용하여 약 80% frame drop에도 robust하게 작동하며 이론상 무한 길이 시퀀스 생성 가능
- **Multi-View Diffusion Generator**: Ray direction map과 temporal attention으로 single camera 환경에서도 3D 사전 지식을 활용하여 rendered views를 생성
- **4DGS-based Data Flywheel**: Generative model과 4D Gaussian Splatting을 결합하여 sim-to-real gap을 감소시키는 자체 강화 데이터 루프 구성
- **State-of-the-Art Performance**: Simulation과 real-world tasks 모두에서 최고 성능 달성
- **Computational Efficiency**: Single RTX 4090에서 8-step action chunk당 약 280ms로 실시간 처리 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2: An overview of our chunk-wise autoregressive generation approach and multi-view diffusion*

- VAE로 observed frames를 latent space에 인코딩하고 diffusion model의 noise prediction 대신 v-prediction 사용
- Chunk 단위로 autoregressive하게 다음 frame들을 생성하며, newly generated frames가 다음 iteration의 clean frames가 됨
- Training 시 random sampling으로 sparse context를 선택하여 video redundancy 활용 및 OOD robustness 강화
- Multi-view diffusion generator block에서 ray direction maps와 spatial/temporal attention을 조합하여 multi-view consistency 학습
- 4DGS로 observation을 3D reconstruction한 후 rendered views를 생성하여 multi-view training data 자동 생성
- Policy head (EnerVerse-A)를 통해 generated video features를 directly physical actions로 변환
- EOS detection으로 sequence generation 종료 (각 frame의 EOS와의 L1 distance 기반)

## Originality

- Chunk-wise autoregressive 방식으로 long-term grounding을 sparse memory로 구현한 novel architecture
- Ray direction map 활용으로 single camera에서 multi-view consistency prior 학습
- 4D Gaussian Splatting과 generative model의 결합을 통한 self-reinforcing data flywheel 구상
- Video diffusion을 3D action-conditioned dynamics로 explicitly align하는 관점의 재정의

## Limitation & Further Study

- Multi-view pre-training을 위한 정확히 calibrated multi-camera 데이터 수집의 노동 집약성
- Threshold 기반 EOS detection의 robustness가 실제 환경 변화에 얼마나 강인한지 상세 분석 부족
- Single camera deployment 시 rendered views의 품질이 실제 multi-camera 데이터보다 얼마나 열등한지 정량적 평가 필요
- 다양한 로봇 플랫폼 및 task 종류에 대한 일반화 성능 검증 필요
- 메모리 효율성 및 다양한 시간 길이의 task에 대한 scaling 특성 미상

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: EnerVerse는 video diffusion을 로봇 조작에 체계적으로 align하면서 3D spatial prior 학습과 data flywheel을 통해 sim-to-real gap을 해결하는 포괄적인 framework를 제시하며, chunk-wise autoregressive와 sparse memory 설계는 독창적이고 실용적이다.

## Related Papers

- 🔄 다른 접근: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — 두 논문 모두 video diffusion을 로봇 조작에 활용하지만 chunk-wise autoregressive vs unified platform이라는 다른 구조를 제시한다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전학습의 visuomotor policy 적용에 대한 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering/review]] — 3D Gaussian Splatting을 4D로 확장하여 시공간적 embodied future space 생성에 적용했다.
- 🏛 기반 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — World Simulation with Video Foundation Models의 비디오 기반 물리 시뮬레이션이 EnerVerse의 video generation과 4D Gaussian Splatting 결합에 기초가 된다.
- 🔄 다른 접근: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — PointWorld의 3D world model scaling과 EnerVerse의 4D Gaussian-based future space는 로봇을 위한 세계 모델링에서 서로 다른 차원적 접근이다.
- 🔄 다른 접근: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — 둘 다 video diffusion 기반 로봇 조작 플랫폼이지만 unified framework vs chunk-wise approach라는 구조적 차이가 있다.
