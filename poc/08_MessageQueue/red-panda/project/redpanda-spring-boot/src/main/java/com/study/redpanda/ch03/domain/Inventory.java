package com.study.redpanda.ch03.domain;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "ch03_inventory")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Inventory {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(unique = true, nullable = false)
    private String productId;

    private int availableQuantity;
    private int reservedQuantity;

    public void reserve(int quantity) {
        if (availableQuantity < quantity) {
            throw new IllegalStateException("Insufficient stock for product: " + productId);
        }
        availableQuantity -= quantity;
        reservedQuantity += quantity;
    }

    public void release(int quantity) {
        if (reservedQuantity < quantity) {
            throw new IllegalStateException(
                    "Cannot release " + quantity + " for product " + productId
                    + ": only " + reservedQuantity + " reserved");
        }
        reservedQuantity -= quantity;
        availableQuantity += quantity;
    }
}
