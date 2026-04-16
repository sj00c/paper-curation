---
title: "1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review"
authors:
  - "Muhammad Tayyab Khan"
  - "Ammar Waheed"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 LLM과 VLM 같은 foundation model들이 로봇공학에 미치는 변혁적 영향을 체계적으로 분석하는 종합 리뷰로, 시뮬레이션, 실제 환경 실행, sim-to-real transfer, 적응형 로봇 등 다양한 응용 분야를 통합적으로 평가한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Khan and Waheed_2025_Foundation Model Driven Robotics A Comprehensive Review.pdf"
---

# Foundation Model Driven Robotics: A Comprehensive Review

> **저자**: Muhammad Tayyab Khan, Ammar Waheed | **날짜**: 2025-07-14 | **URL**: [https://arxiv.org/abs/2507.10087](https://arxiv.org/abs/2507.10087)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

이 논문은 LLM과 VLM 같은 foundation model들이 로봇공학에 미치는 변혁적 영향을 체계적으로 분석하는 종합 리뷰로, 시뮬레이션, 실제 환경 실행, sim-to-real transfer, 적응형 로봇 등 다양한 응용 분야를 통합적으로 평가한다.

## Motivation

- **Known**: LLM과 VLM은 의미론적 이해, 고수준 추론, 교차-모달 일반화 능력을 가지고 있으며, 로봇의 지각, 계획, 제어, 인간-로봇 상호작용 분야에서 개별 역량들이 점진적으로 입증되어 왔다. 기존 연구들은 주로 격리된 기능에 초점을 맞추거나 특정 방법론을 강조해 왔다.
- **Gap**: foundation model 기반 로봇공학의 실제 시스템 수준 통합, 의미론적 grounding과 물리적 실행의 연결, 그리고 실시간 성능, 안전성, 신뢰성 측면에서의 실제 환경 적용 가능성에 대한 종합적 평가가 부족하다.
- **Why**: 로봇이 복잡한 실제 환경에서 인간 수준의 지능(유연성, 적응성, 일반화 능력)을 달성하려면 언어 기반 지능과 물리적 제어를 효과적으로 결합해야 하며, 현재의 개별 기능 중심 연구로는 이 통합적 도전을 해결할 수 없다.
- **Approach**: LLM과 VLM의 진화 경로를 추적하고, 지각(Perception), 계획(Planning), 제어(Control), 인간-로봇 상호작용(HRI)의 네 가지 로봇 핵심 요소별로 foundation model 적용을 체계화하며, procedural scene generation, policy generalization, multimodal reasoning 같은 핵심 트렌드와 embodiment 제한, 데이터 부족, 안전 위험, 계산 제약 같은 병목을 동시에 평가한다.

## Achievement


- **체계적 분류 체계**: 시뮬레이션 기반 설계, 개방형 환경 실행, sim-to-real transfer, 적응형 로봇 등 응용 분야별로 foundation model 활용 패턴을 통합적으로 정리
- **아키텍처 강점과 한계 평가**: foundation model 기반 로봇공학의 의미론적 이해와 추론 능력의 장점과 embodiment 부재, 실시간 처리 어려움, 안전성 위험이라는 근본적 한계를 명확히 규명
- **실용성 중심 분석**: 기존 단편적 리뷰와 달리 실제 환경 적용 가능성과 제약을 고려한 시스템 수준의 전략 평가
- **미래 연구 로드맵**: 의미론적 추론과 물리적 지능을 연결하기 위한 더욱 강건하고 해석 가능하며 embodied된 모델 개발 방향 제시

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- Foundation model 발전 경로 추적: BERT, T5부터 GPT-3, GPT-4, Flamingo, BLIP-2 등 주요 LLM/VLM의 아키텍처 진화와 로봇공학 적용 가능성 분석
- Perception 컴포넌트: CLIP의 open-vocabulary visual recognition, VLM의 multimodal reasoning을 통한 의미론적 매핑 및 객체 인식 능력 검토
- Planning 컴포넌트: LLM의 instruction following과 commonsense inference로 고수준 목표를 행동 시퀀스로 변환하는 능력 분석
- Control 컴포넌트: LLM의 code generation 능력으로 저수준 제어 코드 생성 가능성 검토
- HRI 컴포넌트: multimodal dialogue, VQA, referring expression comprehension 등 인간과의 상호작용 능력 평가
- 병목 요인 식별: semantic grounding, real-time responsiveness, safety assurance, computational constraints 등 실제 배치 시 직면하는 구체적 문제 분석
- Enabling trends 검토: procedural scene generation, policy generalization, multimodal reasoning 같은 해결책 분석

## Originality

- 기존 리뷰와 달리 **통합 시스템 관점**: 격리된 기능이 아닌 perception-planning-control-HRI의 상호작용과 통합을 강조
- **실제 환경 실용성 중심**: 시뮬레이션, 개방형 환경, sim-to-real transfer 등 실제 배치 시나리오별 구체적 평가
- **양면적 평가**: foundation model의 의미론적 강점과 embodiment 부재 같은 근본적 제약을 동시에 조명하여 균형잡힌 관점 제공
- **명확한 병목 규명**: LLM이 물리적 맥락과 sensor data에 agnostic하다는 핵심 문제를 직시하고 현재의 통합 방식이 이를 충분히 해결하지 못함을 지적

## Limitation & Further Study

- **Embodiment 문제 미해결**: LLM이 본질적으로 물리적 역학, 센서 데이터, 메트릭을 이해하지 못하는 근본적 한계에 대한 해결책이 제시되지 않음
- **Multimodal 데이터 부족**: 로봇 중심의 다양한 embodiment에 대한 학습 데이터 부족으로 일반성 제한
- **실시간 성능 달성의 어려움**: LLM의 추론 지연이 로봇의 real-time 제어 요구사항과 충돌하는 문제
- **안전성과 신뢰성**: 언어 모델의 hallucination과 물리적 환경에서의 예측 불가능한 오류에 대한 robust한 검증 메커니즘 부재
- **후속 연구 방향**: (1) 더욱 embodied된 foundation model 개발로 물리 직관 통합, (2) 로봇 특화 학습 데이터 확대, (3) 의미론적 추론과 저수준 제어 간 효율적 연결 메커니즘 개발, (4) 안전성 검증 및 interpretability 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 foundation model 기반 로봇공학의 현황을 가장 포괄적으로 정리한 종합 리뷰로, 기존의 단편적 기능 중심 평가를 넘어 시스템 수준의 통합과 실제 환경 적용 가능성을 균형있게 분석한다. 의미론적 강점과 embodiment 약점을 명확히 구분하여 미래 연구의 방향성을 제시한 점이 주요 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — 둘 다 foundation model의 로봇공학 응용을 종합적으로 다루지만 LLM/VLM 중심 vs 전반적 foundation model로 범위가 다르다.
- 🏛 기반 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — foundation model 시대의 로봇 학습에 대한 기본적인 조망을 제공하는 선행 연구이다.
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — 순수 VLA 모델에 대한 연구를 LLM과 VLM을 포함한 더 넓은 foundation model 관점으로 확장했다.
- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — General-Purpose Robots Survey는 foundation model driven robotics와 유사한 범위를 다루지만 범용 로봇 관점에서 다른 분석 틀을 제시합니다.
- 🔄 다른 접근: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — Vision-Language-Action Models review와 Foundation Model Driven Robotics review는 로봇공학에서 foundation model의 역할을 서로 다른 관점에서 종합적으로 분석한다.
- 🏛 기반 연구: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — Vision-Language-Action Models for Robotics의 VLA 모델 리뷰가 Foundation Model Driven Robotics의 더 넓은 foundation model 응용 분석에 기초적 배경을 제공한다.
- 🏛 기반 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation Model Driven Robotics의 포괄적 리뷰는 로봇틱스 foundation model 응용 조사에 더 넓은 기술적 맥락과 기반을 제공한다.
- 🔗 후속 연구: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — Foundation Model Driven Robotics의 전반적 리뷰를 의사결정 패러다임과 embodied learning으로 구체화하여 발전시킨다.
- 🏛 기반 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — foundation model driven robotics의 포괄적인 리뷰를 제공하여 multimodal fusion과 VLM의 로봇 응용에 대한 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Foundation Model Driven Robotics 서베이가 VLA 모델 연구의 전반적 맥락을 제공한다.
- 🔄 다른 접근: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — 두 survey 모두 foundation model driven robotics를 다루지만 하나는 학습 중심, 다른 하나는 전반적 로봇 시스템 관점에서 접근한다.
- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — Foundation Model Driven Robotics는 foundation model 기반 로봇공학에 대한 또 다른 종합적 리뷰를 제공한다.
- 🔄 다른 접근: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — 둘 다 로봇 분야의 comprehensive review이지만 VLN survey는 navigation에, Foundation Model Driven Robotics는 foundation model에 집중한다.
- 🏛 기반 연구: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — Foundation Model Driven Robotics는 EIIR 프레임워크의 이론적 토대가 되는 로봇 기반 모델 전반에 대한 포괄적 리뷰임
- 🔄 다른 접근: [[papers/1305_Aligning_Cyber_Space_with_Physical_World_A_Comprehensive_Sur/review]] — Foundation Model 기반 로보틱스 리뷰와 사이버-물리 정렬이 다른 관점에서 embodied AI를 분석합니다.
