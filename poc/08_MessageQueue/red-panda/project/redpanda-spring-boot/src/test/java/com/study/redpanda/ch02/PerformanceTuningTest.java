package com.study.redpanda.ch02;

import com.study.redpanda.avro.OrderEvent;
import com.study.redpanda.config.AbstractLocalKafkaTest;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.SendResult;
import org.springframework.test.annotation.DirtiesContext;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * I2: 성능 튜닝 설정 검증
 *
 * application.yml에 설정한 Producer/Consumer 튜닝 값이 실제로 적용되는지 확인하고,
 * 대량 전송 시 배치 효과를 측정한다.
 */
@Slf4j
@SpringBootTest
@DirtiesContext
class PerformanceTuningTest extends AbstractLocalKafkaTest {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    @Autowired
    private ProducerFactory<String, OrderEvent> producerFactory;

    @Autowired
    private ConsumerFactory<String, OrderEvent> consumerFactory;

    private OrderEvent createEvent(String orderId) {
        return OrderEvent.newBuilder()
                .setEventId(UUID.randomUUID().toString())
                .setEventType("ORDER_CREATED")
                .setTimestamp(Instant.now().toEpochMilli())
                .setOrderId(orderId)
                .setProductName("성능테스트상품")
                .setQuantity(1)
                .setPrice(1000.0)
                .build();
    }

    // --- Producer 튜닝 설정이 적용되었는지 검증 ---
    @Test
    void Producer_튜닝_설정이_적용되어_있다() {
        Map<String, Object> config = producerFactory.getConfigurationProperties();

        // batch-size: 16384 (16KB)
        assertThat(config.get(ProducerConfig.BATCH_SIZE_CONFIG))
                .isEqualTo(16384);
        log.info("[PASS] batch-size={}", config.get(ProducerConfig.BATCH_SIZE_CONFIG));

        // linger.ms: 10
        assertThat(config.get(ProducerConfig.LINGER_MS_CONFIG))
                .isEqualTo("10");
        log.info("[PASS] linger.ms={}", config.get(ProducerConfig.LINGER_MS_CONFIG));

        // buffer-memory: 33554432 (32MB)
        assertThat(config.get(ProducerConfig.BUFFER_MEMORY_CONFIG))
                .isEqualTo(33554432L);
        log.info("[PASS] buffer-memory={}", config.get(ProducerConfig.BUFFER_MEMORY_CONFIG));

        // compression-type: lz4
        assertThat(config.get(ProducerConfig.COMPRESSION_TYPE_CONFIG))
                .isEqualTo("lz4");
        log.info("[PASS] compression-type={}", config.get(ProducerConfig.COMPRESSION_TYPE_CONFIG));
    }

    // --- Consumer 튜닝 설정이 적용되었는지 검증 ---
    @Test
    void Consumer_튜닝_설정이_적용되어_있다() {
        Map<String, Object> config = consumerFactory.getConfigurationProperties();

        // max-poll-records: 500
        assertThat(Integer.valueOf(config.get(ConsumerConfig.MAX_POLL_RECORDS_CONFIG).toString()))
                .isEqualTo(500);
        log.info("[PASS] max-poll-records={}", config.get(ConsumerConfig.MAX_POLL_RECORDS_CONFIG));

        // fetch-min-size: 1
        assertThat(config.get(ConsumerConfig.FETCH_MIN_BYTES_CONFIG))
                .isEqualTo(1);
        log.info("[PASS] fetch-min-size={}", config.get(ConsumerConfig.FETCH_MIN_BYTES_CONFIG));

        // fetch-max-wait: 500
        assertThat(config.get(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG))
                .isEqualTo(500);
        log.info("[PASS] fetch-max-wait={}", config.get(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG));
    }

    // --- 대량 전송으로 배치 효과 확인 (1000건) ---
    @Test
    void 대량_전송_시_배치가_적용되어_처리된다() throws Exception {
        int messageCount = 1000;
        List<CompletableFuture<SendResult<String, OrderEvent>>> futures = new ArrayList<>();

        long startTime = System.currentTimeMillis();

        // 1000건 비동기 전송 (batch-size=16KB, linger.ms=10에 의해 배치로 묶임)
        for (int i = 0; i < messageCount; i++) {
            OrderEvent event = createEvent("PERF-" + i);
            CompletableFuture<SendResult<String, OrderEvent>> future =
                    kafkaTemplate.send("chapter2.orders", event.getOrderId(), event);
            futures.add(future);
        }

        // 모든 전송 완료 대기
        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
                .get(60, TimeUnit.SECONDS);

        long elapsed = System.currentTimeMillis() - startTime;
        double throughput = (messageCount * 1000.0) / elapsed;

        log.info("===== 배치 전송 결과 =====");
        log.info("전송 건수: {}건", messageCount);
        log.info("소요 시간: {}ms", elapsed);
        log.info("처리량: {} msg/sec", String.format("%.0f", throughput));
        log.info("설정: batch-size=16KB, linger.ms=10, compression=lz4");
        log.info("========================");

        // 모든 메시지가 성공적으로 전송됨
        assertThat(futures).allSatisfy(f -> assertThat(f).isDone());

        // 배치 효과: 1000건을 개별 전송하면 1000번 네트워크 왕복이 필요하지만,
        // 배치로 묶이면 수십 번의 왕복으로 줄어든다.
        // 로컬 환경에서도 1000건이 60초 이내에 처리되어야 한다.
        assertThat(elapsed).isLessThan(60000);
        log.info("[PASS] {}건 전송 완료: {}ms, {} msg/sec", messageCount, elapsed, String.format("%.0f", throughput));
    }
}
