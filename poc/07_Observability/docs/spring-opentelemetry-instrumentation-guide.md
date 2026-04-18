# Spring Boot OpenTelemetry Instrumentation 가이드

> OpenTelemetry Java Agent를 활용한 Automatic Instrumentation과 Manual Instrumentation의 차이점과 실무 적용 방법

---

## 목차

1. [개요](#1-개요)
2. [Automatic Instrumentation](#2-automatic-instrumentation)
3. [Manual Instrumentation](#3-manual-instrumentation)
4. [Auto vs Manual 비교](#4-auto-vs-manual-비교)
5. [실무 적용 패턴](#5-실무-적용-패턴)
6. [Trace 결과 예시](#6-trace-결과-예시)

---

## 1. 개요

OpenTelemetry는 두 가지 계측 방식을 제공합니다.

| 방식 | 설명 | 코드 수정 |
|------|------|:---------:|
| **Automatic (Zero-code)** | Java Agent가 런타임에 바이트코드를 수정하여 자동 계측 | 불필요 |
| **Manual (Code-based)** | 개발자가 직접 코드로 Span, Metric 등을 생성 | 필요 |

### 아키텍처 개요

```
┌────────────────────────────────────────────────────────────────────┐
│                        Spring Boot Application                      │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                   Your Business Logic                        │  │
│   │                                                              │  │
│   │   OrderService.createOrder()  ─────┐                        │  │
│   │         │                          │                        │  │
│   │         ▼                          │  ❌ Auto로 안 잡힘      │  │
│   │   validateOrder()                  │     (Manual 필요)       │  │
│   │         │                          │                        │  │
│   │         ▼                          │                        │  │
│   │   calculateDiscount()        ──────┘                        │  │
│   │         │                                                    │  │
│   └─────────┼────────────────────────────────────────────────────┘  │
│             │                                                       │
│             ▼                                                       │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │              Framework/Library Layer                         │  │
│   │                                                              │  │
│   │   • Feign Client      ──────┐                               │  │
│   │   • WebClient               │  ✅ Auto로 자동 계측           │  │
│   │   • RestTemplate            │     (Java Agent가 처리)        │  │
│   │   • gRPC Stub         ──────┘                               │  │
│   │   • JDBC/JPA                                                 │  │
│   │   • Kafka Producer/Consumer                                  │  │
│   │                                                              │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. Automatic Instrumentation

### 2.1 Java Agent 설정

#### Dockerfile 방식

```dockerfile
FROM openjdk:17-jdk-slim

# OpenTelemetry Java Agent 다운로드
ADD https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar /app/opentelemetry-javaagent.jar

# Java Agent 설정
ENV JAVA_TOOL_OPTIONS="-javaagent:/app/opentelemetry-javaagent.jar"

# 서비스 설정
ENV OTEL_SERVICE_NAME="my-spring-service"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"

COPY target/app.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

#### Docker Compose 방식

```yaml
version: '3.8'
services:
  my-service:
    build: .
    environment:
      - JAVA_TOOL_OPTIONS=-javaagent:/app/opentelemetry-javaagent.jar
      - OTEL_SERVICE_NAME=my-spring-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
      - OTEL_METRICS_EXPORTER=otlp
      - OTEL_LOGS_EXPORTER=otlp
```

#### 로컬 실행 방식

```bash
java -javaagent:path/to/opentelemetry-javaagent.jar \
     -Dotel.service.name=my-spring-service \
     -Dotel.exporter.otlp.endpoint=http://localhost:4317 \
     -jar app.jar
```

### 2.2 자동 계측 대상 라이브러리

#### HTTP 통신

| 라이브러리 | 자동 계측 | 생성되는 Span |
|------------|:---------:|---------------|
| **Feign Client** | ✅ | `HTTP GET /api/users` |
| **WebClient** | ✅ | `HTTP POST /api/orders` |
| **RestTemplate** | ✅ | `HTTP PUT /api/products/{id}` |
| **OkHttp** | ✅ | `HTTP DELETE /api/items` |
| **Apache HttpClient** | ✅ | `HTTP PATCH /api/settings` |

#### 웹 서버

| 라이브러리 | 자동 계측 | 생성되는 Span |
|------------|:---------:|---------------|
| **Spring MVC** | ✅ | `GET /api/orders/{id}` |
| **Spring WebFlux** | ✅ | `POST /api/orders` |
| **Servlet** | ✅ | `HTTP GET` |

#### 데이터베이스

| 라이브러리 | 자동 계측 | 생성되는 Span |
|------------|:---------:|---------------|
| **JDBC** | ✅ | `SELECT mydb.orders` |
| **JPA/Hibernate** | ✅ | `INSERT mydb.orders` |
| **MyBatis** | ✅ | `UPDATE mydb.users` |
| **R2DBC** | ✅ | `DELETE mydb.items` |

#### 메시징

| 라이브러리 | 자동 계측 | 생성되는 Span |
|------------|:---------:|---------------|
| **Kafka Producer** | ✅ | `orders-topic publish` |
| **Kafka Consumer** | ✅ | `orders-topic process` |
| **RabbitMQ** | ✅ | `order.queue publish` |
| **JMS** | ✅ | `jms.queue send` |

#### 캐시 & 기타

| 라이브러리 | 자동 계측 | 생성되는 Span |
|------------|:---------:|---------------|
| **Redis (Jedis)** | ✅ | `GET` |
| **Redis (Lettuce)** | ✅ | `SET` |
| **gRPC** | ✅ | `grpc.service/Method` |
| **AWS SDK** | ✅ | `S3.PutObject` |

### 2.3 자동 생성되는 메트릭

```
# JVM 메트릭
jvm_memory_used_bytes
jvm_memory_committed_bytes
jvm_gc_duration_seconds
jvm_threads_current

# HTTP 서버 메트릭
http_server_request_duration_seconds
http_server_active_requests

# HTTP 클라이언트 메트릭
http_client_request_duration_seconds

# DB 메트릭
db_client_connections_usage
```

---

## 3. Manual Instrumentation

### 3.1 의존성 추가

```xml
<!-- pom.xml -->
<dependencies>
    <!-- OpenTelemetry API -->
    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-api</artifactId>
    </dependency>
    
    <!-- Instrumentation Annotations (@WithSpan) -->
    <dependency>
        <groupId>io.opentelemetry.instrumentation</groupId>
        <artifactId>opentelemetry-instrumentation-annotations</artifactId>
    </dependency>
</dependencies>

<!-- BOM으로 버전 관리 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.opentelemetry</groupId>
            <artifactId>opentelemetry-bom</artifactId>
            <version>1.40.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

```groovy
// build.gradle
dependencies {
    implementation platform('io.opentelemetry:opentelemetry-bom:1.40.0')
    implementation 'io.opentelemetry:opentelemetry-api'
    implementation 'io.opentelemetry.instrumentation:opentelemetry-instrumentation-annotations'
}
```

### 3.2 현재 Span 접근 및 Attribute 추가

```java
import io.opentelemetry.api.trace.Span;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @PostMapping
    public Order createOrder(@RequestBody OrderRequest request) {
        // Auto-instrumented Span (Spring MVC)에 접근
        Span currentSpan = Span.current();
        
        // 비즈니스 컨텍스트 추가
        currentSpan.setAttribute("order.type", request.getType());
        currentSpan.setAttribute("order.itemCount", request.getItems().size());
        currentSpan.setAttribute("customer.id", request.getCustomerId());
        
        return orderService.createOrder(request);
    }
}
```

### 3.3 @WithSpan 어노테이션 사용

가장 간단한 Manual Instrumentation 방법입니다.

```java
import io.opentelemetry.instrumentation.annotations.WithSpan;
import io.opentelemetry.instrumentation.annotations.SpanAttribute;

@Service
public class OrderService {

    // 메서드 호출 시 자동으로 Span 생성
    @WithSpan("validateOrder")
    public void validateOrder(
            @SpanAttribute("order.id") String orderId,
            @SpanAttribute("order.amount") BigDecimal amount) {
        
        // 검증 로직
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidOrderException("Amount must be positive");
        }
    }
    
    @WithSpan("calculateDiscount")
    public BigDecimal calculateDiscount(
            @SpanAttribute("customer.tier") String customerTier,
            @SpanAttribute("order.amount") BigDecimal amount) {
        
        // 할인 계산 로직
        return switch (customerTier) {
            case "GOLD" -> amount.multiply(new BigDecimal("0.1"));
            case "SILVER" -> amount.multiply(new BigDecimal("0.05"));
            default -> BigDecimal.ZERO;
        };
    }
}
```

### 3.4 Tracer를 이용한 직접 Span 생성

세밀한 제어가 필요할 때 사용합니다.

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.context.Scope;

@Service
public class OrderService {

    // Tracer 인스턴스 획득
    private final Tracer tracer = GlobalOpenTelemetry.getTracer("order-service");
    
    public Order createOrder(OrderRequest request) {
        // 1. 새 Span 생성 및 시작
        Span span = tracer.spanBuilder("createOrder")
                .setAttribute("order.type", request.getType())
                .setAttribute("customer.id", request.getCustomerId())
                .startSpan();
        
        // 2. Span을 현재 Context에 설정
        try (Scope scope = span.makeCurrent()) {
            
            // 비즈니스 로직 실행
            validateOrder(request);
            BigDecimal discount = calculateDiscount(request);
            
            Order order = processOrder(request, discount);
            
            // 3. 결과 Attribute 추가
            span.setAttribute("order.id", order.getId());
            span.setAttribute("order.totalAmount", order.getTotalAmount().doubleValue());
            
            return order;
            
        } catch (Exception e) {
            // 4. 에러 처리
            span.setStatus(StatusCode.ERROR, e.getMessage());
            span.recordException(e);
            throw e;
            
        } finally {
            // 5. Span 종료 (필수!)
            span.end();
        }
    }
}
```

### 3.5 Span Event 추가

특정 시점의 이벤트를 기록합니다.

```java
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.api.common.AttributeKey;

@Service
public class PaymentService {

    public PaymentResult processPayment(PaymentRequest request) {
        Span span = Span.current();
        
        // 이벤트 추가: 결제 시작
        span.addEvent("payment.started", Attributes.of(
            AttributeKey.stringKey("payment.method"), request.getMethod(),
            AttributeKey.doubleKey("payment.amount"), request.getAmount().doubleValue()
        ));
        
        try {
            PaymentResult result = paymentGateway.charge(request);
            
            // 이벤트 추가: 결제 완료
            span.addEvent("payment.completed", Attributes.of(
                AttributeKey.stringKey("payment.transactionId"), result.getTransactionId(),
                AttributeKey.stringKey("payment.status"), result.getStatus()
            ));
            
            return result;
            
        } catch (PaymentException e) {
            // 이벤트 추가: 결제 실패
            span.addEvent("payment.failed", Attributes.of(
                AttributeKey.stringKey("error.code"), e.getErrorCode(),
                AttributeKey.stringKey("error.message"), e.getMessage()
            ));
            throw e;
        }
    }
}
```

### 3.6 Custom Metrics 생성

```java
import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.metrics.LongHistogram;
import io.opentelemetry.api.common.Attributes;

@Service
public class OrderMetricsService {

    private final Meter meter = GlobalOpenTelemetry.getMeter("order-service");
    
    // Counter: 주문 수 카운트
    private final LongCounter orderCounter = meter
            .counterBuilder("app.orders.total")
            .setDescription("Total number of orders")
            .setUnit("{orders}")
            .build();
    
    // Histogram: 주문 금액 분포
    private final LongHistogram orderAmountHistogram = meter
            .histogramBuilder("app.orders.amount")
            .setDescription("Order amount distribution")
            .setUnit("KRW")
            .ofLongs()
            .build();
    
    public void recordOrder(Order order) {
        Attributes attributes = Attributes.of(
            AttributeKey.stringKey("order.type"), order.getType(),
            AttributeKey.stringKey("order.status"), order.getStatus(),
            AttributeKey.stringKey("customer.tier"), order.getCustomerTier()
        );
        
        // 카운터 증가
        orderCounter.add(1, attributes);
        
        // 히스토그램에 값 기록
        orderAmountHistogram.record(order.getTotalAmount().longValue(), attributes);
    }
}
```

---

## 4. Auto vs Manual 비교

### 4.1 적용 대상 비교

| 구분 | Auto (Java Agent) | Manual (코드 작성) |
|------|-------------------|-------------------|
| **대상** | 프레임워크/라이브러리 호출 | 비즈니스 로직, 내부 메서드 |
| **장점** | 코드 수정 없음, 빠른 적용 | 세밀한 제어, 비즈니스 컨텍스트 추가 |
| **단점** | 커스텀 불가, 내부 로직 미추적 | 코드 침투적, 개발 공수 필요 |
| **예시** | Feign, WebClient, JDBC | 주문생성, 할인계산, 검증로직 |

### 4.2 계측 경계 요약

```
┌─────────────────────────────────────────────────────────────────┐
│                     Instrumentation Boundary                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              ❌ Auto로 계측 불가 (Manual 필요)              │  │
│  │                                                            │  │
│  │   • 비즈니스 로직 메서드 (createOrder, validateOrder)      │  │
│  │   • 내부 유틸리티 메서드                                    │  │
│  │   • 조건 분기, 반복문 내부 로직                             │  │
│  │   • 비즈니스 이벤트 (결제완료, 재고부족 등)                  │  │
│  │   • Custom Metrics (주문수, 금액 분포 등)                   │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              ✅ Auto로 자동 계측 (코드 수정 불필요)          │  │
│  │                                                            │  │
│  │   • HTTP Client: Feign, WebClient, RestTemplate           │  │
│  │   • HTTP Server: Spring MVC, WebFlux                      │  │
│  │   • Database: JDBC, JPA, MyBatis                          │  │
│  │   • Messaging: Kafka, RabbitMQ                            │  │
│  │   • Cache: Redis, Memcached                               │  │
│  │   • RPC: gRPC, Dubbo                                      │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. 실무 적용 패턴

### 5.1 권장 하이브리드 패턴

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final Tracer tracer = GlobalOpenTelemetry.getTracer("order-service");
    
    private final PaymentClient paymentClient;      // Feign Client
    private final WebClient inventoryClient;        // WebClient
    private final OrderRepository orderRepository;  // JPA Repository

    public Order createOrder(OrderRequest request) {
        
        // ✅ Manual: 비즈니스 로직 전체를 Span으로 감싸기
        Span span = tracer.spanBuilder("createOrder")
                .setAttribute("order.type", request.getType())
                .setAttribute("customer.id", request.getCustomerId())
                .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            
            // ✅ Manual: 중요한 검증 로직
            validateWithSpan(request);
            
            // ✅ Manual: 할인 계산 로직
            BigDecimal discount = calculateDiscountWithSpan(request);
            
            // ✅ Auto: Feign 호출 → Agent가 자동으로 Child Span 생성
            PaymentResult paymentResult = paymentClient.charge(
                    new PaymentRequest(request.getPaymentInfo(), request.getTotalAmount())
            );
            
            // ✅ Auto: WebClient 호출 → Agent가 자동으로 Child Span 생성
            inventoryClient.post()
                    .uri("/api/inventory/reserve")
                    .bodyValue(new ReserveRequest(request.getItems()))
                    .retrieve()
                    .bodyToMono(Void.class)
                    .block();
            
            // ✅ Auto: JPA save → Agent가 자동으로 DB Span 생성
            Order order = Order.create(request, discount);
            Order savedOrder = orderRepository.save(order);
            
            // ✅ Manual: 결과 Attribute 추가
            span.setAttribute("order.id", savedOrder.getId());
            span.setAttribute("order.finalAmount", savedOrder.getTotalAmount().doubleValue());
            span.addEvent("order.created");
            
            return savedOrder;
            
        } catch (Exception e) {
            span.setStatus(StatusCode.ERROR, e.getMessage());
            span.recordException(e);
            throw e;
        } finally {
            span.end();
        }
    }
    
    @WithSpan("validateOrder")
    private void validateWithSpan(OrderRequest request) {
        Span.current().setAttribute("validation.itemCount", request.getItems().size());
        
        if (request.getItems().isEmpty()) {
            throw new InvalidOrderException("Order must have at least one item");
        }
        // 추가 검증 로직...
    }
    
    @WithSpan("calculateDiscount")
    private BigDecimal calculateDiscountWithSpan(OrderRequest request) {
        Span span = Span.current();
        span.setAttribute("customer.tier", request.getCustomerTier());
        
        BigDecimal discount = switch (request.getCustomerTier()) {
            case "GOLD" -> request.getTotalAmount().multiply(new BigDecimal("0.1"));
            case "SILVER" -> request.getTotalAmount().multiply(new BigDecimal("0.05"));
            default -> BigDecimal.ZERO;
        };
        
        span.setAttribute("discount.amount", discount.doubleValue());
        span.addEvent("discount.calculated");
        
        return discount;
    }
}
```

### 5.2 계층별 적용 가이드

| 계층 | 권장 방식 | 이유 |
|------|-----------|------|
| **Controller** | Auto + Attribute 추가 | Spring MVC가 자동 계측, 요청 파라미터만 추가 |
| **Service** | Manual (주요 메서드) | 비즈니스 로직 경계 명확화 |
| **Repository** | Auto | JPA/MyBatis 자동 계측 |
| **External API** | Auto | Feign/WebClient 자동 계측 |
| **Messaging** | Auto + Event 추가 | Kafka 자동 계측, 비즈니스 이벤트 추가 |

---

## 6. Trace 결과 예시

### 6.1 Jaeger에서 보이는 Trace 구조

```
createOrder (Manual)                                    [250ms]
  │
  ├── validateOrder (Manual - @WithSpan)                [5ms]
  │
  ├── calculateDiscount (Manual - @WithSpan)            [3ms]
  │
  ├── POST payment-service/api/charge (Auto - Feign)    [80ms]
  │     │
  │     └── INSERT payments (Auto - JDBC)               [8ms]
  │
  ├── POST inventory-service/api/reserve (Auto - WebClient) [45ms]
  │     │
  │     └── UPDATE inventory (Auto - JDBC)              [12ms]
  │
  └── INSERT orders (Auto - JPA/JDBC)                   [15ms]
```

### 6.2 Span Attributes 예시

```json
{
  "traceId": "abc123def456",
  "spanId": "span789",
  "operationName": "createOrder",
  "duration": 250,
  "attributes": {
    "order.type": "STANDARD",
    "customer.id": "cust-12345",
    "order.id": "ord-67890",
    "order.finalAmount": 45000.0,
    "validation.itemCount": 3,
    "customer.tier": "GOLD",
    "discount.amount": 5000.0
  },
  "events": [
    { "name": "discount.calculated", "timestamp": "..." },
    { "name": "order.created", "timestamp": "..." }
  ]
}
```

---

## 참고 자료

- [OpenTelemetry Java Agent](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [Supported Libraries](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md)
- [OpenTelemetry Java API](https://opentelemetry.io/docs/languages/java/)
- [OpenTelemetry Demo - Ad Service](https://opentelemetry.io/docs/demo/services/ad/)
