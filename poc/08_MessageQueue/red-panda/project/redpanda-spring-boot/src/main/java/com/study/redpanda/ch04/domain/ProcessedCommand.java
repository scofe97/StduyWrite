package com.study.redpanda.ch04.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;

/**
 * Handler 측 멱등성 보장을 위한 처리 완료 Command 기록
 *
 * Orchestrator가 장애 복구 시 동일 Command를 재전송할 수 있다.
 * Handler는 (sagaId, commandType) 복합 키로 중복 처리를 방지한다.
 *
 * Ch03의 ProcessedEvent와 동일한 preemptive acquire 패턴:
 * INSERT ... WHERE NOT EXISTS → 0이면 이미 처리됨 → 스킵
 */
@Entity
@Table(name = "ch04_processed_command",
        uniqueConstraints = @UniqueConstraint(
                name = "uk_processed_command_saga_type",
                columnNames = {"sagaId", "commandType"}))
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProcessedCommand {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String sagaId;

    @Column(nullable = false)
    private String commandType;

    @Column(nullable = false)
    private Instant processedAt;
}
