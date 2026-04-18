package com.study.redpanda.ch03.dto;

import com.study.redpanda.ch03.domain.OrderLineItem;

import java.util.List;

public record CreateOrderRequest(
        String customerId,
        List<OrderLineItem> items
) {}
