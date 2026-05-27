package com.runnershigh.querydsl.learning;

import com.runnershigh.querydsl.config.QuerydslConfig;
import java.lang.reflect.Proxy;
import java.sql.Connection;
import javax.sql.DataSource;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase.Replace;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

/**
 * 학습 데모 — (a) DataSource 래퍼형 자리에 wrap 라이브러리가 끼었을 때의
 * 양파 구조를 런타임 객체로 관찰한다.
 *
 * profile : test (datasource-proxy 활성, 순정 PostgreSQL driver)
 * 자매    : JdbcWrapperOnionTest (profile=log4jdbc) — (b) Driver 교체형 자리
 *
 * 학습 문서: write/05_data/05-01.JDBC 드라이버 wrap 로깅의 운영 비용.md
 *   §1 Driver 교체형 vs DataSource 래퍼형
 *
 * 핵심 관찰 (두 자리의 차이가 표면에 그대로 박힌다):
 *   [1] dataSource.getClass() = DecoratedDataSource (wrap 흔적이 *표면에* 노출)
 *   [2] conn.getClass()       = JDK $ProxyNN + handler = ConnectionInvocationHandler
 *   [3] 단순 캐스팅 (PgConnection) 실패
 *   [4] unwrap(PGConnection.class) 성공 — 알맹이 PgConnection 까지 도달
 *
 * (b) Driver 교체형(JdbcWrapperOnionTest) 과의 차이:
 *   - 그쪽은 [1] HikariDataSource, [2] HikariProxyConnection — 표면에 wrap 흔적 없음
 *   - 대신 jdbc.audit / jdbc.* 로그가 찍히는 사실로 동작을 증명
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("test")
@Import(QuerydslConfig.class)
class DataSourceWrapperOnionTest {

    @Autowired
    private DataSource dataSource;

    @Test
    @DisplayName("(a) DataSource 래퍼형 — DecoratedDataSource + JDK Proxy 가 표면에 노출 / unwrap 알맹이 도달")
    void datasource_wrapper_layers_and_unwrap() throws Exception {
        System.out.println();
        System.out.println("=== (a) DataSource 래퍼형 양파 관찰 ===");

        Class<?> pgConnectionIface = Class.forName("org.postgresql.PGConnection");
        Class<?> pgConnectionImpl  = Class.forName("org.postgresql.jdbc.PgConnection");

        // [1] DataSource 빈 자체가 wrap 라이브러리 클래스 — 표면에 노출.
        //     (b) Driver 교체형은 여기서 그냥 HikariDataSource 가 보임.
        System.out.println("[1] DataSource 클래스 = " + dataSource.getClass().getName());

        try (Connection conn = dataSource.getConnection()) {
            // [2] Connection 도 wrap 라이브러리 프록시 — 표면에 노출.
            System.out.println("[2] Connection 클래스 = " + conn.getClass().getName());

            if (Proxy.isProxyClass(conn.getClass())) {
                System.out.println("    └ JDK Proxy handler = "
                        + Proxy.getInvocationHandler(conn).getClass().getName());
            }

            // [3] 단순 캐스팅 — 실패.
            //     conn 의 실제 클래스는 JDK 동적 프록시고, PgConnection 과 형제 타입일 뿐.
            System.out.println("[3] 단순 캐스팅 시도: " + pgConnectionImpl.getName() + ".cast(conn)");
            try {
                Object pg = pgConnectionImpl.cast(conn);
                System.out.println("    예상 외 — 캐스팅이 성공함. " + pg);
            } catch (ClassCastException e) {
                System.out.println("    ❌ ClassCastException = " + e.getMessage());
            }

            // [4] unwrap — 양파를 안전하게 푸는 표준 메서드.
            //     wrap 라이브러리가 표면이 다르더라도 알맹이까지 도달하는 동작은 같다.
            System.out.println("[4] conn.isWrapperFor(PGConnection) + conn.unwrap(...)");
            if (conn.isWrapperFor(pgConnectionIface)) {
                Object pg = conn.unwrap(pgConnectionIface);
                System.out.println("    ✅ unwrap 성공, 알맹이 클래스 = " + pg.getClass().getName());
            } else {
                System.out.println("    ⚠ isWrapperFor=false — PGConnection 알맹이를 못 찾음");
            }
        }

        System.out.println("=== /관찰 종료 ===");
        System.out.println();
    }
}
