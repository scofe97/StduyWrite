package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * I3: 메시지 키 설계 + P3: 파티션 지정 전송
 *
 * I3: 같은 key → 항상 같은 파티션 (consistent hashing)
 *     null key → round-robin (파티션 골고루 분배)
 *
 * P3: kafkaTemplate.send(topic, partition, key, value)로 파티션 수동 지정
 *
 * chapter2.orders 토픽은 3개 파티션으로 구성되어 있다.
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class PartitionRoutingTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    private void assertAndLog(String description, Runnable assertion) {
        assertion.run();
        log.info("[PASS] {}", description);
    }

    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("파티션테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- I3: 같은 key는 항상 같은 파티션으로 라우팅된다 ---
    @Test
    void 같은_key는_항상_같은_파티션으로_전송된다() throws Exception {
        String sameKey = "ORDER-KEY-001";
        int firstPartition = -1;

        for (int i = 0; i < 5; i++) {
            OrderEvent event = createEvent("KEY-TEST-" + i);
            SendResult<String, OrderEvent> result = kafkaTemplate
                    .send("chapter2.orders", sameKey, event)
                    .get(10, TimeUnit.SECONDS);

            int partition = result.getRecordMetadata().partition();
            log.info("key={}, partition={}, offset={}", sameKey, partition,
                    result.getRecordMetadata().offset());

            if (i == 0) {
                firstPartition = partition;
            }

            final int expectedPartition = firstPartition;
            assertAndLog("메시지 " + i + ": 같은 key → 같은 파티션(" + expectedPartition + ")",
                    () -> assertThat(partition).isEqualTo(expectedPartition));
        }
    }

    // --- I3: 다른 key는 다른 파티션으로 분산될 수 있다 ---
    @Test
    void 다른_key는_파티션이_분산된다() throws Exception {
        Map<String, Integer> keyPartitionMap = new HashMap<>();

        // 10개의 서로 다른 key로 전송
        for (int i = 0; i < 10; i++) {
            String key = "DIST-KEY-" + i;
            OrderEvent event = createEvent("DIST-" + i);
            SendResult<String, OrderEvent> result = kafkaTemplate
                    .send("chapter2.orders", key, event)
                    .get(10, TimeUnit.SECONDS);

            int partition = result.getRecordMetadata().partition();
            keyPartitionMap.put(key, partition);
            log.info("key={}, partition={}", key, partition);
        }

        // 3개 파티션 중 최소 2개 이상에 분산되어야 함
        long distinctPartitions = keyPartitionMap.values().stream().distinct().count();
        assertAndLog("10개 key가 최소 2개 이상 파티션에 분산 (실제: " + distinctPartitions + ")",
                () -> assertThat(distinctPartitions).isGreaterThanOrEqualTo(2));
    }

    // --- P3: 파티션을 수동으로 지정하여 전송 ---
    @Test
    void 파티션을_수동_지정하면_해당_파티션에_저장된다() throws Exception {
        // chapter2.orders는 3개 파티션 (0, 1, 2)
        for (int targetPartition = 0; targetPartition < 3; targetPartition++) {
            OrderEvent event = createEvent("PART-" + targetPartition);

            // send(topic, partition, key, value) — partition을 명시적으로 지정
            SendResult<String, OrderEvent> result = kafkaTemplate
                    .send("chapter2.orders", targetPartition, event.getOrderId(), event)
                    .get(10, TimeUnit.SECONDS);

            int actualPartition = result.getRecordMetadata().partition();
            log.info("target={}, actual={}, offset={}", targetPartition, actualPartition,
                    result.getRecordMetadata().offset());

            final int expected = targetPartition;
            assertAndLog("파티션 " + targetPartition + "으로 정확히 전송됨",
                    () -> assertThat(actualPartition).isEqualTo(expected));
        }
    }

    // --- P3: 파티션 수동 지정 시 key의 해시는 무시된다 ---
    @Test
    void 파티션_수동_지정_시_key_해시는_무시된다() throws Exception {
        String key = "SAME-KEY";

        // 같은 key인데 파티션 0, 1, 2로 각각 전송
        for (int targetPartition = 0; targetPartition < 3; targetPartition++) {
            OrderEvent event = createEvent("OVERRIDE-" + targetPartition);
            SendResult<String, OrderEvent> result = kafkaTemplate
                    .send("chapter2.orders", targetPartition, key, event)
                    .get(10, TimeUnit.SECONDS);

            int actualPartition = result.getRecordMetadata().partition();

            final int expected = targetPartition;
            assertAndLog("key=" + key + "이지만 파티션 " + targetPartition + "으로 강제 전송",
                    () -> assertThat(actualPartition).isEqualTo(expected));
        }
    }
}
