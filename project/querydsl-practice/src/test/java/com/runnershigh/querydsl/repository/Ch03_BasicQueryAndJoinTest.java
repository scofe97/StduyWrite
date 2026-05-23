package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.Tuple;
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
@ActiveProfiles("test")
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
        long total = queryFactory.select(member.count()).from(member).fetchOne();
        assertThat(total).isEqualTo(fixture.memberCount());
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
    @DisplayName("where status — CANCELED 는 전체의 1/10 (i%10==0)")
    void canceled_count_is_one_tenth() {
        long canceled = queryFactory.select(order.count())
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
