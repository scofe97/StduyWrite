package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.support.listquery.common.query.ListQueryColumn;

/**
 * 실습 5 — 학습 노트 02-04.
 * Member 검색·정렬 컬럼 enum. 운영 ApprovalManagementListColumn 의 시드 축소판.
 */
public enum MemberListColumn implements ListQueryColumn {
    USERNAME("username"),
    CITY("city"),
    AGE("age");

    private final String inputName;

    MemberListColumn(String inputName) {
        this.inputName = inputName;
    }

    @Override
    public String getInputName() {
        return inputName;
    }
}
