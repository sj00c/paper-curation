# HAFO: A Force-Adaptive Control Framework for Humanoid Robots in Intense Interaction Environments

> **저자**: Chenhui Dong, Haozhe Xu, Wenhao Feng, Zhipeng Wang, Yanmin Zhou, Yifei Zhao, Bin He | **날짜**: 2026-01-29 | **DOI**: [10.48550/arXiv.2511.20275](https://doi.org/10.48550/arXiv.2511.20275)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig 1: Overview of the HAFO model. (a) Policy Training. A dual-agent strategy with*

HAFO는 dual-agent RL 프레임워크를 통해 humanoid robot의 하체 보행과 상체 조작을 동시에 최적화하여 강한 외력 상호작용 환경에서 안정적이고 정밀한 제어를 달성한다.

## Motivation

- **Known**: RL 기반 humanoid locomotion과 경량 object manipulation은 진전했으나, 강한 외력 상호작용 환경에서의 견고하고 정밀한 제어는 미흡하다.
- **Gap**: 기존 RL 방법들은 외력을 명시적으로 모델링하지 않아 인간 개입이나 환경 접촉 시 불안정성을 보이며, lower-RL-upper-IK 방식은 상체의 개루프 제어로 외력 적응이 어렵다.
- **Why**: Humanoid robot의 고중심, 좁은 지지대 특성상 고하중 조작과 고도 작업(로프 현수) 같은 강한 외력 환경에서의 안정적 제어가 실제 응용에 필수적이다.
- **Approach**: Spring-damper system으로 외력을 명시적으로 모델링하고, dual-agent(하체-상체) 구조에 constrained residual action space를 적용하며, curriculum learning으로 점진적으로 외력을 증가시킨다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig 3: Unitree G1 Humanoid robot sim2sim results. We evaluate the model’s performance*

- **Dual-agent RL 프레임워크**: 하체는 견고한 보행, 상체는 정밀한 조작을 독립적으로 최적화하면서 협력적 전신 제어 달성
- **Spring-damper 동적 모델**: 외부 인장력을 spring-damper 시스템으로 모델링하여 세밀한 외력 제어 가능
- **자동 모드 전환**: 명시적 상태 머신 없이 RL 정책이 지면 보행과 공중 현수 사이의 모드 전환을 자율적으로 생성
- **다중 환경 적응**: 단일 dual-agent 정책으로 고하중, 추력 교란, 로프 현수 등 다양한 외력 환경에서 안정적 제어
- **고도 작업 선례**: 로프 현수 상태에서의 안정적 운영을 달성한 첫 locomotion 제어 전략

## How

![Figure 2](figures/fig2.webp)

*Fig 2: Spring-damper model and performance analysis. (a) Spring-damper model schematic*

- Lower body agent와 upper body agent의 분리된 RL 정책으로 coupled training 수행
- Constrained residual action space로 상체 에이전트 훈련 안정성과 샘플 효율성 향상
- Spring-damper 파라미터(강성, 감쇠)를 curriculum learning 스케줄에 따라 점진적으로 증가
- 외력 적용 지점을 randomize하여 다양한 교란 조건에 대한 일반화 능력 강화
- Adversarial training으로 robust disturbance-rejection response 학습

## Originality

- Spring-damper 모델을 통한 명시적 외력 동적 모델링으로 기존의 암묵적 처리 방식 개선
- Dual-agent 분리 전략과 constrained residual action space의 결합으로 훈련 안정성과 효율성 동시 달성
- Curriculum learning과 randomization을 통한 progressive force adaptation으로 모드 전환의 자동 생성
- Humanoid robot의 로프 현수 상태 제어라는 novel 응용 분야 개척

## Limitation & Further Study

- 로프 현수 조건이 준정적(quasi-static) 상태에 제한될 가능성 있음 — 동적 현수 조건 확대 필요
- Spring-damper 모델의 파라미터 설정 과정이 manual tuning에 의존할 수 있음 — 자동 파라미터 최적화 연구 필요
- 실제 로봇 실험이 sim2sim 수준에 머물러 있음 — sim2real transfer와 실제 환경 검증 필요
- 복합 외력(여러 방향의 동시 교란) 조건에 대한 평가 부족 — 더 복잡한 상호작용 시나리오 탐색 필요
- 외력 측정 센서 의존성이 낮지만, 실제 환경에서의 외력 추정 정확도 영향 분석 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: HAFO는 spring-damper 모델과 dual-agent RL의 결합으로 humanoid robot의 강한 외력 적응 제어에서 새로운 기준을 제시하며, 특히 로프 현수라는 novel 응용에서 안정적 제어를 최초 달성한 의미 있는 연구다.
