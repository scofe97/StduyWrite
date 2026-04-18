---
title: 03-core-messaging-analysis
tags: []
status: draft
related: []
updated: 2026-04-19
---

# core-messaging 후속 조사 분석

---

> Namastack Outbox 라이브러리의 TPS 적용 가능성, starter 분리 필요 여부, Gradle deprecated 경고의 원인과 수정을 정리한다.

## 1. Namastack Outbox 라이브러리 분석

Outbox 패턴은 비즈니스 데이터와 이벤트 레코드를 같은 DB 트랜잭션에 원자적으로 저장하여, 이벤트 유실을 원천 차단하는 기법이다. Namastack Outbox for Spring Boot는 이 패턴을 라이브러리로 제공한다.

### 1-1. 동작 원리

트랜잭션 내에서 `outbox.schedule(event, key)`를 호출하면 outbox 테이블에 PENDING 상태로 INSERT된다. 도메인 데이터 저장과 같은 트랜잭션이므로 둘 다 커밋되거나 둘 다 롤백된다. 백그라운드 폴러가 주기적으로 PENDING 레코드를 조회하고, `payload_type`에 매칭되는 `@OutboxHandler`를 실행한다. 핸들러가 Kafka 전송에 성공하면 COMPLETED로 마킹하고, 실패하면 지수 백오프로 재시도하거나 `@OutboxFallbackHandler`로 위임한다.

이 구조가 단순 Kafka `send()` 후 커밋하는 방식보다 안전한 이유는 분명하다. Kafka 전송이 실패해도 outbox 레코드가 DB에 남아 있으므로, 폴러가 다음 주기에 재시도한다. DB 커밋 후 Kafka 전송 전에 애플리케이션이 죽어도 마찬가지다.

### 1-2. 256 파티션 분산 처리

Namastack의 특징적인 설계는 256개 논리 파티션이다. 레코드의 key를 일관 해싱하여 256개 파티션 중 하나에 배정한다. 같은 key는 항상 같은 파티션에 들어가므로 순서가 보장된다. 예를 들어 `order-123`에 대한 모든 이벤트는 동일 파티션에서 순차 처리된다. 인스턴스를 추가하거나 제거하면 파티션이 자동으로 리밸런싱되고, 장애 시에는 해당 인스턴스의 파티션을 다른 인스턴스가 인계받는다.

### 1-3. JPA 의존성과 MyBatis 호환

Namastack은 두 가지 starter를 제공한다:

- `namastack-outbox-starter-jdbc`: JDBC를 직접 사용하고 스키마를 자동 생성한다. JPA가 필요 없다.
- `namastack-outbox-starter-jpa`: JPA/Hibernate를 사용하고 스키마를 수동으로 관리해야 한다.

TPS는 MyBatis 기반이므로 JDBC starter를 사용하면 된다. Spring의 `PlatformTransactionManager`를 공유하기 때문에, MyBatis 트랜잭션 안에서 `outbox.schedule()`을 호출하면 같은 트랜잭션 컨텍스트에서 동작한다.

### 1-4. 핵심 API

이벤트를 스케줄링하는 방법은 명령형과 선언적 방식 두 가지다:

```java
// 명령형 — 직접 호출
outbox.schedule(payload, key);

// 선언적 — 어노테이션 기반
@OutboxEvent(key = "#this.orderId")
record OrderCreated(String orderId) {}
```

핸들러는 `@OutboxHandler`로 선언하고, 실패 시 `@OutboxFallbackHandler`가 호출된다:

```java
@OutboxHandler
void handle(OrderCreated event) {
    kafkaTemplate.send(Topics.ORDER_CREATED, event.orderId(), serialize(event));
}

@OutboxFallbackHandler
void onFailure(OrderCreated event, OutboxFailureContext ctx) {
    log.error("Outbox 실패: attempts={}, lastError={}", ctx.attempts(), ctx.lastError());
}
```

### 1-5. 버전 호환성 문제

여기서 문제가 발생한다. Namastack 최신 버전(1.1.0)은 Spring Boot 4.0.0 이상을 요구한다. TPS는 Spring Boot 3.4.1을 사용하므로 최신 버전을 적용할 수 없다. 선택지는 세 가지다:

- Namastack 0.3.x에서 Spring Boot 3.x 호환 버전을 탐색한다
- outbox 테이블과 폴러를 직접 구현한다
- Spring Boot 4.x 업그레이드 후 도입한다

Spring Boot 4.x 업그레이드는 TPS 전체에 영향을 주는 대규모 작업이므로 현실적이지 않다. 0.3.x 호환 여부를 먼저 확인하고, 불가능하면 자체 구현이 합리적인 경로일 것이다.

## 2. starter 분리가 필요한가

결론부터 말하면 불필요하다. Spring Boot 공식 문서는 starter와 auto-configuration을 분리하는 시점을 명확히 구분한다.

**분리가 필요한 경우**: 선택적 기능이 여러 개 있어서 소비 모듈이 원하는 조합만 골라 쓸 때, 또는 오픈소스로 배포할 때.

**단일 모듈로 충분한 경우**: 자동 구성이 단순하고, 선택적 기능이 없으며, 내부 라이브러리일 때.

core-messaging은 정확히 후자에 해당한다. `@AutoConfiguration` + `AutoConfiguration.imports` 파일로 자동 등록되고, 선택적 기능은 tracing 하나뿐인데 이것도 `@ConditionalOnClass`로 처리된다. 같은 팀만 사용하는 Nexus 내부 배포 라이브러리이므로, 별도 starter 모듈을 만들면 관리 포인트만 늘어난다.

starter 분리가 필요해지는 시점은 core-messaging이 여러 flavor를 제공하게 될 때다. 예를 들어 web용 설정과 batch용 설정이 분리되어 소비 모듈이 선택해야 한다면, 그때 `core-messaging-autoconfigure` + `core-messaging-starter-web` + `core-messaging-starter-batch`로 분리하면 된다. 현재로서는 과도한 설계다.

Spring Boot 공식 문서의 표현을 빌리면 이렇다:

> "If the auto-configuration is relatively straightforward and has no optional features, merging the two modules into one is definitely an option."

## 3. Gradle deprecated 경고 수정

### 3-1. 경고 원인

`core-messaging/build.gradle`의 `addJacksonAnnotationsToAvro` 태스크가 레거시 방식으로 정의되어 있었다. Gradle 8.x에서 deprecated 경고를 발생시키는 두 가지 패턴이 있었다:

- `task taskName { }` 대신 `tasks.register('taskName') { }`를 사용해야 한다. `task` 키워드는 Configuration 시점에 즉시 태스크를 생성하지만, `tasks.register`는 실제 실행이 필요할 때까지 생성을 지연(lazy)한다. 빌드 성능에 직접적인 영향을 준다.
- `${buildDir}` 대신 `${layout.buildDirectory.get()}`을 사용해야 한다. `buildDir` 프로퍼티는 Gradle 9.0에서 제거될 예정이다.

### 3-2. 이 태스크가 하는 일

Avro 코드 생성기(`generateAvroJava`)가 만드는 클래스에는 `schema`, `specificData`, `classLoader` 같은 Avro 런타임 내부 필드가 포함된다. 이 필드들이 Jackson 직렬화 대상이 되면 두 가지 문제가 발생한다:

- REST API 응답에 Avro 메타데이터가 포함되어 페이로드가 10배 이상 커진다
- `ClassLoader` 같은 필드는 직렬화 자체가 불가능하여 `JsonMappingException`이 발생한다

`@JsonIgnoreProperties` 어노테이션을 생성된 Java 파일에 주입하여 이 필드들을 직렬화에서 제외한다. core-lib에서 이미 동일한 패턴을 사용하고 있다.

### 3-3. 수정 내용

변경은 네 곳이다:

| 항목 | 수정 전 | 수정 후 |
|------|---------|---------|
| 태스크 정의 | `task addJacksonAnnotationsToAvro { }` | `tasks.register('addJacksonAnnotationsToAvro') { }` |
| 빌드 디렉토리 | `${buildDir}` | `${layout.buildDirectory.get()}` |
| 의존성 참조 | `dependsOn generateAvroJava` | `dependsOn 'generateAvroJava'` (문자열) |
| `project` 접근 | `project.rootDir.path` (execution time) | `def rootPath = rootDir.path` (configuration time 캡처) |
| Maven URL | `url 'https://...'` (공백 할당) | `url = 'https://...'` (명시적 할당) |

네 번째와 다섯 번째는 `--warning-mode all`로 확인한 추가 경고다. Gradle 10.0에서 `Task.project` 접근이 execution time에 금지되므로, configuration time에 `rootDir.path`를 로컬 변수로 캡처한다. Maven URL의 공백 할당 구문(`url 'value'`)도 Gradle 10.0에서 제거 예정이므로 `url = 'value'`로 변경한다.

수정 후 코드는 다음과 같다:

```groovy
tasks.register('addJacksonAnnotationsToAvro') {
    dependsOn 'generateAvroJava'
    def rootPath = rootDir.path
    doLast {
        def avroDir = file("${layout.buildDirectory.get()}/generated-main-avro-java/org/okestro/tps/messaging")
        if (avroDir.exists()) {
            avroDir.eachFileRecurse { file ->
                if (file.isFile() && file.name.endsWith('.java')) {
                    def content = file.text
                    if (!content.contains('@com.fasterxml.jackson.annotation.JsonIgnoreProperties')) {
                        def annotation = '@com.fasterxml.jackson.annotation.JsonIgnoreProperties({"schema", "specificData", "classLoader", "conversions", "fastReaderEnabled", "fastReaderBuilder", "customCoders"})'
                        def newContent = content.replaceAll(
                            /@org\.apache\.avro\.specific\.AvroGenerated\s*\npublic class/,
                            "@org.apache.avro.specific.AvroGenerated\n${annotation}\npublic class"
                        )
                        file.text = newContent
                        println "Added Jackson annotations to ${file.path - rootPath}"
                    }
                }
            }
        }
    }
}
compileJava.dependsOn 'addJacksonAnnotationsToAvro'
```

빌드 검증은 `JAVA_HOME=corretto-17 ./gradlew clean build`로 수행하며, deprecated 경고가 사라지고 Avro 클래스에 어노테이션이 정상 주입되는지 확인한다.
