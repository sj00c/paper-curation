---
title: "1478_MineDreamer_Learning_to_Follow_Instructions_via_Chain-of-Ima"
authors:
  - "Enshen Zhou"
  - "Yiran Qin"
  - "Zhenfei Yin"
  - "Yuzhou Huang"
  - "Ruimao Zhang"
date: "2024.03"
doi: ""
arxiv: ""
score: 4.0
essence: "MineDreamer는 Chain-of-Imagination(CoI) 메커니즘을 통해 MLLM과 diffusion model을 활용하여 Minecraft에서 자연어 지시를 단계별로 상상하고 실행하는 embodied agent이다. CoI는 현재 상태에 맞춘 시각적 프롬프트를 반복적으로 생성하여 지시 추종 능력을 크게 향상시킨다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhou et al._2024_MineDreamer Learning to Follow Instructions via Chain-of-Imagination for Simulated-World Control.pdf"
---

# MineDreamer: Learning to Follow Instructions via Chain-of-Imagination for Simulated-World Control

> **저자**: Enshen Zhou, Yiran Qin, Zhenfei Yin, Yuzhou Huang, Ruimao Zhang, Lu Sheng, Yu Qiao, Jing Shao | **날짜**: 2024-03-18 | **URL**: [https://arxiv.org/abs/2403.12037](https://arxiv.org/abs/2403.12037)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Comparison between MineDreamer and previous studies. In “Chop*

MineDreamer는 Chain-of-Imagination(CoI) 메커니즘을 통해 MLLM과 diffusion model을 활용하여 Minecraft에서 자연어 지시를 단계별로 상상하고 실행하는 embodied agent이다. CoI는 현재 상태에 맞춘 시각적 프롬프트를 반복적으로 생성하여 지시 추종 능력을 크게 향상시킨다.

## Motivation

- **Known**: 최근 foundation model들이 sequential decision-making에서 지시 추종 능력을 보이고 있으며, VPT와 같은 대규모 사전학습 모델들이 존재한다. 그러나 기존 방법들은 추상적이고 순차적인 자연어 지시를 안정적으로 따르는 데 실패한다.
- **Gap**: 텍스트 지시는 추상적이고 순차적이기 때문에 현재 상태를 고려하여 구체적인 시각적 프롬프트로 변환되어야 한다. 기존 방법들은 단일 텍스트 입력으로 안정적인 행동 생성을 하지 못한다.
- **Why**: 일반화된 embodied agent가 다양한 지시를 인간처럼 따를 수 있다면 복잡한 열린 세계 작업을 자동화할 수 있으며, 이는 AI 에이전트의 실용성과 적응성을 크게 향상시킨다.
- **Approach**: MineDreamer는 Imaginator가 지시와 현재 관찰을 기반으로 미래 목표를 상상하고, Prompt Generator가 이를 정밀한 시각적 프롬프트로 변환하며, PolicyNet(VPT)이 이 프롬프트를 따라 행동을 생성하는 3단계 구조를 채택한다. 이 과정을 반복하는 CoI 메커니즘이 핵심이다.

## Achievement

![Figure 5](figures/fig5.webp)

*Fig. 5: Performance on Programmatic Evaluation. MineDreamer surpasses the*

- **Chain-of-Imagination 메커니즘**: Sequential decision-making 영역에 '자기 다중 턴 상호작용'을 도입하여 에이전트가 지시를 안정적으로 따르도록 함", '**MLLM-향상된 diffusion model**: 물리 법칙과 환경 이해를 포함한 고품질 상상을 생성하여 현재 상태에 맞는 정밀한 시각적 프롬프트 제공
- **Goal Drift Collection 방법**: 대규모 자동수집된 egocentric embodied 데이터로 Imaginator 학습
- **성능 향상**: 최고 성능의 generalist agent baseline 대비 거의 2배의 성능 달성(단일 및 다중 단계 지시 모두)

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The Overview of Chain-of-Imagination. The Imaginator imagines a goal*

- Imaginator: Parameter-efficiently fine-tuned diffusion model이 MLLM의 시각적 추론 능력을 활용하여 현재 상태와 지시에 기반한 미래 목표 이미지 생성
- Prompt Generator: 현재 관찰, 미래 상상, 지시를 활용하여 latent visual prompt 재구성
- PolicyNet: 사전학습된 VPT 모델이 latent visual prompt를 조건으로 하여 저수준 제어 행동 생성
- Goal Drift Collection: 타임스탬프 t*에서 다수의 (현재 관찰, 미래 상상) triplet 형성으로 대규모 데이터 자동 수집
- 반복적 CoI 메커니즘: Imaginator와 PolicyNet 간 다중 턴 상호작용을 통해 현재 상태에 맞춘 시각적 프롬프트 순환적 생성

## Originality

- **CoI 메커니즘의 혁신성**: 단순 텍스트-행동 직접 매핑 대신 중간 시각적 상상 단계를 도입하여 상태-의존적 추론 능력 추가
- **MLLM과 diffusion model의 통합**: 기존 diffusion 기반 embodied 제어는 고정 환경에 제한되었으나, MLLM을 활용하여 열린 세계 환경의 물리 규칙과 환경 이해를 동적으로 반영
- **Goal Drift Collection의 자동화**: 수동 데이터 수집 대신 자동화된 방법으로 대규모 egocentric embodied 데이터 획득
- **Self multi-turn interaction**: Sequential decision-making에서 자기 상호작용의 개념을 처음 도입하여 단계적 지시 추종 구현

## Limitation & Further Study

- Minecraft 환경에 한정된 평가로 실제 로봇이나 다른 시뮬레이터로의 일반화 가능성 미검증
- Goal Drift Collection 방법의 자동화 과정에서 노이즈나 오류 데이터 포함 가능성에 대한 분석 부족
- Imaginator의 상상 생성 오류가 누적되어 PolicyNet의 행동 생성 오류로 전파될 수 있으나, 이에 대한 오류 분석 및 대응 메커니즘 미흡
- 장시간 복잡한 다중 단계 작업에 대한 성능 평가 제한적
- **후속 연구**: 실제 로봇 환경에서의 적응, 오류 전파 완화를 위한 robust한 피드백 메커니즘, 더 긴 시간 지평에서의 안정성 향상 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MineDreamer는 Chain-of-Imagination 메커니즘을 통해 자연어 지시 추종 에이전트의 설계에 창의적인 접근을 제시하며, MLLM-enhanced diffusion 모델과 Goal Drift Collection을 결합하여 기존 방법 대비 현저히 우수한 성능을 달성했다. Minecraft 환경에 한정되지만, embodied AI의 지시 추종 능력 향상에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — MineDreamer의 Chain-of-Imagination이 MineDojo의 개방형 환경에서 제공되는 다양한 Minecraft 작업을 체계적으로 처리하는 방법론을 제시한다.
- 🔗 후속 연구: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — MineDreamer가 MP5의 멀티모달 Minecraft 환경에서 Chain-of-Imagination을 통해 더욱 정교한 지시 추종 능력을 구현한다.
- 🔄 다른 접근: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — 둘 다 시각적 추론 체인을 활용하지만, MineDreamer는 상상 기반 계획을, CoT-VLA는 추론 체인 기반 행동 생성에 집중한다.
- 🔄 다른 접근: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — Minecraft에서 instruction following을 위한 chain-of-imagination vs thought chain의 다른 방법
- 🏛 기반 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — MineDreamer가 구현한 지시 추종의 기반이 되는 open-ended embodied agent 개념
- 🏛 기반 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — MineDreamer의 chain-of-imagination을 multimodal memory와 결합하여 더 안정적인 장기 작업 수행을 구현한다.
- ⚖️ 반론/비판: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — Minecraft에서 active perception vs imagination-based reasoning의 대조적 방법론
- 🔗 후속 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — MineDreamer의 chain-of-imagination 접근법이 Voyager의 자동 커리큘럼과 결합되면 더 효과적인 학습이 가능하다
