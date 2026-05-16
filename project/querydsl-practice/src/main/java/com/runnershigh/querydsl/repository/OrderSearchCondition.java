package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.OrderStatus;
import java.time.LocalDateTime;
import lombok.Builder;
import lombok.Getter;

/**
 * 주문 동적 검색 조건 — 모든 필드 nullable.
 * 학습 노트: 01-04.동적 쿼리 — null 안전 BooleanExpression 패턴.
 */
@Getter
@Builder
public class OrderSearchCondition {
    private String memberName;
    private OrderStatus status;
    private LocalDateTime orderDateFrom;
    private LocalDateTime orderDateTo;
    private Integer minTotalAmount;
}
