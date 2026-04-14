# ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control

> **저자**: Jean Pierre Sleiman, He Li, Alphonsus Adu-Bredu, Robin Deits, Arun Kumar, Kevin Bergamin, Mohak Bhardwaj, Scott Biddlestone, Nicola Burger, Matthew A. Estrada, Francesco Iacobelli, Twan Koolen, Alexander Lambert, Erica Lin, M. Eva Mungai, Zach Nobles, Shane Rozen-Levy, Yuyao Shi, Jiashun Wang, Jakob Welner, Fangzhou Yu, Mike Zhang, Alfred Rizzi, Jessica Hodgins, Sylvain Bertrand, Yeuhi Abe, Scott Kuindersma, Farbod Farshidian | **날짜**: 2026-01-30 | **DOI**: [10.48550/arXiv.2602.00401](https://doi.org/10.48550/arXiv.2602.00401)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Hardware deployment of ZEST across diverse data sources and robot morphologies. In order of appearance from top *

ZEST는 다양한 데이터 소스(모션캡처, 비디오, 애니메이션)에서 강화학습으로 정책을 훈련하여 휴머노이드 및 사족 로봇에 zero-shot 배포하는 동작 모방 프레임워크이다. 적응적 샘플링과 모델 기반 보조력(assistive wrench) 커리큘럼을 결합하여 복잡한 다중 접촉 동작을 학습할 수 있다.

## Motivation

- **Known**: 지난 10년간 레그 로봇 제어의 주류 접근법은 오프라인 궤적 생성 후 MPC와 최적화 기반 전신 제어기로 추적하는 방식이었으며, 최근 RL은 암묵적 접촉 역학 학습과 zero-shot 하드웨어 배포로 뛰어난 성능을 보였다.
- **Gap**: 기존 tabula rasa RL은 보상 설계에 민감하고 표본 비효율적이며, 모션 데이터를 활용하는 방법들은 시뮬레이션에서는 좋지만 실제 배포에서 접촉 풍부성과 불확실성을 다루기 어렵고 지속적 fine-tuning이 필요하다.
- **Why**: 휴머노이드 로봇이 인간 중심 환경에서 일상 작업을 수행하려면 다양한 전신 협응 동작을 일반화하여 배포할 수 있어야 하며, 기술 사일로가 아닌 통합 프레임워크로 복잡한 동작을 학습 효율적으로 확보할 필요가 있다.
- **Approach**: ZEST는 적응적 샘플링으로 어려운 동작 세그먼트에 집중하고, model-based assistive wrench를 통한 자동 커리큘럼으로 장기 동작을 가능하게 하며, 중등도 domain randomization만으로 시뮬레이션 학습 후 하드웨어에 zero-shot 배포한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Hardware deployment of ZEST across diverse data sources and robot morphologies. In order of appearance from top *

- **다양한 데이터 소스 통합**: 고품질 MoCap, 노이즈 있는 모노큘러 비디오, 물리 제약 없는 애니메이션을 단일 프레임워크로 처리
- **복잡한 다중 접촉 기술**: Atlas에서 army crawl, breakdancing 등 동적 다중 접촉 스킬을 MoCap으로 학습
- **비디오 직접 전이**: 표현력 있는 댄스와 박스 클라이밍을 비디오에서 Atlas와 Unitree G1로 직접 전이
- **크로스 모폴로지 확장**: Spot 사족 로봇에서 연속 백플립 같은 곡예 능력을 애니메이션으로 학습
- **단순화된 배포 파이프라인**: 접촉 레이블, 참조/관측 윈도우, 상태 추정기, 광범위한 보상 설계 회피

## How

![Figure 3](figures/fig3.webp)

*Fig. 3. Overview of ZEST, which consists of three main stages. (1) Reference data: A diverse set of motions from MoCap, *

- **적응적 샘플링(Adaptive Sampling)**: 훈련 중 어려운 동작 세그먼트에 집중하여 샘플 효율성 향상
- **Model-based Assistive Wrench 커리큘럼**: 정책 학습 초기 단계에서 모델 기반 보조력을 제공하여 점진적으로 난이도 상향
- **강화학습 with 모션 데이터 선행(Prior)**: DeepMimic 스타일의 모방 보상으로 자연스러운 동작 유도, adversarial imitation learning 변형 고려
- **Joint-level Gain 선택 절차**: 폐쇄 체인 액추에이터에 대해 근사적 해석 armature 값에서 게인 도출
- **정제된 액추에이터 모델**: 토크, 속도, 안전 제약의 현실적 모델링
- **중등도 Domain Randomization**: 과도한 무작위화 없이 sim-to-real 갭 최소화

## Originality

- **이질적 데이터 소스 통합**: MoCap, 비디오, 애니메이션을 동일 프레임워크에서 처리하는 통합 방식의 혁신
- **모델 기반 assistive wrench 커리큘럼**: 정책 학습에 물리 기반 지원을 단계적으로 제공하는 자동 커리큘럼 설계
- **접촉 레이블 회피**: 접촉 일정을 사전 정의하지 않고 정책이 암묵적으로 학습하도록 함으로써 설계 복잡성 감소
- **다중 모폴로지 zero-shot 전이**: 휴머노이드(Atlas, G1)와 사족(Spot) 간 동일 정책으로 배포 가능성 시연
- **폐쇄 체인 액추에이터 게인 선택 절차**: 이론 기반 근사로 하이퍼파라미터 튜닝 부담 감소

## Limitation & Further Study

- **시뮬레이션 의존성**: 전체 훈련이 시뮬레이션 기반이므로 중요한 물리 특성이 모델링되지 않으면 실패 가능
- **동작 데이터의 질 의존성**: 입력 데이터(특히 비디오)의 노이즈가 많으면 성능 저하 가능성 미분석
- **환경 적응 한계**: 학습된 정책이 훈련 데이터와 크게 다른 환경/접촉에서 안정성 보장 미약
- **액추에이터 제약 고려 미완성**: 현재 토크/속도 제약을 사후 적용하여 동적 운동의 일부가 실현 불가능할 가능성
- **후속 연구 방향**: (1) 온라인 적응 메커니즘 추가로 하드웨어 편차 자동 보정, (2) 레이트 제약이 높은 센서 활용, (3) 멀티태스크 정책 계층화 구조 개발, (4) 인간 피드백 루프 통합

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ZEST는 heterogeneous 데이터 소스와 다중 로봇 모폴로지에서 zero-shot 배포를 달성하는 획기적 프레임워크로, 적응적 샘플링과 모델 기반 보조력 커리큘럼이 기술적 혁신이며, Atlas와 Spot의 복잡한 다중 접촉 동작 실현은 실제 휴머노이드 제어의 미래 방향을 제시한다.
