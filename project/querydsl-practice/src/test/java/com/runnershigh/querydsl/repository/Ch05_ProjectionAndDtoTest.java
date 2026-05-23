package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.dto.MemberSearchDto;
import com.runnershigh.querydsl.dto.QMemberSearchDto;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
import java.util.List;
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
 * Ch05 — 프로젝션과 DTO 매핑. 10,000건 시드 기준.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch05_ProjectionAndDtoTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("@QueryProjection — 첫 10명 매핑")
    void query_projection_first10() {
        List<MemberSearchDto> result = queryFactory
                .select(new QMemberSearchDto(member.username, member.age, member.address.city))
                .from(member)
                .orderBy(member.username.asc())
                .limit(10)
                .fetch();

        assertThat(result).hasSize(10);
        assertThat(result.get(0).getUsername()).isEqualTo("user_00001");
        assertThat(result.get(0).getCity()).isEqualTo("Seoul");
    }

    @Test
    @DisplayName("Projections.constructor — 첫 10명 동일 매핑")
    void projections_constructor_first10() {
        List<MemberSearchDto> result = queryFactory
                .select(Projections.constructor(MemberSearchDto.class,
                        member.username, member.age, member.address.city))
                .from(member)
                .orderBy(member.username.asc())
                .limit(10)
                .fetch();

        assertThat(result).hasSize(10);
        assertThat(result.get(0).getUsername()).isEqualTo("user_00001");
    }

    @Test
    @DisplayName("DTO 전체 카운트")
    void dto_total_count() {
        long count = queryFactory.select(member.count()).from(member).fetchOne();
        assertThat(count).isEqualTo(fixture.memberCount());
    }
}
