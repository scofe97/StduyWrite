package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.dto.MemberSearchDto;
import java.util.List;

/**
 * 학습 노트: jpa/03-05.커스텀 리포지토리 패턴.
 * Spring Data JPA 가 {@code <Interface>Impl} 명명 규칙으로 구현을 자동 결합한다.
 */
public interface MemberRepositoryCustom {

    List<Member> findByUsernameContains(String keyword);

    List<MemberSearchDto> searchAsDto(String usernameKeyword, Integer minAge, Integer maxAge);
}
