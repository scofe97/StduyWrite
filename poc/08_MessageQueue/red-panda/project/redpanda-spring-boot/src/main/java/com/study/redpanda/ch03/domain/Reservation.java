package com.study.redpanda.ch03.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "ch03_reservations")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Reservation {

    @Id
    private String id;

    private String orderId;
    private String productId;
    private int quantity;

    @Enumerated(EnumType.STRING)
    private ReservationStatus status;
}
