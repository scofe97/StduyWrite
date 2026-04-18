# #1: SAGA 이벤트 설계

sealed interface로 이벤트 계약 정의, 성공/실패/보상 이벤트 분류

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 실습 번호 | #1 (SAGA 이벤트 설계) |
| 주요 파일 | `src/.../ch03/event/OrderSagaEvent.java` 외 9개 record |
| 테스트 파일 | 없음 (이벤트 정의는 별도 테스트 불필요, 서비스 테스트에서 검증) |
| LEARN.md 위치 | line 267~343 |

### 파일 목록

| 파일 | 역할 | 분류 |
|------|------|------|
| `OrderSagaEvent.java` | sealed interface (공통 계약) | 기반 |
| `OrderCreated.java` | SAGA 시작, 주문 정보 포함 | 성공 |
| `InventoryReserved.java` | 재고 예약 완료 | 성공 |
| `PaymentCompleted.java` | 결제 완료 | 성공 |
| `ShippingRequested.java` | 배송 요청 (SAGA 최종) | 성공 |
| `InventoryReservationFailed.java` | 재고 부족 실패 | 실패 |
| `PaymentFailed.java` | 결제 실패 | 실패 |
| `ShippingFailed.java` | 배송 실패 | 실패 |
| `InventoryReleased.java` | 보상: 재고 복구 | 보상 |
| `PaymentRefunded.java` | 보상: 환불 | 보상 |

## 왜 이렇게 구현했는가

### sealed interface 선택 이유

Avro가 아닌 **Java sealed interface + record**를 선택했다. 이유:

1. **Avro의 한계**: Avro는 sealed interface를 표현할 수 없다. SAGA 이벤트는 공통 계약(`orderId`, `correlationId`, `timestamp`)을 강제해야 하는데, Avro의 union type으로는 컴파일 타임 타입 안전성을 보장할 수 없다.
2. **record의 장점**: 불변(immutable), `equals`/`hashCode`/`toString` 자동 생성, 직렬화 친화적. 이벤트는 한번 생성되면 변경되지 않으므로 record가 자연스럽다.
3. **sealed의 장점**: 허용된 구현체를 컴파일 타임에 제한하여, SAGA에 참여하는 이벤트 타입을 명확히 정의. Java 21+ switch 패턴 매칭에서 exhaustiveness 검사도 가능.

### JSON 직렬화 결정

기존 ch02는 Avro + Schema Registry를 사용하지만, ch03는 JSON으로 직렬화한다. 이유:
- sealed interface / record는 Avro 스키마로 변환 불가
- SAGA 이벤트는 서비스 간 계약이므로, 스키마 진화보다 타입 안전성이 더 중요
- 실무에서도 내부 도메인 이벤트는 JSON, 외부 공개 이벤트는 Avro를 쓰는 하이브리드 패턴이 일반적

### 이벤트 분류 체계 (3카테고리)

| 카테고리 | 이벤트 | 역할 |
|----------|--------|------|
| 성공 | OrderCreated → InventoryReserved → PaymentCompleted → ShippingRequested | 정방향 체인 |
| 실패 | InventoryReservationFailed, PaymentFailed, ShippingFailed | 실패 알림 + 보상 트리거 |
| 보상 | PaymentRefunded, InventoryReleased | 역순으로 되돌리기 |

### OrderItem을 OrderCreated 내부 record로 정의한 이유

`OrderItem`은 `OrderCreated` 이벤트 안에서만 사용되는 값 객체다. 별도 파일로 분리하면 10개 → 11개로 파일이 늘어나고, `OrderItem`만 단독으로 사용되는 시나리오가 없다. 응집도를 높이기 위해 `OrderCreated.OrderItem`으로 중첩 정의했다.

## 교차 검증 결과

### Claude 리뷰

- LEARN.md의 이벤트 정의(line 267~343)와 1:1 매칭 확인
- 공통 필드 3개(`orderId`, `correlationId`, `timestamp`)가 모든 record에 존재
- 보상 이벤트의 Javadoc에 보상 역순(ShippingFailed → PaymentRefunded → InventoryReleased) 명시

### LEARN.md와의 차이점

| 항목 | LEARN.md | 구현 | 이유 |
|------|----------|------|------|
| OrderItem 위치 | 별도 타입 (암시적) | `OrderCreated.OrderItem` 내부 record | 응집도 |
| import 구조 | 하나의 코드블록 | 파일별 분리 | Java 컨벤션 (1 public type = 1 file) |

## 핵심 학습 포인트

- **sealed interface는 도메인 이벤트의 타입 안전성을 보장하는 도구다.** 새로운 이벤트를 추가하려면 `permits` 목록에 명시해야 하므로, 의도치 않은 이벤트 타입이 SAGA에 섞이는 것을 방지한다.
- **Avro vs JSON은 이벤트의 성격에 따라 선택한다.** 스키마 진화가 중요한 외부 이벤트는 Avro, 타입 안전성이 중요한 내부 도메인 이벤트는 sealed interface + JSON이 적합하다.
- **보상 이벤트는 실패 이벤트와 분리해야 한다.** `PaymentFailed`(실패 알림)와 `PaymentRefunded`(보상 완료)는 역할이 다르다. 실패는 "문제 발생"을 알리고, 보상은 "되돌리기 완료"를 알린다.
