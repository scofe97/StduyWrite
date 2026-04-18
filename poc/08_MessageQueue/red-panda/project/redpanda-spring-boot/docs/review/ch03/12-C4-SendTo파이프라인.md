# C4: @SendTo 기반 파이프라인 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | Consumer가 메시지를 가공하여 다른 토픽으로 자동 전송하는 파이프라인 패턴 |
| 파일 | `SendToConsumer.java`, `SendToConsumerTest.java`, `KafkaTopicConfig.java` |
| 테스트 | 2개 (정상 파이프라인 변환, null 반환 필터링) |

---

## 왜 이렇게 구현했는가

### @SendTo의 동작 원리

`@KafkaListener`에 `@SendTo("토픽명")`을 붙이면, 메서드의 **반환값이 지정된 토픽으로 자동 전송**된다. KafkaTemplate을 직접 주입하거나 `send()`를 호출할 필요가 없다.

```
chapter2.sendto-input → [SendToConsumer.process()] → chapter2.sendto-output
                          - ORDER_CREATED → ORDER_PROCESSED로 변환
                          - ORDER_CANCELLED → null 반환 (전달 안 함)
```

Spring Boot가 `ConcurrentKafkaListenerContainerFactory`에 `replyTemplate`으로 KafkaTemplate을 자동 등록한다. `@SendTo`는 이 template을 사용하여 반환값을 직렬화하고 전송한다.

### KafkaTemplate 직접 사용과의 비교

| | @SendTo | KafkaTemplate 직접 사용 |
|---|---|---|
| 코드량 | 반환값만 명시 | `kafkaTemplate.send()` 호출 필요 |
| 토픽 지정 | 어노테이션에 고정 | 런타임에 동적 지정 가능 |
| 키 전달 | 원본 메시지의 key를 자동 사용 | 직접 key 지정 |
| 에러 처리 | 메서드 예외 시 전송 안 됨 | try-catch로 세밀한 제어 |
| 적합한 경우 | 고정된 1:1 파이프라인 | 조건에 따라 여러 토픽으로 분기 |

### null 반환 = 전달하지 않음 (필터 패턴)

`@SendTo` 메서드가 `null`을 반환하면 Spring Kafka는 **출력 토픽에 아무것도 전송하지 않는다**. 이를 활용하면 특정 조건의 메시지만 다음 토픽으로 전달하는 **필터 패턴**을 구현할 수 있다.

```java
@KafkaListener(topics = "chapter2.sendto-input", groupId = "sendto-group")
@SendTo("chapter2.sendto-output")
public OrderEvent process(OrderEvent event, Acknowledgment ack) {
    ack.acknowledge();

    // 필터: CANCEL 이벤트는 전달하지 않음
    if ("ORDER_CANCELLED".equals(event.getEventType().toString())) {
        return null;  // output 토픽에 전송 안 됨
    }

    // 변환 후 전달
    return OrderEvent.newBuilder(event)
            .setEventType("ORDER_PROCESSED")
            .build();
}
```

### @SendTo는 @KafkaListener 전용이다

`@SendTo`는 일반 메서드에 붙여도 **동작하지 않는다**. 반드시 `@KafkaListener`와 함께 사용해야 한다.

이유는 `@SendTo`의 반환값 전송을 **Listener Container**가 담당하기 때문이다.

```
Listener Container가 poll() → 메시지 수신
  → @KafkaListener 메서드 호출
  → 반환값 캡처
  → @SendTo가 있으면 replyTemplate(KafkaTemplate)으로 전송
```

일반 메서드(`@RestController`, `@Service`, `@Scheduled` 등)에는 이 반환값을 가로채서 토픽으로 보내주는 컨테이너가 없다. Spring이 반환값을 인식할 수 없으므로 `@SendTo`를 붙여도 무시된다.

| 상황 | 방식 |
|------|------|
| Consumer → 토픽 (파이프라인) | `@SendTo` 사용 가능 |
| REST API → 토픽 | `KafkaTemplate.send()` 직접 호출 |
| 스케줄러 → 토픽 | `KafkaTemplate.send()` 직접 호출 |
| 서비스 로직 → 토픽 | `KafkaTemplate.send()` 직접 호출 |

결론: `@SendTo`는 **Consumer-to-Topic 파이프라인 전용 편의 기능**이고, 그 외 모든 경우는 KafkaTemplate을 직접 사용해야 한다.

### @SendTo를 사용할 수 없는 기타 경우

`@KafkaListener` 안에서도 다음 경우에는 KafkaTemplate을 직접 사용하는 것이 낫다.

| 상황 | 이유 |
|------|------|
| 하나의 입력에서 여러 토픽으로 분기 | @SendTo는 단일 토픽만 지정 가능 |
| 조건에 따라 다른 토픽으로 전송 | 토픽이 어노테이션에 고정되어 동적 변경 불가 |
| 전송 결과(offset, partition) 확인 필요 | @SendTo는 전송 결과를 반환하지 않음 |

### 동적 토픽 전환이 필요하면?

SpEL(Spring Expression Language)로 제한적인 동적 라우팅이 가능하다.

```java
// 원본 메시지의 헤더 값에 따라 토픽 결정
@SendTo("#{headers['output-topic']}")
```

하지만 복잡한 라우팅 로직이 필요하면 KafkaTemplate을 직접 사용하는 것이 명확하다.

### 파이프라인 체이닝

`@SendTo`를 여러 단계로 연결하면 **다단계 파이프라인**을 구성할 수 있다.

```
orders → [검증] → validated-orders → [가격계산] → priced-orders → [알림]
```

각 단계가 독립적인 Consumer이므로:
- **독립 배포**: 검증 로직 변경 시 검증 서비스만 재배포
- **독립 스케일링**: 가격계산이 느리면 해당 Consumer만 인스턴스 증가
- **장애 격리**: 알림 서비스 장애가 검증/가격계산에 영향 없음

---

## 핵심 학습 포인트

1. **@SendTo = 자동 전달** — 반환값을 지정 토픽으로 자동 전송, KafkaTemplate 주입 불필요
2. **null 반환 = 필터링** — 조건에 맞지 않는 메시지를 걸러내는 패턴
3. **key 자동 전달** — 원본 메시지의 key가 출력 메시지에 그대로 사용됨
4. **replyTemplate 자동 설정** — Spring Boot가 KafkaTemplate을 Factory에 자동 등록
5. **제한사항 인지** — 단일 고정 토픽, Consumer 전용, 전송 결과 미반환

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | **High** | `SendToConsumer`의 `latch`, `last*Event` 필드에 volatile 미적용 — 리스너 스레드와 테스트 스레드 간 가시성 이슈 | 간헐 실패 가능 (C7/C8에서 동일 패턴 수정 완료) |
| 2 | **High** | "출력이 없어야 함"을 `await(3s) == false`로만 검증 — 3초 이후 도착하면 false-negative | 부정 시나리오 관찰 창이 너무 짧고 취약 |
