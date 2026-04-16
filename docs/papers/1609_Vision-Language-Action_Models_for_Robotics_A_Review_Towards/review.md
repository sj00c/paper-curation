---
title: "1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards"
authors:
  - "Kento Kawaharazuka"
  - "Jihoon Oh"
  - "Jun Yamada"
  - "Ingmar Posner"
  - "Yuke Zhu"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델이 로봇이 다양한 작업을 수행하도록 하는 통합 학습 방식에 대한 포괄적 리뷰로, 소프트웨어와 하드웨어 통합을 포함한 실제 배포 가이드를 제시한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kawaharazuka et al._2025_Vision-Language-Action Models for Robotics A Review Towards Real-World Applications.pdf"
---

# Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications

> **저자**: Kento Kawaharazuka, Jihoon Oh, Jun Yamada, Ingmar Posner, Yuke Zhu | **날짜**: 2025-10-08 | **URL**: [https://arxiv.org/abs/2510.07077](https://arxiv.org/abs/2510.07077)

---

## Essence


Vision-Language-Action (VLA) 모델이 로봇이 다양한 작업을 수행하도록 하는 통합 학습 방식에 대한 포괄적 리뷰로, 소프트웨어와 하드웨어 통합을 포함한 실제 배포 가이드를 제시한다.

## Motivation

- **Known**: LLM과 VLM이 자연어 처리와 컴퓨터 비전 분야에서 성공을 거두었으며, 일부 연구는 이들을 로봇에 적용하기 위해 고정된 모션 프리미티브나 모방 학습 기반 정책을 사용해왔다.
- **Gap**: 기존 조사는 행동 토큰화(action tokenization)나 고수준 아키텍처에만 초점을 맞췄지만, VLA의 표준화된 아키텍처와 훈련 방법론이 부재하며, 실제 로봇 시스템 배포를 위한 전체 스택(full-stack) 체계적 검토가 부족하다.
- **Why**: VLA는 최소한의 추가 데이터로 새로운 작업을 수행할 수 있는 범용 로봇 정책을 가능하게 하여, 실제 배포의 유연성과 확장성을 크게 높일 수 있기 때문이다.
- **Approach**: 이 논문은 VLA 모델의 진화 과정, 아키텍처, 모달리티별 처리 기법, 학습 패러다임을 체계적으로 검토하고, 로봇 플랫폼, 데이터 수집 전략, 공개 데이터셋, 데이터 증강, 평가 벤치마크를 포함한 실제 배포 고려사항을 제시한다.

## Achievement


- **포괄적 전체 스택 리뷰**: 기존 조사를 넘어 아키텍처뿐만 아니라 로봇 플랫폼, 데이터 수집, 데이터 증강, 평가 벤치마크를 통합하는 최초의 체계적 리뷰 제공
- **VLA 정의 및 분류**: Vision-Language-Action 모델의 명확한 정의(Definition I.1)와 기존 모델들의 분류 체계 확립
- **실무 가이드**: 실제 로봇 시스템에 VLA를 적용하려는 연구자들을 위한 실질적인 가이드 및 권장사항 제시
- **도전 과제 체계화**: 데이터 가용성, 체구화 전이(embodiment transfer), 계산 비용의 세 가지 핵심 도전 과제를 구조화하여 제시

## How


- VLA의 전략적 진화와 아키텍처 전환 경로를 역사적 관점에서 추적
- Vision encoder, Language model, Action decoder 등 핵심 구성 요소와 빌딩 블록 분석
- 멀티모달 입력(시각, 언어, 고유감각 등)의 modality-specific 처리 기법 검토
- Supervised learning, Reinforcement learning, Self-supervised learning 등 다양한 학습 패러다임 분류
- 로봇 시스템별 데이터 수집 전략(텔레오퍼레이션, 원격 조작 등) 분석
- 공개 데이터셋(RLDS, RoboNet, BridgeData 등) 조사 및 분류
- Sim-to-real transfer, Domain randomization 등 데이터 증강 기법 검토
- 로봇 플랫폼 유형(그리퍼 로봇, 휴머노이드, 모바일 로봇 등) 및 평가 벤치마크 분석

## Originality

- 기존 조사와 달리 소프트웨어와 하드웨어를 통합하는 최초의 전체 스택 리뷰 제공
- VLA 모델의 명확한 정의를 제시하여 범위를 명확히 하고 관련 접근법들과의 경계 구분
- 데이터 부족, 체구화 전이, 계산 비용이라는 근본적 도전 과제를 체계적으로 분석
- 이론적 논의와 실제 배포 고려사항을 연계하는 실무 중심의 관점 도입

## Limitation & Further Study

- 논문은 리뷰이므로 새로운 방법론이나 실험적 성과를 제시하지 않음
- VLA의 빠른 발전으로 인해 논문 작성 시점 이후의 최신 모델들(예: 2024년 이후)을 완전히 포함하지 못할 가능성
- 실제 로봇 배포에서의 실패 사례나 한계에 대한 상세한 논의가 제한적일 수 있음
- 다양한 로봇 플랫폼에서의 VLA 성능 비교를 위한 통일된 벤치마크 부재 문제 해결 방안이 불충분
- **후속 연구**: 크로스-도메인 학습, 저데이터 체제에서의 VLA 효율성, 실시간 계산 제약이 있는 엣지 로봇으로의 배포, 인간 피드백 기반 개선 방법론 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 종합 리뷰는 VLA 연구 분야의 현황을 체계적으로 정리하고 실제 로봇 시스템 배포를 위한 실무 가이드를 제공하여, 로봇공학 커뮤니티가 VLA를 효과적으로 적용하는 데 큰 가치를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — 둘 다 VLA 모델 리뷰이지만 이 논문은 실제 배포와 하드웨어 통합에, 전자는 개념적 진전에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1386_Evaluating_Real-World_Robot_Manipulation_Policies_in_Simulat/review]] — 시뮬레이션에서 실제 로봇 정책 평가 연구를 VLA 모델의 실제 배포 가이드로 확장하여 실용적 관점을 제시한다.
- 🏛 기반 연구: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — VLA 모델의 실시간 실행 속도 연구가 실제 로봇 배포를 위한 포괄적 가이드의 핵심 기반 기술을 제공한다.
- 🏛 기반 연구: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo의 오픈소스 범용 로봇 정책이 VLA 모델의 실제 배포를 위한 실용적 프레임워크의 기반을 제공한다.
- 🔄 다른 접근: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — 두 리뷰 논문 모두 VLA 모델을 다루지만 실제 배포 vs 순수 VLA 모델 설계에 중점을 두어 서로 보완적입니다.
- 🔗 후속 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — What Matters in Building VLA Models은 일반 목적 VLA 구축의 핵심 요소를 식별하여 실제 배포 가이드를 보완합니다.
- 🏛 기반 연구: [[papers/1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to/review]] — 로봇을 위한 VLA 모델의 기초적 리뷰를 제공한다.
- 🏛 기반 연구: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Vision-Language-Action Models for Robotics의 VLA 모델 리뷰가 Foundation Model Driven Robotics의 더 넓은 foundation model 응용 분석에 기초적 배경을 제공한다.
- 🔗 후속 연구: [[papers/1446_Large_VLM-based_Vision-Language-Action_Models_for_Robotic_Ma/review]] — VLA Models for Robotics 리뷰를 대규모 VLM 기반 시스템으로 구체화하여 로봇 매니퓰레이션에 특화한다.
- 🏛 기반 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — 로봇 비전을 위한 멀티모달 융합 기법은 VLA 모델 전반의 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1513_Parallels_Between_VLA_Model_Post-Training_and_Human_Motor_Le/review]] — VLA 모델 post-training 방법론은 VLA 모델 전반의 개념과 응용을 이해하는 데 필수적입니다.
- 🔄 다른 접근: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — 둘 다 VLA 모델에 대한 종합적 리뷰를 제공하지만 전자는 일반적 개념과 진전을, 후자는 실제 배포에 중점을 둔다.
