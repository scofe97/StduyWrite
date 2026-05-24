package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.Tuple;
import com.runnershigh.querydsl.domain.Order;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import java.util.List;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

/**
 * Ch03 — 기본 문법과 조인 (학습 노트: write/05_data/querydsl/01-03.기본 문법과 조인.md).
 * Supabase querydsl_practice 스키마에 사전 적재된 1,000 회원 / 1,000 주문 시드 기준.
 */
@Slf4j
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("log4jdbc")
@Import(QuerydslConfig.class)
class Ch03_BasicQueryAndJoinTest {

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("selectFrom + where — username 으로 단건 조회")
    void selectFrom_where_username() {
        Member found = queryFactory
                .selectFrom(member)
                .where(member.username.eq("user_00001"))
                .fetchOne();

        Member member1 = queryFactory
                .selectFrom(member)
                .fetchFirst();   // limit(1) + fetchOne — 노트 L99

        log.info("first member: {}", member1);

        assertThat(found).isNotNull();
        assertThat(found.getAddress().getCity()).isEqualTo("Seoul");
    }

    @Test
    @DisplayName("count — 총 회원 수가 시드 메타와 일치")
    void count_total_members() {
        Long total = queryFactory.select(member.count()).from(member).fetchOne();

        Long total2 = queryFactory.select(member.countDistinct()).from(member).fetchOne();
        assertThat(total).isEqualTo(fixture.memberCount());
        assertThat(total2).isEqualTo(fixture.memberCount());   // PK 전부 고유 → count == countDistinct
    }

    @Test
    @DisplayName("inner join — 주문과 회원 결합 (페이지 100건)")
    void inner_join_orders_with_members() {
        List<Tuple> rows = queryFactory
                .select(order.id, member.username, order.status)
                .from(order)
                .join(order.member, member)
                .orderBy(order.id.asc())
                .limit(100)
                .fetch();

        assertThat(rows).hasSize(100);
    }

    @Test
    @DisplayName("join 세 방식(연관경로·on theta·from 나열)은 결과가 같다 — 노트 01-03")
    void join_three_styles_same_result() {
        // ① 연관 경로 조인 (표준) — @ManyToOne 매핑 따라감
        List<Long> byPath = queryFactory
                .select(order.id)
                .from(order)
                .join(order.member, member)
                .where(member.age.goe(20))
                .orderBy(order.id.asc())
                .fetch();

        // ② on 절 theta join — 엔티티 루트 + 조건 직접
        List<Long> byOn = queryFactory
                .select(order.id)
                .from(order)
                .join(member).on(order.member.eq(member))
                .where(member.age.goe(20))
                .orderBy(order.id.asc())
                .fetch();

        // ③ from 절 나열 (묵시적 조인) — cross join + where
        List<Long> byFrom = queryFactory
                .select(order.id)
                .from(order, member)
                .where(order.member.eq(member), member.age.goe(20))
                .orderBy(order.id.asc())
                .fetch();

        // 세 방식 모두 같은 inner join 결과
        assertThat(byPath).isEqualTo(byOn);
        assertThat(byPath).isEqualTo(byFrom);
    }

    @Test
    @DisplayName("fetch join 실측 — 일반 join vs 단건 fetch vs 컬렉션 fetch 행 수 비교 (노트 01-03 심화)")
    void fetch_join_actual_row_counts() {
        // 회원당 주문 수 분포: 주문 1000 / 회원 1000 = 회원당 1건 (1:1)
        // 주문당 항목 수 분포: 시드가 주문당 OrderItem 1개만 생성 → 데카르트 곱이 미미

        // ── 시나리오: 회원 1번이 낸 주문들 ──
        Long memberId = 1L;

        // ① 단건 fetch join (order.member) — 행 수 = 주문 수 그대로
        List<Order> singleFetch = queryFactory
                .selectFrom(order)
                .join(order.member, member).fetchJoin()
                .where(member.id.eq(memberId))
                .fetch();
        log.info("① 단건 fetch join (order.member) 결과 행 수 = {}", singleFetch.size());

        // ② 컬렉션 fetch join (order.orderItems) — 항목 수만큼 행 증식 (현 시드는 1개라 동일)
        List<Order> collectionFetch = queryFactory
                .selectFrom(order)
                .join(order.orderItems, orderItem).fetchJoin()
                .where(order.member.id.eq(memberId))
                .fetch();
        log.info("② 컬렉션 fetch join (order.orderItems) 결과 행 수 = {}", collectionFetch.size());

        // ③ 컬렉션 fetch join + distinct — PK 기준 중복 제거
        List<Order> collectionDistinct = queryFactory
                .selectFrom(order).distinct()
                .join(order.orderItems, orderItem).fetchJoin()
                .where(order.member.id.eq(memberId))
                .fetch();
        log.info("③ 컬렉션 fetch join + distinct 결과 행 수 = {}", collectionDistinct.size());

        // 전체 주문에서 "주문당 항목 수" 분포도 실측
        List<Tuple> itemsPerOrder = queryFactory
                .select(order.id, orderItem.count())
                .from(order)
                .join(order.orderItems, orderItem)
                .groupBy(order.id)
                .orderBy(orderItem.count().desc())
                .limit(3)
                .fetch();
        itemsPerOrder.forEach(t ->
                log.info("   주문 {} → 항목 {}개", t.get(order.id), t.get(orderItem.count())));

        // 단건 fetch 는 항상 주문 수 = distinct 결과와 동일
        assertThat(singleFetch.size()).isEqualTo(collectionDistinct.size());
    }

    @Test
    @DisplayName("where status — CANCELED 는 전체의 1/10 (i%10==0)")
    void canceled_count_is_one_tenth() {
        var canceled = queryFactory
                .select(order.count())
                .from(order)
                .where(order.status.eq(OrderStatus.CANCELED))
                .fetchOne();
        assertThat(canceled).isEqualTo(fixture.canceledCount());
        assertThat(canceled).isEqualTo(fixture.memberCount() / 10);
    }

    @Test
    @DisplayName("group by — 도시별 회원 수는 균등 분포")
    void group_by_city_is_uniform() {
        List<Tuple> rows = queryFactory
                .select(member.address.city, member.count())
                .from(member)
                .groupBy(member.address.city)
                .orderBy(member.address.city.asc())
                .fetch();

        // 도시 4개 균등 분포 → 각 도시 = memberCount / 4
        assertThat(rows).hasSize(4);
        long perCity = fixture.memberCount() / 4;
        assertThat(rows).extracting(t -> t.get(member.count()))
                .containsExactly(perCity, perCity, perCity, perCity);
    }
}
