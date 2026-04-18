package com.study.redpanda.ch03.dto;

import java.util.List;

/**
 * SAGA 상태 조회 API 응답
 *
 * Choreography의 한계인 "워크플로우 추적 어려움"을 보완한다.
 * correlationId로 4개 서비스의 상태를 한 번에 조회하여 전체 진행 상황을 파악한다.
 */
public record SagaStatusResponse(
        String correlationId,
        OrderInfo order,
        List<ReservationInfo> reservations,
        PaymentInfo payment,
        ShippingInfo shipping,
        List<String> processedSteps
) {
    public record OrderInfo(String orderId, String status, String failureReason, String trackingNumber) {}
    public record ReservationInfo(String reservationId, String productId, int quantity, String status) {}
    public record PaymentInfo(String paymentId, String transactionId, String amount, String status) {}
    public record ShippingInfo(String shippingId, String trackingNumber, String status) {}
}
