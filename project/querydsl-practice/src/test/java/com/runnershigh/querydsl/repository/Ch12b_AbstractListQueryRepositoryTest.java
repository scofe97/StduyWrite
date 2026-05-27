package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import com.runnershigh.querydsl.support.listquery.common.query.ListDetailCondition;
import com.runnershigh.querydsl.support.listquery.common.query.ListQueryRequest;
import com.runnershigh.querydsl.support.listquery.common.query.ListQueryResolver;
import com.runnershigh.querydsl.support.listquery.common.query.ListSearchRequest;
import com.runnershigh.querydsl.support.listquery.common.query.ListSortRequest;
import com.runnershigh.querydsl.support.listquery.common.query.ResolvedListQuery;
import jakarta.persistence.EntityManager;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

/**
 * 실습 5 — 운영 AbstractQuerydslListQueryRepository + Registry + Resolver 그대로 사용.
 * 학습 노트: 02-04 §Functional Predicate Supplier + Hooks 4분할 + Adapter 호출 흐름.
 * <p>
 * 운영 5계층(Controller→UseCase→Service→Port→Adapter) 중 *Adapter+호출자* 만 시드로 축소:
 * - Support: MemberListQuerySupport (registry, policy)
 * - Adapter: 본 테스트 안 inner class MemberListAdapter (findMembers 실행)
 * - 입력:   ListQueryRequest (사용자 API 입력 시뮬레이션)
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch12b_AbstractListQueryRepositoryTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    /**
     * Support 를 extends 한 어댑터 — 운영 ApprovalManagementTableQueryAdapter 시드 버전.
     * 매 메서드 호출이 운영 패턴의 한 흐름:
     *   ① ctx = defaultContext() (이번 쿼리 전용 PathBuilder)
     *   ② buildPredicate(...) — registry/hooks 의 람다가 ctx 받아 평가
     *   ③ buildOrderSpecifiers(...) — orderByComparable 람다 평가
     *   ④ queryFactory.selectFrom(ctx).where(...).orderBy(...).fetch()
     */
    class MemberListAdapter extends MemberListQuerySupport {
        private final ListQueryResolver resolver = new ListQueryResolver();

        List<Member> findMembers(ListQueryRequest request) {
            // 정렬/검색 세팅
            ResolvedListQuery<MemberListColumn> resolved = resolver.resolve(request, policy());

            MemberListQueryContext ctx = MemberListQueryContext.defaultContext();
            Predicate predicate = buildPredicate(resolved, ctx, null);
            OrderSpecifier<?>[] orders = buildOrderSpecifiers(resolved, ctx);

            return queryFactory
                    .selectFrom(ctx.member())     // PathBuilder<Member> 그대로 from·select
                    .where(predicate)
                    .orderBy(orders)
                    .offset(resolved.offset())
                    .limit(resolved.limit())
                    .fetch();
        }
    }

    @Test
    @DisplayName("실습5-1: 상세검색 — city=Seoul (S 타입 selection)")
    void detail_search_city_seoul() {
//        ListDetailCondition cityFilter = new ListDetailCondition();
//        cityFilter.setType("S");
//        cityFilter.setColumn("city");
//        cityFilter.setValueList(List.of("Seoul"));   // S 타입은 valueList (IN 매칭) 사용
//
//        ListSearchRequest search = new ListSearchRequest();
//        search.setColumn("DTL");                       // 상세검색 모드
//        search.setDetail(List.of(cityFilter));
//
//        ListSortRequest sort = new ListSortRequest();
//        sort.setColumn("username");
//        sort.setDirection("ASC");
//
//        ListQueryRequest request = new ListQueryRequest();
//        request.setPage(1);
//        request.setSize(10);
//        request.setSearchObj(search);
//        request.setSortObj(sort);
//
//        List<Member> rows = new MemberListAdapter().findMembers(request);

        ListDetailCondition cityFilter = new ListDetailCondition();
        cityFilter.setType("S");
        cityFilter.setColumn("city");
        cityFilter.setValueList(List.of("Seoul"));

        ListSearchRequest search = new ListSearchRequest();
        search.setColumn("DTL");
        search.setDetail(List.of(cityFilter));


        ListSortRequest sort = new ListSortRequest();
        sort.setColumn("DTL");
        sort.setColumn("username");
        sort.setDirection("ASC");

        ListQueryRequest request = new ListQueryRequest();
        request.setPage(1);
        request.setSize(10);
        request.setSearchObj(search);
        request.setSortObj(sort);

        List<Member> rows = new MemberListAdapter().findMembers(request);


        // 시드: CITIES = {Seoul,Busan,Incheon,Daegu}, city = CITIES[(i-1)%4]
        // → Seoul: i=1,5,9,13,... 즉 user_00001, 00005, 00009, ...
        // username ASC 정렬, page=1 size=10 → 첫 10명
        assertThat(rows).hasSize(10);
        assertThat(rows).allSatisfy(m -> assertThat(m.getAddress().getCity()).isEqualTo("Seoul"));
        assertThat(rows.get(0).getUsername()).isEqualTo("user_00001");
        assertThat(rows.get(9).getUsername()).isEqualTo("user_00037");
    }

    @Test
    @DisplayName("실습5-2: 상세검색 — username REGEXP (T 타입)")
    void detail_search_username_regexp() {
        // username REGEXP '000' → user_00001~user_00099 (앞자리 0 두 개 이상 포함) — 시드 1000명 전부 user_00xxx
        // 정확히는 '_0009' 정도로 좁혀야 의미 있는 부분집합
        ListDetailCondition usernameFilter = new ListDetailCondition();
        usernameFilter.setType("T");
        usernameFilter.setColumn("username");
        usernameFilter.setValue("_0009");           // user_00090~99 (10명)

        ListSearchRequest search = new ListSearchRequest();
        search.setColumn("DTL");
        search.setDetail(List.of(usernameFilter));

        ListSortRequest sort = new ListSortRequest();
        sort.setColumn("username");
        sort.setDirection("ASC");

        ListQueryRequest request = new ListQueryRequest();
        request.setPage(1);
        request.setSize(20);
        request.setSearchObj(search);
        request.setSortObj(sort);

        List<Member> rows = new MemberListAdapter().findMembers(request);

        // user_00090~99 (10명) + user_00190~199 (10명) + ... user_00990~999 (10명) — 너무 많음
        // _0009 는 user_000{90..99} (10명) + user_00{190..199, 290..299, ...} 도 포함
        // 단순화: REGEXP 매칭으로 '_0009' 가 들어간 username 들이 다 잡힘. size 만 검증.
        assertThat(rows).isNotEmpty();
        assertThat(rows).allSatisfy(m -> assertThat(m.getUsername()).contains("_0009"));
        // 첫 매칭 = user_00090 ('user_0009' 패턴 첫 등장)
        assertThat(rows.get(0).getUsername()).isEqualTo("user_00090");
    }

    @Test
    @DisplayName("실습5-3: 정렬만 — age DESC + tieBreaker(username ASC)")
    void sort_only_age_desc_with_tiebreaker() {
        ListSortRequest sort = new ListSortRequest();
        sort.setColumn("age");
        sort.setDirection("DESC");

        ListQueryRequest request = new ListQueryRequest();
        request.setPage(1);
        request.setSize(5);
        request.setSortObj(sort);

        List<Member> rows = new MemberListAdapter().findMembers(request);

        // 시드 age = 20+((i-1)%40) → 20~59 균등. age DESC 첫 그룹 = 59 (i=40,80,120,...,1000 총 25명)
        // age=59 인 i 중 username ASC 첫 5명 = user_00040, 00080, 00120, 00160, 00200
        assertThat(rows).hasSize(5);
        assertThat(rows).allSatisfy(m -> assertThat(m.getAge()).isEqualTo(59));
        assertThat(rows.get(0).getUsername()).isEqualTo("user_00040");
        assertThat(rows.get(4).getUsername()).isEqualTo("user_00200");
    }

    @Test
    @DisplayName("실습5-4: 전체검색 — searchValue 가 username/city OR 결합 (정책 globalSearchColumns)")
    void global_search_all_columns() {
        // ALL 모드: searchValue 가 USERNAME REGEXP OR CITY REGEXP 로 OR 결합
        // 'Seoul' 검색 → city='Seoul' 인 행 (250) + username 에 'Seoul' 들어간 행 (0)
        ListSearchRequest search = new ListSearchRequest();
        search.setColumn("ALL");
        search.setSearchValue("Seoul");

        ListSortRequest sort = new ListSortRequest();
        sort.setColumn("username");
        sort.setDirection("ASC");

        ListQueryRequest request = new ListQueryRequest();
        request.setPage(1);
        request.setSize(10);
        request.setSearchObj(search);
        request.setSortObj(sort);

        List<Member> rows = new MemberListAdapter().findMembers(request);

        assertThat(rows).hasSize(10);
        assertThat(rows).allSatisfy(m -> assertThat(m.getAddress().getCity()).isEqualTo("Seoul"));
    }
}
