package com.study.redpanda.cqrs.query.topology;

import com.study.redpanda.avro.social.PostCreated;
import com.study.redpanda.avro.social.PostLiked;
import com.study.redpanda.cqrs.config.CqrsSerdeFactory;
import com.study.redpanda.cqrs.config.CqrsTopics;
import com.study.redpanda.cqrs.query.model.PostView;
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

import java.util.ArrayList;

/**
 * CQRS Query Side: 게시물 이벤트 스트림 토폴로지
 *
 * post-created와 post-liked 두 토픽을 각각 소비한 뒤 merge()로 합쳐서
 * "posts-store" State Store(KV: postId → PostView)를 구성한다.
 *
 * 토픽이 분리되어 있으므로 PostCreated/PostLiked 간 순서는 보장되지 않는다.
 * PostLiked가 먼저 도착하면 currentView가 null이므로 무시하고 넘어간다.
 */
@Component
public class PostsStreamTopology {

    // 토픽명은 CqrsTopics에서 중앙 관리
    private static final String STORE_NAME = "posts-store";

    private final StreamsBuilder streamsBuilder;
    private final String schemaRegistryUrl;

    public PostsStreamTopology(
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
        KStream<String, SpecificRecord> created = streamsBuilder.stream(CqrsTopics.POST_CREATED, consumed);
        KStream<String, SpecificRecord> liked = streamsBuilder.stream(CqrsTopics.POST_LIKED, consumed);

        // merge 후 단일 스트림으로 집계
        created.merge(liked)
                .groupByKey()
                .aggregate(
                        () -> null, // 초기값: 첫 이벤트 도착 전까지 null
                        this::applyPostEvent,
                        Materialized.<String, PostView, KeyValueStore<Bytes, byte[]>>as(STORE_NAME)
                                .withKeySerde(Serdes.String())
                                .withValueSerde(new JsonSerde<>(PostView.class))
                );
    }

    /**
     * 게시물 이벤트를 PostView에 적용하는 집계 함수.
     *
     * 토픽은 1:1로 분리되어 있지만, merge() 후 타입이 SpecificRecord로 소실되므로
     * instanceof로 분기해야 한다. instanceof 없이 하려면 merge 대신 process()로
     * 각 스트림이 같은 State Store에 독립 접근하는 방식이 있으나 코드가 복잡해진다.
     *
     * - PostCreated: 새 PostView를 빌더로 생성하여 반환 (기존 뷰가 있으면 덮어씀)
     * - PostLiked: likeCount 증가 + likedBy 목록에 userId 추가 (currentView null이면 무시)
     *
     * 주의: PostCreated 재수신 시 기존 like 정보가 초기화된다.
     */
    private PostView applyPostEvent(String postId, SpecificRecord event, PostView currentView) {
        if (event instanceof PostCreated created) {
            return newPostView(created);
        }

        if (event instanceof PostLiked liked) {
            // PostCreated보다 먼저 도착한 경우 — 무시하고 null 유지
            if (currentView == null) return null;
            currentView.setLikeCount(currentView.getLikeCount() + 1);
            currentView.getLikedBy().add(liked.getUserId());
            return currentView;
        }

        // 알 수 없는 이벤트 타입 — 기존 상태 유지
        return currentView;
    }

    private PostView newPostView(PostCreated created) {
        return PostView.builder()
                .postId(created.getPostId())
                .userId(created.getUserId())
                .content(created.getContent())
                .likeCount(0)
                .likedBy(new ArrayList<>())
                .createdAt(created.getTimestamp())
                .build();
    }
}
