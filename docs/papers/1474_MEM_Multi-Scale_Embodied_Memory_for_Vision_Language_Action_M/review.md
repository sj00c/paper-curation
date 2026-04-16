---
title: "1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M"
authors:
  - "Marcel Torne"
  - "Karl Pertsch"
  - "Homer Walke"
  - "Kyle Vedder"
  - "Suraj Nair"
date: "2026.03"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇의 장시간 작업을 위해 비디오 기반 단기 메모리와 텍스트 기반 장기 메모리를 결합한 Multi-Scale Embodied Memory (MEM)을 제안하여, 15분 이상의 복잡한 조작 작업을 수행할 수 있는 Vision Language Action 모델을 구현했다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Action-Value_Reasoning_Systems"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Torne et al._2026_MEM Multi-Scale Embodied Memory for Vision Language Action Models.pdf"
---

# MEM: Multi-Scale Embodied Memory for Vision Language Action Models

> **저자**: Marcel Torne, Karl Pertsch, Homer Walke, Kyle Vedder, Suraj Nair, Brian Ichter, Allen Z. Ren, Haohuan Wang, Jiaming Tang, Kyle Stachowicz, Karan Dhabalia, Michael Equi, Quan Vuong, Jost Tobias Springenberg, Sergey Levine, Chelsea Finn, Danny Driess | **날짜**: 2026-03-04 | **URL**: [https://arxiv.org/abs/2603.03596](https://arxiv.org/abs/2603.03596)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Multi-Scale Embodied Memory (MEM) equips Vision Language Action Models (VLAs) with memory for solving long-horiz*

로봇의 장시간 작업을 위해 비디오 기반 단기 메모리와 텍스트 기반 장기 메모리를 결합한 Multi-Scale Embodied Memory (MEM)을 제안하여, 15분 이상의 복잡한 조작 작업을 수행할 수 있는 Vision Language Action 모델을 구현했다.

## Motivation

- **Known**: 최근 VLA 모델들이 대규모 다양한 데이터로 학습되어 일반화된 조작 능력을 보여주고 있으며, 메모리 추가의 중요성이 인식되고 있다. 그러나 기존 메모리 방식들은 단일 모달리티를 사용하거나 장시간 맥락을 효율적으로 처리하지 못한다.
- **Gap**: 로봇의 장시간 작업에는 폐색 처리, 재적응을 위한 밀집 단기 메모리와 레시피 진행 상황 같은 의미론적 정보를 위한 장기 메모리가 동시에 필요하지만, 기존 접근법들은 하나의 표현 방식으로는 두 요구사항을 동시에 만족하지 못한다.
- **Why**: 실제 로봇 작업은 수십 분 단위의 복잡한 다단계 작업을 요구하며, 이를 효율적으로 처리하는 메모리 시스템은 실세계 로봇 자동화의 실용성을 크게 향상시킬 수 있다.
- **Approach**: MEM은 효율적인 video encoder를 사용한 비디오 기반 단기 메모리와 자연언어로 의미론적 사건을 추적하는 언어 기반 장기 메모리를 결합하여, 다중 시간 스케일의 맥락을 동시에 처리한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Multi-Scale Embodied Memory (MEM) equips Vision Language Action Models (VLAs) with memory for solving long-horiz*

- **장시간 작업 수행**: 주방 정리, 그릴 치즈 샌드위치 준비 등 최대 15분 길이의 복잡한 조작 작업을 성공적으로 수행
- **부분 관찰성 처리**: 자기 폐색(self-occlusion)으로 인한 관찰 손실에도 단기 메모리로 대응하여 안정적 조작 유지
- **맥락 내 적응**: 메모리를 활용하여 그리핑 실패 시 재적응하거나 조작 전략을 동적으로 수정
- **효율성**: 실시간 로봇 제어 제약 조건(수백 밀리초 지연) 내에서 수십 분의 메모리 처리 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2 shows an overview of our MEM system. Our goal*

- π0.6 VLA 모델에 MEM 통합하여 다양한 로봇, 비전-언어, 비디오 데이터로 학습
- 효율적 video encoder 아키텍처를 사용하여 수초 분량의 밀집 이미지 메모리를 압축된 표현으로 변환
- 자연언어 메모리 메커니즘으로 의미론적 사건들을 추적하여 장시간 정보를 효율적으로 저장
- 단기 비디오 메모리와 장기 텍스트 메모리를 정책 입력으로 조합하여 다중 시간 스케일 맥락 제공
- Sparse attention 연산을 활용하여 장시간 비디오 입력의 계산 효율성 향상

## Originality

- 로봇 메모리에 명시적으로 다중 모달리티를 적용한 최초의 체계적 접근으로, 기존 단일 모달리티 방식과 구별됨
- 언어 기반 장기 메모리를 로봇 정책의 의도적 추적 메커니즘으로 통합한 혁신적 설계
- 실시간 로봇 제어 제약 조건 하에서 10분 이상의 고주파 멀티프레임 비디오를 처리하는 효율적 기술 개발

## Limitation & Further Study

- 언어 기반 메모리의 정확성이 VLM의 성능에 크게 의존하므로, 의미 해석 오류 시 누적 가능성
- 비디오 인코더의 압축 과정에서 세밀한 공간 정보(그리핑 각도, 높이 등) 손실 가능성
- 평가가 주로 시뮬레이션 또는 제한된 실제 환경에서만 수행되어, 더 다양한 실제 조건에서의 검증 필요
- 텍스트 메모리 생성 방식이 명시적으로 설명되지 않아, 자동 요약과 수동 기술 간의 차이 불명확
- 후속 연구로 causal confusion 제거를 위한 보조 목적함수 추가, 더 장시간 작업에 대한 확장성 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 로봇의 장시간 작업을 위한 다중 스케일 메모리 아키텍처를 창의적으로 제안하여 15분 이상의 복잡한 조작 작업을 처음으로 성공적으로 구현했으며, 이는 실제 로봇 자동화의 실용성을 크게 향상시키는 중요한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1459_LLM-State_Open_World_State_Representation_for_Long-horizon_T/review]] — 장기간 로봇 작업을 위한 메모리 시스템에서 multi-scale embodied memory vs LLM-based state representation이라는 서로 다른 상태 관리 접근법을 보여준다.
- 🔗 후속 연구: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — embodied reasoning을 위한 state-maintaining 메커니즘을 multi-scale memory로 확장하여 더 복잡한 장기간 작업에서의 상태 추적 능력을 향상시킨다.
- 🏛 기반 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — memory-augmented multi-task agent의 기초 연구로서 MEM의 다중 스케일 메모리 아키텍처 설계에 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — MEM의 다중 스케일 메모리가 Learning Latent Plans from Play의 잠재적 계획 학습과 결합되어 더 효율적인 장기 로봇 제어를 실현한다.
- 🏛 기반 연구: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — MEM의 시공간 메모리 개념이 TraceVLA의 시공간 인식 향상 방법론과 유사한 이론적 기반을 공유한다.
- 🏛 기반 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — 장기간 작업을 위한 메모리 시스템의 기초가 되는 planning with language 개념
- 🔄 다른 접근: [[papers/1462_LOTUS_Continual_Imitation_Learning_for_Robot_Manipulation_Th/review]] — 로봇 조작에서 장기 기억을 위한 multi-scale memory vs continual learning 접근법
- 🔗 후속 연구: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — Hume의 System-2 사고 방식이 MEM의 다중 스케일 메모리 시스템과 결합되어 더욱 복잡한 장기 로봇 작업을 수행할 수 있다.
- 🔗 후속 연구: [[papers/1459_LLM-State_Open_World_State_Representation_for_Long-horizon_T/review]] — MEM의 multi-scale embodied memory 개념을 LLM 기반 장기 작업 계획의 상태 추적으로 확장했다.
- 🔄 다른 접근: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — 둘 다 VLN에서 메모리 표현을 다루지만 MapNav는 2D semantic map을, MEM은 multi-scale embodied memory를 사용하는 다른 접근법입니다.
- 🔗 후속 연구: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — MEM의 multi-scale embodied memory를 spatial-geometric과 visual-semantic으로 특화하여 VLN에 적용했다.
- 🔄 다른 접근: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — 둘 다 embodied navigation에서 통합된 프레임워크를 다루지만 RoboTron-Nav는 multitask collaboration에, MEM은 multi-scale memory에 초점을 맞춘 다른 접근법입니다.
- 🔗 후속 연구: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — multi-scale 메모리를 명시적 상태 유지와 결합하여 더 효과적인 장기 계획을 수행할 수 있습니다.
- 🏛 기반 연구: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — multi-scale embodied memory가 visual tracking에서 Target Identification Memory의 기반이 됩니다.
- 🔄 다른 접근: [[papers/1322_BOSS_Benchmark_for_Observation_Space_Shift_in_Long-Horizon_T/review]] — 멀티스케일 메모리를 활용한 다른 장기 작업 해결 접근법을 제시한다.
