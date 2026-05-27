package com.study.redpanda.ch03;

import com.study.redpanda.ch03.domain.OrderLineItem;
import com.study.redpanda.ch03.domain.OrderStatus;
import com.study.redpanda.ch03.dto.CreateOrderRequest;
import com.study.redpanda.ch03.domain.Order;
import com.study.redpanda.ch03.repository.OrderRepository;
import com.study.redpanda.ch03.repository.InventoryRepository;
import com.study.redpanda.ch03.repository.PaymentRepository;
import com.study.redpanda.ch03.repository.ShippingRepository;
import com.study.redpanda.ch03.service.OrderService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;
import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

/**
 * Ch03 SAGA 정상 플로우 통합 테스트
 *
 * 검증 시나리오:
 * 1. 주문 생성 → OrderCreated 이벤트 발행
 * 2. 재고 예약 → InventoryReserved 이벤트 발행
 * 3. 결제 처리 → PaymentCompleted 이벤트 발행
 * 4. 배송 요청 → ShippingRequested 이벤트 발행
 * 5. 주문 완료 → Order.status = COMPLETED
 *
 * 전체 체인이 Kafka 이벤트로 자율 진행되므로, Awaitility로 최종 상태를 검증한다.
 */
@SpringBootTest
class SagaNormalFlowTest extends AbstractSagaTest {

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private InventoryRepository inventoryRepository;

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private ShippingRepository shippingRepository;

    @BeforeEach
    void resetInventory() {
        // 재고 원복 (이전 테스트에서 변경된 상태 초기화)
        inventoryRepository.findByProductId("PROD-001").ifPresent(inv -> {
            inv.setAvailableQuantity(100);
            inv.setReservedQuantity(0);
            inventoryRepository.save(inv);
        });
        inventoryRepository.findByProductId("PROD-002").ifPresent(inv -> {
            inv.setAvailableQuantity(50);
            inv.setReservedQuantity(0);
            inventoryRepository.save(inv);
        });
    }

    @Test
    @DisplayName("정상 플로우: 주문 생성 → 재고 예약 → 결제 → 배송 → 주문 완료 (COMPLETED)")
    void normalFlow_orderCompletedSuccessfully() {
        // Given: 초기 재고 확인 (SagaDataInitializer가 PROD-001: 100개, PROD-002: 50개 세팅)
        assertThat(inventoryRepository.findByProductId("PROD-001")).isPresent();
        assertThat(inventoryRepository.findByProductId("PROD-002")).isPresent();

        // When: 주문 생성 (SAGA 시작)
        CreateOrderRequest request = new CreateOrderRequest(
                "CUSTOMER-001",
                List.of(
                        new OrderLineItem("PROD-001", "상품A", 2, new BigDecimal("10000")),
                        new OrderLineItem("PROD-002", "상품B", 1, new BigDecimal("20000"))
                )
        );

        Order order = orderService.createOrder(request);

        // Then: 주문이 PENDING으로 생성됨
        assertThat(order.getStatus()).isEqualTo(OrderStatus.PENDING);
        assertThat(order.getCorrelationId()).isNotNull();

        // Then: SAGA 체인이 완료될 때까지 대기 (최대 30초)
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Order completed = orderRepository.findById(order.getId()).orElseThrow();
                    assertThat(completed.getStatus()).isEqualTo(OrderStatus.COMPLETED);
                    assertThat(completed.getTrackingNumber()).isNotNull();
                });

        // Then: DB에 각 단계의 결과가 저장되어 있는지 검증
        // 재고 차감 확인
        var inventory1 = inventoryRepository.findByProductId("PROD-001").orElseThrow();
        assertThat(inventory1.getAvailableQuantity()).isEqualTo(98);  // 100 - 2
        assertThat(inventory1.getReservedQuantity()).isEqualTo(2);

        var inventory2 = inventoryRepository.findByProductId("PROD-002").orElseThrow();
        assertThat(inventory2.getAvailableQuantity()).isEqualTo(49);  // 50 - 1
        assertThat(inventory2.getReservedQuantity()).isEqualTo(1);

        // 결제 기록 확인
        var payment = paymentRepository.findByOrderId(order.getId()).orElseThrow();
        assertThat(payment.getAmount()).isEqualByComparingTo(new BigDecimal("40000"));  // 10000*2 + 20000*1
        assertThat(payment.getTransactionId()).startsWith("TXN-");

        // 배송 기록 확인
        var shipping = shippingRepository.findByOrderId(order.getId()).orElseThrow();
        assertThat(shipping.getTrackingNumber()).startsWith("TRACK-");
    }

    @Test
    @DisplayName("재고 부족: 존재하지 않는 상품 주문 → 주문 실패 (FAILED)")
    void inventoryFailed_orderMarkedAsFailed() {
        // When: 존재하지 않는 상품으로 주문
        CreateOrderRequest request = new CreateOrderRequest(
                "CUSTOMER-002",
                List.of(new OrderLineItem("PROD-999", "없는상품", 1, new BigDecimal("5000")))
        );

        Order order = orderService.createOrder(request);

        // Then: SAGA 실패 → 주문 FAILED
        await().atMost(30, TimeUnit.SECONDS)
                .pollInterval(500, TimeUnit.MILLISECONDS)
                .untilAsserted(() -> {
                    Order failed = orderRepository.findById(order.getId()).orElseThrow();
                    assertThat(failed.getStatus()).isEqualTo(OrderStatus.FAILED);
                    assertThat(failed.getFailureReason()).contains("Inventory");
                });
    }
}
