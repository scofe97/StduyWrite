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
 * Ch02 C7: Consumer Pause 테스트용 Consumer
 *
 * @KafkaListener의 id를 지정하여 KafkaListenerEndpointRegistry로
 * 특정 리스너만 pause/resume할 수 있다.
 *
 * pause() 상태에서는 poll()은 계속 호출되지만 메시지를 가져오지 않는다.
 * → 리밸런싱 없이 파티션 소유권 유지
 */
@Slf4j
@Component
public class PausableConsumer {

    @Getter
    private volatile CountDownLatch latch = new CountDownLatch(1);

    @Getter
    private final AtomicInteger receivedCount = new AtomicInteger(0);

    @Getter
    private volatile OrderEvent lastReceivedEvent;

    public void reset(int count) {
        this.latch = new CountDownLatch(count);
        this.receivedCount.set(0);
        this.lastReceivedEvent = null;
    }

    @KafkaListener(
            id = "pausable-listener",
            topics = "chapter2.pause-test",
            groupId = "pause-test-group"
    )
    public void consume(@Payload OrderEvent event, Acknowledgment ack) {
        int count = receivedCount.incrementAndGet();
        log.info("PausableConsumer received #{}: orderId={}", count, event.getOrderId());
        lastReceivedEvent = event;
        ack.acknowledge();
        latch.countDown();
    }
}
