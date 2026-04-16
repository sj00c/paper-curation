---
title: "1352_DemoDiffusion_One-Shot_Human_Imitation_using_pre-trained_Dif"
authors:
  - "Sungjae Park"
  - "Homanga Bharadhwaj"
  - "Shubham Tulsiani"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "DemoDiffusion은 단일 인간 시연으로부터 로봇이 조작 작업을 수행할 수 있도록 하는 방법으로, kinematic retargeting으로 얻은 궤적을 pre-trained diffusion policy를 이용해 개선한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Park et al._2025_DemoDiffusion One-Shot Human Imitation using pre-trained Diffusion Policy.pdf"
---

# DemoDiffusion: One-Shot Human Imitation using pre-trained Diffusion Policy

> **저자**: Sungjae Park, Homanga Bharadhwaj, Shubham Tulsiani | **날짜**: 2025-06-25 | **URL**: [https://arxiv.org/abs/2506.20668](https://arxiv.org/abs/2506.20668)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Retargeted human hand trajectory to closed-loop robot action sequence, for the task T : “shut down the*

DemoDiffusion은 단일 인간 시연으로부터 로봇이 조작 작업을 수행할 수 있도록 하는 방법으로, kinematic retargeting으로 얻은 궤적을 pre-trained diffusion policy를 이용해 개선한다.

## Motivation

- **Known**: Generalist manipulation policies는 대규모 로봇 데이터셋으로 학습되지만 zero-shot 배포 시 새로운 환경에서 실패하는 경향이 있다. Kinematic retargeting은 간단하지만 embodiment 차이로 인해 부정확하고 open-loop 실행이 brittle하다.
- **Gap**: 기존 방법들은 test-time reinforcement learning (비효율적), paired human-robot 데이터 (수집 어려움), 또는 순수 kinematic retargeting (낮은 정확도) 중 하나에 의존한다. Pre-trained diffusion policy를 활용하여 human demonstration을 closed-loop 방식으로 개선하는 방법이 부족하다.
- **Why**: 일반인이 수집할 수 있는 인간 시연만으로 로봇을 새로운 작업에 신속하게 적응시킬 수 있다면, 실제 환경에서 로봇 시스템의 배포 가능성이 크게 향상된다.
- **Approach**: Kinematic retargeting으로 인간 손 궤적을 로봇 end-effector 궤적으로 변환한 후, pre-trained diffusion policy를 통해 노이즈 제거(denoising) 과정으로 이 궤적을 정제하여 plausible robot actions 분포 내에 머물도록 한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Real-World Manipulation Tasks. Human demonstrations for the 8 evaluation tasks, shown as two frames per task.*

- **실세계 성능**: 8개의 다양한 조작 작업에서 83.8% 평균 성공률 달성 (pre-trained policy 13.8%, kinematic retargeting 52.5% 대비)
- **일반화 능력**: Pre-trained generalist policy가 완전히 실패하는 작업에서도 성공하는 사례 입증
- **실용성**: Test-time training이나 paired human-robot 데이터 없이 one-shot 배포 가능
- **단순성**: Kinematic retargeting과 diffusion denoising의 직관적인 조합으로 구현 용이

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Retargeted human hand trajectory to closed-loop robot action sequence, for the task T : “shut down the*

- 인간 시연으로부터 RGB-D 또는 multi-view 비디오 이용해 3D hand pose 추출
- Hand pose 궤적을 kinematic retargeting을 통해 로봇 end-effector 궤적으로 변환
- Retargeted 궤적에 Gaussian noise 추가
- Pre-trained diffusion policy π̄θ(at|o≤t,T)를 이용해 reverse SDE를 시뮬레이션하며 점진적으로 노이즈 제거
- 현재 관찰값(로봇 상태)에 조건화하여 closed-loop 제어 적용
- 정제된 로봇 action 궤적으로 실제 환경에서 작업 실행

## Originality

- Image editing의 diffusion model 활용 패러다임을 로봇 조작 분야로 적용한 참신한 전이
- Kinematic retargeting의 rough initialization을 diffusion policy의 prior로 정제하는 hybrid 접근법의 창의성
- Human demonstration과 pre-trained robot policy를 결합하되, 새로운 paired data나 online RL 없이 one-shot 배포를 달성한 점
- Embodiment gap을 closed-loop diffusion denoising으로 극복하는 방식의 혁신성

## Limitation & Further Study

- **Hand pose 추출 의존성**: 정확한 3D hand pose 추출이 필수이므로, 손이 가려지거나 추적이 어려운 상황에서 성능 저하 가능
- **Pre-trained policy 필요**: 광범위한 로봇 상호작용 데이터로 pre-trained diffusion policy 필수로, 이러한 데이터 없는 새로운 로봇/작업에 적용 어려움
- **Embodiment 차이 한계**: 인간과 로봇의 신체 구조가 크게 다른 경우 (예: dexterous hand vs. gripper) retargeting 자체가 부정확할 수 있음
- **평가 규모**: 8개 작업의 제한된 실세계 평가; 더 다양한 복잡한 작업에서의 일반화 능력 검증 필요
- **후속 연구**: 다중 인간 시연 활용, 부분적 가시성 환경에서의 robust hand pose 추정, cross-embodiment 적응 메커니즘 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DemoDiffusion은 pre-trained diffusion policy를 kinematic retargeting의 개선에 활용하는 우아한 접근법으로, 실제 환경에서 인간 시연만으로 로봇 조작을 가능하게 한다. 실세계 성능(83.8%)과 기존 방법 대비 우월성을 입증했으며, 실용적 배포 관점에서 높은 가치를 가진다.

## Related Papers

- 🔄 다른 접근: [[papers/1354_Dex1B_Learning_with_1B_Demonstrations_for_Dexterous_Manipula/review]] — 단일 시연과 10억 시연이라는 극단적으로 다른 데이터 규모에서의 모방학습 접근법을 비교합니다.
- 🏛 기반 연구: [[papers/1425_Human2Robot_Learning_Robot_Actions_from_Paired_Human-Robot_V/review]] — 인간-로봇 쌍 데이터를 통한 모방학습이 단일 시연 학습의 기반이 됩니다.
- 🔗 후속 연구: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — 인간 시연을 통한 모방학습에서 장기간 작업에 대한 구체적 해결책을 제시합니다.
- 🏛 기반 연구: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — DemoDiffusion의 적은 시연으로부터 학습하는 one-shot 모방 학습 개념이 RVT-2의 few-shot demonstration 학습 방법론의 기초가 된다.
