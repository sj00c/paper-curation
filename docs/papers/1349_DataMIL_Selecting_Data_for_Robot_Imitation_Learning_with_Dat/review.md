---
title: "1349_DataMIL_Selecting_Data_for_Robot_Imitation_Learning_with_Dat"
authors:
  - "Shivin Dass"
  - "Alaa Khaddaj"
  - "Logan Engstrom"
  - "Aleksander Madry"
  - "Andrew Ilyas"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "DataMIL은 datamodels 패러다임을 로봇 모방학습에 적용하여 대규모 사전 데이터셋에서 작업별 성능을 직접 최적화하는 정책 기반 데이터 선택 프레임워크를 제시한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Robotic_Policy_Evaluation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Dass et al._2025_DataMIL Selecting Data for Robot Imitation Learning with Datamodels.pdf"
---

# DataMIL: Selecting Data for Robot Imitation Learning with Datamodels

> **저자**: Shivin Dass, Alaa Khaddaj, Logan Engstrom, Aleksander Madry, Andrew Ilyas, Roberto Martín-Martín | **날짜**: 2025-05-14 | **URL**: [https://arxiv.org/abs/2505.09603](https://arxiv.org/abs/2505.09603)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Data selection with datamodels. (left) Similarity-based methods select close samples*

DataMIL은 datamodels 패러다임을 로봇 모방학습에 적용하여 대규모 사전 데이터셋에서 작업별 성능을 직접 최적화하는 정책 기반 데이터 선택 프레임워크를 제시한다.

## Motivation

- **Known**: 로봇 공학에서는 대규모 다양한 데이터셋으로 학습한 generalist 정책이 평균 성능은 높지만 개별 작업에서는 저조한 성능을 보이며, 기존 데이터 선택 방법은 의미론적·시각적 유사성 같은 휴리스틱에 의존한다.
- **Gap**: 기존 휴리스틱 기반 데이터 필터링 방법은 실제 정책 성능에 대한 데이터의 영향을 고려하지 않으며, NLP/CV의 datamodels 프레임워크를 로봇 학습에 적용하려면 비용이 많이 드는 실시간 롤아웃 평가 문제를 해결해야 한다.
- **Why**: 대규모 로봇 데이터셋의 효과를 최대화하려면 작업 성공에 실제로 기여하는 데이터를 식별하는 성능 기반 선택이 필수적이며, 이는 샘플 효율을 높이고 실제 배포 시 정책 미세조정 비용을 감소시킨다.
- **Approach**: DataMIL은 validation loss를 대리 목적 함수로 사용하여 실시간 롤아웃 없이 데이터의 정책 성능 영향을 추정하는 datamodel을 학습하고, regression 및 metagradient 기반 추정기를 통해 각 데이터 포인트의 영향도 점수를 계산한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Results for data selection on OXE. We test the performance of policies trained on data*

- **MetaWorld 벤치마크**: 50개 작업에서 최신 기준 대비 10% 성능 향상 달성
- **Open X-Embodiment 데이터셋**: 서로 다른 구현체와 작업에 걸쳐 효과적인 데이터 선택 성공
- **실세계 검증**: LIBERO 10개 작업과 실제 조작 4개 작업에서 일관된 성공률 개선 입증
- **휴리스틱 기반 방법 초과**: 시각적 유사성이나 상태-행동 유사성 같은 기존 휴리스틱 기반 방법들을 지속적으로 능가

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Data selection with datamodels. (left) Similarity-based methods select close samples*

- 정책 학습 알고리즘 A를 black box로 취급하고 데이터 부분집합 D'에 대한 성능 메트릭 M(A(D'))을 근사하는 datamodel f̂를 학습", 'validation loss를 대리 목적 함수로 사용하여 실제 정책 성능과의 상관관계를 유지하면서 비용을 감소
- Regression 기반 estimator: 작은 규모 정책(MetaWorld)에서 데이터-성능 쌍으로부터 직접 학습
- Metagradient 기반 estimator: Octo 같은 대규모 정책에서 gradient 정보를 활용한 효율적 추정
- 선택된 데이터와 작업별 목표 데이터를 co-training으로 결합하여 최종 정책 학습
- validation loss 상관관계를 통해 실환경 평가 없이 데이터 영향도 점수 계산

## Originality

- datamodels 프레임워크를 최초로 로봇 모방학습에 적용하고 실세계 롤아웃의 비용 문제를 해결하는 novel 대리 손실 함수 제안
- 정책 자체를 데이터 선택의 핵심으로 삼는 end-to-end, 성능 기반 접근법으로 기존 휴리스틱 방법과 근본적으로 차별화
- 메타그래디언트 기반 효율적 datamodel 추정기를 대규모 로봇 정책에 적응시킨 기술적 혁신
- Open X-Embodiment 같은 이질적 대규모 데이터셋에서의 데이터 선택 성공으로 실무적 가치 입증

## Limitation & Further Study

- Validation loss와 실제 작업 성능 간의 완벽한 상관관계 보장 부족 — 특정 도메인이나 정책 아키텍처에서 대리 목적 함수의 유효성이 감소할 가능성
- Datamodel 학습 자체에 여러 정책 학습(다양한 D' 부분집합) 필요로 초기 계산 비용이 존재", '실세계 실험이 4개 작업으로 제한적이므로 더 복잡하고 다양한 실제 환경에서의 일반화 미검증
- 후속 연구: (1) 다양한 정책 아키텍처와 도메인에서의 대리 손실 함수의 최적화, (2) 온라인 학습 환경에서 점진적 데이터 선택, (3) 다중 작업 학습 시나리오에서의 확장성

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DataMIL은 datamodels를 로봇 모방학습에 성공적으로 적용하여 성능 기반 데이터 선택이라는 중요한 문제를 해결하며, 광범위한 시뮬레이션 및 실세계 실험을 통해 기존 휴리스틱 기반 방법 대비 일관된 개선을 입증한 높은 가치의 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — 로봇 학습을 위한 대규모 데이터셋의 기초 사례를 제공한다.
- 🔗 후속 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 로봇 모방학습에서 데이터 스케일링을 datamodels로 확장한다.
- 🔄 다른 접근: [[papers/1433_In-Context_Imitation_Learning_via_Next-Token_Prediction/review]] — next-token prediction을 통한 다른 모방학습 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1372_DROID_A_Large-Scale_In-The-Wild_Robot_Manipulation_Dataset/review]] — 야생 환경 로봇 조작 데이터셋에서 데이터 선택을 위한 기초 데이터를 제공합니다.
