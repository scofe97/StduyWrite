# 02. Redpanda Connect 데이터 파이프라인 (Benthos)

> **시리즈**: `learning/07-connectors/` — Redpanda 커넥터 통합 학습
> | [01-이론](./01-source-sink-patterns.md) | **[02-Redpanda Connect](./02-redpanda-connect.md)** | [03-Spring Boot](./03-spring-boot-impl.md) | [04-운영](./04-operations.md) | [05-Helm 배포](./05-helm-deployment.md) |

Redpanda Connect(구 Benthos)는 Go 기반 단일 바이너리(20MB)로, YAML 선언만으로 데이터 파이프라인을 구성한다. 300개 이상의 커넥터가 내장되어 있고, at-least-once 보장이 내장되어 있다. 커넥터 설계 철학과 Kafka Connect 비교는 [01-source-sink-patterns.md §3](./01-source-sink-patterns.md)을 참조한다.

---

## Connect의 역할 경계

Connect는 서비스 사이에서 데이터를 변환·라우팅하는 **인프라 접착제(glue)**다. 비즈니스 로직을 처리하는 도구가 아니다.

| 작업 | Connect | 애플리케이션 코드 |
|------|---------|-----------------|
| 필드 매핑·포맷 변환 (JSON ↔ Avro) | ✅ | 가능하지만 과한 편 |
| 조건부 라우팅 (토픽 분기) | ✅ | 가능 |
| 프로토콜 브릿징 (HTTP → Kafka → DB) | ✅ | 가능 |
| 재시도·DLQ (인프라 에러 처리) | ✅ | 가능 |
| 잔고 확인 → 차감 (상태 읽기+쓰기) | ❌ | ✅ |
| DB + 메시지 원자적 처리 (트랜잭션) | ❌ | ✅ (Outbox, @Transactional) |
| 복잡한 분기 (if-else 3단+) | ❌ 가독성 붕괴 | ✅ |
| 단위 테스트 | YAML 테스트 도구 부족 | ✅ (JUnit, Mockito) |

경계를 구분하는 기준은 단순하다.

```
데이터를 보고 → 변환/라우팅           → Connect
상태를 읽고 → 판단하고 → 상태를 변경   → 애플리케이션 코드
```

Bloblang은 데이터 변환 DSL이지 범용 프로그래밍 언어가 아니라서, 상태 관리나 트랜잭션 기능이 없다. 예를 들어 "주문 이벤트를 Elasticsearch에 적재"는 Connect로 충분하지만, "주문 이벤트를 받아서 재고를 차감하고, 부족하면 취소 이벤트 발행"은 Spring Boot 같은 애플리케이션 코드의 영역이다.

---

## Redpanda Connect 아키텍처

### 파이프라인 구조

```mermaid
flowchart LR
    subgraph "Redpanda Connect Pipeline"
        direction LR
        I["Input<br>(소스 읽기)"]
        P["Pipeline<br>(Processor 변환)"]
        O["Output<br>(목적지 전달)"]
        B["Buffer<br>(선택, 백프레셔)"]

        I --> P --> O
        B -. "백프레셔 시\n메시지 보관" .-> O
    end

    EXT_IN["Kafka / HTTP<br>S3 / PostgreSQL<br>Webhook ..."] --> I
    O --> EXT_OUT["Kafka / HTTP<br>S3 / PostgreSQL<br>Elasticsearch ..."]

    style I fill:#e8f4fd,stroke:#2980b9,color:#333
    style P fill:#fef9e7,stroke:#f39c12,color:#333
    style O fill:#e8f8f5,stroke:#27ae60,color:#333
    style B fill:#f9f9f9,stroke:#95a5a6,color:#333
```

4개 컴포넌트는 독립적으로 교체할 수 있다. Input이 Kafka인지 HTTP인지에 관계없이 Pipeline의 변환 로직은 동일하게 동작하고, Output 역시 PostgreSQL이든 Elasticsearch든 상관없이 Pipeline의 결과를 받는다.

| 컴포넌트 | 역할 | 예시 |
|----------|------|------|
| **Input** | 데이터 소스에서 메시지를 읽어들인다 | Kafka, HTTP, S3, PostgreSQL, Webhook |
| **Pipeline** | 메시지를 변환하거나 필터링한다 | Bloblang, JSON 파싱, 필드 추출 |
| **Output** | 변환된 메시지를 목적지로 전달한다 | Kafka, HTTP, S3, PostgreSQL, Elasticsearch |
| **Buffer** | 백프레셔 발생 시 메시지를 임시 보관한다 (선택) | 메모리, 디스크 기반 버퍼 |

### 관측성 설정 (Observability)

파이프라인 YAML 탑레벨에 `metrics`, `logger`, `tracer` 세 가지 관측성 설정을 선언할 수 있다.

| 설정 | 역할 | 기본값 | 상세 |
|------|------|--------|------|
| **metrics** | 처리량, 지연시간, 에러 수 등 Prometheus `/metrics`로 노출 | 비활성 | [04-operations.md §4](./04-operations.md) |
| **logger** | 파이프라인 이벤트를 구조화된 로그로 stdout 출력 | `level: INFO`, `format: logfmt` | [06-error-recovery.md §4](./06-error-recovery.md) |
| **tracer** | 분산 추적 span을 OTLP/Jaeger로 전송 | 비활성 | [04-operations.md §4](./04-operations.md) |

> 관측성 설정 YAML 예시, 구조화 로깅(`static_fields`, `fields_mapping`), Prometheus 메트릭 상세, Loki 연계는 [06-error-recovery.md §4~§5](./06-error-recovery.md)와 [04-operations.md §4](./04-operations.md)를 참조한다.

### 파일 구조

**파이프라인별 단일 파일 (기본)**

```
connect/
├── orders-to-elastic.yaml
├── users-to-postgres.yaml
├── webhook-to-kafka.yaml
└── dlq-reprocess.yaml
```

하나의 YAML = 하나의 파이프라인이다. `rpk connect run orders-to-elastic.yaml`처럼 파일을 지정해서 실행한다.

### rpk connect CLI 명령어

Redpanda Connect는 `rpk`와 별도의 프로젝트다. `rpk`는 Redpanda 브로커 관리 도구이고, Redpanda Connect(구 Benthos)는 Go 기반 데이터 파이프라인 런타임이다. Docker 이미지도 다르다(`redpandadata/redpanda` vs `redpandadata/connect`). `rpk connect`는 rpk가 Redpanda Connect 바이너리를 래핑하여 호출하는 것이므로, Redpanda 없이도 `redpanda-connect` 바이너리로 독립 실행할 수 있다.

> rpk 브로커 관리 명령어(topic, group, cluster 등)는 [02-fundamentals/appendix-rpk-cli.md](../02-fundamentals/appendix-rpk-cli.md)를 참조한다.

| 명령어 | 용도 | 비고 |
|--------|------|------|
| `rpk connect run <file>` | 단일 파이프라인 실행 | 가장 기본적인 실행 방식 |
| `rpk connect streams [dir]` | Streams Mode (멀티 파이프라인) | REST API로 동적 관리 가능 — 아래 상세 |
| `rpk connect lint <file>` | YAML 문법 검증 | CI에서 배포 전 검증에 활용 |
| `rpk connect test <file>` | 단위 테스트 실행 | YAML 내 `tests:` 블록 실행 |
| `rpk connect list <type>` | 사용 가능한 컴포넌트 조회 | inputs, outputs, processors, caches 등 |
| `rpk connect create <type>/<name>` | 컴포넌트 템플릿 생성 | 빈 YAML 스캐폴딩 |

#### `rpk connect run` — 단일 파이프라인

가장 많이 쓰는 명령어다. YAML 파일 하나를 지정하면 해당 파이프라인이 foreground로 실행된다.

```bash
# 기본 실행
rpk connect run pipeline.yaml

# 환경변수 주입 (YAML 내 ${VAR} 치환)
BROKER_URL=localhost:19092 rpk connect run pipeline.yaml

# 설정 오버라이드 (CLI에서 직접 값 지정)
rpk connect run pipeline.yaml --set input.kafka_franz.seed_brokers=localhost:19092

# 로그 레벨 변경
rpk connect run --log.level DEBUG pipeline.yaml
```

`--set` 플래그는 YAML의 특정 필드를 CLI에서 오버라이드할 때 쓴다. 환경별로 브로커 주소만 다른 경우, YAML을 복사하지 않고 `--set`으로 해결할 수 있다.

#### `rpk connect lint` — 배포 전 검증

파이프라인 YAML의 문법 오류를 실행 전에 잡는다. CI/CD 파이프라인에서 배포 전 검증 단계로 사용하면 런타임 에러를 방지할 수 있다.

```bash
# 단일 파일 검증
rpk connect lint pipeline.yaml

# 디렉토리 전체 검증
rpk connect lint ./connect/*.yaml

# 성공 시 출력 없음 (exit code 0), 실패 시 에러 위치 표시
# 예: pipeline.yaml:15:5 field 'tpic' not recognised
```

`lint`는 필드명 오타, 필수 필드 누락, 잘못된 중첩 구조를 감지한다. 다만 **값의 유효성**(브로커 주소 접속 가능 여부, 토픽 존재 여부)은 검증하지 않는다. 그건 런타임에만 확인할 수 있다.

#### `rpk connect test` — YAML 단위 테스트

파이프라인 YAML 안에 `tests:` 블록을 선언하면, 실제 외부 시스템 없이 변환 로직을 테스트할 수 있다.

```yaml
# pipeline.yaml
pipeline:
  processors:
    - mapping: |
        root.full_name = this.first_name + " " + this.last_name
        root.age_group = if this.age >= 18 { "adult" } else { "minor" }

tests:
  - name: "성인 사용자 변환"
    input_batch:
      - content: '{"first_name":"Kim","last_name":"Minsoo","age":25}'
    output_batches:
      - - json_equals:
            full_name: "Kim Minsoo"
            age_group: "adult"

  - name: "미성년자 변환"
    input_batch:
      - content: '{"first_name":"Lee","last_name":"Jiyoung","age":15}'
    output_batches:
      - - json_equals:
            age_group: "minor"
```

```bash
rpk connect test pipeline.yaml
# 출력: Test 'pipeline.yaml' succeeded
```

`tests:` 블록은 파이프라인 실행 시 무시되므로, 테스트 코드를 파이프라인 파일에 같이 둬도 문제없다. Bloblang 변환 로직이 복잡해질수록 이 테스트의 가치가 올라간다.

#### `rpk connect list` — 컴포넌트 카탈로그

Redpanda Connect에 내장된 300개 이상의 컴포넌트를 카테고리별로 조회한다.

```bash
# 사용 가능한 Input 목록
rpk connect list inputs

# Output 목록
rpk connect list outputs

# Processor 목록
rpk connect list processors

# Cache 목록
rpk connect list caches
```

새 파이프라인을 설계할 때 "이 소스/목적지를 지원하는 컴포넌트가 있는가?"를 확인하는 용도로 쓴다.

#### `rpk connect create` — 템플릿 생성

컴포넌트의 기본 YAML 구조를 출력한다. 공식 문서를 찾아보는 대신 CLI에서 바로 스캐폴딩할 수 있다.

```bash
# kafka_franz Input 템플릿
rpk connect create input/kafka_franz

# http_client Output 템플릿
rpk connect create output/http_client
```

출력된 YAML을 복사해서 필요한 값만 채우면 되므로, 빈 파일에서 시작하는 것보다 빠르고 필드 누락 실수를 줄일 수 있다.

#### Docker 실행

Redpanda Connect는 전용 Docker 이미지(`redpandadata/connect`)로 실행한다. rpk 이미지(`redpandadata/redpanda`)와 **별개**다.

```bash
# 단일 파이프라인
docker run --rm -v $(pwd)/pipeline.yaml:/pipeline.yaml \
  redpandadata/connect run /pipeline.yaml

# Streams Mode
docker run --rm -p 4195:4195 -v $(pwd)/streams:/streams \
  redpandadata/connect streams /streams/*.yaml
```

```yaml
# docker-compose.yml
services:
  connect-jenkins:
    image: redpandadata/connect:4.43
    volumes:
      - ./connect/jenkins-webhook.yaml:/pipeline.yaml
    command: ["run", "/pipeline.yaml"]
    depends_on:
      - redpanda
```

Helm 기반 K8s 배포는 [05-helm-deployment.md](./05-helm-deployment.md)를 참조한다.

**스트림 모드 (여러 파이프라인 동시 실행)**

```
connect/
├── streams/
│   ├── orders-to-elastic.yaml
│   ├── users-to-postgres.yaml
│   └── webhook-to-kafka.yaml
└── resources.yaml              # 공유 리소스 (캐시, rate_limit 등)
```

`rpk connect streams connect/streams/*.yaml`로 디렉토리 단위 실행하면, 프로세스 하나가 여러 파이프라인을 관리한다. 다만 하나의 파이프라인이 크래시하면 프로세스 전체가 영향받을 수 있으므로, 격리가 중요한 환경에서는 단일 파일 방식이 낫다.

### Streams Mode — 런타임 파이프라인 관리

Streams Mode는 REST API를 통해 **런타임에** 파이프라인을 CRUD할 수 있어서, 외부 시스템(Web UI, CI/CD 등)과의 자동 연계가 가능해진다. `rpk connect run`으로 실행한 정적 파이프라인과 Streams Mode는 **같은 프로세스에서 공존할 수 있다**. `-o` 옵션으로 정적 설정(관측성, 공유 리소스)을 로드하면서 REST API로 동적 파이프라인을 추가하는 구성이 가능하다.

| 모드 | 명령어 | 동적 관리 | 정적 파이프라인 병행 |
|------|--------|:---:|:---:|
| 단일 파일 | `rpk connect run pipeline.yaml` | ❌ | - |
| 디렉토리 | `rpk connect streams ./streams/*.yaml` | ❌ (재시작 필요) | ✅ (YAML 파일이 초기 로드됨) |
| **Streams Mode** | `rpk connect streams` (YAML 없이) | ✅ (REST API) | ✅ (`-o` 옵션) |

```bash
# Streams Mode 시작 (빈 상태, REST API로만 관리)
rpk connect streams

# 초기 파이프라인 + 관측성 설정 + 공유 리소스 포함
rpk connect streams ./streams/*.yaml -o ./observability.yaml -r ./resources/*.yaml
```

`-o` 옵션은 **관측성 전용 YAML**을 지정하는 플래그다. 파이프라인이 아닌 `metrics`, `logger`, `tracer` 설정만 담은 파일을 로드한다. 이 설정은 모든 동적 파이프라인에 공통 적용된다.

```yaml
# observability.yaml — -o 옵션으로 로드되는 파일
metrics:
  prometheus:
    path: /metrics
    port: 9090

logger:
  level: INFO
  format: json
  static_fields:
    service: "connect-streams"
```

`-r` 옵션은 **공유 리소스**(cache, rate_limit 등)를 로드한다. 여러 동적 파이프라인이 같은 캐시나 Rate Limit을 참조할 때 사용한다.

기동 후 포트 4195에서 REST API가 활성화된다.

#### REST API 엔드포인트

| 동작 | Method | Endpoint |
|------|--------|----------|
| 전체 조회 | GET | `/streams` |
| 생성 | POST | `/streams/{id}` |
| 수정 (전체) | PUT | `/streams/{id}` |
| 수정 (부분) | PATCH | `/streams/{id}` |
| 삭제 | DELETE | `/streams/{id}` |
| 일괄 설정 | POST | `/streams` |
| 헬스체크 | GET | `/ready` |
| 메트릭 | GET | `/streams/{id}/stats` |
| 리소스 관리 | POST | `/resources/{type}/{id}` |

```bash
# 파이프라인 생성 — YAML body
curl -s -X POST http://localhost:4195/streams/webhook-to-kafka \
  -H "Content-Type: application/x-yaml" \
  -d '
input:
  http_server:
    path: /webhook
    allowed_verbs: [POST]
pipeline:
  processors:
    - mapping: "root = this"
output:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topic: webhook-events
'

# 파이프라인 상태 확인
curl -s http://localhost:4195/streams | jq .

# 파이프라인 삭제
curl -s -X DELETE http://localhost:4195/streams/webhook-to-kafka
```

> **환경변수 보간 제한**: REST API로 생성한 파이프라인에서는 `${ENV_VAR}` 형태의 환경변수 보간이 동작하지 않는다. Bloblang 함수 보간(`${! env("ENV_VAR") }`)은 사용 가능하므로, 동적 생성 시에는 함수 보간을 사용해야 한다.

#### Dynamic Inputs/Outputs

Streams API가 파이프라인 단위의 CRUD라면, Dynamic Input/Output은 **하나의 파이프라인 안에서** 개별 Input/Output을 런타임에 교체하는 메커니즘이다. 파이프라인 YAML에 `dynamic` 타입을 선언하면 REST API 엔드포인트가 자동 생성되어, 해당 파이프라인의 Input이나 Output을 추가/교체/삭제할 수 있다.

```yaml
# 파이프라인 YAML — dynamic input 선언
input:
  dynamic:
    inputs:
      initial-source:        # ← 이 label이 REST API 경로가 된다
        kafka_franz:
          seed_brokers: ["localhost:19092"]
          topics: ["events"]
          consumer_group: dynamic-demo

pipeline:
  processors:
    - mapping: "root = this"

output:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topic: processed-events
```

위 파이프라인을 실행하면, `/inputs/{label}` 엔드포인트가 활성화된다.

```bash
# 새 Input 추가 — label "webhook-source"로 HTTP 서버 Input 추가
curl -X POST http://localhost:4195/inputs/webhook-source \
  -H "Content-Type: application/x-yaml" \
  -d 'http_server: { path: /webhook, allowed_verbs: [POST] }'

# 기존 Input 교체 — label "initial-source"의 토픽 변경
curl -X PUT http://localhost:4195/inputs/initial-source \
  -H "Content-Type: application/x-yaml" \
  -d 'kafka_franz: { seed_brokers: ["localhost:19092"], topics: ["events-v2"], consumer_group: dynamic-demo }'

# Input 제거
curl -X DELETE http://localhost:4195/inputs/webhook-source
```

Dynamic Input은 여러 label이 동시에 존재하면 fan-in처럼 동작한다(모든 Input의 메시지가 같은 pipeline으로 합쳐진다). Dynamic Output도 `/outputs/{label}`로 동일한 패턴이며, 여러 label이 있으면 fan-out처럼 모든 Output에 메시지가 복제된다.

#### 실무 시나리오: Jenkins 다중 인스턴스 자동 연계

사용자가 Web UI에서 Jenkins 인스턴스를 등록하면, 백엔드가 Streams API를 호출하여 해당 인스턴스의 빌드 이벤트를 수집하는 파이프라인을 자동 생성하는 구조다. 핵심은 YAML 템플릿과 API 호출 두 가지뿐이다.

```yaml
# jenkins-pipeline-template.yaml — 인스턴스별로 변수만 교체
input:
  http_client:
    url: "${! env(\"JENKINS_URL\") }/api/json?tree=jobs[name,lastBuild[number,result,timestamp]]"
    verb: GET
    headers:
      Authorization: "Bearer ${! env(\"JENKINS_TOKEN\") }"
    timeout: 10s
    retry_period: 30s

pipeline:
  processors:
    - mapping: |
        root.source = "jenkins"
        root.instance_id = env("INSTANCE_ID")
        root.jobs = this.jobs.map_each(job -> {
          "name": job.name,
          "build_number": job.lastBuild.number,
          "result": job.lastBuild.result,
          "timestamp": job.lastBuild.timestamp
        })

output:
  kafka_franz:
    seed_brokers: ["redpanda:9092"]
    topic: ci-events
```

```bash
# 파이프라인 생성 — 인스턴스별 ID로 등록
curl -X POST http://redpanda-connect:4195/streams/jenkins-prod-01 \
  -H "Content-Type: application/x-yaml" \
  -d @jenkins-pipeline-template.yaml

# 두 번째 인스턴스도 같은 템플릿으로 등록
curl -X POST http://redpanda-connect:4195/streams/jenkins-staging-01 \
  -H "Content-Type: application/x-yaml" \
  -d @jenkins-pipeline-template.yaml

# 인스턴스 제거
curl -X DELETE http://redpanda-connect:4195/streams/jenkins-prod-01
```

Jenkins 인스턴스가 몇 대든 동일한 템플릿으로 파이프라인을 생성할 수 있고, Connect 프로세스를 재시작할 필요가 없다. 백엔드(Java/Go/Python 등)에서는 위 curl과 동일한 HTTP 호출을 코드로 수행하면 된다.

#### 파이프라인 영속성

REST API로 생성한 파이프라인은 **메모리에만 존재**한다. Connect 프로세스가 중단(크래시, 재시작, 컨테이너 재생성)되면 REST API로 등록한 파이프라인은 사라진다. 이 점이 YAML 파일 기반 디렉토리 모드와의 가장 큰 차이다.

| 방식 | 재시작 후 파이프라인 | 적합한 용도 |
|------|:---:|------|
| 디렉토리 모드 (`streams *.yaml`) | ✅ 유지됨 (파일이 곧 설정) | 고정 파이프라인, GitOps |
| REST API 동적 생성 | ❌ 소멸 (메모리 전용) | 동적 연계, 임시 파이프라인 |
| 혼합 (`streams *.yaml` + REST API) | 파일 파이프라인만 유지 | 기본 파이프라인 + 동적 확장 |

프로덕션에서 REST API 파이프라인의 내구성이 필요하면 다음 전략을 사용한다.

1. **디렉토리 기반 영속화**: 백엔드가 파이프라인 YAML을 파일로 저장하고, Connect가 해당 디렉토리를 로드하도록 구성한다. REST API 대신 파일 시스템이 진실의 원천(source of truth)이 된다.
2. **시작 스크립트 재생성**: Connect 시작 시 Init Container나 entrypoint 스크립트에서 DB/API에 저장된 파이프라인 목록을 읽어 REST API로 재등록한다.
3. **혼합 모드**: 고정 파이프라인은 YAML 파일로, 동적 파이프라인은 REST API로 관리하되, 동적 파이프라인 설정을 외부 저장소(DB, ConfigMap 등)에 백업한다.

#### Streams Mode vs Kafka Connect REST API 비교

| 항목 | Redpanda Connect (Streams Mode) | Kafka Connect |
|------|--------------------------------|---------------|
| API 포트 | 4195 | 8083 |
| 파이프라인 단위 | Stream (input→pipeline→output 전체) | Connector (source 또는 sink 하나) |
| 생성 | `POST /streams/{id}` + YAML body | `POST /connectors` + JSON body |
| 일시정지/재개 | ❌ (삭제 후 재생성) | `PUT /connectors/{name}/pause\|resume` |
| 설정 형식 | YAML 또는 JSON | JSON만 |
| 변환 로직 포함 | ✅ (pipeline.processors) | ❌ (SMT로 제한적 변환) |
| 분산 모드 | 단일 프로세스 | 클러스터 기반 자동 분산 |
| 플러그인 관리 | 불필요 (단일 바이너리에 내장) | JAR 설치 + Worker 재시작 |

### YAML 기본 문법

파이프라인 YAML은 `input` → `pipeline` → `output` 세 블록으로 구성된다. **세 블록 모두 필수**이며, 하나라도 빠지면 파이프라인이 시작되지 않는다.

```yaml
input:
  http_server:
    path: /webhook
    allowed_verbs: [POST]

pipeline:
  processors:
    - mapping: |
        root = this
        root.received_at = now()

output:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topic: webhook-events
```

#### Input

데이터를 어디서 가져올지 정의한다. 하나의 파이프라인에 Input은 **하나만** 선언할 수 있다. 여러 소스를 동시에 소비하려면 `broker`로 조합한다.

| 조합 | 역할 |
|------|------|
| `broker` | 여러 Input을 동시에 소비 (fan-in) |
| `sequence` | 여러 Input을 순차적으로 소비 |
| `read_until` | 조건 충족 시 Input 중단 |

```yaml
# broker: 여러 소스를 동시에 소비 (fan-in)
input:
  broker:
    inputs:
      - kafka_franz:
          seed_brokers: ["localhost:19092"]
          topics: ["orders"]
          consumer_group: my-group
      - http_server:
          path: /webhook

# sequence: 첫 번째 소진 → 두 번째로 전환
input:
  sequence:
    inputs:
      - csv:
          paths: ["/data/backfill.csv"]
      - kafka_franz:
          seed_brokers: ["localhost:19092"]
          topics: ["orders"]

# read_until: 조건 충족 시 소비 중단
input:
  read_until:
    input:
      kafka_franz:
        seed_brokers: ["localhost:19092"]
        topics: ["commands"]
    check: this.type == "SHUTDOWN"
```

| Input | 용도 | 핵심 설정 |
|-------|------|-----------|
| `http_server` | 웹훅 수신 (push) | `path`, `allowed_verbs`, `timeout` |
| `kafka_franz` | Kafka/Redpanda 토픽 소비 | `seed_brokers`, `topics`, `consumer_group` |
| `sql_select` | DB 테이블 폴링 (pull) | `dsn`, `table`, `cursor_columns`, `poll_interval` |
| `generate` | 테스트용 더미 데이터 생성 | `mapping`, `interval` |

```yaml
# kafka_franz: Kafka/Redpanda 토픽 소비
input:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topics: ["orders"]
    consumer_group: my-group
    start_from_oldest: false

# http_server: 웹훅 수신 (push 방식)
input:
  http_server:
    path: /api/events
    allowed_verbs: [POST, PUT]
    timeout: 5s

# sql_select: DB 폴링 (pull 방식, CDC 대안)
input:
  sql_select:
    driver: postgres
    dsn: "postgres://user:pass@localhost:5432/mydb"
    table: outbox_events
    columns: [id, payload, created_at]
    where: processed = false
    cursor_columns: [id]
    poll_interval: 5s

# generate: 테스트용 더미 데이터 생성
input:
  generate:
    interval: 1s
    mapping: |
      root.id = uuid_v4()
      root.amount = random_int(min: 100, max: 10000)
      root.status = "PENDING"
      root.created_at = now()
```

#### Pipeline

메시지를 변환·필터링하는 Processor 체인이다. `processors` 배열 순서대로 실행되며, 각 Processor의 출력이 다음 Processor의 입력이 된다.

| Processor | 용도 |
|-----------|------|
| `mapping` | Bloblang으로 필드 변환·추가·삭제 |
| `catch` | 이전 Processor 에러 시 에러 정보 첨부 |
| `log` | 디버깅용 로그 출력 |
| `switch` | 조건별 다른 Processor 적용 |
| `branch` | 메시지 복사 → 별도 처리 → 결과 병합 |
| `dedupe` | 중복 메시지 제거 |

```yaml
# 기본: 변환 → 필터링 → 에러 핸들링
pipeline:
  threads: 4
  processors:
    - mapping: |
        root = this.parse_json()
        root.processed_at = now()

    - mapping: |
        root = if this.status == "CANCELLED" { deleted() } else { this }

    - catch:
        - mapping: |
            root = this
            root.error = error()
```

```yaml
# switch: 메시지 타입별 다른 변환 적용
pipeline:
  processors:
    - switch:
        - check: this.type == "ORDER"
          processors:
            - mapping: |
                root.total = this.items.map_each(i -> i.price * i.qty).sum()

        - check: this.type == "REFUND"
          processors:
            - mapping: |
                root.refund_amount = this.amount * -1

        - processors:                  # default
            - mapping: |
                root.type = "UNKNOWN"
```

```yaml
# branch: 외부 API 조회 결과를 메시지에 병합
pipeline:
  processors:
    - branch:
        request_map: |
          root = this.user_id
        processors:
          - http:
              url: "http://user-service/api/users/${! content()}"
              verb: GET
        result_map: |
          root.user_name = this.name

# dedupe: 캐시 기반 중복 제거
pipeline:
  processors:
    - dedupe:
        cache: dedup_cache
        key: ${! this.event_id }
        drop_on_err: false

cache_resources:
  - label: dedup_cache
    memory:
      default_ttl: 1h
```

#### Output

변환된 메시지를 어디로 보낼지 정의한다. 단독 사용하거나, **wrapper**로 감싸서 제어 로직을 추가할 수 있다.

| Output | 용도 | 핵심 설정 |
|--------|------|-----------|
| `kafka_franz` | Kafka/Redpanda 토픽에 발행 | `seed_brokers`, `topic`, `key`, `compression` |
| `sql_insert` | DB 테이블에 INSERT | `driver`, `dsn`, `table`, `columns` |
| `sql_raw` | 임의 SQL 실행 (UPDATE/DELETE) | `driver`, `dsn`, `query` |
| `http_client` | REST API 호출 | `url`, `verb`, `headers` |
| `sync_response` | `http_server` Input에 동기 응답 반환 | — (본문 없음, 처리 결과가 HTTP 응답 바디가 됨) |

```yaml
# kafka_franz: Kafka/Redpanda 토픽에 발행
output:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topic: clean-orders
    key: ${! this.order_id }
    compression: snappy
    max_in_flight: 1
    idempotent_write: true
    batching:
      count: 100
      period: 100ms

# sql_insert: DB 테이블에 INSERT
output:
  sql_insert:
    driver: postgres
    dsn: "postgres://user:pass@localhost:5432/mydb"
    table: processed_orders
    columns: [order_id, total, status, processed_at]
    args_mapping: |
      root = [
        this.order_id,
        this.total,
        this.status,
        now()
      ]

# http_client: REST API 호출
output:
  http_client:
    url: "http://notification-service/api/notify"
    verb: POST
    headers:
      Content-Type: application/json
      Authorization: "Bearer ${SECRET_TOKEN}"
    max_in_flight: 4
    timeout: 10s
    retry_period: 1s
    max_retry_backoff: 30s

# sync_response: http_server Input에 처리 결과를 동기 응답으로 반환
# (input이 http_server일 때만 의미 있음)
input:
  http_server:
    path: /api/transform
    allowed_verbs: [POST]
    timeout: 10s

pipeline:
  processors:
    - mapping: |
        root = this
        root.processed_at = now()
        root.status = "OK"

output:
  sync_response: {}   # 처리 결과가 그대로 HTTP 응답 바디로 전송됨
```

> **주의 — sync_response의 응답 지연 위험**
>
> 공식 문서 원문: *"Due to delivery guarantees, the response is not sent until all downstream processing and acknowledgements are complete."*
>
> 즉, HTTP 클라이언트는 파이프라인의 **모든 downstream 처리가 완료된 후에야** 응답을 받는다. 이 때문에 다음 상황에서 응답 지연이 사용자에게 직접 전파된다.
>
> - **fan-out이 포함된 경우**: 가장 느린 output이 전체 응답 시간을 결정한다. 감사 로그 적재가 2초 걸리면 HTTP 응답도 2초 지연된다.
> - **느린 sink가 있는 경우**: DB INSERT나 외부 API 호출이 downstream에 있으면, 그 latency가 사용자 응답 시간에 포함된다.
> - **타임아웃 범위 확장**: 애플리케이션 레벨의 타임아웃이 아닌 파이프라인 전체로 타임아웃 기준이 늘어난다.
>
> **권장 패턴**:
> - 즉답형 조회(동기 응답이 필요한 경우): fan-out 최소화, downstream을 가볍게 유지
> - 접수형 커맨드(처리 결과를 기다릴 필요 없는 경우): `202 Accepted` 응답 후 상태 조회 API로 분리
> - 외부 프록시를 앞에 두는 경우: 프록시의 timeout budget을 파이프라인 전체 처리 시간 기준으로 엄격히 설정

#### Output Wrapper (중첩 구조)

Output을 **wrapper**로 감싸면 재시도·폴백·라우팅 같은 제어 로직을 추가할 수 있다.

| Wrapper | 역할 |
|---------|------|
| `retry` | 전달 실패 시 지수 백오프로 재시도 |
| `fallback` | 첫 번째 실패 → 두 번째 output으로 전환 |
| `switch` | 메시지 내용에 따라 조건부 라우팅 |
| `broker` | 하나의 메시지를 여러 output에 동시/순차 전달 |

```yaml
# retry: 실패 시 지수 백오프로 재시도
output:
  retry:
    backoff:
      initial_interval: 1s
      max_interval: 10s
    output:
      kafka_franz:
        seed_brokers: ["localhost:19092"]
        topic: my-topic

# fallback: 첫 번째 실패 시 두 번째(DLQ)로 전환
output:
  fallback:
    - kafka_franz:
        topic: orders
    - kafka_franz:
        topic: orders-dlq

# switch: 메시지 내용에 따라 조건부 라우팅
output:
  switch:
    cases:
      - check: this.priority == "HIGH"
        output:
          kafka_franz:
            topic: orders-high
      - check: this.priority == "LOW"
        output:
          kafka_franz:
            topic: orders-low
      - output:
          kafka_franz:
            topic: orders-normal

# broker: 하나의 메시지를 여러 output에 동시 전달 (fan-out)
output:
  broker:
    pattern: fan_out                   # fan_out | fan_out_sequential | round_robin
    outputs:
      - kafka_franz:
          topic: orders-stream
      - sql_insert:
          driver: postgres
          dsn: "postgres://user:pass@localhost:5432/mydb"
          table: orders
          columns: [id, payload]
          args_mapping: "root = [this.id, this.string()]"
```

> **주의 — fan_out 백프레셔 장애 전파 위험**
>
> 공식 문서 원문: *"If an output applies back pressure it will block all subsequent messages."*
> 공식 문서 원문: *"If an output fails to send a message it will be retried continuously until completion or service shut down."*
>
> 즉, `fan_out`의 output 중 하나라도 느려지거나 실패하면 **전체 파이프라인이 멈추거나 재시도 루프에 빠진다**. 예를 들어 감사 로그를 적재하는 output이 DB 부하로 응답이 느려지면, 메인 Kafka 발행도 함께 차단된다.
>
> 특히 `sync_response`와 함께 사용할 때 위험이 커진다. 사용자 응답 경로와 부가 출력(감사 로그, 검색 인덱스 갱신 등)을 같은 `fan_out`에 묶으면, 부가 출력의 장애가 사용자 응답 지연으로 직접 전파된다.
>
> **권장 패턴**:
> - 사용자 응답에 직접 영향을 주는 output과 부가 출력(감사, 인덱스 등)은 **별도 비동기 파이프라인**으로 분리
> - 부가 출력이 필요하면 Kafka 토픽을 중간 버퍼로 두고, 별도 파이프라인이 해당 토픽을 소비하도록 설계
> - 반드시 같은 파이프라인에 묶어야 한다면 `fan_out_sequential` 대신 `fan_out`을 사용하고, 부가 출력에 `retry` wrapper로 격리

wrapper는 중첩 조합도 가능하다. `retry` 안에 `fallback`을 넣으면, 재시도를 모두 소진한 뒤 DLQ로 보내는 파이프라인이 된다.

```yaml
# 중첩 조합: retry 소진 → fallback → DLQ
output:
  fallback:
    - retry:
        max_retries: 3
        backoff:
          initial_interval: 500ms
          max_interval: 5s
        output:
          http_client:
            url: "http://api/orders"
            verb: POST
    - kafka_franz:
        seed_brokers: ["localhost:19092"]
        topic: orders-dlq
```

#### Output Resources (공유 Output)

`output_resources`는 Output을 이름으로 정의해두고, 파이프라인 여러 곳에서 `resource` 라벨로 참조하는 기능이다. `cache_resources`, `rate_limit_resources`와 같은 계열의 리소스 시스템이다.

DLQ Output처럼 여러 분기에서 동일한 Output을 사용해야 할 때, 설정을 중복 작성하지 않고 한곳에서 관리할 수 있다.

```yaml
pipeline:
  processors:
    - switch:
        - check: 'error().contains("status 4")'
          processors:
            - resource: "dlq_output"     # 이름으로 참조
        - check: 'error().contains("status 5")'
          processors:
            - retry:
                max_retries: 5
                processors:
                  - http:
                      url: "http://api/webhook"
                      verb: POST
            - catch:
                - resource: "dlq_output"  # 같은 Output 재사용

output:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topic: "success-results"

# Output을 이름으로 등록
output_resources:
  - label: dlq_output
    kafka_franz:
      seed_brokers: ["localhost:19092"]
      topic: "dlq-api-sink"
```

`resource`로 참조된 Output은 메인 `output`과 독립적으로 동작한다. 프로세서 안에서 `resource: "dlq_output"`을 호출하면 해당 메시지는 메인 `output`을 거치지 않고 직접 DLQ 토픽에 발행된다.

> 에러 처리에서 `output_resources`를 활용한 구체적인 파이프라인 예제는 [06-error-recovery.md §1](./06-error-recovery.md)을 참조한다.

---

## Bloblang 스크립팅 언어

Bloblang은 Redpanda Connect 전용 데이터 변환 언어다. JSON 데이터를 쉽게 변환할 수 있도록 설계되었으며, 파이프라인 Processor의 `mapping` 블록에서 사용된다.

### 기본 문법

```bloblang
# 1. 필드 접근
root.user_id = this.user.id

# 2. 필드 추가
root.timestamp = now()

# 3. 조건문
root.status = if this.amount > 100 {
  "VIP"
} else {
  "NORMAL"
}

# 4. 문자열 변환
root.email = this.email.lowercase()

# 5. 배열 필터링
root.active_users = this.users.filter(u -> u.active == true)

# 6. 매핑
root.product_names = this.products.map(p -> p.name)

# 7. JSON 파싱
root = this.payload.parse_json()

# 8. 타입 변환
root.price = this.price.number()
```

### 내장 함수

| 함수 | 설명 | 예시 |
|------|------|------|
| `now()` | 현재 타임스탬프 | `root.timestamp = now()` |
| `uuid_v4()` | UUID 생성 | `root.id = uuid_v4()` |
| `lowercase()` | 소문자 변환 | `this.email.lowercase()` |
| `uppercase()` | 대문자 변환 | `this.name.uppercase()` |
| `parse_json()` | JSON 파싱 | `this.payload.parse_json()` |
| `format_json()` | JSON 직렬화 | `this.format_json()` |
| `hash("sha256")` | 해싱 | `this.password.hash("sha256")` |
| `trim()` | 공백 제거 | `this.name.trim()` |

### 실전 예시: 사용자 정보 변환

**입력**:
```json
{
  "USER_ID": "12345",
  "EMAIL": "USER@EXAMPLE.COM",
  "created": "2026-02-06T10:30:00Z",
  "metadata": "{\"tier\":\"premium\"}"
}
```

**Bloblang**:
```bloblang
root.user_id = this.USER_ID
root.email = this.EMAIL.lowercase()
root.created_at = this.created.ts_parse("2006-01-02T15:04:05Z").ts_unix()
root.tier = this.metadata.parse_json().tier
root.is_premium = this.metadata.parse_json().tier == "premium"
```

**출력**:
```json
{
  "user_id": "12345",
  "email": "user@example.com",
  "created_at": 1738802400,
  "tier": "premium",
  "is_premium": true
}
```

---

## 실습 시나리오 1: HTTP Webhook → Redpanda

외부 시스템(GitHub, Stripe 등)에서 발생하는 웹훅 이벤트를 Redpanda 토픽으로 수집한다.

**요구사항**: HTTP POST 웹훅 수신 → 수신 타임스탬프 추가 → `webhook-events` 토픽 저장 → 에러 시 재시도

### 파이프라인 설정 (webhook-to-redpanda.yaml)

첫 번째 Processor는 수신 타임스탬프와 고유 ID를 추가한다. 두 번째 Processor는 `event_type` 필드의 존재 여부를 검증하여, 없으면 `throw`로 에러를 발생시킨다. Output의 `key` 설정은 `event_type` 값을 파티션 키로 사용한다.

```yaml
input:
  http_server:
    path: /webhook
    allowed_verbs: [POST]
    timeout: 30s
    cors:
      enabled: true
      allowed_origins: ["*"]

pipeline:
  processors:
    - mapping: |
        root = this
        root.received_at = now().ts_format("2006-01-02T15:04:05Z07:00")
        root.event_id = uuid_v4()
        root.source = "webhook-server"

    - mapping: |
        root = if !this.exists("event_type") {
          throw("Missing required field: event_type")
        } else {
          this
        }

output:
  retry:
    backoff:
      initial_interval: 1s
      max_interval: 10s
      max_elapsed_time: 1m
    output:
      kafka_franz:
        seed_brokers:
          - localhost:19092
        topic: webhook-events
        key: ${! this.event_type }
        compression: snappy
        max_in_flight: 1
        idempotent_write: true
        batching:
          count: 100
          period: 100ms

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9090

logger:
  level: INFO
  format: json
```

### 실행 및 테스트

```bash
# 실행
rpk connect run webhook-to-redpanda.yaml

# 웹훅 POST 요청
curl -X POST http://localhost:4195/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "order.created",
    "order_id": "ORD-001",
    "amount": 50000
  }'

# 토픽 확인
rpk topic consume webhook-events --format json
```

**출력**:
```json
{
  "event_type": "order.created",
  "order_id": "ORD-001",
  "amount": 50000,
  "received_at": "2026-02-06T10:30:15+09:00",
  "event_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "source": "webhook-server"
}
```

---

## 실습 시나리오 2: Redpanda → PostgreSQL

Redpanda 토픽의 주문 이벤트를 PostgreSQL 데이터베이스에 저장한다. DB INSERT 실패 시 메시지를 DLQ로 안전하게 보관한다.

**요구사항**: `orders` 토픽 구독 → JSON 파싱 후 DB INSERT → 중복 방지 (멱등성) → 에러 시 DLQ

### PostgreSQL 테이블 생성

```sql
CREATE TABLE orders (
    id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

### 파이프라인 설정 (redpanda-to-postgres.yaml)

Output에 `fallback`을 사용하는 것이 이 파이프라인의 핵심이다. `sql_insert`가 실패하면 DLQ 토픽으로 메시지가 전달된다. `ON CONFLICT DO UPDATE` 구문으로 멱등성을 보장한다.

```yaml
input:
  kafka_franz:
    seed_brokers:
      - localhost:19092
    topics:
      - orders
    consumer_group: connect-postgres-sink
    start_from_oldest: false
    checkpoint_limit: 1

pipeline:
  processors:
    - mapping: |
        root = this.parse_json()
        root.processed_at = now().ts_format("2006-01-02 15:04:05")

    - mapping: |
        root = if ![
          this.exists("id"),
          this.exists("customer_id"),
          this.exists("amount"),
          this.exists("status")
        ].all() {
          throw("Missing required fields")
        } else {
          this
        }

output:
  fallback:
    - sql_insert:
        driver: postgres
        dsn: "postgres://user:password@localhost:5432/orders?sslmode=disable"
        table: orders
        columns:
          - id
          - customer_id
          - amount
          - status
          - created_at
          - processed_at
        args_mapping: |
          root = [
            this.id,
            this.customer_id,
            this.amount,
            this.status,
            this.created_at,
            this.processed_at
          ]
        suffix: |
          ON CONFLICT (id) DO UPDATE SET
            amount = EXCLUDED.amount,
            status = EXCLUDED.status,
            processed_at = EXCLUDED.processed_at
        batching:
          count: 100
          period: 1s

    - kafka_franz:
        seed_brokers:
          - localhost:19092
        topic: orders-dlq
        key: ${! this.id }

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9091

logger:
  level: INFO
  format: json
```

### 실행 및 테스트

```bash
# PostgreSQL 시작
docker run -d --name postgres \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=orders \
  -p 5432:5432 postgres:16

docker exec -i postgres psql -U user -d orders < schema.sql
rpk connect run redpanda-to-postgres.yaml

# 주문 이벤트 발행
rpk topic produce orders --format json << EOF
{"id":"ORD-001","customer_id":"CUST-12345","amount":50000,"status":"PENDING","created_at":"2026-02-06T10:30:00Z"}
EOF

# PostgreSQL 확인
docker exec -it postgres psql -U user -d orders -c "SELECT * FROM orders;"
```

---

## 실습 시나리오 3: Redpanda → Redpanda (변환)

원본 주문 이벤트 토픽(`raw-orders`)에서 데이터를 정제하여 클린 토픽(`clean-orders`)으로 전송한다.

**요구사항**: 취소 주문 필터링 → 소액(1000원 미만) 필터링 → 필드 정규화 → 중복 제거 (로그 컴팩션)

### 파이프라인 설정 (redpanda-to-redpanda.yaml)

`deleted()`를 반환하면 해당 메시지는 이후 단계를 거치지 않고 파이프라인에서 제거된다. Output의 `key`를 `order_id`로 지정하면 로그 컴팩션으로 중복 제거 효과를 얻는다.

```yaml
input:
  kafka_franz:
    seed_brokers:
      - localhost:19092
    topics:
      - raw-orders
    consumer_group: order-cleaner
    start_from_oldest: false

pipeline:
  processors:
    - mapping: |
        root = this.parse_json()

    - mapping: |
        root = if this.status == "CANCELLED" {
          deleted()
        } else {
          this
        }

    - mapping: |
        root = if this.amount < 1000 {
          deleted()
        } else {
          this
        }

    - mapping: |
        root.order_id = this.orderId.or(this.order_id).or(this.OrderID)
        root.customer_id = this.customerId.or(this.customer_id)
        root.amount = this.amount.number()
        root.status = this.status.uppercase()
        root.created_at = if this.createdAt.type() == "string" {
          this.createdAt.ts_parse("2006-01-02T15:04:05Z")
        } else {
          this.created_at
        }.ts_format("2006-01-02T15:04:05Z")
        root.cleaned_at = now().ts_format("2006-01-02T15:04:05Z")
        root.version = "v1"

    - mapping: |
        root = this.without(
          "internal_metadata",
          "debug_info",
          "raw_payload"
        )

output:
  kafka_franz:
    seed_brokers:
      - localhost:19092
    topic: clean-orders
    key: ${! this.order_id }
    compression: snappy
    metadata:
      include_patterns:
        - ".*"
    headers:
      source: "order-cleaner"
      version: "1.0"

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9092

logger:
  level: INFO
  format: json
```

### 테스트

```bash
rpk connect run redpanda-to-redpanda.yaml

# 원본 토픽에 다양한 형식의 주문 발행
rpk topic produce raw-orders << 'EOF'
{"orderId":"ORD-001","customerId":"CUST-1","amount":50000,"status":"PENDING","createdAt":"2026-02-06T10:30:00Z"}
{"OrderID":"ORD-002","customerId":"CUST-2","amount":500,"status":"PENDING","createdAt":"2026-02-06T10:31:00Z"}
{"order_id":"ORD-003","customer_id":"CUST-3","amount":30000,"status":"CANCELLED","createdAt":"2026-02-06T10:32:00Z"}
EOF

# 정제된 토픽 확인 (ORD-001만 출력됨)
rpk topic consume clean-orders --format json
```

---

## 실습 시나리오 4: Redpanda ↔ Jenkins (Source + Sink)

Jenkins를 중심으로 **Sink**(배포 요청 토픽 → Jenkins 파이프라인 트리거)와 **Source**(빌드 결과 → 토픽)를 모두 구현한다.

두 파이프라인은 독립적으로 실행된다. Sink 파이프라인이 Jenkins를 트리거하고, Jenkins는 빌드 완료 시 Webhook으로 Source 파이프라인에 결과를 전달한다.

### Part A: Sink — 배포 요청 → Jenkins 파이프라인 트리거

**파이프라인 설정 (deploy-trigger.yaml)**:

```yaml
input:
  kafka_franz:
    seed_brokers:
      - localhost:19092
    topics:
      - deploy-requests
    consumer_group: connect-jenkins-trigger

pipeline:
  processors:
    - mapping: |
        root.job_path = this.job_name.replace("/", "/job/")
        root.parameters = {
          "BRANCH": this.branch.or("main"),
          "ENVIRONMENT": this.environment.or("staging"),
          "VERSION": this.version
        }

output:
  http_client:
    url: 'http://jenkins:8080/job/${! this.job_path }/buildWithParameters'
    verb: POST
    headers:
      Content-Type: application/x-www-form-urlencoded
    basic_auth:
      enabled: true
      username: "${JENKINS_USER}"
      password: "${JENKINS_API_TOKEN}"
    retry_period: 5s
    max_retry_backoff: 30s
    retries: 3

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9093

logger:
  level: INFO
  format: json
```

**테스트**:

```bash
rpk topic produce deploy-requests --format json << 'EOF'
{
  "job_name": "order-service",
  "branch": "main",
  "environment": "staging",
  "version": "1.2.3"
}
EOF
```

### Part B: Source — Jenkins 빌드 결과 → Redpanda

Jenkins에서 빌드 이벤트를 Redpanda에 적재하려면, Jenkinsfile의 `post` 블록에서 빌드 완료 시 Webhook을 호출한다.

**Jenkinsfile 예시**:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh './gradlew build' }
        }
        stage('Test') {
            steps { sh './gradlew test' }
        }
    }
    post {
        always {
            script {
                def payload = [
                    event_type  : "jenkins.build",
                    job_name    : env.JOB_NAME,
                    build_number: env.BUILD_NUMBER as int,
                    status      : currentBuild.currentResult,
                    duration_ms : currentBuild.duration,
                    branch      : env.GIT_BRANCH,
                    commit      : env.GIT_COMMIT,
                    timestamp   : new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'",
                                                     TimeZone.getTimeZone('UTC'))
                ]
                httpRequest(
                    url: 'http://redpanda-connect:4195/ci/jenkins',
                    httpMode: 'POST',
                    contentType: 'APPLICATION_JSON',
                    requestBody: groovy.json.JsonOutput.toJson(payload)
                )
            }
        }
    }
}
```

**Redpanda Connect Source 파이프라인 (ci-events.yaml)**:

```yaml
input:
  http_server:
    path: /ci/jenkins
    allowed_verbs: [POST]
    timeout: 30s

pipeline:
  processors:
    - mapping: |
        root.event_id = uuid_v4()
        root.received_at = now()
        root.source = "jenkins"
        root.job_name = this.job_name
        root.build_id = this.build_number.string()
        root.status = this.status
        root.branch = this.branch
        root.commit = this.commit.or("")
        root.duration_ms = this.duration_ms.or(0)

output:
  kafka_franz:
    seed_brokers:
      - localhost:19092
    topic: ci-events
    key: '${! this.job_name }'
    compression: snappy

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9094

logger:
  level: INFO
  format: json
```

**테스트**:

```bash
rpk connect run ci-events.yaml

curl -X POST http://localhost:4195/ci/jenkins \
  -H "Content-Type: application/json" \
  -d '{
    "job_name": "order-service/main",
    "build_number": 142,
    "status": "SUCCESS",
    "duration_ms": 45200,
    "branch": "main",
    "commit": "abc123f"
  }'

rpk topic consume ci-events --format json
```

### 활용 사례 (다운스트림)

- **DORA 메트릭 계산**: 배포 빈도, 리드 타임, 변경 실패율, 복구 시간을 `ci-events` 토픽에서 집계한다.
- **빌드 실패 알림**: `ci-events` 토픽에서 `status == "FAILURE"` 이벤트를 Slack/Teams로 실시간 전달한다. `switch` output으로 상태별 라우팅도 가능하다.
- **변경 이력 감사 로그**: 누가 언제 어떤 브랜치에 배포했는지를 이벤트 스트림으로 보관한다.

---

## 실습 시나리오 5: MariaDB CDC → Redpanda

CDC(Change Data Capture)는 데이터베이스의 변경 사항(INSERT, UPDATE, DELETE)을 실시간 이벤트 스트림으로 캡처하는 기술이다. 구현 방식은 크게 두 가지다.

| 방식 | 원리 | 지연 | DB 부하 | DELETE 감지 |
|------|------|------|---------|------------|
| **로그 기반** (binlog) | 트랜잭션 로그를 직접 읽음 | ms 단위 | 매우 낮음 | 지원 |
| **폴링 기반** (sql_select) | 주기적 SELECT 쿼리 | 초~분 단위 | 중간 | 미지원 (soft delete 필요) |

> **참조**: CDC 이론 상세는 [01-source-sink-patterns.md §3](./01-source-sink-patterns.md), Debezium PostgreSQL CDC는 [02-kafka-connect.md §5](./02-kafka-connect.md)를 참조한다.

### MariaDB 준비

binlog 형식은 반드시 `ROW`여야 각 행의 변경 전후 값을 온전히 캡처할 수 있다.

**Docker Compose MariaDB 서비스**:

```yaml
  mariadb:
    image: mariadb:11
    container_name: mariadb-cdc
    environment:
      MARIADB_ROOT_PASSWORD: rootpass
      MARIADB_DATABASE: orders_db
      MARIADB_USER: app_user
      MARIADB_PASSWORD: app_pass
    command:
      - --server-id=1
      - --log-bin=mariadb-bin
      - --binlog-format=ROW
      - --binlog-row-image=FULL
      - --expire-logs-days=3
    ports:
      - "3306:3306"
```

**CDC 전용 사용자 생성** (binlog 기반 CDC 사용 시):

```sql
CREATE USER 'cdc_user'@'%' IDENTIFIED BY 'cdc_pass';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'cdc_user'@'%';
FLUSH PRIVILEGES;
```

**테스트 테이블**:

```sql
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    amount INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_orders_updated (updated_at)
) ENGINE=InnoDB;
```

### Redpanda Connect 폴링 CDC 파이프라인

`sql_select` 입력을 사용한 폴링 방식이다. `updated_at` 컬럼을 커서로 사용하여 마지막 폴링 이후 변경된 행만 가져온다.

**파이프라인 설정 (mariadb-cdc.yaml)**:

```yaml
input:
  sql_select:
    driver: mysql
    dsn: "app_user:app_pass@tcp(localhost:3306)/orders_db"
    table: orders
    columns:
      - id
      - customer_id
      - amount
      - status
      - created_at
      - updated_at
    where: "updated_at > ?"
    cursor_columns:
      - updated_at
    init_statement: |
      SET time_zone = '+00:00'

pipeline:
  processors:
    - mapping: |
        root.event_id = uuid_v4()
        root.event_type = "changed"    # DELETE 감지 불가
        root.source = "mariadb.orders_db.orders"
        root.timestamp = now()
        root.payload.id = this.id
        root.payload.customer_id = this.customer_id
        root.payload.amount = this.amount
        root.payload.status = this.status
        root.payload.created_at = this.created_at
        root.payload.updated_at = this.updated_at

output:
  kafka_franz:
    seed_brokers:
      - localhost:19092
    topic: cdc.orders
    key: '${! this.payload.id }'
    compression: snappy
    max_in_flight: 1

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9095

logger:
  level: INFO
  format: json
```

`cursor_columns`에 `updated_at`을 지정하면 Redpanda Connect가 마지막으로 읽은 타임스탬프를 기억하여 다음 폴링에서는 그 이후의 변경만 조회한다. DELETE 감지가 필요하면 soft delete(`deleted_at` 컬럼)를 사용하거나, Debezium을 고려해야 한다.

### Debezium vs Redpanda Connect 폴링 비교

| 항목 | Debezium (Kafka Connect) | Redpanda Connect (sql_select) |
|------|--------------------------|-------------------------------|
| **CDC 방식** | binlog 스트림 (실시간) | 주기적 SELECT 쿼리 |
| **배포** | JVM Worker 클러스터 | 단일 Go 바이너리 (20MB) |
| **설정** | JSON (REST API) | YAML 파일 |
| **변환** | SMT (제한적, 체인) | Bloblang (유연, 스크립팅) |
| **DELETE 감지** | 지원 (tombstone 이벤트) | 미지원 (soft delete 필요) |
| **지연시간** | 밀리초 | 폴링 주기 (초~분) |
| **적합 환경** | 대규모 운영, 실시간 필수 | 경량 PoC, 준실시간 허용 |

### 실행 및 테스트

```bash
docker compose up -d mariadb redpanda
docker exec -i mariadb-cdc mariadb -uapp_user -papp_pass orders_db < schema.sql
rpk connect run mariadb-cdc.yaml

# 데이터 변경 테스트
docker exec -i mariadb-cdc mariadb -uapp_user -papp_pass orders_db <<'SQL'
INSERT INTO orders (customer_id, amount, status) VALUES ('CUST-001', 50000, 'PENDING');
UPDATE orders SET status = 'CONFIRMED' WHERE customer_id = 'CUST-001';
SQL

rpk topic consume cdc.orders --format json
```

**출력**:
```json
{
  "event_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "event_type": "changed",
  "source": "mariadb.orders_db.orders",
  "timestamp": "2026-02-25T10:30:15Z",
  "payload": {
    "id": 1,
    "customer_id": "CUST-001",
    "amount": 50000,
    "status": "CONFIRMED",
    "created_at": "2026-02-25T10:30:00Z",
    "updated_at": "2026-02-25T10:30:10Z"
  }
}
```

---

## 실습 시나리오 6: Transactional Outbox/Inbox → Redpanda Connect

DB 저장과 메시지 발행을 원자적으로 처리하지 않으면 데이터 불일치가 발생한다. Transactional Outbox 패턴은 비즈니스 데이터와 이벤트를 같은 DB 트랜잭션으로 저장하고, 별도 Relay가 이벤트를 브로커로 전달한다. 여기서는 Redpanda Connect를 Outbox Relay로 활용한다.

> **참조**: Outbox/Inbox 이론(원자성 문제, CDC vs Relay 전달 방식, Inbox 멱등성, Debezium EventRouter)은 [09-transactional-messaging.md](../../../../02_Architecture/01-event-driven/learning/09-transactional-messaging.md)를 참조한다.

### Step 1: Outbox 테이블 생성 (MariaDB)

```sql
CREATE TABLE outbox_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    aggregate_type VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload JSON NOT NULL,
    topic VARCHAR(255) NOT NULL,
    created_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
    published_at TIMESTAMP(6) NULL,
    INDEX idx_outbox_unpublished (published_at, created_at)
) ENGINE=InnoDB;
```

`published_at`이 NULL인 행이 아직 발행되지 않은 이벤트다. Relay가 이 행을 읽어 Redpanda에 발행한 뒤 타임스탬프를 기록한다.

### Step 2: 애플리케이션에서 같은 트랜잭션으로 Outbox 기록

```java
@Transactional
public void createOrder(OrderRequest request) {
    Order order = orderRepository.save(new Order(request));

    OutboxEvent event = OutboxEvent.builder()
        .aggregateType("Order")
        .aggregateId(order.getId().toString())
        .eventType("OrderCreated")
        .topic("order.events")
        .payload(objectMapper.writeValueAsString(order))
        .build();
    outboxRepository.save(event);
    // 트랜잭션 커밋 시 둘 다 원자적으로 저장됨
}
```

### Step 3: Redpanda Connect Outbox Relay 파이프라인

`sql_select`로 미발행 이벤트를 폴링하고, `fan_out_sequential`로 Kafka 발행 후 published 마킹을 순차 실행한다. Kafka 발행이 성공한 후에만 마킹하므로, 실패 시 다음 폴링에서 자동 재시도된다.

#### sql_select 폴링 동작 원리

`sql_select`는 커서 기반 증분 폴링으로 동작한다. `cursor_columns`에 지정한 컬럼 기준으로 마지막 읽은 위치 이후의 행만 조회한다.

```sql
-- 첫 번째 폴링 (커서 없음)
SELECT id, aggregate_type, ... FROM outbox_events
WHERE published_at IS NULL
ORDER BY id ASC;

-- 두 번째 폴링 (커서 = 마지막 읽은 id, 예: 42)
SELECT id, aggregate_type, ... FROM outbox_events
WHERE published_at IS NULL AND id > 42
ORDER BY id ASC;
```

| 조건 | 역할 |
|------|------|
| `published_at IS NULL` | 발행 완료된 이벤트 제외 |
| `id > 커서` | 현재 처리 중인 이벤트 재조회 방지 |

```yaml
input:
  sql_select:
    driver: mysql
    dsn: "app_user:app_pass@tcp(localhost:3306)/orders_db"
    table: outbox_events
    columns:
      - id
      - aggregate_type
      - aggregate_id
      - event_type
      - payload
      - topic
      - created_at
    where: "published_at IS NULL"
    cursor_columns:
      - id

pipeline:
  processors:
    - mapping: |
        let topic = this.topic
        let payload = this.payload.parse_json()
        root = $payload
        meta topic = $topic
        meta aggregate_type = this.aggregate_type
        meta aggregate_id = this.aggregate_id
        meta event_type = this.event_type
        meta event_id = this.id.string()
        meta created_at = this.created_at

output:
  broker:
    pattern: fan_out_sequential        # 1번 성공 후에만 2번 실행
    outputs:
      - kafka_franz:
          seed_brokers:
            - localhost:19092
          topic: '${! meta("topic") }'
          key: '${! meta("aggregate_id") }'
          metadata:
            include_patterns: [".*"]
          max_in_flight: 1
      - sql_raw:                       # published_at 마킹 (발행 성공 후에만 실행)
          driver: mysql
          dsn: "app_user:app_pass@tcp(localhost:3306)/orders_db"
          query: "UPDATE outbox_events SET published_at = NOW(6) WHERE id = ?"
          args_mapping: 'root = [ meta("event_id").number() ]'

metrics:
  prometheus:
    enabled: true
    path: /metrics
    port: 9096

logger:
  level: INFO
  format: json
```

`fan_out_sequential`의 동작 방식이 핵심이다. 첫 번째 output(`kafka_franz`)이 성공한 후에만 두 번째 output(`sql_raw` published 마킹)을 실행한다.

```
폴링 → 이벤트 읽음 → Kafka 발행 시도
                       ├─ 성공 → published_at = NOW() 마킹 → 다음 이벤트
                       └─ 실패 → 마킹 안 함 → 다음 폴링에서 재시도
```

발행은 되었지만 마킹 전에 프로세스가 죽으면 다음 폴링에서 같은 이벤트를 다시 발행한다. 따라서 소비자 쪽에서 Inbox 패턴으로 중복을 처리해야 한다.

### Step 4: Inbox 패턴 (소비자 멱등성)

**Inbox 테이블**:

```sql
CREATE TABLE inbox_events (
    event_id VARCHAR(255) PRIMARY KEY,
    aggregate_type VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    processed_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
    INDEX idx_inbox_cleanup (processed_at)
) ENGINE=InnoDB;
```

**소비자 구현**:

```java
@KafkaListener(topics = "order.events")
@Transactional
public void handleOrderEvent(ConsumerRecord<String, String> record) {
    String eventId = new String(record.headers().lastHeader("event_id").value());

    if (inboxRepository.existsById(eventId)) {
        log.info("Duplicate event ignored: {}", eventId);
        return;
    }

    // Inbox 기록 + 비즈니스 로직 수행 (같은 트랜잭션)
    inboxRepository.save(new InboxEvent(eventId, "Order", "OrderCreated"));

    OrderEvent event = objectMapper.readValue(record.value(), OrderEvent.class);
    inventoryService.reserveStock(event);
}
```

### Outbox/Inbox 선택 가이드

| 방법 | 장점 | 단점 | 추천 시점 |
|------|------|------|----------|
| **Outbox + Redpanda Connect (Polling)** | 구현 간단, 추가 인프라 불필요 | 폴링 지연 (수초), Outbox 테이블 관리 필요 | Redpanda Connect를 이미 사용 중일 때 |
| **Outbox + Debezium (CDC)** | 실시간 (ms), binlog 기반 | Debezium 인프라 추가 필요 | 실시간 전달이 필수일 때 |
| **Inbox 패턴** | 소비자 멱등성 완전 보장 | 모든 소비자에 적용 필요 | Outbox와 함께 사용 권장 |

> **Debezium Outbox Event Router**: Debezium을 사용하는 경우, 전용 SMT로 Outbox 테이블의 `aggregate_type` 기반 자동 토픽 라우팅이 가능하다. 상세는 [02-kafka-connect.md §5](./02-kafka-connect.md)의 Outbox Event Router를 참조한다.

---

## 에러 처리 전략

> **이동됨**: 에러 처리 전략(retry, DLQ, switch, catch)의 상세 내용은 [06-error-recovery.md](./06-error-recovery.md)로 이동했다.
>
> - `errored()`/`error()` 함수 레퍼런스: [06 §1](./06-error-recovery.md)
> - HTTP 응답 코드별 분기(4xx/5xx): [06 §2](./06-error-recovery.md)
> - Output 래퍼(`retry`, `fallback`, `switch`): [06 §3](./06-error-recovery.md)
> - 재시도 추적과 구조화 로깅(`catch` + `fields_mapping`): [06 §4](./06-error-recovery.md)
> - 장애 복구 런북(오프셋 리셋, DLQ 재처리): [06 §6](./06-error-recovery.md)

---

## Docker Compose 통합

> Redpanda + Kafka Connect + PostgreSQL 통합 환경은 [02-kafka-connect.md §4](./02-kafka-connect.md)를 참조하세요. Redpanda Connect는 단일 바이너리이므로 Docker Compose 없이 `rpk connect run pipeline.yaml`로 실행할 수 있다.

---

## Kubernetes (Helm) 배포

> K8s 환경에서의 Helm 차트 구조, ConfigMap 기반 파이프라인 주입, Ingress/Service 설정, 헬스체크, 배포 명령어는 [05-helm-deployment.md](./05-helm-deployment.md)를 참조한다.

---

## 성능 최적화

### 배치 처리

```yaml
output:
  kafka_franz:
    seed_brokers: ["localhost:19092"]
    topic: orders
    batching:
      count: 1000
      period: 1s
      byte_size: 1MB
```

### 병렬 처리

`pipeline.threads`를 늘리면 Processor를 병렬로 실행하여 CPU 집약적인 변환 작업의 처리량을 향상시킨다.

```yaml
pipeline:
  threads: 4
  processors:
    - mapping: |
        root = this.parse_json()
```

### 버퍼링

```yaml
buffer:
  memory:
    limit: 100MB
```

---

## 모니터링

> **이동됨**: 메트릭, 로깅, 트러블슈팅 상세는 아래 문서로 이동했다.
>
> - Prometheus 메트릭 + 트러블슈팅 흐름도: [04-operations.md §4](./04-operations.md)
> - 구조화 로깅 (`log` + `fields_mapping` + `static_fields`): [06-error-recovery.md §4](./06-error-recovery.md)
> - Promtail + Loki + Grafana 로그 수집: [06-error-recovery.md §5](./06-error-recovery.md)

---

## 실습 체크리스트

- [ ] Redpanda 클러스터 시작
- [ ] PostgreSQL 데이터베이스 시작 및 테이블 생성
- [ ] **시나리오 1**: HTTP Webhook → Redpanda
  - [ ] `webhook-to-redpanda.yaml` 작성 및 실행
  - [ ] curl로 웹훅 POST 테스트
  - [ ] Redpanda 토픽에서 이벤트 확인
- [ ] **시나리오 2**: Redpanda → PostgreSQL
  - [ ] `redpanda-to-postgres.yaml` 작성 및 실행
  - [ ] 이벤트 발행 후 PostgreSQL 테이블 확인
  - [ ] DLQ 동작 확인
- [ ] **시나리오 3**: Redpanda → Redpanda (변환)
  - [ ] `redpanda-to-redpanda.yaml` 작성
  - [ ] 필터링 및 정규화 로직 구현
  - [ ] 정제된 토픽 확인
- [ ] **시나리오 4**: Jenkins Source + Sink
  - [ ] `deploy-trigger.yaml` 작성 (Sink)
  - [ ] `ci-events.yaml` 작성 (Source)
  - [ ] Jenkins 이벤트 시뮬레이션 (curl)
- [ ] **시나리오 5**: MariaDB CDC → Redpanda
  - [ ] MariaDB binlog 활성화 (ROW 형식)
  - [ ] `mariadb-cdc.yaml` 작성 (sql_select 폴링)
  - [ ] INSERT/UPDATE 후 토픽 이벤트 확인
- [ ] **시나리오 6**: Transactional Outbox/Inbox
  - [ ] outbox_events / inbox_events 테이블 생성
  - [ ] Outbox Relay 파이프라인 작성 (fan_out_sequential)
  - [ ] Kafka 발행 → published 마킹 순차 동작 확인
  - [ ] 소비자 멱등성 (Inbox) 테스트
- [ ] Bloblang 함수 실습
- [ ] 에러 처리 테스트
- [ ] Prometheus 메트릭 확인

---

## 다음 단계

- [03-spring-boot-impl.md](./03-spring-boot-impl.md) — Spring Boot에서 Source/Sink 구현 (Outbox 엔티티 포함)
- [01-source-sink-patterns.md](./01-source-sink-patterns.md) — CDC 이론 (§3), Source/Sink 패턴 상세

---

## 참고 자료

- [Redpanda Connect 공식 문서](https://docs.redpanda.com/redpanda-connect/about)
- [Bloblang 언어 레퍼런스](https://docs.redpanda.com/redpanda-connect/guides/bloblang/about)
- [커넥터 목록 (300+)](https://docs.redpanda.com/redpanda-connect/components/inputs/about)
- [에러 처리 가이드](https://docs.redpanda.com/redpanda-connect/configuration/error_handling)
- [성능 튜닝 가이드](https://docs.redpanda.com/redpanda-connect/guides/performance_tuning)
