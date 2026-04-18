package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.producer.OrderProducer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.support.SendResult;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Producer 동작 검증 테스트
 * - P1: 비동기 전송 (브로커 저장 확인)
 * - P2: 동기 전송 (SendResult 즉시 반환)
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class ProducerTest extends AbstractLocalKafkaTest {

    @Autowired
    private OrderProducer orderProducer;

    private void assertAndLog(String description, Runnable assertion) {
        assertion.run();
        log.info("[PASS] {}", description);
    }

    // --- P1: 비동기 전송 - 10건 발행 후 브로커 저장 검증 ---
    @Test
    void 주문_10건_발행하면_브로커에_저장된다() throws Exception {
        for (int i = 1; i <= 10; i++) {
            // Avro OrderEvent 빌더로 이벤트 생성
            OrderEvent event = OrderEvent.newBuilder()
                    .setEventId(UUID.randomUUID().toString())
                    .setEventType("ORDER_CREATED")
                    .setTimestamp(Instant.now().toEpochMilli())
                    .setOrderId("ORD-" + String.format("%03d", i))
                    .setProductName("상품-" + i)
                    .setQuantity(i)
                    .setPrice(1000.0 * i)
                    .build();

            // 비동기 전송 후 Future로 결과 대기
            CompletableFuture<SendResult<String, OrderEvent>> future =
                    orderProducer.sendOrder(event);
            SendResult<String, OrderEvent> result = future.get(10, TimeUnit.SECONDS);

            // RecordMetadata로 브로커 저장 결과 검증
            assertAndLog("토픽이 chapter2.orders여야 한다 (msg " + i + ")",
                    () -> assertThat(result.getRecordMetadata().topic()).isEqualTo("chapter2.orders"));
            assertAndLog("offset이 0 이상이어야 한다 (msg " + i + ")",
                    () -> assertThat(result.getRecordMetadata().offset()).isGreaterThanOrEqualTo(0));
        }
    }

    // --- P2: 동기 전송 - .get()으로 브로커 ACK 대기 후 결과 즉시 반환 ---
    @Test
    void 동기_전송은_결과를_즉시_반환한다() {
        OrderEvent event = OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId("SYNC-001")
                .setProductName("동기전송상품")
                .setQuantity(1)
                .setPrice(5000.0)
                .build();

        // sendOrderSync()는 내부에서 .get()으로 대기 후 SendResult 직접 반환
        SendResult<String, OrderEvent> result = orderProducer.sendOrderSync(event);

        // SendResult의 두 핵심 객체 검증:
        // - RecordMetadata: 브로커가 실제 저장한 결과
        // - ProducerRecord: Producer가 보낸 원본 메시지
        assertAndLog("SendResult가 null이 아니어야 한다",
                () -> assertThat(result).isNotNull());
        assertAndLog("토픽이 chapter2.orders여야 한다",
                () -> assertThat(result.getRecordMetadata().topic()).isEqualTo("chapter2.orders"));
        assertAndLog("partition이 0 이상이어야 한다",
                () -> assertThat(result.getRecordMetadata().partition()).isGreaterThanOrEqualTo(0));
        assertAndLog("offset이 0 이상이어야 한다",
                () -> assertThat(result.getRecordMetadata().offset()).isGreaterThanOrEqualTo(0));
        assertAndLog("메시지 key가 SYNC-001이어야 한다",
                () -> assertThat(result.getProducerRecord().key()).isEqualTo("SYNC-001"));
    }
}
