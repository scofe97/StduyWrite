package com.runnershigh.querydsl.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.support.TestDataLoader;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

/**
 * Ch07 — 커스텀 리포지토리 패턴 (학습 노트: 02-01.커스텀 리포지토리 패턴.md)
 * <p>
 * 핵심: <Interface>Impl 명명 규칙으로 Spring Data JPA 가 fragment 를 결합한다.
 * MemberRepository 가 MemberRepositoryCustom 을 상속하면 Impl 메서드가 합쳐 노출된다.
 * <p>
 * 실습:
 * - [ ] MemberRepositoryImpl 의 명명을 일부러 바꿔보고 Spring 이 결합 못하는 에러 확인
 * - [ ] fragment 여러 개 합성: MemberRepository 가 두 개의 Custom 인터페이스를 상속하도록
 * - [ ] @SpringBootTest 와 @DataJpaTest 의 Repository 구성 차이 비교
 */
@DataJpaTest
@Import(QuerydslConfig.class)
class Ch07_CustomRepositoryTest {

    @Autowired
    private MemberRepository memberRepository;

    @Autowired
    private EntityManager em;

    @BeforeEach
    void setUp() {
        new TestDataLoader(em).loadDefault();
    }

    @Test
    @DisplayName("[Green] JpaRepository 메서드와 Custom 메서드가 같은 인터페이스로 노출된다")
    void JpaRepository_메서드와_Custom_메서드가_같은_인터페이스로_노출된다() {
        // JpaRepository 기본
        assertThat(memberRepository.count()).isEqualTo(4);

        // Custom 메서드 — Impl 클래스가 결합됐는지 확인
        assertThat(memberRepository.findByUsernameContains("li"))
                .extracting(m -> m.getUsername())
                .containsExactlyInAnyOrder("alice", "charlie");
    }

    @Test
    @DisplayName("[Green] searchAsDto — DTO 매핑까지 한 번에")
    void searchAsDto_DTO_매핑까지_한_번에() {
        var result = memberRepository.searchAsDto(null, 28, 35);

        assertThat(result)
                .extracting(d -> d.getUsername())
                .containsExactlyInAnyOrder("bob", "charlie");
    }

    // TODO [실습 1] Custom 인터페이스 두 개를 MemberRepository 가 동시에 상속해 fragment 합성 확인
    // TODO [실습 2] OrderRepository 도 같은 패턴으로 search/searchPage 를 호출해 보기
}
