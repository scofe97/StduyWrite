package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;
import static org.assertj.core.api.Assertions.assertThat;

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
}
