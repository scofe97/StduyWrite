package com.study.redpanda.cqrs.query.topology;

import com.study.redpanda.avro.social.PostCreated;
import com.study.redpanda.avro.social.UserFollowed;
import com.study.redpanda.avro.social.UserUnfollowed;
import com.study.redpanda.cqrs.config.CqrsSerdeFactory;
import com.study.redpanda.cqrs.config.CqrsTopics;
import com.study.redpanda.cqrs.query.model.TimelineView;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.apache.avro.specific.SpecificRecord;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.processor.api.Processor;
import org.apache.kafka.streams.processor.api.ProcessorContext;
import org.apache.kafka.streams.processor.api.Record;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.state.StoreBuilder;
import org.apache.kafka.streams.state.Stores;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.support.serializer.JsonSerde;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

/**
 * CQRS Query Side: 타임라인 Materialized View 토폴로지
 *
 * 기존 토폴로지(PostsStreamTopology, FollowsStreamTopology)는 DSL(merge+aggregate)을 사용하지만,
 * 타임라인은 Processor API가 필요하다:
 * - 크로스 스토어 조회: PostCreated 도착 시 팔로워 목록을 조회해야 함
 * - 팬아웃 쓰기: 하나의 이벤트가 N명의 팔로워 타임라인에 쓰기
 * - 역방향 인덱스: follows-store는 followerId→followees이지만, followeeId→followers 필요
 *
 * 데이터 흐름:
 *   follow/unfollow 이벤트 → FollowsCacheProcessor → timeline-followers-cache (역방향 인덱스)
 *   post-created 이벤트     → TimelineFanOutProcessor → timeline-store (팬아웃 쓰기)
 *
 * 팔로우 시 기존 게시물 백필 없음 (fan-out on write). 팔로우 이후 작성된 게시물만 타임라인에 포함.
 */
@Component
@Slf4j
public class TimelineStreamTopology {

    static final String TIMELINE_STORE = "timeline-store";
    static final String FOLLOWERS_CACHE_STORE = "timeline-followers-cache";
    private static final int MAX_TIMELINE_ENTRIES = 50;

    private final StreamsBuilder streamsBuilder;
    private final String schemaRegistryUrl;

    public TimelineStreamTopology(
            StreamsBuilder streamsBuilder,
            @Value("${spring.kafka.producer.properties.schema.registry.url}") String schemaRegistryUrl) {
        this.streamsBuilder = streamsBuilder;
        this.schemaRegistryUrl = schemaRegistryUrl;
    }

    /**
     * 토폴로지 구성: Processor API로 2개의 State Store를 크로스 참조한다.
     *
     * DSL의 aggregate()와 달리 Processor API는 여러 State Store에 직접 접근할 수 있다.
     * TimelineFanOutProcessor가 followers-cache에서 팔로워를 조회한 뒤
     * 각 팔로워의 timeline-store에 엔트리를 쓰는 팬아웃 패턴을 구현한다.
     */
    @PostConstruct
    public void buildTopology() {
        SpecificAvroSerde<SpecificRecord> avroSerde = CqrsSerdeFactory.createAvroValueSerde(schemaRegistryUrl);
        Consumed<String, SpecificRecord> consumed = Consumed.with(Serdes.String(), avroSerde);

        // State Store 빌더 등록
        StoreBuilder<KeyValueStore<String, TimelineView>> timelineStoreBuilder =
                Stores.keyValueStoreBuilder(
                        Stores.persistentKeyValueStore(TIMELINE_STORE),
                        Serdes.String(),
                        new JsonSerde<>(TimelineView.class)
                );

        StoreBuilder<KeyValueStore<String, HashSet<String>>> followersCacheBuilder =
                Stores.keyValueStoreBuilder(
                        Stores.persistentKeyValueStore(FOLLOWERS_CACHE_STORE),
                        Serdes.String(),
                        new JsonSerde<>(HashSet.class)
                );

        streamsBuilder.addStateStore(timelineStoreBuilder);
        streamsBuilder.addStateStore(followersCacheBuilder);

        // follow/unfollow 이벤트 → FollowsCacheProcessor (역방향 인덱스 구축)
        streamsBuilder.stream(CqrsTopics.USER_FOLLOWED, consumed)
                .merge(streamsBuilder.stream(CqrsTopics.USER_UNFOLLOWED, consumed))
                .process(FollowsCacheProcessor::new, FOLLOWERS_CACHE_STORE);

        // post-created 이벤트 → TimelineFanOutProcessor (팬아웃 쓰기)
        streamsBuilder.stream(CqrsTopics.POST_CREATED, consumed)
                .process(TimelineFanOutProcessor::new, TIMELINE_STORE, FOLLOWERS_CACHE_STORE);
    }

    // ─── Processor 구현 ─────────────────────────────────────

    /**
     * 팔로우/언팔로우 이벤트를 역방향 인덱스로 변환하는 Processor.
     *
     * 입력: key=followerId, value=UserFollowed/UserUnfollowed
     * 저장: key=followeeId, value=Set<followerId> (역방향)
     *
     * follows-store는 "내가 누구를 팔로우하는가"(followerId→followees)를 저장하지만,
     * 타임라인 팬아웃에는 "누가 나를 팔로우하는가"(followeeId→followers)가 필요하다.
     * 이 Processor가 그 역방향 인덱스를 timeline-followers-cache에 구축한다.
     */
    static class FollowsCacheProcessor implements Processor<String, SpecificRecord, Void, Void> {

        private KeyValueStore<String, HashSet<String>> followersCache;

        @Override
        public void init(ProcessorContext<Void, Void> context) {
            this.followersCache = context.getStateStore(FOLLOWERS_CACHE_STORE);
        }

        @Override
        public void process(Record<String, SpecificRecord> record) {
            SpecificRecord event = record.value();
            String followerId = record.key();

            if (event instanceof UserFollowed followed) {
                String followeeId = followed.getFolloweeId();
                HashSet<String> followers = followersCache.get(followeeId);
                if (followers == null) {
                    followers = new HashSet<>();
                }
                followers.add(followerId);
                followersCache.put(followeeId, followers);
                log.debug("Followers cache: {} now has {} followers", followeeId, followers.size());
            }

            if (event instanceof UserUnfollowed unfollowed) {
                String followeeId = unfollowed.getFolloweeId();
                HashSet<String> followers = followersCache.get(followeeId);
                if (followers != null) {
                    followers.remove(followerId);
                    followersCache.put(followeeId, followers);
                    log.debug("Followers cache: {} now has {} followers", followeeId, followers.size());
                }
            }
        }
    }

    /**
     * PostCreated 이벤트를 팔로워들의 타임라인에 팬아웃하는 Processor.
     *
     * 입력: key=postId, value=PostCreated
     * 동작:
     *   1. followers-cache에서 작성자(userId)의 팔로워 Set 조회
     *   2. 각 팔로워의 timeline-store에서 TimelineView 조회 (없으면 생성)
     *   3. TimelineEntry를 리스트 맨 앞에 추가 (newest first)
     *   4. MAX_TIMELINE_ENTRIES 초과 시 오래된 것부터 제거
     *
     * forward() 호출 없음: 다운스트림 토픽으로 전달하지 않고 State Store에만 쓴다.
     */
    static class TimelineFanOutProcessor implements Processor<String, SpecificRecord, Void, Void> {

        private KeyValueStore<String, TimelineView> timelineStore;
        private KeyValueStore<String, HashSet<String>> followersCache;

        @Override
        public void init(ProcessorContext<Void, Void> context) {
            this.timelineStore = context.getStateStore(TIMELINE_STORE);
            this.followersCache = context.getStateStore(FOLLOWERS_CACHE_STORE);
        }

        @Override
        public void process(Record<String, SpecificRecord> record) {
            if (!(record.value() instanceof PostCreated created)) return;

            String authorId = created.getUserId();
            String postId = created.getPostId();

            // 작성자의 팔로워 목록 조회
            HashSet<String> followers = followersCache.get(authorId);
            if (followers == null || followers.isEmpty()) {
                log.debug("No followers for author {}, skipping fan-out", authorId);
                return;
            }

            // 타임라인 엔트리 생성
            TimelineView.TimelineEntry entry = TimelineView.TimelineEntry.builder()
                    .postId(postId)
                    .authorId(authorId)
                    .content(created.getContent())
                    .createdAt(created.getTimestamp())
                    .build();

            // 각 팔로워의 타임라인에 엔트리 추가
            for (String followerId : followers) {
                TimelineView timeline = timelineStore.get(followerId);
                if (timeline == null) {
                    timeline = TimelineView.builder()
                            .userId(followerId)
                            .entries(new ArrayList<>())
                            .build();
                }

                // newest first: 리스트 맨 앞에 추가
                timeline.getEntries().add(0, entry);

                // 최대 크기 제한
                if (timeline.getEntries().size() > MAX_TIMELINE_ENTRIES) {
                    timeline.setEntries(
                            new ArrayList<>(timeline.getEntries().subList(0, MAX_TIMELINE_ENTRIES))
                    );
                }

                timelineStore.put(followerId, timeline);
            }

            log.debug("Fan-out post {} to {} followers", postId, followers.size());
        }
    }
}
