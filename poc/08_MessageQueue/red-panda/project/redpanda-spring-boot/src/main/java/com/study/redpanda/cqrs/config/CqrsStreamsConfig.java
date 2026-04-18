package com.study.redpanda.cqrs.config;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafkaStreams;
import org.springframework.kafka.annotation.KafkaStreamsDefaultConfiguration;
import org.springframework.kafka.config.KafkaStreamsConfiguration;

import java.util.HashMap;
import java.util.Map;

/**
 * CQRS Query Side 전용 Kafka Streams 설정
 *
 * @EnableKafkaStreams를 선언하여 StreamsBuilder 빈과
 * StreamsBuilderFactoryBean을 자동 등록한다.
 *
 * DEFAULT_STREAMS_CONFIG_BEAN_NAME("defaultKafkaStreamsConfig") 빈을
 * 제공하면 Spring Kafka가 이 설정으로 KafkaStreams 인스턴스를 생성한다.
 *
 * Command Side(CqrsKafkaConfig)의 ProducerFactory/KafkaTemplate과
 * 독립적인 설정이므로 기존 ch02~ch04 코드에 영향을 주지 않는다.
 */
@Configuration
@EnableKafkaStreams
public class CqrsStreamsConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.producer.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    /**
     * Kafka Streams 기본 설정 빈
     *
     * Spring Kafka는 이 빈 이름(DEFAULT_STREAMS_CONFIG_BEAN_NAME)을 찾아
     * KafkaStreams 인스턴스를 생성한다.
     *
     * APPLICATION_ID_CONFIG는 Kafka Streams 앱의 고유 식별자이며,
     * Consumer Group ID와 내부 토픽(changelog, repartition) 접두사로도 사용된다.
     *
     * AUTO_OFFSET_RESET = earliest: Event Store는 처음 기동 시
     * 모든 이벤트를 처음부터 읽어 State Store를 재구성해야 한다.
     */
    @Bean(name = KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
    public KafkaStreamsConfiguration kStreamsConfig() {
        Map<String, Object> props = new HashMap<>();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "cqrs-social-streams");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);

        // Avro SpecificRecord 역직렬화를 위한 Schema Registry 설정
        props.put("schema.registry.url", schemaRegistryUrl);

        // specific.avro.reader=true: GenericRecord 대신 생성된 SpecificRecord 클래스로 역직렬화
        props.put("specific.avro.reader", true);

        // Event Store는 처음부터 읽어 State Store를 재구성해야 한다
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        return new KafkaStreamsConfiguration(props);
    }
}
