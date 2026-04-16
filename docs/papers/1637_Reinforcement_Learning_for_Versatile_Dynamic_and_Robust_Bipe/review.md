---
title: "1637_Reinforcement_Learning_for_Versatile_Dynamic_and_Robust_Bipe"
authors:
  - "Zhongyu Li"
  - "Xue Bin Peng"
  - "Pieter Abbeel"
  - "Sergey Levine"
  - "Glen Berseth"
date: "2024.01"
doi: ""
arxiv: ""
score: 4.0
essence: "이족 로봇의 다양한 동적 보행 기술(걷기, 뛰기, 점프)을 통합적으로 제어하기 위해 dual-history 아키텍처를 갖춘 심화강화학습 프레임워크를 제시하고, 시뮬레이션에서 실제 로봇(Cassie)으로 무튜닝 전이 배포를 성공시켰다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2024_Reinforcement Learning for Versatile, Dynamic, and Robust Bipedal Locomotion Control.pdf"
---

# Reinforcement Learning for Versatile, Dynamic, and Robust Bipedal Locomotion Control

> **저자**: Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, Koushil Sreenath | **날짜**: 2024-01-30 | **URL**: [https://arxiv.org/abs/2401.16889](https://arxiv.org/abs/2401.16889)

---

## Essence


이족 로봇의 다양한 동적 보행 기술(걷기, 뛰기, 점프)을 통합적으로 제어하기 위해 dual-history 아키텍처를 갖춘 심화강화학습 프레임워크를 제시하고, 시뮬레이션에서 실제 로봇(Cassie)으로 무튜닝 전이 배포를 성공시켰다.

## Motivation

- **Known**: 이족 로봇 보행 제어는 수십 년 연구되었으나, 언더액추에이션 동역학, 비선형성, 접촉 불연속성, 주기/비주기 운동의 다양성으로 인해 일반화된 제어 솔루션 개발이 미해결 과제로 남아있다.
- **Gap**: 기존 연구는 단일 보행 기술에 집중하거나 전체 동역학을 활용하지 못했으며, 시간 변화하는 동역학 적응성과 여러 기술 간 강건성을 동시에 달성하는 통합 프레임워크가 부족하다.
- **Why**: 인간 환경은 이족 보행에 최적화되어 있으므로, 다양한 동적 보행 기술을 강건하게 수행하는 이족 로봇은 실제 환경 배포의 핵심 요구사항이며, 이는 로봇 연구의 큰 병목 문제이다.
- **Approach**: Model-free RL을 사용하여 long-term과 short-term I/O 히스토리를 모두 활용하는 dual-history 정책 아키텍처를 설계하고, 다중 단계 학습 프레임워크와 task randomization을 통해 적응성과 강건성을 확보한다.

## Achievement


- **일반화된 이족 보행 제어 프레임워크**: 주기적 기술(걷기, 뛰기)부터 비주기적 기술(점프), 정적 기술(서기)까지 단일 RL 프레임워크로 통합 제어하며 실제 로봇 무튜닝 배포 성공
- **Dual-history 아키텍처**: Non-recurrent RL 정책에 명시적 장단기 I/O 히스토리 및 로봇 크기 정보를 통합하여 다양한 보행 기술에서 최첨단 성능 달성
- **적응성 실증**: 시간 불변 동역학 변화와 접촉 이벤트 같은 시간 변화 현상 모두에 대한 적응성을 시뮬레이션과 실제 로봇에서 검증
- **Task randomization 강건성**: 동역학 무작위화 외에 다양한 과제 학습을 통한 강건성 개선으로 외부 방해에 대한 규응성 달성
- **광범위한 실제 검증**: Cassie 로봇으로 안정적 서기 회복, 다양한 속도 보행, 400m 대시, 높이뛰기 및 멀리뛰기 등 다양한 보행 기술 실제 구현

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: The proposed RL-based controller architecture that leverages*

- Robot proprioceptive I/O를 long-term 히스토리 인코더와 short-term 히스토리로 분리하여 정책 입력 구성
- Base 정책 학습 시 short-term 히스토리와 long-term 히스토리 인코더를 관절(joint) 학습하는 다중 단계 학습 전략 적용
- 환경 동역학 매개변수와 과제 명령(목표 속도, 점프 거리 등)을 광범위하게 무작위화하여 시뮬레이션 학습 수행
- 학습된 정책을 실제 Cassie 로봇에 직접 배포하여 추가 실제 세계 튜닝 없이 전이 학습 성공 검증
- 다양한 외부 방해(푸시, 경사지형 변화 등)에 대한 강건성 실험 및 적응성 분석 수행

## Originality

- Dual-history 아키텍처는 기존 recurrent 정책과 달리 non-recurrent 방식으로 명시적 장단기 정보 통합으로 새로운 설계
- Task randomization을 단순 동역학 무작위화와 구분하여 강건성 향상의 독립적 원인으로 식별한 점이 혁신적
- 단일 RL 프레임워크로 주기/비주기/정적 보행을 통합하는 일반화 접근이 기존 기술별 개별 제어와 차별화
- RL 제어기의 시간 변화하는 동역학 적응성을 실증적으로 상세 분석한 것은 제어 이론과 RL 연결의 새로운 시도

## Limitation & Further Study

- 시뮬레이션-현실 간 차이(Sim2Real gap)를 완전히 해결하지 못했으며, task randomization의 광범위함이 필요했음은 학습 효율성 문제를 시사
- Dual-history 아키텍처의 장기 히스토리 길이 선택에 대한 체계적 가이드라인 부재 및 하이퍼파라미터 민감도 분석 부족
- Cassie에 특화된 검증이므로 다른 이족 플랫폼(예: Atlas, Boston Dynamics Figure)에서의 일반화 검증 필요
- 400m 대시 같은 장시간 운동에서의 에너지 소비, 열 관리, 장기 안정성에 대한 분석 부족
- 후속 연구로 더 복잡한 지형(계단, 울퉁불퉁한 지표), 다중 연락 모드(미끄러짐), 소형 이족 로봇 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이족 로봇 제어라는 도전적 과제에서 dual-history 아키텍처와 task randomization을 통해 통합 RL 프레임워크를 달성하고, 광범위한 실제 로봇 실험으로 다양한 동적 보행 기술의 강건한 구현을 입증한 우수한 연구이다. 다만 아키텍처 설계 선택의 이론적 근거 강화와 다른 플랫폼으로의 확장성 검증이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — Robust and Versatile Bipedal Jumping의 강화학습 기반 점프 제어가 본 논문의 다양한 동적 보행 기술을 확장함
- 🔄 다른 접근: [[papers/2061_Learning_Sim-to-Real_Humanoid_Locomotion_in_15_Minutes/review]] — 두 논문 모두 이족 로봇 sim-to-real을 다루지만, 본 논문은 dual-history 아키텍처를, Learning Sim-to-Real은 15분 학습에 중점을 둠
- 🧪 응용 사례: [[papers/1925_FastStair_Learning_to_Run_Up_Stairs_with_Humanoid_Robots/review]] — FastStair의 계단 오르기 기술이 본 논문의 versatile dynamic locomotion 프레임워크를 실제 계단 환경에 적용한 사례임
- 🔄 다른 접근: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — 두 논문 모두 이족 로봇의 동적 운동을 강화학습으로 학습하지만, 점프와 일반적인 이족보행이라는 다른 태스크를 다룬다.
- 🔄 다른 접근: [[papers/1940_Gait-Conditioned_Reinforcement_Learning_with_Multi-Phase_Cur/review]] — 둘 다 다양한 gait pattern 학습을 다루지만, Gait-Conditioned는 단일 recurrent policy에서의 통합 접근법을, Versatile Bipedal은 별도 제어 전략을 사용합니다.
- 🔗 후속 연구: [[papers/2045_Learning_agile_and_dynamic_motor_skills_for_legged_robots/review]] — 사족 로봇의 민첩한 동적 기술이 이족 로봇의 다양하고 강건한 보행으로 확장될 수 있다.
- 🏛 기반 연구: [[papers/2127_Optimizing_Bipedal_Locomotion_for_The_100m_Dash_With_Compari/review]] — Reinforcement learning for versatile bipedal locomotion이 Cassie 로봇의 100m 대시 최적화에서 이족 보행의 다양한 매개변수 조정의 기술적 기반을 제공합니다.
