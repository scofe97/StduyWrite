# 03. 스키마 진화 및 호환성 관리

Avro 스키마, Schema Registry, 호환성 모드, 진화 전략

마이크로서비스가 독립적으로 배포되려면 이벤트 스키마 변경이 기존 소비자를 깨뜨리지 않아야 한다. 이를 보장하는 것이 스키마 호환성 관리이며, Schema Registry는 이 계약을 중앙에서 강제한다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 스키마 진화 시 호환성 규칙(Forward/Backward/Full)을 이해하고 적용할 수 있다
- Avro 스키마 설계 시 호환성을 유지하는 방법을 설명할 수 있다
- Schema Registry의 역할과 호환성 검증 흐름을 이해한다

---

## 구성:

### 1. 왜 스키마가 필요한가?

#### 문제점: JSON의 한계
```
JSON 직렬화 문제:
├── 타입 안전성 부족 (문자열 "123" vs 숫자 123)
├── 필드명이 매번 포함 → 대역폭 낭비
├── 버전 관리 없음 → Producer/Consumer 스키마 불일치
├── 런타임에만 에러 발견 (필수 필드 누락)
└── 스키마 문서가 코드와 분리 → 문서-코드 불일치
```

#### Avro의 장점
```
Avro 직렬화:
├── 바이너리 포맷 → JSON 대비 50-80% 크기 감소
├── 스키마가 별도 저장 → 필드명 중복 없음
├── 스키마 ID로 버전 관리 → 호환성 검증
├── 컴파일 타임 에러 발견 (코드 생성)
└── 스키마가 단일 진실 공급원(SSOT)
```

### 2. Schema Registry 아키텍처

```
┌─────────────┐
│  Producer   │
└──────┬──────┘
       │ 1. 스키마 등록 요청
       ↓
┌─────────────────────┐
│  Schema Registry    │ ← GET /schemas/ids/1
│  (Redpanda Console) │ ← POST /subjects/{subject}/versions
└─────────┬───────────┘
          │ 2. 스키마 ID 반환 (예: 1)
          ↓
┌─────────────┐
│  Redpanda   │ ← [1][바이너리 데이터]
│   Broker    │   (5바이트 헤더 + Avro 직렬화)
└──────┬──────┘
       │ 3. 메시지 전송 (스키마 ID + 데이터)
       ↓
┌─────────────┐
│  Consumer   │
└─────────────┘
  ↑
  └── 4. 스키마 ID로 Registry에서 스키마 조회 → 역직렬화
```

**와이어 포맷**:
```
[0x00][스키마 ID: 4바이트][Avro 바이너리 데이터]
```

### 3. Avro 스키마 정의

#### 기본 스키마
```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.events",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "status", "type": "string"},
    {"name": "createdAt", "type": "long", "logicalType": "timestamp-millis"}
  ]
}
```

#### 진화된 스키마 (필드 추가)
```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.events",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "status", "type": "string"},
    {"name": "createdAt", "type": "long", "logicalType": "timestamp-millis"},
    {"name": "paymentMethod", "type": ["null", "string"], "default": null}
  ]
}
```

**핵심**: `"type": ["null", "string"]`은 Union 타입 → 필드가 null 가능. default 값 필수.

### 4. 호환성 모드

| 모드 | 설명 | 허용 작업 | 사용 케이스 |
|------|------|----------|-------------|
| **BACKWARD** (기본) | 새 Consumer가 이전 메시지 읽기 가능 | 필드 추가 (default 필수), 필드 삭제 | Consumer 먼저 배포 |
| **FORWARD** | 이전 Consumer가 새 메시지 읽기 가능 | 필드 삭제, 필드 추가 (default 필수) | Producer 먼저 배포 |
| **FULL** | 양방향 호환 (BACKWARD + FORWARD) | 필드 추가/삭제 (default 필수) | 안전한 진화 |
| **NONE** | 호환성 검증 안 함 | 제약 없음 | 프로토타이핑 |

#### 호환성 모드 선택 가이드
```
배포 순서에 따라:
├── Consumer 먼저 배포 → BACKWARD (Consumer가 이전 메시지 읽을 수 있어야 함)
├── Producer 먼저 배포 → FORWARD (이전 Consumer가 새 메시지 읽을 수 있어야 함)
└── 동시 배포 또는 불확실 → FULL (양방향 호환)
```

### 5. Docker Compose 설정

```yaml
version: '3.8'
services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v24.2.4
    command:
      - redpanda start
      - --smp 1
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr internal://redpanda:8082,external://localhost:18082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:18081
    ports:
      - 18081:18081  # Schema Registry
      - 18082:18082  # HTTP Proxy
      - 19092:19092  # Kafka
      - 19644:9644   # Admin API
    healthcheck:
      test: ["CMD-SHELL", "rpk cluster health | grep -E 'Healthy:.+true' || exit 1"]
      interval: 15s
      timeout: 3s
      retries: 5

  console:
    image: docker.redpanda.com/redpandadata/console:latest
    entrypoint: /bin/sh
    command: -c "echo \"$$CONSOLE_CONFIG_FILE\" > /tmp/config.yml; /app/console"
    environment:
      CONFIG_FILEPATH: /tmp/config.yml
      CONSOLE_CONFIG_FILE: |
        kafka:
          brokers: ["redpanda:9092"]
          schemaRegistry:
            enabled: true
            urls: ["http://redpanda:8081"]
    ports:
      - 8080:8080
    depends_on:
      - redpanda
```

**핵심 설정**:
- Schema Registry: `18081` (외부), `8081` (내부)
- Console에서 스키마 관리 가능

### 6. Spring Boot Producer 구현

#### build.gradle
```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.kafka:spring-kafka'
    implementation 'org.apache.avro:avro:1.11.3'
    implementation 'io.confluent:kafka-avro-serializer:7.5.1'
}

repositories {
    mavenCentral()
    maven { url 'https://packages.confluent.io/maven/' }
}
```

#### application.yml
```yaml
spring:
  kafka:
    bootstrap-servers: localhost:19092
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
      properties:
        schema.registry.url: http://localhost:18081
        auto.register.schemas: true
```

**핵심 설정**:
- `KafkaAvroSerializer`: Avro 직렬화 + 스키마 자동 등록
- `auto.register.schemas: true`: 새 스키마 자동 등록

#### Avro 스키마 파일 (src/main/avro/OrderCreated.avsc)
```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.events",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "status", "type": "string"},
    {"name": "createdAt", "type": "long", "logicalType": "timestamp-millis"}
  ]
}
```

#### Gradle Avro 플러그인 설정
```gradle
plugins {
    id 'com.github.davidmc24.gradle.plugin.avro' version '1.9.1'
}

avro {
    createSetters = true
    fieldVisibility = "PRIVATE"
}
```

**빌드 시 자동 생성**: `build/generated-main-avro-java/com/example/events/OrderCreated.java`

#### Producer 서비스
```java
@Service
@RequiredArgsConstructor
public class OrderProducer {
    private final KafkaTemplate<String, OrderCreated> kafkaTemplate;

    public void sendOrder(String orderId, String customerId, double amount) {
        OrderCreated event = OrderCreated.newBuilder()
            .setOrderId(orderId)
            .setCustomerId(customerId)
            .setAmount(amount)
            .setStatus("CREATED")
            .setCreatedAt(System.currentTimeMillis())
            .build();

        kafkaTemplate.send("orders", orderId, event);
        log.info("Sent: {}", event);
    }
}
```

### 7. Spring Boot Consumer 구현

#### application.yml
```yaml
spring:
  kafka:
    bootstrap-servers: localhost:19092
    consumer:
      group-id: order-consumer
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: io.confluent.kafka.serializers.KafkaAvroDeserializer
      properties:
        schema.registry.url: http://localhost:18081
        specific.avro.reader: true
```

**핵심 설정**:
- `specific.avro.reader: true`: Generic Record 대신 생성된 클래스 사용

#### Consumer 리스너
```java
@Component
@Slf4j
public class OrderConsumer {
    @KafkaListener(topics = "orders", groupId = "order-consumer")
    public void consume(ConsumerRecord<String, OrderCreated> record) {
        OrderCreated order = record.value();
        log.info("Consumed: orderId={}, customerId={}, amount={}, status={}",
            order.getOrderId(), order.getCustomerId(), order.getAmount(), order.getStatus());
    }
}
```

### 8. 스키마 진화 시나리오

#### 시나리오 1: 필드 추가 (BACKWARD)
```
1. Producer 스키마에 paymentMethod 필드 추가 (default: null)
2. Producer 재배포 → Schema Registry에 v2 등록
3. 이전 Consumer는 paymentMethod 무시하고 기존 필드만 읽음
4. Consumer 재배포 → paymentMethod 사용
```

**Avro 스키마 v2**:
```json
{
  "fields": [
    ...,
    {"name": "paymentMethod", "type": ["null", "string"], "default": null}
  ]
}
```

#### 시나리오 2: 필드 이름 변경 (aliases)
```json
{
  "fields": [
    {"name": "amount", "type": "double", "aliases": ["totalAmount"]}
  ]
}
```

이전 메시지의 `totalAmount` 필드를 `amount`로 읽을 수 있음.

#### 시나리오 3: 필드 삭제 (FORWARD)
```
1. Consumer에서 해당 필드 사용 중단 → 재배포
2. Producer 스키마에서 필드 삭제 → 재배포
3. 이전 Consumer는 삭제된 필드를 무시 (FORWARD 호환)
```

### 9. Schema Registry API

#### 스키마 등록
```bash
curl -X POST http://localhost:18081/subjects/orders-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schema": "{\"type\":\"record\",\"name\":\"OrderCreated\",\"fields\":[...]}"
  }'
```

#### 스키마 조회
```bash
# 최신 버전
curl http://localhost:18081/subjects/orders-value/versions/latest

# 특정 ID
curl http://localhost:18081/schemas/ids/1
```

#### 호환성 검증
```bash
curl -X POST http://localhost:18081/compatibility/subjects/orders-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "..."}'
```

응답: `{"is_compatible": true}`

#### 호환성 모드 설정
```bash
# 전역 설정
curl -X PUT http://localhost:18081/config \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"compatibility": "FULL"}'

# Subject별 설정
curl -X PUT http://localhost:18081/config/orders-value \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"compatibility": "BACKWARD"}'
```

### 10. 실습 체크리스트

```
□ docker-compose up -d
□ Console 접속 (localhost:8080) → Schema Registry 메뉴 확인
□ Producer 실행 → 메시지 전송 → Registry에 스키마 v1 등록 확인
□ Consumer 실행 → 메시지 소비 확인
□ Avro 스키마에 필드 추가 (default 포함)
□ Producer 재시작 → 새 메시지 전송 → v2 등록 확인
□ 이전 버전 Consumer로 v2 메시지 읽기 테스트
□ Consumer 업데이트 → 새 필드 사용
□ rpk로 토픽 메시지 확인 (바이너리 + 스키마 ID)
```

### 11. 트러블슈팅

#### 스키마 호환성 오류
```
Error: Schema being registered is incompatible with an earlier schema
원인: BACKWARD 모드에서 default 없이 필수 필드 추가
해결: default 값 추가 또는 ["null", "type"] Union 사용
```

#### Specific Avro Reader 오류
```
Error: Could not find class com.example.events.OrderCreated
원인: specific.avro.reader=true인데 클래스 생성 안 됨
해결: gradle avro 플러그인 확인, ./gradlew generateAvroJava 실행
```

#### Schema Registry 연결 실패
```
Error: Failed to connect to schema registry
원인: 잘못된 URL 또는 Registry 미실행
해결: docker ps로 redpanda 상태 확인, 포트 18081 확인
```

### 12. 참고 자료
- [Avro 스펙](https://avro.apache.org/docs/current/spec.html)
- [Schema Registry API](https://docs.confluent.io/platform/current/schema-registry/develop/api.html)
- [Redpanda Schema Registry](https://docs.redpanda.com/current/manage/schema-registry/)
