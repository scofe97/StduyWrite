package com.study.redpanda.cqrs.query.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.HashSet;
import java.util.Set;

/**
 * CQRS Query Side: 팔로우 목록 읽기 모델
 *
 * follows-store State Store에 저장되는 뷰 모델이다.
 * UserFollowed 이벤트로 followees에 추가되고,
 * UserUnfollowed 이벤트로 followees에서 제거된다.
 *
 * Set을 사용하여 같은 사용자를 중복 팔로우해도 한 번만 저장된다.
 * JsonSerde로 직렬화/역직렬화되므로 기본 생성자와 setter가 필요하다.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FollowsView {

    private String followerId;
    @Builder.Default
    private Set<String> followees = new HashSet<>();
}
