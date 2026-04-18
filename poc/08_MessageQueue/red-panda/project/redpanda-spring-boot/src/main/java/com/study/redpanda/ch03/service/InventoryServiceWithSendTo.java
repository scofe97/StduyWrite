package com.study.redpanda.ch03.service;

import com.study.redpanda.avro.saga.SagaInventoryReserved;
import com.study.redpanda.avro.saga.SagaOrderCreated;
import com.study.redpanda.avro.saga.SagaPaymentFailed;
import com.study.redpanda.avro.saga.SagaPaymentRefunded;
import com.study.redpanda.ch03.domain.Inventory;
import com.study.redpanda.ch03.domain.Reservation;
import com.study.redpanda.ch03.domain.ReservationStatus;
import com.study.redpanda.ch03.event.InventoryReleased;
import com.study.redpanda.ch03.event.InventoryReservationFailed;
import com.study.redpanda.ch03.event.InventoryReserved;
import com.study.redpanda.ch03.event.OrderCreated;
import com.study.redpanda.ch03.event.PaymentFailed;
import com.study.redpanda.ch03.event.PaymentRefunded;
import com.study.redpanda.ch03.event.mapper.SagaEventMapper;
import com.study.redpanda.ch03.repository.InventoryRepository;
import com.study.redpanda.ch03.repository.ReservationRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Profile;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * InventoryService의 @SendTo 대안 구현 (비교용)
 *
 * KafkaTemplate 방식과의 트레이드오프를 체감하기 위한 대안 서비스.
 * "ch03-sendto" 프로파일에서만 활성화되어 기존 InventoryService와 충돌하지 않는다.
 *
 * 핵심 관찰:
 * - 성공 경로: @SendTo 덕분에 kafkaTemplate.send() 호출 불필요 → 간결
 * - 실패 경로: 다른 토픽으로 보내야 하므로 KafkaTemplate 여전히 필요 → 하이브리드
 * - 보상 리스너: 이벤트 발행이 필요하므로 @SendTo 적용 불가 → KafkaTemplate 그대로
 *
 * 결론: SAGA처럼 성공/실패 분기가 있으면 @SendTo가 오히려 복잡도를 높인다.
 *
 * ⚠️ 학습용 비교 코드 — 프로덕션 사용 금지
 * 멱등성 체크(EventIdempotencyChecker)가 적용되지 않았으므로,
 * 이 프로파일이 활성화되면 중복 이벤트 처리에 대한 안전장치가 없다.
 */
@Service
@Profile("ch03-sendto")
@Slf4j
public class InventoryServiceWithSendTo {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final InventoryRepository inventoryRepository;
    private final ReservationRepository reservationRepository;

    public InventoryServiceWithSendTo(
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate,
            InventoryRepository inventoryRepository,
            ReservationRepository reservationRepository) {
        this.kafkaTemplate = kafkaTemplate;
        this.inventoryRepository = inventoryRepository;
        this.reservationRepository = reservationRepository;
    }

    // ─── @SendTo 방식: 성공 시 반환값이 자동으로 지정 토픽으로 전송 ──────────

    /**
     * @SendTo로 성공 이벤트를 자동 전달하는 방식.
     *
     * 성공 시: 반환된 SagaInventoryReserved가 chapter3.inventory-reserved로 자동 전송
     * 실패 시: @SendTo는 하나의 토픽만 지정 가능 → 다른 토픽(inventory-reservation-failed)으로
     *         보내려면 KafkaTemplate을 직접 사용해야 함 (하이브리드)
     *
     * null 반환 시 @SendTo는 메시지를 전송하지 않는다 (Spring Kafka 공식 동작).
     */
    @Transactional
    @KafkaListener(topics = "chapter3.order-created",
                   groupId = "ch03-inventory-sendto",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    @SendTo("chapter3.inventory-reserved")
    public SagaInventoryReserved onOrderCreated(SagaOrderCreated avroEvent, Acknowledgment ack) {
        OrderCreated event = SagaEventMapper.toDomain(avroEvent);
        log.info("[SAGA-SENDTO] Processing inventory for order: {}", event.orderId());

        try {
            List<String> reservationIds = new ArrayList<>();

            for (OrderCreated.OrderItem item : event.items()) {
                Inventory inventory = inventoryRepository.findByProductIdWithLock(item.productId())
                        .orElseThrow(() -> new IllegalStateException("Product not found: " + item.productId()));

                inventory.reserve(item.quantity());
                inventoryRepository.save(inventory);

                Reservation reservation = Reservation.builder()
                        .id(UUID.randomUUID().toString())
                        .orderId(event.orderId())
                        .productId(item.productId())
                        .quantity(item.quantity())
                        .status(ReservationStatus.RESERVED)
                        .build();
                reservationRepository.save(reservation);
                reservationIds.add(reservation.getId());
            }

            InventoryReserved domainEvent = new InventoryReserved(
                    event.orderId(),
                    event.correlationId(),
                    Instant.now(),
                    reservationIds);

            log.info("[SAGA-SENDTO] Inventory reserved: orderId={}", event.orderId());
            ack.acknowledge();

            // ✅ @SendTo의 장점: 반환값이 자동으로 chapter3.inventory-reserved로 전송
            // kafkaTemplate.send() 호출이 불필요하다
            return SagaEventMapper.toAvro(domainEvent);

        } catch (Exception e) {
            // ❌ @SendTo의 한계: 실패 토픽이 다르다
            // @SendTo("chapter3.inventory-reserved")는 성공 토픽만 지정할 수 있다.
            // chapter3.inventory-reservation-failed로 보내려면 KafkaTemplate이 필요하다.
            // → 결국 하이브리드가 되어 KafkaTemplate 방식보다 오히려 복잡해진다.
            InventoryReservationFailed failedEvent = new InventoryReservationFailed(
                    event.orderId(),
                    event.correlationId(),
                    Instant.now(),
                    e.getMessage(),
                    List.of());

            kafkaTemplate.send("chapter3.inventory-reservation-failed", SagaEventMapper.toAvro(failedEvent));

            log.error("[SAGA-SENDTO] Inventory reservation failed: orderId={}", event.orderId(), e);
            ack.acknowledge();

            // null 반환 → @SendTo가 메시지를 전송하지 않음
            return null;
        }
    }

    // ─── 보상 트랜잭션: @SendTo 적용 불가 ──────────────────────────────────────
    // 보상 리스너는 재고 복구 후 InventoryReleased 이벤트를 발행해야 한다.
    // 하지만 보상 리스너의 반환값은 "다음 보상 단계의 입력"이 아니라
    // "보상 완료 알림"이므로, @SendTo의 단순 파이프라인 모델에 맞지 않는다.
    // 또한 보상 실패 시 throw로 재시도해야 하므로 반환값을 제어할 수 없다.
    // → KafkaTemplate 방식이 유일한 선택

    @Transactional
    @KafkaListener(topics = "chapter3.payment-failed",
                   groupId = "ch03-inventory-sendto",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onPaymentFailed(SagaPaymentFailed avroEvent, Acknowledgment ack) {
        PaymentFailed event = SagaEventMapper.toDomain(avroEvent);
        log.info("[SAGA-SENDTO-COMPENSATE] PaymentFailed received, releasing inventory: orderId={}", event.orderId());

        try {
            releaseInventory(event.orderId(), event.correlationId());
            ack.acknowledge();
        } catch (Exception e) {
            log.error("[SAGA-SENDTO-COMPENSATE] Failed to release inventory, will retry: orderId={}", event.orderId(), e);
            throw e;
        }
    }

    @Transactional
    @KafkaListener(topics = "chapter3.payment-refunded",
                   groupId = "ch03-inventory-sendto",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onPaymentRefunded(SagaPaymentRefunded avroEvent, Acknowledgment ack) {
        PaymentRefunded event = SagaEventMapper.toDomain(avroEvent);
        log.info("[SAGA-SENDTO-COMPENSATE] PaymentRefunded received, releasing inventory: orderId={}", event.orderId());

        try {
            releaseInventory(event.orderId(), event.correlationId());
            ack.acknowledge();
        } catch (Exception e) {
            log.error("[SAGA-SENDTO-COMPENSATE] Failed to release inventory, will retry: orderId={}", event.orderId(), e);
            throw e;
        }
    }

    private void releaseInventory(String orderId, String correlationId) {
        List<Reservation> reservations = reservationRepository
                .findByOrderIdAndStatus(orderId, ReservationStatus.RESERVED);

        if (reservations.isEmpty()) {
            log.warn("[SAGA-SENDTO-COMPENSATE] No RESERVED reservations found for orderId={}", orderId);
            return;
        }

        List<String> releasedIds = new ArrayList<>();

        for (Reservation reservation : reservations) {
            Inventory inventory = inventoryRepository.findByProductIdWithLock(reservation.getProductId())
                    .orElseThrow(() -> new IllegalStateException("Product not found: " + reservation.getProductId()));

            inventory.release(reservation.getQuantity());
            inventoryRepository.save(inventory);

            reservation.setStatus(ReservationStatus.RELEASED);
            reservationRepository.save(reservation);

            releasedIds.add(reservation.getId());
        }

        InventoryReleased domainEvent = new InventoryReleased(
                orderId, correlationId, Instant.now(), releasedIds);

        kafkaTemplate.send("chapter3.inventory-released", SagaEventMapper.toAvro(domainEvent));

        log.info("[SAGA-SENDTO-COMPENSATE] Inventory released: orderId={}, reservations={}", orderId, releasedIds);
    }
}
