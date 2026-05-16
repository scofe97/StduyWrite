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
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

/**
 * Ch09 — 락과 동시성 제어 (학습 노트: 02-05.락과 동시성 제어.md)
 * <p>
 * 핵심:
 * - @Version 필드의 stale-write 감지 (낙관)
 * - QueryDSL setLockMode(PESSIMISTIC_WRITE) — SELECT … FOR UPDATE 발행 (비관)
 * - Spring Data @Lock 어노테이션 — 메서드 시그니처에 락 모드 박기
 * <p>
 * 실습:
 * - [ ] SQL 로그에서 update 의 where 절에 version 컬럼이 들어가는지 확인
 * - [ ] PESSIMISTIC_WRITE 호출 시 발행되는 SQL 에 'for update' 가 포함되는지 확인
 * - [ ] @Retryable 또는 명시적 루프로 OptimisticLockException 재시도 패턴 추가
 * - [ ] @SpringBootTest + ExecutorService 로 두 스레드 동시 차감 시나리오 재현
 */
@DataJpaTest
@Import({QuerydslConfig.class, ItemRepositoryImpl.class})
class Ch09_LockingTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    @Autowired
    private ItemRepository itemRepository;

    private Fixture fixture;

    @BeforeEach
    void setUp() {
        fixture = new TestDataLoader(em).loadDefault();
    }

    @Test
    @DisplayName("[Green] @Version 은 신규 엔티티에 0 으로 시작해 변경 시 1씩 증가한다")
    void Version_은_신규_엔티티에_0_으로_시작해_변경_시_1씩_증가한다() {
        Long itemId = fixture.javaBook().getId();

        Item before = em.find(Item.class, itemId);
        Long versionBefore = before.getVersion();

        before.decrementStock(1);
        em.flush();

        em.clear();
        Item after = em.find(Item.class, itemId);
        assertThat(after.getVersion()).isEqualTo(versionBefore + 1);
        assertThat(after.getStockQuantity()).isEqualTo(before.getStockQuantity());
    }

    @Test
    @DisplayName("[Red] 낙관 락 — stale 사본을 merge 후 flush 시 OptimisticLockException")
    void 낙관_락_stale_사본을_merge_후_flush_시_OptimisticLockException() {
        Long itemId = fixture.javaBook().getId();
        em.clear();

        // T1 의 시점에서 본 사본 (version=N)
        Item staleSnapshot = em.find(Item.class, itemId);
        em.detach(staleSnapshot);

        // T2 가 같은 row 를 변경 → version=N+1
        Item fresh = em.find(Item.class, itemId);
        fresh.decrementStock(2);
        em.flush();
        em.clear();

        // T1 이 자기 사본으로 다시 변경 시도. Hibernate 6 은 merge 시점에 version 비교 후 즉시 예외를 던진다.
        // (구버전은 flush 시점에 발화 — 동작 시점은 구현 상세이고 의미는 동일하다.)
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
    @DisplayName("[Green] QueryDSL setLockMode(PESSIMISTIC_WRITE) 로 락을 잡고 차감")
    void QueryDSL_setLockMode_PESSIMISTIC_WRITE_로_락을_잡고_차감() {
        Long itemId = fixture.javaBook().getId();
        em.clear();

        Item locked = itemRepository.findById(itemId).orElseThrow();
        int before = locked.getStockQuantity();
        em.clear();

        // SQL 로그에서 'for update' 가 포함된 select 가 발행되는지 확인할 수 있다.
        Item lockedForCheckout = new ItemRepositoryImpl(queryFactory)
                .lockForCheckout(itemId, 1)
                .orElseThrow();

        lockedForCheckout.decrementStock(1);
        em.flush();
        em.clear();

        Item after = em.find(Item.class, itemId);
        assertThat(after.getStockQuantity()).isEqualTo(before - 1);
    }

    @Test
    @DisplayName("[Green] lockForCheckout 은 minStock 미만이면 빈 결과를 돌린다")
    void lockForCheckout_은_minStock_미만이면_빈_결과를_돌린다() {
        Long itemId = fixture.apple().getId(); // stockQuantity=500
        em.clear();

        var impl = new ItemRepositoryImpl(queryFactory);
        assertThat(impl.lockForCheckout(itemId, 100)).isPresent();
        assertThat(impl.lockForCheckout(itemId, 1_000)).isEmpty();
    }

    @Test
    @DisplayName("[Green] Spring Data @Lock — findByIdForUpdate 메서드 동작")
    void Spring_Data_Lock_findByIdForUpdate_메서드_동작() {
        Long itemId = fixture.kotlinBook().getId(); // stockQuantity=50
        em.clear();

        Item locked = itemRepository.findByIdForUpdate(itemId).orElseThrow();
        locked.decrementStock(5);
        em.flush();
        em.clear();

        Item after = em.find(Item.class, itemId);
        assertThat(after.getStockQuantity()).isEqualTo(45);
    }

    // TODO [실습 1] 낙관 락 + @Retryable 결합 — 충돌 발생 시 자동 재시도 코드 작성
    // TODO [실습 2] 두 상품을 한 트랜잭션에서 차감할 때 itemId 오름차순 락 획득 패턴 검증
    // TODO [실습 3] @SpringBootTest 로 ExecutorService + CountDownLatch 동시성 시나리오 재현
    // TODO [실습 4] PostgreSQL 컨테이너(Testcontainers)로 'for update' SQL 직접 확인
}
