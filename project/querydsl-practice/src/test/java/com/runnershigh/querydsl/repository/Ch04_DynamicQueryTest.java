package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Order;
import com.runnershigh.querydsl.domain.OrderStatus;
import java.util.Comparator;
import java.util.List;
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
 * Ch04 — 동적 쿼리. 10,000건 시드 기준 재작성.
 * canceledCount = memberCount/10 = 1,000.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import({QuerydslConfig.class, OrderRepositoryImpl.class})
class Ch04_DynamicQueryTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private OrderRepositoryImpl repository;
    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @BeforeEach
    void setUp() {
        repository = new OrderRepositoryImpl(queryFactory);
    }

    @Test
    @DisplayName("모든 조건 null — 전체 반환")
    void all_null_returns_all() {
        var condition = OrderSearchCondition.builder().build();
        assertThat(repository.search(condition)).hasSize(fixture.memberCount());
    }

    @Test
    @DisplayName("status=CANCELED — memberCount/10 건")
    void status_canceled_one_tenth() {
        var condition = OrderSearchCondition.builder()
                .status(OrderStatus.CANCELED)
                .build();
        assertThat(repository.search(condition)).hasSize(fixture.canceledCount());
    }

    @Test
    @DisplayName("memberName 지정 — 단건")
    void member_name_single() {
        var condition = OrderSearchCondition.builder()
                .memberName(fixture.firstUsername())
                .build();
        assertThat(repository.search(condition))
                .singleElement()
                .satisfies(o -> assertThat(o.getMember().getUsername()).isEqualTo(fixture.firstUsername()));
    }

    @Test
    @DisplayName("status + memberName — 교차 조건")
    void status_and_member_name() {
        // user_00010 은 i=10 → 시드에서 CANCELED
        var condition = OrderSearchCondition.builder()
                .memberName("user_00010")
                .status(OrderStatus.CANCELED)
                .build();
        assertThat(repository.search(condition)).hasSize(1);

        // user_00010 은 ORDERED 상태가 아님 → 0건
        var noMatch = OrderSearchCondition.builder()
                .memberName("user_00010")
                .status(OrderStatus.ORDERED)
                .build();
        assertThat(repository.search(noMatch)).isEmpty();
    }

    @Test
    @DisplayName("동적 정렬 — orderDate 내림차순")
    void sort_by_order_date_desc() {
        var condition = OrderSearchCondition.builder()
                .sortKey("orderDate")
                .ascending(false)
                .build();

        List<Order> result = repository.search(condition);

        assertThat(result).hasSize(fixture.memberCount());
        assertThat(result)
                .extracting(Order::getOrderDate)
                .isSortedAccordingTo(Comparator.reverseOrder());   // 내림차순 검증
    }

    @Test
    @DisplayName("동적 정렬 — 잘못된 sortKey 는 기본 order.id 오름차순")
    void sort_by_unknown_key_falls_back_to_id() {
        var condition = OrderSearchCondition.builder()
                .sortKey("hacker'; DROP TABLE--")   // 화이트리스트 밖 → default
                .ascending(true)
                .build();

        List<Order> result = repository.search(condition);

        assertThat(result).hasSize(fixture.memberCount());
        assertThat(result)
                .extracting(Order::getId)
                .isSortedAccordingTo(Comparator.naturalOrder());   // id 오름차순 fallback
    }
}
