---
title: "1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis"
authors:
  - "Chi-Pin Huang"
  - "Yueh-Hua Wu"
  - "Min-Hung Chen"
  - "Yu-Chiang Frank Wang"
  - "Fu-En Yang"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "ThinkAct는 Vision-Language-Action 추론 작업을 위해 강화학습 기반 시각 잠재 계획을 통해 고수준 추론과 저수준 행동 실행을 연결하는 이중 시스템 프레임워크를 제안한다. 다중모달 LLM이 생성한 추론 계획을 시각 계획 잠재로 압축하여 다운스트림 행동 모델을 조건화하여 장기 계획, 소수샷 적응, 자체 수정 능력을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2025_ThinkAct Vision-Language-Action Reasoning via Reinforced Visual Latent Planning.pdf"
---

# ThinkAct: Vision-Language-Action Reasoning via Reinforced Visual Latent Planning

> **저자**: Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, Yu-Chiang Frank Wang, Fu-En Yang | **날짜**: 2025-07-22 | **URL**: [https://arxiv.org/abs/2507.16815](https://arxiv.org/abs/2507.16815)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We introduce ThinkAct, a reasoning VLA framework capable of thinking before acting. Through*

ThinkAct는 Vision-Language-Action 추론 작업을 위해 강화학습 기반 시각 잠재 계획을 통해 고수준 추론과 저수준 행동 실행을 연결하는 이중 시스템 프레임워크를 제안한다. 다중모달 LLM이 생성한 추론 계획을 시각 계획 잠재로 압축하여 다운스트림 행동 모델을 조건화하여 장기 계획, 소수샷 적응, 자체 수정 능력을 달성한다.

## Motivation

- **Known**: 최근 MLLM 기반 Vision-Language-Action 모델(OpenVLA, TraceVLA)들은 대규모 로봇 데모셋에서 훈련되어 단기 스킬에서는 효과적이지만 복잡한 추론과 장기 계획 능력은 제한적이다. Chain-of-Thought 프롬프팅과 RL 기반 추론이 LLM의 다단계 추론 능력을 향상시키는 것으로 알려져 있다.
- **Gap**: 기존 VLA 모델들은 시각 및 텍스트 입력에서 저수준 행동으로의 엔드-투-엔드 방식으로 작동하기 때문에 구조화된 계획 없이 복잡한 명령, 장기 목표, 분포 외 시나리오를 처리하기 어렵다. CoT 기반 접근법도 고품질 추론 트레이스 생성의 높은 비용으로 인해 특정 시각 장면이나 추론 패턴에 과적합되는 경향이 있다.
- **Why**: 로봇 조작 및 구체화된 AI 작업에서 장기 계획, 소수샷 적응, 자체 수정 능력은 동적 환경에서의 적응성과 복잡한 작업 변형 대처 능력을 크게 향상시킨다. 추론과 행동 실행 사이의 명시적 연결은 모델의 일반화 능력과 해석 가능성을 개선한다.
- **Approach**: ThinkAct는 목표 완성과 궤적 일관성을 기반으로 한 행동 정렬 시각 보상으로 강화되는 GRPO 최적화를 통해 다중모달 LLM이 구체화된 추론 계획을 생성하도록 학습시킨다. 이러한 계획을 시각 계획 잠재로 압축하여 목표 환경에서의 강건한 행동 실행을 위해 다운스트림 행동 모델을 조건화한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: We introduce ThinkAct, a reasoning VLA framework capable of thinking before acting. Through*

- **이중 시스템 아키텍처**: 고수준의 구조화된 추론과 저수준 행동 실행을 시각 잠재 계획을 통해 상호 향상시키는 프레임워크 제안
- **행동 정렬 강화학습**: 목표 완성과 궤적 분포 매칭에 기반한 시각 피드백을 GRPO 최적화에 활용하여 장기 계획 추론을 지원
- **시각 잠재 계획**: 중간 추론 단계를 고수준의 의도를 캡처하는 컴팩트 잠재 궤적으로 압축하여 다양한 환경에 효율적으로 적응
- **포괄적인 성능 개선**: LIBERO 벤치마크에서 소수샷 적응, 장기 계획, 자체 수정 능력을 포함한 구체화된 추론 및 로봇 조작 능력 향상 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of our ThinkAct. (a) Given observation 𝑜𝑡and instruction 𝑙, ThinkAct advances action-*

- 다중모달 LLM을 사용하여 시각 관찰과 텍스트 명령으로부터 구체화된 추론 계획 생성
- 목표 완성 시각 신호와 궤적 정렬 신호를 기반으로 행동 정렬 보상 신호 설계
- GRPO 강화학습 알고리즘을 사용하여 보상 신호로 추론 계획 최적화
- 생성된 추론 계획을 시각 계획 잠재로 압축하는 메커니즘 구현
- 시각 계획 잠재를 입력으로 받아 목표 환경에서 행동을 예측하는 다운스트림 행동 모델 훈련
- 인간 및 로봇 비디오 데이터를 활용하여 구체화된 추론을 시각 관찰에 그라운딩

## Originality

- **시각 기반 행동 정렬 보상의 혁신**: QA 스타일의 보상 신호가 아닌 목표 완성과 궤적 분포 매칭 기반의 구체화된 시각 보상으로 RL 기반 추론을 적용하여 장기 계획과 행동 실행의 연결 강화
- **잠재 궤적 기반 계획 압축**: 구조화된 추론 단계를 컴팩트 시각 잠재로 변환하여 다운스트림 모델의 조건화에 활용하는 새로운 아이디어
- **이중 시스템의 상호 강화**: 추론 개선과 행동 개선이 서로 강화되도록 설계된 통합 프레임워크 제시로 기존 감독 학습 기반 CoT 접근법과 차별화

## Limitation & Further Study

- **계산 복잡성**: 다중모달 LLM에 의한 추론 생성과 GRPO 최적화의 계산 비용이 상당할 수 있으며, 실시간 로봇 제어 시나리오에서의 지연 문제 미언급
- **보상 신호 설계의 의존성**: 목표 완성과 궤적 정렬 신호의 품질이 모델 성능에 직접적으로 영향을 미치므로 다양한 작업 유형에 대한 보상 설계의 범용성 제한 가능성
- **평가 범위**: 주로 LIBERO와 로봇 조작 벤치마크에서만 평가되었으며, 더 다양한 구체화된 AI 시나리오(AR 보조, 네비게이션 등)에서의 적용 가능성은 미확인
- **후속 연구 방향**: 보상 신호 자동 설계, 다중 감각 입력(촉각, 음성) 통합, 실제 로봇 배포에서의 단기-장기 계획 균형 개선 등 고려 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ThinkAct는 행동 정렬 시각 보상을 기반으로 한 혁신적인 GRPO 강화학습과 시각 잠재 계획 압축을 통해 Vision-Language-Action 모델에 구조화된 추론 능력을 효과적으로 부여한다. 장기 계획, 소수샷 적응, 자체 수정 능력을 동시에 달성한 점에서 구체화된 AI 및 로봇 조작 분야에 의미 있는 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 고수준 추론과 저수준 행동의 연결을 위한 서로 다른 아키텍처 - 이중 시스템 vs 삼중 시스템입니다.
- 🏛 기반 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — Vision-Language-Action에서 visual chain-of-thought reasoning의 기반을 제시합니다.
- 🔗 후속 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — 강화학습 기반 시각 잠재 계획을 reinforcement learning framework에 통합할 수 있습니다.
- 🏛 기반 연구: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — ThinkAct의 dual system 프레임워크가 RationalVLA의 rational 의사결정과 시스템 2 사고 구현에 아키텍처적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and/review]] — 고수준 추론과 저수준 실행 통합을 ThinkAct는 dual system으로, RoBridge는 계층적 아키텍처로 서로 다르게 해결한다.
- 🔗 후속 연구: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — Hume의 System-2 thinking 개념이 ThinkAct의 강화학습 기반 시각 잠재 계획과 결합되어 더 정교한 추론 시스템을 구축한다.
- 🔄 다른 접근: [[papers/1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason/review]] — 비전-언어-액션 추론을 위한 다른 강화 시각적 추론 접근 방식입니다.
- 🔗 후속 연구: [[papers/1399_From_Seeing_to_Doing_Bridging_Reasoning_and_Decision_for_Rob/review]] — FSD의 visual reasoning을 더 발전시켜 reinforced visual thinking으로 확장한 모델이다.
- 🏛 기반 연구: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — Hume의 System-2 thinking 개념이 ThinkAct의 강화된 시각적 추론 체인과 유사한 철학적 기반을 공유한다.
- 🏛 기반 연구: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — ThinkAct의 dual system 아키텍처가 RationalVLA의 rational 의사결정 메커니즘 설계에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti/review]] — VLA 모델에서 adaptive reasoning-action switching vs reinforced visual reasoning이라는 서로 다른 추론-행동 통합 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — VLM의 장기 지평선 능력 향상에서 reflection mechanism vs reinforced visual reasoning이라는 서로 다른 test-time computation 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — ThinkAct과 함께 VLA 모델의 추론 강화를 다루지만 이 연구는 embodied CoT에, ThinkAct은 강화 시각 추론에 초점을 맞춘다.
- 🔄 다른 접근: [[papers/1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and/review]] — 인지와 실행의 통합에서 RoBridge는 계층적 아키텍처로, ThinkAct는 dual system으로 서로 다른 방식으로 문제를 해결한다.
- 🔄 다른 접근: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — ThinkAct는 RT-H와 같이 고수준과 저수준 행동을 연결하지만 강화 시각적 추론을 통한 다른 메커니즘을 사용한다.
- 🔄 다른 접근: [[papers/1618_VLA-Reasoner_Empowering_Vision-Language-Action_Models_with_R/review]] — ThinkAct가 VLA-Reasoner와 다른 강화 비전-언어-행동 추론 방식으로 로봇의 사고와 행동을 통합한다.
- 🔗 후속 연구: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — ThinkAct는 Diffusion-VLA의 reasoning injection을 강화학습 기반 시각-언어-행동 추론으로 확장합니다.
- 🔗 후속 연구: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — ThinkAct의 vision-language-action reasoning이 Embodied-R1의 reinforced fine-tuning을 통한 embodied reasoning으로 더욱 발전한 형태이다.
