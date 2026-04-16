---
title: "1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo"
authors:
  - "Mengfei Du"
  - "Binhao Wu"
  - "Zejun Li"
  - "Xuanjing Huang"
  - "Zhongyu Wei"
date: "2024.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Large Vision-Language Model(LVLM)들의 구현화된 환경에서의 공간 이해 능력을 평가하기 위해 egocentric 관점의 6가지 공간 관계를 포함하는 EmbSpatial-Bench 벤치마크를 구축하고, 이를 개선하기 위한 instruction-tuning 데이터셋 EmbSpatial-SFT를 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Du et al._2024_EmbSpatial-Bench Benchmarking Spatial Understanding for Embodied Tasks with Large Vision-Language M.pdf"
---

# EmbSpatial-Bench: Benchmarking Spatial Understanding for Embodied Tasks with Large Vision-Language Models

> **저자**: Mengfei Du, Binhao Wu, Zejun Li, Xuanjing Huang, Zhongyu Wei | **날짜**: 2024-06-09 | **URL**: [https://arxiv.org/abs/2406.05756](https://arxiv.org/abs/2406.05756)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Comparison between EmbSpatial-Bench and*

Large Vision-Language Model(LVLM)들의 구현화된 환경에서의 공간 이해 능력을 평가하기 위해 egocentric 관점의 6가지 공간 관계를 포함하는 EmbSpatial-Bench 벤치마크를 구축하고, 이를 개선하기 위한 instruction-tuning 데이터셋 EmbSpatial-SFT를 제시한다.

## Motivation

- **Known**: LVLM은 instruction following과 visual reasoning 능력으로 embodied AI 시스템 개발에 유망한 방향을 제시하고 있다. 하지만 기존 spatial understanding 벤치마크들은 주로 universal image dataset(COCO, VG)으로부터 구축되며 subject-centric 관점에서 공간 관계를 정의한다.
- **Gap**: LVLM의 embodied 환경에서의 공간 이해 능력에 대한 체계적 평가가 부재하며, 특히 egocentric 관점의 공간 이해 능력 평가 벤치마크가 없다.
- **Why**: embodied agent는 자신을 중심으로 한 egocentric 좌표계에서 instruction을 이해하고 행동을 결정해야 하므로, 이러한 관점에서의 공간 이해 능력 평가는 LVLM 기반 embodied agent 개발에 필수적이다.
- **Approach**: MP3D, AI2-THOR, ScanNet의 annotated 3D 환경으로부터 자동으로 벤치마크를 구축하고, 3D 좌표를 활용하여 egocentric 관점의 공간 관계(above, below, left, right, close, far)를 추출한다. 추가로 instruction-tuning 데이터셋을 구성하여 LVLM의 spatial understanding 능력을 개선한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of the construction pipeline for EmbSpatial-Bench based on existing annotated 3D environments.*

- **EmbSpatial-Bench 구축**: 3,640개의 QA pair, 294개 object category, 277개 scene을 포함하는 embodied spatial understanding 벤치마크 자동 구축
- **포괄적 평가**: 6가지 공간 관계에 대한 다양한 LVLM(BLIP2, InstructBLIP, GPT-4V, Qwen-VL-Max 등) 평가로 현재 LVLM의 부족한 공간 이해 능력 노출(최고 성능 49.11% vs 인간 90.33%)
- **개선 데이터셋**: spatial relationship identification과 object localization 두 가지 auxiliary task를 포함하는 EmbSpatial-SFT instruction-tuning 데이터셋 제시로 LVLM의 embodied spatial understanding 능력 개선 달성

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of the construction pipeline for EmbSpatial-Bench based on existing annotated 3D environments.*

- 3D 환경(MP3D, AI2-THOR, ScanNet)으로부터 random viewpoint에서 RGB-D 이미지 수집
- camera parameter와 3D 좌표를 활용하여 2D bounding box 획득 및 egocentric 관점의 공간 관계 자동 추출(horizontal: left/right, vertical: above/below, depth: close/far)
- 5가지 question template으로 multiple-choice QA pair 생성 및 filtering(bounding box 크기 제약, relation balance) 및 human verification 수행
- spatial relation identification task(25K samples)와 object localization auxiliary task로 구성된 instruction-tuning 데이터셋 EmbSpatial-SFT 구성
- zero-shot 평가로 현재 LVLM의 공간 이해 능력 벤치마킹 및 fine-tuning 후 성능 개선도 측정

## Originality

- **Egocentric 관점 도입**: 기존 벤치마크의 subject-centric 관점에서 벗어나 embodied agent의 관점을 반영한 egocentric spatial relationship 정의 및 평가
- **embodied 3D 환경 기반 구축**: universal 2D image dataset 대신 MP3D, AI2-THOR, ScanNet 등 embodied scenario와 일치하는 3D 환경으로부터 자동 구축
- **6차원 공간 관계 통합**: x(left/right), y(above/below), z(close/far) 축을 모두 포괄하는 6가지 공간 관계를 systematic하게 정의 및 평가
- **보조 task를 통한 개선**: object localization auxiliary task가 spatial relationship identification의 foundation skill임을 인식하고 두 task를 결합한 instruction-tuning 방식 제시

## Limitation & Further Study

- 벤치마크가 indoor scene 위주(COCO, VG 데이터와 유사한 한계)로 outdoor embodied scenario에 대한 평가 부재
- 6가지 기본 공간 관계만 평가하며 'between
- inside
- occluded' 등 더 복잡한 공간 관계 미포함", 'multiple-choice question 형식으로만 평가하여 generation-based spatial reasoning 능력 평가 미흡
- 현재 LVLM의 낮은 성능(최고 49.11%)이 모델의 공간 이해 부재인지 instruction following 부정확성인지 구분이 불명확
- 후속 연구로 outdoor embodied scenario 포함, 더 복잡한 공간 관계 추가, generation-based evaluation 도입, 그리고 embodied action과의 연관성을 직접 검증하는 downstream task 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 embodied AI의 핵심 능력인 spatial understanding을 체계적으로 평가하기 위해 egocentric 관점의 벤치마크를 처음으로 제시하며, 3D 환경 기반의 자동 구축 파이프라인과 개선 데이터셋을 통해 현재 LVLM의 명확한 부족함을 드러내고 개선 방향을 제시한다는 점에서 embodied AI 커뮤니티에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — Multimodal Spatial Language Maps의 공간 이해 방법론이 EmbSpatial-Bench의 egocentric 공간 관계 평가 설계의 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — TopV-Nav의 top-view spatial reasoning이 EmbSpatial-Bench의 egocentric 관점을 다른 시각적 관점으로 확장합니다.
- 🧪 응용 사례: [[papers/1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang/review]] — SpatialVLA는 EmbSpatial-Bench에서 평가하는 공간 이해 능력을 VLA 모델에 직접 통합하는 구체적인 적용 사례입니다.
- 🏛 기반 연구: [[papers/1611_Visual_Instruction_Tuning/review]] — Visual Instruction Tuning의 기본적인 vision-language instruction following이 EmbSpatial-Bench의 spatial understanding evaluation을 위한 기초 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde/review]] — ManipVQA의 robotic affordance injection이 EmbSpatial-Bench에서 embodied spatial understanding으로 확장되어 더 포괄적인 공간 이해 평가를 다룬다.
- 🔄 다른 접근: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — Prismatic VLMs의 general visually-grounded language와 EmbSpatial-Bench의 embodied spatial understanding은 VLM 평가에서 서로 다른 특화 영역을 다룬다.
- 🔄 다른 접근: [[papers/1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason/review]] — embodied AI의 공간 추론 능력을 physical common sense 관점에서 평가하는 다른 접근법입니다.
- 🧪 응용 사례: [[papers/1382_EmbodiedVSR_Dynamic_Scene_Graph-Guided_Chain-of-Thought_Reas/review]] — EmbSpatial-Bench에서 평가할 수 있는 embodied spatial reasoning 기법을 실제 구현한 사례이다.
- 🏛 기반 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — OctoNav의 spatial understanding 능력을 평가하기 위한 embodied navigation benchmark와 평가 방법론을 제공한다.
- 🧪 응용 사례: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — EmbSpatial-Bench가 TopV-Nav의 top-view spatial reasoning 성능을 embodied AI 관점에서 체계적으로 평가할 수 있는 벤치마크를 제공한다.
- 🏛 기반 연구: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — embodied AI의 spatial understanding 벤치마킹 방법론을 제공하여 VLABench의 로봇 조작 평가에 이론적 기반을 제공합니다.
