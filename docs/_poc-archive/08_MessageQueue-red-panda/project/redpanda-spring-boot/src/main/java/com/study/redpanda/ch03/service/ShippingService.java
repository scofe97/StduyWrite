package com.study.redpanda.ch03.service;

import com.study.redpanda.avro.saga.SagaPaymentCompleted;
import com.study.redpanda.ch03.domain.Shipping;
import com.study.redpanda.ch03.domain.ShippingStatus;
import com.study.redpanda.ch03.event.PaymentCompleted;
import com.study.redpanda.ch03.event.ShippingFailed;
import com.study.redpanda.ch03.event.ShippingRequested;
import com.study.redpanda.ch03.domain.SagaStepType;
import com.study.redpanda.ch03.event.mapper.SagaEventMapper;
import com.study.redpanda.ch03.repository.ShippingRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.UUID;

@Service
@Slf4j
public class ShippingService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final ShippingRepository shippingRepository;
    private final EventIdempotencyChecker idempotencyChecker;

    public ShippingService(
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate,
            ShippingRepository shippingRepository,
            EventIdempotencyChecker idempotencyChecker) {
        this.kafkaTemplate = kafkaTemplate;
        this.shippingRepository = shippingRepository;
        this.idempotencyChecker = idempotencyChecker;
    }

    @Transactional
    @KafkaListener(topics = "chapter3.payment-completed",
                   groupId = "ch03-shipping-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onPaymentCompleted(SagaPaymentCompleted avroEvent, Acknowledgment ack) {
        PaymentCompleted event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.SHIPPING_PROCESS)) {
                log.warn("[SAGA] Duplicate ShippingProcess ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            log.info("[SAGA] Processing shipping for order: {}", event.orderId());

            try {
                String trackingNumber = "TRACK-" + UUID.randomUUID().toString().substring(0, 8);

                Shipping shipping = Shipping.builder()
                        .id(UUID.randomUUID().toString())
                        .orderId(event.orderId())
                        .trackingNumber(trackingNumber)
                        .status(ShippingStatus.REQUESTED)
                        .build();
                shippingRepository.save(shipping);

                ShippingRequested domainEvent = new ShippingRequested(
                        event.orderId(),
                        event.correlationId(),
                        Instant.now(),
                        trackingNumber);

                kafkaTemplate.send("chapter3.shipping-requested", SagaEventMapper.toAvro(domainEvent));

                log.info("[SAGA] Shipping requested: orderId={}, tracking={}", event.orderId(), trackingNumber);
                ack.acknowledge();

            } catch (Exception e) {
                ShippingFailed failedEvent = new ShippingFailed(
                        event.orderId(),
                        event.correlationId(),
                        Instant.now(),
                        e.getMessage());

                kafkaTemplate.send("chapter3.shipping-failed", SagaEventMapper.toAvro(failedEvent));

                log.error("[SAGA] Shipping failed: orderId={}", event.orderId(), e);
                ack.acknowledge();  // 실패 이벤트를 발행했으므로 처리 완료로 간주
            }
        } finally {
            SagaMdc.clear();
        }
    }
}
