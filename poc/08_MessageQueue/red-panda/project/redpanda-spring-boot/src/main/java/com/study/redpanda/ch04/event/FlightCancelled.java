package com.study.redpanda.ch04.event;

import java.time.Instant;

/**
 * 항공 예약 취소 완료 이벤트 — 보상 결과 (Flight Service → Orchestrator)
 */
public record FlightCancelled(
        String tripId,
        String sagaId,
        Instant timestamp,
        String reservationId
) {}
