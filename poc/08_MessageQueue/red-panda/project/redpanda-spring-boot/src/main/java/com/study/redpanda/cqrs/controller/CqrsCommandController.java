package com.study.redpanda.cqrs.controller;

import com.study.redpanda.cqrs.command.CreatePostCommand;
import com.study.redpanda.cqrs.command.FollowUserCommand;
import com.study.redpanda.cqrs.command.LikePostCommand;
import com.study.redpanda.cqrs.command.UnfollowUserCommand;
import com.study.redpanda.cqrs.handler.FollowCommandHandler;
import com.study.redpanda.cqrs.handler.PostCommandHandler;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * CQRS Command Side REST API
 *
 * Command는 즉시 처리 결과를 반환하지 않는다. 202 Accepted로 이벤트 발행 성공을
 * 알리고, 실제 상태 조회는 Query Side(practice #4)에서 담당한다.
 */
@RestController
@RequestMapping("/api/cqrs/commands")
@RequiredArgsConstructor
@Slf4j
public class CqrsCommandController {

    private final PostCommandHandler postCommandHandler;
    private final FollowCommandHandler followCommandHandler;

    /**
     * 게시물 생성
     * POST /api/cqrs/commands/posts
     */
    @PostMapping("/posts")
    public ResponseEntity<Map<String, String>> createPost(@RequestBody CreatePostCommand command) {
        log.info("Received CreatePostCommand: userId={}", command.userId());
        String[] result = postCommandHandler.createPost(command);
        return ResponseEntity.accepted().body(Map.of("eventId", result[0], "postId", result[1]));
    }

    /**
     * 게시물 좋아요
     * POST /api/cqrs/commands/posts/like
     */
    @PostMapping("/posts/like")
    public ResponseEntity<Map<String, String>> likePost(@RequestBody LikePostCommand command) {
        log.info("Received LikePostCommand: postId={}, userId={}", command.postId(), command.userId());
        String eventId = postCommandHandler.likePost(command);
        return ResponseEntity.accepted().body(Map.of("eventId", eventId));
    }

    /**
     * 사용자 팔로우
     * POST /api/cqrs/commands/follows
     */
    @PostMapping("/follows")
    public ResponseEntity<Map<String, String>> followUser(@RequestBody FollowUserCommand command) {
        log.info("Received FollowUserCommand: followerId={}, followeeId={}", command.followerId(), command.followeeId());
        String eventId = followCommandHandler.followUser(command);
        return ResponseEntity.accepted().body(Map.of("eventId", eventId));
    }

    /**
     * 사용자 언팔로우
     * DELETE /api/cqrs/commands/follows
     */
    @DeleteMapping("/follows")
    public ResponseEntity<Map<String, String>> unfollowUser(@RequestBody UnfollowUserCommand command) {
        log.info("Received UnfollowUserCommand: followerId={}, followeeId={}", command.followerId(), command.followeeId());
        String eventId = followCommandHandler.unfollowUser(command);
        return ResponseEntity.accepted().body(Map.of("eventId", eventId));
    }
}
