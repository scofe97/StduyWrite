package com.study.redpanda.config;

import org.springframework.test.context.ActiveProfiles;

/**
 * 로컬 Redpanda(docker-compose) 기반 테스트 공통 설정
 *
 * Testcontainers 대신 로컬에 이미 실행 중인 Redpanda를 사용한다.
 * application.yml의 local 프로필 설정을 그대로 활용한다.
 * (localhost:19092 + Schema Registry localhost:18081)
 *
 * 전환 방법: extends AbstractKafkaTest ↔ extends AbstractLocalKafkaTest
 */
@ActiveProfiles("local")
public abstract class AbstractLocalKafkaTest {
}
