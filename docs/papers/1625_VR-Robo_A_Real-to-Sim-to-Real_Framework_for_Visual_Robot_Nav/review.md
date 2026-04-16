---
title: "1625_VR-Robo_A_Real-to-Sim-to-Real_Framework_for_Visual_Robot_Nav"
authors:
  - "Shaoting Zhu"
  - "Linzhan Mou"
  - "Derun Li"
  - "Baijun Ye"
  - "Runhan Huang"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "3D Gaussian Splatting을 활용하여 실제 환경을 포토리얼리스틱한 디지털 트윈으로 재구성하고, 이를 시뮬레이션에 통합하여 RL 기반 시각 네비게이션 정책을 학습한 후 실제 로봇에 무영점 전이하는 Real-to-Sim-to-Real 프레임워크를 제시한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhu et al._2025_VR-Robo A Real-to-Sim-to-Real Framework for Visual Robot Navigation and Locomotion.pdf"
---

# VR-Robo: A Real-to-Sim-to-Real Framework for Visual Robot Navigation and Locomotion

> **저자**: Shaoting Zhu, Linzhan Mou, Derun Li, Baijun Ye, Runhan Huang, Hang Zhao | **날짜**: 2025-02-03 | **URL**: [https://arxiv.org/abs/2502.01536](https://arxiv.org/abs/2502.01536)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our VR-Robo introduces a unified real-to-sim-to-*

3D Gaussian Splatting을 활용하여 실제 환경을 포토리얼리스틱한 디지털 트윈으로 재구성하고, 이를 시뮬레이션에 통합하여 RL 기반 시각 네비게이션 정책을 학습한 후 실제 로봇에 무영점 전이하는 Real-to-Sim-to-Real 프레임워크를 제시한다.

## Motivation

- **Known**: RL과 물리 시뮬레이터를 통한 다리 로봇 제어는 성공적이나, 시뮬레이터가 시각적 현실성과 복잡한 기하를 재현하지 못해 실제 배포 시 sim-to-real 갭이 발생하며, 현존 RGB 기반 시각 정책은 저수준 작업에만 국한된다.
- **Gap**: 기존의 NeRF/3DGS 기반 Real-to-Sim 접근법들은 포토리얼리즘에 중점을 두면서 물리 상호작용과 환경 탐색 메커니즘이 부족하여, RGB 기반 고수준 네비게이션 태스크를 지원하기 어렵다.
- **Why**: 가정용/산업용 로봇의 실제 배포에는 다양한 환경에서 RGB만으로 네비게이션을 수행할 수 있는 견고한 정책이 필수적이며, 시뮬레이션의 포토리얼리즘과 물리 상호작용의 결합이 이를 가능하게 한다.
- **Approach**: 멀티뷰 RGB 이미지로부터 3DGS와 foundation model 제약을 활용하여 기하 일관성 있는 환경을 재구성하고, GS-Mesh 하이브리드 표현으로 Isaac Sim에 통합한 뒤, 물체 임의화와 폐색 인식 장면 구성 전략으로 강화되는 정책을 학습한다.

## Achievement


- **포토리얼리스틱하고 물리 상호작용 가능한 디지털 트윈 생성**: GS-Mesh 하이브리드 표현과 좌표 정렬을 통해 시각적 충실도와 물리 시뮬레이션을 동시에 지원
- **RGB 기반 무영점 sim-to-real 전이**: 깊이/LiDAR 없이 RGB 관찰만으로 학습한 정책이 실제 환경에서 목표 추적 네비게이션을 수행
- **복잡한 환경에서의 빠른 정책 적응**: 물체 임의화와 폐색 인식 구성 전략으로 새로운 환경에서의 탐색과 적응 능력 향상

## How

![Figure 4](figures/fig4.webp)

*Fig. 4: VR-Robo real-to-sim-to-real framework. We build a realistic and interactive simulation environment with GS-mesh*

- Structure from Motion (SfM)으로 카메라 포즈 추정 후 3D Gaussian Splatting으로 장면과 물체를 분리 재구성
- Foundation model 제약 (depth, normal)을 활용한 기하 일관성 강화
- GS-mesh 하이브리드 표현으로 렌더링은 3DGS, 물리 상호작용은 메시 기반으로 처리
- 좌표 정렬(coordinate alignment)을 통해 시뮬레이션과 실제 환경 간 scale 일치
- 에이전트-물체 임의화와 폐색 인식 장면 구성으로 RL 정책의 견고성 향상
- Isaac Sim 내에서 ego-centric RGB 관찰과 proprioception으로 정책 학습
- 학습된 정책을 별도의 재학습 없이 실제 로봇에 배포

## Originality

- GS-mesh 하이브리드 표현으로 포토리얼리즘과 물리 상호작용의 괴리를 처음으로 체계적으로 해결
- Foundation model 제약을 활용한 기하 일관성 재구성 방식이 기존 순수 3DGS 방법보다 구조적으로 개선
- 물체 임의화와 폐색 인식 장면 구성이 환경 변화에 대한 정책 견고성을 구체적으로 강화하는 전략
- RGB 기반만으로 복잡한 multi-level 네비게이션(계단/경사로 오르내림)을 달성한 첫 사례

## Limitation & Further Study

- 멀티뷰 RGB 이미지 수집과 COLMAP 처리가 필요하며, 이로 인한 초기 설정 비용이 상당함
- 3DGS 재구성의 품질이 입력 이미지의 다양성과 coverage에 크게 의존하여, 제약된 뷰에서는 성능 저하 가능
- 메시 기반 물리 상호작용이 연속적인 지형(모래, 풀 등)을 표현하기 어렵고, 테이블·계단 등 이산적 구조에 최적화됨
- 실제 환경의 동적 요소(사람, 물건 이동)에 대한 적응 메커니즘이 부재하여, 장기 배포 시 재구성 필요
- 후속 연구: 온라인 재구성/업데이트 메커니즘, 연속 지형 표현 개선, 동적 환경 추적 기술 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RGB 기반 시각 네비게이션과 로컬로모션의 sim-to-real 갭을 포토리얼리즘과 물리 상호작용의 결합으로 효과적으로 해결하며, 실제 로봇 배포에서의 무영점 전이를 달성한 실용적이고 창의적인 접근법이다.

## Related Papers

- 🔄 다른 접근: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — 두 논문 모두 sim-to-real 전이를 다루지만 시각 네비게이션 vs 정교한 손가락 조작으로 응용 도메인이 다릅니다.
- 🏛 기반 연구: [[papers/1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering/review]] — 3D Gaussian Splatting은 VR-Robo의 포토리얼리스틱 디지털 트윈 구성을 위한 핵심 렌더링 기술을 제공합니다.
- 🔗 후속 연구: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — Real-World Humanoid Locomotion의 실제 로봇 배포 경험은 VR-Robo의 sim-to-real 프레임워크 검증에 중요한 참고사례입니다.
- 🔄 다른 접근: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — 두 논문 모두 sim-to-real 전이를 다루지만 손가락 조작 vs 시각 네비게이션으로 응용 영역이 다릅니다.
