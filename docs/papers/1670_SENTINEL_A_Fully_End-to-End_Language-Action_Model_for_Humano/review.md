---
title: "1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano"
authors:
  - "Yuxuan Wang"
  - "Haobin Jiang"
  - "Shiqing Yao"
  - "Ziluo Ding"
  - "Zongqing Lu"
date: "2025.11"
doi: "10.48550/arXiv.2511.19236"
arxiv: ""
score: 4.0
essence: "SENTINEL은 언어 명령을 휴머노이드 로봇의 저수준 제어 신호로 직접 변환하는 완전 end-to-end 언어-행동 모델로, flow matching을 통해 행동 청크를 생성하고 실제 배포를 위해 잔여 강화학습으로 정제한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_SENTINEL A Fully End-to-End Language-Action Model for Humanoid Whole Body Control.pdf"
---

# SENTINEL: A Fully End-to-End Language-Action Model for Humanoid Whole Body Control

> **저자**: Yuxuan Wang, Haobin Jiang, Shiqing Yao, Ziluo Ding, Zongqing Lu | **날짜**: 2025-11-24 | **DOI**: [10.48550/arXiv.2511.19236](https://doi.org/10.48550/arXiv.2511.19236)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of SENTINEL. Our framework consists of three stages. (1) We construct a language-*

SENTINEL은 언어 명령을 휴머노이드 로봇의 저수준 제어 신호로 직접 변환하는 완전 end-to-end 언어-행동 모델로, flow matching을 통해 행동 청크를 생성하고 실제 배포를 위해 잔여 강화학습으로 정제한다.

## Motivation

- **Known**: 기존 휴머노이드 제어는 원격조종이나 language understanding과 physical execution을 분리하는 모듈식 파이프라인에 의존한다. text-to-motion 모델과 whole body controller의 결합은 두 컴포넌트가 독립적으로 최적화되어 물리적으로 실현 불가능한 동작을 생성한다.
- **Gap**: 모듈식 파이프라인은 중간 표현 또는 정렬 모듈이 필요하여 language-kinematic 간의 tight alignment가 부족하다. 중간 표현 없이 직접 저수준 행동으로 매핑하는 완전 end-to-end 모델은 아직 없다.
- **Why**: end-to-end 접근은 gradient flow를 통해 execution feedback을 language understanding으로 역전파하여 전체 시스템의 joint optimization이 가능하므로, 더 강건하고 일반화 가능한 언어-조건부 구체화 지능을 실현할 수 있다.
- **Approach**: 먼저 pre-trained whole body controller로 인간 동작을 시뮬레이션에서 추적하여 언어-행동 데이터셋을 구성한다. 그 후 flow matching 행동 전문가를 가진 end-to-end 모델을 behavior cloning으로 pre-training하고, 잔여 강화학습으로 open-loop drift를 완화하고 real-world deployment에 적응시킨다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of SENTINEL. Our framework consists of three stages. (1) We construct a language-*

- **완전 end-to-end 프레임워크**: 중간 motion representation이나 latent abstraction 없이 언어와 proprioceptive state를 직접 저수준 29 DoF 타겟으로 변환
- **안정적인 실제 배포**: 시뮬레이션과 실제 로봇에서 strong semantic grounding과 물리적으로 안정적인 행동 실행 달성
- **multi-modal 확장성**: 시각 입력을 waypoint 언어 표현으로 변환하여 navigation 등 추가 모달리티 통합 지원
- **세 단계 학습 파이프라인**: WBC training & BC data collection → flow matching을 통한 pre-training → residual RL post-training으로 점진적 성능 향상

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of SENTINEL. Our framework consists of three stages. (1) We construct a language-*

- Mixture-of-Expert (MoE) policy를 PPO로 학습하여 diverse human motion을 humanoid에서 추적하는 whole body controller 구현
- 공개 human motion 데이터셋과 natural language 설명으로 BC 데이터셋 구성
- CLIP text encoder로 언어 임베딩을 인코딩하고, transformer 기반 언어-상태 인코더로 proprioception history와 결합
- Flow matching을 통해 Gaussian noise에서 action 분포로의 생성 과정을 학습하여 action chunk 생성
- Done prediction head로 open-loop drift 감지 및 action chunk 종료 판단
- Residual RL로 LA 모델의 출력에 잔여 행동을 더하여 real-world deployment 적응 및 refinement

## Originality

- **완전 end-to-end 설계**: 모든 intermediate motion representation을 제거하고 직접 저수준 제어로의 완전 end-to-end 매핑은 기존 문헌에서 사례를 찾기 어려움
- **Flow matching의 행동 생성 적용**: action generation에 flow matching을 적용한 것은 이전에 시도되지 않은 새로운 접근
- **Residual RL을 통한 sim-to-real 적응**: pre-trained 모델에 잔여 강화학습을 추가하는 방식으로 domain randomization과 함께 real-world 배포 최적화
- **Multi-modal 확장성**: 언어로의 입력 변환을 통해 시각, 음성 등 다양한 모달리티 통합 가능한 설계

## Limitation & Further Study

- **데이터셋 규모 및 다양성**: human motion 데이터셋과 text annotation의 규모가 제한되어 있어 더 광범위한 태스크로의 일반화 능력 미지수
- **Action chunking의 open-loop drift**: 고정된 크기의 action chunk로 인한 누적 오류 문제를 residual RL로 완화하지만 근본적 해결은 아님
- **실제 환경의 복잡성**: 시뮬레이션-현실 간 gap이 여전히 존재하며, 매우 동적이거나 예측 불가능한 환경에서의 성능 미평가
- **Transformer 인코더의 계산 비용**: 실시간 제어에 필요한 inference latency와 메모리 사용량에 대한 상세한 분석 부재
- **후속 연구 방향**: (1) 대규모 language-labeled motion 데이터셋 확보, (2) Attention 메커니즘으로의 환경 피드백 실시간 통합, (3) 다양한 로봇 플랫폼으로의 확장성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SENTINEL은 언어-조건부 휴머노이드 제어를 위한 완전 end-to-end 접근의 첫 사례로, 중간 표현을 제거하고 flow matching과 residual RL을 결합한 창의적인 방법론을 제시한다. 시뮬레이션과 실제 로봇 모두에서의 성공적인 배포는 본 접근의 타당성을 입증하며, 향후 구체화 AI 발전에 중요한 기초를 마련한다.

## Related Papers

- 🔄 다른 접근: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — SENTINEL의 flow matching 기반 행동 생성과 Humanoid-LLA의 통합 모션 어휘는 언어-행동 변환의 서로 다른 아키텍처
- 🏛 기반 연구: [[papers/1643_RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with/review]] — RLPF의 강화학습 기반 모션 모델 정제가 SENTINEL의 잔여 강화학습 정제 방법론의 직접적 기반
- 🔗 후속 연구: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — TextOp의 실시간 스트리밍 제어가 SENTINEL의 end-to-end 모델을 동적 명령 수정으로 확장
- 🔗 후속 연구: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — 언어 명령을 휴머노이드 제어로 변환하는 작업에서 SENTINEL의 end-to-end 접근법과 SCHUR의 대규모 데이터 기반 접근법이 상호 보완적이다.
- 🧪 응용 사례: [[papers/2161_Trinity_A_Modular_Humanoid_Robot_AI_System/review]] — 언어 기반 휴머노이드 제어에서 SENTINEL의 언어-행동 모델이 Trinity의 모듈러 AI 시스템에 통합될 수 있다.
- 🔄 다른 접근: [[papers/1702_Task_and_Motion_Planning_for_Humanoid_Loco-manipulation/review]] — 둘 다 언어에서 휴머노이드 제어로의 변환을 다루지만 SENTINEL은 end-to-end 학습, TAMP는 계획 기반 접근을 사용한다
- 🔗 후속 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — SENTINEL의 언어-행동 모델과 SignBot의 수화 상호작용을 결합하면 다중 모달 의사소통이 가능한 휴머노이드를 구현할 수 있다
- 🔄 다른 접근: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — LLM을 활용한 언어-행동 모델링에서 제스처 생성과 전신 제어라는 서로 다른 응용 영역을 다룬다.
- 🔄 다른 접근: [[papers/1643_RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with/review]] — RLPF의 물리 피드백 기반 모션 모델 조정과 SENTINEL의 end-to-end 언어-행동 모델은 상호 보완적 접근법
- 🏛 기반 연구: [[papers/1662_SafeFlow_Real-Time_Text-Driven_Humanoid_Whole-Body_Control_v/review]] — SENTINEL의 end-to-end 언어-행동 모델이 SafeFlow의 텍스트 명령 기반 전신 제어의 직접적 기반
- ⚖️ 반론/비판: [[papers/1702_Task_and_Motion_Planning_for_Humanoid_Loco-manipulation/review]] — TAMP의 체계적 계획 접근이 SENTINEL의 end-to-end 학습 한계를 보완하는 대안적 관점을 제시한다
- 🏛 기반 연구: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — SENTINEL의 end-to-end 언어-행동 모델이 TextOp의 실시간 텍스트 기반 모션 생성의 기본 변환 구조
- 🔄 다른 접근: [[papers/1252_ActiveUMI_Robotic_Manipulation_with_Active_Perception_from_R/review]] — 둘 다 언어 명령을 로봇 행동으로 변환하지만 VoxPoser는 3D value map을, SENTINEL은 end-to-end 학습을 사용한다
- 🏛 기반 연구: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — 대규모 데이터와 모델 스케일링이 SENTINEL의 end-to-end 언어-행동 모델의 성능 향상에 기여할 수 있다.
- 🏛 기반 연구: [[papers/1813_Being-0_A_Humanoid_Robotic_Agent_with_Vision-Language_Models/review]] — end-to-end 언어-행동 모델이 Being-0의 Connector 모듈에서 언어 명령을 실행 가능한 스킬로 변환하는 이론적 기반을 제공한다
- 🏛 기반 연구: [[papers/1819_Beyond_Tools_and_Persons_Who_Are_They_Classifying_Robots_and/review]] — CPST 이론 기반의 로봇 분류가 SENTINEL의 end-to-end 언어-행동 모델에서 AI 에이전트의 법적 지위 정의에 이론적 기반을 제공한다
- 🏛 기반 연구: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — SENTINEL의 flow matching 기반 행동 생성이 CLoSD의 motion diffusion 모델과 직접적으로 연관된 기반 기술
- 🔄 다른 접근: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — 통합 모션 어휘 기반 언어 처리와 SENTINEL의 flow matching은 자유형식 자연언어 제어의 서로 다른 아키텍처
- 🏛 기반 연구: [[papers/1868_DexHub_and_DART_Towards_Internet_Scale_Robot_Data_Collection/review]] — 언어-행동 모델 학습을 위한 데이터 수집 플랫폼을 제공합니다.
- 🔄 다른 접근: [[papers/1898_EgoActor_Grounding_Task_Planning_into_Spatial-aware_Egocentr/review]] — VLM 기반 통합 제어에서 spatial-aware egocentric action과 end-to-end language-action model의 서로 다른 언어 기반 제어 접근법을 비교한다.
- 🏛 기반 연구: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — SENTINEL의 end-to-end language-action model이 RoboGhost의 직접적인 언어-동작 변환 프레임워크의 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — SENTINEL의 언어-행동 모델이 HIAER의 Vision Language Model 기반 의도 추론의 핵심 토대가 된다.
- 🏛 기반 연구: [[papers/1992_Humanoid_Agent_via_Embodied_Chain-of-Action_Reasoning_with_M/review]] — SENTINEL의 end-to-end language-action model이 embodied CoA reasoning의 기반이 됩니다.
- 🔄 다른 접근: [[papers/2025_INTENTION_Inferring_Tendencies_of_Humanoid_Robot_Motion_Thro/review]] — 둘 다 언어-행동 모델이지만 INTENTION은 직관적 물리 이해 중심, SENTINEL은 end-to-end 언어-행동 매핑 중심
- 🔄 다른 접근: [[papers/2039_LangWBC_Language-directed_Humanoid_Whole-Body_Control_via_En/review]] — 언어-행동 모델에서 SENTINEL은 완전 end-to-end를, LangWBC는 CVAE 기반 접근 사용
- 🔗 후속 연구: [[papers/2081_LeVERB_Humanoid_Whole-Body_Control_with_Latent_Vision-Langua/review]] — 완전한 종단간 언어-행동 모델의 확장된 구현을 보여준다.
