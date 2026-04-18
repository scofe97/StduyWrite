package com.study.redpanda.ch04.repository;

import com.study.redpanda.ch04.domain.ProcessedCommand;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.Instant;

/**
 * 처리 완료 Command 저장소 — preemptive acquire 패턴
 *
 * tryAcquire()가 1을 반환하면 최초 처리 → 비즈니스 로직 실행
 * tryAcquire()가 0을 반환하면 중복 → 스킵
 *
 * INSERT ... WHERE NOT EXISTS 네이티브 쿼리로
 * JPA saveAndFlush() + DataIntegrityViolationException의
 * Hibernate 세션 오염 문제를 회피한다.
 */
public interface ProcessedCommandRepository extends JpaRepository<ProcessedCommand, Long> {

    @Modifying
    @Query(value = "INSERT INTO ch04_processed_command (saga_id, command_type, processed_at) " +
            "SELECT :sagaId, :commandType, :processedAt " +
            "WHERE NOT EXISTS (" +
            "  SELECT 1 FROM ch04_processed_command " +
            "  WHERE saga_id = :sagaId AND command_type = :commandType" +
            ")",
            nativeQuery = true)
    int tryAcquire(@Param("sagaId") String sagaId,
                   @Param("commandType") String commandType,
                   @Param("processedAt") Instant processedAt);
}
