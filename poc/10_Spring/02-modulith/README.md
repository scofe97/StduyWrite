# Spring Modulith POC

Spring Modulith + Activity Interface 패턴 학습을 위한 POC 프로젝트

## 핵심 개념

- **Spring Modulith**: 모듈 경계 강제 (internal 패키지)
- **Activity Interface**: 설계 문서와 코드의 1:1 매핑
- **Hexagonal Architecture**: Port & Adapter 패턴
- **Sealed Interface**: 결과 타입 (Success/Failure)

## 프로젝트 구조

```
src/main/java/com/runnershigh/modulith/
├── ModulithApplication.java          # 애플리케이션 진입점
│
└── runner/                           # Runner 모듈
    ├── Runner.java                   # 도메인 엔티티 (public)
    ├── RunnerLevel.java              # Value Object (public)
    ├── RunnerRegisteredEvent.java    # 도메인 이벤트 (public)
    │
    ├── activity/                     # Activity Interface (public)
    │   ├── RegisterRunnerActivity.java   # 등록 Activity
    │   ├── RegisterRunnerCommand.java    # 입력 Command
    │   └── RegisterResult.java           # 결과 (Sealed)
    │
    ├── port/                         # Outbound Port (public)
    │   └── RunnerRepository.java
    │
    └── internal/                     # 구현체 (외부 접근 불가!)
        ├── RunnerService.java            # Activity 구현
        └── InMemoryRunnerRepository.java # Repository 구현
```

## Activity Interface 패턴

```java
// 설계 문서의 Activity Diagram → Activity Interface
public interface RegisterRunnerActivity {
    RegisterResult register(RegisterRunnerCommand command);  // 메인 플로우
    boolean isEmailAvailable(String email);                   // Action
}

// Sealed Interface로 결과 처리
RegisterResult result = activity.register(command);
return switch (result) {
    case Success s -> ResponseEntity.ok(s);
    case Failure f -> ResponseEntity.badRequest().body(f);
};
```

## 실행 방법

```bash
# 빌드
./gradlew build

# 실행
./gradlew bootRun

# 테스트
./gradlew test

# 모듈 구조 검증만
./gradlew test --tests ModularityTests
```

## H2 Console

- URL: http://localhost:8080/h2-console
- JDBC URL: jdbc:h2:mem:testdb
- Username: sa
- Password: (빈칸)

## 테스트 실행

```bash
# 전체 테스트
./gradlew test

# 모듈 구조 검증
./gradlew test --tests ModularityTests

# 도메인 단위 테스트 (빠름, 외부 의존성 없음)
./gradlew test --tests RunnerTest
./gradlew test --tests RunnerLevelTest

# Activity 통합 테스트
./gradlew test --tests RegisterRunnerActivityTest
```

## 학습 자료

### 개념 및 실습
- [usecase-activity-deep-dive.md](docs/usecase-activity-deep-dive.md) - **UseCase/Activity 심층 분석**
- [EXERCISES.md](../spring/docs/spring-modulith/EXERCISES.md) - 실습 과제
- [README.md](../spring/docs/spring-modulith/README.md) - Spring Modulith 개념
- [COMPARISON.md](../spring/docs/spring-modulith/COMPARISON.md) - 아키텍처 비교

### 코딩하는오후 영상 요약 (참고 자료)
- `docs/참고 자료/코딩하는오후-spring-modulith-리팩토링.md` - Response 패턴, @EnableAsync
- `docs/참고 자료/코딩하는오후-internal-service-구현.md` - Activity 패턴, Port
- `docs/참고 자료/코딩하는오후-바이브-모델링-설계.md` - AI 기반 설계
- `docs/참고 자료/코딩하는오후-usecase-액티비티.md` - UseCase → Activity 매핑
