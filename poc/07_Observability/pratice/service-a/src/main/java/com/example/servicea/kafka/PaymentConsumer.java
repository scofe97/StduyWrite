package com.example.servicea.kafka;

import com.example.servicea.dto.PaymentEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class PaymentConsumer {

    private static final Logger log = LoggerFactory.getLogger(PaymentConsumer.class);

    @KafkaListener(topics = "payment-events", groupId = "service-a-group")
    public void handlePaymentEvent(PaymentEvent event) {
        log.info(">>> [KAFKA CONSUMER] 결제 이벤트 수신: {}", event);

        // 비즈니스 로직: 주문 상태 업데이트
        try {
            Thread.sleep(50); // 처리 시뮬레이션
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        if ("COMPLETED".equals(event.getStatus())) {
            log.info(">>> [KAFKA CONSUMER] 주문 {} 완료 처리됨!", event.getOrderId());
        } else {
            log.warn(">>> [KAFKA CONSUMER] 주문 {} 결제 실패!", event.getOrderId());
        }
    }
}
