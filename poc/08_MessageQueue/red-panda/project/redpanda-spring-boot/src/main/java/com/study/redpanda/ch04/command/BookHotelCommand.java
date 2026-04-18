package com.study.redpanda.ch04.command;

import lombok.Builder;

import java.time.LocalDate;

/**
 * 호텔 예약 명령 (Orchestrator → Hotel Service)
 */
@Builder
public record BookHotelCommand(
        String tripId,
        String sagaId,
        String hotelName,
        LocalDate checkIn,
        LocalDate checkOut
) {}
