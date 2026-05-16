package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.dto.MemberSearchDto;
import com.runnershigh.querydsl.dto.QMemberSearchDto;
import com.runnershigh.querydsl.support.TestDataLoader;
import jakarta.persistence.EntityManager;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

/**
 * Ch05 — 프로젝션과 DTO 매핑 (학습 노트: 01-05.프로젝션과 DTO 매핑.md)
 * <p>
 * 핵심: Tuple, Projections.bean/fields/constructor, @QueryProjection 트레이드오프.
 * <p>
 * 실습:
 * - [ ] Projections.bean 으로 OrderSummaryDto 매핑 — 세터 호출 동작 확인
 * - [ ] Projections.fields 로 매핑 — private 필드에도 동작하는지
 * - [ ] @QueryProjection 의존성 침투 — DTO 가 querydsl-core 에 묶이는 비용 vs 컴파일 안정성
 */
@DataJpaTest
@Import(QuerydslConfig.class)
class Ch05_ProjectionAndDtoTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    @BeforeEach
    void setUp() {
        new TestDataLoader(em).loadDefault();
    }

    @Test
    @DisplayName("[Green] @QueryProjection 으로 회원 검색 DTO 매핑")
    void QueryProjection_으로_회원_검색_DTO_매핑() {
        List<MemberSearchDto> result = queryFactory
                .select(new QMemberSearchDto(member.username, member.age, member.address.city))
                .from(member)
                .orderBy(member.username.asc())
                .fetch();

        assertThat(result).hasSize(4);
        assertThat(result).extracting(MemberSearchDto::getUsername)
                .containsExactly("alice", "bob", "charlie", "dave");
        assertThat(result.get(0).getCity()).isEqualTo("Seoul");
    }

    @Test
    @DisplayName("[Green] Projections.constructor 로 동일 매핑")
    void Projections_constructor_로_동일_매핑() {
        List<MemberSearchDto> result = queryFactory
                .select(Projections.constructor(MemberSearchDto.class,
                        member.username, member.age, member.address.city))
                .from(member)
                .orderBy(member.username.asc())
                .fetch();

        assertThat(result).hasSize(4);
    }

    // TODO [실습 1] Projections.fields 사용 시 setter 없는 final 필드는 어떻게 동작하는지 확인
    // TODO [실습 2] OrderSummaryDto 를 Projections.bean 으로 매핑 — null 처리 확인
    // TODO [실습 3] Tuple 직접 fetch — 컬럼 추출 (`tuple.get(member.age)`) 사용감 비교
}
