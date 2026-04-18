# CQRS Query Side - Kafka Streams Topology 구현 계획

**작성일**: 2026-02-24
**리서치**: research/cqrs-query-side-streams.md
**예상 시간**: 1시간

---

## 변경 목표
Kafka Streams로 social 이벤트(PostCreated/PostLiked/UserFollowed/UserUnfollowed)를
소비하여 posts-store/follows-store State Store를 구성한다.

---

## Step 1: Read Model 클래스 생성

**목표**: PostView, FollowsView DTO 작성

**생성 파일**:
- `cqrs/query/model/PostView.java`
- `cqrs/query/model/FollowsView.java`

**검증**: 컴파일 통과

---

## Step 2: Kafka Streams 설정 (CqrsStreamsConfig)

**목표**: @EnableKafkaStreams + KafkaStreamsConfiguration 빈 등록

**생성 파일**:
- `cqrs/config/CqrsStreamsConfig.java`

핵심 설정:
- APPLICATION_ID_CONFIG = "cqrs-social-streams"
- DEFAULT_KEY_SERDE = Serdes.StringSerde
- schema.registry.url 주입
- specific.avro.reader = true (SpecificRecord 역직렬화)
- AUTO_OFFSET_RESET = earliest (Event Store 처음부터 읽기)

---

## Step 3: PostsStreamTopology 구현

**목표**: social.events.posts → posts-store aggregate

**생성 파일**:
- `cqrs/query/topology/PostsStreamTopology.java`

로직:
- SpecificAvroSerde<SpecificRecord>로 스트림 생성
- instanceof PostCreated → 새 PostView 생성
- instanceof PostLiked → likeCount++, likedBy 추가
- Materialized.as("posts-store") with JsonSerde<PostView>

---

## Step 4: FollowsStreamTopology 구현

**목표**: social.events.follows → follows-store aggregate

**생성 파일**:
- `cqrs/query/topology/FollowsStreamTopology.java`

로직:
- instanceof UserFollowed → followees.add(followeeId)
- instanceof UserUnfollowed → followees.remove(followeeId)
- Materialized.as("follows-store") with JsonSerde<FollowsView>

---

## Step 5: 빌드 검증

```bash
./gradlew compileJava
```

---

## 리스크
| 리스크 | 영향 | 대응 |
|--------|------|------|
| SpecificAvroSerde configure() 누락 | Schema Registry 연결 실패 | configure() 호출 명시 |
| ch02~ch04 KafkaTemplate 충돌 | 기존 코드 broken | @Qualifier("cqrsKafkaTemplate") 유지 |
| DEFAULT_STREAMS_CONFIG_BEAN_NAME 오타 | 스트림 미시작 | 상수명 복사 사용 |
