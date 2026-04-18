package com.study.redpanda.ch04.domain;

/**
 * SAGA 전체 상태
 *
 * 상태 전이:
 *   STARTED → IN_PROGRESS → COMPLETED (정상 완료)
 *   STARTED → FAILED (Step 1 실패, 보상 불필요)
 *   IN_PROGRESS → COMPENSATING → COMPENSATED (보상 완료)
 *   COMPENSATING → FAILED (보상 실패, 수동 개입 필요)
 */
public enum SagaStatus {
    STARTED,
    IN_PROGRESS,
    COMPENSATING,
    COMPLETED,
    COMPENSATED,
    FAILED
}
