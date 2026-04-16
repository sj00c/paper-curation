---
title: "1569_Segment_Anything"
authors:
  - "Alexander Kirillov"
  - "Eric Mintun"
  - "Nikhila Ravi"
  - "Hanzi Mao"
  - "Chloe Rolland"
date: "2023.04"
doi: ""
arxiv: ""
score: 4.0
essence: "이미지 분할을 위한 기초 모델 SAM(Segment Anything Model)과 11M 이미지의 1B 마스크로 구성된 SA-1B 데이터셋을 소개하며, 프롬프트 기반의 제로샷 전이 학습이 가능한 범용 분할 시스템을 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Visual_Language_Navigation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kirillov et al._2023_Segment Anything.pdf"
---

# Segment Anything

> **저자**: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollár, Ross Girshick | **날짜**: 2023-04-05 | **URL**: [https://arxiv.org/abs/2304.02643](https://arxiv.org/abs/2304.02643)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We aim to build a foundation model for segmentation by introducing three interconnected components: a prompt-*

이미지 분할을 위한 기초 모델 SAM(Segment Anything Model)과 11M 이미지의 1B 마스크로 구성된 SA-1B 데이터셋을 소개하며, 프롬프트 기반의 제로샷 전이 학습이 가능한 범용 분할 시스템을 제시한다.

## Motivation

- **Known**: NLP에서 foundation model과 프롬프팅 기법의 성공에 기반하여 컴퓨터 비전에서도 CLIP 등 비전-언어 모델이 개발되었으나, 대규모 분할 데이터와 범용 분할 모델은 부족한 상태이다.
- **Gap**: 기존 분할 데이터셋은 웹규모의 자연적 데이터 소스가 부족하고, 특정 작업에만 최적화된 감독 학습 모델이 대부분이며, 새로운 데이터 분포와 작업에 대한 제로샷 일반화 능력이 제한되어 있다.
- **Why**: 이미지 분할을 위한 foundation model의 개발은 다양한 다운스트림 작업에 즉시 적용 가능하며, 새로운 데이터 분포에 대한 강력한 일반화 능력으로 컴퓨터 비전 분야의 생산성을 혁신적으로 향상시킬 수 있다.
- **Approach**: 프롬프트 가능한 분할 작업을 정의하고, 이미지 인코더와 경량 마스크 디코더로 구성된 SAM 아키텍처를 설계한 후, 모델-기반 루프를 통한 데이터 엔진(assisted-manual, semi-automatic, fully automatic 3단계)으로 대규모 다양한 분할 마스크 데이터셋을 자동 수집한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Example images with overlaid masks from our newly introduced dataset, SA-1B. SA-1B contains 11M diverse,*

- **대규모 고품질 데이터셋**: SA-1B는 11M 개의 라이센스 보유 프라이버시 보호 이미지에서 1B 이상의 마스크를 포함하여 기존 분할 데이터셋 대비 400배 이상의 규모를 달성했다.
- **제로샷 전이 성능**: 23개의 다양한 분할 데이터셋에서 SAM은 단일 포그라운드 포인트로도 높은 품질의 마스크를 생성하며, 기존 완전 감독 학습 결과와 경쟁력있거나 우월한 성능을 보인다.
- **범용성과 적응성**: 엣지 검출, 객체 제안 생성, 인스턴스 분할, 텍스트-마스크 예측 등 다양한 다운스트림 작업에서 프롬프트 엔지니어링으로 즉시 적용 가능한 강력한 일반화 능력을 입증했다.
- **실시간 상호작용성**: 이미지 임베딩 재사용으로 웹 브라우저에서 ~50ms 내에 마스크를 생성 가능한 효율적인 실시간 처리를 구현했다.
- **공개 공개**: SAM 모델과 SA-1B 데이터셋을 Apache 2.0 라이선스로 공개하여 분할 기반 모델 연구에 기여한다.

## How

![Figure 1](figures/fig1.webp)

*Figure 1: We aim to build a foundation model for segmentation by introducing three interconnected components: a prompt-*

- **Promptable Segmentation Task 정의**: 포그라운드/배경 포인트, 박스, 마스크, 자유형 텍스트 등 다양한 형태의 프롬프트를 받아 유효한 분할 마스크를 반환하도록 작업을 설계한다.
- **SAM 아키텍처 설계**: 무거운 이미지 인코더(ViT 기반), 프롬프트 인코더, 경량 마스크 디코더의 삼단계 구조로 설계하여 이미지 임베딩 재사용과 빠른 추론을 가능하게 한다.
- **모호성 인식 마스크 생성**: 단일 프롬프트에 대해 여러 개의 유효한 마스크를 예측하도록 학습하여 셔츠 vs 사람과 같은 모호성을 자연스럽게 처리한다.
- **Data Engine 구현**: Assisted-manual 단계에서 주석자 보조, semi-automatic 단계에서 자동 마스크 생성과 수동 보정, fully automatic 단계에서 규칙 그리드의 포그라운드 포인트 프롬프팅으로 이미지당 ~100개 마스크 자동 생성한다.
- **반복적 모델 개선**: 수집된 새로운 데이터로 모델을 개선하고 개선된 모델로 더 나은 마스크를 자동 생성하는 모델-기반 루프를 통해 데이터 품질과 다양성을 지속적으로 향상시킨다.
- **공정성과 편향 분석**: SA-1B 이미지를 지리적·경제적으로 다양한 국가에서 수집하고 인구 집단별 SAM의 성능을 검증하여 책임있는 AI 실천을 구현한다.

## Originality

- **새로운 기초 모델 패러다임**: NLP의 foundation model 개념을 처음으로 체계적으로 이미지 분할 도메인에 적용하여 promptable segmentation task와 zero-shot transfer의 프레임워크를 수립했다.
- **혁신적인 Data Engine**: 모델-기반 루프를 통한 자동 데이터 수집 방법론으로 웹규모 분할 데이터 부재 문제를 창의적으로 해결하고 1B 규모 데이터셋을 구축했다.
- **효율적인 아키텍처 설계**: 이미지 임베딩 재사용과 경량 마스크 디코더의 조합으로 foundation model 성능과 실시간 상호작용성을 동시에 달성하는 우아한 설계를 제시했다.
- **모호성 인식 마스크 예측**: 단일 프롬프트에서 여러 유효한 마스크를 생성하는 기법으로 분할의 근본적인 모호성 문제를 해결하는 새로운 접근을 도입했다.
- **종합적인 제로샷 평가**: 23개 데이터셋과 5가지 이상의 다운스트림 작업을 포괄하는 광범위한 제로샷 평가로 foundation model의 일반화 능력을 최초로 체계적으로 검증했다.

## Limitation & Further Study

- **복잡한 공간 추론 제한**: 세밀한 경계 분할과 인접한 객체 구분에서 성능 저하가 발생할 수 있으며, 복잡한 공간 관계를 요구하는 작업에서 개선이 필요하다.
- **텍스트 프롬프트 성숙도 부족**: 자유형 텍스트 프롬프팅은 예비 수준으로, 텍스트-비전 통합이 더 강력해진다면 추가 성능 향상이 가능하다.
- **도메인 특화 작업 성능**: 의료 이미지, 위성 영상 등 특수 도메인에서는 도메인 특화 모델 대비 성능 격차가 존재할 수 있다.
- **후속 연구 방향**: SAM을 기반으로 한 멀티모달 foundation model 개발, 3D 분할 확장, 더 강력한 텍스트-마스크 정렬 학습, 도메인 특화 적응 기법 등이 필요하다.
- **데이터 공정성 심화**: 현재의 지리적 다양성 검증을 넘어 미묘한 문화적 편향, 라벨링 기준의 편차, 특정 카테고리의 언더리프리젠테이션 등에 대한 더 깊이 있는 분석과 완화 전략이 요구된다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Segment Anything는 foundation model의 개념을 이미지 분할에 성공적으로 적용한 획기적인 연구로, 혁신적인 데이터 엔진과 효율적인 모델 설계를 통해 1B 규모 데이터셋과 강력한 제로샷 일반화 능력을 달성했으며, 공개 공개를 통해 컴퓨터 비전 분야에 광범위한 실제적 영향을 미치는 중요한 기여다.

## Related Papers

- 🔗 후속 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — SAM의 범용 분할 능력이 Grounding DINO의 개방형 어휘 객체 검출과 결합되어 더 정밀한 시각적 grounding을 구현한다.
- 🏛 기반 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — SAM의 프롬프트 기반 제로샷 분할 기술이 RoboPoint의 공간 affordance 예측을 위한 시각적 이해 능력의 기반이 된다.
- 🔄 다른 접근: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — 자기 지도 학습 기반 시각 모델에서 SAM은 분할에, DINOv2는 robust visual feature 학습에 특화된 서로 다른 접근법이다.
- 🔗 후속 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — CLIP-Fields의 weakly supervised semantic field 개념을 확장하여 1B 마스크 데이터를 통한 더 강력한 범용 분할 시스템을 구축했다.
- 🏛 기반 연구: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — VITA의 vision-to-action flow matching이 SAM의 강력한 시각적 분할 능력을 로봇 조작 정책 학습의 기초로 활용한다.
- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — Segment Anything의 segmentation 기능과 결합하여 grounded pre-training을 통한 open-set object detection을 구현한다.
- 🏛 기반 연구: [[papers/1462_LOTUS_Continual_Imitation_Learning_for_Robot_Manipulation_Th/review]] — segment anything의 open-vocabulary segmentation 능력을 continual manipulation learning의 object understanding에 활용하는 기반을 제공한다.
- 🧪 응용 사례: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — Segment Anything을 로봇 조작의 객체 인식 API로 활용하여 multimodal instruction을 action으로 매핑한다.
- 🔗 후속 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — Segment Anything과 결합되어 zero-shot object detection과 segmentation의 기반 기술로 활용된다.
- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — SAM의 범용 분할 능력과 RoboPoint의 affordance keypoint 예측을 결합하면 더 정밀한 로봇 행동 지점 예측이 가능하다.
- 🧪 응용 사례: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — Segment Anything의 segmentation 기능을 CLIP과 결합하여 로봇의 3D 공간 이해와 의미론적 메모리 구축에 활용한 실용적 응용입니다.
