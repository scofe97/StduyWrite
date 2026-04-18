package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import io.confluent.kafka.serializers.KafkaAvroSerializer;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * I4: Schema Registry 등록 전략 테스트
 *
 * auto.register.schemas=false 상태에서:
 * - 미등록 subject로 전송 시 → RestClientException 발생
 * - 이미 등록된 subject로 전송 시 → 정상 전송
 *
 * 이 테스트는 자체 KafkaTemplate을 생성하여 앱의 기본 설정(auto=true)과 격리한다.
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class SchemaRegistryStrategyTest extends AbstractLocalKafkaTest {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.producer.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("스키마전략테스트")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    /**
     * auto.register.schemas=false로 설정된 KafkaTemplate 생성
     */
    private KafkaTemplate<String, OrderEvent> createManualRegistrationTemplate() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put("auto.register.schemas", false);  // 핵심: 자동 등록 비활성화

        DefaultKafkaProducerFactory<String, OrderEvent> factory =
                new DefaultKafkaProducerFactory<>(props);
        return new KafkaTemplate<>(factory);
    }

    // --- 미등록 subject에 전송 시도 → 실패 ---
    @Test
    void 자동등록_비활성화_시_미등록_스키마로_전송하면_실패한다() {
        KafkaTemplate<String, OrderEvent> template = createManualRegistrationTemplate();

        // 사용된 적 없는 토픽 → Schema Registry에 "i4-unregistered-topic-value" subject가 없음
        String unregisteredTopic = "i4-unregistered-topic-" + UUID.randomUUID().toString().substring(0, 8);

        // Schema Registry에 subject가 없으므로 직렬화 단계에서 실패
        // KafkaAvroSerializer는 send() 호출 시 동기적으로 직렬화하므로
        // Future.get()이 아닌 send() 자체에서 SerializationException이 발생한다
        assertThatThrownBy(() ->
                template.send(unregisteredTopic, "key-1", createEvent("UNREG-001"))
                        .get(10, TimeUnit.SECONDS)
        )
                .isInstanceOfAny(
                        ExecutionException.class,
                        org.apache.kafka.common.errors.SerializationException.class
                )
                .rootCause()
                .isInstanceOf(io.confluent.kafka.schemaregistry.client.rest.exceptions.RestClientException.class);

        log.info("[PASS] auto.register.schemas=false + 미등록 subject → RestClientException 발생");
        log.info("  토픽: {}", unregisteredTopic);
        log.info("  원인: KafkaAvroSerializer가 스키마를 등록하지 않고, Registry에도 없으므로 직렬화 실패");

        template.destroy();
    }

    // --- 이미 등록된 subject에 전송 시도 → 성공 ---
    @Test
    void 자동등록_비활성화_시_이미_등록된_스키마로_전송하면_성공한다() throws Exception {
        // 앱의 기본 KafkaTemplate(auto=true)으로 먼저 한 건 보내서 스키마를 자동 등록시킨다
        // 이렇게 하면 "chapter2.i4-preregistered-value" subject가 Registry에 생긴다
        String topic = "chapter2.i4-preregistered";

        // Step 1: 기본 설정(auto=true)인 앱 KafkaTemplate으로 스키마 사전 등록
        // (실무에서는 CI/CD의 gradlew schemaRegistryRegister가 이 역할)
        KafkaTemplate<String, OrderEvent> autoTemplate = createAutoRegistrationTemplate();
        autoTemplate.send(topic, "pre-key", createEvent("PRE-001")).get(10, TimeUnit.SECONDS);
        log.info("[Step 1] auto=true로 스키마 사전 등록 완료 (실무: CI/CD가 담당)");
        autoTemplate.destroy();

        // Step 2: auto=false 템플릿으로 같은 토픽에 전송 → 스키마가 이미 있으므로 성공
        KafkaTemplate<String, OrderEvent> manualTemplate = createManualRegistrationTemplate();
        var result = manualTemplate.send(topic, "key-1", createEvent("MANUAL-001"))
                .get(10, TimeUnit.SECONDS);

        assertThat(result).isNotNull();
        assertThat(result.getRecordMetadata().topic()).isEqualTo(topic);

        log.info("[PASS] auto.register.schemas=false + 사전 등록된 subject → 정상 전송");
        log.info("  토픽: {}, offset: {}", topic, result.getRecordMetadata().offset());
        log.info("  원리: KafkaAvroSerializer가 Registry에서 스키마 ID를 조회(Read-only)하여 직렬화");

        manualTemplate.destroy();
    }

    /**
     * auto.register.schemas=true로 설정된 KafkaTemplate (스키마 사전 등록용)
     */
    private KafkaTemplate<String, OrderEvent> createAutoRegistrationTemplate() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);
        props.put("schema.registry.url", schemaRegistryUrl);
        props.put("auto.register.schemas", true);

        DefaultKafkaProducerFactory<String, OrderEvent> factory =
                new DefaultKafkaProducerFactory<>(props);
        return new KafkaTemplate<>(factory);
    }
}
