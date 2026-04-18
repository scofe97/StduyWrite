package com.study.redpanda;

import org.springframework.test.context.ActiveProfiles;

/**
 * Ch05~Ch11 통합 테스트 공통 설정
 *
 * docker-compose의 로컬 인프라를 직접 사용한다:
 * - Redpanda: localhost:19092 (Kafka) + localhost:18081 (Schema Registry)
 * - PostgreSQL: localhost:15432/saga
 *
 * 사전 조건: docker-compose up -d (Redpanda + PostgreSQL 실행 상태)
 */
@ActiveProfiles("local")
public abstract class AbstractLocalTest {
}
