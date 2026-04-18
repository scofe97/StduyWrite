package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.RetryableConsumer;
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
 * C6: @RetryableTopic 논블록킹 재시도 검증 테스트
 *
 * C5(DefaultErrorHandler)와의 비교:
 * - C5: Consumer 메모리에서 재시도 → 토픽에 메시지 1건만 존재
 * - C6: 재시도 토픽으로 메시지 이동 → retry-0, retry-1 토픽에 각각 1건씩 적재
 *
 * 재시도 흐름:
 * retryable-test → retryable-test-retry-0 (1초) → retryable-test-retry-1 (2초) → retryable-test-dlt
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class RetryableTopicTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private RetryableConsumer retryableConsumer;

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
                .setProductName("재시도테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- C6: 재시도 소진 후 DLT로 전송됨을 검증 ---
    @Test
    void 재시도_소진_후_DLT로_전송된다_논블록킹() throws Exception {
        retryableConsumer.reset(true);

        OrderEvent event = createEvent("RETRY-001");
        kafkaTemplate.send("chapter2.retryable-test", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        // @RetryableTopic: 1초(retry-0) + 2초(retry-1) + 여유 = 충분한 대기
        boolean dltReceived = retryableConsumer.getDltLatch().await(30, TimeUnit.SECONDS);

        // 총 시도 횟수: 1회 원본 + 2회 재시도 = 3회
        assertAndLog("총 시도 횟수가 3이어야 한다 (1회 원본 + 2회 재시도)",
                () -> assertThat(retryableConsumer.getAttemptCount().get()).isEqualTo(3));
        assertAndLog("DLT Consumer가 메시지를 수신해야 한다",
                () -> assertThat(dltReceived).isTrue());
        assertAndLog("DLT 메시지의 orderId가 원본과 일치해야 한다",
                () -> assertThat(retryableConsumer.getLastDltEvent().getOrderId()).isEqualTo("RETRY-001"));
    }

    // --- C6: 정상 처리 시 재시도 토픽을 거치지 않음을 검증 ---
    @Test
    void 정상_처리_시_재시도_토픽을_거치지_않는다() throws Exception {
        retryableConsumer.reset(false);

        OrderEvent event = createEvent("RETRY-OK-001");
        kafkaTemplate.send("chapter2.retryable-test", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        boolean success = retryableConsumer.getSuccessLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("정상 처리가 완료되어야 한다",
                () -> assertThat(success).isTrue());
        assertAndLog("시도 횟수가 1이어야 한다 (재시도 없음)",
                () -> assertThat(retryableConsumer.getAttemptCount().get()).isEqualTo(1));
    }
}
