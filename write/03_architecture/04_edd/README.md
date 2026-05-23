---
title: 04_edd — 이벤트 기반 아키텍처 시리즈
tags: [moc, architecture, event-driven, eda]
status: draft
related:
  - ../README.md
  - ./GAP.md
  - ../../../docs/02_Architecture/03_EventDriven/
  - ../../04_messaging/README.md
updated: 2026-05-23
---

# 04_edd — 이벤트 기반 아키텍처 시리즈
---
> Adam Bellemare "Building Event-Driven Microservices" 17편을 Spring Boot 4.x · Java 25 컨텍스트에서 다시 정리한다. SSOT 는 `docs/02_Architecture/03_EventDriven/`.

본 시리즈는 **이론·원칙·결정 기준**과, EDA를 Kafka로 *적용*하는 도입부 일부까지 다룬다. Kafka·Outbox·Saga·CQRS·Event Sourcing 같은 *순수 도구 레벨 구현 디테일*은 `write/04_messaging/` 이 별도 시리즈로 두텁게 다룬다. 두 시리즈는 상호 `related:` 로 교차 링크된다.

> 2026-05-23 재정의 — 옛 04_messaging/01_EDA/ (EDA 기초·요청응답·202 Polling)는 이 시리즈의 [`05_KafkaApplied/`](05_KafkaApplied/)로 흡수됐다. "EDA 사고 모델 + Kafka 적용"이 이론 측 (01~04절) 옆에 같이 있는 게 학습 동선상 자연스럽다.

## 절 체계

| 절 | 의미 | 문서 |
|----|------|------|
| 01 | 동기와 기초 — 왜 EDA, 토폴로지, 데이터 계약, 기존 시스템 통합 | 01-01 ~ 01-04 |
| 02 | 처리 모델 — CQRS / Event Sourcing / 결정적 스트림 / 상태 / 진화 | 02-01 ~ 02-05 |
| 03 | 워크플로우와 통합 — Saga, Choreography/Orchestration, 요청·응답 통합 | 03-01 ~ 03-03 |
| 04 | 운영 — 지원도구, 테스팅, 배포 | 04-01 ~ 04-03 |
| 05 | Kafka 적용 — EDA 사고 모델을 Kafka 위에 얹는 도입부 | 05-01 ~ 05-03 |

## 문서 목록

### 01번대 — 동기와 기초

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 01-01 | [이벤트 기반 아키텍처](01-01.이벤트%20기반%20아키텍처.md) | 상태 변화를 사실의 흐름으로 다룰 때 얻는 것 | final |
| 01-02 | [토폴로지와 단일 작성자 원칙](01-02.토폴로지와%20단일%20작성자%20원칙.md) | 한 토픽에 한 작성자, materialized state | final |
| 01-03 | [데이터 계약과 스키마 설계 원칙](01-03.데이터%20계약과%20스키마%20설계%20원칙.md) | Explicit Schema · breaking change | final |
| 01-04 | [기존 시스템 통합 — Data Liberation 과 CDC](01-04.기존%20시스템%20통합%20—%20Data%20Liberation%20과%20CDC.md) | Outbox vs CDC vs Trigger 의사결정 | final |

### 02번대 — 처리 모델

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 02-01 | [CQRS](02-01.CQRS.md) | 쓰기·읽기 모델을 왜 갈라야 하는가 | final |
| 02-02 | [이벤트 소싱](02-02.이벤트%20소싱.md) | 현재 상태가 아닌 사건의 시퀀스를 저장한다는 결정 | final |
| 02-03 | [결정적 스트림 처리 — 워터마크와 스트림 타임](02-03.결정적%20스트림%20처리%20—%20워터마크와%20스트림%20타임.md) | Event Time vs Processing Time | final |
| 02-04 | [상태 기반 스트리밍](02-04.상태%20기반%20스트리밍.md) | Internal vs External State Store | final |
| 02-05 | [이벤트 진화 다루기](02-05.이벤트%20진화%20다루기.md) | 의미·스키마 진화의 운영 비용 | final |

### 03번대 — 워크플로우와 통합

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 03-01 | [Saga, Outbox, Request-Response Bridge](03-01.Saga%2C%20Outbox%2C%20Request-Response%20Bridge.md) | 분산 트랜잭션의 실용적 대안 | final |
| 03-02 | [Choreography vs Orchestration](03-02.Choreography%20vs%20Orchestration.md) | 워크플로우 통제권 분산 vs 중앙화 | final |
| 03-03 | [요청-응답과 이벤트 통합](03-03.요청-응답과%20이벤트%20통합.md) | 동기 UX 와 비동기 내부 잇기 | final |

### 04번대 — 운영

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 04-01 | [지원 도구 — 스키마 레지스트리·할당량·오프셋 관리](04-01.지원%20도구%20—%20스키마%20레지스트리·할당량·오프셋%20관리.md) | EDA 운영 도구 카탈로그 | final |
| 04-02 | [이벤트 기반 마이크로서비스 테스팅](04-02.이벤트%20기반%20마이크로서비스%20테스팅.md) | 단위·통합·로컬·원격 테스트 전략 | final |
| 04-03 | [이벤트 기반 마이크로서비스 배포 패턴](04-03.이벤트%20기반%20마이크로서비스%20배포%20패턴.md) | Full-Stop · Rolling · Blue-Green · Breaking Schema | final |

### 05번대 — Kafka 적용 (2026-05-23 흡수)

| # | 문서 | 다루는 질문 | 상태 |
|---|------|------------|------|
| 05-01 | [EDA 기초](05_KafkaApplied/05-01.EDA%20기초.md) | 전통 동기 아키텍처의 한계와 이벤트 기반 사고로의 전환 | draft |
| 05-02 | [EDA 기반 요청응답 통합](05_KafkaApplied/05-02.EDA%20기반%20요청응답%20통합.md) | 비동기 토픽 위에 요청-응답 의미를 얹는 6가지 구조 | draft |
| 05-03 | [202 Accepted + Polling 패턴](05_KafkaApplied/05-03.202%20Accepted%20+%20Polling%20패턴.md) | 오래 걸리는 작업을 동기 API 인터페이스로 노출하는 표준 패턴 | draft |

## 04_messaging 와의 분담

| 본 시리즈가 다루는 것 | 04_messaging 이 다루는 것 |
|----------------------|--------------------------|
| EDA 도입 동기, 사고 모델 (05_KafkaApplied) | (없음 — 05_KafkaApplied로 이관됨) |
| 왜 토폴로지인가, 단일 작성자 원칙의 의미 | Kafka 토픽 디자인 실무 |
| 데이터 계약의 정의·진화 원칙 | Avro · Schema Registry 운영, Confluent wire format |
| Outbox · CDC 선택 기준 | Outbox 구현 패턴, CDC 운영, DLT/Backoff |
| Choreography vs Orchestration 결정 | Saga 두 패턴의 구현 |
| Event Sourcing 의 모델 의미 | Event Sourcing Kafka 구현 |
| (없음) | Spring Kafka 운영 — concurrency, Manual Ack, Batch Listener, KafkaErrorConfig |

## SSOT 매핑 / 갭

[`GAP.md`](GAP.md) 가 `docs/02_Architecture/03_EventDriven/` 17편 ↔ 본 시리즈의 매핑과 미작성 챕터를 박제한다.
