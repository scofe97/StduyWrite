---
title: 06-eda-messaging-patterns
tags: []
status: draft
related: []
updated: 2026-04-19
---

# RabbitMQ 기반 EDA 메시징 패턴
---
> 메시지 브로커를 활용한 Event-Driven Architecture의 핵심 흐름을 정리한다. Producer/Consumer 구조, Exchange 라우팅, 신뢰성 패턴(ACK, DLQ, Outbox)을 중심으로 Kafka와의 차이점도 비교한다.

## 1. EDA의 핵심 구조

Event-Driven Architecture(EDA)는 컴포넌트 간 직접 호출 대신 메시지 브로커를 통해 이벤트를 전달하는 아키텍처다. 호출자는 수신자의 존재를 알 필요가 없으므로 시스템 결합도가 낮아지고, 새로운 Consumer를 추가해도 Producer 코드를 변경하지 않는다.

핵심 구성 요소는 네 가지다:

- **Producer** — 이벤트를 발행하는 애플리케이션. 비즈니스 로직 완료 후 메시지를 브로커에 전송한다.
- **Exchange** — Producer로부터 메시지를 받아 라우팅 규칙에 따라 Queue로 전달한다. RabbitMQ 고유 개념이다.
- **Queue** — 메시지가 Consumer에게 전달될 때까지 저장되는 버퍼다.
- **Consumer** — Queue에서 메시지를 수신하여 처리하는 애플리케이션이다.

메시지 흐름을 요약하면 다음과 같다:

```
Producer → Exchange → (Binding Rule) → Queue → Consumer
```

Kafka는 Exchange 개념이 없다. Producer가 Topic에 직접 발행하고, Consumer Group이 Topic의 Partition을 분배받아 소비한다. RabbitMQ의 Exchange + Binding이 Kafka에서는 Topic + Partition Key에 해당한다.

## 2. 메시지 전달 패턴

### 2-1. Competing Consumers (작업 분배)

여러 Consumer가 하나의 Queue를 공유하면 RabbitMQ는 라운드 로빈 방식으로 메시지를 분배한다. 각 메시지는 단 하나의 Consumer에게만 전달되므로 병렬 처리에 적합하다.

```
Queue "orders"
  ├→ Consumer A (Message 1, 4, 7 ...)
  ├→ Consumer B (Message 2, 5, 8 ...)
  └→ Consumer C (Message 3, 6, 9 ...)
```

이 패턴은 주문 처리, 이미지 변환 같은 작업 큐(Work Queue)에 사용한다. Consumer를 추가하면 처리량이 선형으로 증가하므로 수평 확장이 단순하다. Kafka의 Consumer Group + Partition 분배와 동일한 목적이지만, RabbitMQ는 메시지 단위로 분배하고 Kafka는 Partition 단위로 할당한다는 차이가 있다.

### 2-2. Fanout Exchange (브로드캐스트)

모든 Consumer가 동일한 메시지를 받아야 할 때 Fanout Exchange를 사용한다. Exchange에 바인딩된 모든 Queue에 메시지가 복제된다.

```
Producer → Fanout Exchange "orders"
              ├→ Queue "orders-notification" → Notification Service
              ├→ Queue "orders-analytics"    → Analytics Service
              └→ Queue "orders-inventory"    → Inventory Service
```

주문 생성 이벤트를 알림, 분석, 재고 서비스가 각각 독립적으로 처리하는 시나리오가 대표적이다. Kafka에서는 하나의 Topic에 여러 Consumer Group이 구독하면 동일한 효과를 얻는다. 다만 Kafka는 메시지를 복제하지 않고 각 Consumer Group이 독립된 offset으로 같은 Partition을 읽는 구조다.

### 2-3. Topic Exchange (선택적 라우팅)

라우팅 키의 패턴 매칭으로 메시지를 선택적으로 전달한다. `order.created`, `order.cancelled` 같은 계층적 라우팅 키를 사용하여 Consumer가 관심 있는 이벤트만 수신할 수 있다.

```
Producer → Topic Exchange "events"
              ├→ "order.*"      → Order Service Queue
              ├→ "payment.*"    → Payment Service Queue
              └→ "#"            → Audit Log Queue (모든 메시지)
```

Kafka에서는 Topic 이름 자체로 이벤트를 구분하거나, Consumer 측에서 메시지 헤더/본문을 필터링한다. RabbitMQ의 Topic Exchange가 브로커 레벨에서 필터링을 수행하는 반면, Kafka는 Consumer가 모든 메시지를 받은 뒤 애플리케이션 레벨에서 필터링한다.

## 3. 신뢰성 패턴

### 3-1. 메시지 확인(ACK/NACK)

Consumer가 메시지를 성공적으로 처리했음을 브로커에 알리는 메커니즘이다. `autoAck: false`로 설정하면 Consumer가 명시적으로 ACK를 보내기 전까지 메시지가 Queue에 남는다.

처리 흐름은 다음과 같다:

- 처리 성공 → `BasicAck` → 메시지가 Queue에서 제거된다
- 처리 실패 → `BasicNack(requeue: true)` → 메시지가 Queue의 맨 뒤로 돌아간다
- 처리 실패 → `BasicNack(requeue: false)` → Dead Letter Queue로 이동한다

Kafka에서는 Consumer가 offset을 커밋하는 방식으로 ACK를 대체한다. offset을 커밋하지 않으면 다음 폴링에서 같은 메시지를 다시 읽는다. RabbitMQ는 메시지 단위로 ACK/NACK를 제어할 수 있지만, Kafka는 Partition 내 offset 기준이므로 특정 메시지만 선택적으로 NACK할 수 없다.

### 3-2. Dead Letter Queue (DLQ)

처리할 수 없는 메시지를 별도 Queue로 격리하는 패턴이다. 원본 Queue에 DLQ 설정을 추가하면, NACK된 메시지가 자동으로 DLQ로 라우팅된다.

DLQ 설정에 필요한 속성은 두 가지다:

- `x-dead-letter-exchange` — DLQ 메시지를 받을 Exchange
- `x-dead-letter-routing-key` — DLQ로 라우팅할 때 사용할 키

DLQ에 쌓인 메시지는 운영자가 수동으로 확인하거나, 별도 Consumer가 재처리를 시도한다. `requeue: true`로 무한 재시도하는 것보다 DLQ로 격리한 뒤 원인을 파악하는 것이 프로덕션에서 안전하다.

Kafka에서는 브로커 레벨의 DLQ가 없다. Consumer 애플리케이션에서 처리 실패 시 별도 Topic(예: `orders.dlq`)으로 메시지를 전송하는 방식으로 구현한다. Spring Kafka의 `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`가 이 패턴을 추상화한다.

### 3-3. Transactional Outbox 패턴

DB 트랜잭션과 메시지 발행의 원자성을 보장하는 패턴이다. 비즈니스 로직과 이벤트 정보를 같은 트랜잭션에서 DB에 저장하고, 별도 프로세스가 outbox 테이블을 폴링하여 브로커에 발행한다.

Outbox 패턴의 핵심 흐름은 세 단계로 구성된다:

- 비즈니스 로직 실행 + outbox 테이블에 이벤트 기록 (같은 트랜잭션)
- 트랜잭션 커밋
- Poller/Worker가 outbox 테이블의 미발행 레코드를 조회하여 브로커에 전송

이 패턴은 브로커 종류에 무관하게 적용 가능하다. RabbitMQ든 Kafka든 "DB 쓰기와 메시지 발행을 하나의 원자적 단위로 묶는다"는 목적은 동일하다. 차이점은 Kafka의 경우 Transactional Producer(`acks=all` + `enable.idempotence=true`)로 브로커 레벨의 exactly-once를 지원하지만, RabbitMQ는 Publisher Confirm + Consumer ACK 조합으로 at-least-once까지만 보장한다는 것이다.

Outbox 패턴의 상세 구현과 프로덕션 이슈는 `05-outbox-poller-review.md`에서 다룬다.

## 4. RabbitMQ vs Kafka 메시징 모델 비교

두 브로커는 설계 철학이 근본적으로 다르다. RabbitMQ는 "스마트 브로커, 단순 Consumer" 모델이고 Kafka는 "단순 브로커, 스마트 Consumer" 모델이다. 아래 테이블은 EDA 관점에서 핵심 차이를 정리한 것이다:

| 항목 | RabbitMQ | Kafka |
|------|----------|-------|
| 메시지 라우팅 | Exchange + Binding (브로커가 라우팅) | Topic + Partition Key (Producer가 결정) |
| 메시지 소비 | Push 방식 (브로커 → Consumer) | Pull 방식 (Consumer → 브로커 폴링) |
| 메시지 보존 | 소비 후 삭제 (ACK 시 Queue에서 제거) | 보존 기간까지 유지 (재소비 가능) |
| 순서 보장 | Queue 내 FIFO (단일 Consumer 시) | Partition 내 순서 보장 |
| 수평 확장 | Consumer 추가 (Queue 공유) | Partition 추가 + Consumer Group |
| 재소비 | 불가 (ACK된 메시지는 삭제됨) | offset 리셋으로 가능 |
| 전달 보장 | At-most-once / At-least-once | At-least-once / Exactly-once (Tx) |
| 적합 시나리오 | 작업 큐, RPC, 복잡한 라우팅 | 이벤트 스트리밍, 로그 수집, CQRS |

RabbitMQ는 메시지가 소비되면 Queue에서 사라진다. 장애 복구 시 이미 ACK된 메시지를 다시 읽을 수 없다는 뜻이다. Kafka는 Partition에 메시지가 보존 기간 동안 남아 있으므로, Consumer Group의 offset을 리셋하면 과거 메시지를 재처리할 수 있다. 이 차이가 이벤트 소싱이나 CQRS 패턴에서 Kafka를 선호하는 이유다.

## 5. 메시지 브로커 선택 기준

브로커 선택은 "어떤 브로커가 더 좋은가"가 아니라 "우리 요구사항에 어떤 모델이 맞는가"로 결정해야 한다. 판단 기준은 세 가지다.

첫째, 메시지 재소비가 필요한가이다. 이벤트 소싱, 감사 로그, 장애 시 재처리가 필요하면 Kafka가 적합하다. 메시지를 한 번 처리하고 끝이면 RabbitMQ로 충분하다.

둘째, 라우팅 복잡도가 높은가이다. 메시지 타입, 헤더, 패턴 매칭으로 세밀하게 라우팅해야 하면 RabbitMQ의 Exchange 시스템이 유리하다. Kafka에서 동일한 라우팅을 구현하려면 Topic을 세분화하거나 Consumer 측 필터링이 필요하다.

셋째, 처리량 규모가 어느 정도인가이다. 초당 수만 건 이상의 이벤트 스트리밍이라면 Kafka의 Partition 기반 수평 확장이 효율적이다. 초당 수천 건 수준의 작업 큐라면 RabbitMQ의 운영 단순성이 장점이 된다.
