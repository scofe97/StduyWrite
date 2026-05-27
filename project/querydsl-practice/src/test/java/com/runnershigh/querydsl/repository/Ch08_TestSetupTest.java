package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Member;
import com.runnershigh.querydsl.support.TestDataLoader.Fixture;
import jakarta.persistence.EntityManager;
import java.util.List;
import org.hibernate.Session;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Ch08 — 테스트 셋업 (Q 클래스, @DataJpaTest, JPAQueryFactory 빈 결합).
 *
 * 학습 노트: write/05_data/querydsl/03-01.테스트와 멀티모듈.md
 *
 * 5개 추가 슬롯은 노트 5개 절에 1:1 대응한다.
 *   1. §테스트 슬라이스 선택지         → applicationContextLoadsOnlyJpaSlice
 *   2. §@DataJpaTest에 JPAQueryFactory → searchByUsernameContains
 *   3. §Replace.NONE                   → databaseProductNameIsPostgreSQL
 *   4. §given-when-then 페이징         → pagingFollowsRequestedPageSize
 *   5. §fragment 단위 테스트(변형)     → customFragmentMethodAlone
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch08_TestSetupTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    @Autowired
    private MemberRepository memberRepository;

    @Autowired
    private ApplicationContext applicationContext;

    private final Fixture fixture = new Fixture(
            1000, 900, 100, 1L, 1000L, 1L, 100L, 1L);

    @Test
    @DisplayName("JPAQueryFactory + Q 클래스로 카운트")
    void query_factory_and_qclass_count() {
        long count = queryFactory.select(member.count()).from(member).fetchOne();
        assertThat(count).isEqualTo(fixture.memberCount());
    }

    /**
     * 슬롯 1 — §테스트 슬라이스 선택지.
     *
     * @DataJpaTest 슬라이스가 *JPA 관련 빈만* 올린다는 사실을 입증한다.
     * jpaQueryFactory · memberRepository 는 컨텍스트에 등록되어 있어야 하고,
     * @Service 빈이 끼어드는지 확인하려 임의 service 빈 조회는 NoSuchBeanDefinitionException 으로 끝나야 한다
     * (이 프로젝트는 service 가 아예 없지만, "JPA 외 임의 클래스가 자동 등록되지 않는다"는 슬라이스 성질을 강제).
     */
    @Test
    @DisplayName("@DataJpaTest 슬라이스는 JPA 빈만 올린다")
    void applicationContextLoadsOnlyJpaSlice() {
        assertThat(applicationContext.containsBean("jpaQueryFactory")).isTrue();
        assertThat(applicationContext.containsBean("memberRepository")).isTrue();
        assertThat(applicationContext.containsBean("entityManagerFactory")).isTrue();

        assertThat(applicationContext.getBeansOfType(JPAQueryFactory.class)).hasSize(1);

        assertThatThrownBy(() -> applicationContext.getBean("nonExistingServiceBean"))
                .isInstanceOf(NoSuchBeanDefinitionException.class);
    }

    /**
     * 슬롯 2 — §@DataJpaTest에 JPAQueryFactory 붙이기.
     *
     * 노트 예제는 `repository.search(cond)` 시그니처를 가정하지만, 본 프로젝트는
     * MemberRepositoryCustom#findByUsernameContains 로 같은 의도를 표현한다.
     * 시드 username 은 "user_00001..user_01000" 형식이므로 키워드 "user_0" 으로 1,000명 전원이 잡힌다.
     */
    @Test
    @DisplayName("이름 부분일치 검색 — JPAQueryFactory 빈이 살아 있어야 통과")
    void searchByUsernameContains() {
        // given — 픽스처 1,000명 시드가 이미 적재되어 있다.

        // when
        List<Member> result = memberRepository.findByUsernameContains("user_0");

        // then
        assertThat(result).isNotEmpty();
        assertThat(result).allMatch(m -> m.getUsername().contains("user_0"));
    }

    /**
     * 슬롯 3 — §Replace.NONE.
     *
     * Replace.NONE + @ActiveProfiles("test") 조합이 H2 자동 교체를 끄고
     * application-test.yml 의 PostgreSQL DataSource 를 그대로 쓴다는 것을 직접 확인한다.
     */
    @Test
    @DisplayName("Replace.NONE 이면 실제 PostgreSQL DataSource 가 살아 있다")
    void databaseProductNameIsPostgreSQL() {
        Session session = em.unwrap(Session.class);
        String productName = session.doReturningWork(
                conn -> conn.getMetaData().getDatabaseProductName());

        assertThat(productName).isEqualTo("PostgreSQL");
    }

    /**
     * 슬롯 4 — §given-when-then 페이징.
     *
     * 노트의 `repository.searchPage(...)` 는 본 프로젝트에 없으므로
     * Spring Data JPA 기본 findAll(Pageable) 로 동일 의도를 검증한다.
     * 시드 변동을 흡수하려 totalElements 는 fixture.memberCount() 이상만 단언한다.
     */
    @Test
    @DisplayName("페이지 크기 10 을 요청하면 콘텐츠 10건, total 은 시드 이상")
    void pagingFollowsRequestedPageSize() {
        // given — 시드 1,000명.

        // when
        Page<Member> page = memberRepository.findAll(PageRequest.of(0, 10));

        // then
        assertThat(page.getContent()).hasSize(10);
        assertThat(page.getTotalElements()).isGreaterThanOrEqualTo(fixture.memberCount());
        assertThat(page.getTotalPages()).isGreaterThanOrEqualTo(fixture.memberCount() / 10);
    }

    /**
     * 슬롯 5 — §fragment 단위 테스트(변형).
     *
     * 본 프로젝트엔 별도 fragment 인터페이스가 없으므로,
     * MemberRepositoryCustom 메서드 하나만을 단독으로 호출해 좁은 단위로 검증한다.
     * 실패하면 fragment 구현(MemberRepositoryImpl) 안의 BooleanExpression 조립 또는
     * JPAQueryFactory 주입에 한정해 원인을 격리할 수 있다.
     */
    @Test
    @DisplayName("커스텀 fragment 메서드 단독 호출 — DTO 프로젝션이 좁은 단위로 동작")
    void customFragmentMethodAlone() {
        // when
        var result = memberRepository.searchAsDto("user_0", null, null);

        // then
        assertThat(result).isNotEmpty();
        assertThat(result).allMatch(dto -> dto.getUsername().contains("user_0"));
    }
}
