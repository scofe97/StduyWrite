package com.study.redpanda.ch02.config;

import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.common.TopicPartition;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.util.backoff.FixedBackOff;

/**
 * Ch02 C5: DefaultErrorHandler + DLT 설정
 *
 * @Bean으로 등록하면 Spring Kafka가 모든 Listener Container에 자동 적용한다.
 * Container Factory에 수동으로 setCommonErrorHandler()를 호출할 필요 없다.
 *
 * 동작 흐름:
 * 예외 발생 → BackOff에 따라 재시도 → 재시도 소진 → Recoverer가 DLT로 전송 → offset 전진
 */
@Slf4j
@Configuration
public class KafkaErrorConfig {

    /**
     * DefaultErrorHandler: Consumer 에러 처리의 표준 메커니즘 (Spring Kafka 2.8+)
     *
     * @param kafkaTemplate DLT로 메시지를 전송할 때 사용하는 KafkaTemplate.
     *                      raw 타입을 사용하는 이유: DLT에는 원본 메시지의 byte[]가 그대로 전송되며,
     *                      DeadLetterPublishingRecoverer가 내부적으로 원본 ConsumerRecord를 사용하기 때문이다.
     */
    @Bean
    public DefaultErrorHandler errorHandler(@Qualifier("kafkaTemplate") KafkaTemplate<?, ?> kafkaTemplate) {
        // 1. Recoverer: 재시도 소진 후 DLT로 전송
        //    토픽 이름 규칙: {원본토픽}-dlt, 파티션 -1은 "자동 할당"을 의미
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(
                kafkaTemplate,
                (record, ex) -> {
                    log.warn("Sending to DLT: topic={}, offset={}, exception={}",
                            record.topic(), record.offset(), ex.getMessage());
                    return new TopicPartition(record.topic() + "-dlt", -1);
                }
        );

        // 2. BackOff: 1초 간격으로 최대 2회 재시도 (총 시도 = 1회 원본 + 2회 재시도 = 3회)
        FixedBackOff backOff = new FixedBackOff(1000L, 2);

        DefaultErrorHandler errorHandler = new DefaultErrorHandler(recoverer, backOff);

        log.info("DefaultErrorHandler registered: backOff=1000ms x 2 retries, recoverer=DLT");
        return errorHandler;
    }
}
