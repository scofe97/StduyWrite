package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.util.concurrent.CountDownLatch;

/**
 * Ch02: Producer-Consumer - 주문 이벤트 소비 (Avro)
 */
@Slf4j
@Component
public class OrderConsumer {

    @Getter
    private CountDownLatch latch = new CountDownLatch(1);

    @Getter
    private OrderEvent lastReceivedEvent;

    @Getter
    private int lastReceivedPartition = -1;

    @Getter
    private long lastReceivedOffset = -1;

    @Getter
    private String lastReceivedCorrelationId;

    @Getter
    private String lastReceivedSource;

    // P5: 인터셉터가 자동 주입하는 헤더
    @Getter
    private String lastReceivedServiceName;

    @Getter
    private String lastReceivedSentAt;

    public void resetLatch(int count) {
        this.latch = new CountDownLatch(count);
    }

    @KafkaListener(topics = "chapter2.orders", groupId = "order-consumer-group")
    public void consume(
            @Payload OrderEvent event,
            @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            @Header(KafkaHeaders.OFFSET) long offset,
            @Header(KafkaHeaders.RECEIVED_TIMESTAMP) long timestamp,
            @Header(KafkaHeaders.RECEIVED_KEY) String key,
            @Header(value = "X-Correlation-Id", required = false) String correlationId,
            @Header(value = "X-Source", required = false) String source,
            @Header(value = "X-Service-Name", required = false) String serviceName,
            @Header(value = "X-Sent-At", required = false) String sentAt,
            Acknowledgment ack
    ) {
        log.info("Received: orderId={}, topic={}, partition={}, offset={}, key={}, correlationId={}, source={}, serviceName={}, sentAt={}",
                event.getOrderId(), topic, partition, offset, key, correlationId, source, serviceName, sentAt);

        lastReceivedEvent = event;
        lastReceivedPartition = partition;
        lastReceivedOffset = offset;
        lastReceivedCorrelationId = correlationId;
        lastReceivedSource = source;
        lastReceivedServiceName = serviceName;
        lastReceivedSentAt = sentAt;
        latch.countDown();
        ack.acknowledge();
    }
}
