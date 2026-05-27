# C5: DefaultErrorHandler + DLT 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | Consumer 에러 발생 시 재시도 후 DLT로 전송하는 에러 처리 파이프라인 구현 |
| 파일 | `KafkaErrorConfig.java`, `ErrorProneConsumer.java`, `ErrorHandlerTest.java`, `KafkaTopicConfig.java` |
| 테스트 | 2개 (재시도 소진 후 DLT 전송, 정상 처리 시 에러 핸들러 미개입) |

---

## 왜 이렇게 구현했는가

### DefaultErrorHandler를 @Bean으로 등록한 이유

`@Bean`으로 등록하면 Spring Kafka가 **모든 Listener Container에 자동 적용**한다. Container Factory에 수동으로 `setCommonErrorHandler()`를 호출할 필요가 없다. 이것은 Spring Kafka 2.8+ 표준 방식이다.

### 재시도는 토픽을 거치지 않는다 (블록킹 재시도)

DefaultErrorHandler의 재시도는 **Consumer 메모리 안에서** 일어난다. 브로커에 메시지를 다시 발행하지 않는다.

```
Producer → [토픽: 메시지 1건 적재] → Consumer poll()
                                        ↓
                                  1차 시도 → 예외
                                  2차 시도 → 예외   ← 메모리 내 재전달
                                  3차 시도 → 예외
                                        ↓
                                  재시도 소진 → DLT로 1건 발행
                                  원본 토픽 offset commit
```

**왜 토픽에 메시지가 1건만 있는가?** Kafka 토픽은 **불변 추가 전용 로그(immutable append-only log)**이기 때문이다. Producer가 send()한 시점에 메시지가 적재되고, Consumer의 처리 결과와 무관하게 그대로 남아있다. Consumer는 "어디까지 읽었는지(offset)"만 관리하지, 메시지를 삭제하거나 롤백하지 않는다.

| 상황 | offset 커밋 | 결과 |
|------|------------|------|
| 정상 처리 | `ack.acknowledge()` → 커밋 | 다음 메시지로 진행 |
| 재시도 소진 → DLT 전송 | ErrorHandler가 커밋 | 다음 메시지로 진행 |
| 커밋 안 하고 Consumer 재시작 | 미커밋 | 같은 메시지를 다시 poll |

### RDB 트랜잭션과의 차이

| | RDB (트랜잭션) | Kafka (로그) |
|---|---|---|
| 실패 시 | 롤백 → 데이터 사라짐 | 메시지 그대로 남아있음 |
| 삭제 | DELETE 가능 | 불가 (retention 만료까지 유지) |
| Consumer 역할 | 읽고 수정/삭제 | 읽고 offset만 이동 |

### KafkaTemplate<?, ?>를 raw 타입으로 받는 이유

DLT에는 원본 메시지의 byte[]가 그대로 전송된다. `DeadLetterPublishingRecoverer`가 내부적으로 원본 `ConsumerRecord`를 사용하기 때문에 제네릭 타입이 아닌 와일드카드(`<?, ?>`)로 주입받는다.

### 토픽 자동생성 (NewTopic Bean)

`KafkaTopicConfig`에서 `NewTopic` 빈을 등록하면 **KafkaAdmin**이 애플리케이션 시작 시 자동으로 토픽을 생성한다. 이미 존재하는 토픽은 건드리지 않는다 (파티션 증가만 가능, 감소/삭제 불가). Infrastructure as Code 관점에서 토픽 설정이 코드에 있으므로 리뷰/버전관리가 가능하다.

### "블록킹"의 의미

재시도하는 동안 **해당 파티션의 다른 메시지가 처리되지 못한다.** Consumer 스레드가 BackOff 대기 + 재시도에 묶여 있기 때문이다. 이것이 C6(@RetryableTopic, 논블록킹 재시도)과의 핵심 차이다.

| | DefaultErrorHandler (C5) | @RetryableTopic (C6) |
|---|---|---|
| 재시도 위치 | Consumer 메모리 (in-memory) | 별도 재시도 토픽 |
| 토픽 메시지 수 | 원본 1건 + DLT 1건 | 원본 1건 + 재시도 토픽 N건 + DLT 1건 |
| 파티션 블록킹 | O (블록킹) | X (논블록킹) |
| 사용 시점 | 짧은 재시도, 순서 보장 필요 시 | 긴 재시도, 처리량 우선 시 |

---

## 핵심 학습 포인트

1. **DefaultErrorHandler @Bean** — 등록만 하면 모든 Listener Container에 자동 적용 (Spring Kafka 2.8+)
2. **블록킹 재시도** — 토픽을 거치지 않고 Consumer 메모리에서 같은 레코드를 재전달, 해당 파티션 처리 차단
3. **Kafka는 불변 로그** — Consumer 처리 실패해도 메시지는 토픽에 그대로, offset만 관리
4. **offset 커밋 시점** — 재시도 소진 후 DLT 전송 완료 시 ErrorHandler가 자동 커밋
5. **DLT 토픽 이름 규칙** — `{원본토픽}-dlt`, 파티션 -1은 자동 할당
6. **FixedBackOff(1000L, 2)** — 1초 간격, 최대 2회 재시도 (총 3회 시도 = 1 원본 + 2 재시도)
7. **NewTopic 빈** — KafkaAdmin이 시작 시 자동 생성, 이미 존재하면 무시

---

## Codex 교차 리뷰

| # | 심각도 | 이슈 | 영향 |
|---|--------|------|------|
| 1 | Medium | `getLastDltEvent()` null 체크 없이 바로 `getOrderId()` 호출 | 타임아웃 시 assertion 실패 대신 NPE로 깨져 원인 파악 어려움 |
