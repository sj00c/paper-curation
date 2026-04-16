---
title: "1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action"
authors:
  - "Haoming Song"
  - "Delin Qu"
  - "Yuanqi Yao"
  - "Qizhi Chen"
  - "Qi Lv"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Hume는 Vision-Language-Action 모델에 System-2 slow thinking을 도입한 dual-system 로봇 정책으로, value-guided 반복 샘플링과 cascaded action denoising을 통해 복잡한 로봇 제어 성능을 향상시킨다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Action-Value_Reasoning_Systems"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Song et al._2025_Hume Introducing System-2 Thinking in Visual-Language-Action Model.pdf"
---

# Hume: Introducing System-2 Thinking in Visual-Language-Action Model

> **저자**: Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, Dong Wang, Xuelong Li | **날짜**: 2025-05-27 | **URL**: [https://arxiv.org/abs/2505.21432](https://arxiv.org/abs/2505.21432)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We present Hume, a dual-system vision-language-action model exploring human-like*

Hume는 Vision-Language-Action 모델에 System-2 slow thinking을 도입한 dual-system 로봇 정책으로, value-guided 반복 샘플링과 cascaded action denoising을 통해 복잡한 로봇 제어 성능을 향상시킨다.

## Motivation

- **Known**: LLM에서 Chain-of-Thought와 같은 System-2 thinking이 성공했으며, dual-system VLA 아키텍처들이 효율성을 개선했다. 그러나 로봇 제어에서 효과적인 System-2 thinking의 적용은 미흡하다.
- **Gap**: 기존 dual-system 로봇 정책들은 System 2가 실질적인 thinking과 reasoning을 수행하지 못하며, 로봇 액션의 의미론적 모호성으로 인해 text 기반 CoT를 직접 적용하기 어렵다. 또한 System-2의 'slowness'와 로봇 제어의 'fastness' 요구 사이의 균형 문제가 남아있다.
- **Why**: 복잡한 로봇 작업은 깊은 deliberative thinking을 요구하며, 이는 로봇의 일반화 능력과 dexterous control 성능을 크게 향상시킬 수 있다.
- **Approach**: System 2는 flow matching denoising head와 novel value-query head를 갖춘 VLM 기반 모듈로, state-action value를 추정하여 여러 action 후보 중 최적을 선택한다. System 1은 가벼운 visuomotor policy로 System 2의 선택을 받아 real-time cascaded action denoising을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: We present Hume, a dual-system vision-language-action model exploring human-like*

- **LIBERO 벤치마크 성능 향상**: π0 대비 +4.4% success rate 달성
- **Simpler 벤치마크 성능 향상**: +25.9% improvement 달성
- **실세계 로봇 배포 성능**: +12.9% improvement로 21개 실제 로봇 설정에서 우수한 성능 입증
- **다양한 환경 강건성**: viewpoint, texture, lighting, layout 변화 및 unseen objects/environments에서 우수한 성능
- **효율적인 real-time 제어**: System 2는 4Hz, System 1은 90Hz로 비동기 작동하면서도 성능 유지

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of Hume. Hume contains two systems working asynchronously. Given the*

- System 2는 VLM backbone에 flow matching denoising head로 long-horizon action chunk 예측
- Novel value-query head를 통해 예측된 action chunk의 state-action value 추정
- Value-guided thinking: 여러 action 후보를 반복 샘플링하고 state-action value로 최적 action 선택
- System 1은 System 2의 선택된 action chunk 중 짧은 segment를 받아 현재 visual observation과 robot state를 포함하여 cascaded diffusion denoising 수행
- 배포 시: System 2가 저주파(4Hz)에서 value-guided thinking 실행, System 1이 비동기적으로 고주파(90Hz)에서 fluid action 생성
- Multi-stage training strategy로 System 1과 System 2를 단계적으로 학습

## Originality

- 로봇 제어에서 System-2 slow thinking을 처음으로 체계적으로 도입하여 value estimation 기반의 action selection 메커니즘 제안
- 로봇 액션의 semantic 모호성을 우회하고 value-guided repeat sampling으로 실질적인 thinking 구현
- Cascaded action denoising으로 low-frequency System 2와 high-frequency System 1의 효과적인 비동기 통합 달성
- Flow matching과 value-query head의 조합으로 differentiable한 System-2 thinking 최적화 가능하게 설계

## Limitation & Further Study

- Value-query head의 학습 안정성과 state-action value 추정 정확도에 대한 분석 부족
- System 2의 4Hz 주기와 System 1의 90Hz 주기 간 시간 동기화 메커니즘이 상세히 설명되지 않음
- Cascaded action denoising의 계산 복잡도 및 inference 오버헤드에 대한 분석 미흡
- Value-guided thinking의 '반복 샘플링 횟수' 선택 기준이 명확하지 않음", 'Humanoid 로봇 등 특정 embodiment에 대한 적응성 검증 부족
- 후속 연구: value estimation 정확도 개선, 더 효율적인 비동기 통합 메커니즘 개발, 다양한 embodiment에 대한 일반화 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 로봇 제어에 System-2 slow thinking을 처음으로 적용하여 중요한 conceptual contribution을 제시하며, value-guided thinking과 cascaded action denoising의 novel 조합으로 실질적인 성능 향상을 달성했다. 다만 기술적 세부사항과 design choice의 정당화가 더 보강될 필요가 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — 둘 다 System-2 thinking을 VLA에 도입하지만 value-guided sampling vs global planner라는 다른 구현 방식을 사용한다.
- 🏛 기반 연구: [[papers/1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac/review]] — Embodied-Reasoner의 심층 추론 패러다임을 VLA 모델에 System-2 thinking으로 구체화했다.
- 🔗 후속 연구: [[papers/1542_RoboMonkey_Scaling_Test-Time_Sampling_and_Verification_for_V/review]] — RoboMonkey의 test-time sampling 개념을 System-2 thinking의 value-guided 방식으로 발전시켰다.
- 🔗 후속 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — Hume의 System-2 사고 방식이 MEM의 다중 스케일 메모리 시스템과 결합되어 더욱 복잡한 장기 로봇 작업을 수행할 수 있다.
- 🔄 다른 접근: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — 둘 다 VLA 모델의 추론 능력 향상에 초점을 맞추지만, Hume은 dual-system 접근법을, HybridVLA는 diffusion과 autoregressive 통합에 집중한다.
- 🏛 기반 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — Hume의 System-2 thinking 개념이 ThinkAct의 강화된 시각적 추론 체인과 유사한 철학적 기반을 공유한다.
- 🔗 후속 연구: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — RationalVLA의 rational reasoning을 System-2 slow thinking으로 구체화하여 더 체계적인 추론 과정을 제시한다.
- 🔄 다른 접근: [[papers/1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac/review]] — 두 논문 모두 VLA 모델에 System-2 스타일의 심층 추론을 도입하여 복잡한 로봇 제어를 개선하는 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — 둘 다 dual-system 아키텍처를 VLA에 도입하지만 global planner + policy vs value-guided sampling이라는 다른 구현 방식을 사용한다.
- 🔗 후속 연구: [[papers/1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti/review]] — System-2 thinking을 adaptive reasoning과 결합하여 상황에 따라 추론 깊이를 조절하는 더 효율적인 VLA 시스템을 구축한다.
- 🏛 기반 연구: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — Hume의 System-2 thinking 접근법이 SmartWay의 history-aware reasoning과 backtracking 메커니즘의 이론적 기반을 제공한다.
- 🧪 응용 사례: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — System-2 thinking의 deliberative reasoning 능력을 대규모 로봇 조작 벤치마크에서 실제로 평가하고 검증하는 구체적인 응용 사례를 제공한다.
- 🔗 후속 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — Hume의 System-2 thinking 개념이 ThinkAct의 강화학습 기반 시각 잠재 계획과 결합되어 더 정교한 추론 시스템을 구축한다.
- 🔄 다른 접근: [[papers/1618_VLA-Reasoner_Empowering_Vision-Language-Action_Models_with_R/review]] — VLA에서 추론 능력 강화를 위한 서로 다른 접근법 - MCTS vs system-2 thinking입니다.
- 🔄 다른 접근: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — visual chain-of-thought와 system-2 thinking의 서로 다른 VLA 추론 능력 향상 접근법
- 🔄 다른 접근: [[papers/1336_CogACT_A_Foundational_Vision-Language-Action_Model_for_Syner/review]] — cognition-action 분리 대신 system-2 thinking을 통한 다른 VLA 성능 향상 접근법
