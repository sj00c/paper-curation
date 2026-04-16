---
title: "1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro"
authors:
  - "Yuheng Ji"
  - "Huajie Tan"
  - "Jiayu Shi"
  - "Xiaoshuai Hao"
  - "Yuan Zhang"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboBrain은 로봇 조작을 위해 Planning Capability, Affordance Perception, Trajectory Prediction의 세 가지 핵심 능력을 갖춘 통합 MLLM 모델이며, 이를 학습하기 위해 ShareRobot이라는 대규모 고품질 이질 데이터셋을 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ji et al._2025_RoboBrain A Unified Brain Model for Robotic Manipulation from Abstract to Concrete.pdf"
---

# RoboBrain: A Unified Brain Model for Robotic Manipulation from Abstract to Concrete

> **저자**: Yuheng Ji, Huajie Tan, Jiayu Shi, Xiaoshuai Hao, Yuan Zhang, Hengyuan Zhang, Pengwei Wang, Mengdi Zhao, Yao Mu, Pengju An, Xinda Xue, Qinghang Su, Huaihai Lyu, Xiaolong Zheng, Jiaming Liu, Zhongyuan Wang, Shanghang Zhang | **날짜**: 2025-02-28 | **URL**: [https://arxiv.org/abs/2502.21257](https://arxiv.org/abs/2502.21257)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of RoboBrain. RoboBrain consists of three key robotic capabilities: planning capability, affordance p*

RoboBrain은 로봇 조작을 위해 Planning Capability, Affordance Perception, Trajectory Prediction의 세 가지 핵심 능력을 갖춘 통합 MLLM 모델이며, 이를 학습하기 위해 ShareRobot이라는 대규모 고품질 이질 데이터셋을 제시한다.

## Motivation

- **Known**: MLLM은 시각 인식과 언어 이해에서 우수한 성능을 보이고 있으나, 로봇 장기 조작 작업에 적용할 때는 태스크 분해, 객체 affordance 인식, 궤적 예측 능력이 부족하다.
- **Gap**: 기존 MLLM은 추상적 지시를 구체적 로봇 행동으로 변환하는 세 가지 핵심 능력이 결여되어 있으며, 이를 위한 대규모 세밀한 로봇 조작 전용 데이터셋이 부족하다.
- **Why**: 로봇 조작의 성공률 향상과 장기 작업 수행을 위해서는 추상적 지시를 관리 가능한 부분 작업으로 분해하고, 각 단계에서 정확한 affordance와 궤적을 예측하는 능력이 필수적이다.
- **Approach**: ShareRobot 데이터셋을 구축하여 task planning, object affordance, end-effector trajectory에 대한 다차원 정보를 라벨링하고, 이를 바탕으로 LLaVA 기반 MLLM인 RoboBrain을 다단계 학습 전략과 장시간 비디오, 고해상도 이미지를 활용하여 개발한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5. The performance of our model RoboBrain on the OpenEQA, ShareRobot, and RoboVQA benchmarks. RoboBrain surpassed*

- **ShareRobot 데이셋 개발**: 로봇 조작 작업을 위해 task planning, affordance, trajectory를 포함하는 다차원 정보가 세밀하게 라벨링된 대규모 이질 데이터셋 제시
- **RoboBrain 모델**: Planning, Affordance Perception, Trajectory Prediction 세 가지 핵심 능력을 통합한 통일된 MLLM 개발
- **다단계 학습 전략**: 로봇 데이터와 일반 멀티모달 데이터의 비율 최적화 및 장시간 비디오와 고해상도 이미지 활용
- **성능 개선**: RoboVQA, OpenEQA 등 여러 로봇 벤치마크에서 최첨단 성능 달성 및 affordance, trajectory 예측에서도 경쟁력 있는 결과 제시

## How

![Figure 2](figures/fig2.webp)

*Figure 2. The generation procession of our ShareRobot dataset. Our dataset labels multi-dimensional information, includi*

- ShareRobot 데이터셋: Open X-Embodiment에서 고품질 데이터 추출 후 원자적 작업으로 분해하고 질문-응답 쌍으로 증강
- 데이터 라벨링: 세 명의 인간 주석자가 task planning (세부 단계별 분해), affordance (상호작용 가능 영역 좌표), trajectory (말단 장치 경로점) 라벨링
- 모델 아키텍처: LLaVA 기반으로 historical frame memory와 고해상도 이미지 입력 지원
- 다단계 학습: 로봇 데이터와 일반 멀티모달 데이터의 최적 비율로 순차적 학습
- 장시간 비디오 처리: 연속적 프레임 정보를 활용하여 동적 조작 이해 강화

## Originality

- 로봇 조작을 위한 세 가지 핵심 능력(planning, affordance, trajectory)을 명확히 정의하고 이를 모두 포함하는 통합 MLLM 설계
- 기존 일반 멀티모달 데이터와 로봇 전용 데이터를 조합하는 다단계 학습 전략으로 일반화 능력과 로봇 특화 능력 동시 확보
- 추상 지시에서 구체적 실행으로의 변환 과정을 체계적으로 데이터셋에 반영한 새로운 접근

## Limitation & Further Study

- 실제 로봇 플랫폼에서의 성능 검증이 주로 시뮬레이션 기반이므로 현실 세계 전이 가능성 불명확
- 세 명의 인간 주석자로 라벨링하여 주관성과 인간 실수 가능성 존재
- ShareRobot의 규모와 다양성에 대한 상세한 통계 분석 및 비교 부족
- 후속연구: (1) 실제 로봇 팔을 이용한 현실 세계 평가, (2) 더 다양한 로봇 embodiment와 환경 포함, (3) affordance와 trajectory 라벨링 자동화 방법 개발, (4) 모델의 실패 케이스 분석 및 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboBrain은 로봇 조작을 위한 세 가지 핵심 능력을 체계적으로 정의하고 이를 통합한 MLLM과 고품질 데이터셋을 함께 제시하여, 로봇 AI의 구체적 실행 능력 향상에 의미 있는 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1379_Embodied-R_Collaborative_Framework_for_Activating_Embodied_S/review]] — Embodied-R과 동일하게 통합된 embodied reasoning을 추구하지만 RoboBrain은 조작에 특화되고 ShareRobot 데이터셋을 활용한다.
- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — BridgeData V2의 대규모 로봇 데이터셋 구축 경험이 RoboBrain의 ShareRobot 데이터셋 개발에 중요한 기반이 된다.
- 🔗 후속 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 로봇 제어 능력을 Planning, Affordance, Trajectory 예측의 통합 MLLM 모델로 확장하여 더 포괄적인 조작 시스템을 구축한다.
- 🔄 다른 접근: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — 로봇의 지능적 의사결정을 RoboBrain은 통합 MLLM으로, RationalVLA는 dual system으로 구현하는 서로 다른 접근법이다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 embodied multimodal language model 아키텍처가 RoboBrain의 통합 MLLM 설계에 핵심적인 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — RoboBrain의 통합 MLLM은 RoboCerebra의 장기간 조작 작업에서 계층적 계획-실행을 더 효과적으로 수행할 수 있습니다.
- 🏛 기반 연구: [[papers/1541_RoboMIND_Benchmark_on_Multi-embodiment_Intelligence_Normativ/review]] — ShareRobot 대규모 데이터셋은 RoboMIND와 같은 다중 embodiment 데이터 수집 표준에 중요한 참조점을 제공합니다.
- 🔄 다른 접근: [[papers/1492_Neural_Brain_A_Neuroscience-inspired_Framework_for_Embodied/review]] — 둘 다 통합된 뇌 모델 접근법이지만, Neural Brain은 신경과학 기반을, RoboBrain은 로봇 매니퓰레이션 통합에 초점을 둔다.
- 🔄 다른 접근: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — 로봇이 실행 불가능한 지시를 처리하는 rational 능력을 다룬 두 논문으로, 하나는 dual system으로 다른 하나는 unified MLLM으로 접근한다.
- 🔄 다른 접근: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — 로봇의 의류 조작에서 SKT는 state-aware keypoint trajectory로, RoboBrain은 통합 MLLM으로 서로 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — RoboCerebra의 장기간 조작 평가는 RoboBrain과 같은 통합 뇌 모델의 실제 성능을 검증하는 벤치마크 역할을 합니다.
- 🔗 후속 연구: [[papers/1541_RoboMIND_Benchmark_on_Multi-embodiment_Intelligence_Normativ/review]] — 다중 embodiment 데이터는 RoboBrain과 같은 통합 뇌 모델이 다양한 로봇 플랫폼에서 일반화될 수 있게 합니다.
- 🔄 다른 접근: [[papers/1610_Visual_Embodied_Brain_Let_Multimodal_Large_Language_Models_S/review]] — 둘 다 로봇 조작을 위한 통합된 brain model을 제시하지만 RoboBrain은 별도의 brain model에, VeBrain은 MLLM 통합에 집중합니다.
