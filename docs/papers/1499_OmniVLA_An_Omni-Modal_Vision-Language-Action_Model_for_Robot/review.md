---
title: "1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot"
authors:
  - "Noriaki Hirose"
  - "Catherine Glossop"
  - "Dhruv Shah"
  - "Sergey Levine"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "OmniVLA는 2D 포즈, egocentric 이미지, 자연어 등 다양한 모달리티로 조건화된 목표를 처리할 수 있는 omni-modal vision-language-action 모델로, 9,500시간 이상의 다중 플랫폼 로봇 네비게이션 데이터로 학습되어 강력한 일반화 성능을 달성한다."
tags:
  - "cat/Visual_Language_Navigation"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Visual_Language_Mapping"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hirose et al._2025_OmniVLA An Omni-Modal Vision-Language-Action Model for Robot Navigation.pdf"
---

# OmniVLA: An Omni-Modal Vision-Language-Action Model for Robot Navigation

> **저자**: Noriaki Hirose, Catherine Glossop, Dhruv Shah, Sergey Levine | **날짜**: 2025-09-23 | **URL**: [https://arxiv.org/abs/2509.19480](https://arxiv.org/abs/2509.19480)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: We train a highly generalizable vision-based navigation policy with flexible conditioning, leveraging over 9,500*

OmniVLA는 2D 포즈, egocentric 이미지, 자연어 등 다양한 모달리티로 조건화된 목표를 처리할 수 있는 omni-modal vision-language-action 모델로, 9,500시간 이상의 다중 플랫폼 로봇 네비게이션 데이터로 학습되어 강력한 일반화 성능을 달성한다.

## Motivation

- **Known**: 기존 로봇 네비게이션 정책들은 대부분 단일 모달리티(egocentric 이미지, 2D 포즈, 또는 자연어)로만 학습되며, 이는 실제 환경에서의 적응성을 제한한다. VLA 모델과 modality masking 기법은 조작 분야에서 성공적으로 사용되었다.
- **Gap**: 기존 네비게이션 정책들은 단일 모달리티 조건화만 지원하여 실제 사용 시나리오의 유연성이 부족하고, 다양한 데이터셋을 동시에 활용할 수 없다. End-to-end VLA 기반 omni-modal 네비게이션 모델이 부재하다.
- **Why**: 인간은 자연스럽게 여러 정보 모달리티(GPS, 랜드마크, 언어 지시)를 조합하여 네비게이션을 수행하므로, 로봇도 이러한 유연성을 가져야 하며, omni-modal 학습은 더 풍부한 기하학적·의미론적·시각적 표현을 학습하게 한다.
- **Approach**: OpenVLA 7B 백본을 기반으로 하여 goal 이미지와 2D 포즈를 처리하는 ViT 인코더와 projection layer를 추가하고, 학습 중 randomized modality fusion 전략으로 세 가지 모달리티와 그 조합을 학습한다. Modality dropout과 masking을 통해 모달리티 불균형 문제를 해결한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Network architectures for multi-modal vision-based*

- **Omni-modal 조건화 지원**: 2D 포즈, egocentric 이미지, 자연어 및 이들의 조합으로부터 네비게이션이 가능하며, 사용자가 여러 모달리티를 함께 활용할 수 있다.
- **대규모 학습 데이터 활용**: 10개 플랫폼에서 수집한 9,500시간 이상의 데이터를 통합 학습하여 기존의 단일 모달리티 제약을 극복한다.
- **specialist baseline 초과 성능**: 단일 모달리티로 학습된 specialist 모델들보다 모든 모달리티에서 우수한 성능을 달성한다.
- **강력한 일반화 능력**: 미학습 환경으로의 일반화, 희소 모달리티에 대한 강건성, 새로운 자연어 지시 따르기를 모두 달성한다.
- **효율적 fine-tuning**: 제한된 데이터로 새로운 모달리티와 환경에 빠르게 적응 가능하다.

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Network architectures for multi-modal vision-based*

- OpenVLA 7B 기반 VLA 백본에 DINOv2와 SigLIP을 포함한 visual 인코더 추가
- Goal image와 goal pose를 각각 ViT로 인코딩하여 projection layer를 통해 language embedding space에 정렬
- Llama 2 7B tokenizer로 자연어 프롬프트 처리
- 학습 중 goal image, goal pose, language prompt의 토큰을 randomly mask하는 modality dropout으로 모달리티 불균형 처리
- 추론 시 masking을 통해 이용 가능한 모달리티만 사용 가능하도록 구현
- GNM mixture, LeLaN mixture, Frodobots-2K, BDD-V 등 공개 데이터셋 통합 학습
- Cross-embodiment 데이터 학습으로 다양한 로봇 플랫폼 지원

## Originality

- 네비게이션 분야 최초의 end-to-end VLA 모델로서 omni-modal goal conditioning을 구현하여, 조작 분야의 성공을 네비게이션에 체계적으로 적용한 첫 사례이다.
- Randomized modality fusion 전략으로 서로 다른 데이터셋의 모달리티 불균형을 해결하면서도 각 모달리티의 보완적 정보를 활용한다.
- 9,500시간이라는 대규모 다중 플랫폼 데이터로 pre-training함으로써, 단순히 아키텍처 설계뿐 아니라 데이터 규모와 다양성의 이점을 명확히 보여준다.
- Specialist baseline과의 직접 비교를 통해 omni-modal 학습의 일반화 이점을 정량적으로 입증한다.

## Limitation & Further Study

- 평가가 주로 시뮬레이션 및 제한된 실제 환경 데이터에 국한되었을 가능성 - 더 다양한 실제 환경(극한 날씨, 혼잡 지역)에서의 평가 필요
- Modality fusion의 최적화 방식이 randomized approach에 그쳐 있어, adaptive modality weighting이나 learned fusion mechanism의 탐색 여지가 있다.
- 새로운 모달리티(3D 포인트 클라우드, 깊이 정보 등) 추가 시 아키텍처 수정이 필요한 구조적 제약
- Language instruction의 robust 이해를 위한 hallucination 및 오류 분석이 부족하다.
- 후속 연구: (1) 더욱 복잡한 다중 모달리티 조합의 학습, (2) Continual learning을 통한 새로운 모달리티 온라인 적응, (3) 실제 배포 환경에서의 장기간 성능 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OmniVLA는 로봇 네비게이션에 omni-modal 조건화를 처음으로 체계적으로 도입한 강력한 foundation model로, 대규모 다중 플랫폼 데이터와 효과적인 모달리티 fusion 전략으로 기존 specialist 모델들을 능가하는 성능과 유연성을 달성한다. 이는 로봇 기초 모델의 일반화 및 확장성 연구에 중요한 기여를 한다.

## Related Papers

- 🔗 후속 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OmniVLA의 다중 플랫폼 학습이 OpenVLA의 일반화된 아키텍처를 다양한 로봇 플랫폼에서 검증하고 확장한 연구이다.
- 🔄 다른 접근: [[papers/1491_NaVILA_Legged_Robot_Vision-Language-Action_Model_for_Navigat/review]] — 둘 다 다리 로봇 네비게이션에 VLA를 적용하지만, OmniVLA는 다중 모달리티를, NaVILA는 vision-language-action에 집중한다.
- 🏛 기반 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — OmniVLA의 다중 모달리티 처리가 Visual Language Maps의 공간-언어 매핑 기술을 기반으로 확장된다.
- 🔄 다른 접근: [[papers/1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang/review]] — VLA 모델에서 omni-modal vs spatial representation의 다른 다양성 추구 방식
- 🏛 기반 연구: [[papers/1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver/review]] — OmniVLA의 통합 데이터셋 활용이 기반으로 하는 unified robot learning dataset
- 🔗 후속 연구: [[papers/1628_WholeBodyVLA_Towards_Unified_Latent_VLA_for_Whole-Body_Loco-/review]] — OmniVLA의 다중모달 VLA 접근법이 WholeBodyVLA의 전신 로코모션으로 확장되어 더 포괄적인 로봇 제어를 실현할 수 있습니다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OmniVLA가 확장한 OpenVLA의 기본 오픈소스 VLA 모델 기반
- 🔗 후속 연구: [[papers/1385_EO-1_An_Open_Unified_Embodied_Foundation_Model_for_General_R/review]] — OmniVLA의 omni-modal approach가 EO-1에서 interleaved vision-text-action pre-training으로 더욱 통합된 embodied foundation model로 발전했다.
- ⚖️ 반론/비판: [[papers/1500_OmniVLA_Physically-Grounded_Multimodal_VLA_with_Unified_Mult/review]] — 동일한 OmniVLA 이름으로 omni-modal vs multimodal sensor의 다른 통합 접근법 제시
