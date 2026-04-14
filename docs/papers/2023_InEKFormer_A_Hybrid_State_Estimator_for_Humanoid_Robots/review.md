# InEKFormer: A Hybrid State Estimator for Humanoid Robots

> **저자**: Lasse Hohmeyer, Mihaela Popescu, Ivan Bergonzani, Dennis Mronga, Frank Kirchner | **날짜**: 2025-11-20 | **URL**: [https://arxiv.org/abs/2511.16306](https://arxiv.org/abs/2511.16306)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

InEKFormer는 Invariant Extended Kalman Filter(InEKF)와 Transformer 네트워크를 결합한 하이브리드 상태 추정 방법으로, 인간형 로봇의 floating base 상태를 정확하게 추정한다.

## Motivation

- **Known**: Kalman filter는 로봇 상태 추정에 널리 사용되나 노이즈 파라미터 튜닝에 전문 지식이 필요하며, 최근 하이브리드 방법들이 모델 기반과 데이터 기반 접근법을 결합하여 우수한 성능을 보이고 있다.
- **Gap**: KalmanNet과 KalmanFormer 같은 기존 내부 결합 하이브리드 방법들은 저차원 문제(단순 진자, 2-4 상태)에만 적용되었으며, InEKF와 Transformer를 결합한 접근과 인간형 로봇에 대한 적용이 미흡하다.
- **Why**: 인간형 로봇의 이족 보행은 다양한 환경에서 안정적이고 동적인 움직임을 위해 빠르고 정확한 상태 피드백이 중요하며, 모델 기반 방법의 한계를 극복하고 학습 기반의 장점을 활용할 수 있다.
- **Approach**: InEKF의 propagation과 correction 단계를 유지하면서 Transformer 네트워크를 사용하여 Kalman gain을 학습함으로써, 상태 및 관측 차이의 히스토리로부터 필요한 정보를 암묵적으로 추출한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- **InEKFormer 알고리즘**: InEKF와 Transformer를 내부적으로 결합한 새로운 하이브리드 상태 추정 방법 제안
- **RH5 데이터셋**: 모션 캡처 데이터와 고유감각 측정을 포함한 인간형 로봇 데이터셋 생성 및 공개
- **광범위한 비교**: InEKF, KalmanNet과의 비교를 통해 Transformer의 잠재력을 입증하고 고차원 문제에서의 autoregressive 학습의 중요성 강조

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- InEKF의 state propagation: IMU 측정과 strapdown IMU 모델을 이용한 상태 전이
- Transformer 기반 Kalman gain 학습: 과거 상태와 관측 차이의 시퀀스로부터 Kalman gain 추정
- State correction: Lie exponential을 사용한 보정 단계 수행
- 하이브리드 구조: C++ 기반 모델 기반 부분과 Python/TorchScript 기반 데이터 기반 부분의 분리
- 학습 데이터: walking, squatting, turning, hip movement, single-leg balancing 등 다양한 동작 포함

## Originality

- 기존의 외부 결합(external coupling) 하이브리드 방법과 달리 InEKF와 Transformer를 내부적으로 결합
- RNN 대신 Transformer를 사용하여 더 나은 문맥 해석과 확장성 제공
- InEKF의 상태 공간 대칭성을 유지하면서 학습 기반 Kalman gain 추정
- 인간형 로봇의 full-size 실제 플랫폼에 처음 적용된 내부 결합 하이브리드 방법

## Limitation & Further Study

- 학습 중 robust autoregressive training의 필요성이 강조되었으나 상세한 해결책 미제시
- 공분산 추정이 수행되지 않아 불확실성 정보 활용 제한
- 고차원 상태 공간에서의 계산량과 학습 데이터 요구량에 대한 분석 부족
- 단일 로봇(RH5) 플랫폼에서만 검증되어 다른 인간형 로봇에 대한 일반화 가능성 미검증
- 후속 연구: 다양한 환경 조건(미끄러운 지면, 압축 가능한 지면)에서의 성능 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 InEKF와 Transformer를 내부적으로 결합한 novel hybrid 방법을 제시하고 인간형 로봇에 처음 적용함으로써 상태 추정 분야에 기여하나, autoregressive 학습의 안정성 문제와 일반화에 대한 보다 심층적인 분석이 필요하다.
