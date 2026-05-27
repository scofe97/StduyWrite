# 성능 기대치: 10초 폴링 → ms 이벤트, 파티션 × Consumer = 병렬도

> **한줄 요약**: TPS의 10초 폴링 기반 단일 스레드 처리를 Kafka 이벤트 드리븐 + 파티션 병렬 처리로 전환하여, 메시지 전달 지연을 10초→수 밀리초로, 처리량을 파티션 수 × Consumer 수로 선형 확장한다.

---

## 1. AS-IS 성능 지표 (TPS 폴링 기반)

### 1.1 메시지 전달 지연 (Latency)

**시나리오**: 상태 변경 요청(예: PNDNG→FRWRD) 발행 후 처리될 때까지의 시간

```
요청 발행 (t=0s)
    ↓
[10초 대기] ← 다음 스케줄러 사이클 대기
    ↓
SELECT 5개 PNDNG 주문 (t≈10s)
    ↓
각 주문별로:
  - PNDNG→FRWRD 상태 UPDATE
  - 외부 API 호출 (2~3초)
  - 결과 처리
    ↓
[15초 경과 후 다음 사이클]
SELECT 5개 FRWRD 주문 (t≈25s)
    ↓
처리 완료 (t≈40s+)
```

| 구간 | 시간 | 설명 |
|------|------|------|
| **최소 지연** | 10초 | 다음 스케줄러 사이클까지 대기 |
| **평균 지연** | 15~20초 | 10초(폴링) + 5~10초(처리) |
| **최악 지연** | 40초+ | 4단계 × (10초 폴링 + 5초 처리) |
| **End-to-End** | 40~60초 | 등록→PNDNG→FRWRD→RSPND→CSPNT |

### 1.2 처리량 (Throughput)

```yaml
스케줄러 설정:
  poolSize: 1           # 단일 스레드
  interval: 10000ms     # 10초 주기

배치 처리:
  SELECT … LIMIT 5      # 한 사이클에 5개
  처리: 순차 실행

계산:
  시간당 사이클: 60초 ÷ 10초 = 6 사이클
  시간당 메시지: 6 사이클 × 5 메시지/사이클 = 30 msg/hour
  초당 처리: 30 ÷ 3600 ≈ 0.0083 msg/sec (약 8msg/100sec)

  1000개 메시지 처리 시간: 1000 ÷ 6 × 10초 = 1667초 ≈ 28분
```

**DB 부하 분석**:
```
10초 주기 × 1440분/일 = 144사이클/일
144사이클 × 5개 SELECT = 720개 SELECT/일
+ 각 상태별 UPDATE: 720개 UPDATE/일
+ 외부 API 호출: 720회/일

TPS(Transaction Per Second):
  SELECT: 720 ÷ 86400 ≈ 0.0083 TPS
  UPDATE: 720 ÷ 86400 ≈ 0.0083 TPS
  (매우 낮은 DB 부하)
```

### 1.3 확장성 (Scalability)

```
인스턴스 1개:
  poolSize=1, interval=10s
  → 처리량: 30 msg/hour

인스턴스 2개:
  분산 락 (SELECT ... FOR UPDATE)
  → 락 경합으로 실제 처리량: 30~35 msg/hour (거의 개선 없음)

인스턴스 N개:
  락 병목으로 처리량 증가 정체
  → 수평 확장 불가능
```

---

## 2. TO-BE 성능 기대치 (이벤트 드리븐)

### 2.1 메시지 발행→소비 지연 (Kafka/Redpanda)

```
메시지 발행 (t=0ms)
    ↓
[0.5~2ms] ← Redpanda 브로커 처리 + 압축
    ↓
Consumer Group 폴링
    ↓
[1~5ms] ← 파티션에서 읽기
    ↓
Consumer 처리 시작 (t=2~7ms)
    ↓
비즈니스 로직 처리 (t + 처리시간)
```

| 지표 | 값 | 설명 |
|------|-----|------|
| **발행→브로커** | ~0.5ms | Redpanda C++ 기반 고성능 |
| **브로커→Consumer** | ~2~5ms | 네트워크 + 폴링 대기 |
| **p50 지연** | ~5ms | 중위값 |
| **p99 지연** | ~50ms | 99%의 메시지 |
| **p99.9 지연** | ~500ms | 네트워크 지연 포함 |
| **End-to-End** | 수백ms | 처리 시간 포함 |

### 2.2 처리량 (병렬 처리)

```
6개 파티션 설정:
  partition-0: Consumer-1
  partition-1: Consumer-2
  partition-2: Consumer-3
  partition-3: [미할당]
  partition-4: [미할당]
  partition-5: [미할당]

각 Consumer 처리량: 20 msg/sec
  3개 Consumer × 20 msg/sec = 60 msg/sec

최대 처리량:
  6 파티션 (모두 할당) × 20 msg/sec = 120 msg/sec
```

**처리량 비교**:
```
AS-IS (폴링):        0.0083 msg/sec
TO-BE (이벤트):      60~120 msg/sec
개선율:             7000~14000배
```

### 2.3 확장 공식

```
병렬도 = min(파티션 수, Consumer 수)

처리량(msg/sec) = 파티션 수 × 단일Consumer처리량
                (단, Consumer 수 ≤ 파티션 수)

예시:
  파티션 6 + Consumer 3 → 병렬도 3 → 처리량 = 3 × 20 = 60 msg/sec
  파티션 6 + Consumer 6 → 병렬도 6 → 처리량 = 6 × 20 = 120 msg/sec
  파티션 6 + Consumer 7 → 병렬도 6 → 처리량 = 6 × 20 = 120 msg/sec (1개 미사용)
```

**수평 확장 시나리오**:
```
1단계: 6 파티션, Consumer 3개
  처리량: 60 msg/sec
  병목: Consumer 부족

2단계: 6 파티션, Consumer 6개
  처리량: 120 msg/sec (+100%)
  병목: 파티션 부족

3단계: 12 파티션, Consumer 6개
  처리량: 240 msg/sec (+100%)
  병목: Consumer 부족

4단계: 12 파티션, Consumer 12개
  처리량: 480 msg/sec
  → 선형 확장 가능
```

---

## 3. 정량적 비교 (AS-IS vs TO-BE)

| 지표 | AS-IS (폴링) | TO-BE (이벤트) | 개선율 | 비고 |
|------|-------------|---------------|--------|------|
| **메시지 전달 지연** | 10~40초 | 5~50ms | **200~8000배** | 최악 40초→최상 5ms |
| **단일 메시지 End-to-End** | 40~60초 | 100~500ms | **100~200배** | 등록→완료 |
| **초당 처리량** | ~0.008 msg/sec | 60~120 msg/sec | **7500~15000배** | Consumer 병렬도 기준 |
| **1000개 메시지 처리** | ~28분 | ~10초 | **170배** | 6 Consumer 기준 |
| **최대 동시 처리** | 1개 | 파티션 수 | **6~12배** | PoC: 6 파티션 |
| **장애 복구 시간** | ~60초 | ~30초 | **2배** | 락 만료 vs 리밸런싱 |
| **10초당 DB SELECT** | 5개 | 0개 | **100% 감소** | 폴링 제거 |
| **외부 API 호출/일** | ~720회 | ~17280회 | **24배 증가** | 처리량 증가로 자연스러움 |
| **메모리 사용** | ~500MB | ~1.2GB | **2.4배 증가** | Consumer 버퍼 등 |

---

## 4. 파티션 설계 가이드

### 4.1 파티션 수 결정 공식

```
필요 파티션 수 = 목표 처리량(msg/sec) ÷ 단일Consumer처리량(msg/sec)
                + 여유도(20~30%)

예시 계산:
  목표: 초당 100메시지 처리
  Consumer당 처리량: 20 msg/sec
  필요 파티션: (100 ÷ 20) × 1.25 = 6.25 → 7개

PoC 규모 (10 msg/sec):
  파티션: (10 ÷ 20) × 1.25 = 0.625 → 최소 3개 (여유)

프로덕션 규모 (500 msg/sec):
  파티션: (500 ÷ 20) × 1.25 = 31.25 → 32개
```

### 4.2 파티션 키 전략

**주문 파이프라인 예시**:
```
키: orderId (주문번호)
  orderId=1001 → partition-0
  orderId=1002 → partition-1
  orderId=1003 → partition-0
  orderId=1004 → partition-2

효과:
  ✓ 같은 주문의 모든 이벤트가 같은 파티션 (순서 보장)
  ✓ 파티션 내에서 상태 전이 순서 일관성
  ✓ 중복 처리 방지 (idempotent)

주의사항:
  ✗ 특정 주문에 대량 이벤트 발행 시 핫 파티션
  ✗ 파티션 분배 불균형 모니터링 필수
```

**핫 파티션 예방**:
```
문제 시나리오:
  VIP 고객 orderId=7777에 1000개 이벤트 집중
  → 다른 파티션은 유휴, partition-X는 초과 부하

해결 방안:
  Option 1: 복합 키 사용
    orderId + timestamp를 일부 자릿수만 사용
    → 분산도 증가하지만 순서 보장 정밀도 감소

  Option 2: 별도 우선순위 토픽
    일반: orderId를 키로 (순서 보장)
    VIP: orderId + rand()를 키로 (분산, 순서 미보장)

  Option 3: 토픽 분할
    VIP 고객용 토픽 (파티션 다수)
    일반 고객용 토픽 (파티션 적음)
```

### 4.3 PoC 토픽 파티션 설정

```yaml
# Redpanda 토픽 생성 (PoC)
topics:
  pipeline.execute.request:
    num_partitions: 3
    replication_factor: 1          # PoC
    retention_ms: 86400000         # 1일
    compression_type: 'snappy'

  pipeline.execute.response:
    num_partitions: 3
    replication_factor: 1
    retention_ms: 3600000          # 1시간

  pipeline.status.update:
    num_partitions: 3
    replication_factor: 1
    retention_ms: 604800000        # 7일 (감사 로그)

  tx-orders/analytics/audit:
    num_partitions: 3
    replication_factor: 1
    retention_ms: 2592000000       # 30일

# 프로덕션 권장 설정
production:
  num_partitions: 9~12
  replication_factor: 3
  retention_ms: 604800000          # 7일 (비용 고려)
```

**파티션 증가 절차**:
```
현재: 3 파티션 (Consumer 부족 병목)
목표: 6 파티션

1. 토픽 재생성 (무중단 마이그레이션)
   a. 새 토픽 생성 (6 파티션)
   b. Consumer 재설정 (새 토픽 구독)
   c. 기존 토픽 백그라운드 마이그레이션
   d. 기존 토픽 삭제

2. Consumer 자동 리밸런싱
   리밸런싱 시간: ~30초
   대기: stop → new rebalance → resume
```

---

## 5. 병목 지점과 튜닝

### 5.1 Producer 튜닝 (발행 최적화)

```java
// Spring Boot ProducerConfig
@Configuration
public class ProducerConfig {

    @Bean
    public ProducerFactory<String, OrderEvent> producerFactory() {
        Map<String, Object> props = new HashMap<>();

        // 배치 튜닝
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);     // 16KB
        props.put(ProducerConfig.LINGER_MS_CONFIG, 5);          // 5ms 대기
        props.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 67108864); // 64MB

        // 압축
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");

        // 신뢰도
        props.put(ProducerConfig.ACKS_CONFIG, "all");           // 무손실
        props.put(ProducerConfig.RETRIES_CONFIG, 3);
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 1);

        // 성능
        props.put(ProducerConfig.CONNECTIONS_MAX_IDLE_MS_CONFIG, 540000);

        return new DefaultProducerFactory<>(props);
    }
}

// 성능 특성
튜닝 전:
  처리량: 50 msg/sec
  지연: 10~20ms

배치 + 압축:
  처리량: 120 msg/sec (+140%)
  지연: 5~15ms (압축으로 감소)

acks='all' 변경 시:
  처리량: 60 msg/sec (신뢰도 ↑)
  지연: 15~30ms (확인 대기)
```

### 5.2 Consumer 튜닝 (소비 최적화)

```java
@Configuration
public class ConsumerConfig {

    @Bean
    public ConsumerFactory<String, OrderEvent> consumerFactory() {
        Map<String, Object> props = new HashMap<>();

        // 배치 처리
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500);
        props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, 300000); // 5분
        props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 30000);    // 30초

        // 페칭 최적화
        props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, 1024);        // 1KB
        props.put(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG, 100);       // 100ms

        // 오프셋 관리
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);    // 수동 커밋

        return new DefaultConsumerFactory<>(props);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, OrderEvent>
            kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, OrderEvent> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.setConcurrency(3);  // 병렬도 = 파티션 수
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);
        return factory;
    }
}

// max.poll.records 선택 기준
시나리오 1: 빠른 처리 (< 100ms)
  max.poll.records: 1000
  effect: 배치 크기 ↑, 정시 처리 가능

시나리오 2: 무거운 처리 (5초)
  max.poll.records: 10
  effect: 배치 크기 ↓, 리밸런싱 빈번
  위험: 세션 타임아웃 (max.poll.interval.ms 증가 필요)

시나리오 3: 데이터베이스 쓰기 (2~3초)
  max.poll.records: 100
  effect: 1~3초 처리 시간, 적절한 배치

추천:
  처리시간 × 안전계수(2) < max.poll.interval.ms
  예: 처리 3초 → max.poll.interval.ms ≥ 6000ms
```

**지연 분석 (max.poll.records 영향)**:
```
시나리오: 1000개 메시지, 3 Consumer, 처리 시간 2초

max.poll.records=500:
  배치 1: 500개 (2초)
  배치 2: 500개 (2초)
  총 시간: 4초 (3 Consumer 병렬 고려 시 ~2초)

max.poll.records=10:
  배치 1: 10개 (2초)
  배치 2: 10개 (2초)
  ...
  배치 100: 10개 (2초)
  총 시간: 200초 (배치 오버헤드)

결론: 처리 시간에 맞춰 max.poll.records 조정 필수
```

### 5.3 브로커 튜닝 (Redpanda vs Kafka)

```yaml
# Redpanda 설정 (권장)
redpanda:
  data_directory: /var/lib/redpanda

  # 메모리 (Kafka 50% 수준)
  memory:
    memory_total_percent: 80        # 전체 메모리의 80% 사용

  # I/O 최적화
  storage:
    compression: snappy             # 드라이브 절약
    batch_max_bytes: 1048576        # 1MB 배치

  # 네트워크
  socket_send_buffer_bytes: 262144  # 256KB
  socket_recv_buffer_bytes: 262144

  # 로그 복제
  log_segment_size_bytes: 1073741824 # 1GB (큰 파티션용)

# Kafka 동등 설정
kafka:
  log.segment.bytes: 1073741824      # 1GB
  log.flush.interval.messages: 100000
  log.cleanup.policy: delete
  log.retention.hours: 24

# 성능 비교
지표          | Kafka | Redpanda | 개선율
-------------|-------|----------|--------
시작 시간     | 30초  | 2초      | 15배
메모리 사용   | 1GB   | 500MB    | 50%
처리량        | 100K  | 200K     | 2배
지연(p99)    | 50ms  | 10ms     | 5배
```

---

## 6. 현직 사례

### 6.1 LINE - 초당 최대 4GB 처리

```
규모:
  일일: 2,500억 레코드
  용량: 210TB 데이터
  처리량: 4,000 Mbps (피크)

아키텍처:
  클러스터: 단일 Kafka 클러스터
  토픽: 300+
  Consumer: 50+ 서비스

최적화:
  배치 처리: 10,000 메시지/배치
  압축: snappy
  복제: 3개 (안정성)

결과:
  지연: p99 < 1초
  가용성: 99.99%
```

### 6.2 Uber - Consumer 리밸런싱 최적화

```
문제:
  Consumer 추가 시 리밸런싱 → 지연 증가
  대규모 콘슈머 그룹 (수천 개): 리밸런싱 1~2분

해결:
  Cooperative sticky assignor 도입
  변경 전: 30초 정지 시간
  변경 후: 2~3초 정지 시간 (90% 개선)

구현:
  partition.assignment.strategy:
    CooperativeStickyAssignor
```

### 6.3 사람인 - max.poll.records 튜닝

```
초기 설정:
  max.poll.records: 500
  처리 로직: SELECT ∘ UPDATE (2분 소요)

문제:
  max.poll.interval.ms: 300000 (5분)
  처리 시간: 2분 × 500 = 1000분
  → 세션 타임아웃 발생, Consumer 추방

원인 분석:
  max.poll.records=500, 처리 2분
  → 500 × 2 = 1000분 > 5분 (타임아웃)

해결:
  max.poll.records: 2로 축소
  처리 시간: 2분 × 2 = 4분 < 5분 (안전)

결과:
  안정성 ↑, 처리량 = 2msg/poll
  → max.poll.interval.ms 300초로 단축 (초당 1메시지)

교훈:
  max.poll.records ∝ (max.poll.interval.ms / 처리시간)
```

---

## 7. 성능 모니터링 체크리스트

### 7.1 Producer 모니터링

```java
// Spring Boot Actuator 메트릭
@Component
public class ProducerMetrics {
    private final MeterRegistry meterRegistry;

    public void recordProducerMetrics() {
        // 발행 지연
        meterRegistry.timer("kafka.producer.send.latency")
            .record(() -> producer.send(record));

        // 발행 처리량
        meterRegistry.counter("kafka.producer.records.sent")
            .increment();

        // 배치 크기
        meterRegistry.gauge("kafka.producer.batch.size",
            () -> producerMetrics.getAvgBatchSize());
    }
}

// 모니터링 지표
지표                    | 경고 임계값 | 설명
------------------------|-----------|-------------------
producer.latency        | > 100ms   | 발행 지연 증가
producer.records.sent   | < 100/s   | 처리량 저하
producer.batch.size     | < 1KB     | 배치 효율 저하
producer.compression    | < 30%     | 압축 비율 저하
buffer.usage            | > 80%     | 버퍼 가득 참
```

### 7.2 Consumer 모니터링

```java
@Component
public class ConsumerMetrics {

    public void recordConsumerMetrics() {
        // 소비 지연 (Consumer Lag)
        meterRegistry.gauge("kafka.consumer.lag",
            () -> kafkaConsumerMetrics.getCurrentLag());

        // 처리 시간
        meterRegistry.timer("kafka.consumer.process.time")
            .record(() -> processMessage(record));

        // 리밸런싱
        meterRegistry.counter("kafka.consumer.rebalance")
            .increment();
    }
}

// 모니터링 지표
지표                      | 경고 임계값 | 설명
--------------------------|-----------|------------------------
consumer.lag              | > 10000   | 소비 지연 (메시지 수)
consumer.lag_ms           | > 60000   | 소비 지연 (시간)
consumer.process.time     | > 5000ms  | 처리 시간 증가
consumer.rebalance        | > 1/min   | 리밸런싱 빈번
partition.lag             | > 5000    | 특정 파티션 지연
committed.offset          | ↑ 정상   | 오프셋 진행 상황
fetch.latency             | > 50ms    | 페치 지연
```

### 7.3 브로커 모니터링

```yaml
# Prometheus 메트릭 (Redpanda)
redpanda_cluster_brokers: 3
redpanda_cluster_topics: 10
redpanda_storage_disk_free_bytes: < 10% → 경고

# JMX 메트릭 (Kafka)
kafka.broker:bytes_in_per_sec   # 수신 처리량
kafka.broker:bytes_out_per_sec  # 송신 처리량
kafka.broker:request_queue_size # 처리 대기열
kafka.broker:fetch_consumer_total_time_ms # 소비 지연

# 대시보드 구성
1. Cluster Health
   - Broker 상태 (Up/Down)
   - 복제 팩터 (in-sync replicas)

2. Throughput
   - bytes_in_per_sec (발행)
   - bytes_out_per_sec (소비)

3. Latency
   - producer_send_latency_ms
   - consumer_fetch_latency_ms

4. Lag
   - consumer_lag (모든 Consumer)
   - partition_lag (파티션별)
```

---

## 8. 면접 예상 질문

### Q1. 파티션 수를 어떻게 결정하나요?

**답변 구조**:
```
1. 공식 설명
   필요 파티션 = (목표 처리량 ÷ Consumer당 처리량) × 안전계수

2. PoC 적용 예시
   - 초당 10메시지 처리 목표
   - Consumer당 처리량: 20 msg/sec
   - 필요 파티션: (10 ÷ 20) × 1.25 = 0.625 → 3개 (최소)

3. 병렬도 개념 설명
   파티션 6개 + Consumer 3개 → 병렬도 3
   처리량 = 3개 Consumer × 20 msg/sec = 60 msg/sec

4. 확장 시나리오
   초기: 3 파티션 → 병목 없음 (PoC)
   성장: 6 파티션 + 6 Consumer → 120 msg/sec 달성
   미래: 12 파티션 + 12 Consumer → 240 msg/sec (선형 확장)

5. 파티션 키 고려사항
   - orderId를 키로 → 같은 주문 순서 보장
   - 핫 파티션 주의 (VIP 고객 트래픽 집중)
   - 키 분포 모니터링 필수
```

**따라가기 질문 대비**:
```
Q: "파티션을 너무 많이 만들면 어떻게 되나요?"
A:
  단점:
    - 메모리 오버헤드 (각 파티션 메타데이터)
    - 리밸런싱 시간 증가
    - 저장소 용량 분산 (Fragment)

  권장:
    - 필요한 병렬도 + 20% 여유 (장애 대비)
    - 정기적 재검토 (3개월)

Q: "파티션을 줄일 수 없나요?"
A:
  불가능 (감소 안 됨)
  해결책:
    - 새 토픽 생성 (파티션 설정)
    - Consumer 마이그레이션
    - 기존 토픽 삭제
```

---

### Q2. Consumer 수가 파티션 수보다 많으면 어떻게 되나요?

**답변 구조**:
```
1. 동작 원리 설명
   파티션: [0, 1, 2, 3, 4, 5]
   Consumer: [A, B, C, D, E, F, G, H] (8개)

   할당:
   Consumer-A: partition-0
   Consumer-B: partition-1
   Consumer-C: partition-2
   Consumer-D: partition-3
   Consumer-E: partition-4
   Consumer-F: partition-5
   Consumer-G: [미할당] ← 유휴
   Consumer-H: [미할당] ← 유휴

2. 성능 영향
   처리량: 6 파티션 × 20 msg/sec = 120 msg/sec (변화 없음)
   자원: 2개 Consumer 유휴 (낭비)
   비용: 불필요한 인스턴스 (스케일다운 권장)

3. 리밸런싱 영향
   Consumer 추가/제거 시:
     6 파티션 + 3 Consumer → 6 파티션 + 4 Consumer
     리밸런싱: ~30초 (모든 Consumer 정지)

4. 해결책
   Option 1: Consumer 수 조정
     Consumer = min(파티션 수, 목표 병렬도)

   Option 2: 파티션 증가
     파티션 8개로 확대 → Consumer 8개 활용

   Option 3: Consumer Group 분리
     group-A: partition [0, 1, 2]
     group-B: partition [3, 4, 5]
     (서로 다른 로직 처리 시)

5. 모니터링
   - assigned_partitions: Consumer가 할당받은 파티션
   - Consumer lag: 미할당 Consumer는 0 (처리 없음)
```

**따라가기 질문**:
```
Q: "한 Consumer가 여러 파티션을 처리할 수 있나요?"
A:
  네, 자동 할당
  예: 3개 Consumer × 6개 파티션 = 2 파티션/Consumer

  장점: 자동 로드 밸런싱
  단점: 단일 Consumer 부하 증가 (처리 느려짐)
```

---

### Q3. Kafka/Redpanda의 성능 병목 지점은?

**답변 구조**:
```
1. Producer 병목
   원인:
     - batch.size 작음 → 배치 효율 저하
     - compression 미사용 → 네트워크 대역폭 증가
     - linger.ms 0 → 개별 메시지 발행 (오버헤드)

   해결:
     batch.size: 16KB (기본값, 괜찮음)
     linger.ms: 5ms (배치 대기)
     compression_type: snappy/lz4

2. Consumer 병목
   원인:
     - max.poll.records 너무 크거나 작음
     - 처리 로직이 느림 (DB 쓰기)
     - max.poll.interval.ms 부족

   해결:
     max.poll.records = (max.poll.interval_ms ÷ 처리시간) × 0.5
     fetch.min.bytes 증가 (배치 효율)
     병렬도 증대 (Consumer 추가)

3. 브로커 병목
   원인:
     - 디스크 I/O 한계
     - 메모리 부족 (페이지 캐시)
     - 복제 오버헤드

   해결:
     SSD 사용 (HDD 대비 10배)
     메모리 증가
     복제 팩터 조정 (3→2)

4. 네트워크 병목
   원인:
     - 압축 미사용
     - 데이터 센터 간 복제

   해결:
     compression: snappy
     같은 DC 배포

5. 클라이언트 병목
   원인:
     - 느린 처리 로직
     - 리소스 부족 (CPU, 메모리)

   해결:
     비동기 처리
     스레드 풀 증가
     배치 처리 크기 조정
```

**우선순위**:
```
1순위: 파티션 수 (병렬도) - 가장 큰 영향
2순위: Consumer 병렬도 - 파티션 활용도
3순위: 배치 크기 (max.poll_records) - 처리 시간 조정
4순위: 압축 (snappy/lz4) - 네트워크 절약
5순위: 브로커 설정 - 세부 튜닝
```

---

### Q4. 이벤트 드리븐 전환으로 어떤 성능 개선을 기대하나요?

**답변 구조**:
```
1. 현황 (AS-IS)
   - 10초 주기 폴링
   - 단일 스레드 순차 처리
   - 처리량: ~0.008 msg/sec
   - 지연: 10~40초
   - DB: SELECT 144회/일 (폴링)

2. 전환 (TO-BE)
   - 이벤트 기반 즉시 처리
   - 파티션 × Consumer 병렬
   - 처리량: 60~120 msg/sec (75배)
   - 지연: 5~50ms (200배)
   - DB: 0회 폴링 (제거)

3. 구체적 개선
   a) 지연 개선
      Before: 메시지 발행 → 10초 대기 → 처리
      After: 메시지 발행 → 수ms 처리
      효과: 실시간성 ↑, UX 개선

   b) 처리량 개선
      Before: 1개 메시지 ≈ 12초 (10초 폴링 + 처리)
      After: 1개 메시지 ≈ 100ms (이벤트 기반)
      효과: 대용량 메시지 처리 가능

   c) 확장성 개선
      Before: Consumer 추가 → 락 경합 → 개선 없음
      After: Consumer 추가 → 자동 리밸런싱 → 선형 확장
      예: 3 Consumer → 6 Consumer = 2배 처리량

   d) 인프라 개선
      Before: DB 부하 (SELECT × 144회/일)
      After: 0 (폴링 제거)
      효과: DB 부하 100% 감소, 비용 절감

4. 비즈니스 임팩트
   - 주문 처리 시간: 60초 → 500ms (120배)
   - 피크 시간대 처리량: 30 orders/hour → 120 orders/sec
   - 장애 복구: 60초 → 30초 (자동 리밸런싱)

5. 트레이드오프
   - 메모리 증가: 500MB → 1.2GB
   - 복잡도 증가: 폴링(단순) → 이벤트(복잡)
   - 운영 난이도: 모니터링 필수
```

**따라가기 질문**:
```
Q: "진짜 100배까지 개선되나요?"
A:
  처리량: 실제 7500배 (0.008 → 60 msg/sec)
  지연: 200배 (10초 → 50ms)

  조건:
    - 파티션: 6개 최소
    - Consumer: 충분한 리소스
    - 처리 로직: 최적화됨

Q: "언제부터 개선이 보이나요?"
A:
  즉시: 지연 (10초 → 수ms)
  점진적: 처리량 (Consumer 추가하면서)

  측정:
    - 주차 1: 지연 개선 검증
    - 주차 2~3: 병렬도 증가로 처리량 개선
    - 주차 4: 완전 안정화
```

---

## 9. 면접 체크리스트

### 확실히 답할 수 있는 개념
- [ ] 파티션과 Consumer의 관계 (병렬도 공식)
- [ ] 처리량 계산 (msg/sec = 파티션 × Consumer처리량)
- [ ] 메시지 지연 (발행→소비 시간)
- [ ] 파티션 키의 역할 (순서 보장)
- [ ] max.poll.records의 영향
- [ ] Consumer lag 모니터링
- [ ] 리밸런싱 개념

### 깊이 있게 설명할 수 있는 주제
- [ ] AS-IS (폴링) vs TO-BE (이벤트) 비교표
- [ ] 파티션 수 결정 공식 유도
- [ ] 핫 파티션 문제와 해결책
- [ ] 성능 튜닝 우선순위

### 실제 사례 언급
- [ ] LINE 사례 (초당 4GB, 2500억 레코드)
- [ ] Uber 사례 (Cooperative Sticky Assignor)
- [ ] 사람인 사례 (max.poll.records 튜닝)

---

## 10. 관련 문서

| 문서 | 설명 |
|------|------|
| [01. 스케줄러 → 이벤트 드리븐](../logic-changes/01-scheduler-to-event-driven.md) | 아키텍처 전환 상세 |
| [07. DB 분산 락 → Consumer Group](../logic-changes/07-db-lock-to-consumer-group.md) | 동시성 제어 방식 변경 |
| [09. 모니터링 & Observability](./09-monitoring-observability.md) | 성능 모니터링 방법 |
| [10. 배포 & 운영](./10-deployment-operations.md) | 프로덕션 배포 가이드 |
| [11. 트러블슈팅](./11-troubleshooting.md) | 문제 해결 가이드 |

---

## 11. 핵심 요약

```
AS-IS (폴링):
  지연: 10~40초 (10초 주기)
  처리량: 0.008 msg/sec (단일 스레드)
  확장: 불가능 (락 병목)
  DB: SELECT 144회/일 (폴링 오버헤드)

TO-BE (이벤트):
  지연: 5~50ms (ms 수준)
  처리량: 60~120 msg/sec (병렬도 = 파티션)
  확장: 선형 확장 (Consumer/파티션 추가)
  DB: 0회 폴링 (제거)

핵심 공식:
  병렬도 = min(파티션, Consumer 수)
  처리량 = 파티션 수 × Consumer 처리량
  지연 개선 = 200~8000배

PoC 설정:
  파티션: 3~6개
  Consumer: 3개
  batch.size: 16KB
  compression: snappy
  max.poll_records: 500
```

---

**최종 상태**: 면접 준비 완료 (한국어, 정량적, 사례 포함)
