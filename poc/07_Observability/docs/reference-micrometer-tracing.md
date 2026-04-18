# Micrometer Tracing 레퍼런스

---

### 📌 핵심 요약
> Micrometer Tracing은 JVM 기반 애플리케이션에서 벤더 종속 없이 분산 트레이싱을 구현할 수 있는 **Facade(퍼사드)** 라이브러리다. Spring Cloud Sleuth에서 발전하여 Spring-agnostic하게 설계되었으며, Brave와 OpenTelemetry 두 가지 트레이서를 지원한다. Micrometer 1.10.0+의 Observation API와 통합되어 관찰(Observation) 시 자동으로 Span을 생성한다.

---

### 🎯 학습 목표
- Micrometer Tracing의 목적과 특징을 이해한다
- Brave와 OpenTelemetry Bridge의 차이를 안다
- Span 생성, Baggage, Context Propagation 방법을 안다
- Observation API와의 통합 방법을 이해한다
- 어노테이션 기반 트레이싱을 구현할 수 있다

---

### 📖 본문 정리

#### 1. 개요

##### Micrometer Tracing이란?

> *"Micrometer Tracing은 가장 인기 있는 트레이서 라이브러리에 대한 간단한 퍼사드를 제공하여, 벤더 종속 없이 JVM 기반 애플리케이션 코드를 계측할 수 있게 한다."*

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                          │
├─────────────────────────────────────────────────────────────┤
│                  Micrometer Tracing API                      │
│               (Vendor-neutral Facade)                        │
├──────────────────────┬──────────────────────────────────────┤
│   Brave Bridge       │      OpenTelemetry Bridge            │
│   (micrometer-       │      (micrometer-                    │
│   tracing-bridge-    │      tracing-bridge-                 │
│   brave)             │      otel)                           │
├──────────────────────┼──────────────────────────────────────┤
│       Zipkin         │    Jaeger / Tempo / etc.             │
└──────────────────────┴──────────────────────────────────────┘
```

##### 주요 특징

| 특징 | 설명 |
|------|------|
| **벤더 독립성** | 특정 트레이서 구현에 종속되지 않음 |
| **낮은 오버헤드** | 트레이싱 수집 시 최소한의 성능 영향 |
| **이식성** | 다양한 트레이싱 솔루션 간 유연한 전환 |
| **Observation 통합** | Micrometer 1.10.0+ Observation API 연동 |

##### 역사

```
Spring Cloud Sleuth
        │
        ▼ (Spring-agnostic 추출)
Micrometer Tracing
        │
        ▼ (2022년 11월 GA)
현재 버전: 1.6.1
```

---

#### 2. 용어 정의 (Glossary)

| 용어 | 정의 |
|------|------|
| **Span** | 작업의 기본 단위. 예: RPC 전송, RPC 응답 |
| **Trace** | 트리 구조로 배열된 Span의 집합. 예: 분산 데이터 저장소의 PUT 요청 |
| **Annotation/Event** | 특정 시점에 발생한 일을 기록하는 타임스탬프 마커 |
| **Tracer** | Span의 전체 생명주기(생성, 시작, 중지, 전송)를 관리하는 라이브러리 |
| **Tracing Context** | 프로세스/네트워크 간 분산 트레이싱에 필요한 정보 (trace ID, span ID 등) |
| **Log Correlation** | 로그에 trace ID, span ID를 추가하여 단일 비즈니스 작업 로그를 그룹화 |
| **Latency Analysis Tools** | 내보낸 Span을 수집하여 전체 Trace를 시각화하는 도구 |

---

#### 3. 설치 및 의존성

##### BOM (Bill of Materials) 사용

**Gradle**:
```groovy
implementation platform('io.micrometer:micrometer-tracing-bom:latest.release')
implementation 'io.micrometer:micrometer-tracing'
```

**Maven**:
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.micrometer</groupId>
            <artifactId>micrometer-tracing-bom</artifactId>
            <version>${micrometer-tracing.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-tracing</artifactId>
    </dependency>
</dependencies>
```

##### Bridge 선택 (중요!)

> ⚠️ **반드시 하나의 Bridge만 선택해야 한다. 두 개의 Bridge가 classpath에 있으면 안 된다!**

| Bridge | 의존성 | 백엔드 |
|--------|--------|--------|
| **Brave** | `micrometer-tracing-bridge-brave` | Zipkin |
| **OpenTelemetry** | `micrometer-tracing-bridge-otel` | Jaeger, Tempo, Zipkin 등 |

**Gradle - Brave**:
```groovy
implementation 'io.micrometer:micrometer-tracing-bridge-brave'
```

**Gradle - OpenTelemetry**:
```groovy
implementation 'io.micrometer:micrometer-tracing-bridge-otel'
```

**Maven - Brave**:
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-brave</artifactId>
</dependency>
```

**Maven - OpenTelemetry**:
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
```

---

#### 4. API 사용법

##### Span 생성 및 관리

```java
// 새 Span 생성 (현재 스레드에 Span이 있으면 부모가 됨)
Span newSpan = tracer.nextSpan().name("calculateTax");

// Span 시작 및 스코프 설정
try (Tracer.SpanInScope ws = tracer.withSpan(newSpan.start())) {
    // 태그 추가 (디버깅용 키-값 쌍)
    newSpan.tag("taxValue", taxValue);

    // 이벤트 기록 (타임스탬프 마커)
    newSpan.event("taxCalculated");

    // 비즈니스 로직 실행
    calculateTax();
} finally {
    // Span 종료
    newSpan.end();
}
```

##### 부모-자식 관계

```java
// 명시적으로 부모 Span 지정
Span childSpan = tracer.nextSpan(parentSpan).name("childOperation");
```

```
Trace 계층 구조:
parentSpan
└── childSpan (tracer.nextSpan(parentSpan))
```

##### 크로스 스레드 Span 연속

```java
// 스레드 간 Span 전달 (부모-자식 관계 아님, 동일 Span 계속)
Span spanFromOtherThread = // 다른 스레드에서 전달받음
try (Tracer.SpanInScope ws = tracer.withSpan(spanFromOtherThread)) {
    // 비동기 작업 계속
}
```

---

#### 5. Baggage 관리

**Baggage**: 애플리케이션 간 헤더를 통해 전파되는 속성

```java
// Baggage 생성 및 스코프 설정
try (BaggageInScope baggage = tracer.createBaggageInScope("userId", "12345")) {
    // 이 스코프 내에서 baggage 사용 가능

    // Baggage 조회
    String userId = tracer.getBaggage("userId").get();
}
// 스코프 종료 시 baggage도 종료
```

##### Brave에서 Baggage 설정

```java
// Brave에서는 전파할 필드 목록을 명시해야 함
Tracing.newBuilder()
    .propagationFactory(
        BaggagePropagation.newFactoryBuilder(B3Propagation.FACTORY)
            .add(BaggagePropagationConfig.SingleBaggageField
                .remote(BaggageField.create("userId")))
            .build()
    )
    .build();
```

---

#### 6. 어노테이션 기반 트레이싱

##### 지원 어노테이션

| 어노테이션 | 용도 |
|-----------|------|
| `@NewSpan` | 메서드 호출 시 새 Span 생성 |
| `@ContinueSpan` | 기존 Span에 태그/이벤트 추가 |
| `@SpanTag` | 메서드 파라미터를 Span 태그로 추가 |

##### 사용 예시

```java
@Service
public class TaxService {

    // 새 Span 생성
    @NewSpan("calculateTax")
    public TaxResult calculateTax(@SpanTag("orderId") String orderId,
                                   @SpanTag("amount") BigDecimal amount) {
        // 비즈니스 로직
        return result;
    }

    // 기존 Span에 태그 추가
    @ContinueSpan
    public void updateTax(@SpanTag("newRate") double rate) {
        // 현재 Span에 태그만 추가
    }
}
```

##### AOP 설정 필요

```java
@Configuration
public class TracingConfig {

    @Bean
    public SpanAspect spanAspect(Tracer tracer) {
        return new SpanAspect(
            tracer,
            new DefaultNewSpanParser(),
            new ValueExpressionResolver(),
            new ImperativeMethodInvocationProcessor(tracer)
        );
    }
}
```

---

#### 7. Observation API 통합

##### Handler 구성

```java
// ObservationRegistry에 핸들러 등록
ObservationRegistry registry = ObservationRegistry.create();

// 메트릭 핸들러
registry.observationConfig().observationHandler(
    new DefaultMeterObservationHandler(meterRegistry)
);

// 트레이싱 핸들러
registry.observationConfig().observationHandler(
    new FirstMatchingCompositeObservationHandler(
        // 와이어 통신용 (HTTP, 메시징 등)
        new PropagatingSenderTracingObservationHandler<>(tracer, propagator),
        new PropagatingReceiverTracingObservationHandler<>(tracer, propagator),
        // 기본 트레이싱
        new DefaultTracingObservationHandler(tracer)
    )
);
```

##### Observation 생성

**확장 방식**:
```java
Observation observation = Observation.createNotStarted("myOperation", registry);
observation.start();
try (Observation.Scope scope = observation.openScope()) {
    // 측정할 코드
    doSomething();
} finally {
    observation.stop();
}
```

**간결한 방식**:
```java
Observation.createNotStarted("myOperation", registry)
    .observe(this::doSomething);
```

##### 결과 데이터

```
Observation 실행 시 생성되는 데이터:

1. Timer 메트릭:
   ├── COUNT: 호출 횟수
   ├── TOTAL_TIME: 총 소요 시간
   └── MAX: 최대 소요 시간

2. Span 데이터:
   └── Zipkin/Jaeger 등으로 전송
```

---

#### 8. Context Propagation

##### ThreadLocalAccessor 등록

```java
// 수동 Span 전파용
ContextRegistry.getInstance().registerThreadLocalAccessor(
    new ObservationAwareSpanThreadLocalAccessor(tracer)
);

// 사용자 생성 Baggage 전파용
ContextRegistry.getInstance().registerThreadLocalAccessor(
    new ObservationAwareBaggageThreadLocalAccessor(tracer)
);
```

##### Project Reactor 통합

```java
// Reactor Context에 값 저장
Mono.just("value")
    .contextWrite(Context.of("key", "value"))
    .subscribe();

// 자동 컨텍스트 전파 활성화
Hooks.enableAutomaticContextPropagation();
```

---

#### 9. Tracer 구성 예시

##### Brave + Zipkin

```java
// Zipkin Reporter 설정
AsyncZipkinSpanHandler spanHandler = AsyncZipkinSpanHandler.create(
    URLConnectionSender.create("http://localhost:9411/api/v2/spans")
);

// Brave Tracing 설정
Tracing braveTracing = Tracing.newBuilder()
    .localServiceName("my-service")
    .currentTraceContext(ThreadLocalCurrentTraceContext.newBuilder()
        .addScopeDecorator(MDCScopeDecorator.get())  // MDC 자동 관리
        .build())
    .addSpanHandler(spanHandler)
    .build();

// Micrometer Tracer 생성
Tracer tracer = new BraveTracer(braveTracing.tracer());
```

##### OpenTelemetry + Zipkin

```java
// Zipkin Exporter 설정
SpanExporter spanExporter = ZipkinSpanExporter.builder()
    .setEndpoint("http://localhost:9411/api/v2/spans")
    .build();

// OTel SDK 설정
SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
    .setResource(Resource.create(Attributes.of(
        ResourceAttributes.SERVICE_NAME, "my-service")))
    .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
    .build();

OpenTelemetry openTelemetry = OpenTelemetrySdk.builder()
    .setTracerProvider(tracerProvider)
    .buildAndRegisterGlobal();

// Micrometer Tracer 생성
Tracer tracer = new OtelTracer(
    openTelemetry.getTracer("my-service"),
    new OtelCurrentTraceContext()
);
```

---

#### 10. Exemplars 지원

Exemplar: 메트릭과 트레이스를 연결하는 샘플 데이터

```java
// TracingAwareMeterObservationHandler 사용
registry.observationConfig().observationHandler(
    new TracingAwareMeterObservationHandler<>(
        new DefaultMeterObservationHandler(meterRegistry),
        tracer
    )
);

// 결과: 메트릭에 trace_id, span_id가 exemplar로 첨부됨
```

---

### 🔍 심화 학습

#### Brave vs OpenTelemetry 선택 기준

| 항목 | Brave | OpenTelemetry |
|------|-------|---------------|
| **역사** | Zipkin 생태계, 오래됨 | 최신 표준 |
| **백엔드** | 주로 Zipkin | Jaeger, Tempo, Zipkin 등 다양 |
| **커뮤니티** | 안정적 | 빠르게 성장 중 |
| **Spring 통합** | 잘 됨 | 잘 됨 |
| **권장** | 기존 Zipkin 사용자 | 새 프로젝트, 표준 준수 필요 시 |

#### Handler 실행 순서

| Handler 타입 | 동작 |
|--------------|------|
| `AllMatchingCompositeObservationHandler` | 매칭되는 **모든** 핸들러 실행 |
| `FirstMatchingCompositeObservationHandler` | **첫 번째** 매칭 핸들러만 실행 |

```
Handler 구성 예:
FirstMatchingCompositeObservationHandler
├── PropagatingSenderTracingObservationHandler (HTTP 요청)
├── PropagatingReceiverTracingObservationHandler (HTTP 수신)
└── DefaultTracingObservationHandler (기본 - 위에서 매칭 안 되면)
```

---

### 💡 실무 적용 포인트

1. **Bridge 하나만 선택**: Brave 또는 OTel, 둘 다 쓰지 말 것
2. **BOM 사용**: 버전 충돌 방지
3. **MDC 통합**: `MDCScopeDecorator`로 로그에 trace_id 자동 추가
4. **Observation 우선**: 직접 Span 생성보다 Observation API 권장
5. **어노테이션 활용**: `@NewSpan`, `@ContinueSpan`으로 코드 간결화
6. **Baggage 제한적 사용**: 전파 오버헤드 고려
7. **Exemplar 활성화**: 메트릭-트레이스 연결로 디버깅 효율화

---

### ✅ 정리 체크리스트

- [ ] Micrometer Tracing이 Facade 패턴임을 이해한다
- [ ] Brave와 OpenTelemetry Bridge 중 하나만 선택해야 함을 안다
- [ ] Span 생성 및 종료 방법을 안다
- [ ] 부모-자식 Span 관계를 설정할 수 있다
- [ ] Baggage의 용도와 사용법을 안다
- [ ] `@NewSpan`, `@ContinueSpan`, `@SpanTag` 어노테이션을 안다
- [ ] Observation API와의 통합 방법을 이해한다
- [ ] Context Propagation 설정 방법을 안다
- [ ] Brave와 OpenTelemetry 구성 예시를 참고할 수 있다

---

### 🔗 참고 자료

- [Micrometer Tracing Reference](https://docs.micrometer.io/tracing/reference/index.html)
- [Using Micrometer Tracing Directly (API)](https://docs.micrometer.io/tracing/reference/api.html)
- [Supported Tracers](https://docs.micrometer.io/tracing/reference/tracers.html)
- [Configuring with Micrometer Observation](https://docs.micrometer.io/tracing/reference/configuring.html)
- [Micrometer Tracing Glossary](https://docs.micrometer.io/tracing/reference/glossary.html)
- [Micrometer Tracing Testing](https://docs.micrometer.io/tracing/reference/testing.html)
