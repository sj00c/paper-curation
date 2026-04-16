---
title: "1401_GauDP_Reinventing_Multi-Agent_Collaboration_through_Gaussian"
authors:
  - "Ziye Wang"
  - "Li Kang"
  - "Yiran Qin"
  - "Jiahua Ma"
  - "Zhanglin Peng"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "GauDP는 다중 에이전트 협업 로봇 시스템에서 RGB 이미지로부터 3D Gaussian 필드를 구성하여 전역 일관성과 국소적 정밀성을 동시에 확보하는 새로운 표현 방식을 제안한다. 각 에이전트가 공유된 3D Gaussian 표현에서 과제 관련 특성을 동적으로 쿼리하여 협조와 개별 제어를 동시에 달성한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_GauDP Reinventing Multi-Agent Collaboration through Gaussian-Image Synergy in Diffusion Policies.pdf"
---

# GauDP: Reinventing Multi-Agent Collaboration through Gaussian-Image Synergy in Diffusion Policies

> **저자**: Ziye Wang, Li Kang, Yiran Qin, Jiahua Ma, Zhanglin Peng, Lei Bai, Ruimao Zhang | **날짜**: 2025-11-02 | **URL**: [https://arxiv.org/abs/2511.00998](https://arxiv.org/abs/2511.00998)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Both local and global context are essential in multi-agent collaboration. Comparison of*

GauDP는 다중 에이전트 협업 로봇 시스템에서 RGB 이미지로부터 3D Gaussian 필드를 구성하여 전역 일관성과 국소적 정밀성을 동시에 확보하는 새로운 표현 방식을 제안한다. 각 에이전트가 공유된 3D Gaussian 표현에서 과제 관련 특성을 동적으로 쿼리하여 협조와 개별 제어를 동시에 달성한다.

## Motivation

- **Known**: 기존 다중 에이전트 제어는 국소 관찰만 사용하면 협조 실패를 초래하고, 전역 관찰만 사용하면 세부 제어 능력이 부족하다. Neural Radiance Fields(NeRF)와 3D Gaussian Splatting(3DGS)은 다중 시점 이미지로부터 3D 장면 재구성에 효과적이다.
- **Gap**: 기존 접근법들은 국소 정밀성과 전역 일관성 사이의 균형을 맞추지 못하며, 특히 RGB 입력만으로 point cloud 기반 방법 수준의 성능을 달성하기 어렵다. 다중 에이전트 로봇 조작에 대한 데이터 기반 정책 학습 연구가 부족하다.
- **Why**: 산업 조립, 수술 로봇, 가정용 보조 로봇 등 다양한 실제 응용에서 다중 에이전트 협업이 필수적이며, 에이전트 간 충돌 회피와 작업 동기화를 위해 전역-국소 정보 통합이 중요하다.
- **Approach**: GauDP는 각 에이전트의 RGB 이미지로부터 전역적으로 일관된 3D Gaussian 필드를 재구성한 후, 각 에이전트의 국소 시점에 3D Gaussian 속성을 동적으로 재배치하여 공유 장면 표현에서 과제 관련 특성을 적응적으로 쿼리한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Visualization of Reconstruction Results. Our method achieves significantly improved*

- **RGB 입력 기반 성능**: Point cloud 기반 3D Diffusion Policy에 필적하는 성능을 RGB 입력만으로 달성하였다.
- **기존 방법 대비 우수성**: 이미지 기반 imitation learning 방법들을 현저히 초과하는 성능을 보였다.
- **확장성**: 에이전트 수 증가에 따라 강한 확장성을 유지하며 추가 아키텍처 변경 없이 확대 가능하다.
- **RoboFactory 벤치마크 검증**: 다양한 다중팔 조작 작업에서 검증되었다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: (a) Overview of the proposed GauDP framework for multi-agent imitation learning. Each*

- 각 에이전트의 임의 시점 RGB 관찰로부터 전역적으로 일관된 3D Gaussian 필드 재구성
- 3D Gaussian 속성(위치, 스케일, 회전, 불투명도, 색상)을 각 에이전트 국소 시점으로 동적 재배치
- 공유 3D Gaussian 표현에서 과제 관련 특성을 적응적으로 쿼리하는 메커니즘
- Diffusion Policy 프레임워크와 통합하여 순차 행동 생성
- 추가 센싱 모드(예: 3D point cloud) 없이 RGB만으로 구현

## Originality

- 3D Gaussian Splatting을 다중 에이전트 협업 로봇 제어에 최초 적용하여 전역-국소 정보 통합의 새로운 패러다임 제시
- 동적 특성 재배치 메커니즘으로 전역 일관성과 국소 정밀성을 동시에 달성하는 혁신적 접근
- RGB 입력만으로 point cloud 수준의 성능을 달성하는 효율적 표현 방식 개발

## Limitation & Further Study

- 구현 세부사항 부족: 3D Gaussian 필드 재구성의 최적화 절차, 카메라 자세 추정 방식, 특성 쿼리 메커니즘의 구체적 구현이 논문에 명시되어 있지 않음
- 실제 환경 검증 부재: RoboFactory 시뮬레이터에서만 평가되었으며 실제 로봇 플랫폼에서의 성능이 미검증
- 재구성 조건 가정: 정확한 카메라 자세와 충분한 관찰 중복을 가정하는데, 실제 로봇 환경에서의 이러한 조건 만족 가능성이 불명확
- 후속 연구 방향: 부분적 관찰(occlusion) 처리, 동적 환경에서의 실시간 재구성, 이질적 에이전트 간 협업 확대, 실제 환경으로의 이전학습(transfer learning)

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GauDP는 3D Gaussian Splatting을 창의적으로 활용하여 다중 에이전트 로봇 협업의 근본적 도전에 효과적으로 대응하는 혁신적 방법이다. 강력한 실험 결과와 명확한 동기 부여에도 불구하고, 실제 환경 검증의 부재와 기술적 구현 세부사항의 불충분한 설명이 한계로 지적된다.

## Related Papers

- 🏛 기반 연구: [[papers/1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering/review]] — 3D Gaussian Splatting의 실시간 렌더링 기술을 다중 에이전트 협업을 위한 공유 표현으로 확장했다.
- 🔗 후속 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment의 다중 로봇 학습 개념을 3D Gaussian 기반 협업 프레임워크로 발전시켰다.
- 🔄 다른 접근: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 둘 다 3D 표현을 VLA에 활용하지만 Gaussian fields vs generative world model이라는 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1539_RoboFactory_Exploring_Embodied_Agent_Collaboration_with_Comp/review]] — RoboFactory의 embodied agent collaboration이 GauDP의 3D Gaussian 기반 다중 에이전트 시스템을 더 복잡한 협업 시나리오로 확장합니다.
- 🧪 응용 사례: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — Cross-Embodied Learning의 정책 공유 방법이 GauDP의 공유 3D Gaussian 표현을 실제 다중 로봇 시스템에 적용하는 방법을 제시합니다.
- 🔗 후속 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — Multimodal Spatial Language Maps의 공간 표현이 GauDP에서 3D Gaussian field를 통한 다중 에이전트 공간 협업으로 더욱 발전한 형태이다.
- 🔄 다른 접근: [[papers/1539_RoboFactory_Exploring_Embodied_Agent_Collaboration_with_Comp/review]] — RoboFactory의 compositional constraints와 GauDP의 Gaussian Process 협력은 다중 에이전트 로봇 시스템에서 서로 다른 협력 모델링 접근법이다.
- 🔄 다른 접근: [[papers/1629_Whom_to_Trust_Elective_Learning_for_Distributed_Gaussian_Pro/review]] — 둘 다 multi-agent 시스템에서 협력 학습을 다루지만 Pri-GP는 신뢰도 기반을, GauDP는 Gaussian 분포 기반 접근법을 사용한다.
