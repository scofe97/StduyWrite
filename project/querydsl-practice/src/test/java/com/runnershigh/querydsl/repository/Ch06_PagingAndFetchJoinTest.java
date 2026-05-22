package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
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
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Ch06 — 페이징과 fetch join 함정. 10,000건 시드.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import({QuerydslConfig.class, OrderRepositoryImpl.class})
class Ch06_PagingAndFetchJoinTest {

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
    @DisplayName("searchPage — 첫 페이지 50건")
    void search_page_first_50() {
        var condition = OrderSearchCondition.builder().build();
        Page<?> page = repository.searchPage(condition, PageRequest.of(0, 50));

        assertThat(page.getTotalElements()).isEqualTo(fixture.memberCount());
        assertThat(page.getContent()).hasSize(50);
        assertThat(page.getTotalPages()).isEqualTo(fixture.memberCount() / 50);
    }

    @Test
    @DisplayName("searchPage — 페이지 크기가 전체보다 큰 경우 한 페이지로 끝남")
    void search_page_last_page() {
        var condition = OrderSearchCondition.builder().build();
        int pageSize = fixture.memberCount() * 2;
        Page<?> page = repository.searchPage(condition, PageRequest.of(0, pageSize));

        assertThat(page.getContent()).hasSize(fixture.memberCount());
        assertThat(page.getTotalElements()).isEqualTo(fixture.memberCount());
        assertThat(page.getTotalPages()).isEqualTo(1);
    }
}
