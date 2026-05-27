package com.study.redpanda.cqrs.query.service;

import com.study.redpanda.cqrs.config.CqrsTopics;
import io.confluent.kafka.serializers.KafkaAvroDeserializer;
import io.confluent.kafka.serializers.KafkaAvroDeserializerConfig;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.KeyValueIterator;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.UUID;

/**
 * CQRS Event Replay 서비스
 *
 * Event Store(Kafka 토픽)가 불변 로그(immutable log)이므로,
 * 언제든지 처음부터 다시 재생하여 State Store를 재구축할 수 있다.
 *
 * 두 가지 리플레이 방식을 비교한다:
 *
 * Approach A (Streams Reset): Kafka Streams의 이디오매틱한 방식.
 *   stop → cleanUp → deleteConsumerGroup → start로 State Store를 완전 재구축한다.
 *   파괴적(destructive) — 재구축 중 조회 불가(503).
 *
 * Approach B (Manual Consumer): 교육용 데모.
 *   임시 Consumer Group으로 전체 이벤트를 폴링하여 토픽별 이벤트 수를 집계한다.
 *   비파괴적(non-destructive) — 기존 Streams 앱에 영향 없음.
 *   Event Store가 불변 로그임을 직접 확인하는 목적이다.
 */
@Service
@Slf4j
public class EventReplayService {

    private static final String APPLICATION_ID = "cqrs-social-streams";

    private final StreamsBuilderFactoryBean factoryBean;
    private final KafkaAdmin kafkaAdmin;
    private final String bootstrapServers;
    private final String schemaRegistryUrl;

    public EventReplayService(
            StreamsBuilderFactoryBean factoryBean,
            KafkaAdmin kafkaAdmin,
            @Value("${spring.kafka.bootstrap-servers}") String bootstrapServers,
            @Value("${spring.kafka.producer.properties.schema.registry.url}") String schemaRegistryUrl) {
        this.factoryBean = factoryBean;
        this.kafkaAdmin = kafkaAdmin;
        this.bootstrapServers = bootstrapServers;
        this.schemaRegistryUrl = schemaRegistryUrl;
    }

    /**
     * Approach A: Kafka Streams 리셋으로 State Store 재구축
     *
     * 1. factoryBean.stop() — Streams 인스턴스 중지
     * 2. kafkaStreams.cleanUp() — 로컬 RocksDB State Store 삭제
     * 3. AdminClient.deleteConsumerGroups() — Consumer Group 오프셋 삭제
     * 4. factoryBean.start() — earliest부터 전체 이벤트 리플레이
     *
     * 이 방식이 Kafka Streams의 정석적인 State Store 재구축 방법이다.
     * cleanUp()만으로는 Consumer Group 오프셋이 남아 있어 마지막 위치부터 읽게 된다.
     * deleteConsumerGroups()로 오프셋까지 삭제해야 earliest부터 다시 읽는다.
     *
     * 재구축 중에는 Streams가 REBALANCING 상태이므로 Query API가 503을 반환한다.
     */
    public Map<String, Object> replayViaStreamsReset() {
        long startTime = System.currentTimeMillis();

        try {
            // 1. Streams 중지
            KafkaStreams kafkaStreams = factoryBean.getKafkaStreams();
            factoryBean.stop();
            log.info("Kafka Streams stopped for replay");

            // 2. 로컬 State Store(RocksDB) 삭제
            if (kafkaStreams != null) {
                kafkaStreams.cleanUp();
                log.info("Local State Store (RocksDB) cleaned up");
            }

            // 3. Consumer Group 삭제 (오프셋 리셋)
            try (var adminClient = org.apache.kafka.clients.admin.AdminClient.create(
                    kafkaAdmin.getConfigurationProperties())) {
                adminClient.deleteConsumerGroups(Set.of(APPLICATION_ID)).all().get();
                log.info("Consumer group '{}' deleted", APPLICATION_ID);
            }

            // 4. Streams 재시작 (earliest부터 전체 리플레이)
            factoryBean.start();
            log.info("Kafka Streams restarted — replaying from earliest");

            long elapsed = System.currentTimeMillis() - startTime;
            return Map.of(
                    "method", "streams-reset",
                    "status", "replay_started",
                    "applicationId", APPLICATION_ID,
                    "elapsedMs", elapsed,
                    "note", "State Store is rebuilding. Query API returns 503 until RUNNING state."
            );
        } catch (Exception e) {
            log.error("Streams reset replay failed", e);
            return Map.of(
                    "method", "streams-reset",
                    "status", "failed",
                    "error", e.getMessage()
            );
        }
    }

    /**
     * Approach B: 임시 Consumer로 이벤트 집계 (비파괴적)
     *
     * UUID 기반 새 Consumer Group을 생성하여 모든 CQRS 토픽을 earliest부터 폴링한다.
     * 토픽별 이벤트 개수를 집계하여 반환한다. State Store를 재구축하지 않는다.
     *
     * 이 방식의 목적:
     * - Event Store가 불변 로그임을 직접 확인 (모든 과거 이벤트가 여전히 존재)
     * - 기존 Streams 앱에 영향을 주지 않고 이벤트를 검사
     * - Consumer Group 독립성: 새 Group ID는 기존 오프셋과 무관
     */
    public Map<String, Object> replayViaManualConsumer() {
        String tempGroupId = "cqrs-replay-" + UUID.randomUUID();
        List<String> topics = List.of(
                CqrsTopics.POST_CREATED,
                CqrsTopics.POST_LIKED,
                CqrsTopics.USER_FOLLOWED,
                CqrsTopics.USER_UNFOLLOWED
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

            // 빈 poll 3회 연속이면 모든 이벤트를 소비한 것으로 판단
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
        try (var adminClient = org.apache.kafka.clients.admin.AdminClient.create(
                kafkaAdmin.getConfigurationProperties())) {
            adminClient.deleteConsumerGroups(Set.of(tempGroupId)).all().get();
        } catch (Exception e) {
            log.warn("Failed to delete temp consumer group: {}", tempGroupId, e);
        }

        return Map.of(
                "method", "manual-consumer",
                "tempGroupId", tempGroupId,
                "totalEvents", totalEvents,
                "topicCounts", topicCounts,
                "note", "Non-destructive. Existing Streams app unaffected."
        );
    }

    /**
     * 4개 State Store의 엔트리 수 조회
     *
     * 리플레이 전후 비교 용도. Kafka Streams가 RUNNING 상태여야 한다.
     * 각 스토어를 순회하며 엔트리 수를 카운트한다.
     */
    public Map<String, Object> getStoresStatus() {
        KafkaStreams kafkaStreams = factoryBean.getKafkaStreams();
        if (kafkaStreams == null || kafkaStreams.state() != KafkaStreams.State.RUNNING) {
            return Map.of(
                    "streamsState", kafkaStreams != null ? kafkaStreams.state().toString() : "null",
                    "note", "Kafka Streams not RUNNING. Cannot query State Stores."
            );
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
                    while (iter.hasNext()) {
                        iter.next();
                        count++;
                    }
                }
                storeCounts.put(storeName, count);
            } catch (Exception e) {
                storeCounts.put(storeName, -1L);
                log.warn("Failed to query store '{}': {}", storeName, e.getMessage());
            }
        }

        return Map.of(
                "streamsState", kafkaStreams.state().toString(),
                "stores", storeCounts
        );
    }
}
