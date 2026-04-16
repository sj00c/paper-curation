---
title: "1643_RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with"
authors:
  - "Junpeng Yue"
  - "Zepeng Wang"
  - "Yuxuan Wang"
  - "Weishuai Zeng"
  - "Jiangxing Wang"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 텍스트 기반 인간 동작을 실제 휴머노이드 로봇에 실행 가능한 형태로 변환하는 문제를 해결하기 위해, 물리 시뮬레이터에서의 피드백을 기반으로 대규모 모션 생성 모델을 강화학습으로 미세조정하는 RLPF 프레임워크를 제안한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yue et al._2025_RL from Physical Feedback Aligning Large Motion Models with Humanoid Control.pdf"
---

# RL from Physical Feedback: Aligning Large Motion Models with Humanoid Control

> **저자**: Junpeng Yue, Zepeng Wang, Yuxuan Wang, Weishuai Zeng, Jiangxing Wang, Xinrun Xu, Yu Zhang, Sipeng Zheng, Ziluo Ding, Zongqing Lu | **날짜**: 2025-06-15 | **URL**: [https://arxiv.org/abs/2506.12769](https://arxiv.org/abs/2506.12769)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of RLPF, which consists of three key components: i) Motion Tracking Policy*

본 논문은 텍스트 기반 인간 동작을 실제 휴머노이드 로봇에 실행 가능한 형태로 변환하는 문제를 해결하기 위해, 물리 시뮬레이터에서의 피드백을 기반으로 대규모 모션 생성 모델을 강화학습으로 미세조정하는 RLPF 프레임워크를 제안한다.

## Motivation

- **Known**: 기존 text-to-motion 생성 모델들은 텍스트-동작 의미 정렬에는 성공했으나, 대부분 컴퓨터 그래픽스 분야에서 비롯되어 시각적 품질을 우선시하며 물리적 실현가능성을 간과한다.
- **Gap**: 생성된 동작이 발 슬라이딩, 지면 관통, 동적 불안정성 등 물리 법칙 위반으로 인해 실제 로봇 배포에 실패하며, 인간과 휴머노이드 로봇의 형태 차이로 인한 모션 변환 문제가 해결되지 않았다.
- **Why**: 휴머노이드 로봇 기술의 발전으로 다양한 동작을 수행할 수 있게 되었으나, 각 동작마다 노동집약적인 파라미터 튜닝이 필요하므로, 텍스트 명령으로부터 물리적으로 실현가능한 동작을 자동 생성할 수 있다면 로봇 학습의 확장성과 효율성을 크게 향상시킬 수 있다.
- **Approach**: Motion Tracking Policy를 통해 물리 시뮬레이터에서 생성된 동작의 실현가능성을 평가하고 보상 신호를 생성하며, Alignment Verification Module로 텍스트와의 의미적 일치를 검증하고, 두 신호를 결합하여 PPO 기반 RL로 대규모 모션 모델을 미세조정한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Visualizations of RLPF-w/o align. Since training relies solely on the motion tracking*

- **물리적 실현가능성 달성**: RLPF는 기존 baseline 대비 물리적으로 실현 가능한 동작 생성에서 현저히 우수한 성능을 보이며, 실제 Unitree G1 휴머노이드 로봇에 성공적으로 배포되었다.
- **의미 충실도 보존**: 제안된 Alignment Verification Module이 텍스트 지시와의 의미적 대응을 정량적으로 평가하여, 물리적 최적화 과정에서도 높은 의미 정렬도를 유지한다.
- **통합 최적화 프레임워크**: Motion Tracking Policy의 피드백과 Alignment Verification의 신호를 jointly 최적화하여 물리적 실현가능성과 의미적 정확성 간의 균형을 달성한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of RLPF, which consists of three key components: i) Motion Tracking Policy*

- 대규모 모션 모델(예: MotionGPT)을 기반으로 하여 텍스트 입력으로부터 초기 동작 시퀀스를 생성한다.
- Motion Retargeting을 통해 인간 동작을 로봇의 운동학적 제약 조건에 맞게 변환한다.
- IsaacGym 물리 시뮬레이터에서 Motion Tracking Policy를 이용하여 생성된 동작의 추적 성능을 평가하고 physical feasibility reward를 계산한다.
- CLIP 또는 텍스트 인코더를 활용한 Alignment Verification Module이 생성된 동작과 원본 텍스트 지시 간의 의미적 거리를 측정한다.
- 두 보상 신호(physical + semantic)를 결합하여 PPO 알고리즘으로 대규모 모션 모델의 파라미터를 미세조정한다.
- PD 컨트롤러를 통해 시뮬레이션 결과를 실제 로봇에 적용하고 실행 가능성을 검증한다.

## Originality

- **물리 피드백 기반 RL 미세조정**: RLHF와 유사하게 물리 시뮬레이터에서의 실제 피드백을 보상으로 사용하여 생성 모델을 최적화하는 접근은 text-to-motion 분야에서 처음 시도된 것으로 보인다.
- **Dual-objective 최적화**: 물리적 실현가능성과 의미적 충실도를 동시에 보장하는 unified 프레임워크로 sim-to-real gap을 체계적으로 해결한다.
- **Motion Tracking Policy의 새로운 활용**: Exbody2를 기반으로 한 Motion Tracking Policy를 단순 실행 도구가 아닌 보상 신호 생성 메커니즘으로 혁신적으로 활용한다.

## Limitation & Further Study

- **계산 복잡성**: 매 RL 반복 단계마다 물리 시뮬레이션과 동작 추적을 수행해야 하므로 학습 시간이 길 수 있으며, 확장성 분석이 부족하다.
- **Alignment Verification Module의 의존성**: 텍스트-동작 의미 정렬을 위해 사전학습된 인코더(CLIP 등)에 의존하므로, 특정 도메인이나 언어에 대한 일반화 성능이 제한될 수 있다.
- **형태적응의 제한성**: 제안된 Motion Retargeting이 다양한 휴머노이드 로봇 플랫폼(상이한 DoF, 체형 등)에 적응하는 능력에 대한 평가가 불충분하다.
- **평가 지표의 한계**: 물리적 실현가능성을 주로 motion tracking success rate로 측정하는데, 에너지 효율성이나 안정성 마진 등 다른 중요한 측면이 충분히 다루어지지 않았다.
- **후속 연구 방향**: (1) 더 효율적인 보상 계산 메커니즘 개발, (2) 다양한 로봇 플랫폼에 대한 광범위한 평가, (3) 실시간 텍스트 피드백을 기반으로 한 온라인 학습 확장, (4) 물리적 안정성 마진을 명시적으로 고려하는 보상 설계.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 text-to-motion 생성 모델과 로봇 제어 간의 오랜 간극을 물리적 피드백 기반 RL로 체계적으로 해결하는 창의적 접근을 제시하며, 실제 로봇 배포 성공을 통해 실용적 가치를 입증했다. 다만 계산 효율성과 평가 범위 확대에 대한 추가 연구가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — RLPF의 물리 피드백 기반 모션 모델 조정과 SENTINEL의 end-to-end 언어-행동 모델은 상호 보완적 접근법
- 🏛 기반 연구: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — CLoSD의 diffusion-시뮬레이션 폐쇄루프가 RLPF의 물리 피드백 기반 모델 정제 방법론의 직접적 기반
- 🔗 후속 연구: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — Humanoid-LLA의 자유형식 언어 명령 처리가 RLPF의 텍스트-모션 변환을 실용적 자연언어로 확장
- 🏛 기반 연구: [[papers/1666_Scaling_Large_Motion_Models_with_Million-Level_Human_Motions/review]] — Scaling Large Motion Models의 대규모 인간 모션 데이터 활용 기법이 RLPF의 텍스트 기반 모션 모델 학습의 기초가 됨
- 🔗 후속 연구: [[papers/1952_GENMO_A_GENeralist_Model_for_Human_MOtion/review]] — GENMO의 범용 모션 모델이 RLPF의 대규모 모션 생성 모델을 휴머노이드 실행가능성으로 확장하는 프레임워크임
- 🧪 응용 사례: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — From Language to Locomotion의 retargeting-free 제어가 RLPF의 텍스트-모션 변환을 실제 휴머노이드 제어에 적용한 사례임
- 🏛 기반 연구: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — Large-scale pretraining의 효과를 motion model alignment에 적용한 기반 연구
- 🔄 다른 접근: [[papers/1996_Humanoid_Locomotion_as_Next_Token_Prediction/review]] — Physical feedback 대신 next token prediction으로 motion generation을 해결
- 🏛 기반 연구: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — RLPF의 강화학습 기반 모션 모델 정제가 SENTINEL의 잔여 강화학습 정제 방법론의 직접적 기반
- 🏛 기반 연구: [[papers/1836_CHIP_Adaptive_Compliance_for_Humanoid_Control_through_Hindsi/review]] — 물리적 피드백 기반 강화학습이 CHIP의 hindsight perturbation에서 적응적 컴플라이언스 학습을 위한 이론적 기반을 제공한다
- 🔗 후속 연구: [[papers/1841_CLoSD_Closing_the_Loop_between_Simulation_and_Diffusion_for/review]] — RLPF의 물리 피드백 기반 모션 모델 정제를 CLoSD의 diffusion-시뮬레이션 폐쇄루프로 확장한 형태
- 🔗 후속 연구: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — RLPF의 텍스트-모션 변환을 Humanoid-LLA의 자유형식 자연언어 처리로 확장한 고도화된 형태
- 🔗 후속 연구: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — 물리적 피드백을 통한 대형 모션 모델 정렬로 발전됩니다.
- 🏛 기반 연구: [[papers/2033_Keep_on_Going_Learning_Robust_Humanoid_Motion_Skills_via_Sel/review]] — 물리 피드백을 통한 강화학습이 Keep on Going의 적대적 공격 기반 정책 강화에 실제 환경 기반 검증 제공
- 🏛 기반 연구: [[papers/2059_Learning_Motion_Skills_with_Adaptive_Assistive_Curriculum_Fo/review]] — 물리적 피드백을 통한 강화학습이 적응형 보조력을 활용한 동작 학습에 이론적 기반을 제공한다.
