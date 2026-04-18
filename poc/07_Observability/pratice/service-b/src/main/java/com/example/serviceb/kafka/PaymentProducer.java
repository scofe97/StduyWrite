package com.example.serviceb.kafka;

import com.example.serviceb.dto.PaymentEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class PaymentProducer {

    private static final Logger log = LoggerFactory.getLogger(PaymentProducer.class);
    private static final String TOPIC = "payment-events";

    private final KafkaTemplate<String, PaymentEvent> kafkaTemplate;

    public PaymentProducer(KafkaTemplate<String, PaymentEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendPaymentCompletedEvent(PaymentEvent event) {
        log.info(">>> [KAFKA PRODUCER] 결제 완료 이벤트 발행: {}", event);

        // Micrometer Tracing이 자동으로 Headers에 traceparent 삽입
        kafkaTemplate.send(TOPIC, event.getOrderId(), event)
            .whenComplete((result, ex) -> {
                if (ex == null) {
                    log.info(">>> [KAFKA PRODUCER] 발행 성공 - partition: {}, offset: {}",
                            result.getRecordMetadata().partition(),
                            result.getRecordMetadata().offset());
                } else {
                    log.error(">>> [KAFKA PRODUCER] 발행 실패", ex);
                }
            });
    }
}
