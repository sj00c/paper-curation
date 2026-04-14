# Coordinated Humanoid Manipulation with Choice Policies

> **저자**: Haozhi Qi, Yen-Jen Wang, Toru Lin, Brent Yi, Yi Ma, Koushil Sreenath, Jitendra Malik | **날짜**: 2025-12-31 | **DOI**: [10.48550/arXiv.2512.25072](https://doi.org/10.48550/arXiv.2512.25072)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Coordinated Humanoid Manipulation. We present a teleoperation system and a policy learning framework for*

휴머노이드 로봇의 전신 협조 조작을 위해 모듈식 텔레오퍼레이션 인터페이스와 Choice Policy라는 모방 학습 방식을 결합한 시스템을 제시한다. Choice Policy는 다중 후보 행동을 생성하고 점수를 학습하여 멀티모달 행동을 효율적으로 모델링한다.

## Motivation

- **Known**: 휴머노이드 로봇의 조작은 기존 연구에서 주로 상체만 제어하거나 능동적 머리 제어가 부족했으며, diffusion policy는 실시간성이 떨어지고 행동 복제는 멀티모달 특성을 잘 포착하지 못한다.
- **Gap**: 머리, 손, 다리를 포함한 전신 협조 제어의 동시 달성이 어렵고, 멀티모달 행동을 실시간으로 모델링할 수 있는 효율적인 방법이 부족하다.
- **Why**: 휴머노이드 로봇이 인간 중심 환경에서 복잡한 조작 작업을 자율적으로 수행하려면 전신 협조가 필수적이며, 이는 로봇의 실제 배치 가능성을 크게 높인다.
- **Approach**: 모듈식 텔레오퍼레이션을 통해 고품질 시연 데이터를 효율적으로 수집하고, Choice Policy를 사용하여 다중 행동 후보를 생성 및 점수 매김으로써 단일 forward pass로 멀티모달 행동을 모델링한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Coordinated Humanoid Manipulation. We present a teleoperation system and a policy learning framework for*

- **모듈식 텔레오퍼레이션 인터페이스**: VR 컨트롤러 기반 직관적 제어로 팔 end-effector 추적, 파지 원시형(grasp primitives), 손-눈 협조, 로코모션을 분리하여 효율적인 데이터 수집 가능
- **Choice Policy 알고리즘**: K개의 행동 후보를 생성하고 scoring network로 평가하여 diffusion policy 대비 빠른 추론과 behavior cloning 대비 우수한 멀티모달 행동 모델링 달성
- **실제 작업 검증**: 식기세척기 로딩과 화이트보드 닦기 로코-조작 작업에서 Choice Policy가 diffusion policy와 standard behavior cloning을 현저히 능가
- **손-눈 협조의 중요성 증명**: 장기 지평 작업에서 머리 추적이 성공에 필수적임을 실증적으로 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: An overview of our modular teleoperation interface. Control is decomposed into four modules: arm control (end-*

- VR 컨트롤러 입력을 4개의 모듈(팔, 손, 머리, 로코모션)로 분해하고 각 모듈별 직관적 제어 매핑 설계
- teleoperator의 변동성으로 인한 멀티모달 시연 데이터 자동 생성
- Choice Policy: action proposal network가 K개의 행동 후보 생성, score network가 각 후보와 ground-truth 행동의 겹침 정도(음수 MSE)를 학습
- Training: winner-takes-all 패러다임으로 MSE가 최소인 제안만 backpropagation 적용
- Inference: K개 후보 중 최고 점수 행동 선택하여 실행

## Originality

- 텔레오퍼레이션 측면에서 머리 추적을 포함한 진정한 전신 협조 제어 인터페이스 최초 제시
- Choice Policy는 multi-choice learning을 로봇 제어에 적용한 새로운 접근법으로, diffusion의 느린 추론과 behavior cloning의 낮은 표현력 문제를 동시에 해결
- modular 텔레오퍼레이션과 learning 프레임워크의 시스템 수준 통합 설계

## Limitation & Further Study

- 선정된 두 작업(식기세척기, 화이트보드)이 여전히 제한적이며 더 광범위한 조작 작업에 대한 평가 필요
- Choice Policy의 K값 선택과 최적화, scoring network 설계에 대한 상세한 ablation 분석 부족
- 시뮬레이션과 실제 로봇 간의 차이 분석 및 sim-to-real transfer 성능 평가 미흡
- 텔레오퍼레이션 효율성(데이터 수집 시간, operator 피로도) 측정의 정량적 지표 부재
- 후속 연구: 더 복잡한 다물체 조작 작업 확장, 온라인 학습을 통한 정책 개선, 다양한 휴머노이드 플랫폼 일반화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 휴머노이드 전신 조작을 위한 실용적이고 확장 가능한 시스템을 제시하며, Choice Policy는 멀티모달 행동 모델링에서 효율성과 표현력의 균형을 잘 달성했다. 모듈식 텔레오퍼레이션과 함께 실제 로봇 작업에서의 성공적 검증은 고가치의 실제 기여를 보여준다.
