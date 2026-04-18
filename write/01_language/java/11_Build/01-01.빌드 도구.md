# 빌드 도구

---

> 빌드 도구는 소스 코드를 실행 가능한 산출물로 만드는 전 과정을 자동화한다. Maven은 선언적 XML 설정과 표준 생명주기로 예측 가능성을 제공하고, Gradle은 태스크 기반 모델과 증분 빌드로 유연성과 성능을 제공한다.

## 1. 빌드 도구의 역할

소스 코드를 작성한 후 실제로 실행하기까지는 여러 단계가 필요하다. 이 과정을 수동으로 처리하면 실수가 생기고, 팀원마다 다른 방식으로 진행하면 일관성이 깨진다. 빌드 도구는 이 모든 과정을 표준화하고 자동화한다.

빌드 도구가 처리하는 주요 작업:

- **컴파일**: `.java` 소스 파일을 `.class` 바이트코드로 변환
- **의존성 관리**: 외부 라이브러리를 중앙 저장소(Maven Central 등)에서 다운로드하고 클래스패스에 추가
- **테스트**: JUnit 등 테스트 프레임워크를 실행하고 결과를 리포트로 생성
- **패키징**: 컴파일된 클래스와 리소스를 JAR 또는 WAR로 묶음
- **배포**: 생성된 산출물을 Nexus, Harbor 같은 아티팩트 저장소에 업로드

## 2. Maven vs Gradle 비교

Maven은 2004년, Gradle은 2007년에 등장했다. 두 도구 모두 의존성 관리와 빌드 자동화를 지원하지만 철학이 다르다.

| 항목 | Maven | Gradle |
|------|-------|--------|
| 설정 방식 | XML (`pom.xml`) | Groovy/Kotlin DSL (`build.gradle`) |
| 빌드 모델 | 선언적 생명주기 | 태스크 기반 DAG |
| 증분 빌드 | 제한적 | 기본 지원 |
| 빌드 캐시 | 없음 | 로컬 + 원격 캐시 |
| 유연성 | 낮음 (컨벤션 우선) | 높음 (커스텀 태스크) |
| 학습 곡선 | 낮음 | 중간 |
| 멀티모듈 | 지원 | 더 강력하게 지원 |

규모가 작고 표준적인 Spring Boot 프로젝트라면 Maven이 충분하다. 복잡한 멀티모듈 프로젝트나 빌드 성능이 중요한 대규모 프로젝트에서는 Gradle이 유리하다.

## 3. Maven: POM 구조와 생명주기

Maven의 모든 설정은 `pom.xml`(Project Object Model)에 담긴다. 프로젝트 정보, 의존성, 플러그인, 빌드 설정이 모두 이 파일 하나에 선언된다.

```xml
<project>
    <modelVersion>4.0.0</modelVersion>

    <!-- 프로젝트 좌표 (groupId:artifactId:version으로 고유 식별) -->
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>

    <dependencies>
        <!-- 런타임 의존성 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>

        <!-- 테스트 전용 의존성 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

Maven의 **빌드 생명주기(Lifecycle)**는 순서가 고정된 단계로 구성된다. 특정 단계를 실행하면 그 이전 모든 단계가 자동으로 실행된다.

| 단계 | 설명 |
|------|------|
| `clean` | `target/` 디렉토리 삭제 |
| `compile` | 소스 코드 컴파일 |
| `test` | 테스트 컴파일 및 실행 |
| `package` | JAR/WAR 생성 |
| `install` | 로컬 저장소(`~/.m2`)에 설치 |
| `deploy` | 원격 저장소에 업로드 |

`mvn package`를 실행하면 `validate → compile → test → package` 순서로 자동 진행된다.

**의존성 스코프**는 의존성이 어느 단계에서 필요한지를 지정한다:

- `compile`: 기본값. 컴파일, 테스트, 런타임 모두에서 사용
- `test`: 테스트 코드에서만 사용 (JUnit, Mockito 등)
- `provided`: 컴파일에는 필요하지만 런타임에는 컨테이너가 제공 (Servlet API 등)
- `runtime`: 컴파일에는 불필요하지만 런타임에 필요 (JDBC 드라이버 등)

## 4. Gradle: 태스크 기반 모델

Gradle은 태스크(Task)를 노드로, 태스크 간 의존성을 엣지로 하는 **DAG(Directed Acyclic Graph)**로 빌드를 모델링한다. `build.gradle.kts`(Kotlin DSL)로 설정한다.

```kotlin
// build.gradle.kts
plugins {
    id("java")
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

dependencies {
    // implementation: 컴파일 + 런타임, 의존 모듈에 노출 안 됨
    implementation("org.springframework.boot:spring-boot-starter-web")

    // api: 의존 모듈에도 노출됨 (라이브러리 모듈에서 사용)
    // api("com.example:shared-lib:1.0.0")

    // compileOnly: 컴파일에만 필요 (Lombok 등)
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")

    // testImplementation: 테스트 코드에서만 사용
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
}
```

### 증분 빌드와 빌드 캐시

Gradle의 가장 중요한 성능 기능은 **증분 빌드(Incremental Build)**와 **빌드 캐시(Build Cache)**다. 증분 빌드는 태스크의 입력(소스 파일, 의존성)과 출력(`.class` 파일)을 추적해, 변경이 없으면 태스크를 다시 실행하지 않는다. `UP-TO-DATE`라는 메시지가 이 상태를 나타낸다.

빌드 캐시는 태스크 출력을 로컬 캐시(`~/.gradle/caches/`)에 저장한다. 같은 입력에 대한 출력이 캐시에 있으면 재실행 없이 캐시에서 가져온다. 원격 캐시를 설정하면 팀 전체가 빌드 결과를 공유할 수 있어, CI 빌드 시간이 크게 줄어든다.

```kotlin
// settings.gradle.kts: 빌드 캐시 활성화
buildCache {
    local {
        isEnabled = true
    }
    remote<HttpBuildCache> {
        url = uri("https://cache.example.com/cache/")
        isEnabled = true
        isPush = true
    }
}
```

## 5. Wrapper: 빌드 도구 버전 고정

**Wrapper**(`mvnw` / `gradlew`)는 빌드 도구 자체를 프로젝트에 포함시켜 버전을 고정하는 메커니즘이다. 팀원이 로컬에 Maven이나 Gradle을 설치하지 않아도 `./gradlew build`만 실행하면 지정된 버전이 자동으로 다운로드된다. CI 서버에서도 동일한 버전이 보장돼 "내 로컬에선 되는데" 문제를 방지한다.

```bash
# Gradle Wrapper 생성 (프로젝트 초기화 시 한 번)
gradle wrapper --gradle-version 8.5

# 이후 모든 빌드는 Wrapper로 실행
./gradlew build          # 전체 빌드
./gradlew test           # 테스트만
./gradlew bootRun        # Spring Boot 실행
./gradlew dependencies   # 의존성 트리 출력

# Maven Wrapper
./mvnw clean package
./mvnw test
```

`gradle/wrapper/gradle-wrapper.properties`에 사용할 Gradle 버전이 기록되며, 이 파일은 반드시 git에 커밋해야 한다. Wrapper 스크립트(`gradlew`, `gradlew.bat`)도 함께 커밋해 모든 환경에서 동일한 빌드를 보장한다.
