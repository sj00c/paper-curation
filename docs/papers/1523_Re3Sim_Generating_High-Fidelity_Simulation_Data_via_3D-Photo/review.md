---
title: "1523_Re3Sim_Generating_High-Fidelity_Simulation_Data_via_3D-Photo"
authors:
  - "Xiaoshen Han"
  - "Minghuan Liu"
  - "Yilun Chen"
  - "Junqiu Yu"
  - "Xiaoyang Lyu"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "RE3SIM은 3D 재구성과 신경 렌더링 기술을 활용하여 실제 환경을 고충실도로 복제한 후, 물리 기반 시뮬레이터 내에서 로봇 조작 정책을 학습하는 real-to-sim-to-real 파이프라인이다. 순수 시뮬레이션 데이터만으로 평균 58% 이상의 성공률로 zero-shot sim-to-real 전이를 달성한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_AI_Architectures"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Han et al._2025_Re$^3$Sim Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Ma.pdf"
---

# Re$^3$Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation

> **저자**: Xiaoshen Han, Minghuan Liu, Yilun Chen, Junqiu Yu, Xiaoyang Lyu, Yang Tian, Bolun Wang, Weinan Zhang, Jiangmiao Pang | **날짜**: 2025-02-12 | **URL**: [https://arxiv.org/abs/2502.08645](https://arxiv.org/abs/2502.08645)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Illustration of RE3SIM. a) RE3SIM allows zero-shot policy transfer on various tasks. b) The system pipeline to*

RE3SIM은 3D 재구성과 신경 렌더링 기술을 활용하여 실제 환경을 고충실도로 복제한 후, 물리 기반 시뮬레이터 내에서 로봇 조작 정책을 학습하는 real-to-sim-to-real 파이프라인이다. 순수 시뮬레이션 데이터만으로 평균 58% 이상의 성공률로 zero-shot sim-to-real 전이를 달성한다.

## Motivation

- **Known**: 로봇 학습을 위한 실제 데이터 수집은 비용이 많이 들고, 시뮬레이션은 확장성이 있지만 기하학적 및 시각적 sim-to-real 갭으로 인해 일반화에 실패한다.
- **Gap**: 기존 시뮬레이션은 CAD 모델의 기하학적 부정확성과 저품질 렌더링으로 인해 실세계와의 큰 갭을 가지고 있으며, 배경 재구성의 품질 저하 문제를 효과적으로 해결하지 못했다.
- **Why**: 로봇 정책 학습의 데이터 수집 비용을 획기적으로 줄일 수 있으며, 고충실도 시뮬레이션 데이터 생성을 통해 확장 가능한 로봇 학습 체계를 구축할 수 있기 때문이다.
- **Approach**: multi-view stereo(MVS)를 사용한 메시 재구성과 3D Gaussian splatting(3DGS)을 통한 배경 렌더링, 그리고 메시 기반 객체 렌더링을 결합하여 하이브리드 시각 렌더링을 구현한다. ArUco 마커를 사용하여 실세계 좌표와 시뮬레이션 공간을 정렬하고, 특권 정보(privileged information)를 활용하여 시뮬레이션에서 전문가 시연 데이터를 효율적으로 수집한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Visual comparison between real and simulation. Rendering results from our hybrid rendering method compared*

- **고충실도 재구성 및 시각화**: MVS 기반 메시 재구성과 3DGS 렌더링으로 기하학적 및 시각적 sim-to-real 갭을 크게 감소
- **빠른 장면 재구성**: 3분 이내의 수동 설정으로 새로운 장면 재구성 가능
- **효율적 렌더링**: 480p 해상도에서 2개 독립 카메라 뷰에 대해 24 FPS 렌더링 성능
- **Zero-shot sim-to-real 전이**: 약 10분의 시뮬레이션 데이터 수집으로 평균 58% 이상의 성공률 달성
- **대규모 확장성**: 대규모 시뮬레이션 데이터셋 생성으로 다양한 객체에 일반화되는 강건한 정책 구축

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Illustration of the proposed real-to-sim-to-real system, RE3SIM. It leverages 3D reconstruction and a physics-*

- **메시 재복구**: 구조-동작(structure-from-motion) 접근 방식(COLMAP)을 사용하여 카메라 자세 및 희소 포인트 클라우드 추정
- **MVS 기반 재구성**: 다중 시점 입체 기술으로 배경 메시 재구성
- **3D Gaussian Splatting**: 각 Gaussian을 회전 R과 스케일링 S로부터 공분산 행렬 Σ = RSS^T R^T 계산하여 고충실도 배경 렌더링
- **하이브리드 렌더링**: 배경은 3DGS로, 객체는 메시 기반 텍스처 매핑으로 렌더링
- **실세계 정렬**: ArUco 마커를 통해 실제 환경과 시뮬레이션 공간의 좌표 동기화
- **물리 시뮬레이션**: Isaac Sim, PyBullet, Mujoco 등 물리 엔진을 사용한 동적 시뮬레이션
- **정책 학습**: 특권 정보를 활용한 시뮬레이션 내 전문가 시연으로 모방 학습(imitation learning) 수행

## Originality

- **하이브리드 렌더링 전략**: 배경에는 3DGS, 객체에는 메시 기반 렌더링을 분리하여 적용하여 배경 재구성 품질 문제 해결
- **최소 인간 개입**: ArUco 마커 배치와 사진/비디오 촬영만으로 scene reconstruction 자동화
- **실시간 고충실도 렌더링**: 24 FPS의 높은 렌더링 성능으로 대규모 데이터 생성 가능
- **End-to-end real-to-sim-to-real 파이프라인**: 단계적 프로세스로 명확하고 재현 가능한 시스템 설계

## Limitation & Further Study

- **경직된 물체 태스크 제한**: 변형 가능한 객체(deformable objects)나 유체에 대한 검증 부족
- **탁상 조작 환경 제약**: 테이블탑 로봇 팔에 대해서만 검증되었으며, 이동형 로봇(mobile manipulator) 등으로의 확장 미검토
- **배경 재구성 정확도**: MVS 방식의 배경 메시 재구성이 복잡한 기하학적 구조에서 불완전할 수 있음
- **객체 세분화 요구**: 현재 시스템에서 전경 객체 분할이 필요하며 이 과정에서 일부 인간 개입 필요
- **후속 연구 방향**: (1) 변형 가능 객체 및 입자 기반 시뮬레이션 확장, (2) 모바일 매니퓰레이터 플랫폼 적용, (3) 자동 객체 세분화 기술 개발, (4) 더 복잡한 동역학(접촉, 마찰 등) 모델링

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RE3SIM은 3D 재구성과 신경 렌더링을 효과적으로 결합하여 sim-to-real 갭을 크게 줄이는 실용적인 시스템으로, 최소한의 인간 개입으로 대규모 고품질 시뮬레이션 데이터를 생성할 수 있는 점에서 로봇 학습 분야에 중요한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1297_A_Real-to-Sim-to-Real_Approach_to_Robotic_Manipulation_with/review]] — Re3Sim의 3D-photorealistic 접근법과 기존 real-to-sim-to-real 방법들은 시뮬레이션 충실도 향상의 다른 전략을 제시한다.
- 🏛 기반 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — Video foundation models를 활용한 world simulation 기술이 Re3Sim의 고충실도 시뮬레이션 환경 구축의 핵심 기반 기술이다.
- 🔗 후속 연구: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — GenSim의 자동 시뮬레이션 태스크 생성이 Re3Sim의 고충실도 환경을 활용한 더 다양한 학습 시나리오 구성으로 확장된다.
- 🔄 다른 접근: [[papers/1527_Real2Render2Real_Scaling_Robot_Data_Without_Dynamics_Simulat/review]] — Re3Sim과 R2R2R 모두 real-to-sim 데이터 생성을 다루지만 3D 재구성과 렌더링이라는 다른 핵심 기술을 사용합니다.
- 🔗 후속 연구: [[papers/1552_RoboTwin_Dual-Arm_Robot_Benchmark_with_Generative_Digital_Tw/review]] — 고충실도 시뮬레이션 데이터 생성은 RoboTwin의 generative digital twin과 결합하여 더 현실적인 로봇 훈련 환경을 구축할 수 있습니다.
- 🏛 기반 연구: [[papers/1360_Diffusion_Models_Are_Real-Time_Game_Engines/review]] — 신경 렌더링 기반 시뮬레이션은 실시간 게임 엔진으로서의 확산 모델 기술을 로봇 시뮬레이션에 적용한 사례입니다.
- 🔄 다른 접근: [[papers/1431_Impact_of_Static_Friction_on_Sim2Real_in_Robotic_Reinforceme/review]] — 둘 다 시뮬레이션과 현실 간의 격차를 줄이는 데 초점을 맞추지만, 정적 마찰 연구는 물리적 요소를, Re³Sim은 3D 인식에 중점을 둔다.
- 🏛 기반 연구: [[papers/1413_GraspVLA_a_Grasping_Foundation_Model_Pre-trained_on_Billion-/review]] — 3D-prior 기반 고해상도 시뮬레이션 데이터 생성 개념을 grasping 특화 합성 데이터셋 구축에 적용했다.
- 🔄 다른 접근: [[papers/1527_Real2Render2Real_Scaling_Robot_Data_Without_Dynamics_Simulat/review]] — R2R2R과 Re3Sim 모두 로봇 데이터 생성을 위한 real-to-sim 접근법이지만 동역학 시뮬레이션 필요성에서 차별화됩니다.
- 🔄 다른 접근: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — Re3Sim은 고충실도 시뮬레이션 데이터 생성으로 sim-to-real 문제를 다른 각도에서 해결하는 접근법이다.
- 🏛 기반 연구: [[papers/1540_RoboGen_Towards_Unleashing_Infinite_Data_for_Automated_Robot/review]] — Re³Sim의 3D 생성 기반 고품질 시뮬레이션 데이터 생성 기술이 RoboGen의 자동 데이터 생성 파이프라인에 핵심 기술을 제공한다.
- 🔗 후속 연구: [[papers/1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering/review]] — 고품질 3D 장면 렌더링 기술을 3D-photo guided 시뮬레이션 데이터 생성에 활용할 수 있습니다.
- 🔗 후속 연구: [[papers/1299_A_Survey_of_Robotic_Navigation_and_Manipulation_with_Physics/review]] — 3D 기반 고품질 시뮬레이션 데이터 생성으로 physics simulator의 한계를 극복한다.
