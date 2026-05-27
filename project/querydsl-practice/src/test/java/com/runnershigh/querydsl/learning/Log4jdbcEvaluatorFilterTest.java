package com.runnershigh.querydsl.learning;

import static com.runnershigh.querydsl.domain.QMember.member;

import com.querydsl.jpa.impl.JPAQueryFactory;
import com.runnershigh.querydsl.config.QuerydslConfig;
import jakarta.persistence.EntityManager;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadFactory;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

/**
 * 학습 데모 — log4jdbc 한 사이클이 약 20줄 쏟는 것 + logback EvaluatorFilter 가
 * 폴러 스레드(onion-poller-*) 의 log4jdbc/jdbc/hibernate.SQL 로그를 모두 차단하는 것.
 *
 * 학습 문서: write/05_data/05-01.JDBC 드라이버 wrap 로깅의 운영 비용.md
 *   - §2 출력 모델 비교 (log4jdbc 한 사이클 ~20줄)
 *   - §4 (4) EvaluatorFilter / §6 사고 회고 회차 3 fix
 *
 * 두 번 같은 쿼리를 실행한다.
 *   (A) JUnit 의 "Test worker" 스레드 — EvaluatorFilter 가 폴러 이름과 매칭 안 됨 → 통과 → 20줄
 *   (B) onion-poller-* 스레드 — EvaluatorFilter 매칭 → DENY → 0줄
 *
 * 콘솔 출력 비교로 §6 회고가 박제하는 *thread name 외과적 차단* 의 효과를 눈으로 확인한다.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("log4jdbc")
@Import(QuerydslConfig.class)
class Log4jdbcEvaluatorFilterTest {

    @Autowired
    private EntityManager em;

    @Autowired
    private JPAQueryFactory queryFactory;

    @Test
    @DisplayName("log4jdbc 한 사이클 라인 수 / EvaluatorFilter 폴러 차단 효과")
    @Transactional
    void emit_lines_and_filter_compare() throws Exception {
        System.out.println();
        System.out.println("=== [A] Test worker 스레드 — EvaluatorFilter 통과 (라인 그대로 노출) ===");
        runOneCycle();
        System.out.println("=== [/A] ===");
        System.out.println();

        System.out.println("=== [B] onion-poller-1 스레드 — EvaluatorFilter DENY (라인 0) ===");
        ThreadFactory factory = r -> {
            Thread t = new Thread(r);
            t.setName("onion-poller-1");
            t.setDaemon(true);
            return t;
        };
        Future<?> f = Executors.newSingleThreadExecutor(factory).submit(this::runOneCycle);
        f.get();  // 완료 대기
        System.out.println("=== [/B] ===");
        System.out.println();
    }

    private void runOneCycle() {
        // 한 사이클 = COUNT 한 번. log4jdbc 는 Connection/PreparedStatement/ResultSet 의 모든
        // 메서드 호출을 INFO 한 줄씩 찍으므로, 0건 SELECT 라도 약 15~20줄을 쏟는다.
        Long count = queryFactory.select(member.count()).from(member).fetchOne();
        System.out.println("    (cycle 결과: member count = " + count + ")");
    }
}
