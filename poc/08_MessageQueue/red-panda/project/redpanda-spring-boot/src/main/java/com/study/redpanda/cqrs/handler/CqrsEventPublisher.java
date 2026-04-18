package com.study.redpanda.cqrs.handler;

import com.github.f4b6a3.uuid.UuidCreator;
import org.apache.avro.Schema;
import org.apache.avro.specific.SpecificRecord;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;

/**
 * CQRS 이벤트 공통 발행기
 *
 * 모든 CQRS 이벤트에 공통인 eventId(UUID v7)와 timestamp(epoch millis)를
 * send 직전에 SpecificRecord.put()으로 자동 주입한다.
 * Handler는 도메인 필드만 설정하면 된다.
 *
 * Avro 스키마에서 eventId(default="")와 timestamp(default=0)로 선언하여
 * 빌더가 이 필드 없이도 build()를 허용하도록 했다.
 */
@Component
public class CqrsEventPublisher {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public CqrsEventPublisher(
            @Qualifier("cqrsKafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    /**
     * 이벤트에 eventId/timestamp를 주입하고 Kafka로 발행한다.
     *
     * @param topic Kafka 토픽명
     * @param key   파티션 키 (aggregateId)
     * @param event Avro SpecificRecord (eventId, timestamp 필드 보유)
     * @return 주입된 eventId (UUID v7, 시간 순서 보장)
     */
    public String publish(String topic, String key, SpecificRecord event) {
        String eventId = UuidCreator.getTimeOrderedEpoch().toString();
        long timestamp = Instant.now().toEpochMilli();

        Schema schema = event.getSchema();

        Schema.Field eventIdField = schema.getField("eventId");
        if (eventIdField != null) {
            event.put(eventIdField.pos(), eventId);
        }

        Schema.Field timestampField = schema.getField("timestamp");
        if (timestampField != null) {
            event.put(timestampField.pos(), timestamp);
        }

        kafkaTemplate.send(topic, key, event);

        return eventId;
    }
}
