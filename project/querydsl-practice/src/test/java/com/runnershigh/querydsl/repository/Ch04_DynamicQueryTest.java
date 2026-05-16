package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.support.TestDataLoader;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

/**
 * Ch04 — 동적 쿼리 (학습 노트: 01-04.동적 쿼리.md)
 * <p>
 * 핵심: BooleanBuilder vs BooleanExpression null-return 패턴.
 * OrderRepositoryImpl 의 search() 가 BooleanExpression 패턴을 사용한다.
 * <p>
 * 실습:
 * - [ ] BooleanBuilder 로 같은 검색을 다시 짜 보고 가독성 비교
 * - [ ] memberName + status 두 조건 조합 시 SQL 한 번만 나가는지 확인
 * - [ ] minTotalAmount(주문 합계) 조건은 having 절이 필요 — 직접 추가해 보기
 */
@DataJpaTest
@Import({QuerydslConfig.class, OrderRepositoryImpl.class})
class Ch04_DynamicQueryTest {

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
    @DisplayName("[Green] 모든 조건 null 이면 전체 반환")
    void 모든_조건_null_이면_전체_반환() {
        var condition = OrderSearchCondition.builder().build();
        assertThat(repository.search(condition)).hasSize(3);
    }

    @Test
    @DisplayName("[Green] status=CANCELED 만 1건 반환")
    void status_CANCELED_만_1건_반환() {
        var condition = OrderSearchCondition.builder()
                .status(OrderStatus.CANCELED)
                .build();
        assertThat(repository.search(condition))
                .singleElement()
                .satisfies(o -> assertThat(o.getMember().getUsername()).isEqualTo("charlie"));
    }

    // TODO [실습 1] memberName="bob" + status=ORDERED 조합 결과 검증
    // TODO [실습 2] BooleanBuilder 버전 OrderRepositoryImpl#searchWithBuilder 를 추가하고 같은 케이스로 비교
    // TODO [실습 3] orderDateFrom/To 조건 검증 — 경계값 포함/제외 의미 확인
}
