package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

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
import org.springframework.test.context.ActiveProfiles;

/**
 * Ch07 — 커스텀 리포지토리 패턴. 10,000건 시드.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch07_CustomRepositoryTest {

    @Autowired
    private MemberRepository memberRepository;

    @Autowired
    private EntityManager em;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("JpaRepository.count + Custom.findByUsernameContains")
    void jpa_count_and_custom_contains() {
        assertThat(memberRepository.count()).isEqualTo(fixture.memberCount());

        // user_00001 ~ user_10000 중 'user_00001' 부분 일치 = 1건
        assertThat(memberRepository.findByUsernameContains("user_00001"))
                .extracting(m -> m.getUsername())
                .containsExactly("user_00001");
    }

    @Test
    @DisplayName("searchAsDto — age 범위 필터")
    void search_as_dto_age_range() {
        // age 20~59 균등 분포(40살 단위) → 20~29 는 정확히 memberCount/4
        var result = memberRepository.searchAsDto(null, 20, 29);
        assertThat(result).hasSize(fixture.memberCount() / 4);
    }
}
