package com.study.redpanda.ch03.event;

import java.time.Instant;

/**
 * 배송 요청 성공 이벤트 (SAGA 최종 단계)
 * Shipping Service → Kafka → Order Service (COMPLETED 상태 전환)
 */
public record ShippingRequested(
        String orderId,
        String correlationId,
        Instant timestamp,
        String trackingNumber
) implements OrderSagaEvent {}
