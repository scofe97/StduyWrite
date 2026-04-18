# CQRS & Event Sourcing: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. Eventually Consistent 읽기 모델 지연 허용 범위 — 어느 정도 지연이 수용 가능하고, 지연을 줄이는 방법은

### 왜 이 질문이 중요한가

CQRS 읽기 모델은 Command Side의 이벤트가 Kafka를 거쳐 State Store에 반영되기까지 수십 ms에서 수 초의 지연이 존재한다. 면접에서 "eventual consistency를 어떻게 다루었나"라는 질문은 이 지연을 단순히 "허용한다"고 답하는 사람과, 비즈니스 요구사항에 따라 허용 범위를 정의하고 엔지니어링으로 줄였다는 사람을 구분하는 기준이 된다. 실무에서는 지연이 SLA를 위반하거나 사용자에게 혼란을 주는 시나리오(예: 글 작성 직후 목록에서 안 보임)를 설계 단계에서 인지하지 못하면 재설계 비용이 크다.

### 답변

허용 범위는 도메인의 성격으로 결정한다. 소셜 피드·대시보드처럼 "조금 오래된 데이터도 괜찮다"는 도메인은 수 초 지연이 무방하다. 반면 재고·결제처럼 "방금 내가 결제한 잔액이 즉시 반영되어야 한다"는 도메인은 수백 ms 이내가 요구된다.

**지연을 줄이는 방법 세 가지**

첫째, Kafka Streams의 `commit.interval.ms`와 `cache.max.bytes.buffering`을 낮춘다. 기본값은 30,000ms와 10MB인데, 이를 각각 1,000ms와 0으로 설정하면 처리 지연이 줄어드는 대신 처리량이 감소한다.

```yaml
# application.yml
spring:
  kafka:
    streams:
      properties:
        commit.interval.ms: 1000
        cache.max.bytes.buffering: 0
```

둘째, Write-through 패턴을 사용한다. Command Service가 DB에 쓰는 동시에 Read Model(Redis 등)도 직접 갱신한다. 이중 쓰기의 원자성 문제가 생기지만, 지연은 사실상 0에 가깝다.

셋째, Read-your-writes 보장을 위해 Command 응답에 offset을 포함하고, Query Side에서 해당 offset이 처리된 뒤 응답하는 패턴을 쓴다. Kafka Streams의 `KafkaStreams.store()`에 standby 조회를 막고, 처리된 `currentOffset >= requestedOffset`일 때만 결과를 반환한다.

어느 방법도 은탄환이 아니다. 지연 단축은 처리량 감소 또는 아키텍처 복잡도와 트레이드오프 관계에 있으므로, 비즈니스 SLA를 먼저 명확히 정의한 뒤 가장 단순한 방법부터 시도하는 것이 원칙이다.

---

## Q2. State Store 장애 복구 — RocksDB changelog 기반 복구 시간과 standby replica 전략

### 왜 이 질문이 중요한가

Kafka Streams의 State Store(RocksDB)는 로컬 디스크에 상태를 유지하기 때문에, 인스턴스가 재시작되거나 다른 노드로 파티션이 이동하면 changelog 토픽에서 전체 상태를 복구해야 한다. 복구 시간 동안 해당 파티션의 Interactive Query는 응답 불가 상태가 되므로, 운영팀은 복구 전략을 사전에 설계해야 한다. 면접에서 "Kafka Streams로 CQRS를 구성할 때 장애 복구를 어떻게 처리하나"라는 질문이 자주 등장하며, 단순히 "changelog에서 복구된다"고 답하는 것은 불충분하다.

### 답변

RocksDB는 로컬 상태를 유지하고, Kafka Streams는 상태 변경을 자동으로 changelog 토픽(`<app-id>-<store-name>-changelog`)에 기록한다. 인스턴스 재시작 시 이 changelog를 처음부터 재생하여 상태를 복구하는데, 토픽에 쌓인 이벤트가 많을수록 복구 시간이 길어진다. 이벤트 1억 건이면 수십 분이 걸릴 수 있다.

**standby replica 전략**

`num.standby.replicas`를 1 이상으로 설정하면, 다른 인스턴스가 동일한 State Store의 복사본을 항상 최신 상태로 유지한다. Primary 인스턴스가 다운되면 standby가 거의 즉시 Active로 전환되어 복구 시간이 수초 이내로 줄어든다.

```yaml
spring:
  kafka:
    streams:
      properties:
        num.standby.replicas: 1
```

Standby 인스턴스는 Interactive Query에 직접 응답하지 않지만, `StreamsMetadata`를 통해 Active 인스턴스의 호스트를 알아내어 요청을 포워딩하는 패턴과 결합하면 failover 시나리오에서도 쿼리 가용성을 유지할 수 있다. 비용 측면에서는 인스턴스 수가 늘어나므로, State Store 크기와 허용 복구 시간 SLA를 기준으로 standby 수를 결정한다.

---

## Q3. Event Sourcing에서 스키마 진화 — 이벤트 버전 관리와 upcasting 전략

### 왜 이 질문이 중요한가

이벤트 스트림은 append-only이다. 한번 저장된 이벤트는 수정할 수 없으므로, 필드를 추가하거나 이름을 바꾸거나 타입을 변경하는 순간 기존 이벤트를 읽는 Consumer가 깨질 수 있다. 실무에서는 "2년 전 이벤트를 오늘의 Consumer가 그대로 읽어야 한다"는 요구사항이 일상적이며, 스키마 진화를 설계 초기부터 고려하지 않으면 리플레이 시 호환성 문제로 전체 이벤트 스트림이 무용지물이 된다.

### 답변

스키마 진화 전략은 크게 두 가지로 나뉜다.

**Avro/Schema Registry 기반 호환성 관리**

Confluent Schema Registry(Redpanda 내장)는 스키마 변경 시 호환성을 검증한다. `BACKWARD` 호환성 설정에서는 새 필드에 기본값을 부여해야 하므로, 기존 Consumer가 옛 이벤트도 새 스키마로 읽을 수 있다. 필드를 삭제하거나 타입을 바꾸는 breaking change는 `FULL_TRANSITIVE` 검증에서 차단된다.

```json
// v1
{ "type": "record", "name": "OrderPlaced",
  "fields": [{"name": "orderId", "type": "string"}] }

// v2 — 필드 추가, 기본값 필수
{ "type": "record", "name": "OrderPlaced",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string", "default": "unknown"}
  ]
}
```

**Upcasting 전략**

Breaking change가 불가피하거나 이미 저장된 이벤트를 마이그레이션해야 할 때는 Upcaster 패턴을 쓴다. Consumer가 이벤트를 읽을 때 버전 필드(`eventVersion`)를 확인하여 구버전 이벤트를 현재 버전으로 변환하는 변환기(Upcaster)를 거친다. 이는 Axon Framework에서 공식 지원하는 패턴이다.

```java
// v1 이벤트를 v2로 업캐스팅
if ("OrderPlaced".equals(event.getType()) && event.getVersion() == 1) {
    return new OrderPlacedV2(event.orderId, "unknown"); // customerId 기본값 삽입
}
```

원칙은 "이벤트는 절대 수정하지 않고, 변환은 읽기 시점에 적용한다"이다. 이로써 Event Store의 불변성을 유지하면서 스키마 진화를 흡수한다.

---

## Q4. CQRS에서 쿼리 모델 선택 — RDB vs Elasticsearch vs Redis, 각각 언제 쓰는가

### 왜 이 질문이 중요한가

CQRS의 Query Side는 쓰기 모델과 완전히 독립적으로 최적화할 수 있다. 그러나 "읽기 모델을 어디에 두냐"는 선택은 조회 패턴, 지연 요구사항, 운영 복잡도에 따라 달라진다. 면접에서 "왜 Elasticsearch를 Query Side로 선택했나"라는 질문에 단순히 "검색이 빠르니까"라고 답하면 설계 의도가 없어 보인다. 각 저장소의 강점과 한계를 명확히 알고, 요구사항에 맞게 선택하는 능력이 시니어 레벨에서 중요하다.

### 답변

세 가지 저장소의 적합한 시나리오는 다음과 같다.

| 저장소 | 최적 시나리오 | 주의점 |
|--------|-------------|--------|
| **RDB** (PostgreSQL 등) | 복잡한 집계, 관계형 조인, ACID 보장이 필요한 리포트 | 대용량 전문 검색 성능이 낮음 |
| **Elasticsearch** | 전문 검색(full-text), 멀티 필드 필터, 패싯 집계 | 실시간 일관성 약함, 운영 복잡도 높음 |
| **Redis** | 초저지연 단순 조회, 캐시, 세션, 카운터 | 메모리 비용, 복잡한 쿼리 불가 |

**구체적 예시**

쇼핑몰의 상품 목록(카테고리 필터 + 키워드 검색 + 가격 정렬)은 Elasticsearch가 적합하다. 상품 상세 페이지처럼 단일 ID 조회라면 Redis 캐시가 가장 빠르다. 월별 매출 집계 리포트는 RDB의 집계 쿼리가 적합하다.

Kafka Streams의 State Store(RocksDB)는 위 세 가지와 별도로, Kafka 이벤트에서 직접 Materialized View를 구축할 때 쓴다. 외부 저장소 없이 JVM 인프라 안에서 Interactive Query를 제공한다는 장점이 있지만, 수평 확장 시 파티션 간 쿼리 라우팅을 직접 구현해야 한다. 요구사항이 복잡한 검색이라면 Kafka Connect Sink로 Elasticsearch에 이벤트를 흘려보내는 것이 현실적이다.

---

## Q5. Event Replay 위험성 — 전체 리플레이 vs 스냅샷, 부작용 방지 전략

### 왜 이 질문이 중요한가

Event Replay는 Event Sourcing의 가장 강력한 기능이지만, 잘못 실행하면 이메일 재발송, 결제 재처리, 외부 API 중복 호출 같은 실제 부작용을 일으킨다. 면접에서 "프로덕션에서 리플레이를 어떻게 안전하게 하나"라는 질문은 이론 지식과 운영 경험을 동시에 검증한다. 리플레이 전략을 모르면 "그냥 consumer group을 earliest로 리셋하면 되지 않나"라는 위험한 답변을 하게 된다.

### 답변

**전체 리플레이 vs 스냅샷**

전체 리플레이는 이벤트 스트림의 처음부터 재생하므로 정확하지만, 이벤트가 수억 건이면 수 시간이 걸린다. 스냅샷 패턴은 특정 오프셋에서 상태를 직렬화하여 저장해두고, 그 시점부터만 재생한다. 복구 시간을 수분 이내로 줄일 수 있다.

```
전체 리플레이: Offset 0 → 현재 (느리지만 단순)
스냅샷 리플레이: Snapshot@Offset 10,000,000 + Offset 10,000,001 → 현재 (빠르지만 스냅샷 관리 필요)
```

**부작용 방지 전략 세 가지**

첫째, 이벤트 핸들러를 부작용과 순수 함수로 분리한다. 상태 계산 핸들러(순수 함수)와 외부 시스템 호출 핸들러(이메일, 결제)를 별도 Consumer Group으로 구성하여, 리플레이 시 순수 함수 핸들러만 구동한다.

둘째, `replay` 플래그를 이벤트 헤더에 포함하고, 부작용이 있는 핸들러는 이 플래그가 `true`이면 처리를 건너뛴다.

```java
if (headers.get("x-replay") != null) {
    // 외부 API 호출, 이메일 발송 등 부작용 생략
    return;
}
sendEmail(event);
```

셋째, Kafka의 `Streams Reset Tool`(파괴적)보다 별도 Consumer Group으로 리플레이하는 비파괴적 방식을 선호한다. 기존 Consumer Group의 오프셋을 건드리지 않으므로 운영 중인 서비스에 영향을 주지 않고 리플레이 결과를 검증한 뒤 반영할 수 있다.

리플레이 자체를 안전하게 만들려면 이벤트 핸들러의 멱등성이 전제되어야 한다. 동일 이벤트를 두 번 처리해도 결과가 같은 핸들러를 설계하는 것이 리플레이 전략의 가장 근본적인 기반이다.
