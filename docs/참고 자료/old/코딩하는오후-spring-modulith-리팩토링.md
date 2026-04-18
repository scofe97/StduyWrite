# Spring Modulith 적용 후 리팩토링 코드 리뷰

> 출처: [코딩하는오후 YouTube](https://www.youtube.com/@codingpm)
> 영상: 스프링 모듈리스 적용 후 리펙토링 한 것에 대한 코드 리뷰

---

## 프로젝트 배경

### 구조

```
개별 리포지토리들 (테스트용)
├── LMS
├── 버스 쓰레드 데모
├── 메뉴
├── 파일 업로드
├── 오디팅 (이력 관리)
├── 마이바티스 DSL
└── 데모 UI (React + TanStack Router)
        │
        ▼
    LMS 리포지토리 (통합)
        │
        ▼
    Spring Modulith 2.0 적용
```

### 작업 방식

1. 개별 리포지토리에서 기능별 테스트 코드 작성
2. 모든 테스트 코드와 함께 LMS로 통합
3. Spring Modulith 적용 후 리팩토링

---

## 주요 리팩토링 사항

### 1. Response 객체 구조 (Sealed Interface)

**DefaultResponseHandler** - ResponseBodyAdvice 구현

```java
@RestControllerAdvice
public class DefaultResponseHandler implements ResponseBodyAdvice<Object> {
    // 컨트롤러 응답을 Response 객체로 감싸서 반환
}
```

**Response Sealed Interface**

```java
public sealed interface Response<T> permits Success, Fail {
    // 성공/실패 두 가지 타입만 허용
}

public record Success<T>(T data) implements Response<T> {}
public record Fail<T>(String message, T error) implements Response<T> {}
```

**테스트 시 ParameterizedTypeReference 사용**

```java
// 기존: Post만
ParameterizedTypeReference<Post> ref = new ParameterizedTypeReference<>() {};

// 변경: Response.Success<Post>로 감싸서
ParameterizedTypeReference<Response.Success<Post>> ref =
    new ParameterizedTypeReference<>() {};
```

---

### 2. @EnableAsync 설정

**이유**: `@ApplicationModuleListener`에 `@Async`가 포함되어 있음

```java
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        // 설정...
        return executor;
    }
}
```

**@ApplicationModuleListener 내부 구조** (Spring Modulith 2.0)

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@TransactionalEventListener  // 트랜잭션 이벤트
@Transactional               // 트랜잭션 관리
@Async                       // 비동기 실행
public @interface ApplicationModuleListener {
}
```

**참고**: 버전 1에서는 `@ApplicationEventListener`만 있었고, 트랜잭션 처리가 어려웠음

---

### 3. Primitive → Wrapper 타입 변경

```java
// 기존: null 처리 불가
public record Post(int id, String title) {}

// 변경: null 허용
public record Post(Integer id, String title) {}
```

**이유**: JSON 직렬화 시 null 처리 문제 해결

---

### 4. ChangeEvent 이벤트 시스템

**Sealed Interface로 이벤트 타입 정의**

```java
public sealed interface ChangeEvent<T extends Entity>
    permits Created, Updated, Queried, LoggedIn {
}

public record Created<T extends Entity>(T entity) implements ChangeEvent<T> {}
public record Updated<T extends Entity>(T entity) implements ChangeEvent<T> {}
public record Queried<T extends Entity>(T entity) implements ChangeEvent<T> {}
public record LoggedIn<T extends Entity>(T entity) implements ChangeEvent<T> {}
```

**Entity 인터페이스**

```java
public interface Entity {
    Object getId();  // 모든 엔티티는 ID 필수
}
```

**ChangeEventListener**

```java
@Component
public class ChangeEventListener {

    @ApplicationModuleListener
    public void on(ChangeEvent<? extends Entity> event) {
        // 이력 저장 등 처리
    }
}
```

---

### 5. Entity 타입 풀 경로 저장

**문제**: 이력 데이터 역직렬화 시 클래스 찾기 어려움

```java
// 기존: 클래스명만 저장
entityType = "User"

// 변경: 풀 경로 저장
entityType = "com.example.user.User"
```

**역직렬화 시**

```java
Class<?> targetClass = Class.forName(entityType);
Entity entity = objectMapper.readValue(jsonData, targetClass);
```

---

### 6. 이중 직렬화 버그 수정

**문제**: JSON 데이터가 이중으로 직렬화됨

```java
// 버그: String을 다시 JSON으로 감쌈
String jsonData = objectMapper.writeValueAsString(entity);
String doubleEncoded = objectMapper.writeValueAsString(jsonData);  // ❌
```

**해결**

```java
// 이미 String이면 그대로 사용
if (data instanceof String) {
    return (String) data;
}
return objectMapper.writeValueAsString(data);
```

---

### 7. EventPublicationRegistry 스키마

**용도**: 모듈 간 이벤트 트랜잭션 관리

```sql
-- Spring Modulith 제공 스키마
CREATE TABLE event_publication (
    id UUID PRIMARY KEY,
    listener_id VARCHAR(255),
    event_type VARCHAR(255),
    serialized_event TEXT,
    publication_date TIMESTAMP,
    completion_date TIMESTAMP
);
```

**설정**

```yaml
spring:
  modulith:
    events:
      jdbc:
        schema-initialization:
          enabled: true  # 자동 생성 옵션
```

---

### 8. @TempDir 활용 (파일 테스트)

**기존 방식**: 수동으로 경로 지정, 삭제 필요

**개선 방식**: JUnit의 @TempDir 사용

```java
@Test
void fileUploadTest(@TempDir Path tempDir) {
    // tempDir: 테스트 전용 임시 디렉토리
    // 테스트 종료 후 자동 삭제

    Path serverPath = tempDir.resolve("uploaded-file.txt");

    // 테스트 수행...

    // 검증
    assertThat(Files.exists(serverPath)).isTrue();
}
```

**장점**:
- OS별 임시 경로 자동 처리
- 테스트 종료 후 자동 정리
- 경로 충돌 방지

---

### 9. Scenario API (비동기 이벤트 테스트)

**문제**: `@ApplicationModuleListener`가 `@Async`로 동작하여 테스트 어려움

**해결**: Spring Modulith의 Scenario API

```java
@ApplicationModuleTest
class ChangeEventListenerTest {

    @Test
    void eventTest(Scenario scenario) {
        // scenario: 자동 주입됨

        scenario.stimulate(() -> {
            // 이벤트 발행
            eventPublisher.publishEvent(new Created<>(user));
        })
        .andWaitForEventOfType(Created.class)
        .toArriveAndVerify(event -> {
            // 검증
            assertThat(event.entity()).isNotNull();
        });
    }
}
```

---

## 핵심 교훈

### 통합 시 발생한 문제들

1. **개별 테스트 → 통합 시 실패**
   - 모듈 간 의존성 충돌
   - 빈 등록 순서 문제
   - 트랜잭션 경계 문제

2. **Modulith 적용 시 고려사항**
   - 도메인 모델 소유권 (어느 모듈 소속인지)
   - 이벤트 기반 통신으로 결합도 낮추기
   - 테스트 전략 변경 필요

### 권장 학습 순서

1. Spring Modulith 기본 개념
2. 모듈 구조 설계
3. 이벤트 기반 통신
4. Scenario API를 이용한 테스트
5. EventPublicationRegistry 활용

---

## 관련 리소스

- GitHub: [코딩하는오후 LMS Repository](https://github.com/codingpm)
- Spring Modulith 2.0 공식 문서
- REST Client 시리즈 (ParameterizedTypeReference)

---

## POC 적용 체크리스트

| 항목 | 적용 여부 | 비고 |
|------|----------|------|
| Response Sealed Interface | ☐ | Success/Fail |
| @EnableAsync 설정 | ☐ | AsyncConfig |
| ChangeEvent 구조 | ☐ | 이력 관리용 |
| Entity 인터페이스 | ☐ | getId() 필수 |
| @ApplicationModuleListener | ☐ | 버전 2 신규 |
| EventPublicationRegistry | ☐ | 스키마 필요 |
| Scenario API 테스트 | ☐ | 비동기 테스트 |
| @TempDir 테스트 | ☐ | 파일 업로드 |
