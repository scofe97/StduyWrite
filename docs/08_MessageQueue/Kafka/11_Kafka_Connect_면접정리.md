# Chapter 11: Kafka Connect (외부 시스템 통합) - 면접 심화 정리

---

## 1. Kafka Connect의 아키텍처와 설계 철학

### 1.1 Kafka Connect란 무엇인가

Kafka Connect는 외부 데이터 시스템과 Kafka 클러스터 간의 데이터 이동을 위한 확장 가능하고 신뢰성 있는 프레임워크입니다. 직접 Producer/Consumer를 구현하는 대신 Kafka Connect를 사용하면, 검증된 커넥터를 통해 빠르게 데이터 파이프라인을 구축할 수 있습니다.

Kafka Connect의 핵심 가치는 표준화와 재사용성에 있습니다. 데이터베이스에서 Kafka로 데이터를 가져오는 로직, 오프셋 관리, 에러 처리, 확장성 등의 공통 로직을 프레임워크가 처리하고, 개발자는 데이터 소스/타겟에 특화된 로직만 구현하면 됩니다. 이미 200개 이상의 커넥터가 Confluent Hub에 공개되어 있어, 대부분의 데이터 통합 시나리오에서 기존 커넥터를 활용할 수 있습니다.

### 1.2 핵심 컴포넌트 이해

Kafka Connect의 아키텍처를 구성하는 핵심 컴포넌트들을 이해해야 합니다.

**Connector**는 외부 시스템과의 연결을 정의하는 논리적 단위입니다. 어떤 데이터베이스에 연결할 것인지, 어떤 테이블을 대상으로 할 것인지, 어떤 토픽에 데이터를 쓸 것인지 등의 설정을 담고 있습니다. Connector는 실제 데이터를 처리하지 않고, Task라는 작업 단위를 생성합니다.

**Task**는 실제 데이터 복사 작업을 수행하는 단위입니다. 하나의 Connector는 여러 개의 Task를 생성할 수 있으며, 각 Task는 독립적으로 데이터의 일부분을 처리합니다. 예를 들어, 10개의 테이블을 동기화하는 JDBC Source Connector는 10개의 Task를 생성하여 각 Task가 하나의 테이블을 담당하도록 할 수 있습니다.

**Worker**는 Connector와 Task를 실행하는 JVM 프로세스입니다. Distributed Mode에서는 여러 Worker가 클러스터를 구성하고, Task들이 Worker 간에 분산되어 실행됩니다. Worker 중 하나가 장애가 발생하면, 해당 Worker에서 실행되던 Task들이 다른 Worker로 재배치됩니다.

**Converter**는 데이터의 직렬화/역직렬화를 담당합니다. Kafka Connect 내부에서는 데이터가 구조화된 형태(Struct)로 표현되는데, 이를 Kafka 메시지의 바이트 배열로 변환하거나 그 반대 작업을 수행합니다. JSON, Avro, Protobuf 등 다양한 Converter가 있습니다.

**Transform(SMT)**은 메시지가 Kafka에 쓰여지거나 외부 시스템에 쓰여지기 전에 단일 메시지 단위로 변환을 수행합니다. 필드 추가, 삭제, 이름 변경, 값 마스킹 등의 작업을 선언적으로 수행할 수 있습니다.

```
Kafka Connect 데이터 흐름:

Source Connector:
외부 시스템 → Source Task → Converter → SMT → Kafka Topic

Sink Connector:
Kafka Topic → SMT → Converter → Sink Task → 외부 시스템
```

### 1.3 Source와 Sink Connector의 역할 분담

Source Connector는 외부 시스템에서 Kafka로 데이터를 가져오는 역할을 합니다. 데이터베이스의 변경 사항을 캡처하거나, 파일 시스템을 모니터링하거나, REST API를 주기적으로 폴링하는 등의 작업을 수행합니다. Source Connector의 핵심 책임은 외부 시스템의 데이터를 Kafka Connect 내부 형식으로 변환하고, 처리 위치(오프셋)를 관리하는 것입니다.

Sink Connector는 Kafka에서 외부 시스템으로 데이터를 전송하는 역할을 합니다. Elasticsearch에 검색 인덱스를 업데이트하거나, 데이터 웨어하우스에 분석용 데이터를 적재하거나, S3에 아카이브하는 등의 작업을 수행합니다. Sink Connector는 Consumer Group처럼 동작하여, 토픽의 파티션들이 Task 간에 분배됩니다.

---

## 2. Standalone Mode vs Distributed Mode

### 2.1 Standalone Mode의 구조와 한계

Standalone Mode는 단일 Worker 프로세스에서 모든 Connector와 Task를 실행합니다. 설정 파일을 통해 Connector를 정의하고, 오프셋은 로컬 파일에 저장됩니다.

```
connect-standalone.sh config/standalone.properties \
    connector1.properties \
    connector2.properties
```

Standalone Mode의 한계는 명확합니다. 단일 장애점(Single Point of Failure)이 존재하여 Worker가 죽으면 모든 데이터 파이프라인이 중단됩니다. 수평 확장이 불가능하여 처리량이 Worker 하나의 리소스로 제한됩니다. 런타임에 Connector 추가/수정이 어렵습니다. 이러한 이유로 Standalone Mode는 개발/테스트 환경이나 매우 단순한 파이프라인에서만 사용해야 합니다.

### 2.2 Distributed Mode의 내부 동작

Distributed Mode에서는 여러 Worker가 클러스터를 구성하고, REST API를 통해 Connector를 관리합니다. 모든 상태 정보는 Kafka 토픽에 저장되어 Worker 간에 공유됩니다.

**내부 토픽의 역할**을 이해해야 합니다.

`config.storage.topic`은 Connector와 Task의 설정을 저장합니다. REST API를 통해 Connector를 생성하면, 해당 설정이 이 토픽에 저장되고 모든 Worker가 이를 읽어 동기화합니다. 이 토픽은 단일 파티션으로 구성되어 설정의 순서가 보장됩니다.

`offset.storage.topic`은 Source Connector의 오프셋을 저장합니다. 각 Source Task가 외부 시스템에서 어디까지 데이터를 읽었는지 기록합니다. 이 토픽은 여러 파티션으로 구성되어 다수의 Task가 동시에 오프셋을 커밋할 수 있습니다.

`status.storage.topic`은 Connector와 Task의 상태(RUNNING, PAUSED, FAILED 등)를 저장합니다. 모니터링 도구나 REST API 응답에 사용됩니다.

**리밸런싱 메커니즘**도 중요합니다. Worker가 추가되거나 제거되면, 클러스터는 Task들을 재분배합니다. 이 과정은 Consumer Group의 리밸런싱과 유사합니다. 리밸런싱 동안 일시적으로 데이터 처리가 중단될 수 있으므로, 불필요한 리밸런싱을 최소화하도록 Worker 수를 안정적으로 유지해야 합니다.

### 2.3 프로덕션 환경 권장 설정

프로덕션에서는 반드시 Distributed Mode를 사용해야 합니다. 최소 3개 이상의 Worker를 배포하여 내결함성을 확보합니다. 내부 토픽의 replication.factor는 3으로 설정하여 데이터 유실을 방지합니다.

```properties
# 프로덕션 distributed.properties 예시
bootstrap.servers=broker1:9092,broker2:9092,broker3:9092
group.id=connect-cluster-production

config.storage.topic=connect-configs
config.storage.replication.factor=3

offset.storage.topic=connect-offsets
offset.storage.replication.factor=3
offset.storage.partitions=25

status.storage.topic=connect-status
status.storage.replication.factor=3
status.storage.partitions=5
```

---

## 3. REST API를 통한 운영

### 3.1 Connector 생명주기 관리

Distributed Mode에서 모든 Connector 관리는 REST API를 통해 이루어집니다. 주요 작업의 API 패턴을 숙지해야 합니다.

**Connector 생성**은 POST 요청으로 수행합니다. 설정 JSON을 body에 담아 전송하면, 해당 설정이 config.storage.topic에 저장되고 적절한 Worker에서 Connector와 Task가 시작됩니다.

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-jdbc-source",
    "config": {
      "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
      "connection.url": "jdbc:postgresql://db:5432/mydb",
      "mode": "incrementing",
      "incrementing.column.name": "id",
      "topic.prefix": "db-",
      "tasks.max": "3"
    }
  }'
```

**상태 조회**는 GET 요청으로 수행합니다. Connector와 각 Task의 현재 상태를 확인할 수 있습니다.

```bash
curl http://localhost:8083/connectors/my-jdbc-source/status

# 응답 예시
{
  "name": "my-jdbc-source",
  "connector": {
    "state": "RUNNING",
    "worker_id": "worker1:8083"
  },
  "tasks": [
    {"id": 0, "state": "RUNNING", "worker_id": "worker1:8083"},
    {"id": 1, "state": "RUNNING", "worker_id": "worker2:8083"},
    {"id": 2, "state": "FAILED", "worker_id": "worker3:8083", "trace": "..."}
  ]
}
```

**설정 변경**은 PUT 요청으로 수행합니다. 전체 설정을 새로 제공해야 하며(부분 업데이트 불가), 변경 사항이 적용되면서 Task가 재시작됩니다.

**일시 중지/재개**는 각각 PUT /pause와 /resume으로 수행합니다. 일시 중지된 Connector는 데이터 처리를 멈추지만 오프셋 정보는 유지됩니다. 유지보수 작업이나 문제 해결 시 유용합니다.

### 3.2 Task 단위 관리

개별 Task를 재시작하는 것도 가능합니다. 특정 Task만 실패한 경우, Connector 전체를 재시작하지 않고 해당 Task만 재시작할 수 있습니다.

```bash
curl -X POST http://localhost:8083/connectors/my-jdbc-source/tasks/2/restart
```

이 기능은 일시적인 오류(네트워크 타임아웃, 일시적인 DB 연결 문제 등)로 Task가 실패했을 때 유용합니다.

---

## 4. JDBC Source Connector 심층 분석

### 4.1 동작 모드별 특성

JDBC Source Connector는 관계형 데이터베이스에서 Kafka로 데이터를 가져오는 가장 일반적인 방법입니다. 네 가지 동작 모드가 있으며, 각각의 특성을 이해해야 올바른 모드를 선택할 수 있습니다.

**Bulk Mode**는 전체 테이블을 주기적으로 복사합니다. 매 폴링마다 SELECT * 쿼리를 실행하여 모든 레코드를 가져옵니다. 작은 참조 테이블이나 전체 스냅샷이 필요한 경우에 적합하지만, 대용량 테이블에서는 비효율적입니다.

**Incrementing Mode**는 자동 증가 컬럼(예: id)을 기준으로 새로 추가된 레코드만 가져옵니다. 마지막으로 처리한 id 값을 기억하고, 다음 폴링에서 WHERE id > last_id 조건으로 쿼리합니다. INSERT만 발생하는 테이블에 적합하지만, UPDATE를 감지할 수 없다는 한계가 있습니다.

**Timestamp Mode**는 타임스탬프 컬럼(예: updated_at)을 기준으로 변경된 레코드를 가져옵니다. 마지막으로 처리한 타임스탬프 이후의 레코드를 쿼리합니다. UPDATE를 감지할 수 있지만, 동일 타임스탬프를 가진 레코드가 여러 개 있으면 일부가 누락될 수 있습니다.

**Timestamp+Incrementing Mode**는 두 컬럼을 조합하여 가장 정확한 변경 감지를 제공합니다. 타임스탬프로 대략적인 범위를 좁히고, 같은 타임스탬프 내에서는 id로 정확한 순서를 보장합니다. 대부분의 프로덕션 환경에서 권장되는 모드입니다.

### 4.2 JDBC Source Connector의 근본적 한계

JDBC Source Connector는 폴링 기반이기 때문에 몇 가지 근본적인 한계가 있습니다.

**DELETE 감지 불가**: 레코드가 삭제되면 다음 폴링에서 해당 레코드가 없을 뿐, 삭제되었다는 이벤트를 생성하지 않습니다. 이를 처리하려면 소프트 삭제(deleted_at 컬럼)를 사용하거나 CDC를 사용해야 합니다.

**실시간성 제한**: 폴링 간격만큼의 지연이 발생합니다. 폴링 간격을 줄이면 데이터베이스 부하가 증가합니다.

**데이터베이스 부하**: 매 폴링마다 쿼리가 실행되어 데이터베이스에 부하를 줍니다. 특히 Bulk Mode나 큰 테이블에서 심각할 수 있습니다.

이러한 한계 때문에, 실시간성이 중요하거나 DELETE를 추적해야 하는 경우 CDC(Change Data Capture) 방식을 사용해야 합니다.

---

## 5. Debezium CDC Connector 심층 분석

### 5.1 CDC의 원리

Change Data Capture(CDC)는 데이터베이스의 트랜잭션 로그를 읽어 변경 사항을 캡처하는 방식입니다. 데이터베이스는 트랜잭션의 원자성과 내구성을 보장하기 위해 모든 변경 사항을 로그(WAL, Binlog, Redo Log 등)에 먼저 기록합니다. CDC는 이 로그를 읽어 변경 이벤트를 생성합니다.

Debezium은 가장 널리 사용되는 오픈소스 CDC 플랫폼으로, Kafka Connect 프레임워크 위에서 동작합니다. PostgreSQL, MySQL, MongoDB, Oracle, SQL Server 등 다양한 데이터베이스를 지원합니다.

```
CDC 데이터 흐름:

1. 애플리케이션 → 데이터베이스: INSERT/UPDATE/DELETE 실행
2. 데이터베이스 → 트랜잭션 로그: 변경 사항 기록
3. Debezium → 트랜잭션 로그: 변경 사항 읽기
4. Debezium → Kafka: 변경 이벤트 발행
```

### 5.2 JDBC 폴링 대비 CDC의 장점

CDC는 폴링 방식 대비 여러 장점이 있습니다.

**실시간 변경 감지**: 트랜잭션이 커밋되면 즉시 이벤트가 발생합니다. 폴링 간격에 의한 지연이 없습니다.

**DELETE 감지**: 삭제 연산도 트랜잭션 로그에 기록되므로, DELETE 이벤트를 정확히 캡처할 수 있습니다.

**이전 값(before) 제공**: UPDATE 시 변경 전 값과 변경 후 값을 모두 제공합니다. 이는 감사 로그나 데이터 동기화에 유용합니다.

**데이터베이스 부하 최소화**: 트랜잭션 로그를 읽는 것은 쿼리를 실행하는 것보다 데이터베이스에 훨씬 적은 부하를 줍니다.

**스키마 변경 추적**: 테이블 구조 변경도 캡처하여 하위 시스템에 전파할 수 있습니다.

### 5.3 Debezium 메시지 구조 이해

Debezium이 생성하는 메시지 구조를 이해하면 데이터를 효과적으로 활용할 수 있습니다.

```json
{
  "before": {
    "id": 1001,
    "name": "Alice",
    "email": "alice@old.com"
  },
  "after": {
    "id": 1001,
    "name": "Alice",
    "email": "alice@new.com"
  },
  "source": {
    "connector": "postgresql",
    "db": "inventory",
    "table": "customers",
    "txId": 571,
    "lsn": 24023128
  },
  "op": "u",
  "ts_ms": 1703123456789
}
```

**op 필드**는 작업 유형을 나타냅니다. "c"는 INSERT, "u"는 UPDATE, "d"는 DELETE, "r"은 스냅샷 읽기를 의미합니다.

**before 필드**는 변경 전 레코드 상태입니다. INSERT에서는 null이고, UPDATE와 DELETE에서는 이전 값을 포함합니다. 단, MySQL의 경우 binlog_row_image=FULL 설정이 필요합니다.

**after 필드**는 변경 후 레코드 상태입니다. DELETE에서는 null입니다.

**source 필드**는 변경의 출처 정보를 포함합니다. 데이터베이스, 테이블, 트랜잭션 ID, LSN(Log Sequence Number) 등이 포함됩니다.

### 5.4 스냅샷 모드의 이해

Debezium은 시작 시 기존 데이터를 어떻게 처리할지 결정하는 스냅샷 모드를 제공합니다.

**initial** 모드는 가장 일반적인 설정입니다. 처음 시작할 때 테이블의 전체 데이터를 스냅샷으로 읽고, 이후에는 트랜잭션 로그에서 변경 사항만 캡처합니다.

**never** 모드는 스냅샷 없이 현재 시점부터의 변경만 캡처합니다. 기존 데이터가 필요 없거나 이미 다른 방법으로 동기화된 경우에 사용합니다.

**schema_only** 모드는 테이블 스키마만 읽고 데이터는 읽지 않습니다. 현재 시점부터의 변경만 캡처하되, 스키마 정보는 필요한 경우에 적합합니다.

스냅샷 중에는 테이블에 잠금이 걸릴 수 있으므로, 대용량 테이블에서는 초기 스냅샷 시간과 데이터베이스 부하를 고려해야 합니다.

---

## 6. Single Message Transformations (SMT)

### 6.1 SMT의 역할과 활용

SMT는 Connector 수준에서 메시지를 변환하는 경량 처리 계층입니다. Kafka Streams나 별도의 처리 애플리케이션 없이도 간단한 변환을 수행할 수 있습니다.

**적합한 사용 사례**:
- 필드 추가/삭제/이름 변경
- 민감 정보 마스킹
- 토픽 라우팅 (날짜별, 조건별)
- 데이터 타입 변환
- 메시지 필터링

**부적합한 사용 사례**:
- 여러 메시지 간의 조인이나 집계
- 상태를 유지해야 하는 복잡한 변환
- 외부 시스템 조회가 필요한 변환

### 6.2 주요 SMT 패턴

**MaskField**는 민감 정보를 마스킹합니다. 신용카드 번호, 주민등록번호 등을 고정 값으로 대체합니다.

```json
{
  "transforms": "maskSensitive",
  "transforms.maskSensitive.type": "org.apache.kafka.connect.transforms.MaskField$Value",
  "transforms.maskSensitive.fields": "credit_card,ssn",
  "transforms.maskSensitive.replacement": "****"
}
```

**TimestampRouter**는 타임스탬프를 기반으로 토픽 이름을 동적으로 결정합니다. 날짜별 파티셔닝이나 아카이브에 유용합니다.

```json
{
  "transforms": "routeByDate",
  "transforms.routeByDate.type": "org.apache.kafka.connect.transforms.TimestampRouter",
  "transforms.routeByDate.topic.format": "${topic}-${timestamp}",
  "transforms.routeByDate.timestamp.format": "yyyyMMdd"
}
```

**ValueToKey + ExtractField**는 Value의 특정 필드를 Key로 추출합니다. JDBC Source에서 메시지 키를 설정할 때 자주 사용됩니다.

```json
{
  "transforms": "createKey,extractId",
  "transforms.createKey.type": "org.apache.kafka.connect.transforms.ValueToKey",
  "transforms.createKey.fields": "id",
  "transforms.extractId.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
  "transforms.extractId.field": "id"
}
```

---

## 7. 에러 처리와 복구

### 7.1 에러 허용 정책

Kafka Connect는 처리 중 발생하는 에러에 대해 세 가지 정책을 제공합니다.

**none(기본값)**: 에러 발생 시 Task가 즉시 실패합니다. 데이터 무결성이 중요한 경우 적합합니다.

**all**: 에러가 발생해도 해당 메시지를 건너뛰고 계속 처리합니다. 일부 메시지 손실이 허용되는 경우에 사용합니다.

**log**: 에러를 로깅하고 계속 처리합니다.

### 7.2 Dead Letter Queue (DLQ)

에러 허용 정책을 all로 설정할 때, 실패한 메시지를 DLQ에 저장하여 나중에 분석하고 재처리할 수 있습니다.

```properties
errors.tolerance=all
errors.deadletterqueue.topic.name=connect-dlq
errors.deadletterqueue.topic.replication.factor=3
errors.deadletterqueue.context.headers.enable=true
```

DLQ에 저장된 메시지의 헤더에는 에러 원인, 원본 토픽, 커넥터 이름 등의 컨텍스트 정보가 포함됩니다. 이를 활용하여 문제를 진단하고 수정한 후 메시지를 재처리할 수 있습니다.

---

## 8. 면접 핵심 질문과 모범 답변

### Q1. JDBC Source Connector와 Debezium CDC Connector의 차이점은 무엇인가요?

**모범 답변**: 가장 근본적인 차이는 변경 감지 방식입니다. JDBC Source Connector는 주기적으로 테이블을 쿼리하여 새로운 레코드나 수정된 레코드를 찾습니다. 반면 Debezium은 데이터베이스의 트랜잭션 로그(WAL, Binlog 등)를 읽어 변경 사항을 실시간으로 캡처합니다.

이 차이로 인해 몇 가지 중요한 특성이 달라집니다. 첫째, DELETE 감지입니다. JDBC는 삭제를 감지할 수 없지만, CDC는 삭제 이벤트를 정확히 캡처합니다. 둘째, 실시간성입니다. JDBC는 폴링 간격만큼 지연이 발생하지만, CDC는 트랜잭션 커밋 직후 이벤트가 발생합니다. 셋째, 데이터베이스 부하입니다. JDBC는 매번 쿼리를 실행하여 부하를 주지만, CDC는 로그를 읽는 것이므로 부하가 최소화됩니다.

일반적으로 실시간 동기화, DELETE 추적, 변경 이력 관리가 필요한 경우 CDC를 선택하고, 간단한 데이터 동기화나 CDC 설정이 복잡한 환경에서는 JDBC를 사용합니다.

### Q2. Kafka Connect의 Standalone Mode와 Distributed Mode는 각각 언제 사용하나요?

**모범 답변**: Standalone Mode는 단일 Worker에서 모든 Connector를 실행하며, 설정 파일로 관리됩니다. 오프셋이 로컬 파일에 저장되어 Worker 장애 시 복구가 어렵습니다. 개발/테스트 환경이나 매우 단순한 파이프라인에서만 사용해야 합니다.

Distributed Mode는 여러 Worker가 클러스터를 구성하고, REST API로 관리됩니다. 설정과 오프셋이 Kafka 토픽에 저장되어 Worker 장애 시 자동으로 Task가 재분배됩니다. 프로덕션 환경에서는 반드시 Distributed Mode를 사용해야 합니다.

Distributed Mode에서는 config.storage.topic, offset.storage.topic, status.storage.topic이라는 세 개의 내부 토픽이 사용됩니다. 이 토픽들의 replication.factor를 3으로 설정하여 데이터 유실을 방지해야 합니다.

### Q3. SMT(Single Message Transformations)란 무엇이고 언제 사용하나요?

**모범 답변**: SMT는 Kafka Connect에서 메시지가 Kafka에 쓰여지거나 외부 시스템에 쓰여지기 전에 단일 메시지 단위로 변환을 수행하는 기능입니다. 별도의 스트림 처리 애플리케이션 없이도 Connector 설정만으로 간단한 변환이 가능합니다.

대표적인 사용 사례로는 민감 정보 마스킹(MaskField), 타임스탬프 기반 토픽 라우팅(TimestampRouter), 필드 추가/삭제(InsertField, ReplaceField), Value 필드를 Key로 추출(ValueToKey + ExtractField) 등이 있습니다.

SMT는 단일 메시지에 대한 무상태 변환에 적합합니다. 여러 메시지를 조인하거나 집계하는 등의 상태 기반 처리는 Kafka Streams나 별도의 처리 애플리케이션에서 수행해야 합니다.

### Q4. Debezium에서 스냅샷 모드란 무엇이고 각 모드의 차이는 무엇인가요?

**모범 답변**: 스냅샷 모드는 Debezium Connector가 시작할 때 기존 데이터를 어떻게 처리할지 결정합니다.

initial 모드는 가장 일반적으로 사용되며, 처음 시작 시 테이블 전체 데이터를 읽어 Kafka에 발행하고, 이후에는 트랜잭션 로그에서 변경만 캡처합니다. 새로운 시스템을 구축하거나 기존 데이터 전체가 필요한 경우에 사용합니다.

never 모드는 스냅샷 없이 현재 시점부터의 변경만 캡처합니다. 기존 데이터가 이미 동기화되어 있거나 필요 없는 경우에 적합합니다.

schema_only 모드는 테이블 스키마만 읽고 데이터는 읽지 않습니다. 데이터는 현재 시점부터 캡처하되, 스키마 정보가 필요한 경우에 사용합니다.

스냅샷 중에는 테이블 잠금이 발생할 수 있으므로, 대용량 프로덕션 데이터베이스에서는 스냅샷 시간과 부하를 신중히 고려해야 합니다.

### Q5. Kafka Connect에서 에러 처리는 어떻게 하나요?

**모범 답변**: Kafka Connect는 errors.tolerance 설정으로 에러 처리 정책을 결정합니다. 기본값인 none은 에러 발생 시 Task가 즉시 실패합니다. all로 설정하면 에러가 발생한 메시지를 건너뛰고 계속 처리합니다.

에러 허용 정책을 all로 설정할 때는 Dead Letter Queue(DLQ)를 함께 설정하는 것이 좋습니다. 실패한 메시지가 DLQ 토픽에 저장되어 나중에 분석하고 재처리할 수 있습니다. DLQ 메시지의 헤더에는 에러 원인, 원본 토픽, 커넥터 이름 등의 컨텍스트 정보가 포함됩니다.

프로덕션에서는 DLQ를 모니터링하여 에러 발생 시 알림을 받고, 원인을 분석하여 재처리하는 운영 프로세스를 갖추어야 합니다.

---

## 9. 실무 체크리스트

- [ ] 프로덕션에서는 반드시 Distributed Mode 사용
- [ ] 내부 토픽(config, offset, status)의 replication.factor는 3으로 설정
- [ ] DELETE 추적이 필요하면 CDC(Debezium) 선택
- [ ] tasks.max는 파티션 수 또는 테이블 수에 맞게 조정
- [ ] Schema Registry와 Avro Converter 사용으로 스키마 호환성 관리
- [ ] 민감 정보는 SMT MaskField로 마스킹
- [ ] DLQ 설정으로 에러 메시지 분석 및 재처리 가능하게
- [ ] Connector/Task 상태 모니터링 및 알림 설정
- [ ] Debezium 사용 시 스냅샷 시간과 DB 부하 사전 테스트

---

## 10. 참고 자료

- [Apache Kafka Connect Documentation](https://kafka.apache.org/documentation/#connect)
- [Debezium Documentation](https://debezium.io/documentation/)
- [Confluent Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html)
- [KIP-618: Exactly-Once Support for Source Connectors](https://cwiki.apache.org/confluence/display/KAFKA/KIP-618)
