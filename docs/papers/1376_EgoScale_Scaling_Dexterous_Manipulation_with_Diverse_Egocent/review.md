---
title: "1376_EgoScale_Scaling_Dexterous_Manipulation_with_Diverse_Egocent"
authors:
  - "Ruijie Zheng"
  - "Dantong Niu"
  - "Yuqi Xie"
  - "Jing Wang"
  - "Mengda Xu"
date: "2026.02"
doi: ""
arxiv: ""
score: 4.0
essence: "20,854시간의 대규모 이고센트릭 인간 비디오 데이터로 VLA 모델을 사전학습한 후 소량의 정렬된 인간-로봇 중간학습 데이터로 미세조정하여 22-DoF 손가락 조작 로봇에서 54% 성공률 향상을 달성했다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zheng et al._2026_EgoScale Scaling Dexterous Manipulation with Diverse Egocentric Human Data.pdf"
---

# EgoScale: Scaling Dexterous Manipulation with Diverse Egocentric Human Data

> **저자**: Ruijie Zheng, Dantong Niu, Yuqi Xie, Jing Wang, Mengda Xu, Yunfan Jiang, Fernando Castañeda, Fengyuan Hu, You Liang Tan, Letian Fu, Trevor Darrell, Furong Huang, Yuke Zhu, Danfei Xu, Linxi Fan | **날짜**: 2026-02-18 | **URL**: [https://arxiv.org/abs/2602.16710](https://arxiv.org/abs/2602.16710)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: EgoScale: Two-stage human-to-robot learning framework. A flow-based Vision-Language-Action*

20,854시간의 대규모 이고센트릭 인간 비디오 데이터로 VLA 모델을 사전학습한 후 소량의 정렬된 인간-로봇 중간학습 데이터로 미세조정하여 22-DoF 손가락 조작 로봇에서 54% 성공률 향상을 달성했다.

## Motivation

- **Known**: 인간 행동 데이터를 로봇 정책 학습에 활용할 수 있으며, 이전 연구들은 제한된 설정에서의 인간-로봇 전이를 입증했다. 하지만 대규모 인간 데이터가 정교한 고자유도 손가락 조작을 지원할 수 있는지는 불명확했다.
- **Gap**: 기존 연구는 수십~수백 시간 규모의 작은 인간 데이터셋에 의존했으며, 대부분 저자유도 손이나 그리퍼에 집중하여 세밀한 손가락 관절 움직임이 없었다. 따라서 대규모 인간 데이터가 복잡한 손가락 조작을 의미 있게 지원할 수 있는지 확인이 필요했다.
- **Why**: 인간 행동은 로봇 학습을 위해 매우 확장 가능한 데이터 소스이며, 이를 효과적으로 활용할 수 있다면 로봇 데이터 수집의 부담을 크게 줄이고 다양한 조작 기술을 획득할 수 있다.
- **Approach**: 이고센트릭 손목 모션과 재조정된 손가락 관절 각도를 명시적 감독 신호로 사용하는 두 단계 학습: (1) 대규모 인간 비디오 사전학습으로 신체 물리학에 기반한 표현 학습, (2) 정렬된 인간-로봇 중간학습으로 로봇의 감지 및 제어 공간에 표현을 고착화.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Main Experimental Results. Comparison of Human Pre-train + Mid-Training, Human Pretraining,*

- **스케일링 법칙 발견**: 20,854시간의 인간 데이터에서 손-동작 예측 검증 손실이 데이터 규모에 대해 log-linear 관계를 보이며, 이 손실이 실제 로봇 성능과 강하게 상관관계를 가짐
- **성능 향상**: 22-DoF 손가락 조작 손으로 사전학습 없는 기준 대비 평균 54% 성공률 향상 달성
- **일회성 전이 능력**: 로봇 데모 1개만으로 셔츠 접기 등 미학습 태스크에서 최대 88% 평균 성공률 달성
- **실체 불변성**: 고자유도 인간 손 동작으로 학습한 정책이 Unitree G1의 삼손가락 손처럼 훨씬 다른 로봇 구조에도 효과적으로 전이되어 30% 이상의 절대 성공률 향상 제공

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Human Data Collection and Model Architecture. (Left) Aligned human-robot mid-training data*

- 이고센트릱 RGB 관측, 카메라 모션 추정, 손 포즈를 원시 센서 스트림에서 추출
- 상대 손목 모션 ∆W_t = (W_0^w)^-1 W_t^w로 암 모션 표현하여 카메라 움직임에 불변성 확보
- 21개 인간 손 키포인트를 optimization 기반 재조정을 통해 22-DoF Sharpa 손 관절 공간으로 변환
- 9,869개 장면, 6,015개 태스크, 43,237개 객체를 포함하는 다양한 이고센트릭 활동 데이터셋 20,854시간 수집
- Pretrained VLM 백본과 DiT action expert로 구성된 flow-based VLA 정책 구축
- Text encoder, visual encoder, action encoder/decoder를 포함한 통합 아키텍처로 인간과 로봇 데이터 통일
- 정렬된 인간-로봇 중간학습 데이터 50시간(인간) + 4시간(로봇)로 표현 고착화
- 다운스트림 태스크에 대해 미세조정하여 최종 정책 생성

## Originality

- 기존 연구 대비 **20배 이상 대규모**의 20,854시간 이고센트릭 인간 데이터를 최초로 체계적으로 활용
- 손 동작 예측 손실과 실제 로봇 성능 간의 강한 상관관계를 최초로 입증하여 대규모 인간 데이터를 예측 가능한 감독 신호로 확립
- 상대 손목 모션과 재조정된 손 관절 동작으로의 명시적 동작 감독이 task-agnostic 시각 특성보다 조작에 직접 유용한 정보를 추출하도록 강제
- 소량 정렬 중간학습 데이터로 emergent 일회성/소수 샷 일반화 달성—단 1개 로봇 데모로 미학습 고자유도 태스크 수행
- 고자유도 인간 손 공간에서 학습한 표현이 저자유도 로봇 손으로 실체 불변 전이되는 현상을 최초로 체계적으로 입증

## Limitation & Further Study

- **손 포즈 추정 노이즈**: 인간 손 포즈 추출에 off-the-shelf 인식 파이프라인 사용으로 인한 노이즈가 사전학습에 미치는 영향 미상세 분석
- **실체 차이 처리**: 상대 손목 모션은 공유되지만 손 관절 공간 재조정이 모든 로봇 형태에 완벽하게 작동하는지 미명확—저자유도 손으로의 전이 메커니즘 부재
- **중간학습 데이터 획득 비용**: 정렬된 인간-로봇 중간학습 데이터 수집(vive trackers, Manus gloves, 카메라)에 상당한 하드웨어/인프라 투자 필요
- **태스크 다양성 제한**: 평가가 5개 조작 태스크로 제한되어 광범위한 조작 시나리오 일반화 가능성 미확인
- **로봇 플랫폼 제한**: 주로 22-DoF Sharpa 손에서 평가했으며, 저자유도 손(Unitree G1)에서 성능 감소 발생
- 후속연구: (1) 손 포즈 추정 불확실성 정량화 및 강건성 개선, (2) 다양한 로봇 구조에 대한 일반화 메커니즘 개발, (3) 중간학습 데이터 획득 자동화, (4) 장기 수평 태스크 및 다중 객체 상호작용 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 대규모 이고센트릭 인간 데이터의 스케일링 법칙을 최초로 입증하고 이를 고자유도 손가락 조작에 효과적으로 적용한 중요한 기여를 한다. 명확한 실험 설계와 강력한 실증 결과(54% 성공률 향상, 일회성 전이)는 인간 데이터 기반 로봇 학습의 실행 가능성을 확실히 보여주지만, 포즈 추정 노이즈, 중간학습 데이터 수집 비용, 태스크/플랫폼 다양성 제한이 실제 배포 확대를 위해 해결해야 할 과제로 남아있다.

## Related Papers

- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — BridgeData V2의 large-scale robot learning dataset 구축 경험이 EgoScale의 대규모 egocentric video 데이터 활용 방법론에 기초가 된다.
- 🔄 다른 접근: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — MimicPlay의 human video를 통한 long-horizon imitation과 EgoScale의 egocentric video 기반 dexterous manipulation은 인간 비디오 활용에서 서로 다른 접근이다.
- 🔗 후속 연구: [[papers/1515_Phantom_Training_Robots_Without_Robots_Using_Only_Human_Vide/review]] — Phantom의 human video만을 사용한 로봇 훈련이 EgoScale의 대규모 egocentric 데이터 활용으로 더욱 확장된 형태이다.
- 🔄 다른 접근: [[papers/1425_Human2Robot_Learning_Robot_Actions_from_Paired_Human-Robot_V/review]] — 대규모 인간 데이터를 로봇 학습에 활용하는 방법론에서 egocentric vs paired video 접근법을 비교할 수 있습니다.
- 🏛 기반 연구: [[papers/1426_HumanPlus_Humanoid_Shadowing_and_Imitation_from_Humans/review]] — 인간 동작 데이터 수집 방법론과 로봇 imitation learning 파이프라인의 기반 연구입니다.
- 🔄 다른 접근: [[papers/1425_Human2Robot_Learning_Robot_Actions_from_Paired_Human-Robot_V/review]] — 인간 비디오 데이터를 로봇 학습에 활용하는 방법에서 paired video vs egocentric data의 다른 접근입니다.
- 🏛 기반 연구: [[papers/1426_HumanPlus_Humanoid_Shadowing_and_Imitation_from_Humans/review]] — 다양한 egocentric 데이터 수집 방법이 HumanPlus의 인간 동작 데이터 수집 파이프라인에 기반이 된다.
- 🔗 후속 연구: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — diverse egocentric data를 hierarchical imitation learning과 결합하여 더 효율적인 장기 조작 학습을 달성할 수 있다.
- 🔗 후속 연구: [[papers/1355_DexGarmentLab_Dexterous_Garment_Manipulation_Environment_wit/review]] — EgoScale은 DexGarmentLab의 양손 조작 개념을 다양한 작업으로 확장하여 더 포괄적인 조작 학습 환경을 제공합니다.
