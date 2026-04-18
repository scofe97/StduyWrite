# RabbitMQ Streams - 면접 정리

## 핵심 한 줄 정리

> **RabbitMQ Streams는 2021년 도입된 Kafka 스타일의 append-only 로그로, 소비 후에도 메시지가 삭제되지 않아 재생(replay)과 다중 Consumer 독립 소비가 가능합니다.**

---

## 면접 필수 암기

### Q1. RabbitMQ Streams란 무엇인가요?

**답변 (30초):**
> RabbitMQ Streams는 3.9(2021년)에 도입된 새로운 데이터 구조입니다. 기존 Queue와 달리 **append-only 로그** 방식으로, 메시지 소비 후에도 삭제되지 않습니다. 이를 통해 Kafka처럼 **오프셋 기반 재생**, **다중 Consumer 독립 소비**, **장기 메시지 보존**이 가능합니다. 전용 Stream 프로토콜 사용 시 100만 msg/s 이상의 처리량을 달성할 수 있습니다.

---

### Q2. 기존 Queue와 Streams의 핵심 차이는?

**답변:**

| 항목 | Queue | Stream |
|------|-------|--------|
| **소비 시 삭제** | 삭제됨 | **삭제 안 됨** |
| **재처리** | 불가 | **가능** (오프셋 기반) |
| **다중 Consumer** | 경쟁적 소비 | **독립적 소비** |
| **백로그 효율** | 메모리 부담 | **디스크 효율적** |
| **팬아웃** | Exchange 필요 | **네이티브 지원** |

> 핵심 차이를 한 문장으로: "Queue는 소비하면 사라지고, Stream은 소비해도 남아있다."

---

### Q3. RabbitMQ Streams가 Kafka와 같은 점과 다른 점은?

**같은 점:**
> - Append-only 로그 구조
> - 오프셋 기반 소비
> - 메시지 불변성 및 보존
> - 100만+ msg/s 처리량

**다른 점:**
> - RabbitMQ는 **Queue + Streams 하이브리드** 가능
> - **다중 프로토콜** 지원 (AMQP, MQTT로도 접근 가능)
> - Kafka Connect 같은 **에코시스템은 부족**
> - 2021년 도입으로 **성숙도가 낮음**

---

### Q4. Streams의 오프셋 지정 방식을 설명해주세요.

**답변:**
> ```java
> OffsetSpecification.first()      // 처음부터
> OffsetSpecification.last()       // 마지막(새 메시지만)
> OffsetSpecification.next()       // 다음 메시지부터
> OffsetSpecification.offset(100)  // 특정 오프셋
> OffsetSpecification.timestamp(t) // 특정 시간 이후
> ```
>
> 이를 통해 "어제 오후 3시부터 다시 처리", "오프셋 1000번부터 재생" 같은 요구사항을 쉽게 구현할 수 있습니다.

---

### Q5. Streams를 언제 사용해야 하나요?

**적합한 경우:**
> - **이벤트 소싱**: 이벤트 히스토리 전체 보존
> - **감사 로그**: 규정 준수를 위한 장기 보존
> - **대규모 팬아웃**: 수천 Consumer가 같은 데이터 읽기
> - **버그 수정 후 재처리**: 과거 데이터 다시 처리
> - **시계열 데이터**: 메트릭, 로그 수집

**부적합한 경우:**
> - 복잡한 라우팅이 필요 → Queue 사용
> - 작업 큐 패턴 (소비 후 삭제) → Queue 사용
> - 요청-응답 패턴 → Queue 사용

---

## 깊은 이해를 위한 설명

### 왜 Streams가 필요했나?

RabbitMQ의 전통적인 Queue 모델에는 근본적인 한계가 있었습니다:

**시나리오: 버그로 인한 데이터 오염**
```
Queue 모델:
1. Consumer가 버그 있는 코드로 메시지 처리
2. 처리 완료 → Ack → 메시지 삭제
3. 버그 발견!
4. 😱 이미 삭제된 메시지는 복구 불가
```

```
Stream 모델:
1. Consumer가 버그 있는 코드로 메시지 처리
2. 처리 완료 → 오프셋 기록 → 메시지 유지
3. 버그 발견!
4. 😊 오프셋을 과거로 되돌려 재처리
```

이런 **재처리 가능성**이 이벤트 소싱, 감사 로그, CQRS 패턴에서 필수적입니다.

### Pull vs Push: Streams는 어떤 모델?

RabbitMQ Queue는 **Push** 모델이지만, Streams는 **Pull** 모델입니다:

```
Queue (Push):
Broker ─────push────▶ Consumer
                       (prefetch로 흐름 제어)

Stream (Pull):
Consumer ◀───pull───── Broker
                       (Consumer가 속도 제어)
```

> 이것이 Streams가 Kafka와 유사한 이유입니다. Consumer가 원하는 오프셋에서 원하는 속도로 가져갑니다.

### Super Streams: Kafka 파티션 대응

```
Super Stream: orders
├── orders-0  (partition 0)
├── orders-1  (partition 1)
└── orders-2  (partition 2)

Producer: Routing Key로 파티션 결정
Consumer: 파티션별 병렬 소비
```

> Kafka의 파티셔닝과 동일한 패턴을 RabbitMQ에서 구현한 것입니다. 처리량 확장과 순서 보장을 양립할 수 있습니다.

---

## 코드 레벨 이해

### Stream 생성

```java
Map<String, Object> args = new HashMap<>();
args.put("x-queue-type", "stream");
args.put("x-max-length-bytes", 1_000_000_000L);  // 1GB까지 보존
args.put("x-max-age", "7D");  // 7일 보존

channel.queueDeclare("events", true, false, false, args);
```

### Stream Protocol (고성능)

```java
// 전용 포트 5552 사용
Environment env = Environment.builder()
    .host("localhost")
    .port(5552)
    .build();

// Consumer: 특정 오프셋부터 읽기
Consumer consumer = env.consumerBuilder()
    .stream("events")
    .offset(OffsetSpecification.offset(1000))
    .messageHandler((ctx, msg) -> {
        // 처리
        ctx.storeOffset();  // 오프셋 저장
    })
    .build();
```

> Stream Protocol은 AMQP보다 **훨씬 빠릅니다**. 고처리량이 필요하면 반드시 전용 클라이언트를 사용하세요.

### 보존 정책

```java
// 크기 기반: 5GB 초과 시 오래된 것부터 삭제
args.put("x-max-length-bytes", 5_000_000_000L);

// 시간 기반: 30일 지나면 삭제
args.put("x-max-age", "30D");

// 둘 다 설정 시: 둘 중 하나라도 만족하면 삭제
```

---

## 면접 예상 꼬리 질문

### Q. Streams에서 Consumer Group은 어떻게 동작하나요?

**답변:**
> RabbitMQ Streams는 Kafka와 달리 **명시적 Consumer Group 개념이 없습니다**. 대신 각 Consumer가 **자체적으로 오프셋을 관리**합니다. 같은 Stream을 여러 Consumer가 읽어도 서로 영향을 주지 않습니다. 
>
> Kafka 스타일의 Consumer Group(파티션 할당)이 필요하면 **Super Streams + Single Active Consumer** 패턴을 사용합니다.

### Q. Streams와 Quorum Queue를 함께 쓸 수 있나요?

**답변:**
> 네, 같은 클러스터에서 **용도에 따라 혼용**할 수 있습니다:
> - **Quorum Queue**: 작업 큐, 요청-응답, 복잡한 라우팅
> - **Streams**: 이벤트 로그, 감사 추적, 데이터 파이프라인
>
> 이것이 RabbitMQ의 장점입니다. Kafka는 Stream만 지원하지만, RabbitMQ는 두 패러다임을 모두 지원합니다.

### Q. Streams를 쓰면 Kafka가 필요 없나요?

**답변:**
> 상황에 따릅니다.
>
> **Streams로 충분한 경우:**
> - 스트리밍 + 큐 두 패러다임이 모두 필요
> - 기존 RabbitMQ 인프라 활용
> - 중간 규모 처리량 (수십만 msg/s)
>
> **Kafka가 더 나은 경우:**
> - 대규모 스트리밍이 **핵심** (수백만 msg/s)
> - Kafka Connect, ksqlDB 등 **에코시스템** 필요
> - **검증된 프로덕션 경험**이 중요 (Streams는 2021년~)

### Q. RabbitMQ에서 "메시지 보존이 안 된다"는 말은 더 이상 맞지 않나요?

**답변:**
> 맞습니다. **2021년 Streams 도입 이후로는 틀린 말**입니다. 
>
> - 2021년 이전: Queue 기반으로 소비 시 삭제 → "보존 안 됨"
> - 2021년 이후: Streams로 Kafka 스타일 보존 가능 → "보존 됨"
>
> 다만 Streams는 비교적 최신 기능이라, 레거시 문서나 오래된 비교 자료에서는 여전히 "RabbitMQ는 보존 안 됨"으로 설명하는 경우가 있습니다.
