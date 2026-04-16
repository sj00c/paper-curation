---
title: "990_Networks_of_Scientific_Papers"
authors:
  - "Derek J. De Solla Price"
date: "1965.07"
doi: "10.1126/science.149.3683.510"
arxiv: ""
score: 4.0
essence: "과학논문의 인용 네트워크 패턴을 분석하여 과학 연구 전면(research front)의 특성을 규명한 연구로, 문헌 참고 행위를 통해 전체 과학 지식체계의 구조를 파악한다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Computational_Bibliometric_Analysis"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Research_Reproducibility_Crisis"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Price_1965_Networks of Scientific Papers The pattern of bibliographic references indicates the nature of the s.pdf"
---

# Networks of Scientific Papers: The pattern of bibliographic references indicates the nature of the scientific research front.

> **저자**: Derek J. De Solla Price | **날짜**: 1965-07-30 | **DOI**: [10.1126/science.149.3683.510](https://doi.org/10.1126/science.149.3683.510)

---

## Essence


과학논문의 인용 네트워크 패턴을 분석하여 과학 연구 전면(research front)의 특성을 규명한 연구로, 문헌 참고 행위를 통해 전체 과학 지식체계의 구조를 파악한다.

## Motivation

- **Known**: 과학 문헌은 지난 수 세기 동안 매년 약 7% 비율로 지수적 성장해왔으며, 평균적으로 논문당 약 15개의 참고문헌을 포함한다.
- **Gap**: 인용 네트워크의 전체 구조와 논문의 영향력이 시간에 따라 어떻게 변화하는지, 특히 고인용 논문의 특성과 자동 식별 가능성에 대한 체계적 분석이 부족하다.
- **Why**: 과학 논문의 인용 패턴을 이해함으로써 과학 지식의 진화 과정, 연구의 영향력 평가, 그리고 중요한 논문의 자동 식별이 가능해져 과학 문헌관리 및 정보 검색 체계를 개선할 수 있다.
- **Approach**: Garfield, Kessler, Tukey 등이 수행한 기계 처리 인용 연구(machine-handled citation studies)의 데이터를 바탕으로 참고문헌과 인용의 분포, 빈도, 시간적 변화를 통계적으로 분석한다.

## Achievement


- **참고문헌 분포 분석**: 약 10%의 논문은 참고문헌이 없고, 85%의 논문은 25개 이하의 참고문헌을 포함하며, 상위 1%의 논문은 84개 이상의 참고문헌을 가짐을 규명
- **인용 분포의 불균형성 발견**: 약 35%의 논문이 인용되지 않고, 49%의 논문이 1회만 인용되며, 상위 1%만이 6회 이상 인용됨을 증명
- **매년 인용 균형 모델**: 매년 약 10%의 논문이 '죽고', 생존 논문의 약 60%가 연간 최소 1회 이상 인용될 확률 제시", "**'클래식' 논문의 통계적 특성**: 전체 논문의 약 4%가 연간 4회 이상 인용되는 '클래식' 논문이며, 이들의 특성이 통계적으로 식별 가능함을 시사

## How


- Garfield의 1961 Index와 대규모 대표 표본 인용 데이터 활용
- 논문당 참고문헌 수의 분포를 백분율 기반으로 계산 및 시각화
- 연간 인용 빈도의 분포를 로그 척도로 분석하여 멱법칙(power law) 관계 검증
- 지수적 성장 모델을 적용하여 매년의 참고-인용 균형 계산
- 여러 표본의 데이터를 통합하여 통계적 일관성 확인

## Originality

- 인용 네트워크를 통해 과학 지식의 구조를 체계적으로 분석한 최초의 대규모 연구
- 참고문헌과 인용의 비대칭 분포를 수량화하여 과학 논문의 생명주기 모델 제시
- 기계 처리 인용 데이터의 통계 분석을 통해 과학 정보학(scientometrics)의 기초 확립
- 논문의 영향력을 자동 식별하기 위한 인용지수(citation index) 활용의 가능성 처음 제안

## Limitation & Further Study

- 분석이 1961년 데이터에 기반하여 시대 특성을 반영하며, 장기 시계열 데이터 부족
- 논문이 인용될 확률 간의 상호의존성(rich-get-richer 효과) 존재 여부가 미확인되어 모델의 예측력 제한
- 학문분야별 인용 관행의 차이를 고려하지 않아 범용성 검증 필요
- 책, 학위논문, 미출판 자료 등 비정기간행물 인용은 제외되어 전체 인용 생태계 포착 불완전
- **후속 연구 방향**: 학문분야별·시간대별 상세 분석, 논문의 지속적 인용 가능성 확률 모델 정교화, 자동 클래식 논문 선별 알고리즘 개발 필요

## Evaluation

- Novelty: 5/5
- Technical Soundness: 4/5
- Significance: 5/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 과학 문헌의 인용 네트워크 분석을 통해 과학 지식의 구조와 진화를 정량적으로 규명한 획기적 연구로, 현대 과학계량학과 학술정보 관리의 이론적 기초를 제공한다. 데이터 기반의 엄밀한 통계 분석과 직관적 모델링이 돋보이나, 세부 메커니즘 규명과 장기 추적 데이터를 통한 검증이 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/968_Growth_Rates_of_Modern_Science_Bibliometric_Analysis_Based_o/review]] — 인용 네트워크를 통한 과학 구조 분석이 과학 성장률의 정량적 분석에 기본적 이론적 틀을 제공한다.
- 🔗 후속 연구: [[papers/1081_Science_Citation_IndexA_New_Dimension_in_Indexing_This_uniqu/review]] — Science Citation Index의 새로운 색인 차원 연구가 인용 네트워크 패턴 분석으로 구체화된다.
- 🧪 응용 사례: [[papers/1003_Quantifying_Long-term_Scientific_Impact/review]] — 장기적 과학 영향 정량화가 인용 네트워크 패턴을 통한 연구 전면 특성 분석에 실제 적용된다.
- 🔗 후속 연구: [[papers/944_Co-Citation_Analysis_Bibliographic_Coupling_and_Direct_Citat/review]] — 동시인용, 서지결합, 직접인용 분석이 초기 인용 네트워크 연구를 정교화한 방법론으로 발전시킨다.
- 🧪 응용 사례: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — Semantic Scholar 오픈 연구 코퍼스가 인용 네트워크 패턴 분석을 대규모로 실현할 수 있는 데이터 인프라를 제공한다.
- 🧪 응용 사례: [[papers/1040_The_Price-Pareto_growth_model_of_networks_with_community_str/review]] — 과학 논문의 서지학적 네트워크 패턴이 Price-Pareto 모델의 실제 적용 사례를 보여준다.
- 🏛 기반 연구: [[papers/1056_Where_Do_Your_Citations_Come_From_Citation-Constellation_A_F/review]] — 과학 논문의 서지학적 네트워크 패턴이 인용 네트워크 사회구조 분석의 기본 토대를 제공한다.
- 🏛 기반 연구: [[papers/957_Emergence_of_Scaling_in_Random_Networks/review]] — 초기 인용 네트워크 패턴 연구가 스케일-프리 네트워크 이론 발전의 실증적 토대를 제공한다
- 🏛 기반 연구: [[papers/961_Fast_Unfolding_of_Communities_in_Large_Networks/review]] — 과학 논문의 서지 네트워크 패턴에 대한 기본 이해를 제공하여 커뮤니티 검출의 응용 기반을 마련한다.
- 🔗 후속 연구: [[papers/968_Growth_Rates_of_Modern_Science_Bibliometric_Analysis_Based_o/review]] — 인용 네트워크 패턴 분석을 통한 과학 구조 이해에서 시간적 성장률 분석으로 확장된 관점을 제공한다.
