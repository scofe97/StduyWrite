# Timeline Materialized View

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 실습 번호 | 8 |
| 주요 파일 | `cqrs/query/topology/TimelineStreamTopology.java`, `cqrs/query/model/TimelineView.java`, `cqrs/query/service/TimelineQueryService.java` |
| HTTP 파일 | `http/cqrs/05-interactive-query.http` (9~14번 요청) |
| 관련 원칙 | Fan-out on Write, Processor API, 역방향 인덱스, 크로스 스토어 조회 |

---

## 무엇을 구현했는가

### 왜 DSL이 아닌 Processor API인가

실습 4~5에서 구현한 PostsStreamTopology와 FollowsStreamTopology는 DSL(`merge → groupByKey → aggregate`)을 사용했다. 타임라인은 이 패턴으로 구현할 수 없다. DSL의 `aggregate()`는 하나의 State Store에만 접근 가능하지만, 타임라인 구축에는 두 가지 크로스 스토어 작업이 필요하기 때문이다.

첫째, PostCreated 이벤트가 도착하면 "이 작성자를 팔로우하는 사람이 누구인지" 알아야 한다. 이 정보는 follows-store에 있지 않고 별도의 역방향 인덱스(timeline-followers-cache)에 있다. 둘째, 조회한 팔로워 N명 각각의 timeline-store에 엔트리를 써야 한다. 하나의 입력 이벤트가 N개의 State Store 쓰기를 유발하는 팬아웃(fan-out) 패턴이다.

Processor API는 `init()`에서 여러 State Store 핸들을 얻을 수 있으므로 이 두 요구사항을 모두 충족한다.

### 역방향 인덱스: FollowsCacheProcessor

follows-store는 "내가 누구를 팔로우하는가"(`followerId → Set<followeeId>`)를 저장한다. 그런데 타임라인 팬아웃에는 반대 방향, 즉 "누가 나를 팔로우하는가"(`followeeId → Set<followerId>`)가 필요하다. FollowsCacheProcessor가 이 역방향 인덱스를 timeline-followers-cache에 구축한다.

```java
static class FollowsCacheProcessor implements Processor<String, SpecificRecord, Void, Void> {

    private KeyValueStore<String, HashSet<String>> followersCache;

    @Override
    public void init(ProcessorContext<Void, Void> context) {
        this.followersCache = context.getStateStore(FOLLOWERS_CACHE_STORE);
    }

    @Override
    public void process(Record<String, SpecificRecord> record) {
        SpecificRecord event = record.value();
        String followerId = record.key();

        if (event instanceof UserFollowed followed) {
            String followeeId = followed.getFolloweeId();
            HashSet<String> followers = followersCache.get(followeeId);
            if (followers == null) {
                followers = new HashSet<>();
            }
            followers.add(followerId);
            followersCache.put(followeeId, followers);
        }

        if (event instanceof UserUnfollowed unfollowed) {
            String followeeId = unfollowed.getFolloweeId();
            HashSet<String> followers = followersCache.get(followeeId);
            if (followers != null) {
                followers.remove(followerId);
                followersCache.put(followeeId, followers);
            }
        }
    }
}
```

UserFollowed가 도착하면 `followeeId`를 key로 `followerId`를 Set에 추가하고, UserUnfollowed가 도착하면 제거한다. 이 인덱스 덕분에 게시물 작성 시 O(1)로 팔로워 목록을 조회할 수 있다.

### 팬아웃 쓰기: TimelineFanOutProcessor

PostCreated 이벤트가 도착하면 작성자의 팔로워를 조회하고, 각 팔로워의 타임라인에 엔트리를 추가한다.

```java
static class TimelineFanOutProcessor implements Processor<String, SpecificRecord, Void, Void> {

    private KeyValueStore<String, TimelineView> timelineStore;
    private KeyValueStore<String, HashSet<String>> followersCache;

    @Override
    public void init(ProcessorContext<Void, Void> context) {
        this.timelineStore = context.getStateStore(TIMELINE_STORE);
        this.followersCache = context.getStateStore(FOLLOWERS_CACHE_STORE);
    }

    @Override
    public void process(Record<String, SpecificRecord> record) {
        if (!(record.value() instanceof PostCreated created)) return;

        String authorId = created.getUserId();
        HashSet<String> followers = followersCache.get(authorId);
        if (followers == null || followers.isEmpty()) return;

        TimelineView.TimelineEntry entry = TimelineView.TimelineEntry.builder()
                .postId(created.getPostId())
                .authorId(authorId)
                .content(created.getContent())
                .createdAt(created.getTimestamp())
                .build();

        for (String followerId : followers) {
            TimelineView timeline = timelineStore.get(followerId);
            if (timeline == null) {
                timeline = TimelineView.builder()
                        .userId(followerId)
                        .entries(new ArrayList<>())
                        .build();
            }
            timeline.getEntries().add(0, entry);  // newest first

            if (timeline.getEntries().size() > MAX_TIMELINE_ENTRIES) {
                timeline.setEntries(
                        new ArrayList<>(timeline.getEntries().subList(0, MAX_TIMELINE_ENTRIES))
                );
            }
            timelineStore.put(followerId, timeline);
        }
    }
}
```

핵심 동작을 정리하면 다음과 같다.

1. followers-cache에서 작성자의 팔로워 Set을 조회한다.
2. 팔로워가 없으면 즉시 리턴한다 (팬아웃 대상 없음).
3. TimelineEntry를 생성하고 각 팔로워의 타임라인 앞에 추가한다 (newest first).
4. 타임라인이 50개를 초과하면 오래된 것부터 잘라낸다.
5. `forward()` 호출이 없다. 다운스트림으로 전달하지 않고 State Store에만 쓴다.

### TimelineView 모델

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TimelineView {
    private String userId;
    @Builder.Default
    private List<TimelineEntry> entries = new ArrayList<>();

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class TimelineEntry {
        private String postId;
        private String authorId;
        private String content;
        private long createdAt;
    }
}
```

게시물의 핵심 정보만 비정규화(denormalize)하여 저장한다. 타임라인 조회 시 posts-store를 다시 조인할 필요 없이 TimelineView만으로 피드를 렌더링할 수 있다. 이것이 CQRS에서 "읽기에 최적화된 Materialized View"의 의미다.

### 토폴로지 등록

```java
@PostConstruct
public void buildTopology() {
    // State Store 빌더 등록
    streamsBuilder.addStateStore(timelineStoreBuilder);
    streamsBuilder.addStateStore(followersCacheBuilder);

    // follow/unfollow → 역방향 인덱스
    streamsBuilder.stream(CqrsTopics.USER_FOLLOWED, consumed)
            .merge(streamsBuilder.stream(CqrsTopics.USER_UNFOLLOWED, consumed))
            .process(FollowsCacheProcessor::new, FOLLOWERS_CACHE_STORE);

    // post-created → 팬아웃 쓰기
    streamsBuilder.stream(CqrsTopics.POST_CREATED, consumed)
            .process(TimelineFanOutProcessor::new, TIMELINE_STORE, FOLLOWERS_CACHE_STORE);
}
```

`process()`의 두 번째 인자로 State Store 이름을 전달한다. Kafka Streams는 이 정보를 바탕으로 해당 Processor가 접근할 수 있는 State Store를 제한한다. TimelineFanOutProcessor는 두 Store(timeline-store, timeline-followers-cache) 모두에 접근해야 하므로 두 이름 모두 전달한다.

---

## 왜 이렇게 구현했는가

### Fan-out on Write를 선택한 이유

타임라인 구현에는 Fan-out on Write와 Fan-out on Read 두 가지 접근이 있다.

| 항목 | Fan-out on Write | Fan-out on Read |
|------|-----------------|-----------------|
| 쓰기 시점 | 게시물 작성 시 N명 타임라인에 복사 | 게시물 1건만 저장 |
| 읽기 시점 | timeline-store.get(userId) 1회 | N명의 게시물을 실시간 조합 |
| 읽기 지연 | O(1) — 미리 계산됨 | O(N) — 팔로잉 수에 비례 |
| 쓰기 지연 | O(M) — 팔로워 수에 비례 | O(1) — 이벤트 1건 |
| 적합 대상 | 읽기 >> 쓰기 (소셜 피드) | 쓰기 >> 읽기 |

소셜 피드는 읽기가 쓰기보다 압도적으로 많다. 사용자 1명이 하루에 쓰는 게시물은 몇 건이지만, 타임라인 조회는 수십~수백 회이다. Fan-out on Write는 쓰기 시점에 비용을 지불하고 읽기를 O(1)로 만들기 때문에 이 사용 패턴에 적합하다. Twitter도 초기에 이 방식을 사용했다.

### 역방향 인덱스를 별도 Store로 분리한 이유

follows-store(followerId → followees)를 역방향으로 스캔하여 팔로워를 찾을 수도 있지만, 이는 전체 Store를 순회하는 O(N) 작업이다. timeline-followers-cache(followeeId → followers)를 별도로 유지하면 팔로워 조회가 O(1)이 된다. 메모리를 더 쓰는 대신 쓰기 시점의 팬아웃 성능이 크게 개선된다.

### 팔로우 시 기존 게시물을 백필하지 않는 이유

user-002가 user-001을 새로 팔로우했을 때, user-001의 기존 게시물을 user-002 타임라인에 소급 적용하지 않는다. 팔로우 이후 작성된 게시물만 타임라인에 포함된다. 백필하려면 posts-store를 전체 스캔하여 해당 작성자의 게시물을 필터링해야 하는데, 이는 비용이 크고 Kafka Streams의 스트림 처리 모델과 맞지 않는다. 대부분의 소셜 서비스도 동일한 방식을 채택한다.

### MAX_TIMELINE_ENTRIES = 50 제한의 이유

State Store에 저장하는 타임라인 엔트리를 50개로 제한한 이유는 두 가지다. 첫째, JsonSerde가 TimelineView 전체를 직렬화/역직렬화하므로 리스트가 무한히 커지면 성능이 저하된다. 둘째, 소셜 피드는 최신 게시물이 중요하지 오래된 게시물을 끝까지 스크롤하는 사용자는 드물다. 50개를 초과하면 오래된 것부터 버린다.

---

## 교차 검증 결과

### 데이터 흐름 검증

HTTP 테스트 시나리오(05-interactive-query.http의 9~14번)로 다음을 확인했다.

1. user-002가 user-001을 팔로우한 상태에서, user-001이 게시물을 작성하면 user-002 타임라인에 엔트리가 추가된다.
2. user-003이 user-001을 팔로우한 뒤 user-001이 게시물을 작성하면, user-002와 user-003 타임라인 모두에 팬아웃된다.
3. user-003 타임라인에는 팔로우 이후 게시물만 포함된다 (팔로우 이전 게시물은 백필 없음).
4. 존재하지 않는 타임라인 조회 시 404가 반환된다.

### DSL vs Processor API 비교

| 항목 | DSL (Posts/Follows Topology) | Processor API (Timeline Topology) |
|------|-----|-----|
| 코드량 | 짧다 (aggregate 한 줄) | 길다 (Processor 클래스 2개) |
| State Store 접근 | 자동 관리 (1개) | 수동 관리 (2개 크로스 참조) |
| 팬아웃 | 불가 (1:1 매핑) | 가능 (1:N 쓰기) |
| 적합 대상 | 단일 스트림 집계 | 크로스 스토어 + 팬아웃 |

DSL과 Processor API는 용도가 다르므로 하나의 프로젝트에서 혼용하는 것이 정상이다. 단순 집계는 DSL, 복잡한 크로스 스토어 로직은 Processor API를 선택하면 된다.

### 설계상 주의점

`TimelineFanOutProcessor.process()`에서 `forward()`를 호출하지 않는다. Processor API의 기본 패턴은 입력 → 처리 → forward(다운스트림)이지만, 타임라인은 State Store에 직접 쓰기만 하고 다운스트림으로 전달할 데이터가 없다. 이 때문에 Processor의 출력 타입을 `<Void, Void>`로 선언했다.

---

## 핵심 학습 포인트

- **DSL로 해결할 수 없는 문제가 Processor API의 사용 이유다.** 크로스 스토어 조회와 1:N 팬아웃은 DSL의 `aggregate()`로 표현할 수 없다. Processor API는 여러 State Store에 직접 접근할 수 있으므로 이런 복합 로직에 적합하다.

- **역방향 인덱스는 조회 패턴이 저장 패턴과 다를 때 필요하다.** follows-store의 key는 followerId이지만, 타임라인 팬아웃에는 followeeId로 조회해야 한다. 별도 인덱스를 유지하면 전체 스캔 없이 O(1)로 필요한 데이터에 접근할 수 있다.

- **Fan-out on Write는 읽기 최적화 전략이다.** 쓰기 시점에 N명의 타임라인에 복사하는 비용을 지불하는 대신, 읽기가 State Store 1회 조회로 끝난다. 소셜 피드처럼 읽기가 쓰기보다 압도적으로 많은 도메인에 적합하다.

- **비정규화된 Materialized View는 조인을 제거한다.** TimelineEntry에 authorId, content를 복사해두면 조회 시 posts-store를 참조하지 않아도 된다. CQRS에서 Query Side는 읽기에 최적화된 형태로 데이터를 미리 가공해두는 것이 핵심이다.

- **forward() 없는 Processor도 유효한 패턴이다.** Processor API가 항상 다운스트림으로 데이터를 전달하는 것은 아니다. State Store에만 쓰고 끝나는 "sink processor" 패턴도 존재한다. 이 경우 출력 타입을 `<Void, Void>`로 선언한다.
