package com.study.redpanda.ch04.repository;

import com.study.redpanda.ch04.domain.SagaState;
import com.study.redpanda.ch04.domain.SagaStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.Instant;
import java.util.List;

/**
 * SAGA 상태 저장소
 *
 * 장애 복구 스케줄러가 stalled SAGA를 찾는 쿼리도 포함한다.
 */
public interface SagaStateRepository extends JpaRepository<SagaState, String> {

    List<SagaState> findByTripId(String tripId);

    List<SagaState> findByStatus(SagaStatus status);

    List<SagaState> findByStatusInAndUpdatedAtBefore(
            List<SagaStatus> statuses, Instant threshold);

    List<SagaState> findByStatusIn(List<SagaStatus> statuses);
}
