package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;

/**
 * Ch02 C3: 배치 Consumer - 여러 메시지를 한 번에 수신하여 처리
 *
 * containerFactory = "batchKafkaListenerContainerFactory"로 배치 모드를 지정한다.
 * 기본 Factory와 다른 점: 파라미터가 단일 객체가 아닌 List<OrderEvent>이다.
 *
 * 같은 토픽(chapter2.orders)을 다른 groupId로 구독하므로
 * OrderConsumer와 독립적으로 모든 메시지를 수신한다.
 */
@Slf4j
@Component
public class BatchOrderConsumer {

    @Getter
    private CountDownLatch latch = new CountDownLatch(1);

    // 마지막으로 수신한 배치의 이벤트 목록
    @Getter
    private List<OrderEvent> lastReceivedBatch = new ArrayList<>();

    // 수신한 총 이벤트 수 (여러 배치에 걸쳐 누적)
    @Getter
    private int totalReceivedCount = 0;

    public void resetLatch(int count) {
        this.latch = new CountDownLatch(count);
        this.lastReceivedBatch = new ArrayList<>();
        this.totalReceivedCount = 0;
    }

    /**
     * 배치 모드: poll()에서 가져온 메시지들이 List로 한 번에 전달된다.
     * max.poll.records (기본 500) 이하의 메시지가 한 배치로 들어온다.
     */
    @KafkaListener(
            topics = "chapter2.orders",
            groupId = "batch-consumer-group",
            containerFactory = "batchKafkaListenerContainerFactory"
    )
    public void consumeBatch(List<OrderEvent> events, Acknowledgment ack) {
        log.info("Batch received: size={}", events.size());

        lastReceivedBatch = new ArrayList<>(events);
        totalReceivedCount += events.size();

        events.forEach(event ->
                log.info("  - orderId={}, product={}, price={}",
                        event.getOrderId(), event.getProductName(), event.getPrice()));

        // 배치 전체를 처리한 후 한 번만 ACK → offset 커밋
        ack.acknowledge();

        // 배치 하나를 수신할 때마다 latch 감소
        latch.countDown();
    }
}
