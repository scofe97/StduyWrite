package com.study.redpanda.ch04.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;

/**
 * Outbox 이벤트 엔티티 — Transactional Outbox 패턴
 *
 * Command를 DB 트랜잭션 내에서 outbox 테이블에 저장하고,
 * 별도 Publisher가 폴링하여 Kafka로 발행한다.
 * 이를 통해 DB 커밋과 Kafka 발행의 원자성을 보장한다.
 *
 * <pre>
 * ┌──────────────────────────────────────────────────┐
 * │ 단일 DB TX                                       │
 * │  sagaStateRepository.save(state)                 │
 * │  outboxEventRepository.save(outboxEvent)         │
 * │  → 커밋 성공 = 둘 다 저장됨                       │
 * │  → 커밋 실패 = 둘 다 롤백됨                       │
 * └──────────────────────────────────────────────────┘
 *
 * ┌──────────────────────────────────────────────────┐
 * │ OutboxPublisher (비동기 폴링)                     │
 * │  미발행 이벤트 조회 → Kafka 전송 → published=true │
 * └──────────────────────────────────────────────────┘
 * </pre>
 */
@Entity
@Table(name = "ch04_outbox_event", indexes = {
        @Index(name = "idx_outbox_published_id", columnList = "published, id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OutboxEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** sagaId — 그룹핑/추적용 */
    @Column(nullable = false)
    private String aggregateId;

    /** Kafka 대상 토픽 */
    @Column(nullable = false)
    private String topic;

    /** Kafka 메시지 키 (sagaId) */
    @Column(nullable = false)
    private String messageKey;

    /** Command 타입명: BookFlightCommand, CancelFlightCommand 등 (역직렬화 키) */
    @Column(nullable = false)
    private String commandType;

    /** JSON 직렬화된 Command */
    @Column(nullable = false, columnDefinition = "TEXT")
    private String payload;

    /** 발행 완료 여부 */
    @Column(nullable = false)
    private boolean published;

    private Instant createdAt;
    private Instant publishedAt;

    @PrePersist
    void onCreate() {
        createdAt = Instant.now();
    }
}
