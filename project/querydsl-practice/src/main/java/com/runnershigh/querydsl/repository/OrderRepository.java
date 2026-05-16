package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long>, OrderRepositoryCustom {
}
