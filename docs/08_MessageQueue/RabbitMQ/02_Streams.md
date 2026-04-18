# RabbitMQ Streams

## 1. 개요

RabbitMQ Streams는 **RabbitMQ 3.9.0 (2021년 7월)**에 도입된 새로운 데이터 구조입니다. Kafka와 유사한 **append-only 로그 기반 메시징**을 제공하며, 기존 RabbitMQ에서 불가능했던 메시지 재생(replay)과 장기 보존을 가능하게 합니다.

### 핵심 변화

```
기존 RabbitMQ Queue:
  메시지 소비 → 큐에서 삭제 → 재처리 불가

RabbitMQ Streams:
  메시지 소비 → 로그에 유지 → 무한 재처리 가능
```

---

## 2. Kafka와의 유사점

| 기능 | Apache Kafka | RabbitMQ Streams |
|------|-------------|------------------|
| **데이터 구조** | Append-only 로그 | Append-only 로그 |
| **메시지 불변성** | ✅ | ✅ |
| **오프셋 기반 소비** | ✅ | ✅ |
| **메시지 재생** | ✅ | ✅ |
| **다중 Consumer** | ✅ | ✅ |
| **장기 보존** | ✅ | ✅ |
| **처리량** | 100만+ msg/s | 100만+ msg/s (Stream 프로토콜) |

---

## 3. 아키텍처

### 저장 구조

```
Stream
├── Segment 1 (oldest)
│   ├── Message 0
│   ├── Message 1
│   └── ...
├── Segment 2
│   ├── Message N
│   └── ...
└── Segment 3 (newest)
    └── ...
```

### 특징
- **Segment 파일**: 메시지를 청크 단위로 저장
- **오프셋**: 각 메시지의 고유 위치 식별자
- **복제**: Quorum Queues와 동일하게 Raft 기반 복제

### 소비 모델

```
                    ┌─────────────┐
                    │   Stream    │
                    │ (Log-based) │
                    └─────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   Consumer A        Consumer B        Consumer C
   (offset: 0)       (offset: 100)     (offset: 500)

각 Consumer가 독립적인 오프셋으로 동일 데이터 읽기 가능
```

---

## 4. 지원 프로토콜

RabbitMQ Streams는 두 가지 방식으로 접근 가능:

### 1. AMQP 0-9-1 (기존 방식)
- 기존 RabbitMQ 클라이언트 사용 가능
- 상대적으로 낮은 성능

### 2. Stream Protocol (전용 바이너리 프로토콜)
- **고성능** (AMQP 대비 훨씬 빠름)
- 전용 클라이언트 필요
- 공식 지원: Java, Go, .NET, Rust, Python

---

## 5. 사용 방법

### Stream 생성

```java
// AMQP 방식
Map<String, Object> args = new HashMap<>();
args.put("x-queue-type", "stream");
args.put("x-max-length-bytes", 1_000_000_000L); // 1GB 보존
args.put("x-max-age", "7D"); // 7일 보존

channel.queueDeclare("my-stream", true, false, false, args);
```

### Stream Protocol 사용 (Java)

```java
// 의존성: com.rabbitmq:stream-client

Environment environment = Environment.builder()
    .host("localhost")
    .port(5552)  // Stream 전용 포트
    .build();

// Producer
Producer producer = environment.producerBuilder()
    .stream("my-stream")
    .build();

producer.send(
    producer.messageBuilder()
        .addData("Hello Streams".getBytes())
        .build(),
    confirmationStatus -> { }
);

// Consumer
Consumer consumer = environment.consumerBuilder()
    .stream("my-stream")
    .offset(OffsetSpecification.first())  // 처음부터 읽기
    .messageHandler((context, message) -> {
        System.out.println(new String(message.getBodyAsBinary()));
    })
    .build();
```

### 오프셋 지정

```java
// 처음부터
OffsetSpecification.first()

// 끝부터 (새 메시지만)
OffsetSpecification.last()

// 다음 메시지부터
OffsetSpecification.next()

// 특정 오프셋
OffsetSpecification.offset(12345)

// 타임스탬프 기준
OffsetSpecification.timestamp(timestamp)
```

---

## 6. 보존 정책

### 크기 기반 보존

```java
args.put("x-max-length-bytes", 5_000_000_000L); // 5GB까지 보존
```

### 시간 기반 보존

```java
args.put("x-max-age", "30D");  // 30일
args.put("x-max-age", "12h");  // 12시간
args.put("x-max-age", "7D");   // 7일
```

### Segment 크기

```java
args.put("x-stream-max-segment-size-bytes", 500_000_000L); // 500MB
```

---

## 7. Queue vs Stream 비교

| 특성 | Classic/Quorum Queue | Stream |
|------|---------------------|--------|
| **소비 시 삭제** | 예 | 아니오 |
| **재처리** | 불가 | 가능 |
| **다중 Consumer** | 경쟁적 소비 | 독립적 소비 |
| **오프셋 추적** | Broker 관리 | Consumer 관리 |
| **메시지 순서** | FIFO | FIFO + 오프셋 기반 접근 |
| **팬아웃** | Exchange 필요 | 네이티브 지원 |
| **백로그** | 메모리 부담 | 효율적 (디스크) |

---

## 8. 성능 특성

### 처리량

| 프로토콜 | 예상 처리량 |
|---------|------------|
| AMQP 0-9-1 | 5만-10만 msg/s |
| Stream Protocol | **100만+ msg/s** |

### 지연시간

- Stream Protocol 사용 시 매우 낮은 지연시간
- 대규모 팬아웃에서도 성능 유지

### 최적화 포인트
- **배치 전송**: 여러 메시지를 묶어서 전송
- **Sub-entry batching**: 하나의 엔트리에 여러 메시지 저장
- **압축**: 네트워크/스토리지 효율성 향상

---

## 9. Super Streams (파티셔닝)

Kafka의 파티션과 유사한 개념:

```
Super Stream: orders
├── orders-0 (partition 0)
├── orders-1 (partition 1)
└── orders-2 (partition 2)
```

### 생성

```bash
rabbitmq-streams add_super_stream orders --partitions 3
```

### 라우팅

```java
Producer producer = environment.producerBuilder()
    .superStream("orders")
    .routing(message -> message.getProperties().getCorrelationId())
    .producerBuilder()
    .build();
```

---

## 10. 사용 사례

### 적합한 경우
- **이벤트 소싱**: 이벤트 히스토리 전체 보존
- **감사 로그**: 규정 준수를 위한 장기 보존
- **대규모 팬아웃**: 수천 개의 Consumer
- **재처리 필요**: 버그 수정 후 재처리
- **시계열 데이터**: 메트릭, 로그 스트리밍
- **CDC (Change Data Capture)**: 데이터베이스 변경 추적

### 부적합한 경우
- **복잡한 라우팅**: Exchange 기반 라우팅 필요 → Queue 사용
- **작업 큐**: 소비 후 삭제 필요 → Queue 사용
- **요청-응답 패턴**: 전통적 메시징 필요

---

## 11. Streams vs Kafka

| 항목 | Kafka | RabbitMQ Streams |
|------|-------|------------------|
| **성숙도** | 높음 (2011~) | 중간 (2021~) |
| **에코시스템** | 풍부함 | 성장 중 |
| **Kafka 호환** | - | 없음 |
| **다중 프로토콜** | Kafka만 | AMQP, MQTT, Streams |
| **운영 복잡도** | 중간~높음 | 낮음~중간 |
| **하이브리드** | 스트림만 | 큐 + 스트림 혼합 가능 |

---

## 12. 모니터링

### CLI

```bash
# Stream 정보 확인
rabbitmq-streams list

# 상세 정보
rabbitmq-streams info <stream-name>

# Consumer 오프셋 추적
rabbitmq-streams stream_status <stream-name>
```

### 메트릭
- 메시지 수신/발신 속도
- 현재 오프셋
- 세그먼트 수
- 디스크 사용량

---

## 13. 참고 자료

- [RabbitMQ Streams Overview (2021)](https://blog.rabbitmq.com/posts/2021/07/rabbitmq-streams-overview/)
- [RabbitMQ Streams 공식 문서](https://www.rabbitmq.com/docs/streams)
- [Stream Java Client](https://github.com/rabbitmq/rabbitmq-stream-java-client)
- [RabbitMQ 3.9 Release Notes](https://github.com/rabbitmq/rabbitmq-server/releases/tag/v3.9.0)
