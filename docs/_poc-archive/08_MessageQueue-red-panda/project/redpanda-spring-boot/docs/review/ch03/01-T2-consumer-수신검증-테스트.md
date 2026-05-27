# T2: Consumer 수신 검증 테스트

## 목적

기존 테스트(T1)는 Producer가 브로커에 메시지를 보냈는지만 검증한다. Consumer가 실제로 메시지를 수신하고 처리했는지는 검증하지 않는다. T2는 end-to-end 검증을 추가한다.

```
Producer -> 브로커 전송 (T1) -> Consumer 수신 (T2)
              offset 확인          latch countdown = 0 확인
```

---

## 변경 파일

### 1. OrderConsumer.java

`CountDownLatch`와 `lastReceivedEvent` 필드 추가.

```java
@Getter
private CountDownLatch latch = new CountDownLatch(1);

@Getter
private OrderEvent lastReceivedEvent;

public void resetLatch(int count) {
    this.latch = new CountDownLatch(count);
}

@KafkaListener(topics = "chapter2.orders", groupId = "order-consumer-group")
public void consume(OrderEvent event, Acknowledgment ack) {
    // ... 기존 로깅 ...
    lastReceivedEvent = event;
    latch.countDown();
    ack.acknowledge();
}
```

### 2. ProducerConsumerTest.java

새 테스트 메서드 추가.

```java
@Test
void 주문_10건_발행하면_Consumer가_모두_수신한다() throws Exception {
    int messageCount = 10;
    orderConsumer.resetLatch(messageCount);

    for (int i = 1; i <= messageCount; i++) {
        // ... 이벤트 생성 및 전송 ...
        orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);
    }

    boolean allReceived = orderConsumer.getLatch().await(30, TimeUnit.SECONDS);

    assertThat(allReceived)
            .as("Consumer가 %d건 모두 수신해야 한다", messageCount)
            .isTrue();
    assertThat(orderConsumer.getLastReceivedEvent()).isNotNull();
    assertThat(orderConsumer.getLastReceivedEvent().getOrderId()).startsWith("ORD-");
}
```

---

## 설계 결정과 이유

### CountDownLatch를 사용한 이유

Kafka Consumer는 `@KafkaListener`가 **별도 스레드**(ListenerConsumer)에서 동작한다. 테스트 스레드에서 "Consumer가 10건 받았는지"를 동기적으로 기다리려면 스레드 간 동기화 수단이 필요하다.

`CountDownLatch`는 가장 단순한 blocking wait 메커니즘이다. `countDown()`을 10번 호출하면 `await()`가 풀린다. `await(30, TimeUnit.SECONDS)`로 타임아웃을 설정하여 무한 대기를 방지한다.

### resetLatch(int count) 메서드를 둔 이유

`CountDownLatch`는 재사용이 불가능하다 (count가 0이 되면 다시 올릴 수 없다). 테스트마다 기대 건수가 다를 수 있으므로 새 인스턴스로 교체하는 메서드를 제공한다.

### lastReceivedEvent 필드를 둔 이유

latch만으로는 "수신 완료"만 알 수 있고, **수신된 데이터가 정상인지**는 검증할 수 없다. 마지막 수신 이벤트를 저장하여 내용 검증을 가능하게 했다.

### 프로덕션 코드에 테스트 훅을 노출한 이유

`@SpyBean`으로 Consumer를 감싸는 방법도 있지만, Consumer 수신 카운트는 모니터링(Micrometer Counter)에서도 유용한 정보다. 현재는 학습 프로젝트이므로 간단하게 필드로 노출했다. 프로덕션이라면 Micrometer Counter로 대체하는 것이 더 깔끔하다.

### ORD-010 고정 검증 -> startsWith("ORD-") 변경 이유

**첫 실행 시 실패했다.** expected: `ORD-010`, actual: `ORD-002`.

토픽이 3파티션이다. 메시지 키(`orderId`)의 해시값에 따라 파티션이 분배되므로, **소비 순서는 전송 순서와 다르다.** `ORD-010`이 마지막으로 소비된다는 보장이 없다.

핵심 검증은 latch가 0이 되었는지(= 10건 모두 수신)이다. 마지막 이벤트의 정확한 orderId는 파티션 분배에 의존하므로, "유효한 OrderEvent인가"만 검증하는 것이 올바르다.

---

## 한계점

- `lastReceivedEvent`는 동시성 문제가 있다 (여러 파티션에서 동시에 쓸 수 있음). 프로덕션이라면 `AtomicReference`나 `ConcurrentLinkedQueue`를 써야 한다.
- "몇 건 받았는가"만 검증하고, "어떤 내용을 받았는가"는 약하게 검증한다. `List<OrderEvent>`로 수집하면 더 강한 검증이 가능하다.
- 첫 테스트(T1)에서 Consumer가 이미 메시지를 소비했을 수 있다. `@DirtiesContext`로 테스트 간 컨텍스트를 분리하지만, 같은 클래스 내 테스트 순서에 따라 latch 초기값 이슈가 생길 수 있다.

---

## 테스트 결과

- BUILD SUCCESSFUL
- 2 tests completed, 0 failed
