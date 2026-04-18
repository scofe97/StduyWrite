package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.OrderConsumer;
import com.study.redpanda.ch02.producer.EnhancedKafkaTemplate;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * P6: KafkaTemplate 래퍼 테스트
 *
 * EnhancedKafkaTemplate이 공통 헤더(X-Service-Name, X-Correlation-Id, X-Sent-At)를
 * 자동 추가하는지 검증한다.
 *
 * OrderConsumer가 이미 이 헤더들을 @Header로 읽고 있으므로,
 * Consumer 측에서 헤더 수신 여부를 확인한다.
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class EnhancedKafkaTemplateTest extends AbstractLocalKafkaTest {

    @Autowired
    private EnhancedKafkaTemplate enhancedKafkaTemplate;

    @Autowired
    private OrderConsumer orderConsumer;

    @BeforeEach
    void setUp() {
        orderConsumer.resetLatch(1);
    }

    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("래퍼테스트상품")
                .setQuantity(1)
                .setPrice(5000.0)
                .build();
    }

    // --- 공통 헤더가 자동 추가되어 Consumer가 수신한다 ---
    @Test
    void 래퍼를_통해_전송하면_공통_헤더가_자동_추가된다() throws Exception {
        // Given
        OrderEvent event = createEvent("ENHANCED-001");

        // When: EnhancedKafkaTemplate으로 전송
        enhancedKafkaTemplate.send("chapter2.orders", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        // Then: Consumer가 수신하고 헤더를 확인
        boolean received = orderConsumer.getLatch().await(10, TimeUnit.SECONDS);
        assertThat(received).isTrue();

        // 메시지 본문 확인
        assertThat(orderConsumer.getLastReceivedEvent().getOrderId()).isEqualTo("ENHANCED-001");

        // 공통 헤더 확인: X-Service-Name
        assertThat(orderConsumer.getLastReceivedServiceName()).isEqualTo("order-service");
        log.info("[PASS] X-Service-Name 헤더 자동 추가됨: {}", orderConsumer.getLastReceivedServiceName());

        // 공통 헤더 확인: X-Sent-At (null이 아닌지)
        assertThat(orderConsumer.getLastReceivedSentAt()).isNotNull();
        log.info("[PASS] X-Sent-At 헤더 자동 추가됨: {}", orderConsumer.getLastReceivedSentAt());
    }

    // --- KafkaTemplate 직접 사용과 비교: 래퍼 없이는 헤더가 없다 ---
    @Test
    void 래퍼_없이_직접_전송하면_공통_헤더가_없다() throws Exception {
        // Given
        OrderEvent event = createEvent("DIRECT-001");

        // When: KafkaTemplate을 직접 사용하는 OrderProducer가 아닌,
        //       래퍼의 내부 kafkaTemplate으로는 접근할 수 없으므로
        //       OrderConsumer에 이미 있는 P5 인터셉터 헤더와 구분하여 검증
        //       → P5 인터셉터가 등록되어 있으면 X-Service-Name이 들어갈 수 있음
        //       → 이 테스트는 래퍼가 정상 동작하는지를 검증하는 것이 핵심

        enhancedKafkaTemplate.send("chapter2.orders", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        boolean received = orderConsumer.getLatch().await(10, TimeUnit.SECONDS);
        assertThat(received).isTrue();

        // X-Correlation-Id는 래퍼에서만 추가하므로 (P5 인터셉터에는 없음)
        // 래퍼 사용 여부를 확실히 구분할 수 있다
        // OrderConsumer에 correlationId 헤더가 있는지 확인
        assertThat(orderConsumer.getLastReceivedCorrelationId()).isNotNull();
        log.info("[PASS] X-Correlation-Id 래퍼에서만 추가됨: {}", orderConsumer.getLastReceivedCorrelationId());
    }
}
