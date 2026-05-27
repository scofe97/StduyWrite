package com.study.redpanda.ch03.event;

import java.time.Instant;

/**
 * 결제 실패 이벤트
 * Payment Service → Kafka → Inventory Service (보상: 재고 복구) + Order Service (FAILED)
 */
public record PaymentFailed(
        String orderId,
        String correlationId,
        Instant timestamp,
        String reason,
        String errorCode
) implements OrderSagaEvent {}
