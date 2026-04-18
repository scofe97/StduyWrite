# Coherence & GraalVM 기술 조사

마이크로서비스를 위한 분산 데이터 그리드와 네이티브 이미지 컴파일 기술 조사

---

## 1. Oracle Coherence

### 1.1 개요

**Oracle Coherence**는 분산 인메모리 데이터 그리드(IMDG) 기술로, 여러 서버의 메모리를 하나의 거대한 캐시/데이터 저장소처럼 사용하게 해주는 솔루션이다.

> **한 줄 요약**: 여러 서버에 흩어진 데이터를 마치 하나의 `Map`처럼 쓸 수 있게 해주는 분산 캐시

**공식 사이트**: https://coherence.community/

### 1.2 해결하는 문제

| 문제 | Coherence 해결책 |
|------|------------------|
| **DB 병목** | 자주 쓰는 데이터를 메모리에 캐싱 → DB 부하 감소 |
| **서버 간 데이터 공유** | 여러 서버가 동일한 분산 캐시 접근 |
| **단일 서버 메모리 한계** | 100개 서버 메모리를 합쳐서 사용 |
| **장애 대응** | 자동 데이터 복제로 서버 죽어도 데이터 유지 |

### 1.3 핵심 기능

```
┌─────────────────────────────────────────────────┐
│              Coherence Cluster                  │
├─────────┬─────────┬─────────┬─────────┬────────┤
│ Server1 │ Server2 │ Server3 │ Server4 │ ...    │
│ (JVM)   │ (JVM)   │ (JVM)   │ (JVM)   │        │
├─────────┴─────────┴─────────┴─────────┴────────┤
│  데이터 자동 분산 + 복제 (샤딩 + 백업)           │
└─────────────────────────────────────────────────┘
```

1. **자동 샤딩**: 데이터를 여러 노드에 자동 분배
2. **자동 복제**: 각 데이터의 백업 복사본 유지
3. **Near Cache**: 자주 쓰는 데이터는 로컬에 캐싱
4. **Entry Processor**: 데이터가 있는 곳에서 직접 처리 (네트워크 왕복 감소)

### 1.4 사용 예시 (Java)

```java
// 일반 Map처럼 사용하지만, 실제로는 분산 저장
NamedMap<String, User> users = session.getMap("users");

users.put("user123", new User("홍길동"));  // 클러스터에 분산 저장
User user = users.get("user123");          // 어느 서버에 있든 가져옴
```

### 1.5 Redis와 비교

| 항목 | Coherence | Redis |
|------|-----------|-------|
| 언어 | Java (JVM) | C |
| 데이터 모델 | 객체 그대로 저장 | 문자열/구조체 |
| 쿼리 | 객체 속성으로 검색 가능 | 제한적 |
| 클러스터링 | 내장 (자동 샤딩) | Redis Cluster 별도 구성 |
| 라이선스 | CE는 무료, EE는 유료 | BSD (무료) |

### 1.6 적합한 사용 사례

- **대규모 트래픽** 시스템 (금융, 통신, 이커머스)
- **세션 클러스터링** (여러 WAS 간 세션 공유)
- **실시간 데이터 처리** (이벤트 스트리밍)
- **DB 앞단 캐시** (Redis와 비슷한 역할, 단 JVM 생태계)

---

## 2. Coherence Spring Sock Shop 예제

### 2.1 프로젝트 개요

온라인 양말 쇼핑몰을 마이크로서비스로 구현한 데모 프로젝트

- **저장소**: https://github.com/oracle/coherence-spring-sockshop-sample
- **상태**: 2025년 9월 아카이브 (읽기 전용)

### 2.2 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (UI)                            │
│                    (Weaveworks 원본 사용)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/REST
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Catalog    │    │    Carts     │    │    Orders    │
│   :7001      │    │    :7001     │    │    :7001     │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ Spring Boot  │    │ Spring Boot  │    │ Spring Boot  │
│ + Coherence  │    │ + Coherence  │    │ + Coherence  │
│   (임베디드)  │    │   (임베디드)  │    │   (임베디드)  │
└──────────────┘    └──────────────┘    └──────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Payment    │    │   Shipping   │    │    Users     │
│   :7001      │    │    :7001     │    │    :7001     │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ Spring Boot  │    │ Spring Boot  │    │ Spring Boot  │
│ + Coherence  │    │ + Coherence  │    │ + Coherence  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### 2.3 6개 마이크로서비스

| 서비스 | 역할 | 주요 API |
|--------|------|----------|
| **Catalog** | 상품 목록/검색 | `GET /catalogue`, `GET /catalogue/{id}` |
| **Carts** | 장바구니 관리 | `GET /carts/{customerId}`, `POST /carts/{id}/items` |
| **Orders** | 주문 처리 | `POST /orders`, `GET /orders/{id}` |
| **Payment** | 결제 처리 | `POST /payments` |
| **Shipping** | 배송 관리 | `POST /shipping`, `GET /shipping/{id}` |
| **Users** | 회원/인증 | `POST /login`, `GET /customers/{id}` |

### 2.4 Coherence 임베디드 모드

```
┌─────────────────────────────────────┐
│         Spring Boot App             │
│  ┌───────────────────────────────┐  │
│  │      Business Logic           │  │
│  │   (Controller, Service)       │  │
│  └───────────────┬───────────────┘  │
│                  │                  │
│  ┌───────────────▼───────────────┐  │
│  │    Coherence (임베디드)        │  │  ← DB 대신 Coherence가
│  │    - NamedMap (분산 캐시)      │  │    데이터 저장소 역할
│  │    - 자동 클러스터링           │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**핵심**: 별도 DB 서버 없음 - Coherence가 각 서비스에 임베디드되어 데이터 저장소 역할

### 2.5 코드 구조 (Carts 서비스 예시)

```
carts/
├── src/main/java/
│   └── com/oracle/coherence/examples/sockshop/spring/carts/
│       ├── Cart.java                    # 도메인 모델
│       ├── CartController.java          # REST API
│       ├── CartRepository.java          # 저장소 인터페이스
│       └── CoherenceCartRepository.java # Coherence 구현체
├── pom.xml
└── README.md
```

### 2.6 Repository 패턴

```java
// 인터페이스 (추상화)
public interface CartRepository {
    Cart getCart(String customerId);
    void saveCart(Cart cart);
    void deleteCart(String customerId);
}

// Coherence 구현체
@Repository
public class CoherenceCartRepository implements CartRepository {

    @Inject
    private NamedMap<String, Cart> carts;  // ← Coherence 분산 Map

    @Override
    public Cart getCart(String customerId) {
        return carts.get(customerId);  // 클러스터 어디서든 조회
    }

    @Override
    public void saveCart(Cart cart) {
        carts.put(cart.getCustomerId(), cart);  // 자동 분산 저장
    }
}
```

### 2.7 기존 마이크로서비스와 차이점

| 구분 | 일반적인 구성 | Sock Shop (Coherence) |
|------|--------------|----------------------|
| **데이터 저장** | 각 서비스별 DB (MySQL, MongoDB 등) | Coherence 임베디드 |
| **DB 운영** | DB 서버 별도 관리 필요 | 애플리케이션과 함께 배포 |
| **확장 시** | DB 확장 별도 고려 | Pod 늘리면 자동 확장 |
| **데이터 복제** | DB 레플리케이션 설정 | Coherence 자동 처리 |

---

## 3. GraalVM

### 3.1 개요

**GraalVM**은 Oracle이 만든 고성능 JDK로, Java 애플리케이션을 **네이티브 실행 파일**로 컴파일할 수 있는 기술이다.

**공식 사이트**: https://www.graalvm.org/

### 3.2 핵심 개념: Native Image

```
┌─────────────────────────────────────────────────────────────────┐
│                    기존 Java 실행 방식                           │
├─────────────────────────────────────────────────────────────────┤
│  .java → .class → JVM 위에서 실행 (JIT 컴파일)                   │
│                                                                 │
│  [Java App] ──► [JVM] ──► [OS]                                 │
│                  ↑                                              │
│            무거움, 시작 느림                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  GraalVM Native Image 방식                       │
├─────────────────────────────────────────────────────────────────┤
│  .java → 네이티브 바이너리 (AOT 컴파일)                           │
│                                                                 │
│  [Native Binary] ──► [OS]     ← JVM 없이 직접 실행!             │
│        ↑                                                        │
│   가볍고, 즉시 시작                                               │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 JVM vs GraalVM Native 비교

| 항목 | 일반 JVM | GraalVM Native |
|------|----------|----------------|
| **시작 시간** | 수 초 ~ 수십 초 | **밀리초 단위** |
| **메모리 사용** | 수백 MB | **수십 MB** |
| **이미지 크기** | JRE 포함 ~200MB+ | **~50MB 이하** |
| **Warm-up** | 필요 (JIT) | **불필요 (AOT)** |
| **최대 처리량** | 높음 (JIT 최적화) | 약간 낮음 |

### 3.4 마이크로서비스에서 GraalVM을 쓰는 이유

```
┌─────────────────────────────────────────────────────────────┐
│              Kubernetes 환경에서의 이점                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 빠른 스케일 아웃                                         │
│     ┌─────┐    트래픽 증가     ┌─────┐ ┌─────┐ ┌─────┐     │
│     │ Pod │  ───────────►    │ Pod │ │ Pod │ │ Pod │     │
│     └─────┘    (밀리초 시작)   └─────┘ └─────┘ └─────┘     │
│                                                             │
│  2. 리소스 절약                                              │
│     기존: Pod 1개 = 512MB 메모리                             │
│     Native: Pod 1개 = 64MB 메모리  → 8배 더 많은 Pod 가능    │
│                                                             │
│  3. 컨테이너 이미지 경량화                                    │
│     기존: 300MB+ (JRE 포함)                                  │
│     Native: 50MB (바이너리만)  → 빠른 배포, 적은 저장공간     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.5 컨테이너 이미지 크기 비교

```
┌──────────────────────────────────────────────────────────────┐
│                  Carts Service Container                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   기존 방식:                                                  │
│   ┌────────────────────────────────────────┐                │
│   │  Alpine Linux        (~5MB)            │                │
│   │  + JRE 17            (~200MB)          │                │
│   │  + Spring Boot JAR   (~50MB)           │                │
│   │  + Coherence JAR     (~30MB)           │                │
│   │  ─────────────────────────────         │                │
│   │  Total: ~285MB, 시작: 10-30초          │                │
│   └────────────────────────────────────────┘                │
│                                                              │
│   GraalVM Native 방식:                                       │
│   ┌────────────────────────────────────────┐                │
│   │  Distroless/Static   (~2MB)            │                │
│   │  + Native Binary     (~50MB)           │                │
│   │  ─────────────────────────────         │                │
│   │  Total: ~52MB, 시작: 0.1초             │                │
│   └────────────────────────────────────────┘                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. GraalVM Gradle 설정

### 4.1 기본 설정 (Kotlin DSL)

```kotlin
// build.gradle.kts
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    id("org.graalvm.buildtools.native") version "0.10.0"  // ← GraalVM 플러그인
    kotlin("jvm") version "1.9.21"
}

graalvmNative {
    binaries {
        named("main") {
            imageName.set("my-app")
            mainClass.set("com.example.ApplicationKt")

            buildArgs.add("-O4")                    // 최적화 레벨
            buildArgs.add("--no-fallback")          // JVM fallback 비활성화
            buildArgs.add("--enable-preview")

            // 메모리 설정 (빌드 시)
            buildArgs.add("-J-Xmx8g")
        }
    }

    toolchainDetection.set(false)  // 수동 GraalVM 경로 지정 시
}
```

### 4.2 기본 설정 (Groovy DSL)

```groovy
// build.gradle
plugins {
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
    id 'org.graalvm.buildtools.native' version '0.10.0'
    id 'java'
}

graalvmNative {
    binaries {
        main {
            imageName = 'my-app'
            mainClass = 'com.example.Application'
            buildArgs.add('-O4')
            buildArgs.add('--no-fallback')
        }
    }
}
```

### 4.3 빌드 명령어

```bash
# Native 이미지 빌드
./gradlew nativeCompile

# Native 이미지 실행
./gradlew nativeRun

# Native 테스트 실행
./gradlew nativeTest

# 컨테이너 이미지 빌드 (Buildpacks)
./gradlew bootBuildImage
```

### 4.4 실무용 전체 설정

```kotlin
// build.gradle.kts
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    id("org.graalvm.buildtools.native") version "0.10.0"
    kotlin("jvm") version "1.9.21"
    kotlin("plugin.spring") version "1.9.21"
    kotlin("plugin.jpa") version "1.9.21"
}

graalvmNative {
    binaries {
        named("main") {
            imageName.set("${project.name}")

            // 최적화
            buildArgs.add("-O4")
            buildArgs.add("--no-fallback")
            buildArgs.add("--install-exit-handlers")

            // 빌드 시 메모리
            buildArgs.add("-J-Xmx12g")

            // 디버깅 정보 (운영에서는 제거)
            if (project.hasProperty("debugNative")) {
                buildArgs.add("-g")
                buildArgs.add("-H:+SourceLevelDebug")
            }

            // 빌드 리포트
            buildArgs.add("-H:+BuildReport")
        }

        named("test") {
            buildArgs.add("-O0")  // 테스트는 빠른 빌드
        }
    }

    // Spring AOT 설정
    metadataRepository {
        enabled.set(true)
    }
}

// Native 빌드 전 AOT 처리
tasks.named("nativeCompile") {
    dependsOn("processAot")
}
```

---

## 5. GraalVM 실무 도입 시 문제점

### 5.1 Reflection 문제 (가장 흔함)

```java
// 이런 코드는 Native에서 실패
Class<?> clazz = Class.forName("com.example.MyClass");
Object obj = clazz.getDeclaredConstructor().newInstance();
```

**증상:**
```
Error: Class com.example.MyClass not found
```

**해결책 - reflect-config.json:**
```json
// src/main/resources/META-INF/native-image/reflect-config.json
[
  {
    "name": "com.example.MyClass",
    "allDeclaredConstructors": true,
    "allDeclaredMethods": true,
    "allDeclaredFields": true
  },
  {
    "name": "com.example.dto.UserDto",
    "allDeclaredConstructors": true,
    "allDeclaredMethods": true
  }
]
```

### 5.2 동적 프록시 문제 (JPA, MyBatis 등)

```java
// Spring AOP, JPA Repository 등에서 사용
@Transactional  // ← 프록시 기반
public void saveUser() { }
```

**해결책 - proxy-config.json:**
```json
// src/main/resources/META-INF/native-image/proxy-config.json
[
  {
    "interfaces": [
      "com.example.repository.UserRepository",
      "org.springframework.data.repository.CrudRepository"
    ]
  }
]
```

### 5.3 리소스 파일 누락

```java
// 런타임에 리소스 읽기
InputStream is = getClass().getResourceAsStream("/templates/email.html");
// Native에서는 null 반환!
```

**해결책 - resource-config.json:**
```json
{
  "resources": {
    "includes": [
      {"pattern": "templates/.*"},
      {"pattern": "static/.*"},
      {"pattern": ".*\\.properties$"},
      {"pattern": ".*\\.xml$"}
    ]
  }
}
```

### 5.4 라이브러리 호환성 매트릭스

| 라이브러리 | Native 지원 | 문제점 |
|------------|-------------|--------|
| **Spring Boot 3.x** | ✅ 좋음 | 대부분 동작 |
| **Spring Data JPA** | ⚠️ 주의 | Hibernate 설정 필요 |
| **MyBatis** | ⚠️ 주의 | XML 매퍼 설정 필요 |
| **Lombok** | ⚠️ 주의 | 컴파일 타임이라 대부분 OK |
| **Jackson** | ⚠️ 주의 | DTO reflection 설정 필요 |
| **Logback** | ✅ 좋음 | 기본 지원 |
| **AWS SDK v2** | ⚠️ 주의 | 일부 서비스만 지원 |
| **gRPC** | ❌ 어려움 | 복잡한 설정 필요 |
| **Netty** | ⚠️ 주의 | native transport 설정 |
| **Kafka Client** | ⚠️ 주의 | 추가 설정 필요 |

### 5.5 빌드 시간 문제

```
┌─────────────────────────────────────────────────────────┐
│                    빌드 시간 비교                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  일반 JAR 빌드:     30초 ~ 1분                          │
│  Native 빌드:       5분 ~ 15분+ (프로젝트 규모에 따라)    │
│                                                         │
│  빌드 메모리:       8GB ~ 16GB RAM 필요                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 6. GraalVM 호환성 체크 자동화

### 6.1 Tracing Agent 사용

```bash
# 1. Agent로 실행하여 필요한 설정 자동 수집
java -agentlib:native-image-agent=config-output-dir=src/main/resources/META-INF/native-image \
     -jar build/libs/my-app.jar

# 2. 애플리케이션의 모든 기능 실행 (테스트, API 호출 등)

# 3. 생성된 설정 파일 확인
ls src/main/resources/META-INF/native-image/
# reflect-config.json
# proxy-config.json
# resource-config.json
# serialization-config.json
```

### 6.2 Gradle 태스크로 자동화

```kotlin
// build.gradle.kts
tasks.register<JavaExec>("runWithAgent") {
    classpath = sourceSets["main"].runtimeClasspath
    mainClass.set("com.example.ApplicationKt")
    jvmArgs = listOf(
        "-agentlib:native-image-agent=config-merge-dir=src/main/resources/META-INF/native-image"
    )
}
```

---

## 7. 실무 도입 가이드

### 7.1 단계별 접근법

```
┌─────────────────────────────────────────────────────────────┐
│                  GraalVM 도입 단계                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: 평가 (1-2주)                                      │
│  ├─ 의존성 호환성 체크                                       │
│  ├─ 샘플 프로젝트로 테스트                                   │
│  └─ 빌드 시간/리소스 측정                                    │
│                                                             │
│  Phase 2: 파일럿 (2-4주)                                    │
│  ├─ 간단한 서비스 1개 선정                                   │
│  ├─ Native 빌드 파이프라인 구축                              │
│  └─ 스테이징 환경 배포/테스트                                │
│                                                             │
│  Phase 3: 확대 (점진적)                                     │
│  ├─ 성공한 패턴 문서화                                       │
│  ├─ 다른 서비스로 확대                                       │
│  └─ 모니터링/운영 체계 구축                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 도입하면 안 되는 경우

| 상황 | 이유 |
|------|------|
| **레거시 라이브러리 다수** | Reflection 설정 지옥 |
| **동적 클래스 로딩 필수** | 플러그인 시스템 등 |
| **빠른 개발 사이클 필요** | 빌드 시간 5-15분 |
| **팀 Native 경험 없음** | 디버깅/문제 해결 어려움 |
| **처리량이 시작 시간보다 중요** | JIT가 장기적으로 더 빠름 |

### 7.3 도입하면 좋은 경우

| 상황 | 이점 |
|------|------|
| **Serverless/Lambda** | Cold start 밀리초 |
| **CLI 도구** | 즉시 실행, 배포 간편 |
| **대규모 K8s 클러스터** | 메모리 비용 절감 |
| **빈번한 스케일링** | 빠른 Pod 시작 |
| **신규 프로젝트** | 처음부터 호환성 고려 |

---

## 8. Coherence + GraalVM 조합

### 8.1 왜 이 조합인가?

```
┌─────────────────────────────────────────────────────────────┐
│                    왜 이 조합인가?                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Coherence: 분산 데이터 저장 → DB 서버 제거                  │
│  GraalVM:   경량 실행 환경 → JVM 오버헤드 제거               │
│                                                             │
│  결과:                                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  완전 Self-Contained 마이크로서비스                   │   │
│  │  - 외부 DB 의존 없음                                 │   │
│  │  - JVM 없이 직접 실행                                │   │
│  │  - 밀리초 시작, 최소 메모리                          │   │
│  │  - 무한 수평 확장 가능                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 기술별 역할 정리

| 기술 | 역할 |
|------|------|
| **Coherence** | 데이터를 어디에 저장할지 (분산 캐시) |
| **GraalVM** | 애플리케이션을 어떻게 실행할지 (네이티브 바이너리) |

**함께 쓰면**: DB 없이, JVM 없이, 경량 컨테이너로 무한 확장 가능한 마이크로서비스 구현

---

## 9. 요약

### 9.1 GraalVM Native 실무 도입 판단

```
┌─────────────────────────────────────────────────────────────┐
│              GraalVM Native 실무 도입 판단                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ 적합:                                                    │
│     - 신규 프로젝트 + Spring Boot 3.x                        │
│     - Serverless, 빈번한 스케일링 환경                       │
│     - CLI 도구, 유틸리티                                     │
│                                                             │
│  ⚠️ 주의:                                                    │
│     - 모든 라이브러리 호환성 사전 검증 필수                   │
│     - Tracing Agent로 설정 자동화                            │
│     - CI/CD 빌드 시간/리소스 고려                            │
│                                                             │
│  ❌ 피해야:                                                   │
│     - 레거시 + 복잡한 Reflection 사용                        │
│     - 개발 속도가 최우선인 경우                              │
│     - 팀에 트러블슈팅 경험 없는 경우                         │
│                                                             │
│  💡 권장:                                                    │
│     - 작은 서비스 1개로 파일럿 먼저                          │
│     - 성공 패턴 축적 후 점진적 확대                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 참고 자료

- [Coherence Community](https://coherence.community/)
- [GraalVM 공식 사이트](https://www.graalvm.org/)
- [Coherence Spring Sock Shop](https://github.com/oracle/coherence-spring-sockshop-sample)
- [Spring Boot Native Image Support](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
- [GraalVM Native Build Tools](https://graalvm.github.io/native-build-tools/latest/index.html)
