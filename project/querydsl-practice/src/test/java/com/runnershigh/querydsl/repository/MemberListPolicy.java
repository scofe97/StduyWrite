package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.support.listquery.common.query.DetailConditionType;
import com.runnershigh.querydsl.support.listquery.common.query.ListQueryPolicy;
import com.runnershigh.querydsl.support.listquery.common.query.SortDirection;
import java.util.EnumSet;
import java.util.Map;
import java.util.Set;

/**
 * 실습 5 — Member 검색 정책 (운영 ApprovalManagementListQueryPolicy 시드 버전).
 * - 전체검색(ALL): USERNAME · CITY OR 결합
 * - 상세검색(DTL) 허용 조합: USERNAME=T(REGEXP), CITY=S(selection)
 * - 정렬: USERNAME/CITY/AGE
 */
public class MemberListPolicy implements ListQueryPolicy<MemberListColumn> {

    // 컬럼 타입 반환
    @Override
    public Class<MemberListColumn> getColumnType() {
        return MemberListColumn.class;
    }

    // 글로벌 검색 허용 컬럼
    @Override
    public Set<MemberListColumn> getGlobalSearchColumns() {
        return EnumSet.of(MemberListColumn.USERNAME, MemberListColumn.CITY);
    }

    // 상세 검색 허용 컬럼
    @Override
    public Map<MemberListColumn, Set<DetailConditionType>> getAllowedDetailConditionTypes() {
        return Map.of(
                MemberListColumn.USERNAME, EnumSet.of(DetailConditionType.T),
                MemberListColumn.CITY, EnumSet.of(DetailConditionType.S)
        );
    }

    // 정렬 가능 컬럼
    @Override
    public Set<MemberListColumn> getSortableColumns() {
        return EnumSet.allOf(MemberListColumn.class);
    }

    // 기본 정렬 컬럼
    @Override
    public MemberListColumn getDefaultSortColumn() {
        return MemberListColumn.USERNAME;
    }

    // 기본 정렬 방향
    @Override
    public SortDirection getDefaultSortDirection() {
        return SortDirection.ASC;
    }

    // 동점 처리기 (정렬 조건 같으면 이걸로 진행)
    @Override
    public MemberListColumn getTieBreakerSortColumn() {
        return MemberListColumn.USERNAME;
    }

    // 동정 처리기
    @Override
    public SortDirection getTieBreakerSortDirection() {
        return SortDirection.ASC;
    }
}
