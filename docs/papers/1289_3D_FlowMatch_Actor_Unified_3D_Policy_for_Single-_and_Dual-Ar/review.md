---
title: "1289_3D_FlowMatch_Actor_Unified_3D_Policy_for_Single-_and_Dual-Ar"
authors:
  - "Nikolaos Gkanatsios"
  - "Jiahe Xu"
  - "Matthew Bronars"
  - "Arsalan Mousavian"
  - "Tsung-Wei Ke"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "3D FlowMatch Actor (3DFA)는 flow matching을 사용한 trajectory prediction과 3D pretrained visual representation을 결합하여 단일 팔 및 양팔 로봇 조작을 위한 통합 정책을 제시하며, 이전 3D diffusion 기반 정책 대비 30배 이상 빠른 학습과 추론을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gkanatsios et al._2025_3D FlowMatch Actor Unified 3D Policy for Single- and Dual-Arm Manipulation.pdf"
---

# 3D FlowMatch Actor: Unified 3D Policy for Single- and Dual-Arm Manipulation

> **저자**: Nikolaos Gkanatsios, Jiahe Xu, Matthew Bronars, Arsalan Mousavian, Tsung-Wei Ke, Katerina Fragkiadaki | **날짜**: 2025-08-14 | **URL**: [https://arxiv.org/abs/2508.11002](https://arxiv.org/abs/2508.11002)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Top: 3DFA is a flow-matching policy built atop 3D Diffuser Actor [12]. It encodes the*

3D FlowMatch Actor (3DFA)는 flow matching을 사용한 trajectory prediction과 3D pretrained visual representation을 결합하여 단일 팔 및 양팔 로봇 조작을 위한 통합 정책을 제시하며, 이전 3D diffusion 기반 정책 대비 30배 이상 빠른 학습과 추론을 달성한다.

## Motivation

- **Known**: Diffusion 모델은 멀티모달 행동을 포착하고 3D scene understanding을 통해 고정밀도 action prediction을 달성할 수 있으나, 3DDA와 같은 기존 3D diffusion 정책들은 느린 추론 속도(0.5Hz)와 긴 학습 시간(21일)으로 인해 실제 배포에 제약이 있다.
- **Gap**: 양팔 조작은 높은 시공간 정밀도를 요구하지만, 기존 접근법들은 광범위한 작업에 대해 견고한 일반화를 달성하지 못하고 있으며, 특히 실시간 동적 작업 실행에 필요한 빠른 추론 속도를 제공하지 못한다.
- **Why**: 양팔 로봇 시스템은 더욱 정교하고 조정된 환경 상호작용을 가능하게 하여 복잡한 현실 작업을 수행할 수 있으나, 효율적이고 강력한 정책이 필요하며, 빠른 추론 속도는 실제 로봇 배포와 적응 학습을 위해 필수적이다.
- **Approach**: 3DFA는 DDPM 기반 diffusion을 Rectified Flow로 대체하여 추론 단계를 100에서 5로 감소시키고, 빠른 토큰 샘플링, 최적화된 attention 구현, mixed-precision training 등의 시스템 수준 최적화를 적용한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Ablation study on PerAct2. Left: 3DFA’s performance is stable even with as few as three*

- **PerAct2 벤치마크 성능**: 85.1% 성공률로 새로운 state-of-the-art 달성, π0 대비 41.4% 절대 마진 향상
- **효율성 개선**: 학습 시간을 21일에서 16시간으로, 추론 속도를 0.5Hz에서 18.2Hz로 개선 (30배 이상 가속)
- **실제 로봇 평가**: 자체 구축한 10-task bimanual ALOHA 벤치마크에서 π0를 포함한 강력한 baseline들 초과
- **단일 팔 작업 우수성**: 74개 RLBench 작업에서 state-of-the-art 달성, 7.3% 성능 향상
- **범용성**: sparse keypose 및 dense end-effector trajectory 예측 모두 지원, 단일/양팔 조작에 적용 가능

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Top: 3DFA is a flow-matching policy built atop 3D Diffuser Actor [12]. It encodes the*

- Flow matching에서 Rectified Flow를 채택하여 최적 수송 문제를 해결하고 직선 경로로 noise를 action으로 변환
- 3DDA 아키텍처 기반으로 양팔 조작을 위해 좌/우 팔 토큰 분리 및 각각의 velocity field 예측 (vθ,L, vθ,R)
- RGB-D 입력으로부터 3D point cloud를 생성하고 foundational image encoder로 2D 특징 추출 후 3D 토큰으로 변환
- 3D relative attention을 통해 action 토큰과 visual 토큰 간의 공간적 관계 학습, robot frame으로의 calibration 기반 좌표 변환
- 언어 instruction, proprioception 히스토리, noised trajectory 및 denoising step 정보를 조건으로 한 Denoising Transformer
- 빠른 point sampling, 카메라 입력 최소화, 최적화된 데이터 로딩 파이프라인, efficient attention 구현, mixed-precision training 적용

## Originality

- Flow matching (Rectified Flow)의 로봇 정책에의 첫 적용으로 추론 단계를 획기적으로 감소
- 3DDA의 양팔 조작 확장은 기존 아키텍처 상속이나, flow matching 통합 및 광범위한 시스템 최적화를 통한 실질적 혁신
- 단일 정책으로 sparse keypose 및 dense trajectory 예측을 동시에 처리하는 통합 프레임워크
- 광범위한 실세계 평가와 상세한 ablation study를 통한 각 설계 선택의 기여도 명확화

## Limitation & Further Study

- Flow matching 선택의 이론적 근거: diffusion vs flow matching의 정보론적 비교 및 action 분포 특성 분석 부족
- 5-step inference에서의 trajectory 질의 저하 가능성: 정성적 궤적 분석 및 precision 요구 작업에서의 성능 상세 분석 필요
- 현재 PerAct2의 18개 양팔 작업에 제한: 더 다양한 양팔 조작 작업으로의 일반화 검증 필요
- 실세계 평가가 10-task 벤치마크로 제한적: 더 광범위한 실제 작업 및 환경 변화에 대한 강건성 검증 필요
- 후속 연구: 더 많은 카메라 입력이나 higher fidelity visual representation의 영향 분석, 양팔 coordination 메커니즘 심화 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 3DFA는 flow matching을 로봇 정책에 적용하여 획기적 효율성 개선을 달성하고, 양팔 조작에서 새로운 state-of-the-art를 수립하며, 광범위한 실세계 평가와 ablation을 통해 실용적 로봇 정책의 모범적 사례를 제시하는 고도로 영향력 있는 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 3D diffusion policy의 기반 위에서 flow matching을 통한 30배 속도 개선을 달성한 후속 연구
- 🔄 다른 접근: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — 동일한 로봇 조작 문제를 diffusion 대신 flow matching으로 해결하여 훨씬 빠른 학습과 추론 속도를 제공
- 🏛 기반 연구: [[papers/1465_ManiFlow_A_General_Robot_Manipulation_Policy_via_Consistency/review]] — ManiFlow의 flow matching 기반 manipulation policy 개념을 3D 시각 표현과 결합하여 단일/양팔 통합 정책으로 발전시킨 연구입니다.
- 🔗 후속 연구: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — RDT-1B의 bimanual manipulation을 위한 diffusion 기반 모델을 flow matching으로 개선하고 단일/양팔 통합 접근법으로 발전시킨 연구입니다.
- 🏛 기반 연구: [[papers/1395_FlowPolicy_Enabling_Fast_and_Robust_3D_Flow-based_Policy_via/review]] — 3D FlowMatch Actor의 3D flow-based policy 생성 기법이 FlowPolicy의 Consistency Flow Matching 설계의 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — diffusion policy를 flow matching으로 대체하여 동일한 visuomotor 학습을 훨씬 빠르게 수행하는 개선된 접근법
- 🔄 다른 접근: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 둘 다 3D 시각 표현과 생성 모델을 결합하지만 DP3는 diffusion을, 3DFA는 flow matching을 사용하여 서로 다른 접근법을 제시합니다.
