---
title: "1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level"
authors:
  - "Enyu Zhao"
  - "Vedant Raval"
  - "Hejia Zhang"
  - "Jiageng Mao"
  - "Zeyu Shangguan"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "ManipBench는 Vision-Language Model(VLM)의 저수준 로봇 조작 추론 능력을 평가하기 위한 12,617개의 객관식 문제로 구성된 벤치마크이며, 33개의 VLM을 10개 모델 계열에서 광범위하게 테스트하여 성능 차이를 분석한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_AI_Architectures"
  - "sub/Vision-Language_Object_Manipulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2025_ManipBench Benchmarking Vision-Language Models for Low-Level Robot Manipulation.pdf"
---

# ManipBench: Benchmarking Vision-Language Models for Low-Level Robot Manipulation

> **저자**: Enyu Zhao, Vedant Raval, Hejia Zhang, Jiageng Mao, Zeyu Shangguan, Stefanos Nikolaidis, Yue Wang, Daniel Seita | **날짜**: 2025-05-14 | **URL**: [https://arxiv.org/abs/2505.09698](https://arxiv.org/abs/2505.09698)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: ManipBench is a novel benchmark with over 12,000 multiple-choice questions across three different*

ManipBench는 Vision-Language Model(VLM)의 저수준 로봇 조작 추론 능력을 평가하기 위한 12,617개의 객관식 문제로 구성된 벤치마크이며, 33개의 VLM을 10개 모델 계열에서 광범위하게 테스트하여 성능 차이를 분석한다.

## Motivation

- **Known**: VLM은 고수준 로봇 계획에 사용되어 왔으나, 정확한 로봇 움직임 결정과 같은 저수준 추론 능력은 덜 연구되었다. 로봇 조작을 위한 다양한 벤치마크가 존재하지만 VLM의 저수준 추론 능력을 체계적으로 평가하는 표준화된 벤치마크가 부족하다.
- **Gap**: 기존 VLM 로봇 벤치마크들은 낮은 모델 다양성, 제한된 작업 범위, 혹은 부적절한 평가 메트릭(MSE 등)을 가지고 있으며, 특히 deformable object 조작과 저수준 물리 추론 능력 평가에 초점을 맞춘 포괄적 벤치마크가 없다.
- **Why**: VLM을 로봇 에이전트로 사용할 때 저수준 추론 능력은 실제 조작 성공에 직접 영향을 미치므로, 어떤 VLM이 로봇 제어에 최적인지 파악하고 모델 개선의 방향을 제시하기 위해 체계적인 평가가 필수적이다.
- **Approach**: 실제 로봇 데이터, 수동 큐레이션 fabric 조작 데이터, 시뮬레이션 데이터로부터 mark-based visual prompting을 통해 MCQ 기반 벤치마크를 구성하고, 키포인트 예측 중심의 평가 설계로 효율적인 저수준 추론 능력 평가를 수행한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: The percentage accuracies of the VLMs for evaluating the dimensions of Fabric Manipulation, de-*

- **ManipBench 벤치마크 개발**: pick-and-place, articulated object manipulation, deformable object manipulation, dynamic manipulation 등 다양한 작업을 포함한 12,617개의 MCQ 기반 평가 세트 구성
- **광범위한 VLM 평가**: 33개 VLM을 10개 모델 계열에서 평가하여 모델 간 성능 차이 및 크기별 변화 분석
- **현실과의 연관성 검증**: 벤치마크 성능과 실제 로봇 조작 작업에서의 성공률 간 강한 상관관계 입증
- **성능 갭 분석**: 최고 성능 모델(Gemini-2.5-pro)도 인간 수준 이해와 큰 격차가 있음을 시연

## How

![Figure 2](figures/fig2.webp)

*Figure 2: ManipBench uses real and simulated environments, typically pre-processed with a MOKA-style [6]*

- 실제 로봇 데이터로부터 DROID, Bridge 등 Open-X 데이터셋 활용
- Fabric manipulation을 위한 수동 큐레이션 질문 생성
- 시뮬레이션 환경(ManiSkill 등)에서 생성된 데이터 활용
- Mark-based visual prompting으로 객관식 문제 생성 (gripper mask 주석 활용)
- Keypoint 예측 중심의 평가로 저수준 조작 추론 능력 측정
- MCQ 기반 설계로 trajectory rollout 없이 효율적 평가 수행
- 실제 로봇 실험을 통해 벤치마크 성능과 현실 성능 간 상관관계 분석

## Originality

- MCQ 기반 평가 설계로 기존 MSE 기반 평가의 multimodality 문제 해결
- 실제 로봇 데이터와 시뮬레이션 데이터를 통합하여 포괄적 벤치마크 구성
- Deformable object manipulation에 특화된 대규모 벤치마크 (기존 벤치마크의 주요 한계 극복)
- 저수준 물리 추론(low-level physical reasoning)에 직접 초점을 맞춘 첫 종합 벤치마크
- 모델-성능 간 real-world 검증을 포함하여 벤치마크 신뢰성 입증

## Limitation & Further Study

- 현재 2개 closed-source, 8개 open-source 모델 계열만 포함되어 향후 더 다양한 VLM 추가 필요
- MCQ 형식의 한계로 연속적 trajectory 예측이 필요한 복잡한 조작 작업 평가 미흡
- 실제 로봇 검증 실험이 제한적이므로 더 다양한 실제 조작 작업에서의 상관관계 분석 필요
- Sim-to-real gap이 여전히 존재하므로 시뮬레이션 기반 데이터의 현실 대표성 한계
- Fine-tuning 등 모델 개선 방법론에 대한 체계적 가이드라인 부재
- 특정 도메인(fabric, articulated object)에 대한 세부 성능 분석 심화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ManipBench는 VLM의 저수준 로봇 조작 추론 능력을 체계적으로 평가하는 첫 종합 벤치마크로서, 광범위한 모델 평가, 포괄적 작업 범위, 현실 검증을 통해 로봇 조작 분야에 중요한 기여를 한다. 다만 평가 형식의 한계와 실제 로봇 검증의 확장 필요성이 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — VLABench와 함께 VLM의 로봇 조작 능력 평가에 집중하지만 ManipBench는 저수준 추론에 특화된 벤치마크를 제공한다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA 같은 기존 VLM들의 조작 추론 한계를 체계적으로 분석하여 향후 VLA 모델 개발의 기초 지식을 제공한다.
- 🔄 다른 접근: [[papers/1314_AutoEval_Autonomous_Evaluation_of_Generalist_Robot_Manipulat/review]] — 둘 다 로봇 조작 능력 평가에 초점을 맞추지만, ManipBench는 VLM의 추론 능력을, AutoEval은 일반화된 로봇 평가에 집중한다.
- 🔗 후속 연구: [[papers/1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde/review]] — ManipBench의 저수준 조작 추론 평가가 ManipVQA의 물리적 근거가 있는 어포던스 이해와 결합되어 포괄적 조작 능력 평가를 제공한다.
- 🏛 기반 연구: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — PaLI-X의 멀티링구얼 비전-언어 모델이 ManipBench의 VLM 저수준 조작 추론 평가 기반이 됨
- 🔄 다른 접근: [[papers/1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde/review]] — 로봇 조작을 위한 VLM 평가에서 affordance 주입 vs 벤치마킹의 다른 관점
- 🔗 후속 연구: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — ManipBench의 vision-language 모델 평가 접근법을 VLA 모델로 확장하여 더 포괄적인 능력 평가가 가능하다
