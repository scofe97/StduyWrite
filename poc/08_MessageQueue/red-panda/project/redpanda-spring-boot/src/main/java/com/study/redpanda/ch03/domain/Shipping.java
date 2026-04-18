package com.study.redpanda.ch03.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "ch03_shipments")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Shipping {

    @Id
    private String id;

    private String orderId;
    private String trackingNumber;

    @Enumerated(EnumType.STRING)
    private ShippingStatus status;
}
