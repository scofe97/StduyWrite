package com.runnershigh.tps.domain.common;

import com.runnershigh.tps.infrastructure.util.UuidGenerator;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * 모든 도메인 엔티티의 기본 클래스
 *
 * <p>공통 필드(id, 생성/수정 시간, 감사 정보)를 제공합니다.</p>
 *
 * <h2>UUID v7 사용</h2>
 * <p>id 필드는 UUID v7(시간 기반 순차 UUID)을 사용합니다.
 * 이는 B-Tree 인덱스 성능을 크게 향상시킵니다.</p>
 *
 * @see UuidGenerator
 */
@Getter
@Setter
public abstract class BaseEntity {
    private UUID id;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String createdBy;
    private String updatedBy;

    /**
     * 새로운 엔티티 생성 (UUID v7 자동 할당)
     */
    protected BaseEntity() {
        this.id = UuidGenerator.generate();  // UUID v7 (순차적)
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    protected BaseEntity(UUID id) {
        this.id = id;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public void updateTimestamp() {
        this.updatedAt = LocalDateTime.now();
    }
}
