---
title: "1614_VL-Nav_A_Neuro-Symbolic_Approach_for_Reasoning-based_Vision-"
authors:
  - "Yi Du"
  - "Taimeng Fu"
  - "Zhipeng Zhao"
  - "Shaoshu Su"
  - "Zitong Zhan"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "VL-Nav는 신경-기호 접근법(NeSy)을 통해 복잡한 인간 지시에 따라 미지의 대규모 환경을 탐색하는 로봇 네비게이션 시스템으로, VLM의 추론 능력과 기호적 안내를 결합한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Du et al._2025_VL-Nav A Neuro-Symbolic Approach for Reasoning-based Vision-Language Navigation.pdf"
---

# VL-Nav: A Neuro-Symbolic Approach for Reasoning-based Vision-Language Navigation

> **저자**: Yi Du, Taimeng Fu, Zhipeng Zhao, Shaoshu Su, Zitong Zhan, Qiwei Du, Zhuoqun Chen, Bowen Li, Chen Wang | **날짜**: 2025-02-02 | **URL**: [https://arxiv.org/abs/2502.00931](https://arxiv.org/abs/2502.00931)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: System pipeline overview.Complex tasks are de-*

VL-Nav는 신경-기호 접근법(NeSy)을 통해 복잡한 인간 지시에 따라 미지의 대규모 환경을 탐색하는 로봇 네비게이션 시스템으로, VLM의 추론 능력과 기호적 안내를 결합한다.

## Motivation

- **Known**: 기존 end-to-end 학습은 데이터 부족과 sim2real 전이 문제가 있으며, foundation model 기반 모듈형 방법들은 명시적 단일 목표 탐색에는 효과적이지만 추상적 다중 목표 추론이 부족하다.
- **Gap**: 기존 방법들은 복잡한 다중 목표 작업을 분해하지 못하고 효율적인 탐색 전략이 부족하여, 로봇이 목표 없이 방황하거나 잘못된 객체를 인식하는 문제가 있다.
- **Why**: 자율 이동 로봇이 복잡한 추상적 지시(예: 비가 내리므로 방수 의류 찾기)를 이해하고 대규모 환경에서 효율적으로 탐색할 수 있어야 실제 응용이 가능하기 때문이다.
- **Approach**: VL-Nav는 NeSy Task Planner로 VLM의 추론을 3D scene graph와 image memory의 기호적 메모리에 기반하게 하고, NeSy Exploration System으로 신경 기반 의미 정보와 기호적 휴리스틱 함수를 결합하여 효율적 탐색을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Given the complex instruction, VL-Nav autonomously*

- **DARPA TIAMAT Challenge 성과**: 실내 환경 83.4%, 실외 환경 75% 성공률 달성
- **실제 로봇 배포**: 4개 다양한 환경에서 86.3% 성공률, 483미터 장거리 주행 포함
- **다층 건물 복잡 작업**: 3D 다층 시나리오에서 복잡한 지시 처리 검증
- **일반화 능력**: 실내 폐쇄 환경에서 비정형 실외 환경까지 일반화 가능성 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: System pipeline overview.Complex tasks are de-*

- NeSy Task Planner: 추상적 다중 목표 지시를 원자적 부작업으로 분해하고, 탐색 부작업 또는 목표 지점 이동 부작업을 동적으로 발행
- 3D Scene Graph: 환경의 기하학적 및 의미론적 정보를 저장하여 VLM 추론의 정확성 향상
- Image Memory System: 과거 탐색 기록을 유지하여 VLM이 방문 이력을 기반으로 의사결정
- NeSy Exploration System: lightweight VLM의 의미론적 단서와 frontier-based 휴리스틱을 결합
- VL Scoring: pixel-wise 점수로 작업 관련 영역을 우선순위화하여 불필요한 반복 이동 최소화
- Path Planner: 장애물 회피 및 목표 지점 도달을 위한 경로 계획

## Originality

- 신경-기호 통합의 새로운 구현: VLM의 신경 추론 능력을 3D scene graph와 image memory의 기호적 메모리에 명시적으로 기반하게 함으로써 추론의 신뢰성 향상
- 추상적 다중 목표 추론: 단순 객체 검색을 넘어 의미론적 추론(예: 날씨 → 의류 타입)을 통한 복잡한 작업 해석
- 효율적 탐색 전략의 신경-기호 결합: semantic cue와 geometric frontier를 통합한 VL Scoring으로 기존 방법들보다 우월한 탐색 효율성
- 실제 로봇 검증: 시뮬레이션뿐 아니라 다양한 실제 환경에서의 광범위한 배포 및 평가

## Limitation & Further Study

- 계산 복잡도: NeSy Task Planner와 VL Module의 지속적 동작이 제한된 자원 환경에서 병목이 될 수 있으며, 경량화 방안 추가 연구 필요
- Scene Graph 구성: 초기 scene graph 구축과 유지 보수의 신뢰성에 따라 시스템 성능이 크게 영향을 받으므로, 더 강건한 그래프 생성 방법 필요
- 실외 환경 성능: 실외 환경에서 75% 성공률로 실내 83.4%보다 낮으므로, 야외 다양한 조건(날씨, 조명 변화)에 대한 강건성 개선 필요
- 일반화 한계: DARPA TIAMAT 과제 특화된 시스템으로, 다른 도메인의 복잡한 지시에 대한 적응성 검증 필요
- 장거리 누적 오차: SLAM 기반의 누적 위치 오차가 매우 장거리 탐색에서 문제가 될 수 있으므로, Loop Closure 또는 Global Relocalization 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VL-Nav는 신경-기호 통합을 통해 복잡한 추상적 지시 기반 로봇 네비게이션의 중요한 문제를 해결하며, DARPA TIAMAT에서의 우수한 성과와 실제 로봇 배포를 통해 실용성을 입증한 의미 있는 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason/review]] — physical common sense reasoning이 neuro-symbolic VLN의 추론 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — 복잡한 instruction following을 위한 서로 다른 접근법 - neuro-symbolic vs enhanced waypoint prediction입니다.
- 🔗 후속 연구: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — reinforced embodied reasoning을 neuro-symbolic 접근법과 결합할 수 있습니다.
- 🔗 후속 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — top-view spatial reasoning을 복잡한 추론 기반 네비게이션으로 확장하여 신경-기호 접근법으로 발전시켰습니다.
- 🏛 기반 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — vision-language navigation을 위한 visual language map의 기본 개념을 제공하여 VL-Nav의 추론 기반 네비게이션에 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — 둘 다 large language model을 활용한 로봇 행동 계획을 다루지만 CoPAL은 corrective planning에, VL-Nav는 navigation reasoning에 집중합니다.
- 🏛 기반 연구: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — VL-Nav의 neuro-symbolic 추론을 spatial-geometric과 visual-semantic 분리로 구체화하여 발전시킨다.
- 🔗 후속 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — 신경-기호 접근법을 통해 복잡한 추론이 필요한 vision-language navigation으로 TopV-Nav의 공간 추론을 확장합니다.
