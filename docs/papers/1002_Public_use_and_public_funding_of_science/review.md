---
title: "1002_Public_use_and_public_funding_of_science"
authors:
  - "Yian Yin"
  - "Yuxiao Dong"
  - "Kuansan Wang"
  - "Dashun Wang"
  - "Benjamin F. Jones"
date: "2022"
doi: "10.1038/s41562-022-01397-5"
arxiv: ""
score: 4.0
essence: "공적 자금으로 지원되는 과학연구가 실제로 공중의 필요와 일치하는지 대규모 데이터 연계를 통해 실증적으로 검증한 연구이다. 정부문서, 뉴스미디어, 특허 등 세 개의 공공 영역에서 과학의 활용 패턴을 분석하고 공적 자금 배분과의 정렬성(alignment)을 측정했다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Public_Science_Funding"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yin et al._2022_Public use and public funding of science.pdf"
---

# Public use and public funding of science

> **저자**: Yian Yin, Yuxiao Dong, Kuansan Wang, Dashun Wang, Benjamin F. Jones | **날짜**: 2022 | **DOI**: [10.1038/s41562-022-01397-5](https://doi.org/10.1038/s41562-022-01397-5)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1 | Diversity in public use. a–t, Different scientific fields experience*

공적 자금으로 지원되는 과학연구가 실제로 공중의 필요와 일치하는지 대규모 데이터 연계를 통해 실증적으로 검증한 연구이다. 정부문서, 뉴스미디어, 특허 등 세 개의 공공 영역에서 과학의 활용 패턴을 분석하고 공적 자금 배분과의 정렬성(alignment)을 측정했다.

## Motivation

- **Known**: 과학은 공공재(public good)로서 정부의 공적 자금 지원을 받으며, 이러한 제도 설계는 과학의 광범위한 활용을 가능하게 한다는 것이 알려져 있다. 그러나 과학과 공중의 이익 간 괴리를 주장하는 '두 공동체 이론(two communities theory)'과 '상아탑 비판'이 지속적으로 제기되어 왔다.
- **Gap**: 공적 자금이 실제로 공중의 과학 활용 패턴과 일치하는지를 대규모 체계적 데이터로 실증적으로 검증한 연구가 부족했다. 기존에는 데이터 수집의 어려움으로 인해 공적 영역에서의 과학 활용 실태를 정량적으로 측정하기 어려웠다.
- **Why**: 공적 자금의 효율성과 과학정책의 정당성을 검증하기 위해 공적 투자와 공적 활용 간의 실제 정렬성을 파악하는 것이 필수적이다. 또한 과학이 정부, 산업, 미디어 등 사회 각 분야에서 실제로 어떻게 활용되는지 이해하는 것은 과학의 사회적 역할을 규명하는 데 중요하다.
- **Approach**: Microsoft Academic Graph, Bing 검색엔진, Altmetric, USPTO 특허 데이터, Dimensions 자금 데이터 등 5개의 대규모 데이터셋을 연계하여 2005-2014년 발행 논문의 상류(펀딩) 및 하류(공공활용)를 추적했다. 상대소비지수(Relative Consumption Index, RCI)를 개발하여 과학 분야별 공공 영역별 활용 패턴의 특이성을 정량화했다.

## Achievement


- **공공 활용의 다양성 규명**: 각 과학 분야는 정부, 뉴스, 특허 등 공공 영역에서 특화된 활용 패턴을 보이며, 컴퓨터과학·공학은 특허 중심, 사회과학은 정부·미디어 중심, 생물학은 전 영역에서 광범위하게 활용된다.
- **과학적 영향력과 공중 활용의 정렬**: 공중이 소비하는 과학 아이디어가 과학 공동체 내에서 높은 영향력을 지닌 논문과 긍정적으로 상관관계를 보이며, '상아탑' 비판을 부분적으로 반박한다.", '**공적 자금과 공적 활용의 일관성**: 각 과학 분야의 공적 자금 배분이 해당 분야의 집단적 공공 활용(public use)과 놀라울 정도로 정렬되어 있음을 입증했다.
- **시간 지연의 차이 발견**: 뉴스미디어는 최근 연구(연내 63%)에 집중하는 반면, 정부문서와 특허는 중앙값 10년의 시간 지연을 보이는 구별되는 활용 패턴을 규명했다.

## How


- Microsoft Academic Graph(MAG)의 1,900만 편의 과학논문을 19개 최상위 과학 분야로 분류
- Bing 검색엔진을 통해 미국 정부 전 부처의 600만 개 정부문서 수집 후 기계독해(machine reading) 기술으로 학술논문 인용 자동 식별
- Altmetric 데이터베이스에서 2,701개 미디어 매체의 학술논문 언급 추적 및 연결
- USPTO 특허 전체 데이터와 학술논문 인용 관계 연결 (약 194만 건의 특허-논문 링크)
- Dimensions 데이터셋(400개 이상 펀딩기관, 500만 개 프로젝트)과 논문 매칭을 통해 상류 자금 정보 연계
- 상대소비지수(RCI) 개발: RCI = (특정 분야의 공공영역 인용 비율) ÷ (전체 분야의 공공영역 인용 비율)
- 논문의 과학적 영향력(인용수) 대비 공공 영역에서의 인용 빈도 비교분석
- 분야별·부처별·미디어별 세부 수준에서의 특화도(specialization) 분석

## Originality

- **다중 데이터셋 통합 분석**: 펀딩, 논문, 특허, 정부문서, 뉴스 등 5개 데이터 스트림을 최초로 대규모로 연계하여 과학의 생명주기 전체를 추적한 혁신적 방법론
- **기계독해 기술 활용**: Bing 검색엔진을 기반으로 미국 전 정부부처의 600만 문서에서 학술논문 인용을 자동으로 식별하는 새로운 데이터 수집 방식
- **상대소비지수(RCI) 개발**: 분야 간 출판량 차이를 정규화하여 공공 활용의 특화도를 정량적으로 측정하는 새로운 지표 개발
- **질적 다양성과 양적 정렬의 동시 발견**: 공공 영역의 과학 활용이 매우 다양한 특화 패턴을 보이면서도, 거시적으로는 자금 배분과 일관성 있게 정렬된다는 역설적 발견

## Limitation & Further Study

- **미국 중심 분석**: 정부문서(미국 정부), 특허(USPTO)에 미국 데이터만 포함되어 국가별 차이와 국제적 일반화 가능성 제한
- **시간 범위 제한**: 주요 분석이 2005-2014년 논문으로 국한되어 근래(2015년 이후) 변화 추이 미상
- **'공적 활용'의 협소한 정의**: 정부 인용, 특허 인용, 뉴스 언급만 포함하며 교육, 임상진료, 비영리기관 활용 등 다른 공공 영역 미포함", '**인과관계 미확인**: 데이터 연관성만 보이며, 공적 자금이 실제로 공공 활용을 유도하는지, 아니면 역으로 인기 있는 분야에 자금이 몰리는 건지 인과 방향성 불명확
- **기계독해 오류율**: 정부문서에서 학술논문 인용을 자동으로 추출할 때의 정확성 및 위양성(false positive) 검증 필요
- **매체 선택 편향**: 뉴스 분석이 Altmetric 플랫폼 포함 매체에만 의존하여 온라인 미디어 중심, 소수 매체 누락 가능
- **후속 연구 방향**: 다국가 비교, 분야별 시간 역학 분석, 기술 개발 주기별 과학 활용 지연의 원인 규명, 자금과 활용의 인과성 검증을 위한 자연실험(natural experiment) 설계

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 공적 자금의 정당성에 대한 오랜 학술 논쟁에 대규모 실증 데이터를 처음으로 제시한 중요한 기여다. 5개 데이터셋의 혁신적 연계를 통해 '공적 투자의 공적 효과'를 정량화했으며, 공공 활용의 다양성 속에서도 자금 배분과의 놀라운 정렬성을 발견했다는 점에서 과학정책 연구에 신기원을 제시했다.

## Related Papers

- 🏛 기반 연구: [[papers/980_Linking_Global_Science_Funding_to_Research_Publications/review]] — 글로벌 과학 펀딩과 연구 출판물 간의 연계 분석은 공적 자금과 공중 필요의 정렬성을 평가하는 방법론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1043_The_selective_use_of_physics_knowledge_in_policy_how_interdi/review]] — 물리학 지식이 정책에서 선택적으로 사용되는 양상은 공적 과학이 실제 정책 결정에 활용되는 메커니즘을 구체적으로 보여줍니다.
- 🧪 응용 사례: [[papers/974_Information_Pathways_in_Online_Science_Communication_The_Rol/review]] — 온라인 과학 소통의 정보 경로 분석은 공적 자금 연구가 어떻게 대중에게 전달되는지 이해하는 실증적 도구를 제공합니다.
- 🔗 후속 연구: [[papers/996_Partisan_disparities_in_the_funding_of_science_in_the_United/review]] — 과학에 대한 공공 자금 지원과 활용에 대한 이론적 기반을 실제 정당별 자금 배분 데이터로 실증 분석한다.
- 🔗 후속 연구: [[papers/964_Funding_the_Frontier_Visualizing_the_Broad_Impact_of_Science/review]] — 과학 펀딩의 공공적 활용을 다차원적 사회적 영향 평가로 확장한 연구이다
- 🏛 기반 연구: [[papers/975_Interdisciplinary_papers_supported_by_disciplinary_grants_ga/review]] — 과학의 공공 이용과 공공 자금 지원 관계 연구가 그랜트 유형별 효과 분석의 이론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/980_Linking_Global_Science_Funding_to_Research_Publications/review]] — 과학의 공공 자금 지원 연구에서 펀딩-출판물 연결의 체계적 데이터화로 발전된다.
- 🧪 응용 사례: [[papers/983_Mapping_Research_Funding_and_Outputs_at_the_Topic_Level_in_t/review]] — 과학의 공공 이용과 자금 지원 이론이 북유럽 지역 연구 생태계 분석에 실제 적용된다.
- 🔗 후속 연구: [[papers/1184_Hamemayu_Hayuning_Nagara_A_Bibliometric_Analysis_of_the_Poli/review]] — 공공 자금 지원과 정책의 관계를 Javanese 철학으로 확장 해석한 연구입니다.
