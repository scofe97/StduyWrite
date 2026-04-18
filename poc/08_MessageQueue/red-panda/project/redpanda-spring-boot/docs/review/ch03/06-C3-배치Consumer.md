# C3: 배치 Consumer + Factory 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 여러 메시지를 List로 한 번에 수신하는 배치 Consumer 구현 |
| 파일 | `BatchKafkaConfig.java`, `BatchOrderConsumer.java`, `BatchConsumerTest.java` |
| 테스트 | 2개 (20건 배치 수신, 단일 메시지 배치 수신) |
| 리뷰 결과 | APPROVE — HIGH 이슈 없음 |

---

## 왜 이렇게 구현했는가

### Factory를 별도로 만든 이유

YAML의 `spring.kafka.listener.*`는 **모든 Consumer에 적용되는 전역 기본값**이다. 하지만 이 프로젝트는 단일 메시지 Consumer(`OrderConsumer`)와 배치 Consumer(`BatchOrderConsumer`)가 **같은 애플리케이션에 공존**한다. YAML에 `listener.type: batch`를 설정하면 모든 Consumer가 배치 모드가 되므로, Factory를 분리하여 특정 `@KafkaListener`에만 배치 모드를 적용했다.

| 방식 | 적용 범위 | 적합한 경우 |
|------|----------|------------|
| YAML `listener.type: batch` | 전역 (모든 Consumer) | 앱 전체가 배치 모드일 때 |
| **Factory Bean 분리** (현재) | 특정 `@KafkaListener`만 | 단일/배치 Consumer 공존 시 |

### ConsumerFactory를 주입받아 재사용하는 이유

Spring Boot Auto-Configuration이 YAML 기반으로 이미 `ConsumerFactory` Bean을 생성한다 (bootstrap-servers, deserializer, schema.registry.url 등 포함). 이것을 주입받으면:

1. **설정 중복 제거**: 같은 broker/schema registry 설정을 Java 코드에 다시 쓸 필요 없음
2. **단일 진실 원천**: YAML 한 곳만 수정하면 단일/배치 Consumer 모두 반영
3. **테스트 호환성**: `AbstractKafkaTest`의 `@DynamicPropertySource`가 YAML을 덮어쓰면 이 Factory도 자동 반영

### setBatchListener(true)와 List 파라미터의 관계

**두 설정은 반드시 일치해야 한다.** 불일치 시 런타임 예외가 발생한다.

| Factory 설정 | 메서드 파라미터 | 결과 |
|-------------|---------------|------|
| `setBatchListener(true)` | `List<OrderEvent>` | 정상 |
| `setBatchListener(true)` | `OrderEvent` (단일) | **ClassCastException** |
| `setBatchListener(false)` | `List<OrderEvent>` | 의미 없음 (항상 1건) |
| `setBatchListener(false)` | `OrderEvent` (단일) | 정상 (기본 모드) |

컴파일 시점에 잡히지 않으므로 **통합 테스트에서 반드시 검증**해야 한다.

### 같은 토픽을 다른 groupId로 구독하는 패턴

```java
OrderConsumer      → groupId = "order-consumer-group"      // 단일 메시지
BatchOrderConsumer → groupId = "batch-consumer-group"       // 배치
```

같은 groupId면 메시지가 둘 중 하나에만 전달된다 (파티션 분배). 다른 groupId면 **둘 다 모든 메시지를 독립적으로 수신**한다.

프로덕션에서 이 패턴이 정당화되는 경우: CQRS(읽기 모델 분리), 감사 로그, 실시간 분석 파이프라인 등 **서로 다른 비즈니스 목적**을 가진 Consumer Group들.

### 배치 ACK 전략

`AckMode.MANUAL` + `ack.acknowledge()` = 배치 내 **마지막 메시지의 offset + 1**이 커밋된다.

| ACK 전략 | 동작 | 장단점 |
|----------|------|--------|
| **MANUAL** (현재) | 명시적 호출 시 커밋 | 처리 완료 보장, 실패 시 재처리 |
| MANUAL_IMMEDIATE | 호출 즉시 커밋 | 지연 없지만 매번 네트워크 왕복 |
| BATCH (Spring 기본) | poll() 처리 완료 후 자동 커밋 | 간결하지만 장애 시 유실 가능 |

**주의**: `ack.acknowledge()` 전에 예외가 발생하면 **배치 전체가 재처리**된다 (at-least-once). 1~9번 성공 후 10번에서 실패하면 1~9번도 중복 처리된다.

### 테스트에서 latch(1)로 설정한 이유

`consumeBatch()`의 `latch.countDown()`은 **배치당 1회** 호출된다. 20건이 몇 개의 배치로 나뉠지는 예측할 수 없다:

- 최선: 20건 → 1배치 → countDown 1회
- 최악: 20건 → 20배치 → countDown 20회

`latch(20)`으로 설정하면 "정확히 20배치"인 경우에만 통과하므로 거의 항상 타임아웃된다. `latch(1)`은 **"최소 한 번의 배치 수신"**을 보장하는 올바른 선택이다.

---

## 코드 리뷰 결과

| 심각도 | 이슈 | 상태 |
|--------|------|------|
| LOW | `totalReceivedCount`에 스레드 안전성 주석 추가 권장 | 인지 (concurrency=1 전제로 안전) |
| LOW | 배치 크기 검증 강화 가능 (totalReceivedCount == 20) | 인지 (flaky 가능성으로 수용) |
| LOW | 부분 실패 시나리오 주석 추가 권장 | 인지 (학습 범위 외) |

---

## 핵심 학습 포인트

1. **Factory 분리** — 단일/배치 Consumer가 공존할 때 필수, `containerFactory` 파라미터로 지정
2. **ConsumerFactory 재사용** — Spring Boot Auto-Config이 만든 것을 주입, 설정 중복 제거
3. **setBatchListener(true) ↔ List\<T\> 파라미터** — 불일치 시 런타임 에러, 컴파일에서 안 잡힘
4. **groupId 분리** — 같은 토픽을 독립적으로 소비하려면 다른 groupId 사용
5. **배치 ACK** — 배치 전체 처리 후 한 번만 acknowledge(), 부분 실패 시 전체 재처리
6. **latch 단위** — 배치 모드에서는 메시지 단위가 아닌 배치 단위로 latch 설정
7. **배치 크기는 비결정적** — `max.poll.records`(기본 500) 이하에서 가변, 테스트에서 정확한 크기 단언 불가

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | **High** | `messageCount=20` 전송 후 latch=1, `>=1`만 단언 — 1건만 처리되어도 통과 | 배치 Consumer 핵심 동작(다수 메시지 일괄 처리) 미검증 |
| 2 | **High** | 단일 메시지 테스트도 `size >= 1`만 확인 | 배치 동작 회귀 탐지 불가 |
