package com.study.redpanda.ch03.event;

import java.time.Instant;
import java.util.List;

/**
 * 보상 이벤트: 재고 복구 완료
 * Inventory Service가 PaymentFailed 또는 PaymentRefunded를 받으면 발행
 * 예약된 재고를 원복하고 이 이벤트로 완료를 알림
 */
public record InventoryReleased(
        String orderId,
        String correlationId,
        Instant timestamp,
        List<String> reservationIds
) implements OrderSagaEvent {}
