---
title: "1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr"
authors:
  - "Lirui Wang"
  - "Xinlei Chen"
  - "Jialiang Zhao"
  - "Kaiming He"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "HPT(Heterogeneous Pre-trained Transformers)는 embodiment-specific tokenizer(stem)와 shared transformer trunk를 통해 서로 다른 로봇 embodiment와 task에서 수집한 대규모 이종 데이터에서 사전 학습하여 일반화된 정책 표현을 학습하는 방법을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2024_Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers.pdf"
---

# Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers

> **저자**: Lirui Wang, Xinlei Chen, Jialiang Zhao, Kaiming He | **날짜**: 2024-09-30 | **URL**: [https://arxiv.org/abs/2409.20537](https://arxiv.org/abs/2409.20537)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The Heterogeneous Pre-training concept.*

HPT(Heterogeneous Pre-trained Transformers)는 embodiment-specific tokenizer(stem)와 shared transformer trunk를 통해 서로 다른 로봇 embodiment와 task에서 수집한 대규모 이종 데이터에서 사전 학습하여 일반화된 정책 표현을 학습하는 방법을 제안한다.

## Motivation

- **Known**: 컴퓨터 비전과 자연어 처리에서 대규모 다양한 데이터로 사전 학습한 foundation model이 우수한 성능을 보이며, 최근 로봇 학습에서도 RT-X, Octo, OpenVLA 등이 다중 embodiment 데이터를 활용한 정책 학습을 시도했다.
- **Gap**: 기존 방법들은 주로 vision 부분의 사전 학습이나 unified data format 가정에 기반하며, 로봇의 heterogeneity(다양한 하드웨어, 센서, 환경)를 체계적으로 다루지 못했다. 특히 proprioception과 vision 정보의 embodiment-agnostic 정렬 문제가 미해결되어 있다.
- **Why**: 로봇 정책 학습에서 각 embodiment마다 별도 데이터 수집 및 학습이 필요해 비용이 많이 들고 과적합되기 쉬운데, heterogeneous한 데이터로부터 공유 표현을 학습하면 새로운 embodiment과 task에 대한 데이터 요구량을 줄이고 일반화 성능을 향상시킬 수 있다.
- **Approach**: HPT는 embodiment-specific stem으로 각 embodiment의 proprioception과 vision을 공유 token 시퀀스로 변환하고, shared transformer trunk에서 이 토큰들을 처리하여 task-agnostic하고 embodiment-agnostic한 표현을 학습한다. 52개 dataset과 1B parameters 규모로 사전 학습하고 새로운 embodiment에 fine-tuning한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: HPT architecture. HPT is modularized*

- **Heterogeneous 데이터 정렬**: embodiment-specific tokenizer를 통해 서로 다른 로봇 하드웨어, 센서, 환경의 proprioception과 vision 정보를 공유 latent space로 정렬하는 메커니즘 개발
- **대규모 사전 학습**: 52개의 이종 dataset과 1B parameters 규모로 확장하여 실제 로봇, simulation, 인간 비디오 등 다양한 embodiment domain에서 사전 학습 시 scaling behavior 입증
- **성능 향상**: 여러 simulator benchmark와 실세계 dexterous task에서 unseen task에 대해 20% 이상 fine-tuned policy 성능 개선
- **전이 학습의 효율성**: 새로운 embodiment 적응 시 minimal 데이터와 학습만 필요한 효율적 전이 학습 가능성 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: HPT architecture. HPT is modularized*

- Embodiment-specific stem: 각 embodiment별로 독립적인 proprioception tokenizer와 vision tokenizer를 설계하여 입력을 고정 개수의 token(예: 16개)으로 변환
- Shared transformer trunk: 모든 embodiment의 tokenized representation을 처리하는 공유 transformer를 supervised learning으로 사전 학습
- Task-specific head: 각 downstream task별로 처리된 token을 해당 embodiment의 action space로 매핑하는 decoder 설계
- 다중 data source 통합: 52개의 이종 dataset(real robot, simulation, human video)을 unified framework에서 동시에 학습
- Transfer learning: 사전 학습된 trunk를 새로운 embodiment과 task에 전이하되, 새로운 stem/head pair만 최소한의 데이터로 학습

## Originality

- 이전 연구들은 vision 사전 학습이나 unified format 가정에 의존했으나, HPT는 proprioception과 vision을 모두 고려한 체계적인 embodiment-agnostic 정렬 방식 제시
- Multimodal learning의 alignment 개념(Flamingo, ImageBind, GPT-4o 등)을 로봇 이종 embodiment 문제에 처음으로 체계적으로 적용
- 52개 dataset(기존 연구의 2배)을 활용한 대규모 heterogeneous 사전 학습의 실증적 입증
- Spinal cord의 신경 회로에서 영감을 받은 stem-trunk-head 구조로 생물학적 직관성 제공

## Limitation & Further Study

- Embodiment-specific stem과 head의 설계가 각 embodiment의 특성을 최적으로 반영하기 위해 수동 조정이 필요할 수 있음
- Transfer learning 시 새로운 embodiment에 대한 초기 데이터 수집이 여전히 필요하며, 완전 zero-shot transfer는 불가능
- 52개 dataset 통합으로 인한 domain gap 문제(예: simulation-to-reality gap)의 명시적 해결 방법이 명확하지 않음
- Large-scale 사전 학습으로 인한 계산 비용과 메모리 요구사항이 크며, 배포 환경에서의 실용성 검토 필요
- 후속연구: 자동화된 stem/head 설계, unsupervised alignment 방법, 더욱 큰 규모 dataset 통합, cross-domain generalization 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: HPT는 로봇 학습의 heterogeneity 문제를 체계적으로 해결하기 위해 multimodal alignment 개념을 처음으로 적용하고, 52개 dataset 규모의 대규모 사전 학습으로 실증했다는 점에서 높은 기여도를 지니며, open-source 공개로 커뮤니티 영향력도 클 것으로 예상된다.

## Related Papers

- 🔄 다른 접근: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — BitVLA가 단일 embodiment에서의 효율화에 중점을 두는 반면, HPT는 다중 이종 embodiment에서의 표현 학습에 초점을 맞춘다.
- 🏛 기반 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — Mastering Diverse Domains의 world model 기반 다중 도메인 학습 개념이 HPT의 이종 데이터 사전 학습 방법론의 기초가 된다.
- ⚖️ 반론/비판: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — CrossFormer가 embodiment 간 수동 정렬 없이 학습하는 반면, HPT는 embodiment-specific tokenizer를 통한 명시적 구조화를 추구한다.
- 🔗 후속 연구: [[papers/1524_Reactive_Diffusion_Policy_Slow-Fast_Visual-Tactile_Policy_Le/review]] — RDP의 tactile feedback을 heterogeneous pre-training과 결합하여 proprioceptive-visual-tactile learning을 통합한 더 강력한 policy를 개발할 수 있다.
- 🔄 다른 접근: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — HPT가 embodiment-specific tokenizer를 사용하는 반면, CrossFormer는 수동 정렬 없이 cross-embodied 학습을 달성한다.
- 🏛 기반 연구: [[papers/1629_Whom_to_Trust_Elective_Learning_for_Distributed_Gaussian_Pro/review]] — 이질적인 사전 훈련 모델을 활용한 고유감각-시각 학습이 분산 GP 회귀의 multi-modal 학습 기반을 제공한다.
- 🔄 다른 접근: [[papers/1302_Adapt3R_Adaptive_3D_Scene_Representation_for_Domain_Transfer/review]] — 이종 사전 훈련 데이터 스케일링과 3D 장면 표현 도메인 전이가 다른 일반화 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1500_OmniVLA_Physically-Grounded_Multimodal_VLA_with_Unified_Mult/review]] — 다중 센서 VLA의 기초가 되는 proprioceptive-visual learning의 heterogeneous 접근
