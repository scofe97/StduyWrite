package com.study.redpanda.ch03.repository;

import com.study.redpanda.ch03.domain.Inventory;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface InventoryRepository extends JpaRepository<Inventory, String> {

    Optional<Inventory> findByProductId(String productId);

    /**
     * 비관적 쓰기 잠금(FOR UPDATE)으로 재고 조회
     * 동시에 같은 상품의 재고를 변경하려는 트랜잭션을 직렬화한다
     */
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT i FROM Inventory i WHERE i.productId = :productId")
    Optional<Inventory> findByProductIdWithLock(@Param("productId") String productId);
}
