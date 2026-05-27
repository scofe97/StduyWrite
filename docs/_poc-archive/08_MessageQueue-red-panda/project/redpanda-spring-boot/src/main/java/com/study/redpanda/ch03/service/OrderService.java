package com.study.redpanda.ch03.service;

import com.study.redpanda.avro.saga.SagaInventoryReservationFailed;
import com.study.redpanda.avro.saga.SagaPaymentFailed;
import com.study.redpanda.avro.saga.SagaShippingFailed;
import com.study.redpanda.avro.saga.SagaShippingRequested;
import com.study.redpanda.ch03.domain.Order;
import com.study.redpanda.ch03.domain.OrderStatus;
import com.study.redpanda.ch03.dto.CreateOrderRequest;
import com.study.redpanda.ch03.event.OrderCreated;
import com.study.redpanda.ch03.event.ShippingRequested;
import com.study.redpanda.ch03.domain.SagaStepType;
import com.study.redpanda.ch03.event.mapper.SagaEventMapper;
import com.study.redpanda.ch03.repository.OrderRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

@Service
@Slf4j
public class OrderService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final OrderRepository orderRepository;
    private final EventIdempotencyChecker idempotencyChecker;

    public OrderService(
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate,
            OrderRepository orderRepository,
            EventIdempotencyChecker idempotencyChecker) {
        this.kafkaTemplate = kafkaTemplate;
        this.orderRepository = orderRepository;
        this.idempotencyChecker = idempotencyChecker;
    }

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        String correlationId = UUID.randomUUID().toString();

        BigDecimal totalAmount = request.items().stream()
                .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        Order order = Order.builder()
                .id(UUID.randomUUID().toString())
                .customerId(request.customerId())
                .items(request.items())
                .totalAmount(totalAmount)
                .status(OrderStatus.PENDING)
                .correlationId(correlationId)
                .build();

        orderRepository.save(order);

        // OrderLineItem → OrderCreated.OrderItem 변환
        var eventItems = order.getItems().stream()
                .map(item -> new OrderCreated.OrderItem(
                        item.getProductId(), item.getProductName(),
                        item.getQuantity(), item.getPrice()))
                .toList();

        OrderCreated domainEvent = new OrderCreated(
                order.getId(),
                correlationId,
                Instant.now(),
                order.getCustomerId(),
                eventItems,
                order.getTotalAmount());

        kafkaTemplate.send("chapter3.order-created", SagaEventMapper.toAvro(domainEvent));

        log.info("[SAGA] Order created: orderId={}, correlationId={}", order.getId(), correlationId);
        return order;
    }

    @Transactional
    @KafkaListener(topics = "chapter3.shipping-requested",
                   groupId = "ch03-order-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onShippingRequested(SagaShippingRequested avroEvent, Acknowledgment ack) {
        ShippingRequested event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.ORDER_COMPLETE)) {
                log.warn("[SAGA] Duplicate OrderComplete ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            Order order = orderRepository.findById(event.orderId()).orElseThrow();
            order.setStatus(OrderStatus.COMPLETED);
            order.setTrackingNumber(event.trackingNumber());
            orderRepository.save(order);

            log.info("[SAGA] Order completed: orderId={}, tracking={}", event.orderId(), event.trackingNumber());
            ack.acknowledge();
        } finally {
            SagaMdc.clear();
        }
    }

    @Transactional
    @KafkaListener(topics = "chapter3.inventory-reservation-failed",
                   groupId = "ch03-order-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onInventoryReservationFailed(SagaInventoryReservationFailed avroEvent, Acknowledgment ack) {
        String correlationId = avroEvent.getCorrelationId().toString();
        String orderId = avroEvent.getOrderId().toString();
        SagaMdc.set(correlationId, orderId);
        try {
            if (!idempotencyChecker.tryAcquire(correlationId, SagaStepType.ORDER_FAIL_INVENTORY)) {
                ack.acknowledge();
                return;
            }

            markOrderFailed(orderId, "Inventory: " + avroEvent.getReason().toString());
            ack.acknowledge();
        } finally {
            SagaMdc.clear();
        }
    }

    @Transactional
    @KafkaListener(topics = "chapter3.payment-failed",
                   groupId = "ch03-order-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onPaymentFailed(SagaPaymentFailed avroEvent, Acknowledgment ack) {
        String correlationId = avroEvent.getCorrelationId().toString();
        String orderId = avroEvent.getOrderId().toString();
        SagaMdc.set(correlationId, orderId);
        try {
            if (!idempotencyChecker.tryAcquire(correlationId, SagaStepType.ORDER_FAIL_PAYMENT)) {
                ack.acknowledge();
                return;
            }

            markOrderFailed(orderId, "Payment: " + avroEvent.getReason().toString());
            ack.acknowledge();
        } finally {
            SagaMdc.clear();
        }
    }

    @Transactional
    @KafkaListener(topics = "chapter3.shipping-failed",
                   groupId = "ch03-order-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onShippingFailed(SagaShippingFailed avroEvent, Acknowledgment ack) {
        String correlationId = avroEvent.getCorrelationId().toString();
        String orderId = avroEvent.getOrderId().toString();
        SagaMdc.set(correlationId, orderId);
        try {
            if (!idempotencyChecker.tryAcquire(correlationId, SagaStepType.ORDER_FAIL_SHIPPING)) {
                ack.acknowledge();
                return;
            }

            markOrderFailed(orderId, "Shipping: " + avroEvent.getReason().toString());
            ack.acknowledge();
        } finally {
            SagaMdc.clear();
        }
    }

    private void markOrderFailed(String orderId, String reason) {
        Order order = orderRepository.findById(orderId).orElseThrow();
        order.setStatus(OrderStatus.FAILED);
        order.setFailureReason(reason);
        orderRepository.save(order);

        log.error("[SAGA] Order failed: orderId={}, reason={}", orderId, reason);
    }
}
