package com.study.redpanda.cqrs.command;

import lombok.Builder;

/**
 * 사용자 팔로우 커맨드
 */
@Builder
public record FollowUserCommand(
        String followerId,
        String followeeId
) {}
