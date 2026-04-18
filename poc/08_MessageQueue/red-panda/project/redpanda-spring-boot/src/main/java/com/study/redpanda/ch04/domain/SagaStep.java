package com.study.redpanda.ch04.domain;

/**
 * SAGA 진행 단계
 *
 * Orchestrator가 현재 어떤 단계를 실행 중인지 추적한다.
 * 장애 복구 시 currentStep을 기준으로 재시도 또는 보상 방향을 결정한다.
 */
public enum SagaStep {
    FLIGHT_BOOKING,
    HOTEL_BOOKING,
    COMPLETED
}
