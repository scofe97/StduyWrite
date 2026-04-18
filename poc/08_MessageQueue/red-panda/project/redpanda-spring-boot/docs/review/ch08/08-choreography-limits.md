# #8 Choreography 한계 대응

SAGA 상태 추적 API + correlationId MDC 분산 추적으로 Choreography의 관측 가능성 한계를 보완

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 신규 파일 | `SagaStatusController`, `SagaStatusResponse`, `SagaMdc` |
| 변경 파일 | `OrderService`, `InventoryService`, `PaymentService`, `ShippingService` (4개), `OrderRepository`, `ReservationRepository`, `ProcessedEventRepository` |
| 핵심 전략 | correlationId 기반 통합 조회 API + MDC 로깅으로 서비스 간 추적 |
| 빌드 결과 | compileJava + compileTestJava 성공 |

---

## 1. Choreography의 한계는 무엇인가

Choreography에서는 각 서비스가 독립적으로 이벤트에 반응하므로, 전체 SAGA의 현재 상태를 한곳에서 파악할 수 없다:

- **관측 어려움**: "주문 X는 지금 어디까지 진행됐나?"에 4개 서비스를 각각 조회해야 답할 수 있다
- **디버깅 어려움**: 장애 발생 시 어느 서비스에서 멈췄는지 로그를 일일이 찾아야 한다
- **흐름 파악 어려움**: 이벤트 체인이 길어지면 전체 흐름을 추적하기 힘들다

Orchestration 패턴은 중앙 오케스트레이터가 이 역할을 하지만, Choreography를 유지하면서도 보완할 수 있는 두 가지 방법을 구현했다.

---

## 2. 해결 1: SAGA 상태 추적 API

### 설계

correlationId 하나로 4개 서비스의 상태를 통합 조회하는 REST API:

```
GET /api/ch03/saga/{correlationId}/status
```

### 응답 구조

```java
public record SagaStatusResponse(
    String correlationId,
    OrderInfo order,              // 주문 상태
    List<ReservationInfo> reservations,  // 재고 예약 상태
    PaymentInfo payment,          // 결제 상태
    ShippingInfo shipping,        // 배송 상태
    List<String> processedSteps   // 처리 완료 단계 (멱등성 테이블 재활용)
) { ... }
```

### 왜 이렇게 구현했는가

1. **correlationId → orderId 매핑**: `OrderRepository.findByCorrelationId()`로 먼저 주문을 찾고, orderId로 나머지 서비스를 조회한다. correlationId가 모든 이벤트에 전파되므로 가능하다.

2. **processedSteps 재활용**: #7에서 만든 `ProcessedEvent` 테이블을 재활용한다. `findByCorrelationId()`로 해당 SAGA에서 완료된 단계 목록을 가져온다. 별도의 상태 추적 테이블을 만들지 않고 기존 인프라를 활용한 것이 핵심이다.

3. **null 허용**: 아직 도달하지 않은 서비스의 정보는 null로 반환한다. 예를 들어 재고 예약 중이면 payment=null, shipping=null이다.

### 응답 예시 (정상 완료)

```json
{
  "correlationId": "abc-123",
  "order": { "orderId": "ord-1", "status": "COMPLETED", "trackingNumber": "TRACK-xyz" },
  "reservations": [
    { "reservationId": "res-1", "productId": "PROD-001", "quantity": 2, "status": "RESERVED" }
  ],
  "payment": { "paymentId": "pay-1", "transactionId": "TXN-abc", "amount": "50000", "status": "COMPLETED" },
  "shipping": { "shippingId": "ship-1", "trackingNumber": "TRACK-xyz", "status": "REQUESTED" },
  "processedSteps": ["InventoryReserve", "PaymentProcess", "ShippingProcess", "OrderComplete"]
}
```

### 응답 예시 (결제 실패)

```json
{
  "correlationId": "abc-456",
  "order": { "orderId": "ord-2", "status": "FAILED", "failureReason": "Payment: Insufficient funds" },
  "reservations": [
    { "reservationId": "res-2", "productId": "PROD-001", "quantity": 1, "status": "RELEASED" }
  ],
  "payment": null,
  "shipping": null,
  "processedSteps": ["InventoryReserve", "OrderFail-Payment", "InventoryRelease-PaymentFailed"]
}
```

---

## 3. 해결 2: MDC 분산 추적 로깅

### SagaMdc 유틸리티

```java
public final class SagaMdc {
    public static final String CORRELATION_ID = "correlationId";
    public static final String ORDER_ID = "orderId";

    public static void set(String correlationId, String orderId) {
        MDC.put(CORRELATION_ID, correlationId);
        MDC.put(ORDER_ID, orderId);
    }

    public static void clear() {
        MDC.remove(CORRELATION_ID);
        MDC.remove(ORDER_ID);
    }
}
```

### 적용 패턴

모든 10개 리스너에 동일한 패턴으로 적용:

```java
public void onSomeEvent(AvroEvent avroEvent, Acknowledgment ack) {
    DomainEvent event = SagaEventMapper.toDomain(avroEvent);
    SagaMdc.set(event.correlationId(), event.orderId());
    try {
        // ... 비즈니스 로직 ...
    } finally {
        SagaMdc.clear();  // 반드시 정리 (스레드 풀 재사용 시 오염 방지)
    }
}
```

### 왜 try-finally인가

Kafka Consumer는 스레드 풀을 사용한다. MDC를 정리하지 않으면 다음 메시지 처리 시 이전 correlationId가 로그에 남는다. `finally`에서 정리하면 예외 발생 시에도 안전하다.

### Logback 패턴 설정

```xml
<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level [cid=%X{correlationId}][oid=%X{orderId}] %logger{36} - %msg%n</pattern>
```

이 패턴을 사용하면 모든 로그에 correlationId와 orderId가 자동 포함된다:

```
14:23:45.123 [consumer-1] INFO  [cid=abc-123][oid=ord-1] InventoryService - [SAGA] Inventory reserved
14:23:45.234 [consumer-2] INFO  [cid=abc-123][oid=ord-1] PaymentService - [SAGA] Payment completed
14:23:45.345 [consumer-3] INFO  [cid=abc-123][oid=ord-1] ShippingService - [SAGA] Shipping requested
14:23:45.456 [consumer-4] INFO  [cid=abc-123][oid=ord-1] OrderService - [SAGA] Order completed
```

Kibana/Grafana에서 `cid=abc-123`으로 검색하면 4개 서비스의 로그가 시간순으로 나열된다.

---

## 4. 두 해결책의 역할 분담

| | 상태 추적 API | MDC 분산 추적 |
|---|---|---|
| **목적** | 현재 상태 조회 | 실시간 로그 추적 |
| **사용 시점** | 운영 대시보드, CS 문의 | 장애 디버깅, 흐름 파악 |
| **데이터 소스** | DB (4개 테이블 + ProcessedEvent) | 로그 (ELK, Loki 등) |
| **지연** | DB 조회 시점의 스냅샷 | 실시간 |
| **한계** | 이벤트 체인의 "과정"은 보이지 않음 | 로그 수집 인프라 필요 |

두 가지를 함께 사용하면:
- **"지금 어디까지 갔나?"** → 상태 추적 API
- **"왜 여기서 멈췄나?"** → MDC 로그 검색

---

## 5. Choreography vs Orchestration 전환 판단 기준

이번 구현을 통해 느낀 Choreography의 한계와 전환 기준:

| 기준 | Choreography 유지 | Orchestration 전환 |
|------|-------------------|-------------------|
| 서비스 수 | 3~4개 | 5개 이상 |
| 보상 복잡도 | 선형 역순 | 조건부 분기 (A 실패 → B or C) |
| 상태 추적 | 상태 API로 충분 | 실시간 진행 상태 필수 |
| 흐름 변경 빈도 | 드묾 | 빈번 (새 단계 추가/제거) |
| 팀 구조 | 각 서비스팀 독립 운영 | 중앙 플로우 관리팀 존재 |

현재 Ch08의 4개 서비스 + 선형 보상 구조는 Choreography로 충분하지만, 상태 추적 API와 MDC가 없었다면 디버깅이 어려웠을 것이다.

---

## 6. 핵심 학습 포인트

1. **Choreography의 관측 가능성은 별도로 구축해야 한다**: 이벤트 기반이라 전체 흐름이 코드에 명시되지 않으므로, 상태 추적과 분산 추적을 직접 만들어야 한다.
2. **기존 인프라 재활용**: ProcessedEvent 테이블을 상태 추적에 재활용하면 별도 테이블 없이 처리 단계를 조회할 수 있다.
3. **MDC는 try-finally 필수**: 스레드 풀 재사용 환경에서 MDC 누수는 로그 오염을 초래한다.
4. **correlationId가 만능 키**: 이벤트 설계 시 correlationId를 모든 이벤트에 전파하면, 멱등성(#7) + 상태 추적(#8) + 분산 추적(#8) 세 가지를 모두 해결할 수 있다.
5. **Orchestration 전환은 복잡도가 기준**: 서비스 수, 보상 분기, 흐름 변경 빈도가 임계점을 넘으면 전환을 고려한다.
