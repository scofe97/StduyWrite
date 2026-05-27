package com.study.redpanda.ch04.event;

import java.time.Instant;

/**
 * 항공 예약 실패 이벤트 (Flight Service → Orchestrator)
 */
public record FlightBookingFailed(
        String tripId,
        String sagaId,
        Instant timestamp,
        String reason
) {}
