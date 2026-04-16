---
title: "1568_Search-TTA_A_Multimodal_Test-Time_Adaptation_Framework_for_V"
authors:
  - "Derek Ming Siang Tan"
  - ""
  - "Boyang Liu"
  - "Alok Raj"
  - "Qi Xuan Ang"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Search-TTA는 위성 이미지와 현장 센서 측정을 활용하여 VLM(Vision Language Model)의 예측을 실시간으로 개선하는 멀티모달 테스트타임 적응 프레임워크로, 야외 로봇 시각 탐색 성능을 30%까지 향상시킨다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Tan et al._2025_Search-TTA A Multimodal Test-Time Adaptation Framework for Visual Search in the Wild.pdf"
---

# Search-TTA: A Multimodal Test-Time Adaptation Framework for Visual Search in the Wild

> **저자**: Derek Ming Siang Tan, , Boyang Liu, Alok Raj, Qi Xuan Ang, Weiheng Dai, Tanishq Duhan, Jimmy Chiun, Yuhong Cao, Florian Shkurti, Guillaume Sartoretti | **날짜**: 2025-05-16 | **URL**: [https://arxiv.org/abs/2505.11350](https://arxiv.org/abs/2505.11350)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3: Search-TTA Framework. During inference, given a satellite image and query inputs of other modal-*

Search-TTA는 위성 이미지와 현장 센서 측정을 활용하여 VLM(Vision Language Model)의 예측을 실시간으로 개선하는 멀티모달 테스트타임 적응 프레임워크로, 야외 로봇 시각 탐색 성능을 30%까지 향상시킨다.

## Motivation

- **Known**: VLM(예: CLIP)은 위성 이미지에서 환경-목표 관계를 추론하여 시각 탐색을 위한 우선 정보를 생성할 수 있다. 그러나 도메인 미스매치와 할루시네이션으로 인해 부정확한 예측이 발생할 수 있다.
- **Gap**: 기존 정보기반 경로 계획(IPP) 방식은 사전 정보를 고려하지 않거나, VLM의 오류를 탐색 중 수정할 메커니즘이 없다. 위성 이미지와 다중 모달 데이터로 학습한 야외 시각 탐색 데이터셋도 부족하다.
- **Why**: 환경 모니터링과 수색 구조 등 야외 로봇 응용에서 제한된 배터리와 센서 시야각 내에서 효율적인 탐색이 중요하며, VLM의 오류를 온라인으로 보정하면 탐색 성능을 크게 개선할 수 있다.
- **Approach**: 위성 이미지 인코더를 CLIP 인코더와 정렬하여 목표 존재 확률을 생성하고, Spatial Poisson Point Processes에서 영감을 받은 불확실성 가중 그래디언트 업데이트로 탐색 중 예측을 동적으로 개선한다. 동시에 380k 이미지를 포함한 AVS-Bench 데이터셋을 구축한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: Multimodal Alignment*

- **성능 개선**: Search-TTA는 계획자 성능을 최대 30.0%, 확률 맵 분포를 8.5% 향상시키며, 특히 CLIP 예측이 부족한 경우에서 두드러진다.
- **멀티모달 정렬**: 텍스트 및 음성 모달리티에 대해 추가 학습 없이 제로샷 일반화를 달성하며 emergent alignment를 시연한다.
- **규모 있는 VLM 비교**: 훨씬 더 큰 VLM과 비교할 수 있는 성능을 보이면서도 경량이다.
- **실제 배포**: 하드웨어인루프 테스트를 통해 실제 UAV에서 동작 가능함을 입증한다.
- **새로운 벤치마크**: 인터넷규모 생태계 데이터 기반 380k 학습 이미지와 8k 검증 이미지를 포함한 AVS-Bench 데이터셋을 공개한다.

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Search-TTA Framework. During inference, given a satellite image and query inputs of other modal-*

- 위성 이미지 인코더를 패치 레벨 대조 학습(contrastive learning)으로 CLIP 인코더와 정렬하여 다양한 모달리티 임베딩과의 코사인 유사도 기반 스코어 맵 생성
- 탐색 중 수집한 측정값(온보드 센서 감지)을 기반으로 불확실성 가중 그래디언트 업데이트 수행
- Spatial Poisson Point Processes에서 영감을 받은 정규화 메커니즘으로 안정적인 그래디언트 업데이트 보장
- 플러그앤플레이 인터페이스로 다양한 계획 방법(예: RL 기반)과 입력 모달리티(이미지, 텍스트, 음성) 호환성 제공
- AVS-Bench 데이터셋으로 인도메인(in-domain) 및 아웃도메인(out-of-domain) 분할로 평가

## Originality

- 위성 이미지와 현장 측정을 결합한 온라인 적응 프레임워크는 기존 VLM 기반 탐색 연구에서 미탐색 영역이다.
- Spatial Poisson Point Processes를 VLM 가중치 업데이트에 적용하는 것은 새로운 접근법이다.
- 다중 모달리티 정렬을 통한 emergent alignment의 시연은 인도메인/아웃도메인 일반화에 대한 새로운 통찰을 제공한다.
- 380k 이미지의 대규모 AVS-Bench 데이터셋은 야외 시각 탐색 연구의 중요한 자원이다.
- 모듈식 설계로 다양한 계획자 및 모달리티를 플러그앤플레이로 지원하는 유연성이 특이하다.

## Limitation & Further Study

- 실제 배포는 하드웨어인루프 시뮬레이션에 국한되며, 완전한 현장 실험이 부족하다.
- Spatial Poisson Point Processes 기반 업데이트의 이론적 정당성과 수렴 성질에 대한 분석이 제한적이다.
- 계산량 및 실시간 적응 가능성에 대한 상세한 논의가 필요하다.
- 다양한 환경(도시, 숲 등)과 계절 변화에 대한 견고성 평가가 부족하다.
- 후속 연구는 (1) 완전 현장 테스트, (2) 더 복잡한 멀티에이전트 탐색 시나리오, (3) 동적 환경에 대한 적응성 향상을 고려할 수 있다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Search-TTA는 야외 시각 탐색에서 VLM의 오류를 온라인으로 보정하는 혁신적인 프레임워크로, 대규모 AVS-Bench 데이터셋과 함께 멀티모달 적응과 실제 배포 가능성을 시연한다. 다만 완전한 현장 검증과 이론적 분석이 보완되면 더욱 완성도 있는 연구가 될 것이다.

## Related Papers

- 🏛 기반 연구: [[papers/1568_Search-TTA_A_Multimodal_Test-Time_Adaptation_Framework_for_V/review]] — Test-time adaptation 개념이 야외 로봇의 실시간 환경 적응에 핵심적인 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1342_CorrectNav_Self-Correction_Flywheel_Empowers_Vision-Language/review]] — 로봇의 환경 적응에서 Search-TTA는 멀티모달 테스트타임 적응으로, CorrectNav는 자기교정 메커니즘으로 접근한다.
- 🏛 기반 연구: [[papers/1611_Visual_Instruction_Tuning/review]] — Visual Instruction Tuning의 시각-언어 모델 최적화 기법이 Search-TTA의 VLM 예측 개선 방법론에 기반을 제공한다.
- 🔄 다른 접근: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — ApexNav가 zero-shot 객체 내비게이션에 중점을 두는 반면, Search-TTA는 멀티모달 센서 융합을 통한 시각 탐색 성능 향상에 초점을 맞춘다.
- 🏛 기반 연구: [[papers/1327_CEED-VLA_Consistency_Vision-Language-Action_Model_with_Early/review]] — CEED-VLA의 consistency vision-language-action 모델이 Search-TTA의 멀티모달 테스트타임 적응을 위한 기반 VLM 아키텍처를 제공한다.
- 🔗 후속 연구: [[papers/1490_NavigateDiff_Visual_Predictors_are_Zero-Shot_Navigation_Assi/review]] — NavigateDiff의 시각적 예측 기반 네비게이션을 멀티모달 센서 데이터와 실시간 적응을 통해 야외 로봇 환경으로 확장했다.
