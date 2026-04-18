package com.study.redpanda.ch03.domain;

/**
 * SAGA 처리 단계 타입 (멱등성 키의 eventType 컴포넌트)
 *
 * 각 리스너가 처리하는 단계를 enum으로 정의하여
 * 문자열 오타/불일치를 컴파일 타임에 방지한다.
 *
 * (correlationId, SagaStepType) 복합 키로 단계별 멱등성을 보장.
 */
public enum SagaStepType {

    // === Forward Flow ===
    INVENTORY_RESERVE,
    PAYMENT_PROCESS,
    SHIPPING_PROCESS,
    ORDER_COMPLETE,

    // === Failure (상태 업데이트) ===
    ORDER_FAIL_INVENTORY,
    ORDER_FAIL_PAYMENT,
    ORDER_FAIL_SHIPPING,

    // === Compensation (보상 트랜잭션) ===
    INVENTORY_RELEASE_PAYMENT_FAILED,
    INVENTORY_RELEASE_PAYMENT_REFUNDED,
    PAYMENT_REFUND
}
