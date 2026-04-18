# Java OpenTelemetry 적용 가이드

> OpenTelemetry Demo의 Ad Service를 참고한 Java 애플리케이션 계측 가이드

---

## 목차

1. [개요](#개요)
2. [의존성 설정](#의존성-설정)
3. [OpenTelemetry 초기화](#opentelemetry-초기화)
4. [트레이싱 구현](#트레이싱-구현)
5. [메트릭 구현](#메트릭-구현)
6. [로깅 연동](#로깅-연동)
7. [Feature Flag 연동](#feature-flag-연동)
8. [Docker 배포](#docker-배포)
9. [환경 변수](#환경-변수)

---

## 개요

### OpenTelemetry란?

OpenTelemetry는 분산 시스템에서 **Traces**, **Metrics**, **Logs**를 수집하기 위한 표준화된 관측성(Observability) 프레임워크입니다.

### Ad Service 구조

```
ad/
├── build.gradle                      # 의존성 및 빌드 설정
├── Dockerfile                        # 컨테이너 빌드
└── src/main/
    ├── java/oteldemo/
    │   ├── AdService.java            # 메인 서비스 (Tracing, Metrics)
    │   └── problempattern/           # Chaos Engineering 패턴
    │       ├── CPULoad.java          # CPU 부하 시뮬레이션
    │       ├── GarbageCollectionTrigger.java
    │       └── MemoryUtils.java
    └── resources/
        └── log4j2.xml                # 로깅 설정 (trace_id 포함)
```

---

## 의존성 설정

### build.gradle

```gradle
plugins {
    id 'java'
    id 'application'
    id 'com.google.protobuf' version '0.9.4'  // gRPC 사용 시
}

ext {
    opentelemetryVersion = "1.57.0"
    opentelemetryInstrumentationVersion = "2.23.0"
    grpcVersion = "1.78.0"
}

dependencies {
    // ============================================
    // OpenTelemetry Core
    // ============================================
    implementation "io.opentelemetry:opentelemetry-api:${opentelemetryVersion}"
    implementation "io.opentelemetry:opentelemetry-sdk:${opentelemetryVersion}"

    // ============================================
    // OpenTelemetry Instrumentation Annotations
    // - @WithSpan, @SpanAttribute 어노테이션 지원
    // ============================================
    implementation "io.opentelemetry.instrumentation:opentelemetry-instrumentation-annotations:${opentelemetryInstrumentationVersion}"

    // ============================================
    // gRPC (선택사항 - gRPC 서비스인 경우)
    // ============================================
    implementation "io.grpc:grpc-protobuf:${grpcVersion}"
    implementation "io.grpc:grpc-stub:${grpcVersion}"
    implementation "io.grpc:grpc-netty:${grpcVersion}"

    // ============================================
    // Logging (Log4j2 + OTel MDC 연동)
    // ============================================
    implementation 'org.apache.logging.log4j:log4j-core:2.25.3'

    // ============================================
    // Feature Flags (선택사항)
    // ============================================
    implementation 'dev.openfeature:sdk:1.19.2'
    implementation 'dev.openfeature.contrib.providers:flagd:0.11.18'
}

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}
```

### 핵심 의존성 설명

| 의존성 | 용도 |
|--------|------|
| `opentelemetry-api` | OpenTelemetry API (Tracer, Meter 인터페이스) |
| `opentelemetry-sdk` | SDK 구현체 (실제 데이터 수집/내보내기) |
| `opentelemetry-instrumentation-annotations` | `@WithSpan` 어노테이션 |
| `log4j-core` | 로깅 (MDC로 trace_id 연동) |

---

## OpenTelemetry 초기화

### GlobalOpenTelemetry 사용

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.metrics.Meter;

public class AdService {

    // Tracer 인스턴스 (분산 트레이싱용)
    private static final Tracer tracer = GlobalOpenTelemetry.getTracer("ad");

    // Meter 인스턴스 (메트릭 수집용)
    private static final Meter meter = GlobalOpenTelemetry.getMeter("ad");

    // ...
}
```

**주의**: `GlobalOpenTelemetry`는 **OpenTelemetry Java Agent**가 자동으로 설정합니다.
Agent 없이 사용할 경우 직접 SDK를 초기화해야 합니다.

### 수동 SDK 초기화 (Agent 없이)

```java
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.metrics.SdkMeterProvider;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter;

public class OtelConfig {
    public static void initialize() {
        // OTLP Exporter 설정
        OtlpGrpcSpanExporter spanExporter = OtlpGrpcSpanExporter.builder()
            .setEndpoint("http://otel-collector:4317")
            .build();

        OtlpGrpcMetricExporter metricExporter = OtlpGrpcMetricExporter.builder()
            .setEndpoint("http://otel-collector:4317")
            .build();

        // TracerProvider 설정
        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
            .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
            .build();

        // MeterProvider 설정
        SdkMeterProvider meterProvider = SdkMeterProvider.builder()
            .registerMetricReader(
                PeriodicMetricReader.builder(metricExporter).build()
            )
            .build();

        // OpenTelemetrySdk 빌드 및 글로벌 등록
        OpenTelemetrySdk sdk = OpenTelemetrySdk.builder()
            .setTracerProvider(tracerProvider)
            .setMeterProvider(meterProvider)
            .buildAndRegisterGlobal();
    }
}
```

---

## 트레이싱 구현

### 방법 1: @WithSpan 어노테이션 (권장)

가장 간단한 방법으로, 메서드에 어노테이션을 붙이면 자동으로 Span이 생성됩니다.

```java
import io.opentelemetry.instrumentation.annotations.WithSpan;
import io.opentelemetry.instrumentation.annotations.SpanAttribute;
import io.opentelemetry.api.trace.Span;

public class AdService {

    /**
     * @WithSpan: 이 메서드 호출 시 자동으로 Span 생성
     * @SpanAttribute: 파라미터를 Span 속성으로 기록
     */
    @WithSpan("getAdsByCategory")
    private Collection<Ad> getAdsByCategory(
            @SpanAttribute("app.ads.category") String category) {

        Collection<Ad> ads = adsMap.get(category);

        // 현재 Span에 속성 추가
        Span.current().setAttribute("app.ads.count", ads.size());

        return ads;
    }
}
```

**생성되는 Span 예시**:
```
Span: getAdsByCategory
├── attribute: app.ads.category = "electronics"
└── attribute: app.ads.count = 5
```

### 방법 2: 수동 Span 생성

세밀한 제어가 필요할 때 직접 Span을 생성합니다.

```java
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.context.Scope;

public class AdService {

    private List<Ad> getRandomAds() {
        List<Ad> ads = new ArrayList<>();

        // 1. Span 생성 및 시작
        Span span = tracer.spanBuilder("getRandomAds").startSpan();

        // 2. Span을 현재 컨텍스트로 설정 (try-with-resources)
        try (Scope scope = span.makeCurrent()) {

            // 비즈니스 로직
            Collection<Ad> allAds = adsMap.values();
            for (int i = 0; i < MAX_ADS_TO_SERVE; i++) {
                ads.add(Iterables.get(allAds, random.nextInt(allAds.size())));
            }

            // 3. Span 속성 추가
            span.setAttribute("app.ads.count", ads.size());

        } catch (Exception e) {
            // 4. 에러 발생 시 상태 설정
            span.setStatus(StatusCode.ERROR);
            span.recordException(e);
            throw e;

        } finally {
            // 5. Span 종료 (필수!)
            span.end();
        }

        return ads;
    }
}
```

### Baggage에서 컨텍스트 추출

분산 시스템에서 전파된 컨텍스트(예: session.id)를 읽어옵니다.

```java
import io.opentelemetry.api.baggage.Baggage;
import io.opentelemetry.context.Context;

public void getAds(AdRequest request, StreamObserver<AdResponse> responseObserver) {
    Span span = Span.current();

    // 현재 컨텍스트에서 Baggage 추출
    Baggage baggage = Baggage.fromContextOrNull(Context.current());

    if (baggage != null) {
        // 상위 서비스에서 전달된 session.id 읽기
        String sessionId = baggage.getEntryValue("session.id");

        if (sessionId != null) {
            span.setAttribute("session.id", sessionId);
        }
    }
}
```

### 에러 이벤트 기록

```java
try {
    // 비즈니스 로직
} catch (StatusRuntimeException e) {
    // Span에 에러 이벤트 추가
    span.addEvent("Error", Attributes.of(
        AttributeKey.stringKey("exception.message"), e.getMessage()
    ));

    // Span 상태를 ERROR로 설정
    span.setStatus(StatusCode.ERROR);

    logger.warn("GetAds Failed with status {}", e.getStatus());
    responseObserver.onError(e);
}
```

---

## 메트릭 구현

### Counter (카운터)

누적되는 값(요청 수, 에러 수 등)을 측정합니다.

```java
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.api.common.AttributeKey;

public class AdService {

    // AttributeKey 정의 (재사용)
    private static final AttributeKey<String> AD_REQUEST_TYPE_KEY =
        AttributeKey.stringKey("app.ads.ad_request_type");
    private static final AttributeKey<String> AD_RESPONSE_TYPE_KEY =
        AttributeKey.stringKey("app.ads.ad_response_type");

    // Counter 생성
    private static final LongCounter adRequestsCounter = meter
        .counterBuilder("app.ads.ad_requests")
        .setDescription("Counts ad requests by request and response type")
        .build();

    public void getAds(AdRequest request, StreamObserver<AdResponse> responseObserver) {
        AdRequestType adRequestType = AdRequestType.TARGETED;
        AdResponseType adResponseType = AdResponseType.RANDOM;

        // 요청 처리 로직...

        // 메트릭 기록 (속성과 함께)
        adRequestsCounter.add(1, Attributes.of(
            AD_REQUEST_TYPE_KEY, adRequestType.name(),
            AD_RESPONSE_TYPE_KEY, adResponseType.name()
        ));
    }
}
```

### 그 외 Meter 타입

```java
// Gauge (현재 값) - 메모리 사용량, 활성 연결 수 등
meter.gaugeBuilder("app.memory.heap_used")
    .setDescription("Current heap memory usage")
    .setUnit("bytes")
    .buildWithCallback(measurement -> {
        measurement.record(Runtime.getRuntime().totalMemory());
    });

// Histogram (분포) - 응답 시간, 요청 크기 등
DoubleHistogram responseTimeHistogram = meter
    .histogramBuilder("app.response.latency")
    .setDescription("Response latency distribution")
    .setUnit("ms")
    .build();

responseTimeHistogram.record(latencyMs, Attributes.of(
    AttributeKey.stringKey("endpoint"), "/api/ads"
));
```

---

## 로깅 연동

### log4j2.xml 설정

OpenTelemetry Java Agent는 자동으로 MDC(Mapped Diagnostic Context)에 trace_id, span_id를 주입합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="STDOUT" target="SYSTEM_OUT">
            <!-- trace_id, span_id를 로그에 포함 -->
            <PatternLayout
                pattern="%d{yyyy-MM-dd HH:mm:ss} - %logger{36} - %msg trace_id=%X{trace_id} span_id=%X{span_id} trace_flags=%X{trace_flags} %n"/>
        </Console>
    </Appenders>
    <Loggers>
        <Root level="INFO">
            <AppenderRef ref="STDOUT"/>
        </Root>
    </Loggers>
</Configuration>
```

### 로그 출력 예시

```
2025-01-15 10:30:45 - o.AdService - Processing ad request trace_id=a1b2c3d4e5f6 span_id=1234abcd trace_flags=01
```

**장점**: 로그와 트레이스를 **trace_id**로 연결하여 Jaeger/Grafana에서 상관분석 가능

---

## Feature Flag 연동

### OpenFeature + Flagd 설정

```java
import dev.openfeature.sdk.OpenFeatureAPI;
import dev.openfeature.sdk.Client;
import dev.openfeature.sdk.MutableContext;
import dev.openfeature.contrib.providers.flagd.FlagdProvider;
import dev.openfeature.contrib.providers.flagd.FlagdOptions;

public class AdService {

    private static final String AD_FAILURE = "adFailure";
    private static final String AD_HIGH_CPU_FEATURE_FLAG = "adHighCpu";

    private void initializeFeatureFlags() {
        // Flagd 프로바이더 설정 (OTel 연동 활성화)
        FlagdOptions options = FlagdOptions.builder()
            .withGlobalTelemetry(true)  // OpenTelemetry 연동
            .build();

        FlagdProvider provider = new FlagdProvider(options);
        OpenFeatureAPI.getInstance().setProvider(provider);
    }

    public void getAds(AdRequest request) {
        Client ffClient = OpenFeatureAPI.getInstance().getClient();

        // 평가 컨텍스트 설정 (사용자별 타겟팅 가능)
        MutableContext evaluationContext = new MutableContext();
        evaluationContext.setTargetingKey(sessionId);
        evaluationContext.add("session", sessionId);

        // Boolean 플래그 평가
        if (ffClient.getBooleanValue(AD_FAILURE, false, evaluationContext)) {
            // 10% 확률로 실패 시뮬레이션
            if (random.nextInt(10) == 0) {
                throw new StatusRuntimeException(Status.UNAVAILABLE);
            }
        }

        // CPU 부하 시뮬레이션
        boolean enableHighCpu = ffClient.getBooleanValue(
            AD_HIGH_CPU_FEATURE_FLAG, false, evaluationContext
        );
        cpuLoad.execute(enableHighCpu);
    }
}
```

---

## Docker 배포

### Dockerfile (Multi-stage 빌드)

```dockerfile
# ============================================
# Stage 1: Build
# ============================================
FROM --platform=${BUILDPLATFORM} eclipse-temurin:21-jdk AS builder

WORKDIR /usr/src/app

# Gradle Wrapper 복사
COPY ./src/ad/gradlew* ./src/ad/settings.gradle* ./
COPY ./src/ad/gradle ./gradle

# 의존성 다운로드 (캐싱 활용)
RUN ./gradlew downloadRepos --no-daemon

# 소스 코드 복사 및 빌드
COPY ./src/ad ./
COPY ./pb ./proto
RUN ./gradlew installDist -PprotoSourceDir=./proto --no-daemon

# ============================================
# Stage 2: Runtime
# ============================================
FROM eclipse-temurin:21-jre

ARG OTEL_JAVA_AGENT_VERSION=2.23.0

WORKDIR /usr/src/app

# OpenTelemetry Java Agent 다운로드
ADD --chmod=644 \
    https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v${OTEL_JAVA_AGENT_VERSION}/opentelemetry-javaagent.jar \
    /usr/src/app/opentelemetry-javaagent.jar

# 빌드된 애플리케이션 복사
COPY --from=builder /usr/src/app/build/install/opentelemetry-demo-ad/ ./

# Java Agent 설정 (핵심!)
ENV JAVA_TOOL_OPTIONS="-javaagent:/usr/src/app/opentelemetry-javaagent.jar"

EXPOSE 9555

ENTRYPOINT ["./bin/Ad"]
```

### OpenTelemetry Java Agent

**자동 계측 항목**:
- HTTP 클라이언트/서버 (Spring, JAX-RS, etc.)
- gRPC
- JDBC
- Kafka
- Redis
- 로깅 프레임워크 (Log4j2, Logback)
- 스레드 풀, Executor

**장점**: 코드 수정 없이 대부분의 라이브러리가 자동 계측됨

---

## 환경 변수

### 필수 환경 변수

```bash
# 애플리케이션 포트
AD_PORT=9555

# Feature Flag 서비스 주소
FEATURE_FLAG_GRPC_SERVICE_ADDR=flagd:8013
```

### OpenTelemetry Agent 환경 변수

```bash
# OTLP Exporter 설정
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# 서비스 정보
OTEL_SERVICE_NAME=ad
OTEL_RESOURCE_ATTRIBUTES=service.namespace=opentelemetry-demo,service.version=1.0.0

# 메트릭 Temporality 설정
OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=cumulative

# 샘플링 설정 (선택)
OTEL_TRACES_SAMPLER=parentbased_always_on
```

### docker-compose.yml 예시

```yaml
services:
  ad:
    build:
      context: .
      dockerfile: ./src/ad/Dockerfile
    environment:
      - AD_PORT=9555
      - FEATURE_FLAG_GRPC_SERVICE_ADDR=flagd:8013
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
      - OTEL_SERVICE_NAME=ad
    depends_on:
      - otel-collector
      - flagd
    ports:
      - "9555:9555"
```

---

## 요약: 적용 체크리스트

| 단계 | 필수 | 설명 |
|------|:----:|------|
| 의존성 추가 | ✅ | `opentelemetry-api`, `opentelemetry-sdk` |
| Tracer/Meter 초기화 | ✅ | `GlobalOpenTelemetry.getTracer("service-name")` |
| @WithSpan 어노테이션 | ✅ | 메서드 단위 자동 Span 생성 |
| 수동 Span 생성 | 선택 | 세밀한 제어 필요 시 |
| 메트릭 Counter | 선택 | 요청 수, 에러 수 등 |
| 로그 MDC 연동 | ✅ | `trace_id=%X{trace_id}` 패턴 |
| Java Agent 적용 | ✅ | `-javaagent:opentelemetry-javaagent.jar` |
| 환경 변수 설정 | ✅ | `OTEL_EXPORTER_OTLP_ENDPOINT` 등 |

---

## 참고 자료

- [OpenTelemetry Java Documentation](https://opentelemetry.io/docs/languages/java/)
- [OpenTelemetry Java Agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Demo](https://github.com/open-telemetry/opentelemetry-demo)
- [OpenFeature Java SDK](https://openfeature.dev/docs/reference/technologies/server/java)

---

*문서 작성일: 2025-12-30*
