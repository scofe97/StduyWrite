# Ch10. 모니터링, 관측성, 미래

**핵심 질문**: "시스템 장애를 사전 감지하고 미래 트렌드에 어떻게 대비하는가?"

---

## 🎯 학습 목표

1. 모니터링(Monitoring)과 관측성(Observability)의 개념 차이를 설명할 수 있다.
2. Metrics, Logs, Traces 세 가지 기둥의 역할과 상호 보완 관계를 이해한다.
3. Prometheus + Grafana 스택을 실제 설정 파일 수준에서 구성할 수 있다.
4. SLI/SLO/SLA를 정의하고 에러 버짓 기반으로 릴리스 의사결정을 내릴 수 있다.
5. OpenTelemetry를 사용해 분산 시스템에서 요청 흐름을 추적할 수 있다.
6. AIOps, Platform Engineering, FinOps 등 미래 트렌드가 DevOps에 미치는 영향을 파악한다.

---

## 1. 모니터링 vs 관측성

모니터링(Monitoring)과 관측성(Observability)은 비슷해 보이지만 근본적으로 다른 질문에 답한다. 모니터링은 "알고 있는 문제가 발생했는가?"를 추적한다. CPU 사용률이 80%를 넘으면 알림을 받는다. 디스크가 꽉 찼는지 확인한다. 이미 어떤 지표를 봐야 하는지 알고 있고, 그 지표가 임계값을 넘는지 감시하는 행위다.

관측성(Observability)은 다른 질문에서 출발한다. "내가 예상하지 못한 문제가 왜 발생했는가?" 분산 마이크로서비스 환경에서는 수십 개의 서비스가 복잡하게 얽혀 있기 때문에, 어떤 조합에서 문제가 생길지 사전에 모두 예측할 수 없다. 관측성은 시스템 내부 상태를 외부에서 추론할 수 있도록 충분한 데이터를 시스템이 방출하게 만드는 속성이다. 즉, 관측성은 시스템의 특성이고 모니터링은 그 특성을 활용하는 행위다.

```mermaid
flowchart LR
    A[애플리케이션] -->|Metrics| B[Prometheus]
    A -->|Logs| C[Loki / ELK]
    A -->|Traces| D[Jaeger / Tempo]
    B --> E[Grafana]
    C --> E
    D --> E
    E -->|Alert| F[Alertmanager]
    F -->|Webhook| G[PagerDuty]
    F -->|Slack| H[Slack Channel]

    style A fill:#d4edda,stroke:#28a745,color:#333
    style E fill:#cce5ff,stroke:#007bff,color:#333
    style G fill:#fff3cd,stroke:#ffc107,color:#333
```

---

## 2. 세 가지 기둥: Metrics, Logs, Traces

관측성을 구성하는 세 가지 핵심 데이터 유형을 이해하면 어떤 도구를 언제 써야 하는지 판단이 명확해진다.

**Metrics**는 숫자로 표현되는 시계열 데이터다. HTTP 요청 수, 응답 시간 p99, 에러율 같은 지표들이다. 집계하기 쉽고 저장 비용이 낮아 장기 보존에 적합하다. 대시보드와 알림의 기반이 된다. Prometheus가 이 영역의 표준 도구로 자리잡았다.

**Logs**는 이벤트 단위로 기록된 텍스트 데이터다. "주문 #12345 처리 완료" 같은 구체적인 사건을 담는다. 문제 발생 후 원인을 파악하는 데 가장 직접적인 단서를 제공한다. 단, 비정형 로그(console.log 수준)는 검색이 어렵기 때문에 구조화된 JSON 형식으로 출력하는 것이 실무 표준이다.

**Traces**는 하나의 요청이 여러 서비스를 거치는 전체 여정을 기록한다. 사용자가 "결제" 버튼을 누른 순간부터 최종 응답까지 API Gateway → Order Service → Payment Service → Notification Service를 거치는 각 구간의 시간을 측정한다. 병목이 어느 서비스에 있는지 찾아내는 데 필수적이다.

---

## 3. Prometheus — 완전한 스크레이프 설정

Prometheus는 Pull 방식으로 메트릭을 수집한다. 타겟 서비스의 `/metrics` 엔드포인트를 주기적으로 당겨(scrape)오는 구조다. Push 방식(서비스가 직접 전송)과 비교하면, Pull 방식은 서비스가 죽었는지 Prometheus가 직접 확인할 수 있다는 장점이 있다.

```yaml
# prometheus.yml — 실제 운영 수준의 설정
global:
  scrape_interval: 15s        # 기본 수집 주기
  evaluation_interval: 15s    # 알림 규칙 평가 주기
  external_labels:
    cluster: 'production'     # 알림 라우팅 시 레이블로 활용
    region: 'ap-northeast-2'

# 알림 규칙 파일 로드
rule_files:
  - "rules/alert_rules.yml"
  - "rules/recording_rules.yml"

# Alertmanager 연동
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  # Prometheus 자체 모니터링
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter — 호스트 수준 메트릭
  - job_name: 'node-exporter'
    scrape_interval: 30s
    static_configs:
      - targets:
          - 'node-exporter-1:9100'
          - 'node-exporter-2:9100'
    relabel_configs:
      # 타겟 주소에서 호스트명 추출해 instance 레이블로 설정
      - source_labels: [__address__]
        regex: '([^:]+):.*'
        target_label: instance
        replacement: '$1'

  # 애플리케이션 서비스 — Kubernetes Service Discovery
  - job_name: 'app-services'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['production', 'staging']
    relabel_configs:
      # prometheus.io/scrape: "true" 어노테이션이 있는 Pod만 수집
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # 어노테이션으로 포트 지정 가능
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
        replacement: $1
      # 네임스페이스를 레이블로 추가
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      # Pod 이름을 레이블로 추가
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod

  # Blackbox Exporter — 외부에서 엔드포인트 헬스체크
  - job_name: 'blackbox-http'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://api.example.com/health
          - https://www.example.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
```

### 알림 규칙 파일

```yaml
# rules/alert_rules.yml
groups:
  - name: application.rules
    interval: 30s  # 이 그룹만 30초마다 평가
    rules:
      # Recording Rule — 자주 사용하는 쿼리를 사전 계산해 저장
      - record: job:http_request_duration_seconds:p99
        expr: |
          histogram_quantile(0.99,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

      # Alerting Rule — 에러율 5% 초과 시
      - alert: HighErrorRate
        expr: |
          sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum by (job) (rate(http_requests_total[5m])) > 0.05
        for: 5m  # 5분 지속 시에만 발화 (순간 스파이크 무시)
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "{{ $labels.job }} 에러율 {{ $value | humanizePercentage }}"
          description: "최근 5분 에러율이 5%를 초과했습니다."
          runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

      # Alerting Rule — p99 응답 시간 1초 초과
      - alert: SlowResponseTime
        expr: job:http_request_duration_seconds:p99 > 1.0
        for: 10m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "{{ $labels.job }} p99 응답 시간 {{ $value }}s"
          description: "p99 응답 시간이 10분째 1초를 초과 중입니다."

  - name: infrastructure.rules
    rules:
      # 디스크 사용률 90% 초과
      - alert: DiskSpaceCritical
        expr: |
          (1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) > 0.90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.instance }} 디스크 사용률 위험"
          description: "{{ $labels.mountpoint }} 디스크가 90% 이상 사용됐습니다."
```

---

## 4. Grafana — 완전한 대시보드 JSON

Grafana는 Prometheus, Loki, Tempo 등 다양한 데이터 소스를 시각화한다. 대시보드를 코드로 관리(Dashboard as Code)하면 팀 간 공유와 버전 관리가 가능하다.

```json
{
  "title": "Application Overview",
  "uid": "app-overview-v1",
  "refresh": "30s",
  "time": { "from": "now-1h", "to": "now" },
  "templating": {
    "list": [
      {
        "name": "job",
        "type": "query",
        "datasource": "Prometheus",
        "query": "label_values(http_requests_total, job)",
        "refresh": 2
      }
    ]
  },
  "panels": [
    {
      "title": "Request Rate (RPS)",
      "type": "timeseries",
      "gridPos": { "x": 0, "y": 0, "w": 8, "h": 8 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{job=\"$job\"}[5m]))",
          "legendFormat": "RPS"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "reqps",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 1000 },
              { "color": "red", "value": 5000 }
            ]
          }
        }
      }
    },
    {
      "title": "Error Rate (%)",
      "type": "stat",
      "gridPos": { "x": 8, "y": 0, "w": 4, "h": 8 },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{job=\"$job\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=\"$job\"}[5m])) * 100",
          "legendFormat": "Error Rate"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 1 },
              { "color": "red", "value": 5 }
            ]
          }
        }
      }
    },
    {
      "title": "Response Time Percentiles",
      "type": "timeseries",
      "gridPos": { "x": 12, "y": 0, "w": 12, "h": 8 },
      "targets": [
        {
          "expr": "histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket{job=\"$job\"}[5m])))",
          "legendFormat": "p50"
        },
        {
          "expr": "histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{job=\"$job\"}[5m])))",
          "legendFormat": "p95"
        },
        {
          "expr": "histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{job=\"$job\"}[5m])))",
          "legendFormat": "p99"
        }
      ],
      "fieldConfig": {
        "defaults": { "unit": "s" }
      }
    }
  ]
}
```

---

## 5. 알림 설계 — PagerDuty 연동

알림 설계의 핵심은 "진짜 행동이 필요한 상황에만 사람을 깨운다"는 원칙이다. Alert Fatigue(알림 피로)는 너무 많은 알림이 오면 엔지니어가 알림을 무시하기 시작하는 현상이다. 알림은 사용자 영향이 있을 때, 즉시 조치가 필요할 때만 발화해야 한다.

```yaml
# alertmanager.yml — PagerDuty 라우팅 설정
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'cluster', 'job']
  group_wait: 30s      # 같은 그룹 알림을 묶어서 전송하기 위한 대기
  group_interval: 5m   # 동일 그룹의 알림 재전송 간격
  repeat_interval: 4h  # 해결 안 된 알림 반복 주기
  receiver: 'slack-notifications'  # 기본 수신자

  routes:
    # severity: critical → PagerDuty (온콜 엔지니어 호출)
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true  # 다음 라우트도 계속 평가

    # severity: warning → Slack만
    - match:
        severity: warning
      receiver: 'slack-notifications'

    # team: database → DBA 팀 전용 채널
    - match:
        team: database
      receiver: 'slack-dba-team'

receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<PAGERDUTY_INTEGRATION_KEY>'
        description: '{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}'
        details:
          firing: '{{ .Alerts.Firing | len }}'
          resolved: '{{ .Alerts.Resolved | len }}'
          runbook: '{{ (index .Alerts 0).Annotations.runbook_url }}'
        # 자동 해결: Prometheus에서 알림이 사라지면 PagerDuty 인시던트 자동 종료
        send_resolved: true

  - name: 'slack-notifications'
    slack_configs:
      - api_url: '<SLACK_WEBHOOK_URL>'
        channel: '#alerts'
        title: '[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Severity:* {{ .Labels.severity }}
          *Details:* {{ .Annotations.description }}
          {{ end }}
        send_resolved: true

# 알림 억제 — 부모 알림 발생 시 자식 알림 억제
inhibit_rules:
  # 클러스터 전체 다운 알림이 있으면 개별 서비스 알림 억제
  - source_match:
      alertname: 'ClusterDown'
    target_match_re:
      alertname: '.+'
    equal: ['cluster']
```

---

## 6. OpenTelemetry — 분산 트레이싱

분산 시스템에서 하나의 요청이 여러 서비스를 거칠 때, 각 구간의 처리 시간과 오류를 추적하려면 Context Propagation이 필요하다. 부모 Span의 ID를 HTTP 헤더(W3C TraceContext 표준: `traceparent`)에 담아 전달하면, 다음 서비스가 같은 Trace에 새로운 Span을 추가할 수 있다.

```javascript
// Node.js — OpenTelemetry 트레이싱 설정 (tracing.js)
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

// SDK 초기화 — 애플리케이션 코드보다 먼저 실행해야 함
const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'order-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.2.0',
    'deployment.environment': process.env.NODE_ENV,
  }),
  traceExporter: new OTLPTraceExporter({
    // OpenTelemetry Collector로 전송 (Collector가 Jaeger/Tempo로 중계)
    url: 'http://otel-collector:4318/v1/traces',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Express, HTTP, gRPC, DB 클라이언트 자동 계측
      '@opentelemetry/instrumentation-fs': { enabled: false }, // 파일 I/O는 노이즈
    }),
  ],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());
```

```javascript
// order-service.js — 수동 Span 생성 (비즈니스 로직 추적)
const { trace, context, SpanStatusCode } = require('@opentelemetry/api');

const tracer = trace.getTracer('order-service', '1.0.0');

async function processOrder(orderId, userId) {
  // 현재 요청의 Trace 컨텍스트 안에 새 Span 생성
  return tracer.startActiveSpan('processOrder', async (span) => {
    span.setAttributes({
      'order.id': orderId,
      'user.id': userId,
      'order.source': 'web',
    });

    try {
      const inventory = await checkInventory(orderId);
      span.addEvent('inventory.checked', { available: inventory.available });

      const payment = await chargePayment(userId, inventory.price);
      span.addEvent('payment.charged', { transactionId: payment.txId });

      span.setStatus({ code: SpanStatusCode.OK });
      return { success: true, orderId };
    } catch (err) {
      // 예외를 Span에 기록 — Jaeger UI에서 에러 Span으로 표시됨
      span.recordException(err);
      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
      throw err;
    } finally {
      span.end(); // Span은 반드시 종료해야 전송됨
    }
  });
}
```

### Bad vs Good: 로그 구조화

```javascript
// ❌ Bad — console.log 디버깅
// 검색 불가, 상관관계 추적 불가, 파싱 어려움
console.log('주문 처리 완료: ' + orderId);
console.log('에러 발생', err.message);

// ✅ Good — 구조화된 JSON 로그 + Trace ID 연결
const logger = require('pino')({
  level: 'info',
  formatters: {
    level: (label) => ({ level: label }),  // 레벨을 문자열로
  },
  timestamp: () => `,"timestamp":"${new Date().toISOString()}"`,
});

// OpenTelemetry Trace ID를 로그에 포함 → Grafana에서 로그-트레이스 연결 가능
function getTraceContext() {
  const span = trace.getActiveSpan();
  if (!span) return {};
  const { traceId, spanId } = span.spanContext();
  return { traceId, spanId };
}

logger.info({
  ...getTraceContext(),
  event: 'order.processed',
  orderId,
  userId,
  durationMs: Date.now() - startTime,
}, '주문 처리 완료');

logger.error({
  ...getTraceContext(),
  event: 'order.failed',
  orderId,
  error: {
    name: err.name,
    message: err.message,
    stack: err.stack,
  },
}, '주문 처리 실패');
```

---

## 7. SLI/SLO/SLA와 에러 버짓

SLI(Service Level Indicator)는 측정 가능한 서비스 품질 지표다. "지난 5분간 성공 응답 비율" 같은 구체적인 숫자다.

SLO(Service Level Objective)는 내부 목표다. "SLI가 99.9% 이상이어야 한다"고 설정한다. 이 목표를 달성하지 못한 시간을 에러 버짓(Error Budget)으로 계산한다. 99.9% SLO라면 30일 기준 에러 버짓은 43.8분이다. 버짓이 소진되면 새 기능 배포를 멈추고 안정화에 집중한다.

SLA(Service Level Agreement)는 외부 계약이다. SLO보다 낮게 설정하는 것이 일반적이다(예: SLO 99.9%, SLA 99.5%). 위반 시 고객에게 환불 등 패널티가 발생한다.

```yaml
# SLI/SLO 정의 예시 (Prometheus 쿼리 기반)
slos:
  - name: "API Availability"
    # SLI: 5xx가 아닌 응답 비율
    sli:
      good_events: sum(rate(http_requests_total{status!~"5.."}[30d]))
      total_events: sum(rate(http_requests_total[30d]))
    # SLO: 99.9% 가용성 목표
    objective: 99.9
    # 에러 버짓: (1 - 0.999) * 30일 * 24시간 * 60분 = 43.8분
    error_budget_minutes: 43.8

  - name: "API Latency"
    # SLI: 200ms 이내 응답 비율
    sli:
      good_events: sum(rate(http_request_duration_seconds_bucket{le="0.2"}[30d]))
      total_events: sum(rate(http_request_duration_seconds_count[30d]))
    objective: 95.0  # p95가 200ms 이내
```

---

## 8. 미래 트렌드

**AIOps**는 AI와 머신러닝을 운영에 적용하는 방향이다. 이상 감지(Anomaly Detection)는 고정 임계값 대신 ML 모델이 시계열 패턴을 학습해 평소와 다른 상황을 자동으로 탐지한다. 원인 분석(Root Cause Analysis)도 점점 자동화되고 있다. 하지만 AI가 잘못된 방향으로 학습하면 오히려 장애를 놓칠 수 있어, 인간의 감독이 여전히 필요하다.

**Platform Engineering**은 내부 개발자 플랫폼(IDP, Internal Developer Platform)을 구축해 개발팀이 인프라를 셀프서비스로 사용할 수 있게 하는 접근이다. DevOps가 개발과 운영의 협업을 강조했다면, Platform Engineering은 운영 지식을 플랫폼에 내재화해서 개발자가 쿠버네티스 YAML을 직접 다루지 않아도 되게 만드는 방향이다.

**FinOps**는 클라우드 비용을 엔지니어링 문제로 다루는 분야다. 모니터링이 "시스템이 살아있는가"를 묻는다면, FinOps는 "비용 대비 가치가 있는가"를 묻는다. Prometheus 메트릭에 비용 레이블을 붙여 서비스별 클라우드 지출을 추적하고, 과잉 프로비저닝된 리소스를 자동으로 줄이는 방향으로 발전하고 있다.

---

## 9. 명령어 요약

```bash
# Prometheus
# 설정 파일 문법 검증
promtool check config prometheus.yml
# 알림 규칙 파일 검증
promtool check rules rules/alert_rules.yml
# 특정 시점의 데이터 쿼리 (디버깅용)
promtool query instant http://localhost:9090 'up'

# Grafana
# 대시보드 JSON 파일 임포트 (grafana-cli 또는 API)
curl -X POST http://admin:admin@localhost:3000/api/dashboards/import \
  -H 'Content-Type: application/json' \
  -d @dashboard.json

# Alertmanager
# 현재 발화 중인 알림 확인
curl http://localhost:9093/api/v2/alerts | jq '.[] | {alertname: .labels.alertname, status: .status.state}'
# 알림 억제(Silence) 생성 (유지보수 시간 동안)
amtool silence add alertname=HighErrorRate --duration=2h --comment="배포 중 알림 억제"

# OpenTelemetry
# Collector 상태 확인
curl http://localhost:13133/  # Health Check 엔드포인트
# 수신된 스팬 수 확인 (Collector 메트릭)
curl http://localhost:8888/metrics | grep otelcol_receiver_accepted_spans
```

---

## 10. 체크포인트

- [ ] Prometheus가 Pull 방식인 이유와 Push 방식과의 트레이드오프를 설명할 수 있다.
- [ ] Recording Rule과 Alerting Rule의 차이점을 안다.
- [ ] Grafana 대시보드에서 변수(templating)를 사용해 동적 쿼리를 만들 수 있다.
- [ ] `for: 5m` 설정이 Alert Fatigue 방지에 어떻게 기여하는지 설명할 수 있다.
- [ ] OpenTelemetry에서 Context Propagation이 왜 필요한지, W3C TraceContext 헤더가 어떤 역할을 하는지 안다.
- [ ] 99.9% SLO의 월간 에러 버짓(분)을 계산할 수 있다.
- [ ] 구조화된 JSON 로그가 console.log보다 나은 이유를 Trace ID 연계 관점에서 설명할 수 있다.
