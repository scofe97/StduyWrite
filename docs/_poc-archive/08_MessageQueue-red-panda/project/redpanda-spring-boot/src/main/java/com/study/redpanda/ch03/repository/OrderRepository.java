package com.study.redpanda.ch03.repository;

import com.study.redpanda.ch03.domain.Order;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface OrderRepository extends JpaRepository<Order, String> {
    Optional<Order> findByCorrelationId(String correlationId);
}
