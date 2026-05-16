package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QItem.item;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.domain.Item;
import jakarta.persistence.LockModeType;
import java.util.Optional;
import lombok.RequiredArgsConstructor;

/**
 * 학습 노트: 02-05.락과 동시성 제어
 * <p>
 * QueryDSL 의 setLockMode 적용 패턴. 비관 락(PESSIMISTIC_WRITE)은 SELECT … FOR UPDATE 로,
 * 낙관 락(OPTIMISTIC)은 version 검증 의도 표명으로 동작한다.
 */
@RequiredArgsConstructor
public class ItemRepositoryImpl implements ItemRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    @Override
    public Optional<Item> lockForCheckout(Long itemId, int minStock) {
        Item result = queryFactory
                .selectFrom(item)
                .where(
                        item.id.eq(itemId),
                        item.stockQuantity.goe(minStock)
                )
                .setLockMode(LockModeType.PESSIMISTIC_WRITE)
                .fetchOne();
        return Optional.ofNullable(result);
    }

    @Override
    public Optional<Item> findWithOptimisticLock(Long itemId) {
        Item result = queryFactory
                .selectFrom(item)
                .where(item.id.eq(itemId))
                .setLockMode(LockModeType.OPTIMISTIC)
                .fetchOne();
        return Optional.ofNullable(result);
    }
}
