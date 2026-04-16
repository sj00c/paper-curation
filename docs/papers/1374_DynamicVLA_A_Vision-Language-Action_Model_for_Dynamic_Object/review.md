---
title: "1374_DynamicVLA_A_Vision-Language-Action_Model_for_Dynamic_Object"
authors:
  - "Haozhe Xie"
  - "Beichen Wen"
  - "Jiarui Zheng"
  - "Zhaoxi Chen"
  - "Fangzhou Hong"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "DynamicVLA는 동적 객체 조작을 위한 compact 0.4B VLA 모델로, Continuous Inference와 Latent-aware Action Streaming을 통해 지각-실행 간의 지연을 제거하고 실시간 폐루프 제어를 가능하게 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xie et al._2026_DynamicVLA A Vision-Language-Action Model for Dynamic Object Manipulation.pdf"
---

# DynamicVLA: A Vision-Language-Action Model for Dynamic Object Manipulation

> **저자**: Haozhe Xie, Beichen Wen, Jiarui Zheng, Zhaoxi Chen, Fangzhou Hong, Haiwen Diao, Ziwei Liu | **날짜**: 2026-01-29 | **URL**: [https://arxiv.org/abs/2601.22153](https://arxiv.org/abs/2601.22153)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of DynamicVLA. (a) A 0.4B-parameter VLA architecture couples a lightweight backbone with an action*

DynamicVLA는 동적 객체 조작을 위한 compact 0.4B VLA 모델로, Continuous Inference와 Latent-aware Action Streaming을 통해 지각-실행 간의 지연을 제거하고 실시간 폐루프 제어를 가능하게 한다.

## Motivation

- **Known**: 기존 VLA 모델들은 정적 조작에서는 우수한 성능을 보이지만, 빠르고 예측 불가능한 객체 움직임이 있는 동적 환경에서는 지연으로 인한 지각-실행 불일치 문제로 어려움을 겪는다.
- **Gap**: 동적 객체 조작을 위한 대규모 데이터셋이 부재하며, 기존 VLA 모델들은 추론 지연이 크고 temporal reasoning 능력이 부족해 실시간 반응성과 폐루프 적응이 제한적이다.
- **Why**: 실제 로봇 조작 환경에서는 손받기, 물건 이동, 안정화 등 동적 객체와의 상호작용이 빈번하며, 작은 지연도 작업 실패를 야기하므로 정적 조작 대비 훨씬 엄격한 요구사항을 만족해야 한다.
- **Approach**: compact 0.4B 매개변수 VLA에 convolutional vision encoder를 적용하여 공간 효율성을 확보하고, Continuous Inference로 추론과 실행을 겹치게 하며, Latent-aware Action Streaming으로 시간 정렬된 행동 실행을 강제한다. 또한 자동화된 데이터 수집 파이프라인으로 200K 합성 에피소드와 2K 실제 에피소드를 포함한 Dynamic Object Manipulation (DOM) 벤치마크를 구축한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: (a) Current VLA models face perception–execution (P.E.) gaps and inter-chunk waiting, causing delayed reactions *

- **Compact 모델 설계**: ConvNet 기반 vision encoder를 사용하여 0.4B 매개변수로 빠른 multimodal 추론 가능
- **Continuous Inference**: 추론과 실행을 파이프라인화하여 inter-chunk waiting 제거 및 지연 감소
- **Latent-aware Action Streaming**: 시간 정렬을 통해 지각-실행 간격을 bridging하고 outdated action 폐기
- **DOM 벤치마크**: 2.8K 장면, 206 객체, 200K 합성 + 2K 실제 에피소드를 포함하는 최초의 대규모 동적 조작 데이터셋
- **다중 embodiment 지원**: Franka Emika Panda, AgileX PiPER 등 여러 로봇 플랫폼에서 검증
- **성능 향상**: 응답 속도, 지각, 일반화 측면에서 기존 모델 대비 현저한 개선

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of DynamicVLA. (a) A 0.4B-parameter VLA architecture couples a lightweight backbone with an action*

- FastViT 기반의 convolutional vision encoder로 효율적 spatial compression 및 구조 보존
- SmolLM2-360M의 처음 16 레이어와 별도 Action Expert 레이어 16개로 구성된 경량 아키텍처
- 추론 루프와 실행 루프를 독립적으로 파이프라인화하여 overlapping 실현
- 현재 timestep에서 가장 최신 예측만 선택하는 시간 정렬 메커니즘
- Isaac Sim에서 real-time 6D object pose 및 velocity를 이용한 자동 데이터 생성
- 실제 환경에서 dual RGB view 기반 3D object tracking으로 6D pose/velocity 추정 및 자율 시행
- task-driven state machine controller로 일관된 데이터 수집 및 모델 학습

## Originality

- 동적 객체 조작을 위해 특화된 첫 번째 VLA 모델로, 지각-실행 gap을 명시적으로 해결하는 Latent-aware Action Streaming 제안
- Continuous Inference를 통한 새로운 파이프라인 실행 패러다임으로 실시간성과 적응성 동시 확보
- teleoperation 없이 자동화된 파이프라인으로 동적 조작 데이터 수집하는 혁신적 방법론
- 정적 조작 중심 기존 로봇 학습의 한계를 동적 시나리오로 확장하는 체계적 접근

## Limitation & Further Study

- 0.4B 모델의 성능 ceiling이 존재할 수 있으며, 더 복잡한 장기 지평 작업에서의 확장성 미검증
- DOM 벤치마크는 주로 단순 pick-and-place 기반 동적 작업에 국한되어 있어 더 복잡한 상호작용 시나리오 부재
- 실제 환경에서의 검증이 16개 작업으로 제한적이며, 다양한 embodiment 간 일반화 정도 추가 검증 필요
- 추론 지연이 완전히 제거되지 않으므로, 극도로 빠른 동적 환경에서의 성능 한계 존재
- 후속 연구에서는 더 큰 모델 크기와 성능의 trade-off 분석, 복잡한 멀티 객체 상호작용, 접촉력 피드백 통합 등 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DynamicVLA는 동적 객체 조작이라는 중요한 미해결 문제에 대해 체계적인 모델 설계, 실시간 실행 메커니즘, 대규모 벤치마크를 종합적으로 제시하는 의미 있는 연구로, 특히 Latent-aware Action Streaming과 자동화된 데이터 수집 파이프라인의 혁신성이 두드러진다.

## Related Papers

- 🏛 기반 연구: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — real-time VLA 실행 기술이 DynamicVLA의 continuous inference와 실시간 제어의 핵심 기반
- 🔄 다른 접근: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — dynamic object manipulation을 위한 continuous inference 대신 one-step diffusion을 통한 빠른 정책 실행
- 🏛 기반 연구: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — Real-Time Execution of Action Chunking의 실시간 제어 기법이 DynamicVLA의 continuous inference와 real-time closed-loop control 구현에 기초가 된다.
- 🔗 후속 연구: [[papers/1524_Reactive_Diffusion_Policy_Slow-Fast_Visual-Tactile_Policy_Le/review]] — Reactive Diffusion Policy의 slow-fast visual-tactile learning이 DynamicVLA의 perception-action latency 해결에 대한 확장된 접근 방식을 제시한다.
- 🔄 다른 접근: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — 동적 객체에 특화된 compact VLA와 범용 generalist robot policy의 서로 다른 설계 철학을 보여줍니다.
- 🏛 기반 연구: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — TinyVLA의 효율성 최적화 방법이 실시간 동적 객체 조작을 위한 기반이 됩니다.
- 🔄 다른 접근: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — DynamicVLA와 유사하게 동적 환경을 다루지만 Mixture-of-Transformers로 이해, 생성, 행동을 통합하는 다른 접근법을 제시한다.
