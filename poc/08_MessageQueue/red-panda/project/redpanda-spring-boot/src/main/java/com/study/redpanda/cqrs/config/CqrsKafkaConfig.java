package com.study.redpanda.cqrs.config;

import io.confluent.kafka.serializers.KafkaAvroSerializer;
import io.confluent.kafka.serializers.subject.TopicRecordNameStrategy;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.ProducerListener;

import java.util.HashMap;
import java.util.Map;

/**
 * CQRS Command Side 전용 Kafka 설정
 *
 * Command Side는 이벤트를 발행(Produce)하는 역할만 한다.
 * Query Side(practice #4)가 이벤트를 소비하여 Read Model을 구성하므로,
 * 이 설정에는 Consumer와 Transaction Manager가 필요하지 않다.
 *
 * 트랜잭션 없이 멱등 프로듀서(enable.idempotence=true)만 활성화한다.
 * Consumer-Producer 체인이 없으므로 transactionIdPrefix는 설정하지 않는다.
 */
@Configuration
public class CqrsKafkaConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.producer.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    @Value("${spring.kafka.producer.properties.auto.register.schemas:true}")
    private boolean autoRegisterSchemas;

    /**
     * CQRS Command Side 전용 ProducerFactory
     *
     * 하나의 토픽(social.events.posts, social.events.follows)에
     * 여러 Avro 타입을 발행하므로 TopicRecordNameStrategy를 사용한다.
     */
    @Bean("cqrsProducerFactory")
    public ProducerFactory<String, Object> cqrsProducerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put("auto.register.schemas", autoRegisterSchemas);

        // 하나의 토픽에 여러 Avro 타입을 발행하기 위한 전략 (ch04 패턴과 동일)
        props.put("value.subject.name.strategy", TopicRecordNameStrategy.class);

        // 멱등 프로듀서: PID+시퀀스로 브로커 측 중복 제거
        // transactionIdPrefix 없이 idempotence만 활성화 (Command Side는 단순 발행)
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);

        // ch02 CommonHeaderInterceptor 재사용 (관측성 일관성)
        props.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,
                "com.study.redpanda.ch02.interceptor.CommonHeaderInterceptor");

        return new DefaultKafkaProducerFactory<>(props);
    }

    /**
     * CQRS 전용 KafkaTemplate
     *
     * ProducerListener를 등록하여 모든 send()에 대해 공통 성공/실패 로그를 남긴다.
     * Handler마다 whenComplete()를 반복할 필요가 없어진다.
     */
    @Bean("cqrsKafkaTemplate")
    public KafkaTemplate<String, Object> cqrsKafkaTemplate(
            @org.springframework.beans.factory.annotation.Qualifier("cqrsProducerFactory")
            ProducerFactory<String, Object> producerFactory) {
        KafkaTemplate<String, Object> template = new KafkaTemplate<>(producerFactory);
        template.setProducerListener(cqrsProducerListener());
        return template;
    }

    private ProducerListener<String, Object> cqrsProducerListener() {
        Logger log = LoggerFactory.getLogger("cqrs.producer");

        return new ProducerListener<>() {
            @Override
            public void onSuccess(ProducerRecord<String, Object> record, RecordMetadata metadata) {
                log.info("Event sent: topic={}, key={}, partition={}, offset={}",
                        metadata.topic(), record.key(), metadata.partition(), metadata.offset());
            }

            @Override
            public void onError(ProducerRecord<String, Object> record, RecordMetadata metadata, Exception ex) {
                log.error("Event failed: topic={}, key={}, error={}",
                        record.topic(), record.key(), ex.getMessage(), ex);
            }
        };
    }
}
