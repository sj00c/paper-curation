---
title: "1363_Diffusion_Transformer_Policy"
authors:
  - "Zhi Hou"
  - "Tianyi Zhang"
  - "Yuwen Xiong"
  - "Hengjun Pu"
  - "Chengyang Zhao"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Diffusion Transformer Policy는 큰 멀티모달 diffusion transformer를 사용하여 연속 action sequence를 직접 denoising함으로써, 작은 action head 대신 transformer의 scaling 능력을 활용하는 generalist robot policy이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hou et al._2024_Diffusion Transformer Policy.pdf"
---

# Diffusion Transformer Policy

> **저자**: Zhi Hou, Tianyi Zhang, Yuwen Xiong, Hengjun Pu, Chengyang Zhao, Ronglei Tong, Yu Qiao, Jifeng Dai, Yuntao Chen | **날짜**: 2024-10-21 | **URL**: [https://arxiv.org/abs/2410.15959v4](https://arxiv.org/abs/2410.15959v4)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Illustrations of different robot policy architectures. (a) is the common robot transformer architecture with d*

Diffusion Transformer Policy는 큰 멀티모달 diffusion transformer를 사용하여 연속 action sequence를 직접 denoising함으로써, 작은 action head 대신 transformer의 scaling 능력을 활용하는 generalist robot policy이다.

## Motivation

- **Known**: 최근 large vision-language-action 모델들은 diverse robot dataset으로 pretrain되어 새로운 환경에서 few-shot generalization을 보여주고 있다. 그러나 Robot Transformer, OpenVLA, Octo 등 기존 방식들은 discretized action이나 작은 action head로 개별 action을 예측하여 diverse action space 처리 능력이 제한적이다.
- **Gap**: 기존 diffusion policy 방식(예: Octo)은 작은 MLP network로 single embedding 기반 action을 denoising하고, 사전 fused embedding에 기반하여 action anticipation에 필요한 상세한 역사적 관찰을 충분히 활용하지 못한다. Cross-embodiment dataset의 다양한 camera view와 action space를 처리하는데 한계가 있다.
- **Why**: Generalist robot policy는 diverse한 robot dataset에서 학습하여 새로운 embodiment과 환경으로의 generalization을 가능하게 하며, 이는 로봇 데이터 수집의 시간과 비용을 크게 줄일 수 있다.
- **Approach**: Diffusion Transformer Policy는 in-context conditional diffusion transformer 아키텍처를 통해 action chunks를 직접 denoising한다. 각 historical image observation patch에 조건화되어 visual detail을 보존하면서 transformer의 scalability를 유지하는 causal transformer 기반 구조를 사용한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1.*

- **다중 벤치마크 우수성**: ManiSkill2, Libero, Calvin, SimplerEnv 등 시뮬레이션 벤치마크와 실제 Franka arm에서 OpenVLA, Octo 대비 일관되게 우수한 성능 달성
- **Calvin ABC→D 작업 SOTA**: 단일 third-view camera만으로 completed tasks 평균을 5에서 3.6으로 개선
- **Real-to-Sim 일반화**: SimplerEnv Google Robot 벤치마크에서 강력한 real-to-sim generalization 성능 입증
- **Pretraining 효과**: Calvin에서 success sequence length를 1.2 이상 향상시킴
- **Continuous action 처리**: Discretization 없이 연속 7D end-effector action을 효과적으로 모델링

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Illustrations of different robot policy architectures. (a) is the common robot transformer architecture with d*

- Frozen CLIP으로 언어 instruction tokenization
- DINOv2로 image patch feature 추출 후 end-to-end joint optimization
- Q-Former와 FiLM conditioning으로 instruction context 기반 image feature 선택
- 7D continuous action vector (translation 3D + rotation 3D + gripper 1D)를 zero-padding으로 token dimension에 정렬
- In-context conditional style로 multimodal tokens와 action을 causal transformer로 처리
- Action chunk 단위로 diffusion denoising 수행 (개별 action이 아님)
- Open X-Embodiment Dataset으로 large-scale cross-embodiment pretraining 수행

## Originality

- 기존 Octo의 작은 MLP diffuser 대신 **큰 transformer를 diffuser로 사용**하여 action denoising의 capacity 획기적 증대
- **In-context conditioning 방식** 도입으로 각 historical observation patch에 직접 조건화되어 fused embedding 기반 접근의 한계 극복
- Action chunk 단위 denoising으로 **action sequence의 temporal coherence 향상**
- Continuous action 기반 접근으로 discretization의 내부 편차 문제 해결
- Large-scale cross-embodiment dataset에서의 **transformer scalability 활용** 최적화

## Limitation & Further Study

- Pretrain 단계의 Open X-Embodiment Dataset 접근성과 계산 비용 요구 사항이 높음
- DINOv2는 web data 기반이므로 robot-specific visual feature 학습에 최적화되지 않을 수 있음
- Zero-padding 기반 action representation이 다양한 action space dimension에 효율적인지 불명확
- **후속연구**: 다양한 action type (gripper 비이진화, manipulation-specific action) 처리 확장
- **후속연구**: Real-world deployment에서 computational latency와 실시간 성능 평가 필요
- **후속연구**: Multi-modal diffusion의 computational complexity 최적화 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Diffusion Transformer Policy는 transformer 기반 diffusion 아키텍처로 기존 generalist robot policy의 action space 처리 한계를 효과적으로 극복하며, 여러 벤치마크에서 SOTA 성능과 강력한 generalization을 입증한 의미 있는 기여이다.

## Related Papers

- 🔗 후속 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — 기존 Diffusion Policy의 작은 action head를 큰 transformer로 대체하여 scaling 능력을 향상시킵니다.
- 🔄 다른 접근: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — Diffusion transformer의 효율성을 위한 MoE와 단일 large transformer의 서로 다른 접근법입니다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 오픈소스 generalist robot policy의 기본 구조와 원리를 제공합니다.
- 🔗 후속 연구: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — HybridVLA의 diffusion 기반 action 예측이 Diffusion Transformer Policy의 방법론을 VLM과 통합하여 확장한 형태이다.
- 🔗 후속 연구: [[papers/1419_H3DP_Triply-Hierarchical_Diffusion_Policy_for_Visuomotor_Lea/review]] — Diffusion Transformer Policy를 triply-hierarchical 구조로 확장하여 visuomotor learning을 향상시켰다.
- 🏛 기반 연구: [[papers/1465_ManiFlow_A_General_Robot_Manipulation_Policy_via_Consistency/review]] — diffusion transformer의 기본 아키텍처를 consistency flow training에 적용하는 이론적 토대를 제공한다.
- 🏛 기반 연구: [[papers/1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with/review]] — diffusion transformer의 기본 아키텍처를 navigation diffusion policy에 적용하는 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — Diffusion Transformer Policy와 RDT의 diffusion foundation model은 transformer 구조 활용 방식에서 다른 접근법을 보여준다.
- 🔄 다른 접근: [[papers/1580_Streaming_Flow_Policy_Simplifying_diffusionflow-matching_pol/review]] — Diffusion Transformer Policy가 transformer 기반 diffusion에 중점을 두는 반면, Streaming Flow Policy는 flow-matching의 단순화와 실시간 스트리밍에 초점을 맞춘다.
- 🏛 기반 연구: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — Diffusion Transformer Policy는 VITA가 대안으로 제시하는 기존 diffusion 기반 정책의 기반 연구다.
- 🏛 기반 연구: [[papers/1337_Compose_Your_Policies_Improving_Diffusion-based_or_Flow-base/review]] — Diffusion Transformer Policy의 기본 구조를 여러 정책의 조합으로 확장한 접근방식을 제시합니다.
- 🔗 후속 연구: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — Diffusion Transformer Policy의 기본 구조를 DexVLA가 VLA 프레임워크로 확장하고 embodied curriculum learning과 결합합니다.
- 🔗 후속 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Transformer 정책으로서 diffusion 기반 정책 학습을 확장합니다.
- 🏛 기반 연구: [[papers/1366_Discrete_Diffusion_VLA_Bringing_Discrete_Diffusion_to_Action/review]] — Diffusion Transformer Policy의 기본 아키텍처가 Discrete Diffusion VLA에서 action token 디코딩에 적용되는 transformer-diffusion 결합의 토대를 제공한다.
- 🏛 기반 연구: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — Diffusion Transformer Policy의 기본 아키텍처를 MoE로 확장하여 효율성을 개선한 연구입니다.
