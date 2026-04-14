# WHOLE: World-Grounded Hand-Object Lifted from Egocentric Videos

> **저자**: Yufei Ye, Jiaman Li, Ryan Rong, C. Karen Liu | **날짜**: 2026-02-25 | **URL**: [https://arxiv.org/abs/2602.22209](https://arxiv.org/abs/2602.22209)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Reconstruction Using the Generative Motion Prior. Given a metric-SLAMed egocentric videos, and the object temp*

WHOLE는 egocentric 비디오에서 손과 물체의 상호작용을 joint generative prior를 통해 world space에서 holistically 재구성하는 방법이다.

## Motivation

- **Known**: 기존 방법들은 hand pose estimation과 object pose estimation을 독립적으로 수행하거나 hand-object interaction을 단기 클립에서만 처리한다. Egocentric 비디오는 occlusion과 camera motion으로 인해 매우 challenging하다.
- **Gap**: 손과 물체의 motion을 jointly reasoning하지 않아 inconsistent hand-object relations를 초래하고, out-of-sight cases를 처리하지 못한다. 또한 global 3D world frame에서 장시간 interaction을 reconstruct하는 방법이 부족하다.
- **Why**: Egocentric video에서 손과 물체의 정확한 3D reconstruction은 robot learning, AR/VR 등 downstream applications에 필수적이며, 인간의 공간 reasoning 능력을 computer vision에 구현하는 핵심 과제이다.
- **Approach**: Diffusion-based generative motion prior를 학습하여 hand-object interaction의 joint dynamics를 모델링하고, test time에 visual observations와 VLM-derived contact cues로 이를 guided generation하여 globally consistent 3D trajectories를 생성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Given a metric-SLAMed egocentric video of a person interacting with the scene and the corresponding object tem*

- **Joint Generative Reconstruction**: Hand와 object motion을 jointly reasoning하는 diffusion model을 통해 inconsistent predictions를 해결하고 out-of-sight cases를 처리
- **State-of-the-art Performance**: Hand motion estimation, 6D object pose estimation, relative interaction reconstruction에서 모두 SOTA 달성
- **VLM-based Contact Detection**: Spatially grounded visual prompts로 VLM을 enhance하여 cluttered scenes에서도 robust한 contact localization 실현
- **Long Sequence Reconstruction**: Fixed-length window 기반으로 장시간 interaction sequences를 global 3D space에서 coherent하게 reconstruction

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Reconstruction Using the Generative Motion Prior. Given a metric-SLAMed egocentric videos, and the object temp*

- Diffusion model을 conditional generative prior로 사용하여 hand-object motion의 joint distribution p(H, T, C | O, H̄)을 학습
- Off-the-shelf hand estimator로부터 approximate hand trajectory H̄를 얻고 object template O와 함께 diffusion model의 conditioning input으로 활용
- Denoising process에서 alternating 방식으로 diffusion step과 guidance step을 수행하여 video observations와 일치하도록 refinement
- Gravity-aware local coordinate frame에서 motion prior를 학습하고 test time에 SLAM poses를 통해 world space로 변환
- VLM에 spatial visual prompts를 설계하여 hand-object contact를 automatically annotate하고 이를 guidance objective에 포함
- 2D segmentation masks와 contact cues를 guidance objectives로 하여 reconstructed trajectories가 video observations를 conform하도록 최적화

## Originality

- Hand와 object motion을 independent하게 처리하는 기존 접근에서 벗어나 joint generative model로 interdependency를 명시적으로 모델링
- Egocentric video에서 world frame reconstruction을 hand-object interaction의 맥락에서 addressing한 첫 시도로, global 4D motion capture를 실현
- VLM을 spatial grounding으로 enhance하는 novel approach로 contact detection의 automatic annotation 실현
- Gravity-aware local frame에서의 motion prior learning과 test-time guidance를 결합한 새로운 framework

## Limitation & Further Study

- Object template 제공이 필수적이어서 template-free scenarios에 적용 불가
- Metric SLAM poses에 의존하므로 SLAM failure 시 reconstruction quality 저하 가능
- Fixed-length time window (T=120) 제약으로 인한 장시간 interaction handling의 제한
- VLM contact annotation의 정확도가 ground truth에 비해 약간 떨어지는 경우 존재
- 후속 연구: template-free object reconstruction 통합, online SLAM with reconstruction, longer sequences handling, more diverse interaction types 확대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: WHOLE는 hand-object interaction을 joint generative model로 접근하는 paradigm shift를 제시하며, egocentric video에서 global 3D world frame reconstruction이라는 challenging 문제를 elegant하게 해결한 매우 우수한 연구이다.
