package com.study.redpanda.ch03.repository;

import com.study.redpanda.ch03.domain.Reservation;
import com.study.redpanda.ch03.domain.ReservationStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ReservationRepository extends JpaRepository<Reservation, String> {
    List<Reservation> findByOrderIdAndStatus(String orderId, ReservationStatus status);
    List<Reservation> findByOrderId(String orderId);
}
