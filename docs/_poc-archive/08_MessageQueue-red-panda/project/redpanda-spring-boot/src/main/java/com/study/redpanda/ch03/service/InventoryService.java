package com.study.redpanda.ch03.service;

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
import com.study.redpanda.ch03.domain.SagaStepType;
import com.study.redpanda.ch03.event.mapper.SagaEventMapper;
import com.study.redpanda.ch03.repository.InventoryRepository;
import com.study.redpanda.ch03.repository.ReservationRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
@Slf4j
public class InventoryService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final InventoryRepository inventoryRepository;
    private final ReservationRepository reservationRepository;
    private final EventIdempotencyChecker idempotencyChecker;

    public InventoryService(
            @Qualifier("ch03KafkaTemplate") KafkaTemplate<String, Object> kafkaTemplate,
            InventoryRepository inventoryRepository,
            ReservationRepository reservationRepository,
            EventIdempotencyChecker idempotencyChecker) {
        this.kafkaTemplate = kafkaTemplate;
        this.inventoryRepository = inventoryRepository;
        this.reservationRepository = reservationRepository;
        this.idempotencyChecker = idempotencyChecker;
    }

    @Transactional
    @KafkaListener(topics = "chapter3.order-created",
                   groupId = "ch03-inventory-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onOrderCreated(SagaOrderCreated avroEvent, Acknowledgment ack) {
        OrderCreated event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.INVENTORY_RESERVE)) {
                log.warn("[SAGA] Duplicate InventoryReserve ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            log.info("[SAGA] Processing inventory for order: {}", event.orderId());

            try {
                List<String> reservationIds = new ArrayList<>();

                for (OrderCreated.OrderItem item : event.items()) {
                    // 비관적 잠금으로 재고 조회 (SELECT ... FOR UPDATE)
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

                kafkaTemplate.send("chapter3.inventory-reserved", SagaEventMapper.toAvro(domainEvent));

                log.info("[SAGA] Inventory reserved: orderId={}", event.orderId());
                ack.acknowledge();

            } catch (Exception e) {
                InventoryReservationFailed failedEvent = new InventoryReservationFailed(
                        event.orderId(),
                        event.correlationId(),
                        Instant.now(),
                        e.getMessage(),
                        List.of());

                kafkaTemplate.send("chapter3.inventory-reservation-failed", SagaEventMapper.toAvro(failedEvent));

                log.error("[SAGA] Inventory reservation failed: orderId={}", event.orderId(), e);
                ack.acknowledge();  // 실패 이벤트를 발행했으므로 처리 완료로 간주
            }
        } finally {
            SagaMdc.clear();
        }
    }

    // ─── 보상 트랜잭션 리스너 ──────────────────────────────────────────────

    /**
     * 결제 실패 → 재고 복구 (보상)
     * 결제가 실패하면 이미 예약된 재고를 원복한다.
     */
    @Transactional
    @KafkaListener(topics = "chapter3.payment-failed",
                   groupId = "ch03-inventory-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onPaymentFailed(SagaPaymentFailed avroEvent, Acknowledgment ack) {
        PaymentFailed event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.INVENTORY_RELEASE_PAYMENT_FAILED)) {
                log.warn("[SAGA-COMPENSATE] Duplicate inventory release ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            log.info("[SAGA-COMPENSATE] PaymentFailed received, releasing inventory: orderId={}", event.orderId());

            try {
                releaseInventory(event.orderId(), event.correlationId());
                ack.acknowledge();
            } catch (Exception e) {
                log.error("[SAGA-COMPENSATE] Failed to release inventory, will retry: orderId={}", event.orderId(), e);
                throw e;
            }
        } finally {
            SagaMdc.clear();
        }
    }

    /**
     * 환불 완료 → 재고 복구 (보상)
     * 배송 실패 시 보상 순서: ShippingFailed → PaymentRefunded → InventoryReleased (역순)
     * PaymentService가 환불을 완료한 뒤에야 재고를 복구한다.
     */
    @Transactional
    @KafkaListener(topics = "chapter3.payment-refunded",
                   groupId = "ch03-inventory-service",
                   containerFactory = "ch03KafkaListenerContainerFactory")
    public void onPaymentRefunded(SagaPaymentRefunded avroEvent, Acknowledgment ack) {
        PaymentRefunded event = SagaEventMapper.toDomain(avroEvent);
        SagaMdc.set(event.correlationId(), event.orderId());
        try {
            if (!idempotencyChecker.tryAcquire(event.correlationId(), SagaStepType.INVENTORY_RELEASE_PAYMENT_REFUNDED)) {
                log.warn("[SAGA-COMPENSATE] Duplicate inventory release ignored: correlationId={}", event.correlationId());
                ack.acknowledge();
                return;
            }

            log.info("[SAGA-COMPENSATE] PaymentRefunded received, releasing inventory: orderId={}", event.orderId());

            try {
                releaseInventory(event.orderId(), event.correlationId());
                ack.acknowledge();
            } catch (Exception e) {
                log.error("[SAGA-COMPENSATE] Failed to release inventory, will retry: orderId={}", event.orderId(), e);
                throw e;
            }
        } finally {
            SagaMdc.clear();
        }
    }

    /**
     * 공통 재고 복구 로직
     * RESERVED 상태인 예약을 찾아 재고를 원복하고 InventoryReleased 이벤트를 발행한다.
     */
    private void releaseInventory(String orderId, String correlationId) {
        List<Reservation> reservations = reservationRepository
                .findByOrderIdAndStatus(orderId, ReservationStatus.RESERVED);

        if (reservations.isEmpty()) {
            log.warn("[SAGA-COMPENSATE] No RESERVED reservations found for orderId={}", orderId);
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

        log.info("[SAGA-COMPENSATE] Inventory released: orderId={}, reservations={}", orderId, releasedIds);
    }
}
