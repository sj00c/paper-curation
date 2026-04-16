---
title: "1685_SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Whole"
authors:
  - "Zhengyi Luo"
  - "Ye Yuan"
  - "Tingwu Wang"
  - "Chenran Li"
  - "Sirui Chen"
date: "2025.12"
doi: "10.48550/arXiv.2511.07820"
arxiv: ""
score: 4.0
essence: "인간의 모션 캡처 데이터를 활용한 motion tracking을 기반 작업으로 삼아 42M 파라미터의 대규모 humanoid controller를 학습하고, kinematic planner와 unified token space를 통해 다양한 제어 인터페이스를 지원하는 자연스러운 전신 움직임 제어 시스템을 제시한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Luo et al._2025_SONIC Supersizing Motion Tracking for Natural Humanoid Whole-Body Control.pdf"
---

# SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control

> **저자**: Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi "Jim" Fan, Yuke Zhu | **날짜**: 2025-12-04 | **DOI**: [10.48550/arXiv.2511.07820](https://doi.org/10.48550/arXiv.2511.07820)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: SONIC enables diverse humanoid tasks through a universal control policy that handles diverse input*

인간의 모션 캡처 데이터를 활용한 motion tracking을 기반 작업으로 삼아 42M 파라미터의 대규모 humanoid controller를 학습하고, kinematic planner와 unified token space를 통해 다양한 제어 인터페이스를 지원하는 자연스러운 전신 움직임 제어 시스템을 제시한다.

## Motivation

- **Known**: 기존 humanoid control은 작은 크기의 신경망으로 제한된 행동만 학습하며 각 작업마다 reward engineering이 필요했고, 대규모 foundation models의 성공에도 불구하고 로봇 제어 분야에서는 유사한 스케일링 이점이 입증되지 않았다.
- **Gap**: Humanoid control에서 수십억 파라미터 규모로 스케일링할 수 있는 자연스럽고 확장 가능한 작업이 부재했으며, 다양한 실제 제어 방식을 통합하면서도 단일 정책으로 작동하는 유연한 시스템이 없었다.
- **Why**: 자연스러운 인간형 로봇의 전신 제어는 산업 응용과 실제 배포에 필수적이며, 대규모 모델 학습의 이점이 입증되면 더욱 강건하고 일반화 가능한 control policy 개발을 가능하게 한다.
- **Approach**: Motion tracking을 scalable한 기초 작업으로 선정하여 100M 프레임의 mocap 데이터로 42M 파라미터 모델을 9k GPU hours로 학습하고, kinematic motion planning과 unified token space를 설계하여 VR teleoperation, human video, VLA 모델 등 다양한 입력을 지원한다.

## Achievement


- **대규모 스케일링의 효과 입증**: 데이터, 모델, 계산량을 각각 확장할 때 성능이 지속적으로 개선되는 favorable scaling properties 확인 (94.5% → 98.5% 성공률)
- **범용 motion tracking 달성**: 100M 프레임 학습으로 unseen motion에 대한 강력한 generalization 성능 달성 (AMASS 테스트셋에서 94.3% 성공률, baselines 대비 우수)
- **Interactive kinematic planning**: Real-time universal kinematic planner로 motion space에서의 goal-directed 제어 구현 (navigation, squatting, kneeling, crawling)
- **멀티모달 통합 제어**: VR teleoperation, human video, music, text, VLA 모델을 unified token space를 통해 단일 정책으로 처리
- **실제 로봇 배포**: Unitree G1 humanoid에서 sim-to-real 성능 검증 및 foundation model 학습 파이프라인 구축

## How


- Motion capture 데이터셋(AMASS 등)에서 100M 프레임의 다양한 인간 운동 수집 및 전처리
- Transformer 기반 architecture로 1.2M → 16M → 42M 파라미터 규모로 점진적 확장
- Dense frame-by-frame supervision으로 reward engineering 없이 직접적인 motion tracking 학습
- Kinematic space에서의 motion generation을 통해 interactive goal-directed control 실현
- Token-based unified interface 설계로 heterogeneous input modalities (VR pose, video, text, VLA embeddings)를 동일한 representation space로 통합
- Retargeting 기법으로 human motion을 humanoid 제어 신호로 직접 변환
- SIM-to-real transfer를 위한 simulator와 실제 로봇 간 domain adaptation

## Originality

- Motion tracking을 humanoid control의 scalable foundation task로 명확히 제시한 것 (기존 prior works는 제한적 downstream tasks만 시연)
- Humanoid 제어에서 처음으로 10M 규모를 초과하는 42M 파라미터 모델 및 100M 프레임 규모의 학습 달성
- Unified token space를 통해 teleoperation, video, music, text, VLA 등 이질적인 제어 입력들을 단일 정책으로 통합 (distillation 없는 단일 단계 학습)
- Interactive kinematic planning으로 motion space에서의 goal-directed 제어와 motion tracking을 연결하는 새로운 방식 제시

## Limitation & Further Study

- Evaluation이 주로 simulation 기반이며 실제 로봇 배포는 Unitree G1에만 한정 (다른 humanoid 형태에 대한 일반화 미검증)
- Real-world teleoperation 성능과 시뮬레이션 간의 성능 격차 분석 부족 (real MPJPE = 40.9 vs sim = 42.7은 보고되지만 원인 분석 제한적)
- Motion tracking 기반 foundation의 한계점에 대한 논의 부재 (e.g., 모션 데이터로 표현 불가능한 제어 문제나 높은 불확실성 환경에서의 성능)
- 후속 연구로 더 광범위한 humanoid 형태와 실제 복잡한 환경에서의 실시간 성능, 다양한 embodiment으로의 cross-modal transfer 개선, 그리고 motion tracking 외 보강 학습 신호와의 hybrid 접근 검토 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 humanoid control에 대규모 스케일링을 성공적으로 적용한 첫 사례로, motion tracking을 foundation task로 선정하고 100M 프레임 데이터와 42M 파라미터로 학습하여 강력한 generalization을 보인다. Kinematic planner와 unified token space를 통해 다양한 제어 인터페이스를 단일 정책으로 통합함으로써 실제 응용 가능성을 입증했으며, 체계적인 ablation과 comprehensive evaluation은 연구의 엄밀성을 보강한다.

## Related Papers

- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 두 논문 모두 모션 추적을 다루지만, 대규모 모델과 일반적인 추적이라는 다른 규모의 접근을 사용한다.
- 🏛 기반 연구: [[papers/1655_Robust_and_Generalized_Humanoid_Motion_Tracking/review]] — 강건하고 일반화된 휴머노이드 모션 추적의 기초적인 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1944_General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast/review]] — 일반적인 휴머노이드 전신 제어를 대규모 motion tracking으로 확장하여 더 자연스러운 움직임을 실현한다.
- 🔄 다른 접근: [[papers/1667_SCDP_Learning_Humanoid_Locomotion_from_Partial_Observations/review]] — 대규모 모션 트래킹과 센서 조건부 확산 정책이라는 서로 다른 접근법으로 휴머노이드 전신 제어를 다룬다.
- 🔗 후속 연구: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — 대규모 휴머노이드 제어에서 모션 트래킹과 텍스트 기반 모션 생성이라는 보완적 인터페이스를 제공한다.
- 🔄 다른 접근: [[papers/1744_Unleashing_Humanoid_Reaching_Potential_via_Real-world-Ready/review]] — 대규모 휴머노이드 제어를 위해 서로 다른 접근(42M 파라미터 통합 모델 vs 사전 학습된 원시 스킬 조합)으로 확장성과 일반화를 추구한다.
- 🏛 기반 연구: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — 모션 트래킹 기반 전신 제어의 기본 개념을 대규모 모델과 통합된 토큰 공간으로 확장하여 자연스러운 움직임을 실현했다.
- 🔗 후속 연구: [[papers/1814_Being-H0_Vision-Language-Action_Pretraining_from_Large-Scale/review]] — 비전-언어-액션 사전 학습의 개념을 모션 캡처 데이터와 결합하여 42M 파라미터 규모의 휴머노이드 제어기로 확장했다.
- 🔄 다른 접근: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 자연스러운 전신 움직임 제어를 위해 서로 다른 인터페이스(unified token space vs streaming 자연어)를 통해 사용자 명령을 처리한다.
- 🔄 다른 접근: [[papers/1667_SCDP_Learning_Humanoid_Locomotion_from_Partial_Observations/review]] — 부분 관찰 조건에서의 휴머노이드 제어를 다루며, SCDP는 센서 기반 확산 정책을, SONIC은 대규모 모션 트래킹을 통해 접근한다.
- 🏛 기반 연구: [[papers/1655_Robust_and_Generalized_Humanoid_Motion_Tracking/review]] — SONIC의 대규모 motion tracking 접근법이 본 논문의 강건한 모션 추적 프레임워크의 기반이 된다.
- 🔄 다른 접근: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 자연스러운 전신 움직임 제어를 위해 서로 다른 인터페이스(streaming 자연어 vs unified token space)를 통해 사용자 명령을 처리한다.
- 🔄 다른 접근: [[papers/1745_Unveiling_the_Impact_of_Data_and_Model_Scaling_on_High-Level/review]] — 대규모 모션 데이터 활용에서 텍스트 기반 생성과 모션 트래킹이라는 서로 다른 제어 인터페이스를 제공한다.
- 🔄 다른 접근: [[papers/1744_Unleashing_Humanoid_Reaching_Potential_via_Real-world-Ready/review]] — 대규모 휴머노이드 제어를 위해 서로 다른 접근(사전 학습된 원시 스킬 조합 vs 42M 파라미터 통합 모델)으로 확장성과 일반화를 추구한다.
