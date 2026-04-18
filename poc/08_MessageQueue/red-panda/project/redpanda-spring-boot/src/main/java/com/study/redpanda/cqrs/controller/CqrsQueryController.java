package com.study.redpanda.cqrs.controller;

import com.study.redpanda.cqrs.query.model.FollowsView;
import com.study.redpanda.cqrs.query.model.PostView;
import com.study.redpanda.cqrs.query.model.TimelineView;
import com.study.redpanda.cqrs.query.service.FollowsQueryService;
import com.study.redpanda.cqrs.query.service.PostQueryService;
import com.study.redpanda.cqrs.query.service.TimelineQueryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;

/**
 * CQRS Query Side REST API
 *
 * Command Side(CqrsCommandController)와 완전히 분리된 읽기 전용 API다.
 * State Store를 Interactive Query로 직접 조회하므로 DB가 필요 없다.
 *
 * Command: POST /api/cqrs/commands/...  → 202 Accepted (이벤트 발행)
 * Query:   GET  /api/cqrs/query/...     → 200 OK (State Store 조회)
 */
@RestController
@RequestMapping("/api/cqrs/query")
@RequiredArgsConstructor
@Slf4j
public class CqrsQueryController {

    private final PostQueryService postQueryService;
    private final FollowsQueryService followsQueryService;
    private final TimelineQueryService timelineQueryService;

    // ─── Posts ────────────────────────────────────────────

    /**
     * 게시물 단건 조회
     * GET /api/cqrs/query/posts/{postId}
     */
    @GetMapping("/posts/{postId}")
    public ResponseEntity<?> getPost(@PathVariable String postId) {
        try {
            PostView post = postQueryService.getPost(postId);
            return ResponseEntity.ok(post);
        } catch (NoSuchElementException e) {
            return ResponseEntity.status(404).body(Map.of("error", e.getMessage()));
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 게시물 전체 조회
     * GET /api/cqrs/query/posts
     */
    @GetMapping("/posts")
    public ResponseEntity<?> getAllPosts() {
        try {
            List<PostView> posts = postQueryService.getAllPosts();
            return ResponseEntity.ok(posts);
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 사용자별 게시물 조회
     * GET /api/cqrs/query/users/{userId}/posts
     */
    @GetMapping("/users/{userId}/posts")
    public ResponseEntity<?> getPostsByUser(@PathVariable String userId) {
        try {
            List<PostView> posts = postQueryService.getPostsByUser(userId);
            return ResponseEntity.ok(posts);
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("error", e.getMessage()));
        }
    }

    // ─── Follows ─────────────────────────────────────────

    /**
     * 팔로잉 목록 조회
     * GET /api/cqrs/query/follows/{followerId}
     */
    @GetMapping("/follows/{followerId}")
    public ResponseEntity<?> getFollows(@PathVariable String followerId) {
        try {
            FollowsView follows = followsQueryService.getFollows(followerId);
            return ResponseEntity.ok(follows);
        } catch (NoSuchElementException e) {
            return ResponseEntity.status(404).body(Map.of("error", e.getMessage()));
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 팔로잉 여부 확인
     * GET /api/cqrs/query/follows/{followerId}/is-following/{followeeId}
     */
    @GetMapping("/follows/{followerId}/is-following/{followeeId}")
    public ResponseEntity<?> isFollowing(@PathVariable String followerId,
                                         @PathVariable String followeeId) {
        try {
            boolean following = followsQueryService.isFollowing(followerId, followeeId);
            return ResponseEntity.ok(Map.of("following", following));
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("error", e.getMessage()));
        }
    }

    // ─── Timeline ───────────────────────────────────────────

    /**
     * 타임라인 조회
     * GET /api/cqrs/query/timeline/{userId}
     *
     * 해당 사용자가 팔로우하는 사람들의 게시물 피드를 반환한다.
     * Fan-out on Write 방식이므로 조회 시점에 조인 없이 즉시 반환된다.
     */
    @GetMapping("/timeline/{userId}")
    public ResponseEntity<?> getTimeline(@PathVariable String userId) {
        try {
            TimelineView timeline = timelineQueryService.getTimeline(userId);
            return ResponseEntity.ok(timeline);
        } catch (NoSuchElementException e) {
            return ResponseEntity.status(404).body(Map.of("error", e.getMessage()));
        } catch (IllegalStateException e) {
            return ResponseEntity.status(503).body(Map.of("error", e.getMessage()));
        }
    }
}
