package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Ch02 C9: Idempotent Consumer (중복 처리 방어)
 *
 * Kafka는 at-least-once 보장이므로 같은 메시지가 재전달될 수 있다.
 * eventId 기반 dedup으로 중복 처리를 방어한다.
 *
 * 프로덕션에서는 ConcurrentHashMap 대신 DB dedup 테이블 또는 Redis를 사용한다.
 * - DB: INSERT ... ON CONFLICT DO NOTHING (eventId UNIQUE)
 * - Redis: SET eventId NX EX 3600 (TTL 1시간)
 */
@Slf4j
@Component
public class IdempotentConsumer {

    /** 처리 완료된 eventId를 저장하는 dedup Set (in-memory) */
    private final Set<String> processedEventIds = ConcurrentHashMap.newKeySet();

    /** 실제 처리된 횟수 (중복 skip 제외) */
    @Getter
    private final AtomicInteger processedCount = new AtomicInteger(0);

    /** 중복으로 skip된 횟수 */
    @Getter
    private final AtomicInteger duplicateCount = new AtomicInteger(0);

    @Getter
    private CountDownLatch latch = new CountDownLatch(1);

    @Getter
    private OrderEvent lastProcessedEvent;

    public void resetLatch(int count) {
        this.processedCount.set(0);
        this.duplicateCount.set(0);
        this.processedEventIds.clear();
        this.latch = new CountDownLatch(count);
        this.lastProcessedEvent = null;
    }

    @KafkaListener(topics = "chapter2.idempotent-test", groupId = "idempotent-test-group")
    public void consume(@Payload OrderEvent event, Acknowledgment ack) {
        String eventId = event.getEventId();

        // dedup 체크: 이미 처리한 eventId면 skip
        if (!processedEventIds.add(eventId)) {
            duplicateCount.incrementAndGet();
            log.info("IdempotentConsumer: SKIP duplicate eventId={}, orderId={}",
                    eventId, event.getOrderId());
            ack.acknowledge();
            latch.countDown();
            return;
        }

        // 신규 메시지 처리
        int count = processedCount.incrementAndGet();
        lastProcessedEvent = event;
        log.info("IdempotentConsumer: PROCESSED #{} eventId={}, orderId={}",
                count, eventId, event.getOrderId());

        ack.acknowledge();
        latch.countDown();
    }
}
