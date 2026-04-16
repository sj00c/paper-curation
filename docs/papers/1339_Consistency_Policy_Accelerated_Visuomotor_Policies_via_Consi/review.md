---
title: "1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi"
authors:
  - "Aaditya Prasad"
  - "Kevin Lin"
  - "Jimmy Wu"
  - "Linqi Zhou"
  - "Jeannette Bohg"
date: "2024.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Consistency Policy는 Diffusion Policy를 Consistency Distillation을 통해 단일 스텝으로 빠르게 추론할 수 있도록 가속화한 로보틱 비주얼모터 정책으로, 자원 제약이 있는 로봇 시스템에서 저지연 의사결정을 가능하게 한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Prasad et al._2024_Consistency Policy Accelerated Visuomotor Policies via Consistency Distillation.pdf"
---

# Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation

> **저자**: Aaditya Prasad, Kevin Lin, Jimmy Wu, Linqi Zhou, Jeannette Bohg | **날짜**: 2024-05-13 | **URL**: [https://arxiv.org/abs/2405.07503](https://arxiv.org/abs/2405.07503)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Both Diffusion and Consistency Policy work by sampling random*

Consistency Policy는 Diffusion Policy를 Consistency Distillation을 통해 단일 스텝으로 빠르게 추론할 수 있도록 가속화한 로보틱 비주얼모터 정책으로, 자원 제약이 있는 로봇 시스템에서 저지연 의사결정을 가능하게 한다.

## Motivation

- **Known**: Diffusion Policy는 로봇 제어에서 뛰어난 모방 학습 성능을 보이지만 100개의 denoising step이 필요해 약 1초의 추론 시간이 소요된다. 이미지 생성 도메인에서는 Consistency Model을 통한 distillation으로 단계 수를 감소시키는 방법이 개발되어 있다.
- **Gap**: 로봇 비주얼모터 정책에서 Diffusion Policy의 높은 성능을 유지하면서 추론 속도를 획기적으로 단축하는 방법이 부재하며, Consistency Model을 로보틱 도메인에 효과적으로 적응시킨 연구가 없다.
- **Why**: 많은 로봇 시스템은 공간, 무게, 전력 제약으로 고성능 GPU를 장착할 수 없어 동적 작업이나 실시간 제어가 필요한 경우 Diffusion Policy를 활용할 수 없으므로, 빠른 추론 속도와 높은 성능을 모두 갖춘 대안이 필수적이다.
- **Approach**: Pretrained Diffusion Policy를 EDM framework로 재구성하고 Consistency Trajectory Model (CTM) objective를 사용한 consistency distillation으로 student model을 훈련하여, ODE 궤적의 self-consistency를 강제한다. 주요 설계 결정으로는 consistency objective의 선택, 감소된 초기 샘플 분산, preset chaining steps 설정이 포함된다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Both Diffusion and Consistency Policy work by sampling random*

- **추론 속도 향상**: 모든 테스트 작업에서 가장 빠른 대안 대비 약 10배 빠른 추론 속도 달성 (1초 → ~0.1초 수준)
- **성능 유지**: 6개 시뮬레이션 작업과 3개 실제 로봇 작업에서 Diffusion Policy와 경쟁력 있는 또는 더 높은 성공률 유지
- **저사양 하드웨어 호환**: 노트북 GPU에서의 추론을 시연하여 자원 제약이 있는 로봇 시스템에서의 실용성 입증
- **강건성**: Pretrained Diffusion Policy의 품질에 robust하므로 실무자가 teacher model의 광범위한 테스트를 피할 수 있음

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: CTM enforces self-consistency along a PFODE (black) by sampling*

- EDM framework를 사용하여 DDPM 기반의 Diffusion Policy를 ODE 기반 multi-step framework로 전환
- Consistency Trajectory Model (CTM) objective를 로보틱 도메인에 적응시켜 ODE 궤적의 self-consistency 강제
- ODE상의 서로 다른 두 지점에서 동일한 출력을 예측하도록 student model 훈련
- 초기 샘플 분산 감소 및 preset chaining steps 설정을 통한 성능 최적화
- Dropout의 역할을 특정 CTM objective 영역에서 분석하여 설계 개선
- 6개 시뮬레이션 작업(RoboMimic, state-based 작업)과 3개 실제 로봇 작업에서 체계적으로 평가

## Originality

- 이미지 생성 도메인의 CTM을 처음으로 로보틱 비주얼모터 정책에 성공적으로 적응
- DDPM에서 EDM으로의 framework 변환을 통해 consistency distillation의 효과적 적용 가능 입증
- 로보틱 도메인에 특화된 consistency objective, 초기 분산 감소, chaining steps 설정 등 주요 설계 결정 제시
- Teacher model 품질에 대한 robustness 분석을 통한 실무적 가이드라인 제공
- 단일 스텝 생성으로 기존 병렬화 방법(ParaDiGMS)보다 더 나은 성능과 메모리 효율성 달성

## Limitation & Further Study

- 단일 스텝 생성으로의 극단적 단축으로 인해 매우 복잡한 작업에서 성능 저하 가능성 미검토
- Laptop GPU 수준의 성능만 시연되었으며, 극도로 제한된 엣지 디바이스(마이크로컨트롤러 등)에서의 적용 가능성 불명확
- 실제 로봇 작업이 3개만 포함되어 다양한 실세계 도메인에서의 일반화 능력 검증 부족
- 다른 최신 단계 감축 기법(few-step schemes)과의 비교 분석 부족
- 후속 연구: 다중 스텝 생성 옵션(few-step inference) 지원으로 성능-속도 트레이드오프 조정 가능성 탐색
- 후속 연구: 매우 저사양 임베디드 환경에서의 적용 및 최적화 방법 개발
- 후속 연구: 시뮬레이션-실제 전이(sim-to-real) 성능 개선 전략 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 이미지 생성 도메인의 Consistency Model을 로보틱 비주얼모터 정책에 처음 성공적으로 적용하여, 기존 Diffusion Policy의 높은 성능을 유지하면서 10배 이상의 추론 속도 향상을 달성한 중요한 기여이다. 자원 제약이 있는 로봇 시스템에서의 실용적 가치가 높고, 설계 선택에 대한 명확한 정당성과 실험 검증이 체계적이어서 로보틱 제어 분야에 큰 영향을 미칠 가능성이 높다.

## Related Papers

- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Action Diffusion을 통한 visuomotor 정책 학습의 원리적 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — VLA 모델 가속화를 위한 구조적 가지치기의 구체적인 적용 사례입니다.
- 🔄 다른 접근: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — Diffusion policy의 속도 개선을 위한 또 다른 one-step 접근방식을 제시합니다.
- 🏛 기반 연구: [[papers/1580_Streaming_Flow_Policy_Simplifying_diffusionflow-matching_pol/review]] — Flow-based 정책의 streaming 구현을 위한 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma/review]] — Consistency Policy의 단일 추론 단계 정책 생성 기법이 FiS의 System 1 고속 실행 설계 기반이 됨
- 🔗 후속 연구: [[papers/1465_ManiFlow_A_General_Robot_Manipulation_Policy_via_Consistency/review]] — consistency policy를 flow matching과 결합하여 더 안정적이고 빠른 visuomotor policy를 구현할 수 있다.
- 🔄 다른 접근: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — 두 논문 모두 diffusion 기반 정책의 추론 속도 개선을 목표로 하지만 distillation과 consistency model로 접근법이 다르다.
- 🔗 후속 연구: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — Consistency Policy의 가속화된 정책 실행 기법이 RTC의 실시간 chunking 성능을 더욱 향상시킬 수 있다.
- 🔄 다른 접근: [[papers/1542_RoboMonkey_Scaling_Test-Time_Sampling_and_Verification_for_V/review]] — Consistency Policy가 확산 모델의 가속화에 중점을 두는 반면, RoboMonkey는 VLA 모델의 테스트 시간 샘플링과 검증을 통한 성능 향상에 초점을 맞춘다.
- 🔄 다른 접근: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — Consistency Policy는 VITA와 같은 효율적인 visuomotor 정책이지만 consistency model을 활용하는 다른 접근법이다.
- 🏛 기반 연구: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — ConRFT의 consistency policy 구성요소가 Consistency Policy 방법론을 기반으로 합니다.
- 🔗 후속 연구: [[papers/1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey/review]] — Consistency Policy는 diffusion model survey에서 다룬 sampling 속도 문제를 consistency model로 해결하는 발전된 접근법입니다.
