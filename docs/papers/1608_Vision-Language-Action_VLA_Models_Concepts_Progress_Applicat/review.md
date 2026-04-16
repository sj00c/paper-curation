---
title: "1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat"
authors:
  - "Ranjan Sapkota"
  - "Yang Cao"
  - "Konstantinos I. Roumeliotis"
  - "Manoj Karkee"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델은 시각 인식, 자연어 이해, 구체화된 행동을 단일 계산 프레임워크에서 통합하는 혁신적인 AI 접근법을 제시한다. 이 종합 리뷰는 지난 3년간 발표된 80개 이상의 VLA 모델을 분석하여 개념, 진전, 응용, 도전을 체계적으로 정리한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Sapkota et al._2025_Vision-Language-Action (VLA) Models Concepts, Progress, Applications and Challenges.pdf"
---

# Vision-Language-Action (VLA) Models: Concepts, Progress, Applications and Challenges

> **저자**: Ranjan Sapkota, Yang Cao, Konstantinos I. Roumeliotis, Manoj Karkee | **날짜**: 2025-05-07 | **URL**: [https://arxiv.org/abs/2505.04769](https://arxiv.org/abs/2505.04769)

---

## Essence


Vision-Language-Action (VLA) 모델은 시각 인식, 자연어 이해, 구체화된 행동을 단일 계산 프레임워크에서 통합하는 혁신적인 AI 접근법을 제시한다. 이 종합 리뷰는 지난 3년간 발표된 80개 이상의 VLA 모델을 분석하여 개념, 진전, 응용, 도전을 체계적으로 정리한다.

## Motivation

- **Known**: Vision-Language Models (VLM)는 시각과 언어를 결합하여 다중 모드 이해를 달성했으나, 이를 실제 로봇 행동으로 변환하는 능력이 부족했다. 기존 로봇 시스템은 비전, 언어, 행동이 분리되어 작동하여 일반화와 적응성이 제한적이었다.
- **Gap**: VLM과 로봇 제어 사이의 명확한 통합 격차가 존재했으며, 시각 인식, 언어 이해, 모터 제어를 동시에 수행하는 단일 통합 프레임워크가 부재했다. 기존 파이프라인은 새로운 작업이나 환경에 유연하게 적응할 수 없었다.
- **Why**: VLA 모델은 로봇이 시각적으로 인지하고, 언어 지시를 이해하고, 적절한 행동을 동적으로 실행할 수 있도록 함으로써 embodied AI의 근본적인 한계를 극복한다. 이는 자율 주행차, 의료 로봇, 농업 자동화 등 다양한 실제 응용 분야에서 지능형 자율 행동을 가능하게 한다.
- **Approach**: 이 리뷰는 체계적 문헌 검토 방법론을 채택하여 VLA 시스템의 개념적 기초, 아키텍처 혁신, 효율적 학습 전략, 실시간 추론 가속화를 다룬다. 또한 자율 주행차, 의료/산업 로봇, 정밀 농업, 휴머노이드 로봇, AR 등 다양한 응용 분야를 탐색하고 agentic adaptation과 cross-embodiment 계획을 통한 해결책을 제시한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Mind map illustrating VLA model ecosystem: progress in training efficiency (architectural innovations, data/pa*

- **포괄적 VLA 모델 분석**: 지난 3년간 발표된 80개 이상의 VLA 모델을 체계적으로 분석하고 분류
- **5개 주제별 구조화**: VLA 개념, 진전, 응용, 도전을 5개 테마 기둥으로 조직
- **아키텍처 혁신 정리**: vision-language models, action planners, hierarchical controllers의 통합 방식 체계화
- **다양한 응용 분야 매핑**: 자율 주행차, 의료 로봇, 산업 로봇, 정밀 농업, 휴머노이드 로봇, AR 등에서의 VLA 응용 분석
- **해결 방안 제시**: agentic AI adaptation, cross-embodiment generalization, neuro-symbolic planning 등 구체적 해결책 제안
- **미래 로드맵 제공**: VLA, VLM, agentic AI의 수렴을 통한 socially aligned adaptive general-purpose embodied agents 달성 방향 제시

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Mind map of core VLA concepts. Each color-coded branch highlights*

- 3년간의 문헌 검토를 통한 80개 이상 VLA 모델 수집 및 분석
- core VLA 개념 파악: VLA 정의, 진화 타임라인, 다중 모드 통합, tokenization과 encoding, 학습 패러다임, adaptive execution
- 아키텍처 혁신, 데이터 효율 학습, 파라미터 효율 모델링, 추론 가속화 기술 검토
- real-time control, multimodal action representation, system scalability, unseen task 일반화, ethical deployment 등 주요 도전과제 분석
- 각 도전과제에 대한 targeted solutions 제안 및 평가
- VLA, VLM, agentic AI의 convergence를 통한 미래 발전 방향 제시

## Originality

- VLA 모델의 개념적 기초를 cross-modal learning architectures에서 generalist agents로의 진화로 체계적으로 트레이싱
- Vision, Language, Action의 세 모달리티를 단일 프레임워크로 통합하는 RT-2 이후 발전을 종합적으로 분석
- Action tokenization을 통해 로봇 모터 명령을 수치 또는 기호 표현으로 변환하는 혁신적 접근 강조
- Agentic AI adaptation과 cross-embodiment planning을 통한 새로운 일반화 방안 제시
- Neuro-symbolic planning과 socially aligned embodied agents의 미래 방향 제안

## Limitation & Further Study

- 리뷰 범위가 지난 3년 논문으로 제한되어 초기 관련 연구의 충분한 맥락이 부족할 수 있음
- 80개 모델 분석이라는 규모에서 각 모델의 세부 기술적 비교가 심층적이지 못할 가능성
- 실제 로봇 배포 경험에 기반한 실증적 평가 데이터 부족으로 이론과 실제의 간극 존재 가능
- Safety, bias, ethical deployment 등 중요한 도전과제에 대한 구체적 해결책이 아직 미성숙 단계
- **후속 연구**: 각 응용 분야별 벤치마크 데이터셋 개발, cross-embodiment transfer learning의 구체적 기법 개발, safety-critical 환경에서의 VLA 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 rapidly evolving VLA 분야에 대한 첫 번째 포괄적 종합 리뷰로서, 개념부터 응용까지 체계적으로 정리하고 실제 도전과제와 미래 방향을 명확히 제시한다. embodied AI와 로봇 공학의 발전을 위한 중요한 기초 참고 자료로서 높은 가치를 가진다.

## Related Papers

- 🔄 다른 접근: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — 둘 다 VLA 모델에 대한 종합적 리뷰를 제공하지만 전자는 일반적 개념과 진전을, 후자는 실제 배포에 중점을 둔다.
- 🏛 기반 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Pure VLA 모델에 대한 기존 종합 조사가 80개 이상 VLA 모델을 분석하는 더 포괄적인 리뷰의 기반이 되었다.
- 🔗 후속 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — 로봇공학에서 foundation model의 일반적 응용을 VLA 모델의 구체적 개념과 진전으로 확장하여 심화 분석한다.
- 🏛 기반 연구: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — foundation model 기반 범용 로봇에 대한 종합적 조사가 VLA 모델 연구의 이론적 배경과 발전 방향을 제시한다.
- 🏛 기반 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — 일반적인 VLA 모델 구축에 중요한 요소들을 식별하여 1608의 VLA 개념과 진전 분석에 실증적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to/review]] — VLA 모델의 개념과 응용을 더 넓은 관점에서 확장한다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Vision-Language-Action Models review와 Foundation Model Driven Robotics review는 로봇공학에서 foundation model의 역할을 서로 다른 관점에서 종합적으로 분석한다.
- 🔄 다른 접근: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — VLA Models 서베이는 대규모 모델 중심 vs VLA 아키텍처 중심으로 embodied AI를 다른 관점에서 체계화함
- 🔗 후속 연구: [[papers/1446_Large_VLM-based_Vision-Language-Action_Models_for_Robotic_Ma/review]] — Large VLM-based VLA 서베이가 Vision-Language-Action Models의 일반적 개념을 로봇 매니퓰레이션 영역에서 구체화하고 심화시킨다.
- 🔄 다른 접근: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — 두 survey 모두 VLA 모델을 다루지만 하나는 pure VLA에, 다른 하나는 broader VLA concepts에 집중하는 상호보완적 관점이다.
- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — 둘 다 VLA 모델에 대한 종합적 설문이지만 1608은 VLA에 특화된 반면 1590은 더 넓은 foundation model 관점을 제시합니다.
- 🏛 기반 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — VLA 모델의 전반적인 개념과 발전사를 제공하여 구체적인 구현 요소 분석의 이론적 배경을 마련한다.
- 🧪 응용 사례: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — VLA Models의 concepts와 applications가 VLN taxonomy를 action까지 포함한 더 넓은 프레임워크로 확장하는 데 활용된다.
- 🔄 다른 접근: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — 둘 다 VLA 모델 리뷰이지만 이 논문은 실제 배포와 하드웨어 통합에, 전자는 개념적 진전에 초점을 맞춘다.
- 🧪 응용 사례: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — VLA Models 서베이는 EIIR 프레임워크에서 제시한 embodied intelligence의 실제 구현 방향을 제시함
- 🏛 기반 연구: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — Vision-Language-Action 모델의 개념과 진전이 언어 조건부 로봇 조작 서베이의 이론적 기반을 제공합니다.
