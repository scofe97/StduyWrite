package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.querydsl.core.types.Order;
import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.dsl.PathBuilder;
import com.querydsl.jpa.JPAExpressions;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
import java.util.Comparator;
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
 * Ch13 — PathBuilder, 동적 path 빌더 (학습 노트: 02-01. 응용 사례는 03-04).
 * 문자열 기반 컬럼 접근 — 컴파일 안정성을 잃는 대신 동적 자유(다른 alias·모듈경계·동적 정렬)를 얻는 패턴.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch13_PathBuilderTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("PathBuilder 로 selectFrom — Q 클래스 없이도 동일 결과")
    void path_builder_select_from() {
        PathBuilder<Member> m = new PathBuilder<>(Member.class, "member");

        long count = queryFactory
                .select(m.count())
                .from(m)
                .fetchOne();

        assertThat(count).isEqualTo(fixture.memberCount());
    }

    @Test
    @DisplayName("PathBuilder + getString — 동적 컬럼 접근")
    void path_builder_get_string() {
        PathBuilder<Member> m = new PathBuilder<>(Member.class, "member");

        var found = queryFactory
                .selectFrom(m)
                .where(m.getString("username").eq(fixture.firstUsername()))
                .fetchOne();

        assertThat(found).isNotNull();
        assertThat(found.getUsername()).isEqualTo(fixture.firstUsername());
    }

    @Test
    @DisplayName("PathBuilder + 임베디드 city 접근 — get('address') 후 getString('city')")
    void path_builder_embedded_field() {
        PathBuilder<Member> m = new PathBuilder<>(Member.class, "member");

        long seoulCount = queryFactory
                .select(m.count())
                .from(m)
                .where(m.get("address").getString("city").eq("Seoul"))
                .fetchOne();

        assertThat(seoulCount).isEqualTo(fixture.memberCount() / 4);
    }

    @Test
    @DisplayName("PathBuilder + getNumber — age 범위 필터")
    void path_builder_get_number() {
        PathBuilder<Member> m = new PathBuilder<>(Member.class, "member");

        long count = queryFactory
                .select(m.count())
                .from(m)
                .where(m.getNumber("age", Integer.class).between(20, 29))
                .fetchOne();

        assertThat(count).isEqualTo(fixture.memberCount() / 4);
    }

    @Test
    @DisplayName("실습1: 다른 alias 두 PathBuilder 로 self-join — 같은 도시 평균 나이보다 많은 회원")
    void path_builder_self_join_via_distinct_alias() {
        // 같은 Member 테이블을 outer/inner 두 alias 로 분리 — Q-class 단일 인스턴스로는 안 되는 자리.
        PathBuilder<Member> outer = new PathBuilder<>(Member.class, "outerMember");
        PathBuilder<Member> inner = new PathBuilder<>(Member.class, "innerMember");

        List<Member> result = queryFactory
                .selectFrom(outer)
                .where(outer.getNumber("age", Integer.class).gt(
                        JPAExpressions
                                .select(inner.getNumber("age", Integer.class).avg())
                                .from(inner)
                                .where(inner.get("address").getString("city")
                                        .eq(outer.get("address").getString("city")))
                ))
                .fetch();

        // 각자 자기 도시 평균보다 나이가 많은 회원만 — 전부도 0도 아닌 일부.
        assertThat(result).isNotEmpty();
        assertThat(result.size()).isLessThan((int) fixture.memberCount());
    }

    @Test
    @DisplayName("실습2: 컬럼명 오타는 컴파일을 통과하고 런타임에 터진다 (문자열 기반의 대가)")
    void path_builder_typo_fails_at_runtime() {
        PathBuilder<Member> m = new PathBuilder<>(Member.class, "member");

        // "emial" 오타 — Q-class 였다면 컴파일 에러. PathBuilder 는 실행 시점에야 터진다.
        assertThatThrownBy(() ->
                queryFactory
                        .selectFrom(m)
                        .where(m.getString("emial").eq("x"))
                        .fetch()
        ).isInstanceOf(Exception.class);
    }

    @Test
    @DisplayName("실습3: 동적 정렬 키 — m.getXxx(sortKey) 한 줄로 switch 분기 대체")
    void path_builder_dynamic_sort_key() {
        PathBuilder<Member> m = new PathBuilder<>(Member.class, "member");

        // 화이트리스트로 검증한 sortKey 를 PathBuilder 한 줄에 매핑 (문자열 오타 방어는 화이트리스트가 담당).
        String sortKey = "age";
        OrderSpecifier<Integer> orderByAgeDesc =
                new OrderSpecifier<>(Order.DESC, m.getNumber(sortKey, Integer.class));

        List<Member> result = queryFactory
                .selectFrom(m)
                .orderBy(orderByAgeDesc)
                .limit(50)
                .fetch();

        assertThat(result).hasSize(50);
        assertThat(result)
                .extracting(Member::getAge)
                .isSortedAccordingTo(Comparator.reverseOrder());
    }
}
