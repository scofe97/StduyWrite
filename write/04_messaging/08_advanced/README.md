---
title: 08_advanced MOC
tags: [moc, advanced, messaging, kafka, workflow]
status: final
related:
  - ../README.md
updated: 2026-05-23
---

# 08_advanced — 메시징 심화

---

> 상위 `04_messaging/`이 기본 패턴 이해에 집중한다면, 이 폴더는 그 패턴을 운영 규모로 키울 때 마주치는 두 갈래를 다룹니다. 한 갈래는 같은 문제를 푸는 여러 대안을 비교하는 일이고, 다른 갈래는 그중 워크플로우 엔진 하나를 깊이 들여다보는 일입니다. 학습 트리의 정상 흐름을 마쳤거나 TPS 적용 시점에 도달한 독자가 다음 선택을 가늠할 때 읽는 자료입니다.



## 두 갈래

> 심화라는 한 단어 안에 성격이 다른 두 묶음이 들어 있어 서브폴더로 나눕니다.

`01_variants/`는 본 학습 트리에서 다룬 기본형 하나를 출발점으로 삼아, 같은 문제를 푸는 여러 대안을 트레이드오프 매트릭스로 비교합니다. 예를 들어 폴링 기반 Outbox에서 출발해 log-based CDC·DB 네이티브 시그널·메시징 native까지 펼쳐 놓고 어느 쪽이 어떤 상황에 맞는지 판단 근거를 모읍니다. 관점은 도구 선택입니다.

`02_workflow/`는 그 비교에서 선택지로 등장한 워크플로우 엔진 하나(Temporal)를 골라 깊이 운영하는 방법을 다룹니다. EDA·CDC 학습 트리와 어떻게 결합되어 폭증 트래픽 대응과 실패 격리를 동시에 만드는지 단계적으로 따라갑니다. 관점은 선택된 엔진의 깊은 운영입니다.

두 갈래는 직교합니다. `01_variants/`의 [Saga 엔진 비교](01_variants/01-02.Saga%20엔진%20비교.md)가 엔진 선택의 매트릭스를 제공하고, `02_workflow/`는 그 매트릭스에서 고른 Temporal 한 도구를 파고듭니다. 새 엔진 비교 문서나 새 운영 노트가 늘어나도 두 폴더의 경계는 흔들리지 않습니다.



## 01_variants — 변종·비교

> 기본형 하나에서 출발해 5개 이상의 대안과 트레이드오프를 비교합니다.

- [01-01.Outbox 변종 비교](01_variants/01-01.Outbox%20변종%20비교.md) — 폴링 기반·log-based CDC·DB 네이티브 시그널·메시징 native의 트레이드오프, Shopify·Uber·Wix 등 사례
- [01-02.Saga 엔진 비교](01_variants/01-02.Saga%20엔진%20비교.md) — 손코딩 오케스트레이션 vs Temporal/Cadence/Camunda 8/Conductor/Step Functions, 도입 시그널과 마이그레이션 비용
- [01-03.스트림 처리 진화](01_variants/01-03.스트림%20처리%20진화.md) — Kafka Streams에서 Flink·ksqlDB·Materialize·RisingWave로, exactly-once 보장 비교
- [01-04.스키마 거버넌스](01_variants/01-04.스키마%20거버넌스.md) — 호환성 자동화·subject naming·RBAC·contract testing(Pact, Microcks)·데이터 카탈로그
- [01-05.Outbox 재시도 레이어 분리](01_variants/01-05.Outbox%20재시도%20레이어%20분리.md) — Producer 메모리 재시도와 DB 영속 재시도의 시간 척도 분리, 단순화 시그널 메트릭
- [01-06.Outbox 폴러 0건 SELECT 와 polling cadence](01_variants/01-06.Outbox%20폴러%200건%20SELECT%20와%20polling%20cadence.md) — 0건 SELECT의 세 비용(DB 부하·로그 폭주·SLA 트레이드오프), cadence 결정 변수, adaptive backoff, CDC 대안 비교

각 문서는 출발점·변종 비교·외부 사례·TPS 적용 가능성의 4단 구조를 따릅니다. 출발점은 본 학습 트리에서 다룬 기본형이고(예: 01-01의 출발점은 [05_ConsistencyPattern/01-03.Outbox](../05_ConsistencyPattern/01-03.Outbox.md)의 폴링 Relay), 변종 비교는 5개 이상의 대안과 트레이드오프 매트릭스이며, 외부 사례는 회사 엔지니어링 블로그·공식 문서 같은 1차 자료를 출처 URL과 함께 인용합니다. 마지막으로 현재 `okestro/tps-gitlab2` 코드 기준으로 도입 시그널·리스크·이행 단계를 정리합니다.



## 02_workflow — 워크플로우 깊이 (Temporal)

> 비교에서 고른 엔진 하나를 깊이 운영합니다. 진입점은 [02_workflow/README.md](02_workflow/README.md)입니다.

- [01-01.Workflow 오케스트레이션의 필요성](02_workflow/01-01.Workflow%20오케스트레이션의%20필요성.md) — 손코딩 한계 4시그널, Saga 패턴과 엔진의 관계, 폭증 트래픽 대응의 부하 흡수
- [01-02.Temporal 핵심 개념 - Workflow와 Activity](02_workflow/01-02.Temporal%20핵심%20개념%20-%20Workflow와%20Activity.md) — 결정성 제약, Event History replay, Worker·Task Queue·Execution, Signal/Query/Timer
- [01-03.Temporal Spring Boot 통합](02_workflow/01-03.Temporal%20Spring%20Boot%20통합.md) — Bean 4종, @KafkaListener에서 Start vs Signal, Workflow ID 설계, Local Activity
- [02-01.EDA + CDC + Temporal 통합 아키텍처](02_workflow/02-01.EDA%20+%20CDC%20+%20Temporal%20통합%20아키텍처.md) — 5단 파이프라인 책임 분리, 3계층 재시도, Task Queue 백프레셔, 운영 함정 4가지



## 출처 정책

> 1차 자료를 우선합니다.

회사 엔지니어링 블로그·공식 문서·학술 논문·컨퍼런스 발표를 우선하고, 요약 글이나 미디엄 포스트 같은 2차 자료는 1차 자료 링크와 함께 씁니다. 모든 사례는 출처 URL을 인용 라인이나 footnote로 표기하며, AI 생성 추정이나 일반 통념은 본문에 적지 않습니다. 확인되지 않은 사실은 "추정", "보고된 바에 따르면"처럼 명시합니다.



## 비범위

> 본 폴더가 다루지 않는 것을 명시합니다.

- 기본 패턴 자체의 설명 — 상위 [`04_messaging/`](../README.md) 참조
- 분산 시스템 일반 이론(CAP, FLP impossibility 등) — [`05_data/`](../../05_data/README.md) 참조
- Kafka 기본·Producer/Consumer 디테일 — [`04_BrokerArchitecture/`](../04_BrokerArchitecture/) 참조



## 관련 문서

- [../README.md](../README.md) — 04_messaging 진입점
- [02_workflow/README.md](02_workflow/README.md) — Temporal 워크플로우 갈래 진입점
- [../05_ConsistencyPattern/01-03.Outbox.md](../05_ConsistencyPattern/01-03.Outbox.md) — 01-01 변종 비교의 출발점
- [../05_ConsistencyPattern/01-02.Orchestration Saga.md](../05_ConsistencyPattern/01-02.Orchestration%20Saga.md) — 01-02 Saga 엔진 비교의 패턴 토대
