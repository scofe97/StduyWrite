package com.study.redpanda.cqrs.query.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

/**
 * CQRS Query Side: 게시물 읽기 모델
 *
 * posts-store State Store에 저장되는 뷰 모델이다.
 * PostCreated 이벤트로 초기화되고, PostLiked 이벤트가 올 때마다
 * likeCount와 likedBy가 누적된다.
 *
 * JsonSerde로 직렬화/역직렬화되므로 기본 생성자와 setter가 필요하다.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostView {

    private String postId;
    private String userId;
    private String content;
    private int likeCount;
    @Builder.Default
    private List<String> likedBy = new ArrayList<>();
    private long createdAt;
}
