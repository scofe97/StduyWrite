# LogAspect 개선안: 분산 트레이싱 통합 가이드

> workflow-api의 LogAspect에 TraceID를 통합하여 분산 환경에서도 요청 흐름을 추적할 수 있도록 개선하는 방안

---

## 1. 현재 상태 분석

### 1.1 현재 LogAspect 구조

```
workflow-api/
└── src/main/java/org/okestro/tps/api/
    ├── v3/infrastructure/support/aop/
    │   └── LogAspect.java          ← 분석 대상
    └── infrastructure/config/
        └── LogTraceConfig.java      ← LogTrace Bean 설정
```

### 1.2 현재 코드 분석

**LogAspect.java**:
```java
@Aspect
@Component(value = "LogAspectV3")
@Profile("local")  // ⚠️ 로컬에서만 활성화
@ConditionalOnProperty(name = "trb.release.version", havingValue = "v3.0.5")
@RequiredArgsConstructor
public class LogAspect {
    private final LogTrace logTrace;

    @Pointcut("execution(* org.okestro.tps.api.v3.domain..*.*(..)) && !within(*..mapper..*)")
    public void allComponent(){};

    // ... 다른 Pointcut들

    @Around("allComponent() || allService() || allPersistence() || allEventListener()")
    public Object logTrace(ProceedingJoinPoint joinPoint) throws Throwable {
        TraceStatus status = null;
        try {
            status = logTrace.begin(joinPoint.getSignature().toShortString());
            Object result = joinPoint.proceed();
            logTrace.end(status);
            return result;
        } catch (Throwable e) {
            logTrace.exception(status, e);
            throw e;
        }
    }
}
```

**LogTraceConfig.java**:
```java
@Profile("local")  // ⚠️ 로컬에서만 활성화
@Configuration
public class LogTraceConfig {
    @Bean
    public LogTrace logTrace() {
        return new LogTraceImpl();  // core-lib의 구현체
    }
}
```

### 1.3 현재 문제점

| 문제 | 설명 | 영향 |
|------|------|------|
| **로컬 전용** | `@Profile("local")`로 개발 환경에서만 동작 | 운영 환경에서 로그 추적 불가 |
| **분산 TraceID 없음** | 자체 TraceStatus만 사용, 서비스 간 연결 없음 | 마이크로서비스 간 요청 추적 불가 |
| **MDC 미활용** | 로그에 TraceID가 자동 포함되지 않음 | 로그 검색/필터링 어려움 |
| **core-lib 의존** | LogTrace 인터페이스가 외부 라이브러리에 정의 | 수정 범위 제한 |

### 1.4 현재 로그 출력 예시 (추정)

```
[LogAspect] --> OrderService.createOrder()
[LogAspect]   --> OrderRepository.save()
[LogAspect]   <-- OrderRepository.save() time=45ms
[LogAspect] <-- OrderService.createOrder() time=120ms
```

**문제**: 이 로그가 어떤 HTTP 요청에서 발생했는지 알 수 없음

---

## 2. 개선 목표

### 2.1 목표 상태

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 요청 → workflow-api → pipeline-api → common-api                        │
│         [TraceID: abc123]  [TraceID: abc123]  [TraceID: abc123]        │
│                                                                         │
│ 모든 서비스의 로그에서 TraceID로 검색 가능                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 개선 후 로그 예시

```
2024-12-23 10:00:01.123 INFO  [workflow-api,abc123,span001] --> OrderService.createOrder()
2024-12-23 10:00:01.145 INFO  [workflow-api,abc123,span002]   --> OrderRepository.save()
2024-12-23 10:00:01.190 INFO  [workflow-api,abc123,span002]   <-- OrderRepository.save() time=45ms
2024-12-23 10:00:01.243 INFO  [workflow-api,abc123,span001] <-- OrderService.createOrder() time=120ms
```

**개선점**:
- `abc123`: TraceID - 전체 요청 흐름 식별
- `span001`, `span002`: SpanID - 개별 작업 식별
- 다른 서비스 로그에서도 `abc123`으로 검색 가능

---

## 3. 개선 방안

### 3.1 방안 1: Micrometer Tracing + MDC 통합 (권장)

**개요**: Micrometer Tracing이 자동으로 MDC에 TraceID를 설정하므로, 로그 패턴만 변경하면 됨

**장점**:
- LogAspect 수정 최소화
- 표준 방식 (Spring Boot 3.x 권장)
- FeignClient 호출 시 자동 전파

**단계**:

#### Step 1: 의존성 추가 (build.gradle)

```gradle
dependencies {
    // 기존 의존성 유지...

    // Micrometer Tracing 추가
    implementation 'io.micrometer:micrometer-tracing-bridge-brave'
    implementation 'io.zipkin.reporter2:zipkin-reporter-brave'

    // FeignClient Tracing
    implementation 'io.github.openfeign:feign-micrometer'
}
```

#### Step 2: application.yml 설정

```yaml
spring:
  application:
    name: workflow-api

management:
  tracing:
    sampling:
      probability: 1.0  # 개발: 1.0, 운영: 0.1 권장
  zipkin:
    tracing:
      endpoint: http://zipkin:9411/api/v2/spans

# 로그 패턴에 TraceID/SpanID 포함
logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]"
```

#### Step 3: LogAspect 수정

```java
@Aspect
@Component(value = "LogAspectV3")
// @Profile("local")  // 제거: 모든 환경에서 활성화
@ConditionalOnProperty(name = "log.aspect.enabled", havingValue = "true", matchIfMissing = true)
@RequiredArgsConstructor
@Slf4j
public class LogAspect {

    private final Tracer tracer;  // Micrometer Tracer 주입

    @Around("allComponent() || allService() || allPersistence() || allEventListener()")
    public Object logTrace(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().toShortString();

        // 현재 Span 정보 가져오기
        Span currentSpan = tracer.currentSpan();
        String traceId = currentSpan != null ? currentSpan.context().traceId() : "N/A";

        long startTime = System.currentTimeMillis();

        log.info("--> {} [traceId={}]", methodName, traceId);

        try {
            Object result = joinPoint.proceed();
            long duration = System.currentTimeMillis() - startTime;
            log.info("<-- {} time={}ms", methodName, duration);
            return result;
        } catch (Throwable e) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("<X- {} time={}ms error={}", methodName, duration, e.getMessage());
            throw e;
        }
    }
}
```

### 3.2 방안 2: 커스텀 Span 생성 (고급)

**개요**: 각 메서드 호출을 개별 Span으로 기록하여 Zipkin에서 상세 추적 가능

**장점**:
- Zipkin UI에서 메서드 단위 성능 분석 가능
- 더 세밀한 트레이싱

**단점**:
- 오버헤드 증가
- Span 수 폭증 가능

```java
@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class DetailedLogAspect {

    private final Tracer tracer;
    private final ObservationRegistry observationRegistry;

    @Around("allService()")
    public Object traceMethod(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().toShortString();

        // 새 Span 생성
        Observation observation = Observation.createNotStarted(
            methodName,
            observationRegistry
        );

        return observation.observe(() -> {
            try {
                return joinPoint.proceed();
            } catch (Throwable e) {
                throw new RuntimeException(e);
            }
        });
    }
}
```

### 3.3 방안 3: 기존 LogTrace 확장 (보수적)

**개요**: core-lib의 LogTrace를 확장하여 TraceID 지원 추가

**장점**:
- 기존 코드 변경 최소화
- core-lib 수정 없이 가능

**단점**:
- 표준 방식이 아님
- 유지보수 부담

```java
@Component
@Profile("!local")  // local 외 환경에서 사용
public class DistributedLogTrace implements LogTrace {

    private final Tracer tracer;

    @Override
    public TraceStatus begin(String message) {
        Span currentSpan = tracer.currentSpan();
        String traceId = currentSpan != null ? currentSpan.context().traceId() : generateLocalId();

        // 기존 로직 + TraceID 포함
        log.info("[{}] --> {}", traceId, message);
        return new TraceStatus(traceId, message, System.currentTimeMillis());
    }

    @Override
    public void end(TraceStatus status) {
        long duration = System.currentTimeMillis() - status.getStartTime();
        log.info("[{}] <-- {} time={}ms", status.getTraceId(), status.getMessage(), duration);
    }

    // ...
}
```

---

## 4. 방안 비교

| 항목 | 방안 1 (MDC) | 방안 2 (커스텀 Span) | 방안 3 (LogTrace 확장) |
|------|-------------|---------------------|----------------------|
| **복잡도** | 낮음 | 높음 | 중간 |
| **표준 준수** | ✅ Spring 표준 | ✅ 표준 | ❌ 비표준 |
| **Zipkin 통합** | ⚠️ 로그만 | ✅ 완전 통합 | ❌ 없음 |
| **오버헤드** | 최소 | 높음 | 낮음 |
| **권장 환경** | 일반적인 경우 | 상세 분석 필요 | 레거시 유지 |

**권장**: **방안 1 (MDC 통합)** - 최소 변경으로 최대 효과

---

## 5. 구현 로드맵

### Phase 1: 기반 구축 (1주)

```
□ Micrometer Tracing 의존성 추가
□ application.yml 설정
□ 로컬 Zipkin 환경 구성
□ 기본 동작 확인
```

### Phase 2: LogAspect 개선 (1주)

```
□ @Profile("local") 제거 또는 조건 변경
□ Tracer 주입 및 TraceID 로깅
□ 테스트 환경에서 검증
```

### Phase 3: FeignClient 통합 (1주)

```
□ feign-micrometer 의존성 추가
□ 서비스 간 TraceID 전파 확인
□ 전체 흐름 Zipkin에서 확인
```

### Phase 4: 운영 적용 (1주)

```
□ 샘플링 비율 조정 (운영: 0.1)
□ Zipkin 스토리지 구성 (Elasticsearch)
□ 모니터링 대시보드 구성
□ 팀 교육 및 문서화
```

---

## 6. 설정 예시

### 6.1 환경별 application.yml

**application-local.yml**:
```yaml
management:
  tracing:
    sampling:
      probability: 1.0  # 모든 요청 추적
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans

log:
  aspect:
    enabled: true
```

**application-prod.yml**:
```yaml
management:
  tracing:
    sampling:
      probability: 0.1  # 10%만 추적
  zipkin:
    tracing:
      endpoint: http://zipkin.monitoring.svc:9411/api/v2/spans

log:
  aspect:
    enabled: true  # 또는 false로 비활성화
```

### 6.2 logback-spring.xml

```xml
<configuration>
    <springProperty scope="context" name="appName" source="spring.application.name"/>

    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>
                %d{yyyy-MM-dd HH:mm:ss.SSS} %5p [${appName},%X{traceId:-},%X{spanId:-}] --- [%t] %logger{36} : %msg%n
            </pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
    </root>
</configuration>
```

---

## 7. 예상 효과

### 7.1 정량적 효과

| 지표 | 현재 | 개선 후 |
|------|------|---------|
| 장애 원인 파악 시간 | 30분~2시간 | 5~10분 |
| 로그 검색 효율 | 수동 시간대 필터링 | TraceID 즉시 검색 |
| 서비스 간 추적 | 불가능 | 완전 지원 |

### 7.2 정성적 효과

- **디버깅 효율성**: 한 번의 검색으로 전체 요청 흐름 파악
- **성능 분석**: 병목 구간 즉시 식별
- **팀 협업**: "이 TraceID 확인해봐" 한 마디로 문제 공유

---

## 8. 주의사항

### 8.1 성능 오버헤드

- 트레이싱은 약 **1-3%** 성능 오버헤드 발생
- 샘플링 비율로 조절 가능
- CPU/메모리 모니터링 필요

### 8.2 민감 정보 보호

```yaml
# 민감한 헤더/파라미터 제외
management:
  tracing:
    baggage:
      remote-fields:
        - x-request-id
      # Authorization 헤더 등은 제외
```

### 8.3 Storage 용량

- 일일 Trace 수 × 평균 Span 수 × 보관 기간
- Elasticsearch 사용 시 인덱스 정책 설정 필요

---

## 9. 참고 자료

- [Micrometer Tracing 공식 문서](https://micrometer.io/docs/tracing)
- [Spring Boot Observability](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.observability)
- [Logback MDC 가이드](https://logback.qos.ch/manual/mdc.html)
- [Zipkin 운영 가이드](https://zipkin.io/pages/architecture.html)

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2024-12-23 | 1.0 | 최초 작성 |
