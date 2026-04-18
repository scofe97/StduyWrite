# OpenTelemetry Demo 아키텍처 가이드

> OpenTelemetry Demo (Astronomy Shop) 프로젝트의 전체 아키텍처, 텔레메트리 파이프라인, 데이터 생성 메커니즘 분석

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [서비스 아키텍처](#2-서비스-아키텍처)
3. [텔레메트리 파이프라인](#3-텔레메트리-파이프라인)
4. [Load Generator - 데이터 생성](#4-load-generator---데이터-생성)
5. [Feature Flag 기반 장애 주입](#5-feature-flag-기반-장애-주입)
6. [실행 및 접속 방법](#6-실행-및-접속-방법)

---

## 1. 프로젝트 개요

### 1.1 OpenTelemetry Demo란?

**Astronomy Shop**이라는 가상의 E-Commerce 플랫폼을 구현한 마이크로서비스 데모 프로젝트입니다.

**목적**:
- OpenTelemetry 계측 방법 시연
- 분산 시스템 관측성(Observability) 학습
- Chaos Engineering 실습

**규모**:
- **20개 서비스** (13개 비즈니스 + 7개 인프라)
- **8개 프로그래밍 언어** (Java, Go, Python, Node.js, C#, C++, Rust, PHP)
- **3가지 통신 방식** (gRPC, HTTP, Kafka)

### 1.2 전체 구조도

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                            │
│                              Port 8080                              │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────┐
│                      Frontend Proxy (Envoy)                         │
│                      Load Balancing & Routing                       │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐    ┌────────────────────┐    ┌───────────────────┐
│   Checkout    │    │  Product Catalog   │    │  Recommendation   │
│     (Go)      │    │       (Go)         │    │     (Python)      │
│   Port 5050   │    │    Port 3550       │    │    Port 9001      │
└───────┬───────┘    └────────────────────┘    └───────────────────┘
        │
        ├──────────────────────────────────────────────────┐
        │                    │                    │        │
        ▼                    ▼                    ▼        ▼
┌───────────────┐    ┌───────────────┐    ┌───────────┐ ┌──────────┐
│    Payment    │    │   Shipping    │    │  Currency │ │  Email   │
│   (Node.js)   │    │    (Rust)     │    │   (C++)   │ │ (Python) │
│   Port 7002   │    │  Port 8888    │    │ Port 7001 │ │ Port 6060│
└───────────────┘    └───────────────┘    └───────────┘ └──────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│                         Kafka (9092)                               │
│                    Async Event Streaming                           │
└───────────────────────────────────────────────────────────────────┘
        │
        ├─────────────────────────────┐
        ▼                             ▼
┌───────────────────┐        ┌───────────────────┐
│    Accounting     │        │  Fraud Detection  │
│      (C#)         │        │       (Go)        │
│  Kafka Consumer   │        │   Kafka Consumer  │
└───────────────────┘        └───────────────────┘
```

---

## 2. 서비스 아키텍처

### 2.1 비즈니스 서비스 (13개)

| 서비스 | 언어 | 포트 | 역할 | 통신 방식 |
|--------|------|------|------|-----------|
| **ad** | Java | 9555 | 광고 추천 | gRPC |
| **cart** | C# | 7070 | 장바구니 관리 | gRPC |
| **checkout** | Go | 5050 | 주문 처리 (오케스트레이터) | gRPC |
| **currency** | C++ | 7001 | 환율 변환 | gRPC |
| **email** | Python | 6060 | 이메일 발송 | HTTP |
| **accounting** | C# | - | 회계 처리 | Kafka Consumer |
| **fraud-detection** | Go | - | 사기 탐지 | Kafka Consumer |
| **payment** | Node.js | 7002 | 결제 처리 | gRPC |
| **product-catalog** | Go | 3550 | 상품 목록/검색 | gRPC |
| **product-reviews** | Python | 8080 | 상품 리뷰 + AI | HTTP |
| **recommendation** | Python | 9001 | 추천 엔진 | gRPC |
| **shipping** | Rust | 8888 | 배송비 계산 | gRPC |
| **quote** | Python | 8090 | 견적 관리 | gRPC |

### 2.2 인프라 서비스 (7개)

| 서비스 | 역할 | 포트 |
|--------|------|------|
| **flagd** | Feature Flag 평가 | 8013, 8014 |
| **flagd-ui** | Feature Flag 관리 UI | - |
| **otel-collector** | 텔레메트리 수집/라우팅 | 4317, 4318 |
| **jaeger** | 분산 트레이싱 백엔드 | 16686 |
| **prometheus** | 메트릭 수집 | 9090 |
| **grafana** | 시각화 대시보드 | 3000 |
| **opensearch** | 로그 저장/검색 | 9200 |

### 2.3 데이터 서비스

| 서비스 | 역할 | 포트 |
|--------|------|------|
| **Kafka** | 비동기 이벤트 스트리밍 | 9092 |
| **PostgreSQL** | 회계 데이터베이스 | 5432 |
| **Valkey (Redis)** | 장바구니 캐시 | 6379 |

---

## 3. 텔레메트리 파이프라인

### 3.1 파이프라인 개요

```
┌─────────────────────── 서비스 계층 ───────────────────────┐
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Checkout    │  │   Ad Service │  │ Cart Service │    │
│  │   (Go)       │  │   (Java)     │  │  (.NET)      │    │
│  │              │  │              │  │              │    │
│  │ - Traces     │  │ - Java Agent │  │ - OTEL SDK   │    │
│  │ - Metrics    │  │ - Traces     │  │ - Traces     │    │
│  │ - Logs       │  │ - Metrics    │  │ - Metrics    │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │ OTLP            │ OTLP            │ OTLP       │
└─────────┼─────────────────┼─────────────────┼────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
            ┌───────────────▼──────────────────┐
            │       OTel Collector             │
            │       (Port 4317/4318)           │
            │                                  │
            │  ┌────────────────────────────┐  │
            │  │ RECEIVERS                  │  │
            │  │ - OTLP (gRPC/HTTP)         │  │
            │  │ - Docker stats             │  │
            │  │ - PostgreSQL               │  │
            │  │ - Redis/Valkey             │  │
            │  │ - Host metrics             │  │
            │  └────────────────────────────┘  │
            │                                  │
            │  ┌────────────────────────────┐  │
            │  │ PROCESSORS                 │  │
            │  │ - memory_limiter           │  │
            │  │ - resourcedetection        │  │
            │  │ - transform (URL 정규화)   │  │
            │  └────────────────────────────┘  │
            │                                  │
            │  ┌────────────────────────────┐  │
            │  │ CONNECTORS                 │  │
            │  │ - spanmetrics              │  │
            │  │   (Trace → Metrics 변환)   │  │
            │  └────────────────────────────┘  │
            │                                  │
            └─────┬───────────┬───────────┬────┘
                  │           │           │
        ┌─────────▼───┐  ┌────▼─────┐  ┌──▼──────────┐
        │   Jaeger    │  │Prometheus│  │ OpenSearch  │
        │   Traces    │  │ Metrics  │  │    Logs     │
        │ (Port 16686)│  │(Port 9090)│ │ (Port 9200) │
        └──────┬──────┘  └────┬─────┘  └──────┬──────┘
               │              │               │
               └──────────────┼───────────────┘
                              │
                    ┌─────────▼─────────┐
                    │     Grafana       │
                    │   (Port 3000)     │
                    │                   │
                    │ - Dashboards      │
                    │ - Alerts          │
                    │ - Trace 연계      │
                    │ - Log 검색        │
                    └───────────────────┘
```

### 3.2 OTel Collector 설정

#### Receivers (데이터 수신)

```yaml
receivers:
  # 애플리케이션 텔레메트리 (OTLP)
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
        cors:
          allowed_origins: ["*"]

  # 인프라 메트릭
  docker_stats:
    endpoint: unix:///var/run/docker.sock

  hostmetrics:
    scrapers:
      cpu:
      memory:
      disk:
      network:

  # 데이터베이스 메트릭
  postgresql:
    endpoint: postgres:5432
    username: otel
    password: otel

  redis:
    endpoint: valkey:6379

  # 헬스체크
  httpcheck/frontend-proxy:
    targets:
      - endpoint: http://frontend-proxy:8080
```

#### Processors (데이터 처리)

```yaml
processors:
  # 메모리 보호 (OOM 방지)
  memory_limiter:
    check_interval: 5s
    limit_percentage: 80
    spike_limit_percentage: 25

  # 리소스 속성 자동 감지
  resourcedetection:
    detectors: [env, docker, system]
    override: false

  # URL 정규화 (카디널리티 폭발 방지)
  transform:
    trace_statements:
      - replace_pattern(name, "\\?.*", "")
      - replace_match(name, "GET /api/products/*", "GET /api/products/{productId}")
```

#### Connectors (신호 변환)

```yaml
connectors:
  # Trace에서 자동으로 Metrics 생성
  spanmetrics:
    # 생성되는 메트릭:
    # - traces_spanmetrics_latency (히스토그램)
    # - traces_spanmetrics_calls_total (카운터)
```

**spanmetrics 장점**: 별도 메트릭 계측 없이 Trace에서 RED 메트릭 자동 생성
- **R**ate (요청률)
- **E**rrors (에러율)
- **D**uration (지연 시간)

#### Exporters (데이터 내보내기)

```yaml
exporters:
  # Traces → Jaeger
  otlp:
    endpoint: jaeger:4317
    tls:
      insecure: true

  # Metrics → Prometheus
  otlphttp/prometheus:
    endpoint: http://prometheus:9090/api/v1/otlp
    tls:
      insecure: true

  # Logs → OpenSearch
  opensearch:
    logs_index: otel-logs
    http:
      endpoint: http://opensearch:9200
    sending_queue:
      num_consumers: 10
      queue_size: 1000
```

### 3.3 파이프라인 정의

```yaml
service:
  pipelines:
    # Traces 파이프라인
    traces:
      receivers: [otlp]
      processors: [resourcedetection, memory_limiter, transform]
      exporters: [otlp, spanmetrics]  # Jaeger + 메트릭 변환

    # Metrics 파이프라인
    metrics:
      receivers: [docker_stats, hostmetrics, otlp, postgresql, redis, spanmetrics]
      processors: [resourcedetection, memory_limiter]
      exporters: [otlphttp/prometheus]

    # Logs 파이프라인
    logs:
      receivers: [otlp]
      processors: [resourcedetection, memory_limiter]
      exporters: [opensearch]
```

### 3.4 백엔드 서비스 상세

#### Jaeger (분산 트레이싱)

```yaml
# 설정 파일: src/jaeger/config.yml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger_storage_exporter]

extensions:
  jaeger_query:
    storage:
      traces: memory_backend    # 인메모리 저장
      metrics: metrics_backend  # Prometheus 연계
    base_path: /jaeger/ui

  jaeger_storage:
    memory_backend:
      max_traces: 25000         # 최대 25,000개 트레이스
```

**접속**: `http://localhost:16686`

#### Prometheus (메트릭)

```yaml
# 설정 파일: src/prometheus/prometheus-config.yaml
otlp:
  # OTLP 수신 활성화
  keep_identifying_resource_attributes: true
  promote_resource_attributes:
    - service.name
    - service.version
    - k8s.pod.name
    - host.name
```

**접속**: `http://localhost:9090`

**주요 기능**:
- OTLP API 지원 (Push 방식)
- Exemplar 지원 (Trace-Metric 연계)
- 7일 보관 기간

#### Grafana (시각화)

**접속**: `http://localhost:3000`

**데이터소스**:
- Prometheus (메트릭 + Exemplar)
- Jaeger (트레이스)
- OpenSearch (로그)

---

## 4. Load Generator - 데이터 생성

### 4.1 개요

**Locust** 기반 부하 생성기로, 지속적으로 실제 사용자와 유사한 트래픽을 생성합니다.

**기술 스택**:
- **Locust**: Python 부하 테스트 프레임워크
- **Playwright**: 브라우저 자동화 (선택)
- **OpenTelemetry**: 부하 생성기 자체도 계측
- **OpenFeature**: Feature Flag 연동

### 4.2 사용자 시나리오

Load Generator는 **12가지 사용자 행동**을 가중치에 따라 시뮬레이션합니다:

| 태스크 | 가중치 | 설명 |
|--------|:------:|------|
| `browse_product()` | **10** | 상품 상세 조회 (가장 빈번) |
| `flood_home()` | 5 | 홈페이지 반복 접속 (Feature Flag 제어) |
| `get_recommendations()` | 3 | 추천 상품 조회 |
| `get_ads()` | 3 | 광고 조회 |
| `view_cart()` | 3 | 장바구니 조회 |
| `get_product_reviews()` | 2 | 상품 리뷰 조회 |
| `add_to_cart()` | 2 | 장바구니 추가 |
| `index()` | 1 | 홈페이지 방문 |
| `ask_product_ai_assistant()` | 1 | AI 리뷰 요약 질문 |
| `checkout()` | 1 | 단일 상품 결제 |
| `checkout_multi()` | 1 | 다중 상품 결제 |

**Think Time**: 태스크 간 1~10초 랜덤 대기 (실제 사용자 행동 모방)

### 4.3 트래픽 흐름

```
사용자 세션 생성
├─ Session ID 생성 + Baggage 설정
│   └─ baggage: session.id, synthetic_request=true
│
├─ 태스크 선택 (가중치 기반)
│   ├─ 10 × 상품 조회 (browse_product)
│   ├─ 5 × 홈페이지 플러딩 (Feature Flag 제어)
│   ├─ 3 × 추천/광고/장바구니 조회
│   ├─ 2 × 리뷰 조회/장바구니 추가
│   └─ 1 × 홈/AI/결제
│
├─ 요청 실행
│   ├─ HTTP/gRPC 요청
│   ├─ Trace Span 생성
│   ├─ 메트릭 기록
│   └─ 로그 출력
│
├─ 대기 (1~10초)
│
└─ 반복
```

### 4.4 데이터 생성 코드

```python
# locustfile.py

class WebsiteUser(HttpUser):
    wait_time = between(1, 10)  # 1~10초 Think Time

    def on_start(self):
        # 세션별 고유 ID 생성
        self.session_id = str(uuid.uuid4())

        # Baggage에 세션 정보 설정 (분산 트레이싱 전파)
        ctx = baggage.set_baggage("session.id", self.session_id)
        ctx = baggage.set_baggage("synthetic_request", "true", context=ctx)

    @task(10)  # 가중치 10 (가장 빈번)
    def browse_product(self):
        product = random.choice(products)

        # Span 생성 (트레이싱)
        with self.tracer.start_as_current_span(
            "user_browse_product",
            attributes={"product.id": product}
        ):
            self.client.get(f"/api/products/{product}")

    @task(5)
    def flood_home(self):
        # Feature Flag로 제어되는 부하 생성
        flood_count = get_flagd_value("loadGeneratorFloodHomepage")
        if flood_count > 0:
            for _ in range(flood_count):
                self.client.get("/")

    @task(1)
    def checkout(self):
        user = random.choice(people)

        with self.tracer.start_as_current_span(
            "user_checkout",
            attributes={"user.id": user["email"]}
        ):
            # 1. 장바구니에 상품 추가
            product = random.choice(products)
            self.client.post("/api/cart", json={
                "item": {"productId": product, "quantity": 1},
                "userId": user["userId"]
            })

            # 2. 결제 진행
            self.client.post("/api/checkout", json={
                "userId": user["userId"],
                "email": user["email"],
                "address": user["address"],
                "creditCard": user["creditCard"]
            })
```

### 4.5 브라우저 트래픽 (Playwright)

`LOCUST_BROWSER_TRAFFIC_ENABLED=true` 설정 시 실제 브라우저로 트래픽 생성:

```python
class WebsiteBrowserUser(PlaywrightUser):

    @task
    async def add_product_to_cart(self, page: PageWithRetry):
        # 실제 브라우저에서 DOM 조작
        await page.goto("/", wait_until="domcontentloaded")
        await page.click('p:has-text("Roof Binoculars")')
        await page.click('button:has-text("Add To Cart")')

    @task
    async def change_currency(self, page: PageWithRetry):
        await page.goto("/cart", wait_until="domcontentloaded")
        await page.select_option('[name="currency_code"]', 'CHF')
```

### 4.6 설정

```bash
# .env 파일
LOCUST_WEB_PORT=8089              # Locust UI 포트
LOCUST_USERS=5                    # 동시 사용자 수
LOCUST_HOST=http://frontend-proxy # 대상 호스트
LOCUST_AUTOSTART=true             # 자동 시작
LOCUST_HEADLESS=false             # UI 표시
LOCUST_BROWSER_TRAFFIC_ENABLED=true  # 브라우저 트래픽 활성화
```

**Locust UI 접속**: `http://localhost:8089`

---

## 5. Feature Flag 기반 장애 주입

### 5.1 Flagd 서비스

**이미지**: `ghcr.io/open-feature/flagd:v0.12.9`
**설정 파일**: `src/flagd/demo.flagd.json`

### 5.2 장애 주입 플래그

#### 서비스 장애 (Service Failures)

| Flag | 설명 | 값 |
|------|------|-----|
| `adFailure` | Ad 서비스 10% 확률 실패 | boolean |
| `cartFailure` | Cart 서비스 실패 | boolean |
| `paymentFailure` | Payment 실패율 | 0 ~ 1 (확률) |
| `paymentUnreachable` | Payment 연결 불가 | boolean |
| `productCatalogFailure` | 특정 상품 조회 실패 | boolean |
| `recommendationCacheFailure` | 추천 캐시 실패 | boolean |

#### 리소스 고갈 (Resource Exhaustion)

| Flag | 설명 | 값 |
|------|------|-----|
| `adHighCpu` | CPU 과부하 | boolean |
| `adManualGc` | 강제 GC 트리거 | boolean |
| `emailMemoryLeak` | 메모리 누수 | 1x ~ 10000x |
| `imageSlowLoad` | 이미지 지연 로딩 | 0, 5000, 10000 (ms) |

#### 부하/큐 문제 (Load & Queue)

| Flag | 설명 |
|------|------|
| `kafkaQueueProblems` | Kafka 큐 과부하 + 컨슈머 지연 |
| `loadGeneratorFloodHomepage` | 홈페이지 대량 요청 |

### 5.3 장애 주입 코드 예시

#### Java (Ad Service)

```java
// Feature Flag 평가
Client ffClient = OpenFeatureAPI.getInstance().getClient();

// adFailure: 10% 확률로 실패
if (ffClient.getBooleanValue("adFailure", false, context)) {
    if (random.nextInt(10) == 0) {
        throw new StatusRuntimeException(Status.UNAVAILABLE);
    }
}

// adHighCpu: CPU 과부하 시뮬레이션
if (ffClient.getBooleanValue("adHighCpu", false, context)) {
    cpuLoad.execute(true);  // 4개 스레드로 수학 연산 반복
}

// adManualGc: 강제 GC
if (ffClient.getBooleanValue("adManualGc", false, context)) {
    GarbageCollectionTrigger gct = new GarbageCollectionTrigger();
    gct.doExecute();  // 힙 채우기 + System.gc() 반복
}
```

#### Go (Checkout Service)

```go
// paymentUnreachable: 잘못된 주소로 라우팅
if cs.isFeatureFlagEnabled(ctx, "paymentUnreachable") {
    badAddress := "badAddress:50051"
    paymentService = pb.NewPaymentServiceClient(
        mustCreateClient(badAddress)
    )
    // → 연결 타임아웃 발생
}
```

#### Node.js (Payment Service)

```javascript
// paymentFailure: 확률적 실패
const failureRate = await OpenFeature.getClient()
    .getNumberValue("paymentFailure", 0);

if (failureRate > 0 && Math.random() < failureRate) {
    throw new Error('Payment request failed. Invalid token.');
}
```

### 5.4 Chaos Engineering 시나리오

| 시나리오 | 활성화 플래그 | 예상 증상 |
|----------|-------------|-----------|
| **서비스 장애** | `adFailure` | 에러율 증가, Trace에 에러 표시 |
| **리소스 고갈** | `adHighCpu` + `adManualGc` | 지연 시간 급증, GC 일시 정지 |
| **메모리 누수** | `emailMemoryLeak` (100x) | 메모리 사용량 증가 → OOM |
| **네트워크 장애** | `paymentUnreachable` | 타임아웃, 주문 실패 |
| **큐 포화** | `kafkaQueueProblems` | Consumer Lag 증가, 지연 처리 |
| **부하 급증** | `loadGeneratorFloodHomepage` | 전체 시스템 부하 증가 |

---

## 6. 실행 및 접속 방법

### 6.1 Docker Compose 실행

```bash
# 프로젝트 디렉토리로 이동
cd opentelemetry-demo

# 전체 스택 실행
docker compose up -d

# 로그 확인
docker compose logs -f
```

### 6.2 주요 서비스 접속

| 서비스 | URL | 용도 |
|--------|-----|------|
| **Frontend** | http://localhost:8080 | 쇼핑몰 UI |
| **Grafana** | http://localhost:3000 | 대시보드 |
| **Jaeger** | http://localhost:16686 | 트레이스 조회 |
| **Prometheus** | http://localhost:9090 | 메트릭 조회 |
| **Locust** | http://localhost:8089 | 부하 생성기 UI |

### 6.3 Feature Flag 변경

```bash
# flagd 설정 파일 수정
vim src/flagd/demo.flagd.json

# 예: adFailure 활성화
{
  "adFailure": {
    "defaultVariant": "on",  # off → on 변경
    ...
  }
}

# 컨테이너 재시작
docker compose restart flagd
```

---

## 요약

| 구성 요소 | 역할 | 핵심 포인트 |
|----------|------|------------|
| **Load Generator** | 지속적 트래픽 생성 | Locust + 가중치 기반 시나리오 |
| **OTel Collector** | 텔레메트리 허브 | Receivers → Processors → Exporters |
| **spanmetrics** | Trace → Metrics 변환 | RED 메트릭 자동 생성 |
| **Jaeger** | 분산 트레이싱 | 요청 흐름 시각화 |
| **Prometheus** | 메트릭 저장 | Exemplar로 Trace 연계 |
| **Grafana** | 통합 대시보드 | 메트릭/트레이스/로그 연계 |
| **Flagd** | Feature Flag | 런타임 장애 주입 |

---

*문서 작성일: 2025-12-30*
