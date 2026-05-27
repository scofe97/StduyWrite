package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.Order;
import com.runnershigh.querydsl.dto.OrderSummaryDto;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

/**
 * 학습 노트:
 * - jpa/03-05.커스텀 리포지토리 패턴
 * - 01-04.동적 쿼리 (search)
 * - 01-06.페이징과 fetch join 함정 (searchPage)
 */
public interface OrderRepositoryCustom {

    /**
     * 주문 검색 — 모든 조건 동적.
     */
    List<Order> search(OrderSearchCondition condition);

    /**
     * 페치 조인 + Pageable — HHH000104 회피 패턴 실습.
     */
    Page<Order> searchPage(OrderSearchCondition condition, Pageable pageable);

    /**
     * 주문 요약 통계 — Projections.constructor 매핑 실습.
     */
    List<OrderSummaryDto> findSummaries(OrderSearchCondition condition);
}
