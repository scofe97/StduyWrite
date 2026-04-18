package com.study.redpanda.ch03;

import org.springframework.test.context.ActiveProfiles;

/**
 * Ch03 SAGA 테스트 공통 설정
 *
 * docker-compose의 로컬 인프라를 직접 사용한다:
 * - Redpanda: localhost:19092 (Kafka) + localhost:18081 (Schema Registry)
 * - PostgreSQL: localhost:15432/saga
 *
 * Testcontainers 대신 로컬 인프라를 사용하는 이유:
 * 1. @SpringBootTest가 전체 앱(ch02 Avro + ch03 JSON)을 로드하므로,
 *    application.yml의 local 프로파일에 설정된 Avro 직렬화 설정이 필요하다.
 * 2. docker-compose가 이미 실행 중이면 테스트 시작이 빠르다.
 * 3. 테스트 후 DB 데이터를 직접 확인할 수 있다 (ddl-auto: create-drop).
 *
 * 사전 조건: docker-compose up -d (Redpanda + PostgreSQL 실행 상태)
 */
@ActiveProfiles("local")
public abstract class AbstractSagaTest {
}
