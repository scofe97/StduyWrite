package com.study.redpanda.ch03;

import com.study.redpanda.ch03.domain.*;
import com.study.redpanda.ch03.event.PaymentFailed;
import com.study.redpanda.ch03.event.ShippingFailed;
import com.study.redpanda.ch03.event.mapper.SagaEventMapper;
import com.study.redpanda.ch03.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

/**
 * Ch03 SAGA 보상 트랜잭션 통합 테스트
 *
 * DB에 전제조건을 직접 세팅하고 실패 이벤트를 발행하여 보상 체인을 검증한다.
 * 정상 플로우 전체를 거치지 않고, 보상 리스너만 독립적으로 테스트한다.
 *
 * 시나리오 1: PaymentFailed → InventoryService가 재고 복구
 * 시나리오 2: ShippingFailed → PaymentService가 환불 → InventoryService가 재고 복구 (역순)
 *
 * 사전 조건: docker-compose up -d (Redpanda + PostgreSQL 실행 상태)
 */
@SpringBootTest
class SagaCompensationFlowTest extends AbstractSagaTest {

    @Autowired
    @Qualifier("ch03KafkaTemplate")
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private InventoryRepository inventoryRepository;

    @Autowired
    private ReservationRepository reservationRepository;

    @Autowired
    private PaymentRepository paymentRepository;

    private String testOrderId;
    private String testCorrelationId;

    @BeforeEach
    void setupTestData() {
        testOrderId = "TEST-ORDER-" + UUID.randomUUID().toString().substring(0, 8);
        testCorrelationId = UUID.randomUUID().toString();

        // 재고 원복 (이전 테스트에서 변경된 상태 초기화)
        inventoryRepository.findByProductId("PROD-001").ifPresent(inv -> {
            inv.setAvailableQuantity(100);
            inv.setReservedQuantity(0);
            inventoryRepository.save(inv);
        });

        // 주문 생성 (PENDING 상태)
        Order order = Order.builder()
                .id(testOrderId)
                .customerId("TEST-CUSTOMER")
                .totalAmount(new BigDecimal("30000"))
                .status(OrderStatus.PENDING)
                .correlationId(testCorrelationId)
                .build();
        orderRepository.save(order);
    }

    /**
     * 테스트용 재고 예약 상태를 세팅한다.
     * InventoryService.onOrderCreated가 실행된 후 상태를 시뮬레이션.
     */
    private List<String> setupReservedInventory(String productId, int reserveQty) {
        Inventory inventory = inventoryRepository.findByProductId(productId).orElseThrow();
        int originalAvailable = inventory.getAvailableQuantity();

        // 재고 예약 (available 감소, reserved 증가)
        inventory.setAvailableQuantity(originalAvailable - reserveQty);
        inventory.setReservedQuantity(inventory.getReservedQuantity() + reserveQty);
        inventoryRepository.save(inventory);

        // 예약 기록 생성
        String reservationId = UUID.randomUUID().toString();
        Reservation reservation = Reservation.builder()
                .id(reservationId)
                .orderId(testOrderId)
                .productId(productId)
                .quantity(reserveQty)
                .status(ReservationStatus.RESERVED)
                .build();
        reservationRepository.save(reservation);

        return List.of(reservationId);
    }

    @Test
    @DisplayName("결제 실패 보상: PaymentFailed → 재고 복구 (RESERVED → RELEASED)")
    void paymentFailed_inventoryReleased() {
        // Given: PROD-001에서 2개 예약된 상태 (재고 100 → available=98, reserved=2)
        setupReservedInventory("PROD-001", 2);

        // When: PaymentFailed 이벤트 발행
        PaymentFailed failedEvent = new PaymentFailed(
                testOrderId, testCorrelationId, Instant.now(),
                "INSUFFICIENT_BALANCE", "PAY_ERROR");

        kafkaTemplate.executeInTransaction(ops -> {
            ops.send("chapter3.payment-failed", SagaEventMapper.toAvro(failedEvent));
            return null;
        });

        // Then: 재고 복구 + 예약 RELEASED 확인 (available=100, reserved=0)
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Inventory inventory = inventoryRepository.findByProductId("PROD-001").orElseThrow();
                    assertThat(inventory.getAvailableQuantity()).isEqualTo(100);
                    assertThat(inventory.getReservedQuantity()).isEqualTo(0);

                    // 예약 상태도 비동기 업데이트이므로 Awaitility 안에서 검증
                    List<Reservation> reservations = reservationRepository
                            .findByOrderIdAndStatus(testOrderId, ReservationStatus.RELEASED);
                    assertThat(reservations).hasSize(1);
                });

        // Then: 주문 FAILED 확인 (OrderService.onPaymentFailed 리스너)
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Order order = orderRepository.findById(testOrderId).orElseThrow();
                    assertThat(order.getStatus()).isEqualTo(OrderStatus.FAILED);
                    assertThat(order.getFailureReason()).contains("Payment");
                });
    }

    @Test
    @DisplayName("배송 실패 보상: ShippingFailed → 환불 → 재고 복구 (역순 보상 체인)")
    void shippingFailed_paymentRefunded_thenInventoryReleased() {
        // Given: PROD-001에서 3개 예약 + 결제 완료 상태
        setupReservedInventory("PROD-001", 3);

        Payment payment = Payment.builder()
                .id(UUID.randomUUID().toString())
                .orderId(testOrderId)
                .transactionId("TXN-TEST-001")
                .amount(new BigDecimal("30000"))
                .status(PaymentStatus.COMPLETED)
                .build();
        paymentRepository.save(payment);

        // When: ShippingFailed 이벤트 발행
        ShippingFailed failedEvent = new ShippingFailed(
                testOrderId, testCorrelationId, Instant.now(),
                "DELIVERY_AREA_NOT_SUPPORTED");

        kafkaTemplate.executeInTransaction(ops -> {
            ops.send("chapter3.shipping-failed", SagaEventMapper.toAvro(failedEvent));
            return null;
        });

        // Then 1: 결제 환불 확인 (COMPLETED → REFUNDED)
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Payment refunded = paymentRepository.findByOrderId(testOrderId).orElseThrow();
                    assertThat(refunded.getStatus()).isEqualTo(PaymentStatus.REFUNDED);
                });

        // Then 2: 재고 복구 + 예약 RELEASED 확인 (역순 — 환불 후 재고 복구)
        // PaymentRefunded → InventoryService.onPaymentRefunded → InventoryReleased
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Inventory inventory = inventoryRepository.findByProductId("PROD-001").orElseThrow();
                    assertThat(inventory.getAvailableQuantity()).isEqualTo(100);
                    assertThat(inventory.getReservedQuantity()).isEqualTo(0);

                    // 예약 상태도 비동기 업데이트이므로 Awaitility 안에서 검증
                    List<Reservation> reservations = reservationRepository
                            .findByOrderIdAndStatus(testOrderId, ReservationStatus.RELEASED);
                    assertThat(reservations).hasSize(1);
                });

        // Then 3: 주문 FAILED 확인
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Order order = orderRepository.findById(testOrderId).orElseThrow();
                    assertThat(order.getStatus()).isEqualTo(OrderStatus.FAILED);
                    assertThat(order.getFailureReason()).contains("Shipping");
                });
    }
}
