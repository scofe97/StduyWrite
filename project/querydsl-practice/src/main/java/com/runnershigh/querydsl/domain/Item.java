package com.runnershigh.querydsl.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Version;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Item {

    @Id
    @GeneratedValue
    @Column(name = "item_id")
    private Long id;

    @Column(nullable = false)
    private String name;

    private int price;

    private int stockQuantity;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;

    /**
     * 낙관적 락 — 학습 노트 02-05.락과 동시성 제어.md 참고.
     * JPA 가 update 시 where 절에 version 을 끼워 충돌을 감지한다.
     */
    @Version
    private Long version;

    @Builder
    private Item(String name, int price, int stockQuantity, Category category) {
        this.name = name;
        this.price = price;
        this.stockQuantity = stockQuantity;
        this.category = category;
    }

    /**
     * 재고 차감 — 음수 가드 포함.
     * 호출처는 적절한 락 전략(@Version 낙관 또는 PESSIMISTIC_WRITE 비관)을 선택해야 한다.
     */
    public void decrementStock(int amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be positive: " + amount);
        }
        if (this.stockQuantity < amount) {
            throw new IllegalStateException(
                "insufficient stock: requested=" + amount + ", available=" + stockQuantity
            );
        }
        this.stockQuantity -= amount;
    }
}
