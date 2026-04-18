# P1: 기본 Producer 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | KafkaTemplate을 통한 비동기 메시지 전송 및 orderId 기반 파티션 라우팅 |
| 파일 | `OrderProducer.java`, `ProducerTest.java` |
| 테스트 | 전송 성공 검증 (RecordMetadata 확인) |
| 리뷰 결과 | APPROVE — HIGH 이슈 없음 |

---

## 왜 이렇게 구현했는가

### KafkaTemplate.send()가 CompletableFuture를 반환하는 이유

`send()`는 호출 즉시 반환되고 실제 전송은 백그라운드에서 일어난다. 이것이 **비동기·논블로킹** 설계다.

```java
CompletableFuture<SendResult<String, OrderEvent>> future =
    kafkaTemplate.send(topic, orderId, event);
```

동기 전송(매 메시지마다 브로커 응답 대기)으로 구현하면 브로커 레이턴시가 애플리케이션 스루풋에 직접 영향을 준다. 비동기로 처리하면 Producer는 메시지를 내부 버퍼(`RecordAccumulator`)에 넣고 즉시 다음 작업으로 넘어가며, 브로커와의 I/O는 별도 Sender 스레드가 담당한다.

| 방식 | 스루풋 | 오류 인지 시점 |
|------|--------|--------------|
| 동기 (future.get() 대기) | 낮음 (브로커 레이턴시 직결) | 즉시 |
| **비동기 + whenComplete** (현재) | 높음 (버퍼링 후 배치 전송) | 콜백에서 |

### whenComplete()로 성공/실패 콜백 처리

`whenComplete(result, ex)`는 전송 완료 후 호출된다. `ex`가 `null`이면 성공, 아니면 실패다.

```java
future.whenComplete((result, ex) -> {
    if (ex != null) {
        log.error("전송 실패: {}", ex.getMessage());
    } else {
        log.info("전송 성공: offset={}", result.getRecordMetadata().offset());
    }
});
```

`exceptionally()`나 `thenAccept()`로 분리할 수도 있지만, 성공/실패를 한 곳에서 처리하는 `whenComplete()`가 가독성이 높다. 오류를 무시하고 싶지 않다면 반드시 이 콜백 또는 `send()`의 반환값을 처리해야 한다 — 콜백 없이 future를 버리면 전송 실패가 조용히 묻힌다.

### orderId를 key로 사용하는 이유

Kafka는 **같은 key를 가진 메시지를 같은 파티션으로 라우팅**한다 (기본 파티셔너 기준). `orderId`를 key로 설정하면:

1. **순서 보장**: 동일 주문의 `ORDER_CREATED` → `PAYMENT_COMPLETED` → `SHIPPED` 이벤트가 항상 같은 파티션에 저장되어 Consumer가 순서대로 처리한다.
2. **연관 메시지 집중**: 같은 주문에 관한 이벤트가 한 파티션에 모여 있어 Consumer 측 상태 관리가 단순해진다.

key를 `null`로 두면 Round-Robin 방식으로 파티션이 분배되어 같은 주문 이벤트가 여러 파티션에 흩어질 수 있다. 순서가 중요한 도메인에서는 key 설계가 핵심이다.

| key | 파티션 할당 | 순서 보장 |
|-----|-----------|---------|
| `null` | Round-Robin (랜덤) | 불가 |
| **orderId** (현재) | orderId 해시 → 고정 파티션 | 같은 주문 내 보장 |

### acks=all 설정의 의미

`acks=all`은 리더 브로커가 메시지를 저장하고, **모든 ISR(In-Sync Replica) 팔로워들도 복제 완료**했을 때 ACK를 반환하도록 요구한다.

```yaml
spring.kafka.producer:
  acks: all
```

| acks 값 | ACK 조건 | 내구성 | 레이턴시 |
|---------|---------|--------|---------|
| `0` | 없음 (fire-and-forget) | 최저 | 최저 |
| `1` | 리더만 저장 | 중간 | 중간 |
| **`all`** (현재) | 리더 + 모든 ISR 복제 | 최고 | 높음 |

리더가 ACK 직후 장애가 나도 팔로워에 이미 복제되어 있으므로 메시지가 유실되지 않는다. `enable.idempotence=true`는 내부적으로 `acks=all`을 강제하므로 P7 이후에는 설정이 더욱 중요해진다.

---

## 핵심 학습 포인트

1. **비동기 전송** — `send()`는 논블로킹, 내부 버퍼에 적재 후 Sender 스레드가 배치 전송
2. **whenComplete 필수** — 콜백 없이 future를 버리면 전송 실패가 무음으로 사라짐
3. **key = 파티션 라우팅** — orderId를 key로 설정해야 같은 주문 이벤트의 순서 보장
4. **acks=all = 최고 내구성** — ISR 전체 복제 확인 후 ACK, 리더 장애에도 유실 없음
5. **버퍼링의 장단점** — 스루풋 향상 vs 오류 인지 지연, whenComplete로 지연 인지 처리

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | Medium | "비동기 전송" 테스트(`ProducerTest.java:53-57`)가 매 전송마다 `future.get()` 즉시 호출로 사실상 동기 테스트 | 테스트명/주석과 실제 동작 불일치, 비동기 회귀 탐지 불가 |
