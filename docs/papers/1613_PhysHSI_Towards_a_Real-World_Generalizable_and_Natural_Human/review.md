---
title: "1613_PhysHSI_Towards_a_Real-World_Generalizable_and_Natural_Human"
authors:
  - "Huayi Wang"
  - "Wentao Zhang"
  - "Runyi Yu"
  - "Tao Huang"
  - "Junli Ren"
date: "2025.10"
doi: "10.48550/arXiv.2510.11072"
arxiv: ""
score: 4.0
essence: "PhysHSI는 humanoid 로봇이 실제 환경에서 물체 운반, 앉기, 누우기 등 다양한 상호작용을 자연스럽고 일반화 가능하게 수행할 수 있도록 하는 통합 시스템으로, simulation 기반 AMP 정책 학습과 실시간 LiDAR-camera 기반 객체 인식 모듈을 결합한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_PhysHSI Towards a Real-World Generalizable and Natural Humanoid-Scene Interaction System.pdf"
---

# PhysHSI: Towards a Real-World Generalizable and Natural Humanoid-Scene Interaction System

> **저자**: Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, Qifeng Chen, Jingbo Wang, Jiangmiao Pang | **날짜**: 2025-10-13 | **DOI**: [10.48550/arXiv.2510.11072](https://doi.org/10.48550/arXiv.2510.11072)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of PhysHSI. (a) Dataset Preparation: Human motions from a MoCap dataset are retargeted to humanoid moti*

PhysHSI는 humanoid 로봇이 실제 환경에서 물체 운반, 앉기, 누우기 등 다양한 상호작용을 자연스럽고 일반화 가능하게 수행할 수 있도록 하는 통합 시스템으로, simulation 기반 AMP 정책 학습과 실시간 LiDAR-camera 기반 객체 인식 모듈을 결합한다.

## Motivation

- **Known**: Humanoid 로봇의 개별 능력(동작 생성, 물체 인식)은 각각 발전했으나, 이들을 통합하여 자연스럽고 일반화된 실세계 상호작용을 구현하는 완전한 시스템은 부재했다.
- **Gap**: 기존 방법들은 MoCap 기반 접근이 simulation에만 국한되고 perfect scene observation을 가정하며, RL 기반 방법은 수작업 reward shaping이 필요하고, 실세계 robust 객체 인식과 natural motion을 동시에 달성하지 못했다.
- **Why**: 실제 환경에서 humanoid 로봇의 실용적 배포는 자연스러운 동작, 다양한 시나리오 적응, 그리고 견고한 scene perception을 모두 만족해야 하며, 이는 가정용·산업용 로봇 자동화의 핵심 과제이다.
- **Approach**: Simulation에서 AMP 기반 정책 학습으로 retargeted MoCap 데이터로부터 natural하고 generalizable한 policy를 학습하고, 실세계 배포에서는 LiDAR odometry와 camera-based AprilTag detection을 결합한 coarse-to-fine localization 모듈로 robust scene perception을 제공한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Our system PhysHSI enables humanoid robots to perform diverse real-world interactions indoors and outdoors with *

- **통합 실세계 시스템**: AMP 기반 simulation 학습과 LiDAR-camera 기반 인식을 통합하여 실제 Unitree G1 로봇에서 box carrying, sitting, lying, standing up 등 4가지 주요 작업 성공
- **자연스러운 동작**: Adversarial motion prior을 활용하여 human MoCap 데이터로부터 학습한 lifelike behavior를 달성하며, stylized locomotion 학습도 가능
- **강한 일반화 성능**: 다양한 object goal, scene layout, 환경에서 일관되게 높은 success rate 유지 및 공간/실세계 일반화 검증
- **Robust 객체 인식**: Coarse (LiDAR odometry) + Fine (camera AprilTag) 방식으로 long-horizon task 중 객체 시야 벗어남 상황 처리 및 정밀 위치 추정

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of PhysHSI. (a) Dataset Preparation: Human motions from a MoCap dataset are retargeted to humanoid moti*

- **Data Preparation**: AMASS/SAMP 데이터셋의 human motion을 최적화 기반 retargeting으로 humanoid 동작으로 변환하고, manual annotation을 통해 key contact frame과 객체 궤적 정보를 augment
- **AMP 기반 정책 학습**: Discriminator가 reference motion과 policy 생성 motion을 구별하도록 adversarial training하여 natural style 유지하면서 task completion 달성, stage conditioning (ϕ1 pickup, ϕ2 placement)으로 multi-phase task 지원
- **Coarse-to-Fine Localization**: LiDAR odometry (10Hz)로 object가 camera FOV 밖일 때 long-range directional cue 제공, FOV 내 진입 시 AprilTag detection (30Hz) + odometry 융합으로 precise pose 추정
- **Multi-Frequency Control Pipeline**: LiDAR odometry (10Hz) → Forward Kinematic (25Hz) → Policy inference (50Hz) → PD Controller (500Hz)의 계층적 구조로 실시간 실행
- **Diverse Simulation Environment**: 다양한 object size, shape, scene layout으로 학습하여 real-world generalization 향상

## Originality

- **실세계 AMP 적용의 선례**: Existing AMP 방법들이 simulation에 국한되거나 기본 locomotion에만 사용된 반면, 본 논문은 complex object interaction (carrying, sitting, lying)까지 확장한 첫 real-world AMP 시스템
- **Coarse-to-Fine 인식 설계**: LiDAR odometry와 camera vision을 명시적으로 보완하는 hybrid localization으로 long-horizon task 중 객체 occlusion 극복
- **Post-Annotation 전략**: Retargeted motion에 사후적으로 객체 정보를 annotation하는 방식으로 physically plausible humanoid-object interaction 데이터 생성의 실질적 해결책 제시
- **포괄적 실세계 검증**: Spatial generalization, real-world scenario generalization, localization accuracy 분석 등 다층적 평가를 통한 system-level 검증

## Limitation & Further Study

- **수작업 annotation 필요**: Contact frame과 객체 궤적을 manual하게 annotate해야 하므로 데이터 확장성 및 자동화 수준이 제한됨
- **AprilTag 의존성**: Fine localization이 AprilTag 기반이므로 환경에 사전에 marker 설치 필요하며, 일반적인 real-world object에 대한 generalization 미흡
- **Task 영역 제한**: Box carrying, sitting, lying, standing up 4가지 task로 제한되어 있으며, 더 복잡한 조작(opening drawers, assembling) 등으로의 확장 미제시
- **Perception 범위**: 카메라 FOV와 LiDAR 가시 범위의 제약으로 매우 넓은 실내/실외 환경에서의 대규모 navigation이 제한될 수 있음
- **후속 연구**: (1) Self-supervised 또는 semi-automatic annotation 기법으로 데이터 확장, (2) Vision-based object detection/tracking으로 marker-free 인식 확대, (3) 더 다양한 interaction task 범위 확장, (4) Sim-to-Real 도메인 갭 정량적 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: PhysHSI는 AMP 기반 motion learning과 hybrid sensor fusion을 통합하여 humanoid의 실세계 scene interaction을 처음 실현한 high-impact system으로, 자연스러운 동작과 robust generalization을 동시에 달성했으나, annotation 자동화와 marker-free perception 확대가 실용 배포의 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1984_HoRD_Robust_Humanoid_Control_via_History-Conditioned_Reinfor/review]] — PhysHSI는 LiDAR-camera 기반 객체 인식에, HoRD는 history-conditioned 접근법에 의존하여 휴머노이드 환경 상호작용을 다르게 해결함
- 🔗 후속 연구: [[papers/2134_Perceptive_Humanoid_Parkour_Chaining_Dynamic_Human_Skills_vi/review]] — Perceptive Humanoid Parkour의 동적 환경 인식과 움직임 체이닝 기법이 PhysHSI의 환경 상호작용 능력을 확장할 수 있음
- 🏛 기반 연구: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — Gait-Adaptive Perceptive Humanoid의 실시간 지각 기반 locomotion 기술이 PhysHSI의 실시간 환경 인식 모듈의 기초가 됨
- 🧪 응용 사례: [[papers/1845_Collision-Free_Humanoid_Traversal_in_Cluttered_Indoor_Scenes/review]] — PhysHSI의 실시간 LiDAR-camera 기반 객체 인식이 Collision-Free Traversal의 cluttered 환경 navigation과 직접 연관된다
- 🔄 다른 접근: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — 두 논문 모두 LiDAR 기반 환경 인식을 사용하지만 PhysHSI는 객체 상호작용에, PolygMap은 계단 등반에 특화되어 있다
- 🔗 후속 연구: [[papers/2004_Humanoid_Whole-Body_Locomotion_on_Narrow_Terrain_via_Dynamic/review]] — PhysHSI의 자연스러운 humanoid-scene interaction이 Narrow Terrain Locomotion의 동적 균형 제어와 결합될 수 있다
- 🧪 응용 사례: [[papers/1647_RoboPlayground_구조화된_물리_도메인을_통한_로봇_평가_민주화/review]] — PhysHSI의 scene interaction 능력을 체계적으로 평가할 수 있는 벤치마크 프레임워크
- 🔗 후속 연구: [[papers/1676_SimGenHOI_Physically_Realistic_Whole-Body_Humanoid-Object_In/review]] — SimGenHOI의 물리적 human-object interaction을 실제 환경으로 확장한 시스템
- 🏛 기반 연구: [[papers/1647_RoboPlayground_구조화된_물리_도메인을_통한_로봇_평가_민주화/review]] — Structured evaluation을 위한 framework를 real-world scene interaction에 적용
- 🧪 응용 사례: [[papers/2148_TokenHSI_Unified_Synthesis_of_Physical_Human-Scene_Interacti/review]] — 통합된 HSI 기술이 실제 세계에서 일반화 가능하고 자연스러운 인간-휴머노이드 상호작용 구현에 적용된다.
