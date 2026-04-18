# Spring Boot Integration: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. KafkaTemplate은 멀티스레드 환경에서 공유해도 안전한가

### 왜 이 질문이 중요한가

Spring 컨테이너는 KafkaTemplate을 싱글톤 빈으로 등록한다. 여러 서비스나 스케줄러가 동시에 같은 인스턴스를 호출하는 상황은 실무에서 일상적이다. "스레드 안전하다"는 결론 자체보다, 그 이유와 트랜잭션 활성화 시 달라지는 점을 설명할 수 있어야 면접에서 신뢰를 얻는다.

### 답변

일반 KafkaTemplate(트랜잭션 없음)은 스레드 안전하다. 내부적으로 `ProducerFactory`에서 Producer 인스턴스를 캐싱하며, Kafka Producer 자체가 스레드 안전하게 설계되어 있기 때문이다. 여러 스레드가 동시에 `send()`를 호출해도 내부 배치 버퍼에 순서대로 적재된다.

**트랜잭션 활성화 시 주의점**: `transaction-id-prefix`를 설정하면 각 트랜잭션마다 별도의 Producer 인스턴스가 필요하다. Spring Kafka는 스레드 로컬(ThreadLocal) 기반으로 Producer를 바인딩하므로, 트랜잭션 블록 안에서는 같은 스레드가 Producer를 독점 사용한다.

```yaml
spring:
  kafka:
    producer:
      transaction-id-prefix: order-service-tx-  # 트랜잭션 활성화
```

```java
// 트랜잭션 블록 내부 — 이 스레드의 Producer는 블록이 끝날 때까지 전용으로 사용됨
kafkaTemplate.executeInTransaction(ops -> {
    ops.send("orders", event);
    ops.send("inventory", reserveEvent);
    return true;
});
```

`executeInTransaction()`을 쓰지 않고 `@Transactional`만 붙이는 경우, KafkaTransactionManager가 스레드 로컬로 Producer를 관리하므로 동시 요청 수만큼 Producer 풀이 소모된다. 풀 크기(`producer-factory.max-pool-size`, 기본값 없음)를 의도적으로 제한하지 않으면 커넥션이 무한 증가할 수 있다.

---

## Q2. Consumer 리밸런스 중 처리 중인 메시지는 어떻게 되는가

### 왜 이 질문이 중요한가

리밸런스는 Consumer 그룹에서 멤버가 추가되거나 제거될 때 파티션을 재분배하는 과정이다. 이 시점에 처리 중인 메시지의 offset 커밋 타이밍을 놓치면 중복 처리가 발생한다. at-least-once 보장의 실질적 구현 방법을 물어볼 때 핵심 논거가 된다.

### 답변

리밸런스가 시작되면 현재 스레드의 `poll()` 루프가 중단되고 `onPartitionsRevoked()` 콜백이 호출된다. 이 시점까지 커밋되지 않은 offset은 새 Consumer가 다시 처음부터 읽는다. 즉, 처리는 완료했지만 커밋 전에 리밸런스가 발생하면 **중복 처리**가 일어난다.

**AckMode 선택이 핵심이다.** 기본값인 `BATCH` 모드는 `poll()` 한 번의 결과를 모두 처리한 후 커밋하므로, 배치 중간에 리밸런스가 일어나면 배치 전체를 재처리한다.

```yaml
spring:
  kafka:
    listener:
      ack-mode: MANUAL_IMMEDIATE  # 메시지 하나 처리 직후 즉시 커밋
```

```java
@KafkaListener(topics = "payments")
public void consume(ConsumerRecord<String, PaymentEvent> record, Acknowledgment ack) {
    processPayment(record.value());  // 처리 완료 후
    ack.acknowledge();               // 즉시 커밋 — 리밸런스가 와도 이 메시지는 재처리 안 됨
}
```

중복을 완전히 제거하려면 Consumer 쪽 멱등성(처리 결과를 DB에 기록 후 재처리 시 스킵)이 필요하다. `MANUAL_IMMEDIATE`는 커밋 빈도를 높여 중복 범위를 줄이는 것이지, 중복 자체를 없애지는 않는다.

---

## Q3. Kafka 트랜잭션의 read_committed와 read_uncommitted는 어떻게 다른가

### 왜 이 질문이 중요한가

Exactly-once 처리는 Kafka 트랜잭션의 핵심 가치다. 하지만 Consumer 격리 수준을 잘못 설정하면 트랜잭션이 abort된 메시지까지 읽어서 처리하게 된다. 설정 한 줄의 차이가 데이터 정합성 전체를 좌우하므로, 면접에서 트랜잭션을 논할 때 반드시 따라오는 질문이다.

### 답변

`read_uncommitted`(기본값)는 트랜잭션 커밋 여부와 무관하게 브로커에 도착한 메시지를 모두 읽는다. `read_committed`는 트랜잭션이 커밋된 메시지만 반환하고, abort된 메시지는 건너뛴다.

```yaml
spring:
  kafka:
    consumer:
      isolation-level: read_committed  # abort된 트랜잭션 메시지 필터링
      enable-auto-commit: false        # 트랜잭션에서 offset 커밋 관리
```

**Exactly-once 달성 조건** — 세 가지가 모두 충족되어야 한다.

1. Producer: `enable.idempotence=true` + `transaction-id-prefix` 설정
2. Consumer: `isolation-level=read_committed`
3. Offset 커밋을 트랜잭션에 포함 (`sendOffsetsToTransaction()`)

```java
kafkaTemplate.executeInTransaction(ops -> {
    ops.send("output-topic", result);
    // offset 커밋도 같은 트랜잭션에 포함시켜야 exactly-once
    ops.sendOffsetsToTransaction(
        Map.of(new TopicPartition("input-topic", partition), new OffsetAndMetadata(offset + 1)),
        consumerGroupId
    );
    return true;
});
```

`read_committed` 설정 없이 트랜잭션 Producer만 쓰면 Consumer가 abort된 메시지를 읽어 처리하므로 Exactly-once가 아니다.

---

## Q4. Spring Kafka의 DefaultErrorHandler와 DeadLetterPublishingRecoverer를 어떻게 조합하는가

### 왜 이 질문이 중요한가

Consumer에서 예외가 발생할 때 재시도 횟수, 백오프 시간, 최종 실패 처리를 어떻게 구성하는지는 프로덕션 안정성과 직결된다. 잘못 구성하면 일시적 오류에 무한 재시도가 걸리거나, 영구 오류임에도 계속 배달 시도해 Consumer가 멈추는 상황이 발생한다.

### 답변

`DefaultErrorHandler`는 재시도 정책(BackOff)과 최종 실패 복구 전략(RecoveryCallback)을 조합한다. `DeadLetterPublishingRecoverer`는 실패 메시지를 DLT(Dead Letter Topic)로 발행하는 복구 전략이다.

```java
@Bean
public DefaultErrorHandler errorHandler(KafkaTemplate<String, Object> kafkaTemplate) {
    // 2초 대기 후 최대 3회 재시도
    ExponentialBackOffWithMaxRetries backOff = new ExponentialBackOffWithMaxRetries(3);
    backOff.setInitialInterval(2_000);
    backOff.setMultiplier(2.0);  // 2s → 4s → 8s

    // 재시도 소진 시 {원본토픽}.DLT 로 발행
    DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate);

    DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, backOff);

    // 재시도 불필요한 영구 오류는 즉시 DLT로
    handler.addNotRetryableExceptions(DeserializationException.class, ValidationException.class);

    return handler;
}
```

`addNotRetryableExceptions()`로 역직렬화 오류나 유효성 오류처럼 재시도해도 무의미한 예외를 분류하는 것이 실무 핵심이다. 이를 빠뜨리면 역직렬화 불가 메시지를 3회 재시도한 뒤 DLT로 보내는 불필요한 지연이 발생한다.

---

## Q5. @KafkaListener의 concurrency 설정은 파티션 수와 어떤 관계인가

### 왜 이 질문이 중요한가

처리량을 높이려고 `concurrency`를 늘렸지만 실제로는 효과가 없거나, 오히려 특정 Consumer만 메시지를 독점하는 상황이 실무에서 자주 발생한다. 파티션과 Consumer 스레드의 관계를 이해하지 못하면 튜닝 방향을 잡을 수 없다.

### 답변

`concurrency`는 하나의 `@KafkaListener`가 생성하는 Consumer 스레드 수다. Kafka는 하나의 파티션을 하나의 Consumer만 소비할 수 있으므로, 스레드 수가 파티션 수를 초과하면 초과 스레드는 유휴 상태로 대기한다.

```java
@KafkaListener(
    topics = "orders",
    concurrency = "3"  // 스레드 3개 → 파티션 3개까지 병렬 처리 가능
)
public void consume(OrderEvent event) { ... }
```

```yaml
# 토픽 파티션 수와 concurrency를 맞추는 것이 기본 원칙
spring:
  kafka:
    listener:
      concurrency: 3  # orders 토픽이 3 파티션이라면
```

파티션이 6개인 토픽에 `concurrency=3`이면 스레드 하나가 파티션 2개를 담당한다. 처리 속도가 느린 파티션이 있으면 해당 스레드가 병목이 된다. `concurrency=6`으로 올리면 파티션 하나당 스레드 하나로 최대 병렬성을 확보할 수 있지만, 스레드 수 증가에 따른 컨텍스트 스위칭 비용도 고려해야 한다. 실무에서는 `파티션 수 = concurrency`를 출발점으로 삼고, 부하 테스트로 최적값을 찾는다.
