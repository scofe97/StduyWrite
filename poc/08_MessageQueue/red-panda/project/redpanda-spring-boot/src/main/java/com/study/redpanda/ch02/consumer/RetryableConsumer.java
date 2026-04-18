package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.DltHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.kafka.retrytopic.TopicSuffixingStrategy;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.retry.annotation.Backoff;
import org.springframework.stereotype.Component;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Ch02 C6: @RetryableTopic 기반 논블록킹 재시도 Consumer
 *
 * C5(DefaultErrorHandler)와의 핵심 차이:
 * - C5: Consumer 메모리에서 블록킹 재시도 → 해당 파티션 처리 차단
 * - C6: 별도 재시도 토픽으로 메시지 이동 → 원본 토픽 처리 계속 진행
 *
 * 생성되는 토픽:
 * - chapter2.retryable-test-retry-0 (1초 후 재시도)
 * - chapter2.retryable-test-retry-1 (2초 후 재시도)
 * - chapter2.retryable-test-dlt (재시도 소진 후)
 */
@Slf4j
@Component
public class RetryableConsumer {

    @Getter
    private volatile boolean shouldFail = false;

    /** 처리 시도 횟수 (원본 + 재시도 토픽 포함) */
    @Getter
    private final AtomicInteger attemptCount = new AtomicInteger(0);

    @Getter
    private CountDownLatch successLatch = new CountDownLatch(1);

    @Getter
    private CountDownLatch dltLatch = new CountDownLatch(1);

    @Getter
    private OrderEvent lastDltEvent;

    public void reset(boolean fail) {
        this.shouldFail = fail;
        this.attemptCount.set(0);
        this.successLatch = new CountDownLatch(1);
        this.dltLatch = new CountDownLatch(1);
        this.lastDltEvent = null;
    }

    /**
     * 논블록킹 재시도 Consumer
     *
     * attempts = "3": 총 3회 시도 (1회 원본 + 2회 재시도)
     * backoff: 1초 → 2초 (multiplier=2)
     * topicSuffixingStrategy: -retry-0, -retry-1 형태로 토픽 생성
     * autoCreateTopics: 재시도/DLT 토픽 자동 생성
     *
     * 실패 시 흐름:
     * chapter2.retryable-test → chapter2.retryable-test-retry-0 (1초 후)
     *                         → chapter2.retryable-test-retry-1 (2초 후)
     *                         → chapter2.retryable-test-dlt (최종)
     */
    @RetryableTopic(
            attempts = "3",
            backoff = @Backoff(delay = 1000, multiplier = 2),
            topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE,
            autoCreateTopics = "true"
    )
    @KafkaListener(topics = "chapter2.retryable-test", groupId = "retryable-test-group")
    public void consume(@Payload OrderEvent event, Acknowledgment ack) {
        int attempt = attemptCount.incrementAndGet();
        log.info("RetryableConsumer attempt #{}: orderId={}, shouldFail={}",
                attempt, event.getOrderId(), shouldFail);

        if (shouldFail) {
            throw new RuntimeException("Intentional failure for testing (attempt #" + attempt + ")");
        }

        log.info("RetryableConsumer: successfully processed orderId={}", event.getOrderId());
        ack.acknowledge();
        successLatch.countDown();
    }

    /**
     * DLT Handler: 모든 재시도 소진 후 최종 도착지
     *
     * @DltHandler는 같은 클래스 내에서 @RetryableTopic이 붙은 메서드와 자동 연결된다.
     * 별도 @KafkaListener로 DLT 토픽을 구독할 필요 없음 (C5와의 차이).
     */
    @DltHandler
    public void consumeDlt(
            @Payload OrderEvent event,
            @Header(KafkaHeaders.RECEIVED_TOPIC) String topic,
            @Header(KafkaHeaders.EXCEPTION_MESSAGE) String errorMessage,
            @Header(name = KafkaHeaders.EXCEPTION_FQCN, required = false) String exceptionClass,
            @Header(name = KafkaHeaders.ORIGINAL_TOPIC, required = false) String originalTopic,
            @Header(name = KafkaHeaders.ORIGINAL_OFFSET, required = false, defaultValue = "-1") long originalOffset,
            Acknowledgment ack) {
        log.warn("=== DLT 수신 (RetryableTopic) ===");
        log.warn("  orderId       : {}", event.getOrderId());
        log.warn("  dltTopic      : {}", topic);
        log.warn("  originalTopic : {}", originalTopic);
        log.warn("  originalOffset: {}", originalOffset);
        log.warn("  exceptionClass: {}", exceptionClass);
        log.warn("  errorMessage  : {}", errorMessage);
        lastDltEvent = event;
        ack.acknowledge();
        dltLatch.countDown();
    }
}
