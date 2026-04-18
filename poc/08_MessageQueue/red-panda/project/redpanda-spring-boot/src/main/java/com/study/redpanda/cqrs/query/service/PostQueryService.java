package com.study.redpanda.cqrs.query.service;

import com.study.redpanda.cqrs.query.model.PostView;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.KeyValueIterator;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * CQRS Query Side: 게시물 조회 서비스
 *
 * Kafka Streams의 posts-store State Store를 Interactive Query로 직접 조회한다.
 * 별도 DB 없이 RocksDB 기반 State Store가 읽기 모델 역할을 한다.
 *
 * State Store 접근 전 반드시 KafkaStreams가 RUNNING 상태인지 확인해야 한다.
 * 기동 직후에는 Changelog 토픽에서 상태를 복구 중일 수 있기 때문이다.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class PostQueryService {

    // PostsStreamTopology.STORE_NAME과 동일 (private이므로 직접 참조 불가)
    private static final String STORE_NAME = "posts-store";

    private final StreamsBuilderFactoryBean factoryBean;

    /**
     * 단건 조회: postId로 PostView를 조회한다.
     *
     * State Store에서 key(postId)로 직접 조회하므로 O(1) 성능이다.
     * DB 쿼리 없이 로컬 RocksDB를 읽으므로 네트워크 I/O가 없다.
     */
    public PostView getPost(String postId) {
        ReadOnlyKeyValueStore<String, PostView> store = getStore();
        PostView post = store.get(postId);
        if (post == null) {
            throw new NoSuchElementException("Post not found: " + postId);
        }
        return post;
    }

    /**
     * 전체 조회: posts-store의 모든 PostView를 반환한다.
     *
     * KeyValueIterator는 AutoCloseable이므로 try-with-resources로 반드시 닫아야 한다.
     * 닫지 않으면 RocksDB 리소스가 누수된다.
     */
    public List<PostView> getAllPosts() {
        ReadOnlyKeyValueStore<String, PostView> store = getStore();
        List<PostView> posts = new ArrayList<>();
        try (KeyValueIterator<String, PostView> iter = store.all()) {
            iter.forEachRemaining(kv -> posts.add(kv.value));
        }
        return posts;
    }

    /**
     * 사용자별 조회: 특정 userId가 작성한 PostView 목록을 반환한다.
     *
     * State Store의 key가 postId이므로 userId 기반 조회는 전체 스캔이 필요하다.
     * 프로덕션에서는 userId를 key로 하는 별도 State Store를 만들어야 한다.
     */
    public List<PostView> getPostsByUser(String userId) {
        ReadOnlyKeyValueStore<String, PostView> store = getStore();
        List<PostView> posts = new ArrayList<>();
        try (KeyValueIterator<String, PostView> iter = store.all()) {
            iter.forEachRemaining(kv -> {
                if (kv.value != null && userId.equals(kv.value.getUserId())) {
                    posts.add(kv.value);
                }
            });
        }
        return posts;
    }

    private ReadOnlyKeyValueStore<String, PostView> getStore() {
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
