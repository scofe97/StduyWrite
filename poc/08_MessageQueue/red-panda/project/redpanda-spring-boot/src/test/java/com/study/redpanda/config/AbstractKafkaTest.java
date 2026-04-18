package com.study.redpanda.config;

import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.redpanda.RedpandaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

/**
 * Testcontainers 기반 Kafka + Avro 테스트 공통 설정
 *
 * Redpanda 컨테이너가 Kafka API와 Schema Registry를 모두 제공합니다.
 * 별도 Schema Registry 컨테이너가 불필요합니다.
 */
@Testcontainers
public abstract class AbstractKafkaTest {

    @Container
    static final RedpandaContainer REDPANDA = new RedpandaContainer(
            "docker.redpanda.com/redpandadata/redpanda:v25.3.6"
    );

    @DynamicPropertySource
    static void overrideProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", REDPANDA::getBootstrapServers);
        registry.add("spring.kafka.consumer.properties.schema.registry.url",
                () -> REDPANDA.getSchemaRegistryAddress());
        registry.add("spring.kafka.producer.properties.schema.registry.url",
                () -> REDPANDA.getSchemaRegistryAddress());
    }
}
