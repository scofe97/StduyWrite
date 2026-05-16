package com.runnershigh.querydsl.config;

import jakarta.annotation.PostConstruct;
import jakarta.persistence.EntityManagerFactory;
import org.hibernate.dialect.Dialect;
import org.hibernate.engine.spi.SessionFactoryImplementor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.DatabaseMetaData;

@Component
public class DbInfoPrinter {

    private static final Logger log = LoggerFactory.getLogger("DB");

    private final DataSource dataSource;
    private final EntityManagerFactory emf;

    public DbInfoPrinter(DataSource dataSource, EntityManagerFactory emf) {
        this.dataSource = dataSource;
        this.emf = emf;
    }

    @PostConstruct
    public void print() {
        System.out.println(">>> DbInfoPrinter @PostConstruct called");
        try (Connection conn = dataSource.getConnection()) {
            DatabaseMetaData md = conn.getMetaData();
            Dialect dialect = emf.unwrap(SessionFactoryImplementor.class).getJdbcServices().getDialect();
            log.info("=== Database Info ===");
            log.info("URL      : {}", md.getURL());
            log.info("User     : {}", md.getUserName());
            log.info("Product  : {} {}", md.getDatabaseProductName(), md.getDatabaseProductVersion());
            log.info("Driver   : {} {}", md.getDriverName(), md.getDriverVersion());
            log.info("Schema   : {}", conn.getSchema());
            log.info("Dialect  : {}", dialect.getClass().getSimpleName());
            log.info("=====================");
        } catch (Exception e) {
            log.warn("DB 정보 조회 실패: {}", e.getMessage());
        }
    }
}
