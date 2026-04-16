---
title: "1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to"
authors:
  - "Chao Xu"
  - "Suyu Zhang"
  - "Yang Liu"
  - "Baigui Sun"
  - "Weihong Chen"
date: "2025.12"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델의 구조와 발전을 체계적으로 분석하는 종합 서베이로, 기본 모듈부터 역사적 마일스톤을 거쳐 5가지 핵심 과제까지 단계적으로 설명한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xu et al._2025_An Anatomy of Vision-Language-Action Models From Modules to Milestones and Challenges.pdf"
---

# An Anatomy of Vision-Language-Action Models: From Modules to Milestones and Challenges

> **저자**: Chao Xu, Suyu Zhang, Yang Liu, Baigui Sun, Weihong Chen, Bo Xu, Qi Liu, Juncheng Wang, Shujun Wang, Shan Luo, Jan Peters, Athanasios V. Vasilakos, Stefanos Zafeiriou, Jiankang Deng | **날짜**: 2025-12-12 | **URL**: [https://arxiv.org/abs/2512.11362](https://arxiv.org/abs/2512.11362)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: The structure of this survey in a pyramid format. Section 2 lays*

Vision-Language-Action (VLA) 모델의 구조와 발전을 체계적으로 분석하는 종합 서베이로, 기본 모듈부터 역사적 마일스톤을 거쳐 5가지 핵심 과제까지 단계적으로 설명한다.

## Motivation

- **Known**: VLA 모델은 로봇의 지능화를 위해 시각, 언어, 행동을 통합하는 기초 모델로 빠르게 발전 중이며, 기존 서베이들은 특정 기술 영역이나 모델 아키텍처 중심으로 단편적 정보를 제공하고 있다.
- **Gap**: 기존 서베이는 연구 과제를 부수적인 결론 섹션으로만 다루고, 초보 연구자를 위한 통일된 학습 경로 없이 단순 분류 방식으로 정보를 나열하여 필드 간 통합적 이해가 부족하다.
- **Why**: VLA 분야가 급속도로 확장하고 새로운 모델과 데이터셋이 지속적으로 등장하므로, 체계적이고 진행 단계적인 학습 가이드와 심층적인 문제 분석이 필수적이다.
- **Approach**: 기초 모듈(Perception, Brain, Action), 역사적 발전(Milestones), 5가지 핵심 과제(Representation, Execution, Generalization, Safety, Dataset)의 3단계 피라미드 구조로 설계하여 초보자부터 경험자까지 체계적인 학습 경로를 제공한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: The structure of this survey in a pyramid format. Section 2 lays*

- **구조화된 학습 경로**: 기본 모듈 분해 → 역사적 진화 → 심층 과제 분석의 단계적 구조로 연구자의 자연스러운 학습 궤적 지원
- **심층 과제 분석**: 기존의 개괄적 문제 나열을 넘어 (1) Multi-Modal Alignment and Physical World Modeling, (2) Instruction Following, Planning, and Robust Real-Time Execution, (3) Generalization to Continuous Adaptation, (4) Safety, Interpretability, and Reliable Interaction, (5) Data Construction and Benchmarking Standards의 5대 과제 심층 분석
- **아키텍처 진화 트렌드**: Perception의 Language-Aligned Transformers (SigLIP) 및 DINOv2로의 진화, Brain의 pre-trained VLM 수렴, Action의 discrete tokenization에서 continuous generative modeling (Diffusion)으로의 전환 추적
- **실시간 업데이트 플랫폼**: 프로젝트 페이지를 통한 지속적 업데이트로 빠르게 변화하는 연구 최전선 반영

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: The structure of this survey in a pyramid format. Section 2 lays*

- 기본 모듈 섹션(Section 2)에서 Vision Encoder (CNN, ViT, Language-Supervised/Self-Supervised variants), Robot Brain, Action 모듈의 최신 동향 정리
- 역사적 마일스톤(Section 3)을 통해 VLA 모델, 데이터셋, 평가 벤치마크의 시간별 진화 과정 제시
- 5가지 핵심 과제 각각에 대해 (1) 문제 정의, (2) 기존 해결책 비교, (3) 향후 연구 방향 제시의 3단계 심층 분석
- 멀티모달 얼라인먼트부터 안전성, 데이터 구축까지 VLA 에이전트의 개발 로드맵을 반영한 과제 순서 설정

## Originality

- **문제 중심 설계**: 기존 서베이의 방법론 중심에서 벗어나 핵심 과제를 조사의 중심축으로 재배치하여 미해결 문제에 대한 체계적 분석 제공
- **학습 경로 설계**: 연구자의 심리적 학습 단계를 반영한 피라미드 구조(Modules → Milestones → Challenges)로 새로운 서베이 포맷 제시
- **종합적 과제 프레임워크**: 단순 기술 분류를 넘어 지각-뇌-행동의 통합 관점에서 생성 에이전트 개발의 전체 생명주기 포괄
- **동적 자료**: 전통 논문 형식을 넘어 지속적으로 업데이트되는 프로젝트 페이지를 통해 빠르게 변화하는 필드에 대응

## Limitation & Further Study

- **제한된 심층성**: 스페이스 제약으로 인해 기본 모듈 섹션을 streamlined overview로 축약하여 아키텍처 상세 분석 부족 (저자들이 전문 서베이 추천)
- **평가 프레임워크 미흡**: 과제별 해결책의 정량적 비교 체계가 명확하지 않아 어느 접근법이 더 우월한지 판단 어려움
- **실제 구현 거리**: 문제 정의와 분석에 비해 실제 구현 가능한 솔루션 제시의 깊이가 상대적으로 부족할 수 있음
- **후속 연구**: (1) 각 과제별 벤치마크 성능 메타분석 추가, (2) 서로 다른 과제 간 상충관계(trade-off) 분석, (3) 산업 적용 사례 기반 우선순위 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 서베이는 빠르게 성장하는 VLA 분야에서 기존 단편적 가이드의 한계를 극복하고, 초보자부터 전문가까지 포용할 수 있는 체계적 학습 경로와 심층적 문제 분석을 제공하여 필드의 리더맵 역할을 할 수 있는 가치 있는 자료이다.

## Related Papers

- 🔄 다른 접근: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Pure VLA 모델에 대한 포괄적 서베이로 VLA 구조 분석을 보완한다.
- 🔗 후속 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — VLA 모델의 개념과 응용을 더 넓은 관점에서 확장한다.
- 🏛 기반 연구: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — 로봇을 위한 VLA 모델의 기초적 리뷰를 제공한다.
- 🏛 기반 연구: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — VLA 모델의 모듈 분석 연구가 OpenHelix의 dual-system VLA 아키텍처 설계 요소 분석에 이론적 기초를 제공한다.
- 🔗 후속 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — VLA Models Anatomy가 VLA 모델 구축의 핵심 요소들을 모듈별로 더 상세히 분석하고 확장한다.
- 🏛 기반 연구: [[papers/1300_A_Survey_on_Vision-Language-Action_Models_for_Autonomous_Dri/review]] — VLA 모델의 모듈별 분석은 자율주행용 VLA 시스템 이해에 필수적인 구조적 기초를 제공한다.
