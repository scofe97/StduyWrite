package com.runnershigh.querydsl.repository;

import com.runnershigh.querydsl.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom {
}
