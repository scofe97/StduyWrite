# 빌드 도구: Deep Investigation
> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Gradle이 Maven보다 빠른 구체적 이유는 무엇인가?

### 왜 이 질문이 중요한가
"Gradle이 빠르다"는 말은 많이 들었지만 "왜"를 제대로 설명하지 못하면 팀에서 Maven에서 Gradle로의 전환을 설득할 수 없다. 또한 Gradle 프로젝트에서 빌드가 느리다는 문제가 생겼을 때, 어떤 최적화 옵션을 먼저 확인해야 하는지 알 수 없다. 증분 빌드와 빌드 캐시의 원리를 이해하면 CI/CD 파이프라인 최적화에도 직접 활용할 수 있다.

### 답변

Gradle이 Maven보다 빠른 이유는 세 가지 핵심 메커니즘으로 설명된다.

**메커니즘 1: 증분 빌드(Incremental Build).** Gradle은 각 태스크의 입력(소스 파일, 의존성, 설정값)과 출력(클래스 파일, JAR)의 체크섬을 추적한다. 입력이 변경되지 않았다면 태스크를 재실행하지 않고 `UP-TO-DATE`로 건너뛴다.

```bash
# 첫 번째 빌드
./gradlew compileJava
# > Task :compileJava

# 소스 변경 없이 두 번째 빌드
./gradlew compileJava
# > Task :compileJava UP-TO-DATE  ← 실행 건너뜀

# Maven은 기본적으로 매번 전체 재컴파일
# (maven-compiler-plugin의 useIncrementalCompilation은 제한적)
```

**메커니즘 2: 빌드 캐시(Build Cache).** 증분 빌드가 로컬 변경 감지라면, 빌드 캐시는 **입력의 해시값 기반 결과물 재사용**이다. 같은 입력이라면 다른 머신, 다른 브랜치에서 빌드한 결과도 재사용할 수 있다. CI 환경에서 PR 브랜치가 main 브랜치의 캐시를 재사용하면 빌드 시간이 50~80% 단축될 수 있다.

```bash
# 로컬 빌드 캐시 활성화 (gradle.properties)
org.gradle.caching=true

# 원격 빌드 캐시 (Gradle Enterprise 또는 자체 HTTP 캐시 서버)
# build.gradle.kts
buildCache {
    remote<HttpBuildCache> {
        url = uri("https://cache.example.com/cache/")
        push = System.getenv("CI") != null  // CI에서만 캐시 업로드
    }
}

# 캐시 히트율 확인
./gradlew build --build-cache --info | grep "FROM-CACHE"
```

**메커니즘 3: 병렬 실행과 DAG 기반 태스크 그래프.** Gradle은 태스크 의존성을 DAG(Directed Acyclic Graph)로 표현하고, 의존성이 없는 태스크는 병렬로 실행한다. Maven의 라이프사이클은 선형이라 멀티모듈에서도 순서가 강제된다.

```bash
# 병렬 빌드 활성화
./gradlew build --parallel
# gradle.properties에 영구 설정
org.gradle.parallel=true
org.gradle.workers.max=4  # CPU 코어 수와 동일하게
```

Maven에서 Gradle로 전환 시 주의점: Gradle의 빌드 스크립트(Kotlin DSL/Groovy DSL)는 코드이므로 잘못 작성하면 태스크 캐시 무효화가 과도하게 발생한다. `@Input`, `@Output` 애노테이션을 올바르게 선언하지 않은 커스텀 태스크는 증분 빌드가 작동하지 않는다.

---

## Q2. implementation vs api 의존성 스코프 차이의 실무 영향은?

### 왜 이 질문이 중요한가
멀티모듈 프로젝트에서 `api`와 `implementation`의 차이를 모르면 불필요한 재컴파일이 발생해 빌드가 느려지거나, 반대로 API 유출로 인해 의도하지 않은 의존성 노출이 생긴다. 라이브러리를 개발할 때 이 차이는 API 하위호환성 관리에도 직접 영향을 준다.

### 답변

`implementation`과 `api`의 차이는 **전이적 의존성(transitive dependency) 노출 여부**다.

```
모듈 구조: app → library → guava

library의 build.gradle.kts:
  api("com.google.guava:guava:32.0")        → app도 guava를 사용 가능 (노출)
  implementation("com.google.guava:guava:32.0") → app은 guava 사용 불가 (캡슐화)
```

**`implementation` 사용 시 (권장 기본값)**:

```kotlin
// library/build.gradle.kts
dependencies {
    implementation("com.google.guava:guava:32.0")
}

// library의 내부 구현에서만 guava 사용
// app은 guava 클래스를 직접 참조할 수 없음
// → guava를 다른 라이브러리로 교체해도 app 재컴파일 불필요
```

**`api` 사용 시 (공개 API에 타입이 노출될 때만)**:

```kotlin
// library/build.gradle.kts
dependencies {
    api("com.example:shared-models:1.0")  // library의 public 메서드 반환 타입으로 사용
}

// public ResponseModel getData();  ← ResponseModel이 shared-models의 클래스
// app이 ResponseModel을 받아서 사용해야 하므로 api 필수
```

**빌드 성능 영향**: `implementation`을 사용하면 library의 내부 의존성이 변경돼도 app을 재컴파일하지 않는다. `api`를 사용하면 library 의존성 변경 시 app도 재컴파일이 트리거된다. 대규모 멀티모듈 프로젝트에서 모든 의존성을 `api`로 선언하면 어느 모듈 하나가 바뀌어도 전체 프로젝트가 재컴파일되는 연쇄 반응이 발생한다.

```bash
# 의존성 트리 확인: implementation과 api의 차이 시각화
./gradlew :app:dependencies --configuration compileClasspath

# implementation: library의 guava가 compileClasspath에 미포함
# api: library의 guava가 compileClasspath에 포함
```

**실무 규칙**: 공개 메서드 시그니처(반환 타입, 파라미터 타입)에 사용되는 의존성만 `api`로 선언하고, 나머지는 모두 `implementation`으로 선언한다. 이것이 모듈 경계를 명확히 하고 빌드 시간을 최소화하는 기본 원칙이다.
