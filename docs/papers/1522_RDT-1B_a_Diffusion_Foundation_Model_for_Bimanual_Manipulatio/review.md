---
title: "1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio"
authors:
  - "Songming Liu"
  - "Lingxuan Wu"
  - "Bangguo Li"
  - "Hengkai Tan"
  - "Huayu Chen"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "bimanual manipulation을 위한 1.2B 파라미터 규모의 diffusion foundation model인 RDT를 제시하며, 다중 로봇 데이터셋 사전학습과 physically interpretable unified action space를 통해 높은 일반화 성능을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Dexterous_Spatial_Grasping"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2024_RDT-1B a Diffusion Foundation Model for Bimanual Manipulation.pdf"
---

# RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation

> **저자**: Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, Jun Zhu | **날짜**: 2024-10-10 | **URL**: [https://arxiv.org/abs/2410.07864](https://arxiv.org/abs/2410.07864)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of Robotics Diffusion Transformer with 1B-Parameters (RDT-1B), a*

bimanual manipulation을 위한 1.2B 파라미터 규모의 diffusion foundation model인 RDT를 제시하며, 다중 로봇 데이터셋 사전학습과 physically interpretable unified action space를 통해 높은 일반화 성능을 달성한다.

## Motivation

- **Known**: bimanual manipulation은 로봇 응용에서 필수적이지만 두 팔의 조정 복잡성과 데이터 부족으로 인해 어렵다. 최근 unimanual manipulation을 위한 foundation model 개발이 진행 중이다.
- **Gap**: bimanual manipulation의 multi-modal action distribution을 효과적으로 표현하면서 동시에 heterogeneous multi-modal input의 scalability를 확보해야 한다. 또한 서로 다른 로봇의 action space variation으로 인한 negative transfer 문제가 해결되지 않았다.
- **Why**: bimanual manipulation foundation model은 복잡한 실제 작업에 대한 일반화 가능성을 제공하며, 데이터 부족과 아키텍처 한계를 극복하는 것이 로봇 자동화의 실용적 응용에 중요하다.
- **Approach**: diffusion transformer를 backbone으로 하여 multi-modality를 표현하고, physically interpretable unified action space를 도입하여 서로 다른 로봇의 action representation을 통합한다. 46개 데이터셋으로 사전학습 후 6K+ 에피소드의 bimanual 데이터로 fine-tuning한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of Robotics Diffusion Transformer with 1B-Parameters (RDT-1B), a*

- **Multi-modal Action 표현**: diffusion model의 capacity를 활용하여 bimanual manipulation의 복잡한 action distribution을 효과적으로 모델링
- **확장성과 정확성**: Transformer backbone과 MLP decoding, 개선된 normalization을 통해 high-frequency robotic data의 비선형 동역학을 포착
- **데이터 이질성 해결**: Physically interpretable unified action space로 다양한 로봇의 action을 통합하면서 물리적 의미 보존
- **대규모 사전학습**: 1.2B 파라미터의 최대 규모 diffusion-based robotic manipulation model로 3배 이상의 데이터 증폭
- **우수한 성능**: 56% 성공률 개선, zero-shot 일반화, 1~5 shot few-shot learning, language instruction 이해 능력 입증

## How

![Figure 3](figures/fig3.webp)

*Figure 3: RDT framework. Heterogeneous action spaces of various robots are embedded into a*

- Diffusion Transformer (DiT) backbone 기반으로 multi-modal input (text, vision, action)의 이질성 제거
- Robotic data의 특성 (temporal-spatial discontinuity, high-frequency changes, unstable numerical range)에 맞춘 개선: MLP decoding, improved normalization, alternate condition injection
- Physically interpretable unified action space 설계로 gripper arm을 가진 다양한 로봇의 action representation 통합
- Multi-robot 데이터셋 (46개, ~1M episodes) 활용 사전학습으로 transferable physical knowledge 학습
- ALOHA dual-arm robot 기반 자체 수집 bimanual dataset (6K+ episodes)으로 target-robot fine-tuning
- Language-conditioned visuomotor policy로 T5와 SigLIP 활용한 instruction following 구현
- Diffusion model의 iterative denoising 프로세스를 통한 순차적 action 생성

## Originality

- Bimanual manipulation을 위한 최초의 diffusion foundation model로, multi-modal action distribution을 명시적으로 다루는 새로운 접근
- Physically interpretable unified action space라는 novel 개념으로 heterogeneous robot data의 negative transfer 문제 근본 해결
- Robotic data의 고유한 특성 (nonlinearity, high-frequency, numerical instability)을 반영한 DiT 구조의 맞춤형 개선
- 3배 이상 데이터 증폭을 통한 cross-robot pretraining 전략으로 data scarcity 문제의 실질적 해결

## Limitation & Further Study

- 평가가 ALOHA dual-arm robot에 한정되어 있으며, 다른 bimanual 로봇 플랫폼에서의 성능 일반화 검증 필요
- Physically interpretable unified action space의 설계 원리와 다른 gripper arm 로봇으로의 확장성에 대한 더 자세한 분석 부족
- 1~5 shot few-shot learning의 성능이 아직 완벽하지 않으므로, 극단적으로 적은 데이터 상황에서의 개선 필요
- Fine-tuning dataset의 다양성 (task, object, environment)이 제한적일 수 있으므로, 더 광범위한 bimanual task 커버리지 확대 필요
- 후속 연구로 non-gripper 조작 (dexterous hand)이나 mobile manipulation 등 다양한 로봇 형태로의 확장 가능성 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RDT-1B는 bimanual manipulation을 위한 diffusion foundation model의 획기적 사례로, physically interpretable unified action space 개념과 맞춤형 architecture 설계를 통해 multi-modality와 data heterogeneity 문제를 효과적으로 해결하였으며, 대규모 사전학습과 강력한 실험 결과로 로봇 자동화의 실질적 진전을 보여준다.

## Related Papers

- 🔗 후속 연구: [[papers/1354_Dex1B_Learning_with_1B_Demonstrations_for_Dexterous_Manipula/review]] — RDT-1B의 bimanual manipulation diffusion 접근법이 Dex1B의 dexterous manipulation을 양손 조작으로 확장한 발전된 형태다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy의 visuomotor learning 방법론이 RDT-1B의 bimanual diffusion foundation model의 이론적 기반이다.
- 🔄 다른 접근: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion Transformer Policy와 RDT의 diffusion foundation model은 transformer 구조 활용 방식에서 다른 접근법을 보여준다.
- 🏛 기반 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 대규모 실제 로봇 데이터 학습 방법론이 RDT-1B의 bimanual manipulation foundation model 개발의 기반이 된다.
- 🔗 후속 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — 인간 비디오로 사전학습한 world model을 RDT-1B의 diffusion 기반 bimanual policy와 결합하면 더 효과적인 양팔 조작 학습이 가능하다.
- 🏛 기반 연구: [[papers/1450_Learning_Fine-Grained_Bimanual_Manipulation_with_Low-Cost_Ha/review]] — RDT의 bimanual manipulation을 위한 기본적인 fine-grained bimanual control과 low-cost hardware 활용 방법을 제공한다.
- 🧪 응용 사례: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — RDT의 bimanual manipulation 능력을 BEHAVIOR-1K의 다양한 human-centered embodied tasks에서 평가하고 적용할 수 있다.
- 🔄 다른 접근: [[papers/1450_Learning_Fine-Grained_Bimanual_Manipulation_with_Low-Cost_Ha/review]] — 둘 다 bimanual manipulation을 다루지만 저비용 하드웨어와 diffusion foundation model의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — RDT-1B는 RVT-2와 유사한 정밀 조작 작업을 위해 diffusion 기반 접근법을 사용하는 대안적 방법론이다.
- 🏛 기반 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — 인간 비디오로 사전학습한 world model이 RDT-1B와 같은 diffusion 기반 조작 정책의 효율적인 학습에 기반 지식을 제공한다.
- 🔗 후속 연구: [[papers/1289_3D_FlowMatch_Actor_Unified_3D_Policy_for_Single-_and_Dual-Ar/review]] — RDT-1B의 bimanual manipulation을 위한 diffusion 기반 모델을 flow matching으로 개선하고 단일/양팔 통합 접근법으로 발전시킨 연구입니다.
- 🔗 후속 연구: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — DexVLA의 diffusion action expert와 RDT-1B의 diffusion foundation model은 양손 조작에서 diffusion 기반 정책의 발전을 보여준다.
- 🔄 다른 접근: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — diffusion 기반 bimanual manipulation과 VLA 프레임워크 기반 dexterous grasping은 서로 다른 접근법으로 복잡한 로봇 조작을 해결한다.
