# C9: Idempotent Consumer (dedup) 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | eventId 기반 중복 메시지 처리 방어 (Consumer 측 멱등성) |
| 파일 | `IdempotentConsumer.java`, `IdempotentConsumerTest.java`, `KafkaTopicConfig.java` |
| 테스트 | 2개 (같은 eventId 중복 skip, 다른 eventId 정상 처리) |

---

## 왜 이렇게 구현했는가

### Kafka의 at-least-once와 중복 발생 시나리오

Kafka는 기본적으로 at-least-once 전달을 보장한다. 즉, 메시지가 유실되지 않는 대신 중복이 발생할 수 있다.

중복이 발생하는 시나리오:
1. Consumer가 메시지를 처리하고 `ack.acknowledge()` 호출 전에 크래시 → 재시작 후 같은 메시지를 다시 poll
2. Producer가 네트워크 재시도로 같은 메시지를 2번 전송 (Producer 멱등성이 꺼져있거나 PID가 변경된 경우)
3. Consumer 리밸런싱 중 offset 커밋이 유실 → 이전 메시지 재전달

### dedup 키로 eventId를 선택한 이유

| 키 후보 | 문제점 |
|---------|--------|
| orderId | 같은 주문의 다른 이벤트(생성, 수정, 취소)가 모두 같은 키 → 정상 이벤트도 skip |
| offset | 리밸런싱 후 offset이 바뀔 수 있음, 파티션간 중복 불가 |
| **eventId** | 이벤트마다 고유한 UUID → 정확한 중복 감지 |

### ConcurrentHashMap.newKeySet()을 사용한 이유

`Set.add()`는 **원자적으로 존재 여부 확인 + 삽입**을 수행한다. 별도 동기화 없이 스레드 안전한 dedup이 가능하다.

```java
// add()가 false → 이미 존재 → 중복
if (!processedEventIds.add(eventId)) {
    // skip
    return;
}
// 여기 도달 = 신규 메시지
```

### In-memory vs 영속 저장소

| 방식 | 장점 | 단점 | 적합한 경우 |
|------|------|------|------------|
| **In-memory Set** (현재) | 빠름, 의존성 없음 | 재시작 시 유실, 메모리 한계 | 학습/PoC, 단일 인스턴스 |
| DB dedup 테이블 | 영속, 정확, 여러 인스턴스 공유 | DB 의존성, 약간의 지연 | 프로덕션 (정확성 우선) |
| Redis SET + TTL | 빠름 + 영속 + TTL 자동 만료 | Redis 인프라 필요 | 프로덕션 (성능 + 정확성) |

프로덕션 전환 시: `processedEventIds.add(eventId)` → `INSERT ... ON CONFLICT DO NOTHING` (DB) 또는 `SET eventId NX EX 3600` (Redis)

### 중복 메시지도 ack하는 이유

중복 메시지를 skip할 때도 `ack.acknowledge()`를 호출한다. ack하지 않으면 offset이 전진하지 않아 같은 메시지를 무한히 다시 poll하게 된다.

---

## Producer 멱등성(P7)과의 관계

| | Producer 멱등성 (P7) | Consumer dedup (C9) |
|---|---|---|
| 방어 대상 | 네트워크 재시도 중복 | 모든 종류의 중복 |
| 범위 | 같은 Producer 세션 내 (PID 기반) | eventId 기반으로 출처 무관 |
| PID 변경 시 | 방어 불가 (재시작하면 새 PID) | 방어 가능 |
| 비용 | 설정 한 줄 (거의 무료) | dedup 저장소 필요 |

**결론: 둘 다 필요하다.** Producer 멱등성은 네트워크 레벨만 방어하고, Consumer dedup은 앱 레벨(재시작, 리밸런싱 등)까지 방어한다. Producer 멱등성은 비용이 거의 없으므로 항상 켜고, Consumer dedup으로 나머지를 보완하는 것이 정석이다.

---

## 핵심 학습 포인트

1. **at-least-once → 중복 가능** — Kafka 기본 보장, Consumer에서 방어 필요
2. **eventId 기반 dedup** — orderId가 아닌 이벤트 고유 식별자 사용
3. **Set.add() 원자적 체크** — 별도 동기화 없이 스레드 안전한 중복 감지
4. **중복도 ack 필수** — skip해도 offset 전진시켜야 무한 재전달 방지
5. **P7 + C9 = 완전한 멱등성** — Producer(네트워크 레벨) + Consumer(앱 레벨) 양쪽 방어

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | Medium | count 위주 검증으로 "정확히 어떤 eventId가 처리/중복되었는지" 보장 못함 | 핵심 단언 부족 — 멱등성 로직의 정확성 검증 불가 |
