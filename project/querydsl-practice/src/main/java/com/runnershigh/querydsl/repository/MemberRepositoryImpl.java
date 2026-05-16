package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;

import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.dto.MemberSearchDto;
import com.runnershigh.querydsl.dto.QMemberSearchDto;
import java.util.List;
import lombok.RequiredArgsConstructor;

/**
 * 학습 노트:
 * - 02-01.커스텀 리포지토리 패턴 — Impl 명명 규칙
 * - 01-04.동적 쿼리 — BooleanExpression null-return 패턴
 * - 01-05.프로젝션과 DTO 매핑 — @QueryProjection
 */
@RequiredArgsConstructor
public class MemberRepositoryImpl implements MemberRepositoryCustom {

    private final JPAQueryFactory queryFactory;

    @Override
    public List<Member> findByUsernameContains(String keyword) {
        return queryFactory
                .selectFrom(member)
                .where(usernameContains(keyword))
                .fetch();
    }

    @Override
    public List<MemberSearchDto> searchAsDto(String usernameKeyword, Integer minAge, Integer maxAge) {
        return queryFactory
                .select(new QMemberSearchDto(
                        member.username,
                        member.age,
                        member.address.city
                ))
                .from(member)
                .where(
                        usernameContains(usernameKeyword),
                        ageGoe(minAge),
                        ageLoe(maxAge)
                )
                .fetch();
    }

    private BooleanExpression usernameContains(String keyword) {
        return keyword == null || keyword.isBlank() ? null : member.username.contains(keyword);
    }

    private BooleanExpression ageGoe(Integer age) {
        return age == null ? null : member.age.goe(age);
    }

    private BooleanExpression ageLoe(Integer age) {
        return age == null ? null : member.age.loe(age);
    }
}
