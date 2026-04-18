# 액티비티를 구현하는 Internal Service

> 출처: [코딩하는오후 YouTube](https://www.youtube.com/@codingpm)
> 영상: 액티비티를 구현하는 internal Service

---

## 핵심 메시지

### 테스트 코드의 새로운 관점

**기존 인식**: 테스트 자동화를 위한 부가적인 도구

**제안하는 관점**: **도메인 모델 학습 도구**

```
테스트 코드 = 도메인 모델을 유닛으로 나눠서 학습하는 도구
            (테스트 자동화 ❌, 모델 학습 ✅)
```

> "TDD 논쟁하고 싶지 않습니다. 테스트 코드를 도메인 모델 학습 도구로 정의했기 때문에 TDD와는 전혀 관련 없습니다."

---

## 아키텍처 구조

### 패키지 구조

```
com.example.post/
├── application/               # Activity 인터페이스들
│   ├── CreatePostActivity.java
│   ├── UpdatePostActivity.java
│   ├── DeletePostActivity.java
│   ├── ViewPostDetailActivity.java
│   └── SearchPostActivity.java
│
├── internal/                  # 내부 구현체
│   └── PostService.java       # 모든 Activity 구현
│
├── port/                      # 외부 인프라 연결
│   └── PostClient.java        # 인터페이스 (Port)
│
└── domain/
    └── Post.java
```

### 레이어 관계

```
┌─────────────────────────────────────────────────┐
│                  Application                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Create   │ │ Update   │ │ Search   │ ...    │
│  │ Activity │ │ Activity │ │ Activity │        │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘        │
│       │            │            │               │
│       └────────────┼────────────┘               │
│                    ▼                            │
│  ┌─────────────────────────────────────┐       │
│  │         PostService (internal)       │       │
│  │   implements All Activities          │       │
│  └──────────────────┬──────────────────┘       │
│                     │                           │
│                     ▼                           │
│  ┌─────────────────────────────────────┐       │
│  │         PostClient (port)            │       │
│  │   interface - 외부 인프라 연결        │       │
│  └─────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

---

## Activity 인터페이스 분리 철학

### 왜 분리하는가?

**핵사고널 아키텍처 권장 방식**

```java
// ❌ 하나의 큰 서비스 인터페이스
public interface PostService {
    Post create(Post post);
    Post update(Post post);
    void delete(Long id);
    Post findById(Long id);
    List<Post> search(SearchRQ rq);
}

// ✅ Activity별 분리 (권장)
public interface CreatePostActivity {
    Post createPost(Post post);
}

public interface UpdatePostActivity {
    Post updatePost(Long id, Post post);
}

public interface ViewPostDetailActivity {
    Post postDetail(Long id);
}
// ...
```

### 분리의 장점

| 장점 | 설명 |
|------|------|
| **변경 추적** | 어떤 Activity가 변경됐는지 명확 |
| **Context Boundary** | Activity 단위로 경계 분리 |
| **테스트 용이** | Activity별 독립 테스트 가능 |
| **유연한 조합** | 필요한 Activity만 선택적 구현 |

### Context Boundary에 대한 인사이트

> "DDD에서 Context Boundary를 Aggregate Root(Entity)로 분리한다고 설명하는 경우가 많은데,
> 저는 **Activity에 의해서 Context Boundary가 나눠지는 것**을 경험했습니다."

---

## Internal Service 구현

### 구현체는 하나로 통합

```java
// internal 패키지에 배치
@Service
class PostService implements
    CreatePostActivity,
    UpdatePostActivity,
    DeletePostActivity,
    ViewPostDetailActivity,
    SearchPostActivity {

    private final PostClient postClient;  // Port 주입

    // 모든 Activity 메서드 구현
    @Override
    public Post createPost(Post post) {
        return postClient.createPost(post);
    }

    @Override
    public Post updatePost(Long id, Post post) {
        return postClient.updatePost(id, post);
    }
    // ...
}
```

### 단일 책임 원칙(SRP) 해석

**"객체는 책임을 하나만 가져야 한다"** 보다 정확한 표현:

> **"변경되는 이유는 하나여야 한다"**

- Activity 인터페이스들을 하나의 Service가 구현해도 괜찮음
- 변경 이유: "Activity가 변경되어서"로 통일됨
- **유연하게 개발하자**

---

## Port 인터페이스

### Port의 역할

```
Internal Service ←── Port ──→ External Infrastructure
                 (인터페이스)     (REST Client, DB 등)
```

```java
// port 패키지에 배치 (internal 아님!)
public interface PostClient {
    Optional<Post> findById(Long id);
    List<Comment> findCommentsByPostId(Long postId);
    Post createPost(Post post);
    Post updatePost(Long id, Post post);
    void deletePost(Long id);
    List<Post> searchPosts(Map<String, Object> params);
}
```

### Port의 장점

1. **구현 지연**: 아직 외부 인프라 준비 안 됐어도 개발 가능
2. **Mock 테스트**: 인터페이스를 Mock으로 대체 가능
3. **구현체 교체**: REST → gRPC 등 변경 용이

---

## Optional 처리 전략

### 레이어별 처리 방식

| 레이어 | Optional 사용 | 이유 |
|--------|--------------|------|
| **Port (인터페이스)** | ✅ 사용 | 외부 결과의 불확실성 표현 |
| **Service (리턴)** | ❌ 제거 | 최종 결과만 반환 |

```java
// Port - Optional 반환
public interface PostClient {
    Optional<Post> findById(Long id);
    List<Comment> findCommentsByPostId(Long postId);
}

// Service - Optional 처리 후 결과 반환
@Override
public Post postDetail(Long id) {
    return postClient.findById(id)
        .map(post -> {
            if (post.comments() == null || post.comments().isEmpty()) {
                List<Comment> comments = postClient.findCommentsByPostId(id);
                return post.withComments(comments);  // Wither 패턴
            }
            return post;
        })
        .orElseThrow(() -> new PostNotFoundException(id));
}
```

---

## 실습 예시: PostDetail 구현

### 요구사항

- Post 상세 조회 시 Comment도 함께 가져오기
- Comment가 없으면 별도 조회

### 구현

```java
@Override
public Post postDetail(Long id) {
    return postClient.findById(id)
        .map(post -> {
            // Comment가 없으면 별도 조회
            if (post.comments() == null || post.comments().isEmpty()) {
                List<Comment> comments = postClient.findCommentsByPostId(id);
                return post.withComments(comments);  // Record의 Wither 패턴
            }
            return post;
        })
        .orElseThrow(() -> new PostNotFoundException(id));
}
```

### Record의 Wither 패턴

```java
public record Post(
    Long id,
    String title,
    String body,
    List<Comment> comments
) {
    // 불변 객체에서 특정 필드만 변경한 새 객체 생성
    public Post withComments(List<Comment> newComments) {
        return new Post(this.id, this.title, this.body, newComments);
    }
}
```

---

## 반복 공정의 장점

> "앞부분에서 완벽하게 구현하지 않아도, 뒤에서 알아차려서 다시 단계를 훅 올라가야 되는 케이스 없게끔 구성했습니다."

### 공정 흐름

```
유스케이스 도출
     ↓
Activity 인터페이스 정의
     ↓
Internal Service 구현  ←─┐
     ↓                   │ 반복 가능
Port 인터페이스 도출      │
     ↓                   │
REST Client 구현 ────────┘
     ↓
테스트 코드 작성
```

- 각 단계에서 누락된 부분 발견 시 이전 단계 수정
- 점진적 완성 가능

---

## 과제 & 학습 포인트

### 1. 테스트 적정성 고민

- 서비스 레이어 로직이 단순하면 테스트 생략 고려
- REST Client 구현 시 더 가치 있는 테스트 작성
- **유연하게 판단**

### 2. Spring Boot 테스트 종류 조사

- 슬라이스 테스트 (`@WebMvcTest`, `@DataJpaTest` 등)
- 통합 테스트 (`@SpringBootTest`)
- 목적에 맞는 테스트 선택

---

## POC 적용 체크리스트

| 항목 | 적용 여부 | 비고 |
|------|----------|------|
| Activity 인터페이스 분리 | ☐ | application 패키지 |
| Internal Service 구현 | ☐ | internal 패키지, 모든 Activity implements |
| Port 인터페이스 정의 | ☐ | port 패키지 |
| Optional 처리 전략 | ☐ | Port: Optional, Service: 결과만 |
| Wither 패턴 (Record) | ☐ | 불변 객체 업데이트용 |
| 테스트 코드 (선택적) | ☐ | 도메인 학습 목적 |

---

## 관련 영상

- [스프링 모듈리스 적용 후 리팩토링 코드 리뷰](./코딩하는오후-spring-modulith-리팩토링.md)
- 스프링부트 단위 테스트와 슬라이스 테스트 (재생목록)
