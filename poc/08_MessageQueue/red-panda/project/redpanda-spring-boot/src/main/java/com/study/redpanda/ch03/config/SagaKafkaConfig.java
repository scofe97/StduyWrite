package com.study.redpanda.ch03.config;

import io.confluent.kafka.serializers.KafkaAvroDeserializer;
import io.confluent.kafka.serializers.KafkaAvroDeserializerConfig;
import io.confluent.kafka.serializers.KafkaAvroSerializer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
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
 * ch03 SAGA 전용 Kafka 트랜잭션 설정
 *
 * ch02(비트랜잭션)와 분리하여 ch03 전용 빈을 구성한다:
 *
 * 1. Transactional ProducerFactory: transactional.id로 원자적 메시지 발행
 * 2. KafkaTemplate: 트랜잭션 ProducerFactory 사용
 * 3. KafkaTransactionManager: 리스너 컨테이너가 Kafka TX를 시작/커밋하도록 연결
 * 4. ConsumerFactory: isolation.level=read_committed (커밋된 메시지만 읽음)
 * 5. ListenerContainerFactory: KafkaTransactionManager + read_committed Consumer
 *
 * 주의: JPA 트랜잭션(@Transactional)과 Kafka 트랜잭션은 독립적으로 동작한다.
 * DB 커밋 후 Kafka 커밋이 실패하면 불일치가 발생할 수 있다.
 * 프로덕션에서는 Transactional Outbox 패턴이 완전한 원자성을 보장하는 표준 방법이다.
 */
@Configuration
public class SagaKafkaConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.producer.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    @Value("${spring.kafka.producer.properties.auto.register.schemas:true}")
    private boolean autoRegisterSchemas;

    // ─── Transactional Producer ──────────────────────────────────────────

    @Bean("ch03ProducerFactory")
    public ProducerFactory<String, Object> ch03ProducerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put("auto.register.schemas", autoRegisterSchemas);

        // Kafka 트랜잭션 필수 설정
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);   // PID+시퀀스로 중복 방지
        props.put(ProducerConfig.ACKS_CONFIG, "all");                // 모든 ISR 브로커 확인
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);

        // ch02 CommonHeaderInterceptor 재사용 (관측성 일관성)
        props.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,
                "com.study.redpanda.ch02.interceptor.CommonHeaderInterceptor");

        DefaultKafkaProducerFactory<String, Object> factory = new DefaultKafkaProducerFactory<>(props);
        factory.setTransactionIdPrefix("saga-tx-");  // 트랜잭션 활성화 (인스턴스별 고유 접두사)
        return factory;
    }

    @Bean("ch03KafkaTemplate")
    public KafkaTemplate<String, Object> ch03KafkaTemplate(
            @Qualifier("ch03ProducerFactory") ProducerFactory<String, Object> producerFactory) {
        return new KafkaTemplate<>(producerFactory);
    }

    // ─── Kafka Transaction Manager ───────────────────────────────────────

    /**
     * 리스너 컨테이너가 Kafka 트랜잭션을 시작/커밋하도록 연결한다.
     * 이 매니저가 없으면 send()마다 개별 미니 트랜잭션이 생성되고,
     * Consumer 오프셋이 Kafka TX에 포함되지 않아 exactly-once가 불완전하다.
     *
     * 이 매니저가 있으면:
     * - 리스너가 메시지를 받을 때 Kafka TX 시작
     * - 리스너 내 모든 send()가 같은 TX에 포함
     * - 리스너 정상 반환 → TX 커밋 + 오프셋 커밋 (sendOffsetsToTransaction)
     * - 예외 발생 → TX abort + 오프셋 미커밋 → 재전달
     */
    @Bean("ch03KafkaTransactionManager")
    public KafkaTransactionManager<String, Object> ch03KafkaTransactionManager(
            @Qualifier("ch03ProducerFactory") ProducerFactory<String, Object> producerFactory) {
        return new KafkaTransactionManager<>(producerFactory);
    }

    // ─── Read-Committed Consumer ─────────────────────────────────────────

    @Bean("ch03ConsumerFactory")
    public ConsumerFactory<String, Object> ch03ConsumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

        // 트랜잭션 사용 시 필수: 커밋된 메시지만 읽음
        // read_uncommitted(기본값): abort된 메시지도 보임 → 데이터 불일치
        // read_committed: commitTransaction() 완료된 메시지만 보임 → 원자성 보장
        props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");

        return new DefaultKafkaConsumerFactory<>(props);
    }

    // ─── Error Handler + Dead Letter Topic ─────────────────────────────

    /**
     * 블로킹 재시도 + DLT (Dead Letter Topic) 에러 핸들러
     *
     * @RetryableTopic(논블로킹 재시도)는 KafkaTransactionManager와 공식 비호환이므로,
     * 트랜잭션 환경에서는 DefaultErrorHandler(블로킹 재시도)를 사용한다.
     *
     * 동작 방식:
     * - 리스너에서 예외 발생 → 같은 스레드에서 즉시 재시도 (블로킹)
     * - 재시도 횟수 소진 → DeadLetterPublishingRecoverer가 DLT로 메시지 전송
     * - DLT 토픽명: {원본토픽}.DLT (Spring Kafka 기본 규칙)
     *
     * 재시도 대상 제외 (재시도해도 결과 동일한 예외):
     * - IllegalStateException: 재고 부족, 엔티티 미존재 등 비즈니스 규칙 위반
     *
     * 프로덕션 권장:
     * - ExponentialBackOff + Jitter (Thundering Herd 방지)
     * - 보상 리스너 전용 ContainerFactory (더 많은 재시도 + 엄격한 DLT 알림)
     * - DLT 컨슈머에서 알림 발송 (Slack/PagerDuty)
     */
    @Bean("ch03ErrorHandler")
    public DefaultErrorHandler ch03ErrorHandler(
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate) {
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate);
        // 3회 재시도, 1초 간격 (학습용 간단 설정)
        FixedBackOff backOff = new FixedBackOff(1_000L, 3L);

        DefaultErrorHandler errorHandler = new DefaultErrorHandler(recoverer, backOff);
        // 비즈니스 예외는 재시도하지 않음 (재시도해도 결과 동일)
        errorHandler.addNotRetryableExceptions(IllegalStateException.class);
        return errorHandler;
    }

    // ─── Listener Container Factory ──────────────────────────────────────

    @Bean("ch03KafkaListenerContainerFactory")
    public ConcurrentKafkaListenerContainerFactory<String, Object> ch03KafkaListenerContainerFactory(
            @Qualifier("ch03ConsumerFactory") ConsumerFactory<String, Object> consumerFactory,
            @Qualifier("ch03KafkaTransactionManager") KafkaTransactionManager<String, Object> txManager,
            @Qualifier("ch03ErrorHandler") DefaultErrorHandler errorHandler,
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate) {
        ConcurrentKafkaListenerContainerFactory<String, Object> factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        // 수동 커밋: 리스너에서 ack.acknowledge() 호출 시점에 오프셋 커밋
        // KafkaTransactionManager와 함께 사용하면 ack 호출이 트랜잭션 커밋 시 오프셋에 포함됨
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);

        // KafkaTransactionManager 연결 → 리스너에서 Kafka TX 자동 시작/커밋
        factory.getContainerProperties().setKafkaAwareTransactionManager(txManager);

        // 블로킹 재시도 + DLT: 재시도 소진 시 DLT로 메시지 전송
        factory.setCommonErrorHandler(errorHandler);

        // @SendTo 지원: 리스너 반환값을 자동으로 지정 토픽에 전송하는 데 사용
        // @SendTo를 사용하지 않는 리스너에는 영향 없음
        factory.setReplyTemplate(kafkaTemplate);
        return factory;
    }
}
