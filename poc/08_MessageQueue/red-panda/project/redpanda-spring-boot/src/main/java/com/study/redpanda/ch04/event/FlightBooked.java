package com.study.redpanda.ch04.event;

import java.time.Instant;

/**
 * 항공 예약 성공 이벤트 (Flight Service → Orchestrator)
 */
public record FlightBooked(
        String tripId,
        String sagaId,
        Instant timestamp,
        String reservationId
) {}
