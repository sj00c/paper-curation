---
title: "1483_MuBlE_MuJoCo_and_Blender_simulation_Environment_and_Benchmar"
authors:
  - "Michal Nazarczuk"
  - "Karla Stepanova"
  - "Jan Kristof Behrens"
  - "Matej Hoffmann"
  - "Krystian Mikolajczyk"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "MuBlE는 MuJoCo 물리 엔진과 Blender 렌더러를 결합한 로봇 조작 시뮬레이션 환경으로, 현실적인 시각 관찰과 정확한 물리 모델링을 동시에 제공하여 장기 과제 계획을 지원한다. SHOP-VRB2 벤치마크와 함께 시각-물리 속성을 모두 고려하는 다단계 추론 작업 평가를 가능하게 한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Nazarczuk et al._2025_MuBlE MuJoCo and Blender simulation Environment and Benchmark for Task Planning in Robot Manipulati.pdf"
---

# MuBlE: MuJoCo and Blender simulation Environment and Benchmark for Task Planning in Robot Manipulation

> **저자**: Michal Nazarczuk, Karla Stepanova, Jan Kristof Behrens, Matej Hoffmann, Krystian Mikolajczyk | **날짜**: 2025-03-04 | **URL**: [https://arxiv.org/abs/2503.02834](https://arxiv.org/abs/2503.02834)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2.*

MuBlE는 MuJoCo 물리 엔진과 Blender 렌더러를 결합한 로봇 조작 시뮬레이션 환경으로, 현실적인 시각 관찰과 정확한 물리 모델링을 동시에 제공하여 장기 과제 계획을 지원한다. SHOP-VRB2 벤치마크와 함께 시각-물리 속성을 모두 고려하는 다단계 추론 작업 평가를 가능하게 한다.

## Motivation

- **Known**: 기존 시뮬레이터(ManipulaTHOR, CoppeliaSim, iGibson)는 물리 정확도와 시각 품질 중 하나를 선택해야 하는 트레이드오프를 갖고 있다. 로봇 조작 작업을 위한 벤치마크는 주로 시각 속성 또는 언어 이해만 다루고 있다.
- **Gap**: 현재 체화된 추론 에이전트는 물리적 상호작용을 통해 정보를 획득해야 하는 장기 과제(예: '가장 가벼운 것부터 무거운 것 순으로 분류')를 계획하지 못한다. 고품질 렌더링과 정확한 물리 모델링을 모두 제공하면서 닫힌 루프 상호작용을 지원하는 환경이 부재하다.
- **Why**: 정확한 시뮬레이션 환경은 sim-to-real 전이 성능을 향상시키고, 로봇이 무게, 강성 같은 비시각 속성을 고려한 추론을 학습할 수 있게 한다. 장기 조작 작업을 위한 닫힌 루프 학습 데이터 생성이 필수적이다.
- **Approach**: MuBlE는 robosuite 기반으로 MuJoCo 물리 시뮬레이션 루프와 Blender 렌더링을 분리하여 두 수준의 상호작용(시각-행동 루프, 제어-물리 루프)을 지원한다. SHOP-VRB2는 10가지 다단계 추론 시나리오로 구성되어 시각적, 물리적 측정을 모두 요구한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **MuBlE 환경**: robosuite 기반 모듈식 설계로 높은 품질의 Blender 렌더링과 MuJoCo의 정확한 물리 시뮬레이션을 통합하며, 비시각 속성(무게, 강성)을 포함한 multimodal 데이터 생성 지원
- **SHOP-VRB2 벤치마크**: 12,000개 장면과 10가지 조작 과제로 시각 속성 및 물리 측정을 모두 고려하는 폐쇄 루프 추론 평가 가능
- **Sim-to-real 검증**: CLIER와의 통합으로 시뮬레이션과 실제 로봇 실험 비교를 통해 환경의 현실성 입증
- **설계 유연성**: 연속/이산 행동 공간 모두 지원하고 원시 행동 제어기(approach, gripper closing, lifting 등) 제공

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- MuJoCo를 이용한 정확한 강체 동역학 및 관절 시스템 물리 시뮬레이션
- Blender를 통한 절차적 재료 생성 및 포토리얼리스틱 이미지 렌더링
- 원시 행동 제어기를 통한 높은 수준의 행동 추상화와 저수준 연속 제어의 결합
- 장면 그래프 생성으로 객체 속성 및 관계에 대한 ground truth 제공
- 폐쇄 루프 상호작용을 위한 action-render 루프와 physics 루프의 분리 구조
- YCB 객체를 포함한 sim-to-real 전이 검증 장면(30개) 포함

## Originality

- 고품질 렌더링과 정확한 물리 모델링의 최초 결합 - 기존 시뮬레이터는 둘 중 하나만 우수
- 비시각 물리 속성(무게, 강성)을 행동 제어와 연계한 최초의 벤치마크 설계
- 원시 행동과 연속 제어의 하이브리드 방식으로 두 가지 추상화 수준 모두 지원
- 폐쇄 루프 상호작용을 명시적으로 지원하는 두 수준(시각-행동, 제어-물리)의 상호작용 루프 설계

## Limitation & Further Study

- 현재 tabletop 조작으로 제한되며 전신 이동 로봇이나 복잡한 환경으로의 확장 가능성 검토 필요
- Blender 렌더링의 높은 계산량으로 인한 속도 vs. 품질 트레이드오프 분석 부족
- SHOP-VRB2의 10가지 과제가 얼마나 일반화되는지, 새로운 과제 유형에 대한 성능 평가 필요
- sim-to-real 검증이 YCB 객체 30개 장면으로 제한되어 더 광범위한 검증 필요
- 비시각 속성 감지를 위한 센서 시뮬레이션의 현실성(예: 무게 추정 메커니즘) 상세 설명 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MuBlE는 로봇 조작 연구의 중요한 격차를 해결하여 고품질 렌더링과 정확한 물리를 동시에 제공하며, SHOP-VRB2 벤치마크는 폐쇄 루프 추론에 필요한 멀티모달 데이터를 제공한다. Sim-to-real 검증과 실제 로봇 실험을 통해 실질적 가치를 입증하며 오픈소스 공개로 연구 커뮤니티에 기여한다.

## Related Papers

- 🏛 기반 연구: [[papers/1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R/review]] — MuBlE는 robosuite의 MuJoCo 기반을 확장하여 Blender 렌더링을 추가한 발전된 시뮬레이션 환경입니다.
- 🔄 다른 접근: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — ManiSkill3과 MuBlE 모두 GPU 가속 로봇 시뮬레이션을 제공하지만 서로 다른 렌더링 엔진을 사용합니다.
- 🔗 후속 연구: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — MuBlE의 시각-물리 통합 환경은 3D-VLA와 같은 3D 비전-언어-액션 모델의 훈련에 활용될 수 있습니다.
- 🔗 후속 연구: [[papers/1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R/review]] — robosuite의 기본 시뮬레이션 개념을 MuBlE가 Blender와 결합하여 확장한다.
