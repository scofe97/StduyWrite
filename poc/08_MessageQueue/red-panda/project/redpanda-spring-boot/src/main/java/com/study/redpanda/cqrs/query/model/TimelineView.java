package com.study.redpanda.cqrs.query.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

/**
 * CQRS Query Side: 타임라인 읽기 모델
 *
 * timeline-store State Store에 저장되는 뷰 모델이다.
 * key = userId (타임라인 소유자), value = TimelineView (해당 사용자의 피드)
 *
 * Fan-out on Write 방식: 게시물 작성 시 작성자의 모든 팔로워 타임라인에 엔트리를 추가한다.
 * 팔로우 시점 이전의 기존 게시물은 백필하지 않는다 (Eventual Consistency 허용).
 *
 * JsonSerde로 직렬화/역직렬화되므로 기본 생성자와 setter가 필요하다.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TimelineView {

    private String userId;
    @Builder.Default
    private List<TimelineEntry> entries = new ArrayList<>();

    /**
     * 타임라인의 개별 엔트리.
     *
     * 게시물의 핵심 정보만 비정규화하여 저장한다.
     * posts-store를 조인하지 않고도 타임라인만으로 피드를 렌더링할 수 있다.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class TimelineEntry {
        private String postId;
        private String authorId;
        private String content;
        private long createdAt;
    }
}
