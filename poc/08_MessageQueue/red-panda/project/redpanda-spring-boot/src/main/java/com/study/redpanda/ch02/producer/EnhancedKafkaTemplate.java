package com.study.redpanda.ch02.producer;

import com.study.redpanda.avro.OrderEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

/**
 * Ch02 P6: KafkaTemplate 래퍼 (Spring 방식)
 *
 * P5(ProducerInterceptor)의 Spring 대안.
 * 공통 헤더를 자동 추가하면서 Spring Bean 주입과 조건부 로직을 사용할 수 있다.
 *
 * P5 vs P6:
 * - P5: Kafka 네이티브, YAML 설정, Spring Bean 주입 불가
 * - P6: Spring 방식, Bean 주입 가능, 조건부 헤더, 비즈니스 로직 포함 가능
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class EnhancedKafkaTemplate {

    private static final String SERVICE_NAME = "order-service";

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    /**
     * 공통 헤더를 자동 추가하여 전송한다.
     * - X-Service-Name: 발신 서비스명
     * - X-Correlation-Id: 요청 추적용 UUID
     * - X-Sent-At: 전송 시각 (ISO-8601)
     */
    public CompletableFuture<SendResult<String, OrderEvent>> send(
            String topic, String key, OrderEvent value) {

        ProducerRecord<String, OrderEvent> record = new ProducerRecord<>(topic, key, value);

        // 공통 헤더 자동 추가
        record.headers().add("X-Service-Name",
                SERVICE_NAME.getBytes(StandardCharsets.UTF_8));
        record.headers().add("X-Correlation-Id",
                UUID.randomUUID().toString().getBytes(StandardCharsets.UTF_8));
        record.headers().add("X-Sent-At",
                Instant.now().toString().getBytes(StandardCharsets.UTF_8));

        return kafkaTemplate.send(record)
                .whenComplete((result, ex) -> {
                    if (ex != null) {
                        log.error("EnhancedKafkaTemplate: failed to send key={}", key, ex);
                    } else {
                        log.info("EnhancedKafkaTemplate: sent topic={}, partition={}, offset={}, key={}",
                                result.getRecordMetadata().topic(),
                                result.getRecordMetadata().partition(),
                                result.getRecordMetadata().offset(),
                                key);
                    }
                });
    }
}
