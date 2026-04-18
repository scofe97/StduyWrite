# 20. JDBC Source Connector 데이터 파이프라인

컬리 데이터서비스팀의 JDBC Source Connector 쿼리 기반 CDC 사례 분석

---

> 출처: [컬리 데이터서비스팀의 Kafka Connect 파이프라인](https://helloworld.kurly.com/blog/kafka-connect-pipeline/)

> **사전 지식**: [01-source-sink-patterns.md](../../07-connectors/01-source-sink-patterns.md), [06-docker-deployment.md](../../07-connectors/06-docker-deployment.md) 참조

## §1. 배경과 요구사항

컬리 데이터서비스팀은 여러 DB의 변경 데이터를 Kafka로 추출하는 데이터 파이프라인을 구축해야 했다. 주요 요구사항은 다음과 같다:

1. **다양한 DB 지원**: MySQL, PostgreSQL, Oracle 등 이기종 DB에서 데이터 추출
2. **코드 변경 최소화**: 소스 애플리케이션 수정 없이 데이터 파이프라인 구축
3. **변경 데이터 추적**: INSERT, UPDATE 이벤트를 준실시간으로 Kafka 토픽에 적재
4. **운영 편의성**: DB 관리팀의 WAL/binlog 권한 없이도 도입 가능

Debezium CDC가 이상적이지만, DB 설정 변경(복제 권한, WAL 설정)이 어려운 레거시 환경이 있었기 때문에 JDBC Source Connector를 보조 운영 도구로 선택했다.

---

## §2. Kafka Connect 아키텍처

```
워커(Worker) — Kafka Connect 프로세스 (JVM)
  └─ 커넥터(Connector) — 파이프라인 정의 + 태스크 관리
      └─ 태스크(Task) × N개 — 실제 데이터 추출/삽입 스레드
          └─ Transform(SMT) → Converter → Kafka
```

| 구성 요소 | 역할 | 배포 모드 |
|----------|------|----------|
| **Worker** | Kafka Connect 프로세스 (JVM) | Standalone / Distributed |
| **Connector** | Source(DB→Kafka) 또는 Sink(Kafka→DB) 파이프라인 정의 | 커넥터 플러그인 |
| **Task** | 병렬 처리 단위. `tasks.max`로 병렬도 조절 | 커넥터 내부 스레드 |
| **SMT** | Single Message Transform — 메시지 변환 | 커넥터 설정 |
| **Converter** | 직렬화 포맷 변환 (JSON, Avro 등) | 워커 설정 |

**Standalone vs Distributed 모드:**

Standalone 모드는 단일 프로세스에서 동작하며 개발/테스트에 적합하다. Distributed 모드는 여러 워커가 클러스터를 형성하여 태스크를 분담하고, 워커 장애 시 자동으로 태스크를 재할당한다. 프로덕션에서는 Distributed 모드가 표준이다.

---

## §3. JDBC Source Connector 쿼리 모드

### §3.1 4가지 쿼리 모드

| 모드 | WHERE 조건 | 감지 가능 | 감지 불가 | 적합 테이블 |
|------|-----------|----------|----------|-----------|
| **Bulk** | 없음 (전체 SELECT) | 모든 변경 | 삭제 | 작은 코드 테이블 |
| **Incrementing** | `id > 오프셋` | INSERT | UPDATE, DELETE | 불변 로그 테이블 |
| **Timestamp** | `ts > 오프셋` | INSERT, UPDATE | DELETE, 동일 ts 충돌 | 갱신 추적 가능 테이블 |
| **Timestamp+Incrementing** | `ts > 오프셋 OR (ts = 오프셋 AND id > 오프셋)` | INSERT, UPDATE | DELETE | **가장 안전한 선택** |

**Bulk 모드**는 매 폴링마다 테이블 전체를 SELECT한다. 작은 코드 테이블(상태 코드, 카테고리 등)에는 적합하지만, 대용량 테이블에서는 DB 부하가 크다.

**Incrementing 모드 내부 동작:**

```
1. 첫 폴링: SELECT * FROM table ORDER BY id ASC
2. 오프셋 저장: 마지막 처리한 id 값
3. 다음 폴링: SELECT * FROM table WHERE id > {오프셋} ORDER BY id ASC
4. PK가 auto increment이므로 새 행만 캡처
   → 기존 행의 UPDATE는 id가 변하지 않으므로 감지 불가
```

**Timestamp 모드 내부 동작:**

```
1. 첫 폴링: SELECT * FROM table WHERE ts <= CURRENT_TIMESTAMP ORDER BY ts ASC
2. 오프셋 저장: 마지막 처리한 ts 값
3. 다음 폴링: SELECT * FROM table WHERE ts > {오프셋} AND ts <= CURRENT_TIMESTAMP ORDER BY ts ASC
4. UPDATE 시 ts가 갱신되면 캡처 가능
   → 동일 ts인 2개 행 중 1개만 처리하고 크래시 시 나머지 유실
```

**Timestamp+Incrementing 모드**는 두 가지를 조합하여 동일 타임스탬프 충돌 시 PK로 보완한다. 대부분의 프로덕션 환경에서 권장되는 모드다.

### §3.2 Custom Query 모드

기본 모드들은 단일 테이블에서 SELECT하지만, Custom Query 모드는 `query` 속성으로 임의 SQL을 지정할 수 있다.

```json
{
  "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
  "connection.url": "jdbc:mysql://db:3306/mydb",
  "mode": "timestamp+incrementing",
  "query": "SELECT a.id, a.order_no, a.amount, a.updated_at, b.product_name FROM orders a JOIN products b ON a.product_id = b.id WHERE a.status != 'DELETED'",
  "incrementing.column.name": "id",
  "timestamp.column.name": "updated_at"
}
```

Custom Query의 장점:
- JOIN으로 여러 테이블의 데이터를 하나의 토픽에 통합
- WHERE 조건으로 불필요한 데이터 필터링 (소프트 삭제 제외 등)
- 서브쿼리로 복잡한 비즈니스 로직 적용

Custom Query의 한계:
- **쿼리 복잡도가 DB 부하에 직접 영향**: 매 폴링마다 JOIN 쿼리 실행
- `table.whitelist`와 동시 사용 불가
- 쿼리 결과에 incrementing/timestamp 컬럼이 반드시 포함되어야 함

### §3.3 쿼리 모드별 내부 동작 타임라인

```
시간 →  10:00    10:01    10:02    10:03    10:04    10:05
        |--------|--------|--------|--------|--------|

Bulk:   [전체 SELECT]              [전체 SELECT]
        모든 행 전송                모든 행 재전송 (중복)

Incr:   [id>0]                     [id>3]
        id 1,2,3 전송              id 4,5 전송 (UPDATE 미감지)

TS:     [ts>10:00]                 [ts>10:01]
        ts=10:01 전송              ts=10:02,03 전송 (DELETE 미감지)

TS+I:   [ts>10:00 OR (ts=10:00    [ts>10:01 OR (ts=10:01
         AND id>0)]                 AND id>3)]
```

---

## §4. 데이터 누락 시나리오 3가지

### §4.1 Case 1: Delete/Update 감지 불가

```
10:01 - 배 데이터 INSERT (id=1, ts=10:01)
10:02 - 쿼리 실행: WHERE id > 0 → 배 캡처, 오프셋=id:1
10:03 - 배 데이터 DELETE (테이블에서 제거)
10:04 - 쿼리 실행: WHERE id > 1 → 빈 결과
         → 삭제 이벤트 감지 불가 (Incrementing, Timestamp 모두)
```

**해결책:**
- 소프트 삭제(`deleted_at` 컬럼) + Timestamp 모드 사용
- 또는 Debezium CDC로 binlog/WAL에서 DELETE 이벤트 직접 캡처

JDBC Source Connector는 "현재 상태의 스냅샷"을 주기적으로 캡처하는 방식이므로, 두 스냅샷 사이에 발생한 삭제는 구조적으로 감지할 수 없다.

### §4.2 Case 2: 한 주기 내 다중 변경

```
10:01 - 배 INSERT (ts=10:01)
10:02 - 배 DELETE
10:02 - 사과 INSERT (ts=10:02)
10:05 - 쿼리 실행: WHERE ts > 10:00
         → 사과만 존재 (배는 이미 삭제됨)
         → 배의 INSERT→DELETE 이력 완전 누락
```

근본 원인은 쿼리 기반 CDC가 "현재 상태의 스냅샷"만 볼 수 있다는 점이다. 두 폴링 사이에 생성되고 삭제된 행은 흔적도 남기지 않는다.

### §4.3 Case 3: 장거리 트랜잭션으로 인한 영구 누락 (가장 위험)

```
10:02 - 트랜잭션 A 시작: 배 INSERT (ts=10:02) — 아직 COMMIT 안 됨
10:04 - 트랜잭션 B: 사과 INSERT (ts=10:04) — 즉시 COMMIT
10:05 - 쿼리 실행: WHERE ts > 10:00 AND ts <= 10:05
         → 배는 uncommitted이므로 불가시(invisible) → 사과만 캡처
         → 오프셋 = ts:10:04
10:06 - 트랜잭션 A COMMIT (배의 ts=10:02가 이제 가시적)
10:10 - 쿼리 실행: WHERE ts > 10:04 AND ts <= 10:10
         → 배(ts=10:02)는 오프셋(10:04)보다 이전 → 영구 누락!
```

이 시나리오가 가장 위험한 이유는 **데이터가 DB에 정상적으로 존재하지만 Kafka에는 영원히 전달되지 않기** 때문이다. 오프셋이 10:04로 전진한 이상, ts=10:02인 배 데이터는 어떤 후속 폴링에서도 조회되지 않는다.

---

## §5. timestamp.delay.interval.ms 방어 전략

```
설정: timestamp.delay.interval.ms = 120000 (2분)

10:05 쿼리 실행:
  기존 범위: ts > 오프셋 AND ts <= 10:05
  변경 범위: ts > 오프셋 AND ts <= 10:03  (현재시간 - 2분)
  → 사과(ts=10:04)는 아직 범위 밖 → 미캡처

10:10 쿼리 실행:
  변경 범위: ts > 오프셋 AND ts <= 10:08
  → 배(ts=10:02, 이제 committed) + 사과(ts=10:04) 모두 캡처 ✅
```

**원리**: 현재 시각에서 설정값만큼 뒤로 물러난 시점까지만 쿼리한다. 이 "지연 윈도우" 동안 미커밋 트랜잭션이 커밋될 시간을 벌어준다.

**트레이드오프:**

| 설정값 | 누락 위험 | 적재 지연 | 적합 상황 |
|--------|----------|----------|----------|
| 0 (기본값) | 높음 | 없음 | 트랜잭션 없는 INSERT-only 테이블 |
| 60초 | 중간 | 1분 | 짧은 트랜잭션 |
| 120초 (컬리) | 낮음 | 2분 | 일반적 OLTP |
| 300초+ | 매우 낮음 | 5분+ | 장거리 트랜잭션 |

**권장 공식**: `timestamp.delay.interval.ms = DB 트랜잭션 타임아웃 + 안전 마진`

예를 들어 DB 트랜잭션 타임아웃이 5분이라면, 7분(420,000ms)으로 설정한다. 이렇게 하면 타임아웃 내에 커밋되는 모든 트랜잭션의 데이터를 캡처할 수 있다.

---

## §6. 커넥터 설정 예시

### §6.1 Timestamp+Incrementing 모드 (권장)

```json
{
  "name": "jdbc-source-orders",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:mysql://db-host:3306/mydb?useSSL=true",
    "connection.user": "${file:/secrets/db.properties:user}",
    "connection.password": "${file:/secrets/db.properties:password}",

    "mode": "timestamp+incrementing",
    "incrementing.column.name": "id",
    "timestamp.column.name": "updated_at",
    "timestamp.delay.interval.ms": "120000",

    "table.whitelist": "orders,order_items",
    "topic.prefix": "db.mydb.",
    "poll.interval.ms": "5000",
    "batch.max.rows": "1000",
    "tasks.max": "2",

    "transforms": "addSource,routeByDate",
    "transforms.addSource.type": "org.apache.kafka.connect.transforms.InsertField$Value",
    "transforms.addSource.static.field": "source_table",
    "transforms.addSource.static.value": "orders",
    "transforms.routeByDate.type": "org.apache.kafka.connect.transforms.TimestampRouter",
    "transforms.routeByDate.topic.format": "${topic}-${timestamp}",
    "transforms.routeByDate.timestamp.format": "yyyy-MM-dd",

    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}
```

**주요 설정 설명:**

| 설정 | 값 | 설명 |
|------|-----|------|
| `poll.interval.ms` | `5000` | 5초마다 DB 폴링. 짧을수록 실시간에 가깝지만 DB 부하 증가 |
| `batch.max.rows` | `1000` | 한 번에 가져올 최대 행 수. DB 메모리와 네트워크에 맞게 조정 |
| `tasks.max` | `2` | 병렬 태스크 수. `table.whitelist`의 테이블 수 이하로 설정 |
| `timestamp.delay.interval.ms` | `120000` | 2분 지연 — 장거리 트랜잭션 누락 방어 |
| `connection.password` | `${file:...}` | 비밀번호를 설정 파일에서 로드 (JSON에 평문 노출 방지) |

### §6.2 Custom Query 모드

```json
{
  "name": "jdbc-source-order-summary",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:mysql://db-host:3306/mydb",
    "mode": "timestamp+incrementing",
    "query": "SELECT o.id, o.order_no, o.total_amount, o.updated_at, c.customer_name, c.tier FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.status != 'CANCELLED'",
    "incrementing.column.name": "id",
    "timestamp.column.name": "updated_at",
    "timestamp.delay.interval.ms": "120000",
    "topic.prefix": "enriched.",
    "poll.interval.ms": "10000"
  }
}
```

---

## §7. 오프셋 저장 메커니즘

JDBC Source Connector는 마지막으로 처리한 행의 위치(오프셋)를 저장하여 재시작 시 이어서 처리한다. 저장 방식은 배포 모드에 따라 다르다.

**Standalone 모드:**

```properties
# connect-standalone.properties
offset.storage.file.filename=/var/kafka-connect/offsets/jdbc-source-offsets.json
```

로컬 파일에 JSON 형태로 저장된다. 파일이 삭제되면 처음부터 다시 폴링한다.

**Distributed 모드:**

```properties
# connect-distributed.properties
offset.storage.topic=connect-offsets
offset.storage.replication.factor=3
offset.storage.partitions=25
```

Kafka 내부 토픽(`connect-offsets`)에 저장된다. `__consumer_offsets`와는 별개의 토픽이다. Kafka 자체가 내구성을 보장하므로 워커 장애 시에도 오프셋이 유지된다.

**오프셋 리셋 방법:**

| 방법 | 설명 | 주의사항 |
|------|------|---------|
| 커넥터 삭제 → 재생성 | 오프셋이 커넥터 이름에 바인딩되므로 이름을 변경하면 리셋 | 같은 이름이면 오프셋 유지 |
| `offset.storage.topic` 직접 수정 | Kafka 토픽에서 해당 커넥터의 오프셋 레코드 삭제 | 다른 커넥터 오프셋에 영향 주지 않도록 주의 |
| REST API | `DELETE /connectors/{name}` 후 다른 이름으로 재생성 | 가장 안전한 방법 |

---

## §8. SMT (Single Message Transform) 실전

SMT는 커넥터 내부에서 메시지를 변환하는 경량 플러그인이다. 별도 스트림 처리 파이프라인 없이 간단한 변환을 수행할 수 있다.

### §8.1 InsertField — 메타데이터 추가

```json
"transforms": "addSource,addTimestamp",
"transforms.addSource.type": "org.apache.kafka.connect.transforms.InsertField$Value",
"transforms.addSource.static.field": "source_table",
"transforms.addSource.static.value": "orders",
"transforms.addTimestamp.type": "org.apache.kafka.connect.transforms.InsertField$Value",
"transforms.addTimestamp.timestamp.field": "kafka_ingested_at"
```

소스 테이블명과 Kafka 적재 시간을 메시지에 자동 추가한다. 다운스트림에서 데이터 출처를 추적할 때 유용하다.

### §8.2 ReplaceField — 민감 필드 제거

```json
"transforms": "removeSensitive",
"transforms.removeSensitive.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
"transforms.removeSensitive.exclude": "ssn,credit_card_no,phone"
```

개인정보나 민감 데이터를 Kafka에 적재하기 전에 제거한다. GDPR/개인정보보호법 준수에 필수적이다.

### §8.3 TimestampRouter — 날짜별 토픽 라우팅

```json
"transforms": "routeByDate",
"transforms.routeByDate.type": "org.apache.kafka.connect.transforms.TimestampRouter",
"transforms.routeByDate.topic.format": "${topic}-${timestamp}",
"transforms.routeByDate.timestamp.format": "yyyy-MM-dd"
```

결과: `db.mydb.orders` → `db.mydb.orders-2026-03-05`

날짜별 토픽으로 라우팅하면 특정 날짜의 데이터만 선택적으로 재처리하거나 보존 정책을 차등 적용할 수 있다.

### §8.4 RegexRouter — 토픽명 정규식 변환

```json
"transforms": "renameTopics",
"transforms.renameTopics.type": "org.apache.kafka.connect.transforms.RegexRouter",
"transforms.renameTopics.regex": "db\\.mydb\\.(.*)",
"transforms.renameTopics.replacement": "production.$1"
```

결과: `db.mydb.orders` → `production.orders`

토픽 네이밍 규칙을 변환하여 소스 DB 구조와 Kafka 토픽 구조를 독립적으로 관리할 수 있다.

### §8.5 SMT 체이닝 순서

```json
"transforms": "filter,addMeta,route",
"transforms.filter.type": "...",
"transforms.addMeta.type": "...",
"transforms.route.type": "..."
```

SMT는 `transforms` 속성에 나열된 **순서대로** 실행된다. 순서가 중요한 이유:

1. **필터링을 먼저** — 불필요한 레코드를 조기에 제거하여 후속 변환의 처리량 감소
2. **메타데이터 추가 다음** — 라우팅에 필요한 필드를 먼저 추가
3. **라우팅은 마지막** — 최종 토픽 결정은 모든 변환이 완료된 후

순서를 잘못 지정하면 라우팅에 필요한 필드가 아직 추가되지 않았거나, 필터링이 필요한 레코드가 이미 변환을 거쳐 리소스를 낭비하는 문제가 생긴다.

---

## §9. CDC(Debezium) vs Query(JDBC) 비교

| 항목 | JDBC Source Connector | Debezium CDC |
|------|----------------------|-------------|
| **원리** | 주기적 SELECT 쿼리 | DB WAL/binlog 스트리밍 |
| **지연** | poll.interval.ms + delay | 밀리초 단위 |
| **DELETE 감지** | 불가 | 가능 (tombstone 이벤트) |
| **UPDATE 감지** | Timestamp 모드에서만 | 모든 변경 감지 |
| **DB 부하** | 매 폴링마다 쿼리 실행 | 초기 스냅샷 후 최소 |
| **설정 복잡도** | 낮음 (JSON 설정) | 높음 (DB 권한, WAL 설정) |
| **DB 지원** | JDBC 지원 모든 DB | MySQL, PostgreSQL, Oracle, MongoDB 등 |
| **필요 권한** | SELECT 권한 | 복제 권한 (REPLICATION) |
| **테이블 조건** | Auto Increment PK 또는 Timestamp 컬럼 필수 | 없음 |
| **스키마 변경** | 커넥터 재시작 필요 | 자동 감지 (일부 제한) |
| **데이터 정합성** | 누락 가능 (§4 참조) | WAL 기반 완전 캡처 |

**컬리의 전략**: 주 운영은 Debezium CDC, DB 설정 변경이 어려운 경우 JDBC Source를 보조 운영한다.

**JDBC Source가 적합한 상황:**
- INSERT-only 로그성 테이블 (audit_log, event_log 등)
- DB 관리팀의 WAL/binlog 설정 변경이 불가한 레거시 환경
- 빠른 PoC나 프로토타입 (설정이 간단)
- 코드 테이블처럼 전체 동기화(Bulk 모드)가 적합한 소규모 테이블

**Debezium CDC가 적합한 상황:**
- DELETE, UPDATE를 포함한 모든 변경을 추적해야 하는 경우
- 밀리초 단위 지연이 요구되는 실시간 파이프라인
- 이벤트 소싱이나 CQRS 패턴의 변경 이벤트 소스
- 장거리 트랜잭션이 빈번하여 timestamp.delay가 과도해지는 경우

---

## §10. 모니터링 및 운영

### §10.1 REST API

Kafka Connect는 REST API를 통해 커넥터를 관리한다.

```bash
# 커넥터 상태 확인
GET /connectors/{name}/status

# 응답 예시
{
  "name": "jdbc-source-orders",
  "connector": { "state": "RUNNING", "worker_id": "worker-1:8083" },
  "tasks": [
    { "id": 0, "state": "RUNNING", "worker_id": "worker-1:8083" },
    { "id": 1, "state": "FAILED", "worker_id": "worker-2:8083",
      "trace": "org.apache.kafka.connect.errors.ConnectException: ..." }
  ]
}

# 커넥터 재시작
POST /connectors/{name}/restart

# 개별 태스크 재시작
POST /connectors/{name}/tasks/{taskId}/restart

# 커넥터 일시 중지/재개
PUT /connectors/{name}/pause
PUT /connectors/{name}/resume

# 커넥터 삭제 (오프셋은 유지됨)
DELETE /connectors/{name}
```

### §10.2 JMX 메트릭

| 메트릭 | 설명 | 경보 기준 |
|--------|------|----------|
| `source-record-poll-rate` | 초당 폴링된 레코드 수 | 0으로 떨어지면 커넥터 장애 |
| `source-record-write-rate` | 초당 Kafka에 기록된 레코드 수 | poll-rate 대비 큰 차이 시 병목 |
| `source-record-poll-total` | 누적 폴링 레코드 수 | 추세 모니터링 |
| `task-error-total-record-errors` | 에러 레코드 누적 수 | 증가 추세 시 조사 |
| `offset-commit-success-percentage` | 오프셋 커밋 성공률 | 100% 미만 시 조사 |

### §10.3 장애 시나리오

| 시나리오 | 동작 | 대응 |
|---------|------|------|
| DB 연결 끊김 | 자동 재시도 (backoff) | DB 복구 후 자동 재개 |
| 인증 실패 | 태스크 FAILED | `connection.user/password` 확인 후 재시작 |
| 토픽 미존재 | 자동 생성 (설정에 따라) | `auto.create.topics.enable` 확인 |
| 워커 장애 (Distributed) | 다른 워커에 태스크 자동 재할당 | 워커 복구 후 리밸런스 |
| 오프셋 손상 | 마지막 커밋 지점부터 재폴링 | 중복 가능 — Consumer 멱등성 필요 |

---

## §11. 대안 커넥터 + Redpanda Connect

### §11.1 커넥터 비교

| 커넥터 | 특징 | 라이선스 |
|--------|------|---------|
| **Confluent JDBC Source** | 가장 범용, 커뮤니티 버전은 무료 | Confluent Community License |
| **Aiven JDBC Source** | 오픈소스 fork, 추가 기능 | Apache 2.0 |
| **Debezium JDBC Sink** | Debezium 기반 Sink 전용 (2.x부터) | Apache 2.0 |
| **Redpanda Connect (Benthos)** | YAML 선언적 파이프라인 | BSL |

### §11.2 Redpanda Connect (Benthos) YAML 대안

동일한 JDBC Source 파이프라인을 Redpanda Connect(구 Benthos)로 구현하면 다음과 같다:

```yaml
input:
  sql_select:
    driver: mysql
    dsn: "user:password@tcp(db-host:3306)/mydb"
    table: orders
    columns:
      - id
      - order_no
      - amount
      - updated_at
    where: "updated_at > ?"
    args_mapping: |
      root = [this.checkpoint_timestamp]
    init_statement: ""

pipeline:
  processors:
    - mapping: |
        root = this
        root.source_table = "orders"
        root.kafka_ingested_at = now()
    - mapping: |
        root.ssn = deleted()
        root.credit_card_no = deleted()

output:
  kafka:
    addresses: ["broker:9092"]
    topic: "db.mydb.orders"
    key: "${! json(\"id\") }"
    compression: lz4
```

**JDBC Source Connector vs Benthos 비교:**

| 항목 | JDBC Source Connector | Redpanda Connect (Benthos) |
|------|----------------------|---------------------------|
| 설정 방식 | JSON (Kafka Connect 프레임워크) | YAML (독립 실행) |
| 변환 | SMT (제한적) | Bloblang (튜링 완전) |
| 커넥터 관리 | Kafka Connect REST API | 독립 프로세스 (systemd 등) |
| 오프셋 관리 | 자동 (Kafka 내부 토픽) | 수동 (체크포인트 파일/Redis) |
| 장점 | 생태계 통합, 커뮤니티 | 변환 유연성, 경량 |
| 단점 | SMT 복잡도 한계 | Kafka Connect 생태계 밖 |

Benthos의 Bloblang 프로세서는 SMT보다 훨씬 유연하다. 조건부 변환, 필드 매핑, 데이터 타입 변환 등을 선언적 YAML로 표현할 수 있다. 반면 Kafka Connect 생태계의 모니터링, 분산 모드, 커넥터 플러그인을 사용할 수 없으므로, 단순한 파이프라인에는 Benthos가, 복잡한 커넥터 조합에는 Kafka Connect가 적합하다.

---

## §12. 실전 교훈

1. **쿼리 기반 CDC의 구조적 한계를 인지하라.** JDBC Source Connector는 "현재 상태의 스냅샷"을 폴링하는 방식이다. DELETE와 같은 파괴적 변경은 원리적으로 감지할 수 없다. 이 한계를 모르고 도입하면 데이터 정합성 문제를 늦게 발견한다.

2. **`timestamp.delay.interval.ms`는 보험이지 해결책이 아니다.** 장거리 트랜잭션 누락을 줄여주지만, 트랜잭션 타임아웃을 초과하는 극단적 경우에는 여전히 누락이 발생한다. 100% 정합성이 필요하면 CDC(Debezium)를 선택해야 한다.

3. **Timestamp+Incrementing이 기본 선택이다.** Incrementing은 UPDATE를 감지하지 못하고, Timestamp는 동일 타임스탬프 충돌에 취약하다. 두 가지를 조합한 모드가 가장 안전하며, 대부분의 프로덕션에서 이 모드를 사용한다.

4. **오프셋 리셋은 커넥터 이름을 바꾸는 것이 가장 안전하다.** 오프셋은 커넥터 이름에 바인딩되므로, 기존 커넥터를 삭제하고 새 이름으로 재생성하면 처음부터 다시 폴링한다. 내부 토픽을 직접 수정하는 것은 위험하다.

5. **SMT는 간단한 변환에만 사용하라.** 복잡한 비즈니스 로직은 Kafka Streams나 별도 Consumer에서 처리하는 것이 테스트와 유지보수에 유리하다. SMT는 필드 추가/제거, 토픽 라우팅 같은 단순 변환에 적합하다.

6. **Consumer 멱등성은 JDBC Source에서도 필수다.** 오프셋 커밋 실패, 워커 장애, 리밸런스 등으로 중복 적재가 발생할 수 있다. 다운스트림 Consumer는 항상 멱등하게 설계해야 한다.
