# C1: 기본 Consumer 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 수동 ACK 기반 메시지 소비로 at-least-once 처리 보장 |
| 파일 | `OrderConsumer.java` |
| 테스트 | 단일 메시지 수신 및 처리 완료 검증 |
| 리뷰 결과 | APPROVE — HIGH 이슈 없음 |

---

## 왜 이렇게 구현했는가

### ack-mode: manual 설정과 Acknowledgment.acknowledge()의 관계

`ack-mode: manual`은 **Spring Kafka가 자동으로 offset을 커밋하지 않겠다**는 선언이다. 이 설정 하에서 `@KafkaListener` 메서드는 `Acknowledgment` 파라미터를 받아 처리 완료 시점에 직접 `acknowledge()`를 호출해야 한다.

```java
@KafkaListener(topics = "orders", groupId = "order-consumer-group")
public void consume(OrderEvent event, Acknowledgment ack) {
    process(event);        // 비즈니스 처리
    ack.acknowledge();     // 처리 완료 후 offset 커밋
}
```

`acknowledge()` 전에 예외가 발생하면 offset이 커밋되지 않아 Consumer 재시작 시 해당 메시지부터 다시 수신한다. 이것이 **at-least-once** 보장이다.

### 수동 ACK vs 자동 커밋 비교

| 방식 | offset 커밋 시점 | 장애 시 동작 | 보장 수준 |
|------|----------------|------------|---------|
| **수동 ACK `manual`** (현재) | `acknowledge()` 호출 시 | 재처리 (중복 가능) | at-least-once |
| 자동 커밋 `RECORD` | 메서드 정상 반환 시 | 재처리 | at-least-once |
| 자동 커밋 `BATCH` | poll() 처리 완료 후 | 재처리 | at-least-once |
| 자동 커밋 `TIME` | 주기적 (enable.auto.commit) | **유실 가능** | at-most-once |

`enable.auto.commit=true`(카프카 클라이언트 기본값)는 처리 완료와 무관하게 주기적으로 offset을 커밋한다. 처리 도중 장애가 나면 이미 커밋된 offset 이후 메시지는 다시 읽지 않으므로 **유실(at-most-once)**이 발생한다.

수동 ACK는 "처리 완료 = offset 커밋"을 명시적으로 연결하여 유실 가능성을 제거한다. 대신 중복 처리 가능성을 감수하고, 이를 Consumer 측 idempotency(C9 등)로 보완한다.

### @KafkaListener의 groupId가 Consumer Group을 결정

```java
@KafkaListener(topics = "orders", groupId = "order-consumer-group")
```

`groupId`는 이 Consumer가 속할 **Consumer Group**을 지정한다. Consumer Group의 동작 규칙:

- **같은 groupId**: 그룹 내 Consumer들이 파티션을 나눠 갖는다. 메시지는 그룹 내 한 Consumer에만 전달된다 (로드 밸런싱).
- **다른 groupId**: 독립적인 그룹으로 각자 모든 메시지를 수신한다 (브로드캐스트 유사).

이 프로젝트에서 `OrderConsumer`(단일)와 `BatchOrderConsumer`(배치)가 각각 다른 groupId를 사용하는 이유가 여기 있다 — 같은 토픽을 두 Consumer가 **독립적으로** 전량 소비하기 위함이다.

| Consumer | groupId | 동작 |
|---------|---------|------|
| OrderConsumer | `order-consumer-group` | 단일 메시지, 파티션 일부 담당 |
| BatchOrderConsumer | `batch-consumer-group` | 배치, 동일 토픽 전량 독립 소비 |

### auto-offset-reset: earliest의 의미

```yaml
spring.kafka.consumer:
  auto-offset-reset: earliest
```

Consumer Group이 **처음으로 해당 토픽을 구독**할 때 (저장된 offset이 없을 때) 어디서부터 읽을지 결정한다.

| 값 | 동작 | 사용 시나리오 |
|----|------|-------------|
| **`earliest`** (현재) | 파티션의 가장 오래된 메시지부터 | 테스트, 신규 그룹이 기존 메시지도 처리해야 할 때 |
| `latest` | 이 시점 이후의 새 메시지부터 | 프로덕션 신규 Consumer (과거 이력 불필요) |
| `none` | 저장된 offset 없으면 예외 | offset 유실 감지가 필요한 경우 |

테스트에서 `earliest`가 중요한 이유: Testcontainers 환경에서 Consumer가 시작되기 전에 Producer가 메시지를 보낼 수 있다. `earliest`가 아니면 테스트 시작 전에 전송된 메시지를 Consumer가 놓친다.

---

## 핵심 학습 포인트

1. **ack-mode: manual** — 자동 커밋 비활성화, 처리 완료 시점에 직접 `acknowledge()` 호출
2. **at-least-once** — 수동 ACK는 유실 제거, 장애 시 중복 재처리를 감수
3. **at-most-once의 위험** — `enable.auto.commit=true`는 처리 전 커밋 가능 → 유실
4. **groupId = Consumer Group 식별자** — 같은 groupId면 파티션 분배, 다른 groupId면 독립 소비
5. **auto-offset-reset: earliest** — 신규 그룹의 첫 구독 시 시작 위치, 테스트 안정성에 필수
6. **중복의 책임은 Consumer에게** — 수동 ACK가 유실을 막지만 중복은 dedup 로직(C9)으로 보완

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | **High** | `concurrency=3` 환경에서 `lastReceived*` 단일 필드로 검증 — 리스너 병렬 처리 시 마지막 write가 덮여 다른 메시지 상태를 읽을 수 있음 | 경쟁 상황에서 false positive/negative |
| 2 | Medium | offset `>=0`만 확인하고 payload/orderId/key 정합성 미검증 | 핵심 단언 부족 |
