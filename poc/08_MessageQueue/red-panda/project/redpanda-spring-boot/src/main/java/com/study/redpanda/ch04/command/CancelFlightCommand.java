package com.study.redpanda.ch04.command;

import lombok.Builder;

/**
 * 항공 예약 취소 명령 — 보상 트랜잭션 (Orchestrator → Flight Service)
 */
@Builder
public record CancelFlightCommand(
        String tripId,
        String sagaId,
        String reservationId
) {}
