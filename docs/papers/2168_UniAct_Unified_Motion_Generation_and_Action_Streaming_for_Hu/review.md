---
title: "2168_UniAct_Unified_Motion_Generation_and_Action_Streaming_for_Hu"
authors:
  - "Nan Jiang"
  - "Zimo He"
  - "Wanhe Yu"
  - "Lexi Pang"
  - "Yunhao Li"
date: "2025.12"
doi: "10.48550/arXiv.2512.24321"
arxiv: ""
score: 4.0
essence: "UniAct는 MLLM과 causal streaming pipeline을 결합한 두 단계 프레임워크로, 인간형 로봇이 언어, 음악, 궤적 등 다양한 multimodal 명령을 sub-500ms 지연시간으로 실행할 수 있게 한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Jiang et al._2025_UniAct Unified Motion Generation and Action Streaming for Humanoid Robots.pdf"
---

# UniAct: Unified Motion Generation and Action Streaming for Humanoid Robots

> **저자**: Nan Jiang, Zimo He, Wanhe Yu, Lexi Pang, Yunhao Li, Hongjie Li, Jieming Cui, Yuhan Li, Yizhou Wang, Yixin Zhu, Siyuan Huang | **날짜**: 2025-12-30 | **DOI**: [10.48550/arXiv.2512.24321](https://doi.org/10.48550/arXiv.2512.24321)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. UniAct, a unified framework for multimodal motion generation and action streaming. UniAct enables humanoid rob*

UniAct는 MLLM과 causal streaming pipeline을 결합한 두 단계 프레임워크로, 인간형 로봇이 언어, 음악, 궤적 등 다양한 multimodal 명령을 sub-500ms 지연시간으로 실행할 수 있게 한다.

## Motivation

- **Known**: 인간형 로봇 제어는 저수준 추적과 제어에서 진전했으나, 고수준 multimodal 인식과 전신 실행 간의 격차가 남아있다. 기존 방법들은 end-to-end 매핑이나 계층적 파이프라인 중 하나를 채택하여 real-time 응답성과 명령 이해 간 트레이드오프를 겪고 있다.
- **Gap**: 다양한 modality의 명령을 물리적으로 타당한 움직임으로 안정적이고 실시간으로 변환하는 unified framework가 부재하며, 불완전한 인간 시연에 대한 robustness도 부족하다.
- **Why**: 인간형 로봇의 multimodal instruction following 능력은 일반적 목적의 로봇 어시스턴트 실현에 필수적이며, sub-500ms 응답 지연은 대화형 interaction을 가능하게 한다.
- **Approach**: UniAct는 FSQ를 통해 이질적 입력을 공유 discrete codebook으로 통합하여 cross-modal alignment를 확보하고, MLLM 기반 생성 단계와 causal decoder를 거쳐 robust motion tracker로 실행한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3. UA-Net dataset analysis. (a) Representative text descriptions of human motions from UA-Net. (b) Rendered motio*

- **Unified multimodal framework**: 언어, 음악, 궤적, reference 동작을 하나의 discrete token 공간으로 통합하여 seamless cross-modal translation 실현
- **Low-latency real-time execution**: Sub-500ms 응답 지연으로 responsive humanoid assistant 구현
- **19% improvement in zero-shot tracking**: 불완전한 reference motion에 대한 zero-shot 추적 성공률 향상
- **Comprehensive evaluation**: 1,000+ 시뮬레이션 시행과 100+ 시간의 실제 로봇 운영을 통한 검증
- **UA-Net benchmark**: 20시간 규모의 multimodal 주석이 달린 고품질 인간형 로봇 동작 데이터셋 제공

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of UniAct and multimodal representations.*

- **FSQ 기반 토큰화**: 텍스트, 음악, 궤적, reference motion을 discrete token 표현으로 변환하여 입력 통일
- **MLLM 기반 생성**: Fine-tuned MLLM이 multimodal 입력을 reasoning하여 motion token sequence 생성
- **Causal streaming decoder**: Next-token prediction 패러다임으로 생성된 토큰을 실시간 명령으로 변환
- **Robust motion tracker**: 생성된 명령을 물리적으로 타당한 움직임으로 실행하며 동적 균형 유지
- **Physically grounded manifold**: Discrete action space로 생성을 물리적으로 실현 가능한 영역에 제약

## Originality

- Humanoid control에서 처음으로 MLLM과 robust tracker를 unified framework로 결합
- FSQ 기반의 shared discrete codebook으로 heterogeneous multimodal inputs의 seamless translation 달성
- Causal streaming pipeline을 통해 diffusion 기반 방법 대비 sub-500ms 지연 실현
- Multimodal annotation이 포함된 대규모 humanoid-specific 데이터셋(UA-Net) 구축

## Limitation & Further Study

- 실제 deployment에서의 추가 hardware 제약이나 환경 perturbation에 대한 robustness 평가 부족
- MLLM의 inference 능력 한계로 인한 복잡한 의미론적 추론의 제한 가능성
- Cross-embodiment generalization 성능 미평가 — 다른 humanoid 형태에 대한 일반화 능력 미검증
- UA-Net의 20시간 규모는 대규모 데이터셋 기준으로 여전히 제한적일 수 있음
- **후속 연구**: OOD 상황에 대한 adaptability 강화, 다양한 humanoid morphology에 대한 transfer learning 연구, 더 큰 규모의 multimodal dataset 구축 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: UniAct는 MLLM과 robust tracking을 unified framework로 통합하여 실제 humanoid robot에서 multimodal instruction following을 low latency로 달성한 의미 있는 연구이며, UA-Net 데이터셋 기여와 함께 embodied AI 분야에서 중요한 진전을 나타낸다.

## Related Papers

- 🏛 기반 연구: [[papers/1815_Being-M05_A_Real-Time_Controllable_Vision-Language-Motion_Mo/review]] — Being-M0.5의 실시간 controllable vision-language-motion 기술이 UniAct의 multimodal 명령 처리와 streaming pipeline 구현을 위한 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1893_ECHO_Edge-Cloud_Humanoid_Orchestration_for_Language-to-Motio/review]] — UniAct은 sub-500ms 지연시간에 집중하고 ECHO는 edge-cloud 분산 처리를 통한 서로 다른 실시간 language-to-motion 접근법입니다.
- 🔗 후속 연구: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — UniAct의 multimodal 명령 처리를 EMOTION의 expressive motion sequence generation과 결합하면 더 감정적이고 표현적인 실시간 휴머노이드 제어가 가능합니다.
- 🏛 기반 연구: [[papers/2147_TeleGate_Whole-Body_Humanoid_Teleoperation_via_Gated_Expert/review]] — 실시간 전신 원격조종의 기본 기술이 다양한 multimodal 명령의 통합 스트리밍 실행으로 확장된다.
- 🔄 다른 접근: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — TextOp의 real-time text-driven control과 UniAct의 multimodal command streaming은 서로 다른 input modality 처리 방식을 비교할 수 있음
- 🏛 기반 연구: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — language to locomotion의 retargeting-free 접근법이 UniAct의 MLLM 기반 multimodal 명령 처리의 이론적 기반을 제공함
- 🔄 다른 접근: [[papers/2161_Trinity_A_Modular_Humanoid_Robot_AI_System/review]] — Trinity의 modular AI system과 UniAct의 unified streaming framework는 휴머노이드 AI 시스템의 서로 다른 아키텍처 접근법임
- 🏛 기반 연구: [[papers/1821_BFM-Zero_A_Promptable_Behavioral_Foundation_Model_for_Humano/review]] — promptable behavioral foundation model의 기초 기술이 unified motion generation과 action streaming에 활용된다.
- 🔗 후속 연구: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — CLoSD의 diffusion-RL 폐쇄 루프가 UniAct의 통합 모션 생성으로 확장되어 더 seamless한 행동 스트리밍을 달성할 수 있다
- 🧪 응용 사례: [[papers/1886_DreamControl_Human-Inspired_Whole-Body_Humanoid_Control_for/review]] — 통합 모션 생성과 행동 스트리밍의 실제 구현 사례를 보여줍니다.
- 🔗 후속 연구: [[papers/1937_FRoM-W1_Towards_General_Humanoid_Whole-Body_Control_with_Lan/review]] — UniAct의 통합 동작 생성 및 행동 스트리밍이 FRoM-W1의 언어-전신 제어를 더욱 일반화된 형태로 발전시켰습니다.
- 🔗 후속 연구: [[papers/1952_GENMO_A_GENeralist_Model_for_Human_MOtion/review]] — GENMO의 통합 동작 추정-생성을 UniAct의 unified motion generation과 결합하면 더 포괄적인 휴머노이드 행동 시스템이 가능하다.
- 🔗 후속 연구: [[papers/2147_TeleGate_Whole-Body_Humanoid_Teleoperation_via_Gated_Expert/review]] — 실시간 전신 원격조종 기술을 다양한 multimodal 명령 스트리밍으로 확장한 발전된 형태이다.
