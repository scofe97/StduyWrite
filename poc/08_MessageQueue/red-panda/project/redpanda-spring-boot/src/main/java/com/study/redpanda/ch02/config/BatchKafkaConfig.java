package com.study.redpanda.ch02.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.listener.ContainerProperties;

/**
 * Ch02 C3: 배치 Consumer를 위한 전용 Factory 설정
 *
 * YAML의 spring.kafka.listener.* 는 모든 Consumer에 적용되는 전역 기본값이다.
 * Factory를 직접 만들면 특정 @KafkaListener에만 배치 모드를 적용할 수 있다.
 *
 * - 기본 Factory (kafkaListenerContainerFactory): 단일 메시지 모드
 * - 이 Factory (batchKafkaListenerContainerFactory): 배치 모드
 */
@Configuration
public class BatchKafkaConfig {

    /**
     * 배치 전용 ListenerContainerFactory
     *
     * @param consumerFactory Ch02KafkaConfig가 생성한 기본 ConsumerFactory.
     *                        ch03 SagaKafkaConfig가 자동 구성을 차단하므로 명시적 빈을 사용한다.
     */
    @Bean
    @SuppressWarnings("unchecked")
    public ConcurrentKafkaListenerContainerFactory<String, Object> batchKafkaListenerContainerFactory(
            @Qualifier("kafkaConsumerFactory") ConsumerFactory<String, Object> consumerFactory) {

        ConcurrentKafkaListenerContainerFactory<String, Object> factory =
                new ConcurrentKafkaListenerContainerFactory<>();

        // Ch02KafkaConfig가 생성한 ConsumerFactory 사용
        factory.setConsumerFactory(consumerFactory);

        // 배치 모드 활성화: @KafkaListener에 List<OrderEvent>가 전달된다
        factory.setBatchListener(true);

        // 수동 ACK: 배치 전체를 처리한 후 ack.acknowledge()로 offset 커밋
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);

        return factory;
    }
}
