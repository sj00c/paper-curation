---
title: "1403_Gemini_Robotics_15_Pushing_the_Frontier_of_Generalist_Robots"
authors:
  - "Gemini Robotics Team"
  - "Abbas Abdolmaleki"
  - "Saminda Abeyruwan"
  - "Joshua Ainslie"
  - "Jean-Baptiste Alayrac"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Gemini Robotics 1.5는 Motion Transfer 메커니즘과 embodied thinking 능력을 통해 다중 로봇 플랫폼을 제어할 수 있는 Vision-Language-Action 모델이며, Gemini Robotics-ER 1.5는 embodied reasoning에서 최첨단 성능을 달성하는 Vision-Language 모델이다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/3D_Keypoint_Manipulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Team et al._2025_Gemini Robotics 1.5 Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thi.pdf"
---

# Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer

> **저자**: Gemini Robotics Team, Abbas Abdolmaleki, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Ashwin Balakrishna, Nathan Batchelor, Alex Bewley, Jeff Bingham, Michael Bloesch, Konstantinos Bousmalis, Philemon Brakel, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Christine Chan, Oscar Chang, London Chappellet-Volpini, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, Adrian Collister, David B. D'Ambrosio, Sudeep Dasari, Todor Davchev, Meet Kirankumar Dave, Coline Devin, Norman Di Palo, Tianli Ding, Carl Doersch, Adil Dostmohamed, Yilun Du, Debidatta Dwibedi, Sathish Thoppay Egambaram, Michael Elabd, Tom Erez, Xiaolin Fang, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Ruiqi Gao, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Oliver Groth, Agrim Gupta, Roland Hafner, Steven Hansen, Leonard Hasenclever, Sam Haves, Nicolas Heess, Brandon Hernaez, Alex Hofer, Jasmine Hsu, Lu Huang, Sandy H. Huang, Atil Iscen, Mithun George Jacob, Deepali Jain, Sally Jesmonth, Abhishek Jindal, Ryan Julian, Dmitry Kalashnikov, M. Emre Karagozler, Stefani Karp, Matija Kecman, J. Chase Kew, Donnie Kim, Frank Kim, Junkyung Kim, Thomas Kipf, Sean Kirmani, Ksenia Konyushkova, Li Yang Ku, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Tuan Anh Le, Isabel Leal, Alex X. Lee, Tsang-Wei Edward Lee, Guy Lever, Jacky Liang, Li-Heng Lin, Fangchen Liu, Shangbang Long, Caden Lu, Sharath Maddineni, Anirudha Majumdar, Kevis-Kokitsi Maninis, Andrew Marmon, Sergio Martinez, Assaf Hurwitz Michaely, Niko Milonopoulos, Joss Moore, Robert Moreno, Michael Neunert, Francesco Nori, Joy Ortiz, Kenneth Oslund, Carolina Parada, Emilio Parisotto, Amaris Paryag, Acorn Pooley, Thomas Power, Alessio Quaglino, Haroon Qureshi, Rajkumar Vasudeva Raju, Helen Ran, Dushyant Rao, Kanishka Rao, Isaac Reid, David Rendleman, Krista Reymann, Miguel Rivas, Francesco Romano, Yulia Rubanova, Peter Pastor Sampedro, Pannag R Sanketi, Dhruv Shah, Mohit Sharma, Kathryn Shea, Mohit Shridhar, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Rachel Sterneck, Ian Storz, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Saran Tunyasuvunakool, Jake Varley, Grace Vesom, Giulia Vezzani, Maria Bauza Villalonga, Oriol Vinyals, René Wagner, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Chengda Wu, Markus Wulfmeier, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Jimmy Yan, Sherry Yang, Skye Yang, Yuxiang Yang, Hiu Hong Yu, Wenhao Yu, Wentao Yuan, Yuan Yuan, Jingwei Zhang, Tingnan Zhang, Zhiyuan Zhang, Allan Zhou, Guangyao Zhou, Yuxiang Zhou | **날짜**: 2025-10-02 | **URL**: [https://arxiv.org/abs/2510.03342](https://arxiv.org/abs/2510.03342)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 | The Gemini Robotics 1.5 family of models consists of Gemini Robotics 1.5, a VLA, and Gemini*

Gemini Robotics 1.5는 Motion Transfer 메커니즘과 embodied thinking 능력을 통해 다중 로봇 플랫폼을 제어할 수 있는 Vision-Language-Action 모델이며, Gemini Robotics-ER 1.5는 embodied reasoning에서 최첨단 성능을 달성하는 Vision-Language 모델이다.

## Motivation

- **Known**: Vision-Language-Action (VLA) 모델은 로봇 제어를 위해 시각 입력과 언어 명령을 행동으로 변환할 수 있다. 기존 Gemini Robotics는 단일 로봇 제어에 강점을 보였으나 다중 embodiment 학습의 어려움이 있었다.
- **Gap**: 이전 VLA 모델들은 서로 다른 로봇 플랫폼 간의 기술 전이(skill transfer)가 제한적이었고, 복잡한 다단계 작업 수행 시 명시적 추론 능력이 부족했다.
- **Why**: 범용 로봇은 물리 세계에 대한 깊은 이해, 고급 추론, 일반화된 제어 능력이 필요하며, 이를 통해 실제 환경에서 복잡한 작업을 자율적으로 수행할 수 있게 된다.
- **Approach**: Motion Transfer 메커니즘을 통해 heterogeneous한 다중 embodiment 로봇 데이터로부터 통일된 운동 이해를 학습하고, 행동 전에 자연어 추론 과정을 interleave하는 Thinking VLA를 개발했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 | The Gemini Robotics 1.5 family of models consists of Gemini Robotics 1.5, a VLA, and Gemini*

- **Multi-embodiment 제어**: Motion Transfer를 통해 ALOHA, Bi-arm Franka, Apollo humanoid 로봇을 로봇 특화 post-training 없이 동일 checkpoint로 제어
- **Zero-shot skill transfer**: 한 로봇에서 학습한 기술을 명시적 재학습 없이 다른 로봇으로 전이
- **Embodied thinking 능력**: VLA가 행동 이전에 자연어 기반 추론 과정을 생성하여 복잡한 다단계 작업 분해 및 해석 가능성 향상
- **최첨단 embodied reasoning**: Gemini Robotics-ER 1.5가 시각-공간 이해, 작업 계획, 진행률 추정 등 embodied reasoning 벤치마크에서 최고 성능 달성
- **Agentic 시스템 통합**: VLM orchestrator와 VLA action model의 결합으로 외부 도구 활용, 안전 메커니즘, 장기 작업 수행 가능

## How

![Figure 1](figures/fig1.webp)

*Figure 1 | The Gemini Robotics 1.5 family of models consists of Gemini Robotics 1.5, a VLA, and Gemini*

- Motion Transfer (MT) 메커니즘: 다양한 로봇 소스로부터 학습하여 통일된 운동 및 물리적 상호작용 이해 형성
- Thinking VLA: 시각 관찰을 언어 기반 사고로 변환하고 context window에 thinking trace를 append하여 행동 생성
- Embodied Thinking: VLM과 VLA 모두에 적용되는 추론 능력으로 high-level planning과 low-level action decomposition 지원
- Agentic framework: GR-ER 1.5 (orchestrator)가 사용자 입력 처리, 작업 분해, 성공 감지를 수행하고 GR 1.5 (action model)를 tool로 호출
- Multi-embodiment dataset: ALOHA, Bi-arm Franka, Apollo 플랫폼의 다양한 조작 기술 데이터 수천 개로 학습

## Originality

- Motion Transfer 메커니즘의 도입으로 heterogeneous 로봇 데이터로부터 일반화된 운동 표현 학습이 처음 달성됨
- Thinking VLA 개념: 행동 생성 전에 명시적 자연어 추론 과정을 interleave하는 새로운 VLA 패러다임
- Agentic framework를 통한 VLM과 VLA의 계층적 통합으로 long-horizon task execution과 multi-step reasoning 구현
- Embodied thinking을 여러 추상화 수준에서 적용하여 high-level planning부터 primitive motion prediction까지 일관된 추론 방식 제공

## Limitation & Further Study

- Motion Transfer의 효과가 현재 제한된 로봇 플랫폼(ALOHA, Bi-arm Franka, Apollo)에서만 검증되었으므로 더 다양한 embodiment에서의 일반화 검증 필요
- Agentic 시스템의 안전 메커니즘이 명시적으로 기술되지 않았으므로 실제 배포 환경에서의 안전성 평가 필요
- Thinking VLA의 추론 과정이 inference time compute를 증가시키므로 실시간 로봇 제어 시 성능-지연시간 트레이드오프 분석 필요
- Multi-embodiment 학습 데이터의 규모와 구성에 대한 상세 정보 부족으로 재현성 제한
- 외부 도구(web search 등)를 활용한 task execution 시 지연 시간과 신뢰성에 대한 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Gemini Robotics 1.5는 Motion Transfer, Thinking VLA, embodied reasoning의 세 가지 핵심 혁신을 통해 범용 로봇의 일반화 능력과 추론 능력을 크게 향상시켰으며, multi-embodiment 제어와 zero-shot skill transfer라는 실질적 성과로 로봇 AI의 새로운 경계를 제시한다.

## Related Papers

- 🔗 후속 연구: [[papers/1404_Gemini_Robotics_Bringing_AI_into_the_Physical_World/review]] — Gemini Robotics의 기본 모델을 Motion Transfer와 embodied thinking으로 발전시킨 개선된 버전이다.
- 🔄 다른 접근: [[papers/1498_OmniH2O_Universal_and_Dexterous_Human-to-Humanoid_Whole-Body/review]] — 둘 다 전신 휴머노이드 제어이지만 Gemini는 VLA 모델을, OmniH2O는 원격조종 기반 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti/review]] — 강화학습 기반 embodied reasoning이 Gemini Robotics-ER 1.5의 추론 능력 구현에 기반이 된다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 대규모 멀티모달 로봇 제어에서 OpenVLA와 다른 접근방식으로 다중 플랫폼 통합을 제안한다.
- 🔗 후속 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 웹 지식 전이 개념을 확장하여 더 정교한 Motion Transfer 메커니즘을 구현한다.
- 🏛 기반 연구: [[papers/1404_Gemini_Robotics_Bringing_AI_into_the_Physical_World/review]] — Gemini Robotics 1.5의 기본이 되는 초기 Vision-Language-Action 모델 버전이다.
- 🧪 응용 사례: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — Gemini Robotics의 일반화된 로봇 시스템이 EIIR 프레임워크의 산업 환경 적용을 위한 구체적인 구현 사례를 제공합니다.
- 🔄 다른 접근: [[papers/1308_An_Embodied_Generalist_Agent_in_3D_World/review]] — 둘 다 generalist robotics agent이지만 LEO는 3D 환경에, Gemini Robotics는 범용 로봇 지능에 더 중점을 둡니다.
