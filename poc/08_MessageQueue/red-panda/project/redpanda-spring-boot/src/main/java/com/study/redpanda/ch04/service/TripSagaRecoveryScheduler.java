package com.study.redpanda.ch04.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.study.redpanda.ch04.command.CancelFlightCommand;
import com.study.redpanda.ch04.domain.OutboxEvent;
import com.study.redpanda.ch04.domain.SagaState;
import com.study.redpanda.ch04.domain.SagaStatus;
import com.study.redpanda.ch04.domain.SagaStep;
import com.study.redpanda.ch04.repository.OutboxEventRepository;
import com.study.redpanda.ch04.repository.SagaStateRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.support.TransactionTemplate;

import java.time.Duration;
import java.time.Instant;
import java.util.List;

/**
 * SAGA 타임아웃 감지 + 장애 복구 스케줄러
 *
 * 두 가지 상황을 처리한다:
 *
 * 1. 타임아웃: 서비스가 응답하지 않아 SAGA가 무한 대기하는 경우
 *    - stepStartedAt + STEP_TIMEOUT을 초과하면 보상 트리거
 *    - IN_PROGRESS 상태: 현재 단계 기반으로 보상 시작
 *    - COMPENSATING 상태: 보상 Command 재전송
 *
 * 2. Stalled 복구: Orchestrator 다운 후 재시작 시
 *    - updatedAt이 STALLED_THRESHOLD를 초과한 SAGA를 찾아 복구
 *    - 타임아웃과 동일한 로직이지만 더 긴 임계값 (Orchestrator 재시작 시간 포함)
 *
 * Outbox 패턴 적용:
 * - Command를 Kafka로 직접 전송하지 않고 Outbox 테이블에 저장
 * - TransactionTemplate 범위 내에서 SagaState + OutboxEvent 원자적 커밋
 */
@Component
@Slf4j
public class TripSagaRecoveryScheduler {

    private final SagaStateRepository sagaStateRepository;
    private final OutboxEventRepository outboxEventRepository;
    private final ObjectMapper objectMapper;
    private final TransactionTemplate transactionTemplate;

    // 단계별 타임아웃: 2분 (서비스 응답 대기 최대 시간)
    private static final Duration STEP_TIMEOUT = Duration.ofMinutes(2);

    // Stalled 임계값: 5분 (Orchestrator 다운 + 재시작 시간 포함)
    private static final Duration STALLED_THRESHOLD = Duration.ofMinutes(5);

    // Command 토픽
    private static final String FLIGHT_COMMAND_TOPIC = "chapter4.commands.flight";

    public TripSagaRecoveryScheduler(
            SagaStateRepository sagaStateRepository,
            OutboxEventRepository outboxEventRepository,
            ObjectMapper objectMapper,
            TransactionTemplate transactionTemplate) {
        this.sagaStateRepository = sagaStateRepository;
        this.outboxEventRepository = outboxEventRepository;
        this.objectMapper = objectMapper;
        this.transactionTemplate = transactionTemplate;
    }

    // ─── 타임아웃 감지 (30초마다) ────────────────────────────────────────

    /**
     * IN_PROGRESS 또는 STARTED 상태에서 stepStartedAt + STEP_TIMEOUT을 초과한 SAGA를 찾는다.
     *
     * 각 SAGA를 개별 트랜잭션으로 처리하여, OptimisticLockException 발생 시
     * 해당 SAGA만 스킵하고 나머지는 계속 처리한다.
     */
    @Scheduled(fixedDelay = 30_000)
    public void checkTimeouts() {
        Instant now = Instant.now();

        List<SagaState> activeSagas = sagaStateRepository.findByStatusIn(
                List.of(SagaStatus.IN_PROGRESS, SagaStatus.STARTED));

        for (SagaState saga : activeSagas) {
            if (saga.getStepStartedAt() == null) {
                continue;
            }

            Instant deadline = saga.getStepStartedAt().plus(STEP_TIMEOUT);
            if (now.isAfter(deadline)) {
                handleTimeoutSafely(saga.getSagaId());
            }
        }
    }

    /**
     * 개별 트랜잭션으로 타임아웃 처리. OptimisticLockException은
     * Orchestrator가 이미 해당 SAGA를 처리했음을 의미하므로 스킵한다.
     */
    private void handleTimeoutSafely(String sagaId) {
        try {
            transactionTemplate.executeWithoutResult(status -> {
                // 트랜잭션 내에서 다시 조회 (최신 상태 보장)
                SagaState saga = sagaStateRepository.findById(sagaId).orElse(null);
                if (saga == null) return;

                // 상태 재확인: Orchestrator가 이미 처리했을 수 있음
                if (saga.getStatus() != SagaStatus.IN_PROGRESS
                        && saga.getStatus() != SagaStatus.STARTED) {
                    return;
                }

                log.error("SAGA step timeout: sagaId={}, step={}, stepStartedAt={}",
                        saga.getSagaId(), saga.getCurrentStep(), saga.getStepStartedAt());
                handleTimeout(saga);
            });
        } catch (ObjectOptimisticLockingFailureException e) {
            log.info("Saga {} already updated by orchestrator, skipping timeout", sagaId);
        } catch (Exception e) {
            log.warn("Failed to handle timeout for saga {}: {}", sagaId, e.getMessage());
        }
    }

    /**
     * 타임아웃된 SAGA 처리
     *
     * - Step 1 (FLIGHT_BOOKING) 타임아웃: 보상할 것 없음 → FAILED
     * - Step 2 (HOTEL_BOOKING) 타임아웃: 항공 취소 필요 → COMPENSATING
     */
    private void handleTimeout(SagaState saga) {
        String reason = "Timeout waiting for " + saga.getCurrentStep()
                + " (exceeded " + STEP_TIMEOUT.toSeconds() + "s)";

        if (saga.getCurrentStep() == SagaStep.FLIGHT_BOOKING) {
            saga.setStatus(SagaStatus.FAILED);
            saga.setFailureReason(reason);
            saga.setFailedStep("FLIGHT_BOOKING");
            sagaStateRepository.save(saga);

            log.error("SAGA failed (timeout at Step 1, no compensation): sagaId={}",
                    saga.getSagaId());

        } else if (saga.getCurrentStep() == SagaStep.HOTEL_BOOKING) {
            saga.setStatus(SagaStatus.COMPENSATING);
            saga.setFailureReason(reason);
            saga.setFailedStep("HOTEL_BOOKING");
            sagaStateRepository.save(saga);

            log.warn("SAGA compensation triggered (timeout at Step 2): sagaId={}, " +
                    "cancelling flight reservationId={}", saga.getSagaId(), saga.getFlightReservationId());

            CancelFlightCommand cmd = new CancelFlightCommand(
                    saga.getTripId(), saga.getSagaId(), saga.getFlightReservationId());
            saveOutboxEvent(FLIGHT_COMMAND_TOPIC, saga.getSagaId(), "CancelFlightCommand", cmd);
        }
    }

    // ─── Stalled SAGA 복구 (1분마다) ────────────────────────────────────

    /**
     * Orchestrator 다운 후 재시작 시, 중단된 SAGA를 복구한다.
     *
     * 각 SAGA를 개별 트랜잭션으로 처리하여 OptimisticLockException을 격리한다.
     */
    @Scheduled(fixedDelay = 60_000)
    public void recoverStalledSagas() {
        Instant threshold = Instant.now().minus(STALLED_THRESHOLD);

        List<SagaState> stalledSagas = sagaStateRepository.findByStatusInAndUpdatedAtBefore(
                List.of(SagaStatus.COMPENSATING), threshold);

        for (SagaState saga : stalledSagas) {
            retryCompensationSafely(saga.getSagaId());
        }
    }

    /**
     * 개별 트랜잭션으로 보상 재전송.
     */
    private void retryCompensationSafely(String sagaId) {
        try {
            transactionTemplate.executeWithoutResult(status -> {
                SagaState saga = sagaStateRepository.findById(sagaId).orElse(null);
                if (saga == null) return;

                // 상태 재확인
                if (saga.getStatus() != SagaStatus.COMPENSATING) {
                    return;
                }

                log.warn("Recovering stalled SAGA: sagaId={}, currentStep={}, updatedAt={}",
                        saga.getSagaId(), saga.getCurrentStep(), saga.getUpdatedAt());

                retryCompensation(saga);
            });
        } catch (ObjectOptimisticLockingFailureException e) {
            log.info("Saga {} already updated by orchestrator, skipping recovery", sagaId);
        } catch (Exception e) {
            log.warn("Failed to recover saga {}: {}", sagaId, e.getMessage());
        }
    }

    /**
     * COMPENSATING 상태의 SAGA에 대해 보상 Command를 Outbox에 저장한다.
     */
    private void retryCompensation(SagaState saga) {
        if (saga.getFlightReservationId() != null) {
            CancelFlightCommand cmd = new CancelFlightCommand(
                    saga.getTripId(), saga.getSagaId(), saga.getFlightReservationId());
            saveOutboxEvent(FLIGHT_COMMAND_TOPIC, saga.getSagaId(), "CancelFlightCommand", cmd);

            // updatedAt 갱신 (다음 스케줄에서 다시 잡히지 않도록)
            sagaStateRepository.save(saga);

            log.info("Compensation retry saved to outbox: sagaId={}, CancelFlightCommand(reservationId={})",
                    saga.getSagaId(), saga.getFlightReservationId());
        }
    }

    // ─── 내부 헬퍼 ───────────────────────────────────────────────────────

    /**
     * Command를 Outbox 테이블에 JSON으로 저장한다.
     * TransactionTemplate 범위 내에서 호출되므로 동일 DB TX에서 커밋된다.
     */
    private void saveOutboxEvent(String topic, String sagaId,
                                  String commandType, Object command) {
        try {
            OutboxEvent event = OutboxEvent.builder()
                    .aggregateId(sagaId)
                    .topic(topic)
                    .messageKey(sagaId)
                    .commandType(commandType)
                    .payload(objectMapper.writeValueAsString(command))
                    .published(false)
                    .build();
            outboxEventRepository.save(event);
        } catch (JsonProcessingException e) {
            throw new IllegalStateException(
                    "Failed to serialize command: " + commandType, e);
        }
    }
}
