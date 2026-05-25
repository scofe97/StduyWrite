package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.querydsl.core.types.dsl.Expressions;
import com.querydsl.jpa.JPAExpressions;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
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
 * Ch10 — JPAExpressions 서브쿼리 합성 (학습 노트: 02-02).
 * 스칼라 서브쿼리 / EXISTS / IN / 상관 서브쿼리.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch10_JPAExpressionsTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("IN 서브쿼리 — CANCELED 주문의 회원만")
    void in_subquery_canceled_member_ids() {
        Long count = queryFactory
                .select(member.count())
                .from(member)
                .where(member.id.in(
                        JPAExpressions
                                .select(order.member.id)
                                .from(order)
                                .where(order.status.eq(OrderStatus.CANCELED))
                ))
                .fetchOne();

        assertThat(count).isEqualTo(fixture.canceledCount());
    }

    @Test
    @DisplayName("EXISTS — 주문이 있는 회원 (전부)")
    void exists_members_with_order() {
        Long count = queryFactory
                .select(member.count())
                .from(member)
                .where(
                        JPAExpressions.selectOne()
                                .from(order)
                                .where(order.member.eq(member))
                                .exists()
                )
                .fetchOne();

        assertThat(count).isEqualTo(fixture.memberCount());
    }

    @Test
    @DisplayName("스칼라 서브쿼리 — 주문 1건당 그 주문항목 합계")
    void scalar_subquery_order_total() {
        var rows = queryFactory
                .select(
                        order.id,
                        JPAExpressions
                                .select(Expressions.numberTemplate(Long.class,
                                        "coalesce(sum({0} * {1}), 0)",
                                        orderItem.orderPrice, orderItem.count))
                                .from(orderItem)
                                .where(orderItem.order.eq(order))
                )
                .from(order)
                .limit(5)
                .fetch();

        assertThat(rows).hasSize(5);
        assertThat(rows).allSatisfy(t -> assertThat(t.get(1, Long.class)).isPositive());
    }

    // === 실습 (노트 02-02: 상관 서브쿼리 / NOT EXISTS / 스칼라 LIMIT 1) ===

    @Test
    @DisplayName("실습1: 상관 서브쿼리 — 자기 주문의 항목합계가 전체 평균보다 큰 주문")
    void correlated_subquery_above_average_total() {
        // 상관 서브쿼리: 바깥 order 의 항목합계 — orderItem.order.eq(order) 가 외부 order 직접 참조.
        // sum(price*count) 은 PG 에서 bigint → Long. avg 와 비교하려면 Double 로 맞춘다.
        var perOrderTotal = JPAExpressions
                .select(Expressions.numberTemplate(Double.class,
                        "coalesce(sum({0} * {1}), 0)",
                        orderItem.orderPrice, orderItem.count))
                .from(orderItem)
                .where(orderItem.order.eq(order));        // ← 외부 order 직접 참조 (상관)

        // 비교 기준: 전체 주문항목의 평균 (price * count) — 상관 아닌 독립 서브쿼리. avg 는 Double.
        var avgItemTotal = JPAExpressions
                .select(orderItem.orderPrice.multiply(orderItem.count).avg())
                .from(orderItem);

        var rows = queryFactory
                .select(order.id)
                .from(order)
                .where(perOrderTotal.gt(avgItemTotal))     // 상관 서브쿼리 > 독립 서브쿼리
                .fetch();

        // 평균보다 큰 주문은 일부만 (전부도 0도 아님).
        assertThat(rows).isNotEmpty();
        assertThat(rows.size()).isLessThan((int) fixture.memberCount());
    }

    @Test
    @DisplayName("실습2: NOT EXISTS — 주문이 없는 회원 (시드엔 0명)")
    void not_exists_members_without_order() {
        Long count = queryFactory
                .select(member.count())
                .from(member)
                .where(
                        JPAExpressions.selectOne()
                                .from(order)
                                .where(order.member.eq(member))
                                .notExists()
                )
                .fetchOne();

        // 시드는 회원 1:1 주문이라 주문 없는 회원은 0명. NOT EXISTS 문법 검증.
        assertThat(count).isZero();
    }

    @Test
    @DisplayName("실습3: sub-query LIMIT 의 함정 — orderBy+limit(1) 스칼라 서브쿼리는 PG 에서 평탄화 실패")
    void scalar_subquery_limit_is_environment_dependent() {
        // 노트 02-02 § JPA QueryDSL 의 제약: sub-query 의 LIMIT 은 환경 의존적이다.
        // PostgreSQL 에서는 아래 orderBy+limit(1) 스칼라 서브쿼리가 평탄화되지 않아
        // "more than one row returned by a subquery" 로 실패한다 (LIMIT 이 안 먹음).
        assertThatThrownBy(() ->
                queryFactory
                        .select(JPAExpressions
                                .select(orderItem.orderPrice)
                                .from(orderItem)
                                .orderBy(orderItem.orderPrice.desc())
                                .limit(1L))
                        .from(order)
                        .limit(1)
                        .fetchFirst()
        ).isInstanceOf(Exception.class);
    }

    @Test
    @DisplayName("실습4: LIMIT 우회 — max() 집계 스칼라 서브쿼리로 '가장 비싼 주문항목 가격'")
    void scalar_subquery_max_avoids_limit() {
        // 노트의 권장 우회: LIMIT 1 대신 max() 집계 — 단일 행이 보장돼 평탄화 안전.
        Integer maxPrice = queryFactory
                .select(JPAExpressions
                        .select(orderItem.orderPrice.max())
                        .from(orderItem))
                .from(order)
                .limit(1)
                .fetchFirst();

        assertThat(maxPrice).isNotNull();
        assertThat(maxPrice).isPositive();
    }
}
