---
title: "1080_Robust_Evidence_for_Declining_Disruptiveness_Assessing_the_R"
authors:
  - "Michael Park"
  - "Erin Leahey"
  - "Russell J. Funk"
date: "2026.03"
doi: "10.48550/arXiv.2503.00184"
arxiv: ""
score: 4.0
essence: "Park et al.의 과학 혁신성(disruptiveness) 하락 주장에 대한 Holst et al.의 비판을 반박하며, 영인용(zero backward citation) 논문 제외 후에도 통계적·실질적으로 유의한 하락이 지속됨을 입증한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Park et al._2026_Robust Evidence for Declining Disruptiveness Assessing the Role of Zero-Backward-Citation Works.pdf"
---

# Robust Evidence for Declining Disruptiveness: Assessing the Role of Zero-Backward-Citation Works

> **저자**: Michael Park, Erin Leahey, Russell J. Funk | **날짜**: 2026-03-19 | **DOI**: [10.48550/arXiv.2503.00184](https://doi.org/10.48550/arXiv.2503.00184)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Declining Disruptiveness Matches Major Benchmark Transformations in Science After Excluding Zero-*

Park et al.의 과학 혁신성(disruptiveness) 하락 주장에 대한 Holst et al.의 비판을 반박하며, 영인용(zero backward citation) 논문 제외 후에도 통계적·실질적으로 유의한 하락이 지속됨을 입증한다.

## Motivation

- **Known**: Park et al.(Nature, 2023)이 과학 논문과 특허의 혁신성이 지속적으로 하락함을 보였고, Holst et al.(HATWG)은 이것이 영인용 논문 포함에 따른 인공물(artifact)이라고 주장했다.
- **Gap**: HATWG의 비판이 제시한 데이터와 방법론의 근본적인 결함—특히 비연구 콘텐츠(아동도서, 편집물 등) 과다 포함으로 인한 영인용 논문 과잉 대표—에 대한 체계적 검증이 부족하다.
- **Why**: 과학 혁신성의 하락이 실제 현상인지 측정 오류인지 판별하는 것은 과학 정책, 연구 지원, 혁신 이해에 근본적으로 중요하며, 메타데이터 품질 문제는 과학계량학 연구의 신뢰성을 좌우한다.
- **Approach**: HATWG의 제시 데이터셋, 지표, 영인용 제외 기준을 그대로 채택하여 재분석하고, 그들의 회귀모형을 적용하며, SciSciNet 데이터의 문서 유형 분류를 통해 메타데이터 품질 문제를 정량화한다.

## Achievement


- **영인용 제외 후에도 유의한 하락 확인**: HATWG의 권장 방식(SciSciNet 데이터, CD5 지표, 영인용 제외)을 따랐을 때도 1945-2010년 사이 혁신성이 15.53 백분위수 포인트 하락(p<0.001)
- **HATWG 회귀모형의 모순 노출**: 그들이 영인용 편향 해소를 위해 설계한 회귀모형이 오히려 논문(β=-0.082, p<0.001)과 특허(p<0.001) 모두에서 큰 하락을 보이며, 이는 그들의 중심 주장과 직접 모순
- **메타데이터 품질 문제의 정량화**: HATWG 데이터에 편집물·부고·평론 280만 개, 도서·학위논문 150만 개, 제품·예술 평론 25.4만 개 등 비연구 콘텐츠가 샘플의 20%를 차지하며, 이들이 1945-2010년 사이 40%→8%로 감소한 것이 영인용 감소 추세를 설명
- **실질적 의미의 벤치마크 비교**: 혁신성 하락이 팀 규모 증가(27.96점)에 이어 두 번째로 큰 과학 구조 변화이며, 여성 참여 증가(13.56점), 인용 관행 변화(13.21점)와 비슷한 규모

## How


- HATWG의 SciSciNet 데이터를 Web of Science, OpenAlex 등 외부 데이터베이스와 링크하여 문서 유형 분류 수행
- 키워드 검색을 통해 비연구 콘텐츠 구체적 사례 확인(For Dummies 456건, Dr. Seuss 26권, Captain Underpants 등)
- Paper-level disruptiveness(CD5)를 종속변수로 하는 회귀분석, 발행연도 고정효과와 영인용 지표 포함
- 1945-2010년(논문) 및 1980-2010년(특허) 기간 동안의 예측된 혁신성 변화량(β 계수) 산출 및 p값 검증
- 4가지 추가 혁신성 지표(SciSciNet, WoS)를 활용한 민감도 분석(robustness check)
- Wang and Barabasi의 벤치마크 변화(팀 규모, 여성 참여, 국제 협력, 인용 관행 등)와 백분위수 정규화하여 비교

## Originality

- 비판자의 제시 방법론과 데이터를 그대로 채택하여 오히려 자신의 주장을 강화하는 역설적 접근
- 메타데이터 품질 문제를 단순 주장이 아닌 구체적 문서 유형 분류와 키워드 검색으로 정량화하고 시계열 변화 추적
- 근 100개 독립 연구(다중 데이터베이스, 지표, 비인용 기반 측정)의 체계적 종합으로 현상의 견고성 입증
- 실질적 의미를 통계적 의의와 별도로 벤치마크 비교를 통해 평가하는 2차원 타당성 검증

## Limitation & Further Study

- SciSciNet 데이터 연계 시 완전성 부족—보수적 추정치만 제시되어 실제 비연구 콘텐츠 규모는 더 클 가능성
- 영인용 논문의 포함/제외 논의가 이론적 정당성(혁신적 결과는 영인용할 수 있음)에만 의존하며, 실증적으로 혁신성과의 관계를 분석하지 않음
- HATWG의 시각적 검증 방식 비판이 타당하나, 본 저자들도 Figure 1에서 시각적 표현에 의존함
- 후속 연구: (1) 비연구 콘텐츠의 체계적 제외 기준 개발, (2) 혁신성과 영인용 상태의 인과관계 분석, (3) 다른 과학계량학 지표(h-index, 임팩트 팩터 등)에서의 메타데이터 오염 규모

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 데이터 품질 문제를 명확히 입증하고 비판자의 회귀모형이 자신의 주장을 역설적으로 지지함을 보임으로써 혁신성 하락의 견고성을 강하게 재확인하며, 메타데이터 검증의 중요성을 강조한 의미 있는 반박.

## Related Papers

- 🏛 기반 연구: [[papers/995_Papers_and_patents_are_becoming_less_disruptive_over_time/review]] — 논문과 특허의 파괴성 감소에 대한 원래 연구가 영인용 논문 영향을 분석한 반박 연구의 기반이 된다.
- 🔗 후속 연구: [[papers/1122_The_disruption_index_suffers_from_citation_inflation_Re-anal/review]] — 파괴성 지수가 인용 인플레이션으로 고통받는다는 분석과 영인용 논문의 역할 분석은 모두 파괴성 측정의 방법론적 문제를 다룬다.
- 🧪 응용 사례: [[papers/1005_Quantifying_the_dynamics_of_failure_across_science_startups/review]] — 파괴적 혁신의 감소에 대한 강건한 증거는 과학 분야에서 반복된 실패 후 성공으로 이어지는 패턴 변화를 뒷받침합니다.
- 🔄 다른 접근: [[papers/1122_The_disruption_index_suffers_from_citation_inflation_Re-anal/review]] — 혁신성 감소에 대한 강건한 증거 제시가 인용 인플레이션으로 인한 CD 지수 편향과 다른 관점을 제공한다.
- 🔗 후속 연구: [[papers/995_Papers_and_patents_are_becoming_less_disruptive_over_time/review]] — 혁신성 감소에 대한 견고한 증거 평가로 논문과 특허의 파괴성 감소 연구가 확장된다.
- 🏛 기반 연구: [[papers/936_Atypical_Combinations_and_Scientific_Impact/review]] — 비전형적 조합과 과학 영향력의 관계가 파괴적 혁신 감소 현상의 이론적 배경 제공
- 🔗 후속 연구: [[papers/977_Introducing_multiverse_analysis_to_bibliometrics_The_case_of/review]] — 파괴성 감소에 대한 견고한 증거를 제시한 연구로, 팀 규모와 파괴적 연구의 관계를 다중우주분석으로 확장 검토할 수 있습니다.
- 🔗 후속 연구: [[papers/1138_Arts_and_Humanities_Citation_Index_for_Research_Evaluation_i/review]] — 과학의 파괴성 감소에 대한 견고한 증거 연구가 인문학 분야 인용 색인의 한계를 과학 전반의 맥락에서 설명하기 때문
- ⚖️ 반론/비판: [[papers/984_Mapping_Scholarly_Impact_Citation_Analysis_of_Commerce_Docto/review]] — 과학의 파괴적 혁신성 감소에 대한 강력한 증거는 그래핀 연구처럼 특정 분야의 지속적인 발전과 상반되는 관점을 제시한다.
