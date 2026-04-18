package com.study.redpanda.ch03.service;

import com.study.redpanda.ch03.domain.SagaStepType;
import com.study.redpanda.ch03.repository.ProcessedEventRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.UUID;

/**
 * 선점 방식(preemptive acquire) 멱등성 체커
 *
 * 기존 check-then-act 패턴의 문제:
 * - isDuplicate() 후 비즈니스 로직 실행 후 markProcessed() → 사이에 동시성 갭
 * - markProcessed()에서 DataIntegrityViolationException → 트랜잭션 rollback-only 오염
 * - 실패 경로에서 markProcessed 누락 → 실패 이벤트 중복 발행
 *
 * 선점 방식:
 * 1. tryAcquire()가 조회 + INSERT를 원자적으로 수행 (비즈니스 로직 전)
 * 2. INSERT ... WHERE NOT EXISTS 네이티브 쿼리 → 예외 없음, 트랜잭션 오염 없음
 * 3. 호출자의 @Transactional에 참여 → 비즈니스 로직 실패 시 함께 롤백 → 재시도 가능
 *
 * 사용 패턴:
 * if (!idempotencyChecker.tryAcquire(correlationId, SagaStepType.INVENTORY_RESERVE)) {
 *     ack.acknowledge();
 *     return;  // 중복 → 무시
 * }
 * // 비즈니스 로직 (실패 시 @Transactional 롤백 → ProcessedEvent도 롤백)
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class EventIdempotencyChecker {

    private final ProcessedEventRepository processedEventRepository;

    /**
     * 멱등성 선점 시도.
     * 비즈니스 로직 실행 전에 호출하여 처리 권한을 "선점"한다.
     *
     * @return true = 선점 성공 (진행), false = 이미 처리됨 (스킵)
     */
    public boolean tryAcquire(String correlationId, SagaStepType stepType) {
        // 1차: 빠른 SELECT 조회 (대부분의 중복을 여기서 차단 — DB 부하 최소화)
        if (processedEventRepository.existsByCorrelationIdAndEventType(correlationId, stepType)) {
            log.debug("[IDEMPOTENCY] Already processed: correlationId={}, stepType={}",
                    correlationId, stepType);
            return false;
        }

        // 2차: INSERT ... WHERE NOT EXISTS (동시성 안전, 트랜잭션 오염 없음)
        // 네이티브 쿼리는 enum을 직접 처리할 수 없으므로 .name() 으로 문자열 전달
        int inserted = processedEventRepository.insertIfAbsent(
                UUID.randomUUID().toString(), correlationId, stepType.name(), Instant.now());

        if (inserted == 0) {
            log.warn("[IDEMPOTENCY] Concurrent duplicate detected: correlationId={}, stepType={}",
                    correlationId, stepType);
        }

        return inserted > 0;
    }
}
