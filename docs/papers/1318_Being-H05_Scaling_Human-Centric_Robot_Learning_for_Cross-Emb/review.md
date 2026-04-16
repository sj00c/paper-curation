---
title: "1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb"
authors:
  - "Hao Luo"
  - "Ye Wang"
  - "Wanpeng Zhang"
  - "Sipeng Zheng"
  - "Ziheng Xi"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "Being-H0.5는 인간 중심 학습 패러다임과 통합 액션 공간을 활용하여 다양한 로봇 플랫폼 간 일반화를 가능하게 하는 기초 Vision-Language-Action 모델이다. 35,000시간 이상의 멀티모달 데이터로 구성된 UniHand-2.0을 통해 30개의 로봇 플랫폼에서 강력한 cross-embodiment 성능을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Luo et al._2026_Being-H0.5 Scaling Human-Centric Robot Learning for Cross-Embodiment Generalization.pdf"
---

# Being-H0.5: Scaling Human-Centric Robot Learning for Cross-Embodiment Generalization

> **저자**: Hao Luo, Ye Wang, Wanpeng Zhang, Sipeng Zheng, Ziheng Xi, Chaoyi Xu, Haiweng Xu, Haoqi Yuan, Chi Zhang, Yiqing Wang, Yicheng Feng, Zongqing Lu | **날짜**: 2026-01-19 | **URL**: [https://arxiv.org/abs/2601.12993](https://arxiv.org/abs/2601.12993)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Being-H0.5 at a Glance. We scale human-centric robot learning with Being-H0.5 toward*

Being-H0.5는 인간 중심 학습 패러다임과 통합 액션 공간을 활용하여 다양한 로봇 플랫폼 간 일반화를 가능하게 하는 기초 Vision-Language-Action 모델이다. 35,000시간 이상의 멀티모달 데이터로 구성된 UniHand-2.0을 통해 30개의 로봇 플랫폼에서 강력한 cross-embodiment 성능을 달성한다.

## Motivation

- **Known**: Vision-Language-Action (VLA) 모델은 로봇 조작에 유망하지만, 기존 모델들은 형태학적 이질성(morphological heterogeneity)과 데이터 부족으로 인해 단일 플랫폼에 특화되어 다른 로봇으로의 전이 성능이 저하된다.
- **Gap**: 현존하는 VLA는 로봇 간 모터 공간의 차이를 극복하지 못하며, 복잡한 엔티티(예: dexterous hands)로의 분포 이동(distribution shift)에서 궤적 드리프트(trajectory drift)를 경험한다. 또한 대규모 cross-embodiment 데이터셋과 체계적 데이터 수집 방법론이 부족하다.
- **Why**: 로봇 지능의 확장성은 새로운 플랫폼에 제한된 데이터로도 빠르게 적응할 수 있는 능력에 달려있으며, 이는 다중언어 NLP에서 달성한 수준의 일반화를 로봇공학에서도 실현하기 위해 중요하다.
- **Approach**: 인간 상호작용 데이터를 물리 세계의 '모국어'로 취급하는 인간 중심 학습 패러다임을 제안하고, 이질적 로봇 제어를 의미론적으로 정렬된 슬롯으로 매핑하는 Unified Action Space를 도입한다. Mixture-of-Flow (MoF) 아키텍처로 공유 motor primitives와 체화 특화 전문가를 분리한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Being-H0.5 at a Glance. We scale human-centric robot learning with Being-H0.5 toward*

- **대규모 멀티모달 데이터 구축**: UniHand-2.0 (35,000+ 시간, 120억 tokens, 400백만 샘플) 구성으로 30개 로봇 플랫폼 아우르는 최대 규모 체화 사전학습 데이터셋 제공
- **시뮬레이션 벤치마크 SOTA 달성**: LIBERO에서 98.9%, RoboCasa에서 53.9% 성능 달성
- **Cross-embodiment 강인성**: 5개 로봇 플랫폼 (PND Adam-U, Franka+Inspire, Unitree G1, BeingBeyond D1, LeRobot SO-101)에서 단일 체크포인트로 실세계 배포 성공
- **혁신적 기술 도입**: Manifold-Preserving Gating으로 감각 변화에 대한 강인성 확보, Universal Async Chunking으로 상이한 지연 시간과 제어 프로파일 보정
- **데이터 수집 시스템**: UniCraftor 시스템 개발으로 깊이 정보, 키프레임 이벤트, 카메라 외재성 통합한 200+ 시간 데이터 큐레이션

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of UniHand 2.0. UniHand 2.0 is our large-scale pre-training recipe for human-centric*

- **UniHand-2.0 구성**: 16,000시간 자아중심(egocentric) 인간 비디오 + 14,000시간 로봇 조작 + 5,000시간 시각-언어 이해 데이터 통합
- **Unified Action Space 설계**: 이질적 로봇 제어를 공유 물리 어휘의 토큰으로 표현하여 다양한 형태의 로봇을 통합 잠재 공간으로 정렬
- **Mixture-of-Transformers 아키텍처**: Mixture-of-Flow (MoF) 프레임워크로 공유 attention과 embodiment-specific FFN 결합
- **Human-Centric Pre-training**: Unified Sequence Modeling과 다중 작업 목표를 통해 인간 시연과 로봇 실행 간 다리 구축, Hybrid Human Motion Representation 활용
- **Manifold-Preserving Gating (MPG)**: sensory shift 하에서 valid motion manifold 내 궤적 유지
- **Universal Async Chunking (UAC)**: 상이한 지연 시간과 제어 프로파일을 가진 embodiment 간 청크 단위 제어 일반화
- **Dual-Thread Deployment Architecture**: 실시간 cross-embodiment 배포를 위한 병렬 추론 구조

## Originality

- **인간 중심 패러다임의 근본적 재정의**: 인간 동작을 물리 상호작용의 '모국어'로 개념화하여 로봇 다중언어성(multilinguality)을 달성하는 혁신적 관점", '**최대 규모 embodied 사전학습 데이터**: 200배 규모 증가 (이전 대비)로 30개 로봇 플랫폼 포함한 업계 최대 데이터셋 구축
- **Mixture-of-Flow 아키텍처**: 공유 motor primitives와 체화 특화 전문가를 명시적으로 분리하는 새로운 디코딩 방식
- **Manifold-Preserving Gating 메커니즘**: 분포 이동 하에서도 유효한 행동 다양체를 보존하는 새로운 안정화 기법
- **Universal Async Chunking 프로토콜**: 제어 주파수와 지연이 상이한 로봇 간 청크 기반 제어 일반화
- **UniCraftor 데이터 수집 시스템**: 깊이, 키프레임, 카메라 외재성 통합한 확장 가능한 데이터 수집 인프라

## Limitation & Further Study

- **데이터 편향 문제**: 인간 데이터 중심 학습이 인간과 로봇의 동역학 차이를 완전히 해결하지 못할 수 있으며, 특정 로봇 특화 작업에서 음의 전이 가능성
- **실세계 검증의 제한성**: 5개 로봇 플랫폼 실배포가 주요 성과이지만 더 이질적인 형태 (예: 수중 로봇, 비인형 그리퍼)에서의 성능 미검증
- **계산 효율성 미분석**: 120억 tokens 규모의 거대 사전학습 모델의 추론 지연 시간과 메모리 오버헤드에 대한 상세 분석 부족
- **Manifold-Preserving Gating의 이론적 근거 약화**: MPG가 motion manifold을 정확히 보존하는지에 대한 수학적 보장 또는 수렴성 증명 부재
- **후속 연구 방향**: (1) 더 극단적인 morphological variance (예: 바퀴 로봇 vs. 이족 보행)에서의 일반화 검증, (2) 온라인 학습 또는 적응 메커니즘 통합으로 배포 후 성능 개선, (3) 촉각 정보 등 추가 모드 통합

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Being-H0.5는 인간 중심 학습 패러다임과 대규모 통합 데이터셋을 활용하여 cross-embodiment 로봇 일반화의 중요한 진전을 이룬 의미 있는 연구이며, Mixture-of-Flow, Manifold-Preserving Gating 등의 기술 혁신과 실세계 배포 성공이 로봇공학의 확장성 문제를 해결하는 데 기여한다.

## Related Papers

- 🔗 후속 연구: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — Being-H0.5의 cross-embodiment 일반화와 π0의 generalist robot policy는 범용 로봇 정책의 서로 다른 확장 방향이다.
- 🏛 기반 연구: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — Cross-Embodied Learning의 단일 정책 조작은 Being-H0.5의 30개 로봇 플랫폼 일반화에 핵심 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1601_UniSkill_Imitating_Human_Videos_via_Cross-Embodiment_Skill_R/review]] — Being-H0.5의 인간 중심 학습과 UniSkill의 인간 비디오 모방은 cross-embodiment 학습의 서로 다른 데이터 활용 전략이다.
- 🔄 다른 접근: [[papers/1286_π_05_a_Vision-Language-Action_Model_with_Open-World_Generali/review]] — 둘 다 cross-embodiment VLA 모델이지만 Being-H0.5는 인간 중심 학습에, π0.5는 heterogeneous 데이터 co-training에 특화됩니다.
- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment의 cross-embodiment 데이터와 방법론이 Being-H0.5의 통합 액션 공간 개발의 기초가 됩니다.
- 🏛 기반 연구: [[papers/1294_A_Generalist_Agent/review]] — Gato의 단일 신경망 다중 작업 수행 개념은 Being-H0.5의 cross-embodiment 통합 학습 패러다임의 기초가 된다.
- 🔗 후속 연구: [[papers/1286_π_05_a_Vision-Language-Action_Model_with_Open-World_Generali/review]] — Being-H0.5와 마찬가지로 cross-embodiment 일반화를 목표로 하지만 π0.5는 웹 데이터 활용에 더 중점을 둡니다.
- 🔗 후속 연구: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — π0의 generalist robot policy와 Being-H0.5의 cross-embodiment 일반화는 모두 범용 로봇 정책을 지향한다.
- 🏛 기반 연구: [[papers/1296_A_Pragmatic_VLA_Foundation_Model/review]] — Being-H0.5의 멀티플랫폼 일반화 개념을 실용적인 규모로 축소하여 효율적인 학습에 중점을 둔 pragmatic한 접근법입니다.
