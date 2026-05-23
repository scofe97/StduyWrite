package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Item;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
import jakarta.persistence.OptimisticLockException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

/**
 * Ch09 — 락과 동시성 제어. 10,000건 시드 (상품 100개, 각 stock=100,000).
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import({QuerydslConfig.class, ItemRepositoryImpl.class})
class Ch09_LockingTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    @Autowired
    private ItemRepository itemRepository;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("@Version — 변경 시 version 증가")
    void version_increments_on_change() {
        Long itemId = fixture.firstItemId();

        Item before = em.find(Item.class, itemId);
        Long versionBefore = before.getVersion();

        before.decrementStock(1);
        em.flush();
        em.clear();

        Item after = em.find(Item.class, itemId);
        assertThat(after.getVersion()).isEqualTo(versionBefore + 1);
    }

    @Test
    @DisplayName("낙관 락 — stale 사본 merge 시 OptimisticLockException")
    void optimistic_lock_stale_merge_throws() {
        Long itemId = fixture.firstItemId();
        em.clear();

        Item staleSnapshot = em.find(Item.class, itemId);
        em.detach(staleSnapshot);

        Item fresh = em.find(Item.class, itemId);
        fresh.decrementStock(2);
        em.flush();
        em.clear();

        staleSnapshot.decrementStock(3);

        assertThatThrownBy(() -> {
            em.merge(staleSnapshot);
            em.flush();
        }).isInstanceOfAny(
                OptimisticLockException.class,
                org.springframework.orm.ObjectOptimisticLockingFailureException.class
        );
    }

    @Test
    @DisplayName("PESSIMISTIC_WRITE — 락 잡고 차감")
    void pessimistic_write_decrement() {
        Long itemId = fixture.firstItemId();
        em.clear();

        Item snapshot = itemRepository.findById(itemId).orElseThrow();
        int before = snapshot.getStockQuantity();
        em.clear();

        Item locked = new ItemRepositoryImpl(queryFactory)
                .lockForCheckout(itemId, 1)
                .orElseThrow();
        locked.decrementStock(1);
        em.flush();
        em.clear();

        Item after = em.find(Item.class, itemId);
        assertThat(after.getStockQuantity()).isEqualTo(before - 1);
    }

    @Test
    @DisplayName("lockForCheckout — minStock 미만이면 empty")
    void lock_for_checkout_below_min() {
        Long itemId = fixture.firstItemId();
        em.clear();

        var impl = new ItemRepositoryImpl(queryFactory);
        assertThat(impl.lockForCheckout(itemId, 1)).isPresent();
        // 시드의 stock 은 100,000 이므로 1,000,000 요청은 빈 결과
        assertThat(impl.lockForCheckout(itemId, 1_000_000)).isEmpty();
    }

    @Test
    @DisplayName("Spring Data @Lock — findByIdForUpdate")
    void spring_data_lock() {
        Long itemId = fixture.lastItemId();
        em.clear();

        Item locked = itemRepository.findByIdForUpdate(itemId).orElseThrow();
        int before = locked.getStockQuantity();
        locked.decrementStock(5);
        em.flush();
        em.clear();

        Item after = em.find(Item.class, itemId);
        assertThat(after.getStockQuantity()).isEqualTo(before - 5);
    }
}
