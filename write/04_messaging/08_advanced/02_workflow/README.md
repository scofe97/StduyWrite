---
title: 02_workflow MOC
tags: [moc, workflow, temporal, eda, orchestration]
status: final
source:
  - https://docs.temporal.io/
  - https://temporal.io/blog/
  - 인프런 강의 "폭증하는 트래픽, 어떻게 견딜 것인가? Kafka, Spring, CDC, Temporal"
related:
  - ../README.md
  - ../../05_ConsistencyPattern/01-02.Orchestration Saga.md
  - ../../05_ConsistencyPattern/01-06.CDC.md
  - ../01_variants/01-02.Saga 엔진 비교.md
updated: 2026-05-23
---

# 02_workflow — Workflow 오케스트레이션과 통합 (Temporal)

---

> 워크플로우 엔진은 *긴 흐름·분기·인간 개입·장기 수명*이 동시에 요구될 때 손코딩 오케스트레이션의 운영 비용을 끊는 도구다. 본 폴더는 Temporal을 중심으로, EDA·CDC·Workflow가 통합되어 *폭증 트래픽 대응*과 *실패 격리*를 동시에 만드는 패턴을 정리한다.



## 진입 동기

> EDA만으로 모든 운영 부담이 풀리지는 않는다. 단순 컨슈머는 *분기 많은 긴 흐름*과 *부분 실패의 보상*에서 한계를 보인다.

`[01-02.Orchestration Saga](../../05_ConsistencyPattern/01-02.Orchestration%20Saga.md)`가 Saga의 일반 구조를 다뤘고, `[09-02.Saga 엔진 비교](../01_variants/01-02.Saga%20%EC%97%94%EC%A7%84%20%EB%B9%84%EA%B5%90.md)`가 손코딩과 엔진들의 트레이드오프 매트릭스를 제공한다. 본 폴더는 그중 *Temporal* 한 도구를 깊이 들여다보고, EDA + CDC 학습 트리와 어떻게 결합되는지 단계적으로 따라간다.



## 학습 흐름

> 01-NN은 Temporal 자체(왜→개념→Spring 통합), 02-NN은 통합 아키텍처 순으로 단순→통합으로 흐른다.

### 01 Temporal 입문

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [Workflow 오케스트레이션의 필요성](01-01.Workflow%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%EC%9D%98%20%ED%95%84%EC%9A%94%EC%84%B1.md) | 손코딩 한계 4시그널, Saga 패턴과 엔진의 관계, 폭증 트래픽 대응의 부하 흡수 |
| 01-02 | [Temporal 핵심 개념 - Workflow와 Activity](01-02.Temporal%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90%20-%20Workflow%EC%99%80%20Activity.md) | 결정성 제약, Event History replay, Worker·Task Queue·Execution, Signal/Query/Timer |
| 01-03 | [Temporal Spring Boot 통합](01-03.Temporal%20Spring%20Boot%20%ED%86%B5%ED%95%A9.md) | Bean 4종, @KafkaListener에서 Start vs Signal, Workflow ID 설계, Local Activity |

### 02 통합 아키텍처

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 02-01 | [EDA + CDC + Temporal 통합 아키텍처](02-01.EDA%20%2B%20CDC%20%2B%20Temporal%20%ED%86%B5%ED%95%A9%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | 5단 파이프라인 책임 분리, 3계층 재시도, Task Queue 백프레셔, 운영 함정 4가지 + Docker 디버깅 |



## 학습 순서

> 어디서 시작할지가 모호하면 다음 흐름을 권한다.

1. 손코딩 오케스트레이션이 무너지는 경험이 있다면 → **01-01**부터.
2. Temporal SDK 코드를 처음 보는 상태라면 → **01-02** (결정성과 Event History를 먼저).
3. Spring Boot에 빨리 붙여 보고 싶다면 → **01-03** (Bean 4종 + Kafka 통합).
4. EDA·CDC를 이미 운영 중이고 Temporal을 어디에 끼울지 결정해야 한다면 → **02-01**.



## 외부 사전 지식

> 본 폴더는 다음을 안다고 가정한다.

1. EDA의 기본 모델 — `[01-01.EDA 기초](../../../03_architecture/04_edd/05-01.EDA%20기초.md)` 수준.
2. Outbox 패턴 — `[01-03.Outbox](../../05_ConsistencyPattern/01-03.Outbox.md)` 수준.
3. CDC와 Debezium 설정 — `[01-06.CDC](../../05_ConsistencyPattern/01-06.CDC.md)` 수준.
4. Saga의 코레오그래피/오케스트레이션 차이 — `[01-01](../../05_ConsistencyPattern/01-01.Choreography%20Saga.md)`, `[01-02](../../05_ConsistencyPattern/01-02.Orchestration%20Saga.md)` 수준.

이 사전 지식 없이 02-01을 먼저 읽으면 책임 분리의 의도가 부분적으로만 보인다.



## 향후 확장

> 4편으로 시작했지만 같은 폴더로 자연스럽게 자랄 수 있도록 번호를 설계했다.

확장 후보:

- `01-04.Cadence vs Temporal` — Uber의 원조 엔진 비교 (분리 배경, 커뮤니티 동향)
- `01-05.AWS Step Functions 매핑` — Workflow as code vs ASL DSL의 의사결정
- `02-02.사람 승인 흐름` — Signal 기반 human-in-the-loop 패턴
- `02-03.버전 호환성 운영` — `Workflow.getVersion()` API와 무중단 배포

`[09-02.Saga 엔진 비교](../01_variants/01-02.Saga%20%EC%97%94%EC%A7%84%20%EB%B9%84%EA%B5%90.md)`는 *엔진 선택* 관점, 본 폴더는 *선택된 엔진의 깊은 운영* 관점으로 직교한다. 새 엔진 문서가 늘어나도 두 폴더의 경계는 흔들리지 않는다.



## 출처 정책

> 1차 자료를 우선한다.

각 문서의 `source` 프론트매터에 공식 문서 URL과 강의 메타정보(섹션 번호)를 적는다. 강의 영상 자체는 비공개 콘텐츠이므로 본문에 인용하지 않고, 강의에서 다룬 *주제*를 공식 문서로 재구성한다. 사실 검증이 어려운 강사 고유 견해는 본문에 적지 않는다.



## 경계 기준

> 본 폴더가 *다루지 않는 것*을 명시한다.

- Kafka 기본·Producer/Consumer 디테일 — `[../04_NN](../README.md)` 그룹
- Debezium 설정과 EventRouter 디테일 — `[01-06.CDC](../../05_ConsistencyPattern/01-06.CDC.md)`
- Outbox 테이블 설계 자체 — `[01-03.Outbox](../../05_ConsistencyPattern/01-03.Outbox.md)`
- Saga 패턴의 일반 구조 — `[01-01](../../05_ConsistencyPattern/01-01.Choreography%20Saga.md)`, `[01-02](../../05_ConsistencyPattern/01-02.Orchestration%20Saga.md)`
- 분산 시스템 일반 이론 — `[../../05_data/](../../../05_data/README.md)`

본 폴더는 *Workflow 엔진*과 *그 엔진이 EDA·CDC와 결합될 때의 통합 패턴*에만 집중한다.



## 관련 문서

- [../README.md](../README.md) — 04_messaging 진입점
- [../../05_ConsistencyPattern/01-02.Orchestration Saga.md](../../05_ConsistencyPattern/01-02.Orchestration%20Saga.md) — Saga 패턴의 일반 구조
- [../../05_ConsistencyPattern/01-06.CDC.md](../../05_ConsistencyPattern/01-06.CDC.md) — Debezium CDC 설정
- [../01_variants/01-02.Saga 엔진 비교.md](../01_variants/01-02.Saga%20%EC%97%94%EC%A7%84%20%EB%B9%84%EA%B5%90.md) — 엔진 선택 매트릭스
