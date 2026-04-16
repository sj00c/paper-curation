---
title: "1551_RoboTwin_20_A_Scalable_Data_Generator_and_Benchmark_with_Str"
authors:
  - "Tianxing Chen"
  - "Zanxin Chen"
  - "Baijun Chen"
  - "Zijian Cai"
  - "Yibin Liu"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboTwin 2.0는 MLLM 기반 자동 코드 생성과 시뮬레이션 인루프 피드백을 활용하여 대규모 이원팔 조작 데이터를 생성하는 확장 가능한 프레임워크이며, 구조화된 domain randomization을 통해 sim-to-real 전이를 크게 향상시킨다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/LLM-Based_Reward_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2025_RoboTwin 2.0 A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bi.pdf"
---

# RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation

> **저자**: Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, Yubin Guo, Tian Nian, Xuanbing Xie, Qiangyu Chen, Kailun Su, Tianling Xu, Guodong Liu, Mengkang Hu, Huan-ang Gao, Kaixuan Wang, Zhixuan Liang, Yusen Qin, Xiaokang Yang, Ping Luo, Yao Mu | **날짜**: 2025-06-22 | **URL**: [https://arxiv.org/abs/2506.18088](https://arxiv.org/abs/2506.18088)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of RoboTwin 2.0. RoboTwin 2.0 is a scalable framework for bimanual manipu-*

RoboTwin 2.0는 MLLM 기반 자동 코드 생성과 시뮬레이션 인루프 피드백을 활용하여 대규모 이원팔 조작 데이터를 생성하는 확장 가능한 프레임워크이며, 구조화된 domain randomization을 통해 sim-to-real 전이를 크게 향상시킨다.

## Motivation

- **Known**: 기존 시뮬레이션 기반 데이터 생성은 수동 검증 부재, 단순화된 환경, 체구화된 로봇 간 일반화 부족이라는 세 가지 한계를 가지고 있다.
- **Gap**: 자동 품질 관리 메커니즘, 현실적 domain randomization(clutter, lighting, language 변이), 로봇 체구 특화 affordance 학습이 부재하다.
- **Why**: 이원팔 조작은 복잡한 협력 작업 수행에 필수적이며, 대규모 다양한 데이터 없이는 정책 모델이 환경 변화에 취약하다.
- **Approach**: MLLM 코드 생성 에이전트와 VLM 옵저버로 이루어진 폐루프 피드백 시스템을 구성하고, RoboTwin-OD(731개 객체, 147개 카테고리) 자산 라이브러리 위에서 5축 domain randomization을 적용한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of RoboTwin 2.0. RoboTwin 2.0 is a scalable framework for bimanual manipu-*

- **자동 전문가 데이터 생성**: MLLM과 simulation-in-the-loop 피드백으로 코드 생성 성공률 10.9% 향상 달성
- **대규모 객체 라이브러리**: 731개 객체 인스턴스와 manipulation-relevant 주석 포함한 RoboTwin-OD 구축
- **Sim-to-real 전이 성능**: synthetic 데이터 + 10개 실제 데모로 VLA 모델이 367% 상대 개선, zero-shot 모델 228% 개선 달성
- **포괄적 Domain Randomization**: clutter, lighting, background, tabletop height, language instruction 5축에서 체계적 변이 적용
- **다중 체구 지원**: 50개 이원팔 작업에 5개 로봇 플랫폼 지원 및 100k+ 궤적 데이터셋 공개

## How

![Figure 2](figures/fig2.webp)

*Figure 2: RoboTwin 2.0 Pipeline. Built on RoboTwin-OD and a skill API, the framework uses*

- MLLM 기반 코드 생성 에이전트가 자연어 명령으로부터 작업 프로그램 합성
- VLM 옵저버가 시뮬레이션 실행 모니터링 및 실패 감지, 수정 제안으로 폐루프 피드백 제공
- Skill API 라이브러리와 RoboTwin-OD 활용하여 다양한 객체 카테고리와 조작 시나리오 지원
- Clutter, lighting, background texture, tabletop height, language instruction에 걸친 5축 domain randomization 적용
- 로봇별 kinematic 능력(예: Piper의 저DoF 측면 파지, Franka의 고DoF 정밀 파지) 반영하여 affordance 생성
- VLA 정책 모델을 합성 데이터와 소수 실제 데모(10개)의 조합으로 훈련

## Originality

- MLLM과 VLM 옵저버를 결합한 폐루프 자동 피드백 시스템으로 기존 단방향 코드 생성 개선
- Language instruction을 명시적 domain randomization 축으로 포함하여 기존 visual-only 임의화 확장
- 로봇 체구별 affordance 주석과 action candidate 생성 메커니즘으로 cross-embodiment 일반화 해결
- 731개 객체 147개 카테고리의 대규모 RoboTwin-OD 자산 라이브러리 구축
- 50개 이원팔 작업과 5개 플랫폼에 걸친 포괄적 벤치마크 정의

## Limitation & Further Study

- Domain randomization의 5축이 충분한가: 손 안정성, 물리 시뮬레이션 정확도, 부분 가시성(occlusion) 등 추가 요소 필요 가능
- Zero-shot 성능(228% 개선)은 여전히 절대값으로 낮을 수 있으며, 더 복잡한 실제 환경에서의 검증 필요
- 5개 로봇 플랫폼이 대표성을 가지는가: 유연한 손(dexterous hand) 등 다른 embodiment으로의 확장 미흡
- MLLM 코드 생성의 일반화: 현재 설정 외 새로운 작업 카테고리에 대한 생성 성공률 미검증
- 후속 연구: (1) 부분 관찰, 동적 환경, 접촉 기반 피드백 등 현실성 강화, (2) meta-learning으로 신규 작업 빠른 적응, (3) 대규모 실제 데이터와의 혼합 훈련 전략

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboTwin 2.0는 MLLM 기반 자동 코드 생성, 폐루프 피드백, 다축 domain randomization, 체구 특화 적응을 결합하여 이원팔 조작 연구의 중요한 기반을 제공하며, 367% sim-to-real 개선과 공개 자산/코드로 높은 실용성을 보여준다.

## Related Papers

- 🔗 후속 연구: [[papers/1552_RoboTwin_Dual-Arm_Robot_Benchmark_with_Generative_Digital_Tw/review]] — RoboTwin의 기본 generative digital twin을 MLLM 기반 자동 코드 생성과 확장 가능한 데이터 생성으로 발전시킨 직접적인 후속 연구이다.
- 🏛 기반 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 실제 로봇 학습 방법론이 RoboTwin 2.0의 sim-to-real 전이 최적화에 중요한 실증적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1540_RoboGen_Towards_Unleashing_Infinite_Data_for_Automated_Robot/review]] — 대규모 로봇 데이터 생성에서 RoboTwin 2.0은 시뮬레이션 기반으로, RoboGen은 자동화된 로봇 데이터 생성에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1527_Real2Render2Real_Scaling_Robot_Data_Without_Dynamics_Simulat/review]] — Real2Render2Real의 데이터 확장 개념을 MLLM 기반 자동 생성으로 발전시킨다.
- 🏛 기반 연구: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — MLLM 기반 자동 코드 생성은 GenSim의 대규모 언어 모델을 활용한 시뮬레이션 태스크 생성과 유사한 접근법입니다.
- 🔗 후속 연구: [[papers/1540_RoboGen_Towards_Unleashing_Infinite_Data_for_Automated_Robot/review]] — RoboGen의 자동화 개념을 RoboTwin 2.0이 이원팔 조작과 sim-to-real로 발전시킨다.
- 🏛 기반 연구: [[papers/1552_RoboTwin_Dual-Arm_Robot_Benchmark_with_Generative_Digital_Tw/review]] — RoboTwin의 기본 generative digital twin 개념이 RoboTwin 2.0의 확장 가능한 프레임워크 개발에 직접적인 기반을 제공한다.
