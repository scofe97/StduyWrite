package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.BatchOrderConsumer;
import com.study.redpanda.ch02.producer.OrderProducer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * C3: 배치 Consumer 동작 검증 테스트
 * - batchKafkaListenerContainerFactory로 배치 모드 리스너 동작 확인
 * - 여러 메시지를 전송하면 List<OrderEvent>로 한 번에 수신되는지 검증
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class BatchConsumerTest extends AbstractLocalKafkaTest {

    @Autowired
    private OrderProducer orderProducer;

    @Autowired
    private BatchOrderConsumer batchOrderConsumer;

    private void assertAndLog(String description, Runnable assertion) {
        assertion.run();
        log.info("[PASS] {}", description);
    }

    /** 테스트용 OrderEvent를 생성하는 헬퍼 */
    private OrderEvent createEvent(String orderId, String productName, double price) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName(productName)
                .setQuantity(1)
                .setPrice(price)
                .build();
    }

    // --- C3: 배치 Consumer - 여러 메시지를 List로 수신 ---
    @Test
    void 배치_Consumer가_여러_메시지를_한번에_수신한다() throws Exception {
        int messageCount = 20;
        // 배치가 1회 이상 도착하면 충분 → latch(1)로 설정
        batchOrderConsumer.resetLatch(1);

        // 20건을 빠르게 전송 → poll()에서 한 번에 가져갈 확률을 높인다
        for (int i = 1; i <= messageCount; i++) {
            OrderEvent event = createEvent(
                    "BATCH-" + String.format("%03d", i),
                    "배치상품-" + i,
                    500.0 * i
            );
            orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);
        }

        // 첫 번째 배치가 도착할 때까지 대기
        boolean received = batchOrderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("배치 Consumer가 메시지를 수신해야 한다",
                () -> assertThat(received).isTrue());
        // 배치 모드이므로 lastReceivedBatch는 1건 이상의 리스트
        assertAndLog("배치 크기가 1 이상이어야 한다 (List로 수신)",
                () -> assertThat(batchOrderConsumer.getLastReceivedBatch()).isNotEmpty());
        assertAndLog("수신한 총 이벤트 수가 1 이상이어야 한다",
                () -> assertThat(batchOrderConsumer.getTotalReceivedCount()).isGreaterThanOrEqualTo(1));
        // 배치 내 이벤트의 orderId가 BATCH- 접두사를 가져야 한다
        assertAndLog("배치 내 이벤트의 orderId가 BATCH-로 시작해야 한다",
                () -> assertThat(batchOrderConsumer.getLastReceivedBatch().get(0).getOrderId())
                        .startsWith("BATCH-"));

        log.info("배치 수신 결과: lastBatchSize={}, totalReceived={}",
                batchOrderConsumer.getLastReceivedBatch().size(),
                batchOrderConsumer.getTotalReceivedCount());
    }

    // --- C3: 단일 메시지도 배치(size=1)로 수신됨을 검증 ---
    @Test
    void 단일_메시지도_배치_Consumer는_List로_수신한다() throws Exception {
        batchOrderConsumer.resetLatch(1);

        OrderEvent event = createEvent("BATCH-SINGLE", "단일배치상품", 9999.0);
        orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);

        boolean received = batchOrderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("배치 Consumer가 단일 메시지를 수신해야 한다",
                () -> assertThat(received).isTrue());
        // 1건이지만 여전히 List<OrderEvent>로 전달된다
        assertAndLog("단일 메시지도 List로 수신된다 (size >= 1)",
                () -> assertThat(batchOrderConsumer.getLastReceivedBatch().size()).isGreaterThanOrEqualTo(1));
    }
}
