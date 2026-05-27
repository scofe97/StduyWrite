package com.runnershigh.querydsl.repository;

import com.querydsl.core.types.dsl.PathBuilder;
import com.runnershigh.querydsl.domain.Member;

/**
 * 실습 5 — Member 검색 PathBuilder 컨텍스트.
 * 02-01 컨텍스트 record 패턴 — 별칭 그릇만, JOIN 안 함.
 * defaultContext() 가 매 쿼리마다 새 인스턴스 → 람다 binding 호출 시점 평가 (02-04).
 */
public record MemberListQueryContext(PathBuilder<Member> member) {

    public static MemberListQueryContext defaultContext() {
        return new MemberListQueryContext(
                new PathBuilder<>(Member.class, "member")
        );
    }
}
