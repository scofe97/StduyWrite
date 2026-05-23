package com.runnershigh.querydsl.config;

import com.querydsl.jpa.impl.JPAQueryFactory;
import jakarta.persistence.EntityManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * JPAQueryFactory 빈 등록.
 * <p>
 * 학습 노트: write/05_data/spring/querydsl/01-02.프로젝트 셋업 (Gradle 6.12).md
 */
@Configuration
public class QuerydslConfig {

    @Bean
    public JPAQueryFactory jpaQueryFactory(EntityManager em) {
        return new JPAQueryFactory(em);
    }
}
