package com.study.redpanda.ch03.controller;

import com.study.redpanda.ch03.domain.*;
import com.study.redpanda.ch03.dto.SagaStatusResponse;
import com.study.redpanda.ch03.dto.SagaStatusResponse.*;
import com.study.redpanda.ch03.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * SAGA 상태 추적 API
 *
 * Choreography 패턴에서는 전체 SAGA 진행 상태를 한곳에서 조회할 수 없다.
 * 이 API는 correlationId를 기준으로 4개 서비스(Order, Inventory, Payment, Shipping)의
 * 상태를 통합 조회하여 Choreography의 "관측 가능성" 한계를 보완한다.
 *
 * 프로덕션에서는 Orchestration 전환 시 이 역할이 Orchestrator에 내장된다.
 */
@RestController
@RequestMapping("/api/ch03/saga")
@RequiredArgsConstructor
public class SagaStatusController {

    private final OrderRepository orderRepository;
    private final ReservationRepository reservationRepository;
    private final PaymentRepository paymentRepository;
    private final ShippingRepository shippingRepository;
    private final ProcessedEventRepository processedEventRepository;

    @GetMapping("/{correlationId}/status")
    public ResponseEntity<SagaStatusResponse> getSagaStatus(@PathVariable String correlationId) {
        // 1. Order 조회 (correlationId → orderId 매핑)
        Order order = orderRepository.findByCorrelationId(correlationId).orElse(null);
        if (order == null) {
            return ResponseEntity.notFound().build();
        }

        String orderId = order.getId();

        // 2. 각 서비스 상태 조회
        OrderInfo orderInfo = new OrderInfo(
                order.getId(),
                order.getStatus().name(),
                order.getFailureReason(),
                order.getTrackingNumber());

        List<ReservationInfo> reservationInfos = reservationRepository.findByOrderId(orderId).stream()
                .map(r -> new ReservationInfo(
                        r.getId(), r.getProductId(), r.getQuantity(), r.getStatus().name()))
                .toList();

        PaymentInfo paymentInfo = paymentRepository.findByOrderId(orderId)
                .map(p -> new PaymentInfo(
                        p.getId(), p.getTransactionId(), p.getAmount().toPlainString(), p.getStatus().name()))
                .orElse(null);

        ShippingInfo shippingInfo = shippingRepository.findByOrderId(orderId)
                .map(s -> new ShippingInfo(
                        s.getId(), s.getTrackingNumber(), s.getStatus().name()))
                .orElse(null);

        // 3. 처리 완료 단계 조회 (멱등성 테이블 재활용)
        List<String> processedSteps = processedEventRepository.findByCorrelationId(correlationId).stream()
                .map(pe -> pe.getEventType().name())
                .toList();

        return ResponseEntity.ok(new SagaStatusResponse(
                correlationId, orderInfo, reservationInfos, paymentInfo, shippingInfo, processedSteps));
    }
}
