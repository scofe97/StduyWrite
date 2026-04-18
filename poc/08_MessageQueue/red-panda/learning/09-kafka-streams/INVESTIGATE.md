# Kafka Streams: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

---

## Q1. Facts vs Deltas — KTable에 전체 상태를 넣어야 할까, 변경분만 넣어야 할까

### 왜 이 질문이 중요한가

Kafka Streams를 처음 도입하는 팀이 가장 먼저 부딪히는 설계 결정이 이 질문이다. 선택에 따라 소비자의 코드 복잡도, 토픽의 저장 용량, Log Compaction 효과가 완전히 달라진다. 면접에서는 "KTable이 무엇인가"보다 "언제 Delta 대신 Fact를 써야 하는가"를 더 자주 묻는다.

### 답변

**Fact(전체 상태)**는 소비자가 이전 이벤트를 기억하지 않아도 되는 상황에 적합하다. KTable에 Fact를 넣으면 Log Compaction이 키별 최신 값만 보존하므로, 테이블 크기가 엔티티 수에 비례하고 Storage Store 복구도 빠르다. 소비자 쪽에서 상태를 별도로 관리할 필요가 없다는 것이 핵심 장점이다.

```java
// Fact 이벤트: 소비자는 이 레코드 하나로 현재 상태를 알 수 있다
KTable<String, UserProfile> profiles = builder.table("user-profiles",
    Materialized.as("profiles-store"));
```

**Delta(변경분)**는 원천 시스템이 변경된 필드만 알려주는 경우(예: CDC, 감사 로그)에 불가피하게 사용한다. 소비자는 `aggregate()`로 누적해야 현재 상태를 얻을 수 있다. 페이로드가 작아 네트워크 비용이 낮지만, 순서가 어긋나면 상태가 깨진다.

```java
// Delta 이벤트를 누적해 Fact로 변환하는 패턴
KTable<String, UserProfile> current = stream
    .groupByKey()
    .aggregate(
        UserProfile::empty,
        (key, delta, acc) -> acc.applyDelta(delta),
        Materialized.as("profiles-store")
    );
```

**선택 기준**: 소비자가 여러 개이고 각자 현재 상태가 필요하다면 Fact가 낫다. 변경 이력 자체가 비즈니스 가치를 가진다면(감사, 분쟁 해결) Delta를 보존하되 별도 Fact 토픽을 파생시키는 하이브리드를 고려한다.

---

## Q2. KTable 조인 성능 — KStream-KTable vs KTable-KTable, State Store 크기가 미치는 영향

### 왜 이 질문이 중요한가

조인은 Kafka Streams에서 가장 비싼 연산이다. 프로덕션에서 처리 지연이 발생할 때 원인이 조인인 경우가 많고, 두 조인 방식의 동작 차이를 모르면 잘못된 방향으로 튜닝한다. 면접에서는 "KStream-KTable 조인이 어떻게 동작하나"를 물어보며 내부 메커니즘 이해를 확인한다.

### 답변

**KStream-KTable 조인**은 스트림 레코드가 도착할 때마다 KTable의 현재 값을 로컬 State Store에서 조회한다. KTable 갱신이 먼저 도착해야 조인 결과가 나온다 — 순서가 맞지 않으면 `null`이 반환된다. State Store는 KTable 전체를 로컬에 저장하므로, KTable 크기가 GB 단위면 각 인스턴스의 힙과 디스크 사용량이 그만큼 증가한다.

```java
KStream<String, EnrichedOrder> enriched = orders
    .join(customersTable,                    // 로컬 State Store 조회 (RPC 없음)
          (order, customer) -> enrich(order, customer),
          Joined.with(Serdes.String(), orderSerde, customerSerde));
```

**KTable-KTable 조인**은 양쪽 모두 변경될 때 결과를 재계산하며, 결과 자체도 KTable이다. 양쪽 State Store를 모두 보유하므로 메모리 사용량이 두 배가 된다. Foreign Key Join(`KTable.join(KTable, keyExtractor, ...)`)은 추가로 리파티셔닝 토픽이 생겨 레이턴시가 더 높다.

**성능 관계**: State Store 크기는 `num.stream.threads`와 파티션 수로 분산된다. 파티션이 8개이고 인스턴스가 4개면, 각 인스턴스는 KTable의 1/4만 보유한다. State Store가 크면 RocksDB 캐시 크기(`rocksdb.block.cache.size`)를 늘려 디스크 I/O를 줄인다.

```properties
# 대용량 KTable 튜닝 예시
num.stream.threads=4
rocksdb.block.cache.size=268435456   # 256MB
statestore.cache.max.bytes=10485760  # 10MB
```

---

## Q3. Streams Reset 위험성 — application.id 리셋 시 무슨 일이 벌어지는가

### 왜 이 질문이 중요한가

`kafka-streams-application-reset` 도구는 "재처리가 필요할 때 쓰는 것"으로 단순하게 알려져 있지만, 실행 즉시 State Store를 삭제하고 오프셋을 되돌린다. 이를 프로덕션에서 잘못 사용하면 다운타임 없이 데이터 정합성이 깨질 수 있다. 면접에서는 "운영 중 재처리가 필요하면 어떻게 하겠는가"라는 질문으로 이 지식을 검증한다.

### 답변

리셋이 실행되면 세 가지 일이 순서대로 일어난다. 첫째, 입력 토픽 오프셋을 beginning으로 되돌린다. 둘째, 내부 changelog 토픽과 repartition 토픽을 삭제한다. 셋째, 로컬 State Store 디렉토리(`state.dir`)를 삭제한다. 애플리케이션이 재시작되면 처음부터 다시 처리하며 State Store를 재구축한다.

**프로덕션 안전 절차:**

```bash
# 1. 모든 인스턴스 종료 확인 (리셋 전 반드시 필요)
# 실행 중인 인스턴스가 있으면 리셋이 부분 적용되어 상태가 불일치함
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-app-id --describe

# 2. 리셋 실행 (dry-run 먼저)
kafka-streams-application-reset.sh \
  --application-id my-app-id \
  --bootstrap-servers localhost:9092 \
  --dry-run

# 3. 실제 리셋
kafka-streams-application-reset.sh \
  --application-id my-app-id \
  --bootstrap-servers localhost:9092 \
  --input-topics orders,customers
```

출력 토픽은 리셋해도 자동으로 비워지지 않는다. 재처리 결과가 출력 토픽에 중복으로 쌓이지 않도록 소비자가 멱등성을 보장하거나, 출력 토픽을 별도로 초기화해야 한다. 리셋 대신 새 `application.id`로 별도 인스턴스를 띄워 shadow run하고, 검증 후 트래픽을 전환하는 방법이 더 안전하다.

---

## Q4. Processor API vs DSL — 언제 저수준 API가 불가피한가

### 왜 이 질문이 중요한가

DSL로 충분한 경우에 Processor API를 쓰는 것은 과도한 복잡도를 초래한다. 반대로 DSL이 표현하지 못하는 패턴을 억지로 맞추다 보면 코드가 뒤틀린다. 언제 경계를 넘어야 하는지 기준을 갖고 있어야 실무에서 올바른 결정을 내릴 수 있다. 면접에서는 "DSL로 해결 못한 문제를 겪어봤냐"는 형태로 실전 경험을 확인한다.

### 답변

DSL(`map`, `filter`, `join`, `aggregate`)이 해결하지 못하는 대표적인 세 가지 상황이 있다.

**1. 다중 출력 토픽에 서로 다른 시점으로 전달해야 할 때.** DSL의 `split().branch()`는 같은 레코드를 분기하지만, 다른 State Store 값을 조합해 조건별로 다른 출력 토픽에 다른 타이밍으로 보내는 건 불가능하다.

```java
// Processor API: 하나의 입력에서 두 출력 토픽에 각각 조건부 전달
class OrderRouter implements Processor<String, Order, String, Object> {
    private ProcessorContext<String, Object> context;

    @Override
    public void process(Record<String, Order> record) {
        if (record.value().isHighValue()) {
            context.forward(record.withValue(record.value()), "high-value-orders");
        }
        context.forward(record.withValue(buildAudit(record.value())), "audit-log");
    }
}
```

**2. punctuate() — 시간 기반 주기 작업.** DSL에는 레코드 도착 없이 주기적으로 실행하는 트리거가 없다. 예를 들어 10분마다 State Store를 스캔해 타임아웃된 세션을 강제 종료해야 한다면 `Punctuator`가 필요하다.

**3. 세밀한 State Store 제어.** DSL의 `aggregate()`는 하나의 State Store만 연결된다. Processor API에서는 여러 Store를 동시에 읽고 쓸 수 있어 복잡한 상태 머신 구현이 가능하다.

DSL과 Processor API는 혼합 사용이 가능하다. `KStream.process()`로 DSL 토폴로지 중간에 Processor를 삽입하면, 대부분은 DSL로 유지하면서 필요한 부분만 저수준으로 내려갈 수 있다.

---

## Q5. State Store 복구 시간 — changelog 기반 복구의 실체와 standby replica 단축 효과

### 왜 이 질문이 중요한가

Kafka Streams 인스턴스가 재시작되면 State Store 복구가 완료되기 전까지 해당 파티션의 처리가 중단된다. 대용량 State Store를 운영하는 환경에서 복구 시간이 길면 장애 복구 SLA를 맞추지 못한다. 면접에서는 "Kafka Streams의 고가용성을 어떻게 보장하겠냐"라는 질문의 핵심 답변이 standby replica다.

### 답변

State Store는 로컬 RocksDB에 저장되고, 모든 변경은 changelog 토픽(내부 토픽 `<app-id>-<store-name>-changelog`)에도 기록된다. 인스턴스가 재시작되면 Kafka Streams는 changelog 토픽을 처음부터 재생하여 RocksDB를 복원한다. 복구 시간은 `changelog 레코드 수 × 역직렬화 비용`에 비례한다.

**복구 시간 예시:**
- changelog 토픽에 1천만 레코드, 초당 10만 레코드 복원 → 약 100초 복구 지연
- 복구 중 해당 파티션은 `REBALANCING` 상태로 처리 불가

**standby replica로 단축:** `num.standby.replicas=1`을 설정하면 다른 인스턴스가 changelog를 동일하게 따라가며 복제본 State Store를 유지한다. 장애 발생 시 리밸런싱 후 해당 인스턴스가 해당 파티션을 인수하면, 복구 없이 거의 즉시 처리를 재개한다.

```properties
# 설정: 각 State Store 파티션에 대해 1개 복제본 유지
num.standby.replicas=1
```

```
정상 상태:
  인스턴스 A: 파티션 0~3 담당 (State Store 원본)
  인스턴스 B: 파티션 4~7 담당 (State Store 원본)
               + 파티션 0~3 standby 유지

인스턴스 A 장애 시:
  인스턴스 B: 파티션 0~7 모두 담당
               → 파티션 0~3은 standby에서 즉시 인수 (복구 지연 없음)
```

**tradeoff:** standby replica는 changelog를 지속적으로 소비하므로 인스턴스당 메모리와 디스크가 추가로 필요하다. standby가 없어도 복구 속도를 높이려면 changelog 토픽의 retention을 짧게 유지하거나, State Store 스냅샷(`commit.interval.ms`을 낮춰 로컬 체크포인트 빈도 증가)을 활용한다.
