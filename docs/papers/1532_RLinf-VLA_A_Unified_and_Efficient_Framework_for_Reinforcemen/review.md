---
title: "1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen"
authors:
  - "Hongzhi Zang"
  - "Mingjie Wei"
  - "Si Xu"
  - "Yongji Wu"
  - "Zhen Guo"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "RLinf-VLA는 Vision-Language-Action 모델의 강화학습 훈련을 위한 통합되고 효율적인 프레임워크로, 다양한 VLA 아키텍처, RL 알고리즘, 시뮬레이터를 지원하며 GPU 할당 최적화를 통해 2.27배 속도 향상을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zang et al._2025_RLinf-VLA A Unified and Efficient Framework for Reinforcement Learning of Vision-Language-Action Mo.pdf"
---

# RLinf-VLA: A Unified and Efficient Framework for Reinforcement Learning of Vision-Language-Action Models

> **저자**: Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen Guo, Yuanqing Wang, Hao Lin, Peihong Wang, Liangzhi Shi, Yuqing Xie, Zhexuan Xu, Zhihao Liu, Kang Chen, Wenhao Tang, Quanlu Zhang, Weinan Zhang, Chao Yu, Yu Wang | **날짜**: 2025-10-08 | **URL**: [https://arxiv.org/abs/2510.06710](https://arxiv.org/abs/2510.06710)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1:*

RLinf-VLA는 Vision-Language-Action 모델의 강화학습 훈련을 위한 통합되고 효율적인 프레임워크로, 다양한 VLA 아키텍처, RL 알고리즘, 시뮬레이터를 지원하며 GPU 할당 최적화를 통해 2.27배 속도 향상을 달성한다.

## Motivation

- **Known**: Vision-Language-Action 모델은 인터넷 규모 데이터로 사전학습된 비전-언어 모델을 로봇 데모 데이터셋으로 추가 훈련하여 다양한 작업에서 강한 일반화 능력을 보여준다. RL은 VLA 모델의 사후훈련 패러다임으로 점점 더 중요해지고 있으며 SFT 대비 더 나은 out-of-distribution 일반화를 가능하게 한다.
- **Gap**: 기존 VLA RL 연구는 단편화되어 있으며 공정한 비교를 위한 통합 플랫폼이 부족하고, SimpleVLA-RL 같은 기존 방법들은 구체화된 환경에 맞춘 시스템 최적화가 부재하여 확장성이 제한된다.
- **Why**: 온라인 RL은 모델-환경 상호작용이 반복적이고 밀접하게 결합되어 있어 GPU 유휴 시간과 파이프라인 버블이 발생하기 쉽고, 다양한 시뮬레이터와 모델, 알고리즘을 공정하게 비교할 수 있는 통합 시스템이 필수적이다.
- **Approach**: RLinf-VLA는 다양한 VLA 아키텍처(OpenVLA, OpenVLA-OFT), RL 알고리즘(PPO, GRPO), 시뮬레이터(ManiSkill, LIBERO, RoboTwin)를 지원하는 통합 인터페이스를 제공하고, GPU 병렬화 시뮬레이터를 위한 하이브리드 fine-grained 파이프라인 할당 전략을 도입한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1:*

- **통합 시스템 추상화**: 다양한 시뮬레이터, VLA 아키텍처, RL 알고리즘을 지원하며 collocated, disaggregated, 새로운 hybrid 모드 등 세 가지 실행 모드를 제공
- **효율적 설계**: GPU 병렬화 시뮬레이터를 위한 hybrid fine-grained 파이프라인과 CPU 병렬화 시뮬레이터를 위한 collocated 실행으로 최대 2.27배 속도 향상 달성
- **강력한 성능**: LIBERO 130개 작업에서 98.11%, ManiSkill 25개 작업에서 97.66% 성공률, RoboTwin 6개 작업에서 평균 84.63% 성공률 달성
- **일반화 능력**: 단일 통합 모델이 여러 벤치마크에서 20-85% 성능 개선을 보여주며, RoboTwin 작업에서 평균 63.75% 성능 개선 달성
- **공개 플랫폼**: 오픈소스 활성 유지 플랫폼으로 구체화 인텔리전스 연구 표준화 및 재현성 향상

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Pipeline of Reinforcement Learning for VLA models*

- Generation, Simulator, Training의 세 가지 구성 요소를 포함하는 RL 파이프라인 구조 채택 및 GPU 자원 할당 최적화
- Chunk → Atomic Action → Token의 세 단계 계층 구조를 통해 VLA의 액션 표현 통일
- GPU 병렬화 시뮬레이터를 위한 hybrid fine-grained 파이프라인 할당으로 렌더링, 추론, 훈련 작업 간 효율적 자원 배분
- CPU 병렬화 시뮬레이터를 위한 collocated 실행 모드와 GPU 병렬화 시뮬레이터를 위한 disaggregated 모드 제공
- PPO와 GRPO 같은 다양한 RL 알고리즘의 통합 지원 및 알고리즘 수준의 최적화 포함
- ManiSkill, LIBERO, RoboTwin 등 이질적 시뮬레이터들의 일관된 인터페이스 제공으로 seamless 전환 가능

## Originality

- GPU 병렬화 시뮬레이터를 위한 hybrid fine-grained 파이프라인 할당 전략은 기존 LLM RL 프레임워크의 generic 접근을 벗어나 구체화 환경의 특수성을 반영한 혁신적 설계
- 다양한 시뮬레이터, 모델, 알고리즘을 하나의 통합 인터페이스로 지원하는 포괄적 플랫폼 설계로 공정한 비교 및 체계적 연구 가능성 창출
- Chunk 단위 액션 표현을 POMDP 프레임워크 내에서 통일적으로 처리하는 계층적 추상화 제시

## Limitation & Further Study

- 현재 평가는 주로 시뮬레이션 환경에 제한되어 있으며 실제 로봇 하드웨어에서의 성능 검증이 부족
- 다양한 VLA 아키텍처 지원을 주장하지만 OpenVLA와 OpenVLA-OFT 두 가지만 실험에 포함
- hybrid 파이프라인 할당 전략의 일반화 가능성이나 다른 유형의 GPU 병렬화 시뮬레이터에 대한 적용성 미명확
- 후속 연구로 실제 로봇 플랫폼에서의 대규모 훈련 실험, 더 많은 VLA 아키텍처의 통합, 그리고 sim-to-real 전이 학습 성능 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RLinf-VLA는 VLA 강화학습 연구의 단편화 문제를 해결하는 포괄적 통합 프레임워크이며, GPU 할당 최적화를 통한 실질적 효율성 개선과 강력한 실험 결과로 구체화 인텔리전스 연구의 주요 기초 시설로서의 가치를 입증한다.

## Related Papers

- 🔗 후속 연구: [[papers/1533_RLRC_Reinforcement_Learning-based_Recovery_for_Compressed_Vi/review]] — RLinf-VLA의 효율적인 RL 훈련 프레임워크가 RLRC의 압축된 VLA 모델 성능 복구와 결합되어 전체 배포 파이프라인을 완성한다.
- 🔄 다른 접근: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — RLinf-VLA와 VLA-RL은 모두 VLA 모델의 강화학습 적용을 다루지만 훈련 효율성과 일반적 성능 향상이라는 다른 초점을 가진다.
- 🏛 기반 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — VLA-RFT의 reinforcement fine-tuning 방법론이 RLinf-VLA의 통합 RL 프레임워크 설계의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1과 같은 기존 VLA 모델들의 강화학습 훈련을 RLinf-VLA 프레임워크로 효율적으로 최적화할 수 있다.
- 🏛 기반 연구: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — SimpleVLA-RL의 VLA 강화학습 스케일링 방법론이 RLinf-VLA의 효율적인 훈련 프레임워크 설계에 핵심 기반을 제공한다.
- 🏛 기반 연구: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — RLinf-VLA의 효율적인 VLA 훈련 프레임워크가 실시간 action chunking 정책의 최적화된 실행을 위한 기반 기술을 제공한다.
- 🏛 기반 연구: [[papers/1533_RLRC_Reinforcement_Learning-based_Recovery_for_Compressed_Vi/review]] — RLRC의 RL-based recovery를 위한 효율적인 VLA reinforcement learning training framework를 제공한다.
- 🔄 다른 접근: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — SimpleVLA-RL과 RLinf-VLA는 모두 VLA 강화학습을 다루지만 하나는 학습 확장, 다른 하나는 훈련 효율성에 집중한다.
- 🔗 후속 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — 강화학습 기반 시각 잠재 계획을 reinforcement learning framework에 통합할 수 있습니다.
- 🏛 기반 연구: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — VLA 모델의 강화학습 통합에 대한 통일된 프레임워크를 제공하여 VLA-RL의 방법론적 토대를 마련한다.
- 🔗 후속 연구: [[papers/1618_VLA-Reasoner_Empowering_Vision-Language-Action_Models_with_R/review]] — reinforcement learning framework를 test-time MCTS와 결합할 수 있습니다.
- 🔄 다른 접근: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — RLinf-VLA는 DRL 대신 VLA 모델에 RL을 통합하는 새로운 접근법으로 로봇 학습의 대안적 패러다임을 제시합니다.
- 🔗 후속 연구: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — VLA 모델에 특화된 강화학습 미세조정 프레임워크의 구체적 구현을 보여줍니다.
- 🔗 후속 연구: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — RLinf-VLA는 Embodied-R1의 RFT 훈련 방법을 다양한 VLA 모델로 확장하여 더 일반적인 강화 학습 프레임워크를 제공합니다.
