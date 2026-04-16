---
title: "1712_The_Role_of_Domain_Randomization_in_Training_Diffusion_Polic"
authors:
  - "Oleg Kaidanov"
  - "Firas Al-Hafez"
  - "Yusuf Suvari"
  - "Boris Belousov"
  - "Jan Peters"
date: "2024.11"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Humanoid 로봇의 전신 제어를 위해 Diffusion Policies를 훈련할 때 Domain Randomization의 역할을 조사하며, 조작 작업보다 보행 작업이 훨씬 더 큰 규모와 다양성의 데이터셋을 요구함을 보여준다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kaidanov et al._2024_The Role of Domain Randomization in Training Diffusion Policies for Whole-Body Humanoid Control.pdf"
---

# The Role of Domain Randomization in Training Diffusion Policies for Whole-Body Humanoid Control

> **저자**: Oleg Kaidanov, Firas Al-Hafez, Yusuf Suvari, Boris Belousov, Jan Peters | **날짜**: 2024-11-02 | **URL**: [https://arxiv.org/abs/2411.01349](https://arxiv.org/abs/2411.01349)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Evaluation of Diffusion Policies in a non-randomized target environment. Top: A plot dis-*

본 논문은 Humanoid 로봇의 전신 제어를 위해 Diffusion Policies를 훈련할 때 Domain Randomization의 역할을 조사하며, 조작 작업보다 보행 작업이 훨씬 더 큰 규모와 다양성의 데이터셋을 요구함을 보여준다.

## Motivation

- **Known**: Diffusion Policies는 로봇 조작에서 인상적인 결과를 보였으며, AMP와 같은 모방학습 방법이 humanoid 제어에 효과적임이 알려져 있다. Domain Randomization은 시뮬레이션-실제 간극 해결에 중요한 역할을 한다.
- **Gap**: Diffusion Policies의 보행 및 전신 humanoid 제어 적용성은 충분히 탐색되지 않았으며, 특히 데이터셋 특성(크기, 다양성)이 DP 훈련에 미치는 영향에 대한 체계적인 ablation 연구가 부족하다.
- **Why**: Humanoid 로봇이 인간 환경을 위한 이상적인 구현체로 주목받고 있으며, 풍부한 모션 캡처 데이터를 활용할 수 있으나 효과적인 정책 학습 방법이 필요하다. 데이터셋 특성의 영향을 이해하면 더 효율적인 humanoid 제어 정책 개발이 가능하다.
- **Approach**: IsaacGym 시뮬레이션 환경에서 다양한 Domain Randomization 조건 하에 AMP 에이전트를 훈련하여 합성 시연을 생성하고, 서로 다른 크기와 다양성의 데이터셋으로 훈련된 Diffusion Policies의 성능을 비교한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Evaluation of Diffusion Policies in a non-randomized target environment. Top: A plot dis-*

- **Domain Randomization의 필수성**: DR 없이는 데이터셋 규모가 크더라도 비무작위화 환경에 일반화하지 못하며, DR의 다양한 유형(perturbations, dynamic variations, terrain changes)의 효과를 입증
- **데이터셋 크기-다양성 상호작용**: 조작 작업과 달리 전신 보행 제어는 안정적 성능을 위해 매우 큰 규모와 높은 다양성의 데이터셋이 필요함을 정량적으로 증명
- **Humanoid 제어의 특수성**: 높은 자유도와 균형 요구사항으로 인해 humanoid 보행이 조작 작업보다 데이터 효율성이 현저히 낮음을 처음 체계적으로 분석

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Proposed method. First, a robust and stable RL policy is trained using AMP under ex-*

- AMP 알고리즘을 사용하여 AMASS 모션 캡처 데이터(10개 시퀀스)와 목표 조건부 RL을 결합한 강건한 RL 정책 훈련
- 8가지 서로 다른 환경 설정과 3가지 데이터셋 크기로 총 24개의 구별된 데이터셋 생성
- 각 데이터셋으로 개별 및 집합적으로 Diffusion Policies 훈련
- 비무작위화 평탄 표면과 무작위화된 복잡한 지형의 두 가지 평가 설정으로 성능 검증
- 정규화 보상(Table 1)과 포괄적 Domain Randomization(Table 2) 적용

## Originality

- **첫 ablation 연구**: Humanoid 제어를 위한 데이터셋 생성 시 Domain Randomization의 영향에 대한 첫 체계적인 ablation 연구 제시
- **다층적 DR 분석**: Perturbations, dynamic variations, terrain changes 등 다양한 DR 유형과 novel approach를 포함한 포괄적 분석
- **조작-보행 성능 격차 정량화**: 동일 프레임워크 내에서 조작 작업과 전신 보행 제어의 데이터 요구사항 차이를 직접 비교
- **실제 로봇 기반 데이터**: AMASS 모션 캡처 데이터와 Unitree H1 humanoid를 기반으로 현실성 높은 연구 수행

## Limitation & Further Study

- **시뮬레이션 환경 국한**: IsaacGym 시뮬레이션만 사용하였으며 실제 humanoid 로봇에서의 검증이 부재하므로 sim-to-real 성능 격차 미파악
- **제한된 작업 범위**: 보행과 관련된 기본 작업(방향 이동, 회전)만 평가하였으며 더 복잡한 조작과 보행 통합 작업 미포함
- **계산 비용 분석 부재**: 다양한 DR 설정과 데이터셋 크기에 대한 훈련 시간 및 계산 복잡도 비교 분석 미제시
- **후속 연구**: 실제 humanoid 로봇에서의 sim-to-real 전이 검증, 더 복잡한 다중 작업 환경에서의 성능 평가, 온라인 학습과 결합한 적응적 정책 개선 방법 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 humanoid 제어를 위한 Diffusion Policies의 데이터 요구사항에 대한 첫 체계적 ablation 연구로서, Domain Randomization의 중요성을 명확히 입증하고 조작-보행 작업 간의 근본적 차이를 정량화한다. 다만 실제 로봇 검증과 복잡한 작업으로의 확장이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — SCHUR 프레임워크가 제공하는 대규모 데이터셋이 Diffusion Policies 훈련의 데이터 요구사항 문제를 해결합니다.
- 🔄 다른 접근: [[papers/1791_Advancing_Humanoid_Locomotion_Mastering_Challenging_Terrains/review]] — 복잡한 지형에서의 humanoid 제어를 위해 Diffusion과 World Model Learning이라는 서로 다른 접근법을 사용합니다.
- 🏛 기반 연구: [[papers/1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control/review]] — Diffusion Policies를 캐릭터 제어에 적용한 기반 연구를 휴머노이드 전신 제어로 확장하여 Domain Randomization의 중요성을 체계적으로 분석했다.
- 🔄 다른 접근: [[papers/1943_GBC_Generalized_Behavior-Cloning_Framework_for_Whole-Body_Hu/review]] — 전신 휴머노이드 제어를 위해 서로 다른 접근(Diffusion Policies vs Generalized Behavior-Cloning)을 통해 데이터 요구사항과 성능을 비교 분석한다.
- 🏛 기반 연구: [[papers/1926_FastTD3_Simple_Fast_and_Capable_Reinforcement_Learning_for_H/review]] — 강화학습에서의 효율적 알고리즘 개발 개념을 Diffusion Policies라는 새로운 패러다임에서 Domain Randomization의 역할로 확장하여 분석했다.
- 🏛 기반 연구: [[papers/1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control/review]] — 전신 제어를 위한 Diffusion Policies의 역할을 캐릭터 제어라는 특정 도메인으로 확장하여 Transformer 기반 조건부 모델을 개발했다.
- 🏛 기반 연구: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — 대규모 Humanoid-Union 데이터셋이 Diffusion Policies 훈련에 필요한 데이터 규모 문제를 해결합니다.
- 🔄 다른 접근: [[papers/1791_Advancing_Humanoid_Locomotion_Mastering_Challenging_Terrains/review]] — 복잡한 지형에서의 humanoid 제어를 위해 DWL은 denoising world model을, diffusion policies는 domain randomization을 활용합니다.
