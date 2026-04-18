package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.ch02.consumer.OrderConsumer;
import com.study.redpanda.ch02.producer.OrderProducer;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.support.SendResult;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Consumer 동작 검증 테스트
 * - T2: CountDownLatch 기반 수신 검증
 * - C2: @Header로 메타데이터 접근
 * - P4: 커스텀 헤더 라운드트립
 * - P5: ProducerInterceptor 자동 헤더 주입 검증
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class ConsumerTest extends AbstractLocalKafkaTest {

    @Autowired
    private OrderProducer orderProducer;

    @Autowired
    private OrderConsumer orderConsumer;

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

    // --- T2: Consumer 수신 검증 - CountDownLatch로 비동기 수신 대기 ---
    @Test
    void 주문_10건_발행하면_Consumer가_모두_수신한다() throws Exception {
        int messageCount = 10;
        // latch를 messageCount로 초기화 → Consumer가 countDown()할 때마다 감소
        orderConsumer.resetLatch(messageCount);

        for (int i = 1; i <= messageCount; i++) {
            OrderEvent event = OrderEvent.newBuilder()
                    .setEventId(UUID.randomUUID().toString())
                    .setEventType("ORDER_CREATED")
                    .setTimestamp(Instant.now().toEpochMilli())
                    .setOrderId("ORD-" + String.format("%03d", i))
                    .setProductName("상품-" + i)
                    .setQuantity(i)
                    .setPrice(1000.0 * i)
                    .build();

            orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);
        }

        // latch가 0이 될 때까지 대기 (모든 메시지 수신 완료)
        boolean allReceived = orderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 " + messageCount + "건 모두 수신해야 한다",
                () -> assertThat(allReceived).isTrue());
        assertAndLog("마지막 수신 이벤트가 null이 아니어야 한다",
                () -> assertThat(orderConsumer.getLastReceivedEvent()).isNotNull());
        // 3개 파티션에서 수신하므로 마지막 이벤트의 orderId 순서는 보장되지 않음
        assertAndLog("수신된 orderId가 ORD-로 시작해야 한다",
                () -> assertThat(orderConsumer.getLastReceivedEvent().getOrderId()).startsWith("ORD-"));
    }

    // --- C2: 메타데이터 접근 - @Header로 partition/offset 교차 검증 ---
    @Test
    void Consumer는_메타데이터를_수신할_수_있다() throws Exception {
        orderConsumer.resetLatch(1);

        OrderEvent event = createEvent("META-001", "메타데이터상품", 3000.0);

        // Producer의 SendResult에서 partition을 기록해두고
        SendResult<String, OrderEvent> sendResult =
                orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);

        boolean received = orderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 메시지를 수신해야 한다",
                () -> assertThat(received).isTrue());
        // Consumer가 @Header로 받은 partition == Producer SendResult의 partition
        assertAndLog("Consumer partition == Producer partition",
                () -> assertThat(orderConsumer.getLastReceivedPartition())
                        .isEqualTo(sendResult.getRecordMetadata().partition()));
        assertAndLog("Consumer offset이 0 이상이어야 한다",
                () -> assertThat(orderConsumer.getLastReceivedOffset()).isGreaterThanOrEqualTo(0));
    }

    // --- P4: 커스텀 헤더 전송 - ProducerRecord에 수동 헤더 추가 후 라운드트립 검증 ---
    @Test
    void 커스텀_헤더를_포함하여_전송하면_Consumer가_수신한다() throws Exception {
        orderConsumer.resetLatch(1);

        OrderEvent event = createEvent("HDR-001", "헤더전송상품", 7000.0);

        // Producer가 보낼 커스텀 헤더 (분산 추적용)
        String correlationId = UUID.randomUUID().toString();
        Map<String, String> headers = Map.of(
                "X-Correlation-Id", correlationId,
                "X-Source", "order-service"
        );

        orderProducer.sendOrderWithHeaders(event, headers).get(10, TimeUnit.SECONDS);

        boolean received = orderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 메시지를 수신해야 한다",
                () -> assertThat(received).isTrue());
        // Consumer의 @Header(value="X-Correlation-Id", required=false)로 수신
        assertAndLog("X-Correlation-Id가 Producer가 보낸 값과 일치해야 한다",
                () -> assertThat(orderConsumer.getLastReceivedCorrelationId()).isEqualTo(correlationId));
        assertAndLog("X-Source가 order-service여야 한다",
                () -> assertThat(orderConsumer.getLastReceivedSource()).isEqualTo("order-service"));
    }

    // --- P4: 헤더 없는 전송 - required=false이므로 null로 수신됨을 검증 ---
    @Test
    void 커스텀_헤더_없이_전송하면_null로_수신된다() throws Exception {
        orderConsumer.resetLatch(1);

        OrderEvent event = createEvent("NO-HDR-001", "헤더없는상품", 2000.0);

        // 일반 sendOrder()는 커스텀 헤더를 추가하지 않음
        orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);

        boolean received = orderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 메시지를 수신해야 한다",
                () -> assertThat(received).isTrue());
        // required=false이므로 헤더가 없어도 예외 없이 null 반환
        assertAndLog("헤더 없이 보내면 correlationId는 null이어야 한다 (required=false)",
                () -> assertThat(orderConsumer.getLastReceivedCorrelationId()).isNull());
        assertAndLog("헤더 없이 보내면 source는 null이어야 한다",
                () -> assertThat(orderConsumer.getLastReceivedSource()).isNull());
    }

    // --- P5: ProducerInterceptor - 인터셉터가 자동 주입한 헤더 검증 ---
    @Test
    void 인터셉터가_자동으로_서비스명과_전송시각_헤더를_주입한다() throws Exception {
        orderConsumer.resetLatch(1);

        OrderEvent event = createEvent("ICP-001", "인터셉터상품", 9000.0);

        // 일반 sendOrder() - 수동 헤더 없이 전송
        // CommonHeaderInterceptor가 X-Service-Name, X-Sent-At을 자동 주입
        orderProducer.sendOrder(event).get(10, TimeUnit.SECONDS);

        boolean received = orderConsumer.getLatch().await(30, TimeUnit.SECONDS);

        assertAndLog("Consumer가 메시지를 수신해야 한다",
                () -> assertThat(received).isTrue());
        // 인터셉터가 주입한 X-Service-Name 확인
        assertAndLog("X-Service-Name이 order-service여야 한다 (인터셉터 자동 주입)",
                () -> assertThat(orderConsumer.getLastReceivedServiceName()).isEqualTo("order-service"));
        // 인터셉터가 주입한 X-Sent-At 확인 (ISO-8601 형식)
        assertAndLog("X-Sent-At이 null이 아니어야 한다 (인터셉터 자동 주입)",
                () -> assertThat(orderConsumer.getLastReceivedSentAt()).isNotNull());
        assertAndLog("X-Sent-At이 ISO-8601 형식이어야 한다",
                () -> assertThat(orderConsumer.getLastReceivedSentAt()).contains("T"));
    }
}
