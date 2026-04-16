---
title: "1617_PILOT_A_Perceptive_Integrated_Low-level_Controller_for_Loco-"
authors:
  - "Xinru Cui"
  - "Linxi Feng"
  - "Yixuan Zhou"
  - "Haoqi Han"
  - "Zhe Liu"
date: "2026.01"
doi: "10.48550/arXiv.2601.17440"
arxiv: ""
score: 4.0
essence: "PILOT는 humanoid robot의 loco-manipulation을 위한 통합 단계 RL 프레임워크로, 지각 기반 locomotion과 전신 제어를 단일 policy로 통합하여 비정형 지형에서 안정적인 작업 실행을 가능하게 한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Adaptive_Locomotion_Recovery"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cui et al._2026_PILOT A Perceptive Integrated Low-level Controller for Loco-manipulation over Unstructured Scenes.pdf"
---

# PILOT: A Perceptive Integrated Low-level Controller for Loco-manipulation over Unstructured Scenes

> **저자**: Xinru Cui, Linxi Feng, Yixuan Zhou, Haoqi Han, Zhe Liu, Hesheng Wang | **날짜**: 2026-01-24 | **DOI**: [10.48550/arXiv.2601.17440](https://doi.org/10.48550/arXiv.2601.17440)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Method overview of PILOT. We propose a unified single-stage reinforcement learning framework that seamlessly int*

PILOT는 humanoid robot의 loco-manipulation을 위한 통합 단계 RL 프레임워크로, 지각 기반 locomotion과 전신 제어를 단일 policy로 통합하여 비정형 지형에서 안정적인 작업 실행을 가능하게 한다.

## Motivation

- **Known**: Humanoid robot의 locomotion은 blind policy에서 perception 기반 elevation map 방식으로 발전했으며, 기존 whole-body controller들은 manipulation 능력이 제한적이었다.
- **Gap**: 기존 연구들은 지형 인식 없이 loco-manipulation을 수행하거나, lower-body와 upper-body를 분리하여 제어함으로써 자연스러운 whole-body 협응을 놓치고 있다.
- **Why**: Humanoid robot이 인간 중심 환경에서 계단이나 울퉁불퉁한 지형을 안전하게 이동하면서 조작 작업을 수행해야 하는 실제 응용이 필요하기 때문이다.
- **Approach**: Cross-modal context encoder로 proprioceptive features와 LiDAR 기반 elevation map을 fusion하고, Mixture-of-Experts 구조로 다양한 motor skill을 조정하여 통합된 perceptive loco-manipulation controller를 제안한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3. Real-world Experiments. PILOT successfully executes object transport tasks across challenging terrains. The robo*

- **통합 프레임워크**: 단일 policy로 perception-aware locomotion과 large-workspace whole-body control을 seamlessly 통합
- **다중 모달 인식**: Attention 기반 multi-scale perception encoder로 정확한 foot placement와 terrain awareness 강화
- **운동 기술 조정**: MoE 구조를 통해 locomotion과 manipulation 간의 자연스러운 전환 및 협응 실현
- **실제 성능**: Unitree G1 humanoid robot에서 stairs와 high steps 같은 복잡 지형에서 superior stability와 command tracking precision 달성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Visualization of expert activation across six motion modes. The*

- Robot-centric LiDAR 기반 elevation map으로 주변 지형 정보 캡처
- Prediction 기반 proprioceptive feature와 attention 기반 perceptive representation을 fusion하는 cross-modal context encoder 설계
- Random command sampling으로 feasible command space를 포괄적으로 커버하여 distribution bias 완화
- Mixture-of-Experts policy architecture로 diverse motor skill 간 coordination
- VR interface를 통한 teleoperation과 hierarchical RL 기반 autonomous task execution 지원

## Originality

- Perception-aware whole-body control의 단일 통합 policy 설계로 기존 decoupled approach의 한계 극복
- Cross-modal context encoder를 통한 proprioceptive와 exteroceptive feature의 principled fusion
- MoE 구조를 humanoid loco-manipulation 문제에 적용하여 motor skill 간 자동 specialization 실현
- Motion capture 데이터 대신 progressive random command sampling으로 distribution bias 제거

## Limitation & Further Study

- LiDAR elevation map의 계산 비용과 실시간 처리 가능성에 대한 분석 부재
- 다양한 humanoid robot 플랫폼에 대한 generalization 성능 평가 필요
- 복잡한 manipulation 작업(예: 정밀 assembly)에서의 성능 한계 가능성
- MoE 구조의 expert 수와 activation 메커니즘에 대한 ablation study 심화 필요
- Extremely steep terrain이나 동적 장애물 회피 시나리오에 대한 추가 평가 요구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: PILOT는 humanoid loco-manipulation 문제에 대한 통합적이고 실용적인 해결책을 제시하며, cross-modal perception과 MoE 구조를 통해 기술적 기여와 실제 로봇 구현의 성공적 사례를 보여준다.

## Related Papers

- 🔄 다른 접근: [[papers/1984_HoRD_Robust_Humanoid_Control_via_History-Conditioned_Reinfor/review]] — PILOT는 지각 기반 통합 제어를, HoRD는 이력 조건부 강화학습을 사용하여 휴머노이드 loco-manipulation을 다르게 해결함
- 🔗 후속 연구: [[papers/2017_HWC-Loco_A_Hierarchical_Whole-Body_Control_Approach_to_Robus/review]] — HWC-Loco의 계층적 전신 제어 접근법이 PILOT의 통합 저수준 제어 프레임워크를 더욱 체계적으로 확장함
- 🧪 응용 사례: [[papers/1978_Hiking_in_the_Wild_A_Scalable_Perceptive_Parkour_Framework_f/review]] — Hiking in the Wild의 인지 기반 파쿠어 프레임워크가 PILOT의 지각 기반 제어를 실제 험난한 지형에 적용한 사례임
- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — Loco-manipulation 통합 제어를 단일 policy 대신 residual policy 접근법으로 해결
- 🔗 후속 연구: [[papers/1974_Hierarchical_Vision-Language_Planning_for_Multi-Step_Humanoi/review]] — PILOT의 perception-based control을 hierarchical vision-language planning으로 확장
- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 통합 loco-manipulation을 single policy 대신 residual learning으로 해결
