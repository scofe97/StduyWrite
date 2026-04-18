---
title: 05-outbox-poller-review
tags: []
status: draft
related: []
updated: 2026-04-19
---

# OutboxPoller 코드 리뷰
---
> redpanda-playground의 `OutboxPoller`는 Transactional Outbox 패턴의 Polling Publisher 구현체다. 이 문서는 순서 보장 결함과 트랜잭션 범위 문제를 중심으로 프로덕션 수준의 개선 방향을 정리한다.

## 1. 현재 구현 요약

`OutboxPoller`는 500ms 주기로 `outbox_event` 테이블의 PENDING 레코드를 최대 50건 조회하여 Kafka로 발행한다. 조회 SQL은 `ORDER BY created_at ... FOR UPDATE SKIP LOCKED`를 사용하므로, 다중 인스턴스 환경에서도 같은 레코드를 동시에 처리하지 않는다.

발행 성공 시 `markAsSent`로 상태를 SENT로 전이하고, 실패 시 `incrementRetryCount`로 재시도 횟수를 증가시킨다. `MAX_RETRIES`(5)를 초과하면 DEAD로 전이하여 poison event가 폴링을 점유하는 것을 방지한다. CloudEvents v1.0 헤더와 OpenTelemetry `traceparent`를 함께 전파하여 Tempo에서 HTTP → Outbox → Kafka 구간이 하나의 trace로 연결된다.

핵심 흐름을 요약하면 다음과 같다:

```
PENDING 조회(FOR UPDATE SKIP LOCKED)
  → trace context 복원
  → Kafka send(동기 5s 타임아웃)
  → markAsSent / incrementRetryCount / markAsDead
```

## 2. 순서 보장 문제 (Critical)

같은 `aggregate_id`의 이벤트가 여러 건 PENDING 상태일 때, 선행 이벤트가 실패하면 후행 이벤트가 먼저 Kafka에 적재된다. Consumer 입장에서는 `ORDER_CREATED` → `ORDER_PAID` 순서를 기대했지만 `ORDER_PAID`가 먼저 도착하는 상황이 발생한다.

### 2-1. 문제 시나리오

같은 aggregate의 이벤트 E1~E5가 `created_at` 순서로 조회된다고 가정하면 다음과 같은 흐름이 발생한다:

```
폴링 #1: E1(실패) → E2(성공) → E3(성공) → E4(성공) → E5(성공)
          ↓ incrementRetryCount  ↓ markAsSent (Kafka에 E2~E5 적재)

폴링 #2: E1(성공) → markAsSent
          ↓ Kafka에 E1 적재 — 하지만 이미 E2~E5 뒤에 위치
```

Kafka 파티션 내 메시지 순서가 `E2, E3, E4, E5, E1`이 된다. `aggregate_id`를 파티션 키로 사용하므로 같은 파티션에 들어가는 것은 보장되지만, 파티션 내 순서가 뒤집힌다.

### 2-2. 해결: aggregate 단위 stop-on-failure

같은 `aggregate_id`의 선행 이벤트가 실패하면 해당 aggregate의 후속 이벤트를 건너뛰는 방식이다. 실패한 이벤트는 다음 폴링에서 재시도되며, 그때 후속 이벤트도 함께 처리된다:

```java
Set<String> failedAggregates = new HashSet<>();
for (var event : events) {
    if (failedAggregates.contains(event.getAggregateId())) {
        continue; // 선행 이벤트가 실패한 aggregate는 skip
    }
    try {
        publishWithTraceContext(record, event);
        outboxMapper.markAsSent(event.getId());
    } catch (Exception e) {
        failedAggregates.add(event.getAggregateId());
        handleFailure(event);
    }
}
```

이 방식은 aggregate 간 독립성을 유지하면서도 aggregate 내 순서를 보장한다. 주문 A의 이벤트가 실패해도 주문 B의 이벤트는 정상 발행된다. 다만 실패한 aggregate의 이벤트가 다음 폴링까지 지연되므로, 폴링 주기(현재 500ms)가 해당 aggregate의 최대 지연 시간이 된다.

## 3. @Transactional 범위 문제 (Critical)

`pollAndPublish()` 메서드 전체가 `@Transactional`로 감싸져 있다. `FOR UPDATE SKIP LOCKED`로 잡은 row lock이 메서드가 끝날 때까지 유지되며, 중간에 예외가 발생하면 전체 트랜잭션이 롤백된다.

### 3-1. 문제 시나리오

E1~E50을 처리하는 중 E30에서 DB 예외가 발생하면 다음과 같은 상황이 벌어진다:

```
E1~E29: Kafka send 성공 (브로커에 메시지 적재 완료)
E30:    DB 예외 발생 → 전체 트랜잭션 롤백
결과:   E1~E29의 markAsSent가 롤백 → 다시 PENDING 상태
        다음 폴링에서 E1~E29 재전송 → Kafka에 중복 메시지
```

Kafka send는 외부 시스템 호출이므로 DB 트랜잭션 롤백과 무관하게 이미 적재된 메시지를 회수할 수 없다. 이것이 Outbox 패턴에서 트랜잭션 범위를 신중하게 설계해야 하는 이유다.

### 3-2. 해결: 이벤트별 트랜잭션 분리

`@Transactional`을 `pollAndPublish()`에서 제거하고, 개별 이벤트 처리를 별도 트랜잭션으로 분리한다. `TransactionTemplate`을 사용하면 같은 클래스 내에서도 트랜잭션 경계를 제어할 수 있다:

```java
// @Transactional 제거
@Scheduled(fixedDelay = 500)
public void pollAndPublish() {
    // 조회는 별도 트랜잭션 (FOR UPDATE SKIP LOCKED)
    var events = txTemplate.execute(status ->
            outboxMapper.findPendingEvents(50));
    if (events == null || events.isEmpty()) return;

    Set<String> failedAggregates = new HashSet<>();
    for (var event : events) {
        if (failedAggregates.contains(event.getAggregateId())) {
            continue;
        }
        try {
            publishWithTraceContext(buildRecord(event), event);
            // 발행 성공 후 개별 트랜잭션으로 상태 전이
            txTemplate.executeWithoutResult(status ->
                    outboxMapper.markAsSent(event.getId()));
        } catch (Exception e) {
            failedAggregates.add(event.getAggregateId());
            txTemplate.executeWithoutResult(status ->
                    handleFailure(event));
        }
    }
}
```

이 구조에서 E30이 실패해도 E1~E29의 `markAsSent`는 이미 개별 커밋되었으므로 롤백되지 않는다. `FOR UPDATE SKIP LOCKED`의 lock도 조회 트랜잭션이 끝나면 즉시 해제된다.

단, 이 방식에는 trade-off가 있다. Kafka send 성공 후 `markAsSent` DB 커밋이 실패하면 다음 폴링에서 해당 이벤트가 재전송된다. 따라서 Consumer 측 멱등성 처리가 반드시 필요하다. `ce_id` 헤더(현재 구현에 이미 포함)를 멱등성 키로 활용하는 것이 일반적이다.

## 4. 추가 프로덕션 고려사항

### 4-1. 재시도 백오프 없음 (P1)

실패한 이벤트가 500ms 후 즉시 재시도된다. Kafka 브로커 장애처럼 일시적 문제가 지속되는 경우, `MAX_RETRIES`(5)가 2.5초 만에 소진되어 복구 가능한 이벤트가 DEAD 처리될 수 있다.

`next_retry_at` 컬럼을 추가하고 지수 백오프(Exponential Backoff)를 적용하면 이 문제를 해결할 수 있다. 재시도 간격은 `1초 × 2^retryCount`로 설정하여 1초, 2초, 4초, 8초, 16초로 증가시킨다:

```sql
-- incrementRetryCount 수정
UPDATE outbox_event
SET retry_count = retry_count + 1
    , next_retry_at = NOW() + INTERVAL (POWER(2, retry_count)) SECOND
WHERE id = #{id}
```

```sql
-- findPendingEvents WHERE 조건 추가
WHERE status = 'PENDING'
  AND (next_retry_at IS NULL OR next_retry_at <= NOW())
ORDER BY created_at
```

### 4-2. 메트릭과 알림 없음 (P1)

PENDING 큐 깊이, 발행 성공/실패 횟수, DEAD 이벤트 발생을 모니터링할 수 없다. 문제가 발생해도 로그를 직접 확인하기 전까지는 인지할 수 없다는 뜻이다.

Micrometer Counter/Gauge를 추가하면 Grafana 대시보드와 알림 연동이 가능하다:

```java
private final Counter publishedCounter;
private final Counter failedCounter;
private final Counter deadCounter;
// AtomicInteger gauge로 PENDING 큐 깊이 노출
```

핵심 메트릭은 네 가지다:

- `outbox.events.published` — 발행 성공 카운터
- `outbox.events.failed` — 발행 실패 카운터
- `outbox.events.dead` — DEAD 전이 카운터
- `outbox.queue.pending` — PENDING 큐 깊이 게이지

### 4-3. 동기 블로킹과 배치 발행 (P2)

`kafkaTemplate.send(record).get(5, TimeUnit.SECONDS)`는 이벤트당 최대 5초를 블로킹한다. 50건 배치에서 전부 타임아웃이 발생하면 250초 동안 폴러가 멈추고, 그 사이 PENDING 이벤트가 계속 쌓인다.

Milan Jovanović의 Outbox 스케일링 사례(2B+ messages/day)에서는 순차 발행을 `Task.WhenAll` 기반 병렬 발행으로 전환하여 처리량을 크게 개선했다. Java에서는 `CompletableFuture.allOf()`로 동일한 패턴을 구현할 수 있다:

```java
// 병렬 발행 (aggregate 순서 보장이 불필요한 경우)
var futures = events.stream()
        .map(event -> kafkaTemplate.send(buildRecord(event)))
        .toList();
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
        .get(10, TimeUnit.SECONDS);
```

다만 이 방식은 같은 aggregate 내 순서를 보장하지 않는다. 2절의 stop-on-failure 패턴과 병렬 발행을 결합하려면, aggregate별로 그룹핑한 뒤 aggregate 내부는 순차, aggregate 간은 병렬로 처리해야 한다. 구현 복잡도가 높아지므로, 현재 규모에서는 동기 방식을 유지하면서 타임아웃만 2초로 줄이는 것이 현실적이다.

### 4-4. SENT 레코드 정리 미구현 (P2)

`OutboxMapper`에 `deleteOlderThan()` 메서드가 정의되어 있지만 이를 호출하는 스케줄러가 없다. SENT 상태의 레코드가 무한히 쌓이면 테이블 크기가 증가하고, `findPendingEvents`의 partial index 효율도 점차 떨어진다.

별도 `@Scheduled` 메서드로 일 1회 또는 시간 1회 정리 작업을 수행하면 된다. 보존 기간은 디버깅 용도를 고려하여 7일 정도가 적절하다.

### 4-5. 건별 UPDATE를 배치 UPDATE로 전환 (P2)

현재 구현은 이벤트마다 `markAsSent`를 개별 호출한다. 50건 배치라면 50회의 UPDATE 쿼리가 DB로 전송된다. Milan Jovanović의 스케일링 사례에서는 건별 UPDATE를 단일 배치 UPDATE로 전환하여 300ms → 52ms(82.6% 감소)를 달성했다.

MyBatis에서는 `<foreach>`를 활용한 배치 UPDATE로 구현할 수 있다:

```sql
UPDATE outbox_event
SET status = 'SENT', sent_at = NOW()
WHERE id IN
<foreach collection="ids" item="id" open="(" separator="," close=")">
    #{id}
</foreach>
```

성공한 이벤트 ID를 `List`로 모은 뒤 한 번의 UPDATE로 처리하면 DB 라운드트립이 대폭 줄어든다. 실패한 이벤트는 건수가 적으므로 건별 처리해도 무방하다.

### 4-6. 인덱스 최적화 (P3)

현재 `status = 'PENDING'` 조건의 partial index만 있다면, `ORDER BY created_at`은 filesort가 발생한다. Covered Index를 적용하면 테이블 접근 없이 인덱스만으로 쿼리를 처리할 수 있다. Milan Jovanović의 사례에서는 covered index 적용으로 조회 시간을 70ms → 1ms(98.5% 감소)로 줄였다.

PostgreSQL에서는 `INCLUDE` 절로 SELECT 대상 컬럼을 인덱스에 포함시킬 수 있다:

```sql
CREATE INDEX idx_outbox_pending_created
    ON outbox_event (created_at)
    INCLUDE (id, aggregate_type, aggregate_id, event_type, payload, topic, retry_count, correlation_id, trace_parent)
    WHERE status = 'PENDING';
```

`created_at`을 인덱스 키로 사용하면 `ORDER BY created_at`이 인덱스 스캔 순서와 일치하므로 별도 정렬이 불필요하다. `WHERE status = 'PENDING'` 필터는 partial index 조건으로 처리된다. 다만 `payload` 컬럼이 크면 PostgreSQL의 인덱스 행 크기 제한(2712B)에 걸릴 수 있으므로, 메시지 크기에 따라 `payload`를 INCLUDE에서 제외하는 것도 고려해야 한다.

PENDING 레코드가 수백 건 수준이면 성능 차이는 미미하지만, 장애 상황에서 PENDING이 수만 건으로 급증했을 때 차이가 드러난다.

## 5. 29CM 구현 사례와 비교

29CM은 22년 8월부터 상품 도메인 서비스에 트랜잭셔널 아웃박스 패턴을 적용하여 운영 중이다. 우리 구현과 아키텍처 접근이 다르기 때문에, 차이점을 비교하고 참고할 만한 설계 결정을 정리한다.

### 5-1. 아키텍처 차이: Polling Publisher vs TransactionalEventListener

우리 `OutboxPoller`는 순수 Polling Publisher 방식이다. `@Scheduled`로 주기적으로 PENDING 레코드를 조회하고 Kafka로 발행한다. 29CM은 Spring의 `ApplicationEventPublisher`와 `@TransactionalEventListener`를 조합한 이벤트 리스너 방식을 사용한다.

29CM의 흐름은 다음과 같다:

- 도메인 트랜잭션 내에서 `ApplicationEventPublisher.publishEvent()`로 이벤트 발행
- `@TransactionalEventListener(phase = BEFORE_COMMIT)` 리스너가 outbox 테이블에 이벤트 기록
- `@TransactionalEventListener(phase = AFTER_COMMIT)` + `@Async` 리스너가 Kafka로 메시지 전송
- Kafka 전송 실패 시 outbox 테이블의 미발행 레코드를 배치로 재시도

이 설계의 핵심은 "이벤트 발행 이후에 처리되는 모든 로직은 `TransactionalEventListener`에서 구현한다"는 일관성이다. 도메인 로직은 비즈니스 요구사항에만 집중하고, outbox 기록과 Kafka 전송은 리스너가 담당하므로 관심사 분리가 명확하다. 초기 설계에서는 도메인 트랜잭션 안에 outbox 기록을 직접 넣었지만, 리뷰 과정에서 `BEFORE_COMMIT` 리스너로 옮기는 것이 확장성과 응집성에 유리하다고 판단했다.

우리 구현은 `@Scheduled` 폴링만으로 동작하므로 리스너 방식보다 단순하다. 그러나 이벤트 발행 지연(최대 500ms)이 존재하고, 폴링 주기와 배치 크기의 튜닝이 필요하다는 trade-off가 있다. 29CM 방식은 트랜잭션 커밋 직후 즉시 Kafka 전송을 시도하므로 지연이 적지만, `@Async` 스레드 관리와 graceful shutdown 이슈가 추가로 발생한다.

### 5-2. 상태값 세분화: init / send_success / send_fail

우리 구현은 `PENDING` / `SENT` / `DEAD` 3단계 상태를 사용한다. 29CM은 `init` / `send_success` / `send_fail`로 구분하며, 실패 원인에 따라 상태가 달라진다.

구분이 중요한 이유는 배치 재시도 로직의 대상 선정 때문이다. Kafka 전송을 시도했으나 실패한 이벤트(`send_fail`)와 리스너가 이벤트를 아예 읽지 못한 이벤트(`init`)는 원인이 다르다. `send_fail`은 Kafka 브로커 장애나 네트워크 문제가 원인이고, `init`이 오래 남아 있다면 애플리케이션 배포 시 graceful shutdown이 제대로 동작하지 않았다는 신호다.

우리 구현에서도 `PENDING`이 오래 남는 경우가 Kafka 장애인지, 폴러 자체의 문제인지 구분할 수 없다. `PENDING`을 `INIT`과 `SEND_FAIL`로 분리하면 운영 시 문제 원인 파악이 빨라진다.

### 5-3. Graceful Shutdown 이슈

29CM은 `@Async`로 Kafka 전송을 처리하는데, `ThreadPoolTaskExecutor`에서 `setAwaitTerminationSeconds` 설정을 누락하여 배포 시 Pod가 rolling될 때 async 스레드가 즉시 종료되는 문제를 겪었다. 트랜잭션 커밋 후 리스너가 이벤트를 읽기 전에 프로세스가 종료되면, outbox 테이블에 `init` 상태로 남는 이벤트가 발생한다.

우리 구현은 `@Scheduled` + 동기 Kafka send 방식이므로 이 특정 문제는 발생하지 않는다. 하지만 폴링 중간에 Pod가 종료되면 진행 중인 이벤트의 상태 전이가 완료되지 않을 수 있다. `@Scheduled` 메서드도 Spring의 `TaskScheduler`가 관리하므로, graceful shutdown 설정이 올바르게 적용되어 있는지 확인이 필요하다.

### 5-4. 배치 재시도 기준

29CM의 재시도 배치는 "상태가 `send_success`가 아니면서 `created_at`이 현재 시간 기준 10분 이상 경과한 레코드"를 대상으로 한다. 이 기준은 정상 흐름에서 이벤트가 발행되는 시간(밀리초 단위)을 충분히 넘긴 시점에만 재시도를 시작한다는 의미다.

우리 구현은 500ms마다 PENDING 레코드를 즉시 재시도한다. 29CM의 10분 유예 방식과 비교하면 재시도가 지나치게 공격적이다. 4-1절의 지수 백오프와 함께, 최초 발행 시도와 배치 재시도의 시간 간격을 분리하는 것도 고려할 만하다.

## 6. 수정 우선순위 정리

아래 테이블은 영향도와 구현 난이도를 기준으로 우선순위를 정리한 것이다:

| 우선순위 | 이슈 | 영향 | 난이도 |
|---------|------|------|--------|
| P0 | aggregate 단위 stop-on-failure | 순서 보장 결함 → 비즈니스 로직 오류 | 낮음 |
| P0 | 이벤트별 트랜잭션 분리 | 롤백 시 중복 전송 → 데이터 불일치 | 중간 |
| P1 | 재시도 지수 백오프 | 일시적 장애에 DEAD 처리 과다 | 낮음 |
| P1 | Micrometer 메트릭 추가 | 장애 인지 불가 | 낮음 |
| P1 | 상태값 세분화 (INIT/SEND_FAIL 분리) | 장애 원인 구분 불가 | 낮음 |
| P2 | 동기 타임아웃 축소 (5s → 2s) | 장애 시 폴러 장시간 블로킹 | 낮음 |
| P2 | 배치 UPDATE (건별 → 일괄) | DB 라운드트립 과다 | 낮음 |
| P2 | SENT 레코드 정리 스케줄러 | 테이블 무한 증가 | 낮음 |
| P2 | graceful shutdown 설정 확인 | 배포 시 상태 전이 미완료 | 낮음 |
| P3 | Covered Index 최적화 | 대량 PENDING 시 조회 성능 저하 | 낮음 |

P0 두 건은 기능 정합성에 직결되므로 다음 구현 사이클에서 함께 수정하는 것이 바람직하다. P1은 프로덕션 배포 전 필수이며, P2~P3은 운영 안정화 단계에서 적용한다. 상태값 세분화는 29CM 사례에서 배포 시 `init` 상태 체류 문제를 실제로 겪은 후 도입한 설계이므로, 운영 전에 적용하는 것이 이상적이다.
