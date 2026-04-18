package com.study.redpanda.ch04.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;
import java.time.LocalDate;

/**
 * SAGA 상태 엔티티 — Orchestrator의 핵심 상태 저장소
 *
 * 각 SAGA 인스턴스의 진행 상태, 단계별 결과, 실패 정보를 영속화한다.
 * Orchestrator가 재시작되더라도 이 엔티티를 조회하여 중단된 SAGA를 복구할 수 있다.
 *
 * 설계 결정:
 * - DB 기반 상태 관리 (vs Event Sourcing): 조회 편의성과 구현 단순성 우선
 * - 각 단계의 결과를 직접 저장: 보상 시 필요한 데이터 (flightReservationId 등)
 */
@Entity
@Table(name = "ch04_saga_state")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SagaState {

    @Id
    private String sagaId;

    @Column(nullable = false)
    private String tripId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaStep currentStep;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SagaStatus status;

    // ─── 여행 요청 정보 (SAGA 시작 시 저장) ───────────────────
    private String departure;
    private String arrival;
    private LocalDate travelDate;
    private String hotelName;
    private LocalDate checkIn;
    private LocalDate checkOut;

    // ─── 각 단계의 결과 저장 (보상에 필요) ──────────────────────
    private String flightReservationId;
    private String hotelReservationId;

    // ─── 실패 정보 ──────────────────────────────────────────────
    private String failureReason;
    private String failedStep;

    // ─── 타임스탬프 ─────────────────────────────────────────────
    private Instant createdAt;
    private Instant updatedAt;
    private Instant completedAt;
    private Instant stepStartedAt;

    // ─── 낙관적 잠금 ─────────────────────────────────────────────
    @Version
    private Long version;

    @PrePersist
    void onCreate() {
        createdAt = Instant.now();
        updatedAt = Instant.now();
    }

    @PreUpdate
    void onUpdate() {
        updatedAt = Instant.now();
    }
}
