---
title: "1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented"
authors:
  - "Zihao Wang"
  - "Shaofei Cai"
  - "Anji Liu"
  - "Yonggang Jin"
  - "Jinbing Hou"
date: "2023.11"
doi: ""
arxiv: ""
score: 4.0
essence: "JARVIS-1은 multimodal language model과 multimodal memory를 결합하여 Minecraft의 오픈월드 환경에서 200개 이상의 다양한 작업을 수행할 수 있는 멀티태스크 에이전트이다. 특히 장기 작업(ObtainDiamondPickaxe)에서 기존 최신 에이전트 대비 5배 우수한 신뢰성을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2023_JARVIS-1 Open-World Multi-task Agents with Memory-Augmented Multimodal Language Models.pdf"
---

# JARVIS-1: Open-World Multi-task Agents with Memory-Augmented Multimodal Language Models

> **저자**: Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, Xiaojian Ma, Yitao Liang | **날짜**: 2023-11-10 | **URL**: [https://arxiv.org/abs/2311.05997](https://arxiv.org/abs/2311.05997)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 | How does JARVIS-1 unlock the technology tree of the Minecraft universe. JARVIS-1 can*

JARVIS-1은 multimodal language model과 multimodal memory를 결합하여 Minecraft의 오픈월드 환경에서 200개 이상의 다양한 작업을 수행할 수 있는 멀티태스크 에이전트이다. 특히 장기 작업(ObtainDiamondPickaxe)에서 기존 최신 에이전트 대비 5배 우수한 신뢰성을 달성한다.

## Motivation

- **Known**: LLM 기반 계획 에이전트는 로봇공학 및 Minecraft 같은 오픈월드 환경에서 일부 장기 작업을 처리할 수 있다. 그러나 무한에 가까운 오픈월드 작업 처리와 게임 진행 중 성능 점진적 향상 능력은 부족하다.
- **Gap**: 기존 LLM 기반 에이전트는 multimodal 감각 입력(이미지, 비디오) 인식 불가, 장기 계획 일관성 부족, lifelong learning을 통한 자율적 진화 능력 부재라는 세 가지 주요 문제를 해결하지 못한다.
- **Why**: 오픈월드 환경에서 human-like planning과 embodied control을 달성하는 것은 일반화된 에이전트 개발의 핵심 이정표이며, 이를 통해 더욱 기능적인 생성형 AI 시스템을 구축할 수 있다.
- **Approach**: MineCLIP과 GPT를 결합한 multimodal language model을 기반으로 시각 관찰과 텍스트 지시를 계획으로 변환하고, multimodal memory를 통해 과거 경험을 저장 및 retrieval하여 in-context learning으로 계획을 강화한다. Self-instruct 메커니즘으로 자율적 탐색과 경험 축적을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 | How does JARVIS-1 unlock the technology tree of the Minecraft universe. JARVIS-1 can*

- **200개 이상 다양한 작업 수행**: 단기 작업(나무 자르기)부터 장기 작업(다이아몬드 곡괭이 획득)까지 인간과 유사한 제어/관찰 공간으로 처리
- **5배 향상된 신뢰성**: ObtainDiamondPickaxe 작업에서 기존 VPT(2.5%) 대비 12.5% 성공률 달성
- **근처 완벽한 단기 작업 성능**: 단기 작업에서 거의 완벽한 성능 수준 도달
- **점진적 성능 향상**: 추가 학습 없이 게임 진행 시간 증가에 따라 장기 작업 성능이 지속적으로 개선
- **자율적 개선 능력**: 자체 생성 작업(self-instruct)을 통한 탐색과 multimodal memory 활용으로 lifelong learning 달성

## How

![Figure 3](figures/fig3.webp)

*Figure 3 | Architecture of JARVIS-1 and its self-improving mechanism. (a) JARVIS-1 comprises a memory-*

- MineCLIP(multimodal foundation model)과 GPT(LLM)를 체인으로 연결하여 multimodal language model (MLM) 구성
- 시각 관찰과 현재 상황을 기반으로 한 situation-aware planning으로 동적 환경에 적응
- 과거 성공 경험과 계획을 저장하는 multimodal memory로 in-context learning 수행
- Interactive planning으로 계획 실행 중 환경 피드백을 받아 실시간 계획 수정
- Self-instruct 메커니즘으로 에이전트가 자율적으로 새로운 작업을 생성하고 탐색 수행
- Goal-conditioned controller로 MLM이 생성한 고수준 계획을 저수준 모터 제어로 변환

## Originality

- **MLM 기반 설계**: 단순 LLM이 아닌 MineCLIP+GPT 결합으로 multimodal perception 가능하게 한 혁신적 접근
- **Multimodal memory 기반 in-context learning**: 모델 업데이트 없이 과거 경험을 context에 포함하여 계획 강화하는 novel 방식
- **Self-instruct와 lifelong learning 통합**: 에이전트가 자율적으로 작업을 생성하고 경험을 축적하면서 진화하는 메커니즘
- **Situation-aware interactive planning**: 장기 작업 중 환경 상황 변화(낮밤, 도구 손상)에 대응하는 동적 계획 수립
- **오픈월드 환경의 무한 작업 처리**: 200개 이상의 광범위 작업 수행으로 기존 특정 작업 중심의 제약 극복

## Limitation & Further Study

- **Minecraft 환경 특화**: 다른 오픈월드 환경(로봇, 현실 환경)으로의 일반화 가능성 미검증
- **장기 작업 여전한 낮은 절대 성공률**: 12.5% 성공률은 상대적 개선이지만 실제 배포에는 여전히 낮은 수준
- **Multimodal memory 크기 관리**: 극장기 학습에서 memory 크기 확대 시 retrieval 효율성과 계산 비용 증가 문제 미해결
- **Self-instruct 품질 보증**: 에이전트가 생성하는 작업이 유의미한 탐색으로 이어지는지 정량적 평가 미흡
- **Human preference와 안전성**: 자율적 작업 생성 시 인간의 의도와 안전 제약을 보장하는 메커니즘 부재
- **후속연구**: 다양한 도메인으로의 확장, memory 효율화, 절대 성공률 개선, 인간 alignment 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: JARVIS-1은 multimodal language model과 multimodal memory를 결합한 혁신적 설계로 오픈월드 에이전트의 다중 도전(multimodal perception, 장기 계획, lifelong learning)을 동시에 해결한 획기적 연구이다. Minecraft에서의 5배 성능 향상과 자율적 개선 능력은 일반화된 embodied AI 개발의 중요한 진전을 의미한다.

## Related Papers

- 🔄 다른 접근: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — 둘 다 오픈월드 멀티태스크 에이전트이지만 JARVIS-1은 Minecraft에, Voyager는 일반적인 환경에 집중한다.
- 🏛 기반 연구: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — joint-embedding 예측 아키텍처가 JARVIS-1의 multimodal memory 구조 설계에 기반이 된다.
- 🔗 후속 연구: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — Minecraft 환경에서의 멀티태스크 능력을 multi-modal embodied system으로 더 발전시킨 형태다.
- 🏛 기반 연구: [[papers/1478_MineDreamer_Learning_to_Follow_Instructions_via_Chain-of-Ima/review]] — MineDreamer의 chain-of-imagination을 multimodal memory와 결합하여 더 안정적인 장기 작업 수행을 구현한다.
- 🏛 기반 연구: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — MineDojo의 Minecraft 환경과 오픈월드 에이전트 개념이 JARVIS-1의 멀티태스크 학습 기반을 제공함
- 🏛 기반 연구: [[papers/1459_LLM-State_Open_World_State_Representation_for_Long-horizon_T/review]] — JARVIS-1의 memory-augmented multi-task agent 개념을 장기 작업 계획의 상태 표현으로 발전시켰다.
- 🏛 기반 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — memory-augmented multi-task agent의 기초 연구로서 MEM의 다중 스케일 메모리 아키텍처 설계에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — MP5의 다중모듈 시스템이 확장한 memory-augmented multi-task agent의 기초
- 🔄 다른 접근: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — JARVIS-1은 SIMA와 유사한 다중 환경 instructable agent이지만 메모리 증강된 멀티태스크에 집중하는 차별점이 있다.
- 🔗 후속 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — open-world multi-task agent의 개념을 memory-augmented 시스템으로 확장하여 Voyager의 평생 학습을 더 체계화합니다.
- 🔗 후속 연구: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — JARVIS-1은 LLM 기반 네비게이션을 메모리 증강과 멀티태스크로 확장한 발전된 형태입니다.
