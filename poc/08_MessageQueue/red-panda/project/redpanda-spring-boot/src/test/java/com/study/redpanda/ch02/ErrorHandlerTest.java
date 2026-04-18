package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.ErrorProneConsumer;
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
 * C5: DefaultErrorHandler + DLT 동작 검증 테스트
 * - 재시도 횟수 검증 (BackOff: 1초 x 2회 = 총 3회 시도)
 * - 재시도 소진 후 DLT 전송 검증
 * - 정상 처리 시 에러 핸들러 미개입 검증
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class ErrorHandlerTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private ErrorProneConsumer errorProneConsumer;

    private void assertAndLog(String description, Runnable assertion) {
        assertion.run();
        log.info("[PASS] {}", description);
    }

    /** 테스트용 OrderEvent 생성 헬퍼 */
    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("에러테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- C5: 재시도 소진 후 DLT로 전송됨을 검증 ---
    @Test
    void 재시도_소진_후_DLT로_전송된다() throws Exception {
        // shouldFail=true → 모든 시도에서 예외 발생
        errorProneConsumer.reset(true);

        OrderEvent event = createEvent("ERR-001");
        // error-test 토픽으로 직접 전송 (OrderProducer는 chapter2.orders 전용)
        kafkaTemplate.send("chapter2.error-test", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        // DLT로 전송될 때까지 대기 (1초 x 2회 재시도 + 여유)
        boolean dltReceived = errorProneConsumer.getDltLatch().await(30, TimeUnit.SECONDS);

        // 총 시도 횟수: 1회 원본 + 2회 재시도 = 3회
        assertAndLog("총 시도 횟수가 3이어야 한다 (1회 원본 + 2회 재시도)",
                () -> assertThat(errorProneConsumer.getAttemptCount().get()).isEqualTo(3));
        // DLT로 메시지가 전송되었는지 확인
        assertAndLog("DLT Consumer가 메시지를 수신해야 한다",
                () -> assertThat(dltReceived).isTrue());
        // DLT에 도착한 메시지가 원본과 동일한지 확인
        assertAndLog("DLT 메시지의 orderId가 원본과 일치해야 한다",
                () -> assertThat(errorProneConsumer.getLastDltEvent().getOrderId()).isEqualTo("ERR-001"));
    }

    // --- C5: 정상 처리 시 에러 핸들러가 개입하지 않음을 검증 ---
    @Test
    void 정상_처리_시_에러_핸들러가_개입하지_않는다() throws Exception {
        // shouldFail=false → 예외 없이 정상 처리
        errorProneConsumer.reset(false);

        OrderEvent event = createEvent("OK-001");
        kafkaTemplate.send("chapter2.error-test", event.getOrderId(), event)
                .get(10, TimeUnit.SECONDS);

        // 정상 처리 완료 대기
        boolean success = errorProneConsumer.getSuccessLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("정상 처리가 완료되어야 한다",
                () -> assertThat(success).isTrue());
        // 재시도 없이 1회만 시도
        assertAndLog("시도 횟수가 1이어야 한다 (재시도 없음)",
                () -> assertThat(errorProneConsumer.getAttemptCount().get()).isEqualTo(1));
    }
}
