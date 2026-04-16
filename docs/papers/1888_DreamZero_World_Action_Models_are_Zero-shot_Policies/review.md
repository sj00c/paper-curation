---
title: "1888_DreamZero_World_Action_Models_are_Zero-shot_Policies"
authors:
  - "| **날짜**:"
date: ""
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델에 대한 포괄적인 서베이로, 로봇이 시각, 언어, 행동 데이터를 통합하여 다양한 작업에 일반화할 수 있는 정책을 학습하도록 하는 기술을 체계적으로 검토한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "sub/Adaptive_Locomotion_Recovery"
  - "topic/humanoid"
---

# DreamZero: World Action Models are Zero-shot Policies

> **저자**:  | **날짜**:  | **URL**: [https://dreamzero0.github.io/](https://dreamzero0.github.io/)

---

## Essence


Vision-Language-Action (VLA) 모델에 대한 포괄적인 서베이로, 로봇이 시각, 언어, 행동 데이터를 통합하여 다양한 작업에 일반화할 수 있는 정책을 학습하도록 하는 기술을 체계적으로 검토한다.

## Motivation

- **Known**: LLM과 VLM의 발전이 자연어 처리와 컴퓨터 비전을 변혁했으며, 이러한 기술들이 로봇 분야로 확장되고 있다. 기존 연구들은 LLM/VLM과 로봇 정책을 분리하거나 고정된 모션 프리미티브를 사용하여 일반화 능력이 제한적이었다.
- **Gap**: 기존 서베이들은 action tokenization이나 일반적인 아키텍처에만 초점을 맞춰왔으나, VLA 모델의 소프트웨어와 하드웨어 전체 스택에 대한 포괄적이고 실용적인 검토가 부족하다. VLA 아키텍처와 학습 방법론이 표준화되지 않아 분야에 대한 통일된 이해가 부족하다.
- **Why**: VLA 모델은 작업 특화 데이터 수집 및 학습 필요성을 감소시켜 실제 로봇 배포 비용을 크게 낮출 수 있으며, 다양한 임무와 로봇 형태에 걸쳐 일반화 가능한 로봇 정책 개발을 촉진한다.
- **Approach**: 이 서베이는 VLA 모델의 역사적 발전, 아키텍처, 모달리티 통합 전략, 학습 패러다임을 체계적으로 검토하고, 로봇 플랫폼, 데이터 수집 방법, 데이터셋, 데이터 증강 기법, 평가 벤치마크를 포함한 전체 스택 관점의 포괄적 분석을 제공한다.

## Achievement


- **포괄적 서베이 구조**: 8개 섹션을 통해 설계 전략, 아키텍처, 학습 방법, 데이터 전략, 실제 배포, 실무가를 위한 권장사항을 체계적으로 제시
- **VLA 정의 및 분류**: Definition I.1을 통해 VLA 모델의 범위를 명확히 정의하고 기존 연구와의 차별성을 제시
- **실제 적용 지원**: 로봇 플랫폼, 평가 프로토콜, 실제 응용 분야에 대한 실무 가이던스 제공
- **오픈 리소스**: 학습 접근법, 평가 방법, 모달리티, 데이터셋으로 분류된 모든 참고문헌을 프로젝트 웹사이트에서 제공

## How


- 주요 도전 과제 분석: 데이터 요구사항과 부족, embodiment 전이, 계산 비용 제시
- VLA 모델의 전략적 전이와 아키텍처 진화 검토
- 시각, 언어, 행동 모달리티의 구체적 처리 기법 분석
- Imitation learning을 포함한 주요 학습 패러다임 설명
- 공개 데이터셋 및 데이터 증강 방법 체계적 분류
- 실제 로봇 시스템 배포를 위한 평가 벤치마크 및 프로토콜 검토
- 실무가를 위한 실질적 권장사항 도출

## Originality

- 기존 서베이와 달리 아키텍처와 개발 방법론을 넘어 로봇 플랫폼, 데이터 수집 전략, 공개 데이터셋, 데이터 증강 기법, 평가 벤치마크를 포함한 전체 스택 관점의 포괄적 검토 제시
- VLA 모델을 위한 명확한 정의(Definition I.1)를 제공하여 관련 연구들과의 경계 설정
- 실제 로봇 배포를 고려한 실무적 관점의 권장사항 제공으로 학술 연구와 실제 응용 간의 격차 해소

## Limitation & Further Study

- 서베이 성격상 새로운 기술 개발이나 실험적 성과가 아닌 기존 문헌의 종합이므로 혁신적 알고리즘이나 방법론을 제시하지 않음
- VLA 분야가 아직 초기 단계이므로 장기적 실제 배포 효과에 대한 데이터 부족
- embodiment 전이, 데이터 부족, 계산 비용 등의 근본적 도전 과제에 대한 완전한 해결책이 제시되지 않음
- 후속 연구 방향: 다양한 embodiment 간 효과적인 정책 전이 방법 개발, 웹 규모 데이터와 로봇 데이터의 효과적 통합 전략, 계산 효율성을 개선한 경량 VLA 모델 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 서베이는 VLA 모델에 대한 현재까지의 가장 포괄적이고 실무 지향적인 검토를 제공하며, 로봇 공학 커뮤니티가 VLA를 실제 시스템에 적용할 때 필요한 실질적 가이던스를 효과적으로 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1812_Behavior_Foundation_Model_for_Humanoid_Robots/review]] — Vision-Language-Action 모델과 행동 기반 모델은 모두 범용적인 휴머노이드 정책 학습을 목표로 하지만 서로 다른 접근 방식을 사용한다.
- 🔗 후속 연구: [[papers/1814_Being-H0_Vision-Language-Action_Pretraining_from_Large-Scale/review]] — 대규모 비전-언어-행동 사전학습이 VLA 모델의 실제 구현 사례로 확장될 수 있다.
- 🏛 기반 연구: [[papers/1761_Zero-Shot_Whole-Body_Humanoid_Control_via_Behavioral_Foundat/review]] — 행동 기반 모델이 VLA 모델의 zero-shot 정책 학습을 위한 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1904_EgoVLA_Learning_Vision-Language-Action_Models_from_Egocentri/review]] — Vision-Language-Action 모델에 대한 포괄적 서베이와 구체적인 egocentric VLA 구현이 서로 다른 관점에서 VLA 기술을 다룬다.
- 🧪 응용 사례: [[papers/2161_Trinity_A_Modular_Humanoid_Robot_AI_System/review]] — VLA 모델의 이론적 프레임워크가 Trinity와 같은 modular humanoid AI system의 실제 구현에서 핵심 설계 원리로 활용된다.
- 🔄 다른 접근: [[papers/2000_Humanoid_Policy__Human_Policy/review]] — 인간 정책을 휴머노이드로 전이하는 다른 접근 방식으로, 제로샷 정책 생성에 대한 대안적 관점을 제시한다.
- 🔗 후속 연구: [[papers/1949_Generative_World_Modelling_for_Humanoids_1X_World_Model_Chal/review]] — 1X World Model의 generative world modelling 프레임워크가 DreamZero의 world action model을 더욱 고도화할 수 있는 확장 방향을 제시한다.
- 🔄 다른 접근: [[papers/1821_BFM-Zero_A_Promptable_Behavioral_Foundation_Model_for_Humano/review]] — zero-shot 정책 구현에서 하나는 behavioral foundation model, 다른 하나는 world action model을 사용하는 상호 보완적 접근이다.
- 🔄 다른 접근: [[papers/1949_Generative_World_Modelling_for_Humanoids_1X_World_Model_Chal/review]] — 둘 다 world model을 다루지만 Generative World Modelling은 video-state 예측을, DreamZero는 zero-shot policy를 중심으로 한다.
- 🔗 후속 연구: [[papers/2005_Humanoid_World_Models_Open_World_Foundation_Models_for_Human/review]] — DreamZero의 world action model을 HWM이 humanoid 특화 egocentric 조건화로 확장하여 더 구체적인 제어 토큰 예측을 달성합니다.
