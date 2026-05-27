package com.runnershigh.querydsl.learning;

import com.runnershigh.querydsl.config.QuerydslConfig;
import java.lang.reflect.Field;
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
 * 학습 데모 — JDBC wrapper 양파 구조를 런타임 객체로 직접 관찰한다.
 *
 * 학습 문서: write/05_data/05-01.JDBC 드라이버 wrap 로깅의 운영 비용.md (§0.2 ~ §0.3)
 *
 * 확인 포인트:
 *   1) DataSource 빈 자체가 datasource-proxy 의 한 겹으로 감싸졌는지
 *   2) Connection 의 실제 런타임 클래스 (양파 바깥 껍질)
 *   3) 단순 캐스팅이 ClassCastException 으로 실패한다는 것
 *   4) isWrapperFor + unwrap 으로 알맹이 (PGConnection) 까지 안전하게 내려가는 것
 *
 * test profile 이 PostgreSQL (Supabase) 이므로 알맹이 타깃은 org.postgresql.PGConnection.
 */
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@ActiveProfiles("log4jdbc")
@Import(QuerydslConfig.class)
class JdbcWrapperOnionTest {

    @Autowired
    private DataSource dataSource;

    @Test
    @DisplayName("양파 구조 — DataSource/Connection 실제 클래스 + 단순 캐스팅 실패 vs unwrap 성공")
    void onion_layers_and_unwrap() throws Exception {
        System.out.println();
        System.out.println("=== JDBC wrapper 양파 구조 관찰 ===");

        // postgresql 드라이버는 runtimeOnly 라 컴파일 시점에 타입을 직접 참조할 수 없다.
        // Class.forName 으로 reflection 참조 — 학습 의도(런타임 클래스 관찰)와도 정합.
        Class<?> pgConnectionIface = Class.forName("org.postgresql.PGConnection");
        Class<?> pgConnectionImpl  = Class.forName("org.postgresql.jdbc.PgConnection");

        // 1. DataSource 빈 자체가 한 겹 (datasource-proxy starter 가 씌움)
        System.out.println("[1] DataSource 클래스 = " + dataSource.getClass().getName());

        try (Connection conn = dataSource.getConnection()) {
            // 2. Connection 의 바깥 껍질
            System.out.println("[2] Connection 클래스 = " + conn.getClass().getName());

            // 2-1. JDK 동적 프록시면 InvocationHandler 도 같이 노출
            if (Proxy.isProxyClass(conn.getClass())) {
                System.out.println("    └ JDK Proxy handler = "
                        + Proxy.getInvocationHandler(conn).getClass().getName());
            }

            // 3. 단순 캐스팅 — 실패하는 자리.
            //    Class.cast() 가 (T) obj 캐스팅과 같은 ClassCastException 을 던진다.
            System.out.println("[3] 단순 캐스팅 시도: " + pgConnectionImpl.getName() + ".cast(conn)");
            try {
                Object pg = pgConnectionImpl.cast(conn);
                System.out.println("    예상 외 — 캐스팅이 성공함. 양파 한 겹뿐일 가능성. " + pg);
            } catch (ClassCastException e) {
                System.out.println("    ❌ ClassCastException = " + e.getMessage());
            }

            // 4. 표준 unwrap — 양파를 안전하게 푸는 방법
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

    /**
     * (b) Driver 교체형의 핵심 — Hikari 안에 *숨은* log4jdbc ConnectionSpy 를 reflection
     * 으로 직접 확인한다.
     *
     * 표면 관찰(첫 번째 테스트) 만으로는 `HikariProxyConnection` 까지만 보이고 log4jdbc
     * 흔적은 안 드러난다. HikariProxyConnection.delegate (부모 ProxyConnection 의 protected
     * 필드) 를 Field.setAccessible 로 까면 그 안에 ConnectionSpy 가 박혀 있는 게 확인된다.
     *
     * 학습 의도: 학습 문서 §1 (b) Driver 교체형이 "Hikari 의 아래에 끼어 표면엔 안 보인다"
     *           고 한 사실을 *코드로 직접 증명*. 표면 관찰만 신뢰하면 wrap 라이브러리의
     *           존재 자체를 놓칠 수 있다는 함정을 박제한다.
     */
    @Test
    @DisplayName("(b) Driver 교체형 — Hikari 안에 숨은 log4jdbc ConnectionSpy 를 reflection 으로 확인")
    void peek_hidden_log4jdbc_layer() throws Exception {
        System.out.println();
        System.out.println("=== Hikari 안쪽 양파 까기 (reflection) ===");

        try (Connection conn = dataSource.getConnection()) {
            System.out.println("[표면] " + conn.getClass().getName());

            Object current = conn;
            for (int depth = 1; depth <= 5; depth++) {
                Field delegateField = findField(current.getClass(), "delegate");
                if (delegateField == null) {
                    System.out.println("[깊이 " + depth + "] delegate 필드 없음 — 알맹이 도달 직전 또는 종착");
                    break;
                }
                delegateField.setAccessible(true);
                Object next = delegateField.get(current);
                if (next == null) {
                    System.out.println("[깊이 " + depth + "] delegate = null");
                    break;
                }
                System.out.println("[깊이 " + depth + "] delegate = " + next.getClass().getName());
                current = next;
            }
        }

        System.out.println("=== /관찰 종료 ===");
        System.out.println();
    }

    /**
     * 상위 클래스까지 거슬러 올라가며 필드를 찾는다.
     * HikariProxyConnection 의 delegate 는 부모 ProxyConnection 에 선언돼 있어
     * getDeclaredField 한 번으로는 못 찾는다.
     */
    private static Field findField(Class<?> clazz, String name) {
        while (clazz != null) {
            try {
                return clazz.getDeclaredField(name);
            } catch (NoSuchFieldException ignore) {
                clazz = clazz.getSuperclass();
            }
        }
        return null;
    }
}
