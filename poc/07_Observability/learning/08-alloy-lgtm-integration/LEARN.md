# Ch06. Alloy-Loki-Tempo Integration

**핵심 질문**: "로그와 트레이스를 한 화면에서 연결하려면 무엇을 맞춰야 하는가?"

---

## 1. 도구를 설치했는데 왜 연결이 안 되는가

많은 팀이 Loki(로그)와 Tempo(트레이스)를 같이 설치하고 Grafana에서 둘 다 데이터소스로 등록한다. 그런데 실제 장애가 발생하면 로그 화면과 트레이스 화면을 따로 열고, 타임스탬프를 눈으로 비교하며, "아마 이 로그가 이 trace에 해당할 것이다"라고 추측한다. 도구는 있는데 **연결이 안 되는** 상태다.

이 문제의 원인은 도구가 아니라 **메타데이터**에 있다. 로그와 트레이스를 클릭 한 번으로 오가려면 세 가지 조건이 필요하다.

1. **로그에 trace_id가 포함되어야 한다** — 이것이 로그 → 트레이스 연결의 유일한 키다
2. **resource 속성이 서비스별로 일관되어야 한다** — `service.name`이 로그에서는 "checkout"이고 트레이스에서는 "checkout-svc"면 연결이 깨진다
3. **Grafana 데이터소스 간 링크가 설정되어야 한다** — Loki의 trace_id 필드가 Tempo로 점프하도록 Derived Field를 등록해야 한다

이 세 가지가 모두 갖춰져야 "통합"이다. 하나라도 빠지면 도구가 나란히 있을 뿐 연결되지 않는다.

---

## 2. 통합 아키텍처의 전체 그림

Ch03(Alloy), Ch04(Loki), Ch05(Tempo)를 개별적으로 다뤘다면, 이 챕터는 세 컴포넌트가 **어떻게 협력하는가**를 다룬다.

```mermaid
flowchart TB
    subgraph Apps["Applications"]
        direction LR
        App1["Service A<br/>OTel SDK"]
        App2["Service B<br/>OTel SDK"]
    end

    subgraph Collection["수집 계층"]
        Alloy["Grafana Alloy<br/>OTLP receiver<br/>라벨 부착 + 라우팅"]
    end

    subgraph Storage["저장 계층 (파이프라인이 아닌 백엔드)"]
        direction LR
        Loki["Loki<br/>Logs 저장 + LogQL"]
        Tempo["Tempo<br/>Traces 저장 + TraceQL"]
        Prom["Prometheus / Mimir<br/>Metrics 저장 + PromQL"]
    end

    subgraph Viz["시각화 계층"]
        Grafana["Grafana<br/>Derived Fields<br/>trace_id 클릭 → Tempo"]
    end

    Apps -->|"OTLP<br/>(logs + traces + metrics)"| Alloy
    Alloy -->|"logs + 라벨"| Loki
    Alloy -->|"traces"| Tempo
    Alloy -->|"metrics"| Prom
    Loki --> Grafana
    Tempo --> Grafana
    Prom --> Grafana

    style Alloy fill:#f5f5f5,stroke:#666,color:#333
    style Loki fill:#e8f4e8,stroke:#2d7d2d,color:#333
    style Tempo fill:#e8e8f4,stroke:#2d2d7d,color:#333
    style Prom fill:#f4e8e8,stroke:#7d2d2d,color:#333
```

각 컴포넌트의 역할을 정리하면 이렇다.

| 컴포넌트 | 역할 | 통합에서의 책임 |
|----------|------|---------------|
| **Application** | OTLP로 logs + traces + metrics 내보냄 | 로그에 trace_id 포함, resource 속성 설정 |
| **Alloy** | 수집, 라벨 부착, 라우팅 (파이프라인) | trace_id를 Structured Metadata로 분리, 공통 라벨 부착, 신호별 저장소로 분배 |
| **Loki** | 로그 저장 + LogQL 쿼리 (백엔드) | trace_id로 특정 요청의 로그 조회 |
| **Tempo** | 트레이스 저장 + TraceQL 쿼리 (백엔드) | service.name으로 특정 서비스의 트레이스 조회 |
| **Prometheus/Mimir** | 메트릭 저장 + PromQL 쿼리 (백엔드) | 서비스별 레이턴시, 에러율, 리소스 사용량 조회 |
| **Grafana** | 시각화 + 신호 간 전환 | Derived Field로 Loki ↔ Tempo 링크 |

---

## 3. 연결 키 #1: trace_id

로그와 트레이스를 연결하는 가장 강력한 키는 `trace_id`다. 하나의 요청에 대해 모든 서비스가 동일한 trace_id를 공유하므로, 이 값으로 "이 에러 로그가 어떤 요청 경로에서 발생했는가"를 정확히 추적할 수 있다.

### trace_id가 로그에 들어가는 경로

애플리케이션이 OTel SDK로 계측되어 있으면, 활성 span의 trace_id를 로그에 자동으로 포함할 수 있다. Spring Boot의 경우 Micrometer Tracing이 MDC(Mapped Diagnostic Context)에 trace_id를 넣고, 로그 패턴에서 이를 출력한다.

```xml
<!-- logback-spring.xml -->
<pattern>%d{HH:mm:ss} [%thread] %-5level %logger - [traceId=%X{traceId}, spanId=%X{spanId}] %msg%n</pattern>
```

결과 로그:
```
14:23:05 [http-nio-8080-exec-1] ERROR c.e.OrderService - [traceId=4bf92f3577b34da6a3ce929d0e0e4736, spanId=00f067aa0ba902b7] Payment timeout
```

OTel Java Agent를 사용하면 별도 설정 없이 MDC에 `trace_id`, `span_id`가 자동으로 주입된다. Spring Boot Starter도 마찬가지다. 핵심은 **로그 패턴에 `%X{traceId}`를 포함**하는 것이다. 이것이 빠지면 아무리 SDK가 동작해도 로그 출력에 trace_id가 나타나지 않는다.

### trace_id를 Loki에 어떻게 저장하는가

trace_id가 로그 본문에 출력되면, Loki에 저장할 때 세 가지 위치 중 하나를 선택해야 한다.

| 저장 위치 | 장점 | 단점 | 권장 여부 |
|----------|------|------|----------|
| **Loki 라벨** | 인덱스 타므로 빠른 필터링 | 카디널리티 폭발 — trace_id는 요청마다 다름 | **금지** |
| **로그 본문** | 별도 설정 불요 | `\|= "traceId=abc..."` 본문 스캔 필요 | 기본 |
| **Structured Metadata** | 카디널리티 안전 + 빠른 필터링 | Loki 3.0+ 필요 | **권장** |

Ch04에서 다뤘듯이, trace_id는 요청마다 고유한 값이므로 라벨로 올리면 스트림이 폭발한다. Loki 3.0 이상에서는 **Structured Metadata**에 저장하는 것이 비용과 탐색 양쪽에서 가장 균형 잡힌 선택이다. Structured Metadata는 인덱스에 들어가지 않지만 LogQL에서 필터링할 수 있다.

Alloy에서 이 설정을 하는 방법:

```alloy
// alloy-config.alloy
loki.process "extract_trace" {
  // JSON 로그에서 traceId 필드 추출
  stage.json {
    expressions = { trace_id = "traceId" }
  }

  // 추출된 trace_id를 Structured Metadata로 저장
  stage.structured_metadata {
    values = { trace_id = "trace_id" }
  }

  forward_to = [loki.write.default.receiver]
}
```

### Grafana에서 trace_id 클릭 → Tempo 점프

로그에 trace_id가 있어도, Grafana에서 자동으로 Tempo로 연결되지는 않는다. **Derived Field** 설정이 필요하다.

```yaml
# grafana/provisioning/datasources/datasources.yaml
datasources:
  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      derivedFields:
        - datasourceUid: tempo-uid
          matcherRegex: "traceId=(\\w+)"      # 로그에서 trace_id 추출 정규식
          name: TraceID
          url: "$${__value.raw}"               # 추출된 값으로 Tempo 조회
          datasourceName: Tempo
```

이 설정이 되면 Grafana Explore에서 로그를 볼 때 trace_id 옆에 링크 아이콘이 생기고, 클릭하면 Tempo의 해당 trace 뷰로 바로 이동한다. 이것이 "클릭 한 번으로 로그에서 트레이스로" 전환되는 UX의 실체다.

### 역방향: Tempo에서 로그로

Tempo → Loki 방향도 설정할 수 있다. Tempo 데이터소스에서 trace-to-logs 연동을 설정하면, trace 뷰에서 특정 span을 선택했을 때 해당 서비스의 동일 시간대 로그를 바로 조회할 수 있다.

```yaml
  - name: Tempo
    type: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogs:
        datasourceUid: loki-uid
        filterByTraceID: true        # trace_id로 로그 필터링
        filterBySpanID: false
        mapTagNamesEnabled: true
        mappedTags:
          - key: service.name
            value: service_name      # Tempo의 service.name → Loki의 service_name 라벨로 매핑
```

이렇게 양방향 링크가 설정되면, 로그 → 트레이스 → 로그를 자유롭게 오갈 수 있다.

```mermaid
flowchart LR
    LokiView["Grafana Explore<br/>Loki 로그 조회"]
    DerivedField["Derived Field<br/>traceId 정규식 매칭"]
    TempoView["Grafana Explore<br/>Tempo trace 조회"]
    TraceToLog["tracesToLogs<br/>service.name + 시간대"]

    LokiView -->|"trace_id 클릭"| DerivedField --> TempoView
    TempoView -->|"Logs 탭 클릭"| TraceToLog --> LokiView

    style DerivedField fill:#e8f4e8,stroke:#2d7d2d,color:#333
    style TraceToLog fill:#e8e8f4,stroke:#2d2d7d,color:#333
```

---

## 4. 연결 키 #2: 공통 Resource 속성

trace_id가 **건별 연결 키**라면, `service.name`과 `deployment.environment`는 **탐색의 출발점**이다. 운영자가 장애를 분석할 때 첫 번째로 하는 것은 "어떤 서비스의 어떤 환경에서 문제가 생겼는가"를 좁히는 것이다.

```
탐색 흐름:
  1. service.name = "checkout"
  2. deployment.environment = "prod"
  3. 최근 15분
  4. level = "error"
  → 에러 로그 목록 → trace_id 클릭 → Tempo trace 확인
```

이 흐름이 동작하려면, 로그의 `service_name` 라벨과 트레이스의 `service.name` resource 속성이 **같은 값**이어야 한다. 로그에서는 "checkout"이고 트레이스에서는 "checkout-svc"면, 같은 서비스의 데이터를 연결할 수 없다.

### 속성 일관성을 어디서 보장하는가

OTel SDK에서 설정한 resource 속성이 **모든 신호의 원천**이 된다. 이 값을 한 곳에서 설정하면 로그와 트레이스에 동일한 값이 들어간다.

```bash
# 앱에서 한 번만 설정하면 logs, traces 모두에 적용
OTEL_SERVICE_NAME=checkout
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=prod,service.version=1.2.3
```

Alloy가 이 값을 받아서 Loki 라벨로 매핑할 때 이름이 바뀔 수 있으므로 주의가 필요하다. OTel 표준에서는 `service.name`이지만, Loki 라벨에서는 점(.)을 쓸 수 없으므로 `service_name`으로 변환된다. Grafana의 Derived Field와 tracesToLogs 설정에서 이 매핑을 명시해야 한다.

### 필수 속성과 매핑

| OTel Resource 속성 | Loki 라벨 | Tempo 속성 | 용도 |
|-------------------|----------|-----------|------|
| `service.name` | `service_name` | `service.name` | 서비스 식별 (모든 탐색의 기본 축) |
| `deployment.environment` | `deployment_environment` | `deployment.environment` | 환경 분리 (dev/stg/prod) |
| `service.version` | Structured Metadata | `service.version` | 배포 버전별 비교 |
| `k8s.namespace.name` | `namespace` | `k8s.namespace.name` | K8s 네임스페이스 필터 |

---

## 5. Alloy의 역할: 라우팅과 라벨 부착

Ch03에서 Alloy를 "통합 수집기"로 다뤘지만, 통합 아키텍처에서 Alloy의 가장 중요한 역할은 **신호별 라우팅과 라벨 정규화**다.

### OTLP 수신 → 신호 분리

앱이 OTLP로 보내는 데이터에는 logs와 traces가 섞여 있다. Alloy는 이를 받아서 logs는 Loki로, traces는 Tempo로 분리한다.

```alloy
// OTLP receiver — 앱에서 보내는 모든 신호를 수신
otelcol.receiver.otlp "default" {
  grpc { endpoint = "0.0.0.0:4317" }
  http { endpoint = "0.0.0.0:4318" }

  output {
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.filter.noise.input]    // 노이즈 필터 거쳐서 Tempo로
  }
}

// Trace 노이즈 필터링 (Ch09에서 다룬 패턴)
otelcol.processor.filter "noise" {
  traces {
    span = [
      "name == \"GET /actuator/prometheus\"",
      "name == \"GET /actuator/health\"",
    ]
  }
  output { traces = [otelcol.exporter.otlphttp.tempo.input] }
}

// Logs → Loki로 전송
otelcol.exporter.loki "default" {
  forward_to = [loki.process.extract_trace.receiver]
}

// Traces → Tempo로 전송
otelcol.exporter.otlphttp "tempo" {
  client { endpoint = "http://tempo:4318" }
}
```

### 라벨 정규화

OTel resource 속성은 `service.name` 형태이지만, Loki 라벨은 점(.)을 허용하지 않는다. Alloy가 이 변환을 자동으로 처리하지만, 어떤 속성이 라벨로 승격되고 어떤 것이 Structured Metadata로 가는지는 설정으로 제어해야 한다.

```
OTel resource 속성           →  Loki 저장 위치
service.name                 →  라벨: service_name (승격)
deployment.environment       →  라벨: deployment_environment (승격)
trace_id                     →  Structured Metadata (고카디널리티)
span_id                      →  Structured Metadata (고카디널리티)
service.version              →  Structured Metadata (변경 빈도 높음)
```

이 라벨 승격 결정이 Ch04에서 다룬 "Loki 라벨 전략"의 실체다. 설계는 Loki 관점에서 하고, 구현은 Alloy에서 한다.

---

## 6. 운영 탐색 워크플로우

이론을 다뤘으니, 실제 장애 분석에서 로그-트레이스 통합이 어떻게 쓰이는지 두 가지 시나리오로 확인한다.

### 워크플로우 1: 로그에서 트레이스로 (가장 흔한 패턴)

**시나리오**: Grafana 알림 — "checkout 서비스 에러율 3% → 15% 상승"

```logql
# Step 1: 에러 로그 조회
{service_name="checkout", level="error"} |= "timeout"
```

결과에서 `traceId=4bf92f3577b34da6...`를 발견한다. Derived Field 링크를 클릭하면 Tempo로 이동.

```
# Step 2: Tempo trace 확인
trace_id = 4bf92f3577b34da6a3ce929d0e0e4736

checkout (120ms) ─┬─ inventory-check (15ms)  ✓
                  ├─ price-calculate (8ms)   ✓
                  └─ payment-request (95ms)  ✗ ERROR: connection timeout
                       └─ external-pg (timeout) ✗
```

payment-request span에서 외부 결제 게이트웨이 타임아웃이 원인임을 확인한다. 로그만으로는 "checkout에서 타임아웃"이라는 정보뿐이지만, trace를 통해 **정확히 어디서 95ms를 소비했고 어떤 외부 호출이 실패했는지** 알 수 있다.

### 워크플로우 2: 트레이스에서 로그로

**시나리오**: Tempo에서 P99 레이턴시가 높은 trace를 발견

```
# Step 1: TraceQL로 느린 trace 검색
{ duration > 3s && resource.service.name = "order-api" }

# Step 2: 느린 trace에서 DB 쿼리 span 발견
order-api (3.2s) ─┬─ GET /api/orders (3.1s)
                  └─ SELECT orders WHERE ... (2.9s)  ← 병목
```

DB 쿼리가 2.9초 걸렸다. 하지만 trace만으로는 "왜 이 쿼리가 느렸는가"를 알 수 없다. Tempo의 Logs 탭을 클릭하면 해당 서비스의 동일 시간대 로그로 점프한다.

```logql
# Step 3: 해당 시간대 order-api 로그 확인
{service_name="order-api"} | json | msg =~ "slow query.*"
```

로그에서 "table lock waiting 2.8s"를 발견 — 다른 트랜잭션의 테이블 락이 원인이었다. trace가 "어디가 느린가"를 알려 주고, 로그가 "왜 느린가"를 알려 주는 구조다.

### 두 워크플로우의 공통점

```mermaid
flowchart LR
    What["무슨 일이?<br/>(Loki 로그)"]
    Where["어디서?<br/>(Tempo trace)"]
    Why["왜?<br/>(Loki 로그 상세)"]

    What -->|"trace_id"| Where -->|"service.name + 시간대"| Why

    style What fill:#e8f4e8,stroke:#2d7d2d,color:#333
    style Where fill:#e8e8f4,stroke:#2d2d7d,color:#333
    style Why fill:#f5f5dc,stroke:#8b8b00,color:#333
```

로그가 "무슨 일이 있었는가"를, 트레이스가 "어디서 발생했는가"를, 다시 로그가 "왜 발생했는가"를 답한다. 이 순환이 가능한 이유는 trace_id와 service.name이라는 **공통 메타데이터로 양쪽이 연결**되어 있기 때문이다.

---

## 7. 실제 프로젝트의 통합 구성 (redpanda-playground)

redpanda-playground 프로젝트의 docker-compose.monitoring.yml이 이 통합 아키텍처를 그대로 구현하고 있다.

### 데이터 흐름

```
Spring Boot App (OTel Agent)
  ├─ traces → OTLP HTTP :24318 → Alloy → 노이즈 필터 → Tempo :3200
  ├─ logs   → stdout → Docker log driver → Loki :3100
  └─ metrics → /actuator/prometheus → Prometheus scrape :9090
                                         ↓
                                    Grafana :3000
                                    (Derived Fields + tracesToLogs)
```

### Grafana 데이터소스 링크 설정

```yaml
# docker/monitoring/grafana/provisioning/datasources/datasources.yaml
datasources:
  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "traceId=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"

  - name: Tempo
    type: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogs:
        datasourceUid: loki
        filterByTraceID: true
        mappedTags:
          - key: service.name
            value: service_name
```

이 설정이 있으면 Grafana에서:
- Loki 로그의 `traceId=xxx` 옆에 링크 아이콘 → 클릭하면 Tempo trace 뷰
- Tempo trace 뷰의 Logs 탭 → 해당 서비스 + 시간대의 Loki 로그 조회

### Outbox 패턴에서의 trace 연결

Ch09에서 다뤘듯이, Outbox 패턴에서는 HTTP 요청과 Kafka 발행 사이에 시간 차이가 생긴다. 이때 수동으로 traceparent를 저장/복원하면 Tempo에서 `POST /api/webhooks` → `OutboxPoller.publish` → `kafka send`가 하나의 trace로 보인다. 동시에 Loki에서 같은 trace_id로 조회하면 HTTP 요청 로그와 Kafka 발행 로그가 모두 나온다.

이것이 통합 아키텍처의 가치다. 비동기 처리에서도 trace_id만 유지되면 전체 흐름을 하나의 관점으로 추적할 수 있다.

---

## 8. 설계 원칙

### 원칙 1: 앱은 OTLP만 알면 된다

애플리케이션은 Loki endpoint, Tempo endpoint를 직접 알 필요가 없다. OTLP로 Alloy에 보내면 Alloy가 목적지별로 라우팅한다. 앱의 책임은 두 가지뿐이다.

- `OTEL_EXPORTER_OTLP_ENDPOINT`를 Alloy로 설정
- 로그 패턴에 `traceId`, `spanId` 포함

저장소가 Tempo에서 Jaeger로 바뀌어도, 앱 설정은 변경할 필요가 없다.

### 원칙 2: 연결 키와 검색 키를 분리

| 구분 | 예시 | Loki 저장 위치 | 이유 |
|------|------|-------------|------|
| **검색 키** | `service.name`, `env`, `level` | 라벨 (인덱싱) | 카디널리티 낮음, 항상 필터에 사용 |
| **연결 키** | `trace_id`, `span_id` | Structured Metadata | 카디널리티 높음, 건별 추적용 |

이 두 종류를 같은 라벨 전략으로 다루면, 비용(라벨에 trace_id → 스트림 폭발)이나 탐색성(trace_id가 본문에만 → 연결 느림) 중 하나가 무너진다.

### 원칙 3: 저장소의 역할을 섞지 않는다

Loki에 trace 정보를 넣거나, Tempo에 상세 로그 메시지를 저장하는 것은 안티패턴이다. 각 저장소는 자기 신호에 최적화되어 있다.

- **Loki**: "무슨 일이 있었는가" — 텍스트 기반 상세 정보
- **Tempo**: "어디서 얼마나 걸렸는가" — 구조화된 span 트리

둘을 연결하는 것은 Grafana의 역할이지, 저장소의 역할이 아니다.

### 원칙 4: Alloy는 파이프라인이지 저장소가 아니다

Alloy가 세 신호를 모두 OTLP로 수신하고 라우팅한다고 해서, 저장소가 필요 없어지는 것이 아니다. Alloy는 데이터를 흘려보내는 파이프라인이지, 시계열 데이터를 저장하고 쿼리하는 기능은 없다.

```
Alloy = 택배 기사 (수집, 필터링, 라우팅)
Loki / Tempo / Prometheus(Mimir) = 창고 (저장, 인덱싱, 쿼리)
```

특히 메트릭에서 이 구분이 혼동되기 쉽다. 현재 이 프로젝트는 Prometheus가 앱의 `/actuator/prometheus`를 직접 scrape하는 구조다. 만약 Alloy를 정석대로 도입해서 메트릭도 OTLP로 받게 되면, 수집 경로만 바뀌고 저장소는 여전히 필요하다.

```
현재:   Prometheus ──scrape──▶ 앱         (Prometheus가 수집 + 저장 + 쿼리)
정석:   앱 ──OTLP──▶ Alloy ──▶ Mimir     (Alloy가 수집, Mimir가 저장 + 쿼리)
```

Mimir는 Prometheus의 분산 확장판으로, LGTM 스택에서 M에 해당한다. PromQL을 그대로 사용하며, 장기 저장과 수평 확장을 지원한다. 소규모 환경에서는 Prometheus 단독으로 충분하고, 멀티클러스터나 장기 보관이 필요하면 Mimir로 교체한다.

| 컴포넌트 | 역할 | LGTM에서의 위치 |
|----------|------|----------------|
| **Alloy** | 수집 + 라우팅 (파이프라인) | 수집 계층 |
| **Loki** | 로그 저장 + LogQL 쿼리 | L |
| **Grafana** | 시각화 + 신호 간 연결 | G |
| **Tempo** | 트레이스 저장 + TraceQL 쿼리 | T |
| **Mimir** | 메트릭 저장 + PromQL 쿼리 | M |
| **Prometheus** | 메트릭 수집 + 저장 + 쿼리 (Mimir의 소규모 대안) | M 대체 |

Alloy가 아무리 강력한 수집기여도 택배 경로를 바꾸는 것이지 창고를 없애는 것이 아니다. 이 구분을 이해하면 "Alloy를 도입하면 Prometheus가 필요 없는가?" 같은 혼동이 사라진다.

---

## 9. 면접에서 설명한다면

### "로그와 트레이스를 어떻게 연결하나요?"

핵심은 trace_id입니다. OTel SDK가 활성 span의 trace_id를 MDC에 넣고, 로그 패턴에서 이를 출력합니다. 이 trace_id를 Loki의 Structured Metadata에 저장하면, Grafana의 Derived Field 설정을 통해 로그에서 trace_id를 클릭하면 Tempo의 해당 trace로 바로 이동할 수 있습니다. 역방향으로도 Tempo의 tracesToLogs 설정으로 trace에서 로그로 점프합니다.

### "통합 아키텍처에서 Alloy의 역할은?"

Alloy는 OTLP로 들어오는 로그와 트레이스를 수신해서, 로그는 Loki로 트레이스는 Tempo로 라우팅합니다. 이 과정에서 OTel resource 속성(`service.name`)을 Loki 라벨(`service_name`)로 변환하고, trace_id 같은 고카디널리티 값은 Structured Metadata로 분리합니다. 앱은 Alloy 하나만 알면 되고, 저장소가 바뀌어도 앱 설정을 변경할 필요가 없습니다.

### "연결이 안 될 때 어떻게 진단하나요?"

세 가지를 순서대로 확인합니다. 첫째, 로그에 trace_id가 출력되는지 — 로그 패턴에 `%X{traceId}`가 빠져 있으면 MDC에 있어도 출력되지 않습니다. 둘째, Loki에서 trace_id를 조회할 수 있는지 — Structured Metadata나 본문에 값이 있어야 합니다. 셋째, Grafana의 Derived Field 정규식이 올바른지 — `traceId=(\w+)` 패턴이 실제 로그 형식과 맞아야 링크가 생깁니다.

### "resource 속성의 일관성이 왜 중요한가요?"

로그의 `service_name=checkout`과 트레이스의 `service.name=checkout-svc`처럼 값이 다르면, Grafana에서 같은 서비스의 로그와 트레이스를 연결할 수 없습니다. OTel SDK에서 `OTEL_SERVICE_NAME`을 한 번 설정하면 모든 신호에 동일한 값이 들어가므로, 앱 레벨에서 한 곳만 관리하는 것이 일관성을 유지하는 가장 확실한 방법입니다.
