package com.study.redpanda.cqrs.query.topology;

import com.study.redpanda.avro.social.UserFollowed;
import com.study.redpanda.avro.social.UserUnfollowed;
import com.study.redpanda.cqrs.config.CqrsSerdeFactory;
import com.study.redpanda.cqrs.config.CqrsTopics;
import com.study.redpanda.cqrs.query.model.FollowsView;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import org.apache.avro.specific.SpecificRecord;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Materialized;
import org.apache.kafka.streams.state.KeyValueStore;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.support.serializer.JsonSerde;
import org.springframework.stereotype.Component;

import java.util.HashSet;

/**
 * CQRS Query Side: 팔로우 이벤트 스트림 토폴로지
 *
 * user-followed와 user-unfollowed 두 토픽을 각각 소비한 뒤 merge()로 합쳐서
 * "follows-store" State Store(KV: followerId → FollowsView)를 구성한다.
 *
 * partition key = followerId이므로 같은 사용자의 이벤트는
 * 동일 파티션에 순서대로 쌓인다. groupByKey()로 followerId 기준 집계가 가능하다.
 *
 * UserUnfollowed가 UserFollowed보다 먼저 도착하는 경우(이론상 불가하나 방어):
 * currentView가 null이면 언팔로우를 무시하고 null을 반환한다.
 */
@Component
public class FollowsStreamTopology {

    // 토픽명은 CqrsTopics에서 중앙 관리
    private static final String STORE_NAME = "follows-store";

    private final StreamsBuilder streamsBuilder;
    private final String schemaRegistryUrl;

    public FollowsStreamTopology(
            StreamsBuilder streamsBuilder,
            @Value("${spring.kafka.producer.properties.schema.registry.url}") String schemaRegistryUrl) {
        this.streamsBuilder = streamsBuilder;
        this.schemaRegistryUrl = schemaRegistryUrl;
    }

    /**
     * 토폴로지 구성: 2개 토픽 소비 → merge → groupByKey → aggregate → state store
     */
    @PostConstruct
    public void buildTopology() {
        SpecificAvroSerde<SpecificRecord> avroSerde = CqrsSerdeFactory.createAvroValueSerde(schemaRegistryUrl);
        Consumed<String, SpecificRecord> consumed = Consumed.with(Serdes.String(), avroSerde);

        // 토픽별 스트림 생성
        KStream<String, SpecificRecord> followed = streamsBuilder.stream(CqrsTopics.USER_FOLLOWED, consumed);
        KStream<String, SpecificRecord> unfollowed = streamsBuilder.stream(CqrsTopics.USER_UNFOLLOWED, consumed);

        // merge 후 단일 스트림으로 집계
        followed.merge(unfollowed)
                .groupByKey()
                .aggregate(
                        () -> null, // 초기값: 첫 이벤트 도착 전까지 null
                        this::applyFollowEvent,
                        Materialized.<String, FollowsView, KeyValueStore<Bytes, byte[]>>as(STORE_NAME)
                                .withKeySerde(Serdes.String())
                                .withValueSerde(new JsonSerde<>(FollowsView.class))
                );
    }

    /**
     * 팔로우 이벤트를 FollowsView에 적용하는 집계 함수.
     *
     * 토픽은 1:1로 분리되어 있지만, merge() 후 타입이 SpecificRecord로 소실되므로
     * instanceof로 분기해야 한다. instanceof 없이 하려면 merge 대신 process()로
     * 각 스트림이 같은 State Store에 독립 접근하는 방식이 있으나 코드가 복잡해진다.
     *
     * - UserFollowed: followees Set에 추가 (HashSet이므로 중복 자동 무시)
     * - UserUnfollowed: followees Set에서 제거 (currentView가 null이면 무시)
     */
    private FollowsView applyFollowEvent(String followerId, SpecificRecord event, FollowsView currentView) {
        if (event instanceof UserFollowed followed) {
            if (currentView == null) {
                currentView = newFollowsView(followerId);
            }
            currentView.getFollowees().add(followed.getFolloweeId());
            return currentView;
        }

        if (event instanceof UserUnfollowed unfollowed) {
            // 언팔로우가 팔로우보다 먼저 도착한 경우 — 무시하고 null 유지
            if (currentView == null) return null;
            currentView.getFollowees().remove(unfollowed.getFolloweeId());
            return currentView;
        }

        // 알 수 없는 이벤트 타입 — 기존 상태 유지
        return currentView;
    }

    private FollowsView newFollowsView(String followerId) {
        return FollowsView.builder()
                .followerId(followerId)
                .followees(new HashSet<>())
                .build();
    }
}
