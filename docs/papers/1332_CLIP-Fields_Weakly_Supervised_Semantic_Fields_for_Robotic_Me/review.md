---
title: "1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me"
authors:
  - "Nur Muhammad Mahi Shafiullah"
  - "Chris Paxton"
  - "Lerrel Pinto"
  - "Soumith Chintala"
  - "Arthur Szlam"
date: "2022.10"
doi: ""
arxiv: ""
score: 4.0
essence: "CLIP-Fields는 공간 좌표를 CLIP, Detic, Sentence-BERT 등 웹 사전학습 모델의 의미론적 임베딩으로 매핑하는 암묵적 신경 필드로, 직접 인간 감독 없이 로봇의 3D 의미론적 메모리로 작동한다."
tags:
  - "cat/Visual_Language_Navigation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Open-Vocabulary_Scene_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shafiullah et al._2022_CLIP-Fields Weakly Supervised Semantic Fields for Robotic Memory.pdf"
---

# CLIP-Fields: Weakly Supervised Semantic Fields for Robotic Memory

> **저자**: Nur Muhammad Mahi Shafiullah, Chris Paxton, Lerrel Pinto, Soumith Chintala, Arthur Szlam | **날짜**: 2022-10-11 | **URL**: [https://arxiv.org/abs/2210.05663](https://arxiv.org/abs/2210.05663)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our approach, CLIP-Fields, integrates multiple views of a*

CLIP-Fields는 공간 좌표를 CLIP, Detic, Sentence-BERT 등 웹 사전학습 모델의 의미론적 임베딩으로 매핑하는 암묵적 신경 필드로, 직접 인간 감독 없이 로봇의 3D 의미론적 메모리로 작동한다.

## Motivation

- **Known**: Neural Radiance Fields (NeRF)와 같은 신경 암묵적 표현이 3D 장면 모델링에 효과적이며, CLIP 같은 비전-언어 모델이 2D 이미지에서 강력한 의미론적 추상화를 학습할 수 있다는 것이 알려져 있다.
- **Gap**: 기존 비전-언어 모델은 단일 2D 이미지 입력 기반이어서 3D 공간 추론과의 통합이 제한적이며, 로봇용 공간 의미론적 메모리는 고정 클래스 목록에 의존하거나 인간 주석이 필요한 한계가 있다.
- **Why**: 로봇이 인간 환경에서 복잡한 작업을 수행하려면 유연한 공간 의미론적 메모리가 필수적이며, 약한 감독으로 구축 가능한 열린 어휘 3D 표현은 실제 로봇 응용에 매우 중요하다.
- **Approach**: RGB-D 데이터에서 공간 위치 (x, y, z)를 의미론적 임베딩 벡터로 매핑하는 신경 필드를 대비 손실로 학습하되, 웹 사전학습 모델로부터의 약한 감독을 활용하여 직접 인간 주석을 완전히 제거한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Mean average precision in instance segmentation on the*

- **개방 어휘 기반 3D 의미론적 메모리**: 고정된 클래스 목록 없이 임의의 의미론적 쿼리에 응답 가능한 3D 장면 표현 제공
- **약한 감독 학습**: CLIP, Detic, Sentence-BERT 등 웹 사전학습 모델만으로 감독을 수행하며 인간 주석 완전 제거
- **소량 데이터 효율성**: HM3D 데이터셋에서 Mask-RCNN 대비 훨씬 적은 예시로 인스턴스 식별 및 의미론적 분할 성능 우수
- **실제 로봇 응용**: 의미론적 네비게이션, 인스턴스 분할, 뷰 지역화, 자연언어 기반 객체 위치 파악 등 다양한 작업 수행

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Dataset creation process for CLIP-Fields by processing*

- RGB-D 입력으로부터 다중 뷰 이미지 수집 및 Detic을 이용한 객체 영역 추출
- 각 이미지 영역에서 CLIP 임베딩 추출 및 Sentence-BERT로 자연언어 쿼리 임베딩 생성
- 좌표 기반 신경 네트워크 g(x, y, z)를 정의하여 3D 공간 위치를 의미론적 벡터로 매핑
- 대비 손실(contrastive loss)을 통해 공간 좌표에서 예측된 특징과 이미지/텍스트 임베딩 간 유사성 최대화
- 학습된 필드를 이용해 공간 쿼리, 텍스트 기반 위치 검색, 이미지-뷰 지역화 등 수행

## Originality

- NeRF 기반 암묵적 표현과 CLIP 같은 약한 감독 모델을 직접 결합하여 3D 의미론적 메모리 구축
- 인간 주석 완전 제거하고 웹 사전학습 모델만으로 의미론적 필드 학습 가능함을 입증
- 다중 뷰 정보를 암묵적 신경 필드에 통합하여 단일 뷰 백프로젝션 방식보다 나은 의미론적 일관성 달성
- 로봇의 공간 의미론적 메모리로 활용 가능한 실용적 3D 표현 방식 제시

## Limitation & Further Study

- 사전학습 모델의 성능에 의존하므로 Detic이나 CLIP의 한계(특정 객체 인식 실패 등)를 상속받을 수 있음
- RGB-D 센서 기반으로 제한되어 있으며, 포괄적인 3D 메모리 구축을 위해 충분한 뷰가 필요함
- 실제 로봇 환경에서의 대규모 평가 부재 - 제시된 로봇 실험은 정성적 사례 수준
- 후속 연구: 다른 3D 인코딩 방식 탐색, 동적 환경에서의 업데이트 메커니즘, 더 효율적인 신경 필드 아키텍처 개발, 대규모 실제 로봇 배포 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CLIP-Fields는 웹 사전학습 모델을 활용한 약한 감독 학습으로 인간 주석을 완전히 제거하면서도 개방 어휘 기반 3D 의미론적 메모리를 구축하는 혁신적 접근법이다. 로봇 응용의 실용성과 적은 데이터로도 우수한 성능을 보여주는 점에서 매우 중요한 기여이나, 실제 로봇 환경에서의 대규모 평가 및 동적 장면 처리는 향후 과제이다.

## Related Papers

- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — Grounding DINO의 open-vocabulary grounding 능력이 CLIP-Fields의 의미론적 필드 구축에 핵심적인 기술적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — LERF의 언어 임베딩 radiance field 개념을 로봇 메모리 시스템으로 확장한 실용적 응용입니다.
- 🔗 후속 연구: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — CLIP-Fields의 의미론적 필드가 BeliefMapNav의 3D voxel belief map 구축에 기술적 토대를 제공합니다.
- 🔗 후속 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — CLIP-Fields의 의미론적 공간 매핑 개념이 Visual Language Maps의 로봇 네비게이션 응용으로 확장된 형태입니다.
- 🧪 응용 사례: [[papers/1569_Segment_Anything/review]] — Segment Anything의 segmentation 기능을 CLIP과 결합하여 로봇의 3D 공간 이해와 의미론적 메모리 구축에 활용한 실용적 응용입니다.
- 🏛 기반 연구: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — CLIP-Fields의 의미론적 필드 개념이 BeliefMapNav의 3D voxel 기반 belief map 구축의 이론적 기초를 제공합니다.
- 🔄 다른 접근: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — 로봇 조작에서 언어 기반 객체 이해를 위한 다른 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — CLIP 기반 3D 장면 이해의 기초가 되는 weakly supervised semantic field 방법론
- 🔄 다른 접근: [[papers/1505_Open-vocabulary_Queryable_Scene_Representations_for_Real_Wor/review]] — semantic field 표현에서 open-vocabulary queryable scene vs CLIP-based weakly supervised field라는 서로 다른 장면 이해 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1569_Segment_Anything/review]] — CLIP-Fields의 weakly supervised semantic field 개념을 확장하여 1B 마스크 데이터를 통한 더 강력한 범용 분할 시스템을 구축했다.
- 🏛 기반 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — CLIP-Fields의 weakly supervised semantic field가 visual language map의 기반 기술입니다.
