---
title: "1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua"
authors:
  - "Wenxuan Song"
  - "Jiayi Chen"
  - "Wenxue Li"
  - "Xu He"
  - "Han Zhao"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇이 실행 불가능한 지시를 거부할 수 있는 능력을 갖춘 RationalVLA 모델을 제안하며, 이를 평가하기 위해 6가지 차원의 결함 있는 지시를 포함한 RAMA 벤치마크를 도입한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Robot_Foundation_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Song et al._2025_RationalVLA A Rational Vision-Language-Action Model with Dual System.pdf"
---

# RationalVLA: A Rational Vision-Language-Action Model with Dual System

> **저자**: Wenxuan Song, Jiayi Chen, Wenxue Li, Xu He, Han Zhao, Can Cui, Pengxiang Ding Shiyan Su, Feilong Tang, Xuelian Cheng, Donglin Wang, Zongyuan Ge, Xinhu Zheng, Zhe Liu, Hesheng Wang, Haoang Li | **날짜**: 2025-06-12 | **URL**: [https://arxiv.org/abs/2506.10826](https://arxiv.org/abs/2506.10826)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

로봇이 실행 불가능한 지시를 거부할 수 있는 능력을 갖춘 RationalVLA 모델을 제안하며, 이를 평가하기 위해 6가지 차원의 결함 있는 지시를 포함한 RAMA 벤치마크를 도입한다.

## Motivation

- **Known**: 기존 language-conditioned manipulation 작업은 지시가 환경과 완벽하게 정렬되어 있다고 가정하며, VLA 모델들은 fine-tuning 과정에서 언어 이해 능력의 catastrophic forgetting을 겪는다.
- **Gap**: 실제 로봇 배포 환경에서 모호하거나 실행 불가능한 지시를 처리하는 능력이 부족하며, 기존 벤치마크들이 이러한 defective instructions를 충분히 다루지 못하고 있다.
- **Why**: 로봇이 결함 있는 지시를 실행하면 환경 질서를 교란하고 장기 작업 실패를 초래할 수 있으므로, 실제 배포 시나리오에서 지시 거부 능력은 매우 중요하다.
- **Approach**: MLLM과 저수준 조작 정책을 learnable latent space embeddings으로 연결하는 dual-system 아키텍처를 제안하며, <ACT> 토큰으로 행동 생성, <REJ> 토큰으로 결함 지시 거부를 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **RAMA 벤치마크 구축**: visual, physical, semantic, motion, safety, out-of-context 6가지 차원의 결함 있는 지시를 포함한 14,000개 이상의 샘플로 구성된 데이터셋 제시
- **성능 향상**: RAMA 벤치마크에서 기존 baseline 대비 14.5% 높은 성공률과 0.94의 평균 작업 길이 달성
- **실세계 검증**: 실제 로봇 시험에서 제안 모델의 효과성과 견고성을 입증
- **표준 작업 유지**: 일반적인 조작 작업에서도 경쟁력 있는 성능 유지

## How


- Dual-system 아키텍처로 MLLM(고수준 추론)과 로봇 정책(저수준 제어) 통합
- Learnable latent space embeddings을 인터페이스로 사용하여 두 모듈 간 정보 전달
- <ACT> 토큰을 학습하여 저수준 정책이 행동 생성하도록 지시
- <REJ> 토큰을 학습하여 현재 관찰을 기반으로 결함 지시 거부
- End-to-end training manner로 두 모듈을 함께 최적화
- Hindsight data collection을 통한 defective instruction 데이터셋 구성

## Originality

- 결함 있는 지시의 6가지 차원(visual, physical, semantic, motion, safety, out-of-context)을 체계적으로 정의한 최초의 시도
- <REJ> 토큰 기반의 동적 지시 거부 메커니즘으로 기존 단순 거부 방식과 차별화
- Learnable latent space embeddings을 통한 새로운 dual-system 통합 방식으로 catastrophic forgetting과 복합 언어 이해 능력 결핍 문제 동시 해결
- RAMA 벤치마크와 데이터셋을 함께 제공하여 실제적인 평가 환경 조성

## Limitation & Further Study

- 결함 지시의 6가지 차원이 모든 현실 시나리오를 완벽히 커버하는지에 대한 검증 필요
- Real-world 시험 규모가 제한적으로 보여 더 다양한 환경에서의 일반화 능력 평가 필요
- Computational complexity와 inference time에 대한 상세 분석 부족
- 다양한 로봇 플랫폼(humanoid, wheeled robot 등)에서의 확장 가능성 미검증
- 후속 연구는 더 많은 defective instruction 카테고리 발굴 및 다중 로봇 협력 상황에서의 성능 평가를 고려할 수 있음

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RationalVLA는 실제 로봇 배포에서 중요하지만 그동안 간과되었던 defective instruction 처리 능력을 체계적으로 다루는 혁신적인 작업이며, RAMA 벤치마크와 dual-system 아키텍처의 조합으로 언어 이해와 조작 능력을 효과적으로 통합한 우수한 연구이다.

## Related Papers

- 🔗 후속 연구: [[papers/1458_LLM-Driven_Robots_Risk_Enacting_Discrimination_Violence_and/review]] — LLM 기반 로봇의 차별과 폭력 위험성 연구를 확장하여 실행 불가능한 지시 거부 능력까지 포함한 종합적 안전성을 다룬다.
- 🔄 다른 접근: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — Dual-system VLA 아키텍처에서 OpenHelix는 구조 분석에, RationalVLA는 합리적 판단 능력에 초점을 맞춘 서로 다른 접근이다.
- 🔄 다른 접근: [[papers/1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro/review]] — 로봇이 실행 불가능한 지시를 처리하는 rational 능력을 다룬 두 논문으로, 하나는 dual system으로 다른 하나는 unified MLLM으로 접근한다.
- 🔗 후속 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — RationalVLA의 rational reasoning 능력이 embodied chain-of-thought 추론과 결합되면 더욱 강력한 로봇 의사결정 시스템을 구축할 수 있다.
- 🏛 기반 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — ThinkAct의 dual system 아키텍처가 RationalVLA의 rational 의사결정 메커니즘 설계에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1501_On_the_Vulnerability_of_LLMVLM-Controlled_Robotics/review]] — 실행 불가능한 지시를 거부하는 능력은 LLM/VLM 로봇의 취약성 문제에 대한 직접적인 해결책을 제시합니다.
- 🔄 다른 접근: [[papers/1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma/review]] — RationalVLA와 Fast-in-Slow 모두 dual system 접근법을 사용하지만 안전성과 효율성이라는 다른 목표를 추구합니다.
- 🔄 다른 접근: [[papers/1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma/review]] — RationalVLA와 FiS 모두 dual-system 접근을 취하지만 합리적 추론 vs 속도-정확도 균형에서 다른 초점을 가짐
- 🔗 후속 연구: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — RationalVLA의 rational reasoning을 System-2 slow thinking으로 구체화하여 더 체계적인 추론 과정을 제시한다.
- 🏛 기반 연구: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — rational VLA model의 이론적 기반을 제공하여 reflective planning에서 사용되는 VLM의 추론 능력과 dynamics model 통합에 필요한 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro/review]] — 로봇의 지능적 의사결정을 RoboBrain은 통합 MLLM으로, RationalVLA는 dual system으로 구현하는 서로 다른 접근법이다.
- 🏛 기반 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — ThinkAct의 dual system 프레임워크가 RationalVLA의 rational 의사결정과 시스템 2 사고 구현에 아키텍처적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — RationalVLA는 Diffusion-VLA와 유사하게 추론 능력을 통합하지만 dual 구조를 통해 다른 접근 방식을 사용합니다.
- 🔄 다른 접근: [[papers/1335_Code-as-Monitor_Constraint-aware_Visual_Programming_for_Reac/review]] — VLM 기반 코드 모니터링 대신 dual thinking을 통한 합리적 추론으로 로봇 안전성 확보
- 🔄 다른 접근: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — RationalVLA의 dual vision encoder와 Embodied-R1의 pointing-based representation은 VLM에서 perception-action gap을 서로 다르게 해결하는 접근법이다.
