---
title: "1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey"
authors:
  - "Xuan Xiao"
  - "Jiahang Liu"
  - "Zhipeng Wang"
  - "Yanmin Zhou"
  - "Yong Qi"
date: "2023.11"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 Large Language Models(LLMs)과 multimodal foundation models를 로봇 학습에 적용하는 최신 기술을 체계적으로 조사하는 survey이며, manipulation, navigation, planning, reasoning의 네 가지 주요 영역에서 foundation model 기법의 적용 방식을 분석한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xiao et al._2023_Robot Learning in the Era of Foundation Models A Survey.pdf"
---

# Robot Learning in the Era of Foundation Models: A Survey

> **저자**: Xuan Xiao, Jiahang Liu, Zhipeng Wang, Yanmin Zhou, Yong Qi, Qian Cheng, Bin He, Shuo Jiang | **날짜**: 2023-11-24 | **URL**: [https://arxiv.org/abs/2311.14379](https://arxiv.org/abs/2311.14379)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig.1. Overall structure of the survey.*

이 논문은 Large Language Models(LLMs)과 multimodal foundation models를 로봇 학습에 적용하는 최신 기술을 체계적으로 조사하는 survey이며, manipulation, navigation, planning, reasoning의 네 가지 주요 영역에서 foundation model 기법의 적용 방식을 분석한다.

## Motivation

- **Known**: 전통적 로봇 학습은 imitation learning과 reinforcement learning으로 나뉘며, 이들은 일반화 부족, 환경 적응성 낮음, 계획 및 추론 능력 부족 등의 문제가 있다. 최근 ChatGPT의 등장과 함께 LLMs이 로봇 학습에 적용되기 시작했다.
- **Gap**: 기존 로봇 학습 survey는 단일 작업 중심이고 전통적 방법에 의존하고 있으며, foundation models을 활용한 멀티태스크 로봇 학습에 대한 종합적인 문헌 리뷰가 부족하다.
- **Why**: LLMs과 multimodal foundation models는 복잡한 작업 이해, 지속적 대화, zero-shot 추론 능력을 제공하여 로봇이 일반적 embodied AI로 진화할 수 있게 하며, 이는 산업, 의료, 서비스 로봇 등 실생활 응용에 매우 중요하다.
- **Approach**: 논문은 로봇 학습의 기술 진화, foundation models의 필수 준비 요소(simulator, dataset, framework), 그리고 네 가지 주요 로봇 학습 영역에서의 foundation model 적용 사례를 체계적으로 분석하며, 하드웨어-소프트웨어 분리, 동적 데이터, 인간과의 상호작용 시 일반화 성능 등의 미해결 문제를 논의한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig.1. Overall structure of the survey.*

- **기술 진화 체계화**: Teaching programming(kinesthetic teaching, teleoperation), reinforcement learning, embodied imitation learning, AIGC 기반 생성 모델의 네 단계로 로봇 학습 발전 과정을 정리
- **Foundation model 적용 범위 확대**: LLMs과 multimodal foundation models을 manipulation, navigation, planning, reasoning 네 가지 로봇 학습 주요 영역에 적용하는 방식을 분석
- **미해결 문제 규명**: 로봇 하드웨어-소프트웨어 분리, 동적 데이터의 중요성, 인간 상호작용 시 일반화 성능 등 현존 문헌에서 간과된 핵심 이슈 제시
- **미래 연구 방향 제시**: Multimodal interaction (특히 dynamics data), 로봇 전용 foundation models, AI alignment 등 향후 중점 연구 영역 제안

## How

![Figure 2](figures/fig2.webp)

*Fig.2. Technical Evolution[27-30].*

- 로봇 학습의 역사적 진화를 네 단계로 분류하여 각 단계의 특성, 장단점, 기술적 한계를 분석
- Simulator, dataset, foundation model framework 등 foundation models 도입을 위한 필수 인프라 요소 검토
- Manipulation(grasping, object manipulation), navigation(path planning, obstacle avoidance), planning(task decomposition), reasoning(common sense reasoning, commonsense knowledge)의 네 영역별로 foundation model 적용 사례 조사
- Multimodal data(2D&3D vision, LiDAR, voice, IMU 등)를 활용한 perception-action loop 폐쇄 전략 분석
- 정성적 리뷰 방식으로 선행 연구의 강점과 약점을 비교분석하고 패턴 도출

## Originality

- Foundation models 시대라는 명확한 시간적 프레임을 설정하여 LLMs 등장 이후의 로봇 학습 변화를 체계적으로 조사한 최초의 종합 survey
- 전통적 로봇 학습과 foundation models의 결합 방식을 네 가지 주요 작업 영역으로 분류하여 분석함으로써 새로운 분류체계 제시
- 하드웨어-소프트웨어 decoupling, dynamics data의 중요성, 인간 상호작용 시 일반화 등 기존 로봇 학습 논문에서 간과된 실제 문제들을 명시적으로 규명
- Zero-shot 학습과 embodied AI의 결합 가능성을 제시하여 로봇 학습의 새로운 패러다임 제안

## Limitation & Further Study

- Survey 형식이므로 새로운 알고리즘이나 구체적인 기술적 해법을 제시하지 않으며, 각 영역별 foundation model 적용의 정량적 성능 비교가 부족
- Hardware-software decoupling, dynamics data, generalization with human 등 제시된 미해결 문제에 대한 구체적인 해결방안이나 실험적 검증이 없음
- Simulator와 real world 간의 sim-to-real transfer 문제의 중요성은 언급되지만 이를 극복하는 방법론에 대한 상세 분석 부족
- **후속연구 방향**: Foundation models 자체의 수렴, inference latency, real-time control 가능성 등 로봇 배포 관점의 실용적 문제 해결 필요; Multimodal data fusion과 dynamics modeling을 위한 새로운 foundation model architecture 개발; Embodied AI의 안전성과 AI alignment 확보를 위한 방법론 수립

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 LLMs와 multimodal foundation models의 로봇 학습 적용이라는 새로운 학제간 분야를 체계적으로 정리한 중요한 survey로서, 기술 진화 단계화, 네 가지 주요 작업 영역 분류, 그리고 미해결 실제 문제의 명시적 규명을 통해 향후 embodied AI 연구의 로드맵을 제시한다. 다만 구체적인 기술적 해법과 정량적 성능 비교가 부족하여 실제 구현 단계의 연구자들을 위한 가이드로서의 역할은 제한적이다.

## Related Papers

- 🔄 다른 접근: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation Models in Robotics와 함께 로봇 분야의 기초 모델을 조망하지만 이 연구는 LLM/multimodal 모델에, 다른 연구는 전반적 응용에 집중한다.
- 🔗 후속 연구: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — 범용 로봇을 위한 기초 모델 서베이를 확장하여 특히 언어 및 멀티모달 모델의 로봇 학습 적용에 집중한 전문적 조사를 제공한다.
- 🏛 기반 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Foundation models 시대의 로봇 학습 전반을 다룬 survey가 Pure VLA 모델들의 구체적 분류와 분석의 이론적 배경을 제공한다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — 두 survey 모두 foundation model driven robotics를 다루지만 하나는 학습 중심, 다른 하나는 전반적 로봇 시스템 관점에서 접근한다.
- 🏛 기반 연구: [[papers/1298_A_Survey_of_Embodied_Learning_for_Object-Centric_Robotic_Man/review]] — Robot Learning in the Era of Foundation Models 서베이의 기초 위에 object-centric robotic manipulation에 특화된 embodied learning 관점을 추가한 연구입니다.
- 🏛 기반 연구: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — foundation model 시대의 로봇 학습에 대한 기본적인 조망을 제공하는 선행 연구이다.
- 🔗 후속 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation Models in Robotics와 Robot Learning in the Era of Foundation Models는 로봇틱스에서 foundation model 활용에 대한 상호 보완적인 종합 조사이다.
- 🔄 다른 접근: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — Robot Learning in the Era of Foundation Models는 EMLMs와 유사한 주제를 다루지만 학습 관점에서 다른 분석 프레임워크를 제시합니다.
- 🏛 기반 연구: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — Robot Learning in the Era of Foundation Models의 기본 개념을 계층적/end-to-end 의사결정과 학습으로 체계화한다.
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Pure VLA 모델들의 포괄적 분류가 foundation models 시대 로봇 학습 survey를 VLA 특화 관점으로 심화 확장한다.
- 🏛 기반 연구: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — foundation model 시대의 로봇 학습에 대한 포괄적 조사로 1590의 이론적 배경을 제공합니다.
- 🔗 후속 연구: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — Robot Learning in the Era of Foundation Models는 EIIR의 산업 특화 접근을 학습 관점에서 확장한 연구임
