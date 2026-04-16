---
title: "1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering"
authors:
  - "Bernhard Kerbl"
  - "Georgios Kopanas"
  - "Thomas Leimkühler"
  - "George Drettakis"
date: "2023.08"
doi: ""
arxiv: ""
score: 4.0
essence: "3D Gaussian Splatting은 3D 가우시안 표현과 실시간 렌더링 알고리즘을 결합하여 고품질의 novel-view synthesis를 1080p 해상도에서 30fps 이상으로 달성하는 방법이다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kerbl et al._2023_3D Gaussian Splatting for Real-Time Radiance Field Rendering.pdf"
---

# 3D Gaussian Splatting for Real-Time Radiance Field Rendering

> **저자**: Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis | **날짜**: 2023-08-08 | **URL**: [https://arxiv.org/abs/2308.04079](https://arxiv.org/abs/2308.04079)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Our method achieves real-time rendering of radiance fields with quality that equals the previous method with the*

3D Gaussian Splatting은 3D 가우시안 표현과 실시간 렌더링 알고리즘을 결합하여 고품질의 novel-view synthesis를 1080p 해상도에서 30fps 이상으로 달성하는 방법이다.

## Motivation

- **Known**: NeRF 이후 radiance field 방법들이 novel-view synthesis를 혁신했으나, 고품질 달성을 위해 신경망 학습과 렌더링이 비용이 크고, 빠른 방법들은 품질을 포기하는 트레이드오프가 존재한다.
- **Gap**: 기존 방법들은 고품질과 실시간 렌더링을 동시에 달성하지 못했으며, unbounded scenes의 1080p 해상도 실시간 렌더링(>=30fps)은 불가능했다.
- **Why**: 실시간 novel-view synthesis는 VR/AR, 3D 콘텐츠 제작 등 많은 응용에서 필수적이며, 품질과 속도를 동시에 달성하는 방법의 개발은 실용적 가치가 매우 높다.
- **Approach**: 3D Gaussian을 사용한 scene 표현으로 연속적 volumetric 성질을 유지하면서 빈 공간 계산을 피하고, 최적화 중 density control을 수행하며, visibility-aware anisotropic splatting 렌더링 알고리즘을 개발했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Our method achieves real-time rendering of radiance fields with quality that equals the previous method with the*

- **실시간 렌더링**: 1080p 해상도에서 >= 30fps의 실시간 렌더링 달성 (93-135fps)
- **최고 품질**: Mip-NeRF360과 동등하거나 우수한 PSNR (25.2 vs 24.3)
- **빠른 학습**: 경쟁력 있는 학습 시간 (6-51분) 유지
- **효율적 표현**: 1-5백만 개의 컴팩트한 3D Gaussian으로 scene 표현

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Optimization starts with the sparse SfM point cloud and creates a set of 3D Gaussians. We then optimize and adap*

- SfM sparse point cloud로부터 3D Gaussian 초기화
- 3D position, opacity α, anisotropic covariance, spherical harmonic 계수 최적화
- 최적화 중 적응적 density control로 Gaussian 추가/제거
- GPU 기반 tile-rasterization과 fast sorting을 활용한 visibility-aware rendering
- Anisotropic splatting과 α-blending으로 정확한 image formation model 구현
- 빠른 backward pass를 위해 sorted splats 순회 추적

## Originality

- Anisotropic 3D Gaussian을 radiance field 표현으로 도입 - 기존 point-based 방법과 달리 volumetric 성질 유지
- Interleaved optimization과 adaptive density control의 조합으로 효율적 scene 표현
- Visibility-aware anisotropic splatting - 기존 tile-based rasterization을 3D Gaussian에 적용
- SfM sparse points만으로 고품질 결과 달성 - 기존 MVS 의존성 제거

## Limitation & Further Study

- 매우 복잡한 scene이나 extreme viewing angle에서의 성능 평가 부재
- 동적 scene이나 temporal consistency 처리 미지원
- Gaussian 개수(1-5M)가 많아 메모리 요구사항 상당할 수 있음
- 후속 연구: dynamic scene extension, memory-efficient representation, 더 큰 unbounded scene 처리

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 3D Gaussian Splatting은 radiance field 렌더링에서 품질과 속도의 근본적 트레이드오프를 해결하는 획기적 방법으로, 실시간 고품질 novel-view synthesis를 처음으로 실현한 매우 중요한 기여이다.

## Related Papers

- 🧪 응용 사례: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — 3D Gaussian Splatting의 실시간 렌더링 기술을 ManiSkill3의 GPU 병렬 시뮬레이션에 적용할 수 있습니다.
- 🔗 후속 연구: [[papers/1523_Re3Sim_Generating_High-Fidelity_Simulation_Data_via_3D-Photo/review]] — 고품질 3D 장면 렌더링 기술을 3D-photo guided 시뮬레이션 데이터 생성에 활용할 수 있습니다.
- 🔄 다른 접근: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — 실시간 고품질 시각화에서 Gaussian Splatting과 iGibson의 물리 시뮬레이션이 다른 접근법을 제공합니다.
- 🏛 기반 연구: [[papers/1401_GauDP_Reinventing_Multi-Agent_Collaboration_through_Gaussian/review]] — 3D Gaussian Splatting의 실시간 렌더링 기술을 다중 에이전트 협업을 위한 공유 표현으로 확장했다.
- 🔗 후속 연구: [[papers/1384_EnerVerse_Envisioning_Embodied_Future_Space_for_Robotics_Man/review]] — 3D Gaussian Splatting을 4D로 확장하여 시공간적 embodied future space 생성에 적용했다.
- 🏛 기반 연구: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — LERF의 언어 임베딩 방법론이 3D Gaussian Splatting의 실시간 렌더링과 결합되어 더 효율적인 3D 언어 필드를 구현할 수 있습니다.
- 🔗 후속 연구: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — 3D Gaussian splatting의 실시간 렌더링 기술을 3D 포인트 변위 예측과 결합하여 더 정확하고 효율적인 장면 모델링을 달성한다.
- 🔗 후속 연구: [[papers/1552_RoboTwin_Dual-Arm_Robot_Benchmark_with_Generative_Digital_Tw/review]] — 3D Gaussian Splatting의 실시간 3D 렌더링 기술이 RoboTwin의 generative digital twin 구현에 시각적 품질 향상을 제공한다.
- 🔄 다른 접근: [[papers/1587_Time-Transient_Wireless_RF_Sensor_with_Differentiative_Detec/review]] — Time-Transient RF 센서와 3D Gaussian Splatting은 모두 실시간 환경 감지를 다루지만 무선 RF와 시각적 렌더링이라는 다른 센서 모달리티를 사용한다.
- 🏛 기반 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — 3D Gaussian Splatting의 실시간 3D 장면 표현 기술이 VoxPoser의 3D value map 생성에 핵심적인 기반 기술을 제공한다
- 🏛 기반 연구: [[papers/1625_VR-Robo_A_Real-to-Sim-to-Real_Framework_for_Visual_Robot_Nav/review]] — 3D Gaussian Splatting은 VR-Robo의 포토리얼리스틱 디지털 트윈 구성을 위한 핵심 렌더링 기술을 제공합니다.
