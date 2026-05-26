package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QItem.item;
import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.types.ExpressionUtils;
import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.CaseBuilder;
import com.querydsl.core.types.dsl.Expressions;
import com.querydsl.core.types.dsl.NumberExpression;
import com.querydsl.jpa.JPAExpressions;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.dto.OrderSummaryDto;
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
 * Ch11 — 정렬·집계·프로젝션 보충 (학습 노트: 02-03).
 * countDistinct, CASE 기반 정렬 (NULLS LAST 대체), tie-breaker.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("log4jdbc")
@Import(QuerydslConfig.class)
class Ch11_SortingAggregationProjectionTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("countDistinct — 도시는 4개")
    void count_distinct_cities() {
        Long distinctCities = queryFactory
                .select(member.address.city.countDistinct())
                .from(member)
                .fetchOne();

        assertThat(distinctCities).isEqualTo(4);
    }

    @Test
    @DisplayName("CASE 기반 정렬 — CANCELED 우선 노출")
    void case_order_canceled_first() {

        OrderSpecifier<?> canceledFirst = new CaseBuilder()
                .when(order.status.eq(OrderStatus.CANCELED)).then(0)
                .when(order.status.eq(OrderStatus.COMPLETED)).then(1)
                .otherwise(2)
                .asc();

        var rows = queryFactory
                .selectFrom(order)
                .orderBy(canceledFirst, order.id.asc())
                .limit(5)
                .fetch();

        // 상위 5건 모두 CANCELED 여야 함 — CANCELED 가 1,000건 있으므로 첫 5건은 전부 CANCELED
        assertThat(rows).allSatisfy(o -> assertThat(o.getStatus()).isEqualTo(OrderStatus.CANCELED));
    }

    @Test
    @DisplayName("집계 — 도시별 회원 수 (모두 균등)")
    void group_by_city_uniform() {
        var rows = queryFactory
                .select(member.address.city, member.count())
                .from(member)
                .groupBy(member.address.city)
                .fetch();

        long perCity = fixture.memberCount() / 4;
        assertThat(rows).hasSize(4);
        assertThat(rows).allSatisfy(t ->
                assertThat(t.get(member.count())).isEqualTo(perCity));
    }

    // === 실습 (노트 02-03: NULLS LAST API / countDistinct 부풀림 / ExpressionUtils.as) ===

    @Test
    @DisplayName("실습1: .nullsLast() API — NULL 을 인위 생성한 정렬 키로 NULL 을 뒤로 민다")
    void nulls_last_api_pushes_null_to_tail() {
        // 노트 02-03 § 형태 1: .nullsLast() 는 '같은 컬럼 정렬 방향'에 NULL 위치를 붙인다.
        // 시드 email 은 전부 non-null 이라, 짝수 id 를 NULL 로 매핑한 표현식을 만들어 실증한다.
        // (id % 2 == 0 → NULL, 홀수 → age). NULL 인 행이 .nullsLast() 로 뒤로 가는지 확인.
        // CaseBuilder.then(null) 은 ConstantImpl 이 null 을 거부(NPE)하고,
        // nullExpression() 은 SimpleExpression 이라 otherwise(number) 와 공통 타입이 NumberExpression 으로
        // 안 떨어진다. numberTemplate(Integer.class, "null") 로 NULL 을 number 타입 표현식으로 만든다.
        NumberExpression<Integer> ageOrNull = new CaseBuilder()
                .when(member.id.mod(2L).eq(0L))
                .then(Expressions.numberTemplate(Integer.class, "null"))
                .otherwise(member.age);

        var rows = queryFactory
                .select(member.id, ageOrNull)
                .from(member)
                .orderBy(ageOrNull.asc().nullsLast(), member.id.asc())
                .fetch();

        // 앞쪽은 NOT NULL(홀수 id), NULL 행은 전부 꼬리로. 마지막 행은 NULL 이어야 한다.
        assertThat(rows.get(0).get(1, Integer.class)).isNotNull();
        assertThat(rows.get(rows.size() - 1).get(1, Integer.class)).isNull();
        // NULL 이 시작되면 그 뒤로는 다시 NOT NULL 이 나오지 않는다 (NULL 이 한 덩어리로 꼬리).
        boolean seenNull = false;
        for (var t : rows) {
            Integer v = t.get(1, Integer.class);
            if (v == null) {
                seenNull = true;
            } else {
                assertThat(seenNull).as("NULL 이후 NOT NULL 이 나오면 nullsLast 실패").isFalse();
            }
        }
    }

    @Test
    @DisplayName("실습2: countDistinct 부풀림 — 1:N 조인에서 count > countDistinct")
    void count_distinct_corrects_join_inflation() {
        // 노트 02-03 § countDistinct: 1:N 조인이 한 PK 를 여러 행으로 부풀린다.
        // 시드: Item 100개, 주문 1000건이 item=items[(i-1)%100] 로 분산 → 한 Item 이 OrderItem 10건에 등장.
        // item ⨝ orderItem → count(item.id) 는 OrderItem 수(1000)만큼 부풀고,
        // countDistinct(item.id) 는 실제 고유 Item 수(100)를 센다.
        var row = queryFactory
                .select(item.id.count(), item.id.countDistinct())
                .from(item)
                .join(orderItem).on(orderItem.item.eq(item))
                .fetchOne();

        Long inflated = row.get(item.id.count());
        Long distinct = row.get(item.id.countDistinct());

        // 부풀린 count(=OrderItem 수) > dedup count(=고유 Item 수).
        assertThat(inflated).isGreaterThan(distinct);
        assertThat(inflated).isEqualTo(fixture.memberCount()); // OrderItem 1000건 (주문당 1개)
        assertThat(distinct).isEqualTo(100L);                   // 고유 Item 100개
    }

    @Test
    @DisplayName("실습3: ExpressionUtils.as — 서브쿼리를 DTO 필드(totalAmount)에 alias 매핑")
    void expression_utils_as_binds_subquery_to_dto_field() {
        // 노트 02-03 § ExpressionUtils.as: Projections.fields 안에서 서브쿼리에 .as("name") 은
        // 컴파일은 되지만 런타임에 alias 누락 → ExpressionUtils.as(서브쿼리, Expressions.path(...)) 가 정답.
        // 주문항목 합계를 스칼라 서브쿼리로 계산해 OrderSummaryDto.totalAmount 에 매핑.
        var orderItemTotal = JPAExpressions
                .select(Expressions.numberTemplate(Integer.class,
                        "coalesce(sum({0} * {1}), 0)",
                        orderItem.orderPrice, orderItem.count))
                .from(orderItem)
                .where(orderItem.order.eq(order));

        var rows = queryFactory
                .select(Projections.fields(
                        OrderSummaryDto.class,
                        order.id.as("orderId"),
                        order.member.username.as("memberName"),
                        order.orderDate.as("orderDate"),
                        order.status.as("status"),
                        ExpressionUtils.as(
                                orderItemTotal,
                                Expressions.path(Integer.class, "totalAmount"))  // ← 서브쿼리 alias 우회
                ))
                .from(order)
                .limit(5)
                .fetch();

        assertThat(rows).hasSize(5);
        // 서브쿼리가 alias 로 정확히 매핑돼 totalAmount 필드가 채워졌는지 (0 이 아님).
        assertThat(rows).allSatisfy(dto -> {
            assertThat(dto.getOrderId()).isNotNull();
            assertThat(dto.getMemberName()).isNotBlank();
            assertThat(dto.getTotalAmount()).isPositive();
        });
    }
}
