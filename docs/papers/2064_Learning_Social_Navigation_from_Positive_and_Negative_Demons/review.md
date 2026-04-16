---
title: "2064_Learning_Social_Navigation_from_Positive_and_Negative_Demons"
authors:
  - "Chanwoo Kim"
  - "Jihwan Yoon"
  - "Hyeonseong Kim"
  - "Taemoon Jeong"
  - "Changwoo Yoo"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 긍정적 및 부정적 시연과 규칙 기반 명세로부터 학습한 밀도 기반 보상을 결합하여 동적 인간 환경에서 안전성과 적응성의 균형을 맞춘 모바일 로봇 네비게이션 정책을 개발한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kim et al._2025_Learning Social Navigation from Positive and Negative Demonstrations and Rule-Based Specifications.pdf"
---

# Learning Social Navigation from Positive and Negative Demonstrations and Rule-Based Specifications

> **저자**: Chanwoo Kim, Jihwan Yoon, Hyeonseong Kim, Taemoon Jeong, Changwoo Yoo, Seungbeen Lee, Soohwan Byeon, Hoon Chung, Matthew Pan, Jean Oh, Kyungjae Lee, Sungjoon Choi | **날짜**: 2025-10-14 | **URL**: [https://arxiv.org/abs/2510.12215](https://arxiv.org/abs/2510.12215)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of the proposed framework. A. Reward learning: (a) density-based reward maps are constructed from*

본 논문은 긍정적 및 부정적 시연과 규칙 기반 명세로부터 학습한 밀도 기반 보상을 결합하여 동적 인간 환경에서 안전성과 적응성의 균형을 맞춘 모바일 로봇 네비게이션 정책을 개발한다.

## Motivation

- **Known**: 기존의 고전적 네비게이션 방법은 해석 가능성과 명시적 안전 보장을 제공하지만 일반화가 어렵고, 학습 기반 방법은 적응성이 우수하나 분포 변화와 안전 메커니즘 부족 문제가 있다.
- **Gap**: 데이터 기반 보상의 적응성과 규칙 기반 안전 명세의 신뢰성을 효과적으로 통합하여 동적 인간 환경에서 실시간 배포 가능한 컴팩트한 정책을 얻는 방법이 부족하다.
- **Why**: 혼잡한 인간 환경에서의 로봇 네비게이션은 다양한 인간 행동 적응과 안전 제약 준수를 동시에 만족해야 하는 안전 핵심 문제이며, 실제 배포를 위해 계산 효율성이 필수적이다.
- **Approach**: Teacher-student 프레임워크로 teacher 정책은 긍정/부정 시연으로부터 학습한 density reward와 규칙 기반 장애물 회피·목표 도달 목표를 결합하여 감독 신호를 생성하고, 이를 관찰 기반 student 정책으로 증류하여 불확실성 추정과 함께 실시간 배포한다.

## Achievement


- **통합 보상 설계**: 긍정적/부정적 시연으로부터 학습한 밀도 기반 보상을 obstacle avoidance와 goal reaching을 위한 규칙 기반 항과 결합하여 적응성과 안전성을 동시에 달성
- **Teacher-Student 증류**: short-horizon rollout 평가를 통한 teacher 정책이 제공하는 감독 신호를 불확실성 추정이 포함된 컴팩트 student 정책으로 증류하여 실시간 배포 가능하게 함
- **다층적 검증**: 합성 데이터셋, 엘리베이터 탑승 시뮬레이션, 인간 참여자와의 실제 실험을 통해 성공률과 시간 효율성 면에서 베이스라인 대비 일관된 향상 달성

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of the proposed framework. A. Reward learning: (a) density-based reward maps are constructed from*

- Density reward learning: 경험적 상태-행동 밀도 ˆµ에 대해 보상 R을 최대화하는 최적화 문제를 L2 norm 제약 하에서 풀이
- Rule-based augmentation: obstacle avoidance와 goal reaching을 위한 명시적 비용 함수를 density reward와 결합하여 복합 목적함수 구성
- Teacher policy: sampling-based lookahead controller로 후보 속도 명령들을 시뮬레이션하여 복합 보상으로 평가하고 최고 수익 행동 선택
- Student policy distillation: teacher의 감독 신호를 LiDAR 관찰만 입력으로 받는 학생 정책으로 증류하여 forward simulation 없이 실시간 추론 가능하도록 함
- Uncertainty estimation: student 정책이 네비게이션 위험도를 나타내는 불확실성 추정값 함께 출력하도록 훈련

## Originality

- 긍정적 시연과 부정적 시연을 모두 활용한 density-based reward learning으로 원하는 행동과 피해야 할 행동을 명시적으로 인코딩하는 접근법은 기존 연구보다 더욱 구체적
- Rule-based 안전 명제와 학습 기반 적응성 보상의 통합을 sampling-based lookahead controller의 supervision을 통해 구현하는 것은 합리적인 중개 메커니즘
- Teacher-student 증류에 불확실성 추정을 함께 도입하여 배포 환경에서의 정책 신뢰도를 명시적으로 표현

## Limitation & Further Study

- Density reward learning이 제한된 시연 데이터에만 의존하므로 분포 외 상황(out-of-distribution scenario)에 대한 강건성이 불충분할 수 있음
- Teacher 정책의 lookahead horizon이 제한적이어서 장시간 상호작용 시나리오에 대한 성능이 보장되지 않음
- 실험이 주로 엘리베이터 탑승 시나리오에 집중되어 있어 다양한 보행자 네비게이션 환경으로의 일반화 가능성이 미지수
- Student 정책 증류 과정에서의 성능 손실(performance gap)에 대한 정량적 분석 및 최소화 전략이 부족
- 후속 연구로 더 복잡한 다중 에이전트 상호작용, 완전히 새로운 환경에 대한 전이 학습, 온라인 적응 메커니즘 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 데이터 기반 보상과 규칙 기반 안전 명제의 효과적인 통합을 통해 동적 인간 환경에서의 로봇 네비게이션을 다루는 실용적이고 신뢰할 수 있는 해결책을 제시하며, teacher-student 증류 및 불확실성 추정 기법을 포함한 방법론적 기여와 함께 실제 인간 참여자 실험으로 검증한 점에서 높은 가치를 갖는다.

## Related Papers

- 🔄 다른 접근: [[papers/1932_FocusNav_Spatial_Selective_Attention_with_Waypoint_Guidance/review]] — 웨이포인트 가이드를 통한 공간 선택적 주의 기반 네비게이션의 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/2104_MolmoSpaces_A_Large-Scale_Open_Ecosystem_for_Robot_Navigatio/review]] — 대규모 개방형 생태계를 통한 로봇 네비게이션의 확장된 프레임워크를 제공한다.
- 🏛 기반 연구: [[papers/2111_NoMaD_Goal_Masked_Diffusion_Policies_for_Navigation_and_Expl/review]] — 목표 마스킹 확산 정책을 통한 네비게이션의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2057_Learning_Humanoid_Navigation_from_Human_Data/review]] — 긍정적/부정적 시연을 활용한 사회적 내비게이션이 인간 데이터 기반 내비게이션 학습의 기반을 제공한다.
- 🧪 응용 사례: [[papers/1629_Quantum_deep_reinforcement_learning_for_humanoid_robot_navig/review]] — Learning Social Navigation의 양음 시연 학습이 quantum DRL의 고차원 상태-행동 공간 학습을 사회적 내비게이션에 적용한 사례임
- 🔗 후속 연구: [[papers/2057_Learning_Humanoid_Navigation_from_Human_Data/review]] — 인간 데이터 기반 내비게이션이 긍정적/부정적 시연을 활용한 사회적 내비게이션으로 확장되어 인간 환경 적응을 보여준다.
