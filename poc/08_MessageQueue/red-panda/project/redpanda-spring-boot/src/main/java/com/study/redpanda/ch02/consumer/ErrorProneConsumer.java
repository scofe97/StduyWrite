package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Ch02 C5: 에러 핸들러 테스트용 Consumer
 *
 * shouldFail 플래그로 예외 발생을 제어한다.
 * attemptCount로 재시도 횟수를 추적한다.
 */
@Slf4j
@Component
public class ErrorProneConsumer {

    // 예외를 발생시킬지 여부 (테스트에서 제어)
    @Getter
    private volatile boolean shouldFail = false;

    // 처리 시도 횟수 (원본 + 재시도 포함)
    @Getter
    private final AtomicInteger attemptCount = new AtomicInteger(0);

    // 정상 처리 완료 시 사용
    @Getter
    private CountDownLatch successLatch = new CountDownLatch(1);

    // DLT로 전송된 메시지 수신 확인
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
     * 에러 테스트용 Consumer: shouldFail=true이면 매번 예외를 던진다.
     * DefaultErrorHandler가 BackOff에 따라 재시도하고, 소진 후 DLT로 전송한다.
     */
    @KafkaListener(topics = "chapter2.error-test", groupId = "error-test-group")
    public void consume(@Payload OrderEvent event, Acknowledgment ack) {
        int attempt = attemptCount.incrementAndGet();
        log.info("ErrorProneConsumer attempt #{}: orderId={}, shouldFail={}",
                attempt, event.getOrderId(), shouldFail);

        if (shouldFail) {
            throw new RuntimeException("Intentional failure for testing (attempt #" + attempt + ")");
        }

        // 정상 처리
        log.info("ErrorProneConsumer: successfully processed orderId={}", event.getOrderId());
        ack.acknowledge();
        successLatch.countDown();
    }

    /**
     * DLT Consumer: 재시도 소진 후 {원본토픽}-dlt로 전송된 메시지를 수신한다.
     * DefaultErrorHandler + DeadLetterPublishingRecoverer가 자동으로 전송한다.
     */
    @KafkaListener(topics = "chapter2.error-test-dlt", groupId = "error-test-dlt-group")
    public void consumeDlt(@Payload OrderEvent event, Acknowledgment ack) {
        log.info("DLT received: orderId={}", event.getOrderId());
        lastDltEvent = event;
        ack.acknowledge();
        dltLatch.countDown();
    }
}
