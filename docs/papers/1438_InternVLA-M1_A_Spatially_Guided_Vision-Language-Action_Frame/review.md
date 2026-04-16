---
title: "1438_InternVLA-M1_A_Spatially_Guided_Vision-Language-Action_Frame"
authors:
  - "Xinyi Chen"
  - "Yilun Chen"
  - "Yanwei Fu"
  - "Ning Gao"
  - "Jiaya Jia"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "InternVLA-M1은 공간 그라운딩을 시각-언어-행동 학습의 중심 연결고리로 활용하여, 지시 따르기 로봇의 확장 가능한 일반 지능을 구현한 통합 프레임워크이다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2025_InternVLA-M1 A Spatially Guided Vision-Language-Action Framework for Generalist Robot Policy.pdf"
---

# InternVLA-M1: A Spatially Guided Vision-Language-Action Framework for Generalist Robot Policy

> **저자**: Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, Yang Tian, Bin Wang, Bolun Wang, Fangjing Wang, Hanqing Wang, Tai Wang, Ziqin Wang, Xueyuan Wei, Chao Wu, Shuai Yang, Jinhui Ye, Junqiu Yu, Jia Zeng, Jingjing Zhang, Jinyu Zhang, Shi Zhang, Feng Zheng, Bowen Zhou, Yangkun Zhu | **날짜**: 2025-10-15 | **URL**: [https://arxiv.org/abs/2510.13778](https://arxiv.org/abs/2510.13778)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. InternVLA-M1 integrates spatial grounding into the vision–language–action training pipeline.*

InternVLA-M1은 공간 그라운딩을 시각-언어-행동 학습의 중심 연결고리로 활용하여, 지시 따르기 로봇의 확장 가능한 일반 지능을 구현한 통합 프레임워크이다.

## Motivation

- **Known**: 대규모 multimodal foundation model은 웹 규모의 vision-language 정렬을 통해 강력한 일반화를 보이며, 최근 data-driven VLA 모델들이 teleoperated 데이터셋을 활용한 로봇 제어를 학습하고 있다.
- **Gap**: 기존 VLA 모델들은 고급 언어 이해에 비해 절대/상대 위치 정보를 포함한 공간 추론을 충분히 반영하지 못하며, 계층적 로봇 시스템은 규칙 기반 분해로 인해 자동 확장이 어렵다는 한계가 있다.
- **Why**: 실세계 로봇 행동은 추상적 지시와 구체적 3D 공간에서의 실행 사이의 간극을 bridging하는 embodiment-agnostic 공간 prior가 필요하며, 이러한 이분 설계는 다양한 로봇 플랫폼 간 전이 학습을 가능하게 한다.
- **Approach**: InternVLA-M1은 2.3M 공간 추론 데이터로 '어디서' 행동할지 결정하는 VLM planner와 plug-and-play spatial prompting으로 '어떻게' 행동할지 결정하는 action expert를 이중 감독(dual-supervision) 방식으로 학습한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of InternVLA-M1. InternVLA-M1 adopts a spatially guided two-stage training*

- **SimplerEnv 벤치마크**: Google Robot에서 +14.6%, WidowX에서 +17%의 성공률 향상을 달성하며 box, point, trace 예측에서 강력한 공간 추론 능력 입증
- **Pick-and-Place 확장성**: 244K 합성 에피소드로 200개 작업과 3000+ 객체 대상 6.2% 평균 성능 향상
- **실세계 성능**: 클러스터된 환경에서 7.3% 개선, 합성 co-training으로 미보는 객체/설정에서 +20.6% 달성
- **장기 추론**: reasoning-intensive 시나리오에서 기존 방법(GR00T, π₀) 대비 10% 이상 우월

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of InternVLA-M1. InternVLA-M1 adopts a spatially guided two-stage training*

- Qwen2.5-VL-3B-instruct를 multimodal encoder로 활용하여 공간 prior를 학습하는 VLM planner 구성
- Diffusion Policy 기반 action expert(DINOv2 + state encoder)로 embodiment-specific 제어 신호 생성
- Stage 1: 2.3M multimodal 데이터(web, 실제, 시뮬레이션)로 공간 그라운딩 pre-training 수행
- Stage 2: spatial prompting을 통해 학습된 공간 prior를 로봇 행동에 조건화하여 action post-training 진행
- Dual-supervision으로 인지와 제어를 co-adapt하여 각각 독립 학습하지 않도록 설계
- 시뮬레이션 엔진으로 244K generalized pick-and-place 에피소드 생성하여 학습 데이터 확장

## Originality

- 공간 그라운딩(boxes, points, traces)을 중간 표현으로 활용하여 language 이해와 motor control 간 명시적 연결고리 제공하는 이분 시스템 설계의 참신성
- Embodiment-agnostic spatial prior를 다양한 로봇 플랫폼 간 전이 학습의 기초로 정립하고, embodiment-specific 제어는 downstream adaptation에 위임하는 설계 철학의 혁신성
- Web-scale multimodal data와 로봇 데이터를 통합하는 3M+ 규모의 hybrid pre-training 데이터셋 구성 및 시뮬레이션 기반 합성 데이터 생성 pipeline의 체계성
- Spatial prompting을 plug-and-play 메커니즘으로 구현하여 VLM planner의 공간 추론 능력을 action expert로 효과적 전달하는 방법론

## Limitation & Further Study

- 현재 tabletop pick-and-place 작업 중심으로 평가되었으며, 더 복잡한 조작, humanoid 운동학, mobile navigation 등 다양한 embodiment으로의 확장 검증 필요
- 4.1B 파라미터 모델로 단일 RTX 4090에서 약 12GB 메모리 요구하며, 모바일/edge 로봇 배포 시 경량화 및 압축 방안 미제시
- Spatial grounding pre-training의 2.3M 데이터 중 web 비율과 로봇 데이터 비율, 합성 데이터 품질에 대한 상세 분석 부족
- 실세계 실험이 60+ 객체로 제한적이며, 더 큰 규모의 오브젝트 다양성 및 환경 편차에 대한 robust성 검증 필요
- VLM planner와 action expert 간 정보 흐름 최적화, spatial prompt 설계의 자동화, multi-agent 시나리오로의 확장 등 향후 연구 방향 제시 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: InternVLA-M1은 공간 그라운딩을 중추로 하는 이중 시스템 설계로 instruction-following과 embodied control 간 명확한 인터페이스를 제시하며, 광범위한 벤치마크에서 일관된 성능 향상과 확장성을 입증한 매우 견고한 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1399_From_Seeing_to_Doing_Bridging_Reasoning_and_Decision_for_Rob/review]] — 둘 다 공간 기반 VLA이지만 InternVLA-M1은 공간 그라운딩에, FSD는 visual aids 생성에 집중한다.
- 🔗 후속 연구: [[papers/1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang/review]] — 공간 표현을 VLA에 통합하는 InternVLA-M1의 접근법을 spatial representation으로 더 일반화했다.
- 🏛 기반 연구: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — 통합된 이해-생성-행동 모델의 기본 구조가 InternVLA-M1의 공간 그라운딩 프레임워크에 기반이 된다.
- 🔗 후속 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 기본 구조에 공간 그라운딩을 핵심으로 한 확장 가능한 일반 지능 프레임워크를 구축한다.
- 🏛 기반 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — RoboPoint의 spatial affordance prediction을 vision-language-action 학습의 중심 연결고리로 확장한다.
- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — grounding 기능을 통한 공간적 이해의 기본 원리를 VLA 프레임워크에 적용하는 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — multimodal spatial language maps를 VLA의 공간 그라운딩 메커니즘과 결합하여 더 정확한 공간 추론을 달성할 수 있다.
- 🔄 다른 접근: [[papers/1399_From_Seeing_to_Doing_Bridging_Reasoning_and_Decision_for_Rob/review]] — 둘 다 공간 추론을 통한 VLA 모델이지만 FSD는 visual aids 생성에, InternVLA-M1은 공간 그라운딩에 집중한다.
