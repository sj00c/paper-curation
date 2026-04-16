---
title: "1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action"
authors:
  - "Zhenyang Liu"
  - "Yongchong Gu"
  - "Sixiao Zheng"
  - "Yanwei Fu"
  - "Xiangyang Xue"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "인지신경과학의 에피소딕 메모리 이론에서 영감을 받아, 과거 경험의 축적·회상과 미래 동역학 예측을 통합하는 에피소딕 월드 모델을 VLA 프레임워크에 처음 도입한 TriVLA를 제안한다. Vision-Language Model, Video Diffusion Model, Policy 네트워크의 삼중 시스템 아키텍처로 구현되어 긴 지평의 조작 작업에서 문맥-인식적 행동 생성을 가능하게 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2025_TriVLA A Triple-System-Based Unified Vision-Language-Action Model with Episodic World Modeling for.pdf"
---

# TriVLA: A Triple-System-Based Unified Vision-Language-Action Model with Episodic World Modeling for General Robot Control

> **저자**: Zhenyang Liu, Yongchong Gu, Sixiao Zheng, Yanwei Fu, Xiangyang Xue, Yu-Gang Jiang | **날짜**: 2025-07-02 | **URL**: [https://arxiv.org/abs/2507.01424](https://arxiv.org/abs/2507.01424)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: TriVLA is a unified Vision-Language-Action framework that adopts a triple-system ar-*

인지신경과학의 에피소딕 메모리 이론에서 영감을 받아, 과거 경험의 축적·회상과 미래 동역학 예측을 통합하는 에피소딕 월드 모델을 VLA 프레임워크에 처음 도입한 TriVLA를 제안한다. Vision-Language Model, Video Diffusion Model, Policy 네트워크의 삼중 시스템 아키텍처로 구현되어 긴 지평의 조작 작업에서 문맥-인식적 행동 생성을 가능하게 한다.

## Motivation

- **Known**: Vision-Language Model(VLM)은 개방형 지시를 따르고 상식 추론에 우수하며, 최근 VLA 프레임워크는 VLM을 기반으로 행동 계획과 SE(3) 포즈 예측을 수행한다. 그러나 기존 VLA 모델들은 정적 표현과 제한된 시간적 문맥에 의존하여 단기 반응형 행동에만 능하다.
- **Gap**: 현재 VLA 시스템은 순간적 관찰에만 의존하여 시간적으로 확장된 경험을 인코딩하지 못하며, 동적 환경에서의 강건한 일반화를 제한한다. 에피소딕 메모리처럼 과거와 미래를 모두 통합하는 temporal reasoning 메커니즘이 부재하다.
- **Why**: 로봇이 복잡한 지시를 이해하고 긴 지평의 작업을 계획하려면 순차적 경험을 축적·회상하고 미래 환경 진화를 예측할 수 있어야 하며, 이는 동적 구현체 환경에서 강건하고 일반화 가능한 로봇 지능의 핵심이다.
- **Approach**: Vision-Language Model(System 2)을 통해 관찰과 지시를 해석하고, Video Diffusion Model(System 3)을 통해 과거 상태 시퀀스와 미래 씬 궤적을 인코딩한 후, 이 두 시스템으로부터의 표현을 통합하는 Policy 네트워크(System 1)가 flow-matching과 cross-modal attention을 활용하여 맥락-인식적 행동 시퀀스를 생성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: TriVLA is a unified Vision-Language-Action framework that adopts a triple-system ar-*

- **에피소딕 월드 모델 개념 도입**: 인지신경과학 이론에 기반한 에피소딕 메모리 원칙을 구현하여 로봇이 순차적 다중모달 경험을 축적, 회상, 예측하도록 함
- **삼중 시스템 아키텍처 설계**: System 2의 다중모달 그라운딩과 System 3의 시간 풍부 동역학 모델링을 System 1의 정책 학습에 통합하는 구성적 프레임워크 구현
- **벤치마크 성능 개선**: Calvin ABC→D에서 0.21, LIBERO에서 0.11, MetaWorld에서 0.13의 성능 향상 달성
- **실시간 효율성**: 약 36 Hz 주파수로 동작하는 효율적인 시스템 구현
- **장기 지평 및 개방형 이해**: 실세계 조작 작업과 복합 도구 사용 작업에서 강력한 긴 지평 계획 및 개방형 의도 이해 능력 시연

## How

![Figure 3](figures/fig3.webp)

*Figure 3: The pipeline of TriVLA. TriVLA is a unified Vision-Language-Action framework built*

- **System 2 (Episodic Multimodal Perception)**: Eagle-2 VLM을 사용하여 비전-언어 입력을 처리하고 작업 목표와 문맥 단서를 해석
- **System 3 (Episodic Dynamics Perception)**: Stable Video Diffusion을 인간 및 로봇 조작 데이터셋에 파인튜닝하여 과거 상태 시퀀스로부터 미래 장면 궤적 예측
- **System 1 (Lower-Level Policy)**: Diffusion Transformer 기반 정책으로, flow-matching 메커니즘을 통해 System 2와 3의 출력 토큰을 통합하고 cross-modal attention으로 로봇 상태 및 행동 이력을 고려
- **청크 기반 행동 생성**: 각 타임스텝의 단일 행동 대신 행동의 청크를 예측하여 묵시적 역동역학 사전(inverse-dynamics prior) 유도
- **구현체 특화 인코더/디코더**: 가변하는 상태 및 행동 차원을 관리하기 위한 구현체 특화 모듈 설계

## Originality

- **인지과학 기반 개념화**: 에피소딕 메모리 이론을 명시적으로 로봇 제어에 구현한 것으로, VLA 분야에서 처음으로 정형화된 에피소딕 월드 모델 제안
- **삼중 시스템 구조**: 기존 dual-system 아키텍처를 Video Diffusion Model을 추가하여 확장하여 temporal reasoning 능력 통합
- **통합 프레임워크**: 다중모달 그라운딩(System 2), 동역학 예측(System 3), 정책 학습(System 1)을 통합된 단일 프레임워크로 구현하는 구성적 접근
- **역동역학 사전 유도**: 행동 시퀀스 모니터링을 통해 정책이 자동으로 역동역학 사전을 습득하도록 설계하여 시각 도메인으로의 일반화 전이 촉진

## Limitation & Further Study

- **계산 복잡도**: 세 개의 독립 모델(VLM, VDM, Policy)을 병렬로 실행하므로 에지 디바이스 배포 시 메모리 및 계산 부담이 증가할 수 있음
- **모델 파인튜닝 의존성**: System 3 (Video Diffusion Model)의 성능이 로봇 조작 데이터셋의 품질과 규모에 크게 의존하며, 충분한 데이터 없는 새로운 도메인으로의 전이 학습 성능 미명확
- **System 간 오류 누적**: 다중 시스템 통합에서 System 2나 3의 오류가 System 1의 정책 학습에 영향을 미칠 수 있으며, 이러한 오류 전파 메커니즘에 대한 상세 분석 부재
- **평가 범위 제약**: 실세계 실험이 주로 조작 작업 중심이며, 네비게이션이나 이동-조작 복합 작업에 대한 평가 부족
- **후속 연구 방향**: (1) 경량화 및 증류 기법을 통한 모바일 로봇 적용 확대, (2) 적응적 시스템 가중치 조정으로 오류 누적 완화, (3) 다양한 도메인의 로봇 작업에 대한 확장성 검증, (4) 에피소딕 메모리의 장기 저장 및 활용 메커니즘 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: TriVLA는 인지신경과학의 에피소딕 메모리 개념을 체계적으로 로봇 제어에 도입한 혁신적인 연구로, 삼중 시스템 아키텍처를 통해 temporal reasoning과 문맥-인식적 행동 생성을 통합하여 기존 VLA 모델의 한계를 명확히 극복한다. 벤치마크 및 실세계 작업에서의 우수한 성능과 함께 개념적 명확성을 제시하는 높은 질의 논문이다.

## Related Papers

- 🏛 기반 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — embodied AI를 위한 world model의 포괄적 이해를 제공하는 기반 서베이 연구입니다.
- 🔗 후속 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — human video로부터 구조화된 world model을 에피소딕 메모리와 결합할 수 있습니다.
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — 장기 지평 작업을 위한 서로 다른 접근법 - 에피소딕 메모리 vs 명시적 상태 유지입니다.
- 🔄 다른 접근: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — 둘 다 embodied AI를 위한 world model을 제안하지만 TriVLA는 에피소딕 메모리에, WHALE은 행동 조건화에 중점을 둔다.
- 🏛 기반 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — 비디오 foundation model을 통한 세계 시뮬레이션 연구가 TriVLA의 Video Diffusion Model 기반 미래 예측 시스템의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1631_World_Models/review]] — 기본적인 생성형 world model을 에피소딕 메모리와 삼중 시스템 아키텍처로 확장하여 장기 조작 작업에 특화했다.
- 🔄 다른 접근: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — 둘 다 메모리와 추론을 VLA에 통합하지만 TriVLA는 에피소딕 메모리에, TrackVLA++는 tracking memory에 집중합니다.
- 🏛 기반 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — world model을 통한 다양한 도메인 마스터링 개념을 제공하여 TriVLA의 에피소딕 월드 모델에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma/review]] — TriVLA의 삼중 시스템 구조가 Fast-in-Slow의 dual-system 설계를 이론적으로 확장한 기반을 제공합니다.
- ⚖️ 반론/비판: [[papers/1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti/review]] — unified VLA vs triple-system 기반의 다른 시스템 통합 철학
- 🏛 기반 연구: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — OpenHelix가 분석한 dual-system VLA의 기초가 되는 triple-system 아키텍처 연구
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — 상태 유지를 위한 서로 다른 접근법 - 명시적 상태 추적 vs 에피소딕 메모리 시스템입니다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — 고수준 추론과 저수준 행동의 연결을 위한 서로 다른 아키텍처 - 이중 시스템 vs 삼중 시스템입니다.
- 🔄 다른 접근: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — 둘 다 VLA 모델에 메모리 기능을 추가하지만 TrackVLA++는 tracking 특화 TIM을, TriVLA는 에피소딕 월드 모델을 사용한다.
- 🔄 다른 접근: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — 둘 다 embodied AI용 world model이지만 WHALE은 행동 조건화에, TriVLA는 에피소딕 메모리에 중점을 둔다.
- 🏛 기반 연구: [[papers/1631_World_Models/review]] — World Models의 생성형 world model 개념이 TriVLA의 에피소딕 월드 모델과 미래 동역학 예측의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1373_DualVLA_Building_a_Generalizable_Embodied_Agent_via_Partial/review]] — TriVLA의 삼중 시스템 구조가 DualVLA의 추론-행동 분리 개념의 이론적 확장 기반을 제공합니다.
