# 4. Facts vs Deltas — 실습 (Kafka Streams)

ksqlDB SQL → Kafka Streams Java 변환 실습. Delta `aggregate()` → Fact 파이프라인, Avro Serde, TopologyTestDriver. 선행: [03-facts-vs-deltas.md](./03-facts-vs-deltas.md).

---

## 1. 실습 시나리오

사용자 프로필 서비스에서 필드가 변경될 때마다 Delta 이벤트를 발행한다. 이 Delta 이벤트들을 Kafka Streams로 집계하여 사용자의 현재 전체 상태(Fact)를 별도 토픽에 발행하고 State Store에도 유지한다.

```
[user-profile-changes]        [user-profile-current]
 Delta 이벤트 토픽              Fact 이벤트 토픽 (Log Compacted)
 ─────────────────             ──────────────────────────────
 {userId: "u1",                {userId: "u1",
  changes: {email: "new"}}      name: "김철수",
                         →      email: "new",
 {userId: "u1",                 plan: "premium",
  changes: {plan: "basic"}}     phone: "010-0000-0000"}
```

소비자는 두 토픽을 선택할 수 있다. 변경 이력이 필요하면 `user-profile-changes`, 현재 상태만 필요하면 `user-profile-current`를 구독한다.

---

## 2. ksqlDB 원본 (참고용)

Confluent 코스의 원본 실습은 ksqlDB SQL 기반이다. 이 SQL이 어떤 의도인지 이해하면 Kafka Streams 변환이 자연스러워진다.

```sql
-- Delta 이벤트 토픽을 스트림으로 등록
CREATE STREAM user_profile_changes (
    userId VARCHAR KEY,
    name VARCHAR,
    email VARCHAR,
    plan VARCHAR,
    phone VARCHAR
) WITH (
    KAFKA_TOPIC = 'user-profile-changes',
    VALUE_FORMAT = 'JSON'
);

-- Delta 스트림을 집계하여 현재 상태 테이블 생성
-- LATEST_BY_OFFSET: 같은 키에서 가장 최근에 도착한 값을 선택
CREATE TABLE user_profiles AS
    SELECT
        userId,
        LATEST_BY_OFFSET(name)  AS name,
        LATEST_BY_OFFSET(email) AS email,
        LATEST_BY_OFFSET(plan)  AS plan,
        LATEST_BY_OFFSET(phone) AS phone
    FROM user_profile_changes
    GROUP BY userId
    EMIT CHANGES;
```

`LATEST_BY_OFFSET`은 Kafka 오프셋 기준으로 가장 나중에 도착한 값을 유지한다. `null`인 필드는 이전 값을 그대로 보존하지 않고 `null`로 덮어쓴다는 점에서, 실제 구현에서는 `null` 처리 로직이 필요하다.

Kafka Streams 변환에서는 이 `null` 처리를 `applyDelta()` 메서드에서 명시적으로 다룬다.

---

## 3. 프로젝트 구조

기존 `redpanda-spring-boot` 프로젝트에 Kafka Streams 모듈을 추가하는 방식으로 진행한다. 새 모듈을 별도로 만드는 것보다 기존 docker-compose와 Avro 스키마를 재활용할 수 있어서 효율적이다.

```
redpanda-spring-boot/
├── docker-compose.yml          ← 재사용 (Redpanda + Schema Registry)
├── src/main/avro/              ← 기존 Avro 스키마 디렉토리
│   ├── UserProfileDelta.avsc   ← 신규 추가
│   └── UserProfile.avsc        ← 신규 추가
└── src/main/java/.../
    └── streams/                ← 신규 패키지
        ├── config/
        │   └── KafkaStreamsConfig.java
        ├── topology/
        │   └── UserProfileTopology.java
        ├── model/
        │   ├── UserProfile.java
        │   └── UserProfileDelta.java
        └── query/
            └── UserProfileQueryService.java
```

---

## 4. Avro 스키마 정의

Avro를 사용하면 Schema Registry가 스키마 변경을 추적하고 호환성을 검증해준다. `null` 허용 필드는 Union 타입(`["null", "string"]`)으로 정의한다.

**`UserProfileDelta.avsc`** — Delta 이벤트 스키마

```json
{
  "namespace": "com.example.streams.model",
  "type": "record",
  "name": "UserProfileDelta",
  "doc": "사용자 프로필 변경 이벤트. 변경된 필드만 포함하며, 미변경 필드는 null이다.",
  "fields": [
    {
      "name": "userId",
      "type": "string",
      "doc": "사용자 고유 식별자"
    },
    {
      "name": "name",
      "type": ["null", "string"],
      "default": null,
      "doc": "변경된 이름. 변경 없으면 null"
    },
    {
      "name": "email",
      "type": ["null", "string"],
      "default": null,
      "doc": "변경된 이메일. 변경 없으면 null"
    },
    {
      "name": "plan",
      "type": ["null", "string"],
      "default": null,
      "doc": "변경된 플랜(free/premium/enterprise). 변경 없으면 null"
    },
    {
      "name": "phone",
      "type": ["null", "string"],
      "default": null,
      "doc": "변경된 전화번호. 변경 없으면 null"
    }
  ]
}
```

**`UserProfile.avsc`** — Fact 이벤트 스키마 (전체 상태)

```json
{
  "namespace": "com.example.streams.model",
  "type": "record",
  "name": "UserProfile",
  "doc": "사용자 프로필 현재 상태. Delta 이벤트를 누적하여 구체화된 Fact 이벤트이다.",
  "fields": [
    {
      "name": "userId",
      "type": "string"
    },
    {
      "name": "name",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "email",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "plan",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "phone",
      "type": ["null", "string"],
      "default": null
    },
    {
      "name": "lastUpdated",
      "type": "long",
      "doc": "마지막 업데이트 시각 (epoch milliseconds)"
    }
  ]
}
```

---

## 5. POJO 클래스

Avro 자동 생성 클래스(`UserProfile`, `UserProfileDelta`)에 비즈니스 로직을 직접 추가하면 Avro 재생성 시 덮어써진다. 별도 유틸리티 메서드 클래스로 분리하거나, Avro 클래스를 래핑하는 방식을 권장한다. 여기서는 간결한 실습을 위해 Avro 클래스를 직접 사용하되, `applyDelta()` 로직을 별도 유틸리티 클래스에 두는 방식을 택한다.

```java
package com.example.streams.model;

/**
 * UserProfile 상태 변환 유틸리티.
 * Avro 생성 클래스에 직접 메서드를 추가하지 않기 위해 분리했다.
 */
public class UserProfileMerger {

    /**
     * 현재 UserProfile에 Delta를 적용하여 새 상태를 반환한다.
     * Delta에서 null인 필드는 현재 값을 그대로 유지한다.
     */
    public static UserProfile applyDelta(UserProfile current, UserProfileDelta delta) {
        UserProfile updated = UserProfile.newBuilder(current).build();

        if (delta.getName() != null) {
            updated.setName(delta.getName());
        }
        if (delta.getEmail() != null) {
            updated.setEmail(delta.getEmail());
        }
        if (delta.getPlan() != null) {
            updated.setPlan(delta.getPlan());
        }
        if (delta.getPhone() != null) {
            updated.setPhone(delta.getPhone());
        }
        updated.setLastUpdated(System.currentTimeMillis());
        return updated;
    }

    /**
     * Delta로부터 초기 UserProfile을 생성한다.
     * aggregate()의 초기값 생성에 사용한다.
     */
    public static UserProfile fromDelta(String userId, UserProfileDelta delta) {
        return UserProfile.newBuilder()
            .setUserId(userId)
            .setName(delta.getName())
            .setEmail(delta.getEmail())
            .setPlan(delta.getPlan())
            .setPhone(delta.getPhone())
            .setLastUpdated(System.currentTimeMillis())
            .build();
    }
}
```

---

## 6. Kafka Streams 토폴로지

핵심 로직이 담긴 토폴로지 빌더다. Delta 스트림을 읽어 집계하고 Fact 토픽에 발행한다.

```java
package com.example.streams.topology;

import com.example.streams.model.UserProfile;
import com.example.streams.model.UserProfileDelta;
import com.example.streams.model.UserProfileMerger;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.utils.Bytes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.KeyValueStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

@Configuration
public class UserProfileTopology {

    @Value("${spring.kafka.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    private static final String INPUT_TOPIC  = "user-profile-changes";
    private static final String OUTPUT_TOPIC = "user-profile-current";
    private static final String STORE_NAME   = "user-profiles-store";

    @Bean
    public KStream<String, UserProfileDelta> userProfileStream(StreamsBuilder builder) {
        // Avro Serde 설정
        // specific.avro.reader=true → Avro 생성 클래스(UserProfile 등)로 역직렬화
        Map<String, String> serdeConfig = Map.of(
            "schema.registry.url", schemaRegistryUrl,
            "specific.avro.reader", "true"
        );

        SpecificAvroSerde<UserProfileDelta> deltaSerde = new SpecificAvroSerde<>();
        deltaSerde.configure(serdeConfig, false); // false = 값(value) Serde

        SpecificAvroSerde<UserProfile> profileSerde = new SpecificAvroSerde<>();
        profileSerde.configure(serdeConfig, false);

        // 1. Delta 이벤트 스트림 생성
        KStream<String, UserProfileDelta> deltaStream = builder.stream(
            INPUT_TOPIC,
            Consumed.with(Serdes.String(), deltaSerde)
        );

        // 2. 키(userId)로 그룹핑 후 Delta를 누적하여 현재 상태 테이블 생성
        KTable<String, UserProfile> profileTable = deltaStream
            .groupByKey()
            .aggregate(
                // 초기값: userId가 없는 빈 프로필 (첫 Delta 도착 시 교체됨)
                () -> UserProfile.newBuilder()
                        .setUserId("")
                        .setLastUpdated(0L)
                        .build(),
                // 누산 함수: 기존 상태 + Delta → 새 상태
                (userId, delta, current) -> {
                    // 첫 번째 Delta인 경우 (초기값 상태)
                    if (current.getUserId().isEmpty()) {
                        return UserProfileMerger.fromDelta(userId, delta);
                    }
                    return UserProfileMerger.applyDelta(current, delta);
                },
                // State Store 설정
                Materialized.<String, UserProfile, KeyValueStore<Bytes, byte[]>>as(STORE_NAME)
                    .withKeySerde(Serdes.String())
                    .withValueSerde(profileSerde)
            );

        // 3. KTable을 KStream으로 변환하여 Fact 토픽에 발행
        profileTable
            .toStream()
            .to(OUTPUT_TOPIC, Produced.with(Serdes.String(), profileSerde));

        return deltaStream;
    }
}
```

이 토폴로지에서 주목할 점은 두 가지다. 첫째, `groupByKey()`가 작동하려면 입력 토픽의 파티션 키가 반드시 `userId`여야 한다. 키가 다르면 같은 사용자의 Delta가 서로 다른 Kafka Streams 태스크에서 처리되어 상태가 뒤섞인다. 둘째, `aggregate()`의 초기값은 `Supplier<V>` 형태로 매번 새 인스턴스를 반환해야 한다. 같은 인스턴스를 공유하면 여러 키의 상태가 섞이는 심각한 버그가 생긴다.

---

## 7. Spring Boot 설정

```java
package com.example.streams.config;

import org.apache.kafka.streams.StreamsConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafkaStreams;
import org.springframework.kafka.annotation.KafkaStreamsDefaultConfiguration;
import org.springframework.kafka.config.KafkaStreamsConfiguration;

import java.util.Map;

@Configuration
@EnableKafkaStreams  // Kafka Streams 자동 구성 활성화
public class KafkaStreamsConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${spring.kafka.properties.schema.registry.url}")
    private String schemaRegistryUrl;

    /**
     * KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME 이름으로
     * 빈을 등록해야 Spring Kafka가 Kafka Streams를 자동으로 시작한다.
     */
    @Bean(name = KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
    public KafkaStreamsConfiguration kafkaStreamsConfig() {
        return new KafkaStreamsConfiguration(Map.of(
            StreamsConfig.APPLICATION_ID_CONFIG,    "user-profile-aggregator",
            StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers,
            // Avro 역직렬화 오류 시 DLQ로 보내지 않고 로그만 남기고 건너뜀
            StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
                org.apache.kafka.streams.errors.LogAndContinueExceptionHandler.class,
            // State Store 복구용 Changelog 토픽의 복제 계수 (Redpanda 단일 노드에서는 1)
            "replication.factor", "1"
        ));
    }
}
```

`application.yml` 설정:

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:19092  # Redpanda 기본 포트
    properties:
      # Redpanda 내장 Schema Registry 주소 (Confluent는 localhost:8081)
      schema.registry.url: http://localhost:18081
      specific.avro.reader: "true"

# Kafka Streams 앱 ID (State Store 이름, Changelog 토픽 접두사로 사용됨)
# 같은 클러스터에서 여러 앱을 띄울 때는 각각 고유한 ID 필요
```

---

## 8. docker-compose 설정

기존 `redpanda-spring-boot` 프로젝트의 `docker-compose.yml`을 그대로 사용한다. 새 컨테이너를 추가할 필요 없다.

```yaml
# 기존 redpanda-spring-boot/docker-compose.yml
version: "3.8"
services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v25.3.6
    command:
      - redpanda start
      - --smp 1
      - --memory 1G
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr internal://redpanda:8082,external://localhost:18082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:18081
      - --advertise-schema-registry-addr internal://redpanda:8081,external://localhost:18081
      - --rpc-addr redpanda:33145
      - --advertise-rpc-addr redpanda:33145
    ports:
      - "18081:18081"  # Schema Registry (Confluent는 8081)
      - "18082:18082"  # Pandaproxy
      - "19092:19092"  # Kafka API
    volumes:
      - redpanda-data:/var/lib/redpanda/data

volumes:
  redpanda-data:
```

**Confluent Kafka 사용 시 차이점**: Schema Registry URL이 `localhost:8081`이고, 별도 `schema-registry` 컨테이너가 필요하다. Redpanda는 Schema Registry가 내장되어 있어서 추가 컨테이너 없이 `localhost:18081`로 바로 사용한다.

---

## 9. 토픽 생성

Kafka Streams는 입력/출력 토픽을 자동으로 생성하지 않는다. 앱 시작 전에 미리 만들어야 한다.

```bash
# Redpanda CLI (rpk) 사용
# 입력 토픽: Delta 이벤트 (보존 기간 7일, 이력 추적 목적)
rpk topic create user-profile-changes \
  --partitions 6 \
  --replicas 1 \
  -c retention.ms=604800000

# 출력 토픽: Fact 이벤트 (Log Compaction 적용, 현재 상태만 보존)
rpk topic create user-profile-current \
  --partitions 6 \
  --replicas 1 \
  -c cleanup.policy=compact \
  -c min.cleanable.dirty.ratio=0.1 \
  -c delete.retention.ms=86400000

# 생성 확인
rpk topic list
rpk topic describe user-profile-current
```

파티션 수를 6으로 설정했다. Kafka Streams의 병렬 처리 단위는 파티션이므로, 파티션이 많을수록 더 많은 태스크가 병렬 실행될 수 있다. 단, State Store도 파티션 수만큼 분산되므로 로컬 개발 환경에서는 3~6개가 적당하다.

---

## 10. 테스트 데이터 발행

`rpk`로 테스트 Delta 이벤트를 직접 발행해서 동작을 확인한다.

```bash
# JSON으로 테스트 (Schema Registry 없이 빠른 검증용)
# 실제 프로덕션에서는 Avro 사용

# user-123: 초기 생성
echo '{"userId":"user-123","name":"김철수","email":"kim@example.com","plan":"free","phone":null}' \
  | rpk topic produce user-profile-changes --key=user-123

# user-123: 플랜 변경 (name, email, phone은 null)
echo '{"userId":"user-123","name":null,"email":null,"plan":"premium","phone":null}' \
  | rpk topic produce user-profile-changes --key=user-123

# user-123: 이메일 변경만
echo '{"userId":"user-123","name":null,"email":"new.kim@example.com","plan":null,"phone":null}' \
  | rpk topic produce user-profile-changes --key=user-123

# user-456: 다른 사용자
echo '{"userId":"user-456","name":"이영희","email":"lee@example.com","plan":"enterprise","phone":"010-9999-0000"}' \
  | rpk topic produce user-profile-changes --key=user-456
```

결과 확인:

```bash
# Fact 토픽에 발행된 현재 상태 확인
rpk topic consume user-profile-current --offset=start -n 10

# 예상 출력: user-123의 최종 상태
# key: user-123
# value: {"userId":"user-123","name":"김철수","email":"new.kim@example.com","plan":"premium","phone":null,...}
```

---

## 11. Interactive Query: State Store 조회

Kafka Streams의 Interactive Query는 State Store를 HTTP API로 외부에 노출할 수 있게 해준다. 별도 데이터베이스 없이 현재 사용자 상태를 조회하는 엔드포인트를 만들 수 있다.

```java
package com.example.streams.query;

import com.example.streams.model.UserProfile;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Service
public class UserProfileQueryService {

    private final KafkaStreams kafkaStreams;

    public UserProfileQueryService(KafkaStreams kafkaStreams) {
        this.kafkaStreams = kafkaStreams;
    }

    public UserProfile getProfile(String userId) {
        ReadOnlyKeyValueStore<String, UserProfile> store = kafkaStreams.store(
            StoreQueryParameters.fromNameAndType(
                "user-profiles-store",
                QueryableStoreTypes.keyValueStore()
            )
        );
        return store.get(userId);
    }
}

@RestController
@RequestMapping("/api/profiles")
class UserProfileController {

    private final UserProfileQueryService queryService;

    UserProfileController(UserProfileQueryService queryService) {
        this.queryService = queryService;
    }

    @GetMapping("/{userId}")
    public UserProfile getProfile(@PathVariable String userId) {
        UserProfile profile = queryService.getProfile(userId);
        if (profile == null) {
            throw new RuntimeException("User not found: " + userId);
        }
        return profile;
    }
}
```

이 방식의 장점은 State Store가 인메모리(RocksDB)에 있어서 조회가 매우 빠르다는 점이다. 단점은 State Store가 로컬에 있기 때문에 다중 인스턴스 환경에서 특정 userId의 데이터가 다른 인스턴스의 State Store에 있을 수 있다. 이 경우 KafkaStreams의 `queryMetadataForKey()`로 올바른 인스턴스를 찾아 내부적으로 HTTP 요청을 전달하는 "분산 쿼리" 패턴이 필요하다.

---

## 12. TopologyTestDriver로 단위 테스트

`TopologyTestDriver`는 실제 Kafka 브로커나 Schema Registry 없이 토폴로지를 테스트할 수 있게 해준다. 단위 테스트에서 가장 빠르고 신뢰할 수 있는 검증 방법이다.

```java
package com.example.streams.topology;

import com.example.streams.model.UserProfile;
import com.example.streams.model.UserProfileDelta;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.state.KeyValueStore;
import org.apache.kafka.streams.test.TestRecord;
import org.junit.jupiter.api.*;

import java.util.Properties;

import static org.assertj.core.api.Assertions.assertThat;

class UserProfileTopologyTest {

    private TopologyTestDriver testDriver;
    private TestInputTopic<String, UserProfileDelta> inputTopic;
    private TestOutputTopic<String, UserProfile> outputTopic;

    @BeforeEach
    void setUp() {
        // 실제 토폴로지와 동일한 빌더 사용
        StreamsBuilder builder = new StreamsBuilder();

        // 테스트용 Serde: Schema Registry 없이 JSON 또는 직접 직렬화
        // 여기서는 간결함을 위해 JSON Serde를 사용한다고 가정
        // 실제 프로젝트에서는 MockSchemaRegistryClient를 활용한 Avro Serde 사용 권장

        // 테스트용 MockSerde 사용 (실제 코드에서는 별도 구현 필요)
        var deltaSerde  = new MockUserProfileDeltaSerde();
        var profileSerde = new MockUserProfileSerde();

        // 토폴로지 직접 구성 (Spring Bean 주입 없이)
        KStream<String, UserProfileDelta> deltaStream = builder.stream(
            "user-profile-changes",
            Consumed.with(org.apache.kafka.common.serialization.Serdes.String(), deltaSerde)
        );
        deltaStream
            .groupByKey()
            .aggregate(
                () -> new UserProfile("", null, null, null, null, 0L),
                (userId, delta, current) ->
                    current.getUserId().isEmpty()
                        ? UserProfileMerger.fromDelta(userId, delta)
                        : UserProfileMerger.applyDelta(current, delta),
                Materialized.as("user-profiles-store")
            )
            .toStream()
            .to("user-profile-current", Produced.with(
                org.apache.kafka.common.serialization.Serdes.String(), profileSerde));

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG,    "test-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummy:9092");

        testDriver = new TopologyTestDriver(builder.build(), props);
        inputTopic  = testDriver.createInputTopic("user-profile-changes",
            new StringSerializer(), deltaSerde.serializer());
        outputTopic = testDriver.createOutputTopic("user-profile-current",
            new StringDeserializer(), profileSerde.deserializer());
    }

    @AfterEach
    void tearDown() {
        testDriver.close();
    }

    @Test
    @DisplayName("첫 Delta 이벤트로 초기 프로필이 생성된다")
    void initialDeltaCreatesProfile() {
        // Given
        UserProfileDelta delta = new UserProfileDelta("user-123", "김철수", "kim@example.com", "free", null);

        // When
        inputTopic.pipeInput("user-123", delta);

        // Then
        TestRecord<String, UserProfile> output = outputTopic.readRecord();
        assertThat(output.key()).isEqualTo("user-123");
        assertThat(output.value().getName()).isEqualTo("김철수");
        assertThat(output.value().getEmail()).isEqualTo("kim@example.com");
        assertThat(output.value().getPlan()).isEqualTo("free");
    }

    @Test
    @DisplayName("null 필드는 기존 값을 유지한다")
    void nullFieldPreservesExistingValue() {
        // Given: 초기 프로필 생성
        inputTopic.pipeInput("user-123",
            new UserProfileDelta("user-123", "김철수", "kim@example.com", "free", null));
        outputTopic.readRecord(); // 첫 이벤트 소비

        // When: 플랜만 변경 (나머지 null)
        inputTopic.pipeInput("user-123",
            new UserProfileDelta("user-123", null, null, "premium", null));

        // Then: 이름/이메일은 유지되고 플랜만 변경
        TestRecord<String, UserProfile> output = outputTopic.readRecord();
        assertThat(output.value().getName()).isEqualTo("김철수");   // 기존 값 유지
        assertThat(output.value().getEmail()).isEqualTo("kim@example.com"); // 기존 값 유지
        assertThat(output.value().getPlan()).isEqualTo("premium");  // 변경됨
    }

    @Test
    @DisplayName("State Store에서 현재 상태를 조회할 수 있다")
    void stateStoreQueryReturnsCurrentState() {
        // Given
        inputTopic.pipeInput("user-123",
            new UserProfileDelta("user-123", "김철수", "kim@example.com", "free", null));
        inputTopic.pipeInput("user-123",
            new UserProfileDelta("user-123", null, "new.kim@example.com", null, null));

        // When
        KeyValueStore<String, UserProfile> store =
            testDriver.getKeyValueStore("user-profiles-store");
        UserProfile current = store.get("user-123");

        // Then
        assertThat(current.getEmail()).isEqualTo("new.kim@example.com");
        assertThat(current.getName()).isEqualTo("김철수"); // 변경 안 됨
    }

    @Test
    @DisplayName("서로 다른 사용자의 상태는 독립적으로 관리된다")
    void differentUsersHaveIndependentState() {
        // Given
        inputTopic.pipeInput("user-123",
            new UserProfileDelta("user-123", "김철수", "kim@example.com", "free", null));
        inputTopic.pipeInput("user-456",
            new UserProfileDelta("user-456", "이영희", "lee@example.com", "premium", null));

        // When
        KeyValueStore<String, UserProfile> store =
            testDriver.getKeyValueStore("user-profiles-store");

        // Then
        assertThat(store.get("user-123").getName()).isEqualTo("김철수");
        assertThat(store.get("user-456").getName()).isEqualTo("이영희");
    }
}
```

`TopologyTestDriver`는 Kafka 브로커 없이 로컬에서 실행되므로 CI 환경에서도 외부 의존성 없이 빠르게 실행된다. 복잡한 집계 로직이나 엣지 케이스를 검증하기에 가장 적합한 방법이다.

---

## 13. 검증 흐름 요약

실습을 처음 진행할 때 권장하는 순서다.

```
1. docker-compose up -d          ← Redpanda 시작
2. rpk topic create ...           ← 토픽 생성
3. ./gradlew bootRun              ← Spring Boot + Kafka Streams 시작
4. rpk topic produce (테스트 데이터) ← Delta 이벤트 발행
5. rpk topic consume user-profile-current ← Fact 이벤트 확인
6. curl /api/profiles/user-123   ← Interactive Query 확인
7. ./gradlew test (TopologyTestDriver) ← 단위 테스트 실행
```

---

## Redpanda 호환성 노트

- Confluent 원본 코스에서 Schema Registry URL은 `http://localhost:8081`이지만, Redpanda 내장 Schema Registry는 `http://localhost:18081`을 사용한다. `application.yml`에서 이 포트를 변경하는 것이 유일한 차이점이다.
- `specific.avro.reader=true` 설정은 Redpanda Schema Registry에서도 동일하게 작동한다. Avro SpecificRecord 클래스를 생성해서 쓰는 방식은 브로커와 무관하다.
- Kafka Streams State Store의 Changelog 토픽(`{app-id}-{store-name}-changelog`)이 Redpanda에 자동 생성된다. 앱 재시작 시 이 토픽에서 State Store를 복원하므로, 토픽이 삭제되면 상태가 초기화된다.
- TopologyTestDriver는 브로커와 완전히 독립적으로 실행된다. Redpanda, Confluent Kafka, 그 외 어떤 브로커를 쓰더라도 동일한 단위 테스트 코드가 작동한다.

---

## 체크포인트

- [ ] ksqlDB의 `LATEST_BY_OFFSET`이 Kafka Streams의 `aggregate()`로 어떻게 변환되는지 설명할 수 있다
- [ ] `applyDelta()`에서 `null` 필드를 처리하는 이유를 이해한다 (null = 변경 없음)
- [ ] `aggregate()` 초기값이 `Supplier<V>` 형태여야 하는 이유를 설명할 수 있다 (공유 인스턴스 버그 방지)
- [ ] Redpanda에서 Schema Registry URL이 `:18081`임을 기억한다 (Confluent는 `:8081`)
- [ ] `TopologyTestDriver`로 State Store를 직접 조회하는 테스트 패턴을 따라 작성할 수 있다
- [ ] Log Compaction 설정(`cleanup.policy=compact`)이 Fact 토픽에 필요한 이유를 설명할 수 있다
- [ ] Interactive Query의 다중 인스턴스 한계를 인식하고, 단일 인스턴스 환경에서 어떻게 활용하는지 안다
