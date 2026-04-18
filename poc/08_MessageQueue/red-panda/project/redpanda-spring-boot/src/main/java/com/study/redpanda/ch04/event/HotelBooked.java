package com.study.redpanda.ch04.event;

import java.time.Instant;

/**
 * 호텔 예약 성공 이벤트 (Hotel Service → Orchestrator)
 */
public record HotelBooked(
        String tripId,
        String sagaId,
        Instant timestamp,
        String reservationId
) {}
