---
title: "1004_Quantifying_spatialtemporal_citation_diffusion_of_individual"
authors:
  - "Shuang Zhang"
  - "Feifan Liu"
  - "Haoxiang Xia"
date: "2025.12"
doi: "10.1002/asi.70021"
arxiv: ""
score: 4.0
essence: "본 논문은 문서 표현 학습 알고리즘을 활용하여 지식공간(knowledge space)에서 개별 논문의 인용(citation)이 시간과 공간적으로 어떻게 확산되는지를 정량화한다. 초기 인용 확산 특성이 장기 인용 누적과 논문의 혁신성(novelty)·파괴성(disruptiveness)을 어떻게 결정하는지를 밝힌다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Quantifying spatial–temporal citation diffusion of individual papers in knowledge space.pdf"
---

# Quantifying spatial–temporal citation diffusion of individual papers in knowledge space

> **저자**: Shuang Zhang, Feifan Liu, Haoxiang Xia | **날짜**: 12/2025 | **DOI**: [10.1002/asi.70021](https://doi.org/10.1002/asi.70021)

---

## Essence


본 논문은 문서 표현 학습 알고리즘을 활용하여 지식공간(knowledge space)에서 개별 논문의 인용(citation)이 시간과 공간적으로 어떻게 확산되는지를 정량화한다. 초기 인용 확산 특성이 장기 인용 누적과 논문의 혁신성(novelty)·파괴성(disruptiveness)을 어떻게 결정하는지를 밝힌다.

## Motivation

- **Known**: 개별 논문의 인용 동역학은 멱법칙 분포, '급증-감소(jump-decay)' 트렌드, 초우위 효과(preferential attachment) 등의 시간적 패턴을 보인다는 것이 알려져 있다. 또한 인용은 저널, 학과, 분야를 넘어 확산되며 단순 인용 수로는 논문의 장기 영향을 완전히 측정할 수 없다.
- **Gap**: 기존 연구는 시간적 인용 동역학에 집중했으나, 지식공간에서 인용의 공간적 확산-시간적 축적의 결합 과정(spatial-temporal patterns)은 거의 탐색되지 않았다. 특히 초기 공간적 확산 특성이 장기 인용 누적과 논문 혁신성에 미치는 영향은 미상이다.
- **Why**: 공간-시간적 인용 동역학을 이해하면 단기·장기 영향, 혁신성, 인용 누적의 복잡한 상호작용을 규명할 수 있어 과학평가체계 개선에 필수적이다. 또한 지식공간에서 논문의 광범위하고 먼 영향력을 평가할 수 있게 된다.
- **Approach**: 7개 대규모 학문분야의 수백만 개 논문에서 문서 표현 학습(document representation learning) 알고리즘을 적용하여 의미론적 연관성을 포착하고 저차원 임베딩 공간에서 인용 확산 궤적을 구성한다. 지식거리를 정량적으로 측정하여 공간-시간 확산 패턴을 분석한다.

## Achievement


- **지역화된 인용 이동성**: 인용 범위는 가우스 분포, 인용 거리는 지수 분포를 따르며 의미론적으로 국소화된 인용 패턴을 확인
- **초기 확산과 장기 영향의 연관성**: 초기 인용 확산 폭(breadth)이 넓을수록 장기 인용 성장이 크며, 초기 인용 수가 유사한 논문들 중에서 이 효과가 장기 영향을 크게 증폭
- **혁신/파괴적 논문의 차별적 패턴**: 혁신·파괴적 논문은 인용이 적고 지연되지만 초기에 더 긴 지식거리의 인용을 유인하며, 지식공간에서 광범위하고 먼 영향을 생성(고인용 논문보다도 큼)

## How


- 문서 표현 학습 알고리즘으로 7개 학문분야의 논문들을 저차원 임베딩 공간(지식공간)에 투영
- 각 논문의 인용자(citing papers)들을 시간 순서대로 추적하여 지식공간에서 인용 확산 궤적 구성
- 인용 범위(citation scope): 인용자가 분포한 지식거리 범위를 측정; 인용 거리(citation distance): 각 인용자와 원래 논문 간 임베딩 거리 계산
- 초기 확산 특성(초기 n년의 인용 범위와 거리)과 장기 인용 누적 간 상관분석 및 회귀분석(다른 변수 통제)
- 논문의 혁신성/파괴성을 분류하여 각 그룹의 공간-시간 인용 패턴 비교 분석

## Originality

- 지식공간에서 개별 논문 수준의 공간-시간적 인용 동역학을 정량화한 최초 연구
- 문서 표현 학습 알고리즘을 활용하여 '지식거리' 개념을 정량적으로 구현", '초기 공간적 확산 특성이 장기 인용과 논문 혁신성에 미치는 영향을 실증적으로 규명
- 혁신·파괴적 논문과 고인용 논문의 공간-시간 인용 패턴의 차별성을 체계적으로 밝힘

## Limitation & Further Study

- 7개 주요 학문분야에만 한정되어 다른 분야(인문학 등)의 일반화 가능성 제한
- 문서 표현 학습 알고리즘의 임베딩 공간이 학문적 의미를 완전히 포착하는지 검증 필요
- 인용 동기(방법론적 참고, 반박, 발전 등)를 구분하지 않음
- 후속 연구: 다양한 분야 확대, 인용 동기 분류 추가, 시간에 따른 공간 구조 변화 추적, 학제간 확산의 장기 효과 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 지식공간에서 인용의 공간-시간 확산을 정량화하여 기존 시간적 중심의 인용 분석에 공간적 차원을 추가한 창의적 연구이다. 초기 확산 특성이 장기 영향과 혁신성을 좌우한다는 발견은 과학평가체계와 연구 영향 예측에 중요한 함의를 제공한다.

## Related Papers

- 🏛 기반 연구: [[papers/1017_Science_as_exploration_in_a_knowledge_landscape_tracing_hots/review]] — 지식공간에서의 과학자 탐색 행동 모델링이 개별 논문의 인용 확산을 이해하는 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1050_Unsupervised_embedding_of_trajectories_captures_the_latent_s/review]] — 연구 궤적의 잠재적 구조를 포착하는 비지도 임베딩 방법으로 인용 확산 패턴을 다른 관점에서 분석합니다.
- 🧪 응용 사례: [[papers/962_Forecasting_high-impact_research_topics_via_machine_learning/review]] — 초기 인용 확산 특성을 활용하여 고영향 연구 주제를 예측하는 기계학습 모델에 적용할 수 있습니다.
- 🏛 기반 연구: [[papers/1051_Unsupervised_Word_Embeddings_Capture_Latent_Knowledge_from_M/review]] — 단어 임베딩이 지식의 잠재적 구조를 포착하는 능력은 지식공간에서 인용 확산을 정량화하는 방법론적 기반이 됩니다.
- 🔗 후속 연구: [[papers/995_Papers_and_patents_are_becoming_less_disruptive_over_time/review]] — 논문의 파괴성 감소 추세 분석은 개별 논문의 인용 확산과 혁신성 간의 관계를 거시적 관점에서 보완합니다.
- 🧪 응용 사례: [[papers/1054_Whats_In_Your_Field_Mapping_Scientific_Research_with_Knowled/review]] — 과학 연구를 지식 지도로 매핑하는 방법은 개별 논문의 공간적 인용 확산을 시각화하고 분석하는 도구를 제공합니다.
- 🔗 후속 연구: [[papers/1003_Quantifying_Long-term_Scientific_Impact/review]] — 논문의 장기 영향력을 시간뿐만 아니라 지식공간에서의 공간적 확산까지 고려하여 더 세밀하게 분석합니다.
- 🔗 후속 연구: [[papers/1017_Science_as_exploration_in_a_knowledge_landscape_tracing_hots/review]] — 지식공간에서의 과학자 탐색 행동 모델링을 개별 논문의 인용 확산 분석으로 확장 적용합니다.
- 🔗 후속 연구: [[papers/1056_Where_Do_Your_Citations_Come_From_Citation-Constellation_A_F/review]] — 개별 과학자의 공간-시간적 인용 확산과 인용 네트워크의 사회구조적 경로는 모두 인용의 확산 메커니즘을 분석한다.
- 🔗 후속 연구: [[papers/944_Co-Citation_Analysis_Bibliographic_Coupling_and_Direct_Citat/review]] — 인용 기반 유사성 분석을 공간-시간적 인용 확산 패턴 분석으로 확장하여 더 동적인 관점을 제공한다.
- 🏛 기반 연구: [[papers/951_Defining_and_identifying_Sleeping_Beauties_in_science/review]] — 인용의 시공간적 확산 분석이 잠자는 미녀 현상 이해의 이론적 토대를 제공한다
- 🔗 후속 연구: [[papers/1226_Evaluating_Open_Access_Advantages_for_Citations_and_Altmetri/review]] — 개별 논문의 시공간적 인용 확산 분석을 개방접근과 비개방접근 논문 비교로 확장합니다.
- 🔗 후속 연구: [[papers/984_Mapping_Scholarly_Impact_Citation_Analysis_of_Commerce_Docto/review]] — 개별 논문의 공간-시간적 인용 확산 패턴을 그래핀 연구 분야 전체의 지식 구조 발전과 연결하여 분석할 수 있다.
