---
title: "1391_Fast-in-Slow_A_Dual-System_Foundation_Model_Unifying_Fast_Ma"
authors:
  - "Hao Chen"
  - "Jiaming Liu"
  - "Chenyang Gu"
  - "Zhuoyang Liu"
  - "Renrui Zhang"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Fast-in-Slow (FiS)는 VLM 기반의 System 2 내부에 System 1 실행 모듈을 매개변수 공유로 통합한 통합 dual-system VLA 모델로, 고속 제어와 추론 능력을 동시에 달성한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2025_Fast-in-Slow A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning.pdf"
---

# Fast-in-Slow: A Dual-System Foundation Model Unifying Fast Manipulation within Slow Reasoning

> **저자**: Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, Pheng-Ann Heng | **날짜**: 2025-06-02 | **URL**: [https://arxiv.org/abs/2506.01953](https://arxiv.org/abs/2506.01953)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of FiS-VLA. (a) Unlike previous dual-system VLA methods [1, 2] that attach a*

Fast-in-Slow (FiS)는 VLM 기반의 System 2 내부에 System 1 실행 모듈을 매개변수 공유로 통합한 통합 dual-system VLA 모델로, 고속 제어와 추론 능력을 동시에 달성한다.

## Motivation

- **Known**: 최근 VLA 모델들은 internet-scale pretrained VLM의 상식 추론 능력을 활용하지만 낮은 실행 빈도로 인해 제약을 받는다. Kahneman의 dual-system 이론에 영감을 받은 접근법들은 VLM 기반 System 2와 독립적인 System 1 정책 모델을 분리하여 설계하고 있다.
- **Gap**: 기존 dual-system VLA 방법들은 System 1을 별도의 경량 모델로 유지하여 System 2의 internet-scale pretrained 지식을 완전히 활용하지 못하고, System 1이 풍부한 추론 능력에 접근하기 어렵다.
- **Why**: 로봇 조작에서 일반화된 정책과 실행 효율성의 균형이 필수적이며, 높은 제어 빈도와 정밀한 추론을 동시에 달성하는 것은 실제 응용에 매우 중요하다.
- **Approach**: VLM의 최종 transformer 블록을 System 1으로 재목적화하여 두 시스템이 동일한 기초 모델에서 파생되도록 통합하고, heterogeneous modality input과 asynchronous operating frequency를 적용하여 조정된 추론과 실행을 구현한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of FiS-VLA. (a) Unlike previous dual-system VLA methods [1, 2] that attach a*

- **통합 dual-system 아키텍처**: System 1을 System 2 내부에 매개변수 공유로 임베드하여 원활한 조정 가능
- **고주파 제어 달성**: 117.7 Hz 제어 빈도로 실시간 폐루프 제어 가능
- **SOTA 성능**: 시뮬레이션에서 8%, 실제 작업에서 11% 성공률 개선
- **이질적 설계**: System 2는 2D 관찰/언어 처리, System 1은 robot state/이미지/point cloud 입력 처리

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Framework of FiS-VLA. FiS-VLA leverages an intact VLM for System 2 reasoning*

- VLM의 최종 transformer 블록들을 System 1 실행 모듈로 재목적화하며 전체 VLM을 System 2로 유지
- System 2는 저주파(multimodal latent representation 생성), System 1은 고주파(rapid action 실행) 비동기 운영
- System 1을 위해 fast 3D embedding 전략으로 point cloud를 토큰화하고 공유 vision encoder 사용
- Dual-aware co-training 전략: System 1은 diffusion modeling으로 noised action을 latent vector로 주입, System 2는 autoregressive next-token prediction으로 추론 능력 보존
- 860K 이상의 trajectory로 pretrain 후 고품질 자체 수집 데이터로 fine-tuning
- 1:4의 운영 주파수 비율(System 2:System 1) 설정

## Originality

- 기존의 별도 System 1 정책 모델 부착 방식을 탈피하여, VLM의 내부 블록 자체를 System 1로 재활용하는 혁신적 구조
- Heterogeneous modality input과 asynchronous frequency를 동시에 적용한 설계
- Diffusion modeling과 autoregressive prediction을 dual-aware co-training으로 결합한 훈련 전략
- Neuroscientific 이중 과정 인지 연구에 영감을 받아 로봇 조작에 적용한 이론적 근거

## Limitation & Further Study

- 평가가 주로 단일 팔 시뮬레이션과 이중 팔 실제 작업에 제한되어 다양한 로봇 플랫폼 검증 필요
- Point cloud 기반 3D 정보 처리가 센서 의존도가 높을 수 있음
- Action chunk size 8로 설정된 실험이 다른 chunk 크기에서의 성능 변화 분석 필요
- 대규모 pretrain 데이터(860K+) 필요로 한 리소스 요구사항이 높음
- 실제 환경에서의 다양한 동역학 및 불확실성 대응 능력에 대한 추가 분석 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: FiS-VLA는 dual-system VLA의 구조적 한계를 혁신적으로 해결하고 높은 제어 빈도와 추론 능력을 동시에 달성한 중요한 기여이며, 매개변수 공유를 통한 통합 설계와 이질적 입력/주파수의 체계적 활용이 로봇 조작 분야에 큰 영향을 미칠 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — TriVLA의 삼중 시스템 구조가 Fast-in-Slow의 dual-system 설계를 이론적으로 확장한 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — Ground Slow, Move Fast도 dual-system 접근법을 사용하지만 navigation에 특화된 다른 시스템 분리 전략을 제시합니다.
- 🔗 후속 연구: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — MetaMorph의 universal controller가 Fast-in-Slow의 통합 VLA 모델을 다양한 형태의 로봇으로 확장합니다.
- 🏛 기반 연구: [[papers/1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi/review]] — Consistency Policy의 단일 추론 단계 정책 생성 기법이 FiS의 System 1 고속 실행 설계 기반이 됨
- 🔄 다른 접근: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — RationalVLA와 FiS 모두 dual-system 접근을 취하지만 합리적 추론 vs 속도-정확도 균형에서 다른 초점을 가짐
- 🏛 기반 연구: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — Fast-in-Slow dual-system foundation model의 개념을 VLN 특화 시스템으로 구체화했다.
- 🔄 다른 접근: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — RationalVLA와 Fast-in-Slow 모두 dual system 접근법을 사용하지만 안전성과 효율성이라는 다른 목표를 추구합니다.
- 🔄 다른 접근: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — Fast-in-Slow dual-system과 동일한 이중 시스템 접근이지만 OpenHelix는 VLA에 특화된 분석과 구현을 제공한다.
- 🔗 후속 연구: [[papers/1553_RoBridge_A_Hierarchical_Architecture_Bridging_Cognition_and/review]] — Fast-in-Slow의 dual-system 구조와 RoBridge의 계층적 아키텍처를 결합하면 더 효과적인 인지-실행 통합이 가능하다.
- 🔄 다른 접근: [[papers/1373_DualVLA_Building_a_Generalizable_Embodied_Agent_via_Partial/review]] — Fast-in-Slow도 추론과 행동의 분리 문제를 다루지만 dual-system 접근법으로 DualVLA와 다른 해결책을 제시합니다.
