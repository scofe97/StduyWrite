package com.study.redpanda.cqrs.command;

import lombok.Builder;

/**
 * 게시물 생성 커맨드
 *
 * Command Side는 의도(intent)만 담는다. eventId와 timestamp는
 * Handler가 생성하여 Avro 이벤트에 포함시킨다.
 */
@Builder
public record CreatePostCommand(
        String userId,
        String content
) {}
