package com.study.redpanda.ch04.command;

import lombok.Builder;

import java.time.LocalDate;

/**
 * 항공 예약 명령 (Orchestrator → Flight Service)
 */
@Builder
public record BookFlightCommand(
        String tripId,
        String sagaId,
        String departure,
        String arrival,
        LocalDate travelDate
) {}
