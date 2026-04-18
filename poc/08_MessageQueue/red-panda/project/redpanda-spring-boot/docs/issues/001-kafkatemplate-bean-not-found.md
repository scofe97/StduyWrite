# Issue #001: KafkaTemplate 빈 생성 실패

## 증상

```
Parameter 0 of constructor in com.study.redpanda.ch02.producer.OrderProducer
required a bean of type 'org.springframework.kafka.core.KafkaTemplate' that could not be found.
```

모든 테스트(`HealthCheckControllerTest`, `ProducerConsumerTest` 등)에서 동일한 에러 발생. Java 17/21/25 버전 무관.

## 원인

`Ch09KafkaProducerConfig`에서 `ProducerFactory`와 `KafkaTemplate` 빈을 **@Qualifier 없이** 직접 등록했기 때문.

```java
// 문제 코드 (ch09/config/Ch09KafkaProducerConfig.java)
@Bean
public ProducerFactory<String, Object> ch09ProducerFactory() { ... }

@Bean
public KafkaTemplate<String, Object> ch09KafkaTemplate() { ... }
```

Spring Boot의 `KafkaAutoConfiguration`은 `@ConditionalOnMissingBean`으로 빈 존재 여부를 확인한다.

```java
// KafkaAutoConfiguration (Spring Boot 내부)
@Bean
@ConditionalOnMissingBean(ProducerFactory.class)  // ← ch09ProducerFactory가 있으면 SKIP
public DefaultKafkaProducerFactory<?, ?> kafkaProducerFactory(...) { ... }

@Bean
@ConditionalOnMissingBean(KafkaTemplate.class)    // ← ch09KafkaTemplate이 있으면 SKIP
public KafkaTemplate<?, ?> kafkaTemplate(...) { ... }
```

**결과**: ch09의 JSON용 빈이 등록되면서 → 자동설정의 Avro용 `ProducerFactory`/`KafkaTemplate` 생성이 차단됨 → ch02~ch08에서 `KafkaTemplate<String, OrderEvent>` 주입 실패.

## 진단 과정

1. Java 버전 의심 (Java 25 → 21 → 17) → 동일 실패, 버전 무관
2. 의존성 강제 갱신 (`--refresh-dependencies`) → 동일 실패
3. `debug=true`로 자동설정 리포트 확인 → **핵심 단서 발견**

```
KafkaAutoConfiguration#kafkaProducerFactory:
  Did not match:
    - @ConditionalOnMissingBean found beans of type 'ProducerFactory' → ch09ProducerFactory

KafkaAutoConfiguration#kafkaTemplate:
  Did not match:
    - @ConditionalOnMissingBean found beans of type 'KafkaTemplate' → ch09KafkaTemplate
```

## 해결 방법

### 방법 1: @Qualifier 추가 (공존)

커스텀 빈에 `@Qualifier`를 추가하면 자동설정이 이를 "같은 타입의 다른 빈"으로 인식하지 않는다.

```java
@Bean
@Qualifier("ch09")
public ProducerFactory<String, Object> ch09ProducerFactory() { ... }

@Bean
@Qualifier("ch09")
public KafkaTemplate<String, Object> ch09KafkaTemplate(
        @Qualifier("ch09") ProducerFactory<String, Object> producerFactory) { ... }
```

### 방법 2: 챕터 삭제 (현재 적용)

Ch09 디렉토리를 제거하여 충돌 빈 자체를 삭제.

## 교훈

1. **`@ConditionalOnMissingBean`의 타입 매칭은 인터페이스/부모 타입으로 동작한다.** 빈 이름이 다르더라도 (`ch09ProducerFactory` vs `kafkaProducerFactory`) 같은 `ProducerFactory` 타입이면 조건이 충족된다.

2. **커스텀 `ProducerFactory`/`KafkaTemplate` 빈을 등록할 때는 반드시 `@Qualifier`를 사용해야 한다.** 그렇지 않으면 Spring Boot 자동설정이 차단되어 다른 모든 챕터에 영향을 준다.

3. **진단 시 `debug=true`를 가장 먼저 확인해야 한다.** `CONDITIONS EVALUATION REPORT`에서 어떤 자동설정이 매칭되고 어떤 것이 스킵됐는지 즉시 알 수 있다. 테스트 환경에서는 `src/test/resources/application.properties`에 `debug=true`를 추가하면 된다.

## 환경

- Spring Boot 3.3.0
- spring-kafka 3.2.0
- Apache Avro 1.11.3
- io.confluent:kafka-avro-serializer:7.6.0
- Testcontainers: redpanda v25.3.6
