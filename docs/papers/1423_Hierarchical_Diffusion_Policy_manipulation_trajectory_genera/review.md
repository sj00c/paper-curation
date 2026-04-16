---
title: "1423_Hierarchical_Diffusion_Policy_manipulation_trajectory_genera"
authors:
  - "Dexin Wang"
  - "Chunsheng Liu"
  - "Faliang Chang"
  - "Yichen Xu"
date: "2024.11"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇 조작 작업에서 diffusion model 기반의 계층적 정책을 제안하며, 상위 정책은 접촉점을 예측하고 하위 정책은 접촉점으로 유도된 동작 수열을 생성하여 접촉이 풍부한 작업에서의 성능을 향상시킨다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2024_Hierarchical Diffusion Policy manipulation trajectory generation via contact guidance.pdf"
---

# Hierarchical Diffusion Policy: manipulation trajectory generation via contact guidance

> **저자**: Dexin Wang, Chunsheng Liu, Faliang Chang, Yichen Xu | **날짜**: 2024-11-20 | **URL**: [https://arxiv.org/abs/2411.12982](https://arxiv.org/abs/2411.12982)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Inference Process of Hierarchical Diffusion Policy.*

로봇 조작 작업에서 diffusion model 기반의 계층적 정책을 제안하며, 상위 정책은 접촉점을 예측하고 하위 정책은 접촉점으로 유도된 동작 수열을 생성하여 접촉이 풍부한 작업에서의 성능을 향상시킨다.

## Motivation

- **Known**: Diffusion policy는 다중모드 동작 분포를 모델링할 수 있어 로봇 모방 학습에서 주목받고 있으나, 접촉이 풍부한 작업에서는 성능이 저하되고 제어성이 제한적이다.
- **Gap**: 기존 end-to-end diffusion policy는 로봇과 객체 간의 상호작용을 명시적으로 모델링하지 않아 접촉이 많은 작업에서 어려움을 겪는다. 계층적 구조를 통한 접촉 유도 방식의 필요성이 있다.
- **Why**: 로봇 조작의 본질은 접촉 상태 변화에 기반하므로, 접촉을 명시적으로 모델링하면 장기 수평 작업 학습을 단기 부분 문제로 분해하여 학습 효율성과 제어성을 대폭 향상시킬 수 있다.
- **Approach**: Hierarchical Diffusion Policy는 Guider 네트워크로 고수준 접촉점을 예측하고, Actor 네트워크가 behavioral cloning과 Q-learning의 결합을 통해 접촉점으로 유도된 동작 수열을 생성하는 두 계층의 conditional diffusion process로 구성된다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Hierarchical Diffusion Policy Overview. (a) At time step t during inference, the Guider takes the latest To step*

- **성능 향상**: 6개 작업에서 기존 Diffusion Policy 대비 평균 20.8% 성능 개선 달성
- **해석성 증대**: 계층적 계획으로 각 단계의 궤적 생성 로직이 투명해지고 로봇의 조작 의도가 명확해짐
- **제어성 강화**: 수동 접촉점 지정(prompt guidance)을 통해 인간-로봇 상호작용 강화 및 조작 방식 커스터마이징 가능
- **일반화 능력**: 강체 및 변형 가능 객체 모두 처리 가능하며 실제 환경에서 검증됨

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Hierarchical Diffusion Policy Overview. (a) At time step t during inference, the Guider takes the latest To step*

- Guider 네트워크: 3D point cloud 입력을 통해 conditional denoising diffusion process로 다음 조작의 객체 접촉점 예측
- Actor 네트워크: 관찰의 잠재 변수와 예측된 접촉점을 조건으로 하여 동작 수열 생성
- Snapshot gradient optimization: Q-learning 최적화 시 diffusion process의 모든 시간 단계가 아닌 단일 시간 단계만 기울기 계산하여 학습 속도 향상
- 3D conditioning: point cloud 특징을 denoising 반복과 무관하게 한 번만 추출하여 공간 인식 능력 개선
- Prompt guidance: Guider 네트워크 대신 인간이 직접 접촉점을 지정하여 커스터마이징된 궤적 생성 가능
- Behavioral cloning과 Q-learning 결합: Actor가 조건부 동작 확률 분포를 학습하면서 동시에 접촉점으로의 유도를 학습

## Originality

- 접촉점 예측을 explicit guidance로 사용하여 장기 궤적 생성을 단기 부분 문제로 계층화한 혁신적인 구조
- Snapshot gradient optimization을 제안하여 diffusion 기반 정책의 학습 효율성을 근본적으로 개선
- 3D point cloud 기반 conditioning으로 기존의 평면 이미지 기반 접근법보다 공간 인식 능력 향상
- Prompt guidance 메커니즘으로 자동 생성과 수동 제어 사이의 인터페이스 제공하여 인간-로봇 협력 강화
- Single-finger gripper와 dexterous hand 등 다양한 end-effector에 일반화 가능한 접촉 기반 표현

## Limitation & Further Study

- 접촉점 예측의 정확도가 최종 동작 성능에 직접적으로 영향을 미치므로, Guider 네트워크의 오류 누적 가능성에 대한 분석 부족
- 6개 작업에만 평가되었으며, 더 복잡한 다중 접촉 순서가 필요한 작업에 대한 확장성 검증 필요
- 실제 환경 실험의 규모가 제한적이며, 다양한 객체 특성과 환경 조건에서의 강건성 검증이 필요
- Prompt guidance에서 인간이 제공해야 하는 접촉점 정보의 복잡도 및 학습 곡선에 대한 평가 부재
- Hierarchical 구조의 오버헤드(두 개의 diffusion model 필요)와 계산 비용에 대한 분석 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 로봇 조작의 본질인 접촉을 명시적으로 모델링하여 계층적 diffusion policy를 제안한 혁신적인 연구로, snapshot gradient optimization 등의 기술적 기여와 함께 20.8% 성능 향상을 달성했으며, 해석성과 제어성 측면에서도 유의미한 진전을 이루었다.

## Related Papers

- 🔄 다른 접근: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 3D Diffusion Policy도 로봇 조작에 diffusion을 적용하지만 3D 공간 표현에 특화된 반면, 계층적 접근법은 접촉점 기반 분해에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy는 계층적 확산 정책이 기반으로 하는 로봇 조작에서의 diffusion model 적용에 대한 기초 연구입니다.
- 🔗 후속 연구: [[papers/1419_H3DP_Triply-Hierarchical_Diffusion_Policy_for_Visuomotor_Lea/review]] — H³DP는 계층적 diffusion policy를 삼중 계층으로 더 세분화하여 발전시킨 연구입니다.
- 🔗 후속 연구: [[papers/1419_H3DP_Triply-Hierarchical_Diffusion_Policy_for_Visuomotor_Lea/review]] — 계층적 diffusion policy에서 depth-aware representation을 추가로 고려한 확장 연구입니다.
- 🔗 후속 연구: [[papers/1524_Reactive_Diffusion_Policy_Slow-Fast_Visual-Tactile_Policy_Le/review]] — hierarchical diffusion policy의 개념을 visual-tactile feedback과 결합하여 접촉 기반 조작 작업에서의 계층적 제어를 구현한다.
- 🔗 후속 연구: [[papers/1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey/review]] — 계층적 diffusion policy라는 구체적 응용사례를 통해 서베이 내용을 확장합니다.
