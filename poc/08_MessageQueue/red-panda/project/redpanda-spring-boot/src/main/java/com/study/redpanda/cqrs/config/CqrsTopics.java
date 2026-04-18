package com.study.redpanda.cqrs.config;

import lombok.experimental.UtilityClass;

/**
 * CQRS 토픽명 중앙 관리
 *
 * TopicConfig, CommandHandler, StreamTopology에서 동일한 토픽명 문자열이
 * 중복되어 있었다. 토픽명 변경 시 한 곳만 수정하면 된다.
 */
@UtilityClass
public class CqrsTopics {

    public static final String POST_CREATED = "social.events.post-created";
    public static final String POST_LIKED = "social.events.post-liked";
    public static final String USER_FOLLOWED = "social.events.user-followed";
    public static final String USER_UNFOLLOWED = "social.events.user-unfollowed";
}
