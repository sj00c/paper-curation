---
title: "1484_MuJoCo_Playground"
authors:
  - "Kevin Zakka"
  - "Baruch Tabanpour"
  - "Qiayuan Liao"
  - "Mustafa Haiderbhai"
  - "Samuel Holt"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "MuJoCo Playground는 MJX 기반의 오픈소스 로봇 학습 프레임워크로, GPU에서 빠른 정책 훈련과 다양한 로봇 플랫폼으로의 제로샷 sim-to-real 전이를 가능하게 한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zakka et al._2025_MuJoCo Playground.pdf"
---

# MuJoCo Playground

> **저자**: Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A. Kahrs, Carmelo Sferrazza, Yuval Tassa, Pieter Abbeel | **날짜**: 2025-02-12 | **URL**: [https://arxiv.org/abs/2502.08844](https://arxiv.org/abs/2502.08844)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1:*

MuJoCo Playground는 MJX 기반의 오픈소스 로봇 학습 프레임워크로, GPU에서 빠른 정책 훈련과 다양한 로봇 플랫폼으로의 제로샷 sim-to-real 전이를 가능하게 한다.

## Motivation

- **Known**: 강화학습(RL)을 통한 sim-to-real 전이는 로봇 학습의 주요 패러다임이며, GPU 기반 시뮬레이션은 훈련 속도를 크게 향상시킬 수 있다는 것이 알려져 있다.
- **Gap**: 기존의 로봇 학습 프레임워크들은 설치, 환경 구성, 시각 기반 정책 훈련이 복잡하고, 다양한 로봇 플랫폼에 대한 통합된 sim-to-real 파이프라인이 부족했다.
- **Why**: 로봇 학습의 반복적 개선 과정에서 빠른 훈련 속도와 쉬운 배포는 보상 함수 설계 등 인간의 개입을 통한 효율적인 프로토타이핑을 가능하게 한다.
- **Approach**: MJX 물리 엔진, Madrona 배치 렌더러, 그리고 통합된 훈련 환경을 결합한 완전한 오픈소스 스택을 구현하여, 단일 GPU에서 다양한 로봇 플랫폼의 정책을 빠르게 훈련하고 전이할 수 있도록 설계했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: A preview of locomotion and manipulation environments available in MuJoCo Playground.*

- **포괄적인 환경 스위트**: DM Control Suite, 로코모션(사족 및 이족 로봇), 조작(손가락 및 팔 로봇) 등 다양한 카테고리의 환경 구현
- **시각 기반 정책 훈련**: Madrona 배치 렌더러를 MJX와 통합하여 GPU에서 end-to-end 비전 기반 정책 훈련 가능
- **광범위한 sim-to-real 검증**: Unitree Go1, Berkeley Humanoid, Unitree G1, Booster T1, LEAP Hand, Franka Arm 등 6개 로봇 플랫폼에서 제로샷 전이 달성
- **빠른 훈련 속도**: 단일 GPU에서 대부분의 작업이 분 단위의 훈련으로 완성되는 성능 달성
- **완전 재현 가능성**: 노트북, 하이퍼파라미터, 훈련 곡선이 포함된 완전한 오픈소스 파이프라인 제공

## How

![Figure 4](figures/fig4.webp)

*Fig. 4: Sample renders from the Madrona batch renderer for the*

- MJX를 기반으로 GPU 가속 물리 엔진을 구현하여 병렬 처리 및 고속 시뮬레이션 실현
- JAX 원시 요소를 통해 Madrona 렌더러를 MJX와 통합하여 jit 및 vmap 변환과 호환되도록 설계
- 도메인 랜덤화를 통해 시각 기반 정책의 sim-to-real 전이 강화(기하학 크기, 색상, 조명, 카메라 위치 등)
- 각 로봇 플랫폼별로 조이스틱 명령 추적, 낙하 복구, 물체 재배치 등 특화된 MDP 공식화
- MuJoCo Menagerie의 로봇 자산을 활용하여 다양한 로봇 모델에 대한 일관된 환경 구성

## Originality

- MJX와 Madrona 렌더러의 통합을 통해 GPU에서 물리, 렌더링, 훈련을 완전히 on-device에서 수행하는 혁신적인 파이프라인 구현
- 교사-학생 증류 없이 end-to-end 시각 기반 정책 훈련을 단일 GPU에서 가능하게 한 기술적 기여
- 6개의 다양한 로봇 플랫폼에서 제로샷 sim-to-real 전이를 체계적으로 입증한 광범위한 실증 연구
- pip install 기반의 단순한 설치와 Colab 노트북 기반의 완전한 파이프라인을 제공하여 접근성 극대화

## Limitation & Further Study

- Madrona 렌더러의 일부 기능(변형 가능한 재료, 이동 조명, 지형 높이장)이 아직 미구현된 상태
- DM Control Suite 환경의 시각 기반 훈련은 CartpoleBalance 한 가지만 시연되었으며, 더 광범위한 탐색이 필요
- 실제 로봇 이용 가능성이 제한적일 수 있어 다양한 연구기관에서의 검증이 필요
- 후속 연구로 더 복잡한 시각 특징(변형 가능한 물체, 동적 환경)에 대한 렌더링 지원 확대 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MuJoCo Playground는 MJX와 Madrona를 결합한 혁신적인 기술과 6개 로봇 플랫폼에서의 광범위한 sim-to-real 검증을 통해, 로봇 학습의 접근성과 효율성을 획기적으로 향상시킨 중요한 기여다.

## Related Papers

- 🔄 다른 접근: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — ManiSkill3도 GPU 기반 로봇 시뮬레이션을 제공하지만 더 복잡한 접촉 물리와 렌더링에 특화된 반면, MuJoCo Playground는 단순성과 속도에 중점을 둡니다.
- 🔗 후속 연구: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — MuJoCo Playground의 제로샷 sim-to-real 능력은 시각 기반 손재주 조작의 sim-to-real 연구를 더욱 효율적으로 만듭니다.
- 🏛 기반 연구: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — MuJoCo 기반의 실제 휴머노이드 로코모션 연구는 MuJoCo Playground가 제공하는 시뮬레이션 환경의 실용성을 검증합니다.
- 🔄 다른 접근: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — MuJoCo Playground와 Octo 모두 범용 로봇 정책 학습을 위한 프레임워크이지만 서로 다른 접근 방식을 사용합니다.
- 🔗 후속 연구: [[papers/1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat/review]] — MuJoCo Playground의 빠른 정책 훈련은 AutoRT의 대규모 로봇 오케스트레이션에 필요한 효율적인 학습 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — MJX 기반의 GPU 가속 학습은 OpenVLA와 같은 대규모 VLA 모델의 효율적인 훈련을 가능하게 합니다.
- 🔄 다른 접근: [[papers/1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf/review]] — 둘 다 사족 로봇 시뮬레이션을 다루지만 MuJoCo playground와 forward dynamics model의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — 둘 다 로봇 시뮬레이션 환경이지만, ManiSkill3는 GPU 병렬화에, MuJoCo Playground는 다양한 시뮬레이션 실험에 초점을 둔다.
- 🔄 다른 접근: [[papers/1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf/review]] — 둘 다 사족 로봇을 위한 시뮬레이션 기반 접근법이지만 forward dynamics model과 MuJoCo 기반 학습의 차이점을 비교할 수 있다.
