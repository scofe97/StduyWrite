# #6 KafkaTemplate vs @SendTo 비교

같은 InventoryService의 `onOrderCreated` 로직을 두 가지 방식으로 구현하여 트레이드오프를 비교

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 비교 대상 | `InventoryService` (KafkaTemplate) vs `InventoryServiceWithSendTo` (@SendTo) |
| 핵심 차이 | 성공 이벤트 전송 방식 — 명시적 send() vs 반환값 자동 전송 |
| 활성화 방식 | @SendTo 버전은 `@Profile("ch03-sendto")`로 분리 |
| 설정 변경 | `SagaKafkaConfig`에 `factory.setReplyTemplate(ch03KafkaTemplate)` 추가 |

---

## 1. 두 방식의 코드 비교

### KafkaTemplate 방식 (InventoryService)

```java
@KafkaListener(topics = "chapter3.order-created", ...)
public void onOrderCreated(SagaOrderCreated avroEvent, Acknowledgment ack) {
    try {
        // ... 재고 예약 로직 ...

        // 성공: 명시적으로 토픽 지정하여 전송
        kafkaTemplate.send("chapter3.inventory-reserved", SagaEventMapper.toAvro(domainEvent));
        ack.acknowledge();

    } catch (Exception e) {
        // 실패: 다른 토픽으로 명시적 전송
        kafkaTemplate.send("chapter3.inventory-reservation-failed", SagaEventMapper.toAvro(failedEvent));
        ack.acknowledge();
    }
}
```

### @SendTo 방식 (InventoryServiceWithSendTo)

```java
@KafkaListener(topics = "chapter3.order-created", ...)
@SendTo("chapter3.inventory-reserved")
public SagaInventoryReserved onOrderCreated(SagaOrderCreated avroEvent, Acknowledgment ack) {
    try {
        // ... 재고 예약 로직 (동일) ...

        ack.acknowledge();
        return SagaEventMapper.toAvro(domainEvent);  // ✅ 반환값 → 자동 전송

    } catch (Exception e) {
        // ❌ 실패 토픽이 다름 → KafkaTemplate 필요 (하이브리드)
        kafkaTemplate.send("chapter3.inventory-reservation-failed", SagaEventMapper.toAvro(failedEvent));
        ack.acknowledge();
        return null;  // null → @SendTo 전송 안 함
    }
}
```

---

## 2. 트레이드오프 비교

| 관점 | KafkaTemplate | @SendTo |
|------|---------------|---------|
| **성공 경로 코드량** | `kafkaTemplate.send(토픽, 데이터)` 1줄 | `return 데이터` 1줄 (더 간결) |
| **실패 경로 처리** | 같은 패턴 (send + 다른 토픽) | KafkaTemplate 필요 + null 반환 (하이브리드) |
| **다중 토픽 발행** | 여러 send() 호출 가능 | 하나의 토픽만 지정 가능 |
| **조건부 발행** | if문으로 자유롭게 제어 | 반환값으로만 제어 (null = 미전송) |
| **반환 타입 제약** | void (자유) | 반드시 Avro 객체 반환 필요 |
| **replyTemplate 설정** | 불필요 | Container Factory에 `setReplyTemplate()` 필수 |
| **보상 리스너 적용** | 가능 | 불가능 (실패 시 throw 필요 → 반환값 제어 불가) |
| **일관성** | 모든 리스너에서 동일 패턴 | 정방향만 @SendTo, 보상은 KafkaTemplate → 불일치 |

---

## 3. @SendTo가 적합한 경우

@SendTo는 SAGA에는 부적합하지만, 다음 상황에서는 유용하다:

### 단순 변환 파이프라인

```
[Raw Event] → Enrichment → [Enriched Event] → Processing → [Result]
```

- 입력 1개 → 출력 1개, 실패 분기 없음
- 예: 로그 정규화, 데이터 변환, 형식 컨버전

### 구체적 예시

```java
// ✅ @SendTo에 적합: 단순 변환 (실패 = 예외 → DLT로 전송)
@KafkaListener(topics = "raw-logs")
@SendTo("normalized-logs")
public NormalizedLog onRawLog(RawLog log) {
    return NormalizedLog.builder()
            .timestamp(parseTimestamp(log.getRawTimestamp()))
            .level(normalizeLevel(log.getLevel()))
            .message(sanitize(log.getMessage()))
            .build();
}
```

```java
// ❌ @SendTo에 부적합: 성공/실패 분기 (SAGA)
@KafkaListener(topics = "order-created")
@SendTo("inventory-reserved")  // 실패하면 inventory-reservation-failed로 보내야 하는데?
public InventoryReserved onOrderCreated(OrderCreated event) {
    // 실패 시 다른 토픽으로 보내는 것이 불가능 → 하이브리드 필요
}
```

---

## 4. 왜 SAGA에서는 KafkaTemplate이 더 적합한가

### 이유 1: 성공/실패 토픽 분기

SAGA의 각 단계는 성공 이벤트와 실패 이벤트를 **서로 다른 토픽**으로 발행한다. @SendTo는 하나의 토픽만 지정할 수 있으므로, 실패 경로에서 KafkaTemplate이 불가피하다. 결국 두 가지 방식이 섞인 하이브리드가 되어 코드 가독성이 떨어진다.

### 이유 2: 보상 리스너에 적용 불가

보상 리스너는 성공 시 이벤트 발행 + 실패 시 throw(재시도)가 필요하다. throw하면 반환값이 없으므로 @SendTo로 이벤트를 보낼 수 없다. 결국 보상 리스너는 모두 KafkaTemplate을 사용해야 한다.

### 이유 3: 패턴 일관성

프로젝트 내에서 정방향은 @SendTo, 보상은 KafkaTemplate을 사용하면 두 가지 패턴이 혼재한다. 모든 리스너에서 KafkaTemplate을 사용하면 패턴이 통일되어 유지보수가 쉽다.

---

## 5. @SendTo 사용 시 주의점

### replyTemplate 설정 필수

@SendTo를 사용하려면 Container Factory에 `replyTemplate`을 설정해야 한다. 미설정 시 런타임 에러가 발생한다.

```java
// SagaKafkaConfig.java
factory.setReplyTemplate(kafkaTemplate);  // @SendTo 지원
```

이 설정은 @SendTo를 사용하지 않는 리스너에는 영향을 주지 않는다.

### null 반환 = 미전송

@SendTo 메서드에서 `null`을 반환하면 메시지가 전송되지 않는다. 이것은 Spring Kafka의 공식 동작이며, 실패 시 KafkaTemplate으로 별도 전송 후 null을 반환하는 하이브리드 패턴에서 활용한다.

### Avro 직렬화 호환

@SendTo의 반환값은 `replyTemplate`의 직렬화 설정을 따른다. ch03은 Avro 직렬화를 사용하므로, 반환값은 반드시 Avro SpecificRecord여야 한다.

---

## 6. 선택 체크리스트

| 질문 | Yes → | No → |
|------|-------|------|
| 성공/실패 토픽이 다른가? | KafkaTemplate | @SendTo 가능 |
| 한 리스너에서 여러 토픽으로 발행하는가? | KafkaTemplate | @SendTo 가능 |
| 조건에 따라 발행 여부가 달라지는가? | KafkaTemplate | @SendTo 가능 |
| 실패 시 throw로 재시도하면서 이벤트도 발행해야 하는가? | KafkaTemplate | @SendTo 가능 |
| 단순 변환 파이프라인인가? | @SendTo | KafkaTemplate |
| 프로젝트 내 다른 리스너도 모두 KafkaTemplate인가? | KafkaTemplate (일관성) | @SendTo 가능 |

**위 질문 중 하나라도 Yes → KafkaTemplate 사용**

---

## 7. 핵심 학습 포인트

1. **@SendTo는 "1입력 → 1출력, 단일 토픽" 파이프라인에 최적화**되어 있다. SAGA처럼 성공/실패 분기가 있으면 오히려 코드가 복잡해진다.
2. **null 반환 = 미전송**이라는 Spring Kafka 동작을 활용하면 하이브리드가 가능하지만, 두 가지 패턴이 섞이면 가독성이 떨어진다.
3. **보상 리스너에는 @SendTo를 적용할 수 없다** — 실패 시 throw(재시도)와 이벤트 발행을 동시에 해야 하기 때문이다.
4. **replyTemplate 설정**을 빠뜨리면 @SendTo가 런타임에 실패한다. 기존 리스너에는 영향이 없으므로, 향후 @SendTo 도입 가능성을 위해 미리 설정해두는 것이 안전하다.
5. **패턴 일관성**이 코드 품질에 중요하다. 한 프로젝트 내에서 이벤트 전송 방식을 통일하면 온보딩과 디버깅이 쉬워진다.
