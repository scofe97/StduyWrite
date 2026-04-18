# CQRS Query Side - Kafka Streams Topology 리서치

**작성일**: 2026-02-24
**목표**: Kafka Streams로 social 이벤트를 소비하여 PostView/FollowsView State Store 구성
**영향 범위**: cqrs/ 패키지 (query/, config/ 추가)

---

## 1. 관련 코드 분석

### 주요 파일
| 파일 | 역할 | 수정 필요 |
|------|------|----------|
| `cqrs/config/CqrsKafkaConfig.java` | Command Side Producer 설정 | ❌ 수정 없음 |
| `cqrs/config/CqrsTopicConfig.java` | 토픽 생성 설정 | ❌ 수정 없음 |
| `avro/cqrs/PostCreated.avsc` | 게시물 생성 이벤트 스키마 | ❌ |
| `avro/cqrs/PostLiked.avsc` | 게시물 좋아요 이벤트 스키마 | ❌ |
| `avro/cqrs/UserFollowed.avsc` | 팔로우 이벤트 스키마 | ❌ |
| `avro/cqrs/UserUnfollowed.avsc` | 언팔로우 이벤트 스키마 | ❌ |

### Avro 스키마 필드 확인
- `avro.stringType = 'String'` (build.gradle) → Avro CharSequence가 `java.lang.String`으로 생성됨
  - `.toString()` 호출 불필요 (이미 String 타입)
- PostCreated: eventId, postId, userId, content, timestamp(long)
- PostLiked: eventId, postId, userId, timestamp(long)
- UserFollowed: eventId, followerId, followeeId, timestamp(long)
- UserUnfollowed: eventId, followerId, followeeId, timestamp(long)

### application.yml 핵심 설정
- bootstrap-servers: `localhost:19092`
- schema.registry.url: `${spring.kafka.producer.properties.schema.registry.url}` = `http://localhost:18081`
- specific.avro.reader: `true` (consumer 설정에 있음 → Streams에도 동일 적용 필요)

### @EnableKafkaStreams 현황
- **현재 없음**: 프로젝트 어디에도 `@EnableKafkaStreams` 미사용
- `CqrsStreamsConfig`에 처음 추가해도 충돌 없음

### build.gradle 의존성 확인
- `kafka-streams` ✅ 이미 있음
- `jackson-databind` ✅ 이미 있음 (JsonSerde 사용 가능)
- `kafka-avro-serializer:7.6.0` ✅ 이미 있음

---

## 2. 핵심 발견사항

### stringType = 'String' 중요
build.gradle에 `avro { stringType = 'String' }` 설정이 있어서
Avro 생성 클래스의 String 필드는 이미 `java.lang.String` 타입이다.
`.toString()` 없이 바로 사용 가능하다.

### Avro Serde for Kafka Streams
Kafka Streams에서 Avro SpecificRecord를 역직렬화하려면:
- `io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde` 사용
- Properties에 `schema.registry.url` + `specific.avro.reader=true` 필요

### DEFAULT_STREAMS_CONFIG_BEAN_NAME
Spring Kafka의 `@EnableKafkaStreams`는 `DEFAULT_STREAMS_CONFIG_BEAN_NAME`
("defaultKafkaStreamsConfig") 이름의 `KafkaStreamsConfiguration` 빈을 요구한다.

### KafkaStreamsConfiguration vs StreamsConfig
- `KafkaStreamsConfiguration`은 Spring Kafka 래퍼 (Map 기반)
- 내부적으로 `StreamsConfig`로 변환됨

---

## 3. 주의사항
- [ ] `@EnableKafkaStreams`는 `CqrsStreamsConfig`에만 추가 (기존 설정 파일 건드리지 않음)
- [ ] SpecificAvroSerde 생성 시 `configure()` 호출 필수 (schema.registry.url 주입)
- [ ] `follows-store` 키: followerId (UserFollowed/UserUnfollowed 모두 followerId로 groupByKey)
- [ ] aggregate() 초기값 null → PostLiked/UserUnfollowed가 먼저 오면 방어 처리 필요

---

## 4. 다음 단계
→ plans/cqrs-query-side-streams.md 작성
