---
title: "1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve"
authors:
  - "Dapeng Zhang"
  - "Jing Sun"
  - "Chenghui Hu"
  - "Xiaoyan Wu"
  - "Zhenlong Yuan"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Vision Language Action (VLA) 모델을 체계적으로 분류하고 분석하는 포괄적 서베이로, autoregression-based, diffusion-based, reinforcement-based, hybrid, specialized methods로 VLA 접근법을 분류하여 300개 이상의 최근 연구를 종합한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Pure Vision Language Action (VLA) Models A Comprehensive Survey.pdf"
---

# Pure Vision Language Action (VLA) Models: A Comprehensive Survey

> **저자**: Dapeng Zhang, Jing Sun, Chenghui Hu, Xiaoyan Wu, Zhenlong Yuan, Rui Zhou, Fei Shen, Qingguo Zhou | **날짜**: 2025-09-23 | **URL**: [https://arxiv.org/abs/2509.19012](https://arxiv.org/abs/2509.19012)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: Vision-Language-Action Taxonomy: From Autoregression-based, Diffusion-based, to Reinforcement-based and*

본 논문은 Vision Language Action (VLA) 모델을 체계적으로 분류하고 분석하는 포괄적 서베이로, autoregression-based, diffusion-based, reinforcement-based, hybrid, specialized methods로 VLA 접근법을 분류하여 300개 이상의 최근 연구를 종합한다.

## Motivation

- **Known**: Vision Language Model (VLM)과 Large Language Model (LLM)의 발전으로 로봇의 지각, 이해, 행동 능력이 향상되었으나, 이들 능력을 통합한 VLA 시스템의 체계적 분류와 분석이 부족하다.
- **Gap**: 기존 서베이는 VLM 기초 모델이나 로봇 조작의 전반적 개요에만 초점을 맞추었으며, pure VLA 방법론의 정립된 분류체계와 포괄적 분석이 부재하다.
- **Why**: VLA는 전통적 정책 기반 제어에서 일반화된 로봇공학으로의 패러다임 전환을 대표하며, 복잡한 동적 환경에서 로봇 조작과 의사결정의 실용화를 위해 체계적 이해가 필수적이다.
- **Approach**: VLA 모델의 행동 생성 전략(action-generation strategy)을 기준으로 autoregression-based, diffusion-based, reinforcement-based, hybrid, specialized methods의 5가지 패러다임으로 분류하고, 각 방법의 동기, 핵심 전략, 구현을 상세 분석한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Organization and Structure of the VLA Survey.*

- **VLA 방법론의 체계적 분류**: pure VLA 방법에 대한 명확한 분류체계를 제시하여 행동 생성 전략에 따른 접근법의 차별화된 특성을 파악 가능하게 함
- **포괄적 리소스 개요**: VLA 모델 학습 및 평가에 필수적인 데이터셋, 벤치마크, simulation platform에 대한 종합적 개요 제공
- **응용 도메인 분석**: robotic arm, quadruped robot, humanoid, wheeled robot 등 다양한 로봇 플랫폼에서의 VLA 배포 현황 평가
- **향후 방향 제시**: 데이터 제약, 추론 속도, 안전성 등 핵심 과제를 식별하고 확장 가능한 범용 VLA 방법 개발을 위한 미래 연구 방향 제안

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Illustration of various VLA skeleton.*

- Vision-Language-Action taxonomy 개발: autoregression-based, diffusion-based, reinforcement-based, hybrid, specialized methods로 분류하고 시간 축을 따라 발전 추이 시각화
- 각 패러다임별 심층 분석: 동기(motivation), 핵심 전략(core strategy), 구현 메커니즘(implementation mechanism)을 상세히 검토
- 응용 시나리오 매핑: 로봇 팔, 사족 로봇, 휴머노이드, 자율주행 등 다양한 로봇 유형별 VLA 활용 사례 체계화
- 리소스 인벤토리 구축: 주요 데이터셋, 벤치마크, simulation platform을 조사하여 VLA 개발 생태계 파악
- 문헌 메타분석: 300개 이상의 최근 연구를 종합하여 현황 파악 및 트렌드 분석

## Originality

- Pure VLA 방법론에 특화된 최초의 포괄적 서베이: 기존 VLM 중심이나 로봇공학 전체 역사 중심 서베이와 달리 VLA의 행동 생성 전략을 중심으로 분류
- 5가지 패러다임 분류체계의 제시: autoregression, diffusion, reinforcement learning, hybrid, specialized methods의 상호 연관성과 차별성을 명확히 함
- 멀티모달-행동 통합 프레임워크 분석: 시각, 언어, 행동의 통합 시퀀스 모델링 관점에서 VLA의 고유한 특성 해석

## Limitation & Further Study

- 서베이의 시간 제약성: 300개 연구 수집 이후 신속히 발전하는 VLA 분야의 최신 방법론을 완전히 포괄하지 못할 가능성
- VLA 평가 메트릭 표준화 부재: 다양한 도메인과 데이터셋의 벤치마크가 이질적이어서 방법론 간 직접 비교의 어려움
- 현실-시뮬레이션 갭: 대부분 연구가 시뮬레이션 환경에서 검증되며 실제 로봇 배포의 일반화 성능에 대한 평가 부족
- **후속 연구 방향**: (1) 데이터 효율성 증대를 위한 few-shot, zero-shot VLA 방법 개발, (2) 실시간 추론을 위한 경량 VLA 모델 연구, (3) 안전성 보증 메커니즘 통합, (4) 크로스 도메인 일반화 능력 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 서베이는 VLA 분야의 급속한 발전 속에서 처음으로 체계적인 분류체계를 제시하고 300개 이상의 연구를 종합하여 현황 맵핑을 제공함으로써, VLA 연구자와 로봇공학자들에게 높은 학술적 가치를 제공한다. 다만 시뮬레이션-현실 갭, 평가 메트릭 표준화, 최신 방법론 수용 측면의 개선이 향후 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — Pure VLA 모델들의 포괄적 분류가 foundation models 시대 로봇 학습 survey를 VLA 특화 관점으로 심화 확장한다.
- 🏛 기반 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation Models in Robotics의 전반적 분석이 VLA 모델 survey의 이론적 배경과 분류 체계를 제공한다.
- 🔄 다른 접근: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — 두 survey 모두 VLA 모델을 다루지만 하나는 pure VLA에, 다른 하나는 broader VLA concepts에 집중하는 상호보완적 관점이다.
- 🏛 기반 연구: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Foundation Model Driven Robotics 서베이가 VLA 모델 연구의 전반적 맥락을 제공한다.
- 🔗 후속 연구: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — 범용 로봇을 위한 foundation model 동향을 VLA 모델 관점에서 구체화한다.
- 🔄 다른 접근: [[papers/1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to/review]] — Pure VLA 모델에 대한 포괄적 서베이로 VLA 구조 분석을 보완한다.
- 🔗 후속 연구: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — 순수 VLA 모델에 대한 연구를 LLM과 VLM을 포함한 더 넓은 foundation model 관점으로 확장했다.
- 🔗 후속 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Pure Vision Language Action Models의 VLA 특화 조사가 Foundation Models in Robotics의 더 광범위한 foundation model 응용 연구로 확장된 관계이다.
- 🔄 다른 접근: [[papers/1446_Large_VLM-based_Vision-Language-Action_Models_for_Robotic_Ma/review]] — 둘 다 VLA 모델의 체계적 분석이지만, Large VLM-based 서베이는 로봇 매니퓰레이션에, Pure VLA 서베이는 VLA 모델 전반에 초점을 둔다.
- 🔗 후속 연구: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — VLA 모델 서베이에서 제시된 설계 원칙들을 Prismatic VLMs가 체계적으로 검증한다.
- 🏛 기반 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — Foundation models 시대의 로봇 학습 전반을 다룬 survey가 Pure VLA 모델들의 구체적 분류와 분석의 이론적 배경을 제공한다.
- 🔗 후속 연구: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — Pure VLA Models Survey는 foundation model 서베이를 VLA 모델에 특화하여 확장한 더 구체적인 연구 조사다.
- 🔄 다른 접근: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — Pure VLA Models 서베이가 VLA 모델 구축에 대한 포괄적인 다른 관점과 체계적 분석을 제공한다.
- 🔗 후속 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — VLN survey의 체계적 분류가 Pure VLA Models survey와 결합되어 vision-language-action 전반에 대한 더 포괄적인 이해를 제공한다.
- 🏛 기반 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — Pure VLA 모델에 대한 기존 종합 조사가 80개 이상 VLA 모델을 분석하는 더 포괄적인 리뷰의 기반이 되었다.
- 🔄 다른 접근: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — 두 리뷰 논문 모두 VLA 모델을 다루지만 실제 배포 vs 순수 VLA 모델 설계에 중점을 두어 서로 보완적입니다.
- 🔄 다른 접근: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — 순수 VLA 모델 포괄 서베이와 언어 조건부 조작 서베이가 다른 범위의 분석을 제공합니다.
