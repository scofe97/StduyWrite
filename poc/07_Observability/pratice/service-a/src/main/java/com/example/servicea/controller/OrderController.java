package com.example.servicea.controller;

import com.example.servicea.client.InventoryClient;
import com.example.servicea.dto.OrderEvent;
import com.example.servicea.kafka.OrderProducer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);

    private final InventoryClient inventoryClient;
    private final OrderProducer orderProducer;

    public OrderController(InventoryClient inventoryClient, OrderProducer orderProducer) {
        this.inventoryClient = inventoryClient;
        this.orderProducer = orderProducer;
    }

    /**
     * 복잡한 주문 처리 시나리오
     *
     * 1. [동기 HTTP] Service-B에 재고 확인
     * 2. [비동기 Kafka] 주문 생성 이벤트 발행 → Service-B가 처리
     * 3. [비동기 Kafka] Service-B가 결제 완료 이벤트 발행 → Service-A가 수신
     */
    @PostMapping
    public Map<String, Object> createOrder(@RequestBody Map<String, Object> request) {
        String productId = (String) request.get("productId");
        int quantity = (Integer) request.getOrDefault("quantity", 1);
        String orderId = UUID.randomUUID().toString().substring(0, 8);

        log.info(">>> [ORDER] 주문 생성 시작: orderId={}, productId={}, quantity={}",
                orderId, productId, quantity);

        // 1. 동기 호출: 재고 확인 (HTTP → Service-B)
        log.info(">>> [ORDER] Step 1: 재고 확인 (동기 HTTP 호출)");
        Map<String, Object> inventoryResponse = inventoryClient.checkInventory(productId);
        boolean available = (Boolean) inventoryResponse.get("available");
        int stock = (Integer) inventoryResponse.get("stock");

        log.info(">>> [ORDER] 재고 확인 결과: available={}, stock={}", available, stock);

        if (!available || stock < quantity) {
            log.warn(">>> [ORDER] 재고 부족으로 주문 실패");
            return Map.of(
                "orderId", orderId,
                "status", "REJECTED",
                "reason", "재고 부족"
            );
        }

        // 2. 비동기 발행: 주문 생성 이벤트 (Kafka → Service-B)
        log.info(">>> [ORDER] Step 2: 주문 이벤트 발행 (비동기 Kafka)");
        OrderEvent orderEvent = new OrderEvent(orderId, productId, quantity, "CREATED");
        orderProducer.sendOrderCreatedEvent(orderEvent);

        // 3. 응답 반환 (비동기 결제 처리는 별도로 진행됨)
        log.info(">>> [ORDER] 주문 생성 완료 - 결제 처리 대기 중");
        return Map.of(
            "orderId", orderId,
            "status", "PROCESSING",
            "message", "주문이 접수되었습니다. 결제 처리 중입니다."
        );
    }
}
