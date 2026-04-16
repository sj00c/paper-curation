---
title: "1463_LOVON_Legged_Open-Vocabulary_Object_Navigator"
authors:
  - "Daojie Peng"
  - "Jiahang Cao"
  - "Qiang Zhang"
  - "Jun Ma"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "LOVON은 LLM 기반 계층적 작업 계획과 open-vocabulary 시각 감지를 통합하여 동적이고 비구조화된 환경에서 legged robot의 장시간 객체 네비게이션을 가능하게 하는 통합 프레임워크이다. Laplacian Variance Filtering 등의 기법으로 실제 환경의 시각적 불안정성을 해결하고 여러 legged robot 플랫폼에서 검증되었다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Semantic_Navigation_Exploration"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Peng et al._2025_LOVON Legged Open-Vocabulary Object Navigator.pdf"
---

# LOVON: Legged Open-Vocabulary Object Navigator

> **저자**: Daojie Peng, Jiahang Cao, Qiang Zhang, Jun Ma | **날짜**: 2025-07-09 | **URL**: [https://arxiv.org/abs/2507.06747](https://arxiv.org/abs/2507.06747)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of LOVON’s pipeline. First, the LLM task planner reconfigures the human’s task into basic instructions,*

LOVON은 LLM 기반 계층적 작업 계획과 open-vocabulary 시각 감지를 통합하여 동적이고 비구조화된 환경에서 legged robot의 장시간 객체 네비게이션을 가능하게 하는 통합 프레임워크이다. Laplacian Variance Filtering 등의 기법으로 실제 환경의 시각적 불안정성을 해결하고 여러 legged robot 플랫폼에서 검증되었다.

## Motivation

- **Known**: LLM은 장시간 작업 계획에 효과적이고 open-vocabulary 시각 감지 모델(Grounding DINO 등)은 미리 정의되지 않은 객체를 인식할 수 있다. Legged robot은 바퀴 로봇보다 지형 적응성이 우수하다.
- **Gap**: 기존 방법들은 LLM 기반 계획, open-vocabulary 감지, legged robot 이동성을 효과적으로 통합하지 못하며, 로봇 운동으로 인한 시각 지터, 가림, 목표 손실 등 실제 환경의 도전 과제를 해결하지 못한다. 또한 장시간 다중 목표 작업을 비구조화된 환경에서 수행하는 것이 충분히 탐색되지 않았다.
- **Why**: 장시간 복합 작업을 비구조화된 환경에서 자율적으로 수행하는 legged robot은 실제 산업 및 서비스 로봇 응용에서 중요하며, LLM과 open-vocabulary 시각의 최신 발전을 활용하면 이전에 불가능했던 수준의 적응성과 일반화를 달성할 수 있다.
- **Approach**: LLM으로 장시간 작업을 세부 subtask로 분해하고, open-vocabulary 감지 모델로 실시간 객체 인식을 수행하며, language-to-motion model로 지시사항과 시각 피드백을 동작 벡터로 변환한다. Laplacian Variance Filtering으로 시각적 흔들림을 완화하고 robot execution logic으로 robust한 작업 완료를 보장한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Object navigation of legged robots in diverse open-world scenarios.*

- **통합 프레임워크 개발**: LLM, open-vocabulary 감지, language-to-motion model을 통합하여 복잡한 장시간 네비게이션 작업 계획 및 실행이 가능하다.
- **시각 안정화 기법**: Laplacian Variance Filtering을 통해 legged robot 운동으로 인한 동적 블러링과 시각 지터를 효과적으로 해결한다.
- **멀티 플랫폼 검증**: Unitree Go2, B2, H1-2 등 다양한 legged robot에서 장시간 탐색, 감지, 네비게이션 작업을 성공적으로 수행함을 입증한다.
- **Plug-and-play 호환성**: 여러 legged robot 플랫폼에 즉시 적용 가능한 모듈식 설계로 실제 로봇 응용의 실용성을 보장한다.

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of LOVON’s pipeline. First, the LLM task planner reconfigures the human’s task into basic instructions,*

- LLM 기반 Task Planner: 사용자 지시사항을 구조화된 subtask와 구체적 명령어(속도, 목표 객체 등)로 분해
- Instruction Object Extractor (IOE): 각 subtask에서 목표 객체를 추출하여 detection 모델에 제공
- Laplacian Variance Filtering: 입력 영상에 Laplacian filter를 적용하여 고주파 잡음 제거 및 안정화
- Open-vocabulary Detector: 전처리된 영상에서 실시간으로 목표 객체 감지 및 bounding box 정보 획득
- Language-to-Motion Model: Transformer 기반 모델로 instruction, detection 결과, mission/search state를 입력받아 [Vx, Vy, θ] 동작 벡터 생성
- Robot Execution Logic: mission state(목표 달성 중)와 search state(목표 탐색 중)에 따라 적응적 동작 전환 및 피드백 루프 구성

## Originality

- LLM, open-vocabulary 감지, legged robot 이동성을 처음으로 통합한 장시간 object navigation 시스템 제안
- Legged robot의 고유한 운동 특성(지터, 블라인드 존)에 맞춘 Laplacian Variance Filtering 기법으로 시각 안정화 문제를 해결
- Language-to-Motion Model에 mission state와 search state를 명시적으로 입력하여 task 적응성과 robustness를 향상
- 다중 legged robot 플랫폼(Go2, B2, H1-2)에서 동시에 검증하여 일반화 가능성을 입증

## Limitation & Further Study

- Laplacian Variance Filtering은 과도한 모션 블러에서 효과가 제한될 수 있으며, 더 정교한 동적 이미지 안정화 기법의 필요성 존재
- LLM의 hallucination이나 부정확한 작업 분해 가능성에 대한 error handling mechanism이 상세히 제시되지 않음
- 실험이 주로 실내/제어된 환경에서 수행되었으며, 극단적 날씨, 심한 지형 변화 등 극한 조건에서의 성능 미검증
- 시뮬레이션 환경(Gym-Unreal)과 실제 환경 간의 domain gap이 완전히 해소되지 않음
- 후속 연구로는 multimodal LLM을 통한 시각-언어 통합 이해 강화, reinforcement learning을 통한 동적 환경 학습, 여러 robot의 협력 작업 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LOVON은 LLM 기반 계획과 open-vocabulary 감지를 legged robot과 처음으로 통합하여 비구조화된 환경에서 장시간 object navigation을 달성한 혁신적인 시스템이다. 실제 환경 도전(시각 지터, 목표 손실)에 대한 맞춤형 해결책과 다중 플랫폼 검증을 통해 높은 실용성과 일반화 가능성을 입증하였으나, 극한 환경 성능과 에러 처리 mechanism의 보강이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — 동일한 open-vocabulary 객체 네비게이션 문제에 대해 legged robot vs wheeled robot 플랫폼에서의 서로 다른 구현 방식을 보여준다.
- 🔗 후속 연구: [[papers/1367_DivScene_Towards_Open-Vocabulary_Object_Navigation_with_Larg/review]] — open-vocabulary 객체 네비게이션의 기본 개념을 동적 환경과 legged robot으로 확장하여 더 복잡한 실제 환경에서의 적용을 다룬다.
- 🏛 기반 연구: [[papers/1491_NaVILA_Legged_Robot_Vision-Language-Action_Model_for_Navigat/review]] — legged robot의 vision-language-action 통합에 대한 이론적 기반을 제공하여 LOVON의 다중모달 통합 프레임워크 설계에 영감을 준다.
- 🔗 후속 연구: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — 강화학습 기반 휴머노이드 보행을 객체 네비게이션과 결합하여 legged robot의 장시간 탐색을 가능하게 했다.
- 🧪 응용 사례: [[papers/1486_Multimodal_Perception_for_Goal-oriented_Navigation_A_Survey/review]] — 멀티모달 네비게이션의 이론적 프레임워크가 LOVON의 다리 로봇 개방형 어휘 객체 네비게이션에 실제 적용된다.
- 🔗 후속 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — OctoNav의 일반화된 네비게이션이 LOVON의 다리 로봇 개방형 어휘 객체 네비게이션과 결합되어 더 복잡한 지형에서의 네비게이션을 실현한다.
