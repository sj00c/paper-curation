---
title: "1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode"
authors:
  - "Xi Chen"
  - "Josip Djolonga"
  - "Piotr Padlewski"
  - "Basil Mustafa"
  - "Soravit Changpinyo"
date: "2023.05"
doi: ""
arxiv: ""
score: 4.0
essence: "PaLI-X는 시각 및 언어 컴포넌트를 균형있게 확장한 다국어 비전-언어 모델로, 25개 이상의 벤치마크에서 새로운 최첨단 성능을 달성하며 복잡한 계산과 다국어 객체 검출 같은 새로운 능력을 보여준다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Visual_Language_Navigation"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2023_PaLI-X On Scaling up a Multilingual Vision and Language Model.pdf"
---

# PaLI-X: On Scaling up a Multilingual Vision and Language Model

> **저자**: Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, Siamak Shakeri, Mostafa Dehghani, Daniel Salz, Mario Lucic, Michael Tschannen, Arsha Nagrani, Hexiang Hu, Mandar Joshi, Bo Pang, Ceslee Montgomery, Paulina Pietrzyk, Marvin Ritter, AJ Piergiovanni, Matthias Minderer, Filip Pavetic, Austin Waters, Gang Li, Ibrahim Alabdulmohsin, Lucas Beyer, Julien Amelot, Kenton Lee, Andreas Peter Steiner, Yang Li, Daniel Keysers, Anurag Arnab, Yuanzhong Xu, Keran Rong, Alexander Kolesnikov, Mojtaba Seyedhosseini, Anelia Angelova, Xiaohua Zhai, Neil Houlsby, Radu Soricut | **날짜**: 2023-05-29 | **URL**: [https://arxiv.org/abs/2305.18565](https://arxiv.org/abs/2305.18565)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: [Left] Comparing PaLI-X against PaLI on image-captioning and VQA benchmarks. [Right]*

PaLI-X는 시각 및 언어 컴포넌트를 균형있게 확장한 다국어 비전-언어 모델로, 25개 이상의 벤치마크에서 새로운 최첨단 성능을 달성하며 복잡한 계산과 다국어 객체 검출 같은 새로운 능력을 보여준다.

## Motivation

- **Known**: Vision-Language 모델 확장의 이점이 보고되었으며, Flamingo는 언어 컴포넌트, GIT는 시각 컴포넌트, PaLI는 두 컴포넌트를 함께 확장했지만 각각 단방향적 접근을 취했다.
- **Gap**: 기존 모델들은 시각과 언어 컴포넌트 중 하나에 더 많은 용량을 할당했으며, 매우 큰 규모의 시각 인코더(ViT-22B)를 비전-언어 작업에 활용한 연구가 부족하다.
- **Why**: 균형잡힌 멀티모달 확장은 다양한 복잡한 작업에서 성능을 크게 향상시킬 수 있으며, 새로운 emergence capability 발견을 통해 모델의 확장성과 범용성을 검증할 수 있다.
- **Approach**: ViT-22B 시각 인코더(OCR 사전훈련 포함)와 32B UL2 기반 인코더-디코더를 결합하여, mixture-of-objectives 훈련 전략(prefix-completion과 masked-token completion 혼합)으로 균형잡힌 용량 할당(약 40%-60% 분할)을 달성했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: [Left] Comparing PaLI-X against PaLI on image-captioning and VQA benchmarks. [Right]*

- **벤치마크 성능**: 이미지 캡셔닝, VQA, 문서 이해, 객체 탐지, 비디오 QA, 비디오 캡셔닝 등 25개 이상의 벤치마크에서 새로운 최첨단 성능 달성
- **Pareto frontier 개선**: fine-tuning과 few-shot 성능 간의 Pareto frontier를 Flamingo, Kosmos-1과 비교하여 크게 개선
- **Emergence capability**: 훈련 데이터에 명시적으로 포함되지 않은 복잡 계산(complex counting)과 다국어 객체 탐지 능력 발현
- **다중작업 fine-tuning**: 다양한 벤치마크에 동시에 적응 가능하며 성능 저하 없음
- **다국어 이전학습**: 이미지 내 텍스트 언어와 생성된 캡션 언어 간 전환, 비-영어 레이블을 사용한 객체 탐지

## How

![Figure 4](figures/fig4.webp)

*Figure 4: Visual input for videos: each frame is independently processed by ViT; patch embeddings*

- ViT-22B를 JFT 분류 작업과 OCR 토큰 분류 작업의 혼합으로 사전훈련
- WebLI 데이터셋의 이미지에 GCP Vision API로 OCR 텍스트 주석 추가
- UL2 인코더-디코더 변형(50층 인코더/디코더, 32B 파라미터)을 비전-언어 데이터 혼합으로 사전훈련
- 시각 임베딩을 투영 레이어를 통과시킨 후 텍스트 입력 토큰 임베딩과 concatenate
- Prefix-completion과 masked-token completion 목표를 혼합하여 훈련
- Few-shot 설정에서 N개의 labeled 예제(image-text 쌍)를 shots으로 제공하고 대상 예제 예측
- 다중 이미지/프레임 입력 시 각 이미지를 독립적으로 ViT로 처리 후 패치 레벨 임베딩 flatten 및 concatenate
- OCR 능력이 필요한 작업에서 상류 OCR 시스템의 토큰을 선택적으로 텍스트 입력에 포함

## Originality

- ViT-22B와 같은 초대형 시각 인코더를 OCR 사전훈련과 함께 비전-언어 작업에 처음으로 효과적으로 적용
- 시각 및 언어 컴포넌트를 균형있게 확장(약 40%-60%)한 첫 번째 모델로, 기존 단방향 확장 접근법 극복
- Mixture-of-objectives 훈련 전략을 비전-언어 모델링에 처음으로 적용하여 fine-tuning과 few-shot 간 Pareto frontier 개선
- 다양한 도메인의 15개 이상 벤치마크에 동시 다중작업 fine-tuning 수행 가능한 첫 모델
- 훈련 데이터에 없는 복잡 계산 능력의 emergence 현상을 체계적으로 보고 분석

## Limitation & Further Study

- 모델의 거대한 규모(~54B 파라미터)로 인한 계산 비용과 추론 지연 시간이 실무 배포의 장애 가능성
- OCR 능력이 GCP Vision API 예측에 의존하므로 OCR 시스템의 오류가 누적될 수 있음
- Few-shot 성능 평가 시 샷 선택 전략과 개수에 따른 민감도 분석 부족
- Emergence capability(복잡 계산, 다국어 객체 탐지) 발현의 정확한 메커니즘에 대한 심층 분석 부재
- 후속 연구: 모델 압축/증류를 통한 효율성 개선, 다국어 능력 더욱 강화, 비디오 이해 성능 향상, 다른 모달리티 통합 가능성 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: PaLI-X는 균형잡힌 초대형 비전-언어 모델 확장을 통해 광범위한 작업에서 최첨단 성능을 달성하고 새로운 emergence capability를 보여주는 매우 의미 있는 연구이다. 단, 모델 규모로 인한 실무 적용의 제약과 emergence 메커니즘에 대한 심층 분석이 추가되면 더욱 우수한 논문이 될 것이다.

## Related Papers

- 🏛 기반 연구: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — PaLI-X의 multilingual vision-language scaling이 기반으로 하는 VLM 설계 공간 연구
- 🧪 응용 사례: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — multilingual VLM scaling을 통해 neural scaling laws를 실증한 구체적 사례
- 🔄 다른 접근: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — multilingual vision-language model에서 PaLI-X vs InternVLA의 다른 scaling 접근
- 🔗 후속 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLI-X의 다국어 비전-언어 모델이 PaLM-E의 embodied multimodal 언어 모델로 확장되어 로봇 제어 능력을 추가합니다.
- 🏛 기반 연구: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — VLN-BERT의 시각-언어 사전학습 방법론이 PaLI-X의 다국어 비전-언어 모델 개발의 기초적인 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level/review]] — PaLI-X의 멀티링구얼 비전-언어 모델이 ManipBench의 VLM 저수준 조작 추론 평가 기반이 됨
- 🧪 응용 사례: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — scaling law 분석을 multilingual vision-language model에 적용한 구체적 사례
- 🔗 후속 연구: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — PaLI-X의 multilingual vision-language 확장이 Prismatic VLMs의 설계 원리를 다국어 환경으로 발전시킨다.
- 🏛 기반 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — PaLI-X는 RoboFlamingo가 활용하는 다국어 vision-language 모델의 확장된 기반을 제공한다.
- 🔄 다른 접근: [[papers/1571_Sigmoid_Loss_for_Language_Image_Pre-Training/review]] — 대규모 vision-language 모델에서 Sigmoid Loss는 효율적인 pre-training에, PaLI-X는 multilingual scaling에 초점을 맞춘다.
- 🏛 기반 연구: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — 다국어 비전-언어 모델이 도메인 불변 표현 학습의 이론적 기반을 제공합니다.
