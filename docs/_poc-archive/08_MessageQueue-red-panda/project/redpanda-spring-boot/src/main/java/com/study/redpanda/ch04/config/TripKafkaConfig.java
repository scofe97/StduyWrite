package com.study.redpanda.ch04.config;

import io.confluent.kafka.serializers.KafkaAvroDeserializer;
import io.confluent.kafka.serializers.KafkaAvroDeserializerConfig;
import io.confluent.kafka.serializers.KafkaAvroSerializer;
import io.confluent.kafka.serializers.subject.TopicRecordNameStrategy;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.listener.ContainerProperties;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.kafka.transaction.KafkaTransactionManager;
import org.springframework.util.backoff.FixedBackOff;

import java.util.HashMap;
import java.util.Map;

/**
 * ch04 Trip SAGA Orchestration 전용 Kafka 트랜잭션 설정
 *
 * ch03 SagaKafkaConfig와 동일한 구조로, ch04 전용 빈을 구성한다:
 *
 * 1. Transactional ProducerFactory: transactional.id로 원자적 메시지 발행
 * 2. KafkaTemplate: 트랜잭션 ProducerFactory 사용
 * 3. KafkaTransactionManager: 리스너 컨테이너가 Kafka TX를 시작/커밋하도록 연결
 * 4. ConsumerFactory: isolation.level=read_committed (커밋된 메시지만 읽음)
 * 5. ListenerContainerFactory: KafkaTransactionManager + read_committed Consumer
 */
@Configuration
@EnableScheduling
public class TripKafkaConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.producer.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    @Value("${spring.kafka.producer.properties.auto.register.schemas:true}")
    private boolean autoRegisterSchemas;

    // ─── Transactional Producer ──────────────────────────────────────────

    @Bean("ch04ProducerFactory")
    public ProducerFactory<String, Object> ch04ProducerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put("auto.register.schemas", autoRegisterSchemas);

        // 하나의 토픽에 여러 Avro 타입을 보낼 수 있도록 TopicRecordNameStrategy 사용
        // 기본 TopicNameStrategy는 토픽당 하나의 스키마만 허용하여
        // chapter4.commands.flight에 BookFlightCommand + CancelFlightCommand를 보낼 때 NAME_MISMATCH 발생
        props.put("value.subject.name.strategy", TopicRecordNameStrategy.class);

        // Kafka 트랜잭션 필수 설정
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);   // PID+시퀀스로 중복 방지
        props.put(ProducerConfig.ACKS_CONFIG, "all");                // 모든 ISR 브로커 확인
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);

        // ch02 CommonHeaderInterceptor 재사용 (관측성 일관성)
        props.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,
                "com.study.redpanda.ch02.interceptor.CommonHeaderInterceptor");

        DefaultKafkaProducerFactory<String, Object> factory = new DefaultKafkaProducerFactory<>(props);
        factory.setTransactionIdPrefix("trip-saga-tx-");  // 트랜잭션 활성화 (인스턴스별 고유 접두사)
        return factory;
    }

    @Bean("ch04KafkaTemplate")
    public KafkaTemplate<String, Object> ch04KafkaTemplate(
            @Qualifier("ch04ProducerFactory") ProducerFactory<String, Object> producerFactory) {
        return new KafkaTemplate<>(producerFactory);
    }

    // ─── Kafka Transaction Manager ───────────────────────────────────────

    /**
     * 리스너 컨테이너가 Kafka 트랜잭션을 시작/커밋하도록 연결한다.
     * 이 매니저가 없으면 send()마다 개별 미니 트랜잭션이 생성되고,
     * Consumer 오프셋이 Kafka TX에 포함되지 않아 exactly-once가 불완전하다.
     */
    @Bean("ch04KafkaTransactionManager")
    public KafkaTransactionManager<String, Object> ch04KafkaTransactionManager(
            @Qualifier("ch04ProducerFactory") ProducerFactory<String, Object> producerFactory) {
        return new KafkaTransactionManager<>(producerFactory);
    }

    // ─── Read-Committed Consumer ─────────────────────────────────────────

    @Bean("ch04ConsumerFactory")
    public ConsumerFactory<String, Object> ch04ConsumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);
        // Producer와 동일한 TopicRecordNameStrategy (subject 이름 일관성)
        props.put("value.subject.name.strategy", TopicRecordNameStrategy.class);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

        // 트랜잭션 사용 시 필수: 커밋된 메시지만 읽음
        props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");

        return new DefaultKafkaConsumerFactory<>(props);
    }

    // ─── Error Handler + Dead Letter Topic ─────────────────────────────

    /**
     * 블로킹 재시도 + DLT (Dead Letter Topic) 에러 핸들러
     *
     * @RetryableTopic(논블로킹 재시도)는 KafkaTransactionManager와 공식 비호환이므로,
     * 트랜잭션 환경에서는 DefaultErrorHandler(블로킹 재시도)를 사용한다.
     */
    @Bean("ch04ErrorHandler")
    public DefaultErrorHandler ch04ErrorHandler(
            @Qualifier("ch04KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate) {
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate);
        // 3회 재시도, 1초 간격 (학습용 간단 설정)
        FixedBackOff backOff = new FixedBackOff(1_000L, 3L);

        DefaultErrorHandler errorHandler = new DefaultErrorHandler(recoverer, backOff);
        
        // 비즈니스 예외는 재시도하지 않음 (재시도해도 결과 동일)
        errorHandler.addNotRetryableExceptions(IllegalStateException.class);
        return errorHandler;
    }

    // ─── Listener Container Factory ──────────────────────────────────────

    @Bean("ch04KafkaListenerContainerFactory")
    public ConcurrentKafkaListenerContainerFactory<String, Object> ch04KafkaListenerContainerFactory(
            @Qualifier("ch04ConsumerFactory") ConsumerFactory<String, Object> consumerFactory,
            @Qualifier("ch04KafkaTransactionManager") KafkaTransactionManager<String, Object> txManager,
            @Qualifier("ch04ErrorHandler") DefaultErrorHandler errorHandler,
            @Qualifier("ch04KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate) {
        ConcurrentKafkaListenerContainerFactory<String, Object> factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);

        // 수동 커밋: 리스너에서 ack.acknowledge() 호출 시점에 오프셋 커밋
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);

        // KafkaTransactionManager 연결 → 리스너에서 Kafka TX 자동 시작/커밋
        factory.getContainerProperties().setKafkaAwareTransactionManager(txManager);

        // 블로킹 재시도 + DLT
        factory.setCommonErrorHandler(errorHandler);

        // @SendTo 지원
        factory.setReplyTemplate(kafkaTemplate);
        return factory;
    }
}
