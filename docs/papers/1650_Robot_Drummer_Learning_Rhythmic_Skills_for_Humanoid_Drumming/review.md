---
title: "1650_Robot_Drummer_Learning_Rhythmic_Skills_for_Humanoid_Drumming"
authors:
  - "Asad Ali Shahid"
  - "Francesco Braghin"
  - "Loris Roveda"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 인문형 로봇이 MIDI 악보를 기반으로 드럼을 연주하는 기술을 제시하며, Rhythmic Contact Chain 표현과 temporal decomposition을 활용한 reinforcement learning 프레임워크를 제안한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shahid et al._2025_Robot Drummer Learning Rhythmic Skills for Humanoid Drumming.pdf"
---

# Robot Drummer: Learning Rhythmic Skills for Humanoid Drumming

> **저자**: Asad Ali Shahid, Francesco Braghin, Loris Roveda | **날짜**: 2025-07-15 | **URL**: [https://arxiv.org/abs/2507.11498](https://arxiv.org/abs/2507.11498)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of the Robot Drummer: Starting from a raw MIDI drum track (left), each note-onset is first mapped to a*

본 논문은 인문형 로봇이 MIDI 악보를 기반으로 드럼을 연주하는 기술을 제시하며, Rhythmic Contact Chain 표현과 temporal decomposition을 활용한 reinforcement learning 프레임워크를 제안한다.

## Motivation

- **Known**: 최근 humanoid robotics는 motion imitation 기반의 학습으로 locomotion과 manipulation 기술을 발전시켰으나, 이는 주로 goal-driven 작업에 제한되어 있다. 음악 연주는 process-driven 작업으로 정밀한 타이밍과 장시간의 temporal coordination을 요구한다.
- **Gap**: 기존 RL 기반 음악 연주 연구는 단순화된 시스템(piano의 anthropomorphic hand 또는 2-DoF underactuated drum arm)에만 적용되었으며, humanoid 전신을 활용한 정밀한 드럼 연주 학습에 대한 연구가 부재하다.
- **Why**: 음악 공연과 같은 표현적(expressive) 도메인으로 humanoid robot의 역할을 확장하는 것은 창의적 로봇 제어의 새로운 경계를 의미하며, temporal precision, spatial coordination, dynamic adaptation을 동시에 요구하는 복잡한 제어 문제의 해결을 시연한다.
- **Approach**: 드럼 연주를 시간이 정해진 접촉 이벤트의 순차적 수행으로 공식화하고, 이를 Rhythmic Contact Chain으로 변환한다. 장시간 음악 공연을 고정 길이 segment로 분해하여 단일 policy로 병렬 학습함으로써 exploration 효율성을 높인다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: The humanoid robot demonstrates expressive drumming skills across three songs: In the top row, the robot plays j*

- **다양한 장르의 곡 연주**: 30개 이상의 rock, metal, jazz 트랙에서 높은 F1 score 달성
- **신흥 인간형 연주 전략**: cross-arm strikes와 adaptive stick assignments 같은 자발적 인간형 드럼 기술 발현
- **장시간 temporal coordination**: 분 단위 길이의 복잡한 리듬 패턴을 정밀하게 수행하는 능력 시연

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of the Robot Drummer: Starting from a raw MIDI drum track (left), each note-onset is first mapped to a*

- MIDI 파일에서 드럼 채널을 추출하고 각 note를 물리적 드럼으로 매핑
- 시간 인덱싱된 드럼 시퀀스를 one-hot 벡터로 인코딩하여 Rhythmic Contact Chain 구성
- 각 곡을 고정 길이 segment로 temporal decomposition
- Agent state를 다음 L개 contact goals, robot proprioception, stick/drum 공간 정보로 구성
- Dense rhythmic contact reward를 통해 각 contact 이벤트(정확, 오류, 누락)를 학습 신호로 활용
- Proportional-derivative controller를 통해 joint position target 생성

## Originality

- Rhythmic Contact Chain이라는 새로운 음악 표현 방식으로 RL에 적합한 형태로 변환
- Temporal decomposition 기법을 통해 장시간 process-driven 작업의 탐색 효율 문제 해결
- Dense rhythmic contact reward 설계로 스파스한 피드백 문제 개선
- Humanoid 전신의 다중 팔(multi-limb)을 활용한 드럼 연주의 첫 체계적 RL 적용

## Limitation & Further Study

- MIDI note에서 가장 빈번한 articulation만 선택하여 표현력이 제한됨 (다중 articulation 지원 필요)
- Song-specific MIDI-to-drum 매핑이 필요하여 새로운 곡에 대한 확장성 부족
- 실제 음악 연주의 표현력(dynamics, timing variation 등) 측면의 평가가 부족
- 단순 접촉 성공 여부만이 아닌 음악적 품질에 대한 정성적 평가 필요
- 다양한 drumming style(swing, shuffle 등) 적응에 대한 체계적 분석 부재

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 humanoid robotics에서 process-driven 창의적 작업으로의 확장을 의미 있게 시연하며, Rhythmic Contact Chain과 temporal decomposition이라는 실용적 기법을 통해 장시간 정밀 제어 문제를 효과적으로 해결한다. 30개 이상의 곡에서의 성공적 성과와 신흥 인간형 전략의 발현은 RL 기반 로봇 제어의 창의적 응용 가능성을 강력하게 보여준다.

## Related Papers

- 🔄 다른 접근: [[papers/1682_SMASH_Mastering_Scalable_Whole-Body_Skills_for_Humanoid_Ping/review]] — 드럼 연주와 탁구는 모두 리듬감과 정밀한 타이밍이 요구되는 휴머노이드 스포츠/예술 활동으로 유사한 temporal decomposition 접근법을 활용한다.
- 🏛 기반 연구: [[papers/1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control/review]] — Rhythmic Contact Chain과 temporal decomposition 기법이 실시간 캐릭터 제어를 위한 CAMDM의 조건부 생성 메커니즘에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/2003_Humanoid_Whole-Body_Badminton_via_Multi-Stage_Reinforcement/review]] — Robot Drummer는 MIDI 기반 드럼 연주를, Humanoid Whole-Body Badminton은 배드민턴 기술을 통해 리듬감 있는 휴머노이드 제어를 다르게 구현함
- 🏛 기반 연구: [[papers/1750_Vision_in_Action_Learning_Active_Perception_from_Human_Demon/review]] — Vision in Action의 능동적 지각 기반 인간 시연 학습이 Robot Drummer의 rhythmic skill 학습의 기초가 됨
- 🔗 후속 연구: [[papers/2047_Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Huma/review]] — Learning Athletic Humanoid Tennis Skills의 불완전한 인간 데이터 학습이 Robot Drummer의 temporal decomposition 기반 리듬 학습을 확장함
- 🔄 다른 접근: [[papers/1979_HITTER_A_HumanoId_Table_TEnnis_Robot_via_Hierarchical_Planni/review]] — 드럼 연주와 탁구라는 서로 다른 rhythmic skill을 다루는 접촉 기반 운동 제어 연구입니다.
- 🔗 후속 연구: [[papers/1653_RobotDancing_Residual-Action_Reinforcement_Learning_Enables/review]] — 리듬감과 접촉 제어가 춤 동작의 beat matching에도 적용될 수 있는 확장 가능성을 보여줍니다.
- 🔄 다른 접근: [[papers/1679_SkillMimic_Learning_Basketball_Interaction_Skills_from_Demon/review]] — 농구 상호작용과 드럼 연주 모두 rhythmic skill이지만 대상 객체와의 접촉 방식이 다릅니다.
- 🔄 다른 접근: [[papers/1682_SMASH_Mastering_Scalable_Whole-Body_Skills_for_Humanoid_Ping/review]] — 탁구와 드럼 연주는 모두 정밀한 타이밍과 리듬이 요구되는 휴머노이드 전신 스킬로 유사한 temporal control 기법을 공유한다.
- 🔄 다른 접근: [[papers/1701_Taming_Diffusion_Probabilistic_Models_for_Character_Control/review]] — CAMDM의 실시간 동적 제어와 드럼 연주의 temporal decomposition은 모두 시간적 조건부 모션 생성을 다루는 상호 보완적 접근법이다.
- 🔗 후속 연구: [[papers/2047_Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Huma/review]] — LATENT의 불완전한 인간 데이터 활용이 Robot Drummer의 리듬 스킬 학습과 결합되어 음악적 타이밍이 있는 스포츠 동작 학습 가능
- 🏛 기반 연구: [[papers/2151_Toward_Reliable_Sim-to-Real_Predictability_for_MoE-based_Rob/review]] — Robot crash course의 soft falling learning이 MoE 기반 robust locomotion에서 예외 상황 처리와 recovery 능력의 기술적 토대를 제공합니다.
