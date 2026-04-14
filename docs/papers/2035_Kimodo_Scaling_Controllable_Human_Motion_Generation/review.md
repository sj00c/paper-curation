# Kimodo: Scaling Controllable Human Motion Generation

> **저자**:  | **날짜**: 2026-03-29 | **URL**: [https://arxiv.org/abs/2603.15546](https://arxiv.org/abs/2603.15546)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Controllable Motion Generation. Kimodo supports flexible and intuitive control for motion generation*

NVIDIA의 Kimodo는 700시간의 광학 모션캡처 데이터로 학습한 kinematic motion diffusion model로, 텍스트 프롬프트 및 포괄적인 운동학 제약 조건을 통해 고품질 인간 모션을 생성한다.

## Motivation

- **Known**: 최근 generative model(diffusion, masked model, tokenized transformer)은 텍스트 프롬프트와 운동학 제약 조건을 통한 인간 모션 생성을 가능하게 했으나, 공개 모션캡처 데이터셋의 제한된 규모로 인해 모션 품질과 제어 정확도가 제한되었다.
- **Gap**: 기존 연구들은 비디오 재구성을 통해 대규모 모션 데이터로 확장을 시도했으나 재구성 부정확성으로 인한 품질 저하 문제가 있다. 또한 포화된 벤치마크에서 핵심 설계 결정을 구별하기 어렵다.
- **Why**: 로봇공학, 시뮬레이션, 게임 등의 분야에서 고품질 인간 모션 데이터의 중요성이 증가하고 있으며, 직관적이면서도 정확한 제어가 가능한 생성 모델은 실무 적용 가치가 높다.
- **Approach**: 두 단계의 transformer denoiser 아키텍처로 root와 body 모션을 분리하여 floating, foot skating 등의 인공물을 최소화하면서, full-body keyframe, 2D waypoint, dense path 등 포괄적인 운동학 제약을 지원한다.

## Achievement


- **대규모 데이터 학습**: Bones Rigplay 데이터셋(700시간의 프로덕션 품질 모션캡처)을 활용한 확장 가능한 모션 생성 모델 구현
- **다양한 제어 인터페이스**: 텍스트 프롬프트, full-body keyframe, sparse joint position/rotation, 2D waypoint, dense 2D path, foot contact 패턴 등 6가지 이상의 제약 조건 지원
- **멀티스켈레톤 지원**: SOMA body model, Unitree G1 humanoid robot, SMPL-X skeleton 등 다양한 골격 구조에 대한 모션 생성 및 retargeting
- **다중 프롬프트 생성**: 순차적 또는 동시적 복합 행동 설명 처리 및 여러 프롬프트 체이닝을 통한 장시간 모션 생성
- **상호작용적 저작 도구**: Viser 기반의 직관적인 모션 저작 인터페이스 제공 및 공개 배포

## How


- 신중하게 설계된 motion representation과 두 단계 diffusion architecture(root와 body 분리)로 운동 인공물 최소화
- Text prompt, kinematic constraint 등 조건을 diffusion model에 conditioning하는 flexible한 아키텍처
- Bones Rigplay 데이터셋의 700시간 광학 모션캡처 데이터로 대규모 학습
- Dataset size, model size, batch size(GPU) 등 확장 축(scaling axis)별 영향 분석을 통한 설계 검증
- Interactive authoring demo를 통한 사용자 친화적 모션 생성 및 편집 기능 제공

## Originality

- 기존 비디오 기반 확장 접근과 달리 대규모 스튜디오 모션캡처 데이터를 활용한 고품질 데이터 기반 확장
- Root와 body 모션 분리를 통한 새로운 두 단계 denoiser 아키텍처로 운동학적 제약 충족도와 모션 품질의 균형 달성
- 텍스트 프롬프트와 여섯 가지 이상의 운동학 제약을 통합 지원하는 포괄적 제어 메커니즘
- 로봇, 게임, 시뮬레이션 등 다양한 응용 분야에 대한 멀티스켈레톤 지원 및 실무 검증

## Limitation & Further Study

- 현재 모델은 최대 10초 길이의 단일 프롬프트 입력만 지원하며, 더 긴 시간의 복합 행동은 다중 프롬프트 체이닝에 의존
- RTX 3090에서 2~5초의 생성 시간이 필요하여 실시간 상호작용 응용에는 부적합한 offline authoring 모델
- Bones Rigplay 데이터셋의 구체적인 다양성(coverage)과 제약 학습 데이터 구성 방법에 대한 상세 공개 부족
- 후속 연구는 생성 속도 향상, real-time interactive 모션 생성, 더 복잡한 공간-시간 제약 처리 등이 가능할 것으로 예상

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Kimodo는 대규모 모션캡처 데이터와 혁신적인 두 단계 diffusion 아키텍처를 결합하여 현실적이고 제어 가능한 인간 모션 생성을 달성한 중요한 기여이며, 로봇공학과 콘텐츠 생성 분야에서 실질적인 응용 가치를 제시한다.
