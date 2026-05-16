package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.support.TestDataLoader;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;

/**
 * Ch06 — 페이징과 fetch join 함정 (학습 노트: 01-06.페이징과 fetch join 함정.md)
 * <p>
 * 핵심: HHH000104 경고, distinct, count 쿼리 분리, @BatchSize.
 * <p>
 * 실습:
 * - [ ] OrderRepositoryImpl#searchPage 가 컬렉션 fetch join 없이 동작하는지 SQL 로그로 확인
 * - [ ] 일부러 fetch join + Pageable 코드를 작성해 HHH000104 메시지 재현
 * - [ ] OrderItem 에 @BatchSize 를 붙이고 N+1 → IN 절 묶임 비교
 * - [ ] PageableExecutionUtils 가 count 쿼리를 언제 생략하는지 (마지막 페이지 미만 케이스)
 */
@DataJpaTest
@Import({QuerydslConfig.class, OrderRepositoryImpl.class})
class Ch06_PagingAndFetchJoinTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private OrderRepositoryImpl repository;

    @BeforeEach
    void setUp() {
        new TestDataLoader(em).loadDefault();
        repository = new OrderRepositoryImpl(queryFactory);
    }

    @Test
    @DisplayName("[Green] searchPage 는 PageRequest 페이지 크기를 지킨다")
    void searchPage_는_PageRequest_페이지_크기를_지킨다() {
        var condition = OrderSearchCondition.builder().build();
        Page<?> page = repository.searchPage(condition, PageRequest.of(0, 2));

        assertThat(page.getTotalElements()).isEqualTo(3);
        assertThat(page.getContent()).hasSize(2);
        assertThat(page.getTotalPages()).isEqualTo(2);
    }

    // TODO [실습 1] fetch join 으로 컬렉션을 페이징 시도 → 콘솔에 HHH000104 출력되는지 확인
    // TODO [실습 2] @BatchSize(size = 50) 를 Order.orderItems 에 적용해 N+1 차이 측정
    // TODO [실습 3] count 쿼리 발생 여부 확인 — PageableExecutionUtils 의 최적화 케이스 정리
}
