---
title: "1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey"
authors:
  - "Rosa Wolf"
  - "Yitian Shi"
  - "Sheng Liu"
  - "Rania Rayyes"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 로봇 조작(robotic manipulation) 분야에서 diffusion model의 응용을 종합적으로 리뷰하는 첫 번째 survey로, grasp learning, trajectory planning, data augmentation 등의 주요 응용 분야와 학습 프레임워크, 아키텍처를 체계적으로 분류한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_AI_Architectures"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wolf et al._2025_Diffusion Models for Robotic Manipulation A Survey.pdf"
---

# Diffusion Models for Robotic Manipulation: A Survey

> **저자**: Rosa Wolf, Yitian Shi, Sheng Liu, Rania Rayyes | **날짜**: 2025-04-11 | **URL**: [https://arxiv.org/abs/2504.08438](https://arxiv.org/abs/2504.08438)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Illustrations of diffusion (forward) processes on image, trajectories, and grasp poses (Urain et al. (2023)) a*

본 논문은 로봇 조작(robotic manipulation) 분야에서 diffusion model의 응용을 종합적으로 리뷰하는 첫 번째 survey로, grasp learning, trajectory planning, data augmentation 등의 주요 응용 분야와 학습 프레임워크, 아키텍처를 체계적으로 분류한다.

## Motivation

- **Known**: Diffusion model은 image와 video generation에서 우수한 성능을 보였으며, multi-modal distribution을 모델링할 수 있고 고차원 입출력에 강건하다는 장점이 알려져 있다.
- **Gap**: Diffusion model을 로봇 조작에 적용한 연구가 2022년 이후 증가하고 있으나, 이 분야의 체계적인 리뷰와 분류 체계가 부족했다. 또한 느린 sampling 속도 등의 도전 과제가 해결되어야 한다.
- **Why**: 로봇 조작 작업에는 여러 동등한 해법(redundant solutions)이 존재하므로 multi-modal distribution을 정확히 모델링하는 것이 중요하며, 이는 다양한 환경에서 로봇의 일반화 능력과 다용도성을 향상시킨다.
- **Approach**: 본 survey는 diffusion model의 수학적 기초(score-based DM, DDPM 등), 로봇 조작에 사용되는 네트워크 아키텍처, 주요 응용 분야별 방법론, 그리고 벤치마크와 평가 기준을 체계적으로 제시한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Illustrations of diffusion (forward) processes on image, trajectories, and grasp poses (Urain et al. (2023)) a*

- **첫 번째 종합 survey**: 로봇 조작 분야의 diffusion model 관련 연구를 처음으로 체계적으로 정리하고 분류함
- **다중 응용 분야 포괄**: Trajectory generation, robotic grasp synthesis, visual data augmentation의 세 가지 주요 응용을 상세히 설명
- **학습 프레임워크 통합**: Imitation learning과 reinforcement learning과의 결합 방식을 제시
- **실무적 가이드**: 일반적인 아키텍처, 벤치마크, 도전 과제와 장점을 제시하여 실무자와 연구자 모두에게 유용한 참고자료 제공

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Illustrations of diffusion (forward) processes on image, trajectories, and grasp poses (Urain et al. (2023)) a*

- Score-based diffusion model(NCSN)과 noise prediction network(DDPM)의 두 가지 주요 프레임워크에 대한 수학적 기초를 상세히 설명
- Forward diffusion process(데이터를 점진적으로 노이즈화)와 reverse process(노이즈에서 샘플 생성)의 상호관계를 명확히 제시
- Point cloud, natural language 등 다양한 입력 modality를 지원하는 아키텍처 설계 사례 검토
- Hierarchical planning과 skill learning으로의 통합, diffusion-based data augmentation 기법 분석
- DDIM 등 sampling 효율을 개선한 방법들을 포함하여 실시간 예측을 가능하게 하는 최적화 기법 논의

## Originality

- 로봇 조작 분야에 특화된 첫 번째 diffusion model survey로, 기존의 일반적인 생성 모델 리뷰와 차별화됨
- Multi-modal distribution 모델링의 중요성을 로봇 조작의 redundancy 관점에서 명확히 동기付け
- Imitation learning과 reinforcement learning의 통합, 다중 modality 입력 처리 등 로봇 조작에 특화된 기술 관점을 체계적으로 정리
- 실제 구현에서의 도전 과제(sampling 속도, 고차원 데이터 처리)와 해결 방안을 구체적으로 논의

## Limitation & Further Study

- Survey 성격상 개별 방법의 성능 비교 실험(benchmark 결과)이 제한적일 수 있음
- Sampling 속도 개선에 대한 상세한 정량적 분석이 부족할 수 있으므로 실시간 응용의 실현 가능성 평가 필요
- 로봇 조작의 특정 도메인(예: soft manipulation, deformable object handling)에서의 diffusion model 적용에 대한 논의 확장 필요
- 후속 연구: (1) Real-world 적용에서의 실시간 성능 개선, (2) 더 효율적인 아키텍처 개발, (3) Sim-to-real transfer에서 diffusion model의 역할 규명

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 로봇 조작 분야에서 빠르게 성장하는 diffusion model 연구를 처음으로 체계적으로 정리한 가치 있는 survey로, 연구자와 실무자 모두에게 필수적인 참고자료를 제공한다.

## Related Papers

- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy는 로봇 조작에서 diffusion model 적용의 핵심 원리와 방법론을 제시하여 survey의 중요한 기반 연구입니다.
- 🔗 후속 연구: [[papers/1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi/review]] — Consistency Policy는 diffusion model survey에서 다룬 sampling 속도 문제를 consistency model로 해결하는 발전된 접근법입니다.
- 🧪 응용 사례: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 3D Diffusion Policy는 survey에서 제시된 diffusion 방법론을 3D 공간 이해와 결합한 구체적인 적용 사례입니다.
- 🔗 후속 연구: [[papers/1423_Hierarchical_Diffusion_Policy_manipulation_trajectory_genera/review]] — 계층적 diffusion policy라는 구체적 응용사례를 통해 서베이 내용을 확장합니다.
- 🔄 다른 접근: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — 로봇 조작에서 diffusion model과 foundation model의 서로 다른 관점의 종합적 리뷰를 제공합니다.
- 🏛 기반 연구: [[papers/1405_Generative_Artificial_Intelligence_in_Robotic_Manipulation_A/review]] — 로봇 조작에서 diffusion model 사용에 대한 기초적인 서베이를 제공하여 생성형 AI 전반의 이해를 돕는다.
- 🔄 다른 접근: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — 둘 다 로봇 조작을 위한 diffusion 기반 정책이지만 VITA는 flow matching에, 기존 연구들은 일반적인 diffusion에 집중합니다.
- 🔗 후속 연구: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — 로봇 조작용 diffusion model 서베이는 Diffusion-VLA의 견고한 행동 생성을 위한 diffusion 활용에 포괄적인 배경을 제공한다.
- 🏛 기반 연구: [[papers/1299_A_Survey_of_Robotic_Navigation_and_Manipulation_with_Physics/review]] — 로봇 조작을 위한 확산 모델 서베이가 물리 시뮬레이터와 sim-to-real 전이의 이론적 배경을 제공합니다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — 로봇 조작을 위한 diffusion 모델들에 대한 포괄적인 조사와 이론적 기반을 제공합니다.
