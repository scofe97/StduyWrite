# 빌더 패턴 전환 + HTTP 폴더 정리

---

## 구현 요약

| 항목 | 내용 |
|------|------|
| 실습 번호 | 7 |
| 주요 파일 | `cqrs/query/model/PostView.java`, `cqrs/query/model/FollowsView.java`, `cqrs/query/topology/PostsStreamTopology.java`, `cqrs/query/topology/FollowsStreamTopology.java` |
| HTTP 파일 | `http/cqrs/02-command-side.http`, `http/cqrs/03-event-store.http`, `http/cqrs/04-kafka-streams.http`, `http/cqrs/05-interactive-query.http` |
| 관련 원칙 | 생성 시 빌더 / 변경 시 setter 분리, DRY (HTTP 중복 제거) |

---

## 무엇을 구현했는가

### 빌더 패턴 전환

View 모델에 `@Builder` + `@Builder.Default`를 추가하고, 토폴로지의 생성 코드를 빌더로 전환했다.

**PostView.java 변경:**

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostView {
    private String postId;
    private String userId;
    private String content;
    private int likeCount;
    @Builder.Default
    private List<String> likedBy = new ArrayList<>();
    private long createdAt;
}
```

**PostsStreamTopology — newPostView() 변경:**

```java
// 기존 (setter)
PostView view = new PostView();
view.setPostId(created.getPostId());
view.setUserId(created.getUserId());
view.setContent(created.getContent());
view.setLikeCount(0);
view.setLikedBy(new ArrayList<>());
view.setCreatedAt(created.getTimestamp());
return view;

// 변경 (builder)
return PostView.builder()
        .postId(created.getPostId())
        .userId(created.getUserId())
        .content(created.getContent())
        .likeCount(0)
        .likedBy(new ArrayList<>())
        .createdAt(created.getTimestamp())
        .build();
```

**mutate 코드는 setter 유지:**

```java
// PostLiked 처리 — 기존 객체 변경이므로 setter가 자연스러움
currentView.setLikeCount(currentView.getLikeCount() + 1);
currentView.getLikedBy().add(liked.getUserId());
return currentView;
```

`FollowsView`도 동일한 패턴으로 `@Builder` + `@Builder.Default` 추가, `newFollowsView()`를 빌더로 전환했다.

### HTTP 폴더 정리

기존 4개 `cqrs-*.http` 파일을 `http/cqrs/` 폴더로 이동하고, Command 요청 중복을 제거했다.

**기존 구조:**
```
http/
├── cqrs-command-side.http          ← 모든 Command + rpk
├── cqrs-event-store-topic.http     ← Command 중복 + rpk
├── cqrs-kafka-streams.http         ← Command 중복 + rpk
└── cqrs-interactive-query.http     ← Command 중복 + GET 쿼리
```

**변경 구조:**
```
http/
└── cqrs/
    ├── 02-command-side.http        ← canonical (모든 Command + postId 캡처)
    ├── 03-event-store.http         ← rpk 검증만 (Command 없음)
    ├── 04-kafka-streams.http       ← rpk 검증만 (Command 없음)
    └── 05-interactive-query.http   ← GET 쿼리만 (Command 없음)
```

`02-command-side.http`가 모든 Command API의 원본이다. response handler로 `postId`를 `client.global`에 캡처하면 `05-interactive-query.http`에서 `{{postId}}`로 참조할 수 있다. IntelliJ HTTP Client의 `client.global` 변수는 프로젝트 내 파일 간 공유된다.

---

## 왜 이렇게 구현했는가

빌더 패턴을 생성에만 적용하고 변경(mutate)에는 setter를 유지한 이유는 용도의 차이 때문이다. `PostCreated` 이벤트 처리 시 새 PostView를 만드는 것은 "불변 객체 초기화"에 해당하므로 빌더가 적합하다. 반면 `PostLiked` 이벤트 처리 시 기존 PostView의 likeCount를 증가시키는 것은 "기존 객체 변경"이므로 setter가 자연스럽다. 빌더로 매번 새 객체를 복사하면 불필요한 할당이 발생한다.

`@Builder.Default`를 `likedBy`와 `followees` 필드에 추가한 이유는 Lombok의 `@Builder`가 필드 초기값을 무시하기 때문이다. `@Builder.Default` 없이 `@Builder`만 쓰면 빌더로 생성한 객체의 `likedBy`가 `null`이 된다. `@Builder.Default`는 빌더에서 해당 필드를 명시적으로 설정하지 않았을 때 필드 초기값(`new ArrayList<>()`)을 사용하도록 보장한다.

`@NoArgsConstructor` + `@AllArgsConstructor`를 유지한 이유는 JsonSerde 역직렬화에 기본 생성자가 필요하기 때문이다. Jackson은 기본 생성자로 인스턴스를 만든 뒤 setter로 값을 주입한다. `@Builder`만 있으면 기본 생성자가 없어서 역직렬화가 실패한다.

HTTP 파일에서 Command 요청을 `02-command-side.http`에만 두고 나머지에서 제거한 이유는 DRY 원칙이다. 기존에는 4개 파일 모두에 동일한 POST 요청이 중복되어 있어서 API 변경 시 4곳을 수정해야 했다. `02`를 먼저 실행하고 `03~05`에서 검증하는 순서로 사용하면 중복 없이 전체 흐름을 테스트할 수 있다.

## 교차 검증 결과

### Claude 리뷰

`@Data` + `@Builder` + `@NoArgsConstructor` + `@AllArgsConstructor` 조합은 Lombok에서 흔히 사용되지만, `@Data`의 `@EqualsAndHashCode`가 모든 필드를 포함하므로 주의가 필요하다. `PostView`의 `likedBy`(List)가 equals 비교에 포함되면 성능 이슈가 될 수 있다. 현재 프로젝트에서는 PostView의 equals를 직접 호출하는 코드가 없으므로 문제없다.

HTTP 파일의 `client.global` 변수 공유는 IntelliJ HTTP Client 전용 기능이다. VS Code REST Client 등 다른 도구에서는 동작하지 않는다. 학습 프로젝트에서는 IntelliJ를 사용하므로 문제없다.

### 수정 사항

`@Builder` 추가 후 Lombok 경고 2개 발생 (`@Builder will ignore the initializing expression`) → `@Builder.Default` 추가로 해결. `compileJava` 빌드 통과, 경고 0개.

## 핵심 학습 포인트

- **생성에는 빌더, 변경에는 setter가 자연스럽다.** 새 객체를 만들 때는 빌더로 모든 필드를 한 번에 설정하고 `build()`로 완성한다. 기존 객체의 일부 필드만 바꿀 때는 setter가 간결하다. 하나의 클래스에서 두 패턴을 혼용하는 것은 정상이다.

- **`@Builder.Default`는 필드 초기값과 빌더를 양립시킨다.** Lombok `@Builder`는 기본적으로 필드 초기값을 무시한다. 컬렉션 필드처럼 초기값이 중요한 경우 `@Builder.Default`를 추가하여 빌더에서도 초기값이 적용되도록 해야 한다.

- **`@NoArgsConstructor`는 JSON 역직렬화에 필수다.** Jackson의 기본 전략은 "기본 생성자 + setter"다. `@Builder`만으로는 기본 생성자가 생성되지 않으므로, JsonSerde를 사용하는 모델에는 `@NoArgsConstructor`를 반드시 함께 선언해야 한다.

- **HTTP 테스트 파일도 DRY 원칙을 적용한다.** canonical 파일에서 데이터를 생성하고 변수를 캡처한 뒤, 검증 파일에서 참조하면 Command 요청 중복 없이 전체 흐름을 테스트할 수 있다.
