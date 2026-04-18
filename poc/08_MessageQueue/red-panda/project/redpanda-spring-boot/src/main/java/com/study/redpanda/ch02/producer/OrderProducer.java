package com.study.redpanda.ch02.producer;

import com.study.redpanda.avro.OrderEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.header.internals.RecordHeaders;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

@Slf4j
@Component
@RequiredArgsConstructor
public class OrderProducer {

    private static final long SYNC_TIMEOUT_SECONDS = 10;

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public CompletableFuture<SendResult<String, OrderEvent>> sendOrder(OrderEvent event) {
        return kafkaTemplate.send("chapter2.orders", event.getOrderId(), event)
                .whenComplete((result, ex) -> {
                    if (ex != null) {
                        log.error("Failed to send message: {}", event.getOrderId(), ex);
                    } else {
                        log.info("Sent message: topic={}, partition={}, offset={}",
                                result.getRecordMetadata().topic(),
                                result.getRecordMetadata().partition(),
                                result.getRecordMetadata().offset());
                    }
                });
    }

    public CompletableFuture<SendResult<String, OrderEvent>> sendOrderWithHeaders(
            OrderEvent event, Map<String, String> headers) {
        RecordHeaders recordHeaders = new RecordHeaders();
        headers.forEach((key, value) ->
                recordHeaders.add(key, value.getBytes(StandardCharsets.UTF_8)));

        ProducerRecord<String, OrderEvent> record = new ProducerRecord<>(
                "chapter2.orders",
                null,           // partition (자동 할당)
                event.getOrderId(),  // key
                event,               // value
                recordHeaders        // headers
        );

        return kafkaTemplate.send(record)
                .whenComplete((result, ex) -> {
                    if (ex != null) {
                        log.error("Failed to send message with headers: {}", event.getOrderId(), ex);
                    } else {
                        log.info("Sent with headers: topic={}, partition={}, offset={}, headerCount={}",
                                result.getRecordMetadata().topic(),
                                result.getRecordMetadata().partition(),
                                result.getRecordMetadata().offset(),
                                headers.size());
                    }
                });
    }

    public SendResult<String, OrderEvent> sendOrderSync(OrderEvent event) {
        try {
            SendResult<String, OrderEvent> result = kafkaTemplate
                    .send("chapter2.orders", event.getOrderId(), event)
                    .get(SYNC_TIMEOUT_SECONDS, TimeUnit.SECONDS);

            log.info("Sync sent: topic={}, partition={}, offset={}",
                    result.getRecordMetadata().topic(),
                    result.getRecordMetadata().partition(),
                    result.getRecordMetadata().offset());

            return result;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Interrupted while sending message: " + event.getOrderId(), e);
        } catch (ExecutionException e) {
            throw new RuntimeException("Failed to send message: " + event.getOrderId(), e.getCause());
        } catch (TimeoutException e) {
            throw new RuntimeException("Timeout sending message: " + event.getOrderId(), e);
        }
    }
}
