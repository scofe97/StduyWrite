package com.example.servicea.kafka;

import com.example.servicea.dto.OrderEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class OrderProducer {

    private static final Logger log = LoggerFactory.getLogger(OrderProducer.class);
    private static final String TOPIC = "order-events";

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public OrderProducer(KafkaTemplate<String, OrderEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendOrderCreatedEvent(OrderEvent event) {
        log.info(">>> [KAFKA PRODUCER] 주문 이벤트 발행: {}", event);

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
