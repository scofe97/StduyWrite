package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.producer.OrderProducer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.SendResult;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * P7: Idempotent Producer 설정 검증 테스트
 *
 * Idempotent Producer는 브로커 레벨에서 PID+시퀀스로 중복을 감지한다.
 * 네트워크 재시도로 인한 중복만 방어하며, 앱 레벨 재전송은 방어하지 못한다.
 *
 * 필수 조건: acks=all, enable.idempotence=true, max.in.flight ≤ 5
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class IdempotentProducerTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private OrderProducer orderProducer;

    @Autowired
    private ProducerFactory<String, OrderEvent> producerFactory;

    private void assertAndLog(String description, Runnable assertion) {
        assertion.run();
        log.info("[PASS] {}", description);
    }

    // --- P7: Idempotent Producer 설정이 활성화되어 있는지 검증 ---
    @Test
    void Idempotent_Producer_설정이_활성화되어_있다() {
        Map<String, Object> configs = producerFactory.getConfigurationProperties();

        // enable.idempotence=true 확인
        Object idempotence = configs.get(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG);
        assertAndLog("enable.idempotence가 true여야 한다",
                () -> assertThat(idempotence).isNotNull());
        assertAndLog("enable.idempotence 값 확인",
                () -> assertThat(idempotence.toString()).isEqualTo("true"));

        // acks=all 확인 (idempotence 필수 조건)
        Object acks = configs.get(ProducerConfig.ACKS_CONFIG);
        assertAndLog("acks가 all(-1)이어야 한다 (idempotence 필수)",
                () -> assertThat(acks).isNotNull());

        // max.in.flight.requests.per.connection ≤ 5 확인
        Object maxInFlight = configs.get(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION);
        assertAndLog("max.in.flight.requests.per.connection이 5 이하여야 한다",
                () -> assertThat(Integer.parseInt(maxInFlight.toString())).isLessThanOrEqualTo(5));

        log.info("Idempotent Producer 설정: idempotence={}, acks={}, maxInFlight={}",
                idempotence, acks, maxInFlight);
    }

    // --- P7: Idempotent Producer로 전송 시 정상 동작 검증 ---
    @Test
    void Idempotent_Producer로_메시지를_정상_전송한다() throws Exception {
        OrderEvent event = OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId("IDEM-P-001")
                .setProductName("멱등성Producer상품")
                .setQuantity(1)
                .setPrice(5000.0)
                .build();

        SendResult<String, OrderEvent> result =
                orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);

        assertAndLog("토픽이 chapter2.orders여야 한다",
                () -> assertThat(result.getRecordMetadata().topic()).isEqualTo("chapter2.orders"));
        assertAndLog("offset이 0 이상이어야 한다",
                () -> assertThat(result.getRecordMetadata().offset()).isGreaterThanOrEqualTo(0));

        log.info("Idempotent Producer 전송 성공: partition={}, offset={}",
                result.getRecordMetadata().partition(),
                result.getRecordMetadata().offset());
    }
}
