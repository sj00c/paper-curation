---
title: "1448_Latent_Action_Pretraining_from_Videos"
authors:
  - "Seonghyeon Ye"
  - "Joel Jang"
  - "Byeongguk Jeon"
  - "Sejune Joo"
  - "Jianwei Yang"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "인터넷 규모의 라벨 없는 비디오에서 로봇 행동을 학습하기 위해 VQ-VAE 기반 잠재 행동 양자화와 Vision-Language-Action 모델 사전학습을 결합한 비지도 학습 방법을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ye et al._2024_Latent Action Pretraining from Videos.pdf"
---

# Latent Action Pretraining from Videos

> **저자**: Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, Lars Liden, Kimin Lee, Jianfeng Gao, Luke Zettlemoyer, Dieter Fox, Minjoon Seo | **날짜**: 2024-10-15 | **URL**: [https://arxiv.org/abs/2410.11758](https://arxiv.org/abs/2410.11758)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of Latent Action Pretraining. (1) Latent Action Quantization: We first learn discrete*

인터넷 규모의 라벨 없는 비디오에서 로봇 행동을 학습하기 위해 VQ-VAE 기반 잠재 행동 양자화와 Vision-Language-Action 모델 사전학습을 결합한 비지도 학습 방법을 제안한다.

## Motivation

- **Known**: Vision-Language-Action (VLA) 모델은 대규모 인터넷 데이터로 사전학습되지만, 로봇 행동 레이블이 필요하기 때문에 인터넷 규모의 데이터를 활용하기 어렵다. 인터넷 비디오는 풍부한 인간 행동 데이터를 제공하지만 로봇 행동 레이블이 부재하다.
- **Gap**: 기존 VLA 모델은 사람이 직접 조종한 로봇 행동 레이블이 필수이어서 데이터 확장성이 제한되며, 인터넷 비디오에서 행동 레이블 없이 로봇 정책을 학습하는 효과적인 방법이 부재하다.
- **Why**: 로봇 학습 데이터 수집의 병목을 제거하여 웹 규모 데이터로 로봇 기반 모델을 구축할 수 있으며, 이는 로봇 조작 정책의 일반화 능력과 확장성을 획기적으로 향상시킬 수 있다.
- **Approach**: 먼저 VQ-VAE 목적함수로 이미지 프레임 간 이산 잠재 행동을 비지도 방식으로 학습하고, 이 잠재 행동을 예측하도록 VLA 모델을 사전학습한 후, 소규모 로봇 데이터로 파인튜닝하여 잠재 행동을 로봇 행동으로 매핑한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Real-world Tabletop Manipulation Results. We evaluate on a total of 54 rollouts for each model*

- **상태 기술 성능 초월**: OpenVLA 대비 실제 조작 작업에서 6.22% 성능 향상을 달성하면서 사전학습 효율성은 30배 이상 증가
- **다중 일반화 능력**: 언어 조건화, 미학습 객체 일반화, 미학습 지시문에 대한 의미론적 일반화가 필요한 실제 조작 작업에서 우수한 성능
- **크로스 환경/체현 전이**: 서로 다른 로봇 체형과 환경을 가진 데이터셋에서 통합된 양자화 잠재 행동 표현의 효과성 입증
- **인간 비디오만으로 학습 가능**: Bridgev2와 같은 대규모 로봇 데이터셋으로 사전학습한 모델을 능가하는 성능
- **신경 시뮬레이션 가능성**: 잠재 행동 예측과 디코더를 활용해 폐루프 평가가 가능한 신경망 기반 시뮬레이션 구현

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of Latent Action Pretraining. (1) Latent Action Quantization: We first learn discrete*

- **잠재 행동 양자화 (Stage 1)**: Encoder-Decoder 구조의 VQ-VAE 목적함수를 사용하여 연속 이미지 프레임 간의 이산 잠재 행동을 학습하며, 이는 사전정의된 행동 프라이어 없이 원자적 행동 토큰화를 수행
- **잠재 사전학습 (Stage 2)**: Vision-Language 모델을 이용해 비디오 관찰과 작업 설명으로부터 Stage 1의 잠재 행동을 예측하는 행동 복제(behavior cloning) 수행
- **로봇 행동 파인튜닝 (Stage 3)**: 소규모 로봇 조작 데이터셋으로 파인튜닝하여 잠재 행동 공간을 로봇 끝단(end-effector) 델타 행동 공간으로 매핑
- **다중 데이터 소스 활용**: 로봇 비디오 데이터셋(행동 레이블 미사용) 및 인간 조작 비디오를 동일한 파이프라인으로 처리하여 환경 중심 행동(객체/카메라 이동) 포함
- **확장성 검증**: 모델 크기, 코드북 크기, 사전학습 데이터 규모 등 4가지 차원에서 확장 실험으로 방법의 효율성 입증

## Originality

- **비지도 행동 학습 최초 시도**: 로봇 행동 레이블 없이 인터넷 규모 비디오에서 VLA 모델을 사전학습하는 최초의 체계적 접근
- **VQ-VAE 기반 행동 토큰화**: Byte Pair Encoding 개념을 물리적 행동에 적용하여 사전정의된 행동 표현 없이 자동으로 행동을 양자화
- **다중 체현 통합 표현**: 서로 다른 로봇 형태와 환경의 데이터를 단일 잠재 행동 공간으로 통합하여 일반화 가능한 표현 학습
- **신경 시뮬레이션 활용**: 예측된 잠재 행동과 디코더를 조합하여 폐루프 평가 가능한 월드 모델 구축

## Limitation & Further Study

- **데이터 분포 격차**: 인간 행동과 로봇 행동 간의 신체 특성 차이로 인한 도메인 갭이 완전히 해결되지 않으며, 소규모 로봇 데이터로의 파인튜닝이 여전히 필요
- **잠재 행동 해석성 부족**: 양자화된 잠재 행동 토큰의 의미와 로봇 행동 간의 직접적 대응 관계가 명확하지 않아 디버깅 및 분석 어려움
- **비정상적 작업 성능**: 환경 중심 행동(카메라/객체 이동)은 잘 포착하지만 동적이거나 유연한 조작 작업에 대한 평가 부족
- **계산 비용**: 3단계 파이프라인(양자화 → 사전학습 → 파인튜닝)으로 인한 누적 학습 시간과 메모리 요구사항 상세 분석 부재
- **후속 연구 방향**: 더 큰 규모의 웹 데이터로 사전학습 확대, 다중 행동 모달리티 처리, 강화학습과의 결합을 통한 의사결정 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 로봇 학습의 주요 제약인 행동 레이블 의존성을 제거하는 혁신적 접근으로, 비지도 학습을 통해 인터넷 규모 데이터 활용을 가능하게 하며, 상태 기술 기술을 능가하는 실제 성능 향상을 입증한 매우 중요한 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1480_Moto_Latent_Motion_Token_as_the_Bridging_Language_for_Learni/review]] — 둘 다 비디오에서 motion representation을 학습하지만 VQ-VAE 기반 양자화와 latent motion token의 접근법 차이를 비교할 수 있다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전학습의 기본 방법론을 로봇 행동 학습에 적용하는 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — play 데이터에서의 잠재 계획 학습을 인터넷 규모 비디오 사전학습과 결합하여 더 일반적인 행동 표현을 학습할 수 있다.
- 🔄 다른 접근: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — 둘 다 비지도 학습을 통한 행동 표현 학습을 다루지만 play data와 video data의 활용 방식 차이를 분석할 수 있다.
- 🏛 기반 연구: [[papers/1480_Moto_Latent_Motion_Token_as_the_Bridging_Language_for_Learni/review]] — 비디오에서의 latent action pretraining 연구가 Moto의 motion token 학습 방법론의 이론적 기초를 제공한다.
- 🏛 기반 연구: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — Latent Action Pretraining은 SPRINT의 정책 사전학습을 위한 비디오 기반 사전 훈련 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1347_D2E_Scaling_Vision-Action_Pretraining_on_Desktop_Data_for_Tr/review]] — 둘 다 비디오에서 action 학습을 다루지만 D2E는 데스크톱 데이터를, Latent Action Pretraining은 일반 비디오를 활용합니다.
- 🏛 기반 연구: [[papers/1310_Any-point_Trajectory_Modeling_for_Policy_Learning/review]] — 비디오에서의 잠재 액션 사전 학습 개념이 임의 점 궤적 모델링의 핵심 아이디어를 제공
