package com.study.redpanda.cqrs.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.common.config.TopicConfig;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;

/**
 * CQRS Event Store 토픽 설정 — 토픽 1 이벤트 1 원칙
 *
 * 이벤트 타입별로 전용 토픽을 사용한다. 1 토픽 N 이벤트 방식은
 * Consumer가 이벤트 타입을 런타임에 분기해야 하므로 결합도가 높다.
 * 토픽을 분리하면 Consumer가 필요한 이벤트만 구독할 수 있고,
 * 토픽별 파티션/보존 정책을 독립적으로 튜닝할 수 있다.
 *
 * Event Sourcing에서 모든 이벤트는 영구 보존되어야 하므로 retention.ms=-1로 설정한다.
 *
 * cleanup.policy=delete를 사용하는 이유:
 * - compact는 같은 키의 최신 값만 유지 → Event Sourcing에서는 모든 이력이 필요
 * - delete + retention.ms=-1 = 모든 이벤트를 영구 보존 (Event Store의 핵심 특성)
 *
 * partition key 설계:
 * - post-created, post-liked: postId → 같은 게시물 이벤트가 동일 파티션에 저장
 * - user-followed, user-unfollowed: followerId → 같은 사용자의 팔로우 이벤트 순서 보장
 *
 * 주의: 토픽 분리 후 post-created와 post-liked 간 순서는 보장되지 않는다.
 * Query Side의 aggregate()에서 null 방어 코드가 이를 처리한다.
 */
@Configuration
public class CqrsTopicConfig {

    private NewTopic eventStoreTopic(String name) {
        return TopicBuilder.name(name)
                .partitions(3)
                .replicas(1)
                .config(TopicConfig.RETENTION_MS_CONFIG, "-1")         // 무한 보존 (Event Store)
                .config(TopicConfig.CLEANUP_POLICY_CONFIG, "delete")   // compact 아님 — 전체 이력 보존
                .build();
    }

    @Bean
    public NewTopic postCreatedTopic() {
        return eventStoreTopic(CqrsTopics.POST_CREATED);
    }

    @Bean
    public NewTopic postLikedTopic() {
        return eventStoreTopic(CqrsTopics.POST_LIKED);
    }

    @Bean
    public NewTopic userFollowedTopic() {
        return eventStoreTopic(CqrsTopics.USER_FOLLOWED);
    }

    @Bean
    public NewTopic userUnfollowedTopic() {
        return eventStoreTopic(CqrsTopics.USER_UNFOLLOWED);
    }
}
