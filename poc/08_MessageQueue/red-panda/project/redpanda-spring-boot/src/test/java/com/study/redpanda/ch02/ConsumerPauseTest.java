package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.PausableConsumer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.MessageListenerContainer;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static java.util.concurrent.TimeUnit.SECONDS;
import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

/**
 * C7: Consumer Pause 테스트
 *
 * pause(): poll()은 계속 호출되지만 메시지를 가져오지 않음
 *          → 리밸런싱 없이 파티션 소유권 유지
 * resume(): 다시 메시지를 가져옴 → 즉시 재개 (리밸런싱 불필요)
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class ConsumerPauseTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private PausableConsumer pausableConsumer;

    @Autowired
    private KafkaListenerEndpointRegistry registry;

    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("Pause테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- pause 상태에서 메시지가 소비되지 않고, resume 후 소비된다 ---
    @Test
    void pause하면_메시지를_소비하지_않고_resume하면_재개된다() throws Exception {
        // Step 1: 정상 상태에서 메시지 소비 확인
        pausableConsumer.reset(1);
        kafkaTemplate.send("chapter2.pause-test", "key-1", createEvent("PAUSE-001"))
                .get(10, TimeUnit.SECONDS);

        boolean received = pausableConsumer.getLatch().await(10, TimeUnit.SECONDS);
        assertThat(received).isTrue();
        assertThat(pausableConsumer.getReceivedCount().get()).isEqualTo(1);
        log.info("[PASS] Step 1: 정상 상태에서 메시지 소비 확인");

        // Step 2: pause → 메시지 전송 → 소비되지 않음
        MessageListenerContainer container = registry.getListenerContainer("pausable-listener");
        assertThat(container).isNotNull();
        container.pause();
        log.info("Consumer paused. isPauseRequested={}", container.isPauseRequested());

        // pause가 다음 poll() 사이클에서 적용될 때까지 대기 (Thread.sleep 대신 조건 기반)
        await().atMost(10, SECONDS)
                .until(container::isContainerPaused);

        pausableConsumer.reset(1);
        kafkaTemplate.send("chapter2.pause-test", "key-2", createEvent("PAUSE-002"))
                .get(10, TimeUnit.SECONDS);

        // 3초 대기 — pause 상태이므로 소비되지 않아야 함
        boolean notReceived = pausableConsumer.getLatch().await(3, TimeUnit.SECONDS);
        assertThat(notReceived).isFalse();
        assertThat(pausableConsumer.getReceivedCount().get()).isEqualTo(0);
        log.info("[PASS] Step 2: pause 상태에서 메시지 미소비 확인");

        // Step 3: resume → 밀린 메시지가 소비됨
        container.resume();
        log.info("Consumer resumed");

        boolean resumeReceived = pausableConsumer.getLatch().await(10, TimeUnit.SECONDS);
        assertThat(resumeReceived).isTrue();
        assertThat(pausableConsumer.getLastReceivedEvent().getOrderId()).isEqualTo("PAUSE-002");
        log.info("[PASS] Step 3: resume 후 밀린 메시지 즉시 소비 확인");
    }
}
