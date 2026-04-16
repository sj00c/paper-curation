---
title: "1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi"
authors:
  - "Yiran Qin"
  - "Enshen Zhou"
  - "Qichang Liu"
  - "Zhenfei Yin"
  - "Lu Sheng"
date: "2023.12"
doi: ""
arxiv: ""
score: 4.0
essence: "MP5는 Minecraft에서 장기-지평선 개방형 태스크를 해결하기 위해 MLLMs 기반의 다중모듈 embodied 시스템으로, active perception scheme을 통해 프로세스 의존성과 컨텍스트 의존성을 모두 처리한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Qin et al._2023_MP5 A Multi-modal Open-ended Embodied System in Minecraft via Active Perception.pdf"
---

# MP5: A Multi-modal Open-ended Embodied System in Minecraft via Active Perception

> **저자**: Yiran Qin, Enshen Zhou, Qichang Liu, Zhenfei Yin, Lu Sheng, Ruimao Zhang, Yu Qiao, Jing Shao | **날짜**: 2023-12-12 | **URL**: [https://arxiv.org/abs/2312.07472](https://arxiv.org/abs/2312.07472)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of module interaction in MP5. After receiving the task instruction, MP5 first utilizes Parser to gene*

MP5는 Minecraft에서 장기-지평선 개방형 태스크를 해결하기 위해 MLLMs 기반의 다중모듈 embodied 시스템으로, active perception scheme을 통해 프로세스 의존성과 컨텍스트 의존성을 모두 처리한다.

## Motivation

- **Known**: 최근 LLMs는 장기-지평선 태스크를 sub-objectives로 분해하는 데 성공했으나, 기존 접근법들은 정확한 장면 데이터를 가정하며 컨텍스트 의존적 실행에 취약하다.
- **Gap**: embodied 에이전트가 개방형 perception, 상황 인식 계획, 그리고 다중 모듈의 통합 스케줄링을 동시에 수행할 수 있는 시스템 설계가 부족하다.
- **Why**: 실제 embodied 환경에서 정확한 장면 정보 없이도 장기-지평선 개방형 태스크를 해결할 수 있는 robust 에이전트 개발이 embodied AI의 핵심 목표이기 때문이다.
- **Approach**: MP5는 Parser, Percipient, Planner, Performer, Patroller 5개 모듈을 설계하고, Percipient와 Patroller 간의 다중-라운드 active perception을 통해 상황-인식적 계획 및 실행을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. The process of finishing the task “kill a pig with a stone sward during the daytime near the water with grass *

- **프로세스 의존 태스크 성공률**: diamond-level 난제에서 22% 성공률 달성
- **컨텍스트 의존 태스크 성공률**: 4-6개의 주요 항목을 인식해야 하는 복잡한 장면 이해 태스크에서 91% 성공률 달성
- **개방형 태스크 해결**: 완전히 새로운 개방형 태스크에 대한 우수한 일반화 능력 시연
- **MineLLM 개발**: Minecraft 특화 multimodal LLM 도입으로 perception 정확도 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of module interaction in MP5. After receiving the task instruction, MP5 first utilizes Parser to gene*

- **Parser 모듈**: LoRA-augmented LLM으로 장기 태스크를 순차적 sub-objectives 목록으로 분해
- **Percipient 모듈**: LoRA-enabled MineLLM으로 관찰된 이미지에 대한 다양한 질문에 답변
- **Planner 모듈**: external Memory를 갖춘 LLM으로 sub-objective의 action sequence 설계 및 refinement
- **Performer 모듈**: action sequence를 환경에서 실행하며 Patroller와 빈번히 상호작용
- **Patroller 모듈**: Percipient, Planner, Performer의 응답을 검증하고 active perception을 조율하는 검사자 역할
- **Active Perception Scheme**: Patroller가 Planner와 Performer의 쿼리에 따라 Percipient와 다중-라운드 상호작용하여 context-aware 정보 추출

## Originality

- 기존의 all-seeing 가정을 제거하고 실제 embodied perception의 선택성과 목적-지향성을 반영한 active perception scheme 도입
- 단순 hierarchical decomposition을 넘어 context-aware execution을 위한 Patroller의 검증 메커니즘 설계
- Minecraft 특화 MineLLM 개발로 일반 MLLMs의 한계를 극복한 점
- 5개 모듈의 통합 인터페이스와 multi-round active perception을 통한 시스템적 혁신

## Limitation & Further Study

- 22% 프로세스 의존 태스크 성공률은 여전히 낮으며, 더 복잡한 multi-step 추론이 필요한 영역 개선 필요
- Minecraft라는 제한된 환경에서의 검증으로, 실제 로봇이나 현실 환경으로의 전이 가능성 검토 필요
- MineLLM의 학습 데이터 규모, 일반화 능력, 그리고 다른 domains로의 적용성에 대한 상세 분석 부족
- Active perception의 computational overhead와 latency에 대한 분석 및 최적화 방향 제시 필요
- 후속 연구로 real-world embodied agents에의 적용, 더 효율적인 perception 스케줄링, 그리고 multi-agent 시나리오 확장 고려

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MP5는 active perception scheme을 통해 process-dependent와 context-dependent 태스크를 통합적으로 처리하는 창의적인 접근법을 제시하며, MLLMs 기반 embodied AI의 실질적 발전을 보여준다. 다만 절대적 성능 수치와 실제 환경 전이 가능성에 대한 추가 검증이 요구된다.

## Related Papers

- 🏛 기반 연구: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — Minecraft 환경에서의 embodied agent 개발을 위한 기초 플랫폼을 제공하여 MP5의 다중모듈 시스템 구현에 필요한 환경적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — 시뮬레이션 환경에서의 instructable agent를 Minecraft의 개방형 환경으로 확장하여 더 복잡한 장기 지평선 작업에서의 적용을 다룬다.
- 🔄 다른 접근: [[papers/1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac/review]] — embodied reasoning에서 active perception vs visual search and reasoning이라는 서로 다른 인지 메커니즘 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — Voyager와 같이 Minecraft에서 개방형 태스크를 다루지만 MP5는 active perception과 다중모듈 시스템으로 차별화된다.
- 🏛 기반 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — MP5의 다중모듈 시스템이 확장한 memory-augmented multi-task agent의 기초
- ⚖️ 반론/비판: [[papers/1478_MineDreamer_Learning_to_Follow_Instructions_via_Chain-of-Ima/review]] — Minecraft에서 active perception vs imagination-based reasoning의 대조적 방법론
- 🔗 후속 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — Minecraft 환경에서의 멀티태스크 능력을 multi-modal embodied system으로 더 발전시킨 형태다.
- 🔄 다른 접근: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — Minecraft 기반 embodied agent에서 인터넷 지식 vs 다중모달 시스템의 다른 접근
- 🔗 후속 연구: [[papers/1478_MineDreamer_Learning_to_Follow_Instructions_via_Chain-of-Ima/review]] — MineDreamer가 MP5의 멀티모달 Minecraft 환경에서 Chain-of-Imagination을 통해 더욱 정교한 지시 추종 능력을 구현한다.
- 🔄 다른 접근: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — MP5는 SIMA와 같은 시뮬레이션 환경에서의 embodied AI이지만 Minecraft에서의 다중모달 시스템에 특화된다.
- 🔗 후속 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — MP5가 Voyager의 Minecraft 구체화된 시스템을 다중 모달 오픈엔디드 시스템으로 발전시켰다.
