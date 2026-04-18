package com.study.redpanda.ch03.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;

@Configuration
public class SagaTopicConfig {

    // ─── 토픽 유형 분류 ───────────────────────────────────────────────────
    // 모든 토픽이 Event Topic 패턴이다 (발생한 사실을 기록, cleanup.policy=delete).
    // Forward 토픽: 정방향 비즈니스 이벤트 (order-created, inventory-reserved 등)
    // Compensation 토픽: 보상 트랜잭션 이벤트 (inventory-released, payment-refunded)
    // DLT 토픽: 재시도 소진 후 실패 메시지 격리 (파티션 1)
    // Entity Topic(compact)이나 Command Topic은 사용하지 않는다.

    /** Success: order placed by the customer — Forward Event */
    @Bean
    public NewTopic chapter3OrderCreatedTopic() {
        return TopicBuilder.name("chapter3.order-created")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Success: inventory service reserved items */
    @Bean
    public NewTopic chapter3InventoryReservedTopic() {
        return TopicBuilder.name("chapter3.inventory-reserved")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Success: payment service charged the customer */
    @Bean
    public NewTopic chapter3PaymentCompletedTopic() {
        return TopicBuilder.name("chapter3.payment-completed")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Success: shipping service accepted the order */
    @Bean
    public NewTopic chapter3ShippingRequestedTopic() {
        return TopicBuilder.name("chapter3.shipping-requested")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Failure: inventory service could not reserve items */
    @Bean
    public NewTopic chapter3InventoryReservationFailedTopic() {
        return TopicBuilder.name("chapter3.inventory-reservation-failed")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Failure: payment service rejected the charge */
    @Bean
    public NewTopic chapter3PaymentFailedTopic() {
        return TopicBuilder.name("chapter3.payment-failed")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Failure: shipping service could not accept the order */
    @Bean
    public NewTopic chapter3ShippingFailedTopic() {
        return TopicBuilder.name("chapter3.shipping-failed")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Compensation: inventory service released previously reserved items — Compensation Event */
    @Bean
    public NewTopic chapter3InventoryReleasedTopic() {
        return TopicBuilder.name("chapter3.inventory-released")
                .partitions(3)
                .replicas(1)
                .build();
    }

    /** Compensation: payment service refunded the customer — Compensation Event */
    @Bean
    public NewTopic chapter3PaymentRefundedTopic() {
        return TopicBuilder.name("chapter3.payment-refunded")
                .partitions(3)
                .replicas(1)
                .build();
    }

    // ─── Dead Letter Topics (DLT) ────────────────────────────────────────
    // DefaultErrorHandler가 재시도 소진 후 실패 메시지를 전송하는 토픽.
    // 보상 리스너가 구독하는 토픽 + 상태 업데이트 리스너 토픽의 DLT를 등록한다.
    // forward-flow 리스너(order-created, inventory-reserved, payment-completed)는
    // 내부에서 예외를 catch하므로 DLT에 도달하지 않지만, 예기치 않은 예외 대비용.

    @Bean
    public NewTopic chapter3PaymentFailedDlt() {
        return TopicBuilder.name("chapter3.payment-failed.DLT").partitions(1).replicas(1).build();
    }

    @Bean
    public NewTopic chapter3ShippingFailedDlt() {
        return TopicBuilder.name("chapter3.shipping-failed.DLT").partitions(1).replicas(1).build();
    }

    @Bean
    public NewTopic chapter3PaymentRefundedDlt() {
        return TopicBuilder.name("chapter3.payment-refunded.DLT").partitions(1).replicas(1).build();
    }

    @Bean
    public NewTopic chapter3ShippingRequestedDlt() {
        return TopicBuilder.name("chapter3.shipping-requested.DLT").partitions(1).replicas(1).build();
    }

    @Bean
    public NewTopic chapter3InventoryReservationFailedDlt() {
        return TopicBuilder.name("chapter3.inventory-reservation-failed.DLT").partitions(1).replicas(1).build();
    }
}
