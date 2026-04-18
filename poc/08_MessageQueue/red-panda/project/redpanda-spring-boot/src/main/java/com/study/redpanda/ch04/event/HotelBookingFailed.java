package com.study.redpanda.ch04.event;

import java.time.Instant;

/**
 * 호텔 예약 실패 이벤트 (Hotel Service → Orchestrator)
 */
public record HotelBookingFailed(
        String tripId,
        String sagaId,
        Instant timestamp,
        String reason
) {}
