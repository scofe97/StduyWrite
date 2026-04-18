package com.study.redpanda.ch03.domain;

import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * 주문 항목 (Order 엔티티의 @ElementCollection 대상)
 * OrderCreated.OrderItem(이벤트)과 분리된 도메인 모델
 */
@Embeddable
@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderLineItem {
    private String productId;
    private String productName;
    private int quantity;
    private BigDecimal price;
}
