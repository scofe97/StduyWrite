package com.study.redpanda.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;

@Configuration
public class KafkaTopicConfig {

    // ─── 토픽 유형 분류 ───────────────────────────────────────────────────
    // Event Topic: 발생한 사실을 기록 (cleanup.policy=delete, retention 기반)
    //   → chapter2.orders, chapter2.error-test, chapter2.retryable-test,
    //     chapter2.idempotent-test, chapter2.pause-test, chapter2.circuit-test
    // Command → Event 파이프라인: 입력(Command) → 처리 → 출력(Event)
    //   → chapter2.sendto-input (Command), chapter2.sendto-output (Event)
    // DLT 패턴: 재시도 소진 후 실패 메시지 격리 (파티션 1, 짧은 retention)
    //   → chapter2.error-test-dlt
    // 학습용 네이밍(chapter{n}.{purpose})이므로 프로덕션 패턴({team}.{domain}.{entity})과 다름

    // ch02: basic producer-consumer — Event Topic 패턴
    @Bean
    public NewTopic chapter2OrdersTopic() {
        return TopicBuilder.name("chapter2.orders")
                .partitions(3)
                .replicas(1)
                .build();
    }

    // ch02 C5: 에러 핸들러 테스트용 토픽
    @Bean
    public NewTopic chapter2ErrorTestTopic() {
        return TopicBuilder.name("chapter2.error-test")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C5: DLT (Dead Letter Topic) — DLT 패턴: 재시도 소진 후 메시지가 전송되는 토픽
    @Bean
    public NewTopic chapter2ErrorTestDltTopic() {
        return TopicBuilder.name("chapter2.error-test-dlt")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C6: @RetryableTopic 테스트용 원본 토픽
    // 재시도 토픽(-retry-0, -retry-1)과 DLT(-dlt)는 @RetryableTopic이 자동 생성
    @Bean
    public NewTopic chapter2RetryableTestTopic() {
        return TopicBuilder.name("chapter2.retryable-test")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C9: Idempotent Consumer 테스트용 토픽
    @Bean
    public NewTopic chapter2IdempotentTestTopic() {
        return TopicBuilder.name("chapter2.idempotent-test")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C4: @SendTo 파이프라인 입력 토픽 — Command Topic 패턴 (수행 요청)
    @Bean
    public NewTopic chapter2SendToInputTopic() {
        return TopicBuilder.name("chapter2.sendto-input")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C4: @SendTo 파이프라인 출력 토픽 — Event Topic 패턴 (처리 결과)
    @Bean
    public NewTopic chapter2SendToOutputTopic() {
        return TopicBuilder.name("chapter2.sendto-output")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C7: Consumer Pause 테스트용 토픽
    @Bean
    public NewTopic chapter2PauseTestTopic() {
        return TopicBuilder.name("chapter2.pause-test")
                .partitions(1)
                .replicas(1)
                .build();
    }

    // ch02 C8: Circuit Breaker 테스트용 토픽
    @Bean
    public NewTopic chapter2CircuitTestTopic() {
        return TopicBuilder.name("chapter2.circuit-test")
                .partitions(1)
                .replicas(1)
                .build();
    }
}
