---
title: "1571_Sigmoid_Loss_for_Language_Image_Pre-Training"
authors:
  - "Xiaohua Zhai"
  - "Basil Mustafa"
  - "Alexander Kolesnikov"
  - "Lucas Beyer"
date: "2023.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Language-Image Pre-training을 위해 softmax 정규화 대신 pairwise sigmoid loss를 제안하며, 이는 배치 크기와 무관하게 작동하여 메모리 효율성을 개선하고 작은 배치 크기에서 더 나은 성능을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Visual_Language_Navigation"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhai et al._2023_Sigmoid Loss for Language Image Pre-Training.pdf"
---

# Sigmoid Loss for Language Image Pre-Training

> **저자**: Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, Lucas Beyer | **날짜**: 2023-03-27 | **URL**: [https://arxiv.org/abs/2303.15343](https://arxiv.org/abs/2303.15343)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Efﬁcient loss implementation demonstrated via a mock setup with 3 devices and a global batch size of 12. There*

Language-Image Pre-training을 위해 softmax 정규화 대신 pairwise sigmoid loss를 제안하며, 이는 배치 크기와 무관하게 작동하여 메모리 효율성을 개선하고 작은 배치 크기에서 더 나은 성능을 달성한다.

## Motivation

- **Known**: CLIP과 ALIGN 이후 contrastive learning을 통한 image-text 사전학습이 표준이 되었으며, 이는 softmax 기반의 InfoNCE loss를 사용하여 배치 수준의 정규화를 수행한다.
- **Gap**: 기존 softmax loss는 전체 배치에 대한 전역 정규화가 필요하여 분산 구현이 복잡하고 메모리 효율성이 떨어지며, 배치 크기에 강하게 종속된다.
- **Why**: Language-image pre-training을 더 접근 가능하고 효율적으로 만들어 더 적은 컴퓨팅 자원으로 고품질 모델을 훈련할 수 있으며, 배치 크기의 영향을 체계적으로 분석할 수 있게 한다.
- **Approach**: Sigmoid loss는 각 image-text 쌍을 독립적으로 처리하여 전역 정규화를 제거하고, 이를 Locked-image Tuning(LiT)과 결합하여 SigLiT 모델을 개발한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: The effect of pre-training batch size. Left: SigLiT results, trained for 18B seen examples. Sigmoid loss outpe*

- **효율성**: 4개 TPUv4 칩으로 2일 내에 ImageNet 84.5% zero-shot 정확도 달성
- **배치 크기 유연성**: 작은 배치 크기(< 16k)에서 softmax보다 현저히 우수한 성능을 보이며, 동시에 백만 단위의 극단적 배치 크기 확장 가능
- **메모리 효율성**: Sigmoid loss가 symmetry하며 단일 pass만 필요하여 메모리 사용량 감소
- **확장성 분석**: 배치 크기 증가에 따른 성능 포화 지점을 규명하여 합리적인 배치 크기(32k) 제시

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Efﬁcient loss implementation demonstrated via a mock setup with 3 devices and a global batch size of 12. There*

- Image encoder f(·)와 text encoder g(·)의 L2 정규화된 임베딩에 대해 element-wise sigmoid 손실 적용
- Sigmoid loss: -Σ log_sigmoid(labels * logits) / n 형태로, labels는 대각선이 1이고 나머지가 -1인 행렬
- 학습 가능한 온도 파라미터 t = exp(t')와 bias b를 추가하여 logits = dot(z_img, z_txt.T) * t + b 계산", '분산 학습 시 각 기기가 로컬 배치의 손실만 계산하고 누적하여 all-gather 연산 제거
- Pre-trained vision backbone 사용 시 weight decay 비활성화를 통해 성능 향상
- LiT와 CLIP 두 가지 설정(SigLiT, SigLIP)에서 검증

## Originality

- Sigmoid loss를 image-text contrastive learning에 적용한 것은 신규 접근이며, 기존 dimensionality reduction 관련 연구와 차별화
- 배치 크기와 손실 함수의 개념적 분리는 기존 softmax 중심 설계에서의 근본적 전환
- 극단적 배치 크기(1M)까지 체계적으로 탐색하여 성능 포화 지점을 실증적으로 규명
- 분산 구현의 all-gather 제거를 통한 분산 훈련 효율성 개선은 실무적 혁신

## Limitation & Further Study

- 배치 내 모든 비매칭 쌍이 실제로 비관련 쌍이라는 가정이 불완전하며, 이로 인한 label noise 영향 미분석
- ImageNet zero-shot 정확도에 중점을 두어 다른 downstream task(검색, 감지 등)에서의 성능 평가 제한적
- Sigmoid loss와 softmax loss 간의 수렴 속도, 안정성 등 훈련 역학 비교 부족
- multilingual SigLIP 결과 언급은 있으나 상세 분석 및 언어 간 성능 차이 미제시
- 후속 연구: 다양한 downstream task에서의 평가, 다른 최적화 알고리즘과의 상호작용 분석, label noise 처리 방안

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Sigmoid loss를 통해 language-image pre-training의 효율성과 확장성을 동시에 개선한 우수한 연구로, 실무적 접근 가능성을 크게 높이며 배치 크기의 영향에 대한 중요한 통찰을 제공한다.

## Related Papers

- 🔗 후속 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — CLIP의 기본 language-image pre-training을 sigmoid loss로 개선하여 메모리 효율성과 작은 배치에서의 성능을 향상시킨다.
- 🔄 다른 접근: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — 대규모 vision-language 모델에서 Sigmoid Loss는 효율적인 pre-training에, PaLI-X는 multilingual scaling에 초점을 맞춘다.
- 🏛 기반 연구: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — Sigmoid Loss의 효율적인 vision-language pre-training 기법이 Prismatic VLMs의 설계 공간 탐구에 훈련 효율성 측면의 기반을 제공한다.
- 🧪 응용 사례: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — Sigmoid Loss의 메모리 효율적인 언어-이미지 학습이 Vision-Language Foundation Models의 효과적인 로봇 모방 학습에서 활용될 수 있습니다.
- 🏛 기반 연구: [[papers/1331_CLASS_Contrastive_Learning_via_Action_Sequence_Supervision_f/review]] — CLASS의 contrastive learning via action sequence supervision이 sigmoid loss의 pairwise learning 접근법의 로봇 학습 적용 기초가 된다.
- 🔗 후속 연구: [[papers/1611_Visual_Instruction_Tuning/review]] — Visual Instruction Tuning의 vision-language 학습을 sigmoid loss를 통해 더 효율적이고 메모리 친화적인 방향으로 개선했다.
- 🏛 기반 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — Sigmoid Loss for Language Image Pre-Training의 효율적 학습 방법론이 FAST의 DCT 기반 action tokenization에서 고효율 VLA 학습을 위한 기초가 된다.
- 🔄 다른 접근: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — Sigmoid Loss for Language Image Pre-Training과 다르게 contrastive learning을 통한 이미지-텍스트 학습의 다른 접근법을 제시한다.
