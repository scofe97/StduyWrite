package com.study.redpanda.cqrs.handler;

import com.study.redpanda.avro.social.UserFollowed;
import com.study.redpanda.avro.social.UserUnfollowed;
import com.study.redpanda.cqrs.command.FollowUserCommand;
import com.study.redpanda.cqrs.command.UnfollowUserCommand;
import com.study.redpanda.cqrs.config.CqrsTopics;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * 팔로우 관련 Command Handler (CQRS Command Side)
 *
 * 팔로우/언팔로우 이벤트를 social.events.follows 토픽에 발행한다.
 * followerId를 파티션 키로 사용하여 동일 사용자의 팔로우 이벤트 순서를 보장한다.
 *
 * eventId(UUID v7)와 timestamp는 CqrsEventPublisher가 공통 주입한다.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class FollowCommandHandler {

    private final CqrsEventPublisher eventPublisher;

    // CqrsTopics 중앙 관리 참조

    /**
     * 팔로우 이벤트 발행
     *
     * @param cmd 팔로우 커맨드 (followerId, followeeId)
     * @return 발행된 이벤트의 eventId
     */
    public String followUser(FollowUserCommand cmd) {
        UserFollowed event = UserFollowed.newBuilder()
                .setFollowerId(cmd.followerId())
                .setFolloweeId(cmd.followeeId())
                .build();

        return eventPublisher.publish(CqrsTopics.USER_FOLLOWED, cmd.followerId(), event);
    }

    /**
     * 언팔로우 이벤트 발행
     *
     * @param cmd 언팔로우 커맨드 (followerId, followeeId)
     * @return 발행된 이벤트의 eventId
     */
    public String unfollowUser(UnfollowUserCommand cmd) {
        UserUnfollowed event = UserUnfollowed.newBuilder()
                .setFollowerId(cmd.followerId())
                .setFolloweeId(cmd.followeeId())
                .build();

        return eventPublisher.publish(CqrsTopics.USER_UNFOLLOWED, cmd.followerId(), event);
    }
}
