package com.study.redpanda.cqrs.handler;

import com.study.redpanda.avro.social.PostCreated;
import com.study.redpanda.avro.social.PostLiked;
import com.study.redpanda.cqrs.command.CreatePostCommand;
import com.study.redpanda.cqrs.command.LikePostCommand;
import com.study.redpanda.cqrs.config.CqrsTopics;
import com.github.f4b6a3.uuid.UuidCreator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * 게시물 관련 Command Handler (CQRS Command Side)
 *
 * Kafka가 이벤트 스토어 역할을 한다. DB 저장 없이 검증 후 이벤트를 발행하고,
 * Query Side가 별도로 이벤트를 소비하여 Read Model을 구성한다.
 *
 * eventId(UUID v7)와 timestamp는 CqrsEventPublisher가 공통 주입한다.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class PostCommandHandler {

    private final CqrsEventPublisher eventPublisher;

    // CqrsTopics 중앙 관리 참조

    /**
     * 게시물 생성 이벤트 발행
     *
     * @param cmd 게시물 생성 커맨드 (userId, content)
     * @return [eventId, postId] — Controller에서 응답 조립에 사용
     */
    public String[] createPost(CreatePostCommand cmd) {
        String postId = UuidCreator.getTimeOrderedEpoch().toString();

        PostCreated event = PostCreated.newBuilder()
                .setPostId(postId)
                .setUserId(cmd.userId())
                .setContent(cmd.content())
                .build();

        String eventId = eventPublisher.publish(CqrsTopics.POST_CREATED, postId, event);
        return new String[]{eventId, postId};
    }

    /**
     * 게시물 좋아요 이벤트 발행
     *
     * @param cmd 좋아요 커맨드 (postId, userId)
     * @return 발행된 이벤트의 eventId
     */
    public String likePost(LikePostCommand cmd) {
        PostLiked event = PostLiked.newBuilder()
                .setPostId(cmd.postId())
                .setUserId(cmd.userId())
                .build();

        return eventPublisher.publish(CqrsTopics.POST_LIKED, cmd.postId(), event);
    }
}
