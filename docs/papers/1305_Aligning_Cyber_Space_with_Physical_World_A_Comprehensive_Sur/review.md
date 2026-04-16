---
title: "1305_Aligning_Cyber_Space_with_Physical_World_A_Comprehensive_Sur"
authors:
  - "Yang Liu"
  - "Weixing Chen"
  - "Yongjie Bai"
  - "Xiaodan Liang"
  - "Guanbin Li"
date: "2024.07"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 사이버공간과 물리세계를 연결하는 embodied AI의 최신 동향을 포괄적으로 조사하며, Multi-modal Large Models(MLMs)과 World Models(WMs)의 역할을 강조한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2024_Aligning Cyber Space with Physical World A Comprehensive Survey on Embodied AI.pdf"
---

# Aligning Cyber Space with Physical World: A Comprehensive Survey on Embodied AI

> **저자**: Yang Liu, Weixing Chen, Yongjie Bai, Xiaodan Liang, Guanbin Li, Wen Gao, Liang Lin | **날짜**: 2024-07-09 | **URL**: [https://arxiv.org/abs/2407.06886](https://arxiv.org/abs/2407.06886)

---

## Essence


이 논문은 사이버공간과 물리세계를 연결하는 embodied AI의 최신 동향을 포괄적으로 조사하며, Multi-modal Large Models(MLMs)과 World Models(WMs)의 역할을 강조한다.

## Motivation

- **Known**: 기존의 embodied AI 연구들이 존재했지만, 대부분 MLMs 시대(2023년경) 이전에 출판되었으며, MLMs, WMs, embodied agents의 통합적 고찰이 부족했다.
- **Gap**: MLMs 시대의 embodied AI에 대한 포괄적인 설문이 부재하며, embodied robots, simulators, 그리고 embodied perception/interaction/agents/sim-to-real adaptation의 통합적 분류와 분석이 미흡했다.
- **Why**: Embodied AI는 AGI 달성의 근본적인 경로이며, 로봇공학, 헬스케어, 스마트 제조 등 다양한 응용 분야에서 사이버 공간과 물리 세계를 연결하는 데 핵심적 역할을 한다.
- **Approach**: 대표적인 embodied robots, simulators, 그리고 embodied perception, embodied interaction, embodied agents, sim-to-real adaptation의 네 가지 주요 연구 목표를 체계적으로 분석하고, ARIO라는 새로운 데이터셋 표준을 제안한다.

## Achievement


- **포괄적 분류 체계**: embodied robots(고정형, 사족형 등), general/real-scene simulators, 그리고 네 가지 핵심 연구 영역을 상세한 taxonomy로 정리
- **MLMs와 WMs의 역할 규명**: Multi-modal Large Models과 World Models이 embodied agents의 perception, interaction, reasoning 능력에 기여하는 방식을 분석
- **ARIO 데이터셋 제안**: 258개 시리즈, 321,064개 작업으로부터 약 300만 에피소드를 수집한 통합 대규모 데이터셋 제시
- **도전과제 및 향후 방향 제시**: embodied AI의 현재 한계(장기 메모리, 복잡한 의도 이해, 작업 분해)와 미래 연구 방향 종합

## How


- Embodied robots의 유형(고정형, 사족형, 바퀴형 등) 분류 및 특성 분석
- General simulators(MuJoCo 등)와 real-scene simulators의 특징 비교
- Active visual perception, visual language navigation 등 embodied perception 기법 검토
- Human-robot interaction, task planning 등 embodied interaction 방식 분석
- Vision-language-action models(RT-2, RT-H)와 같은 embodied multi-modal foundation models 조사
- Sim-to-real adaptation의 domain randomization, transfer learning 등 기법 분석
- ABC model(AI brain, Body, Cross-modal sensors) 프레임워크 제안을 통한 embodied agent 아키텍처 구조화

## Originality

- MLMs 시대 이후의 embodied AI 연구를 포괄적으로 다룬 첫 번째 설문으로, 기존 설문들의 outdated된 부분을 보완
- 사이버 공간과 물리 세계의 alignment 관점에서 embodied AI를 재조명하는 새로운 프레임워크 제시
- ARIO 데이터셋 표준과 통합 대규모 데이터셋 제안으로 embodied AI 연구의 벤치마킹 기반 강화
- ABC model(AI brain, Body, Cross-modal sensors)을 통한 체계적인 embodied agent 아키텍처 제안

## Limitation & Further Study

- 설문 논문의 특성상 깊이 있는 이론적 혁신보다는 기존 연구의 종합에 중점을 두고 있어 새로운 알고리즘이나 방법론 제시 부족
- ARIO 데이터셋이 충분히 다양한 embodied environments와 task types을 포괄하는지에 대한 검증 부족
- MLMs의 장기 메모리, 복잡한 의도 이해 문제 등을 해결하기 위한 구체적 기술적 제안이 미흡
- Sim-to-real gap의 근본적 해결을 위한 새로운 패러다임 제시 필요
- Domain-specific embodied AI 응용(헬스케어, 스마트 제조 등)에 대한 심화 분석 부족

## Evaluation

- Novelty: 3/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 MLMs 시대의 embodied AI를 포괄적으로 다룬 중요한 설문 논문으로, 체계적인 taxonomy, ARIO 데이터셋, ABC model 프레임워크를 통해 embodied AI 연구 커뮤니티에 귀중한 참고 자료를 제공한다. 다만 새로운 기술적 혁신보다는 기존 연구의 정리와 분류에 중점을 두고 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — Foundation Model을 통한 범용 로봇 개발이라는 유사한 목표를 다른 관점에서 접근한다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — 물리적 세계와 연결된 멀티모달 언어 모델의 기초적 구현을 제공한다.
- 🔗 후속 연구: [[papers/1294_A_Generalist_Agent/review]] — Generalist Agent를 embodied AI로 확장하는 구체적 방향을 제시한다.
- 🔄 다른 접근: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — 둘 다 embodied multimodal AI를 포괄적으로 다루지만 본 논문은 사이버-물리 연결에, 다른 논문은 개발과 데이터에 더 집중합니다.
- 🔗 후속 연구: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — Large Model Empowered Embodied AI 서베이는 본 논문의 MLM과 WM 중심 관점을 의사결정 관점에서 확장합니다.
- 🔗 후속 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — Embodied AI를 위한 World Model 포괄 서베이와 사이버-물리 연결 서베이가 상호 보완적 관점을 제공합니다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Foundation Model 기반 로보틱스 리뷰와 사이버-물리 정렬이 다른 관점에서 embodied AI를 분석합니다.
