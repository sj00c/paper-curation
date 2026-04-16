---
title: "1409_GR-2_A_Generative_Video-Language-Action_Model_with_Web-Scale"
authors:
  - "Chi-Lam Cheang"
  - "Guangzeng Chen"
  - "Ya Jing"
  - "Tao Kong"
  - "Hang Li"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "GR-2는 38백만 개의 비디오 클립으로 대규모 사전학습한 후 로봇 궤적으로 미세조정하는 generative video-language-action 모델로, 100개 이상의 조작 작업에서 97.7% 평균 성공률을 달성하고 미보기 시나리오에 뛰어난 일반화를 보인다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cheang et al._2024_GR-2 A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation.pdf"
---

# GR-2: A Generative Video-Language-Action Model with Web-Scale Knowledge for Robot Manipulation

> **저자**: Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, Hanbo Zhang, Minzhao Zhu | **날짜**: 2024-10-08 | **URL**: [https://arxiv.org/abs/2410.06158](https://arxiv.org/abs/2410.06158)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview. GR-2 undegoes two stages of training: video generation pre-training and robot data*

GR-2는 38백만 개의 비디오 클립으로 대규모 사전학습한 후 로봇 궤적으로 미세조정하는 generative video-language-action 모델로, 100개 이상의 조작 작업에서 97.7% 평균 성공률을 달성하고 미보기 시나리오에 뛰어난 일반화를 보인다.

## Motivation

- **Known**: Foundation model 패러다임은 언어, 이미지, 비디오 처리에서 성공적이며, 비디오 생성 사전학습이 정책 학습에 유용한 지식을 전이할 수 있음이 알려져 있다.
- **Gap**: 대규모 로봇 데이터 수집의 어려움과 단일 일반화 정책으로 다양한 조작 작업을 수행할 수 있는 생성형 로봇 에이전트의 부재가 존재한다.
- **Why**: 로봇 조작의 다재다능함과 새로운 작업 및 환경에 대한 빠른 적응 능력은 실제 산업 응용에 필수적이며, 대규모 비디오 사전학습을 통해 이를 달성할 수 있다.
- **Approach**: GR-2는 두 단계 학습 프레임워크를 사용한다: (1) Howto100M, Ego4D 등 다양한 공개 데이터와 로봇 데이터셋을 포함한 38백만 개 비디오로 사전학습하여 비디오 생성 능력 확보, (2) 로봇 궤적으로 미세조정하여 행동 예측과 비디오 생성을 동시에 학습한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Multi-Task Learning. We perform experiments in two basic settings (Simple and Distractor) and*

- **대규모 멀티태스크 학습**: 5,000개의 궤적(작업당 평균 50개)으로 100개 이상의 조작 작업을 학습하며 97.7% 평균 성공률 달성
- **강력한 일반화**: 미보기 배경, 환경, 물체, 작업에 대한 예외적인 일반화 능력을 보유하며 100개 이상의 물체를 포함하는 빈 픽킹에서 미보기 물체 처리
- **확장 가능성**: 모델 크기에 따른 성능 향상을 보이는 명확한 scaling law 입증
- **효율적인 학습**: 제한된 로봇 데이터(5,000개 궤적)로 사전학습된 지식을 손실 없이 전이

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Pre-training Dataset. We show sample videos and the verb distribution of the pre-training dataset*

- **비디오 사전학습**: GPT-style transformer로 텍스트 설명과 비디오 프레임으로부터 향후 프레임을 예측하는 auto-regressive 생성 작업 수행
- **토큰화**: 텍스트는 frozen text encoder로, 이미지는 VQGAN으로 discrete token으로 변환
- **멀티뷰 처리**: 로봇 미세조정 단계에서 여러 카메라 뷰를 gracefully 처리하도록 설계
- **행동 생성**: conditional VAE (cVAE)를 사용하여 단계 행동이 아닌 궤적 생성으로 부드러움과 실시간 성능 확보
- **실제 로봇 배포**: Whole-Body Control (WBC) 알고리즘으로 Cartesian 궤적을 최적화하여 7-DoF Kinova Gen3 로봇에 200Hz로 실행

## Originality

- **대규모 이질적 사전학습 데이터**: 38백만 개 비디오(50억 개 토큰)로 GR-1 대비 규모를 대폭 확장하면서 손실 없는 지식 전이 아키텍처 개발
- **생성형과 판별형 학습의 통합**: 사전학습에서 비디오 생성으로 세계 역학을 학습한 후, 미세조정에서 비디오와 행동을 동시 생성하는 듀얼 출력 구조
- **실제 배포 고려**: 궤적 최적화와 실시간 모션 추적을 결합한 WBC 알고리즘으로 실용적 로봇 배포 달성

## Limitation & Further Study

- **데이터셋 규모 의존성**: 사전학습 성능이 대규모 데이터셋에 의존하여 리소스 접근성이 낮은 연구 기관의 재현성 어려움
- **미세조정 데이터량**: 100개 이상 작업에도 불구하고 작업당 평균 50개 궤적만 사용하여 각 작업의 다양성 부족 가능성
- **일반화의 한계**: 미보기 시나리오에 강하지만 물리적 환경의 극단적 변화(극저온, 습지 등)에 대한 평가 부재
- **후속 연구**: 더 효율적인 데이터 활용 방법, 강화학습과의 결합, 다중 로봇 협업 시나리오로의 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GR-2는 대규모 비디오 사전학습과 로봇 데이터 미세조정을 효과적으로 결합하여 로봇 조작의 일반화 능력을 획기적으로 향상시킨 논문이다. 100개 이상의 작업을 소수의 궤적으로 학습하고 미보기 시나리오에 강력한 성능을 보여 실제 로봇 응용에 높은 잠재력을 입증한다.

## Related Papers

- 🔗 후속 연구: [[papers/1410_GR-3_Technical_Report/review]] — GR-2의 generative video-language-action 모델을 더욱 발전시킨 차세대 버전입니다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전학습이 visuomotor policy에 미치는 영향의 기초 연구입니다.
- 🔗 후속 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — GR-2는 GR-1의 비디오 생성 사전학습 아이디어를 계승하여 더욱 발전된 비디오-언어-행동 모델로 진화했습니다.
- 🏛 기반 연구: [[papers/1410_GR-3_Technical_Report/review]] — GR-3의 이전 버전인 GR-2 모델의 기초 연구입니다.
