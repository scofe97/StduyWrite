package com.study.redpanda.ch03.event;

import java.time.Instant;
import java.util.List;

/**
 * 재고 예약 실패 이벤트
 * Inventory Service → Kafka → Order Service (FAILED 상태 전환)
 * 보상 불필요: SAGA의 첫 단계이므로 되돌릴 작업이 없음
 */
public record InventoryReservationFailed(
        String orderId,
        String correlationId,
        Instant timestamp,
        String reason,
        List<String> failedItems
) implements OrderSagaEvent {}
