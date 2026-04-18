# Spring Modulith 실습 과제

> 코드는 직접 작성하세요. 각 과제 완료 후 체크박스를 표시하세요.

---

## 사전 준비

### 1. 의존성 추가

`build.gradle`에 Spring Modulith 의존성을 추가하세요.

**힌트**: README.md의 "의존성 설정" 섹션 참고

- [ ] spring-modulith-starter-core 추가
- [ ] spring-modulith-starter-test 추가
- [ ] BOM 설정

---

## Phase 1: 기본 모듈 구조

### 과제 1-1: 모듈 패키지 생성

다음 구조로 패키지를 생성하세요:

```
com.runnershigh.poc/
├── runner/
│   └── internal/
├── activity/
│   └── internal/
└── PocApplication.java
```

**체크리스트**:
- [ ] runner 패키지 생성
- [ ] runner/internal 패키지 생성
- [ ] activity 패키지 생성
- [ ] activity/internal 패키지 생성

---

### 과제 1-2: Runner 모듈 - 도메인 모델

Runner 모듈의 도메인 모델을 만드세요.

**요구사항**:
- `Runner` 엔티티 (id, name, email, level)
- level은 enum: `BEGINNER`, `INTERMEDIATE`, `ADVANCED`
- 모듈 루트에 배치 (외부 공개)

**체크리스트**:
- [ ] RunnerLevel enum 생성
- [ ] Runner 엔티티 생성 (모듈 루트)

---

### 과제 1-3: Runner 모듈 - Internal 구성요소

Runner 모듈의 internal 구성요소를 만드세요.

**요구사항**:
- `RunnerRepository` - Spring Data JPA Repository
- `RunnerValidator` - 이메일 중복 검증 로직

**체크리스트**:
- [ ] RunnerRepository 생성 (internal)
- [ ] RunnerValidator 생성 (internal)

---

## Phase 2: Activity 패턴 구현

### 과제 2-1: Facade 서비스 생성

외부에 공개되는 `RunnerService`를 만드세요.

**요구사항**:
- 모듈 루트에 배치
- 메서드: `register()`, `findById()`, `updateLevel()`
- 실제 로직은 Activity에 위임 (아직 구현 X)

**체크리스트**:
- [ ] RunnerService 생성 (모듈 루트)
- [ ] 3개 메서드 시그니처 정의

---

### 과제 2-2: Activity 구현

각 유스케이스별 Activity를 구현하세요.

**요구사항**:

| Activity | 역할 |
|----------|------|
| `RegisterRunnerActivity` | 러너 등록 (검증 → 저장 → 이벤트 발행) |
| `UpdateRunnerLevelActivity` | 레벨 업데이트 (조회 → 검증 → 수정) |

**체크리스트**:
- [ ] RegisterRunnerActivity 생성 (internal)
- [ ] UpdateRunnerLevelActivity 생성 (internal)
- [ ] RunnerService에서 Activity 호출하도록 연결

---

### 과제 2-3: 이벤트 정의

모듈 간 통신을 위한 이벤트를 정의하세요.

**요구사항**:
- `RunnerRegistered` 이벤트 (runnerId, registeredAt)
- `RunnerLevelChanged` 이벤트 (runnerId, oldLevel, newLevel)
- 모듈 루트에 배치 (다른 모듈에서 구독 가능)

**체크리스트**:
- [ ] RunnerRegistered 이벤트 생성
- [ ] RunnerLevelChanged 이벤트 생성
- [ ] Activity에서 이벤트 발행 코드 추가

---

## Phase 3: Activity 모듈

### 과제 3-1: Activity 모듈 구조

Activity(운동 기록) 모듈을 구성하세요.

```
activity/
├── Activity.java              # 도메인
├── ActivityService.java       # Facade
├── ActivityRecorded.java      # 이벤트
└── internal/
    ├── ActivityRepository.java
    └── RecordActivityActivity.java  # 운동 기록 Activity
```

**체크리스트**:
- [ ] Activity 도메인 생성 (runnerId, type, distance, duration, recordedAt)
- [ ] ActivityService Facade 생성
- [ ] RecordActivityActivity 생성
- [ ] ActivityRecorded 이벤트 생성

---

### 과제 3-2: 이벤트 핸들러

Activity 모듈에서 Runner 모듈의 이벤트를 구독하세요.

**시나리오**:
- 러너가 등록되면 → 환영 알림 로그 출력
- (실제 알림 기능은 미구현, 로그만)

**체크리스트**:
- [ ] RunnerEventHandler 생성 (internal)
- [ ] @ApplicationModuleListener로 RunnerRegistered 구독
- [ ] 로그 출력 확인

---

## Phase 4: 검증

### 과제 4-1: 모듈 구조 테스트

아키텍처 검증 테스트를 작성하세요.

```java
@Test
void 모듈_구조_검증() {
    // TODO: ApplicationModules.of().verify() 호출
}
```

**체크리스트**:
- [ ] ModularityTests 클래스 생성
- [ ] verify() 테스트 작성
- [ ] 테스트 통과 확인

---

### 과제 4-2: 의도적 위반 테스트

internal 패키지 규칙을 의도적으로 위반해보세요.

**실험**:
1. ActivityService에서 `runner.internal.RunnerRepository` 직접 참조
2. 테스트 실행 → 실패 확인
3. 코드 롤백

**체크리스트**:
- [ ] 의도적 위반 코드 작성
- [ ] verify() 실패 메시지 확인
- [ ] 위반 코드 제거

---

## Phase 5: 문서화

### 과제 5-1: 모듈 문서 생성

Spring Modulith의 자동 문서화 기능을 사용하세요.

```java
@Test
void 모듈_문서_생성() {
    ApplicationModules modules = ApplicationModules.of(Application.class);
    new Documenter(modules).writeDocumentation();
}
```

**체크리스트**:
- [ ] 문서 생성 테스트 작성
- [ ] 생성된 문서 확인 (build/spring-modulith-docs/)
- [ ] 모듈 다이어그램 확인

---

## 최종 구조 확인

완료 후 다음 구조가 되어야 합니다:

```
com.runnershigh.poc/
│
├── runner/
│   ├── Runner.java
│   ├── RunnerLevel.java
│   ├── RunnerService.java
│   ├── RunnerRegistered.java
│   ├── RunnerLevelChanged.java
│   └── internal/
│       ├── RunnerRepository.java
│       ├── RunnerValidator.java
│       ├── RegisterRunnerActivity.java
│       └── UpdateRunnerLevelActivity.java
│
├── activity/
│   ├── Activity.java
│   ├── ActivityService.java
│   ├── ActivityRecorded.java
│   └── internal/
│       ├── ActivityRepository.java
│       ├── RecordActivityActivity.java
│       └── RunnerEventHandler.java
│
└── PocApplication.java
```

---

## 셀프 체크

모든 과제 완료 후 다음을 확인하세요:

| 항목 | 확인 |
|------|------|
| 모든 테스트 통과 | ☐ |
| internal 패키지 규칙 준수 | ☐ |
| 이벤트 발행/구독 동작 확인 | ☐ |
| Facade → Activity 위임 구조 | ☐ |
| 순환 의존성 없음 | ☐ |

---

## Phase 6: 고급 패턴 (코딩하는오후 영상 참고)

> 참고: `docs/참고 자료/코딩하는오후-spring-modulith-리팩토링.md`

### 과제 6-1: Response Sealed Interface

컨트롤러 응답을 통일된 구조로 감싸세요.

**요구사항**:

```java
// Sealed Interface로 Success/Fail만 허용
public sealed interface Response<T> permits Success, Fail {}
public record Success<T>(T data) implements Response<T> {}
public record Fail<T>(String message, T error) implements Response<T> {}
```

**체크리스트**:
- [ ] Response sealed interface 생성
- [ ] Success record 생성
- [ ] Fail record 생성
- [ ] ResponseBodyAdvice 구현 (DefaultResponseHandler)

---

### 과제 6-2: @EnableAsync 설정

비동기 이벤트 처리를 위한 설정을 추가하세요.

**요구사항**:
- `@ApplicationModuleListener`는 내부적으로 `@Async` 포함
- ThreadPoolTaskExecutor 빈 등록 필요 (슬라이스 테스트용)

**체크리스트**:
- [ ] AsyncConfig 클래스 생성
- [ ] @EnableAsync 적용
- [ ] TaskExecutor 빈 등록

---

### 과제 6-3: Scenario API 테스트

비동기 이벤트 테스트를 작성하세요.

**요구사항**:
- `@ApplicationModuleTest` 사용
- `Scenario` API로 이벤트 발행/수신 테스트

```java
@ApplicationModuleTest
class EventTest {
    @Test
    void asyncEventTest(Scenario scenario) {
        scenario.stimulate(() -> /* 이벤트 발행 */)
                .andWaitForEventOfType(RunnerRegistered.class)
                .toArriveAndVerify(event -> /* 검증 */);
    }
}
```

**체크리스트**:
- [ ] @ApplicationModuleTest 적용
- [ ] Scenario 파라미터 주입
- [ ] stimulate() → andWaitForEventOfType() → toArriveAndVerify() 체인
- [ ] 비동기 이벤트 테스트 통과

---

### 과제 6-4: EventPublicationRegistry 스키마

이벤트 트랜잭션 관리를 위한 테이블을 추가하세요.

**요구사항**:
- `event_publication` 테이블 생성
- Spring Modulith 소스에서 스키마 확인 가능

```sql
CREATE TABLE event_publication (
    id UUID PRIMARY KEY,
    listener_id VARCHAR(255),
    event_type VARCHAR(255),
    serialized_event TEXT,
    publication_date TIMESTAMP,
    completion_date TIMESTAMP
);
```

**체크리스트**:
- [ ] schema.sql에 event_publication 테이블 추가
- [ ] 또는 application.yml에 자동 생성 설정

```yaml
spring:
  modulith:
    events:
      jdbc:
        schema-initialization:
          enabled: true
```

---

### 과제 6-5: @TempDir 파일 테스트

파일 업로드 테스트에 임시 디렉토리를 활용하세요.

**요구사항**:
- JUnit의 `@TempDir` 사용
- 테스트 종료 후 자동 정리

```java
@Test
void fileUploadTest(@TempDir Path tempDir) {
    Path uploadPath = tempDir.resolve("test-file.txt");
    // 파일 작업...
    // 테스트 종료 시 자동 삭제
}
```

**체크리스트**:
- [ ] @TempDir 파라미터 사용
- [ ] 임시 경로에 파일 생성/업로드 테스트
- [ ] 테스트 후 디렉토리 자동 삭제 확인

---

## 최종 셀프 체크 (전체)

| 항목 | 확인 |
|------|------|
| Phase 1-5 기본 과제 완료 | ☐ |
| Response Sealed Interface | ☐ |
| @EnableAsync + TaskExecutor | ☐ |
| Scenario API 테스트 | ☐ |
| EventPublicationRegistry | ☐ |
| @TempDir 파일 테스트 | ☐ |

---

## 다음 단계

→ **[COMPARISON.md](./COMPARISON.md)** 에서 장단점 분석
→ **[참고 자료](../../../docs/참고%20자료/)** 영상 요약 문서
