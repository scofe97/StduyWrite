package com.study.redpanda.ch03.event;

import java.time.Instant;

/**
 * 배송 실패 이벤트
 * Shipping Service → Kafka → Payment Service (보상: 환불) + Order Service (FAILED)
 * 보상 역순: 배송 실패 → 환불 → 재고 복구
 */
public record ShippingFailed(
        String orderId,
        String correlationId,
        Instant timestamp,
        String reason
) implements OrderSagaEvent {}
