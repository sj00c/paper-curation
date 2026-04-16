---
title: "1325_CALVIN_A_Benchmark_for_Language-Conditioned_Policy_Learning"
authors:
  - "Oier Mees"
  - "Lukas Hermann"
  - "Erick Rosete-Beas"
  - "Wolfram Burgard"
date: "2021.12"
doi: ""
arxiv: ""
score: 4.0
essence: "CALVIN은 장기간 언어 조건부 로봇 조작 작업을 위한 오픈소스 시뮬레이션 벤치마크로, 자연어 명령을 따라 다단계 조작 작업을 수행하도록 학습하는 에이전트를 평가한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multi-Task_Language_Benchmarks"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Mees et al._2021_CALVIN A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tas.pdf"
---

# CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks

> **저자**: Oier Mees, Lukas Hermann, Erick Rosete-Beas, Wolfram Burgard | **날짜**: 2021-12-06 | **URL**: [https://arxiv.org/abs/2112.03227](https://arxiv.org/abs/2112.03227)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: CALVIN is a benchmark to learn many long-horizon language-conditioned tasks over a range of four manipulation en*

CALVIN은 장기간 언어 조건부 로봇 조작 작업을 위한 오픈소스 시뮬레이션 벤치마크로, 자연어 명령을 따라 다단계 조작 작업을 수행하도록 학습하는 에이전트를 평가한다.

## Motivation

- **Known**: 로봇이 자연어로 지시된 작업을 수행하는 연구가 진행 중이나, 대부분 이산적 행동 원시(discrete action primitives)나 제한된 환경에서 작동한다. 기존 벤치마크들은 표준화되어 있지 않아 접근 방식 비교가 어렵다.
- **Gap**: 연속 제어(continuous control), 장기 시간 수평(long-horizon planning), 다중 모달 입력(multimodal inputs), 자연어 조건화를 모두 포함하는 통합 벤치마크가 없다. 기존 ALFRED 같은 벤치마크는 이산 행동만 지원한다.
- **Why**: 일반적 목적의 로봇이 인간 환경에서 효과적이 되려면 자연어 지시를 이해하고 장기간 복합 작업을 계획·실행할 수 있어야 하며, 이를 위한 표준화된 평가 프레임워크가 필수적이다.
- **Approach**: 시뮬레이션 기반 4개 환경에서 24시간의 무구조 원격조종 플레이 데이터와 20K 언어 지시를 수집하고, 다양한 센서 조합과 환경 구성으로 점진적으로 어려운 평가 프로토콜을 제공한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: CALVIN is a benchmark to learn many long-horizon language-conditioned tasks over a range of four manipulation en*

- **최초의 통합 벤치마크**: 자연어 조건화, 다중 모달 고차원 입력, 7-DOF 연속 제어, 장기 로봇 물체 조작을 모두 포함하는 첫 공개 벤치마크 제공
- **유연한 센서 구성**: RGB-D 정적/그리퍼 카메라, 고유감각 정보, vision-based 촉각 센싱 등 다양한 센서 조합 지원
- **다중 평가 난이도**: 4개 환경에서 3개로 학습 후 미등장 환경으로 테스트하는 zero-shot 일반화 평가 포함
- **베이스라인 성능 분석**: Multi-context imitation learning(MCIL) 베이스라인이 단기 작업에서만 53.9% 성공률을 보이며 장기 작업에서 성능 저하, 개선 여지 명시

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Observation and action spaces supported by CALVIN.*

- 4개 구조적으로 관련된 조작 환경(A, B, C, D) 설계로 작업 다양성 및 공유 구조 확보
- Franka Emika Panda 7-DOF 로봇 팔과 병렬 그리퍼로 현실 기반 시뮬레이션 환경 구성
- 절대/상대 데카르트 포즈, 관절 액션 등 3가지 행동 공간(action space) 지원으로 정책 유연성 극대화
- 무구조 플레이 데이터 기반의 재레이블링(relabeling) 기법으로 기존 imitation learning 접근법 적용 가능
- 학습 환경 수와 센서 조합 조절로 평가 난이도 조정 가능한 프로토콜 제공
- 34개 부분작업, 5단계 장기 수평 평가 시퀀스로 ALFRED의 18개 작업, 4단계보다 확대

## Originality

- 기존 벤치마크(ALFRED)는 이산 행동 분류 방식이나, CALVIN은 연속 제어 정책 학습 요구로 근본적으로 다른 문제 설정
- 무구조 원격조종 플레이 데이터에 자연어 라벨을 결합하는 실용적 데이터 수집 패러다임 제시
- 동일 자연어 명령어로 서로 다른 색상 블록을 구별해야 하는 visual grounding 문제 추가로 이해도 강화
- 미등장 환경과 미등장 언어 표현에 대한 zero-shot 일반화 평가로 추상화 능력 검증

## Limitation & Further Study

- 시뮬레이션 환경에서만 평가되어 sim-to-real 전이(transfer) 성능이 검증되지 않음
- 제시된 MCIL 베이스라인이 충분히 강력하지 않아, 더 나은 방법론과의 비교로 벤치마크 가치 입증 필요
- 24시간의 제한된 플레이 데이터는 현실 규모의 다양성을 완전히 대표하지 못할 수 있음
- 자연어 지시의 의미적 다양성이나 모호성에 대한 구체적 분석 부재
- 후속 연구 방향: 실제 로봇에서의 성능 평가, transformer 기반 순차 모델링 등 더 강력한 에이전트 개발, 능동 학습(active learning) 기법 적용으로 데이터 효율성 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CALVIN은 자연어 기반 장기 로봇 조작의 표준화된 첫 벤치마크로서 로봇 학습 커뮤니티에 중대한 기여를 한다. 높은 평가 난이도와 유연한 설계로 미래 연구를 촉진할 것으로 기대되나, 시뮬레이션 환경의 한계와 현실 적용 검증이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — CALVIN의 장기간 언어 조건부 조작과 ALFRED의 자연어 지시 매핑은 언어 기반 로봇 작업 학습 벤치마크의 발전 과정이다.
- 🧪 응용 사례: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — LIBERO의 평생 로봇 학습 벤치마크는 CALVIN의 다단계 조작 작업을 지속적 학습 관점에서 확장한다.
- 🏛 기반 연구: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — MimicPlay의 장기간 모방 학습은 CALVIN의 언어 조건부 장기 작업 수행에 학습 방법론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — RLBench의 robot learning benchmark 개념을 language-conditioned policy learning과 장기간 조작 작업에 특화하여 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — 둘 다 장기간 로봇 작업을 위한 벤치마크이지만 CALVIN은 language conditioning에, RoboCerebra는 large-scale benchmark에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1457_LIBERO_Benchmarking_Knowledge_Transfer_for_Lifelong_Robot_Le/review]] — 둘 다 언어 조건 정책 학습 벤치마크이지만 LIBERO는 생애주기 학습에, CALVIN은 일반적인 정책 학습에 집중한다.
- 🔄 다른 접근: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — RLBench와 CALVIN 모두 언어 조건화된 로봇 학습 벤치마크이지만 태스크 복잡성과 평가 방식에서 차별화됩니다.
- 🏛 기반 연구: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — language-conditioned policy learning의 기초 벤치마크를 제공하여 RoboCerebra의 장기간 로봇 조작 작업 평가에 필요한 방법론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1591_Towards_Diverse_Behaviors_A_Benchmark_for_Imitation_Learning/review]] — CALVIN의 언어 조건부 정책 학습을 행동 다양성 평가로 확장한다.
- 🔄 다른 접근: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — CALVIN과 같이 언어 조건부 정책 학습을 위한 벤치마크이지만, VLABench는 더 대규모이고 다양한 태스크를 제공한다
- 🔗 후속 연구: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — ALFRED의 자연어 지시 매핑과 CALVIN의 장기간 언어 조건부 조작은 모두 언어 기반 로봇 작업 학습 벤치마크의 발전이다.
- 🔄 다른 접근: [[papers/1312_ARNOLD_A_Benchmark_for_Language-Grounded_Task_Learning_With/review]] — 언어 조건부 정책 학습을 위한 다른 벤치마크 접근법을 제시한다.
