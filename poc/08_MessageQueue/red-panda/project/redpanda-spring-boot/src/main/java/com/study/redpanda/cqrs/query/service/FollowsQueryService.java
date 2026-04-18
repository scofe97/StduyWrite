package com.study.redpanda.cqrs.query.service;

import com.study.redpanda.cqrs.query.model.FollowsView;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.stereotype.Service;

import java.util.NoSuchElementException;
import java.util.Set;

/**
 * CQRS Query Side: 팔로우 관계 조회 서비스
 *
 * Kafka Streams의 follows-store State Store를 Interactive Query로 직접 조회한다.
 * key = followerId, value = FollowsView(followees Set) 구조이다.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class FollowsQueryService {

    // FollowsStreamTopology.STORE_NAME과 동일
    private static final String STORE_NAME = "follows-store";

    private final StreamsBuilderFactoryBean factoryBean;

    /**
     * 팔로잉 목록 조회: followerId가 팔로우하고 있는 사용자 목록을 반환한다.
     */
    public FollowsView getFollows(String followerId) {
        ReadOnlyKeyValueStore<String, FollowsView> store = getStore();
        FollowsView view = store.get(followerId);
        if (view == null) {
            throw new NoSuchElementException("Follows not found: " + followerId);
        }
        return view;
    }

    /**
     * 팔로잉 여부 확인: followerId가 followeeId를 팔로우하고 있는지 확인한다.
     */
    public boolean isFollowing(String followerId, String followeeId) {
        ReadOnlyKeyValueStore<String, FollowsView> store = getStore();
        FollowsView view = store.get(followerId);
        if (view == null) return false;
        Set<String> followees = view.getFollowees();
        return followees != null && followees.contains(followeeId);
    }

    private ReadOnlyKeyValueStore<String, FollowsView> getStore() {
        KafkaStreams kafkaStreams = factoryBean.getKafkaStreams();
        if (kafkaStreams == null || kafkaStreams.state() != KafkaStreams.State.RUNNING) {
            throw new IllegalStateException(
                    "Kafka Streams not ready. State: " +
                            (kafkaStreams != null ? kafkaStreams.state() : "null"));
        }
        return kafkaStreams.store(
                StoreQueryParameters.fromNameAndType(STORE_NAME, QueryableStoreTypes.keyValueStore())
        );
    }
}
