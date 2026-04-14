# Toward Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion

> **저자**: Tianyang Wu, Hanwei Guo, Yuhang Wang, Junshu Yang, Xinyang Sui, Jiayi Xie, Xingyu Chen, Zeyang Liu, Xuguang Lan | **날짜**: 2026-01-31 | **URL**: [https://arxiv.org/abs/2602.00678](https://arxiv.org/abs/2602.00678)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1:*

본 논문은 Mixture-of-Experts (MoE) 기반 사족 로봇 이동 정책과 sim-to-real 전이 가능성을 정량화하는 RoboGauge 평가 프레임워크를 통합하여 신뢰할 수 있는 시뮬레이션-실제 간 갭을 해소하는 통합 프레임워크를 제시한다.

## Motivation

- **Known**: 강화학습을 통한 사족 로봇 이동 제어는 시뮬레이션 기반 훈련으로 유망성을 보였으나, sim-to-real 갭과 보상 과적합으로 인해 정책 전이 실패와 물리 검증의 위험성이 있다.
- **Gap**: 기존 연구는 높은 시뮬레이션 보상이 실제 로봇 안정성을 보장하지 못하며, 신뢰할 수 있는 정량적 지표의 부재로 인해 직접 물리 검증에 의존해야 하는 문제가 있다.
- **Why**: 신뢰할 수 있는 sim-to-real 전이 예측은 로봇 하드웨어 손상 위험을 줄이고 다양한 극한 지형에서의 견고한 이동성 달성을 위해 중요하다.
- **Approach**: MoE 아키텍처를 사용하여 고정된 전문가 네트워크의 게이팅을 통해 지형과 명령을 분해하고, 병렬화된 sim-to-sim 테스트를 통해 다차원 고유감각 기반 메트릭으로 sim-to-real 전이성을 정량화하는 RoboGauge 평가 스위트를 제안한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Comparative analysis against one-stage proprioceptive*

- **RoboGauge 평가 프레임워크**: 7개 지형, 10개 난이도 수준, 4개 도메인 무작위화를 포함한 병렬화된 sim-to-sim 방법론으로 실제 배포 전 하드웨어 손상 위험을 완화
- **MoE 정책 우월성**: 모든 지형 범주에서 CTS, HIM, DreamWaQ 등 기존 단계식 고유감각 방법을 능가하는 다중 지형 표현 능력
- **고속 이동 달성**: Unitree Go2 로봇이 평탄지에서 4 m/s 속도 달성 및 고속 안정성 향상과 관련된 신규 좁은 폭의 보행 출현
- **도전적 지형 횡단**: 눈, 모래, 계단, 경사면, 30cm 장애물 등 미지의 까다로운 지형에서 견고한 이동 성능 입증

## How

![Figure 1](figures/fig1.webp)

*Fig. 1:*

- POMDP로 모델링된 사족 로봇 이동 제어 문제에서 IMU와 조인트 인코더만 사용하는 고유감각 기반 관찰
- K개의 병렬 전문가 서브네트워크 {Ek}와 동적 가중치 할당을 위한 게이팅 네트워크 g로 구성된 MoE 구조
- Concurrent Teacher-Student (CTS) 프레임워크 내에서 MoE를 학생 인코더로 통합하여 학생 모델의 표현 능력 증강
- 6개 메트릭, 7개 지형, 10개 난이도 수준, 3개 목표, 4개 도메인 무작위화를 포함한 병렬화된 RoboGauge 평가
- PD 컨트롤러를 통한 토크 계산으로 목표 조인트 위치 달성
- 특권 관찰(privileged observation)을 훈련 중 사용하되 배포 시에는 관찰만 사용하는 교사-학생 분리

## Originality

- sim-to-real 전이 가능성을 정량화하는 전문적이고 종합적인 RoboGauge 평가 프레임워크의 개발이 신규적
- CTS 프레임워크에 MoE 구조를 통합하여 학생 모델의 표현 능력을 향상시키는 접근법이 기존 교사-학생 방법과 차별화
- 고유감각만을 사용하며 카메라, LiDAR, 발 접촉 센서 등 외수용 센서를 피하는 설계는 극한 환경에서의 견고성 확보에 신규적
- 4 m/s의 높은 속도에서 출현하는 좁은 폭의 보행 특성은 시뮬레이션 기반 정책 최적화의 신규한 발견

## Limitation & Further Study

- RoboGauge의 sim-to-sim 메트릭이 실제 sim-to-real 전이를 완전히 포괄하지 못할 가능성이 있으며, 메트릭과 실제 성능 간의 정확한 대응 관계 분석 필요
- 단일 로봇 플랫폼(Unitree Go2)에서만 검증되었으므로 다양한 사족 로봇 설계에 대한 일반화 가능성 미확인
- 지형 무작위화와 도메인 무작위화의 범위 및 현실성에 대한 자세한 분석이 부족하며, 더 극한적인 환경 조건에서의 성능 평가 필요
- MoE의 전문가 수 K 선택 기준과 게이팅 네트워크의 설계에 대한 이론적 근거와 민감도 분석이 제시되지 않음
- 후속 연구는 RoboGauge 메트릭의 타당성 검증, 다양한 로봇 플랫폼으로의 확장, 더 극한 환경에서의 실제 배포 시험이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 MoE 기반 정책과 RoboGauge 평가 프레임워크를 통합하여 sim-to-real 갭 문제를 체계적으로 해결하고, 극한 지형에서 4 m/s의 견고한 이동 성능을 입증함으로써 사족 로봇 이동 제어 분야에 유의미한 기여를 한다.
