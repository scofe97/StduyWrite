package com.study.redpanda.cqrs.controller;

import com.study.redpanda.cqrs.query.service.EventReplayService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * CQRS Admin REST API
 *
 * Event Replay 및 State Store 상태 조회를 위한 관리 엔드포인트.
 * Command Side(쓰기)나 Query Side(읽기)와 분리된 운영용 API다.
 *
 * 프로덕션에서는 인증/인가가 필수이지만, 학습 프로젝트에서는 생략한다.
 */
@RestController
@RequestMapping("/api/cqrs/admin")
@RequiredArgsConstructor
@Slf4j
public class CqrsAdminController {

    private final EventReplayService eventReplayService;

    /**
     * Approach A: Kafka Streams 리셋으로 State Store 재구축
     * POST /api/cqrs/admin/replay/streams-reset
     *
     * 파괴적(destructive) 작업: 재구축 중 Query API가 503을 반환한다.
     * stop → cleanUp → deleteConsumerGroup → start
     */
    @PostMapping("/replay/streams-reset")
    public ResponseEntity<Map<String, Object>> replayViaStreamsReset() {
        log.info("Admin: Streams reset replay requested");
        Map<String, Object> result = eventReplayService.replayViaStreamsReset();
        return ResponseEntity.ok(result);
    }

    /**
     * Approach B: 임시 Consumer로 이벤트 집계 (비파괴적)
     * POST /api/cqrs/admin/replay/manual-count
     *
     * 기존 Streams 앱에 영향 없이 전체 이벤트를 카운트한다.
     * Event Store가 불변 로그임을 확인하는 교육용 데모.
     */
    @PostMapping("/replay/manual-count")
    public ResponseEntity<Map<String, Object>> replayViaManualConsumer() {
        log.info("Admin: Manual consumer replay requested");
        Map<String, Object> result = eventReplayService.replayViaManualConsumer();
        return ResponseEntity.ok(result);
    }

    /**
     * State Store 상태 조회
     * GET /api/cqrs/admin/stores/status
     *
     * 4개 State Store의 엔트리 수를 반환한다.
     * 리플레이 전후 비교 시 유용하다.
     */
    @GetMapping("/stores/status")
    public ResponseEntity<Map<String, Object>> getStoresStatus() {
        Map<String, Object> result = eventReplayService.getStoresStatus();
        return ResponseEntity.ok(result);
    }
}
