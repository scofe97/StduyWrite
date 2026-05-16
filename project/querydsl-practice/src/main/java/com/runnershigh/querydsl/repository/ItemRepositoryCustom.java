package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.Item;
import java.util.Optional;

/**
 * 학습 노트: 02-05.락과 동시성 제어 — QueryDSL setLockMode 데모.
 * 동적 조건 + 락을 결합하고 싶을 때 자연스러운 진입점.
 */
public interface ItemRepositoryCustom {

    /**
     * 비관 락 + 추가 조건(최소 재고 보장)을 한 쿼리에 결합한다.
     * 같은 락을 도메인 규칙 안에서 표현하고 싶을 때.
     */
    Optional<Item> lockForCheckout(Long itemId, int minStock);

    /**
     * 낙관적 락 강제 적용 — version 비교 의도를 명시.
     * 단순 조회와 의미적으로 같지만, 호출처에서 "이 흐름은 충돌 감지가 핵심" 임을 드러낸다.
     */
    Optional<Item> findWithOptimisticLock(Long itemId);
}
