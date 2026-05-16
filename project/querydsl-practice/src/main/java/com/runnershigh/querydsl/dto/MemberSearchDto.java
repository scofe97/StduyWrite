package com.runnershigh.querydsl.dto;

import com.querydsl.core.annotations.QueryProjection;

/**
 * @QueryProjection 로 받는 DTO 예제 — 회원 검색 결과 행.
 * 학습 노트: 01-05.프로젝션과 DTO 매핑 — 트레이드오프(QueryDSL 의존 vs 컴파일 안정성).
 * <p>
 * Q클래스(QMemberSearchDto)가 함께 생성되며, 사용처에서 {@code new QMemberSearchDto(...)} 로 호출한다.
 */
public class MemberSearchDto {

    private final String username;
    private final int age;
    private final String city;

    @QueryProjection
    public MemberSearchDto(String username, int age, String city) {
        this.username = username;
        this.age = age;
        this.city = city;
    }

    public String getUsername() {
        return username;
    }

    public int getAge() {
        return age;
    }

    public String getCity() {
        return city;
    }
}
