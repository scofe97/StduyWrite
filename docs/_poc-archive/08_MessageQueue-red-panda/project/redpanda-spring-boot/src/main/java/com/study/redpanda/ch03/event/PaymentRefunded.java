package com.study.redpanda.ch03.event;

import java.math.BigDecimal;
import java.time.Instant;

/**
 * 보상 이벤트: 결제 환불 완료
 * Payment Service가 ShippingFailed를 받으면 환불 후 발행
 * Inventory Service는 이 이벤트를 받아 재고를 복구함
 *
 * 보상 순서: ShippingFailed → PaymentRefunded → InventoryReleased (역순)
 */
public record PaymentRefunded(
        String orderId,
        String correlationId,
        Instant timestamp,
        String transactionId,
        BigDecimal amount
) implements OrderSagaEvent {}
