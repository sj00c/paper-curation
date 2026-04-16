---
title: "1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde"
authors:
  - "Siyuan Huang"
  - "Iaroslav Ponomarenko"
  - "Zhengkai Jiang"
  - "Xiaoqi Li"
  - "Xiaobin Hu"
date: "2024.03"
doi: ""
arxiv: ""
score: 4.0
essence: "ManipVQA는 Multi-Modal Large Language Model (MLLM)에 로봇 조작 작업을 위한 affordance 인식과 물리적 개념 이해를 주입하는 프레임워크이다. Visual Question-Answering 형식의 통합 데이터셋과 fine-tuning 전략을 통해 로봇 조작 성능을 향상시킨다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2024_ManipVQA Injecting Robotic Affordance and Physically Grounded Information into Multi-Modal Large La.pdf"
---

# ManipVQA: Injecting Robotic Affordance and Physically Grounded Information into Multi-Modal Large Language Models

> **저자**: Siyuan Huang, Iaroslav Ponomarenko, Zhengkai Jiang, Xiaoqi Li, Xiaobin Hu, Peng Gao, Hongsheng Li, Hao Dong | **날짜**: 2024-03-17 | **URL**: [https://arxiv.org/abs/2403.11289](https://arxiv.org/abs/2403.11289)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of ManipVQA: We created a comprehensive vision-language dataset by merging existing datasets and*

ManipVQA는 Multi-Modal Large Language Model (MLLM)에 로봇 조작 작업을 위한 affordance 인식과 물리적 개념 이해를 주입하는 프레임워크이다. Visual Question-Answering 형식의 통합 데이터셋과 fine-tuning 전략을 통해 로봇 조작 성능을 향상시킨다.

## Motivation

- **Known**: MLLM은 일반적인 image-text 쌍으로 학습되어 상식적 추론과 vision 작업에 뛰어나지만, 로봇 조작 작업에 필요한 affordance와 물리적 개념 이해가 부족하다. 최근 robotic affordance를 다루는 연구들이 있지만 physical information이나 affordance grounding을 충분히 고려하지 못한다.
- **Gap**: 기존 MLLM은 일반적인 이미지 캡셔닝 데이터로 학습되어 로봇 조작에 필수적인 affordance grounding과 물리적 성질 이해가 부족하다. 기존 로봇 affordance 연구들도 explicit affordance grounding이나 물리적 추론을 명시적으로 다루지 않는다.
- **Why**: 로봇 시스템에 MLLM을 통합하는 것은 자연언어 명령 이해를 향상시키지만, 조작 작업의 정확성과 범위를 제한하는 affordance와 물리적 개념의 부족은 실제 로봇 응용의 핵심 장애물이다. 이를 해결하는 것은 로봇의 실제 조작 능력을 크게 향상시킬 수 있다.
- **Approach**: 기존 HANDAL, PACO, RefCOCO, Visual Genome, PhysObjects 등의 데이터셋을 통합하고 ChatGPT로 affordance 기반 태스크를 확장하여 VQA 형식의 포괄적인 데이터셋을 구성한다. 이 데이터셋으로 SPHINX + LLaMa2 기반 MLLM을 fine-tuning하되, 원래의 vision-reasoning 능력을 보존하면서 로봇 특화 지식을 주입한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of ManipVQA: We created a comprehensive vision-language dataset by merging existing datasets and*

- **통합 VQA 데이터셋 구성**: PACO, RefCOCO, Visual Genome, HANDAL, PhysObjects 등 여러 데이터셋을 병합하고 tool detection, affordance grounding, 물리적 개념 이해를 포함하는 VQA 형식으로 통일
- **다중 작업 지원**: REC(Referring Expression Comprehension), REC-Grounding-Affordance, REG(Referring Expression Generation), REG-Physical 등 4가지 관련 작업을 통합 VQA 포맷으로 처리 가능
- **fine-tuning 전략**: 원래의 vision-reasoning 능력을 보존하면서 로봇 affordance와 물리적 지식을 효과적으로 통합하는 fine-tuning 방법 개발
- **강력한 실험 성능**: 로봇 시뮬레이터와 다양한 vision task 벤치마크에서 robust 성능 입증
- **공개 자원**: 코드와 데이터셋을 GitHub에 공개하여 연구 커뮤니티에 기여

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of ManipVQA: We created a comprehensive vision-language dataset by merging existing datasets and*

- 기존 데이터셋(PACO, RefCOCO, Visual Genome, HANDAL, PhysObjects)을 수집하고 통합
- ChatGPT를 사용하여 affordance 기반 작업에 대한 contextually rich 지시문 생성
- tool detection, affordance recognition, 물리적 개념 이해(transparency, liquid storage, seal-ability) 관련 VQA 질문-답변 쌍 구성
- SPHINX의 mixed visual encoders를 활용하여 multi-scale 이미지 처리 (저해상도 224x224 + 4개의 224x224 sub-image)
- LLaMa2 기반 언어 모델에 projection layers를 통해 visual features 정렬
- fine-tuning 시 원래의 vision-reasoning 능력 보존하면서 로봇 특화 지식 주입
- 예측된 bounding boxes와 SAM-HQ를 활용한 affordance 영역 시각화
- heuristic policy와 결합하여 복잡한 조작 작업 수행

## Originality

- 로봇 조작 지식을 MLLM에 주입하기 위해 **unified VQA format**을 활용한 혁신적 접근
- 여러 로봇 관련 데이터셋(HANDAL, PhysObjects, RGB-D Part Affordance)을 통합하여 포괄적인 **robotic manipulation-centric dataset** 구성
- affordance grounding뿐 아니라 물리적 성질 이해(transparency, liquid storage capacity, seal-ability)를 명시적으로 포함한 첫 시도
- 원래의 MLLM 능력을 보존하면서 robotic knowledge를 주입하는 **targeted fine-tuning strategy** 제안
- tool detection (REC), affordance grounding (REC-Grounding-Affordance), affordance localization (REG), 물리적 성질 예측 (REG-Physical) 등 **다양한 로봇 관련 작업을 단일 VQA 형식으로 통합**

## Limitation & Further Study

- 데이터셋이 주로 kitchen tools, workshop tools, garden tools에 집중되어 있어 다른 도메인의 affordance에 대한 일반화 가능성 제한
- 물리적 개념이 transparency, liquid storage, seal-ability 3가지로 제한되어 있으며 더 광범위한 물리적 성질 이해 미흡
- bounding box 기반 affordance grounding은 복잡한 형태의 물체나 multiple contact points를 가진 affordance 표현에 제한
- 로봇 시뮬레이터에서의 평가가 주이며 실제 physical robot에서의 성능 검증 부족
- affordance 다양성(grasp, push, place 등)이 구체적으로 어떻게 처리되는지 명확하지 않음
- 후속 연구로 더 다양한 도메인의 객체와 affordance를 포함한 데이터셋 확장, 3D affordance representation 개발, 실제 로봇 플랫폼에서의 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ManipVQA는 MLLM을 로봇 조작 작업에 적응시키기 위한 포괄적이고 창의적인 접근법을 제시하며, unified VQA format과 통합된 robotic dataset을 통해 affordance 이해와 물리적 추론 능력을 효과적으로 주입한다. 코드와 데이터셋 공개를 통해 연구 커뮤니티에 의미 있는 기여를 하지만, 실제 로봇에서의 검증과 더 광범위한 도메인으로의 확장이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level/review]] — 로봇 조작을 위한 VLM 평가에서 affordance 주입 vs 벤치마킹의 다른 관점
- 🔗 후속 연구: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — ManipVQA의 affordance 개념을 도구 사용까지 확장한 unified representation
- 🏛 기반 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — 공간적 affordance 예측의 기본 개념을 VQA 형태로 발전시킨 기초
- 🔗 후속 연구: [[papers/1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level/review]] — ManipBench의 저수준 조작 추론 평가가 ManipVQA의 물리적 근거가 있는 어포던스 이해와 결합되어 포괄적 조작 능력 평가를 제공한다.
- 🔄 다른 접근: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — ManipVQA는 VLM을 활용한 로봇 조작에서 affordance와 물리적 grounding을 다루는 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — ManipVQA의 로봇 affordance와 물리적 그라운딩 연구가 RoboPoint의 공간적 affordance 예측 방법론의 이론적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1301_A3VLM_Actionable_Articulation-Aware_Vision_Language_Model/review]] — 둘 다 robotic affordance를 다루지만 ManipVQA는 질의응답 형태로, A3VLM은 관절 구조 인식으로 접근합니다.
- 🔗 후속 연구: [[papers/1333_CLIPort_What_and_Where_Pathways_for_Robotic_Manipulation/review]] — CLIPort의 what-where 분리 개념이 ManipVQA의 robotic affordance 이해를 위한 아키텍처적 기반이 됩니다.
- 🔗 후속 연구: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — ManipVQA의 robotic affordance injection이 EmbSpatial-Bench에서 embodied spatial understanding으로 확장되어 더 포괄적인 공간 이해 평가를 다룬다.
