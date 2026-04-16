---
title: "1419_H3DP_Triply-Hierarchical_Diffusion_Policy_for_Visuomotor_Lea"
authors:
  - "Yiyang Lu"
  - "Yufeng Tian"
  - "Zhecheng Yuan"
  - "Xianbang Wang"
  - "Pu Hua"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "H³DP는 RGB-D 입력의 depth-aware layering, 다중 스케일 visual representation, 그리고 hierarchically conditioned diffusion process를 통합하여 visuomotor policy learning에서 시각 인지와 행동 생성 간의 coupling을 강화하는 방법론이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Vision-Language-Action_Distillation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lu et al._2025_H$^3$DP Triply-Hierarchical Diffusion Policy for Visuomotor Learning.pdf"
---

# H$^3$DP: Triply-Hierarchical Diffusion Policy for Visuomotor Learning

> **저자**: Yiyang Lu, Yufeng Tian, Zhecheng Yuan, Xianbang Wang, Pu Hua, Zhengrong Xue, Huazhe Xu | **날짜**: 2025-05-12 | **URL**: [https://arxiv.org/abs/2505.07819](https://arxiv.org/abs/2505.07819)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of H3DP. H3DP integrates three hierarchical design principles across the*

H³DP는 RGB-D 입력의 depth-aware layering, 다중 스케일 visual representation, 그리고 hierarchically conditioned diffusion process를 통합하여 visuomotor policy learning에서 시각 인지와 행동 생성 간의 coupling을 강화하는 방법론이다.

## Motivation

- **Known**: Diffusion Policy를 포함한 생성 모델 기반 접근법들이 robotic manipulation에서 progress를 이루었으나, 이들은 주로 시각 표현과 행동 생성을 독립적으로 개선하면서 둘 사이의 critical coupling을 간과해왔다.
- **Gap**: 기존 visuomotor policy 학습 방법들은 hierarchical action generation만 모델링하거나, multi-scale visual representation을 채택하면서도 두 구성요소 간의 tight correspondence를 명시적으로 구축하지 못했다.
- **Why**: 인간의 의사결정 과정에서 시각 피질은 계층적으로 정보를 처리하고 motor behavior를 생성하므로, 이러한 계층적 구조를 로봇 정책에 도입하면 spatial reasoning과 cluttered scenarios에서의 성능을 크게 향상시킬 수 있다.
- **Approach**: RGB-D 입력을 depth 값에 따라 여러 레이어로 분해하고, 다중 스케일 visual encoder를 통해 coarse-to-fine 특징을 추출한 후, diffusion process의 각 denoising 단계를 해당 시각 특징 스케일과 정렬시킨다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: H3DP can not only achieve superior performance across 44 tasks on 5 simulation bench-*

- **시뮬레이션 성능**: 5개 벤치마크의 44개 작업에서 baseline 대비 평균 +27.5% 상대 성능 개선 달성
- **실제 로봇 성능**: cluttered 환경의 4개 bimanual 조작 작업에서 Diffusion Policy 대비 +32.3% 성능 향상
- **계층적 설계의 유효성**: depth-aware layering이 foreground-background 분리를 명시적으로 수행하여 occlusion과 distraction 억제

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of H3DP. H3DP integrates three hierarchical design principles across the*

- **Depth-Aware Layering**: Linear-increasing discretization 수식(Eq. 1)을 사용하여 RGB-D 입력을 depth 값에 따라 N개의 레이어로 분할하고, 작업 공간에 더 집중하도록 설계
- **Multi-Scale Visual Representation**: 구체적 방법론은 단락이 끝나지 않아 자세한 내용 미제시되었으나, 다양한 granularity의 특징을 여러 스케일에서 추출하는 구조
- **Hierarchical Action Generation in Diffusion**: Denoising 과정을 여러 단계로 분할하여 coarse visual features는 초기 단계에서 global structure(low-frequency)를 형성하고, fine-grained features는 later steps에서 details(high-frequency)를 정제
- **Semantic Alignment**: Multi-scale 시각 특징과 coarse-to-fine 행동 생성을 diffusion process 내에서 직접 정렬하여 semantically grounded action 생성

## Originality

- 입력, representation, action generation의 세 단계 모두에 걸쳐 계층적 구조를 명시적으로 통합하는 통합적 설계로, 기존 works가 주로 action generation 계층화에만 집중했던 점과 차별화
- Depth-aware layering을 단순 RGB-D concatenation 이상으로 발전시켜 depth 정보를 의도적으로 활용한 foreground-background 분리 메커니즘 도입
- Diffusion model의 inherent low-to-high frequency 복원 속성을 명시적으로 활용하여 다중 스케일 시각 특징과 coarse-to-fine 행동 생성을 diffusion process 내에서 정렬

## Limitation & Further Study

- 논문 본문이 발췌본이므로 Multi-Scale Visual Representation의 구체적 구현 방법이 불완전하게 제시되어 있음
- Depth-aware layering의 discretization 전략이 모든 환경 또는 depth distribution에 최적인지 검증 필요 (Appendix에 일부 비교가 있으나 본문 미포함)
- 실제 로봇 실험이 4개 작업으로 제한적이므로, 다양한 manipulation 시나리오에서의 일반화 가능성에 대한 추가 검증 필요
- 계층화된 diffusion process의 computational overhead와 inference speed에 대한 분석 부재
- 후속 연구: 다른 modality(e.g., tactile feedback, language instructions)와의 통합 가능성 탐색, real-to-sim transfer learning에서의 effectiveness 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 3/5
- Overall: 4/5

**총평**: H³DP는 visuomotor policy learning의 critical coupling 문제를 명확하게 식별하고 human visual cortex의 계층적 처리에서 영감을 받아 입력부터 행동 생성까지 일관된 계층적 구조를 구축한 혁신적 접근법이다. 광범위한 실험을 통해 상당한 성능 개선을 입증했으나, 본문이 발췌본으로 일부 기술적 세부사항이 불명확하고 실제 로봇 실험의 규모가 다소 제한적이라는 점은 개선 여지가 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang/review]] — 둘 다 spatial representation을 VLA에 통합하지만 depth-aware layering vs explicit spatial reasoning이라는 다른 방법론을 사용한다.
- 🏛 기반 연구: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 3D Diffusion Policy의 공간적 이해를 RGB-D 기반 hierarchical conditioning으로 더욱 정교화했다.
- 🔗 후속 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion Transformer Policy를 triply-hierarchical 구조로 확장하여 visuomotor learning을 향상시켰다.
- 🔗 후속 연구: [[papers/1423_Hierarchical_Diffusion_Policy_manipulation_trajectory_genera/review]] — 계층적 diffusion policy에서 depth-aware representation을 추가로 고려한 확장 연구입니다.
- 🔗 후속 연구: [[papers/1423_Hierarchical_Diffusion_Policy_manipulation_trajectory_genera/review]] — H³DP는 계층적 diffusion policy를 삼중 계층으로 더 세분화하여 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — 두 논문 모두 장기간 로봇 조작을 위한 계층적 접근법을 제안하지만 RoboCerebra는 VLM 기반 계획에, H3DP는 diffusion 정책에 중점을 둔다.
- 🔄 다른 접근: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — 역방향 궤적 생성 대신 계층적 diffusion을 통한 다른 궤적 모델링 접근법으로 유사한 문제 해결
- 🔗 후속 연구: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — H³DP의 triply-hierarchical diffusion과 MoDE의 efficient expert routing은 모두 diffusion policy의 복잡성과 효율성을 개선하려는 방향이다.
