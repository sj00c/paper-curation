---
title: "1321_Bootstrap_Your_Own_Skills_Learning_to_Solve_New_Tasks_with_L"
authors:
  - "Jesse Zhang"
  - "Jiahui Zhang"
  - "Karl Pertsch"
  - "Ziyi Liu"
  - "Xiang Ren"
date: "2023.10"
doi: ""
arxiv: ""
score: 4.0
essence: "BOSS는 기본 primitive 스킬 세트로부터 LLM의 지도를 받아 스킬 체이닝을 통해 복잡한 장기 작업을 수행할 수 있는 스킬 라이브러리를 자동으로 구축하는 방법론이다. 최소한의 감독으로 환경과의 상호작용을 통해 의미 있는 스킬 조합을 학습한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robot_Policy_Learning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Dexterous_Robot_Manipulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2023_Bootstrap Your Own Skills Learning to Solve New Tasks with Large Language Model Guidance.pdf"
---

# Bootstrap Your Own Skills: Learning to Solve New Tasks with Large Language Model Guidance

> **저자**: Jesse Zhang, Jiahui Zhang, Karl Pertsch, Ziyi Liu, Xiang Ren, Minsuk Chang, Shao-Hua Sun, Joseph J. Lim | **날짜**: 2023-10-16 | **URL**: [https://arxiv.org/abs/2310.10021](https://arxiv.org/abs/2310.10021)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: BOSS learns to execute a large set of useful, long-horizon skills with minimal supervision*

BOSS는 기본 primitive 스킬 세트로부터 LLM의 지도를 받아 스킬 체이닝을 통해 복잡한 장기 작업을 수행할 수 있는 스킬 라이브러리를 자동으로 구축하는 방법론이다. 최소한의 감독으로 환경과의 상호작용을 통해 의미 있는 스킬 조합을 학습한다.

## Motivation

- **Known**: 강화학습에서 장기 작업 학습은 전문가 시연이나 풍부한 보상 함수 같은 밀집 감독을 필요로 한다. 최근 LLM 기반 접근법은 사전학습된 스킬에 대해 top-down 계획은 수행하지만 폐쇄루프 정책 학습은 하지 않는다.
- **Gap**: 기존 LLM 기반 계획 방법은 고정된 저수준 스킬 정책만 사용하므로 환경 차이나 스킬 오류 축적에 취약하다. 또한 무감독 강화학습은 조작 작업의 장기 스킬 학습에서 의미 있는 행동 발견이 어렵다.
- **Why**: 로봇이 최소 감독으로 새로운 복잡 작업을 학습할 수 있다면 로봇 학습의 실용성과 확장성이 크게 향상된다. LLM의 상식 지식을 활용하면서도 환경 상호작용을 통해 robustness를 확보하는 것이 중요하다.
- **Approach**: BOSS는 두 단계로 구성된다: (1) 기본 primitive 스킬 정책을 IQL 오프라인 강화학습으로 사전학습, (2) 스킬 부트스트래핑 단계에서 LLM이 가이드하는 의미 있는 스킬 체인을 샘플링하고 환경 상호작용으로 학습하면서 새로운 스킬을 라이브러리에 추가한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: BOSS learns to execute a large set of useful, long-horizon skills with minimal supervision*

- **LLM 기반 스킬 부트스트래핑**: LLM이 실행된 스킬 체인을 보고 다음 의미 있는 스킬을 샘플링하도록 가이드하여 무작위 탐색보다 훨씬 효율적인 스킬 학습 달성
- **최소 감독 학습**: 기본 primitive 스킬 세트만으로 시작하여 추가 인간 감독 없이 수백 개의 장기 작업 수행 능력 확보
- **폐쇄루프 정책 학습**: 환경 상호작용을 통한 실제 정책 학습으로 스킬 오류 축적에 대한 robustness 향상
- **ALFRED 벤치마크 성능**: 기존 무감독 스킬 학습 방법과 naive 부트스트래핑 대비 새로운 환경의 장기 작업 zero-shot 실행에서 우수한 성능 입증
- **실제 로봇 검증**: 시뮬레이션 환경뿐만 아니라 실제 로봇에서도 방법론의 효과성 확인

## How

![Figure 1](figures/fig1.webp)

*Figure 1: BOSS learns to execute a large set of useful, long-horizon skills with minimal supervision*

- **언어 조건부 정책 사전학습**: 스파스 보상 함수와 언어 주석을 포함한 데이터셋 D_L에 대해 IQL을 사용하여 π(a|s, z) 형태의 언어 조건부 primitive 스킬 정책 학습
- **초기 스킬 샘플링**: 현재 상태에서 의미 있는 초기 스킬을 선택하기 위해 LLM 활용 (논문에서 구체적 방법 명시 필요)
- **LLM 기반 다음 스킬 가이드**: 현재까지 실행된 스킬 체인을 바탕으로 LLM이 의미 있는 다음 스킬에 대한 분포를 예측하고 샘플링
- **정책 업데이트**: 수집된 스킬 체인 실행 경험을 사용하여 정책과 critic 함수 V(s, z)를 온라인으로 업데이트 (IQL 기반)
- **새로운 스킬 추가**: 성공적으로 실행된 스킬 체인을 LLM으로 요약하여 새로운 스킬로 라이브러리 Z에 추가하고 반복적 부트스트래핑 수행
- **Zero-shot 작업 실행**: 부트스트래핑 완료 후 새로운 자연언어 지시에 대해 조건부 정책으로 미학습 장기 작업 실행

## Originality

- **LLM 지도 스킬 부트스트래핑의 혁신**: 기존 LLM 기반 계획의 open-loop 방식과 달리 환경 상호작용을 통한 폐쇄루프 정책 학습을 결합하는 새로운 패러다임 제시
- **스킬 라이브러리의 동적 확장**: 부트스트래핑 과정에서 스킬 체인을 자동 요약하여 라이브러리에 추가함으로써 점진적이고 확장 가능한 스킬 성장 메커니즘 구현
- **최소 감독 조건에서의 장기 작업 학습**: 기존 무감독 RL의 의미 있는 행동 발견 문제를 LLM의 상식 지식으로 해결하는 실용적 접근
- **실제 로봇 시스템의 연속성**: ALFRED 시뮬레이션에서 실제 로봇으로의 성공적 전이 시연으로 방법론의 실제 적용 가능성 증명

## Limitation & Further Study

- **기본 primitive 스킬 의존성**: 방법의 성공이 초기 사전학습된 스킬 세트의 품질과 다양성에 큰 영향을 받음. 적절한 기본 스킬 없이는 효과적인 부트스트래핑 어려움
- **LLM 의존성 및 비용**: LLM을 통한 지속적인 쿼리로 인한 계산 비용 증가 및 LLM의 성능 변동성 문제
- **스킬 요약의 자동성 부족**: 실행된 스킬 체인을 새로운 스킬로 정리하는 과정이 LLM에 의존하므로 요약의 정확성과 일관성 보장 부족
- **환경 특화성**: ALFRED와 같은 특정 가정형 환경에서 주로 검증되었으므로 다른 도메인 (예: 야외 로봇, 산업용 조작)에서의 일반화 가능성 미확인
- **후속 연구 방향**: (1) 더 robust한 스킬 체인 요약 방법 개발, (2) 더 효율적인 LLM 쿼리 전략 연구, (3) 다양한 도메인에서의 일반화 검증, (4) 부트스트래핑 수렴성과 최적성에 대한 이론적 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: BOSS는 LLM의 상식 지식과 강화학습의 환경 상호작용을 창의적으로 결합하여 최소 감독으로 장기 복잡 작업을 학습하는 문제의 실용적이고 확장 가능한 해결책을 제시한다. 실험 검증과 실제 로봇 시연을 통해 높은 신뢰성을 확보했으며, 로봇 학습 분야의 중요한 기여이다.

## Related Papers

- 🔗 후속 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — BOSS의 LLM 기반 스킬 체이닝과 Plan-Seq-Learn의 언어 모델 가이드 RL은 모두 복잡한 장기 작업 해결의 계층적 접근법이다.
- 🔄 다른 접근: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — BOSS의 스킬 라이브러리 자동 구축과 Voyager의 오픈엔디드 에이전트는 자율적 스킬 획득의 서로 다른 방법론이다.
- 🏛 기반 연구: [[papers/1444_Language_to_Rewards_for_Robotic_Skill_Synthesis/review]] — Language to Rewards의 언어 기반 보상 설계는 BOSS의 LLM 가이드 스킬 학습에 핵심적인 기반 메커니즘을 제공한다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — 언어 모델을 구체화 제어에 활용하는 기초적인 접근 방식을 제시합니다.
- 🔄 다른 접근: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — 둘 다 hierarchical action을 다루지만 BOSS는 스킬 체이닝에, RT-H는 language-guided action hierarchy에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1462_LOTUS_Continual_Imitation_Learning_for_Robot_Manipulation_Th/review]] — 둘 다 새로운 기술 학습이지만 LOTUS는 지속적 모방에, Bootstrap은 자체 기술 부트스트래핑에 집중한다.
- 🔗 후속 연구: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — bootstrap learning을 latent plan space에서 확장하여 더 효율적인 기술 조합과 재사용을 달성할 수 있다.
