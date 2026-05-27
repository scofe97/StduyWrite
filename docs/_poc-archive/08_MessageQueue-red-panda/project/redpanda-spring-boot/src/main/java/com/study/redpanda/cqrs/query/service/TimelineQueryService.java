package com.study.redpanda.cqrs.query.service;

import com.study.redpanda.cqrs.query.model.TimelineView;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.stereotype.Service;

import java.util.NoSuchElementException;

/**
 * CQRS Query Side: 타임라인 조회 서비스
 *
 * Kafka Streams의 timeline-store State Store를 Interactive Query로 직접 조회한다.
 * key = userId (타임라인 소유자), value = TimelineView (팔로잉한 사용자들의 게시물 피드)
 *
 * PostQueryService, FollowsQueryService와 동일한 패턴:
 * State Store 접근 전 KafkaStreams RUNNING 상태 확인 필수.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class TimelineQueryService {

    // TimelineStreamTopology.TIMELINE_STORE와 동일
    private static final String STORE_NAME = "timeline-store";

    private final StreamsBuilderFactoryBean factoryBean;

    /**
     * 사용자 타임라인 조회: userId의 타임라인(팔로잉 사용자들의 게시물 피드)을 반환한다.
     *
     * 엔트리는 newest first로 정렬되어 있다 (TimelineFanOutProcessor가 리스트 앞에 추가).
     */
    public TimelineView getTimeline(String userId) {
        ReadOnlyKeyValueStore<String, TimelineView> store = getStore();
        TimelineView timeline = store.get(userId);
        if (timeline == null) {
            throw new NoSuchElementException("Timeline not found: " + userId);
        }
        return timeline;
    }

    private ReadOnlyKeyValueStore<String, TimelineView> getStore() {
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
