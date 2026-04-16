---
title: "1450_Learning_Fine-Grained_Bimanual_Manipulation_with_Low-Cost_Ha"
authors:
  - "Tony Z. Zhao"
  - "Vikash Kumar"
  - "Sergey Levine"
  - "Chelsea Finn"
date: "2023.04"
doi: ""
arxiv: ""
score: 4.0
essence: "저비용 하드웨어로 세밀한 양팔 조작 작업을 학습하기 위해 텔레오퍼레이션 시스템과 Action Chunking with Transformers (ACT) 알고리즘을 결합한 시스템을 제시한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Action_Tokenization_Methods"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2023_Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware.pdf"
---

# Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

> **저자**: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn | **날짜**: 2023-04-23 | **URL**: [https://arxiv.org/abs/2304.13705](https://arxiv.org/abs/2304.13705)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: ALOHA*

저비용 하드웨어로 세밀한 양팔 조작 작업을 학습하기 위해 텔레오퍼레이션 시스템과 Action Chunking with Transformers (ACT) 알고리즘을 결합한 시스템을 제시한다.

## Motivation

- **Known**: 세밀한 조작 작업은 높은 정밀도와 폐쇄루프 시각 피드백을 요구하며, 기존에는 고가의 로봇과 정밀한 센서가 필요했다. 모방 학습은 인간 시연으로부터 직접 학습할 수 있지만 오류 축적 문제가 있다.
- **Gap**: 저비용 하드웨어로도 세밀한 조작을 수행할 수 있는지, 그리고 이를 가능하게 하는 효과적인 모방 학습 알고리즘이 무엇인지 명확하지 않다.
- **Why**: 세밀한 조작 기술의 민주화는 로보틱스의 접근성을 크게 높일 수 있으며, 저비용 시스템에서 고정밀 작업을 수행하려면 학습 기반의 시각 피드백 메커니즘이 필수적이다.
- **Approach**: 약 20,000달러 이하의 저비용 오프더쉘프 로봇 팔 두 쌍으로 텔레오퍼레이션 시스템을 구축하고, action chunking을 통해 다중 스텝 액션 시퀀스를 예측하는 Transformer 기반 CVAE 모델 ACT를 개발한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: ALOHA*

- **저비용 시스템 개발**: 3D 프린팅 부품과 오프더쉘프 로봇으로 구성된 ALOHA 시스템이 20,000달러 이하로 구축되며 정밀한 양팔 조작을 가능하게 함
- **우수한 학습 성능**: 단 10분(50개 궤적)의 시연으로 6가지 세밀한 작업(뚜껑 열기, 배터리 슬롯팅 등)을 80-90% 성공률로 학습
- **ACT 알고리즘**: action chunking과 temporal ensembling을 통해 오류 축적을 완화하고 기존 모방 학습 방법을 큰 폭으로 초월하는 성능 달성
- **다양한 작업 검증**: 정밀도 높은 작업(지퍼타이 스레딩), 동적 작업(탁구공 저글링), 접촉 부자유로운 작업(NIST board 체인 조립) 등을 성공적으로 수행

## How

![Figure 4](figures/fig4.webp)

*Fig. 4: Architecture of Action Chunking with Transformers (ACT). We train ACT as a Conditional VAE (CVAE), which has an *

- **텔레오퍼레이션 하드웨어**: 두 세트의 저비용 ViperX 로봇 팔을 joint-space mapping으로 연결하고 역구동 가능성을 위해 3D 프린팅된 핸들과 사용자 정의 그리퍼 설계
- **다중 카메라 시각 피드백**: 상단, 전면, 양쪽 손목에 각각 카메라를 배치하여 RGB 이미지를 정책 입력으로 사용
- **Action Chunking with Transformers (ACT)**: Transformer 아키텍처를 사용하여 다음 k 타임스텝의 조인트 위치를 예측하는 generative model을 조건부 VAE (CVAE)로 학습
- **Temporal Ensembling**: 정책을 자주 쿼리하고 겹치는 액션 청크들을 평균화하여 부드럽고 정확한 궤적 생성
- **픽셀-투-액션 학습**: RGB 이미지에서 로봇 액션으로의 end-to-end 정책을 학습하여 복잡한 물리 모델링 대신 폐쇄루프 시각 피드백에 의존

## Originality

- **Action Chunking의 심리학적 영감**: 인간이 행동 시퀀스를 chunk로 그룹화하는 개념을 로봇 학습에 처음으로 적용하여 오류 축적 문제 해결
- **저비용 고성능 텔레오퍼레이션**: 오프더쉘프 부품과 3D 프린팅만으로 고가의 수술로봇 수준의 정밀도를 달성하는 혁신적 접근
- **CVAE 기반 sequence modeling**: 단순 Transformer 구조가 아닌 Transformer 기반 CVAE를 사용하여 인간 시연의 다양성을 캡처하는 generative model 구현
- **Temporal Ensembling**: 겹치는 action chunk들의 평균화를 통해 policy smoothness와 정확성을 동시에 달성하는 novel 기법

## Limitation & Further Study

- **샘플 효율성**: 여전히 10분의 시연이 필요하며 매우 제한된 데이터에서의 일반화 능력은 미검증
- **작업 특화성**: 6가지 특정 세밀한 조작 작업으로 평가되었으나 보다 다양한 작업 범주으로의 확장성 불명확
- **시뮬레이션 대 실제 세계**: 실제 로봇에서만 검증되었으며 시뮬레이션 환경에서의 성능과 sim-to-real transfer에 대한 분석 부족
- **하드웨어 의존성**: 특정 로봇 아키텍처(ViperX)에 의존하며 다른 저비용 플랫폼에의 이식성 미검증
- **후속 연구**: (1) 더 적은 시연으로 학습 가능한 방법 개발, (2) 다양한 작업 카테고리로의 일반화 개선, (3) 다른 저비용 로봇 플랫폼에서의 재현성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 저비용 하드웨어와 혁신적인 imitation learning 알고리즘의 결합으로 로보틱 조작의 민주화에 기여하는 중요한 작업이며, Action Chunking with Transformers는 오류 축적 문제를 우아하게 해결하는 독창적 방법론을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — 둘 다 bimanual manipulation을 다루지만 저비용 하드웨어와 diffusion foundation model의 접근법 차이를 비교할 수 있다.
- 🔗 후속 연구: [[papers/1355_DreamDojo_A_Generalist_Robot_World_Model_from_Large-Scale_Hu/review]] — 대규모 dexterous manipulation 데이터를 저비용 시스템에 적용하여 접근 가능한 양팔 조작 학습을 실현할 수 있다.
- 🏛 기반 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — action tokenization의 효율적인 방법론을 양팔 조작 작업에 적용하는 기본 원리를 제공한다.
- 🏛 기반 연구: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — RDT의 bimanual manipulation을 위한 기본적인 fine-grained bimanual control과 low-cost hardware 활용 방법을 제공한다.
- 🧪 응용 사례: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — 저비용 하드웨어를 활용한 정밀 양손 조작 연구는 RVT-2의 고정밀 조작 기술을 실용적 환경에 적용하는 사례다.
