# 최소 자원 중앙 집중 로깅 시스템 도입 제안서

> **요약**: 중앙 집중 로깅 없이는 장애 대응 시간이 길어지고, 보안 감사 추적이 불가능하며, 크로스팀 가시성이 확보되지 않는다. Loki + Alloy + Grafana 조합은 약 500MB RAM으로 운영 가능한 최소 자원 로깅 시스템이며, ELK 대비 CPU 5배, 스토리지 63% 절감이 검증되었다. 본 문서는 대안 비교와 구체적 벤치마크를 통해 도입 근거를 제시한다.

---

## 1. 왜 중앙 집중 로깅이 필수인가

### 장애 대응: SSH 개별 접속의 한계

서버가 3대일 때는 SSH로 각각 접속해 로그를 확인하는 것이 가능하다. 하지만 서버가 10대를 넘어가면 이야기가 달라진다. 장애 발생 시 어느 서버에서 문제가 시작됐는지 파악하려면 모든 서버에 순차 접속해야 하고, 시간 동기화가 안 된 로그를 수동으로 대조해야 한다. 이 과정에서 MTTR(평균 복구 시간)이 수십 분에서 수 시간으로 늘어난다.

중앙 집중 로깅이 있으면 하나의 대시보드에서 모든 서버 로그를 시간순으로 검색할 수 있다. "500 에러가 발생한 시점 전후 5분간 모든 서버 로그"를 한 번의 쿼리로 확인할 수 있다는 것은 장애 대응 속도에 결정적 차이를 만든다.

### 보안 컴플라이언스: 감사 추적 요구

GDPR, PCI-DSS, SOC2 등 주요 보안 프레임워크는 공통적으로 감사 로그의 중앙 수집과 보관을 요구한다. PCI-DSS 10.2~10.3은 접근 로그의 중앙 집중 수집과 최소 1년 보관을 명시하고 있고, SOC2 CC7.2는 보안 이벤트의 탐지와 분석을 위한 모니터링 체계를 요구한다. 감사 시 "이 시점에 누가 어떤 데이터에 접근했는가?"라는 질문에 답하려면, 분산된 로그 파일을 뒤지는 것이 아니라 중앙 시스템에서 즉시 쿼리할 수 있어야 한다.

### DevOps: 크로스팀 가시성

CI/CD 파이프라인의 신뢰성은 배포 후 문제를 얼마나 빠르게 발견하느냐에 달려 있다. 개발팀이 배포하고, 운영팀이 장애를 감지하고, 다시 개발팀에 전달하는 과정에서 로그를 공유할 수 있는 단일 플랫폼이 없으면 커뮤니케이션 비용이 기하급수적으로 증가한다. 중앙 로깅은 "같은 화면을 보고 대화하는 것"을 가능하게 한다.

---

## 2. 최소 로깅 시스템 대안 비교

| 조합 | 구성 | 최소 메모리 | 라이선스 | 장점 | 단점 |
|------|------|-----------|---------|------|------|
| **Loki + Alloy + Grafana** | Go 바이너리 3개 | ~500MB | Apache 2.0 | 최소 자원, OTel 호환, 확장 경로 명확 | 전문 검색(full-text) 약함 |
| **ELK** (Elasticsearch + Logstash + Kibana) | JVM 3개 | ~4-6GB | Elastic License 2.0 | 전문 검색 강력, 생태계 성숙 | JVM 메모리 과다, 운영 복잡 |
| **EFK** (Elasticsearch + Fluentd + Kibana) | JVM 2개 + Ruby 1개 | ~3-5GB | 혼합 | Fluentd가 Logstash보다 가벼움 | 여전히 ES 메모리 문제 |
| **PLG** (Promtail + Loki + Grafana) | Go 3개 | ~500MB | Apache 2.0 | Loki+Alloy와 유사 | Promtail EOL (2026-03-02) |
| **CloudWatch / Datadog** | SaaS | 0 (에이전트만) | 종량제 | 인프라 운영 불필요 | 비용 급증, 벤더 락인 |
| **OpenSearch + Fluent Bit** | JVM 1개 + C 1개 | ~2-4GB | Apache 2.0 | ES 포크, 진정한 오픈소스 | JVM 기반 메모리 부담 |
| **Vector + ClickHouse** | Rust + C++ | ~500MB-1GB | 혼합 | 초고속 분석 쿼리 | 운영 복잡, 생태계 초기 |

**핵심 판단 기준**: 서버 자원이 제한된 환경에서 "최소한의 메모리와 CPU로 중앙 로깅을 확보할 수 있는가?"이다. JVM 기반 솔루션(ELK, EFK, OpenSearch)은 Elasticsearch 단독으로 최소 2GB 힙을 요구하므로, 소규모 환경에서는 과도한 자원 소비가 불가피하다.

---

## 3. Loki + Alloy가 최소 자원에 최적인 이유

### 아키텍처 차이: 라벨 인덱싱 vs 전문 인덱싱

Elasticsearch는 로그의 모든 필드를 역 인덱스(inverted index)로 만든다. "error"라는 단어가 포함된 로그를 밀리초 안에 찾을 수 있지만, 그 대가로 원본 데이터와 맞먹는 크기의 인덱스를 메모리와 디스크에 유지해야 한다.

Loki는 완전히 다른 접근을 취한다. 로그 본문은 인덱싱하지 않고, 메타데이터 라벨(서비스명, 환경, 호스트 등)만 인덱싱한다. 검색 시에는 라벨로 로그 스트림을 좁힌 뒤, 해당 스트림 안에서 grep 방식으로 텍스트를 찾는다. 이 설계 덕분에 인덱스 크기가 극적으로 작아지고, 필요한 메모리와 CPU가 대폭 줄어든다.

전문 검색이 필요한 사용 사례(보안 로그 분석, 복잡한 패턴 매칭)에서는 Elasticsearch가 유리하지만, 대부분의 운영 로깅 시나리오에서는 "이 서비스에서 최근 1시간 내 에러 로그"를 찾는 것이 주된 쿼리 패턴이다. Loki는 이 패턴에 최적화되어 있다.

### Grafana Alloy: 단일 바이너리로 수집 통합

Grafana Alloy는 2024년 GrafanaCON에서 발표된 오픈소스 OpenTelemetry Collector 배포판이다. 기존의 Promtail(로그 수집), Grafana Agent(메트릭 수집)를 하나의 바이너리로 통합했다.

Promtail은 2025년 2월 13일 LTS에 진입했고, 2026년 3월 2일 EOL이 되었다. Grafana Agent도 2025년 11월 1일 EOL이 되었다. 두 도구 모두 공식적으로 Alloy로 대체되었으며, Promtail 설정을 Alloy 설정으로 변환하는 마이그레이션 도구(`alloy convert`)가 제공된다.

Alloy의 자원 사용량은 Grafana 공식 문서 기준으로 다음과 같다:

| 수집 유형 | CPU | 메모리 |
|----------|-----|--------|
| 로그 1 MiB/s 수집 | 1 코어 | 120 MiB |
| Prometheus 메트릭 100만 시리즈 | 0.4 코어 | 11 GiB |

> 출처: [Grafana Alloy Resource Usage](https://grafana.com/docs/alloy/latest/introduction/estimate-resource-usage/)

일반적인 소규모 환경(서버 5~10대, 로그 수십 MiB/s 미만)에서 Alloy는 100~200MB 메모리면 충분하다.

---

## 4. 벤치마크: 구체적 숫자로 본 차이

### SigNoz 벤치마크 (Loki vs Elasticsearch)

테스트 환경: EC2 c6a.4xlarge(16 vCPU, 32 GB RAM), 500GB 로그 데이터 수집

| 지표 | Loki | Elasticsearch | 차이 |
|------|------|--------------|------|
| **수집 속도** | 21,000 logs/sec | 20,000 logs/sec | 유사 |
| **총 수집 시간** (500GB) | 3시간 20분 | 5시간 27분 | **Loki 39% 빠름** |
| **CPU 사용률** | 15% | 75% | **Loki 5배 적음** |
| **메모리 사용** (32GB 중) | ~9.6GB (30%) | ~18GB (60%) | **Loki 47% 적음** |
| **디스크 I/O** | ~50 MiB/s | ~180 MiB/s | **Loki 72% 적음** |
| **저장 용량** (500GB 원본) | 142GB | 388GB | **Loki 63% 적음** |

> 출처: [SigNoz Logs Performance Benchmark](https://signoz.io/blog/logs-performance-benchmark/)

이 벤치마크에서 주목할 점은 CPU 사용률 차이다. Elasticsearch가 75%의 CPU를 소비하는 동안 Loki는 15%만 사용한다. 이는 같은 서버에서 다른 워크로드와 공존할 수 있는 여지가 크다는 뜻이다. 스토리지 역시 Loki가 500GB 원본을 142GB로 압축하는 반면, Elasticsearch는 388GB를 사용한다.

단, Loki는 고카디널리티 라벨(예: traceId를 라벨로 사용) 사용 시 max stream 에러가 발생할 수 있다는 점을 주의해야 한다. 이는 Loki의 설계 철학(라벨은 낮은 카디널리티로 유지)에 기인하므로, 라벨 설계 시 서비스명, 환경, 호스트명 정도로 제한하는 것이 권장된다.

### 비용 비교: SaaS vs 셀프호스팅

월 600GB 로그 수집 기준 비용 비교:

| 항목 | CloudWatch | Datadog | Grafana Cloud | 셀프호스팅 Loki |
|------|-----------|---------|--------------|----------------|
| **수집 비용** | $300/월 ($0.50/GB) | $60/월 ($0.10/GB) | $330/월 (~$0.55/GB) | $0 |
| **인덱싱/저장** | $18/월 ($0.03/GB) | $1,020/월 ($1.70/백만 이벤트) | 포함 | ~$7/월 (S3) |
| **컴퓨팅** | 포함 | 포함 | 포함 | ~$30/월 (t3.medium) |
| **월 총비용** | **~$318** | **~$1,080** | **~$330** | **~$37** |
| **연간 총비용** | **~$3,816** | **~$12,960** | **~$3,960** | **~$444** |

> 출처: [AWS CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/), [Datadog Pricing](https://www.datadoghq.com/pricing/), [Grafana Cloud Pricing](https://grafana.com/pricing/)

Datadog의 실제 비용 핵심은 수집 비용이 아니라 인덱싱 비용이다. 표준 인덱싱(15일 보관)이 100만 이벤트당 $1.70이므로, 1KB 평균 로그 기준 1GB = 약 100만 이벤트 = $1.70 추가 비용이 발생한다. 600GB면 월 $1,020의 인덱싱 비용만으로도 셀프호스팅의 연간 비용을 초과한다.

셀프호스팅의 비용 추정에는 운영 인력 비용이 포함되지 않았다. 하지만 Loki monolithic 모드는 설정이 단순하여 초기 구축 후 운영 부담이 크지 않으며, 이는 뒤의 최소 배포 구성에서 확인할 수 있다.

---

## 5. 최소 배포 구성 예시

### Docker Compose (가장 빠른 시작)

```yaml
# docker-compose.yml
# Loki + Alloy + Grafana 최소 구성
# 총 메모리: ~500MB, 디스크: 로그량에 비례

services:
  loki:
    image: grafana/loki:3.4.3
    command: -config.file=/etc/loki/local-config.yaml
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
    deploy:
      resources:
        limits:
          memory: 256M

  alloy:
    image: grafana/alloy:v1.14.0
    command:
      - run
      - /etc/alloy/config.alloy
      - --server.http.listen-addr=0.0.0.0:12345
    volumes:
      - ./alloy-config.alloy:/etc/alloy/config.alloy:ro
      - /var/log:/var/log:ro          # 호스트 로그 수집
    depends_on:
      - loki
    deploy:
      resources:
        limits:
          memory: 128M

  grafana:
    image: grafana/grafana:11.6.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana-datasources.yaml:/etc/grafana/provisioning/datasources/ds.yaml:ro
    depends_on:
      - loki
    deploy:
      resources:
        limits:
          memory: 128M

volumes:
  loki-data:
  grafana-data:
```

```hcl
// alloy-config.alloy
// 호스트 로그 수집 → Loki 전송 최소 설정

local.file_match "logs" {
  path_targets = [
    {__path__ = "/var/log/*.log", job = "varlogs"},
  ]
}

loki.source.file "log_scrape" {
  targets    = local.file_match.logs.targets
  forward_to = [loki.write.local.receiver]
}

loki.write "local" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}
```

```yaml
# grafana-datasources.yaml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    isDefault: true
```

이 구성으로 `docker compose up -d` 한 번이면 로깅 시스템이 가동된다. Grafana(`localhost:3000`)에 접속하면 Loki 데이터소스가 자동 설정되어 있고, Explore 탭에서 즉시 로그 쿼리가 가능하다.

### Kubernetes Helm 최소 구성

```bash
# Loki (monolithic 모드)
helm install loki grafana/loki \
  --set deploymentMode=SingleBinary \
  --set singleBinary.replicas=1 \
  --set singleBinary.resources.limits.memory=256Mi \
  --set loki.commonConfig.replication_factor=1 \
  --set loki.storage.type=filesystem

# Alloy (DaemonSet으로 각 노드 로그 수집)
helm install alloy grafana/alloy \
  --set alloy.configMap.content="$(cat alloy-config.alloy)"

# Grafana
helm install grafana grafana/grafana \
  --set resources.limits.memory=128Mi \
  --set datasources."datasources\.yaml".apiVersion=1 \
  --set datasources."datasources\.yaml".datasources[0].name=Loki \
  --set datasources."datasources\.yaml".datasources[0].type=loki \
  --set datasources."datasources\.yaml".datasources[0].url=http://loki:3100
```

### Loki Monolithic 모드 한계

Grafana 공식 문서에 따르면, Loki monolithic(단일 바이너리) 모드는 **하루 최대 약 20GB** 로그를 처리할 수 있다. 이를 초과하면 마이크로서비스 모드로의 전환이 권장된다.

하루 20GB는 어느 정도 규모일까?

- 1KB 평균 로그 기준 약 2,000만 줄/일
- 서버 10대가 각각 초당 ~23줄 로그 생성하는 수준
- 대부분의 소규모~중규모 서비스에서 충분한 처리량

> 출처: [Loki Deployment Modes](https://grafana.com/docs/loki/latest/get-started/deployment-modes/)

---

## 6. 단계적 도입 제안

한 번에 전체 관측성 스택을 구축하는 것은 부담이 크다. 아래와 같이 단계적으로 도입하면 각 단계에서 즉시 가치를 얻으면서, 점진적으로 관측성 수준을 높일 수 있다.

### Phase 1: 로그 수집 (최소 구성)

```
[서버 로그] → Alloy → Loki → Grafana
                                  ↑
                             로그 검색/대시보드
```

- **구성**: Loki + Alloy + Grafana (3개 컨테이너)
- **자원**: ~500MB RAM, CPU 최소
- **달성 목표**: 중앙 집중 로그 검색, 장애 시 단일 대시보드 확인
- **소요 시간**: Docker Compose 기준 30분 이내

### Phase 2: 메트릭 추가

```
[서버 메트릭] → Alloy → Prometheus → Grafana
[서버 로그]  → Alloy → Loki      ↗
```

- **추가 구성**: Prometheus (또는 Grafana Mimir)
- **추가 자원**: ~500MB RAM
- **달성 목표**: CPU/메모리/디스크 메트릭 모니터링, 알림 설정
- **핵심 가치**: Alloy가 이미 설치되어 있으므로, 메트릭 수집 설정만 추가하면 된다. 별도 에이전트 설치가 불필요하다.

### Phase 3: 트레이스 추가 (풀 관측성)

```
[서버 메트릭] → Alloy → Prometheus → Grafana
[서버 로그]  → Alloy → Loki      ↗
[서버 트레이스] → Alloy → Tempo    ↗
```

- **추가 구성**: Grafana Tempo
- **추가 자원**: ~256MB RAM
- **달성 목표**: 분산 트레이싱, 요청 흐름 추적, 로그-트레이스 연결
- **핵심 가치**: 로그에서 traceId 클릭 → 해당 요청의 전체 흐름을 시각적으로 확인

각 Phase는 독립적으로 동작하며, 이전 Phase의 구성을 변경하지 않고 추가만 하면 된다. Alloy가 수집 계층을 통합하고 있기 때문에, Phase 2~3에서 새로운 수집 에이전트를 설치할 필요가 없다.

---

## 7. FAQ

**Q: Loki는 전문 검색이 안 되면 불편하지 않은가?**

Loki의 LogQL은 라벨 필터링 후 `|= "error"`, `|~ "timeout|connection refused"` 같은 텍스트 필터링을 지원한다. 로그 분석의 90% 이상은 "특정 서비스의 특정 시간대에서 특정 키워드 검색"이므로, 이 패턴에서는 Elasticsearch와 체감 차이가 거의 없다. 다만, 수백만 줄에서 복잡한 정규식 검색이 빈번하다면 Elasticsearch가 유리하다.

**Q: Loki가 죽으면 로그가 유실되지 않는가?**

Alloy는 로컬에 WAL(Write-Ahead Log)을 유지하므로, Loki가 일시적으로 다운되더라도 Alloy가 버퍼링했다가 Loki 복구 시 재전송한다. 물론, Alloy 자체가 죽는 동안의 로그는 수집되지 않는다.

**Q: 이미 ELK를 쓰고 있는데 마이그레이션이 어렵지 않은가?**

Loki는 ELK를 완전히 대체할 필요가 없다. Alloy는 동시에 여러 대상으로 로그를 전송할 수 있으므로, 기존 ELK를 유지하면서 Loki를 병렬로 운영하다가 점진적으로 전환하는 것이 가능하다.

---

## 8. 결론

| 판단 기준 | ELK | SaaS (Datadog/CW) | **Loki + Alloy + Grafana** |
|----------|-----|-------------------|---------------------------|
| 최소 메모리 | 4-6GB | 0 (에이전트만) | **~500MB** |
| 연간 비용 (600GB/월) | 서버 비용 | $3,800~$13,000 | **~$444 (셀프호스팅)** |
| 설치 난이도 | 높음 (JVM 튜닝) | 낮음 | **낮음 (Docker Compose)** |
| 확장 경로 | ES 클러스터링 | 비용 증가 | **Prometheus/Tempo 추가** |
| 벤더 종속 | Elastic License | 높음 | **없음 (Apache 2.0)** |
| 전문 검색 | 강력 | 강력 | 제한적 (라벨+grep) |

Loki + Alloy + Grafana는 "최소 자원으로 중앙 집중 로깅을 시작하는 것"에 가장 적합한 조합이다. 500MB RAM과 Docker Compose 파일 하나로 30분 안에 구축할 수 있고, 필요에 따라 메트릭과 트레이싱으로 확장할 수 있다. 전문 검색이 약하다는 단점이 있지만, 운영 로깅의 대부분은 라벨 필터링 + 텍스트 검색으로 충분히 커버된다.

비용 측면에서도 월 600GB 로그 기준 연간 $444로, SaaS 대비 최소 8배 이상 저렴하다. ELK 대비해서는 동일 서버에서 5배 적은 CPU를 사용하므로, 기존 서버 자원을 최대한 활용할 수 있다.

**권장 행동**: Phase 1(로그만) Docker Compose 구성을 개발 환경에 먼저 배포하고, 2주간 운영하며 팀 피드백을 수집한 뒤 스테이징/프로덕션으로 확대한다.

---

## 출처

| # | 출처 | 내용 | URL |
|---|------|------|-----|
| 1 | SigNoz Blog | Loki vs ES 벤치마크 (CPU, RAM, 스토리지) | https://signoz.io/blog/logs-performance-benchmark/ |
| 2 | AWS | CloudWatch Logs 가격 ($0.50/GB 수집) | https://aws.amazon.com/cloudwatch/pricing/ |
| 3 | Datadog | Log Management 가격 ($1.70/백만 이벤트 인덱싱) | https://www.datadoghq.com/pricing/ |
| 4 | Grafana | Grafana Cloud 가격 (~$0.55/GB) | https://grafana.com/pricing/ |
| 5 | Grafana | Loki 배포 모드 (monolithic ~20GB/일) | https://grafana.com/docs/loki/latest/get-started/deployment-modes/ |
| 6 | Grafana | Loki 클러스터 사이징 | https://grafana.com/docs/loki/latest/setup/size/ |
| 7 | Grafana | Alloy 자원 사용량 (1 CPU + 120MiB / 1 MiB/s) | https://grafana.com/docs/alloy/latest/introduction/estimate-resource-usage/ |
| 8 | Grafana | Promtail EOL (2026-03-02) | https://grafana.com/docs/loki/latest/send-data/promtail/ |
| 9 | Grafana | Grafana Agent EOL (2025-11-01) | https://grafana.com/docs/agent/latest/static/ |
| 10 | Grafana | Promtail → Alloy 마이그레이션 가이드 | https://grafana.com/docs/alloy/latest/tasks/migrate/from-promtail/ |
