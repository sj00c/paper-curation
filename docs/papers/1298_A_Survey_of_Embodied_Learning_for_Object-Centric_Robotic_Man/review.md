---
title: "1298_A_Survey_of_Embodied_Learning_for_Object-Centric_Robotic_Man"
authors:
  - "Ying Zheng"
  - "Lei Yao"
  - "Yuejiao Su"
  - "Yi Zhang"
  - "Yi Wang"
date: "2024.08"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 object-centric robotic manipulation을 위한 embodied learning의 최신 동향을 체계적으로 조사하며, embodied perceptual learning, embodied policy learning, embodied task-oriented learning의 세 가지 주요 분야로 분류하여 종합적인 서베이를 제공한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zheng et al._2024_A Survey of Embodied Learning for Object-Centric Robotic Manipulation.pdf"
---

# A Survey of Embodied Learning for Object-Centric Robotic Manipulation

> **저자**: Ying Zheng, Lei Yao, Yuejiao Su, Yi Zhang, Yi Wang, Sicheng Zhao, Yiyi Zhang, Lap-Pui Chau | **날짜**: 2024-08-21 | **URL**: [https://arxiv.org/abs/2408.11537](https://arxiv.org/abs/2408.11537)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. An illustration of robotic manipulation system (left) and the typology of embodied learning methods for object-c*

본 논문은 object-centric robotic manipulation을 위한 embodied learning의 최신 동향을 체계적으로 조사하며, embodied perceptual learning, embodied policy learning, embodied task-oriented learning의 세 가지 주요 분야로 분류하여 종합적인 서베이를 제공한다.

## Motivation

- **Known**: Deep learning의 발전으로 computer vision과 NLP 분야에서 큰 성과를 이루었으나, 전통적인 machine learning은 정적 데이터셋에 의존한다. 로봇 조작을 위한 다양한 embodied learning 방법들이 제안되어 왔다.
- **Gap**: 기존 서베이들(특히 Cong et al. 2021)은 3D vision-based 방법에만 국한되어 있으며, 2021년 이후의 최신 연구(LLMs, NeRFs, Diffusion Models, 3D Gaussian Splatting 등)를 포함하지 않는다. 또한 policy learning과 task-oriented learning을 체계적으로 다루는 종합 서베이가 부재하다.
- **Why**: Object-centric robotic manipulation은 차세대 지능형 로봇 개발에 필수적이며, embodied learning을 통한 물리적 상호작용과 지각 피드백 기반의 학습은 전통적 data-driven 방식보다 로봇 조작에 특히 적합하다.
- **Approach**: 논문은 robotic manipulation 시스템의 세 가지 핵심 지능 측면(advanced perception, precise policy generation, task-orientation)에 따라 embodied learning 방법들을 체계적으로 분류하고, 최신 딥러닝 기술들의 응용을 포함하여 종합적으로 검토한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. An illustration of robotic manipulation system (left) and the typology of embodied learning methods for object-c*

- **체계적 분류체계**: Embodied learning을 3개 주요 분야(perceptual, policy, task-oriented)와 7개 세부 방향(data representation, pose estimation, affordance learning, policy representation, policy learning, object grasping, object manipulation)으로 계층적으로 분류
- **최신 기술 포함**: LLMs, NeRFs, Diffusion Models, 3D Gaussian Splatting 등 2021년 이후의 최신 AI 기술을 robotic manipulation에 적용한 연구들을 체계적으로 정리
- **다양한 데이터 표현 방식**: Image-based, 3D-aware, tactile-based 세 가지 representation 방식을 포괄적으로 다루고 비교
- **포괄적 자료 제공**: Public datasets, evaluation metrics, representative applications, current challenges, future research directions을 모두 포함하는 완전한 서베이 제공
- **상위 연구와의 비교**: 기존 41개 관련 서베이와의 차이점을 명확히 하고 본 논문의 우월성 입증

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. An illustration of robotic manipulation system (left) and the typology of embodied learning methods for object-c*

- Object-centric robotic manipulation의 시스템 아키텍처를 로봇 암, 센서, 말단 장치(그리퍼)로 구성하여 설명
- Embodied perceptual learning에서 image-based representation, 3D-aware representation(NeRF, 3D Gaussian Splatting 포함), tactile-based representation 방식들을 검토
- Object pose estimation을 instance-level, category-level, novel object 세 가지 수준으로 구분하여 분석
- Affordance learning을 supervised learning과 interaction-based learning으로 분류하여 정리
- Policy learning을 explicit policy, implicit policy, diffusion policy로 분류
- Policy learning 방법을 reinforcement learning, imitation learning 및 기타 방법으로 구분
- Task-oriented learning을 single-object grasping, multi-object grasping, non-dexterous manipulation, dexterous manipulation으로 세분화
- 각 세부 분야에 대해 대표 논문들을 수집, 분류하고 방법론, 성능, 한계를 비교 분석

## Originality

- 기존 Cong et al. (2021)의 3D vision-centric 접근을 벗어나 image, 3D-aware, tactile 세 가지 representation 방식을 균형있게 다룬 점
- 최신 generative models(Diffusion Models), foundation models(LLMs), novel 3D representation(3D Gaussian Splatting) 등을 robotic manipulation 맥락에서 체계적으로 정리한 점
- Policy learning과 task-oriented learning을 perceptual learning과 동등한 수준의 주요 분야로 격상하여 embodied learning의 전체 파이프라인을 통합적으로 제시한 점
- Object-centric manipulation이라는 명확한 초점으로 navigation, planning 등 다른 embodied AI 분야와 구분하고 집중도를 높인 점

## Limitation & Further Study

- 2024년 8월 프리프린트 기준이므로 그 이후의 최신 발전(예: multimodal LLMs의 급속한 발전)을 완전히 포함하지 못할 수 있음
- Real-world deployment의 성공률, 강건성, 일반화 능력에 대한 정량적 비교가 충분하지 않을 수 있음
- Sim-to-real transfer의 성능 격차와 해결 방안에 대한 심층 분석이 필요함
- 다중 모달(vision + tactile + force feedback) 통합 학습의 최적 방법에 대한 합의가 부재함
- 후속 연구는 (1) foundation models의 robot manipulation 적용, (2) 복잡한 다중 객체 상호작용 시나리오, (3) 실시간 제약 환경에서의 효율적 학습 방법 개발에 집중할 필요가 있음

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 object-centric robotic manipulation을 위한 embodied learning의 최신 동향을 체계적이고 포괄적으로 정리한 우수한 서베이이며, 기존 연구와 달리 최신 generative/foundation models을 포함하고 perception-policy-task의 통합적 관점을 제시함으로써 로봇 조작 분야 연구자들에게 매우 유용한 참고자료가 될 것으로 판단된다.

## Related Papers

- 🧪 응용 사례: [[papers/1354_Dex1B_Learning_with_1B_Demonstrations_for_Dexterous_Manipula/review]] — object-centric manipulation을 dexterous manipulation이라는 구체적 영역에 적용한다.
- 🏛 기반 연구: [[papers/1333_CLIPort_What_and_Where_Pathways_for_Robotic_Manipulation/review]] — 객체 중심 조작을 위한 시각적 이해의 기초가 되는 CLIPort 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — 공간적 어포던스 예측을 통해 object-centric manipulation을 확장한다.
- 🔗 후속 연구: [[papers/1357_Dexterous_Manipulation_through_Imitation_Learning_A_Survey/review]] — Dexterous Manipulation through Imitation Learning 서베이를 object-centric한 embodied learning 관점에서 확장하여 더 체계적인 분류를 제시합니다.
- 🏛 기반 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — Robot Learning in the Era of Foundation Models 서베이의 기초 위에 object-centric robotic manipulation에 특화된 embodied learning 관점을 추가한 연구입니다.
- 🔄 다른 접근: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — 둘 다 embodied AI의 포괄적 서베이이지만 A Survey of Embodied Learning은 object-centric manipulation에, Exploring Embodied는 multimodal large model에 중점을 둡니다.
