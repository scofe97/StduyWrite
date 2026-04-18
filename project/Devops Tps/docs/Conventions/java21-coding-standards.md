# Java 21 코딩 표준

## 개요

TPS-API 프로젝트는 **Java 21 LTS**를 사용합니다.
최신 Java 기능을 적극 활용하여 간결하고 안전한 코드를 작성합니다.

---

## 필수 사용 기능

### 1. Record (데이터 클래스)

**DTO, Command, Query, Value Object에 record 사용**

```java
// ❌ 기존 방식 (사용 금지)
@Getter
@AllArgsConstructor
public class CreateConnectionCommand {
    private final UUID projectId;
    private final ProviderType providerType;
    private final String name;
}

// ✅ Java 21 방식 (필수)
public record CreateConnectionCommand(
    UUID projectId,
    ProviderType providerType,
    String name
) {}
```

**record 적용 대상:**
| 대상 | 예시 |
|------|------|
| Command | `CreateConnectionCommand`, `UpdateBranchCommand` |
| Query | `GetTreeQuery`, `CompareBranchesQuery` |
| DTO | `ConnectionResponse`, `BranchComparisonResult` |
| Value Object | `GitUrl`, `Credential` |
| 내부 데이터 전달 | `ComparisonResult`, `CleanupResult` |

**record 미적용 대상:**
- Entity (JPA 엔티티는 기본 생성자 필요)
- 상태 변경이 필요한 객체

---

### 2. Sealed Classes (봉인 클래스)

**제한된 상속 계층 정의**

```java
// ✅ 상태 타입 정의
public sealed interface ConnectionState
    permits ActiveState, InactiveState, ErrorState {
}

public record ActiveState(Instant activatedAt) implements ConnectionState {}
public record InactiveState(String reason) implements ConnectionState {}
public record ErrorState(String errorMessage, Instant occurredAt) implements ConnectionState {}
```

---

### 3. Pattern Matching

#### 3.1 instanceof 패턴 매칭

```java
// ❌ 기존 방식
if (obj instanceof String) {
    String s = (String) obj;
    return s.length();
}

// ✅ Java 21 방식
if (obj instanceof String s) {
    return s.length();
}
```

#### 3.2 Switch 패턴 매칭

```java
// ✅ Switch Expression + Pattern Matching
public String describe(Object obj) {
    return switch (obj) {
        case null -> "null";
        case String s -> "String: " + s;
        case Integer i -> "Integer: " + i;
        case Connection c -> "Connection: " + c.getName();
        default -> "Unknown: " + obj.getClass();
    };
}
```

#### 3.3 Record 패턴

```java
// ✅ Record Destructuring
public void process(Result result) {
    switch (result) {
        case Success(var data, var message) ->
            log.info("Success: {} - {}", data, message);
        case Failure(var error) ->
            log.error("Failed: {}", error);
    }
}
```

---

### 4. Switch Expression

**항상 switch expression 사용 (statement 금지)**

```java
// ❌ 기존 switch statement
String result;
switch (status) {
    case ACTIVE:
        result = "활성";
        break;
    case INACTIVE:
        result = "비활성";
        break;
    default:
        result = "알 수 없음";
}

// ✅ Switch Expression
String result = switch (status) {
    case ACTIVE -> "활성";
    case INACTIVE -> "비활성";
    default -> "알 수 없음";
};
```

---

### 5. Text Blocks

**여러 줄 문자열에 Text Block 사용**

```java
// ❌ 기존 방식
String json = "{\n" +
    "  \"name\": \"test\",\n" +
    "  \"value\": 123\n" +
    "}";

// ✅ Text Block
String json = """
    {
      "name": "test",
      "value": 123
    }
    """;
```

---

### 6. var 키워드

**명확한 경우에만 var 사용**

```java
// ✅ 타입이 명확한 경우
var connection = connectionRepository.findById(id);
var branches = new ArrayList<Branch>();
var result = service.process(command);

// ❌ 타입이 불명확한 경우 (사용 금지)
var data = getData();  // 반환 타입 불명확
```

---

### 7. Optional 활용

```java
// ✅ Optional 체이닝
public String getConnectionName(UUID id) {
    return connectionRepository.findById(id)
        .map(Connection::getName)
        .orElse("Unknown");
}

// ✅ Optional과 Stream 조합
public List<String> getActiveConnectionNames() {
    return connectionRepository.findAll().stream()
        .filter(c -> c.getStatus() == ConnectionStatus.ACTIVE)
        .map(Connection::getName)
        .toList();  // Java 16+ toList()
}
```

---

### 8. Stream API 개선

```java
// ✅ toList() 사용 (불변 리스트 반환)
List<String> names = connections.stream()
    .map(Connection::getName)
    .toList();

// ✅ mapMulti (flatMap 대체)
List<String> allBranches = repositories.stream()
    .<String>mapMulti((repo, consumer) -> {
        repo.getBranches().forEach(b -> consumer.accept(b.getName()));
    })
    .toList();
```

---

## 프로젝트 적용 예시

### UseCase Command/Query

```java
// application/port/in/ConnectionUseCase.java
public interface ConnectionUseCase {

    // ✅ Record로 Command 정의
    record CreateConnectionCommand(
        UUID projectId,
        ProviderType providerType,
        String name,
        String baseUrl,
        String apiToken,
        Map<String, Object> metadata
    ) {}

    record UpdateConnectionCommand(
        String name,
        String baseUrl,
        String apiToken,
        Map<String, Object> metadata
    ) {}

    Connection createConnection(CreateConnectionCommand command);
    Connection updateConnection(UUID id, UpdateConnectionCommand command);
}
```

### Controller Response

```java
// adapter/in/web/dto/ConnectionResponse.java
public record ConnectionResponse(
    UUID id,
    UUID projectId,
    ProviderType providerType,
    String name,
    String baseUrl,
    ConnectionStatus status,
    Instant createdAt,
    Instant updatedAt
) {
    public static ConnectionResponse from(Connection connection) {
        return new ConnectionResponse(
            connection.getId(),
            connection.getProjectId(),
            connection.getProviderType(),
            connection.getName(),
            connection.getBaseUrl(),
            connection.getStatus(),
            connection.getCreatedAt(),
            connection.getUpdatedAt()
        );
    }
}
```

### 도메인 Value Object

```java
// domain/connection/GitUrl.java
public record GitUrl(
    String protocol,
    String host,
    String namespace,
    String repository
) {
    public GitUrl {
        // Compact Constructor로 유효성 검증
        Objects.requireNonNull(host, "host is required");
        Objects.requireNonNull(repository, "repository is required");
    }

    public static GitUrl parse(String url) {
        // 파싱 로직
        return new GitUrl(protocol, host, namespace, repository);
    }

    public String toHttpsUrl() {
        return "https://%s/%s/%s".formatted(host, namespace, repository);
    }
}
```

---

## 체크리스트

코드 리뷰 시 확인 사항:

- [ ] DTO/Command/Query가 record로 정의되었는가?
- [ ] switch statement 대신 switch expression을 사용했는가?
- [ ] instanceof 패턴 매칭을 사용했는가?
- [ ] 여러 줄 문자열에 Text Block을 사용했는가?
- [ ] Stream에서 `.collect(Collectors.toList())` 대신 `.toList()`를 사용했는가?
- [ ] 불필요한 Lombok 어노테이션(@Getter, @AllArgsConstructor)이 없는가?

---

## 참고

- [JEP 395: Records](https://openjdk.org/jeps/395)
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409)
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441)
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440)
