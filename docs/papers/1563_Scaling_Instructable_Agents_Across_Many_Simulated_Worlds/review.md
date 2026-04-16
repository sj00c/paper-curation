---
title: "1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds"
authors:
  - "SIMA Team"
  - "Maria Abi Raad"
  - "Arun Ahuja"
  - "Catarina Barros"
  - "Frederic Besse"
date: "2024.03"
doi: ""
arxiv: ""
score: 4.0
essence: "SIMA는 키보드-마우스 인터페이스를 통해 자연어 명령을 따르는 embodied AI 에이전트를 다양한 3D 환경(연구용 환경 및 상업 비디오 게임)에서 학습시키는 프로젝트이다. 이는 언어를 지각과 구현된 행동에 그라운딩하여 일반적인 embodied AI 개발을 목표로 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Team et al._2024_Scaling Instructable Agents Across Many Simulated Worlds.pdf"
---

# Scaling Instructable Agents Across Many Simulated Worlds

> **저자**: SIMA Team, Maria Abi Raad, Arun Ahuja, Catarina Barros, Frederic Besse, Andrew Bolt, Adrian Bolton, Bethanie Brownfield, Gavin Buttimore, Max Cant, Sarah Chakera, Stephanie C. Y. Chan, Jeff Clune, Adrian Collister, Vikki Copeman, Alex Cullum, Ishita Dasgupta, Dario de Cesare, Julia Di Trapani, Yani Donchev, Emma Dunleavy, Martin Engelcke, Ryan Faulkner, Frankie Garcia, Charles Gbadamosi, Zhitao Gong, Lucy Gonzales, Kshitij Gupta, Karol Gregor, Arne Olav Hallingstad, Tim Harley, Sam Haves, Felix Hill, Ed Hirst, Drew A. Hudson, Jony Hudson, Steph Hughes-Fitt, Danilo J. Rezende, Mimi Jasarevic, Laura Kampis, Rosemary Ke, Thomas Keck, Junkyung Kim, Oscar Knagg, Kavya Kopparapu, Rory Lawton, Andrew Lampinen, Shane Legg, Alexander Lerchner, Marjorie Limont, Yulan Liu, Maria Loks-Thompson, Joseph Marino, Kathryn Martin Cussons, Loic Matthey, Siobhan Mcloughlin, Piermaria Mendolicchio, Hamza Merzic, Anna Mitenkova, Alexandre Moufarek, Valeria Oliveira, Yanko Oliveira, Hannah Openshaw, Renke Pan, Aneesh Pappu, Alex Platonov, Ollie Purkiss, David Reichert, John Reid, Pierre Harvey Richemond, Tyson Roberts, Giles Ruscoe, Jaume Sanchez Elias, Tasha Sandars, Daniel P. Sawyer, Tim Scholtes, Guy Simmons, Daniel Slater, Hubert Soyer, Heiko Strathmann, Peter Stys, Allison C. Tam, Denis Teplyashin, Tayfun Terzi, Davide Vercelli, Bojan Vujatovic, Marcus Wainwright, Jane X. Wang, Zhengdong Wang, Daan Wierstra, Duncan Williams, Nathaniel Wong, Sarah York, Nick Young | **날짜**: 2024-03-13 | **URL**: [https://arxiv.org/abs/2404.10179](https://arxiv.org/abs/2404.10179)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 | Overview of SIMA. In SIMA, we collect a large and diverse dataset of gameplay from both*

SIMA는 키보드-마우스 인터페이스를 통해 자연어 명령을 따르는 embodied AI 에이전트를 다양한 3D 환경(연구용 환경 및 상업 비디오 게임)에서 학습시키는 프로젝트이다. 이는 언어를 지각과 구현된 행동에 그라운딩하여 일반적인 embodied AI 개발을 목표로 한다.

## Motivation

- **Known**: 비디오 게임 환경은 embodied AI 연구의 중요한 플랫폼으로 사용되어 왔으며, 대규모 언어 모델의 성공은 다양한 데이터 분포에서의 학습이 일반화 성능을 향상시킨다는 것을 보여주었다.
- **Gap**: 기존 연구들은 제한된 환경에서만 언어 명령을 따르도록 했거나 손으로 제작한 행동 공간을 사용했으며, 단일 게임에 최적화된 에이전트만 개발했다. 여러 환경에서 자유로운 자연어 명령을 따르는 일반화된 에이전트는 개발되지 않았다.
- **Why**: 언어와 구현된 행동의 연결은 일반적인 AI 개발의 핵심 과제이며, 시뮬레이션 환경에서의 성공은 로봇 공학 등 실제 응용으로 확장할 수 있는 기초를 제공한다.
- **Approach**: 인간이 사용하는 것과 동일한 키보드-마우스 인터페이스를 유지하면서 여러 비디오 게임과 연구 환경에서 수집한 대규모 다양한 데이터셋으로 에이전트를 학습시킨다. 이는 새로운 환경으로의 확장을 용이하게 하고 인간 모방 학습을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 | Overview of SIMA. In SIMA, we collect a large and diverse dataset of gameplay from both*

- **다중 환경 포트폴리오**: 10개 이상의 3D 환경(연구용 custom 환경 및 상용 비디오 게임) 구축 및 활용
- **통일된 에이전트 인터페이스**: 모든 환경에서 동일한 키보드-마우스 입출력 인터페이스 사용으로 환경 간 일반화 가능성 입증
- **평가 방법론 개발**: 상용 게임에서 언어 명령 완료 여부를 평가하기 위해 OCR 기반 방식과 인간 평가 방법론 개발
- **자연어 명령 처리**: 제한된 문법이 아닌 자유로운 자연어 명령 이해 및 실행 능력 시연

## How

![Figure 4](figures/fig4.webp)

*Figure 4 | Setup & SIMA Agent Architecture. The SIMA agent receives language instructions from a*

- 대규모 다양한 게임플레이 데이터셋을 curated research 환경과 상용 비디오 게임 모두에서 수집
- 시각 관찰(pixel 입력)과 자연어 명령(text 입력)으로부터 키보드-마우스 행동(action 출력)을 매핑하는 에이전트 학습
- 게임 내 상태 접근 없이 인간 플레이어와 동일한 화면 관찰만 사용하는 조건 설정
- 비동기 환경에서의 실시간 상호작용으로 현실적인 제약 조건 반영
- GPU당 하나의 게임 인스턴스 실행 제약 하에서 효율적인 학습 방식 개발
- 연구 환경에서는 ground truth state로 평가, 상용 게임에서는 OCR 및 인간 평가 활용

## Originality

- 기존 언어 기반 게임 에이전트 연구와 달리 상용 게임을 포함한 10개 이상의 다양한 환경에서 동시에 학습하는 스케일 확대
- 손으로 제작한 행동 공간이 아닌 일반 키보드-마우스 인터페이스를 모든 환경에서 일관되게 사용
- 특권 정보(internal game state, rewards) 없이 오직 화면 관찰과 자연어만으로 학습하는 최소 가정 원칙
- 대규모 언어 모델의 다양한 데이터 분포 학습 성공에 영감을 받아 embodied AI에 적용한 창의적 확장

## Limitation & Further Study

- 현재는 단기 수평(short-horizon) 작업에 초점이 맞춰져 있으며 장기 계획 능력은 미흡
- GPU 리소스 제약으로 인한 병렬 처리 한계 (GPU당 하나의 게임 인스턴스만 실행 가능)
- 상용 게임에서의 평가가 OCR 및 인간 평가에 의존하여 객관적 성능 측정의 어려움
- 에이전트가 아직 '인간이 할 수 있는 모든 것'을 달성하지 못하고 있으며 어떤 작업에서의 성공률이나 구체적 벤치마크 결과가 제시되지 않음", '후속 연구로는 장기 계획 능력 강화, 더 많은 게임 및 환경 추가, 실제 로봇 환경으로의 전이 학습 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SIMA는 대규모 다양한 환경에서 자연어 명령을 따르는 embodied AI 에이전트 개발이라는 야심찬 목표를 제시하며, 통일된 인터페이스와 최소 가정을 유지하면서 스케일을 확대한 점에서 창의적이다. 다만 구체적인 정량적 성과 제시 부족과 현재 달성 수준의 명확한 평가가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — Voyager는 SIMA와 같은 embodied agent이지만 Minecraft 환경에서 자율적 탐험과 기술 학습에 특화된 다른 접근법이다.
- 🔄 다른 접근: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — JARVIS-1은 SIMA와 유사한 다중 환경 instructable agent이지만 메모리 증강된 멀티태스크에 집중하는 차별점이 있다.
- 🏛 기반 연구: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — MineDojo는 SIMA가 활용하는 게임 환경 기반 embodied AI 학습의 기반이 되는 오픈엔디드 환경을 제공한다.
- 🔄 다른 접근: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — MP5는 SIMA와 같은 시뮬레이션 환경에서의 embodied AI이지만 Minecraft에서의 다중모달 시스템에 특화된다.
- 🔗 후속 연구: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — SIMA의 다양한 3D 환경 학습 경험이 RoboTron-Nav의 embodied navigation 통합 프레임워크로 구체화되어 적용된다.
- 🔗 후속 연구: [[papers/1294_A_Generalist_Agent/review]] — A Generalist Agent와 SIMA는 모두 범용 AI 에이전트를 목표로 하되 SIMA가 더 다양한 3D 환경으로 확장했습니다.
- 🏛 기반 연구: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — Genie의 생성형 환경 모델링은 SIMA의 다양한 시뮬레이션 환경 학습을 위한 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — 시뮬레이션 환경에서의 instructable agent를 Minecraft의 개방형 환경으로 확장하여 더 복잡한 장기 지평선 작업에서의 적용을 다룬다.
- 🔗 후속 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — OctoNav의 generalist navigation을 다양한 시뮬레이션 환경에서 확장하여 instructable agents로 발전시킬 수 있다.
- 🏛 기반 연구: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — SIMA의 다양한 3D 환경에서의 embodied navigation 경험이 RoboTron-Nav의 통합 navigation 프레임워크 개발에 기반을 제공한다.
- 🔗 후속 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — Scaling Instructable Agents의 다중 시뮬레이션 환경 확장 접근법이 Voyager의 Minecraft 환경을 넘어선 일반화에 활용될 수 있다
- 🔗 후속 연구: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — 여러 시뮬레이션 세계에서의 지시 따르기 에이전트 스케일링을 BEHAVIOR-1K 벤치마크로 확장할 수 있습니다.
- 🧪 응용 사례: [[papers/1417_GRUtopia_Dream_General_Robots_in_a_City_at_Scale/review]] — Scaling Instructable Agents는 GRUtopia의 대규모 시뮬레이션 환경에서 확장 법칙을 탐구하는 실제 적용 사례임
