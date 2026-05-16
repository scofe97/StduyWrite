package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.jpa.impl.JPAQueryFactory;
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
 * Ch08 — 테스트와 멀티모듈 (학습 노트: 02-02.테스트와 멀티모듈.md)
 * <p>
 * 핵심: @DataJpaTest + JPAQueryFactory 빈을 어떻게 끌고 들어오는가.
 * Q클래스 가시성, build/generated 경로, IDE 가 못 찾을 때의 진단.
 * <p>
 * 실습:
 * - [ ] @DataJpaTest 만 단독 사용 시 JPAQueryFactory 미등록 → @Import 없이는 NoSuchBeanDefinitionException
 * - [ ] @SpringBootTest 로 바꿨을 때 비용/속도 차이
 * - [ ] build.gradle 에서 annotationProcessor 한 줄을 빼고 빌드 → Q클래스 누락 에러 재현
 */
@DataJpaTest
@Import(QuerydslConfig.class)
class Ch08_TestSetupTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    @BeforeEach
    void setUp() {
        new TestDataLoader(em).loadDefault();
    }

    @Test
    @DisplayName("[Green] JPAQueryFactory 빈이 주입되고 Q클래스가 컴파일된다")
    void JPAQueryFactory_빈이_주입되고_Q클래스가_컴파일된다() {
        long count = queryFactory.selectFrom(member).fetchCount();
        assertThat(count).isEqualTo(4);
    }

    // TODO [실습 1] @Import 를 제거하고 테스트 — 어떤 에러가 나는지 메시지 정리
    // TODO [실습 2] build/generated/sources/annotationProcessor/java/main 경로에서 Q클래스 직접 확인
    // TODO [실습 3] gradle clean 후 ./gradlew compileJava 만 실행 — Q클래스 생성 시점 관찰
}
