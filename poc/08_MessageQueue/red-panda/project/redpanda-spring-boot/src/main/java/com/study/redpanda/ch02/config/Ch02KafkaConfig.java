package com.study.redpanda.ch02.config;

import jakarta.persistence.EntityManagerFactory;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.transaction.PlatformTransactionManager;

/**
 * ch02 전용 Kafka 기본 빈 설정
 *
 * ch03 SagaKafkaConfig가 ConsumerFactory, ProducerFactory, KafkaTemplate을 등록하면서
 * Spring Boot 자동 구성(@ConditionalOnMissingBean)이 차단된다.
 * ch02가 의존하는 기본 빈들을 명시적으로 생성한다.
 *
 * 반환 타입에 와일드카드(?, ?)를 사용하여 Spring Boot 자동 구성과 동일한 패턴을 따른다.
 * 이렇게 하면 KafkaTemplate<String, OrderEvent> 등 구체 타입 주입에도 매칭된다.
 *
 * @Primary로 표시하여 @Qualifier 없이 주입하면 이 빈들이 선택된다.
 * ch03 서비스는 @Qualifier("ch03...")로 명시적 지정하므로 영향 없음.
 *
 * 추가: ch03 KafkaTransactionManager가 TransactionManager 타입이므로
 * JPA의 transactionManager 자동 구성도 차단된다. JpaTransactionManager도 명시적 생성.
 */
@Configuration
public class Ch02KafkaConfig {

    /**
     * JPA TransactionManager (@Transactional 기본 대상)
     *
     * ch03 KafkaTransactionManager가 TransactionManager 인터페이스를 구현하므로
     * Spring Boot의 @ConditionalOnMissingBean(TransactionManager.class)이 트리거되어
     * JPA TransactionManager 자동 구성이 차단된다. 명시적으로 생성한다.
     */
    @Bean
    @Primary
    public PlatformTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }

    @Bean
    @Primary
    public DefaultKafkaConsumerFactory<?, ?> kafkaConsumerFactory(KafkaProperties kafkaProperties) {
        return new DefaultKafkaConsumerFactory<>(kafkaProperties.buildConsumerProperties(null));
    }

    @Bean
    @Primary
    public DefaultKafkaProducerFactory<?, ?> kafkaProducerFactory(KafkaProperties kafkaProperties) {
        return new DefaultKafkaProducerFactory<>(kafkaProperties.buildProducerProperties(null));
    }

    @Bean
    @Primary
    @SuppressWarnings({"unchecked", "rawtypes"})
    public KafkaTemplate<?, ?> kafkaTemplate(DefaultKafkaProducerFactory producerFactory) {
        return new KafkaTemplate<>(producerFactory);
    }

    @Bean
    @Primary
    @SuppressWarnings({"unchecked", "rawtypes"})
    public ConcurrentKafkaListenerContainerFactory<?, ?> kafkaListenerContainerFactory(
            DefaultKafkaConsumerFactory consumerFactory,
            KafkaTemplate kafkaTemplate) {
        ConcurrentKafkaListenerContainerFactory factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        factory.setReplyTemplate(kafkaTemplate);  // @SendTo 지원
        return factory;
    }
}
