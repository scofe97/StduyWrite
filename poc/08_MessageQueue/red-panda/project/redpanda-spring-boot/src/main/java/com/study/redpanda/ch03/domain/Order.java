package com.study.redpanda.ch03.domain;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.util.List;

@Entity
@Table(name = "ch03_orders")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Order {

    @Id
    private String id;

    private String customerId;

    @ElementCollection
    @CollectionTable(name = "ch03_order_items", joinColumns = @JoinColumn(name = "order_id"))
    private List<OrderLineItem> items;

    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    private String correlationId;
    private String trackingNumber;
    private String failureReason;
}
