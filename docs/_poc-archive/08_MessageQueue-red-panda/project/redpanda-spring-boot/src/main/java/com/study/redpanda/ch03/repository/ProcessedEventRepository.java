package com.study.redpanda.ch03.repository;

import com.study.redpanda.ch03.domain.ProcessedEvent;
import com.study.redpanda.ch03.domain.SagaStepType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.Instant;
import java.util.List;

public interface ProcessedEventRepository extends JpaRepository<ProcessedEvent, String> {
    boolean existsByCorrelationIdAndEventType(String correlationId, SagaStepType eventType);
    List<ProcessedEvent> findByCorrelationId(String correlationId);

    /**
     * 트랜잭션 오염 없는 조건부 INSERT.
     * 레코드가 이미 존재하면 0 반환 (예외 없음), 신규면 1 반환.
     * DataIntegrityViolationException을 발생시키지 않으므로 호출자의 @Transactional이 오염되지 않는다.
     */
    @Modifying
    @Query(nativeQuery = true, value =
            "INSERT INTO ch03_processed_events (id, correlation_id, event_type, processed_at) " +
            "SELECT :id, :correlationId, :eventType, :processedAt " +
            "WHERE NOT EXISTS (" +
            "  SELECT 1 FROM ch03_processed_events " +
            "  WHERE correlation_id = :correlationId AND event_type = :eventType)")
    int insertIfAbsent(@Param("id") String id,
                       @Param("correlationId") String correlationId,
                       @Param("eventType") String eventType,
                       @Param("processedAt") Instant processedAt);
}
