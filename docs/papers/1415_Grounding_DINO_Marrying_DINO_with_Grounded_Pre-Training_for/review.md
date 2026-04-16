---
title: "1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for"
authors:
  - "Shilong Liu"
  - "Zhaoyang Zeng"
  - "Tianhe Ren"
  - "Feng Li"
  - "Hao Zhang"
date: "2023.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Grounding DINO는 Transformer 기반 detector DINO와 grounded pre-training을 결합하여 언어 입력(카테고리명 또는 referring expressions)으로 임의의 객체를 탐지하는 open-set object detector를 제시한다. 핵심은 언어와 비전 모달리티를 세 단계(feature enhancer, language-guided query selection, cross-modality decoder)에서 긴밀히 융합하는 것이다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Visual_Language_Navigation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2023_Grounding DINO Marrying DINO with Grounded Pre-Training for Open-Set Object Detection.pdf"
---

# Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection

> **저자**: Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, Lei Zhang | **날짜**: 2023-03-09 | **URL**: [https://arxiv.org/abs/2303.05499](https://arxiv.org/abs/2303.05499)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: The framework of Grounding DINO. We present the overall framework, a feature*

Grounding DINO는 Transformer 기반 detector DINO와 grounded pre-training을 결합하여 언어 입력(카테고리명 또는 referring expressions)으로 임의의 객체를 탐지하는 open-set object detector를 제시한다. 핵심은 언어와 비전 모달리티를 세 단계(feature enhancer, language-guided query selection, cross-modality decoder)에서 긴밀히 융합하는 것이다.

## Motivation

- **Known**: 기존 closed-set detector들은 사전 정의된 카테고리만 탐지 가능하며, 몇몇 open-set detection 연구들이 CLIP이나 contrastive learning을 활용해 novel category 일반화를 시도했다. GLIP은 phrase grounding 방식으로 region-text pair에 대한 대규모 contrastive training을 제시했다.
- **Gap**: 기존 방법들은 대부분 neck(phase A) 또는 head(phase C)에서만 단일 단계의 feature fusion을 수행하며, CLIP 기반 접근의 효율성이 region-text pair 탐지 작업에 제한적이다. 또한 GLIP의 sub-sentence level text feature 최적화와 fully zero-shot evaluation이 부족하다.
- **Why**: Open-set object detection은 AGI 시스템의 핵심 능력으로, 임의의 객체 탐지 능력은 image editing 등 생성 모델과의 협업을 통해 광범위한 실용적 응용이 가능하다. 따라서 stronger generalization과 더 나은 cross-modality alignment가 필수적이다.
- **Approach**: Transformer 기반 DINO 구조의 layer-by-layer consistency를 활용하여 세 단계 모두에서 feature fusion을 수행한다. 또한 GLIP의 grounded training 방식을 개선하되, sub-sentence level text feature를 도입하여 무관한 카테고리 간 attention을 제거함으로써 모달리티 간 간섭을 완화한다.

## Achievement


- **COCO zero-shot detection**: COCO training data 없이 52.5 AP 달성, 기존 SOTA 대비 상당한 성능 향상
- **ODinW zero-shot benchmark**: 평균 26.1 AP로 새로운 기록 설립
- **다중 평가 설정**: closed-set detection, open-set detection, Referring Expression Comprehension (RefCOCO/+/g) 세 가지 시나리오에서 일관되게 우수한 성능
- **실용적 응용**: Stable Diffusion과 협업하여 image editing application 실현

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Extending closed-set detectors to open-set scenarios.*

- Feature enhancer: self-attention, text-to-image cross-attention, image-to-text cross-attention을 stacking하여 neck 단계(phase A)에서 feature 강화
- Language-guided query selection: 언어 정보를 활용한 query initialization (phase B)으로 detection head 입력 최적화
- Cross-modality decoder: image와 text cross-attention layer를 포함한 head 단계(phase C) decoder로 query representation 향상
- Sub-sentence level text feature: 문장 내 무관한 카테고리 간 attention을 제거하여 category 간 간섭 완화 및 word-level feature 추출 개선
- Large-scale grounded pre-training: object detection data, grounding data, caption data를 통합하여 개념 일반화 능력 확보

## Originality

- **Three-phase fusion의 완전한 구현**: 기존 GLIP (phase A만) 또는 OV-DETR (phase B만)과 달리 DINO의 구조를 활용하여 모든 세 단계에서 tight fusion 달성
- **Sub-sentence level text feature**: GLIP의 random concatenation 방식을 개선하여 무관한 카테고리 간 attention을 명시적으로 제거하는 novel technique 도입
- **Fully zero-shot evaluation**: 기존의 'partial label' 설정(base category로 학습 후 novel category 테스트)과 달리, training split을 완전히 제외한 true zero-shot 평가 기준 수립", '**통합 벤치마크 평가**: closed-set, open-set, referring detection을 단일 모델로 통합 평가하는 포괄적 평가 프레임워크 제시

## Limitation & Further Study

- **계산 복잡도 분석 부재**: 세 단계 모두에서 cross-attention을 수행함으로 인한 계산 비용 및 inference 속도에 대한 정량적 분석 미흡
- **긴 문장 또는 복잡한 referring expressions에 대한 성능 분석 부족**: RefCOCO 벤치마크의 성능은 제시되나, 매우 복잡한 description에 대한 실패 사례 분석 없음
- **Grounded pre-training 데이터셋 구성의 세부 정보 부족**: 어떤 detection/grounding/caption 데이터를 어느 비율로 사용했는지 명확하지 않음
- **도메인 외 일반화 검증 미흡**: 매우 다른 visual domain (의료 영상, 위성 이미지 등)에 대한 zero-shot 성능 평가 미실시
- **후속연구 방향**: (1) 경량화 및 mobile deployment 최적화, (2) multimodal large language model (LLM)과의 통합, (3) video-based open-set detection 확장, (4) 다언어 지원

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Grounding DINO는 Transformer 기반 detector의 structural advantage를 활용하여 세 단계 모두에서 tight language-vision fusion을 구현함으로써, open-set object detection의 새로운 SOTA를 수립했다. 포괄적인 벤치마크 평가와 실용적 응용 사례를 통해 높은 연구 가치를 입증한다.

## Related Papers

- 🏛 기반 연구: [[papers/1569_Segment_Anything/review]] — Segment Anything의 segmentation 기능과 결합하여 grounded pre-training을 통한 open-set object detection을 구현한다.
- 🏛 기반 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — CLIP의 contrastive learning 개념을 확장하여 언어-비전 grounding이 강화된 객체 탐지 모델을 개발한다.
- 🧪 응용 사례: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — Context-Aware Entity Grounding에서 open-vocabulary object detection의 기반 기술로 활용될 수 있다.
- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — Grounding DINO의 언어 기반 객체 탐지가 RoboPoint의 공간 어포던스 예측에서 객체 인식 단계로 확장 활용됩니다.
- 🔄 다른 접근: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — 로봇 조작에서 언어 기반 객체 이해를 위한 다른 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1438_InternVLA-M1_A_Spatially_Guided_Vision-Language-Action_Frame/review]] — grounding 기능을 통한 공간적 이해의 기본 원리를 VLA 프레임워크에 적용하는 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1506_Open-World_Object_Manipulation_using_Pre-trained_Vision-Lang/review]] — MOO가 활용하는 open-vocabulary object detection과 grounding 기능의 기반이 되는 vision-language model을 제공한다.
- 🔗 후속 연구: [[papers/1569_Segment_Anything/review]] — SAM의 범용 분할 능력이 Grounding DINO의 개방형 어휘 객체 검출과 결합되어 더 정밀한 시각적 grounding을 구현한다.
- 🏛 기반 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — Grounding DINO의 개방형 어휘 객체 검출 기술이 RoboPoint의 공간 affordance 예측을 위한 시각적 grounding 능력의 기반이 된다.
- 🏛 기반 연구: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — Grounding DINO의 시각적 grounding 기술이 TrackVLA++의 Target Identification Memory 구현에 핵심 기반을 제공한다.
- 🏛 기반 연구: [[papers/1301_A3VLM_Actionable_Articulation-Aware_Vision_Language_Model/review]] — Grounding DINO의 시각적 grounding 기술은 A3VLM의 관절 구조와 어포던스 인식에 핵심 기반을 제공한다.
- 🏛 기반 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — Grounding DINO의 open-vocabulary grounding 능력이 CLIP-Fields의 의미론적 필드 구축에 핵심적인 기술적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — Grounding DINO의 시각적 grounding 기법이 Embodied-R1의 포인팅 기반 중간 표현 설계의 핵심 기반을 제공합니다.
