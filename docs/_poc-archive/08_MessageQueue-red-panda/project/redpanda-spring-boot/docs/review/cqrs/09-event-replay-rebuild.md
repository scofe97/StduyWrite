# Event Replay & Rebuild

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 실습 번호 | 9 |
| 주요 파일 | `cqrs/query/service/EventReplayService.java`, `cqrs/controller/CqrsAdminController.java` |
| HTTP 파일 | `http/cqrs/06-event-replay.http` |
| 관련 원칙 | Immutable Log, Consumer Group 독립성, State Store 재구축, Eventual Consistency |

---

## 무엇을 구현했는가

### 두 가지 리플레이 방식

Event Replay를 두 가지 접근으로 구현하여 비교했다. 각각의 목적과 특성이 다르다.

| 항목 | Approach A: Streams Reset | Approach B: Manual Consumer |
|------|--------------------------|---------------------------|
| 목적 | State Store 재구축 (프로덕션) | Event Store 검증 (교육용) |
| 파괴성 | 파괴적 — 재구축 중 503 | 비파괴적 — 기존 앱 영향 없음 |
| 원리 | stop → cleanUp → deleteGroup → start | 임시 Consumer Group으로 폴링 |
| 결과 | State Store 완전 재구축 | 토픽별 이벤트 수 집계 |

### Approach A: Kafka Streams Reset

Kafka Streams의 이디오매틱한 State Store 재구축 방법이다. 네 단계를 순서대로 수행한다.

```java
public Map<String, Object> replayViaStreamsReset() {
    try {
        // 1. Streams 중지
        KafkaStreams kafkaStreams = factoryBean.getKafkaStreams();
        factoryBean.stop();

        // 2. 로컬 State Store(RocksDB) 삭제
        if (kafkaStreams != null) {
            kafkaStreams.cleanUp();
        }

        // 3. Consumer Group 삭제 (오프셋 리셋)
        try (var adminClient = AdminClient.create(
                kafkaAdmin.getConfigurationProperties())) {
            adminClient.deleteConsumerGroups(Set.of(APPLICATION_ID)).all().get();
        }

        // 4. Streams 재시작 (earliest부터 전체 리플레이)
        factoryBean.start();

        return Map.of(
                "method", "streams-reset",
                "status", "replay_started",
                "note", "State Store is rebuilding. Query API returns 503 until RUNNING state."
        );
    } catch (Exception e) {
        return Map.of("method", "streams-reset", "status", "failed", "error", e.getMessage());
    }
}
```

각 단계가 필요한 이유는 다음과 같다.

**1단계 stop()**: Streams 인스턴스를 중지해야 2단계의 cleanUp()을 호출할 수 있다. 실행 중인 Streams에 cleanUp()을 호출하면 예외가 발생한다.

**2단계 cleanUp()**: 로컬 RocksDB 디렉토리를 삭제한다. 이것만으로는 부족하다. Consumer Group의 오프셋이 남아 있으면 재시작 시 마지막으로 처리한 위치부터 읽기 때문이다.

**3단계 deleteConsumerGroups()**: Consumer Group 오프셋을 삭제하는 핵심 단계다. Kafka Streams는 `application.id`를 Consumer Group ID로 사용한다. 이 Group을 삭제하면 저장된 오프셋 정보가 사라지고, 재시작 시 `auto.offset.reset=earliest` 설정에 따라 토픽의 처음부터 읽게 된다.

**4단계 start()**: Streams를 재시작하면 처음부터 모든 이벤트를 다시 소비하여 State Store를 완전히 재구축한다. 재구축 중에는 REBALANCING 상태이므로 Query API가 503을 반환한다.

### Approach B: Manual Consumer

기존 Streams 앱에 영향을 주지 않고 Event Store의 내용을 검증하는 교육용 구현이다.

```java
public Map<String, Object> replayViaManualConsumer() {
    String tempGroupId = "cqrs-replay-" + UUID.randomUUID();
    List<String> topics = List.of(
            CqrsTopics.POST_CREATED, CqrsTopics.POST_LIKED,
            CqrsTopics.USER_FOLLOWED, CqrsTopics.USER_UNFOLLOWED
    );

    Properties props = new Properties();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
    props.put(ConsumerConfig.GROUP_ID_CONFIG, tempGroupId);
    props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);
    props.put(KafkaAvroDeserializerConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl);
    props.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);

    Map<String, Integer> topicCounts = new HashMap<>();
    topics.forEach(t -> topicCounts.put(t, 0));
    int totalEvents = 0;

    try (KafkaConsumer<String, Object> consumer = new KafkaConsumer<>(props)) {
        consumer.subscribe(topics);

        int emptyPolls = 0;
        while (emptyPolls < 3) {
            ConsumerRecords<String, Object> records = consumer.poll(Duration.ofSeconds(2));
            if (records.isEmpty()) {
                emptyPolls++;
                continue;
            }
            emptyPolls = 0;
            for (ConsumerRecord<String, Object> record : records) {
                topicCounts.merge(record.topic(), 1, Integer::sum);
                totalEvents++;
            }
        }
    }

    // 임시 Consumer Group 삭제 (정리)
    try (var adminClient = AdminClient.create(
            kafkaAdmin.getConfigurationProperties())) {
        adminClient.deleteConsumerGroups(Set.of(tempGroupId)).all().get();
    } catch (Exception e) {
        log.warn("Failed to delete temp consumer group: {}", tempGroupId, e);
    }

    return Map.of(
            "method", "manual-consumer",
            "totalEvents", totalEvents,
            "topicCounts", topicCounts,
            "note", "Non-destructive. Existing Streams app unaffected."
    );
}
```

세 가지 설정이 이 접근을 가능하게 한다. UUID 기반 Group ID는 기존 Consumer Group과 완전히 독립적이다. `earliest`는 토픽의 처음부터 읽도록 한다. 사용 후 임시 Group을 삭제하여 Kafka에 찌꺼기를 남기지 않는다.

빈 poll이 3회 연속이면 모든 이벤트를 소비한 것으로 판단한다. 1회만으로 종료하면 네트워크 지연이나 파티션 리밸런싱 중에 조기 종료될 수 있다.

### State Store 상태 조회

리플레이 전후 비교를 위해 4개 State Store의 엔트리 수를 조회하는 API도 제공한다.

```java
public Map<String, Object> getStoresStatus() {
    KafkaStreams kafkaStreams = factoryBean.getKafkaStreams();
    if (kafkaStreams == null || kafkaStreams.state() != KafkaStreams.State.RUNNING) {
        return Map.of("streamsState", "not running", "note", "Cannot query State Stores.");
    }

    String[] storeNames = {"posts-store", "follows-store", "timeline-store", "timeline-followers-cache"};
    Map<String, Long> storeCounts = new HashMap<>();

    for (String storeName : storeNames) {
        try {
            ReadOnlyKeyValueStore<String, Object> store = kafkaStreams.store(
                    StoreQueryParameters.fromNameAndType(storeName, QueryableStoreTypes.keyValueStore())
            );
            long count = 0;
            try (KeyValueIterator<String, Object> iter = store.all()) {
                while (iter.hasNext()) { iter.next(); count++; }
            }
            storeCounts.put(storeName, count);
        } catch (Exception e) {
            storeCounts.put(storeName, -1L);
        }
    }

    return Map.of("streamsState", kafkaStreams.state().toString(), "stores", storeCounts);
}
```

### Admin Controller

두 리플레이 방식과 상태 조회를 REST API로 노출한다.

```
POST /api/cqrs/admin/replay/streams-reset     → Approach A (파괴적 재구축)
POST /api/cqrs/admin/replay/manual-count       → Approach B (비파괴적 집계)
GET  /api/cqrs/admin/stores/status             → State Store 엔트리 수 조회
```

---

## 왜 이렇게 구현했는가

### 두 방식을 모두 구현한 이유

Approach A(Streams Reset)만으로도 실무에서는 충분하다. Approach B(Manual Consumer)를 추가로 구현한 이유는 교육적 가치 때문이다.

Approach B는 Kafka Consumer의 동작 원리를 직접 체험하게 한다. Consumer Group이 독립적이라는 것, `earliest`가 처음부터 읽기를 의미한다는 것, `poll()`이 이벤트를 배치로 가져온다는 것을 코드로 확인할 수 있다. Event Store가 "불변 로그"라는 개념도 직접 모든 이벤트를 읽어보면서 체감할 수 있다. 이벤트를 발행한 지 한참 후에도 Consumer로 전체 이벤트를 읽을 수 있다는 사실이 Event Sourcing의 핵심 가치를 증명한다.

### cleanUp()만으로는 불충분한 이유

`kafkaStreams.cleanUp()`은 로컬 RocksDB 디렉토리만 삭제한다. 그러나 Consumer Group 오프셋은 Kafka 브로커(또는 `__consumer_offsets` 토픽)에 저장되어 있다. cleanUp() 후 재시작하면 Kafka Streams는 기존 오프셋을 찾아서 "마지막으로 처리한 다음 이벤트"부터 읽기 시작한다. 로컬 State Store는 비어 있지만 처음부터 읽지 않으므로 State Store가 불완전하게 구축된다.

`deleteConsumerGroups()`로 오프셋을 삭제해야 비로소 "저장된 오프셋 없음 → earliest부터 읽기" 흐름이 동작한다. 이 순서를 이해하는 것이 Event Replay의 핵심이다.

```
cleanUp()만 실행:
  로컬 RocksDB 삭제 → 오프셋 남아있음 → 마지막 위치부터 읽기 → 불완전한 State Store

cleanUp() + deleteConsumerGroups():
  로컬 RocksDB 삭제 → 오프셋 삭제 → earliest부터 읽기 → 완전한 State Store 재구축
```

### 빈 poll 3회 연속 종료 기준의 이유

Manual Consumer에서 `records.isEmpty()`가 1회라도 나오면 즉시 종료하는 것은 위험하다. 파티션 리밸런싱 중이거나 네트워크 일시 지연으로 빈 응답이 올 수 있기 때문이다. 3회 연속 빈 poll이면 "더 이상 읽을 이벤트가 없다"고 합리적으로 판단할 수 있다. `poll(Duration.ofSeconds(2))`이므로 최대 6초(2초 × 3회)를 대기한 후 종료한다.

### 임시 Consumer Group을 삭제하는 이유

UUID 기반 Group은 한 번 쓰고 버리는 용도이지만, Kafka 브로커에 Group 메타데이터가 남아있으면 `rpk group list` 등에 불필요한 항목이 누적된다. `deleteConsumerGroups()`로 정리하면 브로커를 깔끔하게 유지할 수 있다. 삭제 실패 시에도 warn 로그만 남기고 결과는 정상 반환한다. 정리 실패가 비즈니스 로직 실패를 의미하지 않기 때문이다.

---

## 교차 검증 결과

### HTTP 테스트 시나리오 (06-event-replay.http)

4단계로 구성된 테스트 흐름이다.

**1단계 — 현재 상태 확인**: `GET /stores/status`로 4개 State Store의 엔트리 수를 기록한다.

**2단계 — Manual Consumer**: `POST /replay/manual-count`로 전체 이벤트를 집계한다. 이후 Store 상태를 다시 조회하여 1단계와 동일한지 확인한다. 비파괴적이므로 변화가 없어야 한다.

**3단계 — Streams Reset**: `POST /replay/streams-reset`을 실행한다. 즉시 `GET /posts`를 호출하면 503이 반환되어야 한다 (REBALANCING 상태).

**4단계 — 재구축 완료 확인**: 수초 대기 후 Store 상태를 조회한다. 1단계와 동일한 엔트리 수가 복원되어야 한다. 이것이 Event Sourcing의 핵심 증명이다 — 이벤트만 있으면 상태를 완전히 재구축할 수 있다.

### Approach A와 B의 실행 결과 비교

| 측정 항목 | Approach A 결과 | Approach B 결과 |
|----------|----------------|----------------|
| Store 영향 | 재구축됨 (동일 상태) | 영향 없음 |
| 서비스 가용성 | 일시 중단 (503) | 중단 없음 |
| 반환 데이터 | 재시작 상태 메시지 | 토픽별 이벤트 수 |
| 소요 시간 | 수초 (이벤트 양에 비례) | 수초 (폴링 + 대기) |

### Kafka Streams Reset vs Manual Consumer 선택 기준

프로덕션에서 State Store 재구축이 필요한 경우(버그 수정 후 재처리, 토폴로지 변경 등)에는 Approach A를 사용한다. Kafka Streams가 토폴로지에 맞게 자동으로 State Store를 재구축하기 때문이다.

단순히 이벤트 검사나 감사(audit)가 목적이라면 Approach B가 적합하다. 기존 서비스에 영향을 주지 않고 독립적으로 이벤트를 읽을 수 있다.

---

## 핵심 학습 포인트

- **Consumer Group 독립성이 Event Replay를 가능하게 한다.** 새로운 Consumer Group은 기존 Group의 오프셋과 완전히 독립적이다. 같은 토픽을 여러 Group이 동시에 읽을 수 있으며, 서로의 처리 상태에 영향을 주지 않는다. 이 특성이 "기존 서비스를 중단하지 않고 이벤트를 재처리"하는 것을 가능하게 한다.

- **State Store 재구축은 cleanUp() + deleteConsumerGroups() 두 단계가 필요하다.** cleanUp()은 로컬 RocksDB를 삭제하고, deleteConsumerGroups()는 브로커의 오프셋을 삭제한다. 둘 다 해야 earliest부터 다시 읽는다. 하나만 실행하면 불완전한 상태가 된다.

- **Event Store는 불변 로그이므로 상태는 언제든 재파생 가능하다.** 이벤트를 발행한 후 시간이 지나도 토픽에 남아있다(`retention.ms=-1`). Manual Consumer로 전체 이벤트를 읽어보면 "이벤트가 사라지지 않았음"을 직접 확인할 수 있다. 이것이 Event Sourcing에서 이벤트가 source of truth인 이유다.

- **파괴적 리플레이와 비파괴적 리플레이의 트레이드오프를 이해해야 한다.** Streams Reset은 State Store를 완전히 재구축하지만 서비스가 일시 중단된다. Manual Consumer는 서비스에 영향이 없지만 State Store를 갱신하지 않는다. 목적에 따라 선택한다.

- **Kafka Streams의 application.id는 Consumer Group ID와 동일하다.** 이 사실을 알면 Streams Reset의 3단계(`deleteConsumerGroups(APPLICATION_ID)`)가 왜 필요한지 바로 이해된다. application.id를 변경하면 새 Consumer Group이 생성되어 자동으로 earliest부터 읽게 되는데, 이는 learning 문서(05-event-replay-time-travel.md §3)에서 설명한 "새 Topology + 새 Application ID" 리플레이 방식과 같은 원리다.
