---
title: "1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra"
authors:
  - "Shaofeng Yin"
  - "Yanjie Ze"
  - "Hong-Xing Yu"
  - "C. Karen Liu"
  - "Jiajun Wu"
date: "2025.11"
doi: "10.48550/arXiv.2509.20322"
arxiv: ""
score: 4.0
essence: "VisualMimic은 egocentric vision과 hierarchical whole-body control을 결합한 sim-to-real 프레임워크로, 인간의 동작 데이터로 학습한 task-agnostic keypoint tracker와 task-specific visuomotor policy를 통해 humanoid robot의 loco-manipulation을 실현한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yin et al._2025_VisualMimic Visual Humanoid Loco-Manipulation via Motion Tracking and Generation.pdf"
---

# VisualMimic: Visual Humanoid Loco-Manipulation via Motion Tracking and Generation

> **저자**: Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, Jiajun Wu | **날짜**: 2025-11-13 | **DOI**: [10.48550/arXiv.2509.20322](https://doi.org/10.48550/arXiv.2509.20322)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: VisualMimic consists of two training stages: 1) training a general keypoint tracker, where a teacher motion trac*

VisualMimic은 egocentric vision과 hierarchical whole-body control을 결합한 sim-to-real 프레임워크로, 인간의 동작 데이터로 학습한 task-agnostic keypoint tracker와 task-specific visuomotor policy를 통해 humanoid robot의 loco-manipulation을 실현한다.

## Motivation

- **Known**: Humanoid robot의 loco-manipulation은 기존에 외부 motion capture에 의존하거나 특정 작업에만 일반화되는 제약이 있었다. 또한 vision-based RL은 큰 exploration space로 인해 단순한 환경 상호작용(앉기, 계단 오르기)에만 제한되었다.
- **Gap**: Whole-body dexterity, loco-manipulation, visual policy를 모두 만족하면서 real-world에 zero-shot transfer 가능한 통합 프레임워크가 부재했다. 특히 keypoint command만으로는 human-like behavior를 완전히 포착하기 어려웠다.
- **Why**: Humanoid robot이 실제 환경에서 다양한 물체 조작과 이동을 동시에 수행할 수 있게 하는 것은 로보틱스의 오랜 목표이며, 외부 장비 없이 순수 egocentric vision만으로 작동 가능한 시스템은 실제 배포에 필수적이다.
- **Approach**: Teacher-student distillation 방식으로 (1) motion tracker를 이용해 전체 신체 동작을 학습한 후 keypoint tracker로 증류하고, (2) object state 접근권한이 있는 state-based policy로 먼저 학습한 후 visuomotor policy로 증류하며, action clipping과 noise injection으로 안정성을 확보한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Our visuomotor policies generalize across diverse space and time, shown on the box-pushing task.*

- **Zero-shot sim-to-real transfer**: Simulation에서만 학습한 정책이 실제 humanoid robot에 즉시 적용되어 복잡한 loco-manipulation 작업 수행
- **다양한 작업 성공**: 0.5kg 박스 1m 높이로 들어올리기, 3.8kg 대형 박스 밀기, football dribbling, kicking 등 diverse 작업 수행
- **Real-world 강건성**: 실외 환경에서 조명 변화, 불균형한 지면 등의 변수에도 안정적 성능 유지
- **Task-agnostic low-level policy**: 한 번 학습한 keypoint tracker가 모든 새로운 작업에 재사용 가능하여 scalability 향상

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: VisualMimic consists of two training stages: 1) training a general keypoint tracker, where a teacher motion trac*

- **Stage 1 - General Keypoint Tracker**: (1) Teacher motion tracker를 미래 reference motion에 대한 접근권한으로 RL 학습, (2) DAgger를 이용해 keypoint commands만으로 동작하는 student keypoint tracker로 증류
- **Stage 2 - Task-Specific Keypoint Generator**: (1) Object state가 주어진 state-based policy πgenerator_tea를 RL로 학습, (2) Egocentric vision과 proprioception만 사용하는 visuomotor policy πgenerator_stu로 distillation
- **Stability 메커니즘**: (1) Low-level policy 학습 중 noisy commands 적응을 위해 noise injection, (2) Human motion statistics에 기반한 action clipping으로 feasible action space 제약
- **Sim-to-real Gap 해결**: Simulation의 depth image에 heavy masking 적용하여 real-world sensor noise 근사
- **Hierarchical Interface**: Body keypoints (root, hands, feet, head)를 command interface로 사용하여 compact하면서도 expressive한 설계

## Originality

- **Teacher-student distillation의 이중 적용**: Motion tracker → keypoint tracker, state-based policy → visuomotor policy로 두 단계에서 progressive distillation 적용
- **Human motion statistics 기반 action clipping**: RL exploration의 불안정성을 human motion data의 통계 정보로 제약하는 novel approach
- **Hierarchical keypoint command interface**: 전체 신체 제어를 compact한 keypoint로 추상화하면서도 human-like behavior 유지
- **Egocentric vision + whole-body control의 통합**: 기존의 상반된 접근(upper-body vs locomotion, simulation-only vs real-world)을 통합적으로 해결

## Limitation & Further Study

- **Human motion data 의존성**: Keypoint tracker 학습이 curated human motion data에 크게 의존하여, 특이한 작업은 충분한 reference motion 필요
- **Sim-to-real domain gap 잔존**: Heavy masking 등으로 완화하나, 실제로는 여전히 다양한 환경(조명, 표면 재질 등)에서 테스트 필요
- **작업 특화성**: 각 새로운 작업마다 high-level policy 재학습 필요 (low-level은 재사용하나 여전히 task-specific training 필수)
- **평가의 제한성**: Real-world 실험이 주로 controlled setting과 제한된 outdoor 환경에서만 수행되어 극한 환경 성능 미지수
- **Keypoint command의 표현 한계**: Root, hands, feet, head만으로 모든 복잡한 신체 동작을 완전히 표현하기 어려울 수 있음

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VisualMimic은 teacher-student distillation의 창의적 이중 적용과 human motion statistics 기반 제약으로 humanoid loco-manipulation의 현실적 과제를 효과적으로 해결하며, 다양한 작업에서 zero-shot real-world transfer를 입증한 매우 의미 있는 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1749_VIRAL_Visual_Sim-to-Real_at_Scale_for_Humanoid_Loco-Manipula/review]] — 둘 다 visual humanoid loco-manipulation을 다루지만 VIRAL은 대규모 GPU 컴퓨팅에, VisualMimic은 motion tracking에 특화됩니다.
- 🔄 다른 접근: [[papers/1751_Visual_Imitation_Enables_Contextual_Humanoid_Control/review]] — 둘 다 비전 기반 humanoid 제어지만 VIDEOMIMIC은 real-to-sim-to-real, VisualMimic은 hierarchical 접근법을 사용합니다.
- 🏛 기반 연구: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — GMT의 일반적인 모션 추적 기술이 VisualMimic의 task-agnostic keypoint tracker 개발에 기여합니다.
- 🔄 다른 접근: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — 인간 모션을 휴머노이드로 적용하는 과제에서 시각적 모방과 자기지도 적응이라는 서로 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 일반적 모션 트래킹에서 전신 제어로의 확장에서 visual과 residual 접근법이라는 보완적 방법론을 다룬다.
- 🏛 기반 연구: [[papers/1902_EgoMI_Learning_Active_Vision_and_Whole-Body_Manipulation_fro/review]] — egocentric vision을 활용한 전신 조작 학습에서 active vision과 loco-manipulation이라는 관련 영역을 다룬다.
- 🔗 후속 연구: [[papers/1903_EgoMimic_Scaling_Imitation_Learning_via_Egocentric_Video/review]] — EgoMimic의 대규모 egocentric 비디오 모방 학습 기법이 VisualMimic의 egocentric vision 기반 동작 추적을 확장할 수 있다.
- 🏛 기반 연구: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — DeepMimic의 물리 기반 모방 학습 프레임워크가 VisualMimic의 동작 추적 방법론의 기초가 된다.
- 🔄 다른 접근: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — 인간 모션을 휴머노이드로 적응시키는 과제에서 자기지도 적응과 시각적 모방이라는 서로 다른 접근법을 사용한다.
- 🔄 다른 접근: [[papers/1646_RoboMirror_Understand_Before_You_Imitate_for_Video_to_Humano/review]] — RoboMirror와 VisualMimic 모두 비디오 기반 휴머노이드 제어를 다루지만 전자는 VLM 기반 intent 추출에, 후자는 visual imitation에 집중한다
- 🔄 다른 접근: [[papers/1612_PhysHMR_Learning_Humanoid_Control_Policies_from_Vision_for_P/review]] — 같은 비전 기반 humanoid motion imitation 문제를 motion tracking 접근법으로 해결
- 🔄 다른 접근: [[papers/1749_VIRAL_Visual_Sim-to-Real_at_Scale_for_Humanoid_Loco-Manipula/review]] — 둘 다 visual sim-to-real humanoid loco-manipulation을 다루지만 VisualMimic은 motion tracking에 더 초점을 맞춥니다.
- 🔄 다른 접근: [[papers/1751_Visual_Imitation_Enables_Contextual_Humanoid_Control/review]] — 둘 다 인간 영상에서 humanoid 제어를 학습하지만 VisualMimic은 hierarchical control에 더 중점을 둡니다.
- 🔗 후속 연구: [[papers/1969_HDMI_Learning_Interactive_Humanoid_Whole-Body_Control_from_H/review]] — VisualMimic의 visual tracking을 HDMI가 robot-object co-tracking으로 확장하여 더 복잡한 상호작용 시나리오를 처리합니다.
- 🔗 후속 연구: [[papers/1975_Hierarchical_visuomotor_control_of_humanoids/review]] — 시각적 모션 추적 모방이 계층적 시각운동 제어의 현대적 확장이다.
