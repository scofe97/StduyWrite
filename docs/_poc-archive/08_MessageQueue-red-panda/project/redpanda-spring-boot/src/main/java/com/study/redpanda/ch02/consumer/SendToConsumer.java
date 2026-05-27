package com.study.redpanda.ch02.consumer;

import com.study.redpanda.avro.OrderEvent;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.concurrent.CountDownLatch;

/**
 * Ch02 C4: @SendTo 기반 파이프라인
 *
 * Consumer가 메시지를 처리한 후 반환값을 다른 토픽으로 자동 전송한다.
 * KafkaTemplate을 직접 주입하지 않아도 Spring이 자동으로 전송한다.
 *
 * - 정상 처리: OrderEvent를 가공해 ORDER_PROCESSED로 변환 후 output 토픽에 전송
 * - 필터링: null 반환 시 output 토픽에 전송하지 않음 (ORDER_CANCELLED 필터)
 */
@Slf4j
@Component
public class SendToConsumer {

    @Getter
    private CountDownLatch inputLatch = new CountDownLatch(1);

    @Getter
    private CountDownLatch outputLatch = new CountDownLatch(1);

    @Getter
    private OrderEvent lastInputEvent;

    @Getter
    private OrderEvent lastOutputEvent;

    public void reset(int inputCount, int outputCount) {
        this.inputLatch = new CountDownLatch(inputCount);
        this.outputLatch = new CountDownLatch(outputCount);
        this.lastInputEvent = null;
        this.lastOutputEvent = null;
    }

    /**
     * 파이프라인 입력: chapter2.sendto-input → 가공 → chapter2.sendto-output
     *
     * @SendTo는 반환값을 지정된 토픽으로 자동 전송한다.
     * - null 반환 시 전송하지 않음 (필터 패턴)
     * - 반환값이 있으면 KafkaTemplate의 직렬화기로 전송
     */
    @KafkaListener(topics = "chapter2.sendto-input", groupId = "sendto-group")
    @SendTo("chapter2.sendto-output")
    public OrderEvent process(@Payload OrderEvent event, Acknowledgment ack) {
        log.info("SendTo input: orderId={}, eventType={}", event.getOrderId(), event.getEventType());
        lastInputEvent = event;
        inputLatch.countDown();
        ack.acknowledge();

        // 필터: CANCEL 이벤트는 다음 토픽으로 전달하지 않음
        if ("ORDER_CANCELLED".equals(event.getEventType().toString())) {
            log.info("Filtered out cancelled order: {}", event.getOrderId());
            return null;
        }

        // 변환: eventType을 ORDER_PROCESSED로 변경
        return OrderEvent.newBuilder(event)
                .setEventType("ORDER_PROCESSED")
                .setTimestamp(Instant.now().toEpochMilli())
                .build();
    }

    /**
     * 파이프라인 출력: 가공된 메시지를 수신하는 하류 Consumer
     */
    @KafkaListener(topics = "chapter2.sendto-output", groupId = "sendto-output-group")
    public void consumeOutput(@Payload OrderEvent event, Acknowledgment ack) {
        log.info("SendTo output: orderId={}, eventType={}", event.getOrderId(), event.getEventType());
        lastOutputEvent = event;
        ack.acknowledge();
        outputLatch.countDown();
    }
}
