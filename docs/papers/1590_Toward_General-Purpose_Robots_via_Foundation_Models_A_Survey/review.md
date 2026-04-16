---
title: "1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey"
authors:
  - "Yafei Hu"
  - "Quanting Xie"
  - "Vidhi Jain"
  - "Jonathan Francis"
  - "Jay Patrikar"
date: "2023.12"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 NLP와 CV 분야의 foundation models를 로봇 공학에 적용하여 범용 로봇 시스템 개발을 가능하게 하는 방법을 탐구하는 종합 설문조사이며, 기존 vision/language foundation models의 활용과 robotics-specific foundation models의 설계를 다룬다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hu et al._2023_Toward General-Purpose Robots via Foundation Models A Survey and Meta-Analysis.pdf"
---

# Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis

> **저자**: Yafei Hu, Quanting Xie, Vidhi Jain, Jonathan Francis, Jay Patrikar, Nikhil Keetha, Seungchan Kim, Yaqi Xie, Tianyi Zhang, Hao-Shu Fang, Shibo Zhao, Shayegan Omidshafiei, Dong-Ki Kim, Ali-akbar Agha-mohammadi, Katia Sycara, Matthew Johnson-Roberson, Dhruv Batra, Xiaolong Wang, Sebastian Scherer, Chen Wang, Zsolt Kira, Fei Xia, Yonatan Bisk | **날짜**: 2023-12-14 | **URL**: [https://arxiv.org/abs/2312.08782](https://arxiv.org/abs/2312.08782)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: In this paper, we present a survey toward building general-purpose robots via foundation models. We mainly cat*

이 논문은 NLP와 CV 분야의 foundation models를 로봇 공학에 적용하여 범용 로봇 시스템 개발을 가능하게 하는 방법을 탐구하는 종합 설문조사이며, 기존 vision/language foundation models의 활용과 robotics-specific foundation models의 설계를 다룬다.

## Motivation

- **Known**: 기존 로봇 시스템은 특정 작업, 데이터셋, 환경에 맞춰 설계되며 광범위한 레이블 데이터와 작업 특화 모델이 필요하다. NLP와 CV 분야의 foundation models는 우수한 zero-shot 성능과 콘텐츠 생성 능력을 보여주고 있다.
- **Gap**: 기존 로봇 시스템은 distribution shift에 취약하고 일반화 능력이 제한적이며, foundation models이 로봇 공학에 어떻게 적용될 수 있는지, 그리고 로봇 공학 특화 foundation models이 어떤 형태여야 하는지에 대한 체계적 정리가 부족하다.
- **Why**: Foundation models는 데이터 부족, 일반화 문제, 안전성 불확실성 등 로봇 공학의 핵심 문제들을 해결할 수 있는 잠재력을 가지고 있으며, 이를 체계적으로 탐구하면 범용 로봇 개발의 실현 가능성을 높일 수 있다.
- **Approach**: 본 논문은 generalized formulation을 통해 foundation models의 로봇 적용 방식을 정의하고, 로봇 공학의 주요 과제들(generalization, data scarcity, uncertainty, task specification 등)을 분석한 후, 기존 vision/language models의 활용과 robotics-specific foundation models의 분류를 제시한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: In this paper, we present a survey toward building general-purpose robots via foundation models. We mainly cat*

- **체계적 택소노미 제시**: Vision Foundation Models (VFM), Vision Language Models (VLM), Large Language Models (LLM), Vision Language Action models (VLA) 등 다양한 foundation model 유형과 그 로봇 적용 방식을 포괄적으로 분류
- **도전 과제 분석**: Generalization, data scarcity, world model과 primitives 설계, task specification, uncertainty and safety 등 5개의 핵심 로봇 공학 문제를 식별하고 foundation models의 해결 가능성 논의
- **현황 조사**: Robot perception, task planning, action generation, action grounding, data generation, planning/control 강화 등 foundation models의 구체적 활용 영역을 상세히 검토
- **미래 방향 제시**: Cross-embodiment transfer, continual learning, world dynamics models, grounding 등 유망한 연구 방향과 과제를 제안
- **리소스 제공**: 설문 논문 및 관련 프로젝트를 포함한 living GitHub repository 제공으로 커뮤니티 지원

## How

![Figure 4](figures/fig4.webp)

*Figure 4: Comprehensive visualizations of the Open-X Embodiment and Droid Dataset encompassing robot morphologies, envir*

- VFM과 VLM을 로봇 perception에 적용하여 object detection, scene understanding, open-world visual recognition 능력 확보
- LLM과 VLM을 task planning에 활용하여 자연어 명령을 구조화된 계획으로 변환
- VLA models를 통한 end-to-end action generation으로 vision과 language input으로부터 직접 로봇 제어 신호 생성
- Action grounding 기법으로 추상적 동작을 구체적 로봇 제어(joint angles, waypoints 등)로 변환
- LLM과 VGM (Vision Generative Models)을 활용한 합성 데이터 생성으로 데이터 부족 문제 완화
- Prompting 기법을 통해 foundation models의 계획 및 제어 능력 강화
- 로봇 특화 foundation models 개발을 통한 다양한 embodiment과 작업에 대한 transfer learning 실현

## Originality

- 로봇 공학을 위한 foundation models의 개념을 처음으로 체계적으로 정의하고 분류한 종합 설문조사
- 기존 NLP/CV foundation models와 robotics-specific foundation models을 구분하여 각각의 역할과 한계를 명확히 함
- 로봇 공학의 전통적 도전 과제들(generalization, data scarcity, uncertainty, safety)을 foundation models 관점에서 재조명
- Vision Language Action (VLA) models와 같은 새로운 로봇 공학 모델 카테고리를 식별 및 분석
- living repository 형태의 동적 설문조사 제공으로 빠르게 변화하는 분야의 최신 동향 반영

## Limitation & Further Study

- **평가의 불균형**: 많은 robotics foundation models이 아직 초기 단계이며 일관된 벤치마크 부족으로 정량적 비교 어려움
- **실제 배포의 한계**: 대부분의 연구가 시뮬레이션 또는 제한된 실세계 환경에서 수행되어 일반화 능력의 실제 검증 부족
- **데이터 불균형**: 로봇 공학 데이터의 다양성이 NLP/CV 대비 현저히 낮으며, cross-embodiment transfer의 실제 효과가 제한적
- **안전성과 불확실성**: Foundation models의 hallucination 및 예측 불확실성에 대한 해결책이 여전히 미흡
- **Sim-to-real gap**: 시뮬레이션 환경에서의 성과가 실제 로봇에 완벽하게 전이되지 않는 문제 미해결
- **후속 연구 방향**: 더 대규모의 로봇 데이터셋 수집, 표준화된 평가 벤치마크 개발, 실시간 안전 검증 메커니즘 구축, 여러 embodiment 간의 지식 전이 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 로봇 공학에 foundation models를 적용하는 현황을 최초로 포괄적으로 정리한 중요한 설문조사로, 체계적인 택소노미와 명확한 도전 과제 분석을 제공하며, 향후 범용 로봇 개발을 위한 연구 로드맵을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation Models in Robotics는 동일한 로봇 foundation model 주제를 다루지만 응용과 도전 과제에 더 집중하는 다른 관점을 제공한다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Foundation Model Driven Robotics는 foundation model 기반 로봇공학에 대한 또 다른 종합적 리뷰를 제공한다.
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Pure VLA Models Survey는 foundation model 서베이를 VLA 모델에 특화하여 확장한 더 구체적인 연구 조사다.
- 🏛 기반 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — Multimodal Fusion Survey는 로봇 foundation model의 핵심 구성 요소인 다중모달 융합에 대한 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — 둘 다 VLA 모델에 대한 종합적 설문이지만 1608은 VLA에 특화된 반면 1590은 더 넓은 foundation model 관점을 제시합니다.
- 🏛 기반 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — foundation model 시대의 로봇 학습에 대한 포괄적 조사로 1590의 이론적 배경을 제공합니다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — General-Purpose Robots Survey는 foundation model driven robotics와 유사한 범위를 다루지만 범용 로봇 관점에서 다른 분석 틀을 제시합니다.
- 🔄 다른 접근: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — 로봇틱스 foundation model 응용과 foundation model 기반 범용 로봇은 동일한 기술의 현재 상태와 미래 비전을 다루는 서로 다른 관점이다.
- 🧪 응용 사례: [[papers/1404_Gemini_Robotics_Bringing_AI_into_the_Physical_World/review]] — 범용 로봇을 위한 foundation model 서베이는 Gemini Robotics가 제시한 AI의 물리 세계 적용 비전을 체계화함
- 🏛 기반 연구: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — General-Purpose Robots Survey가 EMLMs 리뷰의 foundation model 기반 로봇 개발 동향 분석의 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — 둘 다 embodied AI의 포괄적 조사이지만, 대규모 모델 서베이는 의사결정에, General-Purpose Robots 서베이는 foundation model 전반에 초점을 둔다.
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — 범용 로봇을 위한 foundation model 동향을 VLA 모델 관점에서 구체화한다.
- 🔗 후속 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — 범용 로봇을 위한 기초 모델 서베이를 확장하여 특히 언어 및 멀티모달 모델의 로봇 학습 적용에 집중한 전문적 조사를 제공한다.
- 🏛 기반 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — foundation model 기반 범용 로봇에 대한 종합적 조사가 VLA 모델 연구의 이론적 배경과 발전 방향을 제시한다.
- 🔗 후속 연구: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — General-Purpose Robots 조사가 EIIR의 산업 특화 프레임워크를 더 넓은 범용 로봇 관점으로 확장합니다.
- 🔄 다른 접근: [[papers/1305_Aligning_Cyber_Space_with_Physical_World_A_Comprehensive_Sur/review]] — Foundation Model을 통한 범용 로봇 개발이라는 유사한 목표를 다른 관점에서 접근한다.
