---
title: "1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma"
authors:
  - "Chenguang Huang"
  - "Oier Mees"
  - "Andy Zeng"
  - "Wolfram Burgard"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇 네비게이션과 조작을 위해 pretrained multimodal foundation model의 특징을 3D 환경 재구성과 융합한 spatial language map (VLMaps, AVLMaps)을 제안한다. 이를 통해 자연어, 이미지, 오디오 등 다중모달 쿼리를 공간상의 목표 위치로 그라운딩할 수 있다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Visual_Language_Navigation"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2025_Multimodal Spatial Language Maps for Robot Navigation and Manipulation.pdf"
---

# Multimodal Spatial Language Maps for Robot Navigation and Manipulation

> **저자**: Chenguang Huang, Oier Mees, Andy Zeng, Wolfram Burgard | **날짜**: 2025-06-07 | **URL**: [https://arxiv.org/abs/2506.06862](https://arxiv.org/abs/2506.06862)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. AVLMaps provide an open-vocabulary 3D map*

로봇 네비게이션과 조작을 위해 pretrained multimodal foundation model의 특징을 3D 환경 재구성과 융합한 spatial language map (VLMaps, AVLMaps)을 제안한다. 이를 통해 자연어, 이미지, 오디오 등 다중모달 쿼리를 공간상의 목표 위치로 그라운딩할 수 있다.

## Motivation

- **Known**: Vision-language models (VLMs)는 pretrained multimodal foundation models을 활용하여 로봇의 시각 관찰을 객체 설명에 매칭할 수 있다. 하지만 기존 방법들은 환경 매핑과 단절되어 있거나 공간적 정확도가 부족하며 비전 정보만 사용한다.
- **Gap**: 기존 언어-기반 로봇 네비게이션 방법들은 'sofa와 TV 사이'와 같은 공간적 관계 표현을 지역화할 수 없고, 다양한 로봇 플랫폼에서 재사용 불가능하며, 오디오 같은 추가 모달리티를 활용하지 못한다.
- **Why**: 로봇이 복잡한 자연언어 지시를 따르고 다양한 센서 입력을 활용하여 모호한 환경에서 목표를 정확히 식별할 수 있도록 하는 것은 실제 로봇 응용에 필수적이다.
- **Approach**: Pretrained multimodal foundation models (vision-language 및 audio-language models)의 특징을 3D voxelized map에 밀집적으로 융합하여 공간-의미론적 표현을 구축한다. VLMaps은 시각-언어 특징을, AVLMaps은 여기에 오디오 정보를 추가로 통합한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. AVLMaps provide an open-vocabulary 3D map*

- **VLMaps 개발**: Pretrained multimodal features를 3D 환경 재구성과 융합하여 'sofa와 TV 사이'같은 공간 관계를 직접 지역화 가능", '**다양한 로봇 플랫폼 지원**: 동일 voxelized map에서 서로 다른 로봇 형태를 위한 맞춤형 obstacle map을 생성 가능
- **AVLMaps 확장**: 오디오, 시각, 언어 정보를 통합한 통일된 3D 공간 표현으로 멀티모달 목표 쿼리 지원
- **성능 향상**: 모호한 시나리오에서 top-1 recall이 기존 방법 대비 50% 향상, zero-shot 다중모달 목표 네비게이션 달성
- **다양한 로봇 작업 지원**: Mobile robots과 tabletop manipulators 모두에서 네비게이션 및 조작 작업 수행 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2. The creation and language-conditioned indexing of a VLMap. A VLMap is created by fusing pretrained visual-lang*

- 표준 exploration 알고리즘을 사용하여 로봇의 비디오 스트림과 오디오 녹음으로부터 multimodal spatial language map 자동 구축
- Pretrained multimodal foundation models (CLIP, AudioCLIP, CLAP 등)에서 밀집 특징을 계산하고 3D voxel grid에 융합
- Large Language Models (LLMs)와 Socratic 방식으로 조합하여 자연언어 명령을 공간적으로 그라운딩된 목표 시퀀스로 변환
- 다중모달 쿼리(텍스트, 이미지, 오디오 스니펫)를 voxel grid에서 공간 위치로 매칭하여 목표 지역화
- 오디오, 시각, 의미론적 정보를 활용하여 모호한 환경에서 다양한 가능한 목표 위치 중 올바른 위치 식별

## Originality

- Semantic mapping과 multimodal foundation models을 처음으로 3D spatial representation에 통합하여 공간적 정밀도와 개방형 어휘 이해 동시 달성
- Audio modality를 로봇 네비게이션 맵에 처음으로 체계적으로 도입하여 공간적 다중모달 쿼리 지원
- 단일 map representation이 여러 로봇 embodiments에서 재사용 가능한 설계로 멀티모달 spatial reasoning을 유연하게 확장
- Multimodal ambiguity resolution을 spatial context를 활용하여 해결하는 혁신적 접근법

## Limitation & Further Study

- Pretrained multimodal foundation models의 성능에 크게 의존하므로, 모델 성능 향상에 따라 시스템 성능이 제한됨
- 3D reconstruction quality에 의존하여 poorly reconstructed areas에서 기능 저하 가능
- 계산 비용이 모든 voxel에서 multimodal features를 계산해야 하므로 메모리 및 처리 시간 증가
- Real-world 설정에서의 제한된 평가 - 더 다양한 환경과 시나리오에서의 강건성 검증 필요
- 오디오 정보는 실내 환경에서만 수집 가능하고, 배경 음향 잡음에 대한 robustness 개선 필요
- 향후 다른 센서 모달리티(LiDAR, thermal imaging 등) 통합 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 multimodal foundation models을 3D spatial map에 창의적으로 통합하여 기존 방법의 공간 정밀도와 멀티모달 이해 한계를 동시에 해결한 의미 있는 기여다. Audio modality의 도입과 다양한 로봇 플랫폼 지원으로 실용적 확장성이 우수하며, 50% 성능 향상 등 정량적 결과도 강력하다.

## Related Papers

- 🔗 후속 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — Visual Language Maps를 확장하여 오디오 모달리티까지 포함한 AVLMaps로 다중모달 spatial grounding을 실현했다.
- 🏛 기반 연구: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — LERF의 언어 임베딩 3D 필드 기법이 VLMaps의 공간-언어 매핑 구현의 핵심 기술적 기초가 된다.
- 🔗 후속 연구: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — open-vocabulary 3D scene grounding을 multimodal spatial mapping으로 발전시킨 확장
- 🧪 응용 사례: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — spatial language map의 개념을 composable 3D value maps로 실제 조작에 적용
- 🔗 후속 연구: [[papers/1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang/review]] — Multimodal Spatial Language Maps의 공간 표현 방법론이 SpatialVLA의 시각-언어-행동 모델에서 더 정교한 공간적 이해로 확장됩니다.
- 🔗 후속 연구: [[papers/1401_GauDP_Reinventing_Multi-Agent_Collaboration_through_Gaussian/review]] — Multimodal Spatial Language Maps의 공간 표현이 GauDP에서 3D Gaussian field를 통한 다중 에이전트 공간 협업으로 더욱 발전한 형태이다.
- 🔗 후속 연구: [[papers/1438_InternVLA-M1_A_Spatially_Guided_Vision-Language-Action_Frame/review]] — multimodal spatial language maps를 VLA의 공간 그라운딩 메커니즘과 결합하여 더 정확한 공간 추론을 달성할 수 있다.
- 🏛 기반 연구: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — Multimodal Spatial Language Maps의 spatial-semantic 분리 개념을 dual implicit neural memory로 구체화했다.
- 🔗 후속 연구: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — LERF의 언어-3D 매핑 개념을 로봇 네비게이션과 조작에 직접 적용한 확장 연구
- 🔗 후속 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — visual language map을 multimodal spatial language map으로 확장한 발전된 연구입니다.
- 🏛 기반 연구: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — Multimodal Spatial Language Maps의 공간 이해 방법론이 EmbSpatial-Bench의 egocentric 공간 관계 평가 설계의 기반을 제공합니다.
