# 22. 공식 튜토리얼 보충 (Official Tutorial Supplement)

**Source**: [Redpanda 공식 블로그 - Building event-driven microservices with Spring Boot](https://www.redpanda.com/blog/build-event-driven-microservices-spring-boot)
**GitHub**: [redpanda-data/redpanda-examples](https://github.com/redpanda-data/redpanda-examples) (공식 예제 저장소)
**목적**: 기존 02-producer-consumer.md, 10-manual-commit-deep-dive.md와 중복되지 않는 3개 토픽만 보충한다.

---

## 1. auto-offset-reset 전략 비교

### 세 가지 옵션의 실제 동작 차이

Kafka/Redpanda는 컨슈머가 메시지를 어디서부터 읽을지 결정할 때, 먼저 **커밋된 오프셋**이 있는지 확인한다. 커밋된 오프셋이 없을 때만 `auto-offset-reset` 설정이 적용된다.

- **`latest`**: 컨슈머 그룹 최초 참여 시 새로운 메시지부터 소비. 기존 메시지는 건너뜀.
- **`earliest`**: 토픽의 처음부터(보존 정책 범위 내) 모든 메시지 소비. 재처리에 유용.
- **`none`**: 커밋된 오프셋이 없으면 `NoOffsetForPartitionException` 발생. 가장 엄격.

### 공식 튜토리얼이 `latest`를 선택한 이유

공식 튜토리얼의 coffeeshop 시나리오는 실시간 주문 처리 시스템이다.

**왜 `latest`인가?**
1. **비즈니스 요구사항**: 주문이 들어오면 즉시 처리하는 실시간 시스템
2. **과거 데이터 불필요**: 이미 처리된 과거 주문을 다시 처리할 필요 없음 → 새 주문만 관심
3. **개발/데모 편의**: 앱 재시작 시 이전 테스트 데이터가 재소비되지 않아 깨끗한 상태 유지

### 프로덕션 선택 기준

| 기준 | latest | earliest | none |
|------|--------|----------|------|
| 데이터 유실 허용 | O | X | X |
| 재처리 필요 | X | O | X |
| 첫 배포 시 과거 데이터 | 무시 | 전부 소비 | 에러 |
| 장애 복구 후 | 빠진 메시지 있을 수 있음 | 중복 가능하지만 누락 없음 | 명시적 제어 |
| 권장 시나리오 | 실시간 알림, 모니터링 | 이벤트 소싱, 감사 로그 | Exactly-once 요구 |

**핵심 원칙**: 메시지를 잃어도 되는가? → latest, 잃으면 안 되는가? → earliest 또는 none

### 기존 ch02와의 비교

```yaml
# ch02 application.yml
spring:
  kafka:
    consumer:
      auto-offset-reset: earliest  # 학습 목적: 모든 메시지 확인

# 공식 튜토리얼
spring:
  kafka:
    consumer:
      auto-offset-reset: latest    # 프로덕션 유사: 실시간 처리
```

**왜 ch02는 `earliest`를 사용했는가?**
- 학습 환경에서는 프로듀서가 먼저 메시지를 발행하고, 나중에 컨슈머를 시작하는 경우가 많다
- `earliest`를 사용하면 앱 재시작 시에도 이전에 발행한 테스트 메시지를 다시 확인할 수 있다
- 프로덕션에서는 보통 컨슈머가 먼저 떠 있고 메시지를 기다리므로 `latest`가 더 자연스럽다

### 흔한 실수: "earliest로 설정했는데 메시지가 다시 안 읽혀요"

```
시나리오 1: Consumer 처음 시작
  → 커밋된 오프셋 없음
  → auto-offset-reset: earliest 적용
  → 처음부터 읽기 ✓

시나리오 2: Consumer 재시작
  → 이전에 커밋된 오프셋 있음 (예: offset 100)
  → auto-offset-reset 무시됨
  → offset 100부터 읽기 (처음부터 읽지 않음) ✓

시나리오 3: 새 consumer group으로 시작
  → 이 그룹은 커밋된 오프셋 없음
  → auto-offset-reset: earliest 적용
  → 처음부터 읽기 ✓
```

**핵심 포인트**: `auto-offset-reset`은 **커밋된 오프셋이 없을 때만** 동작한다. 이미 오프셋이 커밋되어 있으면 이 설정은 무시되고, 마지막 커밋 지점부터 소비한다.

### "그러면 earliest와 latest가 뭐가 다른 거야?"

커밋된 오프셋이 있는 정상 운영 상태에서는 **둘 다 동일하게 동작**한다. 차이는 오프셋이 없거나 유효하지 않을 때만 드러난다.

| 상황 | `earliest` | `latest` |
|------|-----------|----------|
| 커밋된 오프셋 **있음** | 커밋 위치부터 재개 | 커밋 위치부터 재개 |
| 커밋된 오프셋 **없음** (신규 그룹) | 토픽 **처음**부터 | 토픽 **끝**부터 (새 메시지만) |
| 커밋된 오프셋이 **유효하지 않음** (retention으로 삭제됨) | 남아있는 가장 오래된 데이터부터 | 끝부터 (중간 데이터 스킵) |

즉 `auto.offset.reset`은 이름 그대로 "오프셋을 **리셋**해야 할 때의 정책"이지, 매번 consume할 때마다 적용되는 설정이 아니다. 차이가 실제로 드러나는 시나리오는 두 가지뿐이다.

1. **새 Consumer Group으로 처음 붙을 때** — `earliest`면 쌓여있던 메시지 전부 처리, `latest`면 지금부터 들어오는 것만
2. **오프셋이 날아갔을 때** (retention 만료, 토픽 재생성 등) — `earliest`면 복구 시도, `latest`면 과거 데이터 포기

**처음부터 다시 읽으려면?**
1. Consumer group ID를 변경하거나
2. 기존 오프셋을 삭제(`kafka-consumer-groups.sh --reset-offsets`)하거나
3. `seek()` API로 명시적으로 오프셋 이동

---

## 2. 파티션 기반 병렬 처리

### 파티션과 컨슈머 관계

Kafka/Redpanda에서 **파티션은 병렬 처리의 단위**다. 이는 물리적인 제약이자 설계 원칙이다.

**핵심 규칙**: 하나의 파티션은 **컨슈머 그룹 내에서** 하나의 컨슈머에게만 할당된다.

**왜 이런 제약이 있는가?**
- **순서 보장**: 하나의 파티션 내에서는 메시지 순서가 보장되어야 한다
- **동시 접근 방지**: 여러 컨슈머가 같은 파티션의 오프셋을 커밋하면 충돌 발생
- **명확한 책임 분리**: 파티션 단위로 처리 책임이 명확히 나뉜다

### 시뮬레이션: 5 파티션 토픽

```
토픽: coffeeshop-orders (5 파티션)

Case 1: 컨슈머 3개 < 파티션 5개
  Consumer-1: [P0, P1]  ← 2개 파티션 담당
  Consumer-2: [P2, P3]  ← 2개 파티션 담당
  Consumer-3: [P4]      ← 1개 파티션 담당
  → 일부 컨슈머가 2개 파티션 담당 (부하 불균형)

Case 2: 컨슈머 5개 = 파티션 5개
  Consumer-1: [P0]
  Consumer-2: [P1]
  Consumer-3: [P2]
  Consumer-4: [P3]
  Consumer-5: [P4]
  → 최적 분배 (1:1 매핑)

Case 3: 컨슈머 7개 > 파티션 5개
  Consumer-1: [P0]
  Consumer-2: [P1]
  Consumer-3: [P2]
  Consumer-4: [P3]
  Consumer-5: [P4]
  Consumer-6: [idle]  ← 유휴 상태
  Consumer-7: [idle]  ← 유휴 상태
  → 파티션 수를 초과한 컨슈머는 놀게 됨
```

**결론**: 최대 병렬도 = 파티션 수. 컨슈머를 아무리 늘려도 파티션보다 많으면 의미 없다.

### Spring Kafka concurrency 설정

단일 애플리케이션 인스턴스에서 여러 컨슈머 스레드를 운영할 수 있다.

```yaml
spring:
  kafka:
    listener:
      concurrency: 3  # 3개의 KafkaMessageListenerContainer 생성
```

```java
// 또는 리스너 레벨에서 지정
@KafkaListener(topics = "coffeeshop-orders", concurrency = "3")
public void consume(OrderEvent event) {
    // 3개 스레드가 각각 파티션을 담당
    log.info("Thread: {}, Message: {}",
             Thread.currentThread().getName(),
             event);
}
```

**주의사항**:
- `concurrency`가 파티션 수보다 크면 남는 스레드는 idle
- 각 스레드가 독립된 Consumer로 동작하므로 **스레드 안전성** 고려 필요
- **메시지 순서**: 같은 파티션 내에서만 보장, 다른 파티션 간에는 보장 안 됨

### 리밸런싱 시나리오

리밸런싱(Rebalancing)은 컨슈머 그룹의 파티션 할당이 재조정되는 과정이다.

**발생 조건**:
1. 새로운 컨슈머가 그룹에 참여 (스케일 아웃)
2. 기존 컨슈머가 그룹에서 이탈 (크래시, 네트워크 장애, 정상 종료)
3. 토픽에 파티션이 추가됨
4. `session.timeout.ms` 내에 heartbeat가 도착하지 않음

**리밸런싱 중 일시적으로 메시지 처리가 중단된다** — 이것이 과도한 스케일 아웃을 피해야 하는 이유.

### partition.assignment.strategy 비교

| 전략 | 설명 | 장점 | 단점 |
|------|------|------|------|
| RangeAssignor (기본) | 토픽별로 파티션을 연속 범위로 할당 | 예측 가능 | 불균형 가능 |
| RoundRobinAssignor | 전체 파티션을 라운드로빈 분배 | 균등 분배 | 토픽 간 관계 무시 |
| StickyAssignor | 기존 할당을 최대한 유지하며 재분배 | 리밸런싱 비용 최소화 | 약간의 불균형 허용 |
| CooperativeStickyAssignor | Sticky + 점진적 리밸런싱 | 처리 중단 최소화 | 복잡도 증가 |

**권장**: CooperativeStickyAssignor (Kafka 3.x+, Redpanda 호환)

```yaml
spring:
  kafka:
    consumer:
      properties:
        partition.assignment.strategy: org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```

---

## 3. 기존 ch02와 공식 튜토리얼 패턴 비교

### 구조 비교 테이블

| 항목 | ch02 (OrderProducer/Consumer) | 공식 튜토리얼 (Coffeeshop) |
|------|------|------|
| **직렬화** | Avro + Schema Registry | JSON (Jackson) |
| **auto-offset-reset** | earliest | latest |
| **메시지 키** | orderId (명시적) | 없음 (null) |
| **커밋 방식** | Manual ACK | Auto commit (기본) |
| **에러 처리** | TODO (미구현) | 기본 Spring 에러 핸들러 |
| **파티션** | 3개 | 5개 |
| **스키마 진화** | Schema Registry로 호환성 관리 | JSON이라 스키마 관리 없음 |
| **목적** | 학습 (모든 기능 시연) | 데모 (단순함 우선) |

### JsonSerializer vs Avro 직렬화 트레이드오프

| 기준 | JSON (Jackson) | Avro + Schema Registry |
|------|---------|------|
| **설정 복잡도** | 낮음 (기본 제공) | 높음 (Registry 필요) |
| **메시지 크기** | 큼 (필드명 포함) | 작음 (바이너리, 스키마 ID만) |
| **스키마 진화** | 런타임 에러 (필드 추가/제거 시) | 호환성 규칙으로 안전하게 진화 |
| **디버깅** | 쉬움 (사람이 읽을 수 있음) | 어려움 (바이너리, 도구 필요) |
| **타입 안전성** | 런타임 | 컴파일 타임 (코드 생성) |
| **프로덕션 적합성** | PoC, 소규모 | 대규모, 마이크로서비스 |

**핵심 판단 기준**:
- "프로듀서와 컨슈머를 같은 팀이 관리하는가?" → JSON도 괜찮음
- "여러 팀이 같은 토픽을 소비하는가?" → Avro + Schema Registry 필수

### Consumer Group 활용 패턴 차이

```
ch02 패턴: 단일 Consumer Group
  group-id: redpanda-spring-boot
  → 모든 Consumer가 하나의 그룹, 메시지 분산 처리

공식 튜토리얼 패턴: 다중 Consumer Group (암시적)
  각 마이크로서비스가 독립 group-id
  → inventory-service, notification-service 등이 각자의 그룹으로 주문 이벤트 소비
```

**다중 Consumer Group이 가능한 이유**: Kafka/Redpanda는 토픽의 메시지를 삭제하지 않고, 각 Consumer Group이 독립적인 오프셋을 관리한다. 따라서 하나의 메시지를 여러 그룹이 각각 읽을 수 있다.

---

## 핵심 요약

1. **auto-offset-reset**: 커밋된 오프셋이 없을 때만 동작. earliest(안전), latest(실시간), none(엄격).
2. **파티션 병렬 처리**: 파티션 수 = 최대 병렬도. concurrency 설정으로 단일 인스턴스 내 병렬화. 리밸런싱 비용 주의.
3. **JSON vs Avro**: 소규모/단일팀이면 JSON, 대규모/다팀이면 Avro. 스키마 진화가 판단 기준.
