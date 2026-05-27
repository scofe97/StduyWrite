package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.CircuitBreakerConsumer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
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
 * C8: Circuit Breaker 연동 테스트
 *
 * 외부 서비스 장애 시 Circuit Breaker가 OPEN되어 즉시 실패하는 것을 검증한다.
 * OPEN 상태에서는 블로킹이 없으므로 poll() 간격 유지 → 리밸런싱 방지.
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class CircuitBreakerConsumerTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private CircuitBreakerConsumer circuitBreakerConsumer;

    @BeforeEach
    void setUp() {
        circuitBreakerConsumer.reset(0, 0);
        // CircuitBreaker 상태 초기화
        circuitBreakerConsumer.getCircuitBreaker().reset();
    }

    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("서킷테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- 정상 상태: 외부 서비스 OK → 처리 성공 ---
    @Test
    void 정상_상태에서_메시지가_성공적으로_처리된다() throws Exception {
        circuitBreakerConsumer.reset(1, 0);
        circuitBreakerConsumer.setExternalServiceDown(false);

        kafkaTemplate.send("chapter2.circuit-test", "key-1", createEvent("CB-OK-001"))
                .get(10, TimeUnit.SECONDS);

        boolean received = circuitBreakerConsumer.getSuccessLatch().await(10, TimeUnit.SECONDS);
        assertThat(received).isTrue();
        assertThat(circuitBreakerConsumer.getSuccessCount().get()).isEqualTo(1);
        assertThat(circuitBreakerConsumer.getCircuitBreaker().getState())
                .isEqualTo(CircuitBreaker.State.CLOSED);

        log.info("[PASS] 정상 상태: CLOSED, 처리 성공");
    }

    // --- 장애 시: 연속 실패 → Circuit OPEN → 즉시 실패 ---
    @Test
    void 연속_실패_시_서킷이_열리고_즉시_실패한다() throws Exception {
        // slidingWindowSize=4, failureRateThreshold=50% → 4건 중 2건 이상 실패 시 OPEN
        // 4건 모두 실패시키면 확실히 OPEN
        circuitBreakerConsumer.reset(0, 6);  // 최소 4건 실패 + OPEN 후 추가 2건
        circuitBreakerConsumer.setExternalServiceDown(true);

        // 6건 전송: 4건으로 OPEN 트리거, 나머지 2건은 OPEN 상태에서 즉시 실패
        for (int i = 0; i < 6; i++) {
            kafkaTemplate.send("chapter2.circuit-test", "key-" + i,
                    createEvent("CB-FAIL-" + i)).get(10, TimeUnit.SECONDS);
        }

        boolean allFailed = circuitBreakerConsumer.getFailureLatch().await(15, TimeUnit.SECONDS);
        assertThat(allFailed).isTrue();

        // Circuit이 OPEN 상태로 전환됨
        assertThat(circuitBreakerConsumer.getCircuitBreaker().getState())
                .isEqualTo(CircuitBreaker.State.OPEN);

        // 6건 모두 실패, 성공 0건 — 예외 타입에 관계없이 전부 실패 경로
        assertThat(circuitBreakerConsumer.getFailureCount().get()).isEqualTo(6);
        assertThat(circuitBreakerConsumer.getSuccessCount().get()).isEqualTo(0);

        // OPEN 상태에서 CallNotPermittedException으로 즉시 차단된 건수
        assertThat(circuitBreakerConsumer.getCircuitOpenCount().get()).isGreaterThan(0);

        log.info("[PASS] 장애 시: Circuit OPEN, 즉시 차단 {}건 (CallNotPermittedException)",
                circuitBreakerConsumer.getCircuitOpenCount().get());
        log.info("  총 실패: {}건, 성공: {}건",
                circuitBreakerConsumer.getFailureCount().get(),
                circuitBreakerConsumer.getSuccessCount().get());
    }
}
