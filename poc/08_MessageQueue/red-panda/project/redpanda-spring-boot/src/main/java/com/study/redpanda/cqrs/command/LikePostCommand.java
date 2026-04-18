package com.study.redpanda.cqrs.command;

import lombok.Builder;

/**
 * 게시물 좋아요 커맨드
 */
@Builder
public record LikePostCommand(
        String postId,
        String userId
) {}
