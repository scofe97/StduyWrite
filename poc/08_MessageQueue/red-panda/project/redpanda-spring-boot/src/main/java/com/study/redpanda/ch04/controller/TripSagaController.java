package com.study.redpanda.ch04.controller;

import com.study.redpanda.ch04.domain.SagaState;
import com.study.redpanda.ch04.repository.SagaStateRepository;
import com.study.redpanda.ch04.service.TripSagaOrchestrator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * Trip SAGA REST API
 *
 * SAGA 시작 및 상태 조회 엔드포인트를 제공한다.
 *
 * POST /api/ch04/saga/start         — SAGA 시작
 * GET  /api/ch04/saga/{sagaId}      — sagaId로 상태 조회
 * GET  /api/ch04/saga/trip/{tripId} — tripId로 상태 조회 (복수)
 */
@RestController
@RequestMapping("/api/ch04/saga")
@RequiredArgsConstructor
@Slf4j
public class TripSagaController {

    private final TripSagaOrchestrator orchestrator;
    private final SagaStateRepository sagaStateRepository;

    /**
     * SAGA 시작 API
     *
     * @param request 여행 예약 요청 정보
     * @return sagaId (SAGA 인스턴스 식별자)
     */
    @PostMapping("/start")
    public ResponseEntity<Map<String, String>> startSaga(@RequestBody StartTripRequest request) {
        log.info("Trip SAGA start request: tripId={}, departure={}, arrival={}",
                request.tripId(), request.departure(), request.arrival());

        String sagaId = orchestrator.startSaga(
                request.tripId(),
                request.departure(),
                request.arrival(),
                request.travelDate(),
                request.hotelName(),
                request.checkIn(),
                request.checkOut());

        return ResponseEntity.ok(Map.of("sagaId", sagaId));
    }

    /**
     * sagaId로 SAGA 상태 조회
     */
    @GetMapping("/{sagaId}")
    public ResponseEntity<SagaState> getSaga(@PathVariable String sagaId) {
        return sagaStateRepository.findById(sagaId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * tripId로 SAGA 상태 목록 조회
     *
     * 하나의 tripId에 여러 SAGA가 존재할 수 있다 (재시도 등).
     */
    @GetMapping("/trip/{tripId}")
    public ResponseEntity<List<SagaState>> getByTripId(@PathVariable String tripId) {
        return ResponseEntity.ok(sagaStateRepository.findByTripId(tripId));
    }

    /**
     * 여행 예약 시작 요청 DTO
     */
    public record StartTripRequest(
            String tripId,
            String departure,
            String arrival,
            LocalDate travelDate,
            String hotelName,
            LocalDate checkIn,
            LocalDate checkOut
    ) {}
}
