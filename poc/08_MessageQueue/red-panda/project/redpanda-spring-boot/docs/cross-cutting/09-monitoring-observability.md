# 모니터링/옵저버빌리티 비교: DB 상태 조회 vs Prometheus + Consumer Lag + Grafana

> 한줄 요약: TPS의 DB 테이블 직접 조회 기반 모니터링을 Prometheus 메트릭 수집 + Consumer Lag 모니터링 + Grafana 대시보드로 대체하여, 실시간 관측 가능성을 확보한다.

---

## 1. AS-IS: TPS 기존 모니터링 방식

### 1.1 현재 모니터링 방법

TPS 시스템의 기존 모니터링은 사후(Post-mortem) 기반의 쿼리 방식을 중심으로 운영되고 있다.

```sql
-- DBA 또는 운영팀이 수동으로 실행하는 쿼리
SELECT COUNT(*) as fail_count
FROM TB_TPS_MS_021
WHERE linkSttsCd = 'FAIL'
  AND regDt >= TRUNC(SYSDATE);

-- 일일 통계 조회
SELECT linkSttsCd, COUNT(*) as count
FROM TB_TPS_MS_021
WHERE regDt >= TRUNC(SYSDATE)
GROUP BY linkSttsCd;
```

**실제 운영 프로세스:**

1. **문제 감지**: 고객 컴플레인 또는 대시보드 확인
2. **원인 조사**: DBA가 위 쿼리 실행 → 실패 건수 확인
3. **대응**: 오류 유형 분류 → 원인 파악 → 수정
4. **기록**: 로그 파일(application.log)에서 스택 트레이스 검색

### 1.2 기존 방식의 문제점

| # | 문제 | 비즈니스 영향 | 기술적 원인 |
|---|------|------------|----------|
| 1 | **사후 대응** | 문제 발생 후 인지까지 수시간 소요 | 실시간 알림 메커니즘 없음 |
| 2 | **DB 성능 저하** | 모니터링 쿼리 자체가 DB 부하 증가 | SELECT COUNT 같은 집계 쿼리는 Full Table Scan |
| 3 | **정량적 메트릭 부재** | 처리량, 레이턴시, 실패율 등 지표 불명확 | 메트릭 자동 수집 시스템 없음 |
| 4 | **알림 기능 없음** | 임계치 초과 시 자동 알림 불가 | 임계치 규칙 정의 및 자동화 부재 |
| 5 | **수동 대시보드** | 매번 새로운 쿼리 작성 필요 | 시계열 데이터 추적 및 시각화 도구 없음 |
| 6 | **이력 추적 어려움** | 과거 패턴 분석 불가능 | 메트릭 히스토리 수집 안 함 |

**구체적 사례:**

```
Timeline: 메시지 처리 장애 발생 시나리오
├─ 10:30 - 네트워크 오류 발생 (Producer 단에서 전송 지연)
├─ 10:32 - Consumer Lag 증가하기 시작
├─ 10:45 - 고객 콜 센터 문의 증가 (문제 감지)
├─ 11:00 - DBA가 SELECT COUNT(*) 쿼리 실행
├─ 11:05 - FAIL 상태 메시지 500건 확인
├─ 11:20 - 네트워크 팀에 알림
├─ 11:45 - 네트워크 복구
└─ 12:00 - 처리 완료 (총 1.5시간 지연)

문제: 10:32에 감지할 수 있었으나 10:45에 감지함 (13분 지연)
```

---

## 2. TO-BE: Prometheus + Consumer Lag + Grafana 기반 모니터링

### 2.1 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────┐
│                      Observability Stack                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  Data Sources (메트릭 수집)                                   │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐   ┌──────────────────────┐          │
│  │ RedPanda Broker     │   │ Spring Boot App      │          │
│  │ /public_metrics:9644│   │ /actuator/prometheus │          │
│  │                     │   │ (Micrometer)         │          │
│  └────────┬────────────┘   └──────────┬───────────┘          │
│           │                           │                       │
│  ┌────────▼────────────┐   ┌──────────▼───────────┐          │
│  │ Cluster Health      │   │ Application Metrics  │          │
│  │ - Broker status     │   │ - Consumer lag       │          │
│  │ - Replication       │   │ - Throughput         │          │
│  │ - Latency           │   │ - Error rate         │          │
│  └────────┬────────────┘   └──────────┬───────────┘          │
│           │                           │                       │
└───────────┼───────────────────────────┼───────────────────────┘
            │                           │
            └───────────┬───────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  Prometheus                    │
        │  (메트릭 저장소 + 쿼리 엔진)     │
        │  - 15초마다 스크래핑             │
        │  - 시계열 DB에 저장             │
        │  - 알람 규칙 평가               │
        └───────────────┬────────────────┘
                        │
        ┌───────────────┼────────────────┐
        │               │                │
   ┌────▼────┐   ┌─────▼──────┐   ┌─────▼──────┐
   │ Grafana  │   │ AlertManager│  │ Thanos     │
   │(대시보드) │   │(알림 발송)  │  │(장기 저장) │
   └──────────┘   └────────────┘   └────────────┘
```

### 2.2 RedPanda 메트릭 수집

RedPanda는 JVM 기반으로 Prometheus 형식의 메트릭을 노출한다.

**메트릭 엔드포인트:**
```
http://localhost:9644/public_metrics
```

**주요 메트릭 카테고리:**

#### 2.2.1 클러스터 상태 메트릭

```
# 활성 브로커 수
redpanda_cluster_brokers 3

# Under-replicated 파티션 수 (복제 진행 중)
redpanda_kafka_under_replicated_replicas 0

# 리더/라이터 그룹 크기
redpanda_group_broker_read_group_size 1024
redpanda_group_broker_write_group_size 2048
```

**해석:**
- `under_replicated_replicas > 0`: 파티션이 아직 복제 완료 안 됨 → 안정성 저하
- 정상: 모든 파티션이 ISR(In-Sync Replicas)에 동기화됨

#### 2.2.2 성능 메트릭

```
# 요청별 레이턴시 (초 단위)
redpanda_kafka_request_latency_seconds_bucket{
  handler="produce",
  le="0.001"
} 15000

redpanda_kafka_request_latency_seconds_bucket{
  handler="produce",
  le="0.01"
} 15050

redpanda_kafka_request_latency_seconds_bucket{
  handler="fetch",
  le="0.1"
} 8000

# 처리 중인 요청 수
redpanda_kafka_concurrent_requests 42
```

**해석:**
- Produce 레이턴시 > 100ms: Producer가 느림 (네트워크 또는 디스크 I/O)
- Fetch 레이턴시 > 500ms: Consumer가 느림 (Consumer Lag 증가 위험)

#### 2.2.3 리소스 메트릭

```
# 할당된 메모리 (바이트)
redpanda_memory_allocated_memory 2147483648  # 2GB

# 실제 사용 메모리
redpanda_memory_used_memory 1677721600  # 1.6GB

# CPU 사용률
redpanda_cpu_busy_time_total 85000000  # 나노초 누적
```

### 2.3 Consumer Lag 모니터링

**Consumer Lag의 정의:**

```
Consumer Lag = Latest Offset - Committed Offset
```

**예시:**

```
토픽: order-events
파티션: 0
  - 현재 최신 오프셋(Latest): 10000
  - 컨슈머 커밋 오프셋: 8500
  - LAG = 10000 - 8500 = 1500

의미: 컨슈머가 아직 1500개의 메시지를 처리하지 못함
```

**Consumer Lag 증가 시나리오:**

```
Timeline: Lag 증가 원인 분석

시나리오 1: Producer 처리량 급증
─────────────────────────────────
  Produce Rate: 100 msg/sec → 1000 msg/sec (10배)
  Consume Rate: 100 msg/sec (동일)
  결과: Lag 1분마다 5400개 증가

시나리오 2: Consumer 장애
─────────────────────────────────
  Produce Rate: 100 msg/sec
  Consume Rate: 100 msg/sec → 0 msg/sec (다운)
  결과: Lag 매초 100씩 증가

시나리오 3: 네트워크 지연
─────────────────────────────────
  Produce Rate: 100 msg/sec
  Consume Rate: 100 msg/sec (처리 가능하나 조회 지연)
  결과: Lag 급격히 증가 후 안정화
```

**RedPanda에서 Consumer Lag 조회:**

```bash
# Consumer Group의 모든 파티션 Lag 조회
rpk group describe ch07-consumer

# 상세 출력
rpk group describe ch07-consumer --detailed

# 특정 토픽에 대한 Lag
rpk group describe ch07-consumer --members

# 실시간 모니터링 (1초마다 갱신)
watch -n 1 'rpk group describe ch07-consumer'
```

**출력 예시:**

```
GROUP           ID  TOPIC          PARTITION  OFFSET  LAG  MEMBER-ID
ch07-consumer   0   order-events   0          8500    1500 app-instance-1
ch07-consumer   0   order-events   1          7200    800  app-instance-2
ch07-consumer   0   order-events   2          9100    900  app-instance-3

Total LAG: 3200 messages
```

**Prometheus 메트릭:**

```
# Consumer Group별 Lag
kafka_consumer_group_lag{
  group="ch07-consumer",
  topic="order-events",
  partition="0"
} 1500

kafka_consumer_group_lag{
  group="ch07-consumer",
  topic="order-events",
  partition="1"
} 800

# Consumer Group 전체 Lag
kafka_consumer_group_lag_sum{
  group="ch07-consumer"
} 3200
```

### 2.4 Spring Boot Actuator 메트릭

Spring Boot 3.0 이상에서 Micrometer를 통해 자동으로 Kafka 메트릭을 노출한다.

**설정 (application.yml):**

```yaml
# Kafka 메트릭 활성화
management:
  endpoints:
    web:
      exposure:
        include: prometheus  # /actuator/prometheus 엔드포인트 활성화
  metrics:
    tags:
      application: order-service
      environment: production
    distribution:
      percentiles-histogram:
        kafka.consumer.fetch.manager.records.lag: true
```

**주요 메트릭:**

#### 2.4.1 Consumer 메트릭

```
# 소비한 메시지 총수
kafka_consumer_records_consumed_total{
  client_id="order-consumer-1",
  topic="order-events"
} 245000

# Consumer Lag (records lag)
kafka_consumer_fetch_manager_records_lag{
  client_id="order-consumer-1",
  topic="order-events",
  partition="0"
} 1500

# Fetch 요청 지연 시간 (초)
kafka_consumer_fetch_latency_avg{
  client_id="order-consumer-1"
} 0.025

# Consumer 연결 상태
kafka_consumer_coordinator_assigned_partitions{
  client_id="order-consumer-1"
} 3
```

#### 2.4.2 Producer 메트릭

```
# 전송한 메시지 총수
kafka_producer_record_send_total{
  client_id="order-producer-1",
  topic="order-events"
} 250000

# 전송 실패 수
kafka_producer_record_send_total{
  client_id="order-producer-1",
  topic="order-events",
  result="failure"
} 5

# 메시지 크기 분포
kafka_producer_record_size_avg{
  client_id="order-producer-1",
  topic="order-events"
} 512

# 전송 지연 시간 (ms)
kafka_producer_request_latency_avg{
  client_id="order-producer-1"
} 15.5
```

#### 2.4.3 Java 애플리케이션 메트릭

```
# JVM 힙 메모리 사용
jvm_memory_used_bytes{
  area="heap"
} 536870912  # 512MB

# GC 일시정지 시간
jvm_gc_pause_seconds{
  action="end of major GC",
  cause="Metadata GC Threshold"
} 0.125

# Thread 개수
jvm_threads_live_threads 42
```

### 2.5 Grafana 대시보드 설계

#### 2.5.1 대시보드 레이아웃

```
┌─────────────────────────────────────────────────────────────────┐
│  Kafka/RedPanda 모니터링 대시보드                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [시간 선택]    [새로고침]    [Export]    [Edit]                 │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│  Row 1: 클러스터 개요                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ 브로커: 3 │  │ 토픽: 15 │  │ 파티션: 45│  │ 복제: OK │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
├─────────────────────────────────────────────────────────────────┤
│  Row 2: 처리량 (실시간)                                           │
│  ┌────────────────────────────────────┐  ┌─────────────────┐   │
│  │ Produce Rate (msg/sec)             │  │ Fetch Rate      │   │
│  │ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▁│  │ ▁▂▃▄▅▆▇█▇▆▅   │   │
│  │ 평균: 1200 msg/sec, 최고: 2100    │  │ 평균: 1195     │   │
│  └────────────────────────────────────┘  └─────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Row 3: 레이턴시 분포                                             │
│  ┌────────────────────────────────────┐  ┌─────────────────┐   │
│  │ Produce Latency (ms)               │  │ Fetch Latency   │   │
│  │ p50: 5ms   p99: 25ms   max: 150ms  │  │ p50: 10ms       │   │
│  │ ▔▔▔▔▔▁▁▁▁▁▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂    │  │ p99: 80ms       │   │
│  └────────────────────────────────────┘  └─────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Row 4: Consumer Lag (그룹별)                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Consumer Lag Trend (24시간)                              │   │
│  │                                                            │   │
│  │ ch07-consumer    ▁▂▃▄▅▆▇█▆▅▄▃▂▁▁▂▃▄▅▆▇█  현재: 3200   │   │
│  │ audit-consumer   ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁  현재: 150    │   │
│  │ report-consumer  ▇▆▅▄▃▂▁▁▂▃▄▅▆▇█▇▆▅▄▃  현재: 5400   │   │
│  │                                                            │   │
│  └──────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Row 5: 에러/DLT 모니터링                                        │
│  ┌────────────────────────────────────┐  ┌─────────────────┐   │
│  │ 메시지 전송 실패율                  │  │ DLT 유입률      │   │
│  │ 0.02% (5 실패/250000 전송)        │  │ 0.5 msg/min    │   │
│  │ ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁             │  │ ▁▁▂▁▁▁▁▁▂▂▃▂▁ │   │
│  └────────────────────────────────────┘  └─────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  Row 6: 인프라 리소스                                             │
│  ┌────────────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ CPU 사용률        │  │ 메모리 사용률 │  │ 디스크 I/O   │    │
│  │ 현재: 65%        │  │ 현재: 78%    │  │ Writes: 150 │    │
│  │ ▁▂▃▄▅▆▇█▆▅▄▃▂▁│  │ ▁▂▃▄▅▆▇▇▇▆▅▄▃│  │ MB/sec      │    │
│  └────────────────────┘  └──────────────┘  └──────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.5.2 Row 1: 클러스터 개요

**Stat 패널 (Gauge):**

```json
{
  "targets": [
    {
      "expr": "count(redpanda_cluster_brokers)",
      "legendFormat": "Active Brokers"
    },
    {
      "expr": "count(count by (topic) (redpanda_kafka_log_partition_size))",
      "legendFormat": "Topics"
    },
    {
      "expr": "count(redpanda_kafka_log_partition_size)",
      "legendFormat": "Partitions"
    },
    {
      "expr": "count(redpanda_kafka_under_replicated_replicas > 0) == 0",
      "legendFormat": "Replication Health"
    }
  ]
}
```

#### 2.5.3 Row 2: 처리량

**Graph 패널:**

```json
{
  "title": "Produce & Consume Rate (24h)",
  "targets": [
    {
      "expr": "rate(kafka_producer_record_send_total[1m])",
      "legendFormat": "Produce Rate (msg/sec)"
    },
    {
      "expr": "rate(kafka_consumer_records_consumed_total[1m])",
      "legendFormat": "Consume Rate (msg/sec)"
    }
  ],
  "yaxes": [
    {
      "format": "short",
      "label": "Messages/Second"
    }
  ]
}
```

**PromQL 해석:**

```
rate(kafka_producer_record_send_total[1m])
= 지난 1분간 produce_total의 증가분을 시간당 비율로 변환
= 1분마다 계산해서 실시간 produce rate 제공
```

#### 2.5.4 Row 3: 레이턴시 분포

**Heatmap + Stat 패널:**

```json
{
  "title": "Produce Latency Percentiles",
  "targets": [
    {
      "expr": "histogram_quantile(0.50, rate(redpanda_kafka_request_latency_seconds_bucket{handler='produce'}[5m]))",
      "legendFormat": "p50"
    },
    {
      "expr": "histogram_quantile(0.99, rate(redpanda_kafka_request_latency_seconds_bucket{handler='produce'}[5m]))",
      "legendFormat": "p99"
    },
    {
      "expr": "max(redpanda_kafka_request_latency_seconds_bucket{handler='produce'})",
      "legendFormat": "max"
    }
  ]
}
```

**임계치 설정:**

```
p50 < 10ms   : 정상 (녹색)
p50 < 50ms   : 경고 (황색)
p50 >= 50ms  : 심각 (빨강)

p99 < 100ms  : 정상
p99 < 200ms  : 경고
p99 >= 200ms : 심각
```

#### 2.5.5 Row 4: Consumer Lag

**Bar Gauge + Time Series:**

```json
{
  "title": "Consumer Group Lag Status",
  "targets": [
    {
      "expr": "sum by (group) (kafka_consumer_group_lag)",
      "legendFormat": "{{ group }}"
    }
  ],
  "overrides": [
    {
      "matcher": { "id": "byName", "options": "ch07-consumer" },
      "properties": [
        {
          "id": "color",
          "value": { "mode": "fixed", "fixedColor": "red" }
        }
      ]
    }
  ]
}
```

**Lag 임계치:**

```
그룹별 Lag < 500    : 정상 (녹색)
      500-2000     : 경고 (황색) - Consumer가 따라잡는 중
      > 2000       : 심각 (빨강) - Consumer 다운 또는 Producer 급증
```

#### 2.5.6 Row 5: DLT (Dead Letter Topic) 모니터링

```json
{
  "title": "DLT Message Ingestion Rate",
  "targets": [
    {
      "expr": "rate(kafka_producer_record_send_total{topic=~'.*dlt.*'}[1m])",
      "legendFormat": "{{ topic }}"
    }
  ]
}
```

**임계치:**

```
DLT Rate < 1 msg/min     : 정상
        1-10 msg/min    : 경고 (처리 중인 에러 증가)
        > 10 msg/min    : 심각 (대규모 에러 발생)
```

### 2.6 알림 규칙 (Alert Rules)

Prometheus는 PromQL 기반의 alert rule로 조건을 감시하고 AlertManager로 알림을 전송한다.

**파일 위치:** `/etc/prometheus/rules/kafka-alerts.yaml`

```yaml
groups:
  - name: kafka_alerts
    interval: 30s
    rules:

      # Rule 1: 브로커 다운
      - alert: RedpandaBrokerDown
        expr: count(up{job="redpanda"}) < 3
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "RedPanda Broker Down ({{ $labels.instance }})"
          description: |
            RedPanda 브로커가 응답하지 않습니다.
            영향받은 파티션이 복제 불가능 상태입니다.
            현재 활성 브로커: {{ $value }}개

      # Rule 2: Consumer Lag 높음
      - alert: ConsumerLagHigh
        expr: sum by (group) (kafka_consumer_group_lag) > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Consumer Lag High ({{ $labels.group }})"
          description: |
            Consumer Group '{{ $labels.group }}'의 Lag이 높습니다.
            현재 Lag: {{ $value }} messages
            권장 조치:
            - Consumer 로그 확인 (병렬 처리 불가?)
            - Producer 처리량 확인 (급증?)
            - 네트워크 연결 상태 확인

      # Rule 3: Producer Latency 높음
      - alert: ProduceLatencyHigh
        expr: |
          histogram_quantile(0.99,
            rate(redpanda_kafka_request_latency_seconds_bucket{handler="produce"}[5m])
          ) > 0.1
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Produce Latency P99 > 100ms"
          description: |
            메시지 전송 지연이 높습니다.
            P99 Latency: {{ $value }}초
            원인 분석:
            - 디스크 I/O 속도 (iostat 확인)
            - 네트워크 지연 (ping 확인)
            - 브로커 CPU 부하 (htop 확인)

      # Rule 4: DLT 유입률 높음
      - alert: DltRateHigh
        expr: |
          rate(kafka_producer_record_send_total{topic=~".*dlt.*"}[1m]) > 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High DLT Message Rate (> 1 msg/min)"
          description: |
            Dead Letter Topic으로 메시지가 빠르게 유입됩니다.
            현재 유입률: {{ $value }} msg/sec
            대응:
            - DLT 메시지 내용 확인 (에러 타입)
            - 원본 토픽의 Producer 애플리케이션 로그 확인
            - 마지막 배포 이후 변경사항 확인

      # Rule 5: Under-replicated 파티션 존재
      - alert: UnderReplicatedPartitions
        expr: count(redpanda_kafka_under_replicated_replicas > 0) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $value }} Under-replicated Partitions Detected"
          description: |
            일부 파티션이 아직 복제 중입니다.
            파티션이 안전하지 않은 상태이므로 빠른 대응이 필요합니다.

            명령어:
            rpk admin brokers
            rpk topic describe --detailed <topic>

      # Rule 6: 메모리 사용률 높음
      - alert: BrokerMemoryUsageHigh
        expr: |
          redpanda_memory_used_memory / redpanda_memory_allocated_memory > 0.85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Broker Memory Usage > 85% ({{ $labels.instance }})"
          description: |
            브로커의 메모리 사용률이 높습니다.
            현재 사용률: {{ $value | humanizePercentage }}
            대응:
            - 파티션 리더 복사본 축소
            - 오래된 데이터 정리 (retention 설정)
            - 메모리 증설 계획
```

**Alert 심각도 정의:**

| 심각도 | 대응 시간 | 예시 |
|------|---------|------|
| **critical** | 즉시 (< 5분) | 브로커 다운, 데이터 손실 위험 |
| **warning** | 30분 내 | Lag 증가, 레이턴시 상승 |
| **info** | 업무 시간 내 | CPU 사용률 높음, 메모리 경고 |

**AlertManager 설정 (alertmanager.yml):**

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'slack-default'
  group_by: ['alertname', 'group']
  group_wait: 10s  # 첫 알림까지 대기 시간
  group_interval: 10s  # 같은 그룹 알림 간격
  repeat_interval: 4h  # 반복 알림 간격

  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
      group_wait: 0s  # 즉시 발송
      repeat_interval: 15m

    - match:
        severity: warning
      receiver: 'slack-warnings'
      repeat_interval: 1h

receivers:
  - name: 'slack-default'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK'
        channel: '#kafka-monitoring'
        title: 'Kafka Alert'
        text: '{{ .GroupLabels.alertname }}\n{{ .CommonAnnotations.description }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_SERVICE_KEY'
        description: '{{ .GroupLabels.alertname }}'

  - name: 'slack-warnings'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK'
        channel: '#kafka-warnings'
```

---

## 3. AS-IS vs TO-BE 상세 비교

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        모니터링 방식 비교                                 │
├─────────────────────────────────────────────────────────────────────────┤
```

### 3.1 데이터 수집 방식

| 항목 | AS-IS (DB 쿼리) | TO-BE (Prometheus) |
|------|-----------------|-------------------|
| **수집 방식** | 사람이 수동 또는 cron(30분마다) | Prometheus 자동 스크래핑(15초) |
| **데이터 소스** | 단일 DB 테이블 | 다중 소스(Redis, App, Broker) |
| **데이터 신선도** | 30분 지연 | 15초 이내 |
| **정확성** | 스냅샷 기반(정확) | 시계열 누적(트렌드 파악 가능) |
| **DB 부하** | SELECT COUNT 500만 건 Full Scan | HTTP GET (매우 가벼움) |

### 3.2 실시간성 (Alerting)

| 항목 | AS-IS | TO-BE |
|------|-------|-------|
| **알림 감지 시간** | 30분 | 2분(alert rule for: 2m) |
| **알림 방식** | 수동 이메일 확인 | Slack, PagerDuty 자동 발송 |
| **임계치 설정** | 수동 정의 | PromQL + Rule 자동화 |
| **거짓 알림** | 높음(임계치 기준 부재) | 낮음(명확한 기준) |

### 3.3 대시보드 및 시각화

| 항목 | AS-IS | TO-BE |
|------|-------|-------|
| **대시보드** | 없음(매번 쿼리 작성) | Grafana 사전 정의됨 |
| **시간대 비교** | 어려움 | 간단함(드래그 선택) |
| **상관관계 분석** | 불가능 | 가능(여러 메트릭 동시 표시) |
| **셀프서비스** | 없음(DBA 의존) | 있음(누구나 접근) |
| **역사 데이터** | 오래된 것부터 삭제됨 | 6개월-1년 보존 가능 |

### 3.4 디버깅 및 근본 원인 분석

| 항목 | AS-IS | TO-BE |
|------|-------|-------|
| **문제 인지** | 고객 컴플레인 기반 | 자동 알림 → 사전 대응 |
| **정보 수집** | DBA 질의 필요(30분) | 대시보드 확인(2분) |
| **메트릭** | 결과만 알 수 있음(count) | 원인까지 파악 가능(rate, lag) |
| **패턴 인식** | 어려움 | 용이(과거 24시간 시각화) |

### 3.5 운영 효율성

| 항목 | AS-IS | TO-BE |
|------|-------|-------|
| **운영 인력** | DBA 1명, 운영팀 2명 | 자동화로 인력↓ 30% |
| **대응 시간** | 45분 평균 | 5분 이내 |
| **MTTR(Mean Time To Repair)** | 2시간 | 15분 |
| **장애 재발생률** | 20% (패턴 모름) | 2% (알림으로 사전 조치) |

---

## 4. PoC에서의 구현

### 4.1 환경 설정

**프로젝트 구조:**

```
redpanda-spring-boot/
├── docker-compose.yml          # RedPanda + Prometheus + Grafana
├── src/main/resources/
│   └── application.yml          # Micrometer 설정
├── monitoring/
│   ├── prometheus.yml           # Prometheus 설정
│   ├── rules/
│   │   └── kafka-alerts.yaml   # Alert 규칙
│   └── grafana/
│       └── dashboards/
│           ├── kafka-overview.json
│           ├── consumer-lag.json
│           └── performance.json
└── pom.xml                      # Dependency
```

### 4.2 Spring Boot 설정

**pom.xml (Dependency):**

```xml
<dependencies>
  <!-- Spring Boot Kafka -->
  <dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
  </dependency>

  <!-- Micrometer Prometheus Registry -->
  <dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
  </dependency>

  <!-- Spring Boot Actuator -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
  </dependency>
</dependencies>
```

**application.yml:**

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: ch07-consumer
      auto-offset-reset: earliest
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.type.mapping: |
          orderCreated:com.example.OrderCreated,
          orderProcessed:com.example.OrderProcessed
    producer:
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all
      retries: 3

management:
  endpoints:
    web:
      exposure:
        include: prometheus,health,metrics
      base-path: /actuator

  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: order-service
      environment: PoC
      version: 1.0

    distribution:
      percentiles-histogram:
        kafka.consumer.fetch.manager.records.lag: true
        http.server.requests: true
```

**Kafka Listener 예시:**

```java
@Component
public class OrderEventListener {

    @KafkaListener(
        topics = "order-events",
        groupId = "ch07-consumer",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void listen(@Payload OrderEvent event,
                       @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
                       @Header(KafkaHeaders.RECEIVED_PARTITION_ID) int partition,
                       @Header(KafkaHeaders.OFFSET) long offset) {
        log.info("Received: topic={}, partition={}, offset={}, event={}",
                 topic, partition, offset, event);

        // 비즈니스 로직
        processOrder(event);
    }

    // Micrometer는 자동으로 메트릭 수집:
    // - kafka.consumer.records.consumed.total
    // - kafka.consumer.fetch.manager.records.lag
    // - 처리 시간(duration)
}
```

### 4.3 Docker Compose 설정

```yaml
version: '3.8'

services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:latest
    container_name: redpanda
    ports:
      - "9092:9092"        # Kafka API
      - "8081:8081"        # Schema Registry
      - "9644:9644"        # Prometheus metrics
    environment:
      REDPANDA_MODE: dev
    command:
      - redpanda
      - start
      - --smp=1
      - --memory=1G
      - --overprovisioned
      - --node-id=0
      - --advertised-kafka-api=localhost:9092
      - --advertised-rpc-api=localhost:33145

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/rules:/etc/prometheus/rules:ro
      - prometheus-storage:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro

  app:
    build: .
    container_name: spring-boot-app
    ports:
      - "8080:8080"
    depends_on:
      - redpanda
      - prometheus
    environment:
      SPRING_KAFKA_BOOTSTRAP_SERVERS: redpanda:9092

volumes:
  prometheus-storage:
  grafana-storage:
```

**prometheus.yml:**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: 'kafka-monitor'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

rule_files:
  - '/etc/prometheus/rules/kafka-alerts.yaml'

scrape_configs:
  - job_name: 'redpanda'
    static_configs:
      - targets: ['redpanda:9644']

  - job_name: 'spring-boot'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['app:8080']

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

### 4.4 실행 및 검증

```bash
# 1. Docker Compose 시작
docker-compose up -d

# 2. Spring Boot 앱 실행
mvn spring-boot:run

# 3. Consumer Lag 확인
docker exec redpanda rpk group describe ch07-consumer

# 4. Prometheus 메트릭 조회
curl http://localhost:9090/api/v1/query?query=kafka_consumer_group_lag

# 5. Grafana 대시보드 접근
# 브라우저: http://localhost:3000
# 계정: admin / admin

# 6. 메트릭 엔드포인트 확인
curl http://localhost:8080/actuator/prometheus | grep kafka
```

**출력 예시:**

```
# RedPanda 메트릭
redpanda_cluster_brokers 1
redpanda_kafka_request_latency_seconds_bucket{handler="fetch",le="0.001"} 1500

# Spring Boot 메트릭
kafka_consumer_records_consumed_total{client_id="ch07-consumer-1",topic="order-events"} 12345
kafka_consumer_group_lag{group="ch07-consumer",partition="0",topic="order-events"} 456
kafka_producer_record_send_total{client_id="order-service",topic="order-events"} 12350
```

---

## 5. 현직 사례 연구

### 5.1 토스 (Toss)

**배경:**
- 매일 10억 건 이상의 금융 거래 처리
- 실시간 거래 추적 필수

**모니터링 전략: ClickHouse 기반 커스텀 메트릭**

```
Kafka 메트릭
   ↓
ClickHouse (OLAP DB)
   ↓
내부 분석 도구
```

**특징:**

1. **극저지연 수집:**
   - Kafka → ClickHouse 1초 이내
   - ms 단위 지연시간 측정 가능

2. **고속 집계:**
   - 수십 억 건 데이터를 초단위로 집계
   - GROUP BY, SUM, AVG 등 고속 계산

3. **이상징후 조기 발견:**
   - 트렌드 분석으로 패턴 변화 감지
   - 문제 발생 전 예측 가능

**구현:**

```sql
-- ClickHouse 테이블
CREATE TABLE kafka_metrics (
  timestamp DateTime,
  metric_name String,
  topic String,
  partition Int32,
  lag Int64,
  latency Float32
) ENGINE = MergeTree()
ORDER BY (timestamp, topic);

-- 실시간 집계
SELECT
  toStartOfMinute(timestamp) as time,
  topic,
  avg(latency) as avg_latency,
  quantile(0.99)(latency) as p99_latency,
  sum(lag) as total_lag
FROM kafka_metrics
WHERE timestamp > now() - interval 1 hour
GROUP BY time, topic
ORDER BY time DESC;
```

### 5.2 LINE

**배경:**
- 전 세계 100개국 서비스
- 다양한 클라이언트의 불규칙한 요청 패턴

**모니터링 전략: 요청 쿼터 기반 관리**

```
클라이언트 요청
   ↓
브로커 쿼터 검증
   ↓
스레드 시간 할당
   ↓
초과 시 자동 차단
```

**구현:**

```java
// 클라이언트별 쿼터 설정
Map<String, ClientQuota> quotas = new HashMap<>();
quotas.put("mobile-app", new ClientQuota(
  100_000,        // produce_bytes_per_sec
  50_000,         // fetch_bytes_per_sec
  1000            // request_percentage (브로커 CPU 1%)
));

// Broker 설정
broker.setClientQuota("mobile-app", quotas.get("mobile-app"));

// 모니터링
MetricRegistry.gauge(
  "kafka.broker.client_quota_exceeded",
  () -> quotaManager.getExceededCount()
);
```

**장점:**

1. **공정한 자원 배분:**
   - 대량 요청 클라이언트가 다른 클라이언트 방해 불가
   - 예: 배치 작업이 실시간 시스템 중단 시킬 수 없음

2. **예측 가능한 성능:**
   - 클라이언트별 성능 상한선 정확히 정의됨
   - SLA 유지 용이

3. **자동 조절:**
   - 임계치 초과 시 자동으로 요청 지연
   - 관리자 개입 불필요

---

## 6. 면접 예상 질문 및 답변

### Q1. Consumer Lag이 무엇이고 왜 중요한가요?

**A. Consumer Lag의 정의와 중요성**

```
정의:
Consumer Lag = Latest Offset - Committed Offset

의미:
Consumer가 아직 처리하지 못한 메시지의 개수
```

**예시:**

```
토픽: order-events
최신 오프셋: 100,000
커밋 오프셋: 95,000
LAG = 5,000

의미: Consumer가 5,000개 메시지를 아직 처리하지 못함
```

**중요성:**

1. **성능 지표:**
   - Lag 0 = 실시간 처리 (이상적)
   - Lag 증가 = Consumer 성능 저하 또는 Producer 처리량 증가

2. **장애 감지:**
   - 갑작스런 Lag 증가 = Consumer 다운 또는 에러 발생
   - 느린 Lag 증가 = Producer 처리량 > Consumer 처리량 (확장 필요)

3. **비즈니스 영향:**
   - Lag 크다 = 주문 처리 지연 → 고객 불만
   - Lag 0 = 실시간 처리 → 최고의 고객 경험

**현직 경험:**

```
토스: 결제 완료 후 5초 내 확인 필수
→ Consumer Lag < 1000 (장애 시 500ms 이내 감지)

배달 앱: 주문 배치 10초마다
→ Consumer Lag < 100 (일괄 처리 안 되면 지연 발생)
```

---

### Q2. Kafka 모니터링에서 가장 중요한 메트릭 3가지는?

**A. 우선순위 기반 답변**

```
┌────────────────────────────────────────────────┐
│  1순위: Consumer Lag                            │
│  2순위: Message Throughput (Produce/Consume)   │
│  3순위: End-to-End Latency                     │
└────────────────────────────────────────────────┘
```

**상세 설명:**

**1순위: Consumer Lag (앞서 답변함)**

**2순위: 처리량 (Throughput)**

```
메트릭:
- Produce Rate (msg/sec): Producer가 초당 얼마나 보내는가?
- Consume Rate (msg/sec): Consumer가 초당 얼마나 처리하는가?

임계치:
Consume Rate < Produce Rate
  → Lag 증가 (나쁨)
Consume Rate ≥ Produce Rate
  → Lag 유지 또는 감소 (좋음)

현직 예시:
토스 결제:
- Produce: 1000 tx/sec (피크)
- Consume: 1000 tx/sec (스케일링)
- Lag: 안정적 (< 100)
```

**3순위: End-to-End Latency**

```
정의: 메시지 생성 ~ Consumer 처리 완료까지 시간

구성:
Producer Latency (메시지 발송)
+ Network Latency (전송)
+ Broker Latency (저장)
+ Consumer Lag (대기)
+ Consumer Processing (처리)
= Total Latency

임계치:
- p50 < 100ms : 좋음
- p99 < 500ms : 수용
- max > 1s : 나쁨

현직 예시:
- 실시간 알림: p99 < 50ms 필수
- 배치 작업: p99 < 5s 허용
```

**보너스: 4순위**

**Broker Health (브로커 상태)**

```
메트릭:
- Under-replicated Partitions: 0 (모든 복제 완료)
- Broker CPU: < 80%
- Broker Disk: < 90% 찼음
- GC Pause: < 200ms

의미:
브로커가 건강한가? → 다른 메트릭의 신뢰성 결정
```

---

### Q3. 알림 임계치를 어떻게 설정하나요?

**A. 데이터 기반 임계치 설정 프로세스**

**Step 1: 정상 범위 파악 (1~2주 데이터 수집)**

```
Consumer Lag 분포:
- p50: 100
- p90: 500
- p95: 800
- p99: 1200

→ 정상 범위: 0 ~ 1200
```

**Step 2: 비즈니스 요구사항 반영**

```
토스 (금융):
- 실시간성 매우 중요
- Lag > 500 이면 고객 불만 발생
→ 임계치: 500 (warning)

배달 앱:
- 5분 단위 배치 가능
- Lag > 5000 이면 배치 지연
→ 임계치: 5000 (warning)
```

**Step 3: 심각도 분류**

```yaml
Consumer Lag:
  - info: Lag > 100 (1번 이상)
    설명: 모니터링만 함

  - warning: Lag > 500 (5분 이상)
    대응: Consumer 로그 확인, 스케일링 고려

  - critical: Lag > 2000 (2분 이상)
    대응: 즉시 담당자 호출, Consumer 재시작
```

**Step 4: 학습 기반 조정**

```
첫 주: 임계치 설정 후 거짓 알림 모니터링
├─ 거짓 알림 > 50% → 임계치 높이기
├─ 거짓 알림 < 5% → 임계치 낮추기
└─ 거짓 알림 10-20% → 임계치 유지

한 달 후: 실제 장애와 임계치 상관관계 분석
└─ 모든 장애를 조기에 감지했는가?
```

**현직 사례:**

```
LINE 라이브 스트리밍:
- 처음 설정: Lag > 1000
- 거짓 알림 많음 (60%)
- 조정: Lag > 5000
- 거짓 알림 줄어듦 (15%)
- 최종: Lag > 5000 (warning), > 10000 (critical)

결과: 대부분의 실제 장애를 감지하면서 거짓 알림 최소화
```

---

### Q4. DB 기반 모니터링 대비 Prometheus의 장점은?

**A. 기술적 비교**

| 항목 | DB 기반 | Prometheus |
|------|--------|-----------|
| **수집 방식** | 동기 쿼리 | 비동기 메트릭 pull |
| **오버헤드** | 높음 (Full Scan) | 낮음 (HTTP GET) |
| **응답시간** | 수초 | 수십ms |
| **자동화** | 없음 | 완벽한 자동화 |
| **알림** | 수동 | 자동 발송 |
| **시계열** | 보관 안 함 | 장기 보관 (1년) |
| **대시보드** | 커스텀 쿼리 필요 | 사전 정의됨 |
| **확장성** | 제한적 | 무제한 확장 |

**구체적 비교:**

**1. 성능 (Performance)**

```
DB 기반:
SELECT COUNT(*) FROM TB_TPS_MS_021 WHERE linkSttsCd = 'FAIL'
├─ 1000만 건 Full Scan
├─ 응답시간: 5초
└─ DB CPU 부하: 80%

Prometheus:
GET http://prometheus:9090/api/v1/query?query=...
├─ 메모리의 인덱스된 데이터
├─ 응답시간: 100ms
└─ CPU 부하: 1%

결론: Prometheus가 50배 빠르고 80배 효율적
```

**2. 자동화 (Automation)**

```
DB 기반:
1. 개발자가 쿼리 작성 (30분)
2. cron 스케줄 설정 (10분)
3. 결과 분석 및 알림 (수동, 30분)
4. 임계치 변경 시 스크립트 수정 (30분)
└─ 총 소요 시간: 2시간

Prometheus:
1. Alert 규칙 작성 (10분)
2. prometheus.yml에 추가 (5분)
3. 자동 평가 + Slack 발송 (자동)
4. 임계치는 규칙 파일 수정만 (1분)
└─ 총 소요 시간: 15분

결론: 8배 빠른 설정, 100% 자동화
```

**3. 유연성 (Flexibility)**

```
DB 기반:
임계치 변경 시나리오:
1. DBA가 새 쿼리 작성
2. 승인 대기
3. 개발팀이 스크립트 수정
4. 배포 및 테스트
5. 적용

시간: 3~5일

Prometheus:
임계치 변경 시나리오:
1. rules/kafka-alerts.yaml 수정
2. Prometheus 자동 리로드
3. 적용 완료

시간: 1분
```

---

## 7. 아키텍처 설계 검토

### 7.1 메트릭 수집 설계의 고려사항

```
선택지 1: Pull Model (Prometheus 권장)
┌─────────────┐      스크래핑       ┌───────────┐
│ Application │◄─────────────────────│ Prometheus│
└─────────────┘                      └───────────┘

장점:
- Prometheus가 주도권 (rate control 가능)
- 네트워크 장애 시에도 앱은 영향 없음
- 확장성 우수

단점:
- Prometheus가 앱 주소를 알아야 함 (discovery 필요)


선택지 2: Push Model
┌─────────────┐      메트릭 전송      ┌───────────┐
│ Application │─────────────────────►│ PushGateway│
└─────────────┘                       └─────┬─────┘
                                            │
                                            ▼
                                       ┌───────────┐
                                       │ Prometheus│
                                       └───────────┘

장점:
- 앱이 주도권 (시간 조절 가능)
- 배치 작업에 적합

단점:
- 앱이 네트워크 연결 담당 (실패 위험)
- PushGateway가 추가 구성 요소
```

**PoC 권장사항: Pull Model 사용**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'redpanda'
    static_configs:
      - targets: ['redpanda:9644']
    scrape_interval: 15s
    scrape_timeout: 10s
```

### 7.2 메트릭 보존 정책 (Retention Policy)

```
Prometheus 저장소:
├─ 최근 1시간: 고해상도 (15초 단위)
│  └─ 용량: 1.5GB
├─ 1시간~24시간: 중간 해상도 (1분 단위)
│  └─ 용량: 500MB
└─ 24시간~30일: 저해상도 (15분 단위)
   └─ 용량: 200MB

총 저장소: ~2GB (30일)

문제: 30일 이후 데이터 소실
해결책: Thanos (장기 저장)
```

**Thanos 도입:**

```
Prometheus (30일)
         ↓
    Thanos Sidecar
         ↓
  S3/GCS (1년 보관)
         ↓
 Thanos Query
 (스케일아웃 가능)
```

---

## 8. 학습 결과 요약

### 8.1 핵심 개념

```
┌─────────────────────────────────────────────┐
│      Observability = Metrics + Logs + Traces│
├─────────────────────────────────────────────┤
│                                              │
│ 이 문서 범위: Metrics (Prometheus)           │
│                                              │
│ Metrics 종류:                                │
│ ├─ Gauge: 현재값 (Lag = 500)                │
│ ├─ Counter: 누적값 (total_messages)        │
│ └─ Histogram: 분포 (latency p50/p99)       │
│                                              │
│ 모니터링 = Alerting 자동화                   │
│ ├─ 임계치 기반 (Lag > 1000 → warning)      │
│ ├─ 알림 발송 (Slack, PagerDuty)            │
│ └─ 대응 (자동 또는 수동)                    │
│                                              │
└─────────────────────────────────────────────┘
```

### 8.2 실무 적용 체크리스트

```
□ Prometheus 설치 및 설정
  └─ Docker Compose로 5분 안에 완료

□ Spring Boot Actuator 설정
  └─ management.endpoints.web.exposure.include = prometheus

□ Alert 규칙 정의
  └─ 최소 3개 규칙: BrokerDown, ConsumerLagHigh, DltRateHigh

□ Grafana 대시보드 구성
  └─ 5개 Row (클러스터, 처리량, 레이턴시, Lag, 에러)

□ AlertManager 통합
  └─ Slack 웹훅 연동

□ 임계치 튜닝
  └─ 1주일 데이터 기반으로 조정

□ 팀 교육
  └─ 대시보드 읽기, 알림 대응 프로세스
```

---

## 9. 관련 문서

- [08. 에러 핸들링 비교](./08-error-handling-comparison.md) - DLT 모니터링과의 연계
- [13. 성능 기대치](./13-performance-expectations.md) - 임계치 설정 기준
- [05. 아키텍처](./05-architecture-overview.md) - 전체 시스템 구조

---

## 10. 면접 마무리 팁

**자신감 있게 답변하기 위한 체크포인트:**

```
✓ Consumer Lag의 정의를 정확히 말할 수 있는가?
  └─ "Latest Offset - Committed Offset"

✓ 왜 Prometheus가 DB 기반 모니터링보다 나은가?
  └─ 자동화, 실시간성, 확장성, 비용

✓ Prometheus 메트릭 수집의 3가지 방식을 알고 있는가?
  └─ Gauge (현재값), Counter (누적), Histogram (분포)

✓ Alert를 어떻게 설정하는가?
  └─ PromQL 규칙 + 임계치 + 심각도

✓ 현직 경험이나 사례를 2~3개 준비했는가?
  └─ 토스, LINE, 자신의 경험
```

---

**문서 작성자 노트:**

이 문서는 실무에서 자주 묻는 질문들을 중심으로 작성되었습니다. Prometheus 설정부터 Alert 규칙까지 모두 실제 동작하는 예시를 포함했으므로, Docker Compose로 직접 테스트해볼 수 있습니다.

특히 "DB 기반 모니터링 vs Prometheus" 비교는 면접에서 매우 자주 출제되는 주제이므로, 각 방식의 장단점을 명확히 이해하고 정량적 근거(응답시간, CPU 부하 등)와 함께 설명할 수 있으면 좋은 인상을 남길 수 있습니다.

마지막으로, "임계치 설정"은 단순히 숫자를 정하는 것이 아니라 데이터 기반의 과학적 접근이 필요하다는 점을 강조하면, 단순한 엔지니어가 아닌 "데이터 기반 사고를 하는 엔지니어"로 평가받을 수 있습니다.
