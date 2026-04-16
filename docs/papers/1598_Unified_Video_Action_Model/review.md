---
title: "1598_Unified_Video_Action_Model"
authors:
  - "Shuang Li"
  - "Yihuai Gao"
  - "Dorsa Sadigh"
  - "Shuran Song"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "UVA는 비디오 생성과 액션 예측을 통합적으로 학습하는 모델로, 공유된 잠재 표현과 분리된 확산 헤드를 통해 높은 정확도와 빠른 추론 속도를 동시에 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_Unified Video Action Model.pdf"
---

# Unified Video Action Model

> **저자**: Shuang Li, Yihuai Gao, Dorsa Sadigh, Shuran Song | **날짜**: 2025-02-28 | **URL**: [https://arxiv.org/abs/2503.00200](https://arxiv.org/abs/2503.00200)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Unified Video Action Model. (a) UVA features a joint video-action latent representation and decoupled video-acti*

UVA는 비디오 생성과 액션 예측을 통합적으로 학습하는 모델로, 공유된 잠재 표현과 분리된 확산 헤드를 통해 높은 정확도와 빠른 추론 속도를 동시에 달성한다.

## Motivation

- **Known**: 로봇 정책 학습에서 비디오 생성은 환경 맥락을 제공하고 액션 예측은 동역학을 모델링할 수 있다. 하지만 기존 방법들은 비디오 생성의 느린 속도나 액션 전용 모델의 제한된 표현력 중 하나를 포기해야 했다.
- **Gap**: 비디오 생성 기반 정책 학습은 생성된 비디오로부터 액션을 추출하므로 추론이 느리고 오류가 누적되며, 액션 전용 방법은 비디오 감독의 이점을 활용하지 못한다.
- **Why**: 로봇 제어에서 실시간 정책 배포를 위해서는 빠른 추론 속도가 필수적이며, 동시에 정확한 액션 예측을 위해 풍부한 시각 정보가 필요하다.
- **Approach**: UVA는 비디오와 액션을 공유된 잠재 공간에서 학습하고, 두 개의 경량 diffusion 헤드를 사용해 비디오와 액션을 분리되게 디코딩하며, 마스크 기반 훈련으로 다양한 작업을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Unified Video Action Model. (a) UVA features a joint video-action latent representation and decoupled video-acti*

- **통합 성능**: PushT Multitask에서 기존 최고 성능 모델 대비 20% 높은 성공률, Libero10에서 5% 향상 달성
- **추론 속도**: 분리된 diffusion 헤드로 비디오 생성을 생략하여 Diffusion Policy와 유사한 속도 유지
- **다목적 활용**: 단일 모델로 정책 학습, forward/inverse dynamics, 비디오 생성, 결합 정책-비디오 플래너 수행 가능
- **강건성**: 마스크 훈련을 통해 비디오 감독이 제공되지 않는 데이터셋에서도 학습 가능

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Network Architecture. Given historical observations {Ot−h+1, . . . , Ot} and corresponding action chunks {At−h, *

- **통합 잠재 표현**: 과거 관찰과 액션을 channel-wise로 연결하여 Transformer를 통해 미래의 공유된 잠재 토큰 생성
- **분리된 diffusion 디코딩**: 동일한 잠재 표현에서 video diffusion 헤드와 action diffusion 헤드를 독립적으로 운영하여 비디오와 액션을 동시에 학습
- **마스크 훈련**: 입력과 출력으로 사용할 비디오/액션을 임의로 마스킹하여 다양한 조건부 생성 작업을 단일 모델로 처리
- **경량화**: 두 diffusion 헤드 모두 경량으로 설계하여 훈련 과정에서도 computational overhead 최소화

## Originality

- 비디오와 액션의 공유 잠재 표현 학습을 통해 두 모달리티 간의 상호작용을 명시적으로 모델링하는 통합 접근
- 분리된 diffusion 헤드 설계로 훈련 중에는 비디오 감독의 이점을 활용하면서도 추론 시에는 비디오 생성을 우회하는 창의적 해결책
- 마스크 훈련의 로봇 정책 학습에서의 활용을 확장하여 dynamics 모델, 비디오 생성, 결합 계획 등 다양한 작업을 통합적으로 지원

## Limitation & Further Study

- 현재 평가는 주로 모의 환경(PushT, Libero)과 제한된 실제 환경 실험으로 진행되어 더 복잡한 실제 로봇 작업에서의 성능 검증 필요
- 마스크 훈련의 다양한 조합이 각각의 작업에 미치는 영향에 대한 상세한 ablation 분석 부재
- diffusion 기반 디코딩의 노이즈 수준과 샘플링 스텝이 최종 성능에 미치는 영향 분석 부족
- 후속 연구로 더 큰 규모 데이터셋에서의 사전학습 및 transfer learning 성능 평가, 다양한 로봇 embodiment에서의 일반화 가능성 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: UVA는 비디오와 액션 학습의 오랜 트레이드오프를 통합 잠재 표현과 분리된 디코딩으로 효과적으로 해결하며, 마스크 훈련을 통한 다목적 활용으로 로봇 학습 프레임워크의 실용성을 크게 향상시킨다.

## Related Papers

- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 비디오와 액션의 통합 학습에 대한 서로 다른 접근법 - diffusion vs autoregressive modeling입니다.
- 🔗 후속 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — video foundation model을 unified video action model로 확장한 응용 연구입니다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전 훈련이 unified video action model의 기반이 됩니다.
- 🏛 기반 연구: [[papers/1360_Diffusion_Models_Are_Real-Time_Game_Engines/review]] — 실시간 게임 엔진으로서의 확산 모델 개념을 제공하여 UVA의 비디오-액션 통합 아키텍처 설계에 영감을 준다.
- 🔗 후속 연구: [[papers/1455_Learning_Universal_Policies_via_Text-Guided_Video_Generation/review]] — 텍스트 가이드 비디오 생성을 unified video action model로 더 체계화하고 일반화했다.
- 🔗 후속 연구: [[papers/1481_Motus_A_Unified_Latent_Action_World_Model/review]] — unified video action model의 개념을 latent action world model과 결합하여 더 통합적인 vision-language-action 프레임워크를 구축한다.
- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — vision-language-action 통합을 위한 서로 다른 모델링 방법 - autoregressive vs diffusion입니다.
- 🔗 후속 연구: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — Unified Video Action Model의 action modeling 개념을 transformer 기반 multi-task action correction과 action discretization으로 발전시킨 연구입니다.
- 🏛 기반 연구: [[papers/1366_Discrete_Diffusion_VLA_Bringing_Discrete_Diffusion_to_Action/review]] — 통합된 비전-언어-액션 모델의 기본 아키텍처를 제공합니다.
