# Connectors: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. Redpanda Connect vs Kafka Connect — 실제로 무엇이 다른가

### 왜 이 질문이 중요한가

팀에서 커넥터 도입을 결정할 때 가장 먼저 나오는 질문이 "Kafka Connect를 쓸까, Redpanda Connect를 쓸까"다. 단순히 "Redpanda를 쓰면 Redpanda Connect"라고 대답하면 틀리는 경우가 많다. 두 프레임워크는 설계 철학 자체가 다르고, 처리량·레이턴시·운영 비용 측면에서 트레이드오프가 명확하다.

### 답변

**아키텍처 차이가 성능 특성을 결정한다.**

Kafka Connect는 JVM 위에서 동작하며 Worker 프로세스가 커넥터 플러그인을 JAR 형태로 로드한다. 분산 모드에서는 Worker 간 상태를 내부 Kafka 토픽(`config`, `offset`, `status`)으로 공유하므로, 수평 확장이 자연스럽지만 Worker 추가 시 리밸런싱 오버헤드가 발생한다. 반면 Redpanda Connect(구 Benthos)는 Go 단일 바이너리(약 20MB)로, 별도 코디네이터 없이 각 인스턴스가 독립적으로 동작한다.

| 항목 | Kafka Connect | Redpanda Connect |
|---|---|---|
| 런타임 | JVM (힙 1GB+ 권장) | Go 바이너리 (메모리 수십 MB) |
| 처리량 | 높음, 파티션 병렬화로 선형 확장 | 높음, 고루틴 기반 경량 병렬 처리 |
| 레이턴시 | GC 일시 정지로 p99 불안정할 수 있음 | GC 없음, p99 레이턴시 일관성 우수 |
| 변환 표현력 | SMT(Single Message Transform)로 단순 변환만 지원 | Bloblang으로 복잡한 변환·라우팅 가능 |
| 커넥터 생태계 | Confluent Hub — 수백 개 프로덕션 검증 플러그인 | 300개 내장, 단 JAR 플러그인 없음 |
| 운영 복잡도 | Worker 클러스터 관리 필요 | 단일 바이너리, Helm으로 즉시 배포 |

**선택 기준:** 이미 Confluent 생태계의 특정 Sink 커넥터(예: Snowflake Sink, Elasticsearch Sink)를 써야 한다면 Kafka Connect가 맞다. 새로 파이프라인을 설계하거나 변환 로직이 복잡한 경우, 또는 컨테이너 메모리가 제한된 환경이라면 Redpanda Connect가 유리하다.

---

## Q2. Bloblang vs jq — 복잡한 변환에서 어디까지 가능한가

### 왜 이 질문이 중요한가

데이터 파이프라인에서 메시지 변환은 피할 수 없다. 면접에서 "Redpanda Connect의 변환 기능을 어떻게 평가하는가"라고 물으면, Bloblang의 표현력과 한계를 명확히 설명할 수 있어야 한다. jq와 비교하면 각각의 적합한 사용처가 분명해진다.

### 답변

**Bloblang은 파이프라인 내장 DSL, jq는 범용 JSON 프로세서다.**

Bloblang은 Redpanda Connect 파이프라인 안에서 실행되도록 설계되어, 메시지 메타데이터 접근(`@`), 조건 분기, 에러 핸들링이 자연스럽게 통합된다.

```yaml
# Bloblang: 중첩 필드 추출 + 조건 분기 + 메타데이터 참조
root.order_id = this.id
root.amount = this.payment.total.amount
root.status = if this.payment.status == "completed" { "success" } else { "pending" }
root.source_topic = @kafka_topic
```

jq는 같은 작업을 할 수 있지만, 파이프라인 메타데이터(`@kafka_topic`)에 접근하려면 별도 처리가 필요하다.

**Bloblang이 jq보다 앞서는 경우:**
- 메시지 메타데이터(오프셋, 토픽, 파티션) 참조
- 에러 포착 후 DLQ로 라우팅하는 패턴 (`catch`, `try`)
- 여러 입력 메시지를 배치 처리하는 집계

**Bloblang의 한계:**
- 재귀 처리나 복잡한 트리 순회는 표현이 어렵다
- 단위 테스트 도구가 부족하여 변환 로직이 길어지면 검증이 어렵다
- if-else 3단 이상으로 중첩되면 YAML 가독성이 급격히 나빠진다. 이 시점에서는 변환 로직을 애플리케이션 코드로 옮기는 것이 맞다

```yaml
# 3단 중첩 — 이 이상이면 애플리케이션 코드로 이동
root.tier = if this.score >= 90 { "gold" }
            else if this.score >= 70 { "silver" }
            else { "bronze" }
```

---

## Q3. Source/Sink 커넥터에서 Exactly-once는 실현 가능한가

### 왜 이 질문이 중요한가

"정확히 한 번 처리"는 분산 시스템 면접의 단골 주제다. Kafka Streams나 트랜잭셔널 프로듀서 맥락에서는 설명하기 쉽지만, 커넥터 계층에서의 Exactly-once는 훨씬 조건이 까다롭다. 면접관이 "커넥터에서도 EOS가 가능한가요?"라고 물을 때, 조건과 한계를 정확히 설명할 수 있어야 한다.

### 답변

**커넥터에서 EOS는 가능하지만, 외부 시스템의 협력이 필수 조건이다.**

Redpanda/Kafka 내부에서는 트랜잭셔널 API로 produce-commit을 원자적으로 처리할 수 있다. 문제는 외부 시스템이다. Source 커넥터가 DB에서 읽어 토픽에 쓰는 시나리오를 보자.

```
[DB] --읽기--> [Source Connector] --produce--> [Redpanda]
                     ↕ offset 저장
```

메시지를 produce한 뒤 오프셋을 저장하기 전에 커넥터가 죽으면, 재시작 시 같은 레코드를 다시 produce한다. 이것이 at-least-once다.

**EOS 달성 조건:**
1. Source 측: Redpanda의 트랜잭셔널 프로듀서를 사용하여 produce와 오프셋 저장을 같은 트랜잭션으로 묶는다. Kafka Connect는 `exactly.once.source.support=enabled` 옵션으로 이를 지원한다.
2. Sink 측: 외부 시스템이 멱등 쓰기(idempotent write) 또는 트랜잭션을 지원해야 한다. PostgreSQL은 `INSERT ... ON CONFLICT DO NOTHING`으로, Elasticsearch는 `_id` 기반 멱등 upsert로 중복을 제거할 수 있다. S3나 HDFS처럼 append-only 시스템은 중복 레코드가 쌓일 수 있다.

**Redpanda Connect의 경우:** at-least-once가 기본이며, EOS는 Sink 시스템의 멱등성으로 보완하는 방식이다. 커넥터 자체에서 트랜잭션을 제공하지 않으므로, 중복 방지는 외부 시스템의 책임이다.

---

## Q4. 커넥터 장애 복구 — 재시작 시 중복 없이 이어받으려면

### 왜 이 질문이 중요한가

프로덕션에서 커넥터 Pod가 재시작되는 일은 흔하다. OOM, 네트워크 단절, 배포 롤링 업데이트 등 원인은 다양하다. "재시작하면 어떻게 되나요?"라는 질문에 오프셋 저장 방식과 중복 처리 전략을 연결해서 답해야 한다.

### 답변

**복구 안전성은 오프셋 저장 타이밍과 Sink의 멱등성으로 결정된다.**

Redpanda Connect는 input → processor → output이 성공한 뒤에 input의 ack를 보낸다. Kafka 입력이라면 ack = 오프셋 커밋이다. 따라서 output(Sink)에 쓰기 성공 전에 프로세스가 죽으면 재시작 후 같은 메시지를 다시 읽는다 — at-least-once 보장이다.

```yaml
# Redpanda Connect 재시도 설정 예시
output:
  retry:
    output:
      http_client:
        url: https://api.example.com/events
    max_retries: 5
    backoff:
      initial_interval: 500ms
      max_interval: 10s
```

**중복 처리 방지 전략:**

1. Sink DB에 유니크 제약: 메시지 ID를 PK 또는 유니크 컬럼으로 사용
   ```sql
   INSERT INTO events (event_id, payload) VALUES ($1, $2)
   ON CONFLICT (event_id) DO NOTHING;
   ```

2. 처리 완료 상태 테이블: `processed_events(event_id, processed_at)` 형태로 이미 처리한 ID를 추적 (08-redpanda Ch03 패턴과 동일)

3. Kafka 컨슈머 오프셋 관리: `auto.commit.enabled=false`로 설정하고 Sink 처리 완료 후 수동 커밋. Redpanda Connect는 이를 자동으로 처리하므로 명시적 설정 불필요

**DLQ 연동:** 재시도 소진 후에도 실패하면 DLQ 토픽으로 라우팅하여 메인 파이프라인이 멈추지 않도록 한다.

```yaml
output:
  fallback:
    - http_client:
        url: https://api.example.com/events
    - kafka_franz:
        topic: events-dlq
        metadata:
          include_patterns: [".*"]
```

---

## Q5. Streams Mode vs 단일 파이프라인 — 언제 Streams Mode를 선택하는가

### 왜 이 질문이 중요한가

Redpanda Connect의 Streams Mode는 단일 프로세스에서 여러 파이프라인을 동시에 관리하는 기능이다. 단순히 "여러 파이프라인이 필요할 때"라는 대답은 불완전하다. 운영 복잡도와 리소스 공유 측면에서 구체적인 판단 기준을 갖춰야 한다.

### 답변

**Streams Mode는 파이프라인 수명주기를 런타임에 제어해야 할 때 선택한다.**

단일 파이프라인 모드(`rpk connect run pipeline.yaml`)는 파이프라인 변경 시 프로세스를 재시작해야 한다. Streams Mode(`rpk connect streams`)는 REST API로 파이프라인을 동적으로 추가·수정·삭제할 수 있다.

```bash
# Streams Mode 실행
rpk connect streams ./pipelines/

# 런타임에 파이프라인 추가 (재시작 없음)
curl -X POST http://localhost:4195/streams/new-pipeline \
  -d @new-pipeline.yaml

# 파이프라인 목록 조회
curl http://localhost:4195/streams
```

**Streams Mode를 선택하는 기준:**

| 상황 | 선택 |
|---|---|
| 파이프라인이 1~3개, 변경 빈도 낮음 | 단일 파이프라인 (Pod별 배포) |
| 파이프라인이 10개 이상, 동적 추가 필요 | Streams Mode |
| 파이프라인별 독립적인 스케일아웃 필요 | 단일 파이프라인 (HPA 적용 가능) |
| 파이프라인 간 리소스(메모리, CPU) 공유로 비용 절감 | Streams Mode |
| 파이프라인 하나의 장애가 다른 파이프라인에 영향 주면 안 될 때 | 단일 파이프라인 |

**핵심 트레이드오프:** Streams Mode는 운영 편의성을 높이지만, 한 파이프라인의 메모리 누수나 CPU 스파이크가 같은 프로세스의 다른 파이프라인에 영향을 줄 수 있다. 격리가 중요한 프로덕션 환경이라면 파이프라인별 Pod 분리가 더 안전하다.
