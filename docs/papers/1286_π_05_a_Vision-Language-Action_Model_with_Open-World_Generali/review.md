---
title: "1286_π_05_a_Vision-Language-Action_Model_with_Open-World_Generali"
authors:
  - "Physical Intelligence"
  - "Kevin Black"
  - "Noah Brown"
  - "James Darpinian"
  - "Karan Dhabalia"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "π0.5는 heterogeneous한 다중 데이터 소스(다양한 로봇, 웹 데이터, 의미론적 예측)에서 co-training하여 실제 가정에서 장시간의 복잡한 조작 작업을 수행할 수 있는 Vision-Language-Action 모델이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Intelligence et al._2025_$π_{0.5}$ a Vision-Language-Action Model with Open-World Generalization.pdf"
---

# $π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization

> **저자**: Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, Ury Zhilinsky | **날짜**: 2025-04-22 | **URL**: [https://arxiv.org/abs/2504.16054](https://arxiv.org/abs/2504.16054)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: The π0.5 model transfers knowledge from a heterogeneous range of data sources, including other robots, high-leve*

π0.5는 heterogeneous한 다중 데이터 소스(다양한 로봇, 웹 데이터, 의미론적 예측)에서 co-training하여 실제 가정에서 장시간의 복잡한 조작 작업을 수행할 수 있는 Vision-Language-Action 모델이다.

## Motivation

- **Known**: VLA 모델들은 end-to-end 로봇 제어에서 좋은 성과를 보였으나, 실제 환경에서의 일반화 능력은 여전히 제한적이다. 기존 연구들은 주로 단일 도메인이나 좁은 데이터 분포에서 학습되어 있다.
- **Gap**: 기존 VLA 모델들은 훈련 데이터와 유사한 환경에서만 평가되며, 복잡한 다단계 작업(예: 주방 청소)의 실제 가정 일반화 능력이 부족하다. 다양한 데이터 소스를 효과적으로 통합하여 broad generalization을 달성하는 방법이 명확하지 않다.
- **Why**: 로봇이 실제 세계에서 유용하려면 미지의 환경에서도 적절히 작동해야 하며, 이는 현재 로봇 학습의 가장 큰 미해결 과제이다. 다양한 지식 소스의 효과적 통합은 스케일 기반의 단순한 데이터 수집보다 더 효율적인 일반화 경로를 제시한다.
- **Approach**: π0.5는 2단계 학습 방식을 사용한다: (1) 웹 데이터, 다양한 로봇 데이터, 의미론적 예측을 포함한 heterogeneous 데이터로 사전학습, (2) 고수준 의미론적 부작업 예측과 저수준 로봇 액션을 함께 fine-tuning하는 계층적 구조로 설계되었다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: π0.5 cleaning a new kitchen. The robot is tasked with cleaning a kitchen in a home that was not in the training *

- **실제 가정에서의 장시간 작업 수행**: 훈련 데이터에 없는 새로운 가정에서 10-15분 길이의 주방·침실 청소 같은 복합 조작 작업을 수행 가능
- **Heterogeneous 데이터 활용의 효과 증명**: 전체 훈련 데이터의 97.6%가 모바일 조작 데이터가 아님에도 불구하고 효과적 학습을 달성
- **계층적 아키텍처의 타당성**: 고수준 의미론적 예측과 저수준 액션 예측의 분리로 서로 다른 지식 소스를 효과적으로 활용
- **End-to-end 학습 기반 실제 로봇 시스템의 첫 성공 사례**: 복잡한 dexterous 조작 기술을 실제 환경에서 입증

## How


- π0 기반 VLA 모델을 확장하여 구현
- 사전학습 데이터 구성: 모바일 조작 로봇 직접 수집 데이터(약 400시간), 정적 로봇 데이터, 웹 데이터(이미지 캡셔닝, 질의응답, 객체 위치화), 고수준 의미론적 작업 예측
- 2단계 훈련: (1) heterogeneous 데이터 혼합으로 사전학습, (2) 저수준 액션과 고수준 의미론적 부작업 라벨로 fine-tuning
- 추론 시간 실행: 모델이 먼저 다음 적절한 의미론적 부작업을 예측한 후, 이를 기반으로 저수준 로봇 액션 청크(action chunk) 생성
- Co-training 통합: 다양한 로봇 플랫폼, 웹 기반 시각 작업, 인간 감독자의 언어 지시를 동일한 sequence modeling 프레임워크에 통합

## Originality

- Heterogeneous 데이터 소스의 체계적 통합 전략: 다양한 로봇, 웹 데이터, 의미론적 예측을 단일 VLA 프레임워크에 조직적으로 결합
- 계층적 의미론적 부작업 예측 메커니즘: 고수준 의미론적 이해와 저수준 조작 제어의 명확한 분리로 각각 다른 지식 소스 활용 가능
- 실제 가정 환경에서의 검증: 이전 연구들이 통제된 환경에서 평가한 것과 달리, 훈련되지 않은 실제 가정에서 장시간 복합 작업 수행 입증
- 97.6% 비관련 데이터로부터의 효과적 전이 학습: 대부분의 데이터가 직접 관련되지 않음에도 일반화 달성하는 방식이 혁신적

## Limitation & Further Study

- **데이터 구성의 투명성 부족**: 각 데이터 소스(웹 데이터, 다양한 로봇)의 정확한 규모, 품질 기준, 선별 방식에 대한 상세 기술 필요
- **일반화 범위의 경계**: 주방·침실 청소 같은 특정 가정용 작업에 초점이 맞춰져 있어 다양한 산업, 야외, 동적 환경으로의 확장 가능성 미확인
- **실패 사례 및 에러 분석 부재**: 성공 사례 중심의 보고로 어떤 상황에서 실패하는지, 오류의 원인이 무엇인지 불명확
- **계산 비용 및 모델 규모**: 모델 크기, 훈련 시간, 추론 지연, 배포 비용에 대한 정보 부족
- **후속 연구 방향**: (1) 장기간 적응학습(continual learning) 메커니즘 개발, (2) 실패 사례로부터의 자동 개선 알고리즘 연구, (3) 다양한 로봇 플랫폼(humanoid, mobile base 없는 arm 등)에의 확장 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: π0.5는 heterogeneous 데이터 소스의 체계적 통합을 통해 VLA 모델의 실제 환경 일반화 문제를 처음으로 실질적으로 해결한 성과이며, 계층적 의미론적 구조와 co-training 프레임워크는 로봇 학습의 중요한 설계 원칙을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — π0.5는 RT-1의 Robotics Transformer 아키텍처를 확장하여 heterogeneous 데이터 소스로 확장한 발전된 형태입니다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 둘 다 오픈소스 Vision-Language-Action 모델이지만 π0.5는 heterogeneous 데이터 co-training에 특화되어 있습니다.
- 🔗 후속 연구: [[papers/1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb/review]] — Being-H0.5와 마찬가지로 cross-embodiment 일반화를 목표로 하지만 π0.5는 웹 데이터 활용에 더 중점을 둡니다.
- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 웹 지식을 로봇 제어에 전이하는 아이디어를 확장하여 더 큰 규모의 heterogeneous 데이터로 발전시킨 VLA 모델입니다.
- 🔄 다른 접근: [[papers/1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb/review]] — 둘 다 cross-embodiment VLA 모델이지만 Being-H0.5는 인간 중심 학습에, π0.5는 heterogeneous 데이터 co-training에 특화됩니다.
