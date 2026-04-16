---
title: "1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S"
authors:
  - "Linxi Fan"
  - "Guanzhi Wang"
  - "Yunfan Jiang"
  - "Ajay Mandlekar"
  - "Yuncong Yang"
date: "2022.06"
doi: ""
arxiv: ""
score: 4.0
essence: "MineDojo는 Minecraft 게임을 기반으로 수천 개의 개방형 작업, 인터넷 규모의 멀티모달 지식베이스(YouTube 영상, Wiki, Reddit), 그리고 사전학습된 비디오-언어 모델을 보상함수로 활용하는 에이전트 학습 알고리즘을 통합하여 일반화 능력을 갖춘 embodied agent를 개발하는 프레임워크이다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Diffusion-Based_Robot_Control"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Fan et al._2022_MineDojo Building Open-Ended Embodied Agents with Internet-Scale Knowledge.pdf"
---

# MineDojo: Building Open-Ended Embodied Agents with Internet-Scale Knowledge

> **저자**: Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, Anima Anandkumar | **날짜**: 2022-06-17 | **URL**: [https://arxiv.org/abs/2206.08853](https://arxiv.org/abs/2206.08853)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: MINEDOJO is a novel framework for developing open-ended, generally capable agents*

MineDojo는 Minecraft 게임을 기반으로 수천 개의 개방형 작업, 인터넷 규모의 멀티모달 지식베이스(YouTube 영상, Wiki, Reddit), 그리고 사전학습된 비디오-언어 모델을 보상함수로 활용하는 에이전트 학습 알고리즘을 통합하여 일반화 능력을 갖춘 embodied agent를 개발하는 프레임워크이다.

## Motivation

- **Known**: Atari, Go 같은 전문 영역에서 자율 에이전트가 높은 성과를 달성했지만, 이들은 고립된 환경에서 제한된 수동 설계 목표로 학습하여 광범위한 작업 일반화에 실패한다.
- **Gap**: 기존 에이전트는 (1) 다양한 개방형 작업을 지원하는 환경, (2) 대규모 멀티모달 사전 지식, (3) 유연하고 확장 가능한 에이전트 아키텍처 중 하나 이상이 부족하여 일반화 가능한 에이전트 개발이 제한되어 있다.
- **Why**: 인간처럼 지속적으로 학습하고 적응할 수 있는 일반화된 embodied agent는 AI 분야의 장기적 목표이며, 이는 다양한 실제 응용(로봇공학, 게임 AI 등)에 필수적이다.
- **Approach**: MineDojo는 개방형 Minecraft 환경에 수천 개의 자연어 작업을 정의하고, 100만 이상의 Minecraft 플레이어가 생성한 730K+ YouTube 영상, 6K+ Wiki 페이지, 340K+ Reddit 포스트를 수집한 뒤, CLIP 스타일의 contrastive video-language model (MineClip)을 이용해 자동 보상함수를 학습하여 에이전트를 훈련한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Visualization of our agent’s learned behaviors on four selected tasks. Leftmost texts are the*

- **시뮬레이션 플랫폼**: MineRL Challenge 대비 두 자리 수 규모로 확대된 1,581개의 programmatic 작업과 creative 작업들로 구성된 벤치마크 제공
- **지식베이스**: 730K+ YouTube 영상(시간 정렬 자막 포함), 6K+ Wiki 페이지, 340K+ Reddit 멀티미디어 포스트로 구성된 인터넷 규모 데이터셋 구축
- **학습 알고리즘**: 사전학습된 video-language model을 보상함수로 활용하여 수동 보상 설계 없이 자연언어 작업 수행 가능
- **평가 프로토콜**: YouTube 영상에서 사전학습된 대규모 video-language model을 활용한 자동 평가 메트릭 제안(Inception score, FID score에서 영감)
- **성능**: 12개 실험 작업의 대다수를 해결했으며, 수동 설계 보상 대비 최대 73% 성공률 개선 달성

## How

![Figure 4](figures/fig4.webp)

*Figure 4: Algorithm design. MINECLIP is a contrastive video-language model pre-trained on*

- Minecraft의 three worlds (Overworld, Nether, End)를 모두 지원하도록 MineRL 기반 시뮬레이터 확장
- Programmatic 작업(자동 검증 가능)과 Creative 작업(자동 검증 불가능)의 두 범주로 작업 정의
- GPT-3를 활용하여 YouTube 튜토리얼에서 채굴한 아이디어를 기반으로 창의적 작업 정의 자동화
- 730K+ Minecraft YouTube 영상과 시간 정렬 자막을 수집하여 MineClip (contrastive video-language model) 훈련
- MineClip의 learned correlation score를 개방어휘(open-vocabulary) 멀티태스크 보상함수로 활용하여 RL 훈련
- 자연언어 작업 지정에 따라 에이전트가 조건부로 행동하는 unified observation/action space 설계
- Human scoring과 보완적 성질의 learned evaluation metric을 제안하여 creative 작업 평가

## Originality

- **개방형 환경과 규모**: Minecraft의 procedural generation을 활용하여 기존 벤치마크(MineRL, 161개)보다 두 자리 수 많은 개방형 작업 구성
- **인터넷 규모 데이터 체계적 구축**: Minecraft 커뮤니티의 집단 지식을 구조화하여 다중 소스(YouTube, Wiki, Reddit) 통합 지식베이스 구성
- **Video-language 모델 기반 보상학습**: CLIP-style contrastive learning을 영상-텍스트 정렬에 활용하여 밀집 보상 설계 없이 개방어휘 보상함수 학습
- **자동 평가 프로토콜**: 생성형 AI(이미지 품질 평가 메트릭 영감) 평가 방식을 embodied agent 평가에 적용하여 human evaluation의 비용 문제 해결
- **Unified agent architecture**: 모든 작업에 동일한 observation/action space와 natural language conditioning을 적용하여 Transformer pre-training 패러다임 활용 가능 설계

## Limitation & Further Study

- Learned evaluation metric이 human judgment와의 합의도가 검증되었지만, 실제 creative 작업의 복잡한 성공 기준을 완벽히 포착하지 못할 가능성
- 현재 에이전트는 12개 작업에 대해 평가되었으므로, 더 광범위한 작업 범위에서의 일반화 성능 검증 필요
- Minecraft 도메인에 특화된 프레임워크로, 다른 embodied environment(로봇공학, 다른 게임)로의 전이 가능성 미검토
- MineClip 모델의 학습에 사용된 YouTube 데이터의 편향(특정 플레이 스타일, 언어 편향) 영향 분석 부재
- 긴 지평(long-horizon) creative 작업에 대한 구체적 성공 사례와 실패 사례 분석 필요
- 후속연구: 다중 모달리티 통합(사운드, 3D 기하학), 연속 학습(continual learning) 능력 강화, 다른 도메인 적응 가능성 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MineDojo는 개방형 환경, 인터넷 규모 지식베이스, 대규모 사전학습 모델을 통합하여 일반화된 embodied agent 연구의 완성도 높은 프레임워크를 제공하며, 전체 코드와 데이터를 공개함으로써 커뮤니티 기여도 우수하다. 다만 다른 도메인 전이 가능성 검증과 더 복잡한 작업에서의 성능 확장이 향후 과제이다.

## Related Papers

- 🔗 후속 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — MineDojo의 open-ended agent 개념을 Voyager에서 더 발전시킨 확장 연구
- 🏛 기반 연구: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — MineDojo가 활용하는 generative interactive environment의 기초 개념
- 🔄 다른 접근: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — Minecraft 기반 embodied agent에서 인터넷 지식 vs 다중모달 시스템의 다른 접근
- 🔄 다른 접근: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — MineDojo는 Minecraft 환경에서 구체적인 embodied agent를 학습시키는 반면, Genie는 범용적인 가상 세계 생성에 중점을 둡니다.
- 🔗 후속 연구: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — MineDojo의 오픈엔디드 환경 개념을 LLM 기반 로봇 시뮬레이션 작업 생성으로 발전시켰다.
- 🏛 기반 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — 인터넷 데이터로 학습된 embodied agent의 개념이 GLAM의 LLM agent 설계에 기반이 된다.
- 🏛 기반 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — MineDojo의 Minecraft 환경과 오픈월드 에이전트 개념이 JARVIS-1의 멀티태스크 학습 기반을 제공함
- 🏛 기반 연구: [[papers/1478_MineDreamer_Learning_to_Follow_Instructions_via_Chain-of-Ima/review]] — MineDreamer의 Chain-of-Imagination이 MineDojo의 개방형 환경에서 제공되는 다양한 Minecraft 작업을 체계적으로 처리하는 방법론을 제시한다.
- 🏛 기반 연구: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — Minecraft 환경에서의 embodied agent 개발을 위한 기초 플랫폼을 제공하여 MP5의 다중모듈 시스템 구현에 필요한 환경적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — MineDojo는 SIMA가 활용하는 게임 환경 기반 embodied AI 학습의 기반이 되는 오픈엔디드 환경을 제공한다.
- 🏛 기반 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — MineDojo가 제공하는 Minecraft 환경과 태스크 프레임워크가 Voyager의 개발과 평가에 기반이 되었다
- 🧪 응용 사례: [[papers/1353_Describe_Explain_Plan_and_Select_Interactive_Planning_with_L/review]] — DEPS의 대화형 계획 방식을 MineDojo 환경에서 실제로 적용하고 검증할 수 있는 플랫폼
- 🔗 후속 연구: [[papers/1417_GRUtopia_Dream_General_Robots_in_a_City_at_Scale/review]] — MineDojo의 인터넷 규모 데이터 개념을 3D 도시 환경으로 확장하여 더 현실적인 로봇 학습 환경을 구축한다.
