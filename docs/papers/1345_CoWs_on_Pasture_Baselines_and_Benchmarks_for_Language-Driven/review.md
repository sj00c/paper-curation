---
title: "1345_CoWs_on_Pasture_Baselines_and_Benchmarks_for_Language-Driven"
authors:
  - "Samir Yitzhak Gadre"
  - "Mitchell Wortsman"
  - "Gabriel Ilharco"
  - "Ludwig Schmidt"
  - "Shuran Song"
date: "2022.03"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇이 자연언어 설명만으로 임의의 물체를 찾을 수 있도록 CLIP 기반의 학습 없는 네비게이션 방법 CoW를 제안하고, 이를 평가하기 위한 Pasture 벤치마크를 소개한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Visual_Language_Navigation"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gadre et al._2022_CoWs on Pasture Baselines and Benchmarks for Language-Driven Zero-Shot Object Navigation.pdf"
---

# CoWs on Pasture: Baselines and Benchmarks for Language-Driven Zero-Shot Object Navigation

> **저자**: Samir Yitzhak Gadre, Mitchell Wortsman, Gabriel Ilharco, Ludwig Schmidt, Shuran Song | **날짜**: 2022-03-20 | **URL**: [https://arxiv.org/abs/2203.10421](https://arxiv.org/abs/2203.10421)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. CLIP on Wheels (CoW) overview. A CoW uses a*

로봇이 자연언어 설명만으로 임의의 물체를 찾을 수 있도록 CLIP 기반의 학습 없는 네비게이션 방법 CoW를 제안하고, 이를 평가하기 위한 Pasture 벤치마크를 소개한다.

## Motivation

- **Known**: 기존 객체 네비게이션은 고정된 카테고리에 대해 훈련되어야 하며, 최근 open-vocabulary 모델들은 이미지 분류에서 성공을 거두었다.
- **Gap**: 로봇이 학습 데이터 없이도 임의의 언어 설명으로 물체를 찾을 수 있는지, 그리고 드물거나 속성 기반의 물체 찾기가 가능한지에 대한 체계적 평가가 부족하다.
- **Why**: 실제 로봇 응용에서는 미리 알려지지 않은 환경과 물체에 대응해야 하므로, 언어 기반의 zero-shot 네비게이션 능력이 중요하다.
- **Approach**: CLIP 기반 open-vocabulary 객체 탐지기와 고전적 탐색 전략을 결합한 CoW 프레임워크를 제안하고, 드물거나 속성 기반, 숨겨진 물체 찾기를 포함한 Pasture 벤치마크에서 평가한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. The PASTURE benchmark for L-ZSON. Text speci-*

- **효율적인 학습 없는 베이스라인**: 추가 학습 없이 CLIP 기반 객체 지역화와 고전적 탐색을 조합한 단순한 CoW가 500M 스텝으로 훈련된 ZSON 최신 방법과 네비게이션 효율(SPL)에서 동등하다.
- **강화된 평가 벤치마크**: 드물거나 보이지 않는 물체, 속성 기반 설명을 포함한 Pasture 벤치마크로 기존 벤치마크의 한계를 극복한다.
- **광범위한 실증 연구**: 90k 이상의 네비게이션 에피소드를 평가하여 CoW의 장단점을 명확히 하며, RoboTHOR에서 최신 방법 대비 15.6% 향상을 달성한다.
- **종합적 베이스라인 분석**: 21개의 CoW 변형을 통해 open-vocabulary 모델, 탐색 정책, 프롬팅 전략 등 다양한 요소를 체계적으로 분석한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2. CLIP on Wheels (CoW) overview. A CoW uses a*

- RGB-D 이미지와 위치 추정값으로부터 top-down map을 생성하여 환경을 매핑한다.
- 탐색 정책(frontier-based, learning-based)을 통해 미탐색 영역을 탐험하고 다양한 시점을 관찰한다.
- CLIP 기반 객체 탐지기(detector-based, reference-based, gradient-based)를 사용하여 대상 물체의 위치 신뢰도를 업데이트한다.
- 신뢰도 임계값을 초과하면 top-down map에서 물체 위치로 경로를 계획하고 STOP 액션을 수행한다.
- Habitat, RoboTHOR, Pasture 환경에서 90k 이상의 에피소드를 통해 성능을 평가한다.

## Originality

- 기존 ZSON 방법들과 달리 시뮬레이션 환경에서의 학습을 완전히 배제하고 open-vocabulary 모델의 zero-shot 능력만으로 객체 네비게이션을 수행하는 접근이 참신하다.
- 드물거나 보이지 않는 물체, 속성 기반 설명 등을 포함한 Pasture 벤치마크는 기존 고정 카테고리 중심 벤치마크의 한계를 극복하고 현실적 응용을 더 잘 반영한다.
- 21개의 다양한 CoW 변형을 통한 체계적 ablation study는 open-vocabulary 모델의 네비게이션 적응 방법을 이해하는 데 새로운 통찰을 제공한다.

## Limitation & Further Study

- CoW 베이스라인들이 언어 설명을 충분히 활용하지 못하며, 특히 속성 기반 설명에서 약점을 보인다.
- 숨겨진 물체 찾기는 시각적 정보만으로는 한계가 있으며, 추가적인 상식 추론 능력이 필요하다.
- 평가가 주로 시뮬레이션 환경(Habitat, RoboTHOR)에 제한되어 실제 로봇 환경에서의 성능 검증이 부족하다.
- 후속 연구는 언어 설명을 더 효과적으로 활용하는 모듈, 숨겨진 물체에 대한 상식 추론 능력, 실제 로봇 플랫폼에서의 검증을 고려해야 한다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 현실적인 로봇 응용을 위해 학습 없는 언어 기반 객체 네비게이션을 체계적으로 연구하며, 새로운 벤치마크와 광범위한 실증 분석을 통해 open-vocabulary 모델의 네비게이션 적응 가능성을 명확히 보여준다. 베이스라인의 단순성과 강력한 성능, 그리고 종합적인 평가 프레임워크는 향후 연구의 중요한 기준을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — 둘 다 자연언어 기반 zero-shot 네비게이션을 다루지만 CoW는 CLIP 기반 방법론을, LM-Nav는 GPT-3+CLIP 조합을 사용하는 다른 접근법입니다.
- 🧪 응용 사례: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — CoW의 언어 기반 zero-shot 네비게이션 방법론이 VLABench의 대규모 언어 조건부 로봇 벤치마크에서 평가될 수 있습니다.
- 🏛 기반 연구: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — CLIP 기반의 시각적 특성 추출이 언어 기반 zero-shot 네비게이션의 핵심 기반입니다.
- 🔄 다른 접근: [[papers/1345_CoWs_on_Pasture_Baselines_and_Benchmarks_for_Language-Driven/review]] — 언어 기반 객체 찾기에서 학습 없는 접근과 학습 기반 접근의 대비를 보여줍니다.
- 🔗 후속 연구: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — Zero-shot 객체 탐색에서 적응적 탐색 전략의 구체적 개선사항을 제시합니다.
- 🔄 다른 접근: [[papers/1342_CorrectNav_Self-Correction_Flywheel_Empowers_Vision-Language/review]] — 언어 지시를 통한 네비게이션에서 오류 복구와 zero-shot 접근의 서로 다른 해결책을 제시합니다.
- 🏛 기반 연구: [[papers/1365_DINOv2_Learning_Robust_Visual_Features_without_Supervision/review]] — CLIP 기반 언어-비전 매칭의 기반이 되는 자기지도학습 시각 특성 추출 방법을 제공합니다.
