package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QItem.item;
import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.Tuple;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.domain.Order;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

/**
 * Ch03 — 기본 문법과 조인 (학습 노트: write/06_data/spring/querydsl/01-03.기본 문법과 조인.md)
 * <p>
 * 본 파일은 완성본 레퍼런스다. 다른 챕터 스캐폴드(Ch04~)를 채울 때 이 패턴을 참고한다.
 */
@DataJpaTest
@Import(QuerydslConfig.class)
class Ch03_BasicQueryAndJoinTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private Fixture fixture;

    @BeforeEach
    void setUp() {
        fixture = new TestDataLoader(em).loadDefault();
    }

    @Test
    @DisplayName("[Green] selectFrom + where 로 회원 단건 조회")
    void selectFrom_where_회원_단건_조회() {
        Member found = queryFactory
                .selectFrom(member)
                .where(member.username.eq("alice"))
                .fetchOne();

        assertThat(found).isNotNull();
        assertThat(found.getEmail()).isEqualTo("alice@runners.io");
        assertThat(found.getAddress().getCity()).isEqualTo("Seoul");
    }

    @Test
    @DisplayName("[Green] inner join — 주문과 회원 결합")
    void inner_join_주문과_회원_결합() {
        List<Tuple> rows = queryFactory
                .select(order.id, member.username, order.status)
                .from(order)
                .join(order.member, member)
                .orderBy(order.id.asc())
                .fetch();

        assertThat(rows).hasSize(3);
        assertThat(rows).extracting(t -> t.get(member.username))
                .containsExactly("alice", "bob", "charlie");
    }

    @Test
    @DisplayName("[Green] left join — 주문 없는 회원도 포함")
    void left_join_주문_없는_회원도_포함() {
        List<Tuple> rows = queryFactory
                .select(member.username, order.id)
                .from(member)
                .leftJoin(order).on(order.member.eq(member))
                .orderBy(member.username.asc())
                .fetch();

        // dave 는 주문이 없어 order.id 가 null.
        assertThat(rows).extracting(t -> t.get(member.username))
                .contains("dave");
        assertThat(rows.stream()
                .filter(t -> "dave".equals(t.get(member.username)))
                .findFirst().orElseThrow()
                .get(order.id))
                .isNull();
    }

    @Test
    @DisplayName("[Green] fetch join — 컬렉션 (orderItems) 즉시 로딩")
    void fetch_join_컬렉션_orderItems_즉시_로딩() {
        // 주의: 컬렉션 fetch join + Pageable 는 HHH000104 — Ch06 에서 다룬다.
        List<Order> orders = queryFactory
                .selectFrom(order)
                .join(order.member, member).fetchJoin()
                .leftJoin(order.orderItems, orderItem).fetchJoin()
                .leftJoin(orderItem.item, item).fetchJoin()
                .where(order.status.eq(OrderStatus.ORDERED))
                .distinct()
                .fetch();

        assertThat(orders).isNotEmpty();
        // 영속성 컨텍스트를 비워도 N+1 없이 접근 가능해야 한다.
        em.clear();
        // 위에서 이미 fetchJoin 으로 가져왔으므로 컬렉션 접근 시 추가 SQL 없음 (수동 검증 가능).
    }

    @Test
    @DisplayName("[Green] 집계 — 회원당 주문 건수 group by")
    void 집계_회원당_주문_건수_group_by() {
        List<Tuple> rows = queryFactory
                .select(member.username, order.count())
                .from(order)
                .join(order.member, member)
                .groupBy(member.username)
                .orderBy(member.username.asc())
                .fetch();

        assertThat(rows).hasSize(3);
        assertThat(rows).extracting(t -> t.get(member.username))
                .containsExactly("alice", "bob", "charlie");
        assertThat(rows).extracting(t -> t.get(order.count()))
                .containsExactly(1L, 1L, 1L);
    }
}
