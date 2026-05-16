package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.Item;
import jakarta.persistence.LockModeType;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

/**
 * 학습 노트: 02-05.락과 동시성 제어.md
 * <p>
 * Spring Data 의 @Lock 어노테이션 데모. 메서드 시그니처에 락 모드를 박아 두는 패턴.
 */
public interface ItemRepository extends JpaRepository<Item, Long>, ItemRepositoryCustom {

    /**
     * 비관 락 — SELECT … FOR UPDATE.
     * @Lock 만으로는 메서드 이름 파생 쿼리에 안전하게 적용되지 않을 수 있어 @Query 와 함께 둔다.
     */
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("select i from Item i where i.id = :id")
    Optional<Item> findByIdForUpdate(@Param("id") Long id);
}
