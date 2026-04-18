package com.study.redpanda.ch03.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;

/**
 * 멱등성 보장을 위한 처리 완료 이벤트 기록
 *
 * (correlationId, eventType) 조합의 유니크 제약으로
 * 같은 이벤트가 여러 번 도착해도 한 번만 처리되도록 보장한다.
 *
 * 동작 원리:
 * 1. 리스너가 이벤트를 받으면 먼저 이 테이블을 조회
 * 2. 이미 처리된 이벤트면 무시 (ack만 수행)
 * 3. 처리 완료 후 이 테이블에 기록 (같은 JPA 트랜잭션)
 * 4. 유니크 제약이 최종 안전망 (동시 처리 시 하나만 성공)
 */
@Entity
@Table(name = "ch03_processed_events",
       uniqueConstraints = @UniqueConstraint(
               name = "uk_correlation_event_type",
               columnNames = {"correlationId", "eventType"}))
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProcessedEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(nullable = false)
    private String correlationId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaStepType eventType;

    @Column(nullable = false)
    private Instant processedAt;
}
