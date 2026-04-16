---
title: "1310_Any-point_Trajectory_Modeling_for_Policy_Learning"
authors:
  - "Chuan Wen"
  - "Xingyu Lin"
  - "John So"
  - "Kai Chen"
  - "Qi Dou"
date: "2023.12"
doi: ""
arxiv: ""
score: 4.0
essence: "Any-point Trajectory Modeling (ATM)은 액션 라벨이 없는 비디오에서 임의의 점들의 미래 궤적을 예측하도록 사전 학습된 궤적 모델을 활용하여, 최소한의 액션-라벨 데이터로도 강건한 visuomotor 정책 학습을 가능하게 하는 프레임워크이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Action_Tokenization_Methods"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wen et al._2023_Any-point Trajectory Modeling for Policy Learning.pdf"
---

# Any-point Trajectory Modeling for Policy Learning

> **저자**: Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, Pieter Abbeel | **날짜**: 2023-12-28 | **URL**: [https://arxiv.org/abs/2401.00025](https://arxiv.org/abs/2401.00025)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Given a task instruction and the initial positions of any set of points in an image frame, our Any-point Traject*

Any-point Trajectory Modeling (ATM)은 액션 라벨이 없는 비디오에서 임의의 점들의 미래 궤적을 예측하도록 사전 학습된 궤적 모델을 활용하여, 최소한의 액션-라벨 데이터로도 강건한 visuomotor 정책 학습을 가능하게 하는 프레임워크이다.

## Motivation

- **Known**: 비디오는 행동, 물리학, 의미론적 지식의 풍부한 원천이지만, 액션 라벨 부재로 인해 제어 학습에 활용하기 어렵다. 기존 비디오 예측 접근법은 픽셀 변화를 모델링하여 hallucination 문제와 높은 계산 비용을 야기한다.
- **Gap**: 비디오 사전 학습과 정책 학습 사이를 연결할 수 있으면서도, 픽셀 수준의 복잡성을 피하고 물리적 동역학을 충실히 모델링할 수 있는 구조화된 표현이 부족하다.
- **Why**: 로봇 정책 학습의 주요 병목은 액션-라벨 시연 데이터 수집의 높은 비용이며, 대규모 비디오 데이터를 효과적으로 활용할 수 있으면 데이터 효율성을 크게 향상시킬 수 있다.
- **Approach**: 임의의 점들의 2D 궤적을 카메라 좌표계에서 예측하도록 ATM을 사전 학습하고, 예측된 궤적을 정책 학습 시 부분 목표(subgoal)로 활용하여 최소한의 액션-라벨 데이터로 정책을 학습한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: We compare with state-of-the-art video pre-training methods on language-conditioned manipulation tasks in the*

- **성능 향상**: 130개 이상의 언어-조건 조작 과제에서 63%의 성공률로 기존 비디오 사전 학습 방법 대비 평균 80% 향상
- **일반성**: 임의의 점에 대해 작동하므로 과제 특화 구조를 필요로 하지 않으며 다양한 환경에 적용 가능
- **전이 학습**: 인간 비디오 및 다른 로봇 형태의 비디오로부터 조작 기술의 효과적인 전이 학습 달성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of our framework. (a) In the first stage, given an action-free video dataset, we first sample 2D points*

- 최근의 비전 모델(Tracking Any Point)을 활용하여 비디오에서 자동으로 점 궤적 생성 및 자기 감독 학습 데이터 구성
- Particle 기반 궤적 모델링으로 픽셀 변화 대신 물리적 동역학 충실히 모델링하며, 물체 항상성과 연속 운동 같은 귀납 편향 자연스럽게 포함
- 카메라 보정 가정을 최소화하기 위해 2D 카메라 좌표계에서 궤적 예측
- 예측된 궤적을 정책 입력으로 제공하여 폐루프 실행 가능하게 함으로써 높은 견고성 달성
- Behavioral cloning 목표로 최소한의 액션-라벨 데이터로 궤적-안내 정책 학습

## Originality

- 픽셀 예측 대신 임의의 점의 궤적을 예측하는 새로운 구조화된 표현 제안으로, 기존 비디오 예측 및 특징 표현 학습과 구별됨
- 점 기반 궤적 모델링이 Tracking Any Point 같은 최신 비전 모듈과의 결합으로 자기 감독 방식의 확장성 있는 데이터 생성 실현
- 임의의 점에 대해 작동하면서도 cross-embodiment 전이 학습을 지원하는 범용성 높은 표현
- 정책 학습 시 폐루프 실행으로 견고성을 확보하면서도 계산 효율성 유지

## Limitation & Further Study

- 점 추적 모델(TAP)의 성능에 의존하므로, 추적 실패 시 궤적 예측 품질 저하 가능
- 비디오 사전 학습 데이터셋과 정책 학습 과제 간의 도메인 차이가 클 경우 전이 효과 감소 가능성
- 현재 조작 과제 중심 평가이며, 더 복잡한 장기 계획을 요하는 과제에서의 성능 미검증
- 후속 연구: 3D 궤적 모델링으로의 확장, 더 다양한 로봇 형태 및 과제 영역에서의 평가, 점 추적의 견고성 향상

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 비디오 데이터를 정책 학습에 효과적으로 활용하는 새로운 접근법으로, 임의의 점 궤적이라는 단순하면서도 강력한 표현을 통해 높은 성능과 일반성을 동시에 달성했다. 광범위한 실험과 명확한 프레임워크로 로봇 학습 분야에 의미 있는 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1448_Latent_Action_Pretraining_from_Videos/review]] — 비디오에서의 잠재 액션 사전 학습 개념이 임의 점 궤적 모델링의 핵심 아이디어를 제공
- 🔄 다른 접근: [[papers/1515_Phantom_Training_Robots_Without_Robots_Using_Only_Human_Vide/review]] — 액션 라벨 없는 학습 문제를 궤적 모델링 대신 인간 비디오만으로 해결하는 다른 접근법
- 🔗 후속 연구: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — Learning Latent Plans from Play의 라벨 없는 학습 개념을 trajectory modeling을 통한 policy learning으로 발전시켜 더 robust한 visuomotor 학습을 가능하게 합니다.
- 🔄 다른 접근: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 둘 다 large-scale video data를 활용하지만 ATM은 궤적 모델링에, Unleashing Large-Scale Video는 generative pre-training에 중점을 둡니다.
