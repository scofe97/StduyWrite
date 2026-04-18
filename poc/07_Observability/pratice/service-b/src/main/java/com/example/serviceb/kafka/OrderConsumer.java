package com.example.serviceb.kafka;

import com.example.serviceb.dto.OrderEvent;
import com.example.serviceb.dto.PaymentEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.UUID;

@Component
public class OrderConsumer {

    private static final Logger log = LoggerFactory.getLogger(OrderConsumer.class);

    private final PaymentProducer paymentProducer;

    public OrderConsumer(PaymentProducer paymentProducer) {
        this.paymentProducer = paymentProducer;
    }

    @KafkaListener(topics = "order-events", groupId = "service-b-group")
    public void handleOrderEvent(OrderEvent event) {
        log.info(">>> [KAFKA CONSUMER] 주문 이벤트 수신: {}", event);

        // 1. 재고 차감 시뮬레이션
        log.info(">>> [KAFKA CONSUMER] 재고 차감 처리 중...");
        try {
            Thread.sleep(100); // 재고 차감 처리
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        log.info(">>> [KAFKA CONSUMER] 재고 차감 완료: productId={}, quantity={}",
                event.getProductId(), event.getQuantity());

        // 2. 결제 처리 시뮬레이션
        log.info(">>> [KAFKA CONSUMER] 결제 처리 중...");
        try {
            Thread.sleep(150); // 결제 처리
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // 3. 결제 완료 이벤트 발행 (→ Service-A로)
        String paymentId = "PAY-" + UUID.randomUUID().toString().substring(0, 6);
        PaymentEvent paymentEvent = new PaymentEvent(
            event.getOrderId(),
            paymentId,
            "COMPLETED",
            System.currentTimeMillis()
        );

        log.info(">>> [KAFKA CONSUMER] 결제 완료 이벤트 발행: {}", paymentEvent);
        paymentProducer.sendPaymentCompletedEvent(paymentEvent);
    }
}
