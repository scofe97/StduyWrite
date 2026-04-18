# UseCase와 Activity Interface 심층 분석

> Clean Architecture, Hexagonal Architecture, Activity Interface 패턴의 통합 이해

---

## 1. 개념적 배경

### 1.1 용어 정리

| 용어 | 출처 | 정의 | 역할 |
|------|------|------|------|
| **UseCase** | Clean Architecture | 시스템이 수행하는 비즈니스 기능 단위 | 비즈니스 플로우 정의 (What) |
| **Interactor** | Clean Architecture | UseCase의 구현체 | 비즈니스 로직 실행 (How) |
| **Port** | Hexagonal Architecture | 시스템 경계의 인터페이스 | 외부와의 통신 계약 |
| **Adapter** | Hexagonal Architecture | Port의 구현체 | 외부 시스템 연결 |
| **Activity** | 코딩하는오후 | 구체적 비즈니스 활동 | 설계 ↔ 코드 매핑 |
| **Action** | 코딩하는오후 | Activity 내 세부 작업 | 메서드 레벨 작업 |

### 1.2 아키텍처 계층 비교

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Clean Architecture                               │
├─────────────────────────────────────────────────────────────────────┤
│  [Frameworks & Drivers] → [Adapters] → [Use Cases] → [Entities]     │
│       (외부)              (변환)       (비즈니스규칙)  (핵심도메인)    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    Hexagonal Architecture                           │
├─────────────────────────────────────────────────────────────────────┤
│  [Primary Adapter] → [Inbound Port] → [Core] → [Outbound Port] → [Secondary Adapter]
│     (Controller)      (UseCase IF)    (Domain)    (Repository IF)    (DB Adapter)
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    Activity Interface (코딩하는오후)                  │
├─────────────────────────────────────────────────────────────────────┤
│  [API] → [Activity Interface] → [Service/Activity Impl] → [Port] → [Infra]
│                ↑
│         설계 문서와 1:1 매핑 (소리치는 아키텍처)
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. 패턴별 상세 분석

### 2.1 Clean Architecture - UseCase/Interactor

**핵심 원칙**: 비즈니스 로직은 프레임워크로부터 독립적이어야 한다

```
UseCase = Interface (Input Boundary)
Interactor = Implementation (비즈니스 로직)
```

**의존성 방향**: 외부 → 내부 (항상 안쪽을 향함)

### 2.2 Hexagonal Architecture - Ports & Adapters

**핵심 원칙**: 애플리케이션은 포트를 통해서만 외부와 통신

| Port 유형 | 방향 | 역할 | 예시 |
|-----------|------|------|------|
| **Inbound (Driving)** | 외부 → 내부 | 애플리케이션 호출 | UseCase 인터페이스 |
| **Outbound (Driven)** | 내부 → 외부 | 외부 시스템 호출 | Repository 인터페이스 |

### 2.3 Activity Interface - 설계와 구현의 일치

**핵심 원칙**: Activity 다이어그램의 활동이 코드의 인터페이스 메서드와 1:1 매핑

```
[Activity Diagram]          →    [Activity Interface]
├── 회원가입하기                   ├── registerMember()
├── 이메일 인증하기                ├── verifyEmail()
└── 프로필 설정하기                └── setupProfile()
```

---

## 3. 실제 코드 예시: 러너 등록 시스템

### 3.1 도메인 모델 (Domain Layer)

```java
// ===== 도메인 엔티티 =====
package com.runnershigh.modulith.runner;

public class Runner {
    private Long id;
    private String name;
    private String email;
    private RunnerLevel level;
    private LocalDateTime registeredAt;

    // 생성자 - 비즈니스 규칙 적용
    public static Runner create(String name, String email) {
        Runner runner = new Runner();
        runner.name = validateName(name);
        runner.email = validateEmail(email);
        runner.level = RunnerLevel.BEGINNER;  // 기본값
        runner.registeredAt = LocalDateTime.now();
        return runner;
    }

    // 비즈니스 로직 - 레벨 승급
    public void promoteLevel() {
        this.level = this.level.next();
    }

    private static String validateName(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        return name.trim();
    }

    private static String validateEmail(String email) {
        if (!email.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }
        return email.toLowerCase();
    }
}

// ===== Value Object =====
public enum RunnerLevel {
    BEGINNER, INTERMEDIATE, ADVANCED, ELITE;

    public RunnerLevel next() {
        return switch (this) {
            case BEGINNER -> INTERMEDIATE;
            case INTERMEDIATE -> ADVANCED;
            case ADVANCED -> ELITE;
            case ELITE -> ELITE;  // 최고 레벨 유지
        };
    }
}
```

### 3.2 Activity Interface 정의 (Application Layer - Inbound Port)

```java
// ===== Activity Interface (Inbound Port) =====
// 설계 문서의 Activity Diagram과 1:1 매핑
package com.runnershigh.modulith.runner.activity;

/**
 * 러너 등록 Activity
 *
 * 비즈니스 플로우:
 * 1. 이메일 중복 확인 (Action)
 * 2. 러너 생성 (Action)
 * 3. 환영 이메일 발송 (확장 Activity)
 */
public interface RegisterRunnerActivity {

    /**
     * 러너 등록 - 메인 플로우
     * @param command 등록 명령
     * @return 등록 결과
     */
    RegisterResult register(RegisterRunnerCommand command);

    /**
     * 이메일 중복 확인 - Action
     */
    boolean isEmailAvailable(String email);
}

// ===== Command (Input) =====
public record RegisterRunnerCommand(
    String name,
    String email
) {
    public RegisterRunnerCommand {
        Objects.requireNonNull(name, "name is required");
        Objects.requireNonNull(email, "email is required");
    }
}

// ===== Result (Output) - Sealed Interface =====
public sealed interface RegisterResult
    permits RegisterResult.Success, RegisterResult.Failure {

    record Success(Long runnerId, String name) implements RegisterResult {}

    record Failure(String reason, FailureType type) implements RegisterResult {
        public enum FailureType {
            DUPLICATE_EMAIL,
            INVALID_DATA,
            SYSTEM_ERROR
        }
    }
}
```

### 3.3 추가 Activity Interface 예시

```java
// ===== 러너 조회 Activity =====
public interface SearchRunnerActivity {

    /**
     * ID로 러너 조회
     */
    Optional<RunnerInfo> findById(Long id);

    /**
     * 레벨별 러너 목록 조회
     */
    List<RunnerInfo> findByLevel(RunnerLevel level);

    /**
     * 전체 러너 검색 (페이징)
     */
    Page<RunnerInfo> search(RunnerSearchCriteria criteria);
}

// ===== DTO (Output) =====
public record RunnerInfo(
    Long id,
    String name,
    String email,
    RunnerLevel level,
    LocalDateTime registeredAt
) {
    public static RunnerInfo from(Runner runner) {
        return new RunnerInfo(
            runner.getId(),
            runner.getName(),
            runner.getEmail(),
            runner.getLevel(),
            runner.getRegisteredAt()
        );
    }
}

// ===== 러너 레벨 관리 Activity =====
public interface ManageRunnerLevelActivity {

    /**
     * 레벨 승급
     */
    LevelChangeResult promote(Long runnerId);

    /**
     * 레벨 수동 설정 (관리자용)
     */
    LevelChangeResult setLevel(Long runnerId, RunnerLevel newLevel);
}
```

### 3.4 Outbound Port 정의

```java
// ===== Repository Port (Outbound) =====
package com.runnershigh.modulith.runner.port;

public interface RunnerRepository {

    Runner save(Runner runner);

    Optional<Runner> findById(Long id);

    Optional<Runner> findByEmail(String email);

    List<Runner> findByLevel(RunnerLevel level);

    Page<Runner> findAll(Pageable pageable);

    boolean existsByEmail(String email);
}

// ===== 이벤트 발행 Port =====
public interface RunnerEventPublisher {

    void publishRegistered(RunnerRegisteredEvent event);

    void publishLevelChanged(RunnerLevelChangedEvent event);
}
```

### 3.5 Service 구현 (Activity Implementation)

```java
// ===== Activity 구현체 (Service) =====
package com.runnershigh.modulith.runner.internal;

@Service
@RequiredArgsConstructor
class RunnerService implements RegisterRunnerActivity, SearchRunnerActivity {

    private final RunnerRepository runnerRepository;
    private final RunnerEventPublisher eventPublisher;

    // ===== RegisterRunnerActivity 구현 =====

    @Override
    @Transactional
    public RegisterResult register(RegisterRunnerCommand command) {
        // Action 1: 이메일 중복 확인
        if (!isEmailAvailable(command.email())) {
            return new RegisterResult.Failure(
                "이미 등록된 이메일입니다",
                RegisterResult.Failure.FailureType.DUPLICATE_EMAIL
            );
        }

        try {
            // Action 2: 러너 생성
            Runner runner = Runner.create(command.name(), command.email());
            Runner saved = runnerRepository.save(runner);

            // Action 3: 이벤트 발행 (확장 Activity 트리거)
            eventPublisher.publishRegistered(
                new RunnerRegisteredEvent(saved.getId(), saved.getEmail())
            );

            return new RegisterResult.Success(saved.getId(), saved.getName());

        } catch (IllegalArgumentException e) {
            return new RegisterResult.Failure(
                e.getMessage(),
                RegisterResult.Failure.FailureType.INVALID_DATA
            );
        }
    }

    @Override
    public boolean isEmailAvailable(String email) {
        return !runnerRepository.existsByEmail(email);
    }

    // ===== SearchRunnerActivity 구현 =====

    @Override
    @Transactional(readOnly = true)
    public Optional<RunnerInfo> findById(Long id) {
        return runnerRepository.findById(id)
            .map(RunnerInfo::from);
    }

    @Override
    @Transactional(readOnly = true)
    public List<RunnerInfo> findByLevel(RunnerLevel level) {
        return runnerRepository.findByLevel(level).stream()
            .map(RunnerInfo::from)
            .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public Page<RunnerInfo> search(RunnerSearchCriteria criteria) {
        return runnerRepository.findAll(criteria.toPageable())
            .map(RunnerInfo::from);
    }
}
```

### 3.6 Adapter 구현

```java
// ===== REST Controller (Primary Adapter) =====
package com.runnershigh.modulith.runner.adapter.api;

@RestController
@RequestMapping("/api/runners")
@RequiredArgsConstructor
public class RunnerController {

    private final RegisterRunnerActivity registerActivity;
    private final SearchRunnerActivity searchActivity;

    @PostMapping
    public ResponseEntity<?> register(@RequestBody @Valid RegisterRequest request) {
        RegisterRunnerCommand command = new RegisterRunnerCommand(
            request.name(),
            request.email()
        );

        RegisterResult result = registerActivity.register(command);

        return switch (result) {
            case RegisterResult.Success s ->
                ResponseEntity.created(URI.create("/api/runners/" + s.runnerId()))
                    .body(new RegisterResponse(s.runnerId(), s.name()));

            case RegisterResult.Failure f ->
                ResponseEntity.badRequest()
                    .body(new ErrorResponse(f.reason(), f.type().name()));
        };
    }

    @GetMapping("/{id}")
    public ResponseEntity<RunnerInfo> getRunner(@PathVariable Long id) {
        return searchActivity.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public ResponseEntity<Page<RunnerInfo>> searchRunners(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        RunnerSearchCriteria criteria = new RunnerSearchCriteria(page, size);
        return ResponseEntity.ok(searchActivity.search(criteria));
    }
}

// ===== Repository Adapter (Secondary Adapter) =====
package com.runnershigh.modulith.runner.adapter.persistence;

@Repository
@RequiredArgsConstructor
class JpaRunnerRepository implements RunnerRepository {

    private final RunnerJpaRepository jpaRepository;

    @Override
    public Runner save(Runner runner) {
        RunnerEntity entity = RunnerEntity.from(runner);
        RunnerEntity saved = jpaRepository.save(entity);
        return saved.toDomain();
    }

    @Override
    public Optional<Runner> findById(Long id) {
        return jpaRepository.findById(id)
            .map(RunnerEntity::toDomain);
    }

    @Override
    public Optional<Runner> findByEmail(String email) {
        return jpaRepository.findByEmail(email)
            .map(RunnerEntity::toDomain);
    }

    @Override
    public boolean existsByEmail(String email) {
        return jpaRepository.existsByEmail(email);
    }

    // ... 나머지 구현
}
```

---

## 4. 패키지 구조

### 4.1 권장 패키지 구조

```
com.runnershigh.modulith/
├── ModulithApplication.java
│
├── runner/                              # Runner 모듈
│   ├── Runner.java                      # 도메인 엔티티 (public)
│   ├── RunnerLevel.java                 # Value Object (public)
│   ├── RunnerRegisteredEvent.java       # 도메인 이벤트 (public)
│   │
│   ├── activity/                        # Activity Interfaces (public)
│   │   ├── RegisterRunnerActivity.java
│   │   ├── SearchRunnerActivity.java
│   │   └── ManageRunnerLevelActivity.java
│   │
│   ├── port/                            # Outbound Ports (public)
│   │   ├── RunnerRepository.java
│   │   └── RunnerEventPublisher.java
│   │
│   └── internal/                        # 구현체 (internal - 외부 접근 불가)
│       ├── RunnerService.java           # Activity 구현
│       ├── JpaRunnerRepository.java     # Repository 구현
│       └── SpringRunnerEventPublisher.java
│
├── activity/                            # Activity 모듈 (다른 도메인)
│   ├── Activity.java
│   ├── activity/
│   │   └── RecordActivityActivity.java
│   └── internal/
│       └── ActivityService.java
│
└── notification/                        # Notification 모듈
    ├── NotificationService.java         # Facade
    └── internal/
        └── EmailNotificationAdapter.java
```

### 4.2 Spring Modulith 모듈 경계

```java
// ModularityTests.java
@Test
void verifyModularity() {
    ApplicationModules modules = ApplicationModules.of(ModulithApplication.class);

    // 검증: internal 패키지 외부 접근 금지
    modules.verify();

    // 출력: 모듈 구조 확인
    modules.forEach(System.out::println);
}
```

**검증 규칙**:
- `runner.internal` → 외부 모듈에서 접근 불가
- `runner.activity` → 외부 모듈에서 접근 가능 (공개 API)
- `runner.port` → 외부 모듈에서 접근 가능

---

## 5. 테스트 전략

### 5.1 Activity 단위 테스트 (필수)

```java
@ExtendWith(MockitoExtension.class)
class RegisterRunnerActivityTest {

    @Mock
    private RunnerRepository runnerRepository;

    @Mock
    private RunnerEventPublisher eventPublisher;

    @InjectMocks
    private RunnerService registerActivity;  // Activity 구현체

    @Test
    void 러너_등록_성공() {
        // Given
        RegisterRunnerCommand command = new RegisterRunnerCommand("홍길동", "hong@test.com");

        when(runnerRepository.existsByEmail("hong@test.com")).thenReturn(false);
        when(runnerRepository.save(any(Runner.class)))
            .thenAnswer(invocation -> {
                Runner runner = invocation.getArgument(0);
                ReflectionTestUtils.setField(runner, "id", 1L);
                return runner;
            });

        // When
        RegisterResult result = registerActivity.register(command);

        // Then
        assertThat(result).isInstanceOf(RegisterResult.Success.class);
        RegisterResult.Success success = (RegisterResult.Success) result;
        assertThat(success.runnerId()).isEqualTo(1L);
        assertThat(success.name()).isEqualTo("홍길동");

        // 이벤트 발행 검증
        verify(eventPublisher).publishRegistered(any(RunnerRegisteredEvent.class));
    }

    @Test
    void 러너_등록_실패_중복_이메일() {
        // Given
        RegisterRunnerCommand command = new RegisterRunnerCommand("홍길동", "existing@test.com");
        when(runnerRepository.existsByEmail("existing@test.com")).thenReturn(true);

        // When
        RegisterResult result = registerActivity.register(command);

        // Then
        assertThat(result).isInstanceOf(RegisterResult.Failure.class);
        RegisterResult.Failure failure = (RegisterResult.Failure) result;
        assertThat(failure.type()).isEqualTo(RegisterResult.Failure.FailureType.DUPLICATE_EMAIL);

        // 저장 호출 안 됨
        verify(runnerRepository, never()).save(any());
    }
}
```

### 5.2 비즈니스 플로우 테스트

```java
class RunnerBusinessFlowTest {

    @Test
    void 러너_등록부터_레벨업까지_전체_플로우() {
        // 1. 등록 Activity
        RegisterResult registerResult = registerActivity.register(
            new RegisterRunnerCommand("김철수", "kim@test.com")
        );
        assertThat(registerResult).isInstanceOf(RegisterResult.Success.class);
        Long runnerId = ((RegisterResult.Success) registerResult).runnerId();

        // 2. 조회 Activity
        Optional<RunnerInfo> found = searchActivity.findById(runnerId);
        assertThat(found).isPresent();
        assertThat(found.get().level()).isEqualTo(RunnerLevel.BEGINNER);

        // 3. 레벨 승급 Activity
        LevelChangeResult levelResult = levelActivity.promote(runnerId);
        assertThat(levelResult.newLevel()).isEqualTo(RunnerLevel.INTERMEDIATE);

        // 4. 변경 확인
        RunnerInfo updated = searchActivity.findById(runnerId).orElseThrow();
        assertThat(updated.level()).isEqualTo(RunnerLevel.INTERMEDIATE);
    }
}
```

### 5.3 Spring Modulith Scenario 테스트

```java
@ApplicationModuleTest
class RunnerModuleIntegrationTest {

    @Autowired
    private RegisterRunnerActivity registerActivity;

    @Autowired
    private Scenario scenario;

    @Test
    void 러너_등록_시_이벤트_발행_확인() {
        // Given
        RegisterRunnerCommand command = new RegisterRunnerCommand("테스트러너", "test@runner.com");

        // When & Then
        scenario.stimulate(() -> registerActivity.register(command))
            .andWaitForEventOfType(RunnerRegisteredEvent.class)
            .matching(event -> event.email().equals("test@runner.com"))
            .toArriveAndVerify(event -> {
                assertThat(event.runnerId()).isNotNull();
            });
    }
}
```

---

## 6. 설계 문서와 코드의 매핑

### 6.1 Activity Diagram → Activity Interface

```
[Activity Diagram: 러너 등록]

┌─────────────────────────────────────┐
│          <<start>>                  │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│     이메일 중복 확인                  │  ← isEmailAvailable()
└──────────────┬──────────────────────┘
               ▼
          ◇ 중복?
         /       \
       Yes        No
        │          │
        ▼          ▼
   ┌─────────┐  ┌─────────────────────┐
   │ 실패반환 │  │    러너 생성         │  ← Runner.create()
   └─────────┘  └──────────┬──────────┘
                           ▼
               ┌─────────────────────┐
               │    저장             │  ← runnerRepository.save()
               └──────────┬──────────┘
                          ▼
               ┌─────────────────────┐
               │  등록 이벤트 발행    │  ← eventPublisher.publishRegistered()
               └──────────┬──────────┘
                          ▼
               ┌─────────────────────┐
               │      <<end>>        │
               └─────────────────────┘
```

### 6.2 Sequence Diagram → Method Flow

```
Controller              Activity              Repository          EventPublisher
    │                       │                      │                    │
    │  register(command)    │                      │                    │
    │──────────────────────>│                      │                    │
    │                       │                      │                    │
    │                       │  existsByEmail()     │                    │
    │                       │─────────────────────>│                    │
    │                       │<─────────────────────│                    │
    │                       │                      │                    │
    │                       │  save(runner)        │                    │
    │                       │─────────────────────>│                    │
    │                       │<─────────────────────│                    │
    │                       │                      │                    │
    │                       │  publishRegistered() │                    │
    │                       │────────────────────────────────────────>│
    │                       │                      │                    │
    │  RegisterResult       │                      │                    │
    │<──────────────────────│                      │                    │
```

---

## 7. 핵심 정리

### 7.1 Activity Interface의 가치

| 문제 | 해결책 |
|------|--------|
| Service 인터페이스의 불명확한 역할 | Activity Interface로 비즈니스 활동 명시 |
| 설계 문서와 코드 불일치 | 1:1 매핑으로 추적 가능 |
| CRUD로 사라지는 비즈니스 플로우 | Activity/Action 계층으로 보존 |
| 테스트 어려움 | Port 추상화로 단위 테스트 용이 |

### 7.2 적용 가이드라인

1. **UseCase 하나 = Activity Interface 하나**
2. **Activity 내 각 단계 = Action (메서드)**
3. **외부 의존성 = Outbound Port로 추상화**
4. **결과 반환 = Sealed Interface (Success/Failure)**
5. **도메인 간 통신 = Event 기반**

### 7.3 Spring Modulith와의 통합

```
Spring Modulith의 internal 패키지 규칙
    + Activity Interface 패턴
    + Event 기반 모듈 간 통신
    ─────────────────────────────
    = 소리치는 아키텍처 (Screaming Architecture)
```

---

## 참고 자료

- [Clean Architecture with Spring Boot | Baeldung](https://www.baeldung.com/spring-boot-clean-architecture)
- [Hexagonal Architecture in Java | HappyCoders](https://www.happycoders.eu/software-craftsmanship/hexagonal-architecture-java/)
- [Ports & Adapters Architecture | Medium](https://medium.com/idealo-tech-blog/hexagonal-ports-adapters-architecture-e3617bcf00a0)
- [Hexagonal Architecture - Ports and Adapters | Hexagonal Me](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html)
- [GitHub - Clean Architecture Example](https://github.com/link-intersystems/clean-architecture-example)
