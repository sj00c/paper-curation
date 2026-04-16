---
title: "1301_A3VLM_Actionable_Articulation-Aware_Vision_Language_Model"
authors:
  - "Siyuan Huang"
  - "Haonan Chang"
  - "Yuhan Liu"
  - "Yimeng Zhu"
  - "Hao Dong"
date: "2024.06"
doi: ""
arxiv: ""
score: 4.0
essence: "A3VLM은 로봇 중심의 행동 학습 대신 물체 중심의 관절 구조(articulation)와 행동 가능성(affordance)을 인식하는 Vision Language Model로, 비용이 많이 드는 로봇 상호작용 데이터 수집을 최소화하면서도 다양한 로봇에 적용 가능한 표현을 학습한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2024_A3VLM Actionable Articulation-Aware Vision Language Model.pdf"
---

# A3VLM: Actionable Articulation-Aware Vision Language Model

> **저자**: Siyuan Huang, Haonan Chang, Yuhan Liu, Yimeng Zhu, Hao Dong, Peng Gao, Abdeslam Boularias, Hongsheng Li | **날짜**: 2024-06-11 | **URL**: [https://arxiv.org/abs/2406.07549](https://arxiv.org/abs/2406.07549)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Articulation Representation in A3VLM*

A3VLM은 로봇 중심의 행동 학습 대신 물체 중심의 관절 구조(articulation)와 행동 가능성(affordance)을 인식하는 Vision Language Model로, 비용이 많이 드는 로봇 상호작용 데이터 수집을 최소화하면서도 다양한 로봇에 적용 가능한 표현을 학습한다.

## Motivation

- **Known**: RT-1, RT-2, ManipLLM 등 기존 VLM 기반 로봇 조작 모델들은 로봇 중심의 행동을 직접 학습하여 높은 성능을 보였으나, 대량의 비용이 많이 드는 로봇 상호작용 데이터 수집이 필요했다. GaPartNet은 물체의 관절 구조를 9가지 타입으로 분류하여 감지했으나 점군(point cloud) 기반으로 작동하여 실제 환경에서 노이즈에 취약했다.
- **Gap**: 기존 방법들은 로봇별 맞춤형 데이터를 요구하고, 물체 기반 표현과 로봇 독립적 표현의 부족으로 인해 재사용성이 낮고 실제 환경에서의 적용성이 제한된다. 또한 관절 구조 인식과 행동 가능성을 동시에 예측할 수 있는 VLM 기반 접근법이 부족하다.
- **Why**: 물체 중심의 로봇 독립적 표현은 다양한 로봇에 재사용 가능한 조작 모델을 학습할 수 있게 하고, 단일 RGB 이미지만으로 3D 관절 구조를 파악할 수 있는 능력은 실제 환경의 노이즈 문제를 해결하며 비용 효율적인 로봇 조작을 가능하게 한다.
- **Approach**: A3VLM은 (Bounding box B, Axis A, Semantic label S) 삼중항으로 물체의 관절 구조와 행동 가능성을 표현하며, 순차적 프롬프트를 통해 4가지 하위 작업으로 분리하여 VLM 미세조정(fine-tuning)을 수행한다. PartNet-Mobility 데이터셋에서 생성한 이미지와 ControlNet 기반 데이터 증강을 활용하여 instruction-following 데이터셋을 구성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Sequential inference with prompts. To answer the first question, A3VLM identifies the corresponding action typ*

- **PartNet-Mobility 벤치마크 우수 성능**: 기존 관련 모델들을 큰 폭으로 능가하는 성능을 달성
- **물체 중심 로봇 독립적 표현**: 특정 로봇에 종속되지 않는 표현으로 다양한 로봇에 적용 가능
- **RGB만으로 3D 관절 구조 예측**: 깊이 데이터 없이 단일 RGB 이미지로 정확한 articulation 정보 추출
- **실제 환경 강건성**: 시뮬레이션과 실제 환경 모두에서 우수한 안정성과 견고성 입증
- **코드 및 자료 공개**: 재현성을 위해 GitHub에서 코드와 학습 자료 제공

## How

![Figure 3](figures/fig3.webp)

*Figure 3. Annotations used for training A3VLM on the PartNet-Mobility dataset.*

- PartNet-Mobility의 2,000개 이상의 관절 물체를 PyRender로 렌더링하여 객체당 40개의 다양한 뷰 이미지 생성
- ControlNet을 활용한 이미지 증강으로 학습 데이터 다양성 증대
- URDF 형식의 회전축(revolute)과 병진축(prismatic) 정보를 활용한 자동 annotation 생성
- 4가지 하위 작업(action type localization, bounding box prediction, axis prediction, semantic label prediction)으로 순차적 학습 구조 설계
- 예측된 관절 구조와 행동 정보를 simple action primitives(sliding, rotating, scrolling)으로 변환하여 로봇 행동 생성

## Originality

- **object-centric representation**: 로봇 중심에서 물체 중심으로의 패러다임 전환으로 로봇 독립성 확보
- **articulation + affordance 통합**: 관절 구조 인식과 행동 가능성을 VLM으로 동시에 예측하는 첫 시도
- **RGB 기반 3D 구조 예측**: 기존 point cloud 기반 방식의 노이즈 문제를 VLM 기반으로 해결
- **단순화된 articulation 분류**: 9가지 타입을 prismatic/revolute 2가지로 단순화하여 학습 효율성 증대
- **instruction-following 데이터셋 자동 구성**: URDF 정보로부터 체계적인 annotation 자동 생성 파이프라인

## Limitation & Further Study

- **시뮬레이션 데이터 의존성**: 학습에 PartNet-Mobility 시뮬레이션 데이터를 주로 활용하여 sim-to-real gap 존재 가능성
- **복잡한 관절 구조 제약**: prismatic과 revolute 2가지로 단순화되어 나선형 조인트 등 복잡한 관절 구조 미지원
- **폐색(occlusion) 처리 미충분**: 일부 부품이 가려진 상황에서의 성능 한계 미평가
- **실시간 성능 미평가**: VLM 기반 순차 추론의 계산량과 실시간 조작 적용 가능성 미확인
- **후속연구 방향**: 다양한 실제 환경의 물체에 대한 학습 데이터 확충, 더 복잡한 관절 구조 지원, 동적 환경에서의 안정성 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: A3VLM은 로봇 조작 문제에 대한 object-centric 패러다임을 제시하며, VLM을 활용하여 물체의 관절 구조와 행동 가능성을 효과적으로 인식하는 혁신적인 접근법이다. 비용 효율성, 로봇 독립성, 실제 환경에서의 강건성을 동시에 달성하여 실용적 가치가 높고 후속 연구에 큰 영감을 줄 수 있는 의미 있는 기여이다.

## Related Papers

- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — A3VLM의 물체 중심 관절 구조 인식과 RoboPoint의 공간 어포던스 예측은 물체 이해 기반 로봇 조작의 보완적 접근법이다.
- 🔄 다른 접근: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — A3VLM의 물체 중심 어포던스와 VoxPoser의 3D 가치 맵 기반 조작은 공간-의미 이해의 서로 다른 표현 방식이다.
- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — Grounding DINO의 시각적 grounding 기술은 A3VLM의 관절 구조와 어포던스 인식에 핵심 기반을 제공한다.
- 🏛 기반 연구: [[papers/1333_CLIPort_What_and_Where_Pathways_for_Robotic_Manipulation/review]] — CLIPort의 what-where pathway 개념이 A3VLM의 물체 중심 관절 구조 인식 접근법의 기초적 아이디어를 제공합니다.
- 🔗 후속 연구: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — UniAff의 통합 affordance 표현은 A3VLM의 물체 중심 행동 가능성 학습을 더 일반화한 접근법입니다.
- 🔄 다른 접근: [[papers/1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde/review]] — 둘 다 robotic affordance를 다루지만 ManipVQA는 질의응답 형태로, A3VLM은 관절 구조 인식으로 접근합니다.
- 🏛 기반 연구: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — 로봇 어포던스 기반 언어 학습의 이론적 기반을 관절 인식 VLM으로 확장합니다.
- 🔄 다른 접근: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — 둘 다 관절형 객체와 affordance를 다루지만 A3VLM은 actionable articulation에 집중하는 다른 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1333_CLIPort_What_and_Where_Pathways_for_Robotic_Manipulation/review]] — CLIPort의 what-where pathway가 A3VLM의 물체 중심 관절 구조 인식의 기초적 아이디어를 제공합니다.
