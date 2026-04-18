package com.study.redpanda.ch03.event;

import java.math.BigDecimal;
import java.time.Instant;

/**
 * 결제 성공 이벤트
 * Payment Service → Kafka → Shipping Service
 */
public record PaymentCompleted(
        String orderId,
        String correlationId,
        Instant timestamp,
        String transactionId,
        BigDecimal amount
) implements OrderSagaEvent {}
