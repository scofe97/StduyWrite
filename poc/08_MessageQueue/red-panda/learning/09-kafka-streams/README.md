# 09. Kafka Streams & Event Design

## 개요

Kafka Streams 이론과 Confluent Event Design 코스를 통합한 학습 디렉토리다. 스트림 처리의 핵심 개념(KStream/KTable, Windowing, EOS)을 다루고, 이벤트 설계의 4가지 차원과 실전 베스트 프랙티스를 다룬다.

> **출처**: [Confluent Event Design Course](https://developer.confluent.io/courses/event-design/intro/)
> **환경**: Redpanda (Kafka API 호환) + Spring Boot
> **이전 위치**: `02-fundamentals/17-stream-processing.md` → `09-kafka-streams/01-stream-processing.md`

## 챕터 목록

| # | 문서 | 설명 | 출처 | 상태 |
|---|------|------|------|------|
| 01 | [01-stream-processing.md](./01-stream-processing.md) | Kafka Streams 이론 — KStream/KTable, Windowing, EOS, State Store | 02-fundamentals에서 이동 | 완료 |
| 02 | [02-event-design-intro.md](./02-event-design-intro.md) | 이벤트 설계 개론, 4가지 차원, 도메인 매핑, 메타데이터 | Event Design: Intro | 완료 |
| 03 | [03-facts-vs-deltas.md](./03-facts-vs-deltas.md) | Fact vs Delta 이벤트, 상태 전달 vs 변경 알림, 선택 가이드 | Event Design: Dimension 1 | 완료 |
| 04 | [04-facts-vs-deltas-handson.md](./04-facts-vs-deltas-handson.md) | 실습: Delta→Fact 구체화 (ksqlDB→Kafka Streams 변환) | Event Design: Hands-On 1 | 완료 |
| 05 | [05-normalized-vs-denormalized.md](./05-normalized-vs-denormalized.md) | 정규화 vs 비정규화, Outbox 패턴, CDC | Event Design: Dimension 2 | 완료 |
| 06 | [06-normalized-vs-denormalized-handson.md](./06-normalized-vs-denormalized-handson.md) | 실습: FK Join으로 비정규화 (ksqlDB→Kafka Streams 변환) | Event Design: Hands-On 2 | 완료 |
| 07 | [07-single-vs-multiple-streams.md](./07-single-vs-multiple-streams.md) | 단일/다중 스트림 설계, 순서 보장, TopicRecordNameStrategy | Event Design: Dimension 3 | 완료 |
| 08 | [08-single-vs-multiple-streams-handson.md](./08-single-vs-multiple-streams-handson.md) | 실습: 장바구니 ADD/REMOVE 집계 (ksqlDB→Kafka Streams 변환) | Event Design: Hands-On 3 | 완료 |
| 09 | [09-discrete-vs-continuous.md](./09-discrete-vs-continuous.md) | 이산/연속 이벤트 흐름, 상태 머신, 메트릭 스트림 | Event Design: Dimension 4 | 완료 |
| 10 | [10-best-practices.md](./10-best-practices.md) | 스키마, 네이밍, 이벤트 ID, 메타데이터, 4차원 통합 가이드 | Event Design: Best Practices | 완료 |

## 학습 순서

### 1단계: 스트림 처리 기초

> 목표: Kafka Streams의 핵심 추상화(KStream, KTable, State Store)와 윈도우 연산을 이해한다.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ① | 01-stream-processing | Kafka Streams의 Topology, KStream/KTable은 어떻게 동작하는가? | ★★★ |

### 2단계: 이벤트 설계 개론

> 목표: 이벤트 설계의 4가지 차원을 파악하고, 도메인 이벤트를 토픽으로 매핑하는 프로세스를 이해한다.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ② | 02-event-design-intro | 이벤트란 무엇이고, 설계 시 어떤 차원을 고려해야 하는가? | ★★☆ |

### 3단계: 4가지 설계 차원 (이론 → 실습 교대)

> 목표: 각 차원의 trade-off를 이해하고, Kafka Streams로 실습한다. 이론과 실습을 교대로 진행.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ③ | 03-facts-vs-deltas | Fact와 Delta 이벤트 중 어떤 것을 선택할까? | ★★☆ |
| ④ | 04-facts-vs-deltas-handson | Delta→Fact 구체화를 Kafka Streams로 어떻게 구현하는가? | ★★★ |
| ⑤ | 05-normalized-vs-denormalized | 이벤트를 정규화할지 비정규화할지 어떻게 결정하는가? | ★★☆ |
| ⑥ | 06-normalized-vs-denormalized-handson | FK Join으로 비정규화를 Kafka Streams로 어떻게 구현하는가? | ★★★ |
| ⑦ | 07-single-vs-multiple-streams | 하나의 토픽에 여러 이벤트 타입을 넣을지 어떻게 결정하는가? | ★★☆ |
| ⑧ | 08-single-vs-multiple-streams-handson | 다중 이벤트 타입의 집계를 Kafka Streams로 어떻게 구현하는가? | ★★★ |
| ⑨ | 09-discrete-vs-continuous | 이산 이벤트와 연속 이벤트 흐름의 차이는 무엇인가? | ★★☆ |

> ③→④, ⑤→⑥, ⑦→⑧ 흐름: 각 차원의 이론을 먼저 익히고 바로 실습으로 확인한다. ⑨는 실습 없이 이론만.

### 4단계: 베스트 프랙티스

> 목표: 4가지 차원을 종합하여 실전 이벤트 설계 의사결정을 내릴 수 있다.

| 순서 | 문서 | 핵심 질문 | 난이도 |
|:---:|------|----------|:-----:|
| ⑩ | 10-best-practices | 이벤트 스키마, 네이밍, 메타데이터의 베스트 프랙티스는? | ★★☆ |

## Redpanda 호환성

Redpanda는 Kafka API와 완전 호환이므로 Kafka Streams 앱을 그대로 사용할 수 있다. 주요 차이점:

| 항목 | Kafka | Redpanda |
|------|-------|----------|
| Schema Registry | 별도 컨테이너 (Confluent) | **내장** (포트 `:18081`) |
| 내부 토픽 (changelog 등) | 자동 생성 | 자동 생성 (동일) |
| Log Compaction | `cleanup.policy=compact` | 동일 설정 |
| Record Headers | 지원 | 동일 지원 |
| TopicRecordNameStrategy | Schema Registry 설정 | 동일 지원 |

Hands-On 문서(04, 06, 08)의 docker-compose는 기존 `redpanda-spring-boot` 프로젝트의 인프라를 재사용한다.

## 관련 폴더

- [02-fundamentals](../02-fundamentals/) — Redpanda 핵심 개념, 토픽 설계, 트랜잭션
- [03-spring-boot-integration](../03-spring-boot-integration/) — Spring Boot 연계 (23-kafka-streams-spring-boot)
- [06-cqrs-event-sourcing](../06-cqrs-event-sourcing/) — CQRS Materialized View (04-kafka-streams-topology)

## 문서 분리 이력

- **01-stream-processing.md**: `02-fundamentals/17-stream-processing.md`에서 이동. Kafka Streams 이론이 Event Design 코스와 함께 독립 디렉토리로 관리되는 것이 학습 흐름상 자연스럽기 때문이다.
