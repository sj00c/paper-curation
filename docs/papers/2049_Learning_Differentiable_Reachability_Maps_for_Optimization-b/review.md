# Learning Differentiable Reachability Maps for Optimization-based Humanoid Motion Generation

> **저자**: Masaki Murooka, Iori Kumagai, Mitsuharu Morisawa, Fumio Kanehiro | **날짜**: 2025-08-15 | **DOI**: [10.48550/arXiv.2508.11275](https://doi.org/10.48550/arXiv.2508.11275)

---

## Essence


휴머노이드 로봇의 운동 생성 비용을 줄이기 위해 미분 가능한 Reachability Map을 학습하는 방법을 제안하며, 이를 연속 최적화 제약 조건으로 활용하여 발디딤, 다중 접촉, 조작 운동 계획을 효율적으로 해결한다.

## Motivation

- **Known**: 기존에는 역운동학(IK)을 반복 계산하거나 이산 reachability map을 그리드 기반으로 생성하는 방식이 사용되었으며, 일부 연구는 GMM이나 neural network를 통해 연속적 reachability 표현을 학습했다.
- **Gap**: 이산 reachability map은 궤적 최적화에 직접 활용 불가능하고, 기존 연속 표현(GMM, NN)은 밀도 추정에 의존하여 비선형 joint-to-task 매핑의 특성을 제대로 반영하지 못한다. 또한 convex polyhedron 근사는 실제 도달 가능 영역을 과도하게 제한한다.
- **Why**: 휴머노이드 로봇의 다양한 운동 계획(발디딤, 다중 접촉, 조작)에서 IK 반복 계산은 계산 비용이 크므로, 미분 가능한 reachability 제약으로 이를 최적화 문제에 직접 내장하면 효율성이 크게 향상된다.
- **Approach**: Task space에서 수집한 end-effector pose 샘플을 바탕으로 이진 분류 문제로 reachability 학습을 공식화하고, neural network 또는 support vector machine을 사용하여 연속·미분 가능한 scalar-valued 함수를 학습한 후, 이를 연속 최적화 제약으로 내장한다.

## Achievement


- **Differentiable Reachability Map 정의 및 학습**: 기존의 이산 map과 달리 task space 좌표에 대해 연속·미분 가능한 reachability 함수를 NN 또는 SVM으로 학습하는 방법 제시
- **임의의 형태 표현**: 볼록 다면체(convex polyhedron) 근사 대신 임의의 복잡한 도달 가능 영역을 정확하게 표현 가능
- **다양한 휴머노이드 운동 계획 적용**: 발디딤 계획, 다중 접촉 운동 계획, 조작-보행 복합 계획(loco-manipulation)에 성공적으로 적용
- **계산 효율성**: IK 반복 계산을 피하고 미분 가능 제약으로 직접 최적화하여 운동 생성 속도 향상

## How


- Task space 샘플 수집: 로봇의 kinematic model을 이용하여 도달 가능한 end-effector pose들을 샘플링하고 binary label(reachable/unreachable) 할당
- 이진 분류 문제 공식화: 입력 x_i(task space 점), 출력 y_i ∈ {-1, 1}인 데이터셋 D 구성
- Neural Network 기반 학습: Multilayer perceptron(MLP)을 구성하여 task space 점을 입력으로 받고 실수값 scalar를 출력, 부호로 도달 가능성 판정
- Support Vector Machine 기반 학습: SVM을 활용하여 task space에서 reachable/unreachable 영역을 분류하는 decision boundary 학습
- Continuous optimization 통합: 학습된 함수 f_R(r)을 제약 조건 f_R(r) ≥ 0 형태로 최적화 문제에 직접 내장
- 다양한 운동 계획 문제 구성: 발디딤, 다중 접촉, 조작-보행 계획을 각각 reachability 제약을 포함한 연속 최적화 문제로 재공식화

## Originality

- **Differentiability 강조**: 기존 discrete 또는 density-based 방식과 달리, task space 좌표에 대한 연속성과 미분 가능성을 명시적으로 정의하고 활용
- **이진 분류 접근**: Reachability를 GMM의 밀도 추정이 아닌 명확한 이진 분류 문제로 재정의하여 비선형 매핑 특성 반영
- **최적화 제약 직접 내장**: 학습된 reachability map을 단순 검증 도구가 아니라 최적화 과정의 미분 가능 제약으로 활용하는 새로운 활용 방식
- **일반화된 형태 표현**: Convex 근사 대신 임의의 복잡한 영역 형태를 flexible하게 표현하는 표현 방식의 일반화

## Limitation & Further Study

- **샘플링 해상도**: Task space 샘플링이 sparse하면 경계 근처에서 학습 정확도가 낮아질 수 있음. 고차원 task space에서는 샘플링 비용 증가
- **모델 선택의 trade-off**: NN은 표현력이 크지만 overfitting 위험이 있고, SVM은 kernel 선택에 민감함. 두 모델의 최적 선택 기준 부재
- **방향(Orientation) 처리**: 논문에서 position과 orientation을 모두 고려한다고 하나, 고차원 orientation 공간(SO(3))에서의 학습 효율성이 명확하지 않음
- **다중 end-effector**: 여러 사지(팔, 다리)의 동시 도달 가능성 제약을 표현하는 방식 부재
- **후속 연구**: 적응적 샘플링 전략, active learning으로 샘플 효율성 향상; 다중 contact configuration 동시 최적화; 실제 하드웨어 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 미분 가능한 reachability map의 개념을 명확히 정의하고 학습 기반으로 구현하여, 기존의 이산 map과 근사 convex 표현의 한계를 극복하는 우수한 기여를 한다. 휴머노이드 운동 계획의 효율성을 실질적으로 향상시킬 수 있는 실용적인 방법론이지만, 고차원 공간과 다중 제약 조건에서의 확장성 검증이 필요하다.
