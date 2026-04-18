package com.study.redpanda.ch03.event;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

/**
 * SAGA 시작 이벤트: 주문이 생성되었을 때 발행
 * Order Service → Kafka → Inventory Service
 */
public record OrderCreated(
        String orderId,
        String correlationId,
        Instant timestamp,
        String customerId,
        List<OrderItem> items,
        BigDecimal totalAmount
) implements OrderSagaEvent {

    /**
     * 주문 항목 (OrderCreated 내부에서만 사용)
     */
    public record OrderItem(
            String productId,
            String productName,
            int quantity,
            BigDecimal price
    ) {}
}
