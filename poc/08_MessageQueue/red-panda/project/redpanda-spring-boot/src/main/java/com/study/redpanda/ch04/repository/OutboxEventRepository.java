package com.study.redpanda.ch04.repository;

import com.study.redpanda.ch04.domain.OutboxEvent;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.Instant;
import java.util.List;

/**
 * Outbox 이벤트 저장소
 *
 * - 폴링: 미발행 이벤트를 id 순서대로 조회 (발행 순서 보장)
 * - 정리: 발행 완료된 오래된 레코드 삭제 (테이블 비대화 방지)
 */
public interface OutboxEventRepository extends JpaRepository<OutboxEvent, Long> {

    /**
     * 미발행 이벤트를 id 오름차순으로 조회 (배치 크기는 Pageable로 제어)
     */
    List<OutboxEvent> findByPublishedFalseOrderByIdAsc(Pageable pageable);

    /**
     * 발행 완료된 오래된 레코드 삭제
     *
     * @param threshold 이 시각 이전에 발행된 레코드를 삭제
     * @return 삭제된 행 수
     */
    @Modifying
    @Query("DELETE FROM OutboxEvent e WHERE e.published = true AND e.publishedAt < :threshold")
    int deletePublishedBefore(@Param("threshold") Instant threshold);
}
