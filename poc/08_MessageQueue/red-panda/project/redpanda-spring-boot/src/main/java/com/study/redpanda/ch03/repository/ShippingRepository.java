package com.study.redpanda.ch03.repository;

import com.study.redpanda.ch03.domain.Shipping;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ShippingRepository extends JpaRepository<Shipping, String> {
    Optional<Shipping> findByOrderId(String orderId);
}
