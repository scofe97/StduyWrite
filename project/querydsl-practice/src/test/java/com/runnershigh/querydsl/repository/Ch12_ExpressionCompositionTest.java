package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrder.order;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.types.OrderSpecifier;
import com.querydsl.core.types.Predicate;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.OrderStatus;
import com.runnershigh.querydsl.support.TestDataLoader;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
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
 * Ch12 — 표현식 합성 (학습 노트: 02-04).
 * BooleanBuilder.or() 누적 vs BooleanExpression 메서드 분해 패턴 비교.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch12_ExpressionCompositionTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("BooleanBuilder.or() 누적 — 여러 username OR 결합")
    void boolean_builder_or_accumulation() {
        BooleanBuilder builder = new BooleanBuilder();
        for (int i = 1; i <= 5; i++) {
            builder.or(member.username.eq(String.format("user_%05d", i)));
        }

        Long count = queryFactory.select(member.count())
                .from(member)
                .where(builder)
                .fetchOne();

        assertThat(count).isEqualTo(5);
    }

    @Test
    @DisplayName("BooleanExpression 분해 — null-safe AND 합성")
    void boolean_expression_decomposition() {
        Predicate where = allOf(
                statusEq(OrderStatus.CANCELED),
                memberNameEq(null)   // null 은 무시
        );

        Long count = queryFactory.select(order.count())
                .from(order)
                .where(where)
                .fetchOne();

        assertThat(count).isEqualTo(fixture.canceledCount());
    }

    @Test
    @DisplayName("두 패턴 동등성 — 같은 조건이면 결과가 같다")
    void equivalence_builder_vs_expression() {
        // Builder 형태
        BooleanBuilder b = new BooleanBuilder()
                .and(order.status.eq(OrderStatus.CANCELED))
                .and(order.member.address.city.eq("Seoul"));

        // Expression 형태
        Predicate e = allOf(
                statusEq(OrderStatus.CANCELED),
                cityEq("Seoul")
        );

        Long c1 = queryFactory.select(order.count()).from(order).where(b).fetchOne();
        Long c2 = queryFactory.select(order.count()).from(order).where(e).fetchOne();

        assertThat(c1).isEqualTo(c2);
    }

    private Predicate allOf(BooleanExpression... exprs) {
        BooleanBuilder b = new BooleanBuilder();
        for (BooleanExpression e : exprs) {
            if (e != null) b.and(e);
        }
        return b;
    }

    private BooleanExpression statusEq(OrderStatus s) {
        return s == null ? null : order.status.eq(s);
    }

    private BooleanExpression memberNameEq(String n) {
        return n == null || n.isBlank() ? null : order.member.username.eq(n);
    }

    private BooleanExpression cityEq(String c) {
        return c == null ? null : order.member.address.city.eq(c);
    }

    // === 실습 (노트 02-04: Functional Predicate Supplier / Hooks 4분할 / ThreadLocal / 가상값 OR 누적) ===

    /** 실습용 컬럼 enum — Member 검색 칼럼을 운영의 Column enum 자리에 축소 대응. */
    enum MemberCol { USERNAME, CITY, AGE }

    @Test
    @DisplayName("실습1: Functional Predicate Supplier — 람다 binding 이 호출 시점에 평가된다")
    void functional_predicate_supplier_evaluates_lazily() {
        // 노트 02-04 § Functional Predicate Supplier: 정적 시점에 표현식을 평가하지 말고
        // 람다(Function<Ctx, BooleanExpression>) 를 등록한다. 호출 시점 평가가 핵심.
        // 시드 축소: ctx = "검색어"(String), 람다는 컬럼별로 검색어를 받아 BooleanExpression 생성.

        Map<MemberCol, Function<String, BooleanExpression>> bindings = new EnumMap<>(MemberCol.class);
        bindings.put(MemberCol.USERNAME, kw -> kw == null ? null : member.username.eq(kw));
        bindings.put(MemberCol.CITY,     kw -> kw == null ? null : member.address.city.eq(kw));
        bindings.put(MemberCol.AGE,      kw -> kw == null ? null : member.age.eq(Integer.parseInt(kw)));

        // 같은 binding 을 두 번 다른 인자로 호출 — 람다라 매번 새 표현식이 만들어진다.
        Long seoulCount = queryFactory.select(member.count())
                .from(member).where(bindings.get(MemberCol.CITY).apply("Seoul")).fetchOne();
        Long busanCount = queryFactory.select(member.count())
                .from(member).where(bindings.get(MemberCol.CITY).apply("Busan")).fetchOne();

        // 시드: 4개 도시 균등 1000/4=250씩.
        assertThat(seoulCount).isEqualTo(250);
        assertThat(busanCount).isEqualTo(250);
        // null 입력은 null 반환 → where(null) 은 무영향 → 전체.
        Long all = queryFactory.select(member.count())
                .from(member).where(bindings.get(MemberCol.USERNAME).apply(null)).fetchOne();
        assertThat(all).isEqualTo(fixture.memberCount());
    }

    /** 실습용 미니 Hooks — 운영 4분할(base/keyword/detail/orderSpecifier) 을 3분할로 축소. */
    interface MiniHooks {
        default Predicate basePredicate() { return null; }
        default Predicate keywordPredicate(MemberCol col, String kw) { return null; }
        default OrderSpecifier<?> orderSpecifier(MemberCol col) { return null; }
    }

    @Test
    @DisplayName("실습2: Hooks 분할 — base 만 override, 나머지는 default null 로 안 쓴다")
    void hooks_split_default_null() {
        // 노트 02-04 § Hooks 4분할: default null 반환으로 안 쓰는 hook 을 그대로 둔다.
        // 결재 이력의 ApprovalHistoryListQuerySupport 가 basePredicate 만 override 한 패턴 재현.
        MiniHooks hooks = new MiniHooks() {
            @Override
            public Predicate basePredicate() {
                return member.age.goe(20);  // 공통 조건: 20세 이상만
            }
            // keywordPredicate / orderSpecifier 는 default null
        };

        BooleanBuilder where = new BooleanBuilder();
        if (hooks.basePredicate() != null)            where.and(hooks.basePredicate());
        if (hooks.keywordPredicate(MemberCol.USERNAME, "x") != null)
            where.and(hooks.keywordPredicate(MemberCol.USERNAME, "x"));  // null → 무영향

        Long count = queryFactory.select(member.count()).from(member).where(where).fetchOne();
        // 시드 age 20~59 전부 20 이상이라 1000 전부 통과.
        assertThat(count).isEqualTo(fixture.memberCount());
    }

    /** 실습용 ThreadLocal holder — 운영 MyToListQuerySupport 의 currentUserId 자리. */
    static class CityContextHolder {
        private final ThreadLocal<String> currentCity = new ThreadLocal<>();
        void bindCity(String city) { currentCity.set(city); }
        void clearCity() { currentCity.remove(); }
        String currentCity() {
            String c = currentCity.get();
            if (c == null) throw new IllegalStateException("city must be bound before use");
            return c;
        }
    }

    @Test
    @DisplayName("실습3: ThreadLocal try/finally — bind→쿼리→clear 라이프사이클 + null 시 거부")
    void threadlocal_lifecycle_with_try_finally() {
        // 노트 02-04 § ThreadLocal: bind→try→finally→clear 의무. clear 누락은 권한 누수 사고.
        CityContextHolder holder = new CityContextHolder();

        // (a) 정상 흐름 — bind 후 쿼리, finally 에서 clear.
        holder.bindCity("Seoul");
        try {
            Long count = queryFactory.select(member.count())
                    .from(member)
                    .where(member.address.city.eq(holder.currentCity()))  // ThreadLocal 에서 읽음
                    .fetchOne();
            assertThat(count).isEqualTo(250);
        } finally {
            holder.clearCity();
        }

        // (b) clear 후 currentCity() 는 IllegalStateException — null 검증이 강제.
        assertThatThrownBy(holder::currentCity)
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("must be bound");
    }

    @Test
    @DisplayName("실습4: BooleanBuilder.or() 가상값 분기 — YOUNG/OLD 같은 age 컬럼의 가상값 OR 합산")
    void boolean_builder_or_virtual_value_branches() {
        // 노트 02-04 § BooleanBuilder.or() 누적: 같은 컬럼 값이 가상값으로 갈라질 때 OR 누적.
        // 운영의 EXCN/TODO 자리에 시드 축소로 YOUNG(age<30) / OLD(age>=50) / 일반 코드값(나이 정수) 대응.
        List<String> values = List.of("YOUNG", "OLD", "35");  // 셋이 동시에 들어옴

        BooleanBuilder builder = new BooleanBuilder();
        boolean hasYoung = values.contains("YOUNG");
        boolean hasOld   = values.contains("OLD");
        List<Integer> remaining = values.stream()
                .filter(v -> !"YOUNG".equals(v) && !"OLD".equals(v))
                .map(Integer::parseInt)
                .toList();

        if (hasYoung) builder.or(member.age.lt(30));         // 가상값 1
        if (hasOld)   builder.or(member.age.goe(50));        // 가상값 2
        if (!remaining.isEmpty()) builder.or(member.age.in(remaining));  // 일반 코드값

        Long count = queryFactory.select(member.count()).from(member).where(builder).fetchOne();
        // 시드 age = 20+((i-1)%40), 즉 20~59 균등 분포.
        // YOUNG: 20~29 → 10/40 = 250건, OLD: 50~59 → 10/40 = 250건, 35: 25건.
        // 셋 영역이 겹치지 않으므로 합 = 525.
        assertThat(count).isEqualTo(525);

        // 빈 builder = where(null) = 무영향 검증.
        Long all = queryFactory.select(member.count()).from(member).where(new BooleanBuilder()).fetchOne();
        assertThat(all).isEqualTo(fixture.memberCount());
    }
}
