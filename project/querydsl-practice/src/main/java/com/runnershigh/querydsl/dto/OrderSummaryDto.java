package com.runnershigh.querydsl.dto;

import com.runnershigh.querydsl.domain.OrderStatus;
import java.time.LocalDateTime;

/**
 * 주문 요약 — Projections.constructor 또는 Projections.fields 로 매핑.
 * 학습 노트: 01-05 프로젝션과 DTO 매핑.
 * <p>
 * 일부러 @QueryProjection 을 쓰지 않는다. Projections.constructor / fields / bean 차이를
 * 직접 비교 실습할 수 있도록 한다.
 */
public class OrderSummaryDto {

    private Long orderId;
    private String memberName;
    private LocalDateTime orderDate;
    private OrderStatus status;
    private int totalAmount;

    public OrderSummaryDto() {}

    public OrderSummaryDto(Long orderId, String memberName, LocalDateTime orderDate, OrderStatus status, int totalAmount) {
        this.orderId = orderId;
        this.memberName = memberName;
        this.orderDate = orderDate;
        this.status = status;
        this.totalAmount = totalAmount;
    }

    public Long getOrderId() { return orderId; }
    public String getMemberName() { return memberName; }
    public LocalDateTime getOrderDate() { return orderDate; }
    public OrderStatus getStatus() { return status; }
    public int getTotalAmount() { return totalAmount; }

    public void setOrderId(Long orderId) { this.orderId = orderId; }
    public void setMemberName(String memberName) { this.memberName = memberName; }
    public void setOrderDate(LocalDateTime orderDate) { this.orderDate = orderDate; }
    public void setStatus(OrderStatus status) { this.status = status; }
    public void setTotalAmount(int totalAmount) { this.totalAmount = totalAmount; }
}
