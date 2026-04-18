package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.IdempotentConsumer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * C9: Idempotent Consumer 동작 검증 테스트
 * - 같은 eventId로 2번 전송 → 1회만 처리 (중복 skip)
 * - 다른 eventId로 2번 전송 → 2회 모두 처리
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class IdempotentConsumerTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private IdempotentConsumer idempotentConsumer;

    private void assertAndLog(String description, Runnable assertion) {
        assertion.run();
        log.info("[PASS] {}", description);
    }

    private OrderEvent createEvent(String eventId, String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(eventId)
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("멱등성테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- C9: 같은 eventId 2번 전송 → 1회만 처리 ---
    @Test
    void 같은_eventId로_2번_전송하면_1회만_처리된다() throws Exception {
        // latch(2): Consumer가 2번 호출될 때까지 대기 (처리 + skip 모두 countDown)
        idempotentConsumer.resetLatch(2);

        String sameEventId = UUID.randomUUID().toString();
        OrderEvent event1 = createEvent(sameEventId, "IDEM-001");
        OrderEvent event2 = createEvent(sameEventId, "IDEM-001");

        kafkaTemplate.send("chapter2.idempotent-test", event1.getOrderId(), event1)
                .get(10, TimeUnit.SECONDS);
        kafkaTemplate.send("chapter2.idempotent-test", event2.getOrderId(), event2)
                .get(10, TimeUnit.SECONDS);

        boolean allReceived = idempotentConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 2건 모두 수신해야 한다",
                () -> assertThat(allReceived).isTrue());
        assertAndLog("실제 처리 횟수는 1이어야 한다 (중복 제거)",
                () -> assertThat(idempotentConsumer.getProcessedCount().get()).isEqualTo(1));
        assertAndLog("중복 skip 횟수는 1이어야 한다",
                () -> assertThat(idempotentConsumer.getDuplicateCount().get()).isEqualTo(1));
    }

    // --- C9: 다른 eventId 2번 전송 → 2회 모두 처리 ---
    @Test
    void 다른_eventId로_2번_전송하면_모두_처리된다() throws Exception {
        idempotentConsumer.resetLatch(2);

        OrderEvent event1 = createEvent(UUID.randomUUID().toString(), "IDEM-002");
        OrderEvent event2 = createEvent(UUID.randomUUID().toString(), "IDEM-003");

        kafkaTemplate.send("chapter2.idempotent-test", event1.getOrderId(), event1)
                .get(10, TimeUnit.SECONDS);
        kafkaTemplate.send("chapter2.idempotent-test", event2.getOrderId(), event2)
                .get(10, TimeUnit.SECONDS);

        boolean allReceived = idempotentConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 2건 모두 수신해야 한다",
                () -> assertThat(allReceived).isTrue());
        assertAndLog("실제 처리 횟수는 2여야 한다 (서로 다른 eventId)",
                () -> assertThat(idempotentConsumer.getProcessedCount().get()).isEqualTo(2));
        assertAndLog("중복 skip 횟수는 0이어야 한다",
                () -> assertThat(idempotentConsumer.getDuplicateCount().get()).isEqualTo(0));
    }
}
