---
title: "1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G"
authors:
  - "Xinghang Li"
  - "Peiyan Li"
  - "Long Qian"
  - "Minghuan Liu"
  - "Dong Wang"
date: "2024.12"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델 개발 시 VLM 백본 선택, 아키텍처 설계, 데이터 활용 시점이라는 세 가지 핵심 요소를 체계적으로 분석하고, 이를 통해 RoboVLMs 프레임워크를 제안하여 로봇 조작 작업에서 최고 성능을 달성한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robot_Policy_Learning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Deep_Reinforcement_Learning_Applications"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2024_What Matters in Building Vision-Language-Action Models for Generalist Robots.pdf"
---

# What Matters in Building Vision-Language-Action Models for Generalist Robots

> **저자**: Xinghang Li, Peiyan Li, Long Qian, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Xinlong Wang, Di Guo, Tao Kong, Hanbo Zhang, Huaping Liu | **날짜**: 2024-12-18 | **URL**: [https://arxiv.org/abs/2412.14058](https://arxiv.org/abs/2412.14058)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: This work mainly considers three key ingredients for building VLAs based on VLMs: How to formulate the problem*

Vision-Language-Action (VLA) 모델 개발 시 VLM 백본 선택, 아키텍처 설계, 데이터 활용 시점이라는 세 가지 핵심 요소를 체계적으로 분석하고, 이를 통해 RoboVLMs 프레임워크를 제안하여 로봇 조작 작업에서 최고 성능을 달성한다.

## Motivation

- **Known**: VLM이 대규모 웹 데이터로 학습되어 강력한 멀티모달 표현 능력을 갖추고 있으며, 최근 여러 VLA 기반 로봇 정책들이 유망한 결과를 보이고 있다는 것이 알려져 있다.
- **Gap**: 기존 VLA 연구들이 다양한 VLM 백본, 아키텍처, 데이터 조합을 사용하지만, 이러한 설계 선택이 로봇 조작 성능에 미치는 영향을 종합적으로 분석한 연구가 부족하다.
- **Why**: VLA의 성능에 영향을 미치는 핵심 설계 요소를 체계적으로 파악하고 명확한 가이드라인을 제시함으로써 향후 일반화된 로봇 정책 개발을 효율적으로 진행할 수 있기 때문이다.
- **Approach**: 8개 이상의 VLM 백본, 4가지 정책 아키텍처, 600개 이상의 실험 설계를 통해 3가지 핵심 질문(어떤 백본, 어떤 아키텍처, 언제 cross-embodiment 데이터 추가)에 대한 답을 체계적으로 찾으며, 이를 바탕으로 유연한 RoboVLMs 프레임워크를 개발한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: The experimental results for RoboVLMs in Simulations and real world.*

- **VLM 백본 분석**: Flamingo, LLaVA, MoonDream, PaliGemma, Qwen, KOSMOS 등 다양한 VLM 구조의 로봇 조작 작업에 대한 효과를 비교 분석
- **아키텍처 설계 가이드**: One-step 모델링, 히스토리 모델링(Interleaved vs Policy Head), 연속/이산 액션 스페이스의 장단점을 명확히 제시
- **데이터 활용 전략**: In-domain 데이터와 cross-embodiment 데이터의 최적 활용 시점과 방식을 규명
- **RoboVLMs 프레임워크**: 새로운 VLM을 쉽게 통합할 수 있고 다양한 설계 선택을 자유롭게 조합 가능한 확장 가능한 프레임워크 제시
- **최고 성능 달성**: 시뮬레이션 환경 3개 작업 및 실제 로봇 실험에서 state-of-the-art 성능 달성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: This work mainly considers three key ingredients for building VLAs based on VLMs: How to formulate the problem*

- 8개 이상의 서로 다른 구조와 크기의 VLM 백본(다양한 visual encoder, fusion mechanism, data scale)에 대한 체계적 비교
- VLA 아키텍처를 히스토리 정보 포함 여부(One-Step vs Historical)와 통합 방식(Interleaved vs Policy Head)으로 분류 후 성능 비교
- 액션 스페이스 설계(연속 vs 이산)에 따른 정책 성능 평가
- Cross-embodiment 데이터를 pre-training 단계와 post-training 단계에 각각 활용했을 때의 영향 분석
- In-domain 로봇 데이터와 다양한 임보디먼트로부터의 데이터를 혼합 활용할 때의 최적 비율과 시점 규명
- Open-source 프레임워크 제공으로 재현성 및 확장성 확보(코드, 모델, 데이터셋, 툴킷 공개)

## Originality

- 로봇 VLA 연구에서 처음으로 600개 이상의 대규모 체계적 실험을 통해 백본, 아키텍처, 데이터 선택의 상호작용을 종합 분석
- 기존 개별 작업 중심의 연구에서 벗어나 설계 선택의 일반화 가능한 가이드라인을 제시하는 메타 수준의 연구 수행
- VLM의 다양한 구조(visual encoder 종류, fusion mechanism 등)가 로봇 제어에 미치는 차별화된 영향을 최초로 실증적으로 규명
- Cross-embodiment 데이터와 in-domain 데이터의 최적 조합 전략을 정량적으로 규명한 첫 연구

## Limitation & Further Study

- 실험이 주로 탁상 조작(tabletop manipulation) 작업에 집중되어 있어 다른 로봇 도메인(이동 조작, 인휴먼 로봇 등)에 대한 일반화 검증 필요
- VLM 백본 분석이 특정 시점(논문 작성 시점)의 공개된 모델들로 제한되어 빠르게 진화하는 VLM 환경에서의 지속적 업데이트 필요
- 시뮬레이션과 실제 환경 간 성능 간격이 존재하며, 실제 환경에서의 더 광범위한 검증이 요구됨
- 계산 비용 분석이 부족하여 각 설계 선택의 효율성-성능 트레이드오프가 명확하지 않음
- 다양한 언어, 문화적 배경의 지시 이해도에 대한 평가 부재

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLA 개발의 핵심 설계 요소를 체계적으로 분석한 중요한 메타 연구로, 광범위한 실증 실험을 통해 실질적인 가이드라인을 제시하고 확장 가능한 프레임워크를 제공함으로써 로봇 기초 모델 연구 커뮤니티에 상당한 기여를 할 것으로 예상된다.

## Related Papers

- 🔄 다른 접근: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — 둘 다 효과적인 VLA 모델 구축을 다루지만 이 논문은 체계적 분석을, VLA-0은 단순한 설계를 제안한다.
- 🏛 기반 연구: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — Prismatic VLM의 시각-언어 모델 설계 공간 연구가 VLA 모델의 백본 선택과 아키텍처 설계 분석의 기반이 되었다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 오픈소스 프레임워크가 범용 VLA 모델 개발 시 고려해야 할 핵심 요소들의 실험적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — 로봇공학에서의 신경망 스케일링 법칙 연구가 VLA 모델의 데이터 활용과 아키텍처 스케일링 분석에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Pure VLA Models 서베이가 VLA 모델 구축에 대한 포괄적인 다른 관점과 체계적 분석을 제공한다.
- 🔗 후속 연구: [[papers/1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to/review]] — VLA Models Anatomy가 VLA 모델 구축의 핵심 요소들을 모듈별로 더 상세히 분석하고 확장한다.
- 🏛 기반 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — VLA 모델의 전반적인 개념과 발전사를 제공하여 구체적인 구현 요소 분석의 이론적 배경을 마련한다.
- 🏛 기반 연구: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Generalist robot policy의 기본 개념을 제공하여 VLA 모델 설계에서 고려해야 할 핵심 요소들의 이론적 근거를 마련한다.
- 🔗 후속 연구: [[papers/1446_Large_VLM-based_Vision-Language-Action_Models_for_Robotic_Ma/review]] — What Matters in Building VLA Models은 대규모 VLM 기반 VLA의 핵심 설계 요소를 실용적 관점에서 심화함
- 🔗 후속 연구: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — 로봇 스케일링 법칙을 vision-language-action model 구축에 적용한 확장 연구
- 🔄 다른 접근: [[papers/1513_Parallels_Between_VLA_Model_Post-Training_and_Human_Motor_Le/review]] — VLA 모델 구축에서 human motor learning vs engineering optimization의 다른 관점
- 🏛 기반 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — 일반적인 VLA 모델 구축에 중요한 요소들을 식별하여 1608의 VLA 개념과 진전 분석에 실증적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — What Matters in Building VLA Models은 일반 목적 VLA 구축의 핵심 요소를 식별하여 실제 배포 가이드를 보완합니다.
- 🔄 다른 접근: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — 둘 다 VLA 모델 구축의 핵심 요소를 분석하지만 VLA-0은 구조 변경 없는 단순함을, 후자는 체계적 설계 분석을 강조한다.
