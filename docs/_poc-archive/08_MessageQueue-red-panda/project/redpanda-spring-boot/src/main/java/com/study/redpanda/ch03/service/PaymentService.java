package com.study.redpanda.ch03.service;

import com.study.redpanda.avro.saga.SagaInventoryReserved;
import com.study.redpanda.avro.saga.SagaShippingFailed;
import com.study.redpanda.ch03.domain.Order;
import com.study.redpanda.ch03.domain.Payment;
import com.study.redpanda.ch03.domain.PaymentStatus;
import com.study.redpanda.ch03.event.InventoryReserved;
import com.study.redpanda.ch03.event.PaymentCompleted;
import com.study.redpanda.ch03.event.PaymentFailed;
import com.study.redpanda.ch03.event.PaymentRefunded;
import com.study.redpanda.ch03.event.ShippingFailed;
import com.study.redpanda.ch03.domain.SagaStepType;
import com.study.redpanda.ch03.event.mapper.SagaEventMapper;
import com.study.redpanda.ch03.repository.OrderRepository;
import com.study.redpanda.ch03.repository.PaymentRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.UUID;

@Service
@Slf4j
public class PaymentService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final PaymentRepository paymentRepository;
    private final OrderRepository orderRepository;
    private final EventIdempotencyChecker idempotencyChecker;

    public PaymentService(
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate,
            PaymentRepository paymentRepository,
            OrderRepository orderRepository,
            EventIdempotencyChecker idempotencyChecker) {
        this.kafkaTemplate = kafkaTemplate;
        this.paymentRepository = paymentRepository;
        this.orderRepository = orderRepository;
        this.idempotencyChecker = idempotencyChecker;
    }

    @Transactional
    @KafkaListener(topics = "chapter3.inventory-reserved",
                   groupId = "ch03-payment-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onInventoryReserved(SagaInventoryReserved avroEvent, Acknowledgment ack) {
        InventoryReserved event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.PAYMENT_PROCESS)) {
                log.warn("[SAGA] Duplicate PaymentProcess ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            log.info("[SAGA] Processing payment for order: {}", event.orderId());

            try {
                Order order = orderRepository.findById(event.orderId())
                        .orElseThrow(() -> new IllegalStateException("Order not found: " + event.orderId()));

                String transactionId = "TXN-" + UUID.randomUUID().toString().substring(0, 8);

                Payment payment = Payment.builder()
                        .id(UUID.randomUUID().toString())
                        .orderId(event.orderId())
                        .transactionId(transactionId)
                        .amount(order.getTotalAmount())
                        .status(PaymentStatus.COMPLETED)
                        .build();
                paymentRepository.save(payment);

                PaymentCompleted domainEvent = new PaymentCompleted(
                        event.orderId(),
                        event.correlationId(),
                        Instant.now(),
                        transactionId,
                        order.getTotalAmount());

                kafkaTemplate.send("chapter3.payment-completed", SagaEventMapper.toAvro(domainEvent));

                log.info("[SAGA] Payment completed: orderId={}, txnId={}", event.orderId(), transactionId);
                ack.acknowledge();

            } catch (Exception e) {
                PaymentFailed failedEvent = new PaymentFailed(
                        event.orderId(),
                        event.correlationId(),
                        Instant.now(),
                        e.getMessage(),
                        "PAY_ERROR");

                kafkaTemplate.send("chapter3.payment-failed", SagaEventMapper.toAvro(failedEvent));

                log.error("[SAGA] Payment failed: orderId={}", event.orderId(), e);
                ack.acknowledge();  // 실패 이벤트를 발행했으므로 처리 완료로 간주
            }
        } finally {
            SagaMdc.clear();
        }
    }

    // ─── 보상 트랜잭션 리스너 ──────────────────────────────────────────────

    /**
     * 배송 실패 → 환불 (보상)
     * 배송이 실패하면 결제를 환불하고 PaymentRefunded 이벤트를 발행한다.
     * 이 이벤트를 InventoryService가 받아 재고를 복구한다 (역순 보상).
     */
    @Transactional
    @KafkaListener(topics = "chapter3.shipping-failed",
                   groupId = "ch03-payment-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onShippingFailed(SagaShippingFailed avroEvent, Acknowledgment ack) {
        ShippingFailed event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.PAYMENT_REFUND)) {
                log.warn("[SAGA-COMPENSATE] Duplicate PaymentRefund ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            log.info("[SAGA-COMPENSATE] ShippingFailed received, refunding payment: orderId={}", event.orderId());

            try {
                Payment payment = paymentRepository.findByOrderId(event.orderId())
                        .orElseThrow(() -> new IllegalStateException("Payment not found for order: " + event.orderId()));

                if (payment.getStatus() == PaymentStatus.REFUNDED) {
                    log.warn("[SAGA-COMPENSATE] Payment already refunded, skipping: orderId={}", event.orderId());
                    ack.acknowledge();
                    return;
                }

                payment.setStatus(PaymentStatus.REFUNDED);
                paymentRepository.save(payment);

                PaymentRefunded domainEvent = new PaymentRefunded(
                        event.orderId(),
                        event.correlationId(),
                        Instant.now(),
                        payment.getTransactionId(),
                        payment.getAmount());

                kafkaTemplate.send("chapter3.payment-refunded", SagaEventMapper.toAvro(domainEvent));

                log.info("[SAGA-COMPENSATE] Payment refunded: orderId={}, txnId={}, amount={}",
                        event.orderId(), payment.getTransactionId(), payment.getAmount());
                ack.acknowledge();
            } catch (Exception e) {
                log.error("[SAGA-COMPENSATE] Failed to refund payment, will retry: orderId={}", event.orderId(), e);
                throw e;
            }
        } finally {
            SagaMdc.clear();
        }
    }
}
