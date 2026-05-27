package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.support.listquery.common.query.ListQueryPolicy;
import com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query.AbstractQuerydslListQueryRepository;
import com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query.QueryColumnBinding;
import com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query.QueryColumnBindingBuilder;
import com.runnershigh.querydsl.support.listquery.infrastructure.persistence.query.QueryColumnBindingRegistry;
import java.util.EnumMap;
import java.util.Map;
import java.util.function.Function;

/**
 * 실습 5 — Member 검색 Support (운영 {@code ApprovalManagementListQuerySupport} 시드 축소판).
 *
 * <p>리스트 검색의 두 축 중 "정적 매핑" 만 다룬다:
 * <ul>
 *   <li><b>registry</b> — 컬럼 → 표현식(detail selection / order by) 람다 등록. 본 클래스에서 채움.</li>
 *   <li><b>hooks</b> — userId 처럼 요청 단위 컨텍스트가 필요한 동적 표현식. 본 실습에선 default(no-op) 사용.</li>
 * </ul>
 *
 * <p>핵심 학습 포인트(노트 02-04 § Functional Predicate Supplier):
 * 모든 binding 은 람다 {@code ctx -> ...} 로 넘긴다. {@code createRegistry()} 가 호출되는 클래스 로딩 시점이 아니라
 * 부모 클래스가 매 쿼리마다 새 {@code MemberListQueryContext} 를 만들어 람다를 적용하는 시점에 평가된다.
 * 람다 안에서 별칭(PathBuilder) 을 매번 다시 얻어오기 때문에 동일 별칭 충돌이 일어나지 않는다.
 */
public abstract class MemberListQuerySupport
        extends AbstractQuerydslListQueryRepository<MemberListColumn, MemberListQueryContext> {

    /** 어떤 컬럼/검색/정렬을 허용할지 결정하는 정책. 클래스당 1개라 정적으로 고정. */
    private static final MemberListPolicy POLICY = new MemberListPolicy();

    /** 컬럼 → QueryDSL 표현식 매핑. 클래스당 1개. {@link #createRegistry()} 에서 빌드해 캐싱. */
    private static final QueryColumnBindingRegistry<MemberListColumn, MemberListQueryContext> REGISTRY = createRegistry();

    /** 부모(AbstractQuerydslListQueryRepository) 에 정책 노출. */
    @Override
    protected ListQueryPolicy<MemberListColumn> policy() {
        return POLICY;
    }

    /** 부모에 컬럼-표현식 매핑 노출. 부모가 정렬/상세조건 만들 때 {@code registry().get(column)} 형태로 호출. */
    @Override
    protected QueryColumnBindingRegistry<MemberListColumn, MemberListQueryContext> registry() {
        return REGISTRY;
    }

    /**
     * 컬럼별 람다 binding 을 등록해 immutable Map 기반 Registry 를 반환한다.
     *
     * <ul>
     *   <li>USERNAME — 키워드(ALL 모드 OR 결합용) + 상세검색(T REGEXP) + 정렬.</li>
     *   <li>CITY     — 키워드 + 상세검색(S selection, IN 매칭) + 정렬. 임베디드 Address.city 경로 사용.</li>
     *   <li>AGE      — 정렬만. 정책에서 키워드/상세검색이 막혀 있어 등록 안 해도 부모가 호출하지 않는다.</li>
     * </ul>
     *
     * <p>마지막 줄 {@code immutable::get} 은 {@code Map.get(key)} 를 함수형 인터페이스
     * {@code QueryColumnBindingRegistry.get(C)} 의 구현으로 변환한다. 람다 호출 시점에 비로소
     * Map lookup 이 일어나는 지연 평가 형태.
     */
    private static QueryColumnBindingRegistry<MemberListColumn, MemberListQueryContext> createRegistry() {
        // enum 키이므로 EnumMap 으로 메모리/조회 효율을 확보. 컬럼이 늘어도 비트셋 기반이라 빠르다.
        Map<MemberListColumn, QueryColumnBinding<MemberListQueryContext>> bindings =
                new EnumMap<>(MemberListColumn.class);

        // USERNAME: 전 영역(키워드/상세/정렬) 허용. ctx.member() 는 호출 시점의 PathBuilder 별칭이라 매 쿼리마다 새 인스턴스.
        bindings.put(
                MemberListColumn.USERNAME,
                QueryColumnBindingBuilder.<MemberListQueryContext>builder()
                        // 글로벌 검색(q) 시 username 컬럼에 regexp 매칭 (ALL 모드면 다른 컬럼과 OR 결합).
                        .keywordRegexp(ctx -> ctx.member().getString("username"))
                        // 상세검색(T 타입) 시 동일하게 regexp 매칭.
                        .detailTextRegexp(ctx -> ctx.member().getString("username"))
                        // 정렬 키 — String 자연순.
                        .orderByComparable(ctx -> ctx.member().getString("username"))
                        .build()
        );

        // CITY: 임베디드(Address) 필드라 ctx.member().get("address").getString("city") 로 한 단계 내려간다.
        bindings.put(
                MemberListColumn.CITY,
                QueryColumnBindingBuilder.<MemberListQueryContext>builder()
                        // 글로벌 검색 시 city 도 OR 후보로.
                        .keywordRegexp(ctx -> ctx.member().get("address").getString("city"))
                        // 상세검색(S 타입) — selection 표현식 + 입력값 정규화 함수(여기선 그대로) 등록.
                        // 부모가 .in(values) 형태로 IN 매칭에 사용.
                        .detailSelection(
                                ctx -> ctx.member().get("address").getString("city"),
                                Function.identity()
                        )
                        // 정렬 키 — city 사전순.
                        .orderByComparable(ctx -> ctx.member().get("address").getString("city"))
                        .build()
        );

        // AGE: 정렬만. 정책이 검색을 허용하지 않으므로 keyword/detail 람다는 등록하지 않는다.
        bindings.put(
                MemberListColumn.AGE,
                QueryColumnBindingBuilder.<MemberListQueryContext>builder()
                        // Number 정렬 — Integer 자연순. orderByComparable 은 Comparable 기반 자동 ASC/DESC 처리.
                        .orderByComparable(ctx -> ctx.member().getNumber("age", Integer.class))
                        .build()
        );

        // 빌드가 끝난 EnumMap 을 불변 사본으로 박제 — 이후 누가 put 해도 운영 시점 사이드이펙트 없음.
        Map<MemberListColumn, QueryColumnBinding<MemberListQueryContext>> immutable = Map.copyOf(bindings);

        // immutable::get == (column) -> immutable.get(column). QueryColumnBindingRegistry 의
        // 단일 추상 메서드 get(C) 자리에 메서드 레퍼런스가 그대로 들어맞아 함수형 인터페이스 구현으로 변환된다.
        return immutable::get;
    }
}
