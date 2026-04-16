---
title: "1070_Challenges_in_High-Throughput_Inorganic_Materials_Prediction"
authors:
  - "Josh Leeman"
  - "Yuhan Liu"
  - "Joseph Stiles"
  - "Scott B. Lee"
  - "Prajna Bhatt"
date: "2024"
doi: "10.1103/PRXEnergy.3.011002"
arxiv: ""
score: 4.0
essence: "고처리량 무기재료 자동 합성 및 예측 시스템의 핵심 문제점들을 분석한 관점 논문으로, Szymanski et al.의 A-lab 연구에서 43개 신규 재료 발견 주장이 신뢰할 수 없음을 지적하고 자동화된 재료 발견의 개선 방향을 제시한다."
tags:
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/AI-Driven_Scientific_Discovery"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Leeman et al._2024_Challenges in High-Throughput Inorganic Materials Prediction and Autonomous Synthesis.pdf"
---

# Challenges in High-Throughput Inorganic Materials Prediction and Autonomous Synthesis

> **저자**: Josh Leeman, Yuhan Liu, Joseph Stiles, Scott B. Lee, Prajna Bhatt, Leslie M. Schoop, Robert G. Palgrave | **날짜**: 2024-3-7 | **DOI**: [10.1103/PRXEnergy.3.011002](https://doi.org/10.1103/PRXEnergy.3.011002)

---

## Essence


고처리량 무기재료 자동 합성 및 예측 시스템의 핵심 문제점들을 분석한 관점 논문으로, Szymanski et al.의 A-lab 연구에서 43개 신규 재료 발견 주장이 신뢰할 수 없음을 지적하고 자동화된 재료 발견의 개선 방향을 제시한다.

## Motivation

- **Known**: 최근 구글 DeepMind는 220만 개의 새로운 결정질 무기 물질을 예측했으며, Berkeley의 A-lab은 로봇과 인공지능을 이용한 자동화된 재료 합성 시스템을 개발하여 71% 성공률을 보고했다.
- **Gap**: 자동화된 재료 발견 시스템에서 파우더 X선 회절(PXRD) 분석의 신뢰성이 부족하고, 재료 예측 시 원소의 결정학적 자리를 공유하는 무질서(disorder) 현상이 고려되지 않는 문제가 존재한다.
- **Why**: 새로운 무기 재료의 발견은 배터리, 데이터 저장, 태양전지 등 기술 혁신의 기초가 되므로, 자동화된 재료 발견이 신뢰할 수 있어야 한다.
- **Approach**: A-lab 논문의 43개 합성 산물 전체를 재분석하여 Rietveld 정제(refinement) 과정의 오류와 무질서한 재료의 미분류 문제를 체계적으로 검토하고, 고체 화학의 기본 원리에 입각한 비판적 분석을 수행한다.

## Achievement


- **Rietveld 분석의 신뢰성 문제 지적**: 자동화된 Rietveld 분석이 아직 신뢰할 수 없으며, AI 기반 Rietveld 피팅 도구 개발이 필수적임을 강조
- **무질서 효과의 과소평가 증명**: 예측된 화합물의 약 2/3이 이미 알려진 무질서 고용체(disordered solid solution) 또는 합금으로, 신규 재료가 아님을 규명
- **재료 신규성의 명확한 정의 제시**: 고체 화학에서 신규 재료를 정의하는 기준(결정 구조, 조성, 성질)을 명확히 하고, 다형체(polymorph)와 고용체의 구별 필요성 강조
- **4가지 분석 오류의 체계화**: 자동 정제 중 대칭성 변화, 공지상(known phase)과의 비교 부재, 혼합상 인식 실패, 무질서 무시 등의 반복적 오류 패턴 확인

## How


- A-lab 논문의 43개 전체 합성 산물에 대한 재검토 및 분류
- PXRD 패턴의 기존 알려진 상(known phases)과의 비교 분석
- Rietveld 정제 결과의 대칭성 변화 검증
- 조성 무질서(compositional disorder)를 고려한 결정학적 재평가
- 고체 화학 원리에 기반한 전문가 평가

## Originality

- 자동화된 재료 발견 시스템의 중요한 논문에 대한 체계적 재평가로, 고처리량 예측 방법론의 맹점을 구체적으로 드러냄
- 무질서 현상을 무기 재료 예측의 핵심 문제로 처음 강조하며, 계산 화학과 실험 화학 간의 패러다임 차이를 명확히 함
- 결정학적 대칭성과 조성 무질서의 관계를 명확히 설명하여 전문가와 비전문가 간의 소통 강화

## Limitation & Further Study

- 본 논문은 비판적 관점 제시에 중점을 두었으므로, Szymanski et al.의 반박이나 재분석 기회가 필요함
- 무질서를 계산 효율적으로 모델링하는 구체적 방법론은 제시되지 않았으며, 후속 연구에서 경제적 계산 방법 개발 필요
- AI 기반 Rietveld 피팅 도구의 구체적 개발 방향이나 벤치마크 제시 부재
- 다른 자동화 실험실(automated lab) 시스템에 대한 평가는 포함되지 않아, 일반화 가능성 제한

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 관점 논문은 고처리량 재료 예측의 현주소와 한계를 날카롭게 분석하며, 자동화 시스템의 신뢰성 문제를 구체적 사례로 제시함으로써 학계에 중요한 경종을 울린다. 특히 무질서(disorder)의 중요성과 Rietveld 분석의 자동화 한계를 강조한 점은 향후 재료 발견 연구의 방향성을 크게 바꿀 수 있는 기여이다.

## Related Papers

- ⚖️ 반론/비판: [[papers/1075_Open_Catalyst_2020_OC20_Dataset_and_Community_Challenges/review]] — 자동화된 재료 발견의 한계를 지적하면서 오픈 촉매 데이터셋 접근법과 대조된다.
- 🏛 기반 연구: [[papers/963_Forecasting_the_future_of_artificial_intelligence_with_machi/review]] — AI 예측의 한계를 이해하는 것이 재료 발견 자동화의 개선 방향 설정에 중요하다.
- ⚖️ 반론/비판: [[papers/1065_A_Survey_of_AI_Scientists/review]] — AI Scientist 시스템의 급속한 발전에 대한 낙관적 전망과 달리, 자동화된 재료 발견의 신뢰성 문제와 개선 필요성을 구체적으로 지적한다.
- 🔄 다른 접근: [[papers/1082_The_Open_Catalyst_2022_OC22_Dataset_and_Challenges_for_Oxide/review]] — 산화 상태 예측이라는 구체적 과제보다는 전반적인 무기재료 자동 합성 시스템의 방법론적 문제점을 비판적으로 분석한다.
- 🧪 응용 사례: [[papers/1051_Unsupervised_Word_Embeddings_Capture_Latent_Knowledge_from_M/review]] — 무기 재료 예측의 고처리량 방법론이 재료과학 문헌에서 추출한 잠재 지식을 실제 연구에 적용하는 사례이다.
- 🔄 다른 접근: [[papers/1082_The_Open_Catalyst_2022_OC22_Dataset_and_Challenges_for_Oxide/review]] — 고처리량 무기 재료 예측이라는 동일한 목표를 다른 재료 시스템에 적용
- 🔗 후속 연구: [[papers/1065_A_Survey_of_AI_Scientists/review]] — AI 기반 자동화된 과학 발견의 구체적 한계 사례를 제시하여, AI Scientist 시스템이 극복해야 할 실제 문제점들을 보여준다.
- 🏛 기반 연구: [[papers/1195_Mapping_the_Research_Landscape_of_Electronic_Properties_of_G/review]] — 고처리량 무기 재료 예측의 도전과제 연구가 그래핀 전자 특성 연구의 계산 복잡성과 예측 모델링 한계를 이해하는 데 중요한 배경을 제공한다.
