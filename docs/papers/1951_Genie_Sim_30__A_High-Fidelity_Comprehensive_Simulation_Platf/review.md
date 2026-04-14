# Genie Sim 3.0 : A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot

> **저자**: Chenghao Yin, Da Huang, Di Yang, Jichao Wang, Nanshu Zhao, Chen Xu, Wenjun Sun, Linjie Hou, Zhijun Li, Junhui Wu, Zhaobo Liu, Zhen Xiao, Sheng Zhang, Lei Bao, Rui Feng, Zhenquan Pang, Jiayu Li, Qian Wang, Maoqing Yao | **날짜**: 2026-01-05 | **URL**: [https://arxiv.org/abs/2601.02078](https://arxiv.org/abs/2601.02078)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of Genie Sim 3.0. Genie Sim 3.0 is a full-cycle robotic simulation platform that integrates environment*

Genie Sim 3.0은 LLM 기반의 자동 장면 생성, VLM 기반의 자동 평가, 10,000시간 이상의 합성 데이터를 통합한 휴머노이드 로봇 조작용 고충실도 시뮬레이션 플랫폼이다.

## Motivation

- **Known**: 로봇 학습은 대규모 다양한 훈련 데이터와 신뢰할 수 있는 평가 벤치마크를 필요로 하며, 현존 시뮬레이션 벤치마크들은 fragmentation, 좁은 범위, 불충분한 sim-to-real transfer 능력을 가지고 있다.
- **Gap**: 고충실도 시뮬레이션 환경 구축에는 전문가의 수작업이 필요하고, 자동 생성은 미세한 제어와 재현성이 부족하며, 현재의 고정된 메트릭 기반 평가는 정교한 작업 완성도를 포착하지 못한다.
- **Why**: 합성 데이터의 대규모 확보와 자동화된 평가는 물리적 데이터 수집의 비용·확장성 문제를 해결하여 로봇 학습 모델의 개발 속도와 일반화 성능을 크게 향상시킬 수 있다.
- **Approach**: LLM 기반 Genie Sim Generator로 자연언어 지시에서 고충실도 장면을 실시간 생성하고, LLM과 VLM을 이용한 자동화된 작업 및 평가 시나리오 생성을 통해 대규모 벤치마크를 구축한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of Genie Sim 3.0. Genie Sim 3.0 is a full-cycle robotic simulation platform that integrates environment*

- **Genie Sim Generator**: 자연언어 인터페이스로 고충실도 시뮬레이션 장면을 실시간 생성하며, 다중 라운드 대화를 통한 반복적 개선을 지원
- **다차원 장면 일반화**: 조명, 배경, 레이아웃, 포즈, 궤적, 센서 노이즈, 로봇 형태 등을 매개변수화하여 수 분 내에 다양한 시나리오 생성
- **자동화된 평가 벤치마크**: LLM으로 100,000개 이상의 작업 지시 및 평가 프로토콜을 자동 생성하고 VLM으로 채점하여 의미론적 이해, 공간 추론, 실행 능력을 평가
- **대규모 합성 데이터셋**: 200개 이상의 작업에 걸친 10,000시간 이상의 합성 데이터를 공개
- **sim-to-real 전이 검증**: 합성 데이터가 제어된 조건 하에서 실세계 데이터의 실질적 대체재임을 실험적으로 입증

## How


- LLM을 활용한 자연언어 기반 장면 생성 파이프라인 개발
- 5,140개의 시뮬레이션 준비 객체 자산 및 의미론적 검색 시스템 구축
- 다중 라운드 대화 기반 반복적 장면 개선 및 다차원 domain randomization 구현
- LLM 기반 작업 및 평가 프로토콜 자동 생성
- VLM 기반 자동화된 평가 파이프라인 구축
- 텔레조작 및 자동화 기반의 이중 모드 데이터 수집 파이프라인 개발
- 3D reconstruction과 visual generative synthesis를 통한 고충실도 시뮬레이션

## Originality

- 로봇 시뮬레이션에서 LLM 기반 장면 생성의 첫 대규모 적용
- VLM을 이용한 자동화된 평가 파이프라인의 개척 - 기존 수작업 평가를 완전 자동화
- 자연언어 인터페이스를 통한 다차원 domain randomization의 직관적 제어 메커니즘
- 100,000개 이상의 평가 시나리오를 통한 다각적 역량 프로파일링 벤치마크의 최초 도입
- 10,000시간 규모의 합성 데이터셋이 실제 sim-to-real 전이에 효과적임을 실증

## Limitation & Further Study

- 현재 구현이 특정 제어 조건 하의 sim-to-real 전이만 검증했으므로, 더 복잡한 미제어 환경에서의 전이 성능 미확인
- VLM 기반 평가의 accuracy와 robustness에 대한 정량적 벤치마킹 부족 - VLM 판단의 일관성과 인간 평가와의 상관성 분석 필요
- 로봇 형태론적 다양성(humanoid 외 다른 형태)에 대한 확장성 제한
- 합성 데이터의 시각적 분포가 특정 렌더링 스타일에 편향될 가능성
- 후속 연구로는 이질적 로봇 플랫폼으로의 일반화, VLM 평가의 신뢰성 강화, 동적 객체 상호작용과 물리 시뮬레이션 정확도 개선이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Genie Sim 3.0은 LLM/VLM을 활용한 자동화된 장면 생성, 평가, 데이터 수집의 엔드-투-엔드 통합을 통해 로봇 학습의 확장성 문제를 해결하는 실질적이고 혁신적인 플랫폼이며, 10,000시간의 공개 합성 데이터셋과 100,000개 평가 시나리오는 커뮤니티에 중대한 기여를 한다.
