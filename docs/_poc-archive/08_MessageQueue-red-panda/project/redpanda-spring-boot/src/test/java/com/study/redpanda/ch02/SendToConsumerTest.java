package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.SendToConsumer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.BeforeEach;
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
 * C4: @SendTo 기반 파이프라인 테스트
 *
 * 1. 정상 파이프라인: input → 가공(ORDER_PROCESSED) → output
 * 2. null 반환 필터링: ORDER_CANCELLED → null → output에 전송 안 됨
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class SendToConsumerTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private SendToConsumer sendToConsumer;

    @BeforeEach
    void setUp() {
        sendToConsumer.reset(1, 1);
    }

    private OrderEvent createEvent(String orderId, String eventType) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType(eventType)
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("파이프라인테스트상품")
                .setQuantity(1)
                .setPrice(10000.0)
                .build();
    }

    // --- 정상 파이프라인: input → ORDER_PROCESSED로 변환 → output ---
    @Test
    void 정상_메시지는_가공되어_output_토픽으로_전달된다() throws Exception {
        // Given
        OrderEvent event = createEvent("SENDTO-001", "ORDER_CREATED");

        // When
        kafkaTemplate.send("chapter2.sendto-input", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        // Then: input Consumer가 수신
        boolean inputReceived = sendToConsumer.getInputLatch().await(10, TimeUnit.SECONDS);
        assertThat(inputReceived).isTrue();
        assertThat(sendToConsumer.getLastInputEvent().getOrderId()).isEqualTo("SENDTO-001");
        assertThat(sendToConsumer.getLastInputEvent().getEventType()).isEqualTo("ORDER_CREATED");

        // Then: output Consumer가 가공된 메시지 수신
        boolean outputReceived = sendToConsumer.getOutputLatch().await(10, TimeUnit.SECONDS);
        assertThat(outputReceived).isTrue();
        assertThat(sendToConsumer.getLastOutputEvent().getOrderId()).isEqualTo("SENDTO-001");
        assertThat(sendToConsumer.getLastOutputEvent().getEventType()).isEqualTo("ORDER_PROCESSED");

        log.info("[PASS] 정상 파이프라인: ORDER_CREATED → ORDER_PROCESSED 변환 후 output 토픽 전달");
    }

    // --- null 반환 필터링: ORDER_CANCELLED → output에 전달되지 않음 ---
    @Test
    void 취소_이벤트는_null_반환으로_output_토픽에_전달되지_않는다() throws Exception {
        // Given
        sendToConsumer.reset(1, 1);  // output latch는 카운트다운되지 않을 것
        OrderEvent event = createEvent("SENDTO-002", "ORDER_CANCELLED");

        // When
        kafkaTemplate.send("chapter2.sendto-input", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        // Then: input Consumer가 수신
        boolean inputReceived = sendToConsumer.getInputLatch().await(10, TimeUnit.SECONDS);
        assertThat(inputReceived).isTrue();
        assertThat(sendToConsumer.getLastInputEvent().getEventType()).isEqualTo("ORDER_CANCELLED");

        // Then: output Consumer는 수신하지 않음 (3초 대기 후 타임아웃)
        boolean outputReceived = sendToConsumer.getOutputLatch().await(3, TimeUnit.SECONDS);
        assertThat(outputReceived).isFalse();
        assertThat(sendToConsumer.getLastOutputEvent()).isNull();

        log.info("[PASS] 필터링: ORDER_CANCELLED → null 반환 → output 토픽 미전달");
    }
}
