---
title: "1453_Learning_Latent_Plans_from_Play"
authors:
  - "Corey Lynch"
  - "Mohi Khansari"
  - "Ted Xiao"
  - "Vikash Kumar"
  - "Jonathan Tompson"
date: "2019.03"
doi: ""
arxiv: ""
score: 4.0
essence: "인간의 비지도 원격조종 플레이 데이터로부터 자기감독 학습을 통해 잠재 계획 공간에서 행동을 조직화하고 재사용하여 다양한 조작 작업을 수행할 수 있는 Play-LMP 방법을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lynch et al._2019_Learning Latent Plans from Play.pdf"
---

# Learning Latent Plans from Play

> **저자**: Corey Lynch, Mohi Khansari, Ted Xiao, Vikash Kumar, Jonathan Tompson, Sergey Levine, Pierre Sermanet | **날짜**: 2019-03-05 | **URL**: [https://arxiv.org/abs/1903.01973](https://arxiv.org/abs/1903.01973)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Play-LMP: A single model that self-supervises control from play data, then generalizes to a wide*

인간의 비지도 원격조종 플레이 데이터로부터 자기감독 학습을 통해 잠재 계획 공간에서 행동을 조직화하고 재사용하여 다양한 조작 작업을 수행할 수 있는 Play-LMP 방법을 제안한다.

## Motivation

- **Known**: 로봇은 전문화된 개별 스킬(예: 그래스핑, 조작)을 학습할 수 있지만, 다양한 범용 스킬의 습득은 어렵다. 기존에는 명시적 보상 설계나 작업별 전문 정책 학습이 필요했다.
- **Gap**: 플레이 데이터는 전문가 시연보다 저렴하고 풍부하지만, 이를 효과적으로 활용하여 여러 작업에 일반화되는 제어 정책을 학습하는 방법이 부족하다.
- **Why**: 로봇이 실세계에서 다양한 변형된 작업들(예: 서로 다른 각도에서 서랍 열기)을 유연하게 수행하려면 작업 연속체에 대한 일반화가 필수적이며, 플레이 데이터는 이를 확장 가능하게 제공할 수 있다.
- **Approach**: Play-LMP는 플레이 데이터에서 행동 시퀀스 윈도우를 샘플링하여 plan recognition과 plan proposal 두 확률적 인코더로 잠재 계획 공간을 형성하고, 정책은 현재/목표 상태와 샘플된 잠재 계획으로 조건화되어 액션을 예측한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: The continuum of skills and its coverage. We advocate for learning the full continuum of skills*

- **데이터 효율성**: 동일한 수집 시간 대비 플레이 데이터가 전문가 시연보다 약 4.2배, 무작위 탐색보다 14.4배 많은 상호작용 공간을 커버함을 실증적으로 입증
- **작업 성능**: 라벨이 없는 플레이로 자기감독된 모델이 18개의 시각 조작 작업에서 개별 전문가 정책을 크게 능가
- **견고성 및 행동**: 플레이 감독 모델이 전문가 정책보다 섭동에 더 견고하며 재시도-까지-성공 행동을 자연스럽게 나타냄
- **자동 구조화**: 작업 레이블을 사용하지 않았음에도 불구하고 에이전트의 잠재 계획 공간이 기능적 작업 주변으로 자동 조직화됨

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Play-LMP: A single model that self-supervises control from play data, then generalizes to a wide*

- 플레이 데이터 메모리에서 무작위 시간 윈도우 샘플링
- Plan recognition 인코더: 전체 시퀀스(현재, 목표, 액션)를 받아 정확히 실행된 행동을 인식하는 분포 출력
- Plan proposal 인코더: 초기/최종 상태만으로부터 이들을 연결하는 가능한 모든 행동에 대한 분포 출력
- 두 분포 간의 KL divergence 최소화하여 plan proposal이 실제 실행된 행동에 높은 확률 할당하도록 형성
- 정책: 현재 상태, 목표 상태, 샘플된 잠재 계획으로 조건화되어 액션 시퀀스 재구성 학습
- 테스트 시: 현재/목표 상태로부터 plan distribution을 한 번 샘플링하여 폐루프 제어 실행

## Originality

- 비지도 플레이 데이터를 자기감독 학습의 기반으로 활용하는 개념적 전환
- Plan recognition과 plan proposal의 이원 인코더 구조로 다중양식 액션 분포를 명시적으로 모델링
- 작업 레이블 없이도 잠재 공간이 기능적 작업으로 자동 조직화되는 현상 발견
- Goal-conditioned imitation learning에서 긴 시간 수평선 조작 작업을 다루는 계층적 잠재 변수 모델 적용

## Limitation & Further Study

- 시뮬레이션된 테이블탑 환경에서만 평가되었으며 실제 로봇 플랫폼에서의 검증 부재
- 플레이 데이터 수집이 여전히 인간 조종에 의존하여 완전 자동화가 아님
- plan proposal에서 샘플링하는 방식이 단일 계획만 사용하므로, 복잡한 다중-계획 시나리오 처리의 한계 가능성
- 플레이 데이터의 질과 양이 성능에 미치는 영향에 대한 상세한 분석 부족
- 후속 연구로 실제 로봇 환경 적용, 자동 탐색 메커니즘 통합, 더 복잡한 장기 작업에 대한 확장성 검증이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 플레이 데이터라는 새로운 감독 신호를 통해 로봇 학습의 확장성 문제를 혁신적으로 접근했으며, 이원 인코더 구조와 자기감독 학습의 결합은 다중양식 제어 문제를 우아하게 해결한다. 시뮬레이션 환경에서의 강력한 실증적 결과와 명확한 제시에도 불구하고, 실제 로봇 적용을 통한 검증이 실용적 영향력을 판단하는 데 중요할 것으로 보인다.

## Related Papers

- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — 대규모 로봇 학습 데이터가 Play-LMP의 비지도 플레이 데이터 학습에 기반을 제공한다.
- 🔗 후속 연구: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — 플레이 데이터에서의 학습을 long-horizon imitation learning으로 더 체계화하고 발전시켰다.
- 🔄 다른 접근: [[papers/1330_CLAM_Continuous_Latent_Action_Models_for_Robot_Learning_from/review]] — 둘 다 연속적인 행동 학습이지만 Play-LMP는 잠재 계획에, CLAM은 연속 잠재 행동에 집중한다.
- 🔗 후속 연구: [[papers/1321_Bootstrap_Your_Own_Skills_Learning_to_Solve_New_Tasks_with_L/review]] — bootstrap learning을 latent plan space에서 확장하여 더 효율적인 기술 조합과 재사용을 달성할 수 있다.
- 🔄 다른 접근: [[papers/1448_Latent_Action_Pretraining_from_Videos/review]] — 둘 다 비지도 학습을 통한 행동 표현 학습을 다루지만 play data와 video data의 활용 방식 차이를 분석할 수 있다.
- 🔗 후속 연구: [[papers/1448_Latent_Action_Pretraining_from_Videos/review]] — play 데이터에서의 잠재 계획 학습을 인터넷 규모 비디오 사전학습과 결합하여 더 일반적인 행동 표현을 학습할 수 있다.
- 🔗 후속 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — MEM의 다중 스케일 메모리가 Learning Latent Plans from Play의 잠재적 계획 학습과 결합되어 더 효율적인 장기 로봇 제어를 실현한다.
- 🔄 다른 접근: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — 둘 다 인간 플레이 데이터를 활용하지만 hierarchical imitation learning과 latent plan learning의 접근법 차이를 비교할 수 있다.
- 🔗 후속 연구: [[papers/1310_Any-point_Trajectory_Modeling_for_Policy_Learning/review]] — Learning Latent Plans from Play의 라벨 없는 학습 개념을 trajectory modeling을 통한 policy learning으로 발전시켜 더 robust한 visuomotor 학습을 가능하게 합니다.
- 🔗 후속 연구: [[papers/1330_CLAM_Continuous_Latent_Action_Models_for_Robot_Learning_from/review]] — Learning Latent Plans from Play의 라벨 없는 학습 개념을 continuous latent action space와 joint training을 통한 실제 환경 grounding으로 발전시킨 연구입니다.
