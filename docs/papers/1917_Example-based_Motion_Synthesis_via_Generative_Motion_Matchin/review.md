---
title: "1917_Example-based_Motion_Synthesis_via_Generative_Motion_Matchin"
authors:
  - "Weiyu Li"
  - "Xuelin Chen"
  - "Peizhuo Li"
  - "Olga Sorkine-Hornung"
  - "Baoquan Chen"
date: "2023.06"
doi: ""
arxiv: ""
score: 4.0
essence: "GenMM은 단일 또는 소수의 예제 모션으로부터 다양한 모션을 생성하는 학습 불필요한 생성 모델로, Motion Matching의 품질을 유지하면서 Bidirectional similarity를 생성 비용 함수로 활용하여 다단계 프레임워크로 점진적으로 모션을 정제한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Text-Conditioned_Motion_Generation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2023_Example-based Motion Synthesis via Generative Motion Matching.pdf"
---

# Example-based Motion Synthesis via Generative Motion Matching

> **저자**: Weiyu Li, Xuelin Chen, Peizhuo Li, Olga Sorkine-Hornung, Baoquan Chen | **날짜**: 2023-06-01 | **URL**: [https://arxiv.org/abs/2306.00378](https://arxiv.org/abs/2306.00378)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. Multi-stage motion synthesis. Starting from the coarsest stage, the generative motion matching at each stage 𝑠ta*

GenMM은 단일 또는 소수의 예제 모션으로부터 다양한 모션을 생성하는 학습 불필요한 생성 모델로, Motion Matching의 품질을 유지하면서 Bidirectional similarity를 생성 비용 함수로 활용하여 다단계 프레임워크로 점진적으로 모션을 정제한다.

## Motivation

- **Known**: Motion Matching은 대규모 모션 데이터베이스를 사용하여 고품질의 자연스러운 캐릭터 애니메이션을 생성하는 산업 표준 방식이며, 최근 deep learning 기반 방법들은 다양한 모션을 생성하지만 긴 훈련 시간, visual artifacts, 복잡한 스켈레톤에 대한 확장성 부족 문제가 있다.
- **Gap**: 기존 data-driven 모션 생성 방법들은 대규모 데이터셋과 오래된 훈련 시간을 요구하며 복잡한 스켈레톤 구조에서 실패하는 반면, 소수 예제로부터 고품질 다양한 모션을 빠르게 생성할 수 있는 방법이 부족하다.
- **Why**: 모션 캡처 데이터 수집은 비용이 높고 스켈레톤 구조의 다양성이 제한되어 있으므로, 제한된 예제로부터 효과적으로 모션을 생성할 수 있는 방법이 애니메이션 제작에서 실용적으로 중요하다.
- **Approach**: Motion Matching의 nearest neighbor 개념을 재해석하여 bidirectional visual similarity를 생성 비용 함수로 사용하고, 다단계 프레임워크에서 초기 랜덤 추측을 예제 모션 패치로 점진적으로 정제하며, 가장 낮은 해상도 단계에 노이즈를 입력하여 생성 다양성을 확보한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Our generative framework enables a variety of example-based motion synthesis tasks, that usually require long of*

- **훈련 불필요한 고속 생성**: 사전 훈련 없이 단 몇 분의 1초 내에 고품질 모션 생성 가능
- **Motion Matching 품질 유지**: Motion Matching의 높은 품질과 충실도를 그대로 상속하면서 생성 능력 추가
- **복잡한 스켈레톤 확장성**: 433개 관절을 가진 매우 복잡한 스켈레톤 구조에서도 안정적으로 작동
- **다양한 응용 시나리오**: Motion completion, key frame-guided generation, infinite looping, motion reassembly 등 기본 Motion Matching으로는 불가능한 작업 수행
- **다중 예제 지원 용이성**: 여러 모션 예제 입력을 자연스럽게 확장 가능

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Multi-stage motion synthesis. Starting from the coarsest stage, the generative motion matching at each stage 𝑠ta*

- Skeleton-aware motion patch extraction으로 복잡한 스켈레톤 구조를 효율적으로 처리
- Bidirectional similarity를 비용 함수로 사용하여 예제의 모든 모션 패치가 합성에 포함되고, 합성 결과가 예제의 패치 분포를 따르도록 강제
- Multi-stage framework에서 coarsest stage부터 시작하여 노이즈 입력으로 초기 다양한 후보 생성
- 각 단계에서 upsampling된 이전 단계의 결과를 초기 추측으로 사용하여 점진적으로 모션 정제
- Generative matching and blending을 통해 motion patch를 적절히 선택 및 블렌딩

## Originality

- Motion Matching을 생성 모델로 재해석한 새로운 관점: 전통적인 nearest neighbor 기반 방식을 bidirectional similarity를 통해 생성 모델로 변환
- Image synthesis의 patch-based generative 개념 (Granot et al. 2022)을 모션 합성에 최초로 적용
- 다단계 프레임워크와 노이즈 기반 초기화를 통한 생성 다양성 확보 전략
- Skeleton-aware patch 추출로 복잡한 스켈레톤 구조 처리의 새로운 솔루션 제시

## Limitation & Further Study

- 예제 모션의 품질이 생성 결과의 상한선을 결정하므로, 저품질 예제로부터는 고품질 모션 생성 불가
- 단일 또는 소수 예제로부터 생성하기 때문에 매우 다양한 모션 스타일 학습의 한계
- Bidirectional similarity 계산의 계산 복잡성이 예제 길이와 생성 길이의 증가에 따라 증가할 가능성
- Motion completion이나 keyframe-guided generation 같은 조건부 생성 작업의 추가 제약 조건 처리 메커니즘의 확장 방향 제시 필요
- 다양한 모션 도메인(보행, 춤, 격투 등)에 대한 광범위한 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GenMM은 Motion Matching의 우수한 품질을 유지하면서 학습 불필요한 생성 모델을 구현한 창의적인 접근법으로, 산업 실무에서 즉시 적용 가능한 실용성과 복잡한 스켈레톤에 대한 강력한 확장성을 제공하는 매우 가치 있는 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/2119_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_G/review]] — 예제 기반 모션 합성과 유연한 관절 제어는 모두 모션 생성에서 세밀한 제어를 제공하지만 접근법이 다르다.
- 🔗 후속 연구: [[papers/1930_Flexible_Motion_In-betweening_with_Diffusion_Models/review]] — 확산 모델 기반 유연한 모션 인터폴레이션이 예제 기반 모션 합성의 확장된 형태이다.
- 🏛 기반 연구: [[papers/1816_Benchmarking_Humanoid_Imitation_Learning_with_Motion_Difficu/review]] — 모션 난이도 벤치마킹이 예제 기반 모션 합성의 품질 평가 기반을 제공한다.
- 🏛 기반 연구: [[papers/1817_Benchmarking_Potential_Based_Rewards_for_Learning_Humanoid_L/review]] — GenMM의 Bidirectional similarity 기반 생성 비용 함수가 potential based rewards 설계에 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/2158_Track_Any_Motions_under_Any_Disturbances/review]] — GenMM의 예제 기반 모션 생성을 외란 하에서도 robust하게 추적할 수 있도록 Track Any Motions 프레임워크로 확장할 수 있다.
- 🏛 기반 연구: [[papers/1917_Example-based_Motion_Synthesis_via_Generative_Motion_Matchin/review]] — Motion Matching의 고품질 모션 생성 기술이 GenMM의 양방향 유사성 기반 생성 비용 함수 설계를 위한 기본적인 방법론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/2146_TEDi_Temporally-Entangled_Diffusion_for_Long-Term_Motion_Syn/review]] — TEDi의 장기간 모션 합성을 위한 temporally-entangled diffusion이 GenMM의 점진적 모션 정제 프레임워크를 시간적으로 확장할 수 있는 방향을 제시한다.
- 🏛 기반 연구: [[papers/1624_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_A/review]] — Generative motion synthesis 방법론을 interactive avatar control에 적용한 기반 연구
- 🏛 기반 연구: [[papers/1863_DemoHLM_From_One_Demonstration_to_Generalizable_Humanoid_Loc/review]] — 생성적 모션 매칭을 통한 예시 기반 동작 합성이 DemoHLM의 단일 시연으로부터 합성 데이터 생성에 필요한 동작 생성 기법을 제공한다.
- 🔄 다른 접근: [[papers/1930_Flexible_Motion_In-betweening_with_Diffusion_Models/review]] — 둘 다 제약 조건을 가진 모션 생성을 다루지만 CondMDI는 diffusion 기반을, GenMM은 Motion Matching 기반 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1989_Human-Humanoid_Robots_Cross-Embodiment_Behavior-Skill_Transf/review]] — generative motion matching의 motion synthesis 기법이 UDH 모델의 behavior primitive 학습을 위한 기초 방법론을 제공한다.
- 🏛 기반 연구: [[papers/2047_Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Huma/review]] — 생성형 모션 매칭이 LATENT의 테니스 프리미브 수정 및 합성에 더 자연스러운 인간-로봇 스포츠 상호작용 기반 제공
- 🏛 기반 연구: [[papers/2088_Make_Tracking_Easy_Neural_Motion_Retargeting_for_Humanoid_Wh/review]] — Example-based Motion Synthesis의 생성형 모션 매칭이 NMR의 클러스터링 기반 모션 리타겟팅의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/2119_OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_G/review]] — 유연한 관절 제어와 예제 기반 모션 합성은 모두 세밀한 모션 제어를 제공하지만 서로 다른 제어 방식을 사용한다.
- 🏛 기반 연구: [[papers/2134_Perceptive_Humanoid_Parkour_Chaining_Dynamic_Human_Skills_vi/review]] — Example-based Motion Synthesis의 생성형 모션 매칭 기법이 Perceptive Humanoid Parkour의 인간 동작 데이터를 원자적 기술로 합성하는 핵심 방법론을 제공한다.
