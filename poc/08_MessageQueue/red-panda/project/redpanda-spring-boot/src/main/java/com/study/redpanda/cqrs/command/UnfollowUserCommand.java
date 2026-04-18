package com.study.redpanda.cqrs.command;

import lombok.Builder;

/**
 * 사용자 언팔로우 커맨드
 */
@Builder
public record UnfollowUserCommand(
        String followerId,
        String followeeId
) {}
