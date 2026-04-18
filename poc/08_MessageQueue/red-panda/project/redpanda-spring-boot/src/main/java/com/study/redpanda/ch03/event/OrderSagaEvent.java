package com.study.redpanda.ch03.event;

import java.time.Instant;

/**
 * Ch03 SAGA Choreography: 주문 SAGA 이벤트 sealed interface
 *
 * 모든 SAGA 이벤트의 공통 계약:
 * - orderId: 어떤 주문에 대한 이벤트인지 식별
 * - correlationId: SAGA 전체 흐름을 추적하는 고유 ID (분산 추적용)
 * - timestamp: 이벤트 발생 시각
 *
 * sealed interface를 사용하는 이유:
 * - 컴파일 타임에 허용된 이벤트 타입을 제한하여 타입 안전성 확보
 * - switch 패턴 매칭에서 exhaustiveness 검사 가능 (Java 21+)
 * - SAGA에 참여하는 이벤트를 명확히 정의
 */
public sealed interface OrderSagaEvent
        permits OrderCreated, InventoryReserved, PaymentCompleted, ShippingRequested,
                InventoryReservationFailed, PaymentFailed, ShippingFailed,
                InventoryReleased, PaymentRefunded {

    String orderId();
    String correlationId();
    Instant timestamp();
}
