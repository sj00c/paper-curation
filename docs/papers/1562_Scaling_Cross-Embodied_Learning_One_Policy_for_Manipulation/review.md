---
title: "1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation"
authors:
  - "Ria Doshi"
  - "Homer Walke"
  - "Oier Mees"
  - "Sudeep Dasari"
  - "Sergey Levine"
date: "2024.08"
doi: ""
arxiv: ""
score: 4.0
essence: "CrossFormer는 20개의 서로 다른 로봇 embodiment에서 900K 궤적으로 학습된 단일 transformer 기반 정책으로, 관찰 및 행동 공간의 수동 정렬 없이 조작, 네비게이션, 보행, 항공 로봇을 모두 제어할 수 있다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Broad_Task_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Doshi et al._2024_Scaling Cross-Embodied Learning One Policy for Manipulation, Navigation, Locomotion and Aviation.pdf"
---

# Scaling Cross-Embodied Learning: One Policy for Manipulation, Navigation, Locomotion and Aviation

> **저자**: Ria Doshi, Homer Walke, Oier Mees, Sudeep Dasari, Sergey Levine | **날짜**: 2024-08-21 | **URL**: [https://arxiv.org/abs/2408.11812](https://arxiv.org/abs/2408.11812)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We introduce CrossFormer, a transformer-based policy trained on 900K trajectories of diverse,*

CrossFormer는 20개의 서로 다른 로봇 embodiment에서 900K 궤적으로 학습된 단일 transformer 기반 정책으로, 관찰 및 행동 공간의 수동 정렬 없이 조작, 네비게이션, 보행, 항공 로봇을 모두 제어할 수 있다.

## Motivation

- **Known**: 로봇 학습은 각 플랫폼별 제한된 데이터로 인해 일반화가 어렵지만, 다중 로봇 데이터로 학습하면 더 넓은 데이터셋을 활용할 수 있다. 기존 연구는 동일한 관찰/행동 공간을 가진 로봇들에 제한되었거나 수동 정렬이 필요했다.
- **Gap**: 서로 다른 센서(카메라, proprioceptive), 액추에이터(2-1400 DoF), 제어 주파수(5-20Hz)를 가진 로봇들을 자동으로 처리하면서 동시에 조작, 네비게이션, 보행, 항공 등 극도로 다양한 embodiment을 제어하는 단일 정책은 아직 없었다.
- **Why**: cross-embodied 학습은 데이터 효율성을 크게 향상시키고, 각 로봇별 맞춤 정책 설계 비용을 줄이며, 일반화된 로봇 정책의 실현 가능성을 보여준다.
- **Approach**: Transformer 기반 정책으로 가변 길이 관찰을 토큰 시퀀스로 직렬화하고, 행동 타입별 readout 토큰과 action-space specific head를 사용하여 임의 차원의 행동을 예측한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: Real Evaluation. We compare CrossFormer to the same architecture trained on just the*

- **900K 궤적, 20개 embodiment 규모**: 조작(단일/이중 팔), 바퀴 로봇, quadcopter, quadruped을 포함하는 가장 크고 다양한 cross-embodied 데이터셋으로 학습
- **관찰/행동 공간 자동 처리**: 수동 정렬 없이 2-1400 DoF의 행동, 다양한 센서 조합, 5-20Hz 제어 주파수 차이를 자동 처리
- **specialist 정책 수준 성능**: 각 embodiment별 맞춤 정책과 성능을 일치시키면서 cross-embodiment 학습 기존 최고 성능 초과
- **실제 로봇 검증**: 광범위한 실제 환경 실험으로 방법의 실용성 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Policy architecture. Our architecture enables cross-embodied policy learning through*

- 모든 관찰(다중 카메라, proprioceptive 센서)을 토큰으로 변환하여 flat sequence로 순서화
- 각 행동 타입(manipulation, navigation, locomotion 등)마다 action readout 토큰을 입력 시퀀스에 삽입
- 대응하는 출력 임베딩을 행동-공간 특화 head로 전달하여 올바른 차원의 벡터 생성
- Action chunking을 사용하여 시간적 일관성 개선
- Language instruction 또는 goal image를 통한 flexible task specification 지원
- OXE dataset의 900K 부분 궤적과 GNM navigation, DROID manipulation, Go1 quadruped, ALOHA bimanual 데이터로 co-training

## Originality

- 최초로 4개 이상의 서로 다른 행동 공간(단일 팔, 이중 팔, 지상 네비게이션, 보행)을 수동 정렬 없이 공동 학습
- 관찰 공간 제약 없이 임의 개수의 카메라와 proprioceptive 센서를 자동 처리하는 구조
- Readout token 기반의 다중 행동 타입 동시 예측 메커니즘으로 기존 방식의 한계 극복
- 20개 embodiment의 극도로 다양한 조합에서 negative transfer 없이 specialist 성능 달성

## Limitation & Further Study

- 학습 데이터 분포에 대한 분석이 명확하지 않음 (각 embodiment별 궤적 개수 분포 미상)
- Fine-tuning 필요성에 대한 분석이 부족 (zero-shot vs. few-shot 성능 비교 부재)
- Failure case 분석이 제시되지 않음 (어떤 embodiment/task 조합에서 어려움을 겪는지 미상)
- 후속 연구: 더 이질적인 embodiment (예: 유연한 로봇, 다리 개수 다양성) 포함; embodiment 인코딩과 데이터 불균형의 영향 연구; 강화학습을 통한 on-robot improvement 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CrossFormer는 cross-embodied 로봇 학습에서 획기적인 진전을 이루었으며, 실용적인 문제(센서/액추에이터 이질성)를 우아하게 해결하고 광범위한 실제 실험으로 검증된 강력한 작업이다.

## Related Papers

- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — CrossFormer의 cross-embodied 학습은 Open X-Embodiment가 제공하는 다양한 로봇 데이터셋을 활용한다.
- 🔄 다른 접근: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — MetaMorph는 CrossFormer와 유사하게 다양한 형태의 로봇을 제어하지만 transformer 기반 universal controller에 집중한다.
- 🏛 기반 연구: [[papers/1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver/review]] — All Robots in One은 CrossFormer가 달성하려는 통합된 다중 embodiment 제어를 위한 표준화된 데이터셋을 제공한다.
- 🏛 기반 연구: [[papers/1346_Cross-Platform_Scaling_of_Vision-Language-Action_Models_from/review]] — Cross-Platform Scaling 연구는 CrossFormer의 다중 embodiment 학습이 가능한 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1447_Latent_Action_Diffusion_for_Cross-Embodiment_Manipulation/review]] — cross-embodiment manipulation의 이론적 기반이 CrossFormer의 다중 로봇 제어에 적용된다.
- 🔄 다른 접근: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — HPT가 embodiment-specific tokenizer를 사용하는 반면, CrossFormer는 수동 정렬 없이 cross-embodied 학습을 달성한다.
- 🔗 후속 연구: [[papers/1628_WholeBodyVLA_Towards_Unified_Latent_VLA_for_Whole-Body_Loco-/review]] — WholeBodyVLA의 whole-body locomotion 개념을 확장하여 조작, 네비게이션, 보행, 항공까지 포괄하는 더 광범위한 embodiment를 다룬다.
- 🧪 응용 사례: [[papers/1401_GauDP_Reinventing_Multi-Agent_Collaboration_through_Gaussian/review]] — Cross-Embodied Learning의 정책 공유 방법이 GauDP의 공유 3D Gaussian 표현을 실제 다중 로봇 시스템에 적용하는 방법을 제시합니다.
- 🔄 다른 접근: [[papers/1424_HiMoE-VLA_Hierarchical_Mixture-of-Experts_for_Generalist_Vis/review]] — Cross-embodied learning에서 단일 정책과 다르게 MoE로 다양한 embodiment를 명시적으로 처리한다.
- 🔄 다른 접근: [[papers/1447_Latent_Action_Diffusion_for_Cross-Embodiment_Manipulation/review]] — 둘 다 cross-embodiment 학습이지만 Latent Action Diffusion은 latent space에, Scaling 논문은 정책 통합에 집중한다.
- 🔄 다른 접근: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — Cross-embodiment 학습에서 MetaMorph는 모듈식 로봇에, 다른 연구는 일반적 조작에 초점을 맞춘 서로 다른 접근법이다.
- 🔗 후속 연구: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo의 cross-embodiment learning을 더욱 확장하여 single policy로 다양한 manipulation 작업을 처리하는 방법을 제시한다.
- 🧪 응용 사례: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Cross-embodied learning 정책이 Open X-Embodiment 데이터셋의 다양한 로봇 플랫폼 데이터를 실제 활용하는 구체적인 응용 사례다.
- ⚖️ 반론/비판: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — CrossFormer가 embodiment 간 수동 정렬 없이 학습하는 반면, HPT는 embodiment-specific tokenizer를 통한 명시적 구조화를 추구한다.
- 🔄 다른 접근: [[papers/1546_Robot_Utility_Models_General_Policies_for_Zero-Shot_Deployme/review]] — 새로운 환경에서의 로봇 배포를 RUM은 zero-shot으로, Scaling Cross-Embodied Learning은 하나의 정책으로 해결하는 다른 접근법이다.
- 🔄 다른 접근: [[papers/1633_X-VLA_Soft-Prompted_Transformer_as_Scalable_Cross-Embodiment/review]] — cross-embodiment learning에서 서로 다른 접근법 - soft prompt vs unified policy입니다.
- 🔄 다른 접근: [[papers/1302_Adapt3R_Adaptive_3D_Scene_Representation_for_Domain_Transfer/review]] — 둘 다 cross-embodiment learning을 다루지만 Adapt3R는 3D scene representation에, Scaling Cross-Embodied는 unified policy에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb/review]] — Cross-Embodied Learning의 단일 정책 조작은 Being-H0.5의 30개 로봇 플랫폼 일반화에 핵심 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1378_Embodied_Navigation_Foundation_Model/review]] — cross-embodied learning의 통합 정책 개념이 navigation foundation model의 핵심 설계 기반
- 🧪 응용 사례: [[papers/1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver/review]] — ARIO의 통합 데이터 표준이 cross-embodied learning 연구에서 실제로 활용될 수 있는 데이터 기반을 제공합니다.
