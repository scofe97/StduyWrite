# C7: Consumer Pause + C8: Circuit Breaker 리뷰

## 구현 요약

| 항목 | 내용 |
|------|------|
| 목적 | 미들웨어 장애 시 리밸런싱 폭풍을 방지하는 두 가지 패턴 |
| 파일 | `PausableConsumer.java`, `CircuitBreakerConsumer.java`, `ConsumerPauseTest.java`, `CircuitBreakerConsumerTest.java` |
| 테스트 | 3개 (pause/resume 동작, 정상 처리, Circuit OPEN 즉시 실패) |
| 의존성 | `resilience4j-circuitbreaker:2.2.0` 추가 |

---

## 왜 이렇게 구현했는가

### 문제: 미들웨어 장애 → 리밸런싱 폭풍

Kafka Consumer는 **단일 스레드**로 poll() → 처리를 반복한다. 외부 API가 30초 타임아웃이면 처리가 블록되어 `max.poll.interval.ms`(기본 5분)를 초과할 수 있다. 초과하면 브로커가 Consumer를 죽은 것으로 판단하고 **리밸런싱**을 발동한다.

```
Consumer A → 결제 API 다운 → 처리 블록 → 리밸런싱
Consumer B → 같은 파티션 재할당 → 같은 API → 블록 → 또 리밸런싱
Consumer C → 재할당 → 블록 → 또 리밸런싱...
→ 리밸런싱 폭풍 (Rebalance Storm)
```

리밸런싱은 **"Consumer가 문제"**일 때 유효하다. **"인프라가 문제"**일 때는 다른 Consumer로 재배정해도 같은 장애를 겪으므로 무의미하고, 오히려 악화된다.

### C7: Consumer Pause — 메시지 fetch 중단

`pause()`는 Kafka Client 레벨에서 **특정 파티션의 fetch를 중단**한다. poll()은 계속 호출되지만 빈 결과를 반환한다.

```
[pause 전] poll() → 500건 반환 → @KafkaListener 처리
[pause 후] poll() → 0건 반환 → @KafkaListener 호출 안 됨
            ↑ poll() 자체는 계속 → max.poll.interval.ms 초과 안 됨
            → 하트비트 유지, 파티션 소유권 유지, 리밸런싱 없음
```

| | pause() | stop() | 아무 대응 없음 |
|---|---------|--------|--------------|
| poll() 호출 | 계속 | 중단 | 블로킹 |
| 파티션 소유권 | **유지** | 반납 (리밸런싱) | 타임아웃 후 반납 |
| 복구 후 | resume() 즉시 재개 | start() + 리밸런싱 | 리밸런싱 대기 |
| 복구 속도 | **즉시** (밀리초) | 느림 | 느림 |

#### 특정 리스너만 pause하기

`@KafkaListener(id = "order-listener")`로 ID를 지정하면 `KafkaListenerEndpointRegistry`에서 해당 리스너만 제어할 수 있다. 결제 API가 다운되었다고 알림 Consumer까지 멈출 필요는 없다.

```java
MessageListenerContainer container = registry.getListenerContainer("pausable-listener");
container.pause();   // 이 리스너만 중단
// ... 복구 후
container.resume();  // 이 리스너만 재개
```

### C8: Circuit Breaker — 실패하는 호출 차단

Circuit Breaker가 OPEN 상태이면 **외부 서비스를 호출하지 않고 즉시 예외**를 던진다. 처리 시간이 밀리초 수준으로 줄어들어 poll() 간격을 유지한다.

```
[CLOSED]    정상 호출 → 성공/실패 기록
[OPEN]      즉시 CallNotPermittedException (0ms, 블로킹 없음)
[HALF_OPEN] 일부 요청으로 복구 확인 → 성공하면 CLOSED, 실패하면 다시 OPEN
```

#### 설정값의 의미

```java
CircuitBreakerConfig.custom()
    .failureRateThreshold(50)           // 실패율 50% 이상 → OPEN
    .slidingWindowSize(4)                // 최근 4건 기준으로 실패율 계산
    .minimumNumberOfCalls(4)             // 최소 4건 호출 후 판단 시작
    .waitDurationInOpenState(Duration.ofSeconds(5))  // OPEN 후 5초 대기 → HALF_OPEN
    .permittedNumberOfCallsInHalfOpenState(2)        // HALF_OPEN에서 2건 시도
    .build();
```

| 설정 | 값 | 의미 |
|------|-----|------|
| failureRateThreshold | 50 | 최근 4건 중 2건 이상 실패 → OPEN |
| slidingWindowSize | 4 | 판단 기준 윈도우 크기 |
| waitDurationInOpenState | 5초 | OPEN 유지 시간, 이후 HALF_OPEN |
| permittedNumberOfCallsInHalfOpenState | 2 | HALF_OPEN에서 시험 호출 수 |

### 실무 패턴: C7 + C8 연동

C7과 C8은 개별적으로도 유효하지만, **연동하면 가장 효과적**이다. Circuit Breaker 상태 전이 이벤트를 감지하여 자동으로 Consumer를 pause/resume한다.

```java
@PostConstruct
public void init() {
    CircuitBreaker cb = cbRegistry.circuitBreaker("payment");
    cb.getEventPublisher()
        .onStateTransition(event -> {
            switch (event.getStateTransition()) {
                case CLOSED_TO_OPEN, HALF_OPEN_TO_OPEN -> pauseAll();
                case OPEN_TO_HALF_OPEN, HALF_OPEN_TO_CLOSED -> resumeAll();
            }
        });
}
```

**연동 효과**:
- OPEN → pause: 메시지를 가져오지 않으므로 실패 건수도 쌓이지 않음
- HALF_OPEN → resume: 소량의 메시지로 복구 확인
- CLOSED → 정상 처리 재개

### C5/C6과의 관계

| 패턴 | 목적 | 재시도 위치 | 적합한 장애 |
|------|------|-----------|------------|
| C5 (DefaultErrorHandler) | 블록킹 재시도 + DLT | Consumer 메모리 | 일시적 오류 |
| C6 (@RetryableTopic) | 논블록킹 재시도 + DLT | 별도 토픽 | 일시적 오류, 처리량 유지 |
| C7 (Consumer Pause) | 메시지 fetch 중단 | - | **인프라 장애** |
| C8 (Circuit Breaker) | 즉시 실패 | - | **외부 서비스 장애** |

C5/C6은 **메시지 레벨** 에러 처리, C7/C8은 **인프라 레벨** 장애 대응이다.

---

## 교차 검증 리뷰 (Claude + Codex)

코드 작성 후 Codex(GPT-5.3)로 교차 검증을 수행했다. Claude가 놓친 맹점을 Codex가 발견하는 Dual-Agent 패턴이다.

### 발견된 이슈 및 수정

| # | 심각도 | 이슈 | 수정 |
|---|--------|------|------|
| 1 | **High** | `catch(Exception)` + 무조건 `ack.acknowledge()` → 실패 메시지 영구 유실 + 오류 은닉 | `CallNotPermittedException`과 `RuntimeException`을 분리 catch. OPEN 상태에서는 ack하지 않음 |
| 2 | **Medium** | `reset()`에서 latch 교체 시 listener thread와 경합 가능 | `CountDownLatch` 필드에 `volatile` 추가 |
| 3 | **Medium** | `Thread.sleep(2000)`으로 pause 적용 대기 → CI에서 flaky | `Awaitility` + `isContainerPaused()` 조건 기반 대기로 교체 |
| 4 | **Medium** | CB 테스트 단언이 약함 (`openCount > 0`만 확인) | `failureCount == 6`, `successCount == 0` 단언 추가 |

### CallNotPermittedException 분리의 의미

수정 전:
```java
catch (Exception e) {
    // 모든 예외를 같은 경로로 처리 — 코드 버그도 "실패 카운트"로 소비됨
    failureCount.incrementAndGet();
    if (circuitBreaker.getState() == OPEN) { ... }
}
ack.acknowledge();  // 성공/실패 무관하게 항상 커밋
```

수정 후:
```java
catch (CallNotPermittedException e) {
    // Circuit OPEN 때문에 차단된 것이 확실 — 외부 서비스를 호출하지 않았음
    circuitOpenCount.incrementAndGet();
    // ack하지 않음 → 복구 후 재처리 가능
} catch (RuntimeException e) {
    // 외부 서비스 호출은 했지만 실패 (CLOSED/HALF_OPEN 상태)
    ack.acknowledge();  // 실무에서는 C5/C6 재시도 전략과 병행
}
```

**왜 분리하는가?**
- `CallNotPermittedException`은 Circuit이 OPEN일 때만 발생 → **확실히** 외부 서비스를 호출하지 않은 것
- 일반 `RuntimeException`은 서비스를 호출했지만 실패한 것 → 원인이 다양 (타임아웃, 5xx, 코드 버그)
- 예외 타입으로 장애 원인을 분류할 수 있어야 모니터링과 알림이 의미를 갖는다

### Claude vs Codex 비교

| 포인트 | Claude | Codex |
|--------|--------|-------|
| CallNotPermittedException 분리 | 지적 | 지적 (간접) |
| HALF_OPEN 복구 테스트 부재 | 지적 | 지적 |
| Thread.sleep flaky | 지적 | 지적 |
| **ack 무조건 호출 위험** | 언급만 | **High로 강조** |
| **catch(Exception) 오류 은닉** | 미지적 | **High로 지적** |
| **테스트 단언 강화** | 미지적 | Medium으로 지적 |

> 하나의 AI가 생성한 코드는 그 AI의 맹점을 포함한다. 독립적인 다른 AI에게 검증을 받으면 이 맹점을 보완할 수 있다.

---

## 핵심 학습 포인트

1. **리밸런싱 폭풍** — 인프라 장애 시 리밸런싱은 무의미, 오히려 악화
2. **pause() ≠ stop()** — pause는 poll() 유지 + 파티션 소유권 유지, stop은 반납
3. **Circuit OPEN = 즉시 실패** — 블로킹 제거로 poll() 간격 유지
4. **C7 + C8 연동** — Circuit 상태 전이에 따라 자동 pause/resume이 실무 패턴
5. **리스너 ID로 세밀한 제어** — 장애 영향 범위만 pause, 나머지는 정상 운영
6. **C5/C6 = 메시지 에러, C7/C8 = 인프라 장애** — 레벨이 다르므로 병행 사용
