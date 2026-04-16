---
title: "1500_OmniVLA_Physically-Grounded_Multimodal_VLA_with_Unified_Mult"
authors:
  - "Heyu Guo"
  - "Shanmu Wang"
  - "Ruichun Ma"
  - "Shiqi Jiang"
  - "Yasaman Ghasempour"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "OmniVLA는 RGB, 적외선, mmWave 레이더, 음향 마이크로폰 등 다중 센서를 통합하는 최초의 VLA 모델로, 센서-마스크된 이미지라는 통일된 표현을 통해 물리적 정보가 포함된 로봇 조작을 가능하게 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Multimodal_Sensor_Encoding"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Guo et al._2025_OmniVLA Physically-Grounded Multimodal VLA with Unified Multi-Sensor Perception for Robotic Manipul.pdf"
---

# OmniVLA: Physically-Grounded Multimodal VLA with Unified Multi-Sensor Perception for Robotic Manipulation

> **저자**: Heyu Guo, Shanmu Wang, Ruichun Ma, Shiqi Jiang, Yasaman Ghasempour, Omid Abari, Baining Guo, Lili Qiu | **날짜**: 2025-11-03 | **URL**: [https://arxiv.org/abs/2511.01210](https://arxiv.org/abs/2511.01210)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: System Overview. OmniVLA processes diverse sensor data into image-like 2D spatial representations, and then*

OmniVLA는 RGB, 적외선, mmWave 레이더, 음향 마이크로폰 등 다중 센서를 통합하는 최초의 VLA 모델로, 센서-마스크된 이미지라는 통일된 표현을 통해 물리적 정보가 포함된 로봇 조작을 가능하게 한다.

## Motivation

- **Known**: VLA 모델은 대규모 비전-언어 사전학습을 통해 로봇 조작에서 우수한 일반화 성능을 보이지만, 대부분 RGB 카메라에만 의존한다. 깊이, 촉각 등 추가 센서 통합 연구는 존재하지만 복잡한 아키텍처와 높은 데이터 요구량이 문제다.
- **Gap**: 기존 VLA 모델은 RGB 이외의 센서 모달리티(열상, 레이더, 음향)와의 효과적 통합 방법이 부족하며, 센서마다 다른 형식과 해상도를 처리하는 확장 가능한 표현이 없다.
- **Why**: 로봇이 인간처럼 다양한 센서 정보를 활용하면 폐쇄된 박스 속 물체 탐지, 옷 아래 벨소리, 온도 기반 작업 등 RGB만으로는 불가능한 복잡한 조작 작업을 수행할 수 있다.
- **Approach**: RGB 이미지에 다양한 센서 정보를 공간적으로 정렬된 마스크 형태로 오버레이하는 센서-마스크된 이미지 표현을 제안하고, 사전학습된 VLA 백본을 확장하여 경량의 센서별 projection 레이어를 추가한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Fig. 5: Examples of Robotic Manipulation Task Completion*

- **다중 센서 VLA의 최초 구현**: RGB, 적외선, mmWave 레이더, 음향 마이크로폰을 통합하는 첫 VLA 모델 개발
- **우수한 성능**: RGB 전용 기준 대비 59% 향상, 원본 센서 입력 기준 대비 28% 향상하여 평균 84% 작업 성공률 달성
- **데이터 효율성**: 원본 센서 기반 모델 대비 50% 데이터로 유사한 성능 달성
- **강한 일반화 능력**: 세 가지 미학습 작업에서 RGB 전용 및 원본 센서 모델을 각각 59%, 28% 상회

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: System Overview. OmniVLA processes diverse sensor data into image-like 2D spatial representations, and then*

- mmWave 레이더와 음향 배열 데이터를 beamforming 처리하여 2D 히트맵 형태의 센서 이미지로 변환
- VLM과 Grounded SAM을 이용한 의미 기반 분할로 관심 객체의 마스크 생성
- 생성된 마스크 영역에 센서 정보를 컬러로 오버레이하여 센서-마스크된 이미지 생성
- 동결된 vision encoder를 통과 후 센서별 경량 MLP projection 레이어를 적용하여 토큰 정렬
- LLM 백본과 diffusion 기반 action expert로 최종 로봇 동작 생성
- 다중 센서 로봇 암 플랫폼에서 RGB 카메라 및 센서 데이터와 조작 시연을 수집하여 학습

## Originality

- 센서-마스크된 이미지라는 신규 중간 표현으로 이질적 센서를 RGB 공간에 통일적으로 통합하는 창의적 접근
- 사전학습된 vision encoder를 재사용하면서도 다양한 센서 하드웨어에 대응 가능한 확장 가능 설계
- 열상, mmWave, 음향 등 기존 VLA에서 미탐색한 센서 모달리티의 로봇 조작 적용
- 단순하면서도 효과적인 경량 projection 레이어 기반 아키텍처로 데이터 효율성과 호환성 동시 달성

## Limitation & Further Study

- 평가가 특정 세 유형의 작업(열상 기반, mmWave 기반, 음향 기반)에 제한되어 다양한 실무 시나리오에서의 성능 검증 필요
- 센서 마스크 생성 과정에서 VLM과 SAM2에 의존하므로 이들 모델의 오류가 전파될 수 있음
- 수집된 데이터셋의 규모와 다양성이 명확히 제시되지 않아 재현 가능성과 일반화 범위 평가 어려움
- 센서 캘리브레이션, 부정렬, 하드웨어 변형에 대한 견고성 분석 미흡
- 후속 연구는 더 많은 센서 모달리티(초음파, 접촉 센서 등) 통합, 실시간 성능 최적화, 시뮬레이션-현실 이전 전략 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OmniVLA는 다중 센서를 VLA에 통합하는 문제에 대해 우아하고 실용적인 솔루션을 제시하며, 센서-마스크된 이미지라는 단순하면서도 효과적인 표현으로 확장 가능성과 데이터 효율성을 동시에 달성한 의미 있는 기여이다.

## Related Papers

- ⚖️ 반론/비판: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — 동일한 OmniVLA 이름으로 omni-modal vs multimodal sensor의 다른 통합 접근법 제시
- 🔄 다른 접근: [[papers/1500_OmniVLA_Physically-Grounded_Multimodal_VLA_with_Unified_Mult/review]] — 물리적 정보를 포함한 VLA에서 unified sensor representation vs 다른 센서 융합 방식
- 🏛 기반 연구: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — 다중 센서 VLA의 기초가 되는 proprioceptive-visual learning의 heterogeneous 접근
- 🏛 기반 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — 멀티모달 융합 기법의 이론적 배경은 OmniVLA의 다중 센서 통합 구현에 핵심적인 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OmniVLA와 OpenVLA 모두 비전-언어-액션 모델이지만 물리적 센서 정보 통합 여부에서 차별화됩니다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — 다중 센서 정보는 BitVLA의 1-bit 양자화된 VLA 모델에서도 활용 가능한 보완적 접근입니다.
- 🔗 후속 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — 멀티모달 융합 기술은 OmniVLA의 다중 센서 통합 접근법의 이론적 토대가 됩니다.
