# HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots

> **저자**: Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, Yuke Zhu | **날짜**: 2024-10-28 | **URL**: [https://arxiv.org/abs/2410.21229](https://arxiv.org/abs/2410.21229)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: HOVER enables versatile humanoid control with a unified*

HOVER는 키네매틱 위치 추적, 조인트 각도 추적, 루트 추적을 포함한 15개 이상의 제어 모드를 지원하는 통합 신경망 제어기로, 정책 증류를 통해 다양한 제어 모드를 단일 정책으로 통합하여 휴머노이드 로봇의 다목적 전신 제어를 실현한다.

## Motivation

- **Known**: 휴머노이드 로봇은 네비게이션, 로코-조작, 탁상 조작 등 다양한 작업을 수행해야 하며, 기존 연구들은 루트 속도 추적, 조인트 각도 추적, 키포인트 추적 등 작업별 특화된 제어 모드를 별도로 개발해왔다.
- **Gap**: 기존 방식들은 각 제어 모드마다 개별 정책을 학습하므로 모드 간 전이가 어렵고 개발 효율이 낮으며, 이를 해결할 통합된 다중 모드 제어기가 부재하다.
- **Why**: 휴머노이드 로봇의 실용성 향상을 위해 정책 재학습 없이 모드 간 원활한 전환이 가능한 통합 제어기가 필수적이며, 이는 향후 휴머노이드 응용의 효율성과 유연성을 크게 향상시킬 수 있다.
- **Approach**: 전신 키네매틱 모션 모방을 모든 제어 모드의 공통 추상화로 삼아 MoCap 데이터로 학습한 Oracle 정책에서 정책 증류(policy distillation)를 통해 다중 모드를 지원하는 통합 정책을 생성한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Comparison between prior work specialists (blue) and our*

- **통합 다중 모드 제어기**: 루트 추적, 조인트 각도 추적, 키네매틱 위치 추적을 포함한 15개 이상의 제어 모드를 단일 정책으로 지원
- **성능 향상**: 개별 학습된 전문가 정책들보다 다중 모드 generalist 정책이 모든 제어 모드에서 우수한 성능을 달성
- **원활한 모드 전환**: 제어 모드 간 실시간 전환이 가능하며 안정적인 제어 유지
- **시뮬레이션 및 실제 로봇 검증**: ExBody, HumanPlus, H2O, OmniH2O 등 다양한 로봇 플랫폼에서 유효성 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of HOVER distillation process. The HOVER policy is distilled from the Oracle policy through propriocept*

- Goal-conditioned RL 프레임워크로 Oracle 정책을 MoCap 인간 모션 데이터에 대해 학습
- Mode mask와 sparsity mask를 통해 상체와 하체의 제어 목표를 독립적으로 활성화
- DAgger 기반 정책 증류로 Oracle의 행동에 student 정책을 정렬하여 supervised learning 수행
- Proprioception masking을 통해 심-투-리얼 갭을 최소화하고 실제 로봇 전개 가능성 확보
- PPO 알고리즘으로 누적 할인 보상을 최대화하는 정책 최적화

## Originality

- 전신 키네매틱 모션 모방을 통합 제어 추상화로 제시한 새로운 관점
- Mode mask와 sparsity mask의 조합으로 유연한 다중 모드 제어 기법 개발
- 정책 증류를 통해 단일 정책이 개별 전문가 정책보다 우수한 성능을 달성하는 counter-intuitive 결과 도출
- 15개 이상의 제어 모드를 통합하는 포괄적 명령 공간 설계

## Limitation & Further Study

- MoCap 데이터 의존성: Oracle 정책의 성능과 다양성이 학습 데이터의 품질에 크게 영향을 받을 가능성
- 실제 로봇 환경의 제약: 논문에서 제시된 실제 로봇 실험의 범위와 복잡도가 시뮬레이션에 비해 제한적일 수 있음
- 계산 복잡도: 다중 모드 정책의 실시간 추론 비용 및 하드웨어 요구사항에 대한 상세 분석 부재
- 후속 연구 방향: 더 복잡한 상호작용 기술(bimanual manipulation, object pushing), 불안정한 환경(soft terrain), 새로운 작업에 대한 few-shot 적응 능력 개선 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: HOVER는 휴머노이드 전신 제어의 다중 모드 통합이라는 실질적이고 중요한 문제를 정책 증류 기반의 우아한 해결책으로 제시하며, 시뮬레이션과 실제 로봇에서 모두 검증된 견고한 성과를 보여준다. 다만 실제 환경의 복잡한 작업에 대한 적응성과 계산 효율성에 대한 심화 분석이 더해지면 완성도가 높아질 수 있다.
