---
title: "1456_LERF_Language_Embedded_Radiance_Fields"
authors:
  - "Justin Kerr"
  - "Chung Min Kim"
  - "Ken Goldberg"
  - "Angjoo Kanazawa"
  - "Matthew Tancik"
date: "2023.03"
doi: ""
arxiv: ""
score: 4.0
essence: "LERF는 CLIP 임베딩을 NeRF에 정합하여 자연어로 3D 장면을 쿼리할 수 있도록 하는 방법이다. 다중 스케일 언어 필드를 학습함으로써 시각적 속성, 의미론, 추상적 개념, 장기 꼬리 객체 등 다양한 형태의 자연어 질의에 실시간으로 응답한다."
tags:
  - "cat/Visual_Language_Navigation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Visual_Language_Mapping"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kerr et al._2023_LERF Language Embedded Radiance Fields.pdf"
---

# LERF: Language Embedded Radiance Fields

> **저자**: Justin Kerr, Chung Min Kim, Ken Goldberg, Angjoo Kanazawa, Matthew Tancik | **날짜**: 2023-03-16 | **URL**: [https://arxiv.org/abs/2303.09553](https://arxiv.org/abs/2303.09553)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Language Embedded Radiance Fields (LERF). LERF grounds CLIP representations in a dense, multi-scale 3D ﬁeld. A*

LERF는 CLIP 임베딩을 NeRF에 정합하여 자연어로 3D 장면을 쿼리할 수 있도록 하는 방법이다. 다중 스케일 언어 필드를 학습함으로써 시각적 속성, 의미론, 추상적 개념, 장기 꼬리 객체 등 다양한 형태의 자연어 질의에 실시간으로 응답한다.

## Motivation

- **Known**: NeRF는 사실적인 3D 장면 재구성에 효과적이지만 의미 정보가 부족하며, CLIP은 강력한 시각-언어 모델이지만 2D에만 적용된다. 기존 2D 오픈 어휘 감지 방법은 마스크 제안이나 세분화 데이터셋을 필요로 한다.
- **Gap**: 3D 장면에서 마스크나 지역 제안 없이 직접적으로 CLIP 임베딩을 밀집하게 정합하는 방법이 부재했으며, 다중 스케일 계층적 언어 쿼리를 지원하는 3D 언어 필드가 없었다.
- **Why**: 자연어는 3D 장면과 상호작용하는 직관적인 인터페이스이며, 이는 로봇공학, 시각-언어 모델 이해, 3D 장면 상호작용 등 다양한 응용 분야에서 실용적 가치가 크다.
- **Approach**: NeRF 최적화 과정에서 위치와 물리적 스케일을 입력으로 하는 언어 필드를 함께 학습하며, 다중 스케일 특성 피라미드를 통해 다양한 스케일의 CLIP 임베딩을 감독한다. DINO 특성으로 정규화하여 최적화된 언어 필드의 매끄러움을 보장한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Results with LERF for 5 in-the-wild scenes. Each image shows a visual rendering of the LERF (Sec. 3), along wi*

- **제로샷 다중 스케일 쿼리**: 마스크나 지역 제안 없이 픽셀 정렬 방식으로 시각적 속성, 추상 개념, 장기 꼬리 객체, 텍스트 등 광범위한 자연어 쿼리를 지원
- **3D 일관성**: 다중 뷰의 CLIP 임베딩을 평균화하여 2D CLIP보다 더 국소화되고 3D 일관성 있는 관련성 맵 생성
- **효율적 최적화**: 기본 NeRF 구현을 크게 지연시키지 않으면서 훈련 가능하며, 최적화 후 실시간 쿼리 응답 제공
- **넓은 적용성**: 로봇공학, 시각-언어 모델 분석, 3D 장면 상호작용 등 다양한 응용 분야에 활용 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2: LERF Optimization: Left: LERF represents a ﬁeld of 3D volumes, parameterized by position x, y, z and scale s (*

- NeRF의 부피 렌더링 프레임워크를 확장하여 위치(x, y, z)와 스케일(s)을 입력으로 하는 언어 필드 네트워크 학습
- 훈련 뷰의 이미지 패치에서 다중 스케일 CLIP 특성 피라미드 사전 계산
- 훈련 중 사영 기하학으로 물리적 스케일을 이미지 스케일에 매핑하여 다중 스케일 감독 신호 생성
- CLIP 코사인 유사성 손실과 DINO 특성 정규화를 결합하여 최적화
- 테스트 시간에 언어 필드를 임의의 스케일에서 쿼리하여 3D 관련성 맵 추출

## Originality

- NeRF에 CLIP 임베딩을 직접 정합하되 마스크나 지역 제안을 필요로 하지 않는 새로운 접근
- 다중 스케일 특성 피라미드를 통해 동일 3D 위치에서 서로 다른 스케일의 언어 의미를 학습하는 독창적 방법
- 사영 기하학을 이용한 물리적 스케일과 이미지 스케일의 매핑으로 밀집 언어 필드 생성
- DINO 특성을 공유 병목으로 통합하여 언어 필드의 기하학적 일관성 강화

## Limitation & Further Study

- 다중 뷰 일관성을 보장하기 위해 여러 훈련 뷰가 필요하므로 데이터 요구량이 높을 수 있음
- CLIP의 한계를 상속받아 특정 시각적 세부사항이나 극단적 스케일에서 표현 능력 제한 가능
- 손잡이 기반 캡처 데이터로만 평가하였으므로 대규모 실내외 장면에서의 확장성 미정
- 정량적 평가가 LSeg 3D 증류 및 OWL-ViT 렌더링 쿼리에 제한되어 더 광범위한 벤치마크 필요
- 후속 연구: 더 효율적인 데이터 수집 방법, 동적 장면 지원, 실시간 증분 학습, 다국어 쿼리 지원

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LERF는 NeRF와 CLIP을 창의적으로 결합하여 3D 장면의 밀집 자연어 쿼리를 실현한 우수한 논문이다. 다중 스케일 언어 필드, 마스크 비의존 설계, 실시간 성능은 실용적 가치가 크며, 로봇공학 및 3D UI 분야에서 즉각적인 영향을 미칠 수 있다.

## Related Papers

- 🔗 후속 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — LERF의 언어-3D 매핑 개념을 로봇 네비게이션과 조작에 직접 적용한 확장 연구
- 🔄 다른 접근: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — 동일한 언어-공간 매핑 문제를 다른 접근법으로 해결한 대안적 방법
- 🏛 기반 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — CLIP 기반 3D 장면 이해의 기초가 되는 weakly supervised semantic field 방법론
- 🏛 기반 연구: [[papers/1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering/review]] — LERF의 언어 임베딩 방법론이 3D Gaussian Splatting의 실시간 렌더링과 결합되어 더 효율적인 3D 언어 필드를 구현할 수 있습니다.
- 🏛 기반 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — LERF의 언어 임베딩 3D 필드 기법이 VLMaps의 공간-언어 매핑 구현의 핵심 기술적 기초가 된다.
- 🔗 후속 연구: [[papers/1600_UniGoal_Towards_Universal_Zero-shot_Goal-oriented_Navigation/review]] — LERF의 language embedded radiance fields가 UniGoal의 통합된 graph 표현을 3D 공간에서 더욱 풍부하게 확장할 수 있다.
- 🔄 다른 접근: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — LERF는 VLMaps와 유사하게 언어를 3D 공간에 embedding하지만 radiance field 기반의 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — LERF의 언어 임베딩 radiance field 개념을 로봇 메모리 시스템으로 확장한 실용적 응용입니다.
- 🏛 기반 연구: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — 언어 임베디드 방사장 LERF가 OVSG의 자유형식 텍스트 쿼리 처리에 기반을 제공합니다.
