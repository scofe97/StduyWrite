# 04. OpenTelemetry 연계

Redpanda와 OpenTelemetry를 연계한 분산 추적, 메트릭 수집, 관찰 가능성(Observability) 구현 가이드입니다.

> **인프라 모니터링**: Prometheus 메트릭, Grafana 대시보드, 알림 설정은 [01-monitoring.md](./01-monitoring.md) 참조. 이 문서는 **애플리케이션 수준 분산 추적**에 집중한다.

---

## 1. OpenTelemetry 개요

### 1.1 OpenTelemetry의 3가지 신호(Signal)

OpenTelemetry는 관찰 가능성을 위한 세 가지 핵심 신호를 제공합니다.

| 신호 | 역할 | 사용 시점 |
|------|------|----------|
| **Metrics** | 시스템 상태 수치 (CPU, 메모리, 처리량) | 시스템 건강 상태 모니터링 시 |
| **Traces** | 요청의 전체 흐름 추적 | 분산 시스템에서 병목 지점 찾을 때 |
| **Logs** | 구조화된 이벤트 기록 | 특정 시점의 상세 정보 확인 시 |

**Metrics는 "무엇이 느린가?"를 알려주고, Traces는 "왜 느린가?"를 보여줍니다.** Logs는 그 시점에 "정확히 무슨 일이 있었는가?"를 기록합니다. 이 세 가지를 함께 사용하면 시스템의 문제를 빠르게 진단할 수 있습니다.

### 1.2 OpenTelemetry가 2025-2026 업계 표준이 된 이유

OpenTelemetry는 다음 세 가지 이유로 관찰 가능성의 사실상 표준이 되었습니다.

#### 벤더 중립성
과거에는 Datadog를 사용하면 Datadog 전용 에이전트를, New Relic을 사용하면 New Relic 전용 에이전트를 설치해야 했습니다. 벤더를 바꾸려면 전체 계측 코드를 다시 작성해야 했습니다. OpenTelemetry는 하나의 표준 SDK로 데이터를 수집하고, 백엔드는 자유롭게 선택할 수 있습니다. Jaeger를 쓰다가 Grafana Tempo로 바꾸어도 애플리케이션 코드는 변경할 필요가 없습니다.

#### OTLP 프로토콜 통일
OpenTelemetry Protocol(OTLP)은 gRPC와 HTTP 기반의 표준 프로토콜입니다. 모든 OTel SDK는 OTLP 형식으로 데이터를 내보내고, 모든 OTel 호환 백엔드는 OTLP 형식을 받을 수 있습니다. 이제 "이 모니터링 도구가 내 언어를 지원하나?"를 걱정할 필요가 없습니다.

#### 언어별 SDK와 자동 계측
Java, Python, Go, Node.js 등 주요 언어별로 공식 SDK가 제공됩니다. 특히 Java Agent는 `-javaagent` 옵션만 추가하면 코드 변경 없이 Kafka, HTTP, JDBC 등의 라이브러리를 자동으로 계측합니다. 이는 레거시 애플리케이션에도 관찰 가능성을 쉽게 추가할 수 있다는 의미입니다.

### 1.3 Redpanda에서 OpenTelemetry의 의미

Redpanda는 Kafka 호환 메시징 플랫폼이므로, 메시지가 어떻게 흐르는지를 추적하는 것이 핵심입니다. OpenTelemetry를 통해 다음을 달성할 수 있습니다.

**메시지 흐름 추적**: 주문 서비스에서 발행한 메시지가 결제 서비스에서 얼마나 지연되었는지, 재시도가 발생했는지를 하나의 Trace로 확인할 수 있습니다. 전체 메시지 처리 시간이 3초인데, 그 중 2.5초가 결제 외부 API 호출에서 발생했다면, 이는 결제 서비스의 타임아웃 설정을 조정해야 한다는 신호입니다.

**장애 원인 분석**: 메시지 처리 중 예외가 발생했을 때, 해당 Span에 에러 정보가 기록됩니다. Jaeger UI에서 빨간색으로 표시된 Span을 클릭하면 정확히 어느 단계에서 어떤 에러가 발생했는지 스택 트레이스와 함께 볼 수 있습니다.

**성능 병목 식별**: Consumer가 메시지를 읽는 시간, 비즈니스 로직 처리 시간, DB 저장 시간을 각각 Span으로 분리하면, 어느 부분이 느린지 시각적으로 확인할 수 있습니다. 전체 처리 시간의 80%가 DB 저장에서 발생한다면, 배치 처리나 인덱스 최적화를 고려해야 합니다.

---

## 2. Redpanda Cloud의 OpenTelemetry 지원

### 2.1 OpenTelemetry JSON 형식 내보내기

Redpanda Cloud는 트레이스 데이터를 OpenTelemetry JSON 형식으로 내보낼 수 있습니다. 이는 Redpanda 브로커 자체의 내부 동작(메시지 수신, 저장, 전송)을 추적할 수 있다는 의미입니다. 클라이언트 측에서 발행한 메시지가 브로커에 도착하여 디스크에 쓰여지고, Consumer에게 전달되는 전체 과정을 Redpanda 관점에서 확인할 수 있습니다.

### 2.2 Jaeger, Grafana Tempo 연동

Redpanda Cloud에서 내보낸 트레이스는 Jaeger나 Grafana Tempo 같은 트레이스 백엔드로 전송됩니다. Jaeger는 Uber에서 개발한 오픈소스 분산 추적 시스템으로, UI가 직관적이고 설정이 간단하여 개발 환경에서 많이 사용됩니다. Grafana Tempo는 Grafana Labs에서 개발한 대규모 트레이스 스토리지로, 메트릭과 로그를 함께 조회할 수 있어 프로덕션 환경에서 선호됩니다.

**연동 예시**:
```yaml
# Redpanda Cloud 설정 (웹 콘솔에서 설정)
exporter:
  type: otlp_http
  endpoint: https://tempo-gateway.example.com/v1/traces
  headers:
    Authorization: "Bearer YOUR_TOKEN"
```

Redpanda Cloud 웹 콘솔에서 "Telemetry" 섹션으로 이동하여 OTLP 엔드포인트를 설정하면, Redpanda 브로커의 내부 동작이 트레이스로 수집됩니다. 이를 통해 "메시지가 브로커에 도착한 시점"과 "Consumer가 가져간 시점" 사이의 지연을 정확히 측정할 수 있습니다.

---

## 3. Redpanda Connect의 OpenTelemetry Collector Tracer

Redpanda Connect(구 Benthos)는 스트림 처리 파이프라인 도구입니다. 메시지를 입력받아 변환하고 출력하는 과정을 YAML로 정의할 수 있습니다. 이 파이프라인의 각 단계를 트레이싱하려면 OTel Tracer를 설정합니다.

### 3.1 기본 설정

```yaml
# Redpanda Connect 파이프라인
input:
  kafka:
    addresses: ["localhost:9092"]
    topics: ["orders"]
    consumer_group: "order-processor"

pipeline:
  processors:
    - bloblang: |
        root = this
        root.processed_at = now()

output:
  http_client:
    url: "http://payment-service/api/payments"
    verb: POST

# OpenTelemetry Tracer 설정
tracer:
  open_telemetry_collector:
    grpc:
      - address: localhost:4317
    http:
      - address: http://localhost:4318
    sampling:
      enabled: true
      ratio: 0.1  # 프로덕션: 10% 샘플링
```

이 설정은 Redpanda Connect 파이프라인의 각 단계(입력 → 처리 → 출력)를 Span으로 기록합니다. `input.kafka`에서 메시지를 읽는 시간, `pipeline.processors`에서 변환하는 시간, `output.http_client`로 전송하는 시간이 각각 별도의 Span으로 생성됩니다. 전체 처리 시간이 500ms인데 그중 480ms가 HTTP 전송이라면, 외부 API의 응답 시간이 병목임을 알 수 있습니다.

### 3.2 gRPC vs HTTP 엔드포인트

OpenTelemetry Collector는 gRPC(포트 4317)와 HTTP(포트 4318) 두 가지 프로토콜을 지원합니다. gRPC는 HTTP/2 기반으로 더 효율적이지만, 일부 방화벽이나 프록시에서 차단될 수 있습니다. HTTP는 HTTP/1.1 기반으로 호환성이 높지만, 대량의 트레이스를 보낼 때 gRPC보다 오버헤드가 큽니다. 프로덕션 환경에서는 gRPC를 권장하며, 네트워크 제약이 있는 경우 HTTP를 사용합니다.

```yaml
# gRPC만 사용 (권장)
tracer:
  open_telemetry_collector:
    grpc:
      - address: otel-collector:4317

# HTTP만 사용 (방화벽 제약 시)
tracer:
  open_telemetry_collector:
    http:
      - address: http://otel-collector:4318

# 둘 다 사용 (Failover)
tracer:
  open_telemetry_collector:
    grpc:
      - address: primary-collector:4317
    http:
      - address: http://backup-collector:4318
```

### 3.3 샘플링 설정으로 프로덕션 오버헤드 관리

모든 요청을 추적하면 트레이스 데이터가 폭증하여 스토리지 비용이 증가하고, 네트워크 오버헤드가 발생합니다. 샘플링은 일정 비율의 요청만 추적하여 오버헤드를 줄입니다.

```yaml
tracer:
  open_telemetry_collector:
    grpc:
      - address: localhost:4317
    sampling:
      enabled: true
      ratio: 0.1  # 10%만 추적
```

**샘플링 비율 선택 가이드**:
- **개발 환경**: `ratio: 1.0` (100%) - 모든 요청을 추적하여 문제를 빠르게 발견합니다.
- **스테이징 환경**: `ratio: 0.5` (50%) - 충분한 샘플로 테스트하면서 비용을 절반으로 줄입니다.
- **프로덕션 환경**: `ratio: 0.1` (10%) - 통계적으로 충분한 샘플을 유지하면서 오버헤드를 최소화합니다.
- **초고트래픽 환경**: `ratio: 0.01` (1%) - 초당 수만 건의 요청이 있는 경우, 1%만 추적해도 충분한 데이터를 얻을 수 있습니다.

10% 샘플링은 평균 지연 시간, 에러율, P99 지연 시간 등의 통계를 신뢰할 수 있는 수준으로 유지하면서도 오버헤드를 90% 줄일 수 있습니다. 단, 특정 사용자의 요청을 100% 추적하고 싶다면 Head-Based Sampling 대신 Tail-Based Sampling을 사용해야 합니다.

### 3.4 버전 요구사항

Redpanda Connect v4.25.0 이상에서 `open_telemetry_collector` tracer가 지원됩니다. 이전 버전을 사용 중이라면 업그레이드가 필요합니다.

```bash
# 버전 확인
rpk connect --version

# Docker 이미지로 최신 버전 사용
docker run --rm docker.redpanda.com/redpandadata/connect:v4.37.0 --version
```

---

## 4. Spring Boot + Kafka + OpenTelemetry 분산 추적

Spring Boot 애플리케이션에서 Kafka(Redpanda)와 OpenTelemetry를 통합하는 방법은 세 가지가 있습니다. 각 방식은 장단점이 다르므로 프로젝트 상황에 맞게 선택합니다.

### 4.1 방식 1: OpenTelemetry Java Agent (Zero-Code)

**장점**: 코드 변경이 전혀 없습니다. JVM 시작 시 `-javaagent` 옵션만 추가하면 됩니다.
**단점**: 세밀한 제어가 어렵고, 에이전트 버전 관리가 필요합니다.
**적합한 경우**: 레거시 애플리케이션, 빠른 POC, 코드 수정 불가 환경

```bash
# OpenTelemetry Java Agent 다운로드
wget https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar

# 애플리케이션 실행
java -javaagent:opentelemetry-javaagent.jar \
  -Dotel.service.name=order-service \
  -Dotel.exporter.otlp.endpoint=http://localhost:4317 \
  -Dotel.exporter.otlp.protocol=grpc \
  -Dotel.traces.sampler=parentbased_traceidratio \
  -Dotel.traces.sampler.arg=0.1 \
  -jar order-service.jar
```

**자동 계측 대상**:
- `kafka-clients` 라이브러리: Producer와 Consumer의 모든 호출이 자동으로 Span으로 기록됩니다.
- `spring-web`: HTTP 요청/응답이 자동으로 추적됩니다.
- `jdbc`: 데이터베이스 쿼리가 자동으로 추적됩니다.
- `http-client`: 외부 HTTP 호출이 자동으로 추적됩니다.

**ProducerRecord 헤더에 trace context 자동 주입**:
Java Agent는 `KafkaProducer.send()`를 호출할 때, ProducerRecord의 헤더에 `traceparent`와 `tracestate` 값을 자동으로 추가합니다. 이는 W3C Trace Context 표준 형식이며, Consumer 측에서 이 헤더를 읽어 동일한 TraceID로 Span을 연결합니다.

```
# ProducerRecord 헤더 (자동 추가됨)
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
            ^^ ^^ trace-id                       ^^ span-id         ^^ sampled

- trace-id: 전체 분산 트레이스의 고유 ID
- span-id: 현재 Span의 고유 ID
- sampled: 01이면 추적 중, 00이면 샘플링에서 제외
```

**ConsumerRecord 헤더에서 trace context 자동 추출**:
Consumer가 메시지를 읽을 때, Java Agent는 헤더에서 `traceparent`를 추출하여 새로운 Span의 부모로 설정합니다. 이를 통해 Producer → Broker → Consumer 전체 흐름이 하나의 Trace로 연결됩니다.

**PRODUCER/CONSUMER span 자동 생성**:
- `PRODUCER` Span: `KafkaProducer.send()` 호출 시점부터 브로커가 ack를 보내는 시점까지의 시간을 측정합니다. 이는 네트워크 지연과 브로커의 처리 시간을 포함합니다.
- `CONSUMER` Span: `KafkaConsumer.poll()`로 메시지를 읽는 시점부터 다음 `poll()` 호출 전까지의 시간을 측정합니다. 이는 메시지 처리 시간을 포함합니다.

### 4.2 방식 2: Spring Boot Starter for OpenTelemetry

**장점**: Spring Boot 생태계와 자연스럽게 통합되며, Auto-configuration이 지원됩니다.
**단점**: 의존성 버전 충돌 가능성이 있고, 문서가 아직 부족합니다.
**적합한 경우**: Spring Boot 3.x+ 프로젝트, Spring Cloud 사용 환경

```xml
<!-- Maven -->
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
    <version>2.11.0-alpha</version>
</dependency>
```

```yaml
# application.yml
otel:
  sdk:
    disabled: false
  traces:
    exporter: otlp
  metrics:
    exporter: otlp
  exporter:
    otlp:
      endpoint: http://localhost:4318
```

이 방식은 Spring Boot의 `@Bean`으로 `OpenTelemetry` 인스턴스를 자동으로 생성하며, `application.yml`의 설정을 읽어 초기화합니다. OTLP 형식으로 Micrometer 시그널을 내보내므로, Spring Actuator의 메트릭을 OTel로 전환할 수 있습니다.

**OTLP 형식으로 Micrometer 시그널 내보내기**:
Spring Boot는 Micrometer를 통해 메트릭을 수집합니다. 이 Starter는 Micrometer의 메트릭을 OTLP 형식으로 변환하여 OTel Collector로 전송합니다. 예를 들어, `http.server.requests` 메트릭이 `http_server_requests_seconds_count`와 `http_server_requests_seconds_sum`으로 내보내집니다.

**Spring 프로젝트의 Observation API 활용**:
Spring 6.0+와 Spring Boot 3.0+는 Observation API를 도입했습니다. 이는 메트릭과 트레이스를 통합하는 추상화 레이어입니다. Observation API를 사용하면 하나의 코드로 메트릭과 트레이스를 동시에 기록할 수 있습니다.

```java
@Service
public class OrderService {
    private final ObservationRegistry registry;

    public OrderService(ObservationRegistry registry) {
        this.registry = registry;
    }

    public Order createOrder(CreateOrderRequest request) {
        return Observation
            .createNotStarted("order.create", registry)
            .lowCardinalityKeyValue("order.type", request.getType())
            .observe(() -> {
                // 비즈니스 로직
                return orderRepository.save(new Order(request));
            });
    }
}
```

이 코드는 `order.create` Span을 생성하며, 동시에 `order.create.seconds` 메트릭도 기록합니다. OpenTelemetry Starter가 있으면 자동으로 OTLP로 내보내집니다.

### 4.3 방식 3: Micrometer Tracing Bridge (권장)

**장점**: Spring Boot 3.x의 공식 트레이싱 방식이며, 안정적이고 문서가 충실합니다.
**단점**: Micrometer 추상화 레이어가 추가되어 순수 OTel보다 약간의 오버헤드가 있습니다.
**적합한 경우**: 대부분의 Spring Boot 3.x 프로젝트에서 권장합니다.

```xml
<!-- Maven pom.xml -->
<dependencies>
    <!-- Micrometer Tracing Bridge for OpenTelemetry -->
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-tracing-bridge-otel</artifactId>
    </dependency>

    <!-- OpenTelemetry OTLP Exporter -->
    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-exporter-otlp</artifactId>
    </dependency>

    <!-- (선택) Zipkin 형식으로 내보내려면 -->
    <dependency>
        <groupId>io.zipkin.reporter2</groupId>
        <artifactId>zipkin-reporter-brave</artifactId>
    </dependency>
</dependencies>
```

```gradle
// Gradle build.gradle
dependencies {
    // Micrometer Tracing Bridge for OpenTelemetry
    implementation 'io.micrometer:micrometer-tracing-bridge-otel'

    // OpenTelemetry OTLP Exporter
    implementation 'io.opentelemetry:opentelemetry-exporter-otlp'

    // Spring Boot Actuator (메트릭 노출용)
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
}
```

```yaml
# application.yml
spring:
  application:
    name: order-service

management:
  tracing:
    sampling:
      probability: 1.0  # 개발: 100%, 프로덕션: 0.1
  otlp:
    tracing:
      endpoint: http://localhost:4318/v1/traces
    metrics:
      export:
        enabled: true
        step: 30s  # 30초마다 메트릭 전송

logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]"
```

**핵심: Spring Kafka는 이미 Micrometer Observation API로 계측되어 있으므로 bridge만 추가하면 Kafka 메시지의 produce/consume 추적이 자동 활성화됨**

Spring Kafka 2.9+ 버전은 내부적으로 `KafkaTemplate.send()`와 `@KafkaListener`에 Observation API를 적용했습니다. 따라서 Micrometer Tracing Bridge를 의존성에 추가하는 순간, 별도의 설정 없이 다음이 자동으로 작동합니다:

1. **Producer Span 생성**: `kafkaTemplate.send("orders", order)`를 호출하면 `kafka.producer.send` Span이 생성됩니다.
2. **Trace Context 주입**: `traceparent` 헤더가 ProducerRecord에 자동으로 추가됩니다.
3. **Consumer Span 생성**: `@KafkaListener`가 메시지를 받으면 `kafka.consumer.receive` Span이 생성됩니다.
4. **Trace Context 추출**: ConsumerRecord 헤더에서 `traceparent`를 읽어 부모 Span과 연결됩니다.

**추가 코드 변경 불필요** - 의존성 추가와 `application.yml` 설정만으로 Kafka 메시지의 전체 흐름이 추적됩니다.

#### 예제 코드

```java
// Producer (Order Service)
@Service
public class OrderPublisher {
    private final KafkaTemplate<String, Order> kafkaTemplate;

    public OrderPublisher(KafkaTemplate<String, Order> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publishOrder(Order order) {
        // Span이 자동으로 생성되고, traceparent 헤더가 주입됨
        kafkaTemplate.send("orders", order.getId(), order);
    }
}

// Consumer (Payment Service)
@Service
public class PaymentListener {
    private final PaymentService paymentService;

    public PaymentListener(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @KafkaListener(topics = "orders", groupId = "payment-service")
    public void onOrder(ConsumerRecord<String, Order> record) {
        // Span이 자동으로 생성되고, traceparent 헤더가 추출됨
        Order order = record.value();
        paymentService.processPayment(order);
    }
}
```

이 코드에는 OpenTelemetry 관련 코드가 전혀 없지만, Jaeger UI에서 다음과 같은 Trace를 볼 수 있습니다:

```
[order-service] kafka.producer.send (topic: orders) - 15ms
  └─ [payment-service] kafka.consumer.receive - 250ms
      └─ [payment-service] PaymentService.processPayment - 240ms
```

---

## 5. 통합 아키텍처 (Docker Compose)

전체 관찰 가능성 스택을 로컬에서 실행하는 Docker Compose 예제입니다. Redpanda, OTel Collector, Jaeger, Grafana를 모두 포함합니다.

### 5.1 Docker Compose 파일

```yaml
# docker-compose.yml
version: "3.8"

services:
  # Redpanda (Kafka 호환 메시징 플랫폼)
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v25.1.1
    container_name: redpanda
    command:
      - redpanda
      - start
      - --smp 1
      - --memory 1G
      - --reserve-memory 0M
      - --overprovisioned
      - --node-id 0
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr internal://redpanda:8082,external://localhost:18082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:18081
      - --rpc-addr redpanda:33145
      - --advertise-rpc-addr redpanda:33145
    ports:
      - "19092:19092"  # Kafka API
      - "18081:18081"  # Schema Registry
      - "18082:18082"  # HTTP Proxy
      - "9644:9644"    # Prometheus Metrics
    healthcheck:
      test: ["CMD-SHELL", "rpk cluster health | grep -q 'Healthy:.*true'"]
      interval: 10s
      timeout: 5s
      retries: 5

  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.96.0
    container_name: otel-collector
    command: ["--config=/etc/otelcol/config.yaml"]
    ports:
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
      - "8888:8888"   # Prometheus metrics (Collector 자체 메트릭)
      - "8889:8889"   # Prometheus exporter (수집한 메트릭)
    volumes:
      - ./otel-collector-config.yaml:/etc/otelcol/config.yaml:ro
    depends_on:
      - jaeger

  # Jaeger (분산 추적 UI)
  jaeger:
    image: jaegertracing/all-in-one:1.54
    container_name: jaeger
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    ports:
      - "16686:16686"  # Jaeger UI
      - "14250:14250"  # gRPC receiver (Jaeger native)
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:16686"]
      interval: 10s
      timeout: 5s
      retries: 3

  # Grafana (메트릭 시각화)
  grafana:
    image: grafana/grafana:10.3.0
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/datasources.yaml:/etc/grafana/provisioning/datasources/datasources.yaml:ro
      - ./grafana/dashboards.yaml:/etc/grafana/provisioning/dashboards/dashboards.yaml:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
    depends_on:
      - jaeger
      - otel-collector

  # Redpanda Console (Redpanda UI)
  console:
    image: docker.redpanda.com/redpandadata/console:v2.8.0
    container_name: redpanda-console
    ports:
      - "8080:8080"
    environment:
      - KAFKA_BROKERS=redpanda:9092
      - KAFKA_SCHEMAREGISTRY_ENABLED=true
      - KAFKA_SCHEMAREGISTRY_URLS=http://redpanda:8081
    depends_on:
      - redpanda
```

**각 서비스의 역할**:
- **Redpanda**: 메시지 브로커로, 애플리케이션 간 비동기 통신을 담당합니다. Prometheus 메트릭은 9644 포트에서 노출됩니다.
- **OTel Collector**: 트레이스와 메트릭을 수집하여 Jaeger, Prometheus 등으로 라우팅합니다. 4317(gRPC), 4318(HTTP) 포트로 OTLP 데이터를 받습니다.
- **Jaeger**: 트레이스를 저장하고 시각화합니다. 16686 포트로 웹 UI에 접근합니다.
- **Grafana**: Prometheus 메트릭을 시각화합니다. Jaeger를 데이터소스로 추가하면 트레이스도 조회할 수 있습니다.
- **Redpanda Console**: Redpanda 클러스터의 토픽, 메시지, 컨슈머 그룹을 관리하는 웹 UI입니다.

### 5.2 OpenTelemetry Collector 설정

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  # Redpanda 메트릭 수집
  prometheus:
    config:
      scrape_configs:
        - job_name: 'redpanda'
          scrape_interval: 15s
          static_configs:
            - targets: ['redpanda:9644']
          metrics_path: /public_metrics

processors:
  # 배치 처리로 성능 최적화
  batch:
    timeout: 1s
    send_batch_size: 1024

  # 리소스 속성 추가
  resource:
    attributes:
      - key: service.namespace
        value: "redpanda-demo"
        action: upsert

  # 메모리 제한 (OOM 방지)
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
    spike_limit_mib: 128

exporters:
  # Jaeger로 트레이스 전송
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

  # Prometheus 형식으로 메트릭 노출
  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: otel
    const_labels:
      environment: local

  # 디버깅용 로깅
  logging:
    loglevel: info

service:
  pipelines:
    # 트레이스 파이프라인
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, resource]
      exporters: [otlp/jaeger, logging]

    # 메트릭 파이프라인
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch, resource]
      exporters: [prometheus, logging]
```

**Receivers**: 데이터를 받는 입구입니다. `otlp` receiver는 애플리케이션에서 보낸 트레이스와 메트릭을 받습니다. `prometheus` receiver는 Redpanda의 메트릭을 스크랩합니다.

**Processors**: 데이터를 변환하거나 필터링합니다. `batch` processor는 여러 개의 Span을 묶어서 전송하여 네트워크 오버헤드를 줄입니다. `memory_limiter`는 메모리 사용량이 512MB를 넘으면 데이터를 버려서 OOM을 방지합니다.

**Exporters**: 데이터를 내보내는 출구입니다. `otlp/jaeger`는 Jaeger로 트레이스를 전송하고, `prometheus`는 메트릭을 Prometheus 형식으로 노출합니다.

**Service Pipelines**: Receiver → Processor → Exporter의 흐름을 정의합니다. `traces` 파이프라인은 트레이스를 처리하고, `metrics` 파이프라인은 메트릭을 처리합니다.

### 5.3 Grafana 데이터소스 설정

```yaml
# grafana/datasources.yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://otel-collector:8889
    isDefault: true

  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    jsonData:
      tracesToMetrics:
        datasourceUid: prometheus
        tags:
          - key: service.name
            value: service
```

**Prometheus 데이터소스**: OTel Collector의 Prometheus exporter(8889 포트)에서 메트릭을 가져옵니다. 기본 데이터소스로 설정됩니다.

**Jaeger 데이터소스**: Jaeger UI(16686 포트)에서 트레이스를 가져옵니다. `tracesToMetrics` 설정을 통해 Trace에서 Metrics로 점프할 수 있습니다. 예를 들어, 느린 요청의 Trace를 보다가 해당 서비스의 전체 지연 시간 메트릭을 확인할 수 있습니다.

### 5.4 실행 및 확인

```bash
# 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f otel-collector

# 서비스 URL
# - Redpanda Console: http://localhost:8080
# - Jaeger UI: http://localhost:16686
# - Grafana: http://localhost:3000 (admin/admin)
# - OTel Collector Metrics: http://localhost:8888/metrics

# 헬스체크
curl http://localhost:16686/   # Jaeger
curl http://localhost:8888/metrics  # OTel Collector
curl http://localhost:9644/public_metrics  # Redpanda

# 정리
docker-compose down -v
```

---

## 참고

- [Redpanda Connect OpenTelemetry Tracer](https://docs.redpanda.com/redpanda-connect/components/tracers/open_telemetry_collector/)
- [OpenTelemetry with Spring Boot (Spring Blog, 2024)](https://spring.io/blog/2024/11/18/opentelemetry-with-spring-boot/)
- [Spring Boot Tracing Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.micrometer-tracing)
