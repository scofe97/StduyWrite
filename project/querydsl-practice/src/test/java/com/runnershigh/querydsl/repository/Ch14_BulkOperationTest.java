package com.runnershigh.querydsl.repository;

import static com.runnershigh.querydsl.domain.QMember.member;
import static com.runnershigh.querydsl.domain.QOrderItem.orderItem;
import static org.assertj.core.api.Assertions.assertThat;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import com.runnershigh.querydsl.domain.Member;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

/**
 * Ch14 — 벌크 연산과 단건 변경 (학습 노트: write/05_data/querydsl/01-07.벌크 연산과 SQL 함수.md).
 *
 * 핵심 대비:
 * - 단건 변경 → 변경 감지(dirty checking) / em.remove / em.persist (1차 캐시·DB 동기)
 * - 다건 일괄 → QueryDSL update()/delete().execute() (영속성 컨텍스트 우회 → clear 필요)
 *
 * @DataJpaTest 는 각 테스트를 트랜잭션으로 감싸 끝나면 롤백하므로, 시드 데이터를 수정/삭제해도 안전하다.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class Ch14_BulkOperationTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    // === 기본 케이스 (참고용 — 노트 §2, §3 과 1:1 대응) ===

    @Test
    @DisplayName("벌크 UPDATE — 조건에 맞는 다건의 age 를 한 번에 +1, 반환값은 영향 행 수")
    void bulk_update_returns_affected_row_count() {
        long before = queryFactory.select(member.count())
                .from(member)
                .where(member.age.lt(28))
                .fetchOne();

        long affected = queryFactory
                .update(member)
                .set(member.age, member.age.add(1))
                .where(member.age.lt(28))
                .execute();

        // 한 번의 UPDATE 로 28세 미만 전원의 age 가 +1 됨 — 영향 행 수가 반환된다.
        assertThat(affected).isEqualTo(before);
    }

    @Test
    @DisplayName("벌크 연산은 영속성 컨텍스트를 우회한다 — clear 전엔 1차 캐시가 옛 값을 들고 있다")
    void bulk_update_bypasses_persistence_context() {
        // 먼저 한 회원을 1차 캐시에 적재
        Member loaded = queryFactory.selectFrom(member)
                .where(member.age.lt(28))
                .fetchFirst();
        int originalAge = loaded.getAge();

        // 벌크로 age +10 (DB 는 바뀌지만 1차 캐시의 loaded 는 그대로)
        queryFactory.update(member)
                .set(member.age, member.age.add(10))
                .where(member.id.eq(loaded.getId()))
                .execute();

        // 같은 엔티티를 다시 find → 1차 캐시 히트 → DB 와 어긋난 옛 값
        Member stillCached = em.find(Member.class, loaded.getId());
        assertThat(stillCached.getAge()).isEqualTo(originalAge); // 함정: 옛 값

        // 안전한 대응: flush + clear 후 다시 읽으면 DB 의 최신 값
        em.flush();
        em.clear();
        Member fresh = em.find(Member.class, loaded.getId());
        assertThat(fresh.getAge()).isEqualTo(originalAge + 10);
    }

    @Test
    @DisplayName("벌크 DELETE — where 조건에 맞는 다건을 한 번에 삭제, 반환값은 삭제 행 수")
    void bulk_delete_returns_deleted_row_count() {
        // 회원은 주문 1건씩 가져 FK 때문에 바로 못 지운다(Member←Order←OrderItem 연쇄).
        // 그래서 말단(leaf)인 OrderItem 을 벌크 삭제한다 — 아무도 참조하지 않아 FK 충돌이 없다.
        // 시드 count 분포는 1~5 (1 + (i-1)%5). count >= 4 인 일부만 골라 삭제한다.
        long target = queryFactory.select(orderItem.count())
                .from(orderItem)
                .where(orderItem.count.goe(4))
                .fetchOne();
        assertThat(target).isPositive();

        long deleted = queryFactory
                .delete(orderItem)
                .where(orderItem.count.goe(4))
                .execute();

        assertThat(deleted).isEqualTo(target);
    }

    // === 실습 (노트 §1 단건 변경 — QueryDSL 이 아니라 EntityManager 가 한다) ===

    @Test
    @DisplayName("실습1: 단건 UPDATE 는 변경 감지로 처리한다 (queryFactory.update 없이도 UPDATE 발행)")
    void single_update_via_dirty_checking() {
        // 한 건을 조회 — 영속 상태로 1차 캐시에 들어온다.
        Member found = queryFactory.selectFrom(member).fetchFirst();
        Long id = found.getId();

        // 변경 메서드만 호출 — save()/update() 어느 것도 부르지 않는다.
        found.changeAge(99);

        // flush 시점에 변경 감지가 UPDATE 를 발행. clear 로 1차 캐시를 비우고 DB 에서 다시 읽는다.
        em.flush();
        em.clear();

        Member reloaded = em.find(Member.class, id);
        assertThat(reloaded.getAge()).isEqualTo(99);
    }

    @Test
    @DisplayName("실습2: 단건 DELETE 는 em.remove 로 처리한다")
    void single_delete_via_em_remove() {
        // 시드 회원은 주문을 가져 FK 충돌이 난다. 주문 없는 회원을 만들어 그 회원을 지운다.
        Member tmp = Member.builder().username("to_delete").age(40).build();
        em.persist(tmp);
        em.flush();
        Long id = tmp.getId();

        em.remove(tmp);
        em.flush();

        Member gone = queryFactory.selectFrom(member)
                .where(member.id.eq(id))
                .fetchOne();
        assertThat(gone).isNull();
    }

    @Test
    @DisplayName("실습3: INSERT 는 em.persist 로 한다 (QueryDSL 에는 INSERT 가 없다)")
    void single_insert_via_em_persist() {
        long before = queryFactory.select(member.count()).from(member).fetchOne();

        em.persist(Member.builder().username("eve").age(20).build());
        em.flush();

        long after = queryFactory.select(member.count()).from(member).fetchOne();
        assertThat(after).isEqualTo(before + 1);
    }
}
