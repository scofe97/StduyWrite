package com.study.redpanda.ch03.event;

import java.time.Instant;
import java.util.List;

/**
 * 재고 예약 성공 이벤트
 * Inventory Service → Kafka → Payment Service
 */
public record InventoryReserved(
        String orderId,
        String correlationId,
        Instant timestamp,
        List<String> reservationIds
) implements OrderSagaEvent {}
