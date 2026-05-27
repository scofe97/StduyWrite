# 19. Production Case Studies

국내 IT기업의 Kafka 프로덕션 설정 사례 (2025~2026)

---

한국의 주요 IT기업들은 Kafka를 대규모 프로덕션 환경에서 운영하고 있습니다. 각 기업의 공개된 기술 블로그와 컨퍼런스 발표를 바탕으로, 실제 프로덕션에서 어떤 설정과 전략을 사용하는지 정리합니다.

## 토스 (Toss) - 금융 도메인

토스는 금융 서비스 특성상 데이터 무결성과 고가용성이 최우선입니다.

**클러스터 아키텍처:**
- Active-Active 데이터센터 이중화 구성
- 양방향 데이터 미러링 (커스텀 Kafka Connect Sink Connector)
- 1,000개 이상 토픽 미러링 운영
- Kubernetes 기반 배포

**토스증권 시세 파이프라인 (이중 Producer 전략):**

```yaml
# 속도 우선 Producer (실시간 시세)
spring:
  kafka:
    producer:
      acks: 0                          # ACK 대기 없이 즉시 전송
      # 실시간 시세는 밀리초 단위 지연이 중요
      # 데이터 유실 시 다음 시세로 대체 가능

# 안전 우선 Producer (거래 데이터)
spring:
  kafka:
    producer:
      acks: all                        # 모든 ISR 복제 확인
      properties:
        enable.idempotence: true       # 중복 방지
      # 거래 데이터는 절대 유실 불가
```

이 패턴은 금융 도메인에서 자주 사용됩니다. 시세처럼 연속적으로 갱신되는 데이터는 일부 유실이 허용되지만(`acks=0`), 주문/거래 데이터는 한 건도 유실되면 안 됩니다(`acks=all` + 멱등성).

**미러링 무한 루프 방지:**
- 메시지 헤더에 Source DC 정보를 추가하여 미러링 데이터 구분
- 헤더에 Source DC 정보가 있으면 재전송 차단
- DLQ(Dead Letter Queue)로 미러링 실패 메시지를 별도 보관 후 재처리

**모니터링:**
- 커스텀 메트릭 리포터로 Kafka 메트릭을 ClickHouse(OLAP DB)에 저장
- ms 단위 지연 시간 측정
- 메시지 인입 건수 트렌드 기반 이상징후 조기 발견

## 우아한형제들 (배달의민족) - 이커머스/배달 도메인

배달의민족은 Kafka를 이벤트 기반 마이크로서비스 통신의 핵심으로 사용합니다.

**아키텍처 특징:**
- 도메인별 토픽 분리 (주문, 배달, 결제 등)
- Consumer Group 기반 독립적 처리
- Kafka를 기반으로 한 이벤트 드리븐 아키텍처 전면 도입

## LINE - 글로벌 메시징 도메인

LINE은 세계 최대 규모의 단일 Kafka 클러스터를 운영합니다.

**규모:**
- 일일 2,500억 건 이상 레코드
- 일일 210TB 데이터
- 초당 최대 4GB 입력
- 50여 개 서비스가 단일 클러스터에 의존

**멀티 테넌시 전략:**
- 단일 클러스터로 운영하여 데이터 디스커버리와 아키텍처를 단순화
- **요청 쿼터(Request Quota)**: 클라이언트별 브로커 스레드 시간을 제한하여 과부하 방지
- 메시지 헤더 기반 클라이언트 식별로 빠른 문제 해결
- 작업 부하 격리로 한 클라이언트의 성능 저하가 다른 클라이언트에 영향 없음

## 사람인 (Saramin) - 채용/HR 도메인

사람인은 메일 시스템 MSA 전환 과정에서 Kafka 도입 시 발생한 실전 문제와 해결 사례를 공유했습니다.

**문제: 메시지 중복 소비 + LAG 증가**

근본 원인은 DB 쿼리가 1분 30초~2분 소요되는데, `max.poll.records`가 기본값 500으로 설정되어 `max.poll.interval.ms`(5분) 내에 처리를 완료하지 못해 리밸런스가 반복된 것입니다.

```yaml
# ❌ 기본 설정으로 인한 문제
spring:
  kafka:
    consumer:
      properties:
        max.poll.interval.ms: 300000    # 5분
        max.poll.records: 500           # 500개 × 2분 = 1000분 필요 → 타임아웃!

# ✅ 해결: 처리 시간에 맞춘 설정 조정
spring:
  kafka:
    consumer:
      properties:
        max.poll.interval.ms: 600000    # 10분으로 확대
        max.poll.records: 2             # 2개 × 2분 = 4분 → 타임아웃 내 완료
```

이 사례는 Kafka 설정을 기본값 그대로 사용하면 안 된다는 것을 보여줍니다. 비즈니스 로직의 처리 시간을 측정하고, 그에 맞게 `max.poll.records`와 `max.poll.interval.ms`를 조정해야 합니다.

## 부하 테스트 사례: RPS 1000에서의 Producer 지연 분석

> 출처: [Kafka Producer/Consumer 지연 문제 분석 및 해결 - RPS 1000 부하 테스트](https://velog.io/@dw_db/Kafka-ProducerConsumer-%EC%A7%80%EC%97%B0-%EB%AC%B8%EC%A0%9C-%EB%B6%84%EC%84%9D-%EB%B0%8F-%ED%95%B4%EA%B2%B0-RPS-1000-%EB%B6%80%ED%95%98-%ED%85%8C%EC%8A%A4%ED%8A%B8)

좋아요/취소(like/unlike) 기능에 Kafka를 적용한 서비스에서, RPS 500에서는 정상이던 시스템이 RPS 1000에서 Producer timeout이 발생한 사례다.

**문제 현상:**

| 지표 | RPS 500 | RPS 1000 | 변화 |
|------|---------|----------|------|
| p95 응답시간 | 7.95ms | 61.2ms | 7.7배 |
| Kafka Producer 지연 | 200~300ms | 2,000~9,000ms | 최대 30배 |
| Consumer lag | 0 | 0 | 정상 |

핵심은 **Consumer lag = 0인데도 Producer에서 TimeoutException이 발생**했다는 점이다. Broker와 Consumer는 정상이고, Producer 내부의 RecordAccumulator → Sender 구간이 병목이었다.

**원인: Hot Key + max.in.flight=1의 조합**

articleId를 Kafka 메시지 key로 사용하여 파티션 순서를 보장하고 있었다. 한 article에 요청이 집중되면(hot key), 해당 key의 메시지는 모두 같은 파티션으로 라우팅된다. `max.in.flight.requests.per.connection=1` 설정 때문에 이전 배치의 ACK를 받아야 다음 배치를 전송할 수 있어, ACK 지연이 누적되면 뒤에 쌓인 배치가 `delivery.timeout.ms`를 초과하여 expire된다.

**시도한 해결책과 결과:**

| 시도 | 내용 | 결과 |
|------|------|------|
| Consumer 병렬화 (파티션 3개, key 유지) | 같은 key는 같은 파티션 → 3개 중 1개만 작동 | 실패 |
| Key 제거 (라운드 로빈) | 3개 Consumer 병렬 처리 성공 | 순서 보장 깨짐 + DB unique 제약 위반 |
| Broker I/O 스레드 확장 | network=8, io=16 | 소폭 개선, timeout 지속 |
| Producer 배치 튜닝 | linger=5ms, batch=128KB, buffer=512MB | p95 개선, 일부 timeout 잔존 |

**핵심 교훈: 순서 보장 ↔ 병렬성 트레이드오프**

1. **Key 기반 파티셔닝의 한계**: 단일 key에 부하가 집중되면 파티션 수를 늘려도 병렬화가 불가능하다. 같은 key는 항상 같은 파티션으로 라우팅되기 때문이다.
2. **Key를 제거하면 병렬화는 가능하지만 순서 보장이 깨진다**: like/unlike가 서로 다른 Consumer에서 동시 처리되어 DB unique 제약 위반이 발생했다.
3. **Consumer lag = 0이 "정상"을 의미하지 않는다**: 메시지 소비와 메시지 전송은 독립적인 문제다. Producer 내부 큐 적체는 Consumer 지표로 발견할 수 없다.
4. **`max.in.flight=1`은 순서를 완벽히 보장하지만 처리량의 상한이 낮다**: 멱등성(`enable.idempotence=true`)이 켜져 있으면 `max.in.flight=5`까지도 순서가 보장되므로, 1로 고정할 필요가 없다.

**Producer 지연 진단 PromQL 예시:**

```promql
# Consumer 처리속도 (ms 단위)
(rate(spring_kafka_listener_seconds_sum[1m]) /
 rate(spring_kafka_listener_seconds_count[1m])) * 1000
```

이 사례는 사람인 사례(Consumer 측 `max.poll.records` 튜닝)와 대비된다. 사람인은 Consumer 처리 시간이 병목이었고, 이 사례는 Producer 내부 배치 전송이 병목이었다. 같은 "지연"이라도 원인 지점이 다르므로, **Consumer lag, Producer 큐 깊이, Broker 응답 시간을 구분하여 모니터링**하는 것이 중요하다.

---

## 교통 알림 시스템: Redis Sorted Set + Kafka 아키텍처

> 출처: [교통 이슈 알림 시스템 개선기 - Redis Sorted Set과 Kafka로 설계 바꾸기](https://velog.io/@mw310/교통-이슈-알림-시스템-개선기-Redis-Sorted-Set과-Kafka로-설계-바꾸기)

"가는길 지금" 프로젝트에서 크롤링 기반 알림을 Redis Sorted Set + Kafka 아키텍처로 전환한 사례입니다.

**기존 문제**: 크롤링 시점에 알림 발송 여부를 판단 → 미래 이슈(예정된 공사) 누락, 크롤링 주기에 종속

**개선 아키텍처**:

```
크롤러 → Redis Sorted Set(score=이슈시작시각) → 스케줄러(ZRANGEBYSCORE)
  → Kafka Topic → Consumer(DB 조회 → 대상자 필터링) → FCM 발송
  → 실패 시 DLT → Slack 알림
```

**Redis Sorted Set 핵심 — 시간 기반 스케줄링**:

```java
// 저장: 이슈 ID만 저장 (score = Unix Timestamp)
redisTemplate.opsForZSet().add("pending_notifications", issueId, startTimestamp);

// 조회: 현재 시각까지 발송해야 할 모든 이슈 (O(log N + M))
Set<String> dueIds = redisTemplate.opsForZSet()
    .rangeByScore("pending_notifications", 0, System.currentTimeMillis());
```

**"이슈 ID만 저장"하는 설계 이유**:

| 비교 | 메시지 미리 생성 | ID만 저장 |
|------|:-------------:|:--------:|
| 메모리 | 사용자 수 x 이슈 수 (폭발) | 이슈 수만 (최소) |
| 내용 수정 | 수만 개 메시지 수정 | DB 원본 1개만 수정 |
| 알림 취소 | 수만 개 키 삭제 | ZREM 한 번 |
| 사용자 정보 | 저장 시점(stale) | 발송 시점(최신) |

**Kafka의 역할 — 트래픽 버퍼 + 장애 격리**:

- 스케줄러는 Kafka에만 발행(즉시 반환) → 시간 체크 본연의 역할에 집중
- 이슈 1,000개 동시 발생 시 Kafka가 순차 저장 → Consumer가 자신의 속도로 소비 (backpressure)
- FCM 장애 시 메시지는 Kafka에 보존 → 복구 후 이어서 처리

**핵심 교훈**: Redis(빠른 스케줄링) + Kafka(신뢰성 버퍼) + DB(영속성) 삼각형 구조. 각 기술의 강점만 활용하여 역할을 분담한다.

---

## 컬리 SCM — Kafka Streams Tumbling Window (재고 정산)

> 출처: [컬리 SCM팀의 Kafka Streams 윈도우 도입기](https://helloworld.kurly.com/blog/2025-kafka-streams-window/)

컬리 SCM팀은 배치 기반 재고 정산을 이벤트 기반으로 전환하면서, 5분 단위 원천 데이터를 상품코드 기준으로 집계해야 했다. 스파이크성 데이터는 윈도우 집계로, 비스파이크 데이터는 즉시 반영하는 하이브리드 전략을 택했다.

> **Kafka Streams 윈도우 기초**: [01-stream-processing.md §5](../../09-kafka-streams/01-stream-processing.md), [23-kafka-streams-spring-boot.md §6](./23-kafka-streams-spring-boot.md) 참조

### 이벤트 시간 vs 스트림 시간 vs 벽시계 시간

Kafka Streams의 시간 모델은 세 가지이며, 이 구분이 윈도우 동작을 이해하는 핵심이다.

| 시간 유형 | 정의 | 결정 주체 |
|----------|------|----------|
| **이벤트 시간 (Event Time)** | 데이터가 실제로 생성된 시간 | Producer가 레코드에 내장 |
| **스트림 시간 (Stream Time)** | Kafka Streams가 인식하는 "현재" 시간. 처리한 레코드 중 가장 큰 타임스탬프 | Streams 프레임워크가 자동 관리 |
| **벽시계 시간 (Wall Clock Time)** | 시스템의 실제 시계 (`System.currentTimeMillis()`) | OS |

**핵심 함정**: 윈도우 종료 ≠ 결과 발행. 윈도우 시간이 끝나도 스트림 시간이 전진해야 윈도우가 닫힌다. 스트림 시간은 **새 이벤트가 도착해야만** 전진하므로, 이벤트가 없으면 시간이 멈춘다.

스트림 시간은 **파티션별로 독립 관리**된다. 모든 입력 파티션에 새 데이터가 있어야 전체 스트림 시간이 전진한다. 하나라도 데이터가 없으면 스트림 시간이 멈추고, `STREAM_TIME` 기반 Punctuator도 호출되지 않는다.

### TimestampExtractor — 시간 기준 재정의

Kafka 레코드에는 기본적으로 **발행 시간(CreateTime)** 이 타임스탬프로 기록된다. 하지만 데이터 생성 시간과 Kafka 발행 시간이 다를 수 있다 (예: 23:59에 생성된 데이터가 00:00에 발행되면 다른 윈도우에 할당됨).

| 구현 | 동작 | 사용 시점 |
|------|------|----------|
| `FailOnInvalidTimestamp` (기본값) | ConsumerRecord의 타임스탬프 사용, 유효하지 않으면 예외 | 대부분의 경우 |
| `LogAndSkipOnInvalidTimestamp` | 유효하지 않은 타임스탬프 skip + 로그 | 불완전한 데이터 허용 시 |
| `UsePartitionTimeOnInvalidTimestamp` | 유효하지 않으면 파티션 시간 사용 | fallback 필요 시 |
| `WallclockTimestampExtractor` | `System.currentTimeMillis()` 사용 | Processing-time 의미론 |
| **커스텀 구현** | 레코드 payload에서 시간 추출 | **컬리의 선택** |

```java
// 컬리의 커스텀 TimestampExtractor
public class EventTimeExtractor implements TimestampExtractor {
    @Override
    public long extract(ConsumerRecord<Object, Object> record, long partitionTime) {
        MyEvent event = (MyEvent) record.value();
        // Kafka 발행 시간(CreateTime) 대신 비즈니스 이벤트 생성 시간 사용
        return event.getCreatedAt().toInstant().toEpochMilli();
    }
}
```

`extract()` 메서드는 ConsumerRecord에서 value를 꺼내 비즈니스 객체로 캐스팅한 뒤, 해당 객체의 `createdAt` 필드를 epoch millis로 변환하여 반환한다. Kafka Streams는 이 시간을 기준으로 윈도우를 할당한다. `partitionTime`은 해당 파티션에서 이전에 처리된 레코드의 타임스탬프로, 커스텀 로직에서 fallback으로 사용할 수 있다.

### Suppress API — 최종 결과만 발행

윈도우 집계 시 기본 동작은 레코드가 도착할 때마다 **중간 결과를 계속 발행**하는 것이다. 정산처럼 "최종 결과 1회만" 필요한 경우 `suppress()`를 사용한다.

```java
.suppress(Suppressed.untilWindowCloses(
    Suppressed.BufferConfig.unbounded()))
```

**Suppress 동작 원리 (KIP-328)**:
1. 윈도우가 열려있는 동안 모든 중간 결과를 내부 버퍼에 보관
2. 윈도우가 닫히면 (스트림 시간 > 윈도우 종료 + grace period) 최종 결과 1건만 발행
3. 이후 동일 윈도우에 대한 추가 발행 없음 → **exactly-once 결과** 보장

| BufferConfig 옵션 | 동작 | 위험 |
|-------------------|------|------|
| `unbounded()` | 메모리 제한 없음 | OOM 가능 (컬리 선택) |
| `maxBytes(n).shutDownWhenFull()` | n바이트 초과 시 graceful shutdown | 데이터 유실 없지만 서비스 중단 |
| `maxBytes(n).spillToDiskWhenFull()` | 디스크 스필오버 | I/O 성능 저하 |

### Grace Period — 지각 이벤트 허용

```java
TimeWindows.ofSizeAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1))
```

Grace period는 "윈도우 종료 후 추가로 얼마나 기다릴 것인가"를 정의한다. 네트워크 지연이나 처리 순서 차이로 늦게 도착하는 이벤트를 수용하는 완충 시간이다.

- KIP-633 이전: 기본 grace period가 24시간이었음 (대부분 과도)
- KIP-633 이후: 명시적으로 지정하도록 변경 (`ofSizeWithNoGrace`, `ofSizeAndGrace`)
- Grace period 초과 이벤트는 **완전히 드롭** (로그도 남지 않음)

### 이벤트 부재 시 윈도우 미발행 문제와 해결

**문제**: 새벽 시간대처럼 이벤트가 없으면 스트림 시간이 멈추고, 이전 윈도우가 영원히 닫히지 않는다.

**삽질 기록:**

| 시도 | 방법 | 결과 | 원인 |
|------|------|------|------|
| 1 | Processor 내부 `context.forward()` | ❌ 실패 | 내부 전파일 뿐, 스트림 시간 갱신 불가 |
| 2 | WindowStore 직접 스캔 + 수동 발행 | ❌ 실패 | Streams 내부 상태와 충돌 → 중복 발행 |
| 3 | **외부 더미 이벤트 발행** | ✅ 성공 | 스트림 시간이 실제로 전진 |

**최종 해결: WindowClosingProcessor + PunctuationType.WALL_CLOCK_TIME**

```java
public class WindowClosingProcessor
    implements Processor<String, InventoryTransactionDto, String, InventoryTransactionDto> {

    @Override
    public void init(ProcessorContext<String, InventoryTransactionDto> context) {
        // WALL_CLOCK_TIME: 벽시계 기반이므로 이벤트 없이도 트리거됨
        context.schedule(Duration.ofMinutes(3), PunctuationType.WALL_CLOCK_TIME, timestamp -> {
            emitWindowedData();
            context.commit();
        });
    }

    private void emitWindowedData() {
        // 핵심: Kafka Producer로 외부에서 소스 토픽에 더미 이벤트 발행
        // → Streams가 이를 소비하면서 스트림 시간이 전진
        // → 과거 윈도우가 닫히고 suppress된 최종 결과가 발행됨
        String topicKey = "dummy-key-" + context.taskId().partition();
        kafkaProducer.publishMessageAsObject(
            toTopic,
            topicKey,
            InventoryTransactionDto.emit(),  // 더미 이벤트 (다운스트림에서 필터링)
            context.taskId().partition()       // 파티션 직접 지정 (핵심!)
        );
    }
}
```

- `PunctuationType.WALL_CLOCK_TIME`: 벽시계 기반 스케줄링이므로 이벤트가 없어도 3분마다 트리거된다. `STREAM_TIME`이었다면 이벤트가 없으면 영원히 호출되지 않는다.
- `context.taskId().partition()`: 스트림 시간은 파티션별로 독립이므로, 모든 파티션에 더미 이벤트를 보내야 한다. 키가 같으면 해싱에 의해 하나의 파티션으로만 가므로, 파티션 번호를 직접 지정하거나 파티션별 고유 키를 사용한다.
- `InventoryTransactionDto.emit()`: 더미 이벤트를 식별할 수 있는 팩토리 메서드. 다운스트림에서 이 마커를 확인하여 더미는 무시한다.

### 전체 토폴로지

```java
@Autowired
public void shipmentStreams(StreamsBuilder streamsBuilder) {
    KStream<String, InventoryTransactionDto> stream =
        streamsBuilder.stream(sourceTopic,
            Consumed.with(STRING_SERDE, TRANSACTION_DTO_SERDE));

    stream
        .groupByKey(Grouped.with(STRING_SERDE, TRANSACTION_DTO_SERDE))   // 상품코드 기준 그룹화
        .windowedBy(TimeWindows.ofSizeAndGrace(
            Duration.ofMinutes(5), Duration.ofMinutes(1)))               // 5분 텀블링 + 1분 유예
        .reduce(this::aggregateTransactions)                             // 같은 윈도우 내 수량 합산
        .suppress(Suppressed.untilWindowCloses(
            Suppressed.BufferConfig.unbounded()))                        // 최종 결과만 발행
        .toStream()
        .map((key, value) -> KeyValue.pair(key.key(), value))            // Windowed<String> → String
        .to(toTopic, Produced.with(STRING_SERDE, TRANSACTION_DTO_SERDE));
}
```

### 실전 교훈

1. **"Kafka Streams는 이벤트를 통해서만 시간이 흐른다"** — 이 원리를 모르면 윈도우가 닫히지 않는 버그를 만난다
2. **경계 시점(자정) 처리**: TimestampExtractor로 이벤트 시간을 정확히 추출해야 윈도우 할당 오류 방지
3. **테스트 어려움**: 시간 기반 검증이라 한 번 확인에 수 분 소요 → TopologyTestDriver 적극 활용

---

## 컬리 데이터서비스 — JDBC Source Connector 데이터 파이프라인

JDBC Source Connector의 4가지 쿼리 모드(Bulk/Incrementing/Timestamp/Timestamp+Incrementing)와 각 모드의 한계, 특히 장거리 트랜잭션으로 인한 데이터 영구 누락 문제를 분석한 사례. `timestamp.delay.interval.ms`를 활용한 방어 전략과 CDC(Debezium)와의 트레이드오프를 다룬다.

> **상세**: [20-jdbc-source-pipeline.md](./20-jdbc-source-pipeline.md)

---

## 쿠팡 주문팀 — 무중단 Consumer Offset Seeking

> 출처: [쿠팡 주문팀의 Spring Kafka Consumer Offset Seeking](https://helloworld.kurly.com/blog/2024-spring-kafka-consumer-offset-seeking/)

프로덕션에서 특정 시점으로 오프셋을 되돌려야 할 때, Kafka CLI는 컨슈머 그룹이 **비활성 상태**여야만 동작한다. 쿠팡 주문팀은 Spring Kafka의 `ConsumerSeekAware`를 활용하여 **컨슈머 실행 중에** 무중단으로 오프셋을 이동하는 방법을 구현했다.

> **수동 커밋 기초**: [04-manual-commit-deep-dive.md](./04-manual-commit-deep-dive.md) 참조

### 문제 정의

```bash
kafka-consumer-groups.sh --reset-offsets --group my-group \
  --to-datetime 2024-11-23T18:47:14 --execute
# Error: "In order to succeed, the group must be empty"
```

프로덕션에서 이것이 문제인 이유:
- 컨슈머 전체 중지 → 해당 시간 동안 **메시지 처리 중단**
- 그룹 내 다른 토픽의 컨슈머까지 영향
- Kafka 관리 팀 권한 의존

### 3가지 대안 분석

| 대안 | 방법 | 한계 |
|------|------|------|
| Kafka 클러스터 권한 획득 | 직접 CLI 실행 | 여전히 **컨슈머 중지 필수** |
| AdminClient API (`alterConsumerGroupOffsets`) | Java API로 오프셋 변경 | 내부적으로 그룹이 **Empty 상태**일 때만 동작 |
| **ConsumerSeekAware** (최종 선택) | 폴링 루프 내에서 seek 수행 | 없음 — **무중단 달성** |

### ConsumerSeekAware 인터페이스

```java
public interface ConsumerSeekAware {
    // 파티션 할당 시 호출 — 콜백을 등록
    void registerSeekCallback(ConsumerSeekCallback callback);

    // 파티션이 할당될 때 호출 — 여기서 초기 오프셋 조정 가능
    void onPartitionsAssigned(Map<TopicPartition, Long> assignments,
                              ConsumerSeekCallback callback);

    // 파티션 해제 시 콜백 정리
    void unregisterSeekCallback(ConsumerSeekCallback callback);
}
```

**ConsumerSeekCallback 메서드들:**

| 메서드 | 동작 |
|--------|------|
| `seek(topic, partition, offset)` | 특정 오프셋으로 이동 |
| `seekToBeginning(topic, partition)` | 가장 처음으로 이동 |
| `seekToEnd(topic, partition)` | 가장 마지막으로 이동 |
| `seekRelative(topic, partition, offset, toCurrent)` | 현재/시작 기준 상대 이동 |
| `seekToTimestamp(topic, partition, timestamp)` | 특정 시간 이후 첫 오프셋으로 이동 |

### AbstractConsumerSeekAware 구현

Spring Kafka 2.3+에서 제공하는 추상 클래스로, 콜백 관리를 자동화한다.

```java
@Component
public class SeekableListener extends AbstractConsumerSeekAware {

    @KafkaListener(topics = "my-topic", groupId = "my-group")
    public void listen(String message) {
        // 비즈니스 로직
    }

    // 외부에서 호출 가능한 오프셋 이동 메서드
    public void seekToEarliest() {
        this.getTopicsAndCallbacks()
            .forEach((topicPartition, callbacks) -> {
                callbacks.forEach(cb -> cb.seekToBeginning(
                    topicPartition.topic(),
                    topicPartition.partition()
                ));
            });
    }

    public void seekToTimestamp(long timestamp) {
        this.getTopicsAndCallbacks()
            .forEach((topicPartition, callbacks) -> {
                callbacks.forEach(cb -> cb.seekToTimestamp(
                    topicPartition.topic(),
                    topicPartition.partition(),
                    timestamp
                ));
            });
    }
}
```

- `AbstractConsumerSeekAware`가 `registerSeekCallback`/`unregisterSeekCallback`를 자동 구현
- `getTopicsAndCallbacks()`는 현재 이 리스너에 할당된 `TopicPartition → ConsumerSeekCallback` 맵 반환
- 콜백의 seek은 다음 `poll()` 호출 전에 적용됨 — 현재 처리 중인 배치에는 영향 없음
- Spring Kafka 3.3+: `getGroupId()` 메서드 추가로 다중 컨슈머 그룹 구분 가능

### 분산 환경 확장: HTTP API + Redis Pub/Sub

단일 서버에서는 위 코드로 충분하지만, **여러 서버에 분산된 컨슈머 그룹**에 동시 적용이 필요하다.

```
[사용자] → POST /consumers/seek (한 서버에 도달)
              ↓
         [Redis Pub/Sub 발행] → "seek-commands" 채널
              ↓         ↓         ↓
         [서버 A]   [서버 B]   [서버 C]
         (리스너)   (리스너)   (리스너)
              ↓         ↓         ↓
         seekTo...  seekTo...  seekTo...
```

**HTTP 엔드포인트:**
```json
POST /consumers/seek
{
  "topics": ["my-topic"],
  "partitions": [0, 1, 2],
  "seekAt": "2024-11-23T18:47:14"
}
```

**분산 전파 대안:**

| 방식 | 장점 | 단점 |
|------|------|------|
| **Redis Pub/Sub** | 간단, 이미 인프라에 있는 경우 많음 | Redis 의존성 추가 |
| **Kafka 내부 토픽** | 추가 인프라 불필요 | 컨슈머가 이 토픽도 소비해야 함 |
| **Spring Cloud Bus** | Spring 생태계 통합 | 설정 복잡 |
| **HTTP broadcast** | 인프라 최소 | 서버 목록 관리 필요 |

### 오픈소스 기여

쿠팡 팀은 Spring Kafka PR #3318을 통해 `getTopicsAndCallbacks()` 메서드를 개선 (3.3.0+):
- 다중 컨슈머 그룹에서 각 그룹별 콜백을 정확히 구분
- `getGroupId()` 메서드 추가로 그룹 식별 가능

---

## 컬리 3PL — Outbox Pattern + Retry Topic 자가 치유 아키텍처

Transactional Outbox 패턴(Namastack 라이브러리)으로 DB-Kafka 발행 원자성을 보장하고, @RetryableTopic 145회(24시간) 자동 재시도로 수신 단계 장애를 자가 치유하는 아키텍처. TopicNameSet을 활용한 토픽별 알림 정책(최초 실패/복구/최종 실패)도 포함한다.

> **상세**: [21-outbox-retry-architecture.md](./21-outbox-retry-architecture.md)

---

## 종합: 국내 IT기업 프로덕션 설정 비교

| 설정 | 토스 (금융) | LINE (메시징) | 부하 테스트 사례 | 일반 권장값 |
|------|------------|--------------|----------------|------------|
| `acks` | `0` (시세) / `all` (거래) | 용도별 차등 | `all` | `all` |
| `enable.idempotence` | `true` (거래) | - | `true` | `true` |
| `max.in.flight.requests` | `5` | - | `1` → 병목 원인 | `5` (멱등성 ON) |
| `batch.size` | 용도별 차등 | 배칭으로 요청 수 제어 | `128KB` | `16384` (16KB) |
| `linger.ms` | - | - | `5` | `5~10` |
| `max.poll.records` | - | - | - | 처리 시간 기반 조정 |
| `max.poll.interval.ms` | - | - | - | 처리 시간 기반 조정 |
| `enable-auto-commit` | `false` | - | - | `false` |
| 클러스터 규모 | Active-Active 이중화 | 단일 초대형 클러스터 | 단일 브로커 | 최소 3 브로커 |
| 모니터링 | ClickHouse + 커스텀 메트릭 | 요청 쿼터 기반 | PromQL | Prometheus + Grafana |
| **핵심 병목** | 데이터센터 간 미러링 | 멀티 테넌트 격리 | Hot Key + in.flight=1 | - |

---

## 실전 프로덕션 설정 템플릿

국내 IT기업 사례를 종합한 Spring Boot 프로덕션 설정입니다:

```yaml
spring:
  kafka:
    bootstrap-servers: broker-0:9092,broker-1:9092,broker-2:9092

    producer:
      acks: all
      retries: 3
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
      properties:
        enable.idempotence: true
        max.in.flight.requests.per.connection: 5    # 멱등성 ON 시 최대값
        batch.size: 16384                            # 16KB 배치
        linger.ms: 5                                 # 5ms 대기 후 배치 전송
        delivery.timeout.ms: 120000                  # 전체 전송 시한 2분
        compression.type: lz4                        # 네트워크 대역폭 절약
        schema.registry.url: http://redpanda:8081
        auto.register.schemas: false                 # 프로덕션에서는 반드시 false
        use.latest.version: true

    consumer:
      group-id: ${spring.application.name}
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: io.confluent.kafka.serializers.KafkaAvroDeserializer
      auto-offset-reset: earliest
      enable-auto-commit: false                      # Kafka 클라이언트 자동 커밋 OFF
      properties:
        schema.registry.url: http://redpanda:8081
        specific.avro.reader: true
        max.poll.records: 100                        # 비즈니스 로직 처리 시간 기반 조정
        max.poll.interval.ms: 300000                 # 5분 (처리 시간에 맞춰 조정)
        session.timeout.ms: 30000                    # 30초
        heartbeat.interval.ms: 10000                 # 10초 (session.timeout의 1/3)

    listener:
      ack-mode: manual                               # Spring 프레임워크 수동 커밋
      concurrency: 3                                 # 파티션 수 이하로 설정
```

---

## 핵심 교훈

1. **용도별 차등 설정**: 토스처럼 시세(속도)와 거래(안전)에 서로 다른 Producer 설정을 사용합니다. 하나의 설정이 모든 상황에 맞지 않습니다.
2. **처리 시간 기반 튜닝**: 사람인 사례처럼 `max.poll.records`와 `max.poll.interval.ms`는 비즈니스 로직의 실제 처리 시간을 측정한 후 설정해야 합니다.
3. **쿼터 기반 격리**: LINE처럼 멀티 테넌트 환경에서는 요청 쿼터로 클라이언트 간 영향을 차단합니다.
4. **수동 커밋 완전 구현**: `enable-auto-commit: false`와 `ack-mode: manual` 두 가지를 반드시 함께 설정합니다.
5. **모니터링은 필수**: 토스의 ClickHouse 기반 커스텀 메트릭처럼, Kafka 운영은 관측 가능성(Observability)이 핵심입니다.
6. **Consumer lag = 0이 "정상"을 의미하지 않는다**: Producer 내부 RecordAccumulator 적체는 Consumer 지표로 발견할 수 없습니다. Producer 큐 깊이, Broker 응답 시간, Consumer lag을 구분하여 모니터링해야 합니다.
7. **Hot Key + `max.in.flight=1`은 처리량 병목**: 멱등성이 켜져 있으면 `max.in.flight=5`까지 순서가 보장되므로, 1로 고정할 이유가 없습니다.
