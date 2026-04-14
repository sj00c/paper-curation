# GMT: General Motion Tracking for Humanoid Whole-Body Control

> **저자**: Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, Xiaolong Wang | **날짜**: 2025-06-17 | **URL**: [https://arxiv.org/abs/2506.14770](https://arxiv.org/abs/2506.14770)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3: An overview of GMT. Here gt denotes the motion target frame, ot denotes proprioceptive*

GMT는 humanoid 로봇이 다양한 전신 모션을 추적할 수 있도록 하는 통합 정책을 학습하는 프레임워크로, Adaptive Sampling 전략과 Motion Mixture-of-Experts 아키텍처를 핵심 요소로 제안한다.

## Motivation

- **Known**: Character animation 분야에서는 single unified controller로 다양한 모션을 수행하는 성공 사례들이 있으며, 최근 humanoid 로봇에서도 motion imitation 기반 제어 연구가 활발하다.
- **Gap**: 기존 연구들은 부분 관찰성, 하드웨어 제약, 불균형 데이터 분포, 모델 표현력 문제 중 일부만 해결하였으며, 진정한 의미의 unified general motion tracking controller는 아직 개발되지 못했다.
- **Why**: Humanoid 로봇이 일상 환경에서 다양한 작업을 수행하려면 광범위한 모션 기술을 보유해야 하며, 이를 위해 수작업 설계를 피하고 human motion data를 활용하는 general purpose controller가 필수적이다.
- **Approach**: GMT는 teacher-student 훈련 프레임워크 내에서 Adaptive Sampling으로 데이터 분포 불균형을 해결하고, Motion MoE 아키텍처로 모델 표현력을 향상시키며, 부분 관찰성과 하드웨어 제약을 체계적으로 처리한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: We deploy the general unified motion tracking policy on a medium-sized humanoid robot.*

- **Adaptive Sampling 전략**: 어려운 모션 세그먼트에 대한 샘플링 비율을 자동으로 증가시켜 AMASS 데이터셋의 불균형 문제를 해결
- **Motion MoE 아키텍처**: 모션 manifold의 다른 영역에 대한 전문화를 강화하여 단일 정책의 표현력과 일반화 능력 개선
- **실제 로봇 배포**: 중형 humanoid 로봇에서 stretching, kicking, dancing, high kicking, kung fu 등 다양한 기술을 안정적으로 수행 달성
- **State-of-the-art 성능**: 8925개 필터링된 motion clips를 사용하여 기존 방법들(ExBody2, HumanPlus, OmniH2O)을 능가하는 성능 달성

## How

![Figure 3](figures/fig3.webp)

*Figure 3: An overview of GMT. Here gt denotes the motion target frame, ot denotes proprioceptive*

- Teacher-student 훈련 프레임워크 도입: privileged information을 활용한 teacher policy를 PPO로 학습한 후 DAgger를 통해 student policy에 지식 이전
- Adaptive Sampling 구현: 각 motion clip의 tracking error를 추적하고 어려운 세그먼트의 샘플링 확률을 동적으로 조정
- Motion Mixture-of-Experts 구성: gating network로 현재 motion target frame에 가장 적합한 expert를 선택하여 모션 처리
- Motion input design: 미래 motion target frames를 CNN으로 처리하여 시간적 의존성 및 모션 다양성 캡처
- Dataset curation: AMASS 데이터셋을 humanoid 로봇 하드웨어 제약에 맞게 필터링하여 불가능한 모션 제거

## Originality

- **Adaptive Sampling의 동적 비율 조정**: 기존의 random clipping이나 고정 확률 기반 샘플링과 달리 실시간 tracking error에 기반한 적응형 샘플링으로 학습 효율성 극대화
- **Motion Manifold 기반 MoE**: 단순 task 분류가 아닌 motion manifold 상의 서로 다른 영역을 gating network로 자동 식별하여 전문화
- **통합 설계의 시너지**: 부분 관찰성, 하드웨어 제약, 데이터 불균형, 모델 표현력 문제를 단일 프레임워크 내에서 체계적으로 해결하는 holistic approach

## Limitation & Further Study

- 전신 제어의 상충 관계: 기존 연구들이 언급한 상체와 하체 제어 간의 본질적 충돌이 완전히 해소되었는지 불명확하며, 더 복잡한 조작 작업과의 통합 가능성 미검증
- Dataset 의존성: AMASS 데이터셋에 기반하고 있으며, 다른 humanoid 플랫폼이나 매우 다른 모션 분포에서의 일반화 능력 미실증
- Partial observability 처리의 한계: teacher-student 프레임워크가 필요하며, 실제 배포 중 예상치 못한 visual occlusion이나 센서 노이즈에 대한 robustness 부재
- 후속 연구 방향: (1) 더 큰 규모의 다양한 humanoid 플랫폼에서의 검증, (2) 적응형 정책으로의 확장을 통한 실시간 task planning 통합, (3) 제약 기반 제어와의 결합을 통한 안전성 보장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GMT는 humanoid 로봇의 general motion tracking에 대한 실질적인 해결책을 제시하며, Adaptive Sampling과 Motion MoE라는 두 가지 실용적 기법으로 기존의 산발적 접근들을 통합한 우수한 연구이다. 실제 로봇 배포 성공과 상태-최첨단 성능은 높은 가치를 제시하지만, 더 광범위한 하드웨어 검증과 이론적 분석 강화가 필요하다.
