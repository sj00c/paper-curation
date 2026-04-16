---
title: "2046_Learning_Agile_Striker_Skills_for_Humanoid_Soccer_Robots_fro"
authors:
  - "Zifan Xu"
  - "Myoungkyu Seo"
  - "Dongmyeong Lee"
  - "Hao Fu"
  - "Jiaheng Hu"
date: "2025.12"
doi: "10.48550/arXiv.2512.06571"
arxiv: ""
score: 4.0
essence: "이 논문은 reinforcement learning 기반의 4단계 학습 프레임워크를 통해 인간형 로봇이 노이즈가 있는 센서 입력에서도 강건한 볼 킹킹 기술을 습득하도록 하는 시스템을 제시한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xu et al._2025_Learning Agile Striker Skills for Humanoid Soccer Robots from Noisy Sensory Input.pdf"
---

# Learning Agile Striker Skills for Humanoid Soccer Robots from Noisy Sensory Input

> **저자**: Zifan Xu, Myoungkyu Seo, Dongmyeong Lee, Hao Fu, Jiaheng Hu, Jiaxun Cui, Yuqian Jiang, Zhihan Wang, Anastasiia Brund, Joydeep Biswas, Peter Stone | **날짜**: 2025-12-10 | **DOI**: [10.48550/arXiv.2512.06571](https://doi.org/10.48550/arXiv.2512.06571)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Left: The network architectures for the teacher and the student network; Right: Multi-stage training framework: *

이 논문은 reinforcement learning 기반의 4단계 학습 프레임워크를 통해 인간형 로봇이 노이즈가 있는 센서 입력에서도 강건한 볼 킹킹 기술을 습득하도록 하는 시스템을 제시한다.

## Motivation

- **Known**: 인간형 로봇의 whole-body control은 locomotion과 manipulation 분야에서 RL을 통해 성공적으로 학습되어 왔다. 사족 로봇은 soccer 작업에서 높은 안정성을 가지고 있어 이미 협력 플레이와 정확한 슈팅을 달성했다.
- **Gap**: 인간형 로봇의 ball-kicking은 빠른 다리 스윙, 한 발 지지에서의 자세 안정성, 그리고 노이즈가 있는 지각 하에서의 강건성이 동시에 필요하지만 이러한 조건들을 모두 다루는 연구가 부족하다.
- **Why**: 인간형 로봇은 인간 환경에서 작동하도록 설계되었으며, soccer 같은 동적이고 지각-의존적 작업은 whole-body control의 실제 적용성을 검증하는 좋은 벤치마크가 된다.
- **Approach**: teacher-student 프레임워크를 확장하여, teacher는 ground-truth 상태 정보로 학습하고 student는 noisy perception으로부터 mimic하는 구조에, 4단계 curriculum 학습(ball chasing → directional kicking → policy distillation → constrained RL adaptation)을 추가했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Left: The network architectures for the teacher and the student network; Right: Multi-stage training framework: *

- **4단계 curriculum 학습 프레임워크**: long-distance chasing, directional kicking, DAgger 기반 policy distillation, N-P3O를 통한 online adaptation을 순차적으로 수행
- **현실적 지각 모델링**: velocity-dependent noise, delayed updates, frame drops를 포함하여 sim-to-real gap 감소
- **높은 kicking 정확도**: 실제 Booster T1 로봇에서 다양한 ball-goal 구성에 대해 평균 66.7% 성공률 달성
- **강건한 constrained RL 적응**: heterogeneous credit assignment를 통해 kick 직전의 부자연스러운 움직임(sharp turning, jittery leg motions) 제거
- **포괄적 ablation 연구**: constrained RL, noise modeling, adaptation stage의 필요성을 실증적으로 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Left: The network architectures for the teacher and the student network; Right: Multi-stage training framework: *

- Stage 1 (Teacher policy chasing): privileged ground-truth ball position을 사용하여 long-distance ball chasing 학습, aggressive domain randomization(external pushes)으로 imperfect state recovery 유도
- Stage 2 (Teacher policy kicking): teacher policy를 확장하여 directional kicking 학습, reward function은 ball-goal alignment와 kick strength 포함
- Stage 3 (Policy distillation): DAgger를 통해 teacher policy를 student policy로 distill, imperfect perception은 velocity-dependent noise model, temporal delays, frame drops로 모델링
- Stage 4 (Adaptation and refinement): N-P3O(constrained RL algorithm)를 사용하여 online adaptation, heterogeneous credit assignment로 motion refinement 수행
- Network architecture: history encoder와 MLP를 사용한 policy network, proprioceptive + ball/goal position estimate 입력
- Deployment: 학습된 student policy를 zero-shot으로 Booster T1 로봇에 배포

## Originality

- Teacher-student 프레임워크에 4단계 curriculum을 체계적으로 구성하여 progressive skill acquisition 달성
- Velocity-dependent noise model, delayed updates, frame drops를 종합적으로 포함한 현실적 지각 모델링
- Constrained RL(N-P3O)과 heterogeneous credit assignment를 결합하여 motion refinement 문제 해결
- Humanoid ball-kicking을 visuomotor whole-body control의 벤치마크 작업으로 체계화

## Limitation & Further Study

- 실제 로봇 평가가 Booster T1 한 종류의 로봇에만 제한됨, 다른 형태의 인간형 로봇에 대한 일반화 가능성 미확인
- 66.7% 성공률은 실제 soccer 경기에 충분하지 않을 수 있으므로, 추가적인 robustness 향상 필요
- 논문에서 computational cost와 학습 시간에 대한 상세한 분석 부재
- 외부 perturbation(opponents의 충돌)에 대한 구체적인 대응 전략이 제한적임
- 후속 연구: 다양한 humanoid morphology에 대한 일반화, real-time adaptation 메커니즘 개선, multi-agent soccer 시나리오로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 noisy perception 환경에서 인간형 로봇의 복잡한 동적 기술을 학습하는 현실적이고 체계적인 프레임워크를 제시하며, 4단계 curriculum, 현실적 지각 모델링, constrained RL 적응의 조합으로 sim-to-real gap을 효과적으로 감소시켰다. 실제 로봇 실험 결과와 포괄적 ablation 연구는 제안 방법의 타당성을 잘 입증하고 있으나, 단일 로봇 플랫폼 평가와 66.7% 성공률이 실무 적용성을 위해서는 추가 개선이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1648_RoboStriker_Hierarchical_Decision-Making_for_Autonomous_Huma/review]] — 휴머노이드 축구에서 강화학습 기반 킥킹 대신 계층적 의사결정을 통한 자율 축구 로봇 접근법을 제시한다.
- 🔗 후속 연구: [[papers/2063_Learning_Soccer_Skills_for_Humanoid_Robots_A_Progressive_Per/review]] — 노이즈 센서 입력에서의 강건한 킥킹 기술을 점진적 학습을 통한 포괄적인 축구 기술로 확장할 수 있다.
- 🏛 기반 연구: [[papers/1683_SoccerDiffusion_Toward_Learning_End-to-End_Humanoid_Robot_So/review]] — end-to-end 휴머노이드 축구 기술 학습의 기본 원리가 강건한 볼 킥킹 시스템 구현에 대한 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1979_HITTER_A_HumanoId_Table_TEnnis_Robot_via_Hierarchical_Planni/review]] — 둘 다 휴머노이드 스포츠 기술이지만 Learning Agile Striker는 축구 킥킹, HITTER는 탁구 기술 중심
- 🔗 후속 연구: [[papers/2003_Humanoid_Whole-Body_Badminton_via_Multi-Stage_Reinforcement/review]] — Learning Agile Striker의 강건한 볼 킥킹 기술이 배드민턴 전신 제어의 다단계 학습과 결합되어 더 다양한 스포츠 기술 달성 가능
- 🔗 후속 연구: [[papers/1683_SoccerDiffusion_Toward_Learning_End-to-End_Humanoid_Robot_So/review]] — 인간 시연으로부터 축구 스킬을 학습하는 기초 연구를 transformer diffusion으로 end-to-end 학습하도록 발전시킨다.
- 🧪 응용 사례: [[papers/1648_RoboStriker_Hierarchical_Decision-Making_for_Autonomous_Huma/review]] — Learning Agile Striker Skills의 축구 스트라이커 기술 학습이 RoboStriker의 계층적 권투 프레임워크를 다른 스포츠에 적용한 사례임
- 🔗 후속 연구: [[papers/1778_A_Hierarchical_Model-Based_System_for_High-Performance_Human/review]] — 불완전한 인간 데이터에서 학습하는 스트라이커 기술을 완전 통합된 축구 시스템으로 확장한 연구입니다.
- 🔄 다른 접근: [[papers/1889_Dribble_Master_Learning_Agile_Humanoid_Dribbling_through_Leg/review]] — 동일한 스포츠 도메인에서 축구 스킬 학습을 다루므로, 휴머노이드의 운동 기능 학습에 대한 비교 연구가 가능하다.
